# Inkling 오픈 웨이트 모델

작성일: 2026-07-23

## 출처와 작업 범위

- 입력 URL: [https://www.alphaxiv.org/abs/2607.introducing-inkling](https://www.alphaxiv.org/abs/2607.introducing-inkling)
- 최종 확인 URL: [https://www.alphaxiv.org/abs/2607.introducing-inkling](https://www.alphaxiv.org/abs/2607.introducing-inkling)
- AlphaXiv 페이지 제목: `Inkling: Our Open-Weights Model`
- AlphaXiv 확인 범위: 상세 페이지는 제목과 `Loading...` 상태만 직접 확인되었다.
- 원문 언어: 영어
- 접근일: 2026-07-23
- 보조 원문: [Thinking Machines Lab 발표문](https://thinkingmachines.ai/news/introducing-inkling/), 2026-07-15 게시
- 모델 카드: [Inkling Model Card](https://thinkingmachines.ai/model-card/inkling/)
- 모델 페이지: [thinkingmachines/Inkling on Hugging Face](https://huggingface.co/thinkingmachines/Inkling)
- 번역 자료: [translation.ko.md](translation.ko.md)

이 폴더는 Thinking Machines Lab의 첫 오픈 웨이트 모델 Inkling 발표를 한국어 학습 자료로 정리한다. 저작권이 있는 원문을 전문 복제하지 않고, 구조와 핵심 수치를 보존한 번역 요약과 실습 코드를 제공한다.

## 한눈에 보기

Inkling은 Thinking Machines Lab이 처음 공개한 오픈 웨이트 foundation model이다. 공식 발표 기준으로 975B total parameters, 41B active parameters를 가진 sparse Mixture-of-Experts(MoE) Transformer이며, 최대 1M token context window를 지원한다. 텍스트, 이미지, 오디오, 비디오를 포함한 45T tokens로 사전학습되었고, 입력으로 텍스트·이미지·오디오를 받아 텍스트를 출력하는 multimodal autoregressive model로 제공된다.

Inkling의 메시지는 "가장 강한 frontier model"이 아니라 "커스터마이징하기 좋은 오픈 웨이트 기반 모델"이다. Thinking Machines Lab은 multimodal capability, efficient controllable thinking effort, Tinker 기반 fine-tuning 접근성을 주요 차별점으로 제시한다.

## 기초 개념

### Open Weights

오픈 웨이트 모델은 모델 구조와 학습된 파라미터를 다운로드하거나 배포 프레임워크에 올려 직접 사용할 수 있는 모델이다. 완전한 open source와는 다를 수 있다. 코드, 데이터, 학습 recipe가 모두 공개되는 것은 아니며, 라이선스와 acceptable use policy를 별도로 확인해야 한다.

### Mixture-of-Experts

MoE는 모든 토큰이 전체 feed-forward network를 통과하지 않고, router가 일부 expert만 선택해 계산하는 구조다. Inkling은 총 파라미터는 975B이지만 토큰당 active parameter는 41B로 제시된다. 이렇게 하면 큰 capacity와 상대적으로 낮은 token당 계산량 사이의 tradeoff를 잡을 수 있다.

### Active Parameters

Active parameters는 한 토큰을 처리할 때 실제로 계산에 참여하는 파라미터 규모다. dense model은 대체로 total과 active가 비슷하지만, sparse MoE는 total이 훨씬 크고 active는 일부 expert만 포함한다. 비용, 지연시간, 처리량을 판단할 때 total parameter만 보면 과장될 수 있으므로 active parameter도 함께 봐야 한다.

### Controllable Thinking Effort

Inkling은 inference에서 thinking effort를 조절해 성능과 생성 토큰 수를 맞바꿀 수 있게 설계되었다고 설명된다. 같은 모델이라도 effort를 낮추면 비용과 latency를 줄이고, effort를 높이면 어려운 reasoning에서 더 많은 토큰을 써 성능을 높이는 방향이다.

### Tinker

Tinker는 Thinking Machines Lab의 fine-tuning 플랫폼이다. 발표문은 Inkling이 Tinker에서 fine-tuning 가능하며, Playground를 통해 모델을 시험해 볼 수 있다고 설명한다. 또한 Inkling이 Tinker를 사용해 자기 자신을 lipogram 모델로 fine-tune하는 데모를 제시한다.

## 핵심 요약

- Inkling은 2026-07-15 공개된 Thinking Machines Lab의 첫 오픈 웨이트 모델이다.
- 공식 발표 기준 모델 크기는 975B total, 41B active parameters이다.
- 모델 카드는 66-layer decoder-only sparse MoE Transformer라고 설명한다.
- 각 토큰은 256 routed experts 중 6개와 2 shared experts를 사용한다.
- context window는 최대 1M tokens이며, Tinker에서는 64K와 256K context 옵션이 제공된다고 공지되어 있다.
- 입력 modality는 text, image, audio이고 출력은 text이다.
- 사전학습 데이터는 text, image, audio, video를 포함한 45T tokens로 설명된다.
- 라이선스는 Apache 2.0이다.
- BF16 checkpoint는 최소 2TB aggregated VRAM이 필요하고, NVFP4 checkpoint는 최소 600GB aggregated VRAM으로 낮아진다고 모델 카드가 밝힌다.
- 발표문은 대규모 asynchronous RL을 30M+ rollouts까지 확장했고, reasoning eval reward가 log-linear하게 개선되었다고 설명한다.
- Inkling-Small preview는 276B total, 12B active parameters로 소개되며, full weights는 테스트 완료 후 공개 예정이라고 되어 있다.

## 상세 정리

### 1. 모델의 위치

Inkling은 "모든 벤치마크에서 최강"이라는 포지션보다 "다양한 조직과 개발자가 fine-tune해서 쓸 수 있는 multimodal open-weights base"라는 포지션을 잡는다. 발표문은 실제 사용자가 특정 업무, 지식, product workflow에 맞춰 모델을 바꾸는 상황을 강조한다.

이 점에서 Inkling은 단일 API 모델 경쟁보다 open weights, Tinker fine-tuning, partner ecosystem, deployment backend와 연결된다.

### 2. 핵심 제원

| 항목 | 내용 |
| --- | --- |
| 제공자 | Thinking Machines Lab, Inc. |
| 공개일 | 2026-07-15 |
| 라이선스 | Apache 2.0 |
| 모델 타입 | Multimodal autoregressive transformer |
| 아키텍처 | 66-layer decoder-only sparse MoE |
| 파라미터 | 975B total, 41B active |
| Context window | 최대 1M tokens |
| 입력 | Text, image, audio |
| 출력 | Text |
| 수치 형식 | BF16, MXFP8, NVFP4 |
| 배포 | Tinker API, third-party providers, Hugging Face weights |

### 3. 아키텍처

Inkling의 MoE layer는 256 routed experts와 2 shared experts를 포함하고, 토큰마다 routed expert 6개가 활성화된다. 발표문은 DeepSeek-V3 계열 MoE 설계를 참고했다고 설명한다.

Attention은 sliding-window layer와 global layer를 5:1 비율로 섞고, 8 KV heads를 사용한다. 위치 인코딩은 RoPE 대신 relative positional embedding을 사용한다고 설명된다. 또한 key/value projection 이후와 residual branch가 main residual stream에 합류하기 전 두 위치에 short convolution을 적용한다.

Multimodal 처리에서는 발표문과 모델 카드 모두 text, image, audio가 shared hidden space에서 함께 처리된다는 점을 강조한다. 발표문은 audio input을 dMel spectrogram으로 설명하고, 모델 카드는 audio를 discrete token encoding으로 설명한다. 두 공식 문서의 표현이 다르므로 세부 구현은 모델 카드와 릴리스 파일을 함께 확인하는 것이 좋다.

### 4. 학습과 post-training

Inkling은 text, image, audio, video를 포함한 45T tokens로 사전학습되었다. 최적화는 큰 matrix weight에는 Muon, 다른 parameter에는 Adam을 쓰는 hybrid strategy로 설명된다.

Post-training은 math, agentic code and tool use, audio, image, chat, safety domain을 넓게 포함한다. 초기 SFT bootstrap에는 Kimi K2.5 같은 open-weights model이 생성한 synthetic data가 일부 쓰였고, compute 대부분은 synthetic 및 human-created environment에서 대규모 RL에 사용되었다고 한다.

RL at scale 섹션은 30M+ rollouts와 두 번의 긴 continuous run을 언급한다. 발표문은 held-out aggregate reasoning eval reward가 SFT initialization에서 release checkpoint까지 log-linear하게 개선되었다고 제시한다.

### 5. Controllable Thinking Effort

Inkling은 effort setting을 조절해 평균 생성 토큰 수와 성능을 tradeoff하도록 설계되었다. 발표문은 Terminal Bench 2.1, Humanity's Last Exam, IFBench 등에서 effort sweep을 보여 주며, 특정 점수에 도달하는 데 필요한 token 수가 경쟁 모델 대비 낮을 수 있다고 주장한다.

실무적으로는 어려운 문제에는 높은 effort, 반복적이고 latency-sensitive한 작업에는 낮은 effort를 쓰는 식으로 운영할 수 있다. fine-tuning 대상 업무가 명확하다면, 한 가지 benchmark 점수보다 effort-performance curve 전체를 보는 것이 더 중요하다.

### 6. Multimodality

Inkling은 텍스트뿐 아니라 이미지와 오디오 입력을 직접 다룬다. 발표문은 speech transcription, spoken instruction following, recording QA, longer-form audio reasoning, chart/diagram/math visual reasoning을 사용 사례로 언급한다.

Vision 쪽에서는 image를 patch 단위로 처리하고, inference 때 Python tool로 zooming/cropping을 수행해 시각 추론과 code reasoning을 결합할 수 있다고 설명한다.

### 7. Safety와 한계

모델 카드는 Inkling이 안전성 평가와 외부 테스트를 거쳤고, CBRN, cyber, loss of control, sycophancy, harmful manipulation, vulnerable users 등을 평가했다고 설명한다. 동시에 hallucination, instruction following 실패, 긴 multi-turn 대화 성능 저하, 데이터 편향, 언어·문화별 성능 차이 같은 foundation model 공통 한계를 명시한다.

오픈 웨이트 모델은 downstream deployment에서 추가 moderation, rate limiting, monitoring, use-case-specific safeguards가 필요하다. 의료, 법률, 안전중요 의사결정 같은 high-stakes 영역은 domain validation과 human oversight 없이 사용하지 않는 것이 원문 권고에 가깝다.

### 8. 실행과 배포 관점

Hugging Face 모델 페이지는 Transformers, vLLM, SGLang 등 사용 예시를 제공한다. 다만 실제 self-hosting은 매우 큰 하드웨어가 필요하다. 모델 카드 기준 BF16은 2TB 이상 aggregated VRAM, NVFP4는 600GB 이상 aggregated VRAM이 필요하다.

개발자가 일반 GPU 한두 장으로 직접 전체 모델을 실행하기는 어렵다. 현실적인 접근은 Tinker, Together AI, Fireworks, Modal, Databricks, Baseten 같은 API/provider를 쓰거나, 대규모 GPU cluster에서 vLLM/SGLang/TokenSpeed/Unsloth/Hugging Face stack을 사용하는 것이다.

## 용어 정리

| 용어 | 의미 |
| --- | --- |
| Open weights | 모델 파라미터가 공개되어 다운로드·배포·fine-tuning 가능한 형태 |
| MoE | 토큰마다 일부 expert만 활성화하는 sparse neural network 구조 |
| Routed expert | Router가 토큰별로 선택하는 expert |
| Shared expert | 모든 토큰에 공통으로 활성화되는 expert |
| Active parameters | 한 토큰 처리에 실제 참여하는 파라미터 규모 |
| Context window | 모델이 한 번에 참조할 수 있는 입력·출력 토큰 범위 |
| Thinking effort | 추론에 투입하는 생성 토큰·계산량을 조절하는 설정 |
| NVFP4 | NVIDIA Blackwell 계열에서 효율적 inference를 위한 4-bit format |
| BF16 | bfloat16 수치 형식 |
| Tinker | Thinking Machines Lab의 모델 fine-tuning 플랫폼 |
| Tinker Cookbook | Tinker 기반 학습 recipe와 예제 모음 |
| FORTRESS | 무기·폭력 관련 harmful request 거절 및 benign over-refusal을 보는 안전성 benchmark |
| StrongREJECT | 명백히 해로운 요청에 대한 refusal 평가 |

## 실습 학습 가이드

- [01_foundations.ipynb](01_foundations.ipynb): MoE 라우팅과 active parameter 개념을 작은 숫자로 계산한다.
- [02_practice.ipynb](02_practice.ipynb): controllable thinking effort의 성능·토큰·비용 tradeoff를 시뮬레이션한다.
- [03_advanced.ipynb](03_advanced.ipynb): fine-tuning objective와 evaluation loop를 lipogram 예제로 만들고, calibration·safety gate를 함께 확인한다.

## 다음 학습 경로

1. Dense Transformer와 sparse MoE의 compute/memory 차이를 비교한다.
2. vLLM, SGLang, llama.cpp, Hugging Face Transformers에서 large multimodal model serving 방식이 어떻게 다른지 조사한다.
3. Tinker Cookbook이나 유사 fine-tuning 플랫폼에서 SFT, RL, LoRA, full-parameter training의 비용 차이를 정리한다.
4. Effort-performance curve를 자체 업무 benchmark에 맞춰 측정하는 스크립트를 만든다.
5. Open weights deployment에서는 모델 자체 safety만 믿지 말고 입력 필터, 출력 필터, monitoring, human review를 포함한 defense-in-depth를 설계한다.
