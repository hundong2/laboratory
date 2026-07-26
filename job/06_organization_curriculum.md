# 로보틱스 AI 조직 역량 커리큘럼

작성일: 2026-07-26

대상: 신입 엔지니어부터 subsystem technical lead까지
운영 원칙: 강의 20%, 실습 60%, 설계·코드 리뷰 20%

## 1. 최종 목표

이 과정의 목표는 “모델을 학습할 수 있는 사람”을 늘리는 것이 아니다. 다음을 독립적으로 수행할 수 있는 조직을 만드는 것이다.

1. 문제를 ODD, latency, 안전 비용, 자원 예산으로 명세한다.
2. sensor data의 시간·좌표계·calibration 품질을 검증한다.
3. 재현 가능한 Python 기준 모델과 dataset lineage를 만든다.
4. C++/ROS 2에서 같은 model contract를 구현한다.
5. 실제 장치에서 성능·전력·온도·장시간 안정성을 측정한다.
6. rosbag, SIL, HIL, closed-course, shadow 단계의 evidence를 만든다.
7. 실패를 안전하게 감지하고 rollback 가능한 release를 운영한다.

## 2. 기존 커리큘럼 재평가

| 영역 | 기존 수준 | 조직 기준의 문제 | 이번 보완 |
|---|---|---|---|
| Python→ONNX→C++ | 강함 | 단일 합성 모델 중심 | golden vector, release gate, 장치 증거 추가 |
| 경량화 | 입문 | INT8 한 경로 위주 | backend별 PTQ/QAT/mixed precision 판단 보강 |
| ROS 2 | 입문 | topic 연결 중심 | time/tf/QoS/executor/lifecycle/tracing 보강 |
| 로보틱스 기초 | 부족 | 추정·계획·제어와 AI 출력의 연결 부족 | 시스템 기초 문서 신설 |
| 데이터 | 부족 | bag 수집 이후 품질·lineage·split 부족 | MCAP, QA, group split, 재현성 tuple 추가 |
| C++ 시스템 | 부분적 | memory/concurrency/RT 기준 부족 | latest-only worker와 hot-path 기준 추가 |
| 검증 | 부분적 | 정상 입력과 단일 benchmark 중심 | 장애 주입, SIL/HIL, scenario coverage 추가 |
| 안전·보안 | 개요 | 적용 제품별 표준·evidence 부족 | 제품군별 기준과 supply-chain gate 추가 |
| 조직 운영 | 없음 | 역할별 기대 수준·평가 기준 없음 | 14주 과정, rubric, 승급 gate 신설 |

## 3. 숙련도 체계

### L0: 학습자

- 안내에 따라 environment와 실습을 재현한다.
- timestamp, frame, dtype, shape, 단위를 설명한다.
- 실패한 테스트의 로그를 수집한다.

### L1: 기능 기여자

- 작은 모델을 학습·export하고 Python/C++ 동등성을 검증한다.
- ROS 2 package, QoS, rosbag replay를 독립 수행한다.
- 정해진 release gate를 통과하는 변경을 제출한다.

### L2: subsystem owner

- latency와 safety requirement를 component budget으로 분해한다.
- dataset split, calibration, model/runtime version을 설계한다.
- 장애 주입, scenario, hardware benchmark를 CI/nightly에 연결한다.
- regression 원인을 data/model/runtime/system으로 분리한다.

### L3: technical lead/release owner

- ODD와 hazard에서 verification strategy를 만든다.
- 여러 subsystem의 timing, compute, network budget을 조정한다.
- build vs buy, hardware/runtime 선택을 evidence로 결정한다.
- release waiver와 residual risk를 승인하거나 거부한다.
- fleet telemetry에서 개선 loop와 rollback을 운영한다.

승급은 수강 시간이나 quiz 점수가 아니라 실제 artifact와 review evidence로 결정한다.

## 4. 공통 역량 매트릭스

각 항목을 0~3으로 평가한다.

| 역량 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Linux | 명령 실행 | process/resource 확인 | profiling·service·container | RT scheduling·IRQ·장애 분석 |
| Python/ML | notebook 실행 | 학습·평가 | 재현 pipeline·fine-tuning | data/model 전략과 failure analysis |
| C++ | 문법 | RAII·CMake·test | concurrency·profiling | bounded RT architecture |
| ROS 2 | pub/sub | QoS·tf2·bag | executor·lifecycle·composition | RMW/network/graph 최적화 |
| 센서 | 값 읽기 | 단위·rate | time sync·calibration | observability·fusion failure 분석 |
| 배포 | 파일 실행 | ONNX C++ | TensorRT/OpenVINO·cross build | platform portfolio와 release 전략 |
| 검증 | manual check | unit/contract | SIL/HIL/fault injection | scenario coverage와 safety evidence |
| 운영 | 로그 확인 | version/rollback | drift·fleet monitoring | incident command와 continuous improvement |

개인별 radar chart를 만드는 것보다 다음 분기에 0 또는 1인 핵심 항목을 어떤 실제 업무로 끌어올릴지 합의하는 것이 중요하다.

## 5. 14주 공통 과정

주당 권장 시간은 강의 2시간, 실습 6시간, review 2시간이다.

### 0주차: 진단과 환경

- 사전 진단: Linux, Python, C++, 선형대수, ROS 2
- 장비 inventory와 권한 확인
- repository, issue, code review 규칙
- 결과물: 재현 가능한 environment report
- gate: 새 PC에서 동료가 같은 test를 실행

### 1주차: 물리 시스템과 시간

- closed loop, sampling, aliasing
- sensor/host/receive/process timestamp
- clock offset, drift, jitter
- 실습: `labs/01_time_sync.py`
- gate: max skew와 drop 정책을 requirement에서 유도

### 2주차: 좌표계, calibration, 추정

- SE(3), transform chain, quaternion
- camera/LiDAR/IMU calibration
- covariance와 state estimation
- 실습: transform inverse/chain property test 작성
- gate: frame 방향 오류를 test가 잡음

### 3주차: Python 기준 모델

- dataset group split, baseline, metric 비용
- `01_foundations.ipynb`
- 실습: 합성 데이터를 실제 팀 CSV 또는 공개 dataset adapter로 교체
- gate: leakage 없는 split report

### 4주차: fine-tuning과 불확실성

- `02_fine_tuning.ipynb`
- 실제 vision 직무는 `08_vision_transfer_learning.ipynb`
- head-only/partial/full unfreeze
- class imbalance, calibration, abstention
- gate: 3 seed 평균·분산과 위험 클래스 recall 제출

### 5주차: export와 경량화

- `03_advanced.ipynb`
- ONNX contract, FP16, PTQ, QAT, structured pruning
- 실습: golden vector 100건 Python↔runtime 비교
- gate: accuracy·size·latency trade-off 보고서

### 6주차: 현대 C++와 runtime

- RAII, move, span/view, error boundary
- allocation과 cache, thread safety
- 필독·코드리딩: [`cpp/CPP_MASTERCLASS.md`](cpp/CPP_MASTERCLASS.md)의 소유권, tensor 수명, happens-before, 예외 경계 점검
- `cpp/main.cpp`, `labs/04_latest_only_worker.cpp`
- gate: ASan/UBSan과 Release benchmark 통과

### 7주차: ROS 2 시스템

- message/interface, tf2, QoS, RMW
- executor, callback group, lifecycle, composition
- 실습: Python 기준 node와 C++ node에 같은 bag 재생
- gate: timestamp 보존, QoS 호환, 결과 동등성

### 8주차: Linux/장치 최적화

- PREEMPT_RT, scheduling, affinity, page fault
- Jetson/TensorRT 또는 Intel/OpenVINO 경로
- `04_platform_recipes.md`
- gate: 실제 target에서 p50/p95/p99/max, memory, power, thermal

### 9주차: 데이터와 MLOps

- MCAP record/convert, dataset QA
- DVC 또는 사내 data catalog, experiment tracking
- model registry와 artifact signature
- gate: 임의 release를 code/data/model/runtime tuple로 재현

### 10주차: 검증과 장애 주입

- unit, contract, integration, replay, SIL, HIL
- `labs/02_fault_injection.py`, `labs/03_release_gate.py`
- gate: 필수 고장 10개 중 detection/fallback/recovery evidence

### 11주차: 안전·보안

- hazard, ODD, safe state, SOTIF 관점
- secure boot/update, SBOM, credential, network
- gate: subsystem hazard analysis와 abuse case review

### 12~13주차: capstone

- [07_capstone.md](07_capstone.md)의 실제 release 후보 제작
- 교차 팀 design review와 red-team fault injection
- gate: 자동 release gate와 현장 demo 모두 통과

### 14주차: 운영 회고와 승급 심사

- evidence dossier review
- 실패 원인과 개선 action
- 개인 숙련도 재평가
- 다음 분기 production ownership 지정

## 6. 역할별 심화 트랙

### Perception/ML

- sensor physics와 annotation guideline
- architecture와 loss 선택
- uncertainty/calibration/OOD
- active learning과 hard-negative mining
- TensorRT/OpenVINO graph 분석

필수 산출물: data card, model card, error taxonomy, quantization report.

### Robotics integration

- message/interface와 tf tree
- state estimation, tracking, planning interface
- executor, lifecycle, launch, diagnostics
- rosbag/SIL/HIL

필수 산출물: interface contract, timing diagram, launch architecture, bag regression suite.

### Platform/runtime

- BSP/kernel/driver, container, cross compilation
- CPU/GPU/DLA/NPU memory path
- scheduling, tracing, thermal/power
- OTA, secure boot, SBOM

필수 산출물: platform support matrix, reproducible image, p99 profile, rollback package.

### Controls/safety

- vehicle/robot dynamics와 controller
- hazard analysis, safety requirement
- monitor/fallback/safe state
- scenario coverage와 closed-loop acceptance

필수 산출물: safety concept, fault tree 또는 equivalent analysis, scenario suite, residual risk.

## 7. 실습 운영 방식

### 개인 실습만으로 끝내지 않는다

각 실습은 네 역할을 돌아가며 수행한다.

- implementer: 코드와 문서 작성
- reviewer: contract와 test 검토
- operator: 처음 보는 환경에서 실행
- red team: 잘못된 입력과 환경을 주입

### review 질문

1. 요구사항에서 이 threshold가 어떻게 나왔는가.
2. 평균이 아니라 tail과 deadline miss를 보았는가.
3. time/frame/unit 계약이 코드와 message에 있는가.
4. 데이터 누수와 ODD coverage를 어떻게 막았는가.
5. 실패를 탐지하고 어디까지 containment하는가.
6. 이전 release로 어떻게 돌아가는가.
7. 동료가 같은 결과를 재현할 수 있는가.

### 금지하는 합격 사유

- “노트북이 끝까지 실행됨”
- “데모에서 한 번 성공함”
- “평균 latency가 빠름”
- “accuracy가 지난 모델보다 높음”
- “Jetson에서 돌아감”

각 문장은 contract, 분포, 실패 사례, 재현성, safety evidence가 없으면 불충분하다.

## 8. 평가 rubric

총점 100점이지만 필수 gate 실패는 점수와 무관하게 불합격이다.

| 영역 | 배점 | 우수 기준 |
|---|---:|---|
| 문제·ODD·요구사항 | 10 | metric과 threshold가 hazard/운영 요구에서 추적됨 |
| 데이터 품질·lineage | 15 | group split, QA, version, 개인정보 처리 |
| 모델 품질 | 15 | 위험 클래스, calibration, challenge set, 여러 seed |
| C++/ROS 2 품질 | 15 | ownership, contract, QoS, lifecycle, diagnostics |
| 실기기 성능 | 15 | tail, miss rate, power, thermal, 장시간 |
| 검증 깊이 | 15 | golden, bag, SIL/HIL, fault injection |
| 안전·보안 | 10 | safe state, signature, SBOM, least privilege |
| 재현성과 설명 | 5 | 새 환경에서 동료가 재현 |

필수 gate:

- checksum 또는 signature가 틀린 모델을 로드하지 않는다.
- stale/NaN/wrong-shape 입력이 actuator 경로에 전달되지 않는다.
- Python/C++ golden test가 허용 오차 안이다.
- 위험 클래스 recall이 정한 하한 이상이다.
- 실제 장치 p99와 deadline miss rate가 기준 안이다.
- rollback 절차를 실제로 한 번 수행했다.

## 9. 조직 운영 지표

사람을 model accuracy로 평가하지 않는다. 조직 시스템이 좋아지는지를 본다.

- 신규 구성원의 첫 재현 성공까지 걸린 시간
- 실험 중 재현 가능한 비율
- release 전 자동 검출된 regression 수
- 현장 발견 대비 SIL/HIL 발견 비율
- rollback 평균 시간
- bag/data 품질 불량률
- flaky test 비율
- p99 latency regression 복구 시간
- incident에서 missing telemetry 비율
- 동일 원인의 반복 incident 수

지표를 개인 처벌에 사용하면 숨기기 행동을 만든다. process 병목과 학습 투자 우선순위를 찾는 데 사용한다.

## 10. 리더의 운영 cadence

- 매주: 실습 demo와 failure review
- 격주: architecture/contract review
- 매월: target hardware performance council
- release마다: safety/security/evidence review
- 분기마다: competency matrix와 ownership 재조정
- incident마다: blame-free postmortem과 regression test 추가

리더는 “더 빨리 모델을 넣으라”보다 “어떤 evidence가 있어야 안전하게 넣을 수 있는가”를 일관되게 물어야 한다.
