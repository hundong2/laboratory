# 로보틱스 AI 엔지니어가 반드시 이해해야 할 시스템 기초

작성일: 2026-07-26
확인 기준일: 2026-07-26

이 문서는 AI 모델을 “로봇에서 돌아가는 제품”으로 만드는 데 필요한 기초를 모델 학습보다 한 단계 아래에서 설명한다. 모델 정확도가 높아도 시간, 좌표계, 단위, 실행 순서, 제어 안정성을 틀리면 로봇은 실패한다.

## 1. 로봇은 닫힌 고리 시스템이다

서버 AI는 입력을 받아 답을 반환하는 것으로 끝나는 경우가 많다. 로봇은 출력이 물리 세계를 바꾸고, 바뀐 세계가 다시 센서 입력으로 돌아오는 closed loop다.

```text
센서 → 상태 추정 → 인지 → 계획 → 제어 → actuator
  ↑                                      │
  └──────────── 바뀐 물리 세계 ──────────┘
```

따라서 모델의 작은 지연도 다음 주기의 입력을 바꾼다.

예를 들어 10 m/s로 이동하는 차량의 인지 결과가 100 ms 늦으면, 단순 계산으로 이미 1 m 이동한 뒤의 세계를 과거 영상으로 판단한다.

```text
이동 거리 = 속도 × 지연시간
         = 10 m/s × 0.1 s
         = 1 m
```

로봇 AI의 품질은 다음을 함께 만족해야 한다.

- 무엇을 보았는가: 인지 정확도와 불확실성
- 언제 보았는가: sensor timestamp와 end-to-end age
- 어디에서 보았는가: coordinate frame과 calibration
- 언제까지 유효한가: deadline과 stale policy
- 틀렸을 때 무엇을 하는가: fallback과 안전 상태

## 2. 시간: 수신 시각과 측정 시각은 다르다

### 네 가지 시간을 구분한다

| 시간 | 의미 | 흔한 실수 |
|---|---|---|
| 측정 시각 | 센서가 물리량을 실제로 샘플한 시각 | callback 수신 시각으로 덮어씀 |
| 장치 시각 | 센서 내부 clock의 시각 | host clock과 같은 것으로 가정 |
| 수신 시각 | host가 packet/message를 받은 시각 | network·driver 지연을 측정 지연으로 오해 |
| 처리 완료 시각 | 추론·후처리가 끝난 시각 | 원본 timestamp 대신 결과 timestamp로 사용 |

결과 메시지는 원본 측정 timestamp를 보존하고, 별도로 처리 지연과 publish 시각을 기록하는 편이 좋다.

### clock offset과 drift

- offset: 두 clock 사이의 고정된 차이
- drift: 시간이 지나며 차이가 변하는 현상
- jitter: 지연시간이 매번 달라지는 현상

카메라와 LiDAR를 host 수신 시각만으로 합치면 network queue가 흔들릴 때 서로 다른 순간의 물체를 같은 순간으로 처리할 수 있다. 하드웨어 trigger, PTP, GNSS time, 장치 timestamp 지원 여부를 먼저 확인한다.

### 동기화 전략

| 전략 | 장점 | 위험 |
|---|---|---|
| exact timestamp | 짝의 의미가 명확함 | 실제 센서에서 정확히 같은 timestamp가 드묾 |
| approximate sync | 작은 시간차를 허용 | tolerance가 크면 다른 상태를 결합 |
| latest value | 구현이 단순함 | 고주기/저주기 센서 사이 age가 불명확 |
| interpolation | 연속 상태에 유용 | 불연속 이벤트와 회전 보간을 조심 |

동기화 tolerance는 “잘 맞는 숫자”가 아니라 물체 속도, 센서 주기, 허용 위치 오차에서 역산한다.

```text
허용 시간차 ≤ 허용 공간 오차 / 최대 상대 속도
```

최대 상대 속도 20 m/s에서 0.2 m 이상 어긋나면 안 된다면 시간차는 10 ms 이하여야 한다.

## 3. 좌표계와 SE(3)

### 점과 frame

`[x, y, z]`라는 숫자만으로는 위치가 완성되지 않는다. 어느 frame에서 표현했는지가 필요하다.

- `map`: 장기간 고정된 세계 좌표
- `odom`: 지역적으로 연속적이지만 drift할 수 있는 좌표
- `base_link`: 로봇 몸체 기준 좌표
- `camera_link`, `lidar_link`: 센서 장착 좌표

같은 물체의 camera frame 점을 base frame으로 바꾸려면 rotation과 translation이 모두 필요하다.

```text
p_base = R_base_camera · p_camera + t_base_camera
```

homogeneous transform으로 쓰면 다음과 같다.

```text
T = [ R  t ]
    [ 0  1 ]
```

### transform 방향

`T_A_B`를 “B frame의 점을 A frame으로 바꾸는 transform”으로 정의하면:

```text
p_A = T_A_B · p_B
T_A_C = T_A_B · T_B_C
T_B_A = inverse(T_A_B)
```

팀 전체가 이 표기 규칙을 하나로 고정해야 한다. 함수 이름에 `from`과 `to`를 명시하고 단위 테스트에 identity, inverse, transform chain을 포함한다.

### 회전 표현

| 표현 | 장점 | 주의점 |
|---|---|---|
| Euler angle | 사람이 읽기 쉬움 | 회전 순서와 gimbal lock |
| rotation matrix | 점 변환이 직접적 | 9개 값, 직교성 유지 |
| quaternion | 보간과 합성에 유리 | 순서 `xyzw`/`wxyz`, 정규화, 부호 동치 |

quaternion `q`와 `-q`는 같은 회전을 나타낸다. 단순 원소 차이로 회전 오차를 비교하면 잘못된 평가가 될 수 있다.

## 4. Calibration은 한 번 하고 끝나는 파일이 아니다

### intrinsic과 extrinsic

- intrinsic: 카메라 focal length, principal point, distortion처럼 센서 내부 특성
- extrinsic: 센서와 로봇 몸체 또는 센서 간 상대 pose
- temporal calibration: 센서 간 clock offset과 지연

현장에서 extrinsic이 바뀌는 원인:

- 충격과 진동
- bracket의 열팽창
- 센서 교체
- 정비 중 재장착
- firmware update로 timestamp 정의 변경

calibration 파일에는 장치 serial, 날짜, 방법, residual, 온도 조건, 담당자, checksum을 포함한다. 시작 시 로봇 BOM과 calibration 대상 serial이 일치하는지 검사한다.

## 5. Sampling, aliasing, filtering

센서 신호의 최고 주파수보다 sampling rate가 충분히 높지 않으면 높은 주파수가 낮은 주파수로 보이는 aliasing이 생긴다. 단순히 모델이 학습으로 해결할 수 있는 문제가 아니다.

- sampling 주기를 기록한다.
- anti-aliasing filter와 센서 내부 filter 설정을 확인한다.
- moving average는 noise를 줄이지만 phase delay를 만든다.
- low-pass cutoff는 제어 loop 대역폭과 함께 정한다.
- 누락 샘플을 0으로 채우지 말고 validity mask 또는 명시적 상태로 전달한다.

## 6. 상태 추정과 불확실성

로봇은 위치, 속도, 자세 같은 상태를 직접 완벽하게 측정하지 못한다. 여러 noisy measurement를 합쳐 추정한다.

### 기본 형태

```text
x_k = f(x_{k-1}, u_k) + process noise
z_k = h(x_k) + measurement noise
```

- `x`: 알고 싶은 state
- `u`: control input
- `z`: 센서 measurement
- process noise: 모델이 설명하지 못하는 변화
- measurement noise: 센서 오차

Kalman filter 계열은 covariance를 이용해 예측과 측정을 얼마나 믿을지 결정한다. covariance를 “적당히 작은 상수”로 넣으면 filter가 과신하거나 요동한다. 로그에서 residual과 innovation consistency를 검토해야 한다.

AI 모델도 score 하나만 주기보다 다음을 고려한다.

- calibration error: confidence 0.9가 실제 90% 정답인가
- epistemic uncertainty: 학습 데이터가 부족해서 모르는가
- aleatoric uncertainty: 센서 noise와 본질적 모호성인가
- out-of-distribution: 학습 범위 밖인가

confidence threshold는 validation F1 최대점 하나로 정하지 말고 위험 비용과 fallback 용량에서 정한다.

## 7. Planning과 control을 최소한 이해해야 하는 이유

### planning

- global planning: 지도와 목표를 이용한 큰 경로
- local planning: 주변 장애물과 동역학을 고려한 짧은 horizon
- trajectory: 시간에 따른 pose, velocity, acceleration의 연속 목표

AI perception의 출력이 planning에 들어갈 때 필요한 것은 클래스 정확도만이 아니다.

- position/velocity covariance
- tracking identity stability
- prediction horizon과 uncertainty
- free-space continuity
- false positive가 planning을 막는 정도
- false negative가 collision risk를 만드는 정도

### control

controller는 현재 state와 목표 trajectory의 오차를 줄이는 actuator command를 만든다. 주기와 지연은 stability margin에 직접 영향을 준다.

- PID: 오차, 누적 오차, 변화율을 조합
- feedforward: 원하는 동작에 필요한 command를 모델로 예측
- MPC: 동역학과 제약을 포함해 horizon 최적화

인지 모델의 latency가 바뀌면 controller tuning 가정도 달라질 수 있다. AI 최적화 전후에 closed-loop simulation을 다시 돌린다.

## 8. 실시간성: 빠름이 아니라 예측 가능성

### hard, firm, soft real-time

- hard: deadline miss 자체가 시스템 실패
- firm: deadline을 넘긴 결과는 가치가 없어 폐기
- soft: 늦어도 쓸 수 있지만 품질이 저하

카메라 인지 결과는 firm real-time인 경우가 많다. 500 ms 늦은 결과를 queue 순서대로 처리하기보다 폐기하고 최신 frame을 처리해야 한다.

### latency budget

30 Hz sensor의 주기는 약 33.3 ms다.

```text
capture 4 ms
driver/transport 3 ms
preprocess 4 ms
inference 10 ms
postprocess 3 ms
publish/fusion 4 ms
여유 5.3 ms
```

각 구간의 p99를 단순 합하면 correlation을 놓칠 수 있으므로 end-to-end trace도 측정한다. 평균, p50, p95, p99, max, deadline miss rate를 함께 본다.

### Linux에서의 핵심

- PREEMPT_RT는 더 많은 kernel 경로와 interrupt를 scheduler가 preempt할 수 있게 한다.
- `SCHED_FIFO` 우선순위는 잘못 쓰면 시스템을 굶길 수 있다.
- CPU affinity와 IRQ affinity를 의도적으로 설계한다.
- 실시간 구간 전에 memory를 preallocate하고 page를 fault-in한다.
- hot path에서 heap allocation, file I/O, blocking log, unbounded lock을 피한다.
- `cyclictest`, ROS tracing, `perf`, Nsight Systems 등으로 측정한다.

PREEMPT_RT만 설치했다고 user-space code가 자동으로 deterministic해지지는 않는다.

## 9. C++ 제품 코드의 최소 기준

### 소유권

- 값: 작고 복사 의미가 분명한 객체
- `std::unique_ptr`: 단일 소유권
- `std::shared_ptr`: 실제 공동 소유가 필요할 때만
- reference/span: 소유하지 않는 view이며 원본 수명을 넘지 않음

`shared_ptr`를 습관적으로 사용하면 수명과 해제 시점이 불명확해지고 atomic reference count 비용이 생긴다.

### hot path

- buffer와 tensor를 재사용한다.
- 최대 크기를 알고 bounded container를 쓴다.
- 예외가 real-time 경로에서 전파되지 않게 경계를 둔다.
- clock은 `steady_clock`을 사용한다.
- lock 범위를 줄이고 priority inversion을 검토한다.
- sanitizer와 static analysis를 CI에 둔다.

권장 검증:

```text
Debug/ASan+UBSan
TSan 전용 build
Release benchmark
clang-tidy
compiler warning as error
fuzz/property test
```

## 10. ROS 2를 “토픽 연결 도구” 이상으로 이해한다

### DDS/RMW와 QoS

QoS는 통신 의미의 일부다.

| 정책 | 질문 |
|---|---|
| reliability | 일부 유실을 허용하는가 |
| history/depth | 과거 메시지를 몇 개 보관하는가 |
| durability | 늦게 연결한 subscriber가 마지막 값을 받아야 하는가 |
| deadline | 예상 주기 안에 메시지가 오는가 |
| lifespan | 오래된 메시지를 전달할 가치가 있는가 |
| liveliness | publisher가 살아 있음을 어떻게 판단하는가 |

RMW 구현마다 일부 고급 정책 지원이 다를 수 있다. 실제 선택한 Fast DDS, Cyclone DDS, Zenoh 등의 지원과 성능을 같은 test matrix로 측정한다.

### executor와 callback

- callback이 오래 걸리면 같은 executor의 다른 callback이 지연될 수 있다.
- multithreaded executor는 자동으로 thread-safe를 보장하지 않는다.
- callback group으로 동시에 실행 가능한 작업을 명시한다.
- subscription callback에서는 최신 입력을 bounded queue에 넣고 worker가 추론하게 할 수 있다.
- service와 parameter 변경이 실시간 경로의 lock을 잡지 않게 한다.

### lifecycle

구성 단계와 실행 단계를 나누면 다음을 명확히 할 수 있다.

- configure: 모델 checksum, shape, calibration, memory allocation
- activate: 입력을 받고 결과를 publish
- deactivate: 새 결과를 중단하고 안전 상태로 전환
- cleanup: resource 해제
- error: 진단과 rollback

### composition과 zero-copy

같은 process의 component composition은 serialization과 process hop을 줄일 수 있다. GPU pipeline에서는 CPU로 내려왔다 다시 올리는 복사가 병목이 된다. NVIDIA NITROS 같은 type adaptation/negotiation 기술은 GPU memory의 불필요한 복사를 줄이지만, 실제 graph 전체의 latency와 utilization으로 검증해야 한다.

## 11. 데이터 엔지니어링

### rosbag이 곧 dataset은 아니다

bag을 수집한 뒤 다음 품질 검사가 필요하다.

- topic과 message type/version
- sensor serial과 calibration version
- timestamp 역행, gap, duplicate
- frame_id와 tf tree
- expected rate와 실제 rate
- drop 수와 recording 부하
- 개인정보와 위치정보
- 시나리오, 날씨, 조도, ODD metadata

MCAP의 compression preset은 기록 부하와 장기 보관 목적이 다르다. 현장에서는 fast write로 기록하고, offboard에서 index와 압축을 복원하는 두 단계 전략을 쓸 수 있다.

### split

frame 단위 random split은 인접 frame 누수를 만든다.

```text
권장 split key:
robot_id + mission_id + route + date + site
```

같은 로봇과 같은 주행이 train/test 양쪽에 들어가지 않도록 group split을 사용한다. 드문 위험 시나리오는 별도의 challenge set으로 유지한다.

### 재현성 tuple

실험 하나는 최소 다음 tuple로 식별한다.

```text
code commit
dataset version
label version
calibration version
base model checksum
hyperparameters
container/toolchain digest
random seeds
hardware
metrics
```

Git만으로 대용량 센서 데이터를 관리하지 않는다. DVC, object storage, 사내 catalog 등으로 content address와 접근 통제를 둔다.

## 12. 학습과 경량화의 깊은 기준

### fine-tuning 전에 확인할 것

1. 배포 backend가 모델의 operator를 지원하는가.
2. input resolution과 sequence length가 latency budget에 들어오는가.
3. 라이선스가 상용 배포와 weight 수정·재배포를 허용하는가.
4. 사전학습 domain이 목표 sensor와 얼마나 가까운가.
5. calibration/normalization을 정확히 재현할 수 있는가.

### fine-tuning 실험 설계

- head-only, partial unfreeze, full unfreeze를 같은 split에서 비교한다.
- learning rate는 새 head와 backbone에 다르게 둘 수 있다.
- class imbalance는 sampling, loss weight, hard example mining을 비교한다.
- augmentation은 물리적으로 가능한 변화만 적용한다.
- seed 여러 개로 평균과 분산을 본다.
- test set은 모델 선택에 사용하지 않는다.

### 경량화 순서

```text
입력/architecture 축소
→ operator fusion/graph optimization
→ FP16/BF16
→ PTQ INT8
→ mixed precision
→ QAT
→ structured pruning
→ distillation
```

한 번에 여러 기법을 적용하지 않는다. 각 단계마다 정확도, 위험 클래스 recall, latency, memory, power의 변화 원인을 분리한다.

### 모델 출력의 시스템 품질

- classification: calibration, 위험 클래스 recall, abstention
- detection: 거리/크기별 mAP, localization error, NMS stability
- segmentation: class IoU, boundary error, temporal flicker
- depth: 거리 구간별 absolute/relative error
- tracking: ID switch, fragmentation, latency
- trajectory: ADE/FDE뿐 아니라 collision, comfort, rule compliance

## 13. 검증 피라미드

```text
정적 분석·format
  → unit test
  → model contract/golden vector
  → component integration
  → rosbag open-loop replay
  → SIL 시나리오
  → HIL
  → closed-course
  → shadow fleet
  → 제한 ODD canary
```

아래 단계에서 찾을 수 있는 오류를 위 단계까지 미루지 않는다.

- unit: transform 방향, threshold, shape, NaN
- contract: Python/C++ logits 동등성
- bag replay: timestamp, QoS, 실제 분포
- SIL: closed-loop 상호작용
- HIL: driver, bus, timing, actuator interface
- closed-course: 물리 sensor와 vehicle dynamics
- shadow: 실제 운영 분포와 drift

## 14. 고장 주입

정상 입력만으로는 제품 준비를 증명할 수 없다.

필수 고장:

- 빈 입력, 잘못된 shape/dtype
- NaN/Inf, saturated sensor
- timestamp 역행과 오래된 입력
- sensor drop, burst, out-of-order
- model 파일 손상과 checksum 불일치
- GPU out-of-memory
- inference timeout
- disk full과 log 폭주
- network loss/jitter
- CPU/GPU thermal throttling
- node crash와 restart loop
- calibration 불일치

각 고장에 detection, containment, fallback, recovery, operator visibility를 정의한다.

## 15. 안전과 보안

안전 표준은 제품 유형마다 다르므로 법무·안전 담당자와 적용 범위를 정한다.

- 산업용 robot과 cell: ISO 10218-1:2025, ISO 10218-2:2025
- 무인 산업차량/AMR: ISO 3691-4:2023
- 도로 차량 기능 안전: ISO 26262 계열
- 의도된 기능의 성능 부족: ISO 21448:2022 SOTIF
- 협동 robot: ISO/TS 15066 등 적용 범위 검토

AI 출력은 safety function으로 자동 승격되지 않는다. hazard analysis, safety requirement, 독립 monitor, safe state, verification evidence가 필요하다.

보안 최소 기준:

- secure boot와 signed update
- model/config signature와 checksum
- 최소 권한 container/process
- ROS 2/DDS 보안과 network segmentation
- debug port와 default credential 제거
- SBOM, dependency scan, license inventory
- 취약점 대응 SLA와 rollback
- fleet credential rotation
- 수집 데이터 암호화와 retention

## 16. 이론을 실습으로 연결하기

다음 순서로 진행한다.

1. [labs/01_time_sync.py](labs/01_time_sync.py)에서 sensor timestamp 동기화와 drop을 측정한다.
2. [labs/02_fault_injection.py](labs/02_fault_injection.py)에서 stale·NaN·shape·timeout fallback을 시험한다.
3. [labs/03_release_gate.py](labs/03_release_gate.py)에서 모델 release를 Boolean gate로 판정한다.
4. [labs/04_latest_only_worker.cpp](labs/04_latest_only_worker.cpp)에서 오래된 frame을 쌓지 않는 C++ worker를 구현한다.
5. [06_organization_curriculum.md](06_organization_curriculum.md)의 capstone에서 rosbag/SIL/HIL 증거를 하나의 release dossier로 제출한다.
