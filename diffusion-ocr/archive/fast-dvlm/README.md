# Fast-dVLM 학습 노트

작성일: 2026-09-05

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [연구 질문과 기여](#연구-질문과-기여)
- [기초 개념](#기초-개념)
- [방법](#방법)
- [데이터·평가 지표](#데이터평가-지표)
- [주요 결과](#주요-결과)
- [한계와 재현 주의](#한계와-재현-주의)
- [Trillion Labs OCR 접근과의 관계](#trillion-labs-ocr-접근과의-관계)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 원문: [arXiv:2604.06832](https://arxiv.org/abs/2604.06832), DOI `10.48550/arXiv.2604.06832`
- 확인 버전: v2, 2026-04-10(최초 제출 2026-04-08)
- 저자: Chengyue Wu, Shiyi Lan, Yonggan Fu, Sensen Gao, Jin Wang, Jincheng Yu, Jose M. Alvarez, Pavlo Molchanov, Ping Luo, Song Han, Ligeng Zhu, Enze Xie
- 출판 상태: arXiv preprint
- 라이선스: [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/). NoDerivatives 조건 때문에 전문 번역 재배포는 피하고 짧은 인용과 독립적 한국어 해설만 제공한다.
- 접근일: 2026-09-05
- 확인 범위: 공식 metadata·초록, v2 PDF 20쪽 전체(본문, 참고문헌, 부록 A-D). 모든 페이지 PNG 렌더링과 contact sheet 시각 검토를 완료했다.
- 번역·해설: [공식 제목 번역 파일](./Fast-dVLM%20-%20Efficient%20Block-Diffusion%20VLM%20via%20Direct%20Conversion%20from%20Autoregressive%20VLM.번역.md)

## 한눈에 보기

Fast-dVLM은 이미 멀티모달 정렬된 Qwen2.5-VL-3B AR VLM을 block diffusion VLM으로 직접 미세조정한다. 텍스트 LLM을 먼저 diffusion으로 바꾼 뒤 vision을 붙이는 two-stage 방식보다 동일한 2M multimodal samples/1 epoch에서 direct conversion이 평균 73.3 대 60.2로 높았다.

핵심 recipe는 block-size annealing, causal clean context, response-boundary auto-truncation, vision-efficient concatenation, joint AR/diffusion loss다. 추론은 KV cache를 유지하는 block denoising 또는 같은 모델의 diffusion draft + AR verify로 수행한다. SGLang과 W8A8 FP8까지 합쳐 MMMU-Pro-V에서 AR baseline 대비 최대 6.18x end-to-end speedup을 보고했다.

## 연구 질문과 기여

### 연구 질문

1. AR VLM을 diffusion VLM으로 바꿀 때 text-first two-stage와 full-VLM direct path 중 어느 쪽이 같은 예산을 더 잘 쓰는가?
2. continuous vision embeddings와 discrete response tokens를 복제·누수 없이 dual-stream attention에 넣는 방법은 무엇인가?
3. block diffusion의 NFE 이득이 실제 single-stream VLM serving의 wall-clock 가속으로 이어지는가?

### 기여

- pretrained AR VLM의 multimodal alignment를 보존하는 direct conversion recipe를 제시했다.
- multi-turn 경계를 넘는 noisy block의 label leakage를 auto-truncation으로 막았다.
- vision token을 clean stream에 한 번만 넣어 peak memory 15.0%, training time 14.2%를 줄였다고 보고했다.
- causal context attention으로 AR mode와 KV cache를 유지해 self-speculative verification을 가능하게 했다.
- 11 VLM benchmarks와 H100 batch 1 환경에서 품질·Tokens/NFE·TPS를 함께 평가했다.

## 기초 개념

- AR VLM은 image embedding을 prefix로 넣어도 response token은 보통 왼쪽부터 하나씩 만든다.
- block diffusion은 완료 block 사이에는 causal 순서를 유지하고 현재 block 내부만 병렬 복원한다.
- direct conversion은 vision-language alignment가 이미 있는 checkpoint를 출발점으로 삼는다.
- speculative decoding은 빠른 draft를 강한 verifier가 검사하며, 거절은 품질 손실이 아니라 낮은 수락률로 나타나게 한다.

## 방법

### Direct conversion

- two-stage: Qwen2.5-Instruct-3B -> 300K text-only diffusion samples -> vision encoder/MLP 결합 -> multimodal fine-tuning.
- direct: Qwen2.5-VL-3B 전체를 약 2M multimodal instruction samples로 한 단계 joint fine-tuning.

두 경로의 multimodal data와 1-epoch compute를 맞춘 비교에서 direct가 모든 10개 short-answer benchmark 축에서 높았다. 논문은 같은 최종 ceiling을 증명하지 않고, 제한 예산에서 pretrained alignment의 효율 이점이라고 해석한다.

### Training attention과 loss

입력 `x=(v,w)`에서 vision embeddings `v`는 clean stream에만 둔다. noisy stream `w_t`는 response text만 포함한다.

- noisy-to-noisy: 같은 block 내부 bidirectional.
- noisy-to-clean: 이전 causal context와 vision tokens를 참조.
- clean-to-clean: token-level causal.

clean path에는 AR loss, noisy path의 masked response에는 diffusion loss를 주며 `alpha=beta=0.5`로 동일 가중한다.

### 네 가지 adaptation

1. block-size annealing: `2,4,8,...,32`처럼 작은 block에서 시작해 진행률에 따라 키운다.
2. causal context: 이전 clean context의 AR representation을 보존한다.
3. auto-truncation: response 마지막 block을 실제 경계에서 잘라 다음 turn prompt를 보지 못하게 한다.
4. vision-efficient concatenation: 손상되지 않는 vision token을 noisy stream에 복제하지 않는다.

### Inference

- MDM mode: cached causal context에서 첫 token을 AR로 seed하고 나머지 block을 mask로 채워 threshold `tau`에 따라 denoise한다.
- linear self-spec: diffusion 1 forward draft + causal 1 forward verify, longest matching prefix와 첫 AR mismatch token을 확정하고 cache를 crop한다. 이론상 block size `B`에서 최대 `B/2` tokens/NFE다.
- quadratic self-spec: 한 forward에 `B(B+1)` query tokens를 펼쳐 여러 acceptance point의 verify와 next proposal을 계산한다. NFE는 낮지만 `O(B^2)` compute 때문에 현재 kernel에서는 느릴 수 있다.
- system: SGLang scheduler, paged KV cache, optimized kernel/CUDA graph, SmoothQuant W8A8 FP8.

## 데이터·평가 지표

- 초기 checkpoint: Qwen2.5-VL-3B.
- 학습: NVILA mixture를 참고한 약 2M samples. ShareGPT4V, LLaVA-Instruct, DVQA, ChartQA, AI2D, GeoQA, DocVQA, SynthDoG 등을 포함한다.
- 64 H100, DeepSpeed ZeRO-2, BF16, gradient checkpointing, 1 epoch, global batch 256, peak LR `5e-6`, target block size 32.
- short answer 10개: AI2D, ChartQA, DocVQA, GQA, MMBench, MMMU, POPE, RealWorldQA, SEEDBench2+, TextVQA.
- long answer: MMMU-Pro-V.
- 평가 도구: VLMEvalKit, AR baseline과 같은 prompt/post-processing.
- 효율: H100 1장, batch 1. TPS와 MMMU-Pro-V의 response >200 token subset에서 Tokens/NFE를 측정한다.

## 주요 결과

- short-answer 평균: AR 74.0, Fast-dVLM MDM 73.3/1.95 Tokens/NFE, self-spec 74.0/2.63 Tokens/NFE.
- MMMU-Pro-V: AR 26.3, MDM 21.4, self-spec 24.6. 긴 sequential reasoning에서는 diffusion의 품질 격차가 더 크다.
- direct vs two-stage: 평균 73.3 vs 60.2. DocVQA +31.5, ChartQA +21.4, AI2D +18.1 point 차이라고 보고한다.
- ablation 평균: full 57.3, causal context 제거 44.4(-22.5%), annealing 제거 54.8(-4.4%), auto-truncation 제거 55.2(-3.7%).
- `tau`: 1.0에서 accuracy 21.6/약 1 token-step, 0.9에서 21.4/1.95, 0.4에서 18.5/2.90. default는 0.9다.
- progressive system result: AR 56.7 TPS -> MDM 82.2 -> linear self-spec 112.7 -> SGLang 319.0 -> FP8 350.3 TPS. 마지막은 6.18x이며 accuracy는 26.3에서 23.8로 낮다.

“품질 손실 없이 6x”로 단순화하면 안 된다. benchmark 평균 동률은 self-spec short-answer 비교이고, 6.18x 수치는 MMMU-Pro-V에서 FP8까지 누적한 결과로 점수가 2.5 point 낮다.

## 한계와 재현 주의

- CC BY-NC-ND라 이 폴더는 논문 번역본이 아니라 제한 인용 기반 분석이다.
- v2 arXiv preprint이며 독립 재현이나 peer-reviewed 최종판을 확인하지 못했다.
- direct path의 우세는 1 epoch/2M samples라는 제한 예산에서의 결과다. 동일 최종 수렴점은 가설이다.
- 품질 비교, Tokens/NFE, TPS가 다른 subset·조건에서 측정된다. 표의 분모를 반드시 함께 기록해야 한다.
- 6.18x는 SGLang과 quantization의 기여까지 누적한다. algorithm-only speedup은 linear self-spec의 1.98x TPS다.
- quadratic mode는 NFE가 높아도 current kernel에서 더 낮은 TPS였다. NFE를 latency proxy로 단정할 수 없다.
- training mixture가 평가 benchmark와 겹치는 구성요소를 포함하므로 split·contamination 관리가 필요하다.
- physical AI 사례는 정성 예시이며 closed-loop safety를 평가한 결과가 아니다.

## Trillion Labs OCR 접근과의 관계

블로그가 직접 “방법론적으로 가장 가까운 선행 연구”로 지목한 논문이다. [Trillion Labs OCR 글](https://blog.trillionlabs.co/posts/diffusion-ocr/)과 다음 구조를 공유한다.

| 항목 | Fast-dVLM | Trillion Labs OCR |
|---|---|---|
| 시작 모델 | Qwen2.5-VL-3B | GLM-OCR 0.9B |
| 변환 | full AR VLM direct conversion | OCR checkpoint를 AR+block diffusion 겸용으로 fine-tune |
| vision | clean stream에 한 번만 배치 | 이미지·prompt는 항상 clean |
| clean attention | token-level causal | token-level causal + AR loss |
| noisy attention | block 내부 bidirectional, 이전 clean context | 같은 구조, complement masking streams |
| 추론 | diffusion draft + AR verify | one-shot draft + longest-prefix verify |
| block | target 32 | 32 |
| 지표 | 11 VLM tasks, MMMU-Pro-V, TPS/NFE | OmniDocBench, pages/s, tokens/forward |

차이는 OCR이 출력이 이미지에 더 강하게 고정되고 표/수식 문법이 구조화되어 draft acceptance가 길다는 점이다. Trillion Labs는 greedy AR과 byte-level 동일성을 검증하고 평균 9.6 tokens/forward, decode-only 3.85x를 보고한다. Fast-dVLM의 vision-efficient concatenation과 auto-truncation은 OCR 모델 학습에서도 특히 재사용할 가치가 있는 설계다.

## 용어 정리

- `auto-truncation`: response 끝에서 noisy block을 잘라 미래 turn prompt 누수를 막는 attention 처리.
- `vision-efficient concatenation`: 변하지 않는 vision embedding을 clean stream에 한 번만 넣는 방식.
- `Tokens/NFE`: model evaluation 한 번당 확정 token 수. wall-clock TPS와 같지 않다.
- `linear self-speculation`: draft 1회와 verify 1회를 쓰는 prefix acceptance 방식.
- `quadratic self-speculation`: 여러 acceptance point를 `O(B^2)` query layout에 펼치는 방식.

## 실습 학습 가이드

1. [01_foundations.ipynb](./01_foundations.ipynb): block-causal attention과 response-boundary truncation을 boolean matrix로 만든다.
2. [02_practice.ipynb](./02_practice.ipynb): direct vs two-stage를 “alignment 보존 비용” toy learning curve로 비교한다.
3. [03_advanced.ipynb](./03_advanced.ipynb): threshold, acceptance, NFE, system multiplier를 분리해 speed-quality frontier를 계산한다.

표준 라이브러리만 사용하며 실제 VLM, H100, SGLang 결과를 재현하지 않는다.

## 다음 학습 경로

1. Block Diffusion의 probability factorization과 KV cache 근거를 읽는다.
2. Nemotron-Labs-Diffusion의 joint objective와 mode switching을 비교한다.
3. 실제 변환 실험에서는 AR checkpoint, tokenizer, data split, block schedule, quantization을 고정하고 baseline과 동일 prompt로 평가한다.
4. OCR 적용에서는 text/table/formula 영역별 수락 길이와 page-level fixed cost를 별도 측정한다.
