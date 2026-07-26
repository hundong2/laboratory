# ROS 2 C++ 통합 실습

작성일: 2026-07-25

## 목표와 범위

이 패키지는 “이미 표준화된 float 특성 네 개”를 `normalized_sensor_features` 토픽으로 받아 ONNX Runtime 추론 후 클래스 번호를 `prediction` 토픽으로 발행한다.

교육 목적의 최소 예제이므로 실제 로봇에서는 다음을 바꿔야 한다.

- `Float32MultiArray` 대신 timestamp와 단위를 가진 전용 interface message
- metadata 기반 전처리와 model checksum 검사
- lifecycle node와 진단(diagnostic)
- callback을 막지 않는 worker 또는 component/executor 설계
- timeout, stale input, NaN/Inf, 반복 오류의 fallback

## workspace 구성

```bash
mkdir -p ~/edge_ws/src
cp -r job/ros2 ~/edge_ws/src/edge_ai_demo
cd ~/edge_ws
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -y
colcon build \
  --symlink-install \
  --cmake-args \
  -DCMAKE_BUILD_TYPE=Release \
  -DONNXRUNTIME_ROOT=/opt/onnxruntime
source install/setup.bash
```

메모리 오류와 undefined behavior를 찾는 개발용 빌드는 다음처럼 별도 workspace에서 수행한다. Sanitizer가 삽입된 실행 파일의 latency는 제품 성능 수치로 사용하지 않는다.

```bash
colcon build \
  --cmake-args \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DONNXRUNTIME_ROOT=/opt/onnxruntime \
  -DEDGE_AI_WARNINGS_AS_ERRORS=ON \
  -DEDGE_AI_ENABLE_ASAN_UBSAN=ON
```

data race를 찾을 때는 AddressSanitizer와 동시에 켜지 말고 별도 ThreadSanitizer 빌드를 운영한다. ROS 2나 vendor runtime 내부에서 나온 보고도 곧바로 무시하지 말고, 최소 재현과 suppression 근거를 함께 남긴다.

JetPack 6/Ubuntu 22.04에서 ROS 2 Humble을 사용한다면 source 경로를 `/opt/ros/humble/setup.bash`로 바꾼다. 보드 이미지와 ROS 배포판의 공식 호환성을 먼저 확인한다.

## 노드 실행

터미널 1:

```bash
source ~/edge_ws/install/setup.bash
export LD_LIBRARY_PATH=/opt/onnxruntime/lib:${LD_LIBRARY_PATH}
ros2 run edge_ai_demo edge_ai_node \
  --ros-args \
  -p model_path:=$PWD/job/artifacts/sensor_model.onnx
```

터미널 2에서 이미 표준화된 예제 입력을 한 번 발행한다.

```bash
source ~/edge_ws/install/setup.bash
ros2 topic pub --once \
  /normalized_sensor_features \
  std_msgs/msg/Float32MultiArray \
  "{data: [0.0, 0.0, 0.0, 0.0]}"
```

터미널 3에서 결과를 확인한다.

```bash
source ~/edge_ws/install/setup.bash
ros2 topic echo /prediction
```

## 코드 흐름

```text
ROS callback
  → 입력 길이 4 검사
  → std::array<float, 4>
  → Ort::Value tensor view
  → session.Run
  → 출력 shape 3 검사
  → argmax
  → std_msgs/Int32 발행
```

## QoS를 이해해야 하는 이유

`SensorDataQoS()`는 보통 최신 센서 샘플이 중요하고 일부 유실을 허용할 수 있는 흐름에 적합한 출발점이다. 그러나 제어 명령이나 이벤트는 같은 정책을 그대로 쓰면 안 된다.

- 카메라: 오래된 frame queue를 모두 처리하는 것보다 최신 frame을 처리하는 편이 나을 수 있다.
- 상태/명령: 전달 신뢰성과 이력 정책이 더 중요할 수 있다.
- 여러 센서 융합: timestamp와 동기화 정책이 필수다.

QoS는 publisher와 subscriber가 호환되어야 연결된다. `ros2 topic info -v`로 양쪽 정책을 확인한다.

## 실무 확장 순서

1. 센서 message에 `std_msgs/Header`와 단위를 추가한다.
2. metadata JSON에서 mean/std와 class map을 읽는다.
3. 입력 timestamp가 너무 오래되면 frame을 버린다.
4. inference worker queue 깊이를 1로 제한하고 최신 입력으로 덮어쓴다.
5. `ros2 bag play`로 Python 기준 노드와 C++ 노드에 같은 입력을 재생한다.
6. 클래스, logits, latency를 자동 비교한다.
7. lifecycle configure에서 모델을 검증하고 activate 후에만 결과를 발행한다.
8. diagnostic topic에 모델 버전, p99 latency, 오류율, drop 수를 노출한다.
9. 시뮬레이터와 hardware-in-the-loop를 통과한 뒤 shadow mode로 현장 검증한다.

## 안전 경고

이 예제의 `stop_required` 결과를 실제 brake/actuator에 직접 연결하지 않는다. 모델 오류, 센서 오류, 통신 지연을 독립적으로 감시하는 안전 계층과 시스템 수준의 hazard analysis가 필요하다.
