# ROS 2 Jazzy/Humble에서 충분한 최소 CMake 버전을 선언한다.
cmake_minimum_required(VERSION 3.16)
# edge_ai_demo라는 C++ 프로젝트를 선언한다.
project(edge_ai_demo LANGUAGES CXX)

# C++17 표준을 강제로 사용한다.
set(CMAKE_CXX_STANDARD 17)
# 낮은 표준으로 자동 대체하지 못하게 한다.
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# 컴파일러 고유 확장을 끈다.
set(CMAKE_CXX_EXTENSIONS OFF)

# 일반 빌드에서는 경고를 표시하고, CI에서는 이 옵션으로 경고를 오류로 승격할 수 있다.
option(EDGE_AI_WARNINGS_AS_ERRORS "Treat compiler warnings as errors" OFF)
# 개발용 build에서 address/undefined behavior sanitizer를 켜는 선택지다.
option(EDGE_AI_ENABLE_ASAN_UBSAN "Enable AddressSanitizer and UndefinedBehaviorSanitizer" OFF)

# ament 패키지 macro를 찾는다.
find_package(ament_cmake REQUIRED)
# ROS 2 C++ client library를 찾는다.
find_package(rclcpp REQUIRED)
# 예제 입력·출력 메시지가 있는 std_msgs를 찾는다.
find_package(std_msgs REQUIRED)

# ONNX Runtime 설치 root는 colcon build 때 직접 전달해야 한다.
if(NOT DEFINED ONNXRUNTIME_ROOT)
  # 다른 버전을 우연히 link하지 않도록 누락을 configure error로 처리한다.
  message(FATAL_ERROR "Pass --cmake-args -DONNXRUNTIME_ROOT=/opt/onnxruntime")
# 조건문을 닫는다.
endif()

# ROS node 실행 파일과 source를 연결한다.
add_executable(edge_ai_node src/edge_ai_node.cpp)
# GCC와 Clang 계열에서는 실무에서 놓치기 쉬운 변환·shadowing까지 경고한다.
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  # PRIVATE는 이 실행 파일을 컴파일할 때만 warning option을 적용한다는 뜻이다.
  target_compile_options(
    edge_ai_node
    PRIVATE
      -Wall
      -Wextra
      -Wpedantic
      -Wconversion
      -Wshadow
  )
# MSVC에서는 /W4가 실무적으로 유용한 높은 경고 수준이다.
elseif(MSVC)
  # 외부 dependency가 아니라 우리가 작성한 target에만 경고 수준을 적용한다.
  target_compile_options(edge_ai_node PRIVATE /W4)
# 지원 compiler 분기를 닫는다.
endif()

# CI가 warning 없는 상태를 강제하려 할 때만 Werror/WX를 추가한다.
if(EDGE_AI_WARNINGS_AS_ERRORS)
  # GCC와 Clang의 모든 warning을 compile error로 바꾼다.
  if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    # target 단위 설정이라 workspace의 다른 ROS package에는 영향을 주지 않는다.
    target_compile_options(edge_ai_node PRIVATE -Werror)
  # MSVC에서 /WX는 warning을 error로 승격한다.
  elseif(MSVC)
    # target 단위로 /WX를 추가한다.
    target_compile_options(edge_ai_node PRIVATE /WX)
  # compiler 분기를 닫는다.
  endif()
# warnings-as-errors option 분기를 닫는다.
endif()

# Sanitizer는 성능 측정용 Release가 아니라 결함 탐지용 Debug/RelWithDebInfo에 사용한다.
if(EDGE_AI_ENABLE_ASAN_UBSAN)
  # 이 예제는 GCC 또는 Clang의 sanitizer flag 조합을 기준으로 한다.
  if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    # compile 단계에 stack trace용 frame pointer와 두 sanitizer를 삽입한다.
    target_compile_options(
      edge_ai_node
      PRIVATE
        -fsanitize=address,undefined
        -fno-omit-frame-pointer
    )
    # link 단계에도 같은 sanitizer runtime을 연결해야 실행 시 검사가 동작한다.
    target_link_options(edge_ai_node PRIVATE -fsanitize=address,undefined)
  # 지원하지 않는 compiler에서 조용히 무시하면 안전 검사를 했다고 오해할 수 있다.
  else()
    # configure 단계에서 명시적으로 중단해 검증 누락을 방지한다.
    message(FATAL_ERROR "EDGE_AI_ENABLE_ASAN_UBSAN requires GCC or Clang")
  # compiler 분기를 닫는다.
  endif()
# sanitizer option 분기를 닫는다.
endif()

# ONNX Runtime header 폴더를 node target에만 추가한다.
target_include_directories(edge_ai_node PRIVATE "${ONNXRUNTIME_ROOT}/include")
# rclcpp와 std_msgs의 include, library 정보를 ament 방식으로 추가한다.
ament_target_dependencies(edge_ai_node rclcpp std_msgs)
# 지정한 root의 lib 폴더에서만 ONNX Runtime을 찾는다.
find_library(
  # 검색 결과를 담을 변수다.
  ONNXRUNTIME_LIBRARY
  # 플랫폼별 실제 파일 이름의 공통 부분이다.
  NAMES onnxruntime
  # 공급 archive의 일반적인 library 위치다.
  PATHS "${ONNXRUNTIME_ROOT}/lib"
  # 시스템 다른 버전 사용을 막는다.
  NO_DEFAULT_PATH
)
# 라이브러리가 없으면 link 단계까지 기다리지 않고 중단한다.
if(NOT ONNXRUNTIME_LIBRARY)
  # 사용자가 고쳐야 할 root를 오류에 표시한다.
  message(FATAL_ERROR "onnxruntime library not found under ${ONNXRUNTIME_ROOT}/lib")
# 조건문을 닫는다.
endif()
# ROS node에 ONNX Runtime library를 link한다.
target_link_libraries(edge_ai_node "${ONNXRUNTIME_LIBRARY}")
# install은 ros2 run이 찾는 lib/<package> 경로로 실행 파일을 복사한다.
install(TARGETS edge_ai_node DESTINATION lib/${PROJECT_NAME})

# BUILD_TESTING 옵션이 켜진 CI에서 lint 도구를 구성한다.
if(BUILD_TESTING)
  # 자동 lint package를 찾는다.
  find_package(ament_lint_auto REQUIRED)
  # package.xml의 lint 의존성으로 모든 검사를 등록한다.
  ament_lint_auto_find_test_dependencies()
# 테스트 조건문을 닫는다.
endif()

# 패키지 색인과 environment hook 생성을 완료한다.
ament_package()
