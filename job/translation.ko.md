# 주요 공식 문서 한국어 번역 요약

작성일: 2026-07-25

심화 개정일: 2026-07-26

접근일: 2026-07-26

원문 언어: 영어
번역 방식: 저작권이 있는 문서를 전문 복제하지 않고, 이 학습 주제에 필요한 구조와 의미를 한국어로 재구성했다.

## ROS 2 문서

원문:

- [ROS 개발자 문서](https://docs.ros.org/index.html)
- [ROS 2 Jazzy Ubuntu 설치](https://docs.ros.org/en/jazzy/Installation/Alternatives/Ubuntu-Install-Binary.html)
- [ROS 2에서 Python 패키지 사용](https://docs.ros.org/en/jazzy/How-To-Guides/Using-Python-Packages.html)

핵심 내용:

- ROS는 로봇 애플리케이션을 만들기 위한 라이브러리와 도구 모음이다.
- 공식 문서는 Jazzy Jalisco를 최신 ROS 2 LTS로 안내하며 일반 사용자에게 권장한다.
- Jazzy의 사전 빌드 Ubuntu 바이너리는 Ubuntu 24.04 Noble의 x86_64와 ARM64를 지원한다.
- ROS 2 개발에서는 `rosdep`으로 시스템 의존성을 설치하고 `colcon`으로 workspace를 빌드한다.
- Python 가상환경을 ROS 2 바이너리와 함께 사용할 때는 ROS 2를 빌드한 시스템 Python과의 호환성을 주의해야 한다. Conda처럼 다른 인터프리터를 쓰면 바이너리 호환 문제가 날 수 있다.
- 개발 버전인 Rolling은 breaking change가 생길 수 있으므로 제품 기준선으로는 안정 배포판을 선택한다.

이 가이드에 반영한 판단:

- 일반 Ubuntu 24.04 실습 기준선은 ROS 2 Jazzy로 둔다.
- JetPack 6 계열처럼 Ubuntu 22.04 기반 장치는 보드 이미지와 공급사 호환성 때문에 ROS 2 Humble을 쓰는 경우가 있으므로, OS·ROS·JetPack 조합을 프로젝트별로 고정한다.

## ONNX Runtime 문서

원문:

- [ONNX Runtime 개요](https://onnxruntime.ai/docs/)
- [C++ 시작하기](https://onnxruntime.ai/docs/get-started/with-cpp.html)
- [Execution Provider](https://onnxruntime.ai/docs/execution-providers/)
- [그래프 최적화](https://onnxruntime.ai/docs/performance/model-optimizations/graph-optimizations.html)
- [양자화](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html)

핵심 내용:

- Python에서 학습한 모델을 C/C++·C#·Java 애플리케이션에서 실행하는 것이 ONNX Runtime의 대표 사용 흐름이다.
- 런타임은 그래프를 최적화한 후 가능한 연산을 CPU, CUDA, TensorRT 같은 Execution Provider에 배치한다.
- 그래프 최적화에는 상수 접기, 중복 제거, 연산 결합, layout 최적화 등이 있다.
- 제품 시작 시간을 줄이려면 대상 하드웨어와 같은 환경에서 offline optimized model을 만들 수 있다.
- 양자화는 FP32 값을 INT8 공간으로 사상한다. 동적 양자화는 실행 중 activation 범위를 계산하고, 정적 양자화는 대표 calibration 데이터로 미리 범위를 계산한다.
- 일반적인 권장 출발점은 RNN/Transformer에는 동적 양자화, CNN에는 정적 양자화다.
- PTQ가 정확도 목표를 만족하지 못하면 원래 학습 프레임워크에서 QAT를 수행한 뒤 ONNX로 다시 내보낸다.
- 양자화가 항상 빨라지는 것은 아니다. 대상 하드웨어의 INT8 명령 지원과 quantize/dequantize 비용을 실제로 측정해야 한다.
- 외부에서 받은 모델은 정확도, 성능, 적합성뿐 아니라 과도한 자원을 사용하는 악성 그래프 가능성도 검증해야 한다.

이 가이드에 반영한 판단:

- ONNX를 Python↔C++ 계약으로 사용한다.
- export 직후 원본과 출력 동등성을 검사한다.
- 양자화 전후의 정확도·모델 크기·실기기 latency를 함께 gate로 사용한다.

## NVIDIA TensorRT와 JetPack 문서

원문:

- [TensorRT 최신 문서](https://docs.nvidia.com/deeplearning/tensorrt/latest/)
- [TensorRT 설치 개요](https://docs.nvidia.com/deeplearning/tensorrt/latest/installing-tensorrt/installing.html)
- [JetPack 통합 설치 안내](https://docs.nvidia.com/deeplearning/tensorrt/latest/installing-tensorrt/install-alternative.html)

핵심 내용:

- TensorRT는 PyTorch, TensorFlow, ONNX 등에서 온 학습 모델을 NVIDIA GPU용 고성능 추론 엔진으로 최적화한다.
- 혼합 정밀도와 여러 정수 정밀도를 지원하며, 실제 지원 범위는 GPU 세대와 TensorRT 버전에 따라 달라진다.
- TensorRT는 학습된 모델을 하드웨어별 binary engine(plan)으로 컴파일한다.
- C++ 애플리케이션은 `libnvinfer`, ONNX parser 등의 라이브러리에 링크해 엔진을 실행한다.
- Jetson에서는 JetPack이 TensorRT, CUDA 등 플랫폼 소프트웨어를 묶어 제공하므로 임의 조합보다 JetPack 지원 조합을 우선한다.
- 성능 최적화는 먼저 측정하고, quantization·dynamic shape·CUDA graph·프로파일링을 반복하는 과정이다.

이 가이드에 반영한 판단:

- ONNX는 이식 가능한 원본 산출물로 보관하고 TensorRT engine은 대상 장치에서 생성한다.
- plan 파일만 보관하지 않고 생성에 사용한 ONNX, calibration, TensorRT/CUDA/JetPack 정보를 함께 추적한다.

## OpenVINO 문서

원문:

- [OpenVINO 공식 문서](https://docs.openvino.ai/)

핵심 내용:

- OpenVINO Runtime은 ONNX 등에서 온 모델을 Intel CPU, GPU, NPU를 포함한 지원 장치에서 실행한다.
- 같은 모델이라도 `CPU`, `GPU`, `NPU`, `AUTO` 같은 장치 선택과 비동기 요청 수에 따라 latency와 throughput이 달라진다.
- 양자화와 weight compression은 모델 크기와 메모리 사용량을 줄일 수 있지만, 대상 장치의 실제 지원과 정확도 측정이 필요하다.
- `benchmark_app`은 모델, 장치, shape, API 방식을 지정해 성능을 반복 측정하는 공식 도구다.

이 가이드에 반영한 판단:

- Intel 대상 장치에서는 검증된 ONNX를 유지한 채 OpenVINO Runtime 경로를 별도 비교한다.
- server throughput 설정과 로봇의 batch 1 deadline 설정을 구분한다.

## Autoware 문서

원문:

- [Autoware 문서](https://autowarefoundation.github.io/autoware-documentation/main/)
- [Autoware 설치](https://autowarefoundation.github.io/autoware-documentation/main/installation/)
- [Autoware launch 구조](https://autowarefoundation.github.io/autoware-documentation/main/contributing/coding-guidelines/ros-nodes/launch-files/)

핵심 내용:

- Autoware는 sensing, localization, perception, planning, control, vehicle interface를 포함하는 ROS 2 기반 자율주행 스택이다.
- camera, LiDAR, radar 센서 융합, 객체 추적, NDT·GNSS/IMU 기반 위치추정, 행동·경로 계획, trajectory following 등을 다룬다.
- rosbag replay와 AWSIM 같은 시뮬레이션을 검증 수단으로 사용한다.
- launch 구조는 Vehicle, System, Map, Sensing, Localization, Perception, Planning, Control 모듈로 나뉜다.
- Docker, source, Debian package 등 설치 방식이 있으며, 실험 기능을 포함한 Universe와 안정적인 핵심을 지향하는 Core의 역할이 구분된다.
- 신경망 기반 perception 기능은 GPU를 필요로 할 수 있으며 대상 장치 자원이 중요한 제약이다.

이 가이드에 반영한 판단:

- 학습 예제의 단일 분류 결과를 곧바로 차량 제어로 연결하지 않는다.
- 기록 데이터 재생, 시뮬레이션, 모듈 단위 검증, shadow mode를 배포 전 필수 흐름으로 설명한다.

## LiteRT for Microcontrollers 문서

원문:

- [마이크로컨트롤러 모델 빌드·변환](https://ai.google.dev/edge/litert/microcontrollers/build_convert)

핵심 내용:

- MCU는 RAM과 저장공간이 작고 지원 연산자가 제한되므로 처음부터 작은 모델 구조를 설계해야 한다.
- 학습 모델을 FlatBuffer 형식으로 변환하고 post-training quantization으로 크기를 더 줄일 수 있다.
- 파일시스템이 없는 MCU에서는 모델 파일을 C byte array로 바꾸어 firmware에 포함할 수 있다.
- 모델 크기뿐 아니라 연산량, 전력, 발열, 런타임 arena 메모리를 함께 고려한다.
- 모든 TensorFlow 연산이 Micro 런타임에서 지원되는 것은 아니므로 모델 설계 단계에서 resolver의 지원 연산을 확인한다.

이 가이드에 반영한 판단:

- Raspberry Pi/Jetson 같은 Linux SBC와 MCU를 같은 배포 문제로 취급하지 않는다.
- MCU가 목표라면 ONNX Runtime C++ 실습 다음에 억지로 이식하지 않고 LiteRT Micro/CMSIS-NN 제약에 맞춰 모델을 다시 설계한다.

## 번역 대조 점검

- 제품명, 파일 형식, API 명칭은 원문 표기를 유지했다.
- 버전은 고정된 사실처럼 일반화하지 않고 확인 기준일과 대상 OS 조합을 함께 적었다.
- 명령과 코드의 의미를 바꾸는 번역은 하지 않았다.
- 실제 장치의 지원 매트릭스는 변경될 수 있으므로 배포 직전에 각 공식 문서를 다시 확인해야 한다.

## ROS 2 실시간성·동기화·성능 분석

원문:

- [ROS 2 실시간 시스템 배경](https://design.ros2.org/articles/realtime_background.html)
- [ROS 2 실시간 시스템 구현 제안](https://design.ros2.org/articles/realtime_proposal.html)
- [message_filters 문서](https://docs.ros.org/en/ros2_packages/rolling/api/message_filters/message_filters.html)
- [ros2_tracing 실습](https://docs.ros.org/en/lyrical/Tutorials/Advanced/ROS2-Tracing-Trace-and-Analyze.html)
- [ROS 2 performance_test](https://docs.ros.org/en/rolling/p/performance_test/)

핵심 내용:

- 실시간성은 계산 결과뿐 아니라 deadline 안에 결과를 내는 것을 포함한다.
- hard, firm, soft real-time은 deadline miss 때 결과를 어떻게 취급하는지 구분한다.
- latency 평균만으로 predictability를 설명할 수 없으며 jitter, deadline miss, page fault와 failure mode를 측정해야 한다.
- lifecycle의 초기화 단계는 memory allocation과 설정을 수행하고 실행 단계는 제한된 동작만 수행하도록 나누는 데 유용하다.
- DDS/RMW와 QoS 선택은 latency와 predictability에 영향을 주므로 실제 middleware 조합을 측정해야 한다.
- `message_filters`는 header timestamp를 이용해 여러 입력을 결합하며 queue size와 tolerance가 drop과 time skew를 결정한다.
- `ros2_tracing`과 `performance_test`는 callback과 통신 경로의 성능 분석에 사용할 수 있다.

## Linux PREEMPT_RT

원문:

- [Linux kernel real-time preemption](https://www.kernel.org/doc/html/latest/core-api/real-time/index.html)
- [PREEMPT_RT 동작 원리](https://cdn.kernel.org/doc/html/latest/core-api/real-time/theory.html)

핵심 내용:

- PREEMPT_RT는 많은 lock과 interrupt 처리 경로를 scheduler가 다룰 수 있는 preemptible/threaded 형태로 바꾼다.
- priority inheritance는 높은 우선순위 thread가 낮은 우선순위 lock owner 때문에 무한정 막히는 문제를 줄인다.
- threaded interrupt는 긴 interrupt 처리 경로를 scheduler 통제 아래로 이동시킨다.
- real-time scheduling, memory/page fault, CPU와 IRQ affinity, lock 설계는 user-space가 별도로 올바르게 구성해야 한다.
- PREEMPT_RT kernel만으로 application의 hard real-time 보장이 자동 생성되는 것은 아니다.

## Isaac ROS Benchmark와 NITROS

원문:

- [Isaac ROS Benchmark](https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_benchmark/index.html)
- [NITROS type](https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_nitros/isaac_ros_nitros_type/index.html)

핵심 내용:

- Isaac ROS Benchmark는 graph의 throughput, latency, utilization을 재현 가능한 입력과 설정으로 비교하도록 한다.
- NITROS는 ROS 2 type adaptation과 negotiation을 활용해 GPU 가속 graph의 불필요한 CPU memory copy를 줄이는 것을 목표로 한다.
- 최적화 여부는 단일 node kernel 시간이 아니라 graph 전체 latency와 utilization으로 검증해야 한다.
- 2026-07-26 기준 지원 플랫폼과 JetPack 조합은 빠르게 바뀌므로 공식 support matrix를 release 직전에 다시 확인한다.

## Autoware 평가 workflow

원문:

- [신규 node 추가와 평가 절차](https://autowarefoundation.github.io/autoware-documentation/main/tutorials/others/an-example-procedure-for-adding-and-evaluating-a-new-node/)
- [Scenario test simulation](https://autowarefoundation.github.io/autoware-documentation/main/demos/scenario-simulation/scenario-simulator/scenario-test-simulation/)
- [Planning Data Analyzer](https://autowarefoundation.github.io/autoware_tools/main/planning/autoware_planning_data_analyzer/)

핵심 내용:

- 신규 node 평가 전에 표준 구성을 실행해 비교 baseline을 만든다.
- 실제 차량 또는 AWSIM에서 rosbag을 기록하고, 구현 뒤 logging simulator에서 같은 입력을 재생한 다음 realtime 환경으로 이동한다.
- rosbag 기록 자체가 계산 부하와 time series에 영향을 줄 수 있으므로 기록 품질을 검증한다.
- scenario simulator는 machine-readable 성공·실패 조건으로 planning을 반복 검증할 수 있다.
- planning 평가는 ADE/FDE만이 아니라 TTC, lane keeping, progress, comfort, collision, traffic compliance 같은 여러 측면을 포함한다.

## rosbag2 MCAP과 데이터 관리

원문:

- [rosbag2 MCAP storage](https://docs.ros.org/en/ros2_packages/kilted/api/rosbag2_storage_mcap/)
- [DVC command reference](https://dvc.org/doc/command-reference/)

핵심 내용:

- MCAP storage는 chunk, compression, CRC, index 설정에 따라 기록 부하, 파일 크기, random access, 무결성이 달라진다.
- `fastwrite`는 현장 기록 부하를 줄이는 대신 index와 CRC 일부를 포기할 수 있어 장기 보관 전에 변환하는 흐름이 권장된다.
- 데이터와 실험은 code commit만이 아니라 dataset, parameter, metric, artifact를 함께 versioning해야 재현할 수 있다.
- 대용량 sensor data는 Git에 직접 넣기보다 content-addressed cache와 object storage를 사용하는 도구나 사내 체계가 필요하다.

## 로봇·자율주행 안전 표준

원문:

- [ISO 10218-1:2025](https://www.iso.org/standard/73933.html)
- [ISO 3691-4:2023](https://www.iso.org/standard/83545.html)
- [ISO 21448:2022](https://www.iso.org/standard/77490.html)

핵심 내용:

- ISO 10218-1:2025는 산업용 robot 자체의 안전 요구를, Part 2는 robot application과 cell integration을 다룬다.
- ISO 3691-4:2023은 AGV, AMR 등 무인 산업차량과 시스템의 safety requirement와 verification을 다룬다.
- ISO 21448:2022 SOTIF는 고장 자체가 아니라 specification 또는 sensor/algorithm 성능 부족으로 생기는 비합리적 위험을 줄이기 위한 argument와 V&V 활동을 다룬다.
- 적용 표준은 제품, 사용 환경, 관할, intended use에 따라 달라지므로 이 문서는 인증 해석을 대신하지 않는다.

## ROS 2 통신 보안과 software supply chain

원문:

- [ROS 2 Security keystore](https://docs.ros.org/en/ros2_documentation/jazzy/Tutorials/Advanced/Security/The-Keystore.html)
- [ROS 2 DDS-Security integration](https://design.ros2.org/articles/ros2_dds_security.html)
- [CISA SBOM 소비 권고](https://www.cisa.gov/sites/default/files/2024-08/SECURING_THE_SOFTWARE_SUPPLY_CHAIN_RECOMMENDED_PRACTICES_FOR_SOFTWARE_BILL_OF_MATERIALS_CONSUMPTION-508.pdf)

핵심 내용:

- SROS 2는 DDS Security를 사용하기 위한 key, certificate, governance, permission policy와 enclave를 관리한다.
- production CA와 private key는 실습처럼 즉석 생성해 공유하지 않고 조직의 PKI와 rotation/revocation 정책으로 관리해야 한다.
- permissive와 enforce 전략의 차이를 알고, production에서는 승인되지 않은 participant와 topic 접근을 차단하는 policy를 시험한다.
- SBOM은 보유 자체보다 integrity, origin, completeness를 확인하고 알려진 취약점과 실제 배포 artifact를 연결하는 운영이 중요하다.
- model, metadata, container, native library도 code와 같은 release supply chain으로 서명·검증·rollback해야 한다.
