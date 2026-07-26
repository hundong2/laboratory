// array는 입력 shape처럼 길이가 컴파일 시점에 고정된 값을 안전하게 보관한다.
#include <array>
// chrono는 시스템 시계 변경의 영향을 받지 않는 추론 경과 시간을 측정한다.
#include <chrono>
// cmath는 softmax에서 지수 함수 std::exp를 제공한다.
#include <cmath>
// cstddef는 배열 크기와 인덱스에 쓰는 std::size_t를 정의한다.
#include <cstddef>
// cstdint는 ONNX tensor shape의 고정 폭 정수 std::int64_t를 제공한다.
#include <cstdint>
// exception은 std::exception 기반 오류 메시지를 처리한다.
#include <exception>
// filesystem::path는 Windows wide path와 Linux byte path 차이를 표준 방식으로 감싼다.
#include <filesystem>
// iomanip은 소수점 출력 자릿수를 정하는 std::setprecision을 제공한다.
#include <iomanip>
// iostream은 표준 출력 std::cout과 오류 출력 std::cerr를 제공한다.
#include <iostream>
// stdexcept는 잘못된 입력에 던질 std::runtime_error를 제공한다.
#include <stdexcept>
// string은 모델 경로와 입력 문자열을 소유하는 std::string을 제공한다.
#include <string>
// vector는 runtime에 따라 길이가 정해지는 출력 tensor를 보관한다.
#include <vector>

// onnxruntime_cxx_api.h는 C API를 RAII 객체로 감싼 ONNX Runtime C++ 인터페이스다.
#include <onnxruntime_cxx_api.h>

// 익명 namespace는 이 파일 안에서만 쓰는 함수가 다른 번역 단위와 충돌하지 않게 한다.
namespace {

// CLI token 하나를 문자열 전체가 유한한 float일 때만 받아들인다.
float ParseFiniteFloat(const char* text, const char* field_name) {
  // std::string은 길이 확인과 오류 메시지 생성을 위해 token을 소유한다.
  const std::string token(text);
  // stof가 실제로 소비한 문자 수를 받아 "1.2abc" 같은 부분 parsing을 막는다.
  std::size_t consumed = 0;
  // stof는 형식 오류와 범위 초과를 예외로 알리며 main의 오류 경계가 이를 처리한다.
  const float value = std::stof(token, &consumed);
  // token 끝까지 소비하지 않았다면 숫자 뒤에 잘못된 문자가 붙은 것이다.
  if (consumed != token.size()) {
    // field 이름과 원문을 함께 보여 CLI 입력 오류를 즉시 찾게 한다.
    throw std::runtime_error(
        std::string(field_name) + " is not a complete float: " + token);
  }
  // stof는 구현에 따라 "nan"과 "inf"를 정상 변환하므로 별도로 거부한다.
  if (!std::isfinite(value)) {
    // 센서 계약은 모든 feature가 유한한 실수라는 뜻이다.
    throw std::runtime_error(std::string(field_name) + " must be finite");
  }
  // 문법·범위·유한성 검사를 모두 통과한 값을 반환한다.
  return value;
}

// Session 생성 직후 한 번 호출해 잘못된 model을 실제 frame 처리 전에 거부한다.
void ValidateModelContract(const Ort::Session& session) {
  // 이 교육 model은 입력 tensor 하나만 허용한다; 여러 입력이면 metadata/code가 맞지 않는다.
  if (session.GetInputCount() != 1) {
    // model 교체 오류를 시작 단계에서 발견하도록 실제 개수를 메시지에 포함한다.
    throw std::runtime_error(
        "expected exactly 1 input, got " + std::to_string(session.GetInputCount()));
  }
  // 출력도 class logits tensor 하나만 허용한다.
  if (session.GetOutputCount() != 1) {
    // 첫 출력만 조용히 사용하는 대신 contract 불일치를 즉시 실패시킨다.
    throw std::runtime_error(
        "expected exactly 1 output, got " + std::to_string(session.GetOutputCount()));
  }
  // GetTensorTypeAndShapeInfo는 첫 입력의 element type과 선언 shape를 제공한다.
  const Ort::TensorTypeAndShapeInfo input_info =
      session.GetInputTypeInfo(0).GetTensorTypeAndShapeInfo();
  // Python export contract는 float32이므로 다른 dtype은 byte 해석 전에 거부한다.
  if (input_info.GetElementType() != ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT) {
    // dtype mismatch는 implicit conversion에 맡기지 않는다.
    throw std::runtime_error("model input must be float32");
  }
  // export 때 dynamic_axes로 batch만 -1일 수 있고 feature 축은 반드시 4다.
  const std::vector<std::int64_t> input_shape = input_info.GetShape();
  // short-circuit OR 덕분에 shape가 2차원이 아닐 때 input_shape[1]을 읽지 않는다.
  if (input_shape.size() != 2 || input_shape[1] != 4) {
    // 입력 rank/feature 수가 다르면 CreateTensor shape와 model 의미가 어긋난다.
    throw std::runtime_error("model input shape must be [batch, 4]");
  }
  // batch는 dynamic(-1) 또는 이 실행기가 사용하는 고정 1만 허용한다.
  if (input_shape[0] != -1 && input_shape[0] != 1) {
    // 고정 batch 8 model에 batch 1 buffer를 넘기는 식의 오류를 차단한다.
    throw std::runtime_error("model input batch dimension must be dynamic or 1");
  }
  // 첫 출력도 tensor type/shape 정보로 검증한다.
  const Ort::TensorTypeAndShapeInfo output_info =
      session.GetOutputTypeInfo(0).GetTensorTypeAndShapeInfo();
  // logits를 float pointer로 읽기 전에 output dtype을 확인한다.
  if (output_info.GetElementType() != ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT) {
    // INT64 label model이나 quantized raw output을 잘못 float로 읽지 않게 한다.
    throw std::runtime_error("model output must be float32 logits");
  }
  // 출력은 [batch, class]의 2차원 tensor이며 class 수는 3이어야 한다.
  const std::vector<std::int64_t> output_shape = output_info.GetShape();
  // class 축이 3인지 확인해 class_names 배열과의 index 계약을 지킨다.
  if (output_shape.size() != 2 || output_shape[1] != 3) {
    // 다른 class model을 metadata 없이 교체하는 것을 시작 단계에서 막는다.
    throw std::runtime_error("model output shape must be [batch, 3]");
  }
  // 출력 batch도 입력과 마찬가지로 dynamic 또는 고정 1이어야 한다.
  if (output_shape[0] != -1 && output_shape[0] != 1) {
    // batch 1 입력에 여러 결과를 반환하는 모델을 단일-frame 실행기로 처리하지 않는다.
    throw std::runtime_error("model output batch dimension must be dynamic or 1");
  }
}

// const reference는 logits를 복사하지 않고 읽으며 새 확률 vector만 소유해 반환한다.
std::vector<float> Softmax(const std::vector<float>& logits) {
  // 빈 출력은 잘못된 모델 계약이므로 의미 있는 예외를 던진다.
  if (logits.empty()) {
    // runtime_error는 main의 std::exception catch에서 처리된다.
    throw std::runtime_error("model returned an empty logits tensor");
  }
  // 첫 값을 초기 최댓값으로 두어 매우 작은 음수만 있어도 올바르게 처리한다.
  float maximum = logits.front();
  // 모든 logits를 순회하며 수치 안정화에 쓸 최댓값을 찾는다.
  for (const float value : logits) {
    // NaN/Inf 하나가 전체 softmax를 오염시키므로 계산 전에 contract 오류로 바꾼다.
    if (!std::isfinite(value)) {
      // downstream이 임의 class를 선택하지 않도록 명시적으로 실패한다.
      throw std::runtime_error("model returned a non-finite logit");
    }
    // 더 큰 값을 발견하면 maximum을 갱신한다.
    if (value > maximum) {
      // 현재 value를 새 최댓값으로 저장한다.
      maximum = value;
    }
  }
  // 출력 확률과 같은 길이의 벡터를 0.0으로 초기화한다.
  std::vector<float> probabilities(logits.size(), 0.0F);
  // 각 클래스의 지수값을 합산할 변수를 0으로 시작한다.
  float denominator = 0.0F;
  // size_t 인덱스로 logits와 probabilities의 같은 위치에 접근한다.
  for (std::size_t index = 0; index < logits.size(); ++index) {
    // 최댓값을 뺀 뒤 exp를 적용해 overflow 위험을 줄인다.
    probabilities[index] = std::exp(logits[index] - maximum);
    // 나중에 합이 1이 되도록 나눌 분모에 현재 지수값을 더한다.
    denominator += probabilities[index];
  }
  // 정상 유한 logits라면 양수여야 하지만 방어적으로 분모도 검증한다.
  if (!std::isfinite(denominator) || denominator <= 0.0F) {
    // 0 나눗셈과 NaN probability 발행을 막는다.
    throw std::runtime_error("softmax denominator is not finite and positive");
  }
  // 모든 지수값을 합으로 나누기 위해 확률 벡터를 다시 순회한다.
  for (float& probability : probabilities) {
    // 참조 변수 probability를 수정해 원본 벡터 값이 정규화되게 한다.
    probability /= denominator;
  }
  // 합이 1인 클래스 확률 벡터를 호출자에게 반환한다.
  return probabilities;
}

// argc와 argv에서 모델 경로 뒤의 네 센서 입력을 float array로 변환한다.
std::array<float, 4> ParseInput(const int argc, char* argv[]) {
  // 프로그램명+모델 경로+특성 4개이므로 정확히 6개 인수가 필요하다.
  if (argc != 6) {
    // 사용법 오류를 예외로 전달하면 main이 한 곳에서 오류 형식을 통일한다.
    throw std::runtime_error(
        "usage: edge_infer <model.onnx> <vibration_z> <temperature_z> "
        "<current_z> <rotation_error_z>");
  }
  // 각 위치를 이름 있는 지역 변수로 나누면 CLI 순서와 센서 의미를 review하기 쉽다.
  const float vibration_z = ParseFiniteFloat(argv[2], "vibration_z");
  // 세 번째 CLI 값은 표준화된 온도 변화다.
  const float temperature_z = ParseFiniteFloat(argv[3], "temperature_z");
  // 네 번째 CLI 값은 표준화된 전류다.
  const float current_z = ParseFiniteFloat(argv[4], "current_z");
  // 다섯 번째 CLI 값은 표준화된 회전 오차다.
  const float rotation_error_z = ParseFiniteFloat(argv[5], "rotation_error_z");
  // std::array initializer 순서는 training metadata의 feature_names와 같아야 한다.
  return {vibration_z, temperature_z, current_z, rotation_error_z};
}

// 익명 namespace의 범위가 여기서 끝난다.
}  // namespace

// main은 운영체제가 프로그램을 시작할 때 호출하는 진입점이다.
int main(int argc, char* argv[]) {
  // try 블록은 runtime과 입력 parsing에서 생긴 예외를 마지막 catch로 모은다.
  try {
    // argv[1]에 접근하기 전 ParseInput이 argc를 확인하도록 먼저 호출한다.
    std::array<float, 4> input_values = ParseInput(argc, argv);
    // filesystem::path는 Linux char와 Windows wchar_t 경로를 native c_str로 제공한다.
    const std::filesystem::path model_path = argv[1];
    // ORT_LOGGING_LEVEL_WARNING은 경고 이상만 출력하고 "edge-infer"는 logger 이름이다.
    Ort::Env environment(ORT_LOGGING_LEVEL_WARNING, "edge-infer");
    // SessionOptions는 thread와 graph optimization 정책을 session 생성 전에 설정한다.
    Ort::SessionOptions session_options;
    // intra-op thread를 1로 제한해 작은 모델에서 thread 생성 비용과 변동을 줄인다.
    session_options.SetIntraOpNumThreads(1);
    // ORT_ENABLE_ALL은 runtime이 지원하는 그래프 최적화를 모두 활성화한다.
    session_options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);
    // path::c_str은 플랫폼 native 문자형을 반환하므로 수동 UTF-8→wide 변환을 피한다.
    Ort::Session session(environment, model_path.c_str(), session_options);
    // 이름과 tensor memory를 얻기 전에 모델의 개수·dtype·shape 계약을 검증한다.
    ValidateModelContract(session);
    // 기본 allocator는 runtime이 반환하는 입력·출력 이름 메모리를 관리한다.
    Ort::AllocatorWithDefaultOptions allocator;
    // 첫 번째 입력 이름을 RAII 문자열 포인터로 받는다.
    Ort::AllocatedStringPtr input_name = session.GetInputNameAllocated(0, allocator);
    // 첫 번째 출력 이름도 RAII 문자열 포인터로 받는다.
    Ort::AllocatedStringPtr output_name = session.GetOutputNameAllocated(0, allocator);
    // Run API는 C 문자열 포인터 배열을 요구하므로 입력 이름 주소 하나를 배열에 담는다.
    const std::array<const char*, 1> input_names = {input_name.get()};
    // 출력 이름도 같은 방식으로 길이 1 배열에 담는다.
    const std::array<const char*, 1> output_names = {output_name.get()};
    // 모델 계약에 따라 batch 1, 특성 4의 64비트 정수 shape를 만든다.
    const std::array<std::int64_t, 2> input_shape = {1, 4};
    // CPU allocator의 일반 메모리를 tensor가 참조한다는 정보를 만든다.
    const Ort::MemoryInfo memory_info =
        Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
    // CreateTensor는 input_values 메모리를 복사하지 않고 mutable float tensor view로 감싼다.
    // 따라서 input_values는 const가 아니며 input_tensor와 Run이 끝날 때까지 반드시 살아 있어야 한다.
    Ort::Value input_tensor = Ort::Value::CreateTensor<float>(
        // memory_info는 pointer가 가리키는 메모리가 CPU arena 호환임을 설명한다.
        memory_info,
        // data는 std::array의 연속된 첫 float 주소이며 const_cast가 필요 없는 mutable pointer다.
        input_values.data(),
        // element_count는 byte 수가 아니라 float 원소 네 개다.
        input_values.size(),
        // shape_data는 [1, 4] 정수 배열의 첫 주소다.
        input_shape.data(),
        // shape_len은 rank 2를 뜻한다.
        input_shape.size());
    // steady_clock은 시간 동기화로 벽시계가 바뀌어도 경과 시간 측정이 역행하지 않는다.
    const auto started_at = std::chrono::steady_clock::now();
    // Run은 입력 tensor를 모델에 넣고 요청한 출력 tensor 벡터를 반환한다.
    std::vector<Ort::Value> outputs = session.Run(
        // null RunOptions는 terminate flag나 tag 없는 기본 실행을 뜻한다.
        Ort::RunOptions{nullptr},
        // 입력 이름 배열의 첫 주소다.
        input_names.data(),
        // 입력 Ort::Value 한 개의 주소다.
        &input_tensor,
        // 입력 tensor 개수는 1이다.
        1,
        // 요청할 출력 이름 배열의 첫 주소다.
        output_names.data(),
        // 요청 출력 개수도 1이다.
        1);
    // 추론 직후 종료 시각을 읽어 출력 변환 시간과 구분한다.
    const auto finished_at = std::chrono::steady_clock::now();
    // 출력이 없거나 첫 출력이 tensor가 아니면 모델 계약 위반으로 처리한다.
    if (outputs.empty() || !outputs.front().IsTensor()) {
      // 조용히 잘못된 메모리를 읽지 않고 명시적인 오류를 발생시킨다.
      throw std::runtime_error("first model output is not a tensor");
    }
    // 첫 tensor의 shape와 원소 수 정보를 가져온다.
    const Ort::TensorTypeAndShapeInfo output_info =
        outputs.front().GetTensorTypeAndShapeInfo();
    // GetElementCount는 batch를 포함한 전체 출력 float 개수를 반환한다.
    const std::size_t output_count = output_info.GetElementCount();
    // 학습 예제는 정확히 세 클래스 logits를 출력해야 한다.
    if (output_count != 3) {
      // 예상과 실제 원소 수를 함께 표시해 모델 교체 오류를 쉽게 찾게 한다.
      throw std::runtime_error(
          "expected 3 logits, got " + std::to_string(output_count));
    }
    // GetTensorData는 runtime이 소유한 연속 float 출력 메모리의 읽기 전용 주소다.
    const float* output_data = outputs.front().GetTensorData<float>();
    // 포인터 범위를 vector로 복사해 Softmax와 안전하게 값 수명을 분리한다.
    const std::vector<float> logits(output_data, output_data + output_count);
    // Python과 같은 안정화 softmax로 logits를 확률로 바꾼다.
    const std::vector<float> probabilities = Softmax(logits);
    // max_element 없이 단순 loop로 가장 높은 확률의 클래스 인덱스를 구한다.
    std::size_t predicted_class = 0;
    // 두 번째 클래스부터 현재 최고 확률과 비교한다.
    for (std::size_t index = 1; index < probabilities.size(); ++index) {
      // 더 높은 확률이면 예측 클래스 인덱스를 갱신한다.
      if (probabilities[index] > probabilities[predicted_class]) {
        // index를 새 최고 클래스 위치로 저장한다.
        predicted_class = index;
      }
    }
    // duration_cast는 steady_clock 차이를 microseconds 정수 단위로 바꾼다.
    const auto elapsed_us =
        std::chrono::duration_cast<std::chrono::microseconds>(finished_at - started_at);
    // 클래스 인덱스와 사람이 읽을 label을 같은 순서로 고정한다.
    const std::array<const char*, 3> class_names = {
        // index 0은 metadata의 normal class와 정확히 같아야 한다.
        "normal",
        // index 1은 warning class다.
        "warning",
        // index 2는 stop_required class다.
        "stop_required",
    };
    // fixed와 setprecision(6)은 확률을 소수점 여섯 자리로 일관되게 표시한다.
    std::cout << std::fixed << std::setprecision(6);
    // 모델의 입력·출력 이름을 표시해 metadata 계약을 빠르게 확인한다.
    std::cout << "input=" << input_name.get() << " output=" << output_name.get() << '\n';
    // 최고 클래스 번호와 label을 한 줄에 표시한다.
    std::cout << "class=" << predicted_class
              << " label=" << class_names[predicted_class] << '\n';
    // 세 클래스 확률을 순서대로 표시한다.
    std::cout << "probabilities=" << probabilities[0] << ',' << probabilities[1] << ','
              << probabilities[2] << '\n';
    // 단일 호출 경과 시간을 microseconds로 표시하되 실제 승인은 반복 benchmark를 사용한다.
    std::cout << "latency_us=" << elapsed_us.count() << '\n';
    // 0은 프로그램이 정상 종료되었다는 운영체제 관례다.
    return 0;
  // ONNX Runtime과 표준 라이브러리 예외를 const reference로 받아 slicing과 복사를 피한다.
  } catch (const std::exception& error) {
    // 오류 원인을 표준 오류 스트림에 표시해 shell redirect와 monitoring이 구분하게 한다.
    std::cerr << "edge_infer error: " << error.what() << '\n';
    // 1은 실행 실패를 호출한 shell이나 CI에 전달한다.
    return 1;
  }
}
