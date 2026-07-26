"""PyTorch checkpoint를 ONNX로 내보내고 INT8 양자화와 acceptance gate를 실행한다."""

# argparse는 모델 경로와 benchmark 반복 수를 명령행에서 바꾸게 한다.
import argparse
# json은 메타데이터와 benchmark 보고서를 읽고 쓰는 데 사용한다.
import json
# perf_counter_ns는 wall-clock 변경과 무관한 추론 경과 시간을 측정한다.
from time import perf_counter_ns
# Path는 입력과 출력 파일 경로를 운영체제 독립적으로 다룬다.
from pathlib import Path

# NumPy는 ONNX Runtime 입력과 출력 비교, 백분위 계산을 담당한다.
import numpy as np
# onnx는 내보낸 그래프의 형식 유효성을 검사한다.
import onnx
# onnxruntime은 ONNX 모델을 Python에서 실행한다.
import onnxruntime as ort
# torch는 checkpoint를 읽고 원본 모델 출력을 계산한다.
import torch
# QuantType은 양자화된 weight 자료형을 지정한다.
from onnxruntime.quantization import QuantType
# quantize_dynamic은 calibration 없이 실행 시 weight를 INT8로 변환한다.
from onnxruntime.quantization import quantize_dynamic

# 같은 폴더의 모델 구조를 import해 checkpoint의 state_dict를 복원한다.
from fine_tune import TinySensorNet


# model을 지정한 artifact 폴더로 export하고 두 ONNX 경로를 반환한다.
def export_and_quantize(artifact_dir: Path) -> tuple[Path, Path]:
    """PyTorch→ONNX export, checker, 동적 INT8 양자화를 순서대로 수행한다."""

    # 학습 checkpoint 파일 경로를 만든다.
    checkpoint_path = artifact_dir / "sensor_model.pt"
    # weights_only=True는 pickle 기반 임의 객체 복원을 제한해 안전성을 높인다.
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
    # 저장된 클래스 수로 학습 때와 같은 모델 구조를 만든다.
    model = TinySensorNet(num_classes=int(checkpoint["num_classes"]))
    # state_dict의 학습 가중치를 새 모델 객체에 복사한다.
    model.load_state_dict(checkpoint["model_state"])
    # eval은 export 중 모델을 평가 동작으로 고정한다.
    model.eval()
    # zeros는 batch 1, 특성 4의 export 예제 입력을 만든다.
    example_input = torch.zeros(1, 4, dtype=torch.float32)
    # FP32 ONNX 모델을 저장할 경로다.
    fp32_path = artifact_dir / "sensor_model.onnx"
    # torch.onnx.export가 실제 계산 그래프와 parameter를 ONNX 파일로 직렬화한다.
    torch.onnx.export(
        # 첫 인수는 export할 PyTorch 모델이다.
        model,
        # 두 번째 인수는 그래프를 추적할 대표 입력 tuple이다.
        (example_input,),
        # f는 생성할 ONNX 파일 경로다.
        f=fp32_path,
        # input_names는 C++에서 조회할 입력 tensor 이름을 고정한다.
        input_names=["sensor_features"],
        # output_names는 C++에서 조회할 출력 tensor 이름을 고정한다.
        output_names=["class_logits"],
        # 첫 batch 축을 가변으로 선언해 여러 샘플도 한 번에 처리하게 한다.
        dynamic_axes={"sensor_features": {0: "batch"}, "class_logits": {0: "batch"}},
        # opset 17은 여러 현재 런타임에서 널리 지원되는 ONNX 연산자 집합이다.
        opset_version=17,
        # dynamo=False는 작은 교육 예제에서 전통적인 안정 export 경로를 명시한다.
        dynamo=False,
    )
    # load는 방금 생성한 ONNX protobuf를 메모리로 읽는다.
    onnx_model = onnx.load(fp32_path)
    # checker는 shape, type, graph 연결이 ONNX 규격에 맞지 않으면 예외를 낸다.
    onnx.checker.check_model(onnx_model)
    # INT8 weight를 가진 ONNX 파일 경로다.
    int8_path = artifact_dir / "sensor_model.int8.onnx"
    # 동적 양자화는 이 Linear 중심 모델의 weight를 calibration 없이 줄인다.
    quantize_dynamic(
        # model_input은 원본 FP32 ONNX 경로다.
        model_input=fp32_path,
        # model_output은 양자화 결과 경로다.
        model_output=int8_path,
        # QInt8은 signed 8-bit 정수 weight를 사용한다.
        weight_type=QuantType.QInt8,
    )
    # 두 파일 경로를 이후 동등성 검사와 benchmark에 반환한다.
    return fp32_path, int8_path


# path의 ONNX 모델을 CPUExecutionProvider로 실행할 Session을 만든다.
def make_session(path: Path) -> ort.InferenceSession:
    """CPU 기준 ONNX Runtime session을 생성한다."""

    # SessionOptions는 그래프 최적화와 스레드 같은 session 설정을 담는다.
    options = ort.SessionOptions()
    # ORT_ENABLE_ALL은 사용 가능한 기본·확장·layout 최적화를 활성화한다.
    options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    # providers를 명시하면 개발 PC의 다른 가속기가 결과에 몰래 개입하지 않는다.
    return ort.InferenceSession(path, sess_options=options, providers=["CPUExecutionProvider"])


# 같은 입력을 원본 PyTorch와 ONNX에 넣고 최대 절대 오차를 반환한다.
def compare_outputs(model_path: Path, checkpoint_path: Path) -> float:
    """export가 계산 의미를 보존했는지 고정 난수 입력으로 확인한다."""

    # checkpoint를 CPU에 안전하게 불러온다.
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
    # checkpoint와 동일한 출력 클래스 수의 모델을 만든다.
    model = TinySensorNet(num_classes=int(checkpoint["num_classes"]))
    # 학습된 parameter를 모델에 복원한다.
    model.load_state_dict(checkpoint["model_state"])
    # 원본 모델을 평가 모드로 바꾼다.
    model.eval()
    # manual_seed로 비교 입력이 반복 실행마다 같게 한다.
    generator = torch.Generator().manual_seed(123)
    # randn은 batch 16의 표준화된 센서 입력을 흉내 낸다.
    torch_input = torch.randn(16, 4, generator=generator)
    # inference_mode는 원본 출력 계산에서 gradient 기록을 끈다.
    with torch.inference_mode():
        # detach 후 numpy로 바꾸어 런타임 출력과 같은 자료 구조로 만든다.
        torch_output = model(torch_input).numpy()
    # FP32 ONNX 모델을 실행할 session을 만든다.
    session = make_session(model_path)
    # run의 None은 모든 출력을 요청하고 dictionary는 이름별 입력을 제공한다.
    ort_output = session.run(None, {"sensor_features": torch_input.numpy()})[0]
    # abs 차이의 최댓값은 두 구현의 가장 큰 logits 오차다.
    return float(np.max(np.abs(torch_output - ort_output)))


# session, 입력, 반복 수를 받아 warm-up 이후 latency 백분위를 계산한다.
def benchmark(
    session: ort.InferenceSession,
    sample: np.ndarray,
    repeats: int,
) -> dict[str, float]:
    """단일 샘플 ONNX 추론의 p50, p95, p99를 밀리초로 계산한다."""

    # 30회 warm-up으로 session 초기화와 cache 효과를 본 측정에서 덜어 낸다.
    for _ in range(30):
        # 출력값은 버리지만 추론 연산은 실제 수행한다.
        session.run(None, {"sensor_features": sample})
    # 각 반복 경과 시간을 저장할 빈 리스트다.
    elapsed_ms: list[float] = []
    # 충분한 표본으로 tail latency를 관찰한다.
    for _ in range(repeats):
        # monotonic 고해상도 시작 시각을 읽는다.
        started_ns = perf_counter_ns()
        # 한 건의 실제 ONNX 추론을 실행한다.
        session.run(None, {"sensor_features": sample})
        # 나노초 차이를 밀리초로 바꿔 목록에 추가한다.
        elapsed_ms.append((perf_counter_ns() - started_ns) / 1_000_000.0)
    # percentile 결과를 JSON에 저장 가능한 Python float로 바꾼다.
    return {
        "p50_ms": float(np.percentile(elapsed_ms, 50)),
        "p95_ms": float(np.percentile(elapsed_ms, 95)),
        "p99_ms": float(np.percentile(elapsed_ms, 99)),
    }


# 명령행 옵션을 정의하고 Namespace로 반환한다.
def parse_args() -> argparse.Namespace:
    """artifact·report 폴더와 benchmark 반복 수를 읽는다."""

    # ArgumentParser가 --help와 type 검사를 제공한다.
    parser = argparse.ArgumentParser(description=__doc__)
    # 학습 산출물이 있는 기본 폴더는 job/artifacts다.
    parser.add_argument("--artifact-dir", type=Path, default=Path("artifacts"))
    # benchmark JSON을 저장할 기본 폴더는 job/reports다.
    parser.add_argument("--report-dir", type=Path, default=Path("reports"))
    # p99를 보기 위한 반복 수는 기본 500회다.
    parser.add_argument("--repeats", type=int, default=500)
    # 실제 명령행을 읽어 반환한다.
    return parser.parse_args()


# export, 비교, benchmark, acceptance gate를 한 번에 수행한다.
def main() -> None:
    """배포 산출물을 만들고 품질·크기·속도 보고서를 저장한다."""

    # 명령행 설정을 읽는다.
    args = parse_args()
    # report 폴더가 없으면 부모까지 생성한다.
    args.report_dir.mkdir(parents=True, exist_ok=True)
    # FP32와 INT8 ONNX 모델을 생성한다.
    fp32_path, int8_path = export_and_quantize(args.artifact_dir)
    # PyTorch와 FP32 ONNX logits의 최대 절대 오차를 계산한다.
    maximum_absolute_error = compare_outputs(fp32_path, args.artifact_dir / "sensor_model.pt")
    # 고정된 표준화 입력 한 건을 contiguous float32 배열로 만든다.
    sample = np.array([[0.0, 0.0, 0.0, 0.0]], dtype=np.float32)
    # FP32 모델 session을 생성한다.
    fp32_session = make_session(fp32_path)
    # INT8 모델 session을 생성한다.
    int8_session = make_session(int8_path)
    # 같은 입력에서 두 ONNX 모델의 logits를 계산한다.
    fp32_output = fp32_session.run(None, {"sensor_features": sample})[0]
    # 양자화 모델의 logits도 계산한다.
    int8_output = int8_session.run(None, {"sensor_features": sample})[0]
    # 양자화로 생긴 단일 검증 입력의 최대 logits 차이를 계산한다.
    quantized_maximum_absolute_error = float(np.max(np.abs(fp32_output - int8_output)))
    # 파일 크기는 stat의 byte 수로 측정한다.
    fp32_size = fp32_path.stat().st_size
    # INT8 파일 크기도 byte 단위로 측정한다.
    int8_size = int8_path.stat().st_size
    # 모든 측정값과 명시적인 통과 기준을 한 JSON 객체에 모은다.
    report = {
        "environment_note": "이 결과는 실행한 장치에만 유효하며 실제 배포 장치에서 다시 측정해야 한다.",
        "pytorch_vs_onnx_max_abs_error": maximum_absolute_error,
        "fp32_vs_int8_sample_max_abs_error": quantized_maximum_absolute_error,
        "fp32_size_bytes": fp32_size,
        "int8_size_bytes": int8_size,
        "size_ratio_int8_over_fp32": int8_size / fp32_size,
        "fp32_latency": benchmark(fp32_session, sample, args.repeats),
        "int8_latency": benchmark(int8_session, sample, args.repeats),
        "gates": {
            "pytorch_vs_onnx_error_below_1e-4": maximum_absolute_error < 1e-4,
            "int8_file_created": int8_path.is_file(),
        },
    }
    # benchmark 보고서 파일 경로를 만든다.
    report_path = args.report_dir / "benchmark.json"
    # UTF-8 쓰기 모드로 보고서 파일을 연다.
    with report_path.open("w", encoding="utf-8") as file:
        # indent=2로 사람이 검토하기 쉬운 JSON을 저장한다.
        json.dump(report, file, ensure_ascii=False, indent=2)
    # 전체 보고서를 콘솔에도 출력한다.
    print(json.dumps(report, ensure_ascii=False, indent=2))
    # 필수 export 동등성 gate가 실패하면 CI가 감지하도록 예외를 낸다.
    if not report["gates"]["pytorch_vs_onnx_error_below_1e-4"]:
        # RuntimeError 메시지에 실제 오차를 포함한다.
        raise RuntimeError(f"PyTorch/ONNX output mismatch: {maximum_absolute_error}")


# 직접 실행할 때만 export pipeline을 시작한다.
if __name__ == "__main__":
    # 전체 배포 산출물 생성과 검증을 실행한다.
    main()
