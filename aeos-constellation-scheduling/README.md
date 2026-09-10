# 현실적인 지구관측 군집위성 스케줄링: AEOS-Bench와 AEOS-Former

작성일: 2026-09-10  
확인 기준일: 2026-09-10

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [연구 질문과 핵심 기여](#연구-질문과-핵심-기여)
- [AEOS-Bench](#aeos-bench)
- [AEOS-Former 원리](#aeos-former-원리)
- [손실함수와 평가 지표](#손실함수와-평가-지표)
- [실험 결과를 정확히 읽는 법](#실험-결과를-정확히-읽는-법)
- [강점·한계·재현 위험](#강점한계재현-위험)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 사용자 입력: [alphaXiv PDF](https://www.alphaxiv.org/pdf/2510.26297)
- 접근 가능한 최종 출판본: [NeurIPS 2025 Proceedings](https://proceedings.neurips.cc/paper_files/paper/2025/hash/7c40c5050bd029a3ea7ff8b01412f735-Abstract-Conference.html), DOI `10.52202/085713-2878`
- 공개 preprint: [arXiv:2510.26297v1](https://arxiv.org/abs/2510.26297), 2025-10-30 제출
- 저자: Luting Wang, Yinghao Xiang, Hongliang Huang, Dongjun Li, Chen Gao, Si Liu
- 출판처: Advances in Neural Information Processing Systems 38, NeurIPS 2025 Main Conference Track
- 논문 라이선스: arXiv HTML에 표시된 [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)
- 공식 코드: [buaa-colalab/AEOSBench](https://github.com/buaa-colalab/AEOSBench), Apache License 2.0

NeurIPS 최종 PDF는 22쪽이며 본문, 참고문헌, NeurIPS Paper Checklist(논문 체크리스트), 한계·사회적 영향·시나리오 모델링 부록을 포함한다. arXiv v1은 15쪽이다. 제목·저자·핵심 방법과 결과가 일치하는 것을 대조했고, 이 폴더는 최종 출판본을 기준으로 설명한다.

문장 대조 번역은 [논문 번역](Towards%20Realistic%20Earth-Observation%20Constellation%20Scheduling%20-%20Benchmark%20and%20Methodology.번역.md)에 있다. 참고문헌은 서지 정보를 변형하지 않기 위해 원문 링크를 사용하며, NeurIPS 체크리스트는 연구 본문이 아니므로 문항 전체를 중복 번역하지 않고 핵심 공개·재현성 답변만 해설한다.

## 한눈에 보기

이 논문은 하나의 모델만 제안하지 않는다. 현실적인 군집위성 스케줄링 연구에 부족했던 공통 시험장인 `AEOS-Bench`와, 물리 제약을 attention에 넣는 `AEOS-Former`를 함께 제안한다.

```text
궤도·자세·전력·센서 물리 시뮬레이터
  -> 3,907개 위성 asset과 동적 imaging task
  -> greedy 초기 할당 + 반복 filtering + 사람 검수
  -> 16,410개 scenario의 AEOS-Bench
  -> constraint module: 실행 가능성 + 자세 제어 시간 예측
  -> constraint-aware Transformer: 위성-작업 assignment
  -> simulator exploration에서 좋은 trajectory 선별
  -> dataset에 합쳐 재학습
```

핵심 아이디어는 `실행 불가능한 위성-작업 쌍을 모델이 단순히 사후에 벌점받게 하지 말고, 물리 실행 가능성을 별도 모듈로 학습해 cross-attention과 최종 선택을 직접 제한하자`는 것이다.

## 기초 개념

### AEOS와 일반 지구관측 위성의 차이

AEOS(Agile Earth Observation Satellite, 민첩 지구관측 위성)는 자세를 적극적으로 바꿔 지상 목표를 촬영한다. 궤도가 목표 위를 지나는지만으로 작업이 가능한 것이 아니다. 센서 FOV(Field of View, 시야), 현재 자세, 목표 방향, 자세 전환 시간, 반작용 휠 한계, 배터리, 촬영 지속시간과 time window를 모두 만족해야 한다.

### 스케줄링 문제

시간마다 여러 위성 중 어떤 위성이 어떤 작업을 수행할지 정한다. 위성 수를 `N_S`, 작업 수를 `N_T`라 하면 행동 벡터 `a=[a_1,...,a_NS]`의 각 원소는 `0`(센서 끄기) 또는 작업 ID다. 가능한 조합은 매우 빠르게 커지므로 전수검색은 현실적인 규모에서 어렵다.

### Transformer가 쓰이는 이유

Transformer(트랜스포머)는 attention(어텐션)을 이용해 많은 작업 후보 사이의 관계를 병렬로 계산한다. Pointer Network처럼 조합 최적화의 선택 문제를 sequence/assignment 예측으로 바꿀 수 있다. 그러나 순수 attention은 궤도·자세·전력 제약을 자연스럽게 보장하지 않으므로 논문은 constraint module을 추가한다.

### 정적·동적 특성

- 정적 satellite feature: 질량, 관성모멘트, 센서 특성, 궤도요소처럼 scenario 동안 고정되는 값
- 동적 satellite feature: 현재 자세, true anomaly(진근점이각), 배터리 잔량처럼 시간에 따라 바뀌는 값
- 정적 task feature: 목표 좌표, release time, due time, 필요 촬영시간
- 동적 task feature: 현재까지의 촬영 progress

논문은 동적 상태를 과거 행동만으로 추론시키지 않고 매 timestep마다 simulator에서 직접 조회한다.

## 연구 질문과 핵심 기여

연구 질문은 다음 세 가지다.

1. 수십 기 위성과 수백 개 동적 작업을 포함하면서 실제 물리를 반영한 공통 benchmark를 만들 수 있는가?
2. 물리·운용 제약을 neural scheduler 내부에 직접 표현하면 효율적인 assignment가 가능한가?
3. expert annotation으로 시작해 simulator exploration 결과를 다시 학습 데이터로 넣으면 성능을 개선할 수 있는가?

논문의 기여:

- 3,907개 조정된 satellite asset과 16,410개 scenario를 포함한 AEOS-Bench
- dynamics, energy, FOV, continuity, time window의 다섯 제약을 검사하는 Basilisk 기반 closed-loop simulator
- 실행 가능성 logit과 최소 자세 제어 시간을 예측하는 internal constraint module
- constraint-derived cross-attention mask를 갖는 encoder-decoder scheduler
- supervised pretraining과 simulation-driven exploration을 반복하는 학습 절차
- CR, PCR, WCR, TAT, PC, CS의 여섯 지표와 seen/unseen/realistic test split

## AEOS-Bench

### 규모와 split

| 항목 | 값 |
|---|---:|
| satellite assets | 3,907 |
| scenarios/trajectories | 16,410 |
| scenario당 위성 | 1~50기 |
| scenario당 imaging tasks | 50~300개 |
| trajectory 길이 | 3,600 timestep, 논문 표에서 1시간 |
| train | 16,218 trajectories, 2,907 assets |
| val-seen | 64 scenarios, train과 같은 위성 집합 |
| val-unseen | 64 scenarios, train에 없는 500 assets |
| test | 64 scenarios, 공개 웹 자료에서 얻은 특성의 500 assets |

### scenario 물리

시뮬레이터는 orbital dynamics(궤도 역학), attitude control(자세 제어), power system(전력계), sensor payload(센서 탑재체)를 모델링한다. 저궤도에서 궤도요소·질량·관성 특성을 표본추출하고 MRP(Modified Rodrigues Parameters, 수정 로드리게스 매개변수) 기반 자세 제어를 사용한다.

### annotation 생성

각 scenario는 distance-based initialization에서 출발한다. 가까운 목표가 자세 기동상 오히려 실패할 수 있으므로 iterative filter와 human quality review를 거친다. 이 annotation은 실행 가능한 높은 품질의 reference schedule이지만, 논문이 모든 scenario에서 수학적 전역 최적해임을 증명한 것은 아니다. 따라서 `ground truth`는 `검수된 학습 목표`라는 의미로 읽어야 한다.

## AEOS-Former 원리

### 1. 입력 표현

정적·동적 행렬을 feature 축으로 결합한다.

```math
S=[S^s;S^d] ∈ R^(N_S × d_S),  T=[T^s;T^d] ∈ R^(N_T × d_T)
```

현재 timestep의 sinusoidal time embedding을 추가하고 release/due time은 현재 시각에 대한 상대 offset으로 바꾼다. categorical feature는 embedding lookup, continuous feature는 linear projection을 사용한다.

### 2. Internal Constraint Module

위성 `i`와 작업 `j`의 결합 feature를 MLP(Multi-Layer Perceptron, 다층 퍼셉트론)에 넣어 두 값을 예측한다.

- `ŝ_i,j`: 위성이 작업을 완수할 수 있다는 feasibility logit
- `t̂_i,j`: 필요한 자세 조정 시간

직접적인 pair label은 모든 쌍에 없으므로, 실제 완성 trajectory에서 위성 `i`가 작업 `j`에 `n` timestep 이상 연속 기여했다면 근사 label `s̃_i,j=1`로 둔다. 이는 계산비를 줄이지만 공동 작업의 인과 기여도를 완벽히 분리하지 못하는 weak supervision(약한 지도)의 한 형태다.

### 3. Constraint-aware attention

task encoder가 contextual task feature `h_T`를 만들고 satellite decoder가 constraint mask `M` 아래 task에 cross-attention한다.

```math
M_i,j = w × ŝ_i,j + b
```

`w`와 `b`를 0으로 초기화해 학습 초기에 불안정한 constraint prediction이 attention을 즉시 지배하지 않게 한다. assignment score는 null assignment vector `h_φ`도 포함해 센서를 끄는 선택을 표현한다.

추론 때는 `sigmoid(ŝ_i,j) > τ_s`를 만족하지 않는 쌍을 제거한 뒤 최고 점수 작업을 선택한다. 즉 learned constraint가 soft guidance인 동시에 최종 feasibility gate 역할도 한다.

### 4. Simulation-based iterative learning

처음에는 AEOS-Bench의 annotation으로 지도학습한다. 그다음 모델이 무작위 scenario에서 schedule을 생성하고 comprehensive score가 threshold `τ_e`를 넘은 trajectory만 데이터셋에 다시 넣어 재학습한다. 이것은 임의의 자기학습이 아니라 simulator가 물리 제약과 결과를 평가하는 filtered dataset aggregation이다.

## 손실함수와 평가 지표

### 학습 손실

```math
L_s = mean(BCE(ŝ_i,j, s̃_i,j))
L_t = sum(s̃_i,j × MSE(t̂_i,j,t̃_i,j)) / sum(s̃_i,j)
L_a = CE(A, a+1)
L = w_s L_s + w_t L_t + w_a L_a
```

BCE(Binary Cross-Entropy, 이진 교차 엔트로피)는 feasibility, MSE(Mean Squared Error, 평균제곱오차)는 제어 시간, CE(Cross-Entropy, 교차 엔트로피)는 assignment class를 학습한다. 실험은 `w_s=w_t=w_a=1`이다. `L_t`는 positive pair가 없는 batch에서 분모가 0이 되지 않도록 구현상 guard가 필요하다.

### 여섯 평가 지표

- CR(Completion Rate, 완수율): 전체 작업 중 완료된 작업 비율
- PCR(Partial Completion Rate, 부분 완수율): 요구 지속시간 대비 최대 진행률
- WCR(Weighted Completion Rate, 가중 완수율): 작업 duration을 반영한 CR
- TAT(Turn-Around Time, 처리 완료 시간): 평균 작업 완료 시간, 낮을수록 좋음
- PC(Power Consumption, 전력 소비량): 촬영 중 센서가 사용한 에너지, 낮을수록 좋음
- CS(Comprehensive Score, 종합 점수): 완수·시간·전력을 결합, 낮을수록 좋음

```math
CS=(0.6 CR + 0.2 PCR + 0.2 WCR)^(-1) + TAT/7 + PC/100
```

CR·PCR·WCR이 논문 표에서 `%`인지 식에서 0~1 비율인지 구현을 확인해야 한다. 단위와 scaling이 달라지면 CS의 세 항 가중치 의미가 크게 변한다.

## 실험 결과를 정확히 읽는 법

### Main comparison

| Split | Method | CS↓ | CR % | PCR % | WCR % | TAT h↓ | PC Wh↓ |
|---|---|---:|---:|---:|---:|---:|---:|
| Val-seen | MSCPO-SHCS | 5.85 | 28.77 | 32.93 | 28.23 | 7.75 | 135.93 |
| Val-seen | AEOS-Former | **5.00** | **30.47** | **33.68** | **30.05** | **7.50** | **71.27** |
| Val-unseen | MSCPO-SHCS | 5.21 | 35.35 | **39.45** | 34.85 | 7.27 | 140.83 |
| Val-unseen | AEOS-Former | **4.43** | **35.42** | 38.93 | **35.14** | **6.78** | **68.99** |
| Test | MSCPO-SHCS | 7.33 | **19.44** | **24.00** | 18.71 | 6.23 | 149.20 |
| Test | AEOS-Former | **6.28** | 19.25 | 22.31 | **18.73** | **5.67** | **40.91** |

`모든 baseline을 능가한다`는 표현은 주로 CS에 대해 타당하다. test에서 AEOS-Former의 CR과 PCR은 MSCPO-SHCS보다 약간 낮다. 장점은 특히 전력 소비 감소와 종합 균형이다. 모델 선택 시 임무가 완료율을 최우선하는지, 에너지를 포함한 효율을 최우선하는지 분리해야 한다.

### Ablation

constraint module은 전력 소비를 크게 낮추는 경향이 있고 iterative training은 완수율을 올리는 경향이 있다. test에서 iterative training만 쓴 변형의 CR은 `24.67%`로 두 모듈을 모두 쓴 최종 모델의 `19.25%`보다 높지만 PC는 `149.26 Wh` 대 `40.91 Wh`다. 최종 모델이 단일 지표 최대가 아니라 multi-objective balance를 택한 결과다.

## 강점·한계·재현 위험

### 강점

- 작은 정적 toy problem이 아니라 closed-loop 물리 simulator에서 실행 가능성을 평가한다.
- seen/unseen/웹 기반 test asset을 나눠 위성 특성 일반화를 시험한다.
- 제약 예측을 attention과 최종 선택에 연결해 해석 가능한 중간 출력을 제공한다.
- benchmark, simulator, baseline, 학습 코드를 Apache-2.0으로 공개했다.

### 논문이 밝힌 한계

각 task를 하나의 지점으로 표현한다. 실제 영상 임무의 area target, partial coverage, flexible time window, spatial priority는 후속 과제다.

### 추가로 주의할 점

1. `ground truth`는 전역 최적해 보증이라기보다 greedy 초기화·filter·사람 검수로 만든 reference다.
2. 논문은 `entire AEOS-Bench` 통계로 normalize한다고 서술한다. 실제 구현이 test 통계를 사용한다면 leakage가 될 수 있으므로 train-only normalization 여부를 확인해야 한다.
3. 비교 baseline은 새 환경에 맞게 저자가 수정했다. 원 논문 구현과 동일한 hyperparameter budget인지 확인해야 공정성을 평가할 수 있다.
4. 단일 run 표에는 분산·신뢰구간이 없다. 여러 seed와 paired scenario test가 필요하다.
5. sensor energy만 PC에 포함된다면 자세 제어용 reaction wheel과 전체 spacecraft 전력 효율을 대표하지 못한다.
6. 코드 README는 2026-09-10 기준 training이 200,000 iteration까지 계속된다고 적지만 논문은 3단계 총 90,000 iteration이라고 설명한다. evaluation 예시 checkpoint도 100,000이다. 재현 시 정확한 release/commit/config를 동결해야 한다.
7. 공개 저장소의 간편 다운로드 부분에는 아직 `TODO: urls`가 남아 있어 데이터 접근 절차가 완전히 매끄럽지는 않다.

## 용어 정리

| 약어/용어 | 영문 전체 이름 | 한국어와 논문 내 역할 |
|---|---|---|
| AEOS | Agile Earth Observation Satellite | 민첩 지구관측 위성. 자세를 바꿔 목표를 촬영하는 자원 |
| FOV | Field of View | 센서 시야. 목표 관측 가능성 제약 |
| LEO | Low Earth Orbit | 저궤도. benchmark의 위성 궤도 영역 |
| MRP | Modified Rodrigues Parameters | 수정 로드리게스 매개변수. 3차원 자세 표현·제어 |
| MLP | Multi-Layer Perceptron | 다층 퍼셉트론. constraint module 구현 |
| BCE | Binary Cross-Entropy | 이진 교차 엔트로피. 실행 가능성 학습 손실 |
| MSE | Mean Squared Error | 평균제곱오차. 제어시간 회귀 손실 |
| CR/PCR/WCR | Completion/Partial/Weighted Completion Rate | 완수·부분 완수·가중 완수율 |
| TAT | Turn-Around Time | 작업 완료까지 평균 시간 |
| PC | Power Consumption | 센서 촬영 전력 소비량 |
| CS | Comprehensive Score | 다섯 성능 축을 결합한 낮을수록 좋은 종합 지표 |
| RL | Reinforcement Learning | 강화학습. 관련 baseline과 iterative exploration 맥락 |
| MDP | Markov Decision Process | 마르코프 결정 과정. 상태·행동·보상으로 순차 의사결정을 표현 |
| SOTA | State of the Art | 최고 수준 결과. 반드시 어떤 지표·split인지 제한해 읽어야 함 |

## 실습 학습 가이드

- [01_foundations.ipynb](01_foundations.ipynb): time window, slew, energy를 갖는 toy scheduler와 greedy feasibility
- [02_practice.ipynb](02_practice.ipynb): constraint logit, attention mask, assignment와 여섯 평가 지표
- [03_advanced.ipynb](03_advanced.ipynb): ablation, 종합 점수 민감도, train/test normalization leakage와 iterative filtering

세 notebook은 Python 표준 라이브러리만 쓰는 toy reproduction이다. AEOS-Bench의 대규모 데이터, Basilisk 물리 엔진, PyTorch 모델과 논문 수치를 재현했다고 주장하지 않는다. 공식 코드는 Python 3.11.10, PyTorch 2.6.0+cu124, 다중 GPU 환경을 안내하며 논문은 8 RTX 4090 GPU에서 약 48 GPU-hours를 보고한다.

## 다음 학습 경로

1. 첫 notebook에서 hard constraint를 만족하는 schedule을 직접 만든다.
2. 두 번째에서 `constraint score → attention bias → 최종 gate`의 차이를 확인한다.
3. 세 번째에서 CS weight가 결론을 어떻게 바꾸는지 sensitivity analysis한다.
4. 공식 저장소의 `constellation/new_transformers`와 simulator wrapper를 실제 revision에 고정해 읽는다.
5. 여러 seed, train-only normalization, 에너지 범위 확대, area target으로 재현 연구를 설계한다.

전문가 수준의 독해는 높은 점수만 기억하는 것이 아니라 `목적함수·제약·annotation 품질·split·단위·비교 예산`이 결론을 어떻게 결정하는지 추적하는 것이다.
