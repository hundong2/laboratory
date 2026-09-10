# Towards Realistic Earth-Observation Constellation Scheduling: Benchmark and Methodology — 문장 대조 번역

## 논문 메타데이터

| 항목 | 내용 |
|---|---|
| 원문 제목 | Towards Realistic Earth-Observation Constellation Scheduling: Benchmark and Methodology |
| 한국어 제목 | 현실적인 지구관측 군집위성 스케줄링을 향하여: 벤치마크와 방법론 |
| 저자 | Luting Wang, Yinghao Xiang, Hongliang Huang, Dongjun Li, Chen Gao, Si Liu |
| 출판처 | Advances in Neural Information Processing Systems 38, NeurIPS 2025 Main Conference Track |
| DOI | `10.52202/085713-2878` |
| 최종 출판본 | https://proceedings.neurips.cc/paper_files/paper/2025/hash/7c40c5050bd029a3ea7ff8b01412f735-Abstract-Conference.html |
| 사용자 입력 | https://www.alphaxiv.org/pdf/2510.26297 |
| arXiv | `2510.26297v1`, 2025-10-30, https://arxiv.org/abs/2510.26297 |
| 사용한 버전 | NeurIPS 2025 최종 PDF, arXiv v1과 핵심 내용 대조 |
| 원문 언어 | 영어 |
| 접근일 | 2026-09-10 |
| 라이선스 | arXiv HTML 표시 기준 Creative Commons Attribution 4.0 International(CC BY 4.0) |

## 번역·접근 범위

| Section | 상태 | 범위 |
|---|---|---|
| 제목·초록 | 완료 | 전체 문장 대조 |
| 1 Introduction | 부분 번역 | 문제·기여·핵심 수치 전체, 반복 설명 압축 |
| 2 Related Work | 부분 번역 | 방법 계보와 차별점 중심 |
| 3 AEOS-Bench | 부분 번역 | 문제 설정·제약·수집·split 핵심 문장과 표 해설 |
| 4 AEOS-Former | 완료 | 핵심 설명과 식 (1)~(9) 대조·해설 |
| 5 Experiments | 부분 번역 | 설정·지표·주요 결과·ablation 중심 |
| 6 Conclusion | 완료 | 전체 |
| A Limitations | 완료 | 전체 |
| B Broader Impacts | 완료 | 전체 |
| C Scenario Modeling | 부분 번역 | 구성과 표 범위 중심 |
| References | 원문 링크 참조 | 서지 기록을 임의 번역하지 않음 |
| NeurIPS Paper Checklist | 부분 번역 | 연구 본문이 아닌 제출 체크리스트로서 핵심 답변만 요약 |

최종 PDF는 22쪽으로 시각 검사했다. 표·수식·그림이 포함된 2단 편집의 읽기 순서를 확인했으며, arXiv의 HTML 수식을 함께 대조했다. 아래에 없는 원문 문장을 번역 완료로 과장하지 않는다.

## 읽기 전 핵심 배경

- **AEOS (Agile Earth Observation Satellite, 민첩 지구관측 위성)**: 자세를 빠르게 바꿔 지상의 여러 목표를 촬영할 수 있는 위성이다.
- **constellation scheduling(군집위성 스케줄링)**: 여러 위성과 여러 촬영 작업을 시간·전력·자세·센서 제약 아래 배정하는 조합 최적화 문제다.
- **constraint-aware attention(제약 인식 어텐션)**: 모든 후보를 동일하게 비교하지 않고 물리적으로 가능한 위성-작업 쌍에 attention을 집중시키는 방식이다.
- **simulation-based iterative learning(시뮬레이션 기반 반복 학습)**: 모델이 만든 일정표를 simulator로 평가하고 좋은 결과를 다시 학습 데이터에 넣는 반복 절차다.

## Title

**S001 — Original**

Towards Realistic Earth-Observation Constellation Scheduling: Benchmark and Methodology

**S001 — 한국어**

(현실적인 지구관측 군집위성 스케줄링을 향하여: 벤치마크와 방법론)

## Abstract

**S002 — Original**

Agile Earth Observation Satellites (AEOSs) constellations offer unprecedented flexibility for monitoring the Earth’s surface, but their scheduling remains challenging under large-scale scenarios, dynamic environments, and stringent constraints.

**S002 — 한국어**

(민첩 지구관측 위성(AEOS) 군집은 지표면 감시에 전례 없는 유연성을 제공하지만, 대규모 시나리오·동적 환경·엄격한 제약 아래에서의 스케줄링은 여전히 어렵다.)

- **용어·약어 해설**
  - **AEOS (Agile Earth Observation Satellite, 민첩 지구관측 위성)**: 궤도 통과만 기다리지 않고 자세를 기동해 목표를 촬영한다.

**S003 — Original**

Existing methods often simplify these complexities, limiting their real-world performance.

**S003 — 한국어**

(기존 방법은 이러한 복잡성을 자주 단순화하며, 그 결과 현실 환경에서의 성능이 제한된다.)

**S004 — Original**

We address this gap with a unified framework integrating a standardized benchmark suite and a novel scheduling model.

**S004 — 한국어**

(우리는 표준화된 벤치마크 모음과 새로운 스케줄링 모델을 통합한 하나의 프레임워크로 이 간극을 해결한다.)

**S005 — Original**

Our benchmark suite, AEOS-Bench, contains 3,907 finely tuned satellite assets and 16,410 scenarios.

**S005 — 한국어**

(AEOS-Bench라는 벤치마크 모음에는 세밀하게 조정된 위성 자산 3,907개와 시나리오 16,410개가 들어 있다.)

**S006 — Original**

Each scenario features 1 to 50 satellites and 50 to 300 imaging tasks.

**S006 — 한국어**

(각 시나리오는 1~50기의 위성과 50~300개의 촬영 작업으로 구성된다.)

**S007 — Original**

These scenarios are generated via a high-fidelity simulation platform, ensuring realistic satellite behavior such as orbital dynamics and resource constraints.

**S007 — 한국어**

(이 시나리오들은 고충실도 시뮬레이션 플랫폼으로 생성되어 궤도 역학과 자원 제약 같은 현실적인 위성 동작을 반영한다.)

**S008 — Original**

Ground truth scheduling annotations are provided for each scenario.

**S008 — 한국어**

(각 시나리오에는 정답으로 사용하는 스케줄링 annotation이 제공된다.)

- **번역자 주:** 여기서 ground truth는 검수된 reference assignment이며, 모든 경우의 전역 최적해가 증명됐다는 뜻은 아니다.

**S009 — Original**

To our knowledge, AEOS-Bench is the first large-scale benchmark suite tailored for realistic constellation scheduling.

**S009 — 한국어**

(저자들이 아는 범위에서 AEOS-Bench는 현실적인 군집위성 스케줄링에 맞춘 최초의 대규모 벤치마크 모음이다.)

**S010 — Original**

Building upon this benchmark, we introduce AEOS-Former, a Transformer-based scheduling model that incorporates a constraint-aware attention mechanism.

**S010 — 한국어**

(이 벤치마크를 토대로 저자들은 제약 인식 어텐션 메커니즘을 포함한 Transformer 기반 스케줄링 모델 AEOS-Former를 제안한다.)

**S011 — Original**

A dedicated internal constraint module explicitly models the physical and operational limits of each satellite.

**S011 — 한국어**

(전용 내부 제약 모듈은 각 위성의 물리적·운용상 한계를 명시적으로 모델링한다.)

**S012 — Original**

Through simulation-based iterative learning, AEOS-Former adapts to diverse scenarios, offering a robust solution for AEOS constellation scheduling.

**S012 — 한국어**

(AEOS-Former는 시뮬레이션 기반 반복 학습을 통해 다양한 시나리오에 적응하며 AEOS 군집 스케줄링을 위한 견고한 해법을 제공한다.)

**S013 — Original**

Experimental results demonstrate that AEOS-Former outperforms baseline models in task completion and energy efficiency, with ablation studies highlighting the contribution of each component.

**S013 — 한국어**

(실험 결과에서 AEOS-Former는 작업 완수와 에너지 효율 면에서 기준 모델보다 우수하며, ablation study는 각 구성요소의 기여를 보여준다.)

- **용어·약어 해설**
  - **ablation study(절제 연구)**: 구성요소를 하나씩 제거하거나 추가해 성능 변화로 기여도를 추정한다.

## 1 Introduction

**S014 — Original**

Agile Earth Observation Satellites have emerged as a transformative technology in remote sensing, enabling rapid and flexible monitoring of the Earth’s surface.

**S014 — 한국어**

(민첩 지구관측 위성은 원격탐사에서 변혁적인 기술로 등장해 지표면을 빠르고 유연하게 감시할 수 있게 했다.)

**S015 — Original**

By operating cooperatively in constellations, multiple AEOSs can dramatically increase revisit frequency and broaden coverage beyond the capability of a single satellite.

**S015 — 한국어**

(여러 AEOS가 군집으로 협력하면 단일 위성의 능력을 넘어 재방문 빈도를 크게 높이고 관측 범위를 넓힐 수 있다.)

**S016 — Original**

The AEOS constellation scheduling problem seeks to optimally assign imaging tasks across satellites to maximize task completion while minimizing time and resource expenditure, all within real-world constraints.

**S016 — 한국어**

(AEOS 군집 스케줄링 문제는 현실 제약을 모두 지키면서 작업 완수를 최대화하고 시간과 자원 소비를 최소화하도록 촬영 작업을 위성들에 최적으로 배정하려 한다.)

**S017 — Original**

The challenge of AEOS constellation scheduling stems from three core factors.

**S017 — 한국어**

(AEOS 군집 스케줄링의 어려움은 세 가지 핵심 요인에서 나온다.)

**S018 — Original**

First, modern constellations may comprise dozens of satellites tasked with hundreds of imaging requests.

**S018 — 한국어**

(첫째, 현대의 군집은 수십 기 위성과 수백 건의 촬영 요청으로 구성될 수 있다.)

**S019 — Original**

This scale renders exhaustive searches infeasible and strains both heuristic algorithms and reinforcement-learning methods.

**S019 — 한국어**

(이 규모에서는 전수검색이 불가능해지고 heuristic algorithm과 reinforcement learning 방법 모두 큰 부담을 받는다.)

**S020 — Original**

Second, the operating environment is highly dynamic: new tasks can appear or expire at any moment, satellite positions and attitudes are continuously changing, batteries cycle through charge and discharge, and satellites may even join or leave the constellation.

**S020 — 한국어**

(둘째, 운용 환경은 매우 동적이다. 새 작업은 언제든 생기거나 만료되고, 위성의 위치와 자세는 계속 변하며, 배터리는 충전과 방전을 반복하고, 위성이 군집에 들어오거나 빠질 수도 있다.)

**S021 — Original**

Scheduling algorithms must adapt on the fly without foreknowledge of these changes.

**S021 — 한국어**

(스케줄링 알고리즘은 이러한 변화를 미리 알지 못한 채 즉석에서 적응해야 한다.)

**S022 — Original**

Third, every assignment of tasks must respect strict constraints, such as the available battery energy, the sensor field of view, and the allowable time window for each task, or the imaging request cannot be fulfilled.

**S022 — 한국어**

(셋째, 모든 작업 배정은 가용 배터리 에너지, 센서 시야, 작업별 허용 시간창 같은 엄격한 제약을 지켜야 하며 그렇지 않으면 촬영 요청을 완수할 수 없다.)

**S023 — Original**

Any practical scheduling model must simultaneously scale to large constellations, adapt in real time, and respect every operational constraint.

**S023 — 한국어**

(실용적인 스케줄링 모델은 대규모 군집으로 확장되고 실시간으로 적응하면서 모든 운용 제약을 동시에 지켜야 한다.)

**S024 — Original**

Moreover, the absence of a common benchmark prevents fair comparison across scheduling models.

**S024 — 한국어**

(또한 공통 벤치마크가 없으면 스케줄링 모델끼리 공정하게 비교할 수 없다.)

**S025 — Original**

Our benchmark is built on a simulation platform powered by the Basilisk engine, which accurately models each satellite’s orbital dynamics, attitude control, and other physical characteristics.

**S025 — 한국어**

(이 벤치마크는 Basilisk 엔진 기반 시뮬레이션 플랫폼 위에 구축되며, 각 위성의 궤도 역학·자세 제어·기타 물리 특성을 정밀하게 모델링한다.)

**S026 — Original**

AEOS-Bench includes 16,410 scenarios, each featuring 1 to 50 satellites, 50 to 300 imaging tasks, and 3,600 timesteps.

**S026 — 한국어**

(AEOS-Bench에는 16,410개 시나리오가 있으며, 각 시나리오는 1~50기 위성, 50~300개 촬영 작업, 3,600 timestep으로 구성된다.)

**S027 — Original**

The test split incorporates real satellite data from publicly available sources, enabling evaluation on authentic data.

**S027 — 한국어**

(test split은 공개 출처의 실제 위성 데이터를 포함해 현실 데이터에서 평가할 수 있게 한다.)

**S028 — Original**

By predicting a feasibility probability and minimal control time, this module produces a constraint-driven attention mask to guide scheduling.

**S028 — 한국어**

(이 모듈은 실행 가능성 확률과 최소 제어 시간을 예측해 스케줄링을 이끄는 제약 기반 attention mask를 만든다.)

**S029 — Original**

After pretraining on AEOS-Bench annotations, it is deployed in our simulator to explore random scenarios.

**S029 — 한국어**

(AEOS-Bench annotation으로 사전학습한 뒤 모델을 simulator에 배치해 무작위 시나리오를 탐색한다.)

**S030 — Original**

Schedules exceeding a preset performance threshold are merged back into AEOS-Bench for retraining.

**S030 — 한국어**

(미리 정한 성능 임계값을 넘는 schedule은 AEOS-Bench에 다시 합쳐 재학습에 사용한다.)

## 2 Related Work

**S031 — Original**

Methods can be broadly classified as optimization-based or neural-network-based.

**S031 — 한국어**

(방법은 크게 최적화 기반과 신경망 기반으로 분류할 수 있다.)

**S032 — Original**

Most existing benchmarks for multi-satellite scheduling include fewer than 10 scenarios, limiting their diversity and generalizability.

**S032 — 한국어**

(기존 다중 위성 스케줄링 벤치마크 대부분은 시나리오가 10개보다 적어 다양성과 일반화 가능성이 제한된다.)

**S033 — Original**

Early studies rely on exact solvers to optimize satellite assignments.

**S033 — 한국어**

(초기 연구는 위성 배정을 최적화하기 위해 exact solver에 의존한다.)

**S034 — Original**

Although these methods guarantee optimality, their computational cost escalates sharply with the problem scale.

**S034 — 한국어**

(이 방법들은 최적성을 보장하지만 문제 규모가 커지면 계산비용이 급격히 증가한다.)

**S035 — Original**

Subsequent heuristic methods aim to improve scalability.

**S035 — 한국어**

(후속 heuristic 방법들은 확장성을 개선하려 한다.)

**S036 — Original**

While these methods offer faster runtimes, their performance diminishes with large-scale or dynamic scenarios.

**S036 — 한국어**

(이 방법들은 실행시간은 더 짧지만 대규모 또는 동적 시나리오에서 성능이 저하된다.)

**S037 — Original**

Pointer Networks provide a sequence-to-sequence formulation for combinatorial assignments.

**S037 — 한국어**

(Pointer Network는 조합 배정 문제를 sequence-to-sequence 형식으로 표현한다.)

**S038 — Original**

Despite promising results, many of these methods simplify key physical constraints.

**S038 — 한국어**

(유망한 결과에도 불구하고 이 방법들 가운데 다수는 핵심 물리 제약을 단순화한다.)

**S039 — Original**

In contrast, our AEOS-Former integrates an intrinsic constraint module that explicitly enforces physical and operational limitations, substantially improving the feasibility and fidelity of generated schedules.

**S039 — 한국어**

(반면 AEOS-Former는 물리·운용 한계를 명시적으로 반영하는 내재적 제약 모듈을 통합해 생성 일정의 실행 가능성과 충실도를 크게 개선한다.)

## 3 The AEOS-Bench Suite

### 3.1 Problem Setup

**S040 — Original**

To capture the essential physics that determines task feasibility, we model each satellite as a composition of four core subsystems: orbital dynamics, attitude control, power system, and sensor payload.

**S040 — 한국어**

(작업 실행 가능성을 결정하는 핵심 물리를 포착하기 위해 각 위성을 궤도 역학, 자세 제어, 전력계, 센서 탑재체의 네 하위 시스템으로 모델링한다.)

**S041 — Original**

Satellites occupy low-Earth orbit, with parameters like orbital elements, mass properties, and moments of inertia sampled uniformly from representative ranges.

**S041 — 한국어**

(위성은 저궤도에 있으며 궤도요소, 질량 특성, 관성모멘트 같은 매개변수는 대표 범위에서 균등 표본추출된다.)

**S042 — Original**

Attitude control employs the Modified Rodrigues Parameters formalism, with control gains and actuator limits specified per satellite.

**S042 — 한국어**

(자세 제어에는 MRP 형식을 사용하며 제어 이득과 actuator 한계는 위성별로 지정한다.)

- **용어·약어 해설**
  - **MRP (Modified Rodrigues Parameters, 수정 로드리게스 매개변수)**: 회전을 3개 매개변수로 표현하는 자세 표현법이다.

**S043 — Original**

Imaging tasks arrive dynamically, each defined by a release time, due time, required observation duration, and the ground-target coordinates.

**S043 — 한국어**

(촬영 작업은 동적으로 도착하며 각 작업은 공개 시각, 마감 시각, 필요한 관측 지속시간, 지상 목표 좌표로 정의된다.)

**S044 — Original**

We adopt a two-tier action abstraction to separate high-level scheduling from low-level control.

**S044 — 한국어**

(고수준 스케줄링과 저수준 제어를 분리하기 위해 2계층 행동 추상화를 사용한다.)

**S045 — Original**

The scheduler outputs an assignment vector a, where each element selects sensor-off or a task for one satellite.

**S045 — 한국어**

(스케줄러는 배정 벡터 `a`를 출력하며 각 원소는 해당 위성의 센서 끄기 또는 수행 작업을 선택한다.)

**S046 — Original**

We enforce 5 constraints in our platform: dynamics, energy, FOV, continuity, and time window.

**S046 — 한국어**

(플랫폼은 dynamics, energy, FOV, continuity, time window의 다섯 제약을 강제한다.)

**S047 — Original**

Any high-level assignment that violates these constraints is rejected by the simulator, and only successful observations are recorded for downstream benchmarking.

**S047 — 한국어**

(이 제약을 위반한 고수준 배정은 simulator가 거부하며, 성공한 관측만 이후 벤치마킹을 위해 기록한다.)

### 3.2 Data Collection

**S048 — Original**

Low control gains result in slow attitude adjustments, while overloaded actuators can destabilize the satellite, risking task failures.

**S048 — 한국어**

(제어 이득이 낮으면 자세 조정이 느리고 actuator에 과부하가 걸리면 위성이 불안정해져 작업 실패 위험이 생긴다.)

**S049 — Original**

While our platform supports closed-loop simulation, training scheduling models from scratch via simulator roll-outs is computationally expensive.

**S049 — 한국어**

(플랫폼은 closed-loop simulation을 지원하지만 simulator rollout으로 스케줄링 모델을 처음부터 학습하는 것은 계산비용이 크다.)

**S050 — Original**

Each AEOS-Bench scenario begins with a distance-based initialization.

**S050 — 한국어**

(각 AEOS-Bench 시나리오는 거리 기반 초기화에서 시작한다.)

**S051 — Original**

While simple and intuitive, this method often assigns tasks that lie too close to the satellite, leading to attitude control failures.

**S051 — 한국어**

(이 방법은 단순하고 직관적이지만 위성에 지나치게 가까운 작업을 자주 배정해 자세 제어 실패로 이어진다.)

**S052 — Original**

Therefore, we introduce the iterative filter stage and human quality review.

**S052 — 한국어**

(따라서 저자들은 반복 filtering 단계와 사람의 품질 검토를 도입한다.)

### 3.3 Data Analysis

**S053 — Original**

The train split consists of 16,218 trajectories with 2,907 satellite assets.

**S053 — 한국어**

(train split은 2,907개 위성 자산을 사용하는 16,218개 trajectory로 구성된다.)

**S054 — Original**

The val-seen split includes 64 scenarios using the same satellites as the train split.

**S054 — 한국어**

(val-seen split은 train split과 같은 위성을 사용하는 64개 시나리오다.)

**S055 — Original**

The val-unseen split features 64 scenarios with 500 satellites not present in the train split.

**S055 — 한국어**

(val-unseen split은 train split에 없는 위성 500개로 만든 64개 시나리오다.)

**S056 — Original**

The test split contains 64 scenarios with 500 satellites, each having realistic properties sourced from the web.

**S056 — 한국어**

(test split에는 웹에서 얻은 현실적 특성을 가진 위성 500개로 구성한 64개 시나리오가 있다.)

## 4 The AEOS-Former Model

### 4.1 Dynamic Data Processing

**S057 — Original**

Dynamic properties, such as task progress and satellite attitude, are not contained within these static matrices.

**S057 — 한국어**

(작업 진행도와 위성 자세 같은 동적 특성은 정적 행렬에 들어 있지 않다.)

**S058 — Original**

Instead, we query our simulator at each timestep to retrieve the current dynamic satellite and task properties.

**S058 — 한국어**

(대신 매 timestep마다 simulator를 조회해 현재 위성과 작업의 동적 특성을 가져온다.)

**S059 — Original / Equation (1)**

`S=[S^s;S^d]∈R^(N_S×d_S), T=[T^s;T^d]∈R^(N_T×d_T)`

**S059 — 한국어**

(위성 입력 `S`와 작업 입력 `T`는 각각 정적 feature와 동적 feature를 feature 축으로 이어 붙인 행렬이다.)

- `N_S`, `N_T`: 위성과 작업 개수
- `d_S`, `d_T`: 결합한 feature 차원
- 출력 shape는 각각 `N_S × d_S`, `N_T × d_T`다.

**S060 — Original**

To embed temporal context into AEOS-Former, we incorporate a sinusoidal time embedding at the current timestep.

**S060 — 한국어**

(AEOS-Former에 시간 맥락을 넣기 위해 현재 timestep의 sinusoidal time embedding을 사용한다.)

**S061 — Original**

Task release and due times are converted into relative time offsets with respect to the current timestep.

**S061 — 한국어**

(작업의 공개 시각과 마감 시각은 현재 timestep에 대한 상대 시간 offset으로 변환한다.)

### 4.2 The Internal Constraint Module

**S062 — Original / Equation (2)**

`f̂_i,j = C([S_i;T_j]), 1≤i≤N_S, 1≤j≤N_T`

**S062 — 한국어**

(내부 제약 모듈 `C`는 위성 `i`와 작업 `j`의 feature를 결합해 해당 쌍의 예측값을 만든다.)

**S063 — Original**

The output comprises two components: a predicted feasibility logit and an estimated time for attitude adjustment.

**S063 — 한국어**

(출력은 예측된 실행 가능성 logit과 추정 자세 조정 시간의 두 성분으로 구성된다.)

**S064 — Original**

Many tasks are accomplished through the collaboration of multiple satellites, making it challenging to attribute task completion to individual satellites directly.

**S064 — 한국어**

(많은 작업이 여러 위성의 협력으로 완수되므로 작업 완수의 기여를 개별 위성에 직접 귀속하기 어렵다.)

**S065 — Original**

We set the approximate label to one if a satellite contributed to a completed task for at least n consecutive timesteps.

**S065 — 한국어**

(한 위성이 완수된 작업에 적어도 `n`개 연속 timestep 동안 기여했다면 근사 label을 1로 둔다.)

**S066 — Original / Equation (3)**

`L_s = (1/(N_S N_T)) Σ_i Σ_j BCE(ŝ_i,j,s̃_i,j)`

**S066 — 한국어**

(실행 가능성 손실 `L_s`는 모든 위성-작업 쌍의 예측 logit과 근사 이진 label 사이 BCE 평균이다.)

**S067 — Original / Equation (4)**

`L_t = Σ_i Σ_j s̃_i,j MSE(t̂_i,j,t̃_i,j) / Σ_i Σ_j s̃_i,j`

**S067 — 한국어**

(시간 손실 `L_t`는 positive pair에 대해서만 예측 제어시간과 기준 제어시간의 MSE를 평균한다.)

- **번역자 주:** positive pair가 하나도 없으면 분모가 0이 되므로 구현에서 해당 batch를 건너뛰거나 epsilon 처리가 필요하다.

### 4.3 Satellite-Task Matching

**S068 — Original / Equation (5)**

`E_S=[E_S(S);E_t], E_T=[E_T(T);E_t]`

**S068 — 한국어**

(위성과 작업 projection에 현재 시간 embedding을 각각 결합한다.)

**S069 — Original**

Categorical data are looked up in embedding matrices, while continuous ones use linear projections.

**S069 — 한국어**

(범주형 데이터는 embedding matrix에서 조회하고 연속형 데이터는 linear projection을 사용한다.)

**S070 — Original**

The decoder attends to tasks under a cross-attention mask derived from the constraint logits.

**S070 — 한국어**

(decoder는 constraint logit에서 만든 cross-attention mask 아래 작업 feature에 attention한다.)

**S071 — Original**

The mask is defined as `M_i,j = w × ŝ_i,j + b`, with `w,b` initialized to zero for stable training.

**S071 — 한국어**

(mask는 `M_i,j=w×ŝ_i,j+b`로 정의하며 안정적인 학습을 위해 `w,b`를 0으로 초기화한다.)

**S072 — Original / Equation (6)**

`A=h_S · [h_φ;h_T]^T ∈ R^(N_S×(1+N_T))`

**S072 — 한국어**

(assignment score matrix `A`는 각 위성 표현과 null 선택 및 모든 작업 표현의 내적으로 계산한다.)

**S073 — Original**

The null assignment is represented by a trainable vector.

**S073 — 한국어**

(아무 작업도 하지 않는 null assignment는 학습 가능한 vector로 표현한다.)

**S074 — Original / Equation (8)**

`â_i = -1 + argmax_j 1{σ(ŝ_i,j)>τ_s} · A_i,j`

**S074 — 한국어**

(추론에서는 feasibility probability가 임계값 `τ_s`보다 큰 작업만 남긴 뒤 assignment score가 가장 큰 작업을 선택한다.)

### 4.4 Simulation-based Iterative Learning

**S075 — Original / Equation (9)**

`L = w_s L_s + w_t L_t + w_a L_a`

**S075 — 한국어**

(전체 손실은 실행 가능성, 제어 시간, 작업 배정 손실의 가중합이다.)

**S076 — Original**

This stage bootstraps the model with basic scheduling strategies learned from expert annotations.

**S076 — 한국어**

(지도학습 단계는 전문가 annotation에서 배운 기본 스케줄링 전략으로 모델을 초기화한다.)

**S077 — Original**

We then collect only those trajectories whose performance exceeds a predefined threshold.

**S077 — 한국어**

(그다음 성능이 미리 정의한 임계값을 넘는 trajectory만 수집한다.)

**S078 — Original**

These high-quality schedules are added back into the training set, and the loop repeats until convergence.

**S078 — 한국어**

(이 고품질 schedule을 학습 집합에 다시 넣고 수렴할 때까지 반복한다.)

## 5 Experiments

### 5.1 Implementation Details

**S079 — Original**

The internal constraint module is implemented as a multi-layer perceptron with two hidden layers of width 1024.

**S079 — 한국어**

(내부 제약 모듈은 폭 1,024인 은닉층 두 개를 가진 MLP로 구현한다.)

**S080 — Original**

The Transformer encoder and decoder are configured with a width of 512, a depth of 12, and 16 attention heads.

**S080 — 한국어**

(Transformer encoder와 decoder는 폭 512, 깊이 12, attention head 16개로 설정한다.)

**S081 — Original**

Training uses AdamW with a base learning rate of 10^-4 and weight decay of 10^-4.

**S081 — 한국어**

(학습은 기본 learning rate `10^-4`, weight decay `10^-4`의 AdamW optimizer를 사용한다.)

**S082 — Original**

Each training batch contains 48 timesteps uniformly sampled from a trajectory.

**S082 — 한국어**

(각 training batch에는 하나의 trajectory에서 균등 표본추출한 48개 timestep이 들어 있다.)

**S083 — Original**

The complete iterative pipeline comprises three supervised stages, culminating in a total of 90,000 iterations.

**S083 — 한국어**

(전체 반복 pipeline은 세 번의 지도학습 단계로 구성되며 총 90,000 iteration에 이른다.)

**S084 — Original**

Training and evaluation use 256 CPU cores, 984 GB RAM, and 8 RTX 4090 GPUs; training requires about 48 GPU-hours.

**S084 — 한국어**

(학습과 평가는 CPU core 256개, RAM 984 GB, RTX 4090 GPU 8개를 사용하며 학습에는 약 48 GPU-hour가 필요하다.)

### 5.2 Evaluation Metrics

**S085 — Original**

Completion rate measures the proportion of completed tasks out of all.

**S085 — 한국어**

(CR은 전체 작업 중 완수된 작업의 비율을 측정한다.)

**S086 — Original**

Partial completion rate assesses the ratio of the maximum progress to the total required duration.

**S086 — 한국어**

(PCR은 전체 요구 지속시간에 대한 최대 진행량의 비율을 평가한다.)

**S087 — Original**

Weighted completion rate is a weighted version of completion rate, considering task durations.

**S087 — 한국어**

(WCR은 작업 지속시간을 고려해 CR에 가중치를 준 지표다.)

**S088 — Original**

Turn-around time calculates the average time taken to complete tasks, reflecting scheduling efficiency.

**S088 — 한국어**

(TAT는 작업 완료에 걸린 평균 시간을 계산해 스케줄링 효율을 나타낸다.)

**S089 — Original / Equation (10)**

`CS=(w_CR CR+w_PCR PCR+w_WCR WCR)^(-1)+w_TAT TAT+w_PC PC`

**S089 — 한국어**

(CS는 완수 지표의 가중합 역수에 처리시간과 전력 소비의 가중 항을 더한 값으로, 작을수록 좋다.)

### 5.3 Main Results

**S090 — Original**

On the test split, AEOS-Former achieves 6.28 CS, surpassing MSCPO-SHCS by 16.7%.

**S090 — 한국어**

(test split에서 AEOS-Former의 CS는 6.28로 MSCPO-SHCS보다 16.7% 우수하다.)

**S091 — Original**

The integrated constraint module and iterative learning yield a better balance between completion rate and power consumption.

**S091 — 한국어**

(통합 제약 모듈과 반복 학습은 완수율과 전력 소비 사이에서 더 나은 균형을 만든다.)

**S092 — Original**

On val-seen, the constraint module increases completion rate from 27.47 to 28.06 and reduces power consumption from 135.94 to 69.76.

**S092 — 한국어**

(val-seen에서 제약 모듈은 CR을 27.47에서 28.06으로 높이고 PC를 135.94에서 69.76으로 낮춘다.)

**S093 — Original**

Due to the conflict between completion rate and power consumption, the final completion rate is lower than that achieved by iterative training alone.

**S093 — 한국어**

(완수율과 전력 소비가 충돌하기 때문에 최종 모델의 CR은 반복 학습만 사용한 경우보다 낮다.)

### 5.4 Analysis

**S094 — Original**

As the number of satellites increases from 1 to 50, comprehensive score initially decreases before stabilizing, while completion rate consistently increases.

**S094 — 한국어**

(위성 수가 1기에서 50기로 증가할 때 CS는 처음 낮아지다 안정화되고 CR은 꾸준히 증가한다.)

**S095 — Original**

This suggests a trade-off between task completion and resource consumption.

**S095 — 한국어**

(이는 작업 완수와 자원 소비 사이의 trade-off를 보여준다.)

**S096 — Original**

An increase in the number of tasks leads to lower completion rates and more resource consumption.

**S096 — 한국어**

(작업 수가 늘면 완수율은 낮아지고 자원 소비는 커진다.)

## 6 Conclusion

**S097 — Original**

This work introduces a comprehensive framework for Agile Earth Observation Satellites constellation scheduling.

**S097 — 한국어**

(이 연구는 민첩 지구관측 위성 군집 스케줄링을 위한 포괄적인 프레임워크를 제안한다.)

**S098 — Original**

We present AEOS-Bench, a standardized benchmark with 3,907 satellite assets and 16,410 scenarios, enforcing realistic constraints and providing ground truth annotations.

**S098 — 한국어**

(저자들은 현실적인 제약을 강제하고 정답 annotation을 제공하는, 3,907개 위성 자산과 16,410개 시나리오 규모의 표준 benchmark AEOS-Bench를 제시한다.)

**S099 — Original**

We also propose AEOS-Former, a Transformer-based scheduler featuring a novel constraint module.

**S099 — 한국어**

(또한 새로운 제약 모듈을 갖춘 Transformer 기반 scheduler AEOS-Former를 제안한다.)

**S100 — Original**

Through simulation-based iterative learning, AEOS-Former outperforms baselines across diverse scenarios, with ablation studies validating the effectiveness of each component.

**S100 — 한국어**

(시뮬레이션 기반 반복 학습을 통해 AEOS-Former는 다양한 시나리오에서 baseline보다 우수하며 ablation study는 각 구성요소의 효과를 검증한다.)

## A Limitations

**S101 — Original**

In AEOS-Bench, each task is represented as a single location point.

**S101 — 한국어**

(AEOS-Bench에서 각 작업은 하나의 위치 점으로 표현된다.)

**S102 — Original**

Future work will incorporate area-based task representations, allowing each observation request to span a defined region.

**S102 — 한국어**

(후속 연구에서는 각 관측 요청이 정해진 영역에 걸치도록 area-based task representation을 도입할 계획이다.)

**S103 — Original**

This would enable evaluation under more realistic constraints, such as partial area coverage, time-window flexibility, and spatial prioritization.

**S103 — 한국어**

(그러면 부분 영역 coverage, 유연한 time window, 공간 우선순위 같은 더 현실적인 제약에서 평가할 수 있다.)

## B Broader Impacts

**S104 — Original**

AEOS-Bench is an open-source suite for constellation scheduling research, enabling researchers to develop more effective models and conduct fair comparisons.

**S104 — 한국어**

(AEOS-Bench는 군집 스케줄링 연구를 위한 open-source suite로, 연구자가 더 효과적인 모델을 개발하고 공정하게 비교할 수 있게 한다.)

**S105 — Original**

In disaster response, optimized task assignment delivers timely data to first responders, improving search and rescue operations, damage assessment, and resettlement planning.

**S105 — 한국어**

(재난 대응에서 최적화된 작업 배정은 초기 대응자에게 적시에 데이터를 전달해 수색·구조, 피해 평가, 재정착 계획을 개선한다.)

**S106 — Original**

In environmental protection, high-quality imagery enables early detection of illegal logging and industrial pollution.

**S106 — 한국어**

(환경 보호에서는 고품질 영상이 불법 벌목과 산업 오염을 조기에 탐지하게 해준다.)

## C Scenario Modeling

**S107 — Original**

The simulation platform includes reaction wheels, batteries, sensors, and solar panels.

**S107 — 한국어**

(시뮬레이션 플랫폼은 반작용 휠, 배터리, 센서, 태양전지판을 포함한다.)

**S108 — Original**

Reaction wheels and sensors draw power from batteries, while solar panels recharge those batteries.

**S108 — 한국어**

(반작용 휠과 센서는 배터리 전력을 사용하고 태양전지판은 배터리를 충전한다.)

**S109 — Original**

A planetary environment supplies solar incidence angles and simulates gravitational forces.

**S109 — 한국어**

(행성 환경 모듈은 태양 입사각을 제공하고 중력을 시뮬레이션한다.)

**S110 — Original**

Closed-loop attitude control uses navigation, attitude guidance, MRP control, and reaction-wheel control modules.

**S110 — 한국어**

(closed-loop 자세 제어는 navigation, attitude guidance, MRP control, reaction-wheel control 모듈을 사용한다.)

**S111 — Original**

The MRP algorithm adjusts satellite orientation to keep target locations in view.

**S111 — 한국어**

(MRP 알고리즘은 목표 지점을 시야에 유지하도록 위성 방향을 조정한다.)

### 표 4·5 해설

위성 매개변수에는 질량 `50~200 kg`, 태양전지판 면적 `5~10 m²`, 센서 half-FOV `0.5~1.5 rad`, 센서 전력 `2~8 W`, 배터리 용량 `8,000~30,000 mA·h`, 반작용 휠 속도 `-6,000~6,000 rpm`, 궤도 장반경 `6,800~8,000 km` 등이 포함된다. 작업은 연속 관측 최소시간 `15~60 s`, 공개·마감 시각 `0~3,600 s`, 목표 위도·경도로 정의된다. 표의 분포가 실제 fleet population의 빈도를 뜻하는 것은 아니며 scenario generation 범위다.

## NeurIPS Paper Checklist 학습 메모

저자들은 주요 claim이 실험 결과로 뒷받침된다고 답하고 limitation section을 제공한다. 코드와 데이터를 공개하며 compute resource와 hyperparameter를 본문에 기록한다. 그러나 README의 200,000 iteration 안내와 논문의 90,000 iteration, 데이터 간편 다운로드의 `TODO`처럼 2026-09-10 현재 그대로 실행할 때 확인이 필요한 차이가 있다.

## 약어 및 기술 용어 사전

| 원어/약어 | 한국어 | 의미 | 최초 등장 |
|---|---|---|---|
| AEOS | 민첩 지구관측 위성 | 자세 기동으로 목표를 촬영하는 위성 | S002 |
| benchmark | 벤치마크 | 방법을 같은 조건에서 비교하는 데이터·환경·지표 | S004 |
| ground truth | 정답 annotation | 학습·평가 기준으로 쓰는 reference schedule | S008 |
| Transformer | 트랜스포머 | attention 기반 encoder-decoder 모델 | S010 |
| attention | 어텐션 | 후보 관계의 중요도를 가중합하는 연산 | S010 |
| heuristic | 휴리스틱 | 최적성보다 빠른 좋은 해를 찾는 경험적 탐색 | S019 |
| RL | 강화학습 | 환경 상호작용의 보상으로 policy를 학습 | S019 |
| FOV | 시야 | 센서가 한 번에 관측할 수 있는 각도 범위 | S022 |
| LEO | 저궤도 | 지구 가까운 위성 궤도 영역 | S041 |
| MRP | 수정 로드리게스 매개변수 | 3차원 자세 표현 | S042 |
| MLP | 다층 퍼셉트론 | constraint module의 신경망 | S079 |
| BCE | 이진 교차 엔트로피 | feasibility 분류 손실 | S066 |
| MSE | 평균제곱오차 | control-time 회귀 손실 | S067 |
| CR | 완수율 | 전체 중 완료 작업 비율 | S085 |
| PCR | 부분 완수율 | 요구 촬영시간 대비 최대 진행률 | S086 |
| WCR | 가중 완수율 | duration을 반영한 완수율 | S087 |
| TAT | 처리 완료 시간 | 평균 작업 완료 시간 | S088 |
| PC | 전력 소비량 | 센서 촬영 에너지 | S089 |
| CS | 종합 점수 | 완료·시간·전력을 결합한 낮을수록 좋은 지표 | S089 |

## 번역 검수 기록

- NeurIPS 최종 PDF 22쪽의 전 페이지 contact sheet를 확인했다.
- PDF의 2단 편집, figure/table caption, appendix 위치를 시각적으로 대조했다.
- arXiv HTML의 수식 (1)~(10)과 PDF 추출 결과를 교차 확인했다.
- 숫자·단위·split 이름과 `↑/↓` 지표 방향을 원문 표와 대조했다.
- 원문이 가능성·저자 주장으로 표현한 부분을 확정 사실로 강화하지 않았다.
- 참고문헌은 서지 record 왜곡을 피하기 위해 원문에 유지했다.

[← 학습 README](README.md)
