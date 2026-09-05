# Block Diffusion - 선택 문장 대조 번역과 절별 해설

## 논문 metadata

| 항목 | 내용 |
|---|---|
| 원문 제목 | Block Diffusion: Interpolating Between Autoregressive and Diffusion Language Models |
| 저자 | Marianne Arriola; Aaron Gokaslan; Justin T. Chiu; Zhihan Yang; Zhixuan Qi; Jiaqi Han; Subham Sekhar Sahoo; Volodymyr Kuleshov |
| 출판처·연도 | ICLR 2025 Oral |
| 식별자 | arXiv:2503.09573, DOI 10.48550/arXiv.2503.09573 |
| 원문 URL | <https://arxiv.org/abs/2503.09573> |
| 사용 버전 | v3, 2025-05-17 |
| 원문 언어 | 영어 |
| 접근일 | 2026-09-05 |
| 라이선스 | CC BY 4.0 |

[학습 README로 돌아가기](./README.md)

## 번역·접근 범위

공식 v3 PDF 28쪽 전체를 확인했지만 이 파일은 전문 대체물이 아니라 선택 문장 대조와 절별 학습 해설이다. 수식은 핵심 관계만 다시 표기하고, 원문의 긴 증명과 참고문헌은 복제하지 않는다.

| 구역 | 상태 | 처리 |
|---|---|---|
| metadata·Abstract | 부분 번역 | 핵심 문장 1개 대조 + 요약 |
| 1 Introduction | 부분 번역 | 문제·기여 상세 해설 |
| 2 Background | 부분 번역 | AR/D3PM 배경 |
| 3 Block Diffusion LM | 부분 번역 | distribution·algorithm |
| 4 Likelihood Gap | 부분 번역 | single-token case·variance |
| 5 Low-Variance Schedules | 부분 번역 | clipped schedule·grid search |
| 6 Experiments | 부분 번역 | PPL·generation·ablation |
| 7 Discussion | 부분 번역 | 선행 연구·한계 |
| 8 Conclusion | 부분 번역 | 결론 |
| Appendix A-D | 부분 번역 | NELBO·mask·kernel·setup·samples |
| References | 원문 미수록 | 공식 PDF 참조 |

## 읽기 전 핵심 배경

- D3PM (Discrete Denoising Diffusion Probabilistic Model, 이산 잡음제거 확산 확률 모델): discrete state를 forward corruption하고 reverse model이 복원한다.
- NELBO (Negative Evidence Lower Bound, 음의 증거 하한): NLL의 계산 가능한 상계다.
- block size: 한 번의 diffusion conditional이 다루는 token 수다.
- clipped schedule: mask probability를 `[beta, omega]` 구간에서만 표본화한다.

## 선택 문장 대조

### Abstract

**S001 — Original**

In this work, we introduce a class of block diffusion language models that interpolate between discrete denoising diffusion and autoregressive models.

**S001 — 한국어**

(우리는 이산 잡음제거 확산 모델과 자기회귀 모델 사이를 보간하는 block diffusion 언어 모델을 제안한다.)

- **용어·약어 해설**
  - **interpolate(보간)**: block size를 바꾸면 token-level AR과 full-sequence diffusion 사이의 factorization·병렬성이 연속적으로 달라진다는 뜻이다.

## 절별 한국어 해설

### 1. Introduction

기존 discrete diffusion LM의 세 약점은 fixed output length, bidirectional attention으로 인한 KV-cache 비호환, AR보다 낮은 likelihood quality다. BD3-LM은 block 사이는 AR, block 안은 diffusion으로 만들어 앞의 두 문제를 구조적으로 완화한다. 세 번째 문제에는 estimator variance 분석과 custom noise schedule을 적용한다.

### 2. Background - Language Modeling Paradigms

AR은 정확한 chain rule factorization과 efficient teacher-forced training을 제공하지만 길이 `L` 생성에 `L` sequential steps가 필요하다. D3PM은 forward transition으로 token을 noise/mask state로 보내고 reverse conditional을 학습하지만 보통 output dimension을 미리 고정한다.

### 3. Block Diffusion Language Modeling

#### 3.1 Distribution and architecture

```text
p_theta(x) = product_(b=1..B) p_theta(x^b | x^<b)
-log p_theta(x) <= sum_b L_diff(x^b, x^<b; theta)
```

각 block conditional에 diffusion NELBO를 적용한 합도 전체 NLL의 valid upper bound다. 하나의 Transformer를 block-causal attention으로 공유한다. 현재 block token은 같은 block과 이전 blocks를 볼 수 있다.

#### 3.2 Efficient training and sampling

clean `x`에서 모든 block의 K/V를 얻고 noisy block prediction을 계산하려면 naive하게 block loop가 필요하다. vectorized 방식은 clean/noisy를 이어 특수 mask로 한 kernel에서 처리한다. sampling은 이전 clean block K/V를 cache한 채 현재 block만 denoise하고, 완료 후 다음 block으로 이동한다.

### 4. Understanding Likelihood Gaps

#### 4.1 Masked BD3-LM

continuous time mask schedule `alpha_t`에서 mask probability는 `1-alpha_t`다. simplified NELBO는 masked-token log probability의 weighted expectation이다. block size가 커질수록 NELBO가 느슨해질 수 있다.

#### 4.2 Single-token case

block size 1에서는 기대상 diffusion objective가 AR NLL로 환원된다. 그럼에도 LM1B에서 기본 diffusion PPL은 `<=25.56`, AR은 22.88이었다. random masking 때문에 평균 절반 token만 loss에 기여해 effective batch signal이 줄고 variance가 커지는 것이 설명이다. 항상 mask하는 tuned schedule은 22.88을 회복했고 loss variance는 1.52에서 0.11로 줄었다.

#### 4.3 Gradient variance

NELBO 자체가 schedule 불변이어도 finite Monte Carlo gradient는 그렇지 않다. 논문은 batch와 time sampling 양쪽을 포함하는 variance estimator를 정의한다. 이 구분이 핵심이다. unbiased 또는 같은 기대값이라는 사실은 낮은 variance나 빠른 optimization을 보장하지 않는다.

### 5. Low-Variance Noise Schedules

mask rate 0이나 1 부근은 학습 신호가 비효율적이다. `m ~ U[beta, omega]`로 극단을 clip하고 validation마다 NELBO variance를 최소화하는 범위를 grid search한다. size 128/16/4의 최적 범위가 달랐고, 작은 block에는 더 높은 masking이 유리했다.

### 6. Experiments

#### 6.1 Likelihood

110M model을 LM1B 65B tokens, OWT 524B tokens로 학습했다. LM1B에서 block 4 PPL `<=28.23`은 MDLM `<=31.78`보다 낮다. OWT에서도 20.73 대 22.98이다. AR 17.54에는 아직 격차가 있다. zero-shot PubMed에서는 block 4 bound 42.52가 표의 AR 48.59보다 낮았다.

#### 6.2 Sample quality and length

BD3-LM은 EOS까지 block을 이어 training context 1024보다 긴 문장을 만들 수 있다. 500 samples에서 최대 9982 tokens였다. 2048-token generation의 GPT2-Large Gen PPL은 block 4가 23.6, MDLM 41.3, AR 13.2다. 외부 evaluator PPL이므로 model likelihood와 다른 지표다.

#### 6.3 Ablations

clipped range는 block-specific하다. LM1B 3B-token fine-tune에서 block 4의 `U[0.45,0.95]`는 PPL 29.21/variance 6.24, linear `U[0,1]`은 30.18/23.45였다. vectorized attention은 two-forward 방식보다 20-25% 빠르게 학습됐다.

### 7. Discussion and Prior Work

D3PM/MDLM의 discrete likelihood, SSD-LM의 Gaussian block diffusion, semi-autoregressive models와 비교한다. BD3-LM의 장점은 tractable likelihood upper bound, KV caching, token 수로 제한되는 NFE다. 저자는 training overhead, sequential blocks, task-specific block size, hallucination·copyright·harmful output을 한계로 든다.

### 8. Conclusion

block factorization으로 variable length/KV cache를 얻고, variance-aware schedule로 discrete diffusion의 PPL을 개선했다는 결론이다. AR gap은 남으며 작은 block의 품질과 큰 block의 parallelism 사이 trade-off가 핵심 설계 변수다.

### Appendix A-D

- A-B: block NELBO derivation, masked forward/reverse, size 1 NLL 환원, NELBO tightness, `2L x 2L` attention mask.
- B.7: PyTorch FlexAttention sparse block mask와 compile/kernel 최적화.
- C: LM1B/OWT preprocessing, 110M architecture, 65B/524B training, low-discrepancy likelihood sampling, generation stopping.
- D: MDLM, BD3-LM, AR의 긴 sample. 정성 예시는 cherry-picking 가능성을 고려한다.

## 수식·표 읽기

- PPL의 `<=` 부호를 제거하지 않는다. diffusion NELBO upper bound임을 나타낸다.
- Table 2는 낮은 NELBO variance와 낮은 test PPL의 상관을 보이지만 세 block size의 작은 grid다.
- Table 6의 max length는 품질과 동일하지 않으며 entropy stopping을 사용한다.
- Table 7의 Gen PPL은 GPT2-Large가 평가한 sample quality proxy다.

## 약어 및 기술 용어 사전

| 원어·약어 | 한국어 | 역할 | 최초 등장 |
|---|---|---|---|
| BD3-LM | 블록 이산 잡음제거 확산 LM | 제안 모델 class | S001 |
| D3PM | 이산 잡음제거 확산 확률 모델 | 각 block conditional의 기반 | 배경 |
| NELBO | 음의 증거 하한 | NLL upper bound 목적식 | 배경 |
| KV cache | 키-값 캐시 | 완료 block computation 재사용 | 3 |
| clipped schedule | 절단 noise schedule | extreme mask rate를 제외해 variance 완화 | 5 |
| PPL | perplexity, 혼란도 | token likelihood 기반 품질 지표 | 6 |
| Gen PPL | 생성 혼란도 | GPT2-Large가 sample에 부여한 품질 proxy | 6 |
| NFE | 모델 평가 횟수 | sampling model calls | 6 |
| FlexAttention | 유연 attention kernel | sparse `2L` mask 계산 최적화 | 부록 |

## 번역 검수 기록

- arXiv v3와 ICLR 2025 Oral, CC BY 4.0, DOI를 대조했다.
- 28쪽 전 페이지를 렌더링해 본문 1-10쪽, 참고문헌, contents, appendix proofs, algorithm, samples를 확인했다.
- S001 Original/한국어 쌍과 단조 sentence ID를 검사했다.
- PPL 상계의 `<=`, 1.52/0.11 variance, 20-25%, length 9982를 원문 표·본문에서 재확인했다.
- 전문 번역이 아니라 `부분 번역`임을 범위표에 명시했다.
