# SEED 논문 및 코드 핵심 번역

작성일: 2026-07-19

## 번역 대상과 범위

- 논문: [SEED: Self-Evolving On-Policy Distillation for Agentic Reinforcement Learning](https://arxiv.org/abs/2607.14777)
- 코드: [jinyangwu/SEED](https://github.com/jinyangwu/SEED)
- Hugging Face Paper: [2607.14777](https://huggingface.co/papers/2607.14777)
- 논문 제출일: 2026-07-16
- 확인 기준일: 2026-07-19

이 파일은 논문과 README의 전문 번역이 아니다. 저작권이 있는 원문을 그대로 복제하지 않고, 학습자가 구조를 이해할 수 있도록 초록, 방법, 실험, 실행 흐름의 핵심을 한국어로 번역 및 해설한다.

## 제목

SEED: 에이전트형 강화학습을 위한 자기진화 on-policy 증류

## 초록 번역 요약

대형 언어 모델은 점점 더 긴 horizon을 가진 interactive agent로 학습되고 있다. 이런 agent는 여러 turn 동안 환경과 상호작용하고, 도구를 사용하며, 환경 피드백을 반영해야 한다. outcome-based reinforcement learning은 실용적인 최적화 방식이지만, 보상이 trajectory 전체 수준에서 드물게 주어지기 때문에 중간 의사결정에 대한 안내가 부족하다. 그 결과 episode-level outcome과 token-level policy learning 사이에 감독 간극이 생긴다.

SEED는 완료된 on-policy trajectory를 학습 중 hindsight skill로 바꾸고, 그 skill이 행동 확률에 미치는 영향을 다시 policy model에 증류하는 자기진화 프레임워크다. 먼저 policy가 완료된 trajectory를 분석해 재사용 가능한 workflow, 결정적 관찰, 실패 회피 규칙을 담은 자연어 skill을 생성할 수 있도록 fine-tuning한다.

RL 중에는 현재 policy가 trajectory를 수집하는 actor 역할과 trajectory에서 hindsight skill을 추출하는 analyzer 역할을 동시에 수행한다. policy update가 의사결정 능력과 skill 분석 능력을 함께 개선하므로, hindsight supervision도 현재 policy의 행동 분포에 맞게 계속 진화한다.

SEED는 sampled action을 ordinary context와 skill-augmented context에서 다시 점수화한다. skill 때문에 생긴 log-probability 변화는 dense token-level on-policy distillation signal로 변환된다. 이 signal은 outcome-based RL과 함께 최적화되어 auxiliary supervision이 현재 trajectory distribution과 맞게 유지된다.

논문은 텍스트 기반 및 비전 기반 agentic task 실험에서 SEED가 성능과 sample efficiency를 일관되게 개선하고 unseen scenario에도 강한 일반화를 보였다고 보고한다.

## 방법 핵심 번역

### 문제 설정

장기 agentic task는 부분 관측 MDP로 볼 수 있다. 에이전트는 각 시점에서 observation을 받고 interaction history를 유지하며 다음 action을 생성한다. completed trajectory는 observation, action, reward의 시퀀스이고, outcome은 보통 episode가 끝난 뒤에만 제공된다.

이 설정에서 표준 RL은 trajectory-level reward의 기대값을 높이려 한다. 그러나 policy는 history 전체에 흩어진 token-level decision을 학습해야 한다. SEED는 completed trajectory 이후에만 알 수 있는 hindsight 정보를 token-level auxiliary signal로 바꿔 이 간극을 줄인다.

### Stage 1: Hindsight-skill SFT

첫 단계는 단일 policy model이 trajectory를 분석하고 자연어 hindsight skill을 생성할 수 있게 준비하는 단계다.

1. base policy로 skill augmentation 없이 ordinary trajectory를 수집한다.
2. 외부 analyzer가 completed trajectory를 읽고 hindsight skill을 작성한다.
3. 형식이 올바른 annotation만 SFT dataset으로 유지한다.
4. policy model을 trajectory input에서 skill target을 예측하도록 fine-tune한다.

이렇게 만들어진 checkpoint는 이후 RL 단계에서 actor이자 analyzer로 사용된다.

### Stage 2: Self-evolving OPD

각 RL update 시작 시 현재 policy snapshot을 freeze해 `old policy`로 둔다. 이 snapshot은 task prompt에서 trajectory를 수집하고, 같은 trajectory를 분석해 hindsight skill을 생성한다. 그 뒤 trainable policy는 환경 보상 기반 RL objective와 OPD objective를 함께 최적화한다.

update가 끝나면 새 policy가 다음 update의 old policy가 된다. 따라서 actor가 마주치는 trajectory 분포와 analyzer가 만드는 hindsight supervision이 함께 바뀐다. 이것이 SEED의 self-evolving 구조다.

### OPD 신호

SEED는 이미 샘플링된 action token을 고정한 뒤 두 가지 context에서 다시 log-probability를 계산한다.

- ordinary history만 있는 context
- ordinary history에 hindsight skill을 추가한 context

skill context에서 특정 token의 log-probability가 더 높아지면, 그 token은 hindsight skill이 지지하는 행동으로 해석된다. 이 차이를 sigmoid gate로 바꿔 token별 OPD supervision 강도를 정한다. teacher branch는 stop-gradient 처리되고, gradient는 ordinary student branch에만 흐른다.

결과적으로 OPD loss는 gate가 큰 token의 ordinary policy likelihood를 높이는 방향으로 작동한다. skill은 학습 중에만 쓰이며, inference에서는 policy가 ordinary history만 보고 행동한다.

### Joint objective

최종 학습 objective는 환경 결과를 최적화하는 RL loss와 hindsight skill 효과를 내재화하는 OPD loss를 더한 형태다.

```text
L_SEED = L_RL + lambda_opd * L_OPD
```

논문에서는 RL term으로 group-relative advantage를 사용하는 GRPO 계열 objective를 사용한다.

## GitHub README 실행 흐름 요약

공개 저장소는 veRL 기반 대규모 학습 코드를 포함한다. README의 큰 흐름은 다음과 같다.

1. `conda create -n seed python==3.12`로 기본 환경을 만든다.
2. `vllm`, `flash-attn`, 로컬 패키지를 설치한다.
3. ALFWorld, WebShop, Search-based QA 환경을 각각 준비한다.
4. `.env`에 GPU, 모델 경로, 데이터 경로, analyzer endpoint를 설정한다.
5. `scripts/sft/...` 아래 스크립트로 Stage 1 SFT 데이터를 만들고 checkpoint를 학습한다.
6. `examples/seed_trainer/...` 아래 스크립트로 Stage 2 self-evolving OPD RL을 실행한다.
7. 필요하면 `scripts/model_merger.py`로 distributed checkpoint를 병합한다.

WebShop은 Python 3.10 환경을 별도로 요구하고, Search-based QA는 local retrieval server와 index 다운로드가 필요하다. 따라서 공식 재현은 일반 노트북 실습보다 훨씬 무거운 실험 인프라를 전제로 한다.

## 실험 결과 핵심

GitHub README는 세 가지 주요 결과를 요약한다.

- trajectory-level hindsight를 token-level OPD signal로 바꾸면 outcome-only RL보다 성능이 개선된다.
- skill을 inference-time prompt로 넣는 것보다 skill 효과를 policy에 내재화하는 편이 낫다.
- static distillation보다 최신 policy가 계속 analyzer가 되는 self-evolving distillation이 낫다.

논문 표의 Qwen2.5-3B-Instruct 설정에서는 SEED가 ALFWorld 평균, Search-based QA 평균, WebShop success에서 GRPO보다 높은 값을 보였다. 별도 분석에서는 sample efficiency와 unseen ALFWorld generalization에서도 이점을 보고한다.

## 학습자 메모

- SEED는 "좋은 skill prompt를 찾아 추론 때 붙이는 방법"이 아니라, skill의 효과를 학습 중 policy에 흡수하는 방법이다.
- actor와 analyzer가 같은 checkpoint를 공유한다는 점이 self-evolving의 핵심이다.
- OPD는 skill이 action을 직접 만들게 하지 않는다. 이미 on-policy로 나온 action을 두 context에서 다시 점수화한다.
- training-time 비용은 크지만 inference-time 구조는 단순하다.
- 논문 수식을 읽을 때는 `Delta`, `gate`, `OPD loss`, `GRPO advantage`의 역할을 분리해서 보면 쉽다.
