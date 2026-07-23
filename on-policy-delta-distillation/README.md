# On-Policy Delta Distillation

작성일: 2026-07-23

## 출처와 작업 범위

- 입력 URL: [https://www.alphaxiv.org/abs/2607.15161](https://www.alphaxiv.org/abs/2607.15161)
- 최종 확인 URL: [https://www.alphaxiv.org/abs/2607.15161](https://www.alphaxiv.org/abs/2607.15161)
- AlphaXiv Overview: [https://www.alphaxiv.org/overview/2607.15161](https://www.alphaxiv.org/overview/2607.15161)
- arXiv: [https://arxiv.org/abs/2607.15161](https://arxiv.org/abs/2607.15161)
- PDF: [https://pdfs.assets.alphaxiv.org/2607.15161v1.pdf](https://pdfs.assets.alphaxiv.org/2607.15161v1.pdf)
- 코드 저장소: [https://github.com/naver-ai/opd2](https://github.com/naver-ai/opd2)
- 페이지 제목: `On-Policy Delta Distillation`
- 원문 언어: 영어
- 접근일: 2026-07-23
- arXiv 제출일: 2026-07-16
- 저자: Byeongho Heo, Jaehui Hwang, Sangdoo Yun, Dongyoon Han
- 소속: NAVER AI Lab
- 주제 분류: Machine Learning(cs.LG), Computation and Language(cs.CL)
- DOI: [10.48550/arXiv.2607.15161](https://doi.org/10.48550/arXiv.2607.15161)
- 코드 상태: GitHub 저장소는 확인되었으나, 2026-07-23 기준 README에 “code and training recipes will be released soon”으로 표시되어 있다.
- 번역 자료: [translation.ko.md](translation.ko.md)

이 폴더는 On-Policy Delta Distillation(OPD²) 논문을 한국어 학습 자료로 정리한다. 일반 웹사이트 URL 입력이므로 `translation.ko.md`를 함께 만들었으며, 원문 전문을 복제하지 않고 핵심 구조와 수식, 실험 결과를 학습용으로 재구성했다.

## 한눈에 보기

OPD²는 reasoning-tuned teacher를 그대로 모방하는 대신, teacher가 자신의 base model에서 reasoning tuning을 거치며 어떻게 바뀌었는지를 distillation reward로 쓰는 방법이다.

기존 On-Policy Distillation(OPD)은 student가 생성한 token에 대해 teacher 확률과 student 확률의 차이를 reward로 사용한다. 이 방식은 teacher의 reasoning skill뿐 아니라 teacher의 말투, 일반적 선호, pretraining에서 온 스타일도 함께 전달할 수 있다. OPD²는 teacher와 teacher-base의 log probability 차이, 즉 delta signal을 사용해 reasoning tuning으로 생긴 변화만 더 직접적으로 전달하려 한다.

논문은 수학, 과학, 코드 reasoning benchmark에서 OPD²가 기존 OPD와 ExOPD를 일관되게 앞섰다고 보고한다. 특히 Qwen3-1.7B의 평균 math reasoning 성능을 34.8%에서 54.6%로 끌어올린 결과가 AlphaXiv 요약에 제시되어 있다.

## 기초 개념

### Knowledge Distillation

Knowledge Distillation(KD)은 큰 teacher model의 지식을 작은 student model로 옮기는 학습 방식이다. 전통적으로는 teacher output distribution을 student가 따라가도록 cross-entropy나 KL divergence를 줄인다.

### On-Policy Distillation

On-policy distillation은 student가 직접 rollout을 생성하고, 그 생성 token을 teacher가 token-level로 평가해 student를 업데이트한다. SFT처럼 teacher가 만든 정답 sequence만 따라 하는 것이 아니라, student가 실제로 낸 답변 위에서 학습하기 때문에 RL과 비슷한 구조를 가진다.

### OPD Reward

기존 OPD의 token reward는 다음 형태다.

```text
R_OPD_t = log pi_teacher(y_t | x, y_<t) - log pi_student(y_t | x, y_<t)
```

teacher가 student보다 어떤 token을 더 선호하면 positive reward가 되고, 덜 선호하면 negative reward가 된다.

### Delta Signal

OPD²의 핵심은 teacher와 teacher-base를 비교하는 delta signal이다.

```text
R_delta_t = log pi_teacher(y_t | x, y_<t) - log pi_teacher_base(y_t | x, y_<t)
```

여기서 teacher는 reasoning tuning을 거친 모델이고, teacher_base는 그 전의 base model이다. 이 차이는 teacher가 reasoning tuning을 통해 얻은 변화의 흔적을 나타낸다.

### Centering

Delta reward는 student policy와 직접 비교하지 않으므로 안정성이 떨어질 수 있다. 논문은 reward에서 기대값을 빼 advantage처럼 zero-centered signal을 만든다. 이렇게 하면 특정 token이 평균 대비 얼마나 좋은지 볼 수 있다.

### Joint Conditioning

Delta signal만 쓰면 student와 teacher의 전체 방향이 어긋날 수 있다. OPD²는 centered delta signal과 centered OPD signal이 같은 부호일 때만 업데이트를 적용하는 joint conditioning을 사용한다. 이는 delta가 reasoning-specific 방향을 주고, OPD가 teacher의 전체 선호와 일관되는지 gate 역할을 하는 구조다.

## 핵심 요약

- OPD는 RL의 sparse reward 문제를 줄이고 token-level supervision을 제공하는 post-training 방법이다.
- 기존 OPD는 teacher distribution 전체를 모방하기 때문에 reasoning skill과 상관없는 teacher의 base preference도 전달할 수 있다.
- OPD²는 reasoning-tuned teacher와 teacher-base의 log probability 차이를 delta signal로 정의한다.
- Delta signal은 reasoning tuning이 teacher distribution에 만든 변화를 더 직접적으로 포착한다.
- 원문 분석에서 delta signal은 `hence`, `however`, `therefore`, `regardless` 같은 논리 연결 표현을 강화하고, `perhaps`, `see`, `try`, `consider` 같은 모호하거나 일반적인 문제풀이 표현을 억제하는 경향을 보였다.
- 잘못된 reasoning trace에서 delta signal은 기존 OPD보다 오류 지점에 더 일관되게 negative feedback을 주는 것으로 시각화된다.
- 안정화를 위해 centering과 joint conditioning이 도입된다.
- 실험은 Math, Science, Code 세 reasoning domain에서 이루어졌고, Qwen3 1.7B/4B/8B, non-thinking/thinking mode, Gemma-4 계열까지 포함한다.
- OPD²는 기존 OPD와 ExOPD보다 일관되게 높은 성능을 보였고, 짧은 post-training 기간만으로도 강한 reasoning 성능을 달성했다고 보고한다.

## 상세 정리

### 1. 문제의식

LLM post-training은 SFT와 RL을 중심으로 발전해 왔다. RL은 verifiable reward가 있으면 강력하지만 reward design, sparse feedback, noisy signal 문제가 있다. OPD는 teacher가 token-level dense feedback을 주므로 RL보다 안정적이고 효율적인 대안이 될 수 있다.

하지만 기존 OPD는 teacher를 "좋은 모델"로만 보고 전체 output distribution을 모방한다. teacher의 reasoning ability는 post-training으로 얻은 부분이지만, teacher distribution에는 base model에서 온 자연스러운 언어 선호와 스타일도 남아 있다. OPD²는 이 섞인 신호를 분해하려는 시도다.

### 2. Delta signal의 직관

Reasoning-tuned teacher와 teacher-base가 같은 token을 비슷하게 선호한다면, 그 token은 일반 언어 modeling이나 pretraining prior에서 온 선호일 가능성이 높다. 반대로 tuning 후 teacher가 base보다 훨씬 더 선호하게 된 token은 reasoning tuning이 만든 변화일 가능성이 높다.

OPD²는 이 차이를 distillation reward로 삼는다. 즉 student에게 "teacher 자체를 복제하라"가 아니라 "teacher가 reasoning tuning을 통해 배운 변화 방향을 따라가라"라고 신호를 준다.

### 3. 기존 OPD와의 차이

| 항목 | 기존 OPD | OPD² |
| --- | --- | --- |
| reward 비교 대상 | teacher vs student | teacher vs teacher-base |
| 주요 목표 | teacher distribution 모방 | reasoning tuning delta 전달 |
| 장점 | 구현이 단순하고 token-level supervision 가능 | reasoning-specific signal을 더 잘 분리 |
| 위험 | 스타일·base preference까지 전이 | delta만 쓰면 수렴 안정성 문제 |
| 안정화 | student-teacher KL 구조 | centering + joint conditioning |

### 4. Centering

Delta signal은 raw log probability 차이이므로 전체적으로 한쪽 부호에 치우칠 수 있다. 논문은 student sampling distribution에 대한 기대 reward를 빼서 advantage를 만든다.

```text
A_delta_t = R_delta_t - E_{y ~ pi_student}[R_delta_t]
```

이렇게 하면 단순히 reward가 큰지 작은지가 아니라, 현재 context에서 가능한 token 평균 대비 얼마나 좋은지를 비교한다.

### 5. Joint conditioning

OPD²는 최종 advantage를 다음 방식으로 gate한다.

```text
A_OPD2_t = A_delta_t  if A_delta_t * A_OPD_t > 0
           0          otherwise
```

즉 delta signal과 기존 OPD signal이 같은 방향을 가리킬 때만 update한다. 이는 delta signal이 teacher의 reasoning change를 포착하더라도, teacher 전체 선호와 모순되는 업데이트를 피하기 위한 장치다.

### 6. 실험 구성

논문은 Math, Science, Code 세 domain을 1:1:1 비율로 섞은 training set을 구성한다. 각 domain은 OpenMathReasoning, OpenScienceReasoning-2, OpenCodeReasoning 계열 데이터를 사용한다. Evaluation은 7개 Math, 3개 Science, 4개 Code benchmark에 걸쳐 이루어진다.

모델은 Qwen3 family의 여러 크기와 mode를 사용하고, Gemma-4 계열에서도 검증한다. 비교 대상은 vanilla OPD, ExOPD 등 on-policy distillation 방법이다.

### 7. 주요 결과

AlphaXiv 요약은 Qwen3-1.7B에서 math 평균 성능이 34.8%에서 54.6%로 개선되었다고 설명한다. 또한 OPD²는 standard OPD보다 3.6 points, ExOPD보다 3.2 points 높은 결과를 보였다고 정리한다.

Gemma4-E4B-it에서도 math 성능이 60.6%에서 67.8%로 개선되었고, ExOPD보다 2.5 points 높았다고 요약되어 있다. 원문은 OPD²가 non-thinking뿐 아니라 thinking mode에서도 성능 저하 없이 개선을 제공하는 점을 강조한다.

### 8. 비용과 한계

OPD²는 teacher-base forward pass가 추가로 필요하다. AlphaXiv overview는 이 때문에 training time이 약 8-28% 증가할 수 있다고 설명한다. 다만 논문에서는 OPD류 학습이 보통 짧은 step 안에 peak에 도달하므로 성능 이득 대비 overhead가 크지 않다고 해석한다.

한계도 분명하다. teacher와 teacher-base가 같은 계열로 잘 정렬되어 있어야 delta의 의미가 선명하다. 또한 reasoning tuning의 변화가 항상 좋은 방향만 의미하지는 않을 수 있다. OPD²의 joint conditioning은 이를 줄이려는 장치지만, 다른 model family나 domain에서의 일반화는 계속 검증해야 한다.

## 용어 정리

| 용어 | 의미 |
| --- | --- |
| KD | Knowledge Distillation. Teacher 지식을 student로 옮기는 학습 |
| OPD | On-Policy Distillation. Student rollout 위에서 teacher token feedback으로 학습 |
| OPD² | On-Policy Delta Distillation. Delta signal을 쓰는 OPD 변형 |
| Teacher | 더 크거나 더 강한 지식 제공 모델 |
| Student | distillation으로 학습되는 모델 |
| Teacher-base | Teacher가 reasoning tuning을 받기 전 base checkpoint |
| Delta signal | `log pi_teacher - log pi_teacher_base` |
| Centering | reward 기대값을 빼 advantage로 만드는 안정화 |
| Joint conditioning | delta와 OPD signal이 같은 방향일 때만 update하는 gate |
| Thinking mode | 모델이 reasoning trace를 생성하는 모드 |
| Non-thinking mode | 긴 reasoning trace 없이 직접 답변하는 모드 |
| ExOPD | OPD²가 비교하는 reward extrapolation 기반 on-policy distillation 방법 |

## 실습 학습 가이드

- [01_foundations.ipynb](01_foundations.ipynb): teacher, student, teacher-base token distribution으로 OPD reward와 delta signal을 직접 계산한다.
- [02_practice.ipynb](02_practice.ipynb): centering과 joint conditioning을 구현하고, OPD² advantage가 어떤 token만 업데이트하는지 확인한다.
- [03_advanced.ipynb](03_advanced.ipynb): Math/Science/Code toy benchmark에서 OPD, ExOPD, OPD² 결과를 비교하고 overhead 대비 성능 이득을 분석한다.

## 다음 학습 경로

1. Hinton et al.의 classical knowledge distillation과 sequence-level KD를 복습한다.
2. RL policy gradient와 OPD gradient의 공통점을 정리한다.
3. Teacher-base checkpoint가 없을 때 delta signal을 근사할 수 있는 방법을 고민한다.
4. ExOPD, top-k OPD, representation distillation과 OPD²의 차이를 비교한다.
5. 실제 코드가 공개되면 작은 Qwen 계열 모델로 Math/Code subset에 OPD²를 재현해 본다.
