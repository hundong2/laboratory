# 실무형 필수 실습

작성일: 2026-07-26

이 폴더의 실습은 모델 정확도 밖에서 발생하는 로봇 제품 실패를 다룬다. 각 파일은 실행문 바로 위의 한국어 주석으로 문법과 설계 이유를 설명한다.

## 실습 1: 센서 시간 동기화

```bash
cd job
python labs/01_time_sync.py
```

배우는 내용:

- sensor timestamp와 host 도착 순서의 차이
- approximate synchronization
- tolerance, unmatched drop, max skew
- 오래된 데이터를 억지로 결합하지 않는 정책

합격 과제:

1. 최대 상대 속도와 허용 공간 오차에서 tolerance를 계산한다.
2. 카메라 30 Hz, LiDAR 10 Hz, 3 ms jitter를 simulation한다.
3. match rate, drop rate, p95 skew를 보고한다.
4. tolerance를 두 배로 했을 때 match는 늘지만 의미가 왜 나빠질 수 있는지 설명한다.

## 실습 2: 고장 주입과 안전 경계

```bash
python labs/02_fault_injection.py
```

배우는 내용:

- shape, NaN/Inf, timestamp, timeout 검사
- 정상 결과와 fallback 결과의 명시적 구분
- 연속 오류 circuit breaker
- detection, containment, recovery, telemetry

합격 과제:

1. stale, NaN, wrong shape, timeout을 각각 주입한다.
2. inference 함수가 호출되기 전에 거부되는 고장을 구분한다.
3. 세 번 연속 오류 뒤 breaker가 열리는지 확인한다.
4. 정상 입력 한 번으로 breaker를 자동 초기화할지, 운영자 reset만 허용할지 위험 분석한다.

주의: 이 Python 예제는 동기 호출이 끝난 뒤 timeout을 판정한다. 실제 native/GPU call을 강제 중단하는 구조가 아니다. 제품에서는 격리 worker process, runtime timeout 지원, watchdog, actuator 안전 계층을 조합한다.

## 실습 3: 자동 release gate

```bash
python labs/03_release_gate.py \
  --rules configs/release_gates.json \
  --baseline configs/baseline_report.json \
  --candidate configs/candidate_report.json \
  --output reports/release_gate_result.json
```

정상 예제는 exit code 0이어야 한다.

다음 값을 하나씩 나쁘게 바꾸고 exit code가 2가 되는지 확인한다.

- `stop_recall`
- `p99_ms`
- `checksums_verified`
- `rollback_tested`
- `soak_minutes`

합격 과제:

1. 팀 subsystem의 실제 요구사항으로 threshold를 교체한다.
2. threshold마다 requirement 또는 hazard ID를 추가한다.
3. candidate가 baseline보다 정확도는 높지만 p99가 나쁜 경우 release 판단을 문서화한다.
4. waiver가 필요하다면 만료일, owner, residual risk를 별도 파일로 관리한다.

## 실습 4: C++ latest-only worker

Ubuntu에서:

```bash
cd job
g++ \
  -std=c++17 \
  -O2 \
  -Wall \
  -Wextra \
  -Wpedantic \
  -pthread \
  labs/04_latest_only_worker.cpp \
  -o /tmp/latest_only_worker
/tmp/latest_only_worker
```

배우는 내용:

- producer와 inference worker 분리
- queue를 무한히 쌓지 않고 최신 frame으로 교체
- `mutex`, `condition_variable`, 종료 조건
- processed, replaced, frame age, p99

합격 과제:

1. producer 2 ms, inference 5 ms에서 대체 수를 기록한다.
2. unbounded FIFO로 바꿔 마지막 frame age를 비교한다.
3. inference를 1~10 ms 무작위로 바꿔 p99를 측정한다.
4. stop 동안 wait 중인 worker가 deadlock 없이 종료되는지 test한다.
5. TSan build로 data race를 확인한다.

## 자동 테스트

```bash
cd job
python -m unittest discover -s tests -v
```

Python 실습의 핵심 정책은 테스트로 고정한다. C++ 실습은 Ubuntu CI에서 compile, TSan, Release benchmark job을 별도로 둔다.
