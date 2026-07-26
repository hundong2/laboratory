# 최종 실전 과제: 배포 가능한 로보틱스 AI 기능 출시

작성일: 2026-07-26

권장 기간: 2~3주
팀 구성: 3~5명

## 미션

네 개의 센서 특성으로 `normal`, `warning`, `stop_required`를 판단하는 교육 모델을 실제 ROS 2 component와 target hardware release 후보로 만든다.

모델 출력은 실제 actuator에 연결하지 않는다. `stop_required`는 diagnostic 또는 shadow topic으로만 발행한다.

## 제공 입력

- `src/fine_tune.py`
- `src/export_optimize.py`
- `cpp/main.cpp`
- `ros2/`
- `labs/`
- 팀이 수집하거나 공개적으로 사용 가능한 센서 데이터

합성 데이터만으로 최종 합격할 수 없다. 최소 한 개의 실제 또는 물리 simulator 데이터 경로를 연결해야 한다.

## 1. 요구사항 작성

다음을 숫자로 제출한다.

- 입력 feature, 단위, range, rate
- timestamp clock과 허용 age
- class 의미와 downstream 행동
- 위험 클래스 recall 하한
- 허용 false stop 비율
- p99 end-to-end latency
- deadline miss rate
- RAM/VRAM, power, thermal budget
- ODD와 out-of-scope
- timeout과 invalid input의 fallback

threshold의 근거가 없으면 요구사항으로 인정하지 않는다.

## 2. 데이터 release

필수 산출물:

```text
data-card.md
dataset-manifest.json
split-manifest.json
calibration/
qa-report.json
```

검사:

- robot/mission/site/date group split
- 중복과 인접 frame leakage
- timestamp gap/역행
- class와 ODD coverage
- sensor/calibration version
- 개인정보와 retention

## 3. 모델 후보

최소 세 후보를 같은 test protocol로 비교한다.

1. 간단한 baseline
2. fine-tuned FP32
3. FP16 또는 INT8 경량 후보

보고서:

- 여러 seed의 평균과 표준편차
- confusion matrix
- 위험 클래스 precision/recall
- confidence calibration
- challenge set
- 실패 예제 taxonomy
- 파일 크기와 operator 지원

## 4. model contract

필수:

- ONNX checker
- 입력/출력 이름, shape, dtype
- mean/std, class map
- opset, model checksum
- golden input/output 100건 이상
- Python↔ONNX↔C++ 허용 오차

의도적으로 metadata의 class 순서를 바꾸었을 때 test가 실패해야 한다.

## 5. ROS 2 component

필수 기능:

- timestamp와 frame을 가진 전용 input/output message
- lifecycle configure에서 model과 metadata 검증
- bounded latest-only queue
- stale, NaN/Inf, wrong shape 거부
- timeout과 반복 runtime 오류의 degraded state
- model version, latency, drop 수 diagnostic
- QoS 선택 근거

입력 callback에서 동기 추론을 오래 수행하는 구조는 latency evidence 없이 승인하지 않는다.

## 6. 실기기 검증

대상 장치에서 다음을 기록한다.

```text
hardware/BOM
OS/kernel/BSP
driver/runtime/container digest
CPU/GPU/NPU mode
p50/p95/p99/max
deadline miss rate
peak RAM/VRAM
power
temperature
30분 이상 soak test
```

개발 PC 수치를 target 수치로 대체할 수 없다.

## 7. 검증 단계

필수 evidence:

1. unit/property test
2. golden contract test
3. rosbag open-loop replay
4. fault injection
5. SIL closed-loop 또는 simulator integration
6. 가능한 경우 HIL
7. shadow output 비교

고장 주입은 최소 다음을 포함한다.

- stale
- out-of-order timestamp
- NaN/Inf
- wrong shape
- sensor burst/drop
- model corruption
- inference timeout
- node restart
- disk/log pressure
- thermal throttling 또는 인위적 CPU contention

## 8. release package

```text
release/
  model.onnx
  metadata.json
  checksums.txt
  SBOM
  container-or-install-manifest
  model-card.md
  data-card.md
  benchmark.json
  validation-report.md
  known-limitations.md
  rollback.md
```

release candidate는 [labs/03_release_gate.py](labs/03_release_gate.py)의 자동 gate를 통과해야 한다.

## 9. red-team 심사

다른 팀이 다음 중 하나 이상을 사전 고지 없이 주입한다.

- clock drift
- calibration mismatch
- queue backlog
- model/metadata version mismatch
- GPU memory pressure
- malformed message
- unsupported runtime version

평가 대상은 “고장이 발생하지 않음”이 아니라 detection, containment, recovery, telemetry다.

## 10. 최종 demo 순서

1. 정상 bag replay
2. Python/C++ golden 동등성
3. 실제 target latency dashboard
4. stale/NaN/model corruption 장애 주입
5. fallback 확인
6. 신모델 배포
7. 자동 gate 실패 release 거부
8. 이전 모델 rollback

## 11. 합격 판정

[06_organization_curriculum.md](06_organization_curriculum.md)의 100점 rubric을 사용한다. 모든 필수 gate를 통과하고 80점 이상이어야 한다.

특히 다음은 즉시 불합격이다.

- test set 또는 challenge set을 학습 선택에 사용
- target 장치 측정 없음
- stale/invalid input을 정상 결과처럼 발행
- model checksum 검증 없음
- rollback 미실행
- 알려진 위험과 한계를 문서에서 숨김
