# FlashSAC: Fast and Stable Off-Policy Reinforcement Learning for High-Dimensional Robot Control

## 논문 metadata

| 항목 | 내용 |
|---|---|
| 한국어 제목 | FlashSAC: 고차원 로봇 제어를 위한 빠르고 안정적인 오프폴리시 강화학습 |
| 저자 | Donghu Kim, Youngdo Lee, Minho Park, Kinam Kim, Takuma Seno, I Made Aswin Nahrendra, Sehee Min, Daniel Palenicek, Florian Vogt, Danica Kragic, Jan Peters, Jaegul Choo, Hojoon Lee |
| 학회 | Robotics: Science and Systems 2026 (RSS 2026), Paper ID 99, Control & Dynamics |
| 식별자 | arXiv:2604.04539, arXiv DOI 10.48550/arXiv.2604.04539 |
| 기준 원문 | [RSS proceedings PDF](https://www.roboticsproceedings.org/rss22/p099.pdf), 14쪽 |
| 대조 원문 | [arXiv v2](https://arxiv.org/abs/2604.04539v2), 2026-05-15 |
| 프로젝트·코드 | [Project](https://holiday-robot.github.io/FlashSAC) · [GitHub](https://github.com/Holiday-Robot/FlashSAC) |
| 원문 언어 | 영어 |
| 접근일 | 2026-07-27 |
| 라이선스 | arXiv v2에 표시된 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

이 문서는 CC BY 4.0 원문의 한국어 번역·해설이며 원저자의 보증이나 승인을 뜻하지 않는다. RSS PDF를 기준으로 번역하고, PDF 추출이 불명확한 수식과 다단 문장 순서는 렌더링과 arXiv HTML로 대조했다.

[한국어 분석과 실습으로 돌아가기](README.md)

## 번역·접근 범위

| 절 | 상태 | 범위 |
|---|---|---|
| 제목·저자·그림 1 설명 | 완료 | 원문 대조 |
| Abstract | 완료 | 전체 문장 대조 |
| I. Introduction | 부분 번역 | 문제 설정, 핵심 주장과 기여 |
| II. Related Work | 부분 번역 | 세 연구 흐름과 FlashSAC의 차이 |
| III. Preliminary | 부분 번역 | MDP, SAC, 수식 (2)~(5) |
| IV. FlashSAC | 부분 번역 | 모든 핵심 구성과 수식 (6)~(7) |
| V. Experiments | 부분 번역 | 네 실험 범주, 비교 조건과 핵심 결과 |
| VI. Analysis | 부분 번역 | coverage, scaling, architecture, exploration ablation |
| VII. Lessons and Opportunities | 완료 | 전체 핵심 논지 |
| Acknowledgements | 한국어 요약 | 지원 기관·기여자 |
| References | 원문 유지 | 서지정보는 RSS PDF 참조 |

이 파일은 초록을 완역하고 본문의 연구 논증을 문장 단위로 선별 번역한다. 생략된 세부 baseline 설명, 모든 task별 curve와 114개 참고문헌을 전체 번역한 것으로 과장하지 않는다.

## 읽기 전 핵심 배경

- **RL (Reinforcement Learning, 강화학습)**: 행동 결과의 보상을 이용해 policy를 학습한다.
- **Off-policy RL(오프폴리시 강화학습)**: 현재 policy뿐 아니라 과거 policy가 모은 데이터도 재사용한다.
- **Critic(가치 평가기)**: 상태-행동의 장기 return을 예측한다.
- **Bootstrapping(부트스트래핑)**: critic의 미래 예측을 현재 target에 사용한다. 효율적이지만 오차가 되먹임될 수 있다.
- **Asymptotic performance(점근 성능)**: 충분히 오래 학습했을 때 도달하는 최종 성능 수준이다.

## 제목과 그림 1

**S001 — Original**

FlashSAC: Fast and Stable Off-Policy Reinforcement Learning for High-Dimensional Robot Control

**S001 — 한국어**

FlashSAC: 고차원 로봇 제어를 위한 빠르고 안정적인 오프폴리시 강화학습

**S002 — Original**

Tasks grouped by state-action dimensionality, with representative examples shown for each category.

**S002 — 한국어**

과제를 상태-행동 차원에 따라 묶고 각 범주의 대표 예를 제시한다.

**S003 — Original**

In low-dimensional settings, FlashSAC achieves performance comparable to PPO.

**S003 — 한국어**

저차원 설정에서 FlashSAC은 PPO와 비슷한 성능을 달성한다.

- **용어·약어 해설**
  - **PPO (Proximal Policy Optimization, 근접 정책 최적화)**: update 때 policy가 지나치게 크게 변하지 않도록 제한하는 온폴리시 알고리즘이다.

**S004 — Original**

In high-dimensional settings, FlashSAC substantially outperforms PPO in both asymptotic return and wall-clock efficiency.

**S004 — 한국어**

고차원 설정에서 FlashSAC은 점근 return과 실제 경과 시간 효율 양쪽에서 PPO를 크게 앞선다.

**S005 — Original**

FlashSAC enables sim-to-real transfer within minutes, whereas PPO requires hours of training.

**S005 — 한국어**

FlashSAC은 수 분의 학습으로 sim-to-real 이전을 가능하게 하지만 PPO에는 수 시간이 필요하다.

- **번역자 주:** 이 문장은 그림 1의 평지 Unitree G1 실험을 요약한다. 논문 뒤의 거친 지형 계단 실험은 FlashSAC 약 4시간, PPO 약 20시간으로 보고되므로 모든 sim-to-real 과제가 “수 분”이라는 뜻은 아니다.

## Abstract

**S006 — Original**

Reinforcement learning (RL) is a core approach for robot control when expert demonstrations are unavailable.

**S006 — 한국어**

전문가 시연을 구할 수 없을 때 강화학습(RL)은 로봇 제어의 핵심 접근법이다.

**S007 — Original**

On-policy methods such as Proximal Policy Optimization (PPO) are widely used for their stability, but their reliance on narrowly distributed on-policy data limits accurate policy evaluation in high-dimensional state and action spaces.

**S007 — 한국어**

PPO 같은 온폴리시 방법은 안정성 때문에 널리 사용되지만, 좁게 분포한 온폴리시 데이터에 의존하므로 고차원 상태·행동 공간에서 policy를 정확히 평가하는 데 한계가 있다.

**S008 — Original**

Off-policy methods can overcome this limitation by learning from a broader state-action distribution, yet suffer from slow convergence and instability, as fitting a value function over diverse data requires many gradient updates, causing critic errors to accumulate through bootstrapping.

**S008 — 한국어**

오프폴리시 방법은 더 넓은 상태-행동 분포에서 학습해 이 한계를 극복할 수 있지만, 다양한 데이터에 가치 함수를 맞추려면 gradient update가 많이 필요하고 부트스트래핑을 통해 critic 오차가 누적되므로 수렴이 느리고 불안정하다.

**S009 — Original**

We present FlashSAC, a fast and stable off-policy RL algorithm built on Soft Actor-Critic.

**S009 — 한국어**

우리는 Soft Actor-Critic을 기반으로 한 빠르고 안정적인 오프폴리시 강화학습 알고리즘 FlashSAC을 제시한다.

- **용어·약어 해설**
  - **SAC (Soft Actor-Critic)**: 기대 return과 policy entropy를 함께 최적화하는 오프폴리시 actor-critic 알고리즘이다.

**S010 — Original**

Motivated by scaling laws observed in supervised learning, FlashSAC sharply reduces gradient updates while compensating with larger models and higher data throughput.

**S010 — 한국어**

지도학습에서 관찰된 scaling law에 착안하여 FlashSAC은 gradient update 횟수를 크게 줄이는 대신 더 큰 모델과 더 높은 데이터 처리량으로 보완한다.

**S011 — Original**

To maintain stability at increased scale, FlashSAC explicitly bounds weight, feature and gradient norms, curbing critic error accumulation.

**S011 — 한국어**

규모를 키운 상태에서도 안정성을 유지하기 위해 FlashSAC은 weight, feature, gradient norm을 명시적으로 제한하여 critic 오차 누적을 억제한다.

**S012 — Original**

Across over 60 tasks in 10 simulators, FlashSAC consistently outperforms PPO and strong off-policy baselines in both final performance and training efficiency, with the largest gains on high-dimensional tasks such as dexterous manipulation.

**S012 — 한국어**

10개 simulator의 60개가 넘는 과제에서 FlashSAC은 최종 성능과 학습 효율 양쪽 모두에서 PPO와 강력한 오프폴리시 baseline을 일관되게 앞서며, dexterous manipulation 같은 고차원 과제에서 개선 폭이 가장 크다.

**S013 — Original**

In sim-to-real humanoid locomotion, FlashSAC reduces training time from hours to minutes, demonstrating the promise of off-policy RL for sim-to-real transfer.

**S013 — 한국어**

휴머노이드 보행의 sim-to-real 실험에서 FlashSAC은 학습 시간을 수 시간에서 수 분으로 줄여 sim-to-real 이전을 위한 오프폴리시 강화학습의 가능성을 보여 준다.

## I. Introduction

**S014 — Original**

The long-standing goal of robot learning is to develop agents that generalize across a wide range of tasks in the real world.

**S014 — 한국어**

로봇 학습의 오랜 목표는 현실 세계의 폭넓은 과제에 일반화하는 agent를 개발하는 것이다.

**S015 — Original**

While large-scale imitation learning from real-world data has recently yielded impressive results in robotic control, reinforcement learning from simulation remains a core paradigm when expert demonstrations are unavailable, incomplete, or insufficient.

**S015 — 한국어**

최근 현실 데이터의 대규모 모방학습이 로봇 제어에서 인상적인 결과를 냈지만, 전문가 시연이 없거나 불완전하거나 충분하지 않을 때 simulation 강화학습은 여전히 핵심 paradigm이다.

**S016 — Original**

In this regime, on-policy methods such as Proximal Policy Optimization (PPO) have proven effective: PPO is stable, easy to tune, and its data inefficiency is acceptable when fresh on-policy data can be collected cheaply.

**S016 — 한국어**

값싼 새 온폴리시 데이터를 수집할 수 있는 조건에서는 PPO가 안정적이고 tuning하기 쉬우며 데이터 비효율도 감당할 수 있어 효과적이었다.

**S017 — Original**

However, this regime is becoming less representative of modern robot learning.

**S017 — 한국어**

그러나 이런 조건은 현대 로봇 학습을 점점 덜 대표하게 되고 있다.

**S018 — Original**

Emerging applications—including humanoid locomotion, dexterous manipulation, and vision-based control—involve much higher-dimensional state and action spaces, where policy evaluation and improvement from narrowly distributed on-policy data become substantially harder.

**S018 — 한국어**

휴머노이드 보행, dexterous manipulation, vision 기반 제어 같은 새 응용은 훨씬 고차원인 상태·행동 공간을 가지므로 좁게 분포한 온폴리시 데이터만으로 policy를 평가하고 개선하기가 훨씬 어렵다.

**S019 — Original**

Off-policy RL offers a natural alternative.

**S019 — 한국어**

오프폴리시 강화학습은 자연스러운 대안이다.

**S020 — Original**

By reusing diverse experience from a replay buffer, off-policy methods can achieve substantially higher data efficiency than on-policy approaches.

**S020 — 한국어**

오프폴리시 방법은 replay buffer의 다양한 경험을 재사용해 온폴리시 접근보다 훨씬 높은 데이터 효율을 달성할 수 있다.

**S021 — Original**

A central challenge is learning an accurate value function from broad replay data.

**S021 — 한국어**

핵심 난점은 폭넓은 replay 데이터에서 정확한 가치 함수를 학습하는 것이다.

**S022 — Original**

In high-dimensional settings, fitting this critic accurately over diverse replay data often requires many gradient updates, which not only increases training time but also compounds estimation errors through repeated bootstrapping, as the critic is optimized toward targets that depend on its own predictions.

**S022 — 한국어**

고차원 설정에서 다양한 replay 데이터에 critic을 정확히 맞추려면 흔히 많은 gradient update가 필요하며, 이는 학습 시간을 늘릴 뿐 아니라 critic 자신의 예측에 의존하는 target을 반복해서 부트스트래핑하므로 추정 오차도 누적시킨다.

**S023 — Original**

To maintain stability, FlashSAC explicitly controls critic update dynamics by bounding weight, feature, and gradient norms, thereby preventing the accumulation of critic errors.

**S023 — 한국어**

안정성을 유지하기 위해 FlashSAC은 weight, feature, gradient norm을 제한하여 critic update 동역학을 명시적으로 제어하고 critic 오차의 누적을 막는다.

**S024 — Original**

In sim-to-real humanoid walking, FlashSAC reduces training time from hours to minutes while maintaining stable real-world deployment, demonstrating that off-policy RL can be both fast and stable for scalable sim-to-real robot learning.

**S024 — 한국어**

휴머노이드 보행 sim-to-real에서 FlashSAC은 안정적인 현실 배치를 유지하면서 학습 시간을 수 시간에서 수 분으로 줄여, 확장 가능한 sim-to-real 로봇 학습에서 오프폴리시 강화학습이 빠르면서 안정적일 수 있음을 보여 준다.

## II. Related Work

**S025 — Original**

On-policy RL has been the dominant paradigm for simulation-based robot learning when environment interaction is cheap and massively parallelizable.

**S025 — 한국어**

환경 상호작용이 저렴하고 대규모 병렬화할 수 있을 때 온폴리시 강화학습은 simulation 기반 로봇 학습의 지배적인 paradigm이었다.

**S026 — Original**

Off-policy RL decouples data collection from policy optimization by storing transitions in a replay buffer and reusing them across updates.

**S026 — 한국어**

오프폴리시 강화학습은 transition을 replay buffer에 저장하고 여러 update에서 재사용해 데이터 수집과 policy 최적화를 분리한다.

**S027 — Original**

Off-policy model-free RL suffers from three persistent challenges: slow training, unstable training dynamics, and exploration in high-dimensional action spaces.

**S027 — 한국어**

오프폴리시 model-free 강화학습에는 느린 학습, 불안정한 학습 동역학, 고차원 행동 공간의 탐색이라는 세 가지 지속적인 문제가 있다.

**S028 — Original**

Prior work has primarily addressed each challenge in isolation.

**S028 — 한국어**

선행 연구는 주로 각 문제를 따로 다루었다.

**S029 — Original**

FlashSAC unifies these directions: it achieves fast training by sharply reducing gradient updates while scaling model capacity and data throughput, maintains stable training dynamics by jointly bounding weight, feature, and gradient norms, and adopts a lightweight noise-repetition scheme that produces temporally-correlated exploration without per-environment overhead.

**S029 — 한국어**

FlashSAC은 이 흐름들을 통합한다. 모델 용량과 데이터 처리량을 키우면서 gradient update를 크게 줄여 빠르게 학습하고, weight·feature·gradient norm을 함께 제한해 안정적인 학습 동역학을 유지하며, 환경별 overhead 없이 시간적으로 상관된 탐색을 만드는 가벼운 noise repetition을 사용한다.

## III. Preliminary

**S030 — Original**

We model robotic control as a discounted Markov Decision Process (MDP), \(\mathcal M=(\mathcal S,\mathcal A,P,r,\gamma)\).

**S030 — 한국어**

로봇 제어를 할인된 Markov Decision Process(MDP) \(\mathcal M=(\mathcal S,\mathcal A,P,r,\gamma)\)로 모델링한다.

- **용어·약어 해설**
  - **MDP (Markov Decision Process, 마르코프 의사결정과정)**: 상태, 행동, 전이확률, 보상, 할인율로 순차 의사결정을 표현한다.

**S031 — Original**

The goal is to learn a policy \(\pi(a|s)\) that maximizes the discounted sum of rewards.

**S031 — 한국어**

목표는 할인된 보상 합을 최대화하는 policy \(\pi(a|s)\)를 학습하는 것이다.

**S032 — Original**

SAC stores transitions \((s,a,r,s')\) collected under past policies in a replay buffer \(\mathcal D\), and trains the policy using samples drawn from this buffer.

**S032 — 한국어**

SAC은 과거 policy가 수집한 transition \((s,a,r,s')\)을 replay buffer \(\mathcal D\)에 저장하고 이 buffer에서 뽑은 sample로 policy를 학습한다.

**S033 — Original**

Beyond maximizing expected return, SAC incorporates an entropy regularization term that encourages exploration.

**S033 — 한국어**

SAC은 기대 return을 최대화하는 것에 더해 탐색을 장려하는 entropy regularization 항을 포함한다.

**S034 — Original**

To reduce approximation errors in bootstrapped value learning, SAC commonly employs clipped double Q-learning, maintaining two action-value functions.

**S034 — 한국어**

SAC은 부트스트래핑 가치학습의 근사 오차를 줄이기 위해 보통 두 개의 action-value 함수를 유지하는 clipped double Q-learning을 사용한다.

**S035 — Original**

The minimum of the two estimates is used when forming targets, reducing the impact of optimistic value errors.

**S035 — 한국어**

target을 만들 때 두 추정값의 최솟값을 사용하여 낙관적인 가치 오차의 영향을 줄인다.

**S036 — Original**

Each critic is trained by minimizing a bootstrapped Bellman error using slowly updated target networks.

**S036 — 한국어**

각 critic은 천천히 갱신되는 target network를 사용한 부트스트래핑 Bellman 오차를 최소화하도록 학습한다.

### 수식 (2)~(5) 해설

\[
\mathcal L_\pi(\theta)=\mathbb E_{s\sim\mathcal D,a\sim\pi_\theta}
\left[\alpha\log\pi_\theta(a|s)-\min_{i=1,2}Q_{\phi_i}(s,a)\right]
\]

Actor는 높은 Q-value를 선호하되 \(\alpha\log\pi\) entropy 항으로 탐색을 유지한다.

\[
\bar\phi_j\leftarrow\tau\phi_j+(1-\tau)\bar\phi_j,\quad j\in\{1,2\}
\]

\(\tau\)가 작은 exponential moving average는 target critic을 천천히 움직인다.

\[
\mathcal L_Q(\phi_i)=\mathbb E_{(s,a,r,s')\sim\mathcal D}
\left[Q_{\phi_i}(s,a)-y\right]^2
\]

\[
y=r+\gamma\left(\min_jQ_{\bar\phi_j}(s',a')-\alpha\log\pi_\theta(a'|s')\right),
\quad a'\sim\pi_\theta(\cdot|s')
\]

target \(y\)가 target critic의 예측을 포함한다는 점이 효율과 불안정성의 공통 근원이다.

## IV. FlashSAC

**S037 — Original**

FlashSAC achieves strong asymptotic performance with fast wall-clock time through three complementary mechanisms.

**S037 — 한국어**

FlashSAC은 서로 보완하는 세 가지 mechanism으로 높은 점근 성능과 빠른 wall-clock 시간을 달성한다.

**S038 — Original**

FlashSAC takes a different approach inspired by the scaling trends observed in supervised learning: under a fixed compute budget, larger models trained with larger batches and fewer updates converge faster than smaller models with frequent updates.

**S038 — 한국어**

FlashSAC은 지도학습의 scaling 경향에서 착안해 고정 compute 예산에서 큰 batch와 적은 update로 학습한 큰 모델이 자주 update한 작은 모델보다 빨리 수렴한다는 다른 접근을 취한다.

**S039 — Original**

We collect data using 1024 parallel simulation environments, enabling rapid accumulation of diverse trajectories.

**S039 — 한국어**

1024개 병렬 simulation 환경에서 데이터를 수집하여 다양한 trajectory를 빠르게 축적한다.

**S040 — Original**

FlashSAC uses a replay buffer of up to 10M transitions, an order of magnitude larger than the 1M commonly used in standard off-policy configurations.

**S040 — 한국어**

FlashSAC은 표준 오프폴리시 설정에서 흔히 쓰는 1백만보다 한 자릿수 큰 최대 1천만 transition replay buffer를 사용한다.

**S041 — Original**

A larger buffer preserves such long-tail experiences and maintains the diversity of training data available to the critic throughout learning.

**S041 — 한국어**

더 큰 buffer는 이런 long-tail 경험을 보존하고 학습 내내 critic이 사용할 수 있는 학습 데이터의 다양성을 유지한다.

**S042 — Original**

FlashSAC employs a 2.5M-parameter, 6-layer network for both the actor and critic, paired with a batch size of 2048 that nearly saturates GPU utilization.

**S042 — 한국어**

FlashSAC은 actor와 critic에 각각 2.5M 파라미터의 6층 network를 사용하고 GPU 이용률을 거의 포화시키는 batch size 2048을 결합한다.

**S043 — Original**

The updates-to-data ratio is set to 2/1024, meaning only 2 gradient updates are performed per 1024 new transitions.

**S043 — 한국어**

UTD 비율은 2/1024로, 새 transition 1024개마다 gradient update를 2번만 수행한다.

- **용어·약어 해설**
  - **UTD (Updates-to-Data ratio)**: 새로 얻은 데이터량 대비 최적화 update 횟수다.

**S044 — Original**

We use mixed-precision throughout training, which reduces wall-clock time by 5-10%.

**S044 — 한국어**

학습 전체에서 mixed precision을 사용하며, 저자들은 이것이 wall-clock 시간을 5~10% 줄인다고 보고한다.

**S045 — Original**

After the final block, we apply RMSNorm to bound per-sample feature norms before value heads, preventing out-of-distribution inputs from producing unbounded activations that destabilize bootstrapping.

**S045 — 한국어**

마지막 block 뒤 value head 앞에 RMSNorm을 적용해 sample별 feature norm을 제한하고, 분포 밖 입력이 부트스트래핑을 불안정하게 만드는 무제한 activation을 생성하지 못하게 한다.

**S046 — Original**

We apply batch normalization before each nonlinearity to keep activations well-scaled.

**S046 — 한국어**

activation scale을 적절하게 유지하도록 각 nonlinearity 앞에 BatchNorm을 적용한다.

**S047 — Original**

We concatenate current and next-state transitions into a single batch so that both share the same statistics, ensuring consistency in the Bellman update.

**S047 — 한국어**

현재 상태와 다음 상태 transition을 하나의 batch로 연결하여 같은 statistics를 공유하게 하고 Bellman update의 일관성을 확보한다.

**S048 — Original**

We represent the Q-value as a categorical distribution over atoms uniformly spaced on a fixed support.

**S048 — 한국어**

Q-value를 고정 support에 균일하게 놓인 atom들의 categorical distribution으로 표현한다.

**S049 — Original**

This distributional formulation smooths the optimization landscape and reduces sensitivity to noisy targets.

**S049 — 한국어**

이 distributional formulation은 optimization landscape를 매끄럽게 하고 noisy target에 대한 민감도를 낮춘다.

**S050 — Original**

After each gradient step, we project each weight vector onto the unit-norm sphere and each normalization parameter vector to norm \(\sqrt d\).

**S050 — 한국어**

각 gradient step 뒤 모든 weight vector를 unit-norm sphere에 projection하고 normalization parameter vector는 norm \(\sqrt d\)가 되게 한다.

**S051 — Original**

This constrains the network to encode information through direction rather than scale.

**S051 — 한국어**

이 제약은 network가 scale보다 방향으로 정보를 encoding하게 한다.

**S052 — Original**

We set \(\sigma_{\mathrm{tgt}}=0.15\) in all experiments.

**S052 — 한국어**

모든 실험에서 \(\sigma_{\mathrm{tgt}}=0.15\)로 설정한다.

**S053 — Original**

At each repetition interval, a noise vector is sampled for action selection and held constant for \(k\) consecutive steps.

**S053 — 한국어**

각 반복 구간에서 행동 선택용 noise vector를 sample하고 연속 \(k\) step 동안 일정하게 유지한다.

**S054 — Original**

The repetition length \(k\) is drawn from a Zeta distribution, favoring short repeat intervals while occasionally producing long, correlated action sequences.

**S054 — 한국어**

반복 길이 \(k\)는 Zeta 분포에서 뽑아 짧은 반복 구간을 선호하되 가끔 길고 상관된 행동 sequence를 만든다.

### 수식 (6): adaptive reward scaling

\[
\bar r_t=
\frac{r_t}
{\max\left(\sqrt{\sigma^2_{t,G}+\epsilon},\,G_{t,\max}/G_{\max}\right)}
\]

- \(r_t\): 원래 reward
- \(\sigma^2_{t,G}\): running discounted return variance
- \(G_{t,\max}\): 관찰된 return의 running maximum magnitude
- \(G_{\max}\): distributional critic support의 상한

분모가 너무 작아지는 것을 막으면서 critic의 고정 support 안에 effective return을 유지한다.

### 수식 (7): unified entropy target

\[
\bar{\mathcal H}=\frac{1}{2}|\mathcal A|
\log(2\pi e\sigma_{\mathrm{tgt}}^2)
\]

action dimension \(|\mathcal A|\)에 선형으로 비례하므로 embodiment마다 target entropy를 따로 손으로 지정하는 부담을 줄인다.

## V. Experiments

**S055 — Original**

We evaluate FlashSAC on a diverse suite of robotic control tasks, measuring both asymptotic performance and wall-clock time on a single RTX 5090 GPU.

**S055 — 한국어**

단일 RTX 5090 GPU에서 점근 성능과 wall-clock 시간을 모두 측정하며 다양한 로봇 제어 과제에서 FlashSAC을 평가한다.

**S056 — Original**

Off-policy methods are trained for 50M environment steps, while PPO is trained for 200M steps, requiring approximately three times the compute of FlashSAC.

**S056 — 한국어**

오프폴리시 방법은 50M environment step 동안 학습하고 PPO는 200M step 동안 학습하여 FlashSAC의 약 3배 compute가 필요하다.

**S057 — Original**

On low-dimensional tasks, FlashSAC slightly outperforms PPO.

**S057 — 한국어**

저차원 과제에서 FlashSAC은 PPO를 약간 앞선다.

**S058 — Original**

On high-dimensional tasks, FlashSAC demonstrates a clear and consistent advantage.

**S058 — 한국어**

고차원 과제에서는 FlashSAC이 분명하고 일관된 우위를 보인다.

**S059 — Original**

Compared to FastTD3, FlashSAC is markedly more stable, converging across all tasks where FastTD3 frequently fails or underperforms.

**S059 — 한국어**

FastTD3와 비교하면 FlashSAC은 훨씬 안정적이며 FastTD3가 자주 실패하거나 낮은 성능을 보인 과제에서도 모두 수렴한다.

**S060 — Original**

In the single-environment setting, FlashSAC matches or exceeds dedicated sample-efficient methods without task-specific tuning.

**S060 — 한국어**

단일 환경 설정에서도 FlashSAC은 과제별 tuning 없이 전용 sample-efficient 방법과 같거나 높은 성능을 보인다.

**S061 — Original**

All vision-based methods are trained for 1M environment steps with an action repeat of 2.

**S061 — 한국어**

모든 vision 기반 방법은 action repeat 2로 1M environment step 동안 학습한다.

**S062 — Original**

Across vision-based tasks, FlashSAC matches or exceeds all baselines in asymptotic performance while converging faster in wall-clock time.

**S062 — 한국어**

vision 기반 과제에서 FlashSAC은 모든 baseline과 같거나 높은 점근 성능을 보이면서 wall-clock 시간 기준으로 더 빨리 수렴한다.

**S063 — Original**

On flat terrain, FlashSAC achieves stable real-world locomotion after approximately 20 minutes of training, whereas PPO requires about 3 hours to reach comparable performance.

**S063 — 한국어**

평지에서 FlashSAC은 약 20분 학습 뒤 안정적인 현실 보행을 달성하지만 PPO가 비슷한 성능에 도달하려면 약 3시간이 필요하다.

**S064 — Original**

FlashSAC successfully climbs unseen stairs after approximately 4 hours of training, while PPO requires nearly 20 hours to achieve a similar capability.

**S064 — 한국어**

FlashSAC은 약 4시간 학습 뒤 훈련에서 보지 않은 계단을 성공적으로 오르지만 PPO가 비슷한 능력을 얻는 데는 거의 20시간이 필요하다.

- **번역자 주:** 이 시간은 simulation 학습 시간이며 실제 robot의 안전 검증 시간 전체를 뜻하지 않는다.

## VI. Analysis

**S065 — Original**

Off-policy data covers a substantially broader region of the state-action space, reflecting experience accumulated across diverse behavior policies stored in the replay buffer.

**S065 — 한국어**

오프폴리시 데이터는 replay buffer에 저장된 다양한 behavior policy의 누적 경험을 반영하여 상태-행동 공간의 훨씬 넓은 영역을 덮는다.

**S066 — Original**

On-policy data, by contrast, is tightly concentrated around the final policy's distribution.

**S066 — 한국어**

반면 온폴리시 데이터는 최종 policy의 분포 주변에 조밀하게 집중된다.

**S067 — Original**

Increasing replay buffer size improves performance up to 10M transitions by stabilizing training.

**S067 — 한국어**

Replay buffer를 최대 10M transition까지 늘리면 학습이 안정되어 성능이 좋아진다.

**S068 — Original**

However, overly large buffers such as 50M slow learning because recent high-quality samples are drawn less frequently.

**S068 — 한국어**

그러나 50M처럼 지나치게 큰 buffer는 최근의 고품질 sample이 덜 자주 뽑히므로 학습을 늦춘다.

**S069 — Original**

Increasing batch size and model capacity, along with reducing the UTD ratio, accelerate convergence.

**S069 — 한국어**

Batch size와 model capacity를 키우고 UTD 비율을 줄이면 수렴이 빨라진다.

**S070 — Original**

As architectural components are added, parameter, feature, and gradient norms remain bounded throughout training with no uncontrolled growth.

**S070 — 한국어**

Architecture 구성 요소를 추가할수록 parameter, feature, gradient norm이 제어되지 않은 채 커지지 않고 학습 내내 제한된 범위에 머문다.

**S071 — Original**

The condition number also decreases monotonically, reaching its lowest value with the full FlashSAC architecture.

**S071 — 한국어**

Condition number도 단조롭게 감소해 완전한 FlashSAC architecture에서 가장 낮아진다.

**S072 — Original**

Repeating sampled action noise across consecutive steps produces coherent exploratory trajectories rather than uncorrelated perturbations that are quickly averaged out by the dynamics in high-dimensional control tasks.

**S072 — 한국어**

Sample한 action noise를 연속 step에서 반복하면 고차원 제어 동역학에 의해 빠르게 평균화되는 비상관 perturbation 대신 일관된 탐색 trajectory가 만들어진다.

## VII. Lessons and Opportunities

**S073 — Original**

We presented FlashSAC, a fast and stable off-policy RL framework for high-dimensional robotics.

**S073 — 한국어**

우리는 고차원 로봇을 위한 빠르고 안정적인 오프폴리시 강화학습 framework FlashSAC을 제시했다.

**S074 — Original**

Off-policy RL is an appealing alternative, but its adoption has been limited by slow training speed and instability in critic learning arising from function approximation error and bootstrapped updates.

**S074 — 한국어**

오프폴리시 강화학습은 매력적인 대안이지만 function approximation error와 부트스트래핑 update에서 생기는 느린 학습과 critic 불안정성 때문에 채택이 제한되었다.

**S075 — Original**

FlashSAC addresses these challenges by scaling data and model capacity while reducing gradient updates, and integrating explicit architectural constraints on critic updates.

**S075 — 한국어**

FlashSAC은 데이터와 모델 용량을 키우면서 gradient update를 줄이고 critic update에 명시적인 architecture 제약을 통합하여 이 문제를 다룬다.

**S076 — Original**

Together, these yield strong asymptotic performance and up to an order-of-magnitude reduction in wall-clock time compared to on-policy methods.

**S076 — 한국어**

이 구성들은 함께 높은 점근 성능과 온폴리시 방법 대비 최대 한 자릿수 규모의 wall-clock 시간 단축을 만든다.

**S077 — Original**

While this work focuses on state-based control, extending these critic-stabilization principles to tactile-based learning is a promising direction for future work.

**S077 — 한국어**

이 연구는 state 기반 제어에 초점을 맞추지만 critic 안정화 원리를 tactile 기반 학습으로 확장하는 것은 유망한 후속 연구 방향이다.

## Acknowledgements 요약

저자들은 Younggyo Seo와 Yekyung Nah의 의견에 감사를 표한다. 연구는 IITP의 Korea government(MSIT) grant, KAIST AI 대학원 프로그램, hessian.AI의 독일 Excellence Strategy 지원, German Federal Ministry of Research, Technology and Space, Robotics Institute Germany의 지원을 받았다고 기록한다.

## 수식·그림 읽기 메모

- **Figure 1**: 저차원, 고차원, sim-to-real 세 범주를 한눈에 비교한다. 서로 다른 과제의 정규화 score를 절대값처럼 비교하지 않는다.
- **Figure 2**: inverted residual block 안에서 차원을 \(d\to4d\to d\)로 확장·축소하고 BatchNorm, ReLU, residual, 마지막 RMSNorm을 배치한다.
- **Figure 3~5**: x축은 environment step이 아니라 compute time이다. curve의 최종 높이와 수렴 속도를 함께 읽는다.
- **Figure 6**: 실제 Unitree G1 계단 보행과 simulation 학습 시간을 비교한다.
- **Figure 7**: replay buffer의 off-policy 표본이 final policy rollout보다 넓은 상태-행동 영역을 덮는다는 정성·밀도 근거다.
- **Figure 8**: buffer는 무조건 클수록 좋지 않으며 50M에서 최근 표본 희석 trade-off가 보인다.
- **Figure 9**: 구성 요소를 누적하는 ablation이다. 개별 요소의 완전한 독립 효과와 동일하지 않다.
- **Figure 10**: \(\sigma_{\mathrm{tgt}}\) 0.15~0.2가 비슷하게 작동하고 noise repetition이 aggregate score를 개선한다.

## 약어 및 기술 용어 사전

| 원어·약어 | 한국어 | 의미 | 최초 등장 |
|---|---|---|---|
| RL | 강화학습 | reward로 policy를 학습하는 순차 의사결정 | S006 |
| PPO | 근접 정책 최적화 | 온폴리시 policy gradient 방법 | S003 |
| Off-policy RL | 오프폴리시 강화학습 | 과거 policy의 데이터도 재사용 | S007 |
| SAC | Soft Actor-Critic | entropy regularization 오프폴리시 actor-critic | S009 |
| Critic | 가치 평가기 | \(Q(s,a)\)를 예측 | S008 |
| Bootstrapping | 부트스트래핑 | 미래 예측을 현재 target에 사용 | S008 |
| MDP | 마르코프 의사결정과정 | 상태·행동·전이·보상·할인율 모델 | S030 |
| Replay buffer | 재현 버퍼 | 과거 transition 저장소 | S020 |
| UTD | 데이터 대비 업데이트 비율 | 새 데이터량 대비 gradient update | S043 |
| RMSNorm | 제곱평균제곱근 정규화 | feature scale을 제한하는 normalization | S045 |
| Distributional critic | 분포형 critic | scalar 대신 return 분포를 예측 | S048 |
| Sim-to-real | 시뮬레이션-현실 이전 | simulation policy를 실제 robot에 배치 | S005 |
| DoF | 자유도 | 독립적으로 움직이는 축의 수 | S012 |
| Wall-clock time | 실제 경과 시간 | 현실에서 측정한 학습 소요 시간 | S004 |

## 번역 검수 기록

- 2026-07-27: RSS PDF 14쪽 전체의 page count와 text layer를 확인했다.
- 2026-07-27: 14개 페이지를 PNG로 렌더링하고 제목, 다단 순서, 수식 (1)~(7), Figure 1~10, References 시작·종료 페이지를 시각 대조했다.
- 2026-07-27: 제목·저자는 RSS 공식 Paper ID 99 페이지와 대조했다.
- 2026-07-27: arXiv v2의 revision 날짜와 CC BY 4.0 license link를 확인했다.
- PDF abstract의 “over 60 tasks”와 RSS 프로그램 abstract의 “50+ tasks” 표현 차이를 보존하고 [분석 문서](README.md)에 기록했다.
- 본문에서 가능성을 말하는 “can”, “promising”은 확정 사실로 강화하지 않았다.
