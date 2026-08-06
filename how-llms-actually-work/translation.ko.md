# How LLMs Actually Work 한국어 번역 요약

작성일: 2026-08-06

## 원문 정보와 번역 범위

- 원문: [How LLMs Actually Work](https://www.0xkato.xyz/how-llms-actually-work/)
- 저자: 0xkato
- 게시일: 2026-06-01
- 원문 언어: 영어
- 접근일: 2026-08-06
- 페이지 표시: 26분 분량
- 확인된 저작권 표시: `0xkato © 2026`

별도 open license를 확인하지 못했으므로 원문 문장과 그림을 전문 복제하지 않습니다. 아래 내용은 원문의 section 순서, 주장과 예시의 의미를 보존한 한국어 번역 요약입니다.

## 소개

이 글은 현대 LLM이 어떻게 작동하는지 순서대로 설명합니다. 대부분의 현대 LLM은 Transformer block을 반복해서 쌓으므로, 그 내부 장치를 이해하면 전체 구조의 상당 부분을 파악할 수 있습니다. 복잡한 수식을 피한 입문 설명이지만, 실제 수학을 별도로 학습할 필요는 있습니다.

현대 모델은 대체로 Transformer 계열의 골격을 공유합니다. 차이는 학습 data, 규모와 configuration, 그리고 base model 위에 적용한 post-training에서 생깁니다.

## Tokenization

모델은 text를 직접 읽지 않고 integer ID를 읽습니다. Tokenizer는 문자열을 고정 vocabulary의 항목에 대응하는 정수 sequence로 변환합니다. Vocabulary는 대체로 수만에서 수십만 항목 규모입니다.

Token은 보통 완전한 word가 아니라 subword 조각입니다. Whole-word 방식은 vocabulary가 지나치게 커지고 새 word에 약하며, character 방식은 sequence가 너무 길어집니다. Subword는 두 극단 사이를 절충합니다.

이 차이는 철자 문제에서 드러납니다. 모델은 사람이 보는 letter를 직접 세는 것이 아니라 token ID를 처리합니다. Model family마다 tokenizer가 다르고, 선택은 계산량과 다국어 coverage에 영향을 줍니다.

## Embeddings

Token ID는 그 자체로 의미가 없는 row index입니다. Embedding matrix는 vocabulary 항목마다 긴 learned vector 하나를 저장합니다. ID를 입력하면 해당 row를 조회하며, vector 길이는 model hidden size입니다.

Training 과정에서 비슷한 문맥에 나타나는 token은 관련된 geometry를 형성합니다. 다만 이 단계의 embedding만으로 sequence의 어느 위치에 token이 있었는지는 알 수 없습니다.

## Positional encoding

Plain self-attention에는 word order가 내장되어 있지 않습니다. Original Transformer는 position마다 다른 sine·cosine pattern을 embedding에 더했습니다.

많은 현대 모델은 RoPE (Rotary Position Embeddings)를 사용합니다. RoPE는 위치에 따른 각도로 Query와 Key vector를 회전시킵니다. 두 token의 attention score에는 회전 차이가 반영되므로 상대 거리를 자연스럽게 표현할 수 있고 별도 learned parameter를 추가하지 않습니다.

Position encoding이 있어도 긴 prompt 중간의 정보를 덜 안정적으로 사용하는 “lost in the middle” 현상이 보고되었습니다. 중요한 정보를 처음이나 끝에 배치하는 prompt 전략은 이 관찰과 관련됩니다.

## Attention

Attention은 각 token이 볼 수 있는 다른 token 중 무엇이 중요한지 정하게 합니다. 각 token은 learned matrix를 통해 Query, Key, Value 세 vector로 변환됩니다.

- Query: 다른 token에서 어떤 정보를 찾는가
- Key: 찾는 대상과 어떻게 matching되는가
- Value: match가 강할 때 전달할 정보

Query와 Key의 scaled dot product로 match score를 만들고 softmax로 합이 1인 weight로 바꿉니다. 그 weight로 Value를 가중합하면 다른 token의 문맥 정보가 현재 token representation에 들어옵니다.

GPT식 decoder-only model은 왼쪽에서 오른쪽으로 생성하므로 causal mask로 미래 위치를 숨깁니다. 글은 반복 pattern을 찾아 이어 가는 induction head를 in-context learning의 구체적 mechanism 사례로 소개합니다.

Full attention은 모든 token pair를 비교하므로 긴 sequence에서 계산 비용이 빠르게 증가합니다. FlashAttention, sparse attention과 linear attention 연구는 이 부담을 줄이려는 접근입니다.

## Multi-head attention

언어에는 문법, 대명사 지시, 장거리 참조와 위치 관계가 동시에 존재합니다. Multi-head attention은 독립적인 learned projection을 사용하는 여러 attention pass를 병렬 실행합니다.

각 head는 원 token vector의 고정 조각을 단순히 받는 것이 아닙니다. 전체 vector를 각 head의 작은 Q·K·V 공간으로 투영합니다. Head 결과를 이어 붙인 다음 learned output projection으로 다시 full-size vector로 섞습니다.

생성 중에는 과거 token의 Key·Value를 KV cache에 저장합니다. GQA (Grouped-Query Attention)는 여러 query head가 더 적은 key/value head를 공유해 cache memory와 inference 비용을 줄입니다.

## Feed-forward network

Attention이 token 사이 정보를 교환한다면 FFN은 각 token vector를 독립적으로 처리합니다. 일반적으로 차원을 확장하고 nonlinear function을 적용한 뒤 원래 차원으로 줄입니다.

Nonlinearity가 없으면 연속된 linear layer는 하나의 linear transformation으로 합쳐집니다. Original Transformer는 ReLU를 사용했고 이후 GELU, 현대 LLM에서는 SwiGLU가 널리 쓰입니다.

Dense Transformer에서는 FFN이 parameter의 큰 비중을 차지합니다. 연구는 FFN activation과 특정 개념·사실의 연관, ROME 같은 targeted model editing을 탐구해 왔습니다. 다만 지식이 하나의 neuron에만 국소적으로 저장된다고 단순화해서는 안 됩니다.

MoE (Mixture of Experts)는 하나의 FFN 대신 여러 expert와 router를 두고 token마다 일부 expert만 실행합니다. 따라서 총 parameter는 크게 늘리면서 token당 활성 계산량은 더 느리게 증가시킬 수 있습니다.

## Residual stream과 layer normalization

Attention이나 FFN의 출력은 기존 token vector를 대체하지 않고 더해집니다. 이 residual connection은 정보와 gradient가 깊은 network를 통과하는 shortcut을 제공합니다. Layer가 쌓이며 갱신이 누적되는 경로를 residual stream이라고 설명합니다.

Normalization은 반복적인 addition 속에서 vector scale이 폭발하거나 사라지는 것을 막습니다. Original Transformer는 sublayer 뒤에 normalization하는 post-norm이었지만 많은 현대 모델은 sublayer 앞에 두는 pre-norm을 사용합니다.

LLaMA, Mistral, Gemma와 Phi 계열 등에 사용되는 RMSNorm은 평균을 빼는 단계를 생략하고 vector의 RMS scale을 조정합니다.

## Next-token prediction

모든 layer가 끝나면 생성 시 마지막 token 위치의 final vector를 vocabulary 크기의 logits로 바꿉니다. Softmax를 적용하면 다음 token probability distribution이 됩니다.

Temperature는 distribution의 sharpness를 조절하고 top-k와 top-p는 선택 후보를 제한합니다. Token 하나를 뽑아 입력 뒤에 붙이고, KV cache를 재사용해 다음 token을 예측합니다. 종료 token이나 길이 제한을 만날 때까지 반복합니다.

Base LLM의 핵심 training signal은 다음 token prediction입니다. Instruction following, 선호와 safety behavior는 이후 post-training에서 조정할 수 있습니다.

Speculative decoding은 작은 draft model이 여러 token을 제안하고 큰 model이 병렬 검증합니다. 올바른 acceptance scheme을 쓰면 큰 model 단독 실행과 같은 분포를 유지하면서 생성 속도를 높일 수 있습니다.

## Architecture와 trained weights

많은 현대 LLM은 tokenization, embedding, position encoding, attention·FFN block, residual stream, normalization과 next-token prediction이라는 넓은 구조를 공유합니다.

모델마다 달라지는 것은 다음과 같습니다.

- 서로 다른 data와 scale에서 학습된 weights
- layer 수, vocabulary, head, parameter, dense 또는 MoE 같은 configuration
- instruction tuning, human feedback 학습과 safety control 같은 post-training

최근 널리 채택된 선택에는 pre-norm, RMSNorm, RoPE, SwiGLU와 GQA가 있으며 큰 모델 일부는 MoE를 사용합니다. 이들은 2017년 architecture 위에서 여러 해 동안 축적된 개선입니다.

## 앞으로의 방향

Transformer 계열은 language뿐 아니라 vision, audio와 multimodal system에도 퍼졌습니다. 한편 Mamba 같은 state-space model과 hybrid architecture는 긴 sequence를 위한 대안으로 연구되고 있습니다.

Architecture가 달라지더라도 sequence를 표현 단위로 바꾸고, 의미와 순서를 표현하며, 멀리 떨어진 정보를 결합하고, 다음 출력을 계산해야 한다는 문제는 남습니다. 원문의 목표는 독자가 현대 model paper와 model card에서 각 설명이 architecture의 어느 부분을 가리키는지 알아볼 수 있게 하는 것입니다.

## 번역 검수 메모

- 원문의 section 순서를 유지했습니다.
- Q/K/V, RoPE, GQA, KV cache, FFN, MoE, RMSNorm과 decoding 용어를 일관되게 표기했습니다.
- 원문 그림은 복제하지 않고 설명된 관계만 요약했습니다.
- 특정 proprietary model 구조는 공개 범위가 다르다는 원문의 단서를 보존했습니다.

분석과 실습은 [`README.md`](README.md)에서 이어집니다.
