"""추론 경계에서 잘못된 입력과 timeout을 안전한 fallback으로 바꾸는 실습."""

# dataclass는 입력과 결과를 명시적인 불변 record로 만든다.
from dataclasses import dataclass
# isfinite는 NaN과 양/음의 무한대를 검사한다.
from math import isfinite
# perf_counter_ns는 system clock 변경과 무관한 경과 시간을 측정한다.
from time import perf_counter_ns
# Callable은 주입 가능한 inference 함수의 입력·출력 계약을 설명한다.
from typing import Callable


# frozen=True는 callback 안에서 실수로 frame timestamp와 feature를 바꾸지 못하게 한다.
@dataclass(frozen=True)
class SensorFrame:
    """측정 timestamp와 이미 표준화된 네 feature를 가진 입력."""

    # measured_at_ms는 sensor가 실제로 측정한 monotonic 기준 시각이다.
    measured_at_ms: float
    # features는 예제 model contract의 float 네 개다.
    features: tuple[float, ...]


# frozen=True는 발행 뒤 result 상태가 바뀌지 않게 한다.
@dataclass(frozen=True)
class InferenceResult:
    """정상 예측 또는 명시적인 fallback 상태."""

    # accepted가 True일 때만 predicted_class를 downstream 판단에 사용할 수 있다.
    accepted: bool
    # predicted_class는 정상 결과의 class index이며 fallback에서는 -1이다.
    predicted_class: int
    # reason은 정상 또는 거부 사유를 machine-readable 문자열로 기록한다.
    reason: str
    # latency_ms는 inference를 호출한 경우 실제 동기 호출 경과 시간이다.
    latency_ms: float


# Callable alias는 feature tuple을 받아 score tuple을 반환하는 model 함수다.
ModelFunction = Callable[[tuple[float, ...]], tuple[float, ...]]


class SafeInferenceRunner:
    """입력 계약, age, runtime 결과, 연속 오류를 검사하는 안전 경계."""

    # age와 inference deadline, 연속 오류 한도를 명시적으로 받는다.
    def __init__(
        self,
        maximum_age_ms: float,
        inference_deadline_ms: float,
        maximum_consecutive_failures: int,
    ) -> None:
        # 음수 또는 0인 제한값은 안전 정책을 무력화하므로 거부한다.
        if maximum_age_ms <= 0.0 or inference_deadline_ms <= 0.0:
            # ValueError는 구성 단계에서 parameter 오류를 드러낸다.
            raise ValueError("age and deadline limits must be positive")
        # 연속 오류 한도도 최소 1이어야 breaker가 의미가 있다.
        if maximum_consecutive_failures < 1:
            # 잘못된 breaker 설정을 즉시 거부한다.
            raise ValueError("maximum_consecutive_failures must be at least one")
        # stale 판단에 사용할 최대 입력 age를 저장한다.
        self.maximum_age_ms = maximum_age_ms
        # 동기 inference가 끝난 뒤 비교할 deadline을 저장한다.
        self.inference_deadline_ms = inference_deadline_ms
        # breaker를 열 연속 실패 횟수를 저장한다.
        self.maximum_consecutive_failures = maximum_consecutive_failures
        # 새 runner는 실패가 없으므로 0에서 시작한다.
        self.consecutive_failures = 0

    # 실패 수를 증가시키고 공통 fallback result를 만드는 내부 함수다.
    def _reject(self, reason: str, latency_ms: float = 0.0) -> InferenceResult:
        # 모든 거부를 연속 실패로 계산해 반복 고장을 감지한다.
        self.consecutive_failures += 1
        # -1 class와 reason을 가진 명시적 미수용 결과를 반환한다.
        return InferenceResult(False, -1, reason, latency_ms)

    # now_ms를 주입하면 test가 실제 시계를 기다리지 않고 age를 재현할 수 있다.
    def run(
        self,
        frame: SensorFrame,
        now_ms: float,
        model: ModelFunction,
    ) -> InferenceResult:
        """frame을 검증하고 model을 호출한 뒤 안전하게 결과를 반환한다."""

        # breaker가 열린 동안 model을 호출하지 않아 연쇄 장애와 자원 고갈을 막는다.
        if self.consecutive_failures >= self.maximum_consecutive_failures:
            # breaker 거부 자체는 실패 수를 더 늘리지 않고 현재 상태를 유지한다.
            return InferenceResult(False, -1, "circuit_open", 0.0)
        # 미래 timestamp는 clock mismatch 또는 잘못된 time domain을 뜻한다.
        if frame.measured_at_ms > now_ms:
            # inference 전에 future timestamp 입력을 containment한다.
            return self._reject("timestamp_in_future")
        # 결과를 사용할 때 입력이 얼마나 오래되었는지 ms로 계산한다.
        age_ms = now_ms - frame.measured_at_ms
        # 최대 허용 age를 넘긴 frame은 계산해도 현재 상태를 나타내지 않는다.
        if age_ms > self.maximum_age_ms:
            # stale frame은 model을 호출하지 않고 즉시 버린다.
            return self._reject("stale_input")
        # model contract는 정확히 네 feature를 요구한다.
        if len(frame.features) != 4:
            # wrong shape를 native runtime까지 전달하지 않는다.
            return self._reject("wrong_shape")
        # 모든 feature가 유한한지 검사한다.
        if not all(isfinite(value) for value in frame.features):
            # NaN/Inf는 model 전체로 퍼지기 전에 경계에서 차단한다.
            return self._reject("non_finite_input")
        # inference 동기 호출 직전 monotonic 시작 시각을 ns로 읽는다.
        started_ns = perf_counter_ns()
        # runtime exception을 node/process 전체 장애가 아닌 frame 오류로 containment한다.
        try:
            # 주입된 model 함수로 logits 또는 score를 계산한다.
            scores = model(frame.features)
        # 교육 예제에서는 모든 Exception을 경계에서 잡고 reason을 기록한다.
        except Exception as error:
            # 구체 타입 이름을 telemetry reason에 포함해 원인 집계를 돕는다.
            return self._reject(f"runtime_error:{type(error).__name__}")
        # 호출 경과 나노초를 밀리초로 변환한다.
        latency_ms = (perf_counter_ns() - started_ns) / 1_000_000.0
        # 동기 호출이 deadline을 넘으면 늦은 결과를 downstream에 보내지 않는다.
        if latency_ms > self.inference_deadline_ms:
            # firm real-time 정책으로 timeout 결과를 폐기한다.
            return self._reject("inference_timeout", latency_ms)
        # 예제 classifier는 세 class score를 반환해야 한다.
        if len(scores) != 3:
            # output contract 위반도 잘못된 model artifact로 간주한다.
            return self._reject("wrong_output_shape", latency_ms)
        # output score가 NaN/Inf이면 argmax 결과를 신뢰할 수 없다.
        if not all(isfinite(score) for score in scores):
            # 비정상 runtime 출력을 발행하지 않는다.
            return self._reject("non_finite_output", latency_ms)
        # range는 1과 2 index를 순회하며 현재 최고 score 위치를 찾는다.
        predicted_class = max(range(len(scores)), key=scores.__getitem__)
        # 정상 결과가 나오면 연속 실패 수를 0으로 복구한다.
        self.consecutive_failures = 0
        # accepted=True와 class, 정상 reason, latency를 반환한다.
        return InferenceResult(True, predicted_class, "ok", latency_ms)


# 직접 실행할 때 정상과 네 가지 고장을 차례로 주입한다.
if __name__ == "__main__":
    # 50 ms age, 20 ms inference deadline, 3회 breaker 정책을 만든다.
    runner = SafeInferenceRunner(50.0, 20.0, 3)
    # 간단한 model 함수는 첫 세 feature를 score로 돌려준다.
    demo_model: ModelFunction = lambda features: (
        features[0],
        features[1],
        features[2],
    )
    # now=1000 ms에서 10 ms 전 측정된 정상 frame을 만든다.
    valid = SensorFrame(990.0, (0.1, 0.8, 0.1, 0.0))
    # 정상 결과는 class 1과 accepted=True를 반환해야 한다.
    print(runner.run(valid, 1000.0, demo_model))
    # 100 ms 오래된 입력을 주입한다.
    print(runner.run(SensorFrame(900.0, valid.features), 1000.0, demo_model))
    # NaN 입력을 주입한다.
    print(runner.run(SensorFrame(999.0, (0.0, float("nan"), 0.0, 0.0)), 1000.0, demo_model))
    # 잘못된 feature 수를 주입해 세 번째 연속 실패로 breaker를 연다.
    print(runner.run(SensorFrame(999.0, (0.0, 1.0)), 1000.0, demo_model))
    # breaker가 열린 뒤 정상 frame도 model 호출 없이 circuit_open으로 거부된다.
    print(runner.run(valid, 1000.0, demo_model))
