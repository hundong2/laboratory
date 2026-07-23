# On-Policy Delta Distillation 한국어 번역 요약

작성일: 2026-07-23

## 원문 정보

- AlphaXiv URL: [https://www.alphaxiv.org/abs/2607.15161](https://www.alphaxiv.org/abs/2607.15161)
- AlphaXiv Overview: [https://www.alphaxiv.org/overview/2607.15161](https://www.alphaxiv.org/overview/2607.15161)
- arXiv URL: [https://arxiv.org/abs/2607.15161](https://arxiv.org/abs/2607.15161)
- PDF URL: [https://pdfs.assets.alphaxiv.org/2607.15161v1.pdf](https://pdfs.assets.alphaxiv.org/2607.15161v1.pdf)
- GitHub: [https://github.com/naver-ai/opd2](https://github.com/naver-ai/opd2)
- 제목: `On-Policy Delta Distillation`
- 원문 언어: 영어
- 접근일: 2026-07-23
- 제출일: 2026-07-16
- 저자: Byeongho Heo, Jaehui Hwang, Sangdoo Yun, Dongyoon Han

이 문서는 AlphaXiv와 arXiv에서 확인한 논문 구조를 따라 작성한 한국어 학습용 번역 요약이다. 원문 전문을 그대로 복제하지 않고 핵심 섹션 흐름과 수식, 수치, 실험 메시지를 보존해 재구성했다.

## 초록

On-policy distillation은 reinforcement learning의 대안적 post-training 방법이다. Reward model이 만드는 제약을 줄이고, teacher model이 token-level supervision을 제공할 수 있다는 장점이 있다. 하지만 OPD가 여러 환경에서 연구되고 적용되어 왔음에도, 기본 reward design은 충분히 탐구되지 않았다.

논문은 teacher output distribution을 직접 모방하는 대신, delta signal이라는 새로운 distillation reward를 제안한다. Delta signal은 reasoning capability를 얻기 위해 instruction tuning을 받기 전 teacher base model과, reasoning-tuned teacher model 사이의 차이로 정의된다. 따라서 reasoning tuning이 만든 변화를 포착하고 reasoning capability를 더 직접적으로 전달하는 신호가 된다.

저자들은 이 방법을 On-Policy Delta Distillation(OPD²)이라고 부른다. 수학, 과학, 코드 reasoning benchmark 실험에서 OPD²는 기존 on-policy distillation보다 일관되게 더 좋은 결과를 보였고, 짧은 post-training 기간만으로도 reasoning LLM이 강한 성능을 내도록 했다.

## 1. 서론

LLM 사용이 확장되면서 요구사항도 다양해졌다. Pretraining은 여전히 next-token prediction을 통해 일반적 능력을 만드는 핵심 방법이지만, downstream 요구에 맞추려면 post-training이 중요하다.

Post-training에는 보통 SFT와 RL이 포함된다. SFT는 큰 모델이 만든 desired output을 따라 하게 만들고, RL은 모델이 생성한 응답의 품질을 평가해 더 좋은 출력을 향해 최적화한다. 최근에는 RL의 대안으로 OPD가 활발히 연구된다.

OPD는 student가 생성한 sequence를 teacher가 token-level로 평가하고, teacher가 높게 보는 token을 강화하고 낮게 보는 token을 약화한다. 이 방식은 reward design 걱정을 줄이고, sparse RL reward보다 조밀한 supervision을 제공한다.

하지만 기존 OPD reward는 단순히 teacher와 student의 log probability 차이를 쓴다. Teacher model은 reasoning tuning 이후에도 base model에서 온 자연 언어 선호와 스타일을 유지하므로, teacher 전체를 모방하는 것이 reasoning knowledge만 전달하는 최적 방법은 아닐 수 있다.

## 2. 방법

### 2.1 기존 OPD

기존 OPD는 student rollout `y ~ pi_theta(. | x)` 위에서 teacher distribution과 student distribution 사이의 KL divergence를 줄인다. Token-level reward는 다음과 같다.

```text
R_OPD_t =
  log pi_teacher(y_t | x, y_<t)
  - log pi_student(y_t | x, y_<t)
```

이 reward는 sampled token에만 적용된다. Teacher가 student보다 해당 token을 더 선호하면 student가 그 token의 확률을 높이도록 학습하고, 반대면 낮추도록 학습한다.

### 2.2 Delta signal

OPD²는 teacher 자체가 아니라 teacher가 reasoning tuning을 통해 얻은 변화에 주목한다. 이를 위해 teacher의 base model을 함께 사용한다.

```text
R_delta_t =
  log pi_teacher(y_t | x, y_<t)
  - log pi_teacher_base(y_t | x, y_<t)
```

이 signal은 teacher가 base에서 reasoning-tuned model로 바뀌는 과정에서 어떤 token을 더 선호하게 되었는지 나타낸다. 논문은 target knowledge가 단순 next-token prediction이 아니라 reasoning ability이므로, teacher의 base prior가 아니라 reasoning tuning의 변화가 더 직접적인 학습 신호라고 본다.

### Signal 분석

논문은 word cloud, token-level visualization, word-level statistics로 delta signal을 분석한다.

Word cloud에서 delta signal은 `hence`, `note`, `instead`, `however`, `yet` 같은 논리 연결 표현을 더 강하게 강화한다. 반대로 `see`, `try`, `verify`, `confirm` 같은 exploratory 또는 verification-related 표현은 기존 OPD 대비 약화되는 경향을 보인다.

간단한 math, science, code reasoning 예제에서는 일부러 틀린 reasoning trace를 넣고 OPD와 delta signal을 비교한다. Delta signal은 잘못된 추론이 시작되는 token 주변에 더 강한 negative signal을 주는 경향을 보인다. 기존 OPD는 언어적으로 그럴듯하지만 틀린 reasoning token에도 positive signal을 줄 수 있다.

통계 분석에서는 Math, Code, Science 각 domain에서 10k questions를 샘플링해 generated reasoning token을 분석한다. Delta signal은 여러 domain에서 explicit logical connection words를 강화하고, vague uncertainty나 generic problem-solving narration을 억제하는 경향을 보인다.

## 2.3 On-Policy Delta Distillation(OPD²)

Delta signal은 유용하지만 직접 사용하면 convergence issue가 생길 수 있다. Student policy와 비교하지 않는 reward이기 때문에, 특정 positive delta token으로 과도하게 수렴할 위험이 있다.

이를 해결하기 위해 논문은 두 가지 design을 추가한다.

### Centering

Reward에서 student sampling distribution에 대한 기대 reward를 빼 advantage를 만든다.

```text
A_delta_t = R_delta_t - E[R_delta_t]
A_OPD_t = R_OPD_t - E[R_OPD_t]
```

이렇게 하면 token reward의 절대값보다 현재 context에서 평균 대비 더 좋은지 나쁜지를 볼 수 있다.

### Joint conditioning

최종 update는 delta advantage와 OPD advantage의 부호가 일치할 때만 적용한다.

```text
A_OPD2_t =
  A_delta_t, if A_delta_t * A_OPD_t > 0
  0,         otherwise
```

이 조건은 common descent 방향을 찾는 gate처럼 작동한다. Delta signal은 reasoning-specific direction을 제공하고, OPD signal은 teacher의 전체 preference와 student의 위치를 반영해 안정성을 준다.

## 3. 실험

논문은 Math, Science, Code 세 domain에서 실험한다. Training set은 각 domain에서 같은 수의 question을 뽑아 1:1:1 비율로 구성한다. Post-training은 mixed-domain training set에서 on-policy distillation 방식으로 수행하고, 평가는 7개 Math, 3개 Science, 4개 Code benchmark에서 진행한다.

검증 범위는 다음과 같다.

- Qwen3 여러 크기: 1.7B, 4B, 8B
- Non-thinking mode와 thinking mode
- Gemma-4-E4B-it
- 비교 방법: 기존 OPD, ExOPD 등

## 주요 결과

AlphaXiv overview는 OPD²가 모든 Qwen3 model size와 mode에서 Math, Code, Science 평균 reasoning score가 가장 높았다고 정리한다.

대표 결과는 다음과 같다.

| 설정 | 결과 요약 |
| --- | --- |
| Qwen3-1.7B Math | 평균 math reasoning이 34.8%에서 54.6%로 상승 |
| Qwen3-1.7B 비교 | standard OPD보다 3.6 points, ExOPD보다 3.2 points 높음 |
| Qwen3-4B OPD² | 다른 방법으로 학습한 8B 모델보다 높은 경우 보고 |
| Gemma4-E4B-it Math | 60.6%에서 67.8%로 상승, ExOPD보다 2.5 points 높음 |

Thinking mode에서는 기존 OPD가 강한 reasoning model을 오히려 망가뜨리는 경우가 있지만, OPD²는 더 안정적으로 개선을 제공한다는 점이 강조된다.

## 계산 비용

OPD²는 teacher-base model을 추가로 forward해야 하므로 기존 OPD보다 비용이 증가한다. AlphaXiv overview는 training time overhead를 약 8-28%로 정리한다.

다만 OPD 계열 방법은 보통 짧은 post-training step에서 peak performance에 도달하므로, 성능 이득과 비교하면 overhead가 비교적 작다고 논문은 해석한다.

## 왜 delta signal이 중요한가

이 논문의 핵심 메시지는 "teacher model의 모든 지식이 distillation에 똑같이 유용하지 않다"는 것이다. Teacher에는 일반 언어 능력, 스타일, pretraining prior, reasoning tuning으로 생긴 변화가 모두 섞여 있다.

Delta signal은 teacher가 reasoning-tuned model이 되며 바뀐 부분을 분리하려 한다. 따라서 student는 teacher의 최종 상태 전체가 아니라 teacher의 학습 궤적, 특히 reasoning skill을 만든 변화 방향을 배운다.

이 관점은 distillation을 단순 복제가 아니라 skill-specific transfer로 바라보게 한다.

## 결론

OPD²는 on-policy distillation의 reward design을 바꾼다. 기존 OPD가 teacher의 최종 output distribution을 모방했다면, OPD²는 teacher가 reasoning tuning을 거치며 base model에서 어떻게 달라졌는지를 distill한다.

Centering과 joint conditioning을 결합한 OPD²는 다양한 모델 크기, reasoning mode, model family에서 더 안정적인 성능 향상을 보였다. 특히 작은 모델의 reasoning capability를 효율적으로 끌어올리고, 이미 강한 thinking model을 추가로 개선할 때 유용한 방법으로 제시된다.

향후 실제 코드와 training recipes가 공개되면, 작은 모델에서 OPD²의 delta signal이 domain별로 어떤 token과 reasoning pattern을 강화하는지 직접 재현해 보는 것이 좋은 후속 학습이 된다.
