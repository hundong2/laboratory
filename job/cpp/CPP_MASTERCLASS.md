# C++ 초고수의 로보틱스 AI 코드 해설

작성일: 2026-07-26

대상: C++ 문법 입문자부터 ROS 2 subsystem owner까지

이 문서는 “코드가 무엇을 하는지”보다 “어떤 불변식이 코드를 안전하게 만드는지”를 전수한다. 주석은 번역기가 아니다. `i++`를 “i를 증가시킨다”라고만 설명하면 제품 지식이 남지 않는다. 좋은 주석은 다음을 설명한다.

1. 이 객체가 무엇을 소유하는가.
2. 이 pointer/reference는 언제까지 유효한가.
3. 복사하는가, view만 만드는가.
4. 어느 thread가 읽고 쓰는가.
5. 실패했을 때 어느 경계에서 containment하는가.
6. 이 숫자와 shape가 어떤 외부 contract에서 왔는가.
7. 더 빠르게 바꿀 때 깨질 수 있는 불변식은 무엇인가.

## 1. 이번 C++ 감사 결과

검토 대상:

- [main.cpp](main.cpp)
- [edge_ai_node.cpp](../ros2/src/edge_ai_node.cpp)
- [04_latest_only_worker.cpp](../labs/04_latest_only_worker.cpp)
- 두 CMake build 파일

발견하고 개선한 부분:

| 발견 | 위험 | 개선 |
|---|---|---|
| `const_cast`로 입력 tensor 생성 | 실제 const object를 runtime이 쓰면 undefined behavior 가능 | 입력 buffer를 의도적으로 mutable하게 소유 |
| 모델의 첫 입력/출력만 가정 | 잘못된 model도 load 후 frame 처리까지 진행 | 시작 시 count/dtype/rank/shape 검증 |
| `std::stof("nan")`, `std::stof("1.2abc")` 허용 가능 | NaN 오염 또는 잘못된 CLI token의 부분 변환 | 소비 문자 수와 `std::isfinite`를 모두 검사 |
| Windows path의 단순 byte→wide 변환 | 비ASCII 경로 손상 | `std::filesystem::path::c_str()` |
| ROS main의 생성자 예외 미처리 | model load 실패가 불명확한 process 종료 | process 경계 `try/catch`, fatal log, exit 1 |
| ROS callback의 일부 ONNX 객체가 `try` 밖에 있음 | `CreateTensor` 예외가 executor 경계로 탈출 | 첫 ORT 객체 생성부터 publish 직전까지 frame 단위 containment |
| callback이 mutable `SharedPtr`를 참조로 받음 | payload 변경 가능성과 비관용적 callback signature | 읽기 전용 `ConstSharedPtr`를 값으로 받아 수명을 공유 |
| worker count에 불필요한 atomic | 초보자가 “thread가 있으면 전부 atomic”으로 오해 | thread confinement와 `join` happens-before 사용 |
| Stop 이후 Push 허용 | 종료된 worker에 처리되지 않는 frame 저장 | `Push`가 `bool`로 거부를 알림 |
| p99 index 정의가 암묵적 | 작은 표본에서 percentile 의미 혼동 | nearest-rank `ceil(p*N)-1` 명시 |
| 기본 빌드 경고·Sanitizer 선택지가 없음 | narrowing, shadowing, UB가 review를 통과할 가능성 | target 단위 경고와 ASan/UBSan CI option 추가 |

## 2. 가장 중요한 C++ 질문: 누가 소유하는가

### 값 객체

```cpp
std::array<float, 4> input_values;
```

`input_values`는 네 float를 직접 소유한다. stack object라고 흔히 말하지만 C++ 표준의 본질은 automatic storage duration이다. scope를 벗어나면 destructor가 호출되고 storage lifetime이 끝난다.

### owning smart pointer

```cpp
std::unique_ptr<ModelRunner>
```

`unique_ptr`는 단일 소유자다. 복사할 수 없고 move할 수 있다. 수명과 파괴 시점을 가장 명확하게 표현하므로 기본 선택이다.

```cpp
std::shared_ptr<Node>
```

`shared_ptr`는 control block의 strong reference count가 0이 될 때 객체를 파괴한다. “편해서” 쓰지 않는다.

- reference count 갱신에 atomic 비용이 있을 수 있다.
- 마지막 owner가 어느 thread인지에 따라 destructor 실행 thread가 달라진다.
- cycle이 생기면 파괴되지 않는다.
- `weak_ptr`로 비소유 관계를 표현해야 할 수 있다.

ROS 2 node가 `shared_ptr`인 이유는 executor와 호출자가 node 수명을 공동 관리하기 때문이다.

### non-owning view

```cpp
const float* output_data = output.GetTensorData<float>();
```

이 pointer는 output memory를 소유하지 않는다. `Ort::Value output`이 파괴되거나 runtime buffer가 무효화되면 pointer도 dangling이 된다.

따라서 예제는 다음처럼 즉시 복사한다.

```cpp
std::vector<float> logits(output_data, output_data + output_count);
```

복사 비용이 싫어서 pointer를 member에 저장하면 수명 증명이 먼저 필요하다.

## 3. ONNX Runtime tensor의 수명

다음 코드는 입력을 복사하지 않는다.

```cpp
Ort::Value input_tensor = Ort::Value::CreateTensor<float>(
    memory_info,
    input_values.data(),
    input_values.size(),
    input_shape.data(),
    input_shape.size());
```

관계:

```text
input_values가 float memory를 소유
    ↑
input_tensor는 그 memory를 보는 tensor view
    ↑
session.Run은 호출 동안 view를 사용
```

필수 불변식:

- `input_values`는 `Run`이 끝날 때까지 살아 있다.
- vector를 쓴다면 `CreateTensor` 뒤에 resize/push_back해서 reallocation하지 않는다.
- element count와 shape 곱이 같다.
- model dtype과 C++ pointer element type이 같다.
- GPU memory를 넘기면 `MemoryInfo`도 실제 device와 일치해야 한다.

초판의 `const_cast<float*>`는 제거했다. C API가 mutable pointer를 요구한다고 실제 const object의 주소를 억지로 바꾸는 습관은 위험하다. API가 쓰지 않는다고 문서화되어 있어도, 처음부터 mutable buffer를 만드는 편이 의도가 정확하다.

## 4. RAII를 “자동 delete”보다 깊게 이해하기

RAII는 resource acquisition is initialization이다. resource의 유효 기간을 C++ 객체 lifetime과 묶는다.

예제:

- `Ort::Env`: ONNX Runtime 환경
- `Ort::Session`: native model/session
- `Ort::AllocatedStringPtr`: runtime allocator 문자열
- `std::lock_guard`: mutex 잠금
- `std::unique_lock`: condition wait가 unlock/relock할 수 있는 잠금
- `std::thread`: native thread handle

좋은 RAII의 효과:

- 모든 return/exception 경로에서 정리
- 소유권을 type으로 표현
- cleanup 호출 순서 감소

주의: `std::thread` destructor는 join을 자동 수행하지 않는다. joinable 상태로 destructor가 호출되면 `std::terminate`다. C++20에서는 `std::jthread`가 stop token과 자동 join을 제공한다. 이 과정은 C++17 호환을 위해 명시적으로 `join()`한다.

## 5. 선언 순서가 파괴 순서다

class member는 initializer list에 적은 순서가 아니라 class에 선언된 순서로 생성된다. 파괴는 역순이다.

ROS node:

```text
environment_
session_options_
session_
input_name_
output_name_
subscription/publisher
```

`session_`은 `environment_`를 사용하므로 environment가 먼저 생성되고 session보다 나중에 파괴되어야 한다. 현재 선언 순서가 그 불변식을 지킨다.

compiler warning `-Wreorder`를 켜는 이유가 이것이다. initializer list만 읽고 안심하면 안 된다.

## 6. `const`를 정확히 사용한다

```cpp
const std::vector<float>& logits
```

- reference: vector 전체 복사를 피한다.
- `const`: 함수가 vector 원소를 바꾸지 않는다는 contract다.

```cpp
const float* output_data
```

- pointer가 가리키는 float를 이 pointer로 수정하지 않는다.
- pointer 변수 자체는 다른 주소로 바꿀 수 있다.

```cpp
float* const pointer
```

- pointer 주소는 고정이지만 가리키는 float는 바꿀 수 있다.

```cpp
const float* const pointer
```

- 주소와 가리키는 값 모두 이 이름을 통해 바꾸지 않는다.

`const`는 thread safety가 아니다. 다른 alias가 같은 object를 수정할 수 있다.

## 7. 복사와 move

latest-only queue는 다음 signature를 쓴다.

```cpp
bool Push(Frame frame);
```

by-value를 쓰는 이유:

- lvalue caller는 한 번 복사해 함수가 독립 소유한다.
- rvalue caller는 move construction할 수 있다.
- 함수 안에서 `std::move(frame)`으로 storage에 옮길 수 있다.

`std::move`는 실제 이동 연산이 아니다. 객체를 rvalue로 cast한다. 실제 resource transfer는 대상 type의 move constructor/assignment가 수행한다.

현재 `Frame`은 숫자와 `time_point`뿐이라 복사도 싸다. image buffer라면 `shared_ptr<const Image>` 또는 pool handle 같은 소유권 설계를 별도로 해야 한다.

## 8. condition variable을 올바르게 기다린다

잘못된 형태:

```cpp
condition.wait(lock);
use(data);
```

condition variable은 이유 없이 깨어나는 spurious wakeup이 허용된다. 올바른 형태:

```cpp
condition.wait(lock, [this] {
  return stopped_ || latest_.has_value();
});
```

predicate가 true일 때만 wait를 빠져나온다.

또한 상태 변경과 predicate 검사는 같은 mutex 아래에서 이루어져야 lost wakeup과 data race를 막을 수 있다.

notify는 lock을 해제한 뒤 호출했다. 반드시 그래야 하는 것은 아니지만, 깨어난 thread가 곧바로 같은 mutex에서 막히는 일을 줄인다.

## 9. happens-before와 불필요한 atomic

worker만 `processed`와 `ages_ms`를 쓴다. main은 `worker.join()` 뒤에 읽는다.

`join()`은 worker 완료와 join 이후 main 사이에 synchronization을 만든다. worker의 write는 main read보다 happens-before다. 따라서 일반 `std::size_t`와 vector로 충분하다.

atomic이 필요한 예:

- worker 실행 중 다른 thread가 count를 동시에 읽음
- lock 없이 여러 worker가 같은 count를 증가

atomic도 복합 불변식을 자동 보호하지 않는다.

```cpp
if (count.load() > 0) {
  use(queue.front());
}
```

count와 queue가 같은 상태를 나타내야 한다면 mutex 또는 더 엄밀한 lock-free algorithm이 필요하다.

## 10. memory order를 함부로 낮추지 않는다

`memory_order_relaxed`는 “빠른 atomic” 옵션이 아니다. 해당 atomic 변수 자체의 원자성만 보장하며 다른 memory write의 ordering을 전달하지 않는다.

stop flag와 buffer publish를 lock-free로 구현하면서 relaxed만 사용하면 consumer가 새 flag와 오래된 buffer를 볼 수 있다. acquire/release와 object lifetime을 증명할 수 없다면 mutex가 더 안전하고 종종 충분히 빠르다.

## 11. exception 경계를 설계한다

예제는 세 경계를 둔다.

1. CLI `main`: parsing/model/runtime 오류 → stderr + exit 1
2. ROS callback: 한 frame runtime 오류 → 해당 frame 폐기 + ROS error log
3. ROS process `main`: node 생성/spin 오류 → fatal log + shutdown + exit 1

제품에서 모든 예외를 무조건 계속 처리하면 안 된다.

- recoverable: invalid frame, 일시적 timeout
- restartable: runtime context 손상, GPU reset
- fatal configuration: checksum/shape/class map 불일치

callback에서 같은 fatal 오류를 무한 반복 로그로 남기는 대신 circuit breaker, lifecycle error 전환, supervisor restart를 사용한다.

real-time hot path에서는 exception의 worst-case 비용과 library 정책을 검토한다. 일부 조직은 해당 경로에서 exception을 금지하고 `expected`/status code를 사용한다.

## 12. undefined behavior를 경계한다

대표 사례:

- dangling pointer/reference
- out-of-bounds
- signed integer overflow
- data race
- 잘못된 type pointer로 memory 읽기
- 실제 const object 수정
- 초기화하지 않은 값 읽기
- lifetime이 시작되지 않은 storage를 object로 사용

undefined behavior는 “예외가 발생한다”가 아니다. compiler가 그런 상황은 없다고 가정해 예상 밖 최적화를 할 수 있다.

도구:

```bash
-fsanitize=address,undefined
-fsanitize=thread
clang-tidy
```

ASan/UBSan과 TSan은 보통 같은 실행 파일에 함께 넣지 않고 별도 CI job으로 운영한다.

## 13. shape 검증이 곧 memory safety다

다음 값은 함께 맞아야 한다.

```text
model input dtype = float32
C++ pointer type = float*
buffer elements = 4
runtime shape = [1, 4]
model declared shape = [batch, 4]
```

“ONNX Runtime이 알아서 오류를 내겠지”에 기대지 않는다. 잘못된 custom operator나 native integration에서는 shape 오류가 memory corruption으로 확대될 수 있다.

현재 코드는 session 생성 직후 다음을 확인한다.

- input/output 각 1개
- float32
- input `[dynamic-or-1, 4]`
- output `[batch, 3]`

frame마다 변하지 않는 것은 시작 때 한 번, 실제 runtime output과 유한성은 frame 경계에서 다시 확인한다.

## 14. softmax와 argmax

softmax는 수치 안정성을 위해 최대 logit을 뺀다.

```text
softmax_i = exp(logit_i - max_logit) / Σ exp(logit_j - max_logit)
```

최대값을 빼도 class 순서는 변하지 않는다.

ROS node는 class index만 필요하므로 softmax 없이 logits의 argmax를 쓴다. CLI는 사람이 확률을 보도록 softmax를 계산한다.

주의:

- logits가 calibration된 확률이라는 뜻은 아니다.
- NaN이 있으면 일반 비교가 모두 false가 될 수 있다.
- threshold가 필요하면 softmax와 model calibration을 검증한다.

## 15. ROS executor와 thread safety

현재 node는 기본 callback group을 사용한다. 기본 group은 `MutuallyExclusive`이므로 동일 group callback은 동시에 실행되지 않는다.

다음 변경은 동시성 검토를 다시 요구한다.

- Reentrant callback group
- MultiThreadedExecutor에 여러 group
- service로 model hot-swap
- timer와 subscription이 같은 session/buffer 사용
- 여러 camera가 같은 node를 호출

ONNX Runtime Session이 concurrent Run을 지원하더라도 다음은 별개다.

- input/output buffer가 호출별로 독립인가
- execution provider와 custom op가 thread-safe인가
- GPU stream과 allocator가 공유되는가
- 결과 순서와 timestamp pairing이 유지되는가

“library가 thread-safe”와 “우리 algorithm이 thread-safe”를 구분한다.

## 16. lock scope와 logging

mutex를 잡은 채 다음을 하지 않는다.

- inference
- file/network I/O
- blocking ROS publish
- 대량 log format
- callback 호출

latest-only queue는 shared state 복사/이동만 lock 안에서 하고 notify와 inference는 밖에서 한다.

실시간 경로의 log는 allocation, format, lock, disk I/O를 유발할 수 있다. 반복 오류는 throttle하고 counter/diagnostic으로 집계한다.

## 17. false sharing과 cache

여러 thread가 서로 다른 atomic counter를 갱신해도 같은 cache line에 있으면 core 사이 cache invalidation이 반복될 수 있다. 이를 false sharing이라 한다.

고주기 telemetry counter는:

- thread-local 누적 후 주기적 merge
- `alignas(std::hardware_destructive_interference_size)` 검토
- 측정으로 실제 병목 확인

작은 교육 예제에 무조건 padding을 넣지는 않는다. 복잡도는 profiler evidence가 있을 때 추가한다.

## 18. CMake build type을 이해한다

- Debug: 보통 `-O0 -g`, 디버깅
- RelWithDebInfo: 최적화와 symbol, profiling
- Release: 최적화된 성능 측정

latency는 Debug build로 승인하지 않는다. 반대로 Release만 돌리면 memory 오류를 늦게 찾는다.

권장 CI matrix:

```text
Debug + ASan/UBSan
Debug 또는 별도 build + TSan
Release + unit/integration
RelWithDebInfo + profiler
target hardware Release + soak
```

## 19. 주석 품질 규칙

유지할 주석:

- 수명과 소유권
- thread/lock 불변식
- 단위, frame, shape, dtype
- failure policy
- requirement/hazard 근거
- platform/library의 놀라운 동작

줄일 주석:

- 코드와 완전히 같은 말을 반복
- 변경 이력을 서술
- 오래된 TODO
- 구현과 어긋난 설명

교육 코드에는 문법 설명을 많이 남겼다. 제품 코드에서는 이 문서와 onboarding 자료로 문법 설명을 옮기고, source에는 “왜”와 불변식을 중심으로 유지한다.

## 20. 코드 리뷰 체크리스트

- [ ] 모든 raw pointer/reference의 owner와 lifetime을 말할 수 있는가?
- [ ] vector/string reallocation 뒤 pointer를 보관하지 않는가?
- [ ] member 선언 순서와 dependency가 일치하는가?
- [ ] move 후 객체를 잘못 사용하지 않는가?
- [ ] callback 동시 실행 가능성을 명시했는가?
- [ ] shared state가 mutex 또는 증명된 atomic protocol 아래 있는가?
- [ ] condition variable에 predicate가 있는가?
- [ ] hot path allocation/I/O/log/lock 시간이 bounded인가?
- [ ] dtype, shape, element count를 native pointer 사용 전에 검사하는가?
- [ ] NaN/Inf와 stale timestamp를 거부하는가?
- [ ] 예외가 frame, node, process 중 올바른 경계에서 처리되는가?
- [ ] sanitizer와 Release benchmark가 모두 있는가?

## 21. 실습 과제

### 과제 A: dangling pointer 만들고 잡기

지역 vector의 `data()`를 반환하는 잘못된 함수를 작성하고 ASan으로 실패를 관찰한다. 수정본은 vector 자체를 값으로 반환하거나 owner가 살아 있는 scope에서 span/view를 사용한다.

### 과제 B: data race 만들고 잡기

latest-only worker의 `processed`를 producer도 동시에 수정하게 만들고 TSan 결과를 본다. mutex, atomic, thread confinement 세 해결책의 의미와 비용을 비교한다.

### 과제 C: model contract 파괴

- class 4개 model
- input `float64`
- input shape `[1, 5]`
- NaN logits model

각 model이 callback 전 또는 frame 경계에서 거부되는지 확인한다.

### 과제 D: executor concurrency

Reentrant callback group과 두 subscription으로 바꾸고 동시 Run을 trace한다. shared buffer를 일부러 추가해 TSan 실패를 만든 뒤 호출별 buffer 또는 pool로 수정한다.

### 과제 E: allocation 제거

frame마다 생성하는 input/output container를 preallocated runner member로 옮긴다. 최적화 전후 p99와 allocation count를 측정한다. 빨라졌다는 가정이 아니라 수치로 결론을 낸다.
