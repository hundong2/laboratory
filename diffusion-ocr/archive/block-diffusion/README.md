# Block Diffusion 학습 노트

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

- 원문: [arXiv:2503.09573](https://arxiv.org/abs/2503.09573), DOI `10.48550/arXiv.2503.09573`
- 확인 버전: v3, 2025-05-17(최초 제출 2025-03-12)
- 저자: Marianne Arriola, Aaron Gokaslan, Justin T. Chiu, Zhihan Yang, Zhixuan Qi, Jiaqi Han, Subham Sekhar Sahoo, Volodymyr Kuleshov
- 출판: ICLR 2025 Oral
- 라이선스: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- 접근일: 2026-09-05
- 확인 범위: 공식 metadata·초록, v3 PDF 28쪽 전체, 본문 1-8, 참고문헌, 부록 A-D. 전 페이지를 PNG로 렌더링해 수식·표·algorithm·sample page를 시각 확인했다.
- 번역·해설: [공식 제목 번역 파일](./Block%20Diffusion%20-%20Interpolating%20Between%20Autoregressive%20and%20Diffusion%20Language%20Models.번역.md)

## 한눈에 보기

Block Diffusion은 문장을 여러 연속 block으로 나눈다. block 사이는 autoregressive하게 순서대로 만들고, 현재 block 안에서는 discrete diffusion으로 여러 token을 병렬 복원한다. block size 1이면 AR에 가까워지고 전체 길이면 full-sequence diffusion에 가까워지는 연속적인 설계다.

이 factorization은 이미 완료된 block의 KV cache를 재사용하고 EOS가 나올 때까지 block을 추가해 arbitrary-length generation을 지원한다. 논문의 두 번째 핵심은 masked diffusion의 Monte Carlo gradient variance가 likelihood gap을 키운다는 분석이다. 극단적 mask rate를 제외하는 data-driven clipped schedule로 variance와 perplexity를 함께 낮춘다.

## 연구 질문과 기여

### 연구 질문

1. fixed-length와 KV-cache 비호환이라는 discrete diffusion의 제약을 block factorization으로 해결할 수 있는가?
2. block size 1에서 기대 목적식이 AR NLL과 같은데도 실제 perplexity가 나쁜 이유는 무엇인가?
3. noise schedule을 바꿔 objective의 기대값은 유지하면서 gradient estimator variance를 낮출 수 있는가?

### 기여

- BD3-LM(Block Discrete Denoising Diffusion Language Model) distribution과 NELBO를 정의했다.
- clean sequence와 block별 noisy sequence를 특수 attention으로 연결해 모든 block loss를 vectorize했다.
- 완료 block의 KV caching과 block 내부 parallel sampling을 결합한 arbitrary-length sampler를 제안했다.
- loss/gradient variance estimator를 도입하고 block size별 clipped masking range를 data-driven하게 선택했다.
- LM1B/OWT에서 기존 discrete diffusion보다 낮은 perplexity와 더 긴 generation을 보고했다.

## 기초 개념

### Block factorization

길이 `L`을 size `K`의 `B=L/K` blocks로 나누면 다음과 같다.

```text
p_theta(x) = product_b p_theta(x^b | x^<b)
```

각 conditional `p_theta(x^b | x^<b)` 자체가 discrete denoising diffusion이다. 이전 block은 clean context, 현재 block은 noisy/masked state다. `K=1`이면 token-level AR factorization에 가까우며 `K=L`이면 full diffusion이다.

### NELBO와 gradient variance

masked diffusion의 NELBO estimator는 random time/mask를 표본화한다. objective의 기대값이 noise schedule에 불변이어도 mini-batch estimator의 분산은 불변이 아니다. mask가 거의 없으면 극소수 token에 큰 가중치가 걸리고, 거의 전부 mask면 학습 신호가 쉬운 marginal prediction에 치우친다.

## 방법

### 효율적 학습

각 block을 따로 denoise하면 `B`번 model call이 필요하다. 제안 algorithm은 clean `x`와 block별 noisy tokens를 길이 `2L` input으로 이어 하나의 sparse attention kernel에서 계산한다.

- clean-clean: block causal/clean context 계산.
- noisy-noisy: 각 noisy block 내부 attention.
- noisy-clean: 현재 noisy block은 이전 clean blocks만 참조.
- clean-noisy: 차단해 label leakage 방지.

각 token은 clean representation과 noisy prediction에 필요한 계산을 거치지만 block loop를 없앤다. FlexAttention sparse kernel을 사용한 구현은 two-forward 방식보다 training 20-25% 빠르다고 보고했다. regular diffusion보다는 여전히 2x 미만 범위에서 비싸다.

### Sampling과 KV cache

block `b`를 denoise할 때 이전 `1..b-1`의 K/V를 cache한다. block이 완료되면 그 K/V를 cache에 붙이고 다음 block으로 간다. EOS 또는 별도 stopping criterion까지 반복할 수 있어 training context보다 긴 출력도 가능하다.

### Data-driven clipped schedule

mask probability를 `m ~ Uniform(beta, omega)`로 제한한다. validation epoch마다 `(beta, omega)` grid를 탐색해 NELBO variance proxy를 최소화한다. 최적 범위는 block size마다 다르다.

- size 128: `U[0, 0.5]`가 표의 최저 PPL/variance.
- size 16: `U[0.3, 0.8]`가 최저 PPL.
- size 4: 더 강한 masking `U[0.5, 1]`가 최저 PPL.

## 데이터·평가 지표

- LM1B: BERT-base-uncased tokenizer, context 128, test perplexity.
- OpenWebText(OWT): GPT-2 tokenizer, context 1024, 마지막 100K documents validation.
- architecture: 12 layers, hidden 768, 12 heads, 110M parameters.
- training: base maximum-block model 850K updates, block-size-specific 150K fine-tuning. LM1B 65B tokens/73 epochs, OWT 524B tokens/60 epochs.
- likelihood: test PPL 및 PTB, WikiText, LM1B, LAMBADA, AG News, PubMed, arXiv zero-shot PPL.
- generation: 500 samples length 통계, 300 samples의 GPT2-Large generative PPL, NFE.

PPL 앞의 `<=`는 diffusion NELBO로 얻은 upper bound임을 뜻한다. AR의 exact likelihood와 그대로 같은 종류의 숫자로 보면 안 된다.

## 주요 결과

- single-token LM1B: AR PPL 22.88, 기본 BD3-LM `<=25.56`, full-mask tuned schedule 22.88. loss variance는 1.52에서 0.11로 감소했다.
- LM1B 65B tokens: MDLM `<=31.78`, BD3-LM block 16 `<=30.60`, 8 `<=29.83`, 4 `<=28.23`.
- OWT 524B tokens: AR 17.54, MDLM `<=22.98`, BD3-LM block 16 `<=22.27`, 8 `<=21.68`, 4 `<=20.73`.
- zero-shot: BD3-LM block 4는 WikiText 31.31, LM1B 60.88, AG News 61.67로 diffusion baselines 중 가장 낮고 PubMed 42.52는 표의 AR 48.59보다 낮다. dataset/tokenization 조건을 같이 봐야 한다.
- 길이: 500 OWT samples에서 SEDD 최대 1024, BD3-LM block 16 최대 9982, AR 최대 131K. median은 각각 1021, 798, 4008이다.
- 길이 2048 generative PPL: AR 13.2, MDLM 41.3, BD3 block 16/8/4는 31.5/28.2/23.6. 모두 2K NFE다.
- vectorized training은 two-forward 구현 대비 20-25% speedup.

작은 block이 likelihood와 sample quality에는 유리했지만 block 수가 늘어 순차성이 커진다. “최고 PPL”과 “최고 parallelism”은 서로 다른 operating point다.

## 한계와 재현 주의

- BD3 training은 standard diffusion보다 비싸며 제안 vectorization도 2L input과 custom sparse attention이 필요하다.
- block을 순차 생성하므로 작은 block에서는 AR과 비슷한 latency·control 제약이 남는다.
- 최적 block size와 clipped mask range는 task/data에 의존한다.
- likelihood 수치는 diffusion NELBO upper bound와 AR exact PPL이 혼합된다.
- 110M model의 LM1B/OWT 결과가 대규모 instruction-tuned LM에 그대로 확장된다는 보장은 없다.
- long generation stopping에는 EOS 외에 최근 256-token entropy <4 조건도 사용하고, 이 경우 generative PPL 보고에서는 sample을 재생성한다. 선택 편향 가능성을 함께 봐야 한다.
- OWT 60 epochs와 benchmark overlap 가능성을 고려해 contamination 검사가 필요하다.
- 생성 모델의 hallucination, copyright, harmful output 위험은 그대로 남는다.
- notebooks는 factorization, attention, variance schedule을 보여주는 toy이며 논문 PPL을 재현하지 않는다.

## Trillion Labs OCR 접근과의 관계

[Trillion Labs OCR 글](https://blog.trillionlabs.co/posts/diffusion-ocr/)은 이 논문을 block diffusion 개념의 직접 reference로 사용한다.

| 항목 | Block Diffusion | Trillion Labs OCR |
|---|---|---|
| 기본 단위 | autoregressive blocks + diffusion tokens | 동일한 block causal 구조 |
| 주목적 | arbitrary length, KV cache, likelihood | OCR decoding wall-clock 가속 |
| 학습 | BD3 NELBO와 variance-optimized schedule | clean AR + corrupted diffusion joint loss, complementary masks |
| 추론 | block 내부 iterative denoising | one-shot block draft 후 AR verify |
| 정확성 | diffusion distribution/sample quality | AR greedy와 byte-level 동일 |
| block trade-off | 작을수록 PPL 개선, 병렬성 감소 | size 32 고정, acceptance와 page latency 측정 |

블로그는 순수 diffusion의 동시 commit 오류를 보았기 때문에 BD3 sampler를 최종 decoder가 아니라 drafter로 사용한다. AR verifier가 틀린 draft를 출력 오류 대신 낮은 acceptance/속도 저하로 바꾼다. 또한 표·수식처럼 구조가 강한 OCR 영역은 block 안 병렬 예측에 유리하므로 범용 OWT보다 큰 block을 활용할 여지가 있다.

## 용어 정리

- `BD3-LM`: block conditional마다 discrete diffusion을 쓰는 semi-autoregressive LM.
- `NELBO`: NLL의 계산 가능한 상계. 표의 `<= PPL` 표기와 연결된다.
- `clipped schedule`: mask rate의 극단을 잘라 estimator variance를 낮추는 schedule.
- `block-causal attention`: 이전 block 전체와 현재 block 내부만 허용하는 attention.
- `generative PPL`: 생성 sample을 외부 LM이 평가한 값으로, 모델 자체 likelihood와 다르다.

## 실습 학습 가이드

1. [01_foundations.ipynb](./01_foundations.ipynb): block factorization과 block-causal attention mask를 시각화한다.
2. [02_practice.ipynb](./02_practice.ipynb): arbitrary-length block generation과 KV cache 회계를 toy sampler로 구현한다.
3. [03_advanced.ipynb](./03_advanced.ipynb): mask range별 Monte Carlo variance를 측정하고 grid search로 clipped schedule을 고른다.

모두 Python 표준 라이브러리와 고정 seed만 쓴다.

## 다음 학습 경로

1. LLaDA의 full masked diffusion 목적식과 `1/t` 가중치를 먼저 복습한다.
2. 이 폴더의 variance notebook에서 schedule의 기대값과 estimator 분산을 구분한다.
3. Nemotron-Labs-Diffusion의 strict causal clean stream과 joint AR loss를 비교한다.
4. Fast-dVLM/Trillion Labs에서 block 32, one-shot draft, AR verify로 발전한 시스템 설계를 추적한다.
