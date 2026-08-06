# How LLMs Actually Work 분석과 실습

작성일: 2026-08-06

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [핵심 요약](#핵심-요약)
- [상세 정리](#상세-정리)
- [정확히 읽기 위한 보충](#정확히-읽기-위한-보충)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 원문: [How LLMs Actually Work](https://www.0xkato.xyz/how-llms-actually-work/)
- 저자: 0xkato
- 게시일: 2026-06-01
- 표시 읽기 시간: 26분
- 원문 언어: 영어
- 접근일: 2026-08-06
- 확인 방법: JavaScript 렌더링된 원문 본문과 섹션·그림 설명을 직접 확인
- 이용 조건: 페이지 하단 저작권 표시는 `0xkato © 2026`이며 별도 재사용 license는 확인하지 못함

저작권이 있는 글의 전문을 복제하지 않고, 원문의 주제 흐름과 기술적 의미를 유지한 한국어 번역 요약을 [`translation.ko.md`](translation.ko.md)에 제공합니다.

## 한눈에 보기

LLM의 기본 계산은 다음 흐름으로 요약할 수 있습니다.

```text
text
  → tokenizer와 token ID
  → embedding vector
  → position 정보(RoPE 등)
  → [normalization → attention → residual → FFN → residual] × N
  → vocabulary logits
  → sampling
  → 다음 token을 붙이고 반복
```

원문은 수식을 최소화하면서 현대 decoder-only Transformer의 주요 부품을 연결합니다. 특히 GQA, KV cache, SwiGLU, RMSNorm, MoE와 speculative decoding까지 소개한다는 점이 강점입니다.

## 기초 개념

### Language model

주어진 token sequence `x₁, …, xₜ` 다음에 올 token의 조건부확률 `P(xₜ₊₁ | x₁, …, xₜ)`을 학습하는 모델입니다. 한 문장의 확률은 각 다음-token 조건부확률의 곱으로 분해할 수 있습니다.

### Transformer block

attention으로 token 사이 정보를 섞고, FFN으로 각 token의 표현을 독립적으로 변환하는 layer입니다. residual connection과 normalization이 깊은 stack의 학습을 안정화합니다.

### Context와 weights

context는 현재 요청에 들어온 token이며 inference가 끝나면 model weights에 자동 저장되지 않습니다. weights는 training과 post-training에서 학습된 parameter입니다. 둘을 구분해야 “대화를 기억한다”와 “모델이 학습했다”를 혼동하지 않습니다.

## 핵심 요약

1. LLM은 문자열을 직접 읽지 않고 tokenizer가 만든 정수 token ID를 처리합니다.
2. embedding table은 ID를 dense vector로 바꾸며, layer를 통과한 뒤에는 문맥화된 representation이 됩니다.
3. RoPE는 Query·Key의 회전을 통해 attention score에 상대적 위치 정보를 반영합니다.
4. scaled dot-product attention은 `softmax(QKᵀ/√dₖ)V`로 token 사이 정보를 섞습니다.
5. causal mask는 다음 token을 예측하는 위치가 미래 token을 보지 못하게 합니다.
6. multi-head attention은 전체 표현의 서로 다른 learned projection에서 여러 관계를 병렬로 봅니다.
7. GQA는 여러 query head가 더 적은 key/value head를 공유해 KV-cache memory를 줄입니다.
8. FFN은 각 token에 독립적으로 적용되며 dense Transformer parameter의 큰 비중을 차지합니다.
9. residual connection은 기존 표현에 sublayer의 갱신을 더하고, normalization은 scale을 안정화합니다.
10. 마지막 token representation을 vocabulary logits로 바꾼 뒤 sampling하고, 선택한 token을 붙여 반복합니다.

## 상세 정리

### 1. Tokenization

subword tokenizer는 word vocabulary의 거대함과 character sequence의 비효율 사이를 절충합니다. tokenizer가 다르면 같은 문장이 다른 token 수가 되므로 비용, context 길이와 다국어 표현 효율도 달라집니다. 철자·글자 수 문제에서 LLM이 흔들리는 이유 중 하나는 입력 단위가 사람이 보는 character와 다르기 때문입니다.

### 2. Embedding

token embedding matrix `E ∈ ℝ^(|V|×d_model)`에서 ID에 해당하는 row를 조회합니다. 이 초기 vector는 token type마다 고정이지만 attention과 FFN을 거치면서 주변 문맥에 따라 달라집니다. 입력 embedding과 최종 unembedding weight를 공유하는 weight tying도 흔한 구현 선택입니다.

### 3. Position과 RoPE

attention 자체는 순서를 자동으로 알지 못합니다. 원 Transformer는 sinusoidal position vector를 더했고, 많은 현대 LLM은 RoPE를 사용합니다. RoPE는 2차원 쌍마다 position에 비례한 각도로 Q와 K를 회전시켜 dot product가 상대 위치 차이에 의존하도록 만듭니다.

### 4. Attention과 causal mask

각 token representation을 서로 다른 matrix로 투영해 Q, K, V를 만듭니다. Q와 K의 similarity를 `√dₖ`로 나누고 mask를 적용한 다음 softmax weight로 V를 합칩니다. decoder-only model의 upper-triangular causal mask는 미래 위치 score를 사실상 `-∞`로 만듭니다.

### 5. Multi-head, GQA와 KV cache

각 head는 원 vector의 고정 slice를 받는 것이 아니라 전체 vector에 대한 독립적인 learned projection을 사용합니다. 생성 중에는 이전 token의 K·V를 cache해 매 step prefix를 다시 투영하지 않습니다. GQA는 query head 수보다 KV head 수를 줄여 cache 크기와 memory bandwidth를 절약합니다.

### 6. FFN, activation과 MoE

FFN은 보통 차원을 확장한 뒤 nonlinear activation을 적용하고 다시 축소합니다. activation이 없으면 여러 linear transformation은 하나의 linear transformation으로 합쳐집니다. 현대 LLM은 GELU나 gated SwiGLU를 자주 사용합니다. MoE는 여러 expert FFN 중 일부만 token별로 활성화해 총 parameter 수와 활성 계산량을 분리합니다.

### 7. Residual stream과 normalization

attention과 FFN의 결과는 기존 representation에 더해집니다. pre-norm 구조는 sublayer 전에 normalization을 적용해 깊은 network에서 gradient 흐름을 안정화합니다. RMSNorm은 mean을 빼지 않고 root-mean-square로 scale을 맞추는 단순한 방식입니다.

### 8. Logits, decoding과 반복

마지막 위치 vector를 vocabulary 크기의 logits로 투영하고 softmax probability를 계산합니다. temperature는 logits의 상대적 sharpness를 바꾸고, top-k와 top-p는 sampling 후보를 제한합니다. 생성은 종료 token 또는 길이 제한에 도달할 때까지 한 token씩 진행됩니다.

### 9. Architecture와 trained weights

tokenization, stacked Transformer block과 next-token objective는 많은 모델이 공유하지만 tokenizer, layer·head·hidden size, dense/MoE 구성, data, 학습 규모와 post-training은 다릅니다. 공개되지 않은 proprietary model의 세부 구조는 추정과 확인된 사실을 구분해야 합니다.

## 정확히 읽기 위한 보충

- “embedding이 의미를 가진다”는 유용한 직관이지만, 초기 token embedding과 layer를 지난 contextual representation은 다릅니다.
- `king - man + woman ≈ queen`은 고전적인 word embedding 예시이지 모든 현대 subword embedding table에서 항상 성립하는 법칙이 아닙니다.
- 특정 FFN neuron과 개념의 상관관계가 발견되더라도 사실 하나가 neuron 하나에만 저장된다고 단정할 수 없습니다. 지식 표현은 대체로 분산되어 있습니다.
- full attention의 score matrix는 sequence 길이에 대해 quadratic이지만, 실제 latency는 prefill·decode, KV cache, hardware kernel과 memory bandwidth에 따라 달라집니다.
- attention weight가 높다는 사실만으로 인간이 이해하는 인과적 “설명”이라고 볼 수 없습니다.
- temperature 0도 실행 환경과 backend 차이까지 포함한 절대적 재현성을 보장하지는 않습니다.

## 용어 정리

| 용어 | 의미 |
|---|---|
| Token | tokenizer가 처리하는 text 조각 |
| Embedding | discrete ID를 dense vector로 표현한 값 |
| Hidden size | token representation vector의 차원 |
| RoPE | Q·K 회전으로 위치를 반영하는 방식 |
| Q/K/V | 조회 조건, 매칭 표지, 전달할 정보 vector |
| Causal mask | 미래 token 접근을 막는 mask |
| Attention head | 독립 projection을 사용하는 attention 계산 단위 |
| GQA | 여러 query head가 적은 KV head를 공유하는 구조 |
| KV cache | 이전 token의 K·V를 저장하는 inference cache |
| FFN | token별 nonlinear transformation |
| MoE | 선택된 expert만 활성화하는 sparse FFN 구조 |
| Residual stream | layer별 갱신이 더해지는 representation 경로 |
| RMSNorm | RMS 기준으로 vector scale을 맞추는 normalization |
| Logit | softmax 이전의 vocabulary별 raw score |

## 실습 학습 가이드

1. [`01_foundations.ipynb`](01_foundations.ipynb): token ID, embedding, softmax와 sampling
2. [`02_practice.ipynb`](02_practice.ipynb): RoPE, causal self-attention과 multi-head projection
3. [`03_advanced.ipynb`](03_advanced.ipynb): residual·RMSNorm·SwiGLU block, autoregressive loop와 KV-cache 용량 분석

세 notebook은 NumPy만 사용하며 실제 LLM을 다운로드하지 않는 toy reproduction입니다. 원 모델의 품질이나 학습 결과를 재현한다고 주장하지 않습니다.

## 다음 학습 경로

1. Vaswani et al., *Attention Is All You Need*에서 attention 수식과 original architecture를 확인합니다.
2. RoFormer에서 RoPE의 relative position 성질을 공부합니다.
3. LLaMA·Mistral technical report에서 RMSNorm, SwiGLU와 GQA 구성을 비교합니다.
4. FlashAttention을 통해 수학적으로 같은 attention을 IO-aware하게 계산하는 방법을 학습합니다.
5. Transformer Circuits와 ROME 연구를 읽을 때 관찰·개입·인과 주장 수준을 구분합니다.
