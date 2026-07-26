# Python 실험에서 C++ 임베디드 AI 배포까지

작성일: 2026-07-25

조직용 심화 개정일: 2026-07-26

확인 기준일: 2026-07-26
대상 환경: Ubuntu 24.04 + ROS 2 Jazzy(일반 PC/ARM64), JetPack 6/Orin 또는 JetPack 7/Thor 계열은 공급사 지원 조합에 맞춰 선택

## 출처와 작업 범위

이 가이드는 “Python으로 빠르게 모델을 실험하고, 검증된 모델을 Linux의 C/C++ 애플리케이션과 ROS 2에 넣어 로봇·자율주행·임베디드 장치에서 운영하는 과정”을 처음부터 실습하도록 구성했다.

사용자가 특정 하드웨어를 지정하지 않았으므로 다음과 같이 가정했다.

- 첫 실습은 GPU가 없어도 가능한 작은 센서 분류 모델로 진행한다.
- 교환 가능한 중간 형식으로 ONNX를 사용한다.
- C++ 기본 런타임은 CPU와 ARM64에서 시작하기 쉬운 ONNX Runtime으로 한다.
- Jetson에서는 TensorRT, Intel CPU/GPU/NPU에서는 OpenVINO, 메모리가 매우 작은 MCU에서는 LiteRT for Microcontrollers를 대안으로 설명한다.
- 로봇 소프트웨어의 결합 지점은 ROS 2 노드로 한다.
- 안전이 중요한 실제 차량·로봇에서는 본 예제를 곧바로 제어기에 연결하지 않고 시뮬레이션, 기록 데이터 재생, shadow mode를 거쳐야 한다.

주요 공식 자료:

- [ROS 2 문서와 최신 LTS 안내](https://docs.ros.org/index.html)
- [ROS 2 Jazzy Ubuntu 설치](https://docs.ros.org/en/jazzy/Installation/Alternatives/Ubuntu-Install-Binary.html)
- [ONNX Runtime 개요](https://onnxruntime.ai/docs/)
- [ONNX Runtime C++ 시작하기](https://onnxruntime.ai/docs/get-started/with-cpp.html)
- [ONNX Runtime 양자화](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html)
- [NVIDIA TensorRT 문서](https://docs.nvidia.com/deeplearning/tensorrt/latest/)
- [OpenVINO 문서](https://docs.openvino.ai/)
- [Autoware 문서](https://autowarefoundation.github.io/autoware-documentation/main/)
- [Autoware 신규 노드 rosbag 평가 절차](https://autowarefoundation.github.io/autoware-documentation/main/tutorials/others/an-example-procedure-for-adding-and-evaluating-a-new-node/)
- [ROS 2 실시간 시스템 배경](https://design.ros2.org/articles/realtime_background.html)
- [ROS 2 Security keystore](https://docs.ros.org/en/ros2_documentation/jazzy/Tutorials/Advanced/Security/The-Keystore.html)
- [Linux PREEMPT_RT 문서](https://www.kernel.org/doc/html/latest/core-api/real-time/index.html)
- [Isaac ROS Benchmark](https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_benchmark/index.html)
- [ROS 2 MCAP storage](https://docs.ros.org/en/ros2_packages/kilted/api/rosbag2_storage_mcap/)
- [ISO 10218-1:2025 산업용 로봇 안전](https://www.iso.org/standard/73933.html)
- [ISO 3691-4:2023 무인 산업차량 안전](https://www.iso.org/standard/83545.html)
- [ISO 21448:2022 SOTIF](https://www.iso.org/standard/77490.html)
- [CISA SBOM 소비 권고](https://www.cisa.gov/sites/default/files/2024-08/SECURING_THE_SOFTWARE_SUPPLY_CHAIN_RECOMMENDED_PRACTICES_FOR_SOFTWARE_BILL_OF_MATERIALS_CONSUMPTION-508.pdf)
- [LiteRT for Microcontrollers 모델 변환](https://ai.google.dev/edge/litert/microcontrollers/build_convert)

공식 영문 자료의 핵심 한국어 재구성은 [translation.ko.md](translation.ko.md)에 있다.

## 조직용 재평가와 개정 방향

초판은 Python 모델을 ONNX와 C++로 옮기는 입문 흐름에는 충분했지만, 선도 로보틱스 조직의 공통 교육과 release 책임 기준으로는 다음이 부족했다.

| 부족했던 부분 | 제품에서 생기는 결과 | 이번 개정 |
|---|---|---|
| 센서 시간·좌표계·calibration | 서로 다른 순간과 frame을 결합 | [05_robotics_foundations.md](05_robotics_foundations.md) |
| 추정·계획·제어와 AI의 연결 | 높은 모델 점수와 나쁜 closed-loop 동작 | 시스템 기초의 state estimation/planning/control |
| ROS 2 executor·lifecycle·실시간성 | callback 정체, stale 결과, p99 악화 | QoS/RMW/executor/PREEMPT_RT 심화 |
| 데이터 lineage와 group split | frame leakage와 재현 불가능한 실험 | MCAP QA, 재현성 tuple, dataset release |
| 장애 주입과 release 판정 | 정상 demo는 성공하지만 현장 오류에 취약 | [labs/README.md](labs/README.md)의 자동 실습 |
| 역할별 숙련도와 평가 | 수강 완료가 역량으로 오인됨 | [06_organization_curriculum.md](06_organization_curriculum.md) |
| 종합 출시 evidence | 모델·runtime·안전 검토가 분리됨 | [07_capstone.md](07_capstone.md) |

개정 이후의 중심 질문은 “모델이 돌아가는가?”가 아니라 다음 일곱 가지다.

1. 입력의 시간, frame, 단위, 유효 범위가 증명되는가.
2. 같은 code/data/model/runtime 조합을 다른 구성원이 재현할 수 있는가.
3. Python, ONNX, C++ 결과가 golden vector 허용 오차 안인가.
4. 실제 target의 tail latency, memory, power, thermal이 budget 안인가.
5. stale·NaN·timeout·파일 손상에서 안전한 fallback이 동작하는가.
6. rosbag, SIL, HIL, shadow 단계의 evidence가 있는가.
7. 잘못된 release를 자동 거부하고 이전 release로 rollback할 수 있는가.

## 한눈에 보기

실무의 핵심은 “Python을 C++로 번역”하는 것이 아니다. 모델 파일과 전처리·후처리 규약을 고정하고, C++에서 같은 규약을 재현하는 것이다.

```text
문제/지표 정의
  → 데이터 수집·분리
  → Python 기준 모델
  → 파인튜닝
  → 정확도 회귀 테스트
  → ONNX 내보내기
  → 경량화(FP16/INT8/가지치기)
  → 대상 장치 C++ 벤치마크
  → ROS 2 통합
  → 시뮬레이션/rosbag/shadow mode
  → 제한된 현장 배포
  → 모니터링과 롤백
```

완료 조건은 단순히 “모델이 실행됨”이 아니다.

| 게이트 | 최소 확인 항목 |
|---|---|
| 품질 | 기준 모델 대비 정확도 저하, 클래스별 recall, 오탐/미탐 |
| 속도 | p50/p95/p99 지연시간, 센서 주기 안에서 완료되는지 |
| 자원 | 최대 RAM/VRAM, 모델 크기, CPU/GPU 사용률, 전력·온도 |
| 호환성 | 대상 OS·아키텍처·런타임 버전에서 재현 가능한지 |
| 안전 | timeout, 입력 이상, 모델 로드 실패 때 안전한 fallback |
| 운영 | 모델 버전, 로그, 원격 롤백, canary/shadow 배포 |

## 어떤 플랫폼과 프레임워크를 선택하는가

“가장 유명한 도구”보다 목표 하드웨어와 운영 제약에 맞는 도구가 옳다.

| 목표 장치 | 보통의 1차 선택 | 이유 | 주의점 |
|---|---|---|---|
| Ubuntu x86 CPU | ONNX Runtime 또는 OpenVINO | C++ API, 배포가 단순함 | 실제 CPU 명령어와 스레드 수로 측정 |
| Intel CPU/GPU/NPU | OpenVINO | Intel 하드웨어 최적화와 변환 도구 | 지원 연산과 장치 플러그인 확인 |
| NVIDIA Jetson | TensorRT + JetPack, 필요 시 Isaac ROS | FP16/INT8, CUDA/DLA 활용 | 엔진은 장치·TensorRT 버전에 민감 |
| NVIDIA DRIVE | DRIVE OS + TensorRT | 자동차용 NVIDIA 스택 | 라이선스·안전 프로세스·지원 매트릭스 확인 |
| Raspberry Pi/일반 ARM64 Linux | ONNX Runtime 또는 LiteRT | CPU 기반 소형 배포 | NEON, 메모리, 발열을 실기기에서 측정 |
| Android/Linux 모바일 SoC | LiteRT 또는 공급사 NPU SDK | 모바일 가속기 delegate 활용 | 지원 연산이 제한될 수 있음 |
| Cortex-M/ESP32/STM32급 MCU | LiteRT for Microcontrollers, CMSIS-NN | 파일시스템 없이 작은 C 배열 모델 사용 | RAM·flash·연산자 지원이 매우 제한적 |
| 로봇 시스템 결합 | ROS 2, Nav2, MoveIt 2, Isaac ROS | 센서·추론·제어를 노드와 토픽으로 분리 | QoS, timestamp, 실시간성, 복사 비용 |
| 자율주행 전체 스택 | Autoware + ROS 2 | sensing부터 control까지 공개 구조 | 실제 도로 투입은 별도의 안전 검증 필수 |
| 시뮬레이션 | Gazebo, CARLA, AWSIM | 실제 장비 전 시나리오 반복 | sim-to-real 차이를 별도 관리 |

권장 출발점:

1. 하드웨어가 미정이면 `PyTorch → ONNX → ONNX Runtime CPU`.
2. Jetson으로 확정되면 같은 ONNX를 TensorRT로 빌드해 비교한다.
3. Intel 장치로 확정되면 OpenVINO 경로를 비교한다.
4. MCU라면 처음부터 작은 연산자 집합과 메모리 예산으로 모델을 다시 설계한다.

## 기초 개념

### 학습과 추론

- 학습(training): 정답 데이터로 가중치를 바꾸는 과정이다. 대개 Python과 GPU를 사용한다.
- 파인튜닝(fine-tuning): 이미 학습된 가중치를 새 데이터에 맞게 조금 더 학습한다.
- 추론(inference): 고정된 가중치로 새 입력의 결과를 계산한다. C++ 배포의 주 작업이다.
- 런타임(runtime): ONNX Runtime, TensorRT처럼 모델 그래프를 실행하는 라이브러리다.
- 실행 제공자(Execution Provider): ONNX Runtime에서 CPU, CUDA, TensorRT 등 실제 계산 백엔드를 선택하는 계층이다.

### 전처리와 후처리

모델 정확도 차이의 흔한 원인은 모델 자체보다 Python과 C++의 입력 처리 차이다.

- 센서 단위: m/s인지 km/h인지
- 채널 순서: RGB인지 BGR인지
- 텐서 배치: NCHW인지 NHWC인지
- 정규화: `(x - mean) / std`의 mean/std 값과 자료형
- resize: 보간법, letterbox, crop 방식
- 출력: softmax 적용 여부, threshold, NMS 파라미터

이 값들은 코드에 흩어 놓지 말고 모델 메타데이터와 테스트 벡터로 버전 관리한다.

### 실시간이라는 말

평균 10 ms만으로 실시간을 증명할 수 없다. 30 Hz 카메라라면 한 프레임 예산은 약 33.3 ms지만 센서 수신, 전처리, 추론, 후처리, 통신이 모두 그 안에 들어가야 한다. p99 지연과 deadline miss 비율도 측정한다.

### ROS 2의 역할

ROS 2는 모델 학습 도구가 아니라 로봇 구성 요소 사이의 통신·수명주기·설정·빌드를 돕는 미들웨어와 도구 모음이다.

```text
Camera/LiDAR Node
  → Preprocess/Inference Node
  → Tracking/Fusion Node
  → Planning Node
  → Control Node
  → Vehicle Interface
```

AI 노드는 센서 timestamp를 보존하고, 처리 시간이 deadline을 넘거나 입력이 오래되면 결과를 폐기해야 한다.

## 실무 적용 프로세스

### 0단계: 문제를 모델보다 먼저 정의한다

예: “진동 센서 네 개로 정상/주의/정지 필요 상태를 20 ms 안에 분류한다.”

- 입력 shape와 단위
- 출력 클래스와 행동
- 실패 비용: 오탐과 미탐 중 무엇이 더 위험한가
- 대상 장치의 CPU/GPU/NPU, RAM, 전력, 온도
- 센서 주기와 end-to-end latency budget
- 정상 동작 영역(ODD)과 범위를 벗어났을 때 fallback

### 1단계: 데이터 계약과 분리를 고정한다

현장 데이터는 시간·장치·장소가 섞이기 쉽다. 무작위 row 분할만 하면 같은 주행의 인접 프레임이 train과 validation에 동시에 들어가 과도하게 좋은 점수가 나온다.

- 주행, 날짜, 장치 ID 기준으로 train/validation/test를 분리한다.
- test는 마지막까지 학습에 사용하지 않는다.
- class imbalance와 드문 위험 사례를 따로 보고한다.
- 개인정보·위치 정보·라이선스와 보존 기간을 확인한다.
- 원본 데이터, 라벨 버전, 전처리 코드를 함께 추적한다.

### 2단계: Python 기준 모델을 만든다

처음부터 큰 모델을 쓰지 않는다. 가장 단순한 baseline과 작은 모델을 먼저 비교한다.

```bash
cd job
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
jupyter lab
```

Windows의 현재 저장소에서도 문서와 순수 NumPy 실습 검증은 가능하지만, ROS 2/C++ 배포 실습은 Ubuntu 24.04 또는 대응 Docker/WSL2 환경을 권장한다.

### 3단계: 경량 모델을 파인튜닝한다

권장 순서:

1. 배포 가능한 작은 사전학습 모델을 고른다.
2. 원래 입력 전처리를 그대로 재현한다.
3. 분류 head만 새 작업에 맞게 교체한다.
4. backbone을 얼리고 head만 짧게 학습한다.
5. 작은 learning rate로 backbone 일부 또는 전체를 푼다.
6. validation 지표와 과적합을 확인한다.
7. 고정 test set으로 최종 한 번 평가한다.
8. 모델과 함께 class map, mean/std, 입력 shape를 저장한다.

작은 모델 후보 예:

- 이미지: MobileNetV3, EfficientNet-Lite, SqueezeNet, 작은 YOLO 계열
- 시계열/센서: 작은 1D CNN, GRU, MLP, Tiny Transformer
- 음성: MobileNet/DS-CNN 계열

모델 이름만 보고 선택하지 말고 대상 런타임의 연산자 지원, 실제 latency, 메모리, 정확도를 함께 본다.

### 4단계: 경량화는 쉬운 것부터 적용한다

| 기법 | 언제 | 장점 | 위험 |
|---|---|---|---|
| 더 작은 구조 | 가장 먼저 | 재현성이 좋고 모든 런타임에 유리 | 정확도 한계 |
| FP16 | GPU/NPU | 크기 감소, Tensor Core 활용 | CPU에서 이득이 없을 수 있음 |
| INT8 PTQ | 대표 calibration 데이터가 있을 때 | 속도·메모리 개선 가능 | 정확도 하락, 지원 op 확인 |
| QAT | PTQ 정확도가 부족할 때 | INT8 정확도 회복 가능 | 학습과 export가 복잡 |
| 구조적 pruning | 채널/헤드 제거가 가능할 때 | 실제 tensor 크기 감소 | 재학습 필요 |
| 비구조적 pruning | 희소 가속기가 있을 때 | 압축 가능 | 일반 하드웨어에서 빨라지지 않을 수 있음 |
| distillation | 큰 teacher가 있을 때 | 작은 student 품질 개선 | 학습 파이프라인 추가 |

중요: 파일 크기가 줄었다고 latency가 줄었다는 뜻은 아니다. 반드시 대상 장치에서 측정한다.

### 5단계: ONNX로 계약을 고정한다

- 가능한 한 배포에서 필요한 고정 입력 크기로 먼저 성공시킨다.
- ONNX checker와 런타임 로드로 유효성을 확인한다.
- Python 원본과 ONNX 출력의 최대 절대 오차를 비교한다.
- 실제 데이터에서 정확도 회귀 테스트를 다시 실행한다.
- 입력/출력 이름, shape, dtype, opset, 전처리를 기록한다.

### 6단계: 대상 장치에서 엔진을 만든다

- TensorRT engine은 개발 PC가 아니라 실제 배포 장치 또는 동일한 환경에서 빌드한다.
- INT8 calibration 데이터는 실제 운영 분포를 대표해야 한다.
- 엔진 캐시는 GPU, TensorRT, CUDA 버전과 함께 관리한다.
- warm-up 후 충분한 횟수로 p50/p95/p99와 peak memory를 잰다.
- 성능 측정 중 CPU governor, 전력 모드, 온도 throttling 상태를 기록한다.

### 7단계: C++ 애플리케이션에 통합한다

C++ 추론 코드는 다음 책임으로 나눈다.

```text
ModelRunner: 세션 생성, 입력/출력 tensor, 추론
Preprocessor: 단위·정규화·shape 변환
Postprocessor: score, threshold, class map
HealthMonitor: timeout, stale input, 오류 횟수, fallback
Application/ROS Node: 센서 구독과 결과 발행
```

RAII와 명확한 소유권을 사용하고, steady clock으로 latency를 측정한다. hot path에서 반복적인 메모리 할당과 모델 재로딩을 피한다.

### 8단계: ROS 2에 붙인다

1. Python 노드로 토픽과 메시지 계약을 먼저 검증한다.
2. 같은 bag 입력으로 C++ 노드의 결과를 비교한다.
3. QoS를 센서 특성에 맞춘다. 최신 프레임이 중요한 카메라에서는 오래된 queue를 처리하지 않는다.
4. callback 안에서 긴 추론으로 executor를 막지 않도록 callback group, 별도 worker, component 구조를 검토한다.
5. lifecycle node로 configure/activate/deactivate 전환과 모델 로드 실패를 관리한다.
6. rosbag replay → simulator → hardware-in-the-loop → shadow mode 순으로 진행한다.

### 9단계: 안전하게 배포하고 운영한다

- 모델 버전과 checksum을 시작 로그에 남긴다.
- input drift, confidence 분포, latency, drop rate, 온도를 모니터링한다.
- 신모델은 canary 또는 shadow mode로 구모델과 비교한다.
- 실패 시 즉시 이전 모델로 돌아갈 수 있게 한다.
- 모델 출력이 직접 actuator 명령이 되지 않도록 규칙 기반 안전 계층을 둔다.
- 자동차 안전은 ISO 26262, SOTIF 등 조직의 적용 표준과 안전 담당 검토를 따른다. 이 학습 예제는 안전 인증 자료가 아니다.

## 실습 학습 가이드

### 권장 순서

#### 개인 기초 실습

1. [05_robotics_foundations.md](05_robotics_foundations.md)
   모델보다 먼저 시간, 좌표계, calibration, 추정·계획·제어, 실시간성, 데이터와 안전의 기반을 학습한다.
2. [01_foundations.ipynb](01_foundations.ipynb)
   센서 데이터, 정규화, softmax, latency budget, Python 기준 출력의 의미를 배운다. 외부 데이터 다운로드 없이 실행한다.
3. [02_fine_tuning.ipynb](02_fine_tuning.ipynb)
   작은 PyTorch 모델을 사전학습한 뒤 새 장치 데이터에 맞춰 head-only와 전체 미세조정을 비교한다.
4. [03_advanced.ipynb](03_advanced.ipynb)
   ONNX export, Python↔ONNX 동등성, INT8 동적 양자화, 정확도·크기·지연시간 acceptance gate를 실행한다.
5. [08_vision_transfer_learning.ipynb](08_vision_transfer_learning.ipynb)
   실제 `ImageFolder` 데이터에서 MobileNetV3-Small을 head-only와 전체 미세조정한 뒤 ONNX와 metadata를 만든다.
6. [04_platform_recipes.md](04_platform_recipes.md)
   Ubuntu CPU, Jetson/TensorRT, Intel/OpenVINO, ARM64, MCU, ROS 2, Autoware 대상별 명령과 검증 항목을 실습한다.
7. [cpp/README.md](cpp/README.md)
   생성된 ONNX 모델을 ONNX Runtime C++로 읽고 한 건을 추론한다.
8. [cpp/CPP_MASTERCLASS.md](cpp/CPP_MASTERCLASS.md)
   소유권·수명·RAII·move·condition variable·happens-before·undefined behavior·ONNX tensor view·ROS executor를 코드 감사 결과와 함께 깊게 학습한다.
9. [ros2/README.md](ros2/README.md)
   같은 추론 클래스를 ROS 2 C++ 노드에 연결하는 최소 패키지를 빌드한다.
10. [labs/README.md](labs/README.md)
   시간 동기화, stale/NaN/timeout, circuit breaker, 자동 release gate, latest-only C++ worker를 직접 실패시키며 학습한다.

#### 조직 과정

1. [06_organization_curriculum.md](06_organization_curriculum.md)의 사전 진단으로 개인별 L0~L3 수준을 정한다.
2. 14주 공통 과정과 Perception/ML, Integration, Platform, Controls/Safety 심화 트랙을 병행한다.
3. 각 실습에서 implementer, reviewer, operator, red team 역할을 순환한다.
4. [07_capstone.md](07_capstone.md)에서 실제 또는 물리 simulator 데이터와 target hardware를 사용한 release 후보를 만든다.
5. 점수뿐 아니라 checksum, invalid input, golden vector, p99, rollback 필수 gate를 모두 통과해야 합격한다.

### 실습 산출물

```text
job/
  artifacts/
    sensor_model.pt
    sensor_model.onnx
    sensor_model.int8.onnx
    metadata.json
  reports/
    benchmark.json
```

`artifacts/`와 `reports/`는 노트북 실행 시 만들어지며 Git에는 생성물을 커밋하지 않도록 설정했다.

### 각 코드 라인을 읽는 방법

노트북은 코드 셀 바로 앞에 줄 번호별 설명 표를 둔다. C++ 예제는 각 실행문 위에 한국어 주석을 넣고 [cpp/README.md](cpp/README.md)에서 문법과 수명주기를 다시 설명한다. 주석을 지우고 직접 다시 작성해 보는 것이 가장 좋은 복습이다.

## 실무 체크리스트

### 모델 승인

- [ ] test set이 train/validation과 주행·날짜·장치 단위로 분리되었다.
- [ ] 전체 정확도뿐 아니라 위험 클래스 recall을 확인했다.
- [ ] Python과 배포 런타임의 출력 오차가 허용 범위 안이다.
- [ ] 경량화 전후의 정확도 차이를 기록했다.
- [ ] 입력 범위 밖 값과 NaN/Inf를 처리한다.

### 장치 승인

- [ ] 실제 장치의 p50/p95/p99 latency를 측정했다.
- [ ] 장시간 실행 시 온도와 throttling을 측정했다.
- [ ] 메모리 부족과 모델 파일 손상을 시험했다.
- [ ] 센서 중단, 오래된 timestamp, queue 적체를 시험했다.
- [ ] watchdog과 안전 fallback이 동작한다.

### 릴리스 승인

- [ ] OS, 런타임, 드라이버, 모델 checksum을 고정했다.
- [ ] 재현 가능한 컨테이너 또는 설치 스크립트가 있다.
- [ ] 구모델과 신모델을 shadow/canary로 비교했다.
- [ ] 롤백 절차와 담당자가 정해졌다.
- [ ] 로그에 민감한 원본 센서 데이터가 무단 저장되지 않는다.

## 용어 정리

| 용어 | 뜻 |
|---|---|
| ONNX | 학습 프레임워크와 추론 런타임 사이의 모델 교환 형식 |
| ONNX Runtime | ONNX 모델을 여러 CPU/GPU/NPU 백엔드에서 실행하는 런타임 |
| TensorRT | NVIDIA GPU용 모델 최적화·추론 SDK |
| OpenVINO | Intel 하드웨어 중심의 모델 최적화·추론 도구 |
| ROS 2 | 로봇용 통신, 패키지, 빌드, 실행 도구 생태계 |
| Autoware | ROS 2 기반의 공개 자율주행 소프트웨어 스택 |
| FP16 | 16비트 부동소수점 표현 |
| INT8 | 8비트 정수 표현; calibration 또는 QAT가 필요할 수 있음 |
| PTQ | 학습 후 양자화(Post-Training Quantization) |
| QAT | 양자화 오차를 흉내 내며 다시 학습하는 Quantization-Aware Training |
| calibration | 대표 입력으로 activation 범위를 측정하는 절차 |
| distillation | 큰 teacher의 출력을 작은 student가 학습하는 방법 |
| pruning | 중요도가 낮은 가중치·채널·헤드를 제거하는 방법 |
| latency | 입력부터 출력까지 걸린 시간 |
| throughput | 단위 시간당 처리량 |
| p99 | 측정값의 99%가 이 값 이하라는 백분위 지연시간 |
| QoS | ROS 2 메시지 전달 신뢰성, queue 깊이 등의 정책 |
| rosbag | ROS 토픽을 기록하고 재생하는 데이터 형식·도구 |
| shadow mode | 신모델 결과를 제어에는 쓰지 않고 구모델과 비교하는 운영 방식 |
| ODD | 시스템이 정상 동작하도록 설계된 환경·조건의 범위 |

## 다음 학습 경로

1. 본 실습의 4개 입력을 실제 CSV 센서 데이터로 교체한다.
2. 이미지 문제라면 MobileNetV3 또는 작은 탐지 모델로 같은 export gate를 반복한다.
3. `trtexec` 또는 OpenVINO benchmark tool로 실제 장치 성능을 비교한다.
4. rosbag으로 동일 입력을 Python/C++ 노드에 재생하고 결과를 자동 비교한다.
5. Gazebo·CARLA·AWSIM에서 센서 지연, drop, 악천후 시나리오를 추가한다.
6. 모델 레지스트리, 데이터 버전, CI의 정확도/latency 회귀 테스트를 연결한다.
7. 실제 actuator 연결 전 조직의 안전 분석과 독립 검토를 수행한다.
