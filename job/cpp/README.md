# ONNX Runtime C++ 추론 실습

작성일: 2026-07-25

## 목표

`../03_advanced.ipynb`이 생성한 `sensor_model.onnx`를 C++에서 한 번 로드하고, 표준화가 끝난 네 개 센서 값을 추론한다. 이 최소 예제는 모델 로드, tensor 생성, `Run`, 출력 shape 검사, softmax, latency 측정까지 포함한다.

소유권·수명·RAII·move·condition variable·happens-before·undefined behavior·ROS executor까지 깊게 이해하려면 [CPP_MASTERCLASS.md](CPP_MASTERCLASS.md)를 먼저 또는 병행해서 읽는다.

## 사전 요구 사항

- Ubuntu x86_64 또는 ARM64
- CMake 3.20 이상
- C++17 컴파일러
- 대상 아키텍처용 ONNX Runtime C/C++ 배포 archive
- 먼저 완료한 `02_fine_tuning.ipynb`와 `03_advanced.ipynb`

[공식 C++ 시작 문서](https://onnxruntime.ai/docs/get-started/with-cpp.html)에서 대상 OS와 아키텍처에 맞는 archive 또는 빌드 방법을 확인한다. x86_64 archive를 ARM64에 복사하면 실행되지 않는다.

## 빌드

```bash
cd job/cpp
cmake -S . -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DONNXRUNTIME_ROOT=/opt/onnxruntime
cmake --build build --parallel
```

동적 라이브러리가 표준 검색 경로에 없다면 실습 shell에서만 경로를 추가한다.

```bash
export LD_LIBRARY_PATH=/opt/onnxruntime/lib:${LD_LIBRARY_PATH}
```

메모리와 undefined behavior 검사용 별도 build:

```bash
# 일반 Release 결과와 섞지 않도록 sanitizer 전용 build 폴더를 사용한다.
cmake -S . -B build-sanitize \
  -DCMAKE_BUILD_TYPE=Debug \
  -DONNXRUNTIME_ROOT=/opt/onnxruntime \
  -DEDGE_INFER_ENABLE_ASAN_UBSAN=ON \
  -DEDGE_INFER_WARNINGS_AS_ERRORS=ON
# instrumentation이 포함된 실행 파일을 빌드한다.
cmake --build build-sanitize --parallel
# 정상 입력과 의도적으로 잘못된 입력을 모두 실행해 sanitizer report를 확인한다.
./build-sanitize/edge_infer ../artifacts/sensor_model.onnx 0.0 0.0 0.0 0.0
```

ThreadSanitizer는 ASan과 별도 build/job으로 운영한다. 현재 단일 thread CLI보다 [latest-only worker](../labs/04_latest_only_worker.cpp)와 ROS multi-threaded 실습에 적용한다.

## 실행

네 입력은 원시 센서값이 아니라 `artifacts/metadata.json`의 mean과 std로 이미 표준화한 값이다.

```bash
./build/edge_infer ../artifacts/sensor_model.onnx 0.0 0.0 0.0 0.0
```

예상 출력 형태:

```text
input=sensor_features output=class_logits
class=1 label=warning
probabilities=0.012345,0.976543,0.011112
latency_us=123
```

확률과 시간은 학습 결과와 장치에 따라 달라진다.

## 핵심 문법과 수명주기

| 코드 요소 | 의미와 사용 이유 |
|---|---|
| `#include <...>` | header의 선언을 현재 번역 단위에 포함한다. |
| `std::array<float, 4>` | 특성 수가 컴파일 시점에 네 개로 고정된 연속 메모리다. |
| `const T&` | 객체를 복사하지 않고 읽기 전용 참조로 받는다. |
| `Ort::Env` | process 수준의 ONNX Runtime logging 환경이다. Session보다 오래 살아야 한다. |
| `Ort::SessionOptions` | graph optimization과 thread 정책을 Session 생성 전에 정한다. |
| `Ort::Session` | 모델을 읽고 최적화한 실행 객체다. 프레임마다 만들지 않는다. |
| `Ort::AllocatedStringPtr` | Runtime allocator가 만든 이름 문자열을 scope 종료 때 자동 해제한다. |
| `Ort::Value::CreateTensor<float>` | 기존 연속 float 메모리를 tensor view로 감싼다. 입력 배열은 `Run`이 끝날 때까지 살아 있어야 한다. |
| `session.Run(...)` | 이름과 tensor를 연결해 한 번의 추론을 실행한다. |
| `GetTensorData<float>()` | Runtime이 소유한 출력 주소를 읽는다. `Ort::Value`보다 오래 보관하면 안 된다. |
| RAII | 객체 scope가 끝날 때 destructor가 native 자원을 해제하도록 소유권을 묶는 C++ 패턴이다. |
| `std::chrono::steady_clock` | NTP나 사용자 시계 변경의 영향을 받지 않는 경과 시간 측정용 시계다. |
| `try`/`catch` | parsing·runtime 오류를 process crash 대신 명시적 exit code와 로그로 바꾼다. |

## Python과 결과 비교

동일한 표준화 입력을 `onnxruntime.InferenceSession`과 C++ 실행기에 넣고 logits 또는 확률을 비교한다. 단일 예제만 보지 말고 고정 test vector 수백 건을 CSV/binary로 저장해 CI에서 비교한다.

허용 오차 예:

- FP32 Python↔C++ logits 최대 절대 오차 `< 1e-5`
- INT8은 정확도 지표와 클래스별 recall 저하를 별도로 gate

## 제품 코드로 확장할 때

- 모델을 frame마다 로드하지 말고 process 또는 lifecycle configure 단계에서 한 번 로드한다.
- 입력·출력 이름과 shape를 시작 시 검사한다.
- 전처리는 metadata에서 읽고, 모델 checksum과 metadata version을 함께 검사한다.
- tensor buffer를 재사용해 hot path의 allocation을 줄인다.
- warm-up 후 수천 번 측정해 p50/p95/p99를 기록한다.
- timeout, stale input, NaN/Inf, Runtime exception의 fallback을 정의한다.
