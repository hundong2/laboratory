# Attention Is All You Need - 문장 대조 번역과 한국어 해설

작성일: 2026-07-26

## 논문 metadata

| 항목 | 내용 |
|---|---|
| 원문 제목 | Attention Is All You Need |
| 저자 | Ashish Vaswani 외 7명 |
| 발표 | 31st Conference on Neural Information Processing Systems, NIPS 2017 |
| 식별자 | arXiv:1706.03762v7, DOI 10.48550/arXiv.1706.03762 |
| 최초 제출 | 2017-06-12 |
| 확인한 버전 | v7, 2023-08-02 |
| 원문 언어 | 영어 |
| 원문 | [abstract page](https://arxiv.org/abs/1706.03762), [HTML](https://arxiv.org/html/1706.03762v7), [PDF](https://arxiv.org/pdf/1706.03762v7) |
| 접근일 | 2026-07-26 |
| 라이선스 표시 | arXiv perpetual non-exclusive distribution license |

## 번역·접근 범위

| section | 상태 | 제공 방식 |
|---|---|---|
| Abstract | 부분 번역 | 짧은 원문 문장 1개와 즉시 대조 번역, 나머지는 한국어 해설 |
| 1 Introduction | 완료 | 한국어 의미 해설 |
| 2 Background | 완료 | 한국어 의미 해설 |
| 3 Model Architecture | 완료 | 한국어 의미 해설과 수식·shape 설명 |
| 4 Why Self-Attention | 완료 | 한국어 의미 해설과 복잡도 표 |
| 5 Training | 완료 | 한국어 의미 해설과 주요 hyperparameter |
| 6 Results | 완료 | 한국어 의미 해설과 핵심 수치·불일치 메모 |
| 7 Conclusion | 완료 | 한국어 의미 해설 |
| References | 해당 없음 | 서지 목록을 재작성하지 않고 원문 링크 제공 |
| Appendix visualizations | 완료 | 그림의 관찰 포인트를 한국어로 설명 |

### 저작권과 번역 방식

원문 페이지는 논문 텍스트 전체의 번역·재배포를 허용하는 오픈 라이선스를 표시하지 않는다. 따라서 원문 전체를 이 파일에 복제하지 않는다. 아래에는 학습 목적의 짧은 문장 대조 예시 하나만 싣고, 나머지 section은 저자 주장의 강도·수식·수치·구조를 보존한 한국어 해설로 제공한다.

원문 전체와 문장 단위로 대조하려면 이 파일과 [공식 HTML](https://arxiv.org/html/1706.03762v7)을 나란히 연다.

## 읽기 전 핵심 배경

- 2017년 당시 강력한 sequence model은 RNN, LSTM, GRU 또는 convolution을 중심으로 구성되는 경우가 많았다.
- RNN은 이전 hidden state가 다음 step 계산에 필요하므로 한 training example 내부의 token 위치를 완전히 병렬 계산하기 어렵다.
- 기존 attention은 흔히 RNN encoder-decoder를 보조했다.
- 이 논문은 sequence 위치 간 정보 전달을 self-attention 중심으로 재구성하고 recurrence와 convolution을 핵심 architecture에서 제거했다.

## 문장 대조 번역

### Abstract

**S001 - Original**

We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.

**S001 - 한국어**

(우리는 recurrence와 convolution을 완전히 없애고 attention mechanism만을 기반으로 하는 새롭고 단순한 network architecture인 Transformer를 제안한다.)

- **용어·약어 해설**
  - **Transformer(트랜스포머)**: recurrence 없이 attention을 중심으로 sequence를 처리하도록 이 논문이 제안한 encoder-decoder architecture다.
  - **attention mechanism(어텐션 메커니즘)**: query와 key의 관련도로 value를 가중합해 필요한 정보를 모으는 연산이다.
  - **recurrence(순환 구조)**: 이전 time step의 hidden state를 다음 step에 다시 사용하는 계산 구조다.
  - **convolution(합성곱)**: 일정한 kernel을 주변 위치에 적용해 local pattern을 결합하는 연산이다.

## Section별 한국어 의미 해설

아래 내용은 원문 문장의 복제가 아니라 section별 주장과 근거를 한국어로 풀어쓴 학습용 해설이다.

### Abstract 해설

기존의 대표적인 sequence transduction model은 encoder와 decoder를 가진 복잡한 recurrent 또는 convolutional network에 기반했고, 강력한 model은 그 둘을 attention으로 연결했다. 저자들은 recurrence와 convolution 없이 attention으로 구성한 Transformer를 제안한다.

두 기계번역 과제에서 Transformer는 높은 품질과 더 큰 병렬화 가능성을 보이면서 학습 시간을 줄였다. English-German에서는 28.4 BLEU, English-French에서는 abstract 기준 41.8 BLEU를 보고한다. 또한 제한된 data와 큰 data 조건의 English constituency parsing에 적용해 번역 이외 과제로의 확장 가능성을 시험한다.

### 1. Introduction 해설

RNN 계열은 sequence 위치와 계산 step을 맞춰 hidden state를 차례대로 갱신한다. 이 구조는 이전 step 결과가 있어야 다음 step을 계산할 수 있어 example 내부 병렬화를 제한한다. sequence가 길어지면 memory 제약 때문에 batch를 크게 만들기도 어렵다.

factorization이나 conditional computation으로 효율을 높인 연구가 있었지만 순차 계산이라는 근본 제약은 남았다. attention은 위치 간 거리에 상관없이 dependency를 연결할 수 있었으나 당시에는 대부분 recurrent network와 함께 사용됐다.

Transformer의 핵심 주장은 recurrence를 제거하고 attention으로 입력과 출력 사이의 global dependency를 직접 구성할 수 있다는 것이다. 논문은 이 구조가 더 높은 병렬성을 제공하고 당시 번역 품질의 최고 수준에 도달할 수 있음을 실험으로 뒷받침한다.

### 2. Background 해설

Extended Neural GPU, ByteNet, ConvS2S 같은 연구도 순차 계산을 줄이기 위해 convolution을 사용했다. 그러나 멀리 떨어진 두 위치를 연결하는 데 필요한 operation 수는 architecture에 따라 거리에 비례하거나 로그로 증가한다.

self-attention은 한 sequence 안의 서로 다른 위치를 연결해 sequence representation을 만든다. reading comprehension, summarization, textual entailment, sentence representation 등에서 이미 사용되고 있었다. 저자들은 Transformer가 입력과 출력 representation 계산을 전적으로 self-attention에 맡긴 첫 sequence transduction model이라고 설명한다.

### 3. Model Architecture 해설

#### 3.1 Encoder와 decoder stack

encoder는 동일한 layer 6개를 쌓는다. 각 layer는 multi-head self-attention과 position-wise FFN이라는 두 sub-layer를 가진다. 각 sub-layer 주위에 residual connection을 두고 그 뒤에 layer normalization을 적용한다.

$$
\mathrm{LayerNorm}(x+\mathrm{Sublayer}(x))
$$

residual addition을 하려면 두 항의 shape가 같아야 하므로 모든 sub-layer와 embedding 출력은 `d_model = 512`를 유지한다.

decoder도 layer 6개를 쌓지만 encoder 출력에 attention하는 세 번째 sub-layer가 추가된다. decoder self-attention에는 미래 위치를 보지 못하게 mask를 적용한다. 정답 output embedding을 한 위치 오른쪽으로 shift해 위치 `i`의 예측이 `i`보다 앞선 출력만 사용하게 한다.

#### 3.2 Scaled dot-product attention

$$
\mathrm{Attention}(Q,K,V)
=
\mathrm{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
$$

1. `QKᵀ`로 모든 query와 key의 dot-product score를 만든다.
2. score를 `√d_k`로 나눠 차원이 클 때 softmax가 지나치게 포화되는 것을 완화한다.
3. key 방향으로 softmax를 적용해 합이 1인 weight를 만든다.
4. weight와 `V`를 곱해 각 query가 모은 context vector를 만든다.

dot-product attention은 최적화된 matrix multiplication을 활용할 수 있어 실무에서 빠르고 memory-efficient하다. scaling이 없고 `d_k`가 크면 dot product의 크기가 커져 softmax gradient가 매우 작아질 수 있다는 것이 논문의 동기다.

#### 3.2.2 Multi-head attention

$$
\mathrm{head}_i
=
\mathrm{Attention}(QW_i^Q,KW_i^K,VW_i^V)
$$

$$
\mathrm{MultiHead}(Q,K,V)
=
\mathrm{Concat}(\mathrm{head}_1,\ldots,\mathrm{head}_h)W^O
$$

Q, K, V를 서로 다른 학습 projection으로 여러 번 변환하고 각 head에서 attention을 병렬 수행한다. 각 head 결과를 concat한 뒤 다시 output projection을 적용한다. 서로 다른 representation subspace와 위치 관계를 동시에 살필 수 있다는 것이 목적이다.

base model은 head 8개, head당 key/value 차원 64를 사용한다. `8 × 64 = 512`라서 concat 뒤 model dimension과 맞는다.

#### 3.2.3 세 attention 경로

- encoder-decoder attention: decoder의 query가 encoder의 key와 value를 조회한다.
- encoder self-attention: Q, K, V가 모두 이전 encoder layer 출력에서 온다.
- decoder self-attention: Q, K, V가 decoder에서 오며 미래 연결을 `-∞` mask로 차단한다.

#### 3.3 Position-wise FFN

$$
\mathrm{FFN}(x)
=
\max(0,xW_1+b_1)W_2+b_2
$$

모든 위치에 같은 FFN을 독립 적용한다. layer마다 parameter는 다르다. base model은 512차원을 2048차원으로 넓힌 뒤 ReLU를 거쳐 다시 512차원으로 줄인다.

#### 3.4 Embedding과 softmax

입력·출력 token은 `d_model` 차원의 embedding으로 바뀐다. decoder 출력은 linear projection과 softmax를 거쳐 다음 token 확률이 된다. 논문은 두 embedding layer와 pre-softmax linear transformation 사이에 weight matrix를 공유한다. embedding에서는 weight에 `√d_model`을 곱한다.

#### 3.5 Positional encoding

$$
PE_{(pos,2i)}
=
\sin\left(pos / 10000^{2i/d_{\text{model}}}\right)
$$

$$
PE_{(pos,2i+1)}
=
\cos\left(pos / 10000^{2i/d_{\text{model}}}\right)
$$

Transformer에는 위치를 순서대로 갱신하는 recurrence가 없으므로 embedding에 위치 정보를 더한다. 차원마다 서로 다른 주기의 sine·cosine을 사용한다. 학습형 positional embedding과 비교했을 때 논문 조건에서는 결과가 거의 같았고, 저자들은 더 긴 길이로의 외삽 가능성을 기대해 sinusoidal 방식을 선택했다.

### 4. Why Self-Attention 해설

논문은 layer를 비교할 때 세 기준을 사용한다.

1. layer당 총 계산 복잡도
2. 필요한 최소 순차 operation 수
3. 멀리 떨어진 dependency 사이의 최대 path length

| layer | layer당 복잡도 | 순차 operation | 최대 path |
|---|---:|---:|---:|
| self-attention | `O(n²d)` | `O(1)` | `O(1)` |
| recurrent | `O(nd²)` | `O(n)` | `O(n)` |
| convolutional | `O(knd²)` | `O(1)` | `O(log_k n)` |
| restricted self-attention | `O(rnd)` | `O(1)` | `O(n/r)` |

`n`은 sequence length, `d`는 representation dimension, `k`는 convolution kernel size, `r`은 restricted attention neighborhood size다.

self-attention은 모든 위치를 한 layer에서 직접 연결하므로 path length가 짧다. 번역 문장처럼 `n < d`인 조건에서는 recurrent layer보다 계산상 유리할 수 있다. 반면 매우 긴 sequence에서는 `n²` 항이 부담이 되므로 local attention 같은 제한 방식이 필요할 수 있다고 논문도 향후 과제로 언급한다.

### 5. Training 해설

#### Data와 batching

- English-German: 약 450만 sentence pair, shared BPE vocabulary 약 37,000
- English-French: 약 3,600만 sentence, word-piece vocabulary 약 32,000
- 각 batch: source 약 25,000 token과 target 약 25,000 token

문장 길이가 비슷한 example을 함께 batch해 padding 낭비를 줄인다.

#### Hardware와 schedule

P100 GPU 8개가 있는 한 machine에서 학습했다. base model은 100,000 step, 약 12시간이고 big model은 300,000 step, 약 3.5일이었다고 보고한다.

#### Optimizer

Adam parameter는 `β₁ = 0.9`, `β₂ = 0.98`, `ε = 10⁻⁹`다.

$$
\mathrm{lrate}
=
d_{\text{model}}^{-0.5}
\min(
\mathrm{step}^{-0.5},
\mathrm{step}\cdot\mathrm{warmup\_steps}^{-1.5}
)
$$

warmup 4,000 step까지 learning rate를 선형 증가시키고 이후 역제곱근으로 감소시킨다.

#### Regularization

- residual dropout
- embedding과 positional encoding 합에 dropout
- label smoothing `ε_ls = 0.1`

label smoothing은 model이 덜 확신하게 만들어 perplexity는 나빠질 수 있지만 accuracy와 BLEU는 개선했다고 보고한다. 서로 다른 metric이 항상 같은 방향으로 움직이지 않는 사례다.

### 6. Results 해설

#### Machine translation

| model | EN-DE BLEU | EN-FR BLEU | 추정 training cost |
|---|---:|---:|---:|
| Transformer base | 27.3 | 38.1 | `3.3 × 10¹⁸` FLOPs |
| Transformer big | 28.4 | 41.8 | `2.3 × 10¹⁹` FLOPs |

big model은 English-German에서 당시 보고된 model과 ensemble보다 2 BLEU 이상 높은 28.4를 기록했다. base model도 더 낮은 training cost로 기존 경쟁 model을 앞섰다고 보고한다.

English-French는 abstract와 Table 2에 41.8이 있으나 본문 설명에는 41.0이 등장한다. 원문의 내부 수치 불일치이므로 둘 중 하나를 임의로 고치지 않고 위치를 구분해 기록한다.

평가에서는 마지막 checkpoint 여러 개를 평균했고 beam size 4, length penalty `α = 0.6`을 사용했다. 따라서 단일 마지막 checkpoint의 greedy decoding만으로 원 수치를 비교하면 조건이 다르다.

#### Model variation

- single head는 가장 좋은 비교 설정보다 BLEU가 낮았다.
- head 수를 과도하게 늘려 head당 차원을 줄여도 품질이 낮아졌다.
- key dimension을 줄이면 품질이 나빠져 compatibility 계산이 단순하지 않음을 시사했다.
- 더 큰 model은 대체로 더 좋았고 dropout은 overfitting 완화에 중요했다.
- learned positional embedding과 sinusoidal encoding은 해당 실험에서 거의 같은 결과였다.

이 결과는 “head가 많을수록 무조건 좋다”거나 “sinusoidal 방식이 항상 우월하다”는 뜻이 아니다. 고정된 compute와 해당 dataset 조건의 ablation이다.

#### English constituency parsing

Transformer를 구조적 제약이 강하고 출력이 입력보다 긴 constituency parsing에 적용했다. WSJ만 사용하는 약 40K sentence 조건과 약 17M sentence를 활용한 semi-supervised 조건을 실험했다. 번역용 base 설정에서 task-specific tuning을 많이 하지 않았는데도 경쟁력 있는 결과를 얻었다고 보고한다.

### 7. Conclusion 해설

저자들은 Transformer를 recurrent layer 대신 multi-head self-attention을 사용하는 최초의 fully attention-based sequence transduction model로 정리한다. 번역에서는 recurrent·convolutional architecture보다 빠르게 학습하면서 당시 최고 수준 결과를 보고했다.

향후 과제로 text 이외의 image·audio·video, 큰 입출력에 대한 local/restricted attention, generation의 순차성 감소를 제시한다. 이 부분은 실험으로 이미 완성된 결과가 아니라 연구 계획이다.

### Appendix attention visualization 해설

- Figure 3: 한 encoder head가 멀리 떨어진 동사와 보어 관계에 높은 weight를 주는 사례를 보여준다.
- Figure 4: 일부 head가 대명사와 관련 명사 사이의 관계를 포착한 것처럼 보이는 사례다.
- Figure 5: 서로 다른 head가 문장 구조와 관련된 서로 다른 pattern을 학습한 것처럼 보인다.

그림의 표현은 “seems”, “apparently”처럼 가능성의 언어를 사용한다. 따라서 attention map을 문법 규칙이나 인과 설명으로 확정하지 않는다.

## 수식·그림 검수 기록

- PDF 15페이지를 PNG로 렌더링해 page 1, 3, 4, 6, 8, 9, 13, 14, 15를 시각 대조했다.
- Figure 1의 encoder·decoder 방향과 masked attention 위치를 확인했다.
- Figure 2의 Scale → optional Mask → Softmax → Value multiplication 순서를 확인했다.
- Table 1의 complexity·sequential operation·path length를 확인했다.
- Table 2·3의 base/big 수치와 head ablation을 확인했다.
- Appendix의 attention visualization은 해석 가능성의 사례이지 인과 증명이 아님을 구분했다.

## 약어 및 기술 용어 사전

| 원어·약어 | 한국어 | 의미 | 최초 등장 |
|---|---|---|---|
| Transformer | 트랜스포머 | attention 중심 encoder-decoder architecture | S001 |
| RNN | 순환 신경망 | 이전 hidden state를 다음 step에 전달하는 network | 배경 |
| LSTM | 장단기 기억 네트워크 | gating으로 장기 dependency 학습을 보완한 RNN | 배경 |
| GRU | 게이트 순환 유닛 | LSTM보다 단순한 gate 구조의 RNN | 배경 |
| sequence transduction | 시퀀스 변환 | 입력 sequence를 출력 sequence로 바꾸는 문제 | Abstract |
| encoder | 인코더 | 입력을 문맥 representation으로 변환하는 부분 | Abstract |
| decoder | 디코더 | 조건부로 출력 sequence를 생성하는 부분 | Abstract |
| self-attention | 자기 어텐션 | 같은 sequence에서 Q·K·V를 만드는 attention | Background |
| Q, Query | 쿼리 | 현재 위치가 찾으려는 정보 표현 | 3.2 |
| K, Key | 키 | query와 비교할 색인 표현 | 3.2 |
| V, Value | 값 | attention weight로 실제 집계할 내용 | 3.2 |
| scaled dot-product attention | 스케일드 닷프로덕트 어텐션 | dot product를 `√d_k`로 나누는 attention | 3.2.1 |
| softmax | 소프트맥스 | score를 합이 1인 양수 weight로 변환 | 3.2.1 |
| multi-head attention | 멀티헤드 어텐션 | 여러 projection 공간의 attention을 병렬 결합 | 3.2.2 |
| causal mask | 인과 마스크 | decoder가 미래 token을 보지 못하게 차단 | 3.2.3 |
| FFN | 순방향 신경망 | 각 token 위치에 독립 적용하는 두 linear layer | 3.3 |
| residual connection | 잔차 연결 | sub-layer 입력을 출력에 더하는 경로 | 3.1 |
| layer normalization | 계층 정규화 | feature 축 통계를 이용하는 normalization | 3.1 |
| embedding | 임베딩 | discrete token을 연속 벡터로 변환 | 3.4 |
| positional encoding | 위치 인코딩 | token 순서를 embedding에 주입하는 벡터 | 3.5 |
| auto-regressive | 자기회귀 | 이전 출력에 조건부로 다음 출력을 생성 | 3.1 |
| BPE | 바이트 페어 인코딩 | 빈번한 symbol pair를 병합하는 subword tokenization | 5.1 |
| BLEU | 이중언어 평가 대체 지표 | n-gram overlap 기반 기계번역 평가 점수 | Results |
| FLOPs | 부동소수점 연산 수 | 계산량을 나타내는 연산 횟수 지표 | Results |
| PPL, perplexity | 퍼플렉서티 | model이 정답 sequence에 부여한 확률의 품질 지표 | Results |
| label smoothing | 레이블 스무딩 | one-hot target을 완화해 과신을 줄이는 regularization | 5.4 |
| dropout | 드롭아웃 | 학습 중 일부 activation을 무작위로 제거 | 5.4 |
| warmup | 워밍업 | 초기 learning rate를 점진적으로 높이는 구간 | 5.3 |
| beam search | 빔 탐색 | 여러 후보 sequence를 유지하는 decoding | 6.1 |
| checkpoint averaging | 체크포인트 평균 | 여러 시점의 weight를 평균해 한 model을 만드는 방법 | 6.1 |
| constituency parsing | 구문 성분 분석 | 문장을 계층적 phrase structure로 분석하는 과제 | 6.3 |
| WSJ | Wall Street Journal | Penn Treebank의 영어 parsing dataset 영역 | 6.3 |

## 다음 읽기

- [한국어 학습 가이드](README.md)
- [기초 attention 실습](01_foundations.ipynb)
- [multi-head·mask 실습](02_practice.ipynb)
- [positional encoding·schedule·복잡도 실습](03_advanced.ipynb)
