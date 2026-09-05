# Nemotron-Labs-Diffusion 학습 노트

작성일: 2026-09-05

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [연구 질문과 기여](#연구-질문과-기여)
- [기초 개념과 방법](#기초-개념과-방법)
- [데이터·평가 지표](#데이터평가-지표)
- [주요 결과](#주요-결과)
- [한계와 재현 주의](#한계와-재현-주의)
- [Trillion Labs OCR 접근과의 관계](#trillion-labs-ocr-접근과의-관계)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 원문: [arXiv:2607.05722](https://arxiv.org/abs/2607.05722), DOI `10.48550/arXiv.2607.05722`
- 확인 버전: v1, 2026-07-07
- 저자: Yonggan Fu 외 25명(NVIDIA, Georgia Tech, HKU, University of Chicago, MIT 소속 포함)
- 출판 상태: arXiv preprint
- 라이선스: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- 접근일: 2026-09-05
- 확인 범위: 공식 metadata·초록, v1 PDF 21쪽 전체(본문 1-8, 참고문헌, 부록 A-C). 모든 페이지를 PNG로 렌더링해 그림·표·다단 순서를 시각 확인했다.
- 번역·해설: [공식 제목 번역 파일](./Nemotron-Labs-Diffusion%20-%20A%20Tri-Mode%20Language%20Model%20Unifying%20Autoregressive,%20Diffusion,%20and%20Self-Speculation%20Decoding.번역.md)

## 한눈에 보기

Nemotron-Labs-Diffusion(NLD)은 한 checkpoint가 세 모드로 동작하는 3B/8B/14B 언어 모델군이다.

1. AR mode: 한 토큰씩 causal decoding
2. diffusion mode: 한 블록의 여러 mask를 병렬 복원
3. self-speculation mode: diffusion이 block draft를 쓰고 같은 가중치의 AR 경로가 검증

이를 위해 `L = L_AR + alpha L_diff`, `alpha=0.3`의 공동 목적식과 clean/noisy dual stream attention을 사용한다. 논문의 중요한 실무 결론은 모드에 절대 우열이 있는 것이 아니라 concurrency와 hardware에 따라 선택해야 한다는 것이다. 낮은 concurrency에서는 self-speculation, 높은 concurrency에서는 AR이 유리할 수 있고, 이상적 sampler를 가정한 diffusion에는 더 큰 이론적 여지가 있다.

## 연구 질문과 기여

### 세 연구 질문

- AR과 diffusion은 경쟁 관계인가, 한 모델에서 상호 보완할 수 있는가?
- diffusion draft + AR verify가 MTP 계열보다 강한 가속기가 될 수 있는가?
- 현재 sampler를 넘어선 diffusion decoding의 속도 상한은 충분히 큰가?

### 기여

- causal AR loss와 block diffusion loss를 동일 모델에서 joint training하는 tri-mode framework를 제안했다.
- global token-level loss averaging, data-parallel rank별 mask ratio, AR-first two-stage training을 조합해 diffusion 학습 분산을 낮췄다.
- linear self-speculation, quadratic self-speculation, LoRA-enhanced diffusion drafter를 비교했다.
- serial denoising 목표를 정확히 보존하는 recursive dynamic compaction으로 diffusion SOL(speed-of-light) 상한을 추정했다.
- base, instruct, vision-language variant를 3B/8B/14B로 제시하고 실제 SGLang/GPU 환경에서 throughput을 측정했다.

## 기초 개념과 방법

### Joint objective

```text
L_AR   = -sum_i log p_theta(x_i | x_<i)
L_diff = E_t[-(1/t) sum_b log p_theta(x_b | noisy(x_b,t), x_<b)]
L      = L_AR + alpha * L_diff,  alpha = 0.3
```

Stage 1은 `alpha=0`인 AR continued pretraining으로 left-to-right prior를 강화하고, Stage 2에서 joint objective를 켠다. 25B-token ablation에서 기본 block-wise attention 평균 54.23에서 global averaging 56.35, rank-varying mask 57.06, two-stage 62.80, AR loss 추가 70.28로 상승했다. 이는 구성 요소를 순차 추가한 실험이므로 각 효과의 완전한 독립 추정치는 아니다.

### Dual-stream attention

- clean-to-clean: 엄격한 token-level causal attention으로 AR loss와 AR inference를 보존한다.
- noisy-to-noisy: 현재 block 안은 bidirectional, block 사이는 causal이다.
- noisy-to-clean: denoise 중인 block은 이전 clean block만 본다. 현재·미래 정답은 볼 수 없어야 한다.

loss는 sample별 평균이 아니라 batch 내 기여 token 전체의 global average를 사용한다. mask 수가 적은 sample이 `1/t`로 과도한 영향력을 갖는 것을 완화하려는 설계다.

### 세 추론 모드

- AR: 표준 causal KV cache를 사용한다. 동시 요청이 많아 compute가 찬 환경에 적합하다.
- diffusion: block 내부 mask를 confidence 또는 학습된 sampler로 선택해 병렬 commit한다.
- linear self-speculation: diffusion forward 1회가 `k`개를 draft하고 AR forward 1회가 longest matching prefix를 검증한다. 실질 TPF는 수락 길이를 두 forward로 나눈다.
- quadratic self-speculation: draft·verify 후보를 구조화한 `O(k^2)` token layout으로 한 forward에 융합한다. NFE는 줄지만 kernel 비용이 크다.

LoRA variant는 attention `o_proj`에 rank 128 adapter 약 36M parameters(약 0.4%)를 붙여 draft를 AR verifier와 더 맞춘다.

### Diffusion SOL

SOL은 완전 mask block을 한 위치씩 serial하게 복원해 얻은 diffusion target과 정확히 같은 결과를, 병렬 commit으로 몇 forward에 재현할 수 있는지 측정한다. recursive dynamic compaction은 confidence 순 후보 중 결과를 보존하는 최대 안전 부분집합을 탐색한다. 이는 현실 sampler가 아니라 expensive oracle-like 분석이며 배포 throughput과 혼동하면 안 된다.

## 데이터·평가 지표

- base 8B: Ministral3 계열 pretrained model에서 시작해 Stage 1 AR 1T tokens, Stage 2 joint 300B tokens, sequence length 4096, 256 H100.
- instruct: 45B SFT tokens, sequence length 16K, prompt는 mask하지 않고 answer에만 loss, 256 H100.
- model family: 3B, 8B, 14B base/instruct 및 8B VLM.
- instruct 10 tasks: GPQA, IFEval, MMLU, HumanEval, MBPP, LiveCodeBench-CPP, GSM8K, Math500, AIME24, AIME25.
- VLM: AI2D, ChartQA, DocVQA, MMMU, MathVista, RealWorldQA, MMMU-Pro-V 등.
- efficiency: TPF(tokens per forward), tok/s, system throughput, per-user throughput. SPEED-Bench의 713 samples/11 categories를 SOL 분석에 사용했다.

TPF는 hardware 시간을 직접 뜻하지 않는다. quadratic mode처럼 한 forward의 token 수와 attention 비용이 크면 TPF가 높아도 tok/s가 낮을 수 있다.

## 주요 결과

- NLD-8B instruct의 10-task 평균: AR 63.61, diffusion 63.18, linear SS 62.81, quadratic SS 64.04. 평균 TPF는 각각 1.00, 2.57, 5.99, 6.38이다.
- 같은 표의 Qwen3-8B는 평균 정확도 62.75/TPF 1.00이다. 따라서 “6x”는 정확도 약 6배가 아니라 forward당 token 수 비교다.
- SOL: block 32에서 category 평균 7.60 TPF, block 4에서는 2.89. multilingual 11.26, coding 10.24로 구조화된 영역이 높았다.
- diffusion SOL real TPF 6.02와 linear self-speculation 3.41의 차이는 76.5%다. 목표 출력은 각각 diffusion serial target과 AR verifier target으로 서로 다르다는 제한이 있다.
- 배포: GB200에서 linear self-speculation은 AR 대비 최대 3.3x, 최적 kernel 수치는 3.97x/1015 tok/s로 보고됐다. 논문 초록의 SGLang SPEED-Bench 비교는 Qwen3-8B 대비 약 4x throughput이다.
- acceptance length: NLD native/LoRA 5.46/6.82, Eagle3/MTP 2.75/4.24 평균. coding·math·reasoning·multilingual에서는 격차가 더 컸다.

## 한계와 재현 주의

- v1 preprint의 저자 보고 결과이며 독립 재현·peer review가 확인되지 않았다.
- SOL은 5000-forward simulation budget의 expensive 분석이지 실제 online sampler가 아니다.
- diffusion SOL과 self-speculation은 보존하는 target distribution이 달라 76.5%는 동일 출력·동일 시스템의 직접 속도 비교가 아니다.
- GPU(H100, GB200, RTX Pro 6000, DGX Spark), quantization(FP8/INT4), kernel, concurrency에 따라 결론이 달라진다.
- 3B/8B/14B와 mode 사이의 prompt, sampling, block length를 동일하게 고정해야 품질 비교가 가능하다.
- joint training과 LoRA에 대규모 비공개/외부 데이터 및 많은 GPU가 필요해 이 notebook으로 재현할 수 없다.
- confidence sampler와 non-prefix safe commit은 여전히 open challenge다.

## Trillion Labs OCR 접근과의 관계

[Trillion Labs OCR 글](https://blog.trillionlabs.co/posts/diffusion-ocr/)의 방법적 골격과 가장 직접적으로 겹치는 논문 중 하나다.

| 항목 | Nemotron-Labs-Diffusion | Trillion Labs OCR |
|---|---|---|
| 공동 학습 | AR + block diffusion | clean AR + corrupted block diffusion |
| draft | 같은 모델의 diffusion mode | 같은 GLM-OCR 기반 모델의 diffusion view |
| verify | 같은 모델의 AR mode | 같은 모델의 AR view |
| accept | longest matching prefix | longest matching prefix + 첫 mismatch의 AR token |
| 범위 | 범용 LM/VLM, 3B-14B | OCR 0.9B, block 32 |
| 주요 지표 | 10-task accuracy, TPF, SPEED-Bench tok/s | OmniDocBench, tokens/forward, pages/s |
| 배포 결론 | concurrency별 mode switching | single-stream H100에서 3.85x decode-only, 1.34x page-level |

OCR 출력은 이미지 증거와 HTML·표 문법에 강하게 제약된다. 따라서 자유 작문보다 긴 draft prefix가 맞을 수 있고, 블로그는 평균 약 19 token/round, 전체 forward당 9.6 token을 보고한다. NLD가 범용적으로 보인 “structured category에서 acceptance가 높다”는 관찰을 OCR 도메인에서 더 극단적으로 활용한 사례다.

## 용어 정리

- `tri-mode`: 같은 weights로 AR, diffusion, self-speculation을 선택하는 구성.
- `acceptance length`: 한 draft-verify cycle에서 연속으로 수락한 token 수.
- `real TPF`: acceptance를 해당 cycle의 실제 model forward 수로 나눈 값.
- `SOL`: 현실 sampler가 아니라 diffusion serial target을 보존하는 분석적 상한.
- `global loss averaging`: sample별 평균 대신 batch의 기여 token을 함께 평균하는 분산 완화 방식.

## 실습 학습 가이드

1. [01_foundations.ipynb](./01_foundations.ipynb): AR, diffusion, self-speculation의 forward/commit 회계를 비교한다.
2. [02_practice.ipynb](./02_practice.ipynb): longest-prefix draft-verify와 mismatch 교정을 구현한다.
3. [03_advanced.ipynb](./03_advanced.ipynb): concurrency·acceptance·forward cost를 바꿔 mode 선택과 SOL 상한을 분석한다.

표준 라이브러리만 사용하며 논문 checkpoint나 SPEED-Bench 결과를 재현한다고 주장하지 않는다.

## 다음 학습 경로

1. LLaDA에서 full-sequence masked diffusion의 확률적 기반을 익힌다.
2. Block Diffusion에서 KV-cache-compatible block factorization과 variance schedule을 읽는다.
3. Fast-dVLM에서 direct AR-VLM conversion, auto-truncation, vision-efficient concatenation을 비교한다.
4. 실제 시스템에서는 TPF뿐 아니라 prefill, KV memory, scheduler, latency percentile, end-to-end task metric을 함께 기록한다.
