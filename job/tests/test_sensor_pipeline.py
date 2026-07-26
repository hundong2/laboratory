"""순수 NumPy 실습의 데이터 누수 방지와 학습 동작을 확인한다."""

# unittest는 Python 표준 라이브러리의 테스트 runner다.
import unittest
# sys는 test 실행 위치와 무관하게 job root를 module 검색 경로에 넣는 데 사용한다.
import sys
# Path는 현재 test 파일 위치에서 job root를 계산한다.
from pathlib import Path

# NumPy는 배열 값과 shape 검증에 사용한다.
import numpy as np

# 현재 파일의 부모 tests, 그 부모가 job root다.
JOB_ROOT = Path(__file__).resolve().parents[1]
# 저장소 root에서 실행해도 `src` package를 찾도록 job root를 앞에 넣는다.
if str(JOB_ROOT) not in sys.path:
    # insert(0, ...)은 설치된 동명 package보다 현재 실습 코드를 우선한다.
    sys.path.insert(0, str(JOB_ROOT))

# job 루트에서 `python -m unittest`로 실행할 때 src package의 공개 객체를 가져온다.
from src.sensor_pipeline import SoftmaxClassifier
# 같은 모듈에서 표준화 객체를 가져온다.
from src.sensor_pipeline import Standardizer
# 정확도 계산 함수를 가져온다.
from src.sensor_pipeline import accuracy
# 합성 데이터 생성 함수를 가져온다.
from src.sensor_pipeline import make_sensor_dataset
# softmax 함수를 가져온다.
from src.sensor_pipeline import softmax


# TestCase를 상속하면 assert 계열 검증 메서드를 사용할 수 있다.
class SensorPipelineTest(unittest.TestCase):
    """센서 분류 기준 pipeline의 핵심 불변 조건을 검사한다."""

    # test_ 접두사는 unittest가 자동으로 실행할 테스트 메서드라는 뜻이다.
    def test_softmax_rows_sum_to_one(self) -> None:
        """softmax의 각 샘플 확률 합이 1인지 확인한다."""

        # 서로 크기가 다른 두 샘플 logits를 만든다.
        logits = np.array([[1.0, 2.0, 3.0], [1000.0, 1001.0, 999.0]], dtype=np.float32)
        # 직접 구현한 softmax로 확률을 계산한다.
        probabilities = softmax(logits)
        # axis=1로 각 행의 확률 합을 계산한다.
        row_sums = probabilities.sum(axis=1)
        # assert_allclose는 부동소수점 오차 범위 안에서 모두 1인지 검사한다.
        np.testing.assert_allclose(row_sums, np.ones(2), atol=1e-6)

    # 두 번째 테스트는 실제 학습이 손실을 줄이고 충분한 정확도를 내는지 본다.
    def test_training_reaches_expected_accuracy(self) -> None:
        """작은 기준 모델이 보지 못한 합성 test에서 95% 이상인지 확인한다."""

        # 학습용 합성 데이터를 고정 seed로 만든다.
        train_x, train_y = make_sensor_dataset(samples_per_class=100, seed=1)
        # 독립 test 데이터를 다른 seed로 만든다.
        test_x, test_y = make_sensor_dataset(samples_per_class=40, seed=2)
        # 전처리 통계는 학습 입력에만 fit한다.
        standardizer = Standardizer.fit(train_x)
        # 모델 입력 특성 수와 출력 클래스 수를 명시한다.
        model = SoftmaxClassifier(input_dim=4, num_classes=3, seed=3)
        # 표준화한 학습 데이터로 250회 전체 배치 경사하강을 수행한다.
        losses = list(model.fit(standardizer.transform(train_x), train_y, epochs=250))
        # 마지막 loss가 첫 loss보다 작은지 확인한다.
        self.assertLess(losses[-1], losses[0])
        # test도 학습 통계로만 표준화한 뒤 정확도를 계산한다.
        score = accuracy(model.predict(standardizer.transform(test_x)), test_y)
        # 너무 낮은 정확도는 데이터·gradient·전처리 회귀를 뜻한다.
        self.assertGreaterEqual(score, 0.95)


# 파일을 직접 실행해도 unittest runner가 시작되게 한다.
if __name__ == "__main__":
    # verbosity=2는 각 테스트 이름과 결과를 자세히 표시한다.
    unittest.main(verbosity=2)
