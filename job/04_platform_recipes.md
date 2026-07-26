# 대상 장치별 배포 실습 레시피

작성일: 2026-07-25
확인 기준일: 2026-07-25

이 문서는 `03_advanced.ipynb`에서 검증한 `artifacts/sensor_model.onnx`를 각 대상 환경으로 옮기는 다음 실습이다. 명령의 버전 번호와 archive 이름은 일부러 고정하지 않았다. 보드 OS 이미지와 공급사 지원 매트릭스에 맞는 버전을 선택해야 하기 때문이다.

## 공통 준비: 배포 묶음을 만든다

다음 파일을 하나의 버전으로 함께 관리한다.

```text
release/sensor-model-1/
  sensor_model.onnx
  metadata.json
  golden_inputs.npy
  golden_outputs.npy
  SHA256SUMS
  release-notes.md
```

- `sensor_model.onnx`: 교환 가능한 FP32 기준 모델
- `metadata.json`: 입력 shape/dtype/name, mean/std, class map
- `golden_inputs.npy`: Python과 C++ 비교에 쓰는 고정 test vector
- `golden_outputs.npy`: 허용 오차와 함께 저장한 기준 logits
- `SHA256SUMS`: 전송 중 손상과 잘못된 모델 로드를 찾는 checksum
- `release-notes.md`: 데이터·코드·opset·지표·알려진 한계

Ubuntu에서 checksum을 만든다.

```bash
# release 폴더로 이동해 출력 파일 이름이 짧고 재현 가능하게 한다.
cd release/sensor-model-1
# sha256sum은 두 핵심 배포 파일의 SHA-256 digest를 계산한다.
sha256sum sensor_model.onnx metadata.json > SHA256SUMS
# -c는 저장된 digest와 현재 파일을 다시 계산해 일치 여부를 검사한다.
sha256sum -c SHA256SUMS
```

## 레시피 A: Ubuntu x86_64/ARM64 + ONNX Runtime

가장 먼저 통과시킬 이식성 기준선이다.

1. [공식 ONNX Runtime C++ 안내](https://onnxruntime.ai/docs/get-started/with-cpp.html)에서 대상 아키텍처에 맞는 배포 archive를 준비한다.
2. `/opt/onnxruntime` 아래에 `include/`와 `lib/`가 오도록 둔다.
3. [cpp/README.md](cpp/README.md)의 CMake 명령으로 빌드한다.
4. golden input을 C++ 실행기에 넣고 Python 결과와 비교한다.
5. `taskset`, CPU governor, 전원 모드, 온도를 기록한 뒤 반복 benchmark를 한다.

```bash
# Release 최적화로 별도 build 폴더를 configure한다.
cmake -S cpp -B cpp/build \
  -DCMAKE_BUILD_TYPE=Release \
  -DONNXRUNTIME_ROOT=/opt/onnxruntime
# 현재 CPU core 수를 활용해 edge_infer target을 병렬 빌드한다.
cmake --build cpp/build --parallel
# 동적 linker가 libonnxruntime.so를 찾도록 현재 shell의 검색 경로에 추가한다.
export LD_LIBRARY_PATH=/opt/onnxruntime/lib:${LD_LIBRARY_PATH}
# batch 1, 표준화 입력 네 개로 추론 smoke test를 실행한다.
./cpp/build/edge_infer artifacts/sensor_model.onnx 0.0 0.0 0.0 0.0
```

제품에서는 `LD_LIBRARY_PATH`에 의존하기보다 package 설치, RPATH, container 중 조직 표준을 선택한다.

## 레시피 B: NVIDIA Jetson + TensorRT

### 1. 환경을 고정한다

- Jetson 모델과 compute capability
- JetPack/Jetson Linux
- CUDA, cuDNN, TensorRT
- 전력 모드와 clock
- 사용할 GPU 또는 DLA

JetPack은 이 조합을 통합 제공한다. Ubuntu PC에서 최신 TensorRT만 따로 골라 만든 engine을 Jetson에 복사하는 방식은 피한다.

2026-07-26 기준 [Isaac ROS Benchmark 공식 지원표](https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_benchmark/index.html)는 Jetson Thor와 JetPack 7.1, ROS 2 Jazzy 조합을 포함한다. 기존 Orin 제품은 JetPack 6 계열을 유지하는 경우가 있으므로 “최신 버전으로 일괄 업그레이드”하지 않는다. 제품 line마다 다음 compatibility lock을 둔다.

```text
board/SKU
  ↔ BSP/JetPack
  ↔ Ubuntu
  ↔ CUDA/cuDNN/TensorRT
  ↔ ROS 2/Isaac ROS
  ↔ camera driver
  ↔ model engine cache
```

새 platform은 같은 기능의 golden bag, scenario, power/thermal test를 모두 다시 통과해야 한다.

### 2. FP16 engine을 실제 Jetson에서 만든다

```bash
# trtexec가 읽을 ONNX와 만들 engine 경로를 명시한다.
trtexec \
  --onnx=artifacts/sensor_model.onnx \
  --saveEngine=artifacts/sensor_model.fp16.engine \
  --fp16 \
  --shapes=sensor_features:1x4
```

줄별 의미:

- `trtexec`: TensorRT에 포함된 model build·benchmark CLI다.
- `--onnx`: parser가 읽을 검증된 교환 모델이다.
- `--saveEngine`: 현재 장치와 TensorRT 환경에 최적화된 plan 파일을 저장한다.
- `--fp16`: 지원 layer에서 반정밀도를 사용하도록 builder에 허용한다.
- `--shapes`: dynamic batch로 export한 입력의 실제 최적화 shape를 지정한다.

FP16을 지정해도 모든 layer가 반드시 FP16이 되는 것은 아니다. `trtexec` 로그에서 fallback과 layer precision을 확인한다.

### 3. INT8을 적용한다

이 작은 MLP의 ONNX Runtime 동적 INT8 파일을 TensorRT에 그대로 넣는 것이 항상 최선은 아니다. TensorRT가 지원하는 Q/DQ graph를 export하거나 실제 운영 분포의 calibration cache를 사용한다.

순서:

1. 실제 센서 범위·상태·온도를 대표하는 calibration set을 고른다.
2. FP32/FP16 기준 정확도를 고정한다.
3. TensorRT 지원 Q/DQ export 또는 calibrator를 사용한다.
4. engine build log에서 INT8로 실행된 layer를 확인한다.
5. test set의 전체 정확도와 `stop_required` recall을 비교한다.
6. FP16/INT8의 p99, 전력, 온도를 같은 조건에서 비교한다.

### 4. Jetson 성능을 재현한다

```bash
# 현재 Jetson 전력 모드와 사용 가능한 모드를 확인한다.
sudo nvpmodel -q
# tegrastats는 GPU/CPU/RAM/온도/전력 상태를 실시간으로 보여 준다.
tegrastats
# 저장된 FP16 engine을 충분한 반복으로 실행해 latency와 throughput을 측정한다.
trtexec \
  --loadEngine=artifacts/sensor_model.fp16.engine \
  --warmUp=1000 \
  --duration=30
```

`jetson_clocks`와 전력 모드 변경은 성능과 발열에 영향을 준다. 팀 정책과 장치 열 설계를 확인하고, 사용한 설정을 보고서에 기록한다.

## 레시피 C: Intel CPU/GPU/NPU + OpenVINO

OpenVINO는 ONNX 모델을 직접 읽을 수 있다. 지원 장치 목록은 설치한 runtime과 driver에 따라 달라진다.

```bash
# 별도 가상환경에서 OpenVINO runtime과 도구를 설치한다.
python3 -m pip install openvino
# 사용 가능한 OpenVINO 장치와 benchmark_app 옵션을 확인한다.
benchmark_app --help
# CPU에서 batch 1 모델의 동기 추론 성능을 측정한다.
benchmark_app \
  -m artifacts/sensor_model.onnx \
  -d CPU \
  -shape "[1,4]" \
  -api sync
```

줄별 의미:

- `-m`: 읽을 ONNX/IR 모델 경로다.
- `-d CPU`: 실행 장치를 CPU로 고정한다. 지원되는 경우 `GPU`, `NPU`, `AUTO`를 별도로 비교한다.
- `-shape "[1,4]"`: dynamic 입력의 실제 shape를 고정한다.
- `-api sync`: 단일 요청 latency를 보기 쉬운 동기 API를 쓴다.

throughput 목표라면 async request 수와 stream을 조정할 수 있지만, 로봇의 단일 센서 frame deadline과 server batching 목표를 혼동하지 않는다.

## 레시피 D: Raspberry Pi/일반 ARM64 Linux

1. 보드가 `aarch64`인지 확인한다.
2. ARM64 ONNX Runtime 또는 해당 보드에 맞게 빌드한 runtime을 사용한다.
3. NEON과 thread 설정이 실제 build에 반영되었는지 확인한다.
4. swap에 기대지 않고 peak RSS를 측정한다.
5. fan 유무와 enclosure를 실제 제품 조건으로 맞춰 30분 이상 측정한다.

```bash
# uname은 kernel이 보고하는 CPU architecture를 표시한다.
uname -m
# lscpu는 core 수와 CPU 기능 정보를 표시한다.
lscpu
# time -v는 실행 시간과 최대 resident memory를 함께 보고한다.
/usr/bin/time -v \
  ./cpp/build/edge_infer artifacts/sensor_model.onnx 0.0 0.0 0.0 0.0
```

한 번 실행한 `time` 결과에는 process 시작과 모델 로드가 포함된다. steady-state 추론 latency는 process 안에서 session을 재사용하며 별도로 반복 측정한다.

## 레시피 E: MCU + LiteRT for Microcontrollers

MCU는 Linux SBC 실습의 단순 축소판이 아니다.

### 설계 전에 정할 예산

- flash: firmware + model + 상수
- SRAM: tensor arena + stack + 통신 buffer
- 한 inference의 cycle 수
- 센서 주기, duty cycle, 전력
- 지원 가능한 operator 목록

일반 흐름:

```text
작은 TensorFlow/Keras 모델
  → representative dataset
  → full integer quantization
  → .tflite FlatBuffer
  → operator compatibility 확인
  → xxd로 C byte array
  → firmware link
  → tensor arena peak 확인
  → 실제 MCU cycle/전력 측정
```

파일시스템이 없는 MCU에서 모델을 C 배열로 바꾸는 예:

```bash
# -i는 binary byte를 C 배열 initializer로 변환한다.
xxd -i sensor_model.tflite > sensor_model_data.cc
```

생성 배열은 가능하면 `const`로 두어 writable SRAM이 아니라 read-only flash 영역에 배치되게 한다. 실제 linker section은 toolchain과 보드 설정을 확인한다.

## 레시피 F: ROS 2와 rosbag 회귀 시험

### 1. 같은 입력을 기록한다

```bash
# -o 뒤 폴더에 센서 입력과 기준 결과 두 토픽을 기록한다.
ros2 bag record \
  -o bags/sensor-regression-v1 \
  /normalized_sensor_features \
  /reference_prediction
```

### 2. C++ 노드에 재생한다

```bash
# --clock은 bag의 simulated time을 제공하며 node의 use_sim_time 설정과 맞춰야 한다.
ros2 bag play bags/sensor-regression-v1 --clock
```

### 3. 자동 비교한다

- message timestamp 또는 sequence로 Python 기준 결과와 C++ 결과를 짝짓는다.
- class 일치율뿐 아니라 logits 최대 오차를 저장한다.
- callback latency, queue drop, 오래된 입력 폐기 수를 함께 기록한다.
- CI의 일반 PC 회귀와 실제 보드의 nightly hardware test를 구분한다.

## 레시피 G: Autoware/자율주행 스택에 추가한다

새 perception 모델을 바로 전체 차량에 넣지 않고 모듈 경계를 따라 진행한다.

1. 입력 topic, 좌표계, timestamp, calibration 계약을 문서화한다.
2. 독립 ROS 2 component로 model runner를 만든다.
3. 기존 message type과 launch parameter 규칙을 따른다.
4. 저장된 rosbag으로 기존 component와 결과를 비교한다.
5. perception만 켠 logging simulator로 검증한다.
6. CARLA/AWSIM 시나리오에서 날씨·조도·가림·센서 drop을 시험한다.
7. planning/control에는 결과를 쓰지 않는 shadow mode로 실제 센서 분포를 확인한다.
8. 안전 검토와 승인 뒤 제한된 ODD에서 canary 배포한다.
9. KPI 악화나 timeout 때 기존 component로 즉시 rollback한다.

Autoware의 모듈은 Vehicle, System, Map, Sensing, Localization, Perception, Planning, Control 등으로 나뉜다. AI 모델 파일은 대개 그중 한 component의 내부 구현이며, 전체 시스템 안전을 대신하지 않는다.

## 공통 실패 진단표

| 증상 | 먼저 확인할 것 | 흔한 원인 |
|---|---|---|
| Python은 맞고 C++은 틀림 | 한 건의 전처리 tensor byte 비교 | RGB/BGR, mean/std, dtype, layout |
| ONNX load 실패 | opset, unsupported op, runtime version | 새 exporter op, custom op |
| INT8 정확도 급락 | calibration 분포와 클래스별 activation | 대표성 부족, outlier, 잘못된 scale |
| INT8이 더 느림 | 실제 INT8 kernel/EP 배치 여부 | Q/DQ overhead, 작은 모델, 미지원 hardware |
| 첫 frame만 느림 | session build와 warm-up | lazy initialization, engine cache |
| p99만 큼 | thread, queue, thermal, memory allocation | CPU 경쟁, GC/allocator, throttling |
| ROS 메시지가 쌓임 | QoS depth와 callback 시간 | 동기 추론으로 executor 차단 |
| Jetson engine load 실패 | engine 생성 환경 | TensorRT/CUDA/GPU/JetPack 불일치 |
| 장시간 뒤 느려짐 | 온도·clock·전력 로그 | thermal throttling |

## 완료 기록 양식

```text
모델 버전:
ONNX SHA-256:
데이터 버전:
대상 보드:
OS/Kernel:
ROS 2:
Runtime/Driver:
전력 모드:
정확도/위험 클래스 recall:
p50/p95/p99:
peak RAM/VRAM:
30분 온도 범위:
실패 테스트:
rollback artifact:
승인자/일자:
```
