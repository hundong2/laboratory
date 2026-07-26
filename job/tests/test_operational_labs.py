"""시간 동기화, 고장 경계, release gate의 핵심 정책을 자동 검증한다."""

# importlib.util은 숫자로 시작하는 실습 파일을 경로에서 module로 불러온다.
import importlib.util
# sys.modules 등록은 dataclass가 동적 module의 namespace를 찾게 한다.
import sys
# unittest는 Python 표준 test case와 assertion을 제공한다.
import unittest
# Path는 tests 폴더에서 job root와 lab 파일 경로를 계산한다.
from pathlib import Path
# ModuleType은 동적으로 읽은 module의 반환 타입을 설명한다.
from types import ModuleType


# 현재 tests 폴더의 부모가 job root다.
JOB_ROOT = Path(__file__).resolve().parents[1]


# 파일 이름과 안전한 module 이름을 받아 Python module로 실행한다.
def load_lab(file_name: str, module_name: str) -> ModuleType:
    """숫자로 시작하는 lab 파일을 import 가능한 module로 읽는다."""

    # spec_from_file_location은 module 이름과 실제 파일 경로를 연결한다.
    specification = importlib.util.spec_from_file_location(
        module_name,
        JOB_ROOT / "labs" / file_name,
    )
    # loader를 만들 수 없으면 test 환경 또는 경로가 잘못된 것이다.
    if specification is None or specification.loader is None:
        # RuntimeError로 test collection 단계에서 문제를 명확히 한다.
        raise RuntimeError(f"cannot load lab module: {file_name}")
    # module_from_spec은 spec에 맞는 빈 module object를 만든다.
    module = importlib.util.module_from_spec(specification)
    # dataclass decorator가 module annotation을 찾도록 exec 전에 등록한다.
    sys.modules[module_name] = module
    # exec_module은 lab 파일을 module namespace에서 실행한다.
    specification.loader.exec_module(module)
    # 함수와 class가 채워진 module을 반환한다.
    return module


# 세 실습 module을 test collection 때 한 번만 읽는다.
TIME_SYNC = load_lab("01_time_sync.py", "job_lab_time_sync")
# fault module도 고유 이름으로 읽는다.
FAULTS = load_lab("02_fault_injection.py", "job_lab_faults")
# release gate module을 고유 이름으로 읽는다.
RELEASE_GATE = load_lab("03_release_gate.py", "job_lab_release_gate")


# TestCase를 상속해 policy별 자동 검증을 정의한다.
class OperationalLabsTest(unittest.TestCase):
    """제품 경계의 핵심 실패 정책이 회귀하지 않게 한다."""

    # timestamp 차이가 tolerance 안/밖일 때 match 수를 확인한다.
    def test_time_synchronizer_drops_unmatched_samples(self) -> None:
        """동기화 tolerance 밖의 sample을 억지로 결합하지 않는다."""

        # left stream에는 0, 10, 20 ms sample 세 개를 만든다.
        left = [
            TIME_SYNC.Sample(0.0, 0, 0.0),
            TIME_SYNC.Sample(10.0, 1, 1.0),
            TIME_SYNC.Sample(20.0, 2, 2.0),
        ]
        # right는 앞의 두 sample만 2 ms 차이이고 마지막은 멀리 둔다.
        right = [
            TIME_SYNC.Sample(2.0, 0, 0.0),
            TIME_SYNC.Sample(12.0, 1, 1.0),
            TIME_SYNC.Sample(40.0, 2, 2.0),
        ]
        # tolerance 3 ms에서 앞의 두 pair만 결합한다.
        matches, unmatched_left, unmatched_right = TIME_SYNC.approximate_synchronize(
            left,
            right,
            3.0,
        )
        # 정확히 두 pair가 만들어져야 한다.
        self.assertEqual(len(matches), 2)
        # left의 20 ms sample 한 개가 unmatched다.
        self.assertEqual(unmatched_left, 1)
        # right의 40 ms sample 한 개도 unmatched다.
        self.assertEqual(unmatched_right, 1)

    # 정상 입력과 stale 입력의 accepted 상태를 확인한다.
    def test_safe_runner_rejects_stale_without_calling_model(self) -> None:
        """stale frame은 runtime 호출 전에 containment한다."""

        # 연속 실패 3회까지 허용하는 runner를 만든다.
        runner = FAULTS.SafeInferenceRunner(50.0, 100.0, 3)
        # model 호출 여부를 list 길이로 관찰한다.
        calls: list[tuple[float, ...]] = []

        # model 함수는 호출 입력을 기록하고 정상 score 세 개를 반환한다.
        def model(features: tuple[float, ...]) -> tuple[float, ...]:
            # 전달된 feature를 calls에 추가한다.
            calls.append(features)
            # class 1이 가장 높은 정상 score다.
            return (0.1, 0.8, 0.1)

        # 현재보다 100 ms 오래된 입력은 최대 age 50 ms를 넘는다.
        frame = FAULTS.SensorFrame(900.0, (0.0, 0.0, 0.0, 0.0))
        # now=1000 ms에서 stale 판정을 실행한다.
        result = runner.run(frame, 1000.0, model)
        # stale 결과는 accepted가 False다.
        self.assertFalse(result.accepted)
        # reason은 machine-readable stale_input이다.
        self.assertEqual(result.reason, "stale_input")
        # model은 한 번도 호출되지 않아야 한다.
        self.assertEqual(calls, [])

    # 연속 실패 한도 뒤 circuit이 열리는지 확인한다.
    def test_safe_runner_opens_circuit(self) -> None:
        """반복 invalid input 뒤 추가 runtime 호출을 차단한다."""

        # 두 번 연속 실패하면 breaker가 열리게 한다.
        runner = FAULTS.SafeInferenceRunner(50.0, 100.0, 2)
        # 정상 형태를 돌려주는 단순 model 함수다.
        model = lambda features: (0.1, 0.8, 0.1)
        # wrong shape 첫 입력으로 실패 수를 1로 만든다.
        runner.run(FAULTS.SensorFrame(999.0, (0.0,)), 1000.0, model)
        # wrong shape 두 번째 입력으로 실패 수를 한도까지 올린다.
        runner.run(FAULTS.SensorFrame(999.0, (0.0,)), 1000.0, model)
        # 이후 정상 shape도 circuit_open으로 거부되어야 한다.
        result = runner.run(
            FAULTS.SensorFrame(999.0, (0.0, 0.0, 0.0, 0.0)),
            1000.0,
            model,
        )
        # breaker 상태에서는 accepted가 False다.
        self.assertFalse(result.accepted)
        # 명확한 circuit_open reason을 확인한다.
        self.assertEqual(result.reason, "circuit_open")

    # release rule을 만족하는 candidate가 통과하는지 본다.
    def test_release_gate_passes_complete_candidate(self) -> None:
        """모든 metric과 evidence가 좋은 candidate를 승인한다."""

        # 최소, 최대, Boolean evidence를 포함한 작은 rule set이다.
        rules = {
            "minimum": {"quality.recall": 0.98},
            "maximum": {"runtime.p99_ms": 20.0},
            "required_true": ["evidence.rollback"],
            "required_nonempty": ["identity.model_version"],
        }
        # baseline은 현재 production 비교값이다.
        baseline = {
            "quality": {"recall": 0.99},
            "runtime": {"p99_ms": 15.0},
        }
        # candidate는 모든 독립 rule을 만족한다.
        candidate = {
            "identity": {"model_version": "candidate-1"},
            "quality": {"recall": 0.99},
            "runtime": {"p99_ms": 16.0},
            "evidence": {"rollback": True},
        }
        # 실패 사유가 빈 리스트인지 확인한다.
        self.assertEqual(
            RELEASE_GATE.evaluate_release(rules, baseline, candidate),
            [],
        )

    # 위험 class recall과 rollback evidence가 나쁘면 동시에 실패해야 한다.
    def test_release_gate_reports_multiple_failures(self) -> None:
        """release gate가 첫 오류에서 멈추지 않고 모든 실패를 수집한다."""

        # recall 하한과 rollback evidence를 요구한다.
        rules = {
            "minimum": {"quality.recall": 0.98},
            "required_true": ["evidence.rollback"],
        }
        # baseline은 이 rule에서 직접 비교하지 않지만 함수 계약상 object를 전달한다.
        baseline: dict[str, object] = {}
        # candidate는 recall과 rollback이 모두 기준 미달이다.
        candidate = {
            "quality": {"recall": 0.90},
            "evidence": {"rollback": False},
        }
        # 모든 rule을 적용한다.
        failures = RELEASE_GATE.evaluate_release(rules, baseline, candidate)
        # 두 개의 독립 실패 사유가 모두 보고되어야 한다.
        self.assertEqual(len(failures), 2)


# 파일을 직접 실행할 때도 상세 unittest runner를 시작한다.
if __name__ == "__main__":
    # verbosity=2는 각 policy test 이름과 결과를 표시한다.
    unittest.main(verbosity=2)
