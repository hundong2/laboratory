"""baseline과 candidate 보고서를 규칙에 따라 판정하는 자동 release gate."""

# argparse는 네 JSON 경로를 명령행 인수로 받는다.
import argparse
# json은 rule과 report를 읽고 판정 결과를 저장한다.
import json
# Path는 파일 경로와 부모 폴더 생성을 안전하게 처리한다.
from pathlib import Path
# Any는 JSON에서 읽은 여러 자료형의 dictionary 타입을 설명한다.
from typing import Any


# JSON object의 type alias로 긴 annotation 반복을 줄인다.
JsonObject = dict[str, Any]


# UTF-8 JSON 파일을 읽고 최상위 object인지 검사한다.
def load_json(path: Path) -> JsonObject:
    """지정 경로의 JSON object를 반환한다."""

    # with 문은 parsing 성공/실패와 관계없이 파일을 닫는다.
    with path.open("r", encoding="utf-8") as file:
        # load는 file object의 JSON 값을 Python 객체로 변환한다.
        value = json.load(file)
    # release rule과 report는 최상위 JSON object여야 한다.
    if not isinstance(value, dict):
        # list나 scalar를 받으면 key 기반 gate를 적용할 수 없으므로 거부한다.
        raise ValueError(f"{path} must contain a JSON object")
    # type checker가 JsonObject로 이해할 수 있는 dictionary를 반환한다.
    return value


# 중첩 key를 점으로 연결한 "metrics.p99_ms" 형식으로 조회한다.
def read_key(document: JsonObject, dotted_key: str) -> Any:
    """점으로 구분한 중첩 key의 값을 반환한다."""

    # 현재 탐색 위치를 최상위 document에서 시작한다.
    current: Any = document
    # split은 점마다 key path를 나눈다.
    for part in dotted_key.split("."):
        # 현재 위치가 object가 아니거나 key가 없으면 명확한 오류를 낸다.
        if not isinstance(current, dict) or part not in current:
            # KeyError에 전체 dotted path를 넣어 report 수정 위치를 알려 준다.
            raise KeyError(dotted_key)
        # 다음 중첩 값으로 이동한다.
        current = current[part]
    # 마지막 key의 실제 값을 반환한다.
    return current


# 최소/최대/회귀/Boolean rule을 모두 적용해 실패 사유 목록을 만든다.
def evaluate_release(
    rules: JsonObject,
    baseline: JsonObject,
    candidate: JsonObject,
) -> list[str]:
    """candidate가 모든 release rule을 만족하지 못한 이유를 반환한다."""

    # 실패가 없으면 최종적으로 빈 리스트가 된다.
    failures: list[str] = []
    # minimum object의 각 metric과 하한을 순회한다.
    for key, minimum in rules.get("minimum", {}).items():
        # candidate의 실제 값을 읽는다.
        actual = read_key(candidate, key)
        # 실제 값이 하한보다 작으면 실패 사유를 추가한다.
        if actual < minimum:
            # 메시지에 key, 실제 값, 요구 값을 모두 넣는다.
            failures.append(f"{key}={actual} is below minimum {minimum}")
    # maximum object의 각 metric과 상한을 순회한다.
    for key, maximum in rules.get("maximum", {}).items():
        # candidate의 실제 값을 읽는다.
        actual = read_key(candidate, key)
        # 실제 값이 상한보다 크면 실패다.
        if actual > maximum:
            # 실제 값과 상한을 실패 사유에 기록한다.
            failures.append(f"{key}={actual} exceeds maximum {maximum}")
    # max_drop_from_baseline은 높을수록 좋은 metric의 허용 하락 폭이다.
    for key, maximum_drop in rules.get("max_drop_from_baseline", {}).items():
        # baseline의 승인된 값을 읽는다.
        baseline_value = read_key(baseline, key)
        # candidate의 새 값을 읽는다.
        candidate_value = read_key(candidate, key)
        # baseline에서 candidate를 빼 실제 하락 폭을 계산한다.
        drop = baseline_value - candidate_value
        # 하락 폭이 허용값보다 크면 regression이다.
        if drop > maximum_drop:
            # 실제 drop과 허용 drop을 메시지에 기록한다.
            failures.append(f"{key} dropped by {drop}, allowed {maximum_drop}")
    # max_increase_from_baseline은 낮을수록 좋은 metric의 허용 증가 폭이다.
    for key, maximum_increase in rules.get("max_increase_from_baseline", {}).items():
        # baseline 값을 읽는다.
        baseline_value = read_key(baseline, key)
        # candidate 값을 읽는다.
        candidate_value = read_key(candidate, key)
        # candidate에서 baseline을 빼 악화된 증가 폭을 계산한다.
        increase = candidate_value - baseline_value
        # 허용 증가보다 크면 실패 사유를 추가한다.
        if increase > maximum_increase:
            # 실제 increase와 허용값을 기록한다.
            failures.append(f"{key} increased by {increase}, allowed {maximum_increase}")
    # required_true 목록은 evidence Boolean이 반드시 정확히 True여야 한다.
    for key in rules.get("required_true", []):
        # `is not True`는 1 같은 truthy 값도 잘못된 schema로 거부한다.
        if read_key(candidate, key) is not True:
            # 누락이 아닌 False evidence임을 명시한다.
            failures.append(f"{key} must be true")
    # required_nonempty는 version과 hardware 식별 정보가 빈 값이 아닌지 본다.
    for key in rules.get("required_nonempty", []):
        # 실제 값을 읽는다.
        value = read_key(candidate, key)
        # None, 빈 문자열, 빈 list/object는 release identity로 쓸 수 없다.
        if value is None or value == "" or value == [] or value == {}:
            # 어떤 field가 비었는지 실패 사유에 기록한다.
            failures.append(f"{key} must be non-empty")
    # 모든 rule의 실패 사유를 호출자에게 반환한다.
    return failures


# 명령행 경로 인수를 정의한다.
def parse_args() -> argparse.Namespace:
    """rule, baseline, candidate, output 경로를 읽는다."""

    # ArgumentParser는 help와 필수 인수 검사를 자동 제공한다.
    parser = argparse.ArgumentParser(description=__doc__)
    # --rules는 조직이 승인한 threshold JSON이다.
    parser.add_argument("--rules", type=Path, required=True)
    # --baseline은 현재 production release의 측정 report다.
    parser.add_argument("--baseline", type=Path, required=True)
    # --candidate는 새 release 후보의 같은 schema report다.
    parser.add_argument("--candidate", type=Path, required=True)
    # --output은 machine-readable 판정 결과를 저장할 경로다.
    parser.add_argument("--output", type=Path, required=True)
    # 실제 process 명령행을 parsing해 Namespace로 반환한다.
    return parser.parse_args()


# 파일을 읽고 gate를 적용하고 exit code를 결정한다.
def main() -> int:
    """release gate 결과를 JSON으로 저장하고 통과 0, 실패 2를 반환한다."""

    # 명령행 설정을 읽는다.
    args = parse_args()
    # 규칙 JSON을 읽는다.
    rules = load_json(args.rules)
    # production baseline report를 읽는다.
    baseline = load_json(args.baseline)
    # release candidate report를 읽는다.
    candidate = load_json(args.candidate)
    # 모든 rule을 적용해 실패 이유를 계산한다.
    failures = evaluate_release(rules, baseline, candidate)
    # 빈 실패 목록일 때만 passed가 True다.
    result = {
        # bool 변환으로 빈 리스트 True/False 의미를 뒤집어 통과 여부를 만든다.
        "passed": not failures,
        # 실패 사유 전체를 CI artifact에 남긴다.
        "failures": failures,
        # 어떤 model을 판정했는지 candidate version을 기록한다.
        "candidate_model_version": read_key(candidate, "identity.model_version"),
    }
    # output 부모 폴더가 없으면 생성한다.
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # UTF-8 쓰기 모드로 output 파일을 연다.
    with args.output.open("w", encoding="utf-8") as file:
        # indent=2로 code review와 CI log에서 읽기 쉽게 저장한다.
        json.dump(result, file, ensure_ascii=False, indent=2)
    # console에도 같은 결과를 출력한다.
    print(json.dumps(result, ensure_ascii=False, indent=2))
    # 통과는 0, gate 실패는 일반 실행 오류와 구분되는 2를 반환한다.
    return 0 if result["passed"] else 2


# import 때는 실행하지 않고 CLI로 호출할 때만 main을 시작한다.
if __name__ == "__main__":
    # SystemExit은 main의 정수 결과를 process exit code로 전달한다.
    raise SystemExit(main())
