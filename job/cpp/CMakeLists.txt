# 이 파일을 해석할 최소 CMake 버전을 3.20으로 정한다.
cmake_minimum_required(VERSION 3.20)
# 프로젝트 이름과 사용 언어가 C++임을 선언한다.
project(edge_infer LANGUAGES CXX)

# C++17을 요구해 std::filesystem이 아닌 기본 현대 C++ 기능을 안정적으로 사용한다.
set(CMAKE_CXX_STANDARD 17)
# 컴파일러가 더 낮은 표준으로 조용히 대체하지 못하게 한다.
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# GNU 전용 확장보다 이식 가능한 표준 C++ 모드를 사용한다.
set(CMAKE_CXX_EXTENSIONS OFF)

# 교육/CI에서 warning을 오류로 승격할지 선택하는 option이며 기본은 OFF다.
option(EDGE_INFER_WARNINGS_AS_ERRORS "Treat compiler warnings as errors" OFF)
# AddressSanitizer와 UndefinedBehaviorSanitizer를 켤지 선택한다.
option(EDGE_INFER_ENABLE_ASAN_UBSAN "Enable ASan and UBSan on GCC/Clang" OFF)

# 사용자가 -DONNXRUNTIME_ROOT=/opt/onnxruntime처럼 설치 루트를 넘겼는지 확인한다.
if(NOT DEFINED ONNXRUNTIME_ROOT)
  # 필요한 값을 빠뜨렸을 때 찾을 위치를 추측하지 않고 명확한 오류를 낸다.
  message(FATAL_ERROR "Pass -DONNXRUNTIME_ROOT=/absolute/path/to/onnxruntime")
# 조건문을 닫는다.
endif()

# main.cpp 한 파일로 edge_infer 실행 파일 target을 만든다.
add_executable(edge_infer main.cpp)
# onnxruntime_cxx_api.h가 있는 include 폴더를 이 target에만 추가한다.
target_include_directories(edge_infer PRIVATE "${ONNXRUNTIME_ROOT}/include")
# libonnxruntime.so 또는 Windows import library를 찾을 경로를 지정한다.
find_library(
  # 찾은 절대 경로를 저장할 CMake 변수 이름이다.
  ONNXRUNTIME_LIBRARY
  # 라이브러리 기본 이름이며 플랫폼별 prefix와 suffix는 CMake가 처리한다.
  NAMES onnxruntime
  # 공급사 배포 archive의 일반적인 lib 폴더를 우선 검색한다.
  PATHS "${ONNXRUNTIME_ROOT}/lib"
  # 시스템의 우연한 다른 버전을 사용하지 않도록 지정 경로만 찾는다.
  NO_DEFAULT_PATH
)
# 라이브러리를 찾지 못하면 configure 단계에서 즉시 중단한다.
if(NOT ONNXRUNTIME_LIBRARY)
  # 설치 경로와 archive 구조를 고치라는 오류를 표시한다.
  message(FATAL_ERROR "onnxruntime library was not found under ${ONNXRUNTIME_ROOT}/lib")
# 조건문을 닫는다.
endif()
# 실행 파일에 ONNX Runtime 동적 라이브러리를 link한다.
target_link_libraries(edge_infer PRIVATE "${ONNXRUNTIME_LIBRARY}")
# GCC/Clang에서 흔한 실수를 warning으로 보여 준다.
target_compile_options(
  # warning은 edge_infer source를 compile할 때만 적용한다.
  edge_infer
  # PRIVATE는 이 target을 link하는 다른 target에 option을 전파하지 않는다.
  PRIVATE
  # generator expression은 GCC 또는 Clang일 때만 Unix 계열 warning flag를 추가한다.
  $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall;-Wextra;-Wpedantic;-Wconversion;-Wshadow>
)

# 사용자가 warning-as-error option을 켰는지 확인한다.
if(EDGE_INFER_WARNINGS_AS_ERRORS)
  # GCC/Clang에서는 모든 활성 warning을 compile 실패로 바꾼다.
  target_compile_options(edge_infer PRIVATE $<$<CXX_COMPILER_ID:GNU,Clang>:-Werror>)
  # MSVC에서는 /WX가 같은 역할을 한다.
  target_compile_options(edge_infer PRIVATE $<$<CXX_COMPILER_ID:MSVC>:/WX>)
# warning-as-error 조건을 닫는다.
endif()

# sanitizer option을 켠 경우 지원하는 compiler에 compile/link instrumentation을 추가한다.
if(EDGE_INFER_ENABLE_ASAN_UBSAN)
  # GCC/Clang이 아니면 아래 flag가 호환되지 않으므로 configure를 거부한다.
  if(NOT CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    # 조용히 sanitizer 없이 빌드되는 것보다 명확한 실패가 안전하다.
    message(FATAL_ERROR "EDGE_INFER_ENABLE_ASAN_UBSAN requires GCC or Clang")
  # 지원 compiler 분기의 반대 조건을 닫는다.
  endif()
  # compile instrumentation, frame pointer 유지, 첫 오류 후 계속 실행 금지를 설정한다.
  target_compile_options(
    # edge_infer source에 sanitizer instrumentation을 넣는다.
    edge_infer
    # PRIVATE scope로 외부 target에 전파하지 않는다.
    PRIVATE
    # address는 use-after-free/out-of-bounds, undefined는 여러 UB를 검사한다.
    -fsanitize=address,undefined
    # frame pointer를 유지하면 sanitizer stack trace가 더 정확하다.
    -fno-omit-frame-pointer
    # recover를 끄면 첫 UB에서 실패해 CI가 놓치지 않는다.
    -fno-sanitize-recover=all
  )
  # 최종 실행 파일에도 sanitizer runtime을 link하도록 같은 핵심 flag를 추가한다.
  target_link_options(edge_infer PRIVATE -fsanitize=address,undefined)
# sanitizer option 조건을 닫는다.
endif()
