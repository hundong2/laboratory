// array는 모델의 고정 입력 shape와 이름 포인터 배열에 사용한다.
#include <array>
// cmath는 sensor와 runtime 출력의 NaN/Inf를 검사하는 std::isfinite를 제공한다.
#include <cmath>
// cstddef는 tensor 원소 수와 message 길이의 std::size_t를 명시한다.
#include <cstddef>
// cstdint는 ROS 출력의 고정 폭 정수와 ONNX shape의 int64_t를 명확히 한다.
#include <cstdint>
// exception은 node 생성과 spin 경계에서 std::exception을 처리한다.
#include <exception>
// functional은 subscription callback을 연결하는 std::bind를 제공한다.
#include <functional>
// memory는 node와 publisher의 std::shared_ptr 소유권 타입을 제공한다.
#include <memory>
// stdexcept는 모델 계약 위반을 나타내는 예외 타입을 제공한다.
#include <stdexcept>
// string은 model_path parameter 값을 소유한다.
#include <string>
// vector는 runtime이 반환하는 출력 tensor 목록을 보관한다.
#include <vector>

// ONNX Runtime C++ RAII API를 포함한다.
#include <onnxruntime_cxx_api.h>
// rclcpp는 ROS 2 C++ Node, QoS, logging, spin API를 제공한다.
#include <rclcpp/rclcpp.hpp>
// Int32는 예측 클래스 번호를 발행하는 최소 예제 메시지다.
#include <std_msgs/msg/int32.hpp>
// Float32MultiArray는 이미 표준화된 센서 특성 네 개를 받는 예제 메시지다.
#include <std_msgs/msg/float32_multi_array.hpp>

// placeholders::_1은 std::bind가 ROS callback의 첫 인수를 전달하게 한다.
using std::placeholders::_1;

// rclcpp::Node를 상속하면 parameter, subscription, publisher, logger를 사용할 수 있다.
class EdgeAiNode final : public rclcpp::Node {
 public:  // ROS main이 생성자를 호출해야 하므로 construction API만 공개한다.
  // 생성자에서 모델과 ROS 통신 객체를 한 번 준비한다.
  EdgeAiNode()
      // 부모 Node의 이름을 edge_ai_node로 등록한다.
      : Node("edge_ai_node"),
        // ONNX Runtime process 환경을 경고 로그 수준으로 만든다.
        environment_(ORT_LOGGING_LEVEL_WARNING, "edge-ai-node"),
        // session_은 model_path를 읽은 뒤 본문에서 대입하므로 처음에는 null이다.
        session_(nullptr) {
    // model_path parameter를 선언하고 기본값을 빈 문자열로 둔다.
    const std::string model_path =
        this->declare_parameter<std::string>("model_path", "");
    // 빈 경로로는 안전하게 시작할 수 없으므로 configure 단계에서 실패시킨다.
    if (model_path.empty()) {
      // invalid_argument는 launch 파일의 필수 parameter 누락을 명확히 나타낸다.
      throw std::invalid_argument("required parameter 'model_path' is empty");
    }
    // 작은 모델의 intra-op thread를 하나로 제한해 latency 변동을 줄인다.
    session_options_.SetIntraOpNumThreads(1);
    // 가능한 graph optimization을 모두 활성화한다.
    session_options_.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);
    // Linux ROS 2 환경의 char 경로로 모델을 한 번 로드한다.
    session_ = Ort::Session(environment_, model_path.c_str(), session_options_);
    // callback을 등록하기 전에 입력/출력 개수·dtype·shape를 모두 검사한다.
    ValidateModelContract();
    // 기본 allocator로 runtime 입력·출력 이름의 메모리를 관리한다.
    Ort::AllocatorWithDefaultOptions allocator;
    // 첫 입력 이름을 소유하는 RAII 포인터를 member에 저장한다.
    input_name_ = session_.GetInputNameAllocated(0, allocator);
    // 첫 출력 이름도 node 수명 동안 유지한다.
    output_name_ = session_.GetOutputNameAllocated(0, allocator);
    // 예측 클래스 번호를 depth 10의 기본 reliable QoS로 발행한다.
    prediction_publisher_ =
        // template 인수는 compile time ROS message type이다.
        this->create_publisher<std_msgs::msg::Int32>("prediction", 10);
    // SensorDataQoS는 최신 센서 데이터 우선의 best-effort, 작은 queue 정책이다.
    sensor_subscription_ =
        this->create_subscription<std_msgs::msg::Float32MultiArray>(
            // 첫 인수는 node namespace 기준 topic 이름이다.
            "normalized_sensor_features",
            // 둘째 인수는 sensor stream에 맞춘 best-effort QoS profile이다.
            rclcpp::SensorDataQoS(),
            // 셋째 인수는 수신 message를 이 객체의 member 함수에 전달한다.
            std::bind(&EdgeAiNode::OnSensorFeatures, this, _1));
    // 시작 로그에 모델 경로를 남겨 어떤 artifact가 로드됐는지 확인하게 한다.
    RCLCPP_INFO(this->get_logger(), "loaded model: %s", model_path.c_str());
  }

 private:  // callback과 native resource는 외부가 임의 호출·변경하지 못하게 숨긴다.
  // Session 생성 직후 한 번 호출하므로 frame hot path에 반복 검증 비용을 넣지 않는다.
  void ValidateModelContract() const {
    // 예제 node는 하나의 feature tensor만 처리한다.
    if (session_.GetInputCount() != 1) {
      // 다른 model을 실수로 지정했을 때 node activation 전에 실패한다.
      throw std::runtime_error("model must expose exactly one input");
    }
    // 예제 node는 하나의 logits tensor만 처리한다.
    if (session_.GetOutputCount() != 1) {
      // 여러 출력 중 첫 번째를 임의 선택하지 않는다.
      throw std::runtime_error("model must expose exactly one output");
    }
    // 첫 입력 tensor의 element type과 선언 shape를 읽는다.
    const Ort::TensorTypeAndShapeInfo input_info =
        session_.GetInputTypeInfo(0).GetTensorTypeAndShapeInfo();
    // input_values.data()를 float pointer로 넘기므로 model dtype도 float32여야 한다.
    if (input_info.GetElementType() != ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT) {
      // implicit conversion을 기대하지 않고 artifact 계약을 거부한다.
      throw std::runtime_error("model input dtype must be float32");
    }
    // dynamic batch는 -1, feature 축은 고정 4인 [batch, 4] shape를 기대한다.
    const std::vector<std::int64_t> input_shape = input_info.GetShape();
    // OR의 short-circuit로 rank가 다르면 존재하지 않는 두 번째 축을 읽지 않는다.
    if (input_shape.size() != 2 || input_shape[1] != 4) {
      // 잘못된 shape에서 native memory를 해석하는 오류를 방지한다.
      throw std::runtime_error("model input shape must be [batch, 4]");
    }
    // 고정 batch model이라면 이 node가 만드는 batch 1과 일치해야 한다.
    if (input_shape[0] != -1 && input_shape[0] != 1) {
      // batch 8 전용 model에 네 float만 전달하지 않게 한다.
      throw std::runtime_error("model input batch must be dynamic or 1");
    }
    // 출력 tensor 계약도 시작 단계에서 확인한다.
    const Ort::TensorTypeAndShapeInfo output_info =
        session_.GetOutputTypeInfo(0).GetTensorTypeAndShapeInfo();
    // GetTensorData<float>()를 사용하기 전에 output dtype을 고정한다.
    if (output_info.GetElementType() != ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT) {
      // int label이나 quantized byte tensor를 float logits로 오해하지 않는다.
      throw std::runtime_error("model output dtype must be float32");
    }
    // 출력은 [batch, 3 classes]여야 prediction index 의미가 맞는다.
    const std::vector<std::int64_t> output_shape = output_info.GetShape();
    // class 축이 세 개인 2차원 tensor인지 검사한다.
    if (output_shape.size() != 2 || output_shape[1] != 3) {
      // class map이 다른 model을 조용히 발행하는 것을 막는다.
      throw std::runtime_error("model output shape must be [batch, 3]");
    }
    // output batch 축도 dynamic 또는 이 node가 처리하는 고정 1이어야 한다.
    if (output_shape[0] != -1 && output_shape[0] != 1) {
      // 여러 frame 결과를 단일 prediction message로 잘못 축약하지 않는다.
      throw std::runtime_error("model output batch must be dynamic or 1");
    }
  }

  // ConstSharedPtr은 payload를 읽기 전용으로 만들어 callback 안의 우발적 변경을 막는다.
  // smart pointer 자체는 값으로 받는다. 이 형태가 rclcpp의 표준 callback signature이며,
  // callback 실행이 끝날 때까지 message 수명을 명시적으로 공유한다.
  void OnSensorFeatures(
      std_msgs::msg::Float32MultiArray::ConstSharedPtr message) {
    // 모델 계약은 정확히 네 개의 이미 표준화된 float 입력이다.
    if (message->data.size() != 4) {
      // throttle을 쓰지 않은 최소 예제이므로 제품에서는 반복 오류 로그를 제한해야 한다.
      RCLCPP_ERROR(
          this->get_logger(),
          "expected 4 normalized features, got %zu",
          message->data.size());
      // 잘못된 입력을 모델에 전달하지 않고 callback을 즉시 끝낸다.
      return;
    }
    // model에 전달하기 전 모든 feature가 유한한지 검사한다.
    for (const float value : message->data) {
      // NaN/Inf는 비교와 argmax를 오염시켜 임의 class를 만들 수 있다.
      if (!std::isfinite(value)) {
        // invalid frame 한 건을 버리고 runtime은 호출하지 않는다.
        RCLCPP_ERROR(this->get_logger(), "rejected non-finite sensor feature");
        // callback을 종료해 잘못된 tensor가 downstream으로 가지 않게 한다.
        return;
      }
    }
    // 첫 Ort 객체 생성부터 publish 직전까지를 frame 단위 오류 경계로 감싼다.
    // CreateTensor도 잘못된 shape나 provider 상태에서 예외를 던질 수 있기 때문이다.
    try {
      // ONNX shape는 batch 1과 특성 4의 64비트 정수 배열이다.
      const std::array<std::int64_t, 2> input_shape = {1, 4};
      // CreateTensor에 전달할 연속 float 입력을 ROS message에서 복사한다.
      std::array<float, 4> input_values = {
          // index 0은 metadata의 vibration과 같은 순서여야 한다.
          message->data[0],
          // index 1은 temperature_delta다.
          message->data[1],
          // index 2는 current다.
          message->data[2],
          // index 3은 rotation_error다.
          message->data[3],
      };
      // CPU arena allocator가 관리하는 일반 메모리 정보를 만든다.
      const Ort::MemoryInfo memory_info =
          Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
      // callback scope의 input_values를 복사 없는 tensor view로 감싼다.
      Ort::Value input_tensor = Ort::Value::CreateTensor<float>(
          // CPU memory 종류를 설명한다.
          memory_info,
          // std::array가 소유한 연속 float 네 개의 시작 주소다.
          input_values.data(),
          // byte 수가 아니라 float element 수 4다.
          input_values.size(),
          // [1, 4] shape 배열의 시작 주소다.
          input_shape.data(),
          // tensor rank는 2다.
          input_shape.size());
      // Run이 요구하는 입력 이름 C 문자열 배열을 만든다.
      const std::array<const char*, 1> input_names = {input_name_.get()};
      // 요청할 출력 이름 C 문자열 배열을 만든다.
      const std::array<const char*, 1> output_names = {output_name_.get()};
      // 한 건의 동기 추론을 실행하고 출력 Ort::Value 목록을 받는다.
      std::vector<Ort::Value> outputs = session_.Run(
          // terminate flag와 run tag가 없는 기본 RunOptions다.
          Ort::RunOptions{nullptr},
          // 입력 이름 pointer 배열이다.
          input_names.data(),
          // 입력 tensor 한 개의 주소다.
          &input_tensor,
          // 입력 개수는 1이다.
          1,
          // 요청할 출력 이름 pointer 배열이다.
          output_names.data(),
          // 출력 개수도 1이다.
          1);
      // 방어적으로 반환 vector와 tensor 여부를 다시 검사한다.
      if (outputs.empty() || !outputs.front().IsTensor()) {
        // startup contract가 맞아도 runtime/provider 오류는 frame 경계에서 처리한다.
        throw std::runtime_error("runtime did not return the expected tensor");
      }
      // 첫 출력의 전체 원소 수가 세 클래스인지 확인한다.
      const std::size_t output_count =
          outputs.front().GetTensorTypeAndShapeInfo().GetElementCount();
      // 잘못된 모델 파일을 조용히 읽지 않도록 계약 위반을 예외로 바꾼다.
      if (output_count != 3) {
        // runtime_error가 아래 catch에서 ROS 오류 로그로 변환된다.
        throw std::runtime_error("model output does not contain 3 logits");
      }
      // 첫 tensor의 읽기 전용 float 메모리 주소를 얻는다.
      const float* logits = outputs.front().GetTensorData<float>();
      // 세 logits 중 NaN/Inf가 하나라도 있으면 예측을 발행하지 않는다.
      for (std::size_t index = 0; index < output_count; ++index) {
        // isfinite는 NaN과 양/음의 무한대를 모두 False로 판정한다.
        if (!std::isfinite(logits[index])) {
          // output corruption을 아래 catch가 한 frame 오류로 containment하게 한다.
          throw std::runtime_error("runtime returned a non-finite logit");
        }
      }
      // 첫 클래스를 현재 최고 클래스의 시작값으로 둔다.
      std::size_t predicted_index = 0;
      // 남은 두 클래스 logits를 첫 클래스와 비교한다.
      for (std::size_t index = 1; index < output_count; ++index) {
        // 더 큰 logit은 softmax 뒤에도 더 큰 확률이므로 softmax 계산을 생략할 수 있다.
        if (logits[index] > logits[predicted_index]) {
          // 최고 클래스 번호를 현재 index로 갱신한다.
          predicted_index = index;
        }
      }
      // 발행할 기본 Int32 message 객체를 만든다.
      std_msgs::msg::Int32 prediction_message;
      // 세 클래스 index는 int32 범위 안임을 계약 검증했으므로 명시적으로 변환한다.
      prediction_message.data = static_cast<std::int32_t>(predicted_index);
      // prediction topic으로 결과를 발행한다.
      prediction_publisher_->publish(prediction_message);
    // Ort와 표준 예외 모두 std::exception 기반이므로 한 catch에서 메시지를 읽는다.
    } catch (const std::exception& error) {
      // 오류를 기록하고 이 frame만 버린다; 제품에서는 오류 횟수와 fallback도 관리한다.
      RCLCPP_ERROR(this->get_logger(), "inference failed: %s", error.what());
    }
  }

  // environment_는 session_보다 먼저 생성되고 나중에 파괴되어야 한다.
  Ort::Env environment_;
  // session_options_는 session 생성 설정을 소유한다.
  Ort::SessionOptions session_options_;
  // session_은 모델과 native 추론 자원을 node 수명 동안 소유한다.
  Ort::Session session_;
  // input_name_은 Run 호출마다 사용할 입력 이름 메모리를 소유한다.
  Ort::AllocatedStringPtr input_name_{nullptr};
  // output_name_은 Run 호출마다 사용할 출력 이름 메모리를 소유한다.
  Ort::AllocatedStringPtr output_name_{nullptr};
  // sensor_subscription_은 subscription이 생성 직후 파괴되지 않게 소유한다.
  rclcpp::Subscription<std_msgs::msg::Float32MultiArray>::SharedPtr sensor_subscription_;
  // prediction_publisher_는 결과 topic publisher를 소유한다.
  rclcpp::Publisher<std_msgs::msg::Int32>::SharedPtr prediction_publisher_;
};

// main은 ROS 2 process의 진입점이다.
int main(int argc, char* argv[]) {
  // init은 ROS argument, logging, middleware 전역 상태를 초기화한다.
  rclcpp::init(argc, argv);
  // node 생성, model load, executor 실행 예외를 process 경계에서 한 번 더 처리한다.
  try {
    // make_shared는 node와 rclcpp executor 사이의 공유 수명을 관리한다.
    const auto node = std::make_shared<EdgeAiNode>();
    // 기본 callback group은 MutuallyExclusive이므로 같은 node callback은 직렬 실행된다.
    // Reentrant group이나 여러 executor thread로 바꾸면 Session/backend 동시 실행도 재검증한다.
    rclcpp::spin(node);
    // 정상 종료 전에 middleware와 전역 ROS resource를 정리한다.
    rclcpp::shutdown();
    // 정상 process 종료 상태 0을 반환한다.
    return 0;
  // 생성자와 spin에서 전파된 표준 예외를 process crash 메시지보다 명확한 fatal log로 바꾼다.
  } catch (const std::exception& error) {
    // 독립 logger는 EdgeAiNode 생성이 실패했어도 사용할 수 있다.
    RCLCPP_FATAL(rclcpp::get_logger("edge_ai_node_main"), "%s", error.what());
    // 예외 경로에서도 ROS 전역 resource를 정리한다.
    rclcpp::shutdown();
    // non-zero exit code로 supervisor가 실패와 restart policy를 판단하게 한다.
    return 1;
  }
}
