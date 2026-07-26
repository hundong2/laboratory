"""두 센서 stream의 timestamp를 tolerance 안에서만 결합하는 실습."""

# dataclass는 timestamp와 payload를 이름 있는 불변 record로 표현한다.
from dataclasses import dataclass
# statistics는 평균과 백분위 계산 전 정렬에 필요한 기본 통계를 제공한다.
from statistics import mean
# random은 재현 가능한 sensor jitter와 drop을 simulation한다.
import random


# order=True는 timestamp 기준 정렬과 비교 연산을 dataclass가 자동 생성한다.
@dataclass(frozen=True, order=True)
class Sample:
    """센서가 측정한 시각과 간단한 payload를 함께 보관한다."""

    # timestamp_ms는 host 수신 시각이 아니라 센서 측정 시각이다.
    timestamp_ms: float
    # sequence는 원래 sensor frame 순서를 추적하는 번호다.
    sequence: int
    # value는 예제 payload이며 실제로는 image, point cloud, IMU 등이 된다.
    value: float


# rate_hz, duration, jitter, drop을 받아 timestamp가 있는 stream을 만든다.
def simulate_stream(
    rate_hz: float,
    duration_ms: float,
    jitter_ms: float,
    drop_probability: float,
    clock_offset_ms: float,
    seed: int,
) -> list[Sample]:
    """고정 주기 sensor에 jitter, drop, clock offset을 적용한다."""

    # 입력 rate는 양수여야 period를 계산할 수 있다.
    if rate_hz <= 0.0:
        # ValueError는 호출자의 잘못된 실험 설정을 명확히 표시한다.
        raise ValueError("rate_hz must be positive")
    # default_rng 대신 표준 random.Random을 써 외부 package 없이 재현한다.
    generator = random.Random(seed)
    # 1초는 1000 ms이므로 센서 nominal period를 ms로 계산한다.
    period_ms = 1000.0 / rate_hz
    # 생성한 Sample을 순서대로 담을 빈 리스트다.
    samples: list[Sample] = []
    # sequence는 drop되더라도 원래 frame 번호를 유지한다.
    sequence = 0
    # nominal_time_ms는 jitter가 적용되기 전 센서의 이상적인 측정 시각이다.
    nominal_time_ms = 0.0
    # simulation duration 안의 모든 nominal frame을 생성한다.
    while nominal_time_ms < duration_ms:
        # random이 drop 확률 이상일 때만 현재 frame을 기록한다.
        if generator.random() >= drop_probability:
            # uniform은 양방향 jitter를 허용해 측정 시각 흔들림을 흉내 낸다.
            jitter = generator.uniform(-jitter_ms, jitter_ms)
            # timestamp에는 sensor clock offset과 현재 jitter를 모두 적용한다.
            timestamp_ms = nominal_time_ms + clock_offset_ms + jitter
            # payload는 sequence를 float로 바꾼 단순 관찰값이다.
            samples.append(Sample(timestamp_ms, sequence, float(sequence)))
        # drop 여부와 무관하게 원래 sensor sequence를 증가시킨다.
        sequence += 1
        # 다음 nominal sensor period로 이동한다.
        nominal_time_ms += period_ms
    # jitter 때문에 timestamp 순서가 바뀔 수 있어 측정 시각 기준으로 정렬한다.
    return sorted(samples)


# left와 right stream을 허용 time skew 안에서 greedy하게 짝짓는다.
def approximate_synchronize(
    left: list[Sample],
    right: list[Sample],
    tolerance_ms: float,
) -> tuple[list[tuple[Sample, Sample]], int, int]:
    """가장 가까운 순차 sample을 결합하고 양쪽 unmatched 수를 반환한다."""

    # 음수 tolerance는 의미가 없으므로 설정 오류로 처리한다.
    if tolerance_ms < 0.0:
        # 호출자가 즉시 설정을 고치도록 ValueError를 발생시킨다.
        raise ValueError("tolerance_ms must be non-negative")
    # 두 stream에서 결합된 sample pair를 저장한다.
    matches: list[tuple[Sample, Sample]] = []
    # left_index는 아직 처리하지 않은 left sample 위치다.
    left_index = 0
    # right_index는 아직 처리하지 않은 right sample 위치다.
    right_index = 0
    # 어느 한 stream이 끝날 때까지 두 현재 timestamp를 비교한다.
    while left_index < len(left) and right_index < len(right):
        # 양수 skew는 left가 right보다 나중 측정되었음을 뜻한다.
        skew_ms = left[left_index].timestamp_ms - right[right_index].timestamp_ms
        # 절대 time 차이가 tolerance 안이면 같은 물리 순간의 pair로 인정한다.
        if abs(skew_ms) <= tolerance_ms:
            # 현재 두 sample을 하나의 match로 기록한다.
            matches.append((left[left_index], right[right_index]))
            # 사용한 left sample 다음으로 이동한다.
            left_index += 1
            # 사용한 right sample 다음으로 이동한다.
            right_index += 1
        # left가 tolerance보다 너무 과거이면 앞으로도 현재 right와 맞지 않는다.
        elif skew_ms < -tolerance_ms:
            # 현재 left sample을 unmatched로 버리고 다음 left를 본다.
            left_index += 1
        # right가 tolerance보다 너무 과거인 대칭 상황이다.
        else:
            # 현재 right sample을 unmatched로 버리고 다음 right를 본다.
            right_index += 1
    # 각 stream 전체 수에서 match 수를 빼면 최종 unmatched 수가 된다.
    unmatched_left = len(left) - len(matches)
    # right에도 같은 pair 수를 사용했으므로 같은 방식으로 계산한다.
    unmatched_right = len(right) - len(matches)
    # pair 목록과 양쪽 drop 통계를 호출자에게 반환한다.
    return matches, unmatched_left, unmatched_right


# 정렬된 값과 0~100 percentile을 받아 nearest-rank 백분위를 계산한다.
def percentile(values: list[float], percentage: float) -> float:
    """외부 package 없이 작은 실습용 nearest-rank 백분위를 계산한다."""

    # 빈 값은 백분위를 정의할 수 없으므로 설정/데이터 오류다.
    if not values:
        # ValueError로 호출자가 match가 없는 상태를 처리하게 한다.
        raise ValueError("cannot compute percentile of an empty list")
    # percentage는 0과 100 사이여야 한다.
    if percentage < 0.0 or percentage > 100.0:
        # 허용 범위를 벗어난 입력을 즉시 거부한다.
        raise ValueError("percentage must be between 0 and 100")
    # sorted는 원본 리스트를 바꾸지 않고 오름차순 복사본을 만든다.
    ordered = sorted(values)
    # round 대신 nearest-rank와 유사하게 위쪽 index를 선택한다.
    index = int((percentage / 100.0) * (len(ordered) - 1))
    # 계산된 유효 index의 값을 반환한다.
    return ordered[index]


# match 목록을 사람이 검토하고 release gate에 넣을 통계로 바꾼다.
def summarize(matches: list[tuple[Sample, Sample]]) -> dict[str, float]:
    """pair의 절대 timestamp skew 평균, p95, 최대를 계산한다."""

    # pair가 하나도 없으면 잘못된 tolerance 또는 clock 상태다.
    if not matches:
        # 조용히 0을 반환하면 완벽한 동기화로 오해할 수 있어 예외를 낸다.
        raise ValueError("no synchronized pairs")
    # 각 pair의 절대 측정 시각 차이를 ms로 계산한다.
    absolute_skews = [
        abs(left.timestamp_ms - right.timestamp_ms)
        for left, right in matches
    ]
    # JSON 직렬화 가능한 float 통계를 dictionary로 반환한다.
    return {
        # matched_pairs는 float가 아니어도 되지만 통계 형식을 단순화해 float로 둔다.
        "matched_pairs": float(len(matches)),
        # mean은 모든 pair의 평균 time skew다.
        "mean_skew_ms": mean(absolute_skews),
        # p95는 대부분의 pair가 어느 time 차이 안인지 보여 준다.
        "p95_skew_ms": percentile(absolute_skews, 95.0),
        # max는 관찰된 최악의 time 차이다.
        "max_skew_ms": max(absolute_skews),
    }


# 직접 실행할 때만 camera와 LiDAR 예제 simulation을 수행한다.
if __name__ == "__main__":
    # 30 Hz camera stream을 2초 동안 ±1.5 ms jitter와 2% drop으로 만든다.
    camera = simulate_stream(30.0, 2000.0, 1.5, 0.02, 0.0, seed=1)
    # 10 Hz LiDAR에는 4 ms clock offset과 ±1 ms jitter를 적용한다.
    lidar = simulate_stream(10.0, 2000.0, 1.0, 0.0, 4.0, seed=2)
    # 8 ms tolerance 안에서 순차 camera와 LiDAR sample을 결합한다.
    pairs, camera_unmatched, lidar_unmatched = approximate_synchronize(
        camera,
        lidar,
        tolerance_ms=8.0,
    )
    # timestamp 품질 통계를 계산한다.
    statistics = summarize(pairs)
    # 생성된 두 stream의 전체 sample 수를 출력한다.
    print(f"camera={len(camera)} lidar={len(lidar)}")
    # 결합 수와 양쪽 unmatched 수를 출력한다.
    print(
        f"matched={len(pairs)} "
        f"camera_unmatched={camera_unmatched} "
        f"lidar_unmatched={lidar_unmatched}"
    )
    # 평균, p95, max skew dictionary를 출력한다.
    print(statistics)
