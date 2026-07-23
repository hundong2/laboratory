# SEED: Self-Evolving On-Policy Distillation

작성일: 2026-07-19
갱신일: 2026-07-23

## 출처와 작업 범위

- 이번 입력 URL: [arXiv:2607.14777](https://arxiv.org/abs/2607.14777)
- 최종 URL: `https://arxiv.org/abs/2607.14777`
- arXiv 페이지 제목: `SEED: Self-Evolving On-Policy Distillation for Agentic Reinforcement Learning`
- 원문 언어: 영어
- 접근 일자: 2026-07-23
- 이전 참고 URL 1: [GitHub - jinyangwu/SEED](https://github.com/jinyangwu/SEED)
- 이전 참고 URL 2: [Hugging Face Papers - 2607.14777](https://huggingface.co/papers/2607.14777)
- PDF 원문: [arXiv PDF](https://arxiv.org/pdf/2607.14777)
- 논문 제목: `SEED: Self-Evolving On-Policy Distillation for Agentic Reinforcement Learning`
- 제출일: 2026-07-16
- 확인 기준일: 2026-07-23
- 코드 공개: GitHub README 기준 2026-07-16 공개
- 라이선스: GitHub 저장소 기준 MIT License
- 작업 범위: arXiv abstract 페이지와 PDF 본문을 우선 기준으로 SEED의 문제의식, 두 단계 학습 구조, OPD 손실, GRPO 결합, 실험 결과, 구현 흐름을 한국어 학습 자료와 표준 라이브러리 기반 실습으로 정리한다.

원문과 코드 문서는 영어이므로 [translation.ko.md](translation.ko.md)에 핵심 초록과 구조를 한국어로 번역 및 해설했다. arXiv experimental HTML 링크는 이번 확인 환경에서 열리지 않았고, abstract 페이지와 PDF는 접근 가능했다. 이 폴더의 노트북은 공식 구현을 재현하지 않고, SEED의 핵심 아이디어를 작은 수치 예제로 학습하기 위한 축소 구현이다.

## 한눈에 보기

SEED는 장기 LLM 에이전트를 강화학습으로 학습할 때 생기는 "최종 성공/실패 보상은 있는데 중간 의사결정에 대한 감독은 부족한 문제"를 다룬다. ALFWorld, WebShop, Search-based QA 같은 환경에서는 에이전트가 여러 단계 동안 관찰하고 행동하며 도구를 써야 한다. 하지만 보상은 보통 에피소드 끝에서 한 번 주어지므로 어떤 token, action, observation이 좋았는지 직접 알려주지 않는다.

SEED의 핵심은 완료된 on-policy trajectory를 hindsight skill로 다시 읽고, 그 skill이 동일한 action token의 확률을 얼마나 높이는지 측정한 뒤, 그 차이를 dense token-level distillation 신호로 policy에 증류하는 것이다. 즉 "완료 후에 알게 된 교훈"을 inference-time prompt나 외부 memory로 남기는 대신, 학습 중 policy 파라미터 안에 내재화한다.

SEED는 두 단계로 구성된다.

1. Hindsight-skill SFT: 완료된 trajectory를 분석해 자연어 skill을 쓰는 능력을 policy에 먼저 학습시킨다.
2. Self-evolving OPD RL: 현재 policy가 trajectory를 수집하고, 같은 checkpoint가 analyzer 역할로 hindsight skill을 만들며, ordinary context와 skill-augmented context의 log-probability 차이를 OPD 신호로 사용한다.

추론 시에는 analyzer, skill bank, retrieval module, skill prompt가 필요 없다. 배포되는 것은 일반 policy 하나뿐이다.

## 기초 개념

### 장기 에이전트 강화학습

장기 에이전트 과제에서는 모델이 한 번 답하고 끝나는 것이 아니라 여러 turn 동안 관찰, 추론, 행동, 도구 호출, 피드백 반영을 반복한다. 예를 들어 WebShop에서는 상품을 검색하고 속성을 비교한 뒤 구매 결정을 내려야 한다. Search-based QA에서는 검색 도구로 증거를 찾은 뒤 답해야 한다.

### Sparse trajectory-level reward

많은 에이전트 환경은 에피소드가 끝난 뒤 성공 여부나 최종 점수만 제공한다. 이것을 sparse trajectory-level reward라고 볼 수 있다. 문제는 reward가 "성공했다" 또는 "실패했다"만 알려주고, 중간의 어떤 행동을 강화하거나 교정해야 하는지는 직접 말해주지 않는다는 점이다.

### Hindsight skill

hindsight skill은 완료된 trajectory를 보고 나중에 정리한 자연어 교훈이다. 성공 trajectory에서는 재사용 가능한 workflow나 결정적 관찰을 추출할 수 있고, 실패 trajectory에서는 피해야 할 행동이나 수정 규칙을 추출할 수 있다.

예시:

- 성공 skill: "물건 위치를 찾기 전에 receptacle을 먼저 확인하지 말고, 관찰에서 object 후보를 좁힌 뒤 이동하라."
- 실패 회피 skill: "검색 결과가 부족하면 첫 페이지 요약만 믿지 말고 추가 query를 만들어 evidence를 보강하라."

### On-policy distillation

on-policy distillation은 policy가 실제로 생성한 action을 대상으로 distillation을 수행한다. 외부 teacher가 만든 이상적인 답을 그대로 따라 하는 것이 아니라, 현재 policy의 trajectory 분포 위에서 supervision을 만든다. 이 덕분에 policy가 실제로 겪는 상태와 실패 모드에 더 잘 맞는다.

### OPD의 직관

같은 action token을 두 context에서 다시 점수화한다.

- ordinary context: 에이전트가 실제로 행동할 때 본 history
- skill-augmented context: 완료 후 추출한 hindsight skill을 추가한 history

skill을 추가했을 때 어떤 token의 log-probability가 올라가면, 그 token은 hindsight skill이 지지하는 행동이라고 본다. SEED는 이 상승분을 gate로 바꾸어 해당 token을 더 강하게 학습한다.

## 핵심 요약

- SEED는 `SElf-Evolving On-Policy Distillation`의 약자다.
- arXiv v1은 2026-07-16 09:57:18 UTC에 제출되었고, 분야는 `cs.CL`이다.
- 저자는 Jinyang Wu, Shuo Yang, Zhengxi Lu, Fan Zhang, Yuhao Shen, Lang Feng, Haoran Luo, Zheng Lian, Shuai Zhang, Zhengqi Wen, Jianhua Tao다.
- 문제는 episode-level sparse reward와 token-level policy learning 사이의 supervision gap이다.
- Stage 1은 외부 analyzer로 trajectory-skill SFT 데이터를 만들고 policy가 trajectory를 분석할 수 있게 한다.
- Stage 2는 현재 policy snapshot이 actor와 analyzer 역할을 동시에 수행한다.
- actor는 on-policy trajectory를 수집하고 analyzer는 완료된 trajectory에서 hindsight skill을 생성한다.
- sampled action은 고정한 채 ordinary context와 skill-augmented context에서 다시 log-probability를 계산한다.
- 두 log-probability의 차이, 즉 skill-induced shift를 sigmoid gate로 바꾼다.
- OPD loss는 gate가 큰 token의 ordinary policy likelihood를 높이는 방향으로 작동한다.
- 최종 objective는 GRPO 계열 outcome-based RL loss와 OPD loss를 함께 최적화한다.
- 학습이 끝난 뒤 inference에는 skill이나 analyzer를 쓰지 않는다.
- GitHub README 기준 실험은 ALFWorld, Search-based QA, WebShop에서 GRPO와 여러 skill-distillation baseline보다 강한 성능을 보였다고 정리한다.

## 상세 정리

### 1. 문제 정의

논문은 long-horizon agentic task를 부분 관측 MDP로 본다. 에이전트는 시간 `t`마다 observation을 받고, 지금까지의 interaction history `h_t`를 바탕으로 action `a_t`를 생성한다. completed trajectory `tau`에는 observations, actions, rewards, final outcome이 들어 있다.

표준 RL objective는 trajectory reward의 기대값을 높이는 것이다. 하지만 이 목적 함수만으로는 긴 interaction history 안의 token-level decision을 세밀하게 지도하기 어렵다. 성공 trajectory에도 우연히 나쁜 행동이 섞일 수 있고, 실패 trajectory에도 다음 시도에 유용한 부분 전략이 들어 있을 수 있다.

SEED는 이 간극을 completed trajectory에서 뽑은 hindsight skill로 메운다.

### 2. Stage 1: Hindsight-skill SFT

첫 단계는 policy가 trajectory analyzer 역할을 할 수 있게 만드는 준비 과정이다.

1. base policy로 skill 없이 ordinary trajectory를 수집한다.
2. 외부 analyzer가 completed trajectory를 읽고 hindsight skill을 작성한다.
3. 형식 검사를 통과한 `(trajectory input, skill target)` 쌍을 SFT 데이터로 사용한다.
4. backbone policy를 이 데이터로 fine-tune해 analyzer-capable policy checkpoint를 만든다.

GitHub README는 paper-style workflow에서 180개 task와 task당 8개 rollout을 기본 규모로 사용한다고 설명한다. 논문 implementation detail도 180개 training task와 8 rollout, 총 1,440 trajectory를 언급한다.

### 3. Stage 2: Self-evolving OPD RL

두 번째 단계에서는 각 RL update 시작 시 현재 policy를 frozen snapshot `pi_old`로 둔다. 이 snapshot은 두 역할을 한다.

- actor: task prompt에서 on-policy trajectory를 샘플링한다.
- analyzer: 완료된 trajectory를 읽고 hindsight skill을 만든다.

그 다음 trainable policy는 GRPO 기반 RL objective와 OPD objective를 함께 최적화한다. update가 끝나면 개선된 policy가 다음 iteration의 actor이자 analyzer가 된다. 그래서 decision policy와 hindsight supervision이 함께 진화한다.

### 4. Skill-induced log-probability shift

SEED의 OPD는 action을 새로 생성하지 않는다. 이미 sampled된 action token을 그대로 두고 두 context에서 다시 점수화한다.

- `log pi_theta(action_token | ordinary_history)`
- `log pi_theta(action_token | skill_augmented_history)`

두 값의 차이를 `Delta`라고 하면, `Delta > 0`인 token은 hindsight skill이 ordinary context보다 그 행동을 더 지지한다는 뜻이다. SEED는 `sigmoid(beta * Delta)`를 gate로 사용한다. gate가 클수록 해당 token을 ordinary policy가 더 강하게 내재화하도록 학습한다.

### 5. GRPO와 OPD의 결합

SEED는 outcome-based RL을 버리지 않는다. group-relative advantage를 사용하는 GRPO 계열 objective로 전체 task success를 최적화하면서, OPD loss를 auxiliary dense supervision으로 더한다.

개념적으로 최종 loss는 다음 형태다.

```text
L_SEED = L_RL + lambda_opd * L_OPD
```

RL term은 "결과가 좋은 trajectory를 강화"하고, OPD term은 "hindsight skill이 지지한 token-level 행동을 ordinary policy에 내재화"한다.

### 6. Inference-time 단순성

SEED의 중요한 제품 관점 장점은 inference-time 구조가 단순하다는 것이다. 학습 중에는 analyzer와 hindsight skill을 쓰지만, 배포 시에는 일반 policy만 사용한다. 즉 skill prompt를 붙이거나, skill bank를 검색하거나, 외부 analyzer를 추가 호출할 필요가 없다.

이 점은 latency, serving cost, prompt 관리, 외부 memory 품질 문제를 줄여준다. 대신 학습 과정은 무겁다. 공개 README의 설치 안내는 veRL, vLLM, flash-attn, ALFWorld, WebShop, Search-R1 retrieval server 같은 큰 실험 인프라를 요구한다.

### 7. 실험 결과 해석

논문과 README는 ALFWorld, Search-based QA, WebShop을 중심으로 결과를 제시한다. GitHub README는 세 가지 주장을 요약한다.

- dense hindsight supervision이 outcome-only RL보다 낫다.
- skill을 inference prompt로 넣는 것보다 skill 효과를 policy에 내재화하는 편이 낫다.
- static distillation보다 최신 policy가 만든 self-evolving distillation이 낫다.

arXiv 표의 Qwen2.5-3B-Instruct 결과에서는 SEED가 ALFWorld 평균 91.8, Search-based QA 평균 45.7, WebShop success 78.9를 기록한 것으로 정리되어 있다. 같은 설정에서 GRPO는 각각 75.0, 36.4, 63.3이다.

논문은 sample efficiency에서도 SEED가 GRPO보다 높은 결과를 보였다고 보고한다. 예를 들어 ALFWorld에서는 60% 데이터로 SEED가 80.7을 달성해 full-data GRPO의 75.0을 넘었다고 설명한다. ALFWorld unseen split에서는 GRPO 평균 70.9에서 SEED 86.2로 15.3점 향상됐다고 보고한다.

### 8. 한계와 주의점

- 논문 결과는 특정 backbone, 환경, hyperparameter, infrastructure 위에서 나온 것이다.
- 공개 실험 재현에는 고성능 GPU, 여러 conda 환경, retrieval server, benchmark setup이 필요하다.
- hindsight skill의 품질은 analyzer 능력과 prompt 형식에 의존한다.
- OPD gate가 잘못된 skill을 지지하면 잘못된 행동도 내재화될 수 있다.
- inference-time은 단순하지만 training-time 비용은 커진다.
- 공개 코드가 빠르게 변할 수 있으므로 실행 전에 GitHub README와 scripts를 다시 확인해야 한다.

## 용어 정리

| 용어 | 뜻 |
| --- | --- |
| SEED | Self-Evolving On-Policy Distillation |
| Agentic RL | 환경과 여러 turn 상호작용하는 LLM agent를 강화학습하는 방식 |
| Trajectory | observation, action, reward가 시간 순서로 이어진 에피소드 기록 |
| Sparse reward | 에피소드 끝에서 드물게 제공되는 보상 |
| Hindsight skill | 완료된 trajectory를 보고 나중에 추출한 자연어 교훈 |
| SFT | Supervised Fine-Tuning, 정답 텍스트를 예측하도록 지도학습하는 단계 |
| OPD | On-Policy Distillation, 현재 policy가 만든 분포 위에서 수행하는 증류 |
| GRPO | Group Relative Policy Optimization, trajectory group 내 상대 advantage를 사용하는 RL 방식 |
| Log-probability shift | skill context가 ordinary context 대비 action token 확률을 얼마나 바꾸는지 나타내는 차이 |
| Gate | OPD 신호를 token별로 얼마나 강하게 적용할지 정하는 가중치 |
| Stop-gradient | teacher signal 쪽으로 gradient가 흐르지 않게 막는 처리 |
| Skill-augmented context | ordinary history에 hindsight skill을 추가한 학습용 context |
| On-policy skill | 현재 policy가 직접 만든 trajectory에서 추출한 skill |
| Static distillation | 한 번 만든 고정 skill이나 teacher signal로 계속 증류하는 방식 |
| Inference-time prompt | 배포 시 모델 입력에 추가로 붙이는 instruction이나 skill text |

## 실습 학습 가이드

- `01_foundations.ipynb`: sparse reward, trajectory, group-relative advantage가 왜 token-level supervision gap을 만드는지 작은 예제로 확인한다.
- `02_practice.ipynb`: ordinary context와 skill-augmented context의 log-probability 차이를 gate로 바꾸고 OPD loss를 계산한다.
- `03_advanced.ipynb`: actor와 analyzer가 같은 policy snapshot에서 함께 진화하는 self-evolving 루프를 장난감 환경으로 시뮬레이션한다.

공식 코드를 실행하려면 GitHub README의 환경 구성을 따라야 한다. 이 폴더의 노트북은 논문 구조를 이해하기 위한 교육용 코드이며 외부 패키지를 사용하지 않는다.

## 다음 학습 경로

1. LLM agent 기초: ReAct, tool use, multi-turn environment interaction을 학습한다.
2. 강화학습 기초: policy gradient, PPO, GRPO, advantage normalization을 비교한다.
3. Distillation 기초: teacher-student distillation, self-distillation, on-policy distillation을 구분한다.
4. Hindsight learning: HER, verbal reflection, trajectory summary 기반 agent learning을 살펴본다.
5. SEED 코드 읽기: `scripts/sft`, `examples/seed_trainer`, environment setup을 따라가며 Stage 1과 Stage 2 실행 경로를 확인한다.
6. 재현 실험 설계: 작은 ALFWorld subset이나 toy environment에서 OPD coefficient, gate sharpness, rollout group size를 바꿔본다.
