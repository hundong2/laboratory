# Attention Is All You Need 학습 가이드

작성일: 2026-07-26

## 출처와 작업 범위

- 논문: [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- 확인한 원문: [arXiv v7 HTML](https://arxiv.org/html/1706.03762v7), [arXiv v7 PDF](https://arxiv.org/pdf/1706.03762v7)
- 저자: Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin
- 발표: 31st Conference on Neural Information Processing Systems, NIPS 2017
- 최초 제출: 2017-06-12
- 확인한 버전: arXiv v7, 2023-08-02
- 확인일: 2026-07-26
- 분야: Computation and Language, Machine Learning
- 원문 언어: 영어
- PDF 상태: 15페이지, 암호화 없음, 다단 편집과 수식·표·그림을 렌더링하여 시각 검수

arXiv 페이지에는 perpetual non-exclusive distribution license가 표시되어 있으며, PDF에는 적절한 출처 표기 아래 표와 그림을 보도·학술 목적으로 재사용할 수 있다는 별도 문구가 있다. 논문 텍스트 전체를 재배포할 수 있는 오픈 라이선스로 확인되지는 않았으므로, [번역 자료](Attention%20Is%20All%20You%20Need.번역.md)는 짧은 문장 대조 예시와 섹션별 한국어 해설로 구성했다.

## 한눈에 보기

이 논문의 핵심은 “순서를 처리하려면 반드시 recurrence가 필요하다”는 당시의 관행을 깨고, encoder와 decoder의 핵심 연산을 attention으로 구성한 Transformer를 제안한 것이다.

논문의 논리 흐름은 다음과 같다.

1. RNN은 token 위치를 시간 순서대로 처리해 학습 병렬화가 어렵다.
2. attention은 멀리 떨어진 위치도 직접 연결할 수 있다.
3. 여러 관계를 동시에 표현하도록 multi-head attention을 사용한다.
4. recurrence가 사라져 순서 정보가 없으므로 positional encoding을 더한다.
5. residual connection, layer normalization, feed-forward network를 결합해 깊은 encoder-decoder를 만든다.
6. 기계번역과 constituency parsing 실험으로 품질·학습 효율·다른 과제에 대한 일반화를 평가한다.

## 먼저 바로잡을 오해

### “Attention만 있다”는 말의 범위

Transformer가 attention 연산만으로 이루어졌다는 뜻은 아니다. 각 layer에는 다음 요소도 있다.

- token embedding
- positional encoding
- residual connection
- layer normalization
- position-wise feed-forward network
- decoder의 causal mask
- 출력 linear projection과 softmax

제목의 의미는 sequence 간 정보 전달의 중심에서 recurrent layer와 convolutional layer를 제거하고 attention을 사용했다는 것이다.

### 모든 attention이 항상 빠른 것은 아니다

길이 `n`, 표현 차원 `d`일 때 dense self-attention의 주요 score matrix는 `n × n`이므로 계산·메모리 비용이 길이에 대해 제곱으로 증가한다. 논문은 당시 번역 문장처럼 `n < d`인 조건에서 recurrent layer보다 유리한 경우를 논증한다. 매우 긴 sequence에서는 이 가정과 hardware 특성을 다시 측정해야 한다.

### attention weight가 곧 설명은 아니다

논문의 부록은 head마다 장거리 의존성, 대명사 관계, 문장 구조와 관련돼 보이는 pattern을 시각화한다. 그러나 특정 weight가 높다는 사실만으로 모델의 완전한 인과 설명이라고 단정할 수는 없다.

## 기초 개념

### Sequence transduction

입력 sequence를 다른 출력 sequence로 바꾸는 문제다. 번역에서는 영어 token sequence를 독일어 token sequence로 변환한다. 입력과 출력 길이가 다를 수 있다.

### Encoder와 decoder

- encoder: 입력 token을 문맥이 반영된 연속 벡터 sequence로 바꾼다.
- decoder: 이미 생성한 출력과 encoder 표현을 사용해 다음 token 확률을 만든다.
- auto-regressive generation: 앞에서 생성한 token을 조건으로 다음 token을 하나씩 생성한다.

### Query, Key, Value

attention은 검색에 비유하면 이해하기 쉽다.

- Query(Q): 지금 찾고 싶은 정보
- Key(K): 각 위치가 어떤 정보인지 비교하기 위한 색인
- Value(V): 선택되었을 때 실제로 가져올 내용

Query와 Key의 유사도로 가중치를 만든 뒤 Value의 가중합을 계산한다. Q, K, V는 원래 token 그 자체가 아니라 학습 가능한 linear projection을 거친 표현이다.

## 핵심 수식

### Scaled dot-product attention

$$
\mathrm{Attention}(Q,K,V)
=
\mathrm{softmax}\left(\frac{QK^\top}{\sqrt{d_k}} + M\right)V
$$

논문 식 (1)에는 mask `M`이 직접 쓰이지 않지만 decoder 구현을 함께 이해하기 위해 표시했다.

shape를 batch 축 없이 쓰면 다음과 같다.

| 기호 | shape | 의미 |
|---|---:|---|
| `Q` | `n_q × d_k` | query sequence |
| `K` | `n_k × d_k` | key sequence |
| `V` | `n_k × d_v` | value sequence |
| `QKᵀ` | `n_q × n_k` | 모든 query-key score |
| attention weight | `n_q × n_k` | key 방향 합이 1인 확률 |
| 출력 | `n_q × d_v` | 각 query가 모은 문맥 |

#### 왜 `√d_k`로 나누는가

Q와 K 각 성분의 평균이 0, 분산이 1이고 독립이라고 단순화하면 dot product의 분산은 `d_k`에 비례한다. 차원이 커질수록 score 절댓값이 커져 softmax가 한쪽으로 포화되고 gradient가 작아질 수 있다. `√d_k`로 나누면 score scale을 안정시키는 데 도움이 된다.

이 주장은 [01_foundations.ipynb](01_foundations.ipynb)에서 scaling 전후 entropy와 gradient-friendly한 분포를 비교한다.

### Multi-head attention

$$
\mathrm{MultiHead}(Q,K,V)
=
\mathrm{Concat}(\mathrm{head}_1,\ldots,\mathrm{head}_h)W^O
$$

$$
\mathrm{head}_i
=
\mathrm{Attention}(QW_i^Q,KW_i^K,VW_i^V)
$$

각 head는 다른 projection 공간에서 관계를 찾는다. 논문의 base model은 다음 설정을 사용한다.

- `d_model = 512`
- `h = 8`
- `d_k = d_v = 64`
- `h × d_v = 512`

head 수만 늘린다고 항상 좋아지는 것은 아니다. 전체 계산량을 비슷하게 유지하면 head당 차원이 작아져 정보 병목이 생길 수 있으며, 논문의 ablation에서도 너무 적거나 너무 많은 head가 모두 불리할 수 있음을 보여준다.

### Position-wise feed-forward network

$$
\mathrm{FFN}(x)
=
\max(0, xW_1+b_1)W_2+b_2
$$

같은 두 linear transformation을 모든 token 위치에 독립적으로 적용한다. base model에서 입력·출력은 512차원이고 내부 차원은 2048이다. token 간 정보 이동은 attention이 담당하고, FFN은 각 위치의 channel 표현을 비선형 변환한다.

### Positional encoding

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

recurrence와 convolution이 없으면 token 순서를 자동으로 알 수 없다. 그래서 embedding과 같은 차원의 위치 벡터를 더한다. 짝수 차원은 sine, 홀수 차원은 cosine을 사용하고 차원마다 파장이 달라진다.

논문은 학습형 positional embedding도 실험했으며 당시 조건에서는 유사한 결과를 보고했다. sinusoidal 방식을 선택한 이유는 학습 때 보지 못한 더 긴 길이로 외삽할 가능성에 대한 가설이었다. 이것은 모든 조건에서 장문 일반화를 보장한다는 증명이 아니다.

### Learning-rate schedule

$$
\mathrm{lrate}
=
d_{\text{model}}^{-0.5}
\min\left(
\mathrm{step}^{-0.5},
\mathrm{step}\cdot\mathrm{warmup\_steps}^{-1.5}
\right)
$$

처음 `warmup_steps = 4000`까지는 선형으로 증가하고 이후 step의 역제곱근에 비례해 감소한다. [03_advanced.ipynb](03_advanced.ipynb)에서 peak 위치와 `d_model` 변화의 영향을 그린다.

## 모델 구조

### Encoder layer

1. multi-head self-attention
2. residual addition
3. layer normalization
4. position-wise FFN
5. residual addition
6. layer normalization

논문의 표기는 `LayerNorm(x + Sublayer(x))`이므로 현재 흔히 “post-norm”이라 부르는 형태다.

### Decoder layer

1. masked multi-head self-attention
2. residual addition과 normalization
3. encoder-decoder multi-head attention
4. residual addition과 normalization
5. position-wise FFN
6. residual addition과 normalization

decoder self-attention은 미래 위치 score를 `-∞`로 만들어 softmax 확률이 0이 되게 한다. 출력 embedding을 한 칸 오른쪽으로 이동하는 teacher-forcing 입력과 함께 사용해야 현재 위치가 정답 token을 미리 보지 않는다.

### 세 종류의 attention

| 위치 | Q 출처 | K·V 출처 | 목적 |
|---|---|---|---|
| encoder self-attention | 이전 encoder layer | 이전 encoder layer | 입력 전체 문맥 결합 |
| decoder masked self-attention | 이전 decoder layer | 이전 decoder layer | 과거 출력만 사용 |
| encoder-decoder attention | decoder | encoder 최종 출력 | 출력 위치가 입력 위치를 조회 |

## 학습 설정과 결과를 읽는 법

### Data와 batch

- English-German: 약 450만 sentence pair, shared BPE vocabulary 약 37,000
- English-French: 약 3,600만 sentence, word-piece vocabulary 약 32,000
- batch: 문장 수가 아니라 source 약 25,000 token과 target 약 25,000 token을 기준으로 구성

길이가 비슷한 문장을 묶으면 padding 낭비를 줄일 수 있다. 재현할 때 “batch size”를 문장 개수만으로 비교하면 원 논문의 token budget과 달라진다.

### Base와 big

| 설정 | `N` | `d_model` | `d_ff` | head | train step | parameter |
|---|---:|---:|---:|---:|---:|---:|
| base | 6 | 512 | 2048 | 8 | 100K | 약 65M |
| big | 6 | 1024 | 4096 | 16 | 300K | 약 213M |

원 논문은 P100 GPU 8개를 사용했다. base는 약 12시간, big은 약 3.5일 학습했다고 보고한다. 오늘날 다른 GPU에서 걸린 wall-clock time만 비교하지 말고 precision, kernel, batch token 수, framework와 communication 구성을 함께 기록해야 한다.

### 주요 보고 결과

- English-German newstest2014: big model BLEU 28.4
- English-French newstest2014: Table 2의 big model BLEU 41.8
- English-German에서 당시 보고된 ensemble 최고치보다 2 BLEU 이상 개선했다고 기술
- constituency parsing에서도 별도의 대규모 architecture 변경 없이 경쟁력 있는 결과를 보고

본문 English-French 설명에는 41.0이라는 수치가 등장하지만 abstract와 Table 2에는 41.8이 표시된다. 학습 자료에서는 이 불일치를 숨기지 않고 표와 문장의 출처 위치를 구분한다.

### BLEU를 읽을 때

BLEU는 n-gram overlap 기반 기계번역 지표다. tokenization, case 처리, test set과 구현이 다르면 숫자를 직접 비교할 수 없다. 현대 결과와 비교하려면 동일한 평가 script와 dataset version을 사용해야 한다.

## 논문의 강점

- recurrence를 제거한 명확하고 검증 가능한 architecture 제안
- 계산 복잡도, 순차 연산 수, 최대 path length라는 세 관점으로 self-attention을 설명
- 번역 품질뿐 아니라 training cost를 함께 비교
- head 수, 차원, 깊이, dropout, positional encoding을 바꾼 ablation 제공
- 다른 구조화 출력 과제인 constituency parsing으로 범용성 탐색
- attention visualization으로 내부 pattern을 관찰할 단서 제공

## 한계와 재현 시 주의점

- dense attention은 긴 sequence에서 `O(n²)` score memory가 필요하다.
- 결과는 2017년의 dataset, tokenization, hardware, software stack에 의존한다.
- Table의 training FLOPs는 실측 energy가 아니라 hardware 처리량과 시간에 기반한 추정이다.
- ablation은 모든 조합을 독립적으로 완전히 탐색한 것이 아니다.
- attention visualization만으로 인과적 설명 가능성을 확정할 수 없다.
- 원 논문 설정을 노트북 toy model에 적용한 결과는 WMT 재현이 아니다.
- seed, data order, tokenizer, checkpoint averaging, beam search가 결과에 영향을 준다.

## 실습 학습 가이드

### 실행 환경

세 notebook은 GPU 없이 NumPy로 실행할 수 있다.

```bash
cd attention-is-all-you-need
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install "numpy>=1.26" "jupyterlab>=4"
jupyter lab
```

Windows PowerShell에서는 activate 명령만 다음처럼 바꾼다.

```powershell
.\.venv\Scripts\Activate.ps1
```

실습은 원 논문의 WMT training을 재현하는 것이 아니라 핵심 연산과 검증 조건을 작은 입력에서 재현한다. 따라서 notebook 실행 결과를 논문 BLEU 재현 결과로 보고하면 안 된다.

1. [01_foundations.ipynb](01_foundations.ipynb)
   - Q·K·V shape
   - 안정적인 softmax
   - `√d_k` scaling
   - padding mask
2. [02_practice.ipynb](02_practice.ipynb)
   - causal mask
   - 여러 head의 split·transpose·concat
   - self-attention과 cross-attention 비교
3. [03_advanced.ipynb](03_advanced.ipynb)
   - sinusoidal positional encoding
   - 논문 learning-rate schedule
   - sequence length별 attention memory
   - scaling ablation과 검증 gate

각 notebook은 작은 NumPy 예제로 논문의 핵심 연산을 재현한다. WMT 번역 성능을 재현한다고 주장하지 않으며, shape·mask·수치 안정성에 집중한다.

## 권장 학습 순서

1. [문장 대조 번역·한국어 해설](Attention%20Is%20All%20You%20Need.번역.md)에서 용어와 논리 흐름을 읽는다.
2. 이 README의 수식을 종이에 shape와 함께 다시 쓴다.
3. 세 notebook을 순서대로 실행하고 assertion을 통과시킨다.
4. `QKᵀ`, mask, softmax, `V` 곱의 중간 tensor를 직접 출력한다.
5. PyTorch의 `scaled_dot_product_attention` 또는 `MultiheadAttention` 결과와 비교한다.
6. 마지막으로 작은 copy/reverse task를 학습해 causal mask 누락이 validation에 미치는 영향을 측정한다.

## 용어 정리

자세한 정의와 최초 등장 위치는 [번역 자료의 용어 사전](Attention%20Is%20All%20You%20Need.번역.md#약어-및-기술-용어-사전)을 참고한다.

## 다음 학습 경로

- pre-norm과 post-norm의 최적화 차이
- rotary positional embedding과 relative position bias
- grouped-query attention과 multi-query attention
- FlashAttention처럼 정확한 attention을 memory-efficient하게 계산하는 방법
- local, sparse, linear attention의 trade-off
- encoder-only, decoder-only, encoder-decoder 계열의 목적 함수 차이
- quantization, KV cache와 embedded inference의 latency·memory 분석
