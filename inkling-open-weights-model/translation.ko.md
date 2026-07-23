# Inkling: Our Open-Weights Model 한국어 학습 번역

작성일: 2026-07-23

## 원문 정보

- AlphaXiv URL: [https://www.alphaxiv.org/abs/2607.introducing-inkling](https://www.alphaxiv.org/abs/2607.introducing-inkling)
- AlphaXiv 페이지 제목: `Inkling: Our Open-Weights Model`
- 원문 발표문: [https://thinkingmachines.ai/news/introducing-inkling/](https://thinkingmachines.ai/news/introducing-inkling/)
- 모델 카드: [https://thinkingmachines.ai/model-card/inkling/](https://thinkingmachines.ai/model-card/inkling/)
- Hugging Face: [https://huggingface.co/thinkingmachines/Inkling](https://huggingface.co/thinkingmachines/Inkling)
- 원문 언어: 영어
- 접근일: 2026-07-23

AlphaXiv 상세 페이지는 직접 접근 시 제목과 `Loading...` 상태만 확인되었다. 따라서 이 문서는 연결된 공식 발표문과 모델 카드를 기준으로 원문 구조를 유지한 한국어 학습용 번역 요약이다. 원문 전문을 그대로 복제하지 않고 핵심 주장, 수치, 표의 의미를 보존했다.

## 제목과 도입

원문 제목은 "Inkling: Our Open-Weights Model"이다. 한국어로는 "Inkling: 우리의 오픈 웨이트 모델" 또는 "Inkling: Thinking Machines Lab의 오픈 웨이트 모델"로 옮길 수 있다.

Thinking Machines Lab은 인간의 의지와 판단을 확장하는 AI를 만들겠다는 목표 아래, 모델 커스터마이징 플랫폼 Tinker와 협업형 AI 시스템을 공개해 왔다. 이번 발표의 핵심은 처음부터 직접 학습한 모델의 full weights를 공개해 사용자가 자기 목적에 맞게 모델을 바꿀 수 있게 한다는 점이다.

Inkling은 975B total parameters와 41B active parameters를 가진 Mixture-of-Experts Transformer다. 최대 1M token context window를 지원하고, text, image, audio, video를 포함한 45T tokens로 사전학습되었다. 함께 Inkling-Small preview도 공개되었는데, 이는 276B total, 12B active parameters를 가진 더 가벼운 모델이다.

원문은 Inkling이 현재 공개·비공개 모델 전체에서 가장 강한 모델이라고 주장하지 않는다. 대신 multimodal capability, controllable thinking effort, Tinker 기반 fine-tuning 가능성을 조합해 커스터마이징에 좋은 open-weights base model이라고 설명한다.

## 자기 fine-tuning 데모

발표문은 Inkling이 Tinker를 사용해 자기 자신을 fine-tune하는 데모를 보여 준다. 목표는 "응답에서 알파벳 e를 쓰지 않는 lipogram model"이 되는 것이다.

데모 흐름은 다음과 같다.

1. Inkling이 objective와 scoring function을 작성한다.
2. Tinker로 fine-tuning job을 실행한다.
3. base model 대비 목표 행동이 개선되었는지 평가한다.
4. 새 checkpoint로 전환한다.

이 데모의 의미는 Inkling이 단순히 채팅만 하는 모델이 아니라, fine-tuning workflow를 코드로 구성하고 평가까지 연결할 수 있다는 점이다. 실제 production에서 자기 수정 모델을 그대로 쓰라는 뜻보다는, Tinker를 통한 customization loop를 보여 주는 예시로 이해하는 것이 안전하다.

## Capabilities

### Generalist model

Inkling은 agentic reasoning, coding, instruction following, factuality, vision, audio 등 여러 영역에서 균형 잡힌 성능을 목표로 훈련되었다. 원문은 이 breadth가 customization에 중요하다고 설명한다. 실제 사용자는 단일 benchmark 점수보다 다양한 workflow에 맞게 모델을 조정할 수 있는 유연성을 필요로 하기 때문이다.

### Agentic coding and tool use

Inkling은 coding agent와 tool-use harness 안에서 동작하도록 학습되었다. 훈련 중 tool set과 schema를 무작위화해 특정 harness에 과하게 의존하지 않도록 했다고 설명한다.

발표문은 one-shot web app 생성, browser-use agent가 폼을 채우는 예, cohesive PDF artifact 생성, long refinement loop를 통한 multiplayer snake game 구현 같은 데모를 제시한다. Design Arena Agentic Web Dev leaderboard에서도 open-weights 모델 중 강한 위치에 있다고 설명한다.

### Controllable thinking effort

Inkling은 effort setting을 조절해 성능과 token efficiency 사이의 tradeoff를 선택할 수 있다. 원문은 Terminal Bench 2.1, Humanity's Last Exam, IFBench에서 effort-performance curve를 보여 준다. 예시로 Terminal Bench에서 Nemotron 3 Ultra와 같은 성능에 도달하는 데 약 1/3 수준의 토큰을 쓴다고 설명한다.

실무적으로 이는 "모든 요청에 항상 최대 추론"을 쓰지 않고, 비용·latency·정확도 요구사항에 따라 effort를 선택할 수 있다는 뜻이다.

### Multimodality

Inkling은 text, image, audio를 입력으로 받아 text output을 생성한다. 발표문은 speech transcription, spoken instruction following, audio recording question answering, long-form audio reasoning, chart/diagram/math visual reasoning을 주요 capability로 든다.

Vision 쪽에서는 이미지 patch를 모델 hidden space로 옮기고, audio 쪽은 dMel spectrogram 또는 모델 카드의 표현상 discrete token encoding을 통해 처리한다고 설명된다. 두 공식 문서의 표현이 조금 다르므로 실제 구현 세부사항은 모델 카드와 릴리스 코드를 같이 확인해야 한다.

### Epistemics

원문은 calibration, instruction following, censorship resistance를 묶어 epistemics라고 부른다. 사실성을 위해서는 지식 암기만으로 부족하고, 모델이 자기 확신을 적절히 표현해야 한다고 설명한다.

Forecasting과 factual QA에서 제대로 모를 때 "모른다"거나 hedged answer를 내는 능력, rubric grader와 claims grader를 함께 사용해 helpfulness와 hallucination reduction을 동시에 노리는 학습 등이 언급된다.

### Safety

Inkling은 text, image, audio modality 전반에 대해 내부 safety spec에 맞춰 학습되었고 외부 safety tester 검증을 거쳤다고 한다. 평가 영역에는 CBRN, cyber, loss of control, sycophancy, vulnerable users, harmful manipulation 등이 포함된다.

모델 카드는 Inkling이 open-weight ecosystem에서 이미 사용 가능한 수준을 넘어서는 material uplift risk를 보이지 않았다고 결론 내린다. 다만 harmful topic이 role-play나 우회 표현으로 제시될 때 occasional compliance가 생길 수 있어, downstream deployer가 defense-in-depth를 적용해야 한다고 권고한다.

## Benchmarking Inkling

발표문은 모든 evaluation을 effort 0.99와 temperature 1.0에서 수행했다고 설명한다. coding eval에는 256K max-token trajectory limit이 사용되었다.

대표 수치는 다음과 같다. 모두 발표문과 모델 카드 기준이며, 확인일은 2026-07-23이다.

| 영역 | 지표 | Inkling |
| --- | --- | --- |
| Reasoning | HLE text only | 29.7% |
| Reasoning | HLE with tools | 46.0% |
| Reasoning | AIME 2026 | 97.1% |
| Reasoning | GPQA Diamond | 87.2% |
| Agentic coding | SWEBench Verified | 77.6% |
| Agentic coding | SWEBench Pro Public | 54.3% |
| Agentic coding | Terminal Bench 2.1 Best Harness | 63.8% |
| Vision | MMMU Pro Standard 10 | 73.5% |
| Vision | Charxiv RQ with python | 82.0% |
| Audio | MMAU | 77.2% |
| Audio | VoiceBench | 91.4% |
| Safety | FORTRESS Adversarial | 78.0% |
| Safety | StrongREJECT | 98.6% |

원문은 외부 모델의 경우 externally reported evaluations를 사용한 항목이 있고, 일부 benchmark는 내부 harness 또는 self-reported number를 사용한다고 명시한다. 따라서 숫자는 절대적 서열보다 평가 조건과 함께 해석해야 한다.

## The Making of Inkling

### Architecture

Inkling은 sparse MoE feed-forward backbone을 가진 66-layer decoder-only Transformer다. 각 MoE layer는 256 routed experts와 2 shared experts를 가지며, token마다 6 routed experts가 선택된다.

Attention은 sliding-window와 global layer를 5:1 비율로 섞고, 8 KV heads를 사용한다. 위치 표현에는 RoPE 대신 relative positional embedding을 사용한다. 또한 attention과 MLP residual branch 주변에 short convolution을 넣어 효율성과 long-context 성능을 노린다.

### Training

사전학습은 text, image, audio, video를 포함한 45T tokens로 수행되었다. 최적화는 큰 matrix weight에 Muon, 다른 parameter에 Adam을 사용하는 hybrid 방식이다. Weight decay는 learning rate의 제곱에 결합되어 긴 training horizon에서도 weight scale을 안정적으로 유지하도록 했다고 설명된다.

Post-training은 math, agentic code/tool use, audio, image, chat, safety에 걸쳐 넓게 수행되었다. 초기 SFT는 Kimi K2.5 같은 open-weights model이 생성한 synthetic data를 일부 사용했고, 대부분의 compute는 large-scale RL에 투입되었다.

### RL at scale

원문은 asynchronous RL을 30M+ rollouts까지 확장했고, AIME, HLE, GPQA 등을 포함한 held-out aggregate reasoning eval reward가 log-linear하게 개선되었다고 설명한다. 또한 effort level을 system message와 per-token cost로 조절해, 모델이 서로 다른 rollout에서 서로 다른 양의 token을 쓰도록 학습했다고 한다.

RL이 진행되면서 chain-of-thought가 더 간결해지는 현상도 관찰되었다. 이는 reward가 직접 목표로 삼은 것이 아니라 efficiency 압력에서 나온 compression으로 해석된다.

## Inkling-Small

Inkling-Small은 Inkling과 함께 preview로 소개된 더 가벼운 모델이다. 276B total parameters, 12B active parameters를 가지며, reasoning과 agentic task의 일부 benchmark에서 Inkling에 가까운 성능을 보인다.

원문은 Inkling-Small이 cost와 latency가 중요한 coding, LLM grading, synthetic data generation workload에 적합하다고 설명한다. 다만 full weights는 아직 테스트 완료 후 공개 예정이라고 명시한다.

## Customizing Inkling

Thinking Machines Lab은 많은 real-world problem이 generalist model만으로 충분히 해결되지 않으며, 조직의 특수 지식과 목적을 반영한 fine-tuning이 gap을 줄인다고 본다.

Inkling은 Tinker에서 fine-tuning 가능하고, Tinker console의 Inkling Playground에서 대화형으로 시험해 볼 수 있다. 또한 Together AI, Fireworks, Modal, Databricks, Baseten 같은 provider API와 SGLang, vLLM, TokenSpeed, Unsloth, Hugging Face integration이 언급된다.

모델의 full weights는 Hugging Face에 original checkpoint와 NVIDIA Blackwell system용 NVFP4 checkpoint로 제공된다고 한다.

## 모델 카드에서 확인한 배포 조건

모델 카드는 self-hosting에 필요한 하드웨어를 구체적으로 제시한다.

| Checkpoint | 최소 VRAM 조건 |
| --- | --- |
| BF16 | 최소 2TB aggregated VRAM, 예: 8x NVIDIA B300 또는 16x NVIDIA H200 |
| NVFP4 | 최소 600GB aggregated VRAM, 예: W4A4 4x NVIDIA B300 또는 W4A16 8x NVIDIA H200 |

Required software로는 SGLang, vLLM, TokenSpeed, Unsloth, Hugging Face 및 각 dependency가 언급된다. 따라서 로컬 소비자용 GPU에서 바로 실행하는 모델이라기보다, 대규모 inference cluster 또는 provider API를 전제로 한 모델로 이해해야 한다.

## Bias, Risks, Limitations

Inkling도 다른 foundation model과 마찬가지로 hallucination, instruction following 실패, 긴 multi-turn 대화 성능 저하, training data bias, 언어·문화·도메인별 성능 격차를 가질 수 있다.

모델 카드는 의료, 법률, safety-critical decision-making처럼 높은 책임이 필요한 분야에서는 추가 fine-tuning, domain-specific validation, human oversight 없이 사용하지 말 것을 권고한다. 또한 open deployment에서는 moderation, rate limiting, monitoring 같은 application-layer safeguards가 필요하다.
