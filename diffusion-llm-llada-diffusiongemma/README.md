# 확산 언어 모델: LLaDA에서 DiffusionGemma까지

작성일: 2026-07-22

## 출처와 작업 범위

- 원문: [확산 언어 모델(Diffusion LLM)의 개념과 동작에 대한 연구 정리: LLaDA에서 DiffusionGemma까지](https://discuss.pytorch.kr/t/diffusion-llm-llada-diffusiongemma/11311)
- 작성자: 9bow(박정환)
- 게시일: 2026-07-20
- 원문 언어: 한국어
- 확인일: 2026-07-22
- 학습용 재구성본: [translation.ko.md](translation.ko.md)
- 핵심 1차 자료: [LLaDA 논문](https://arxiv.org/abs/2502.09992), [DiffusionGemma 모델 카드](https://huggingface.co/google/diffusiongemma-26B-A4B-it), [vLLM 통합 글](https://vllm.ai/blog/2026-06-10-diffusion-gemma)

원문은 확산 LLM의 기초부터 모델 계보, 디코딩, 추론 가속과 강화학습까지 광범위한 연구를 연결한 한국어 survey 형식의 게시글입니다. 이 문서는 핵심 개념과 비교 축을 다시 구성하고, 수치는 각 연구가 보고한 조건에 종속된다는 점을 명시합니다.

## 한눈에 보기

자기회귀 언어 모델은 왼쪽에서 오른쪽으로 토큰 하나씩 생성합니다. 확산 언어 모델(dLLM)은 답변 공간 전체 또는 일정한 block을 mask/noise 상태로 시작하고, 여러 위치를 동시에 반복 복원합니다.

```text
자기회귀(AR)
[확정] [확정] [다음?] [ ] [ ]  → 한 토큰씩 진행

마스킹 확산
[MASK] [MASK] [MASK] [MASK] [MASK]
  → 여러 위치 예측 → 불확실 위치 재마스킹
  → 여러 위치 예측 → 점진적 확정
```

매 forward pass에서 여러 토큰을 확정할 수 있다는 것이 잠재적 속도 이점입니다. 그러나 양방향 attention으로 매 단계 전체 canvas를 다시 계산하고 전통적인 AR KV cache를 그대로 쓰기 어려워, **병렬 생성 가능성 자체가 wall-clock 가속을 보장하지는 않습니다.**

현재 실용적 방향은 순수 확산보다 block diffusion 또는 hybrid입니다.

- block 안: 양방향 병렬 복원
- block 사이: 왼쪽에서 오른쪽으로 commit
- prompt와 이전 block: encoder KV cache 재사용
- 불확실도에 따라 token 순서와 종료 단계 동적 결정

## 기초 개념

### 자기회귀 언어 모델

Sequence 확률을 chain rule로 분해합니다.

```text
p(x1, x2, ..., xL) = p(x1) p(x2|x1) ... p(xL|x< L)
```

장점은 likelihood 계산이 쉽고, 이미 확정한 token의 key/value를 KV cache에 저장해 다음 step에서 재사용할 수 있다는 점입니다. 단점은 token 의존성이 본질적으로 순차적이라는 점입니다.

### 연속 확산과 이산 확산

Image diffusion은 clean data에 Gaussian noise를 점진적으로 더하는 forward process와 noise에서 data를 복원하는 reverse process를 짝지어 학습합니다.

Text token은 이산적이므로 Gaussian noise 대신 categorical corruption을 사용합니다. 대표적인 absorbing-state diffusion은 token을 특별한 `[MASK]` 상태로 바꾸고 reverse process가 원래 token을 예측합니다.

### LLaDA의 masking process

LLaDA는 시간 `t ∈ [0, 1]`를 뽑고 각 token을 확률 `t`로 독립 masking합니다.

- `t = 0`: 거의 clean sequence
- `t = 1`: 전체 mask
- training: mask된 위치에만 cross-entropy, `1/t` 가중
- sampling: 전체 mask response에서 시작해 반복 예측과 remasking

LLaDA 논문은 이 loss를 model negative log-likelihood의 upper bound와 연결합니다. BERT의 고정 약 15% MLM은 representation learning 목적이고, masked diffusion은 다양한 mask ratio와 반복 reverse process로 전체 문장을 생성하는 generative model이라는 점이 다릅니다.

### 양방향 attention

dLLM mask predictor는 각 mask를 채울 때 왼쪽과 오른쪽 문맥을 모두 봅니다. Causal mask가 없는 양방향 attention이 any-order 생성과 전체 구조 수정 가능성을 주지만, 매 denoising step에 token 표현이 바뀔 수 있어 AR 방식 KV cache를 그대로 적용하기 어렵습니다.

### Remasking

한 step에서 모든 mask 위치의 token distribution을 예측한 뒤 일부만 확정하고 나머지는 다시 mask합니다.

- random: 이론적 reverse schedule에 맞춘 무작위 선택
- low confidence: 최대 확률이 낮은 token을 다시 mask
- entropy: 불확실성이 큰 token을 다시 mask
- confidence margin: 1위와 2위 확률 차이가 큰 위치부터 확정
- trajectory consistency: 여러 step에 걸쳐 예측이 일관된 위치만 확정

Sampling step과 generation length는 품질·속도 trade-off를 만드는 hyperparameter입니다.

## 핵심 요약

### AR과 dLLM 비교

| 축 | 자기회귀 LLM | 마스킹 확산 LLM |
|---|---|---|
| 생성 순서 | 왼쪽→오른쪽 고정 | 여러 위치를 병렬·임의 순서로 복원 |
| attention | causal | 양방향 |
| 한 pass의 후보 | 보통 다음 token 1개 | mask 위치 전체 |
| KV cache | 자연스럽게 적용 | 전체 canvas 순수 확산에서는 어려움 |
| likelihood | chain rule로 정확 계산 | ELBO/Monte Carlo 근사 필요 |
| 길이 | EOS까지 동적 | 초기 canvas 길이 또는 block 정책 필요 |
| 강점 후보 | 고품질 범용 생성, 성숙한 serving | 낮은 batch latency, infilling, 제약 충족, 수정 |
| 병목 | 순차성, memory bandwidth | 반복 full pass, sampling schedule, cache |

### 세대별 모델

| 모델 | 접근 | 핵심 의미 |
|---|---|---|
| LLaDA 8B | 처음부터 masked diffusion으로 2.3T token pretraining | 비-AR도 scale, ICL, instruction following이 가능하다는 존재 증명 |
| Dream 7B | Qwen2.5-7B AR weight에서 diffusion continual training | 기존 AR 지식 재사용, shift operation과 CART |
| Mercury | 상용 code dLLM과 전용 engine | 병렬성을 실제 wall-clock throughput으로 전환하려는 제품화 |
| DiffusionGemma | Gemma 4 MoE 기반 multimodal block diffusion | shared encoder/decoder mode, multi-canvas와 vLLM native serving |
| Nemotron Diffusion | AR·diffusion·self-speculation 3-mode | 같은 model이 workload에 따라 decoding mode 전환 |

## 상세 정리

### 1. LLaDA: 처음부터 학습한 8B dLLM

LLaDA는 vanilla Transformer mask predictor를 causal mask 없이 학습합니다. 8B model은 2.3T token과 약 0.13M H800 GPU hour로 pretraining하고, 4.5M pair로 SFT했습니다. SFT에서는 prompt는 clean하게 두고 response만 masking합니다.

논문의 핵심 주장은 scalability, in-context learning, instruction following이 AR 구조에만 고유한 성질이 아니라 적절한 generative modeling과 scale에서 나올 수 있다는 것입니다.

주의할 점:

- LLaDA와 다른 model은 training data와 post-training recipe가 다릅니다.
- 일부 benchmark 우위가 architecture 자체만의 인과 효과라고 단정할 수 없습니다.
- generation length가 hyperparameter이고 전통적 KV cache가 없습니다.
- 원 논문의 SFT model은 RL alignment를 사용하지 않았습니다.

### 2. Dream: AR knowledge를 diffusion으로 이전

Dream 7B는 Qwen2.5-7B weight로 초기화해 diffusion objective로 이어 학습합니다.

- **shift operation**: 기존 hidden state가 다음 위치를 예측하던 구조를 유지해 AR knowledge 손상을 줄임
- **CART**: 주변 clean context 양에 따라 token별 noise level을 조절

AR 초기화는 training compute를 절감할 수 있지만 learning rate가 너무 크면 기존 왼쪽→오른쪽 지식이 빠르게 손상될 수 있습니다.

### 3. Block diffusion

전체 response를 한꺼번에 복원하는 대신 고정 크기 block/canvas로 나눕니다.

```text
prompt prefill(KV)
  → block 1 전체 병렬 denoise → commit
  → block 2 전체 병렬 denoise → commit
  → ...
```

이는 AR과 diffusion 사이의 spectrum입니다. Block 크기 1이면 AR에 가까워지고, 전체 길이면 순수 diffusion에 가까워집니다. Block size는 parallelism, denoising 난이도, cache 재사용과 memory를 함께 바꿉니다.

### 4. DiffusionGemma

원문이 인용한 모델 카드 기준 사양:

- 전체 parameter 25.2B, 활성 3.8B
- 128 expert 중 8개 활성 + shared expert
- 30 layer
- canvas length 256
- context 최대 256K
- text/image/video input

Encoder와 decoder가 weight를 공유하되 mode가 다릅니다.

- encoder mode: causal attention으로 prompt와 commit block을 처리하고 KV cache 유지
- decoder mode: bidirectional attention으로 현재 canvas 반복 복원
- self-conditioning: 이전 step의 softmax 정보를 다음 step에 입력
- entropy-bounded denoising과 adaptive stopping
- 최대 denoising step 48

모델 카드 비교에서는 같은 계열 AR Gemma 4보다 여러 품질 benchmark가 낮은 대신, low batch에서 높은 per-user generation throughput을 목표로 합니다. 이 결과는 H100/H200, FP8, batch size 1과 vLLM Model Runner V2 같은 특정 조건에 종속됩니다.

### 5. vLLM serving

DiffusionGemma는 vLLM이 native로 지원한 첫 dLLM으로 소개됩니다. Standard AR loop와 다른 iterative model state를 관리하기 위해 ModelState abstraction을 사용하고, canvas를 speculative decoding의 draft set처럼 다뤄 일부 기존 data path를 재사용합니다.

Prompt encoder가 AR KV cache를 사용하므로 prefix caching도 가능합니다. 다만 canvas 내부의 양방향 반복 연산까지 일반 AR KV cache가 해결해 주는 것은 아닙니다.

### 6. Decoding order

어떤 token을 먼저 확정할지가 품질을 크게 좌우합니다.

- 쉬운 위치부터 풀면 어려운 infilling subproblem을 우회할 수 있습니다.
- Sudoku 같은 constraint satisfaction에서는 confidence margin order가 random order보다 크게 유리하다는 보고가 있습니다.
- 반대로 math/code reasoning에서는 쉬운 token부터 채우면서 중요한 high-entropy branch를 우회해 solution diversity가 줄 수 있다는 “flexibility trap” 반론도 있습니다.

따라서 any-order가 항상 좋다는 결론은 잘못입니다. Task 구조와 평가 목표에 따라 AR order, confidence order, hybrid order를 비교해야 합니다.

### 7. 추론 가속 축

가속은 서로 다른 축에서 일어납니다.

1. **Step 수 감소**: adaptive stopping, early answer convergence
2. **Step당 계산 감소**: 변하지 않은 token/cache 재사용, saliency token selection
3. **Pass당 commit 증가**: parallel decoding, larger block
4. **Serving 효율**: paging, dynamic batching, custom kernel, MoE routing
5. **Hybrid verification**: diffusion draft + AR verification

논문에서 “몇 배 가속”을 볼 때는 baseline, batch size, hardware, precision, output length, 품질 유지 조건을 함께 확인해야 합니다.

### 8. 강화학습과 선호 최적화

dLLM은 완성 sequence likelihood를 chain rule로 쉽게 계산하지 못해 RL/DPO에 추가 문제가 생깁니다.

- LLaDA 1.5/VRPO: ELBO 기반 preference score의 variance와 bias를 줄임
- d1/diffu-GRPO: mean-field와 random prompt masking으로 log probability를 싸게 근사
- GDPO 계열: diffusion trajectory의 token credit와 off-policy bias 개선 시도
- JustGRPO: RL training 동안 AR order policy를 사용해 표준 GRPO를 단순 적용

연구별 sampler, evaluation과 baseline이 다르므로 같은 model 이름의 숫자를 직접 나란히 비교하면 안 됩니다.

## 실무 평가 체크리스트

- [ ] 실제 use case가 low-concurrency latency인지 high-throughput serving인지 구분했는가?
- [ ] 동일 hardware, precision, batch, output length에서 AR과 비교했는가?
- [ ] tokens/s가 확정 token 기준인지 예측 후보 token 기준인지 확인했는가?
- [ ] quality를 같은 decoding budget과 benchmark protocol로 비교했는가?
- [ ] denoising step, block size, remask strategy를 기록했는가?
- [ ] prompt KV cache와 canvas 내부 cache를 구분했는가?
- [ ] EOS·PAD·고정 canvas length의 낭비를 측정했는가?
- [ ] early stopping이 열린 생성에서도 안전한지 검증했는가?
- [ ] any-order가 solution diversity를 떨어뜨리지 않는지 pass@k로 확인했는가?
- [ ] 모델 카드와 상용 보고의 비공개 조건을 한계로 기록했는가?

## 논문과 수치를 읽을 때 주의할 점

- 서로 다른 연구의 benchmark 숫자는 model revision, prompt, sampler와 평가 harness가 다릅니다.
- 병렬로 여러 token을 예측해도 반복 step에서 다시 바뀌는 token은 최종 throughput에 포함하면 안 됩니다.
- Batch size 1 speedup은 high-concurrency server의 총 처리량 우위와 다릅니다.
- DiffusionGemma 품질·속도 수치는 공개 model card와 특정 vLLM engine 조건의 보고입니다.
- 순수 diffusion, block diffusion, self-speculation을 모두 “dLLM 속도” 하나로 묶지 않아야 합니다.
- 해석 가능성 연구는 self-conditioning vector를 해석 가능하게 볼지에 따라 결론이 크게 달라집니다.
- 현재 분야는 빠르게 변하고 있어 model/API 지원 상태를 실행 시점에 다시 확인해야 합니다.

## 용어 정리

| 용어 | 뜻 |
|---|---|
| dLLM | 반복 denoising으로 text를 생성하는 diffusion language model |
| absorbing state | token이 들어가면 forward process에서 떠나지 않는 `[MASK]` 상태 |
| mask predictor | 현재 mask sequence에서 원래 token을 예측하는 network |
| denoising step | mask/noise를 줄이는 한 번의 반복 |
| remasking | 불확실한 예측을 다음 step을 위해 다시 mask하는 처리 |
| canvas | block diffusion이 한 번에 복원하는 token 영역 |
| self-conditioning | 이전 step의 distribution/hidden signal을 다음 step에 재사용 |
| adaptive stopping | 수렴 신호를 보고 최대 step 전에 종료하는 전략 |
| block diffusion | block 안은 diffusion, block 사이는 AR인 hybrid 생성 |
| any-order generation | 고정된 왼쪽→오른쪽이 아닌 순서로 token을 확정하는 생성 |
| flexibility trap | 쉬운 위치 우선이 중요한 불확실한 branch 다양성을 없앨 수 있는 현상 |
| self-speculation | 같은 model의 diffusion mode가 draft하고 AR mode가 검증하는 방식 |

## 실습 학습 가이드

1. [`01_foundations.ipynb`](01_foundations.ipynb): mask ratio `t`에 따른 이산 forward corruption을 구현합니다.
2. [`02_practice.ipynb`](02_practice.ipynb): 여러 위치를 예측하고 confidence가 높은 token부터 확정하는 반복 denoising을 실습합니다.
3. [`03_advanced.ipynb`](03_advanced.ipynb): AR, 순수 diffusion, block diffusion의 pass 수와 병렬 commit, adaptive stopping 효과를 비교합니다.

모든 notebook은 Python 표준 라이브러리만 사용하며 실제 model weight나 GPU가 필요하지 않습니다. 실제 학습이 아니라 algorithm의 제어 흐름을 이해하는 toy simulation입니다.

## 다음 학습 경로

1. LLaDA 논문의 forward/reverse process와 loss upper bound를 읽습니다.
2. Mask ratio schedule과 remasking schedule을 분리해 구현합니다.
3. Random, max probability, entropy, margin order를 동일 toy task에서 비교합니다.
4. Block size와 denoising step을 바꾸며 theoretical pass 수와 실제 latency를 함께 측정합니다.
5. DiffusionGemma model card와 vLLM integration의 정확한 runtime 조건을 재현합니다.
6. Constraint task와 open-ended reasoning에서 any-order의 효과를 따로 평가합니다.
7. RL 연구는 likelihood estimator의 bias/variance와 sampler-policy mismatch부터 검토합니다.

## 참고 링크

- [PyTorchKR 원문](https://discuss.pytorch.kr/t/diffusion-llm-llada-diffusiongemma/11311)
- [LLaDA](https://arxiv.org/abs/2502.09992)
- [DiffusionGemma 모델 카드](https://huggingface.co/google/diffusiongemma-26B-A4B-it)
- [DiffusionGemma vLLM 통합](https://vllm.ai/blog/2026-06-10-diffusion-gemma)
- [Nemotron Diffusion 모델 카드](https://huggingface.co/nvidia/Nemotron-Labs-Diffusion-8B)
