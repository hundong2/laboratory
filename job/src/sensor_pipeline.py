"""외부 데이터 없이 전처리와 작은 softmax 분류기를 연습하는 순수 NumPy 모듈."""

# dataclass는 평균과 표준편차를 한 객체로 묶어 주는 표준 라이브러리 기능이다.
from dataclasses import dataclass
# perf_counter_ns는 시스템 시계 변경의 영향을 받지 않는 고해상도 경과 시간 측정 함수다.
from time import perf_counter_ns
# Iterable은 함수가 여러 학습 손실값을 반환한다는 타입 설명에 사용한다.
from typing import Iterable

# NumPy는 벡터와 행렬 계산을 담당한다.
import numpy as np


# frozen=True는 생성 뒤 평균과 표준편차 참조를 다른 객체로 바꾸지 못하게 한다.
@dataclass(frozen=True)
class Standardizer:
    """학습 데이터에서 얻은 통계로 입력을 표준화한다."""

    # mean은 각 센서 특성의 학습 데이터 평균이다.
    mean: np.ndarray
    # std는 각 센서 특성의 학습 데이터 표준편차다.
    std: np.ndarray

    # cls를 받는 classmethod이므로 Standardizer.fit(x) 형태로 호출할 수 있다.
    @classmethod
    def fit(cls, x: np.ndarray) -> "Standardizer":
        """학습 데이터만 사용해 평균과 표준편차를 계산한다."""

        # axis=0은 행들을 모아 각 열, 즉 각 센서 특성의 평균을 계산한다.
        mean = x.mean(axis=0, keepdims=True)
        # 표준편차도 열별로 계산하며 keepdims=True로 shape를 (1, 특성 수)로 유지한다.
        std = x.std(axis=0, keepdims=True)
        # 1e-6보다 작은 표준편차를 1로 바꾸어 0으로 나누는 문제를 막는다.
        safe_std = np.where(std < 1e-6, 1.0, std)
        # 계산한 두 배열을 가진 불변 Standardizer 객체를 반환한다.
        return cls(mean=mean, std=safe_std)

    # self는 fit으로 만든 통계를, x는 변환할 새 입력을 뜻한다.
    def transform(self, x: np.ndarray) -> np.ndarray:
        """학습 통계를 이용해 새 입력을 평균 0, 표준편차 1에 가깝게 바꾼다."""

        # broadcasting으로 모든 행에 같은 학습 평균과 표준편차를 적용한다.
        return (x - self.mean) / self.std


# samples_per_class는 클래스당 샘플 수, shift는 새 장치의 센서 편향을 흉내 낸다.
def make_sensor_dataset(
    samples_per_class: int = 120,
    seed: int = 7,
    shift: float = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    """정상·주의·정지 필요의 세 상태를 나타내는 합성 센서 데이터를 만든다."""

    # default_rng는 같은 seed에서 같은 데이터를 재현하는 지역 난수 생성기다.
    rng = np.random.default_rng(seed)
    # 각 행은 진동, 온도 변화, 전류, 회전 오차의 클래스 중심값을 나타낸다.
    centers = np.array(
        [
            [0.15, 0.10, 0.20, 0.10],
            [0.55, 0.45, 0.50, 0.40],
            [0.90, 0.85, 0.80, 0.95],
        ],
        dtype=np.float32,
    )
    # 새 장치에서 네 센서가 조금씩 다르게 치우치는 현상을 벡터로 표현한다.
    device_shift = np.array([shift, -shift * 0.5, shift * 0.25, shift], dtype=np.float32)
    # 클래스별 입력 배열을 모을 빈 Python 리스트다.
    feature_blocks: list[np.ndarray] = []
    # 클래스별 정답 배열을 모을 빈 Python 리스트다.
    label_blocks: list[np.ndarray] = []
    # enumerate는 중심 벡터와 동시에 0, 1, 2 클래스 번호를 만든다.
    for class_id, center in enumerate(centers):
        # normal은 center 주변에 표준편차 0.08인 센서 잡음을 만든다.
        block = rng.normal(
            loc=center + device_shift,
            scale=0.08,
            size=(samples_per_class, centers.shape[1]),
        ).astype(np.float32)
        # clip은 합성 센서값을 예제의 유효 범위 0~1.2 안으로 제한한다.
        block = np.clip(block, 0.0, 1.2)
        # 현재 클래스의 입력 블록을 전체 입력 목록에 추가한다.
        feature_blocks.append(block)
        # full은 현재 블록의 모든 행에 같은 class_id 정답을 붙인다.
        label_blocks.append(np.full(samples_per_class, class_id, dtype=np.int64))
    # concatenate는 세 입력 블록을 행 방향의 한 배열로 합친다.
    x = np.concatenate(feature_blocks, axis=0)
    # 정답 블록도 한 개의 1차원 배열로 합친다.
    y = np.concatenate(label_blocks, axis=0)
    # permutation은 입력과 정답을 같은 순서로 섞기 위한 행 인덱스를 만든다.
    order = rng.permutation(len(y))
    # 섞인 인덱스를 두 배열에 똑같이 적용해 입력-정답 대응을 유지한다.
    return x[order], y[order]


# logits는 모델이 낸 정규화 전 점수 행렬이다.
def softmax(logits: np.ndarray) -> np.ndarray:
    """각 행의 점수를 합이 1인 클래스 확률로 바꾼다."""

    # 행별 최댓값을 빼면 exp에서 매우 큰 수가 생기는 수치 overflow를 줄인다.
    stable_logits = logits - logits.max(axis=1, keepdims=True)
    # exp는 각 안정화 점수에 자연상수 e의 지수 함수를 적용한다.
    exp_values = np.exp(stable_logits)
    # 각 행을 그 행의 합으로 나누어 모든 클래스 확률의 합을 1로 만든다.
    return exp_values / exp_values.sum(axis=1, keepdims=True)


class SoftmaxClassifier:
    """행렬곱 하나로 동작해 C++ 이식 원리를 쉽게 볼 수 있는 기준 모델."""

    # 입력 특성 수, 출력 클래스 수, 난수 seed를 받아 작은 가중치를 초기화한다.
    def __init__(self, input_dim: int, num_classes: int, seed: int = 11) -> None:
        # 이 객체만 쓰는 난수 생성기를 만들어 전역 난수 상태를 오염시키지 않는다.
        rng = np.random.default_rng(seed)
        # normal로 입력 특성×클래스 shape의 작은 초기 가중치를 만든다.
        self.weights = rng.normal(0.0, 0.01, size=(input_dim, num_classes)).astype(np.float32)
        # bias는 클래스마다 하나이며 처음에는 모두 0이다.
        self.bias = np.zeros((1, num_classes), dtype=np.float32)

    # x의 각 행에 같은 weights와 bias를 적용한다.
    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        """입력 배치의 클래스별 확률을 반환한다."""

        # @는 (배치, 특성)과 (특성, 클래스)의 행렬곱을 수행한다.
        logits = x @ self.weights + self.bias
        # softmax로 정규화된 확률을 호출자에게 돌려준다.
        return softmax(logits)

    # argmax는 각 행에서 가장 큰 확률의 열 번호를 선택한다.
    def predict(self, x: np.ndarray) -> np.ndarray:
        """입력 배치의 가장 가능성 높은 클래스 번호를 반환한다."""

        # axis=1은 각 샘플 행 안에서 클래스 열을 비교한다는 뜻이다.
        return self.predict_proba(x).argmax(axis=1)

    # 학습 데이터, 정답, 반복 수, 학습률을 받아 경사하강법을 수행한다.
    def fit(
        self,
        x: np.ndarray,
        y: np.ndarray,
        epochs: int = 250,
        learning_rate: float = 0.08,
    ) -> Iterable[float]:
        """cross-entropy를 최소화하도록 가중치와 bias를 갱신한다."""

        # 입력 행 수는 gradient를 평균낼 때 사용한다.
        sample_count = x.shape[0]
        # identity matrix에서 y에 해당하는 행을 골라 one-hot 정답을 만든다.
        one_hot = np.eye(self.bias.shape[1], dtype=np.float32)[y]
        # epoch별 손실을 학습 곡선으로 확인할 수 있게 저장한다.
        losses: list[float] = []
        # range(epochs)는 0부터 epochs-1까지 같은 전체 배치 학습을 반복한다.
        for _ in range(epochs):
            # 현재 가중치로 모든 학습 샘플의 확률을 계산한다.
            probabilities = self.predict_proba(x)
            # clip은 log(0)이 음의 무한대가 되는 것을 막는다.
            safe_probabilities = np.clip(probabilities, 1e-7, 1.0)
            # one-hot 정답 위치의 음의 로그 확률을 평균내 cross-entropy를 구한다.
            loss = -np.sum(one_hot * np.log(safe_probabilities)) / sample_count
            # float로 바꾸면 NumPy scalar가 아닌 일반 Python 값으로 기록된다.
            losses.append(float(loss))
            # softmax+cross-entropy의 logits gradient는 예측 확률-정답이다.
            gradient_logits = (probabilities - one_hot) / sample_count
            # 전치한 입력과 logits gradient의 행렬곱으로 가중치 gradient를 구한다.
            gradient_weights = x.T @ gradient_logits
            # 모든 샘플의 logits gradient를 더해 bias gradient를 구한다.
            gradient_bias = gradient_logits.sum(axis=0, keepdims=True)
            # 학습률을 곱한 gradient를 빼서 손실이 감소하는 방향으로 weights를 이동한다.
            self.weights -= learning_rate * gradient_weights
            # bias도 같은 경사하강 규칙으로 갱신한다.
            self.bias -= learning_rate * gradient_bias
        # 전체 손실 목록을 반환해 수렴 여부를 확인하게 한다.
        return losses


# predictions와 targets는 같은 길이의 클래스 번호 배열이어야 한다.
def accuracy(predictions: np.ndarray, targets: np.ndarray) -> float:
    """전체 샘플 중 예측이 맞은 비율을 계산한다."""

    # 비교 결과 Boolean 배열의 평균은 True 비율과 같으므로 정확도가 된다.
    return float((predictions == targets).mean())


# classifier와 한 건 입력을 받아 반복 추론 시간의 백분위를 측정한다.
def benchmark_latency_ms(
    classifier: SoftmaxClassifier,
    sample: np.ndarray,
    repeats: int = 500,
) -> dict[str, float]:
    """warm-up 뒤 단일 샘플 추론의 p50, p95, p99 밀리초를 반환한다."""

    # 20회 사전 실행은 첫 호출의 cache와 초기화 비용을 측정에서 덜어 낸다.
    for _ in range(20):
        # 결과를 사용하지 않아도 실제 NumPy 연산은 수행된다.
        classifier.predict_proba(sample)
    # 각 반복의 경과 시간을 밀리초로 저장할 빈 리스트다.
    elapsed_ms: list[float] = []
    # repeats만큼 같은 단일 입력을 실행해 분포를 만든다.
    for _ in range(repeats):
        # 시작 시각을 나노초 단위 monotonic clock으로 읽는다.
        started_ns = perf_counter_ns()
        # 측정 대상인 실제 추론 함수를 한 번 실행한다.
        classifier.predict_proba(sample)
        # 종료 시각에서 시작 시각을 빼고 1,000,000으로 나누어 ms로 바꾼다.
        elapsed_ms.append((perf_counter_ns() - started_ns) / 1_000_000.0)
    # percentile은 긴 꼬리를 포함한 대표 지연시간 세 값을 계산한다.
    return {
        "p50_ms": float(np.percentile(elapsed_ms, 50)),
        "p95_ms": float(np.percentile(elapsed_ms, 95)),
        "p99_ms": float(np.percentile(elapsed_ms, 99)),
    }


# 이 파일을 직접 실행할 때만 아래 데모가 동작하게 하는 Python 표준 진입점 조건이다.
if __name__ == "__main__":
    # seed가 고정된 학습용 합성 센서 데이터를 만든다.
    train_x, train_y = make_sensor_dataset(samples_per_class=120, seed=7)
    # 다른 seed의 데이터로 보지 못한 test set을 만든다.
    test_x, test_y = make_sensor_dataset(samples_per_class=40, seed=99)
    # 학습 입력에만 fit하여 test 정보가 전처리에 새지 않게 한다.
    standardizer = Standardizer.fit(train_x)
    # 학습과 test에 동일한 학습 통계를 적용한다.
    normalized_train_x = standardizer.transform(train_x)
    # test 입력도 학습 평균과 표준편차로 변환한다.
    normalized_test_x = standardizer.transform(test_x)
    # 특성 네 개와 클래스 세 개를 가진 선형 softmax 모델을 만든다.
    model = SoftmaxClassifier(input_dim=4, num_classes=3)
    # 전체 배치 경사하강법으로 기준 모델을 학습한다.
    training_losses = list(model.fit(normalized_train_x, train_y))
    # 보지 못한 test set의 정확도를 계산한다.
    test_accuracy = accuracy(model.predict(normalized_test_x), test_y)
    # test 첫 샘플 한 건의 추론 지연시간 분포를 측정한다.
    latency = benchmark_latency_ms(model, normalized_test_x[:1])
    # 첫 손실과 마지막 손실을 표시해 학습 방향이 맞는지 확인한다.
    print(f"loss: {training_losses[0]:.4f} -> {training_losses[-1]:.4f}")
    # 정확도를 소수점 넷째 자리까지 표시한다.
    print(f"test accuracy: {test_accuracy:.4f}")
    # latency dictionary를 그대로 표시해 p50/p95/p99를 비교한다.
    print(f"latency: {latency}")
