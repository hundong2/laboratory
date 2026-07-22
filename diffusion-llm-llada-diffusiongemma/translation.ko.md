# 원문 한국어 학습용 재구성본

원문: [확산 언어 모델(Diffusion LLM)의 개념과 동작에 대한 연구 정리: LLaDA에서 DiffusionGemma까지](https://discuss.pytorch.kr/t/diffusion-llm-llada-diffusiongemma/11311)

- 원문 언어: 한국어
- 작성자: 9bow(박정환)
- 게시일: 2026-07-20
- 확인일: 2026-07-22

원문이 한국어이므로 직역본이 아니라 섹션의 흐름, 주요 모델과 연구 주제를 보존한 교정·학습용 재구성본입니다. 개별 논문의 상세 수치와 그림은 원문 및 연결된 1차 자료를 확인하세요.

## 확산 언어 모델이란 무엇인가

주류 LLM은 token을 왼쪽에서 오른쪽으로 하나씩 예측합니다. dLLM은 답변 영역을 mask 상태로 두고 여러 번 denoising하며 여러 token을 병렬로 복원합니다.

AR은 순차성 때문에 길이에 따라 latency가 증가하고, 이미 쓴 앞부분을 뒤에서 수정하기 어렵습니다. dLLM은 한 forward pass에서 여러 token을 예측하고 전체 구조를 오가며 수정할 수 있지만, 반복 full-sequence 계산과 cache 문제가 새로 생깁니다.

## 확산 개념을 언어로 옮기기

Image diffusion은 clean image에 Gaussian noise를 더하는 forward process와 이를 걷어내는 reverse process를 학습합니다. Text는 이산적이므로 token을 `[MASK]`로 바꾸는 categorical corruption을 사용합니다.

LLaDA 계열은 `t`에 따라 각 token을 독립 masking합니다. Mask predictor는 모든 mask 위치를 동시에 예측하고, 학습 loss는 mask token에 대한 가중 cross-entropy입니다. Sampling은 전체 mask에서 시작해 예측과 remasking을 반복합니다.

BERT MLM과 닮았지만 BERT는 고정된 소수 mask의 representation learning이고, masked diffusion은 다양한 noise level과 반복 reverse process를 통해 전체 sequence를 생성하는 확률 model을 목표로 합니다.

## 양방향 attention과 KV cache

dLLM은 mask의 양쪽 문맥을 모두 사용하므로 bidirectional attention을 씁니다. 이것이 parallel restoration을 가능하게 하지만 step마다 canvas 전체 표현이 바뀔 수 있어 AR의 KV cache를 그대로 재사용하기 어렵습니다.

LLaDA는 confidence가 낮은 token을 다시 mask하고 높은 confidence token부터 확정합니다. Step 수가 많으면 품질이 좋아질 수 있지만 latency가 늘어납니다.

## Block diffusion

Response를 여러 block으로 나눠 block 안은 양방향 diffusion, block 사이는 왼쪽→오른쪽으로 진행합니다. 이 hybrid는 prompt와 이전 block에 KV cache를 사용하면서 현재 block에서는 병렬성을 얻습니다. LLaDA의 semi-autoregressive sampling과 DiffusionGemma, Nemotron 및 여러 가속 연구가 이 구조를 사용합니다.

## 기반 모델의 지형

### LLaDA

LLaDA는 8B masked diffusion model을 처음부터 2.3T token으로 pretraining하고 4.5M pair로 SFT했습니다. Scaling, in-context learning과 instruction following이 AR에만 고유하지 않다는 가능성을 제시합니다.

Random mask ratio, bidirectional Transformer, mask-only cross-entropy와 iterative remasking이 핵심입니다. Reversal task의 양방향 성질도 강조하지만 generation length, KV cache와 alignment 측면의 한계가 있습니다.

### Dream 7B와 Dream-Coder

Dream은 Qwen2.5-7B weight에서 시작해 diffusion으로 계속 학습합니다. Shift operation으로 기존 next-token 지식을 보존하고 CART로 token별 context에 맞는 noise level을 사용합니다. Dream-Coder는 code 특화 AR model을 초기화로 쓰고 verifiable reward RL을 더합니다.

### Mercury

Mercury는 전용 inference engine과 OpenAI-compatible API를 갖춘 상용 code dLLM입니다. 높은 reported speed가 특징이지만 parameter, training data와 sampler 세부가 모두 공개되지는 않아 동일 조건 재현에는 한계가 있습니다.

### DiffusionGemma

Gemma 4 MoE 기반 open-weight multimodal dLLM입니다. Encoder와 decoder가 weight를 공유하지만 encoder는 causal attention과 KV cache로 prompt/commit block을 처리하고 decoder는 bidirectional attention으로 256-token canvas를 반복 복원합니다.

Self-conditioning, entropy-bounded denoising과 adaptive stopping을 사용하고 최대 48 step을 둡니다. 같은 계열 AR model보다 여러 quality benchmark는 낮지만 low batch에서 높은 per-user throughput을 목표로 합니다.

vLLM은 Model Runner V2의 state abstraction과 speculative decoding data path를 활용해 DiffusionGemma를 첫 native dLLM으로 통합했습니다.

### Nemotron Diffusion

하나의 model이 AR, diffusion, self-speculation decoding을 지원합니다. Joint AR+diffusion objective로 학습하고 diffusion mode가 여러 token draft를 만들며 AR mode가 검증합니다. 별도 draft model 없이 KV cache를 공유하는 hybrid입니다.

## 어떤 token을 먼저 여는가

Standard sampler는 현재 confidence나 entropy로 확정 위치를 고릅니다. 더 최근 연구는 여러 step prediction의 trajectory consistency, confidence gap을 이용한 early stopping과 task-aware order를 연구합니다.

Constraint satisfaction task에서는 confidence-based order가 어려운 infilling을 피하는 데 도움이 될 수 있습니다. 반면 math/code에서는 쉬운 token을 먼저 확정하다 중요한 high-entropy branch를 우회해 solution diversity가 줄 수 있다는 반론이 있습니다. Any-order의 효용은 task dependent입니다.

## 추론 가속

가속 연구는 다음 병목을 다룹니다.

- 변화하지 않는 token representation cache
- 중요한 token만 다시 계산하는 saliency selection
- long-context block attention cache
- adaptive stopping으로 불필요한 denoising step 제거
- dynamic expert sharing으로 MoE memory와 parallelism 분리
- diffusion block을 speculative draft로 활용

Pass 수 감소와 step당 계산 감소는 결합할 수 있지만, 보고된 배수는 hardware·batch·precision·baseline과 quality 조건을 확인해야 합니다.

## 투명성과 안전성

DiffusionGemma는 step 사이 self-conditioning vector가 opaque reasoning channel인지가 논점입니다. 이를 해석 불가능하다고 보면 AR보다 긴 opaque serial path가 생기지만, logit lens 분석에서는 많은 정보가 현재/인접 final token을 가리킨다는 주장도 있습니다.

여러 canvas 사이 진행이 AR이라는 점과 현재 training recipe에 결론이 의존할 수 있어, dLLM이 본질적으로 더 투명하거나 불투명하다고 단정하기는 이릅니다.

## 강화학습과 preference optimization

dLLM은 sequence likelihood가 intractable해 DPO/GRPO에 필요한 log probability를 정확히 얻기 어렵습니다. ELBO와 Monte Carlo 근사는 variance와 bias를 만듭니다.

- VRPO는 sampling budget 배치와 antithetic sampling으로 variance를 줄임
- diffu-GRPO는 mean-field와 random prompt masking으로 policy gradient를 근사
- 후속 연구는 token credit, trajectory marginalization과 off-policy bias를 개선
- JustGRPO는 training policy만 AR order로 제한해 표준 GRPO를 적용

각 연구의 baseline과 sampler가 달라 절대 수치를 직접 비교하면 안 됩니다.

## 종합 전망

dLLM은 AR을 즉시 대체하는 단일 기술이라기보다 새로운 decoding axis입니다. Constraint completion, infilling과 low-concurrency latency에서는 장점이 보이지만 범용 quality, likelihood-based alignment와 serving ecosystem은 AR이 성숙합니다.

가장 현실적인 흐름은 두 paradigm을 결합하는 것입니다. Prompt와 과거 block에는 AR/KV cache를 사용하고, 현재 block은 diffusion으로 복원하거나, diffusion draft를 AR이 검증합니다. 앞으로의 비교는 “AR 대 diffusion”보다 workload별 block size, decoding order, cache와 verification의 조합을 중심으로 이뤄질 가능성이 큽니다.

## 확인 시 주의

게시글은 2026-07-20 당시의 폭넓은 연구 지형을 정리합니다. Model revision과 serving 지원은 빠르게 바뀌므로 실행 전 모델 카드와 runtime 공식 문서를 다시 확인해야 합니다. 상용 model의 reported throughput과 서로 다른 논문의 benchmark는 동일 조건 비교가 아닙니다.
