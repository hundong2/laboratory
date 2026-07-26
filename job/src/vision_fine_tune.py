"""실제 ImageFolder 데이터로 MobileNetV3-Small을 두 단계 파인튜닝하고 ONNX로 내보낸다."""

# argparse는 dataset과 epoch 설정을 명령행 인수로 받는다.
import argparse
# copy는 validation 최고 model state를 독립 복사하는 데 사용한다.
import copy
# json은 C++ 전처리와 class map metadata를 저장한다.
import json
# random은 Python 난수 seed를 고정한다.
import random
# Path는 train/val/test와 artifact 경로를 안전하게 결합한다.
from pathlib import Path

# NumPy seed를 고정해 transform 외 실험 변동을 줄인다.
import numpy as np
# torch는 tensor, 자동 미분, checkpoint, ONNX export를 제공한다.
import torch
# nn은 CrossEntropyLoss와 Linear 같은 신경망 구성 요소를 제공한다.
from torch import nn
# DataLoader는 image dataset을 mini-batch로 읽는다.
from torch.utils.data import DataLoader
# datasets는 폴더 이름을 class로 해석하는 ImageFolder를 제공한다.
from torchvision import datasets
# MobileNet_V3_Small_Weights는 공식 사전학습 weight와 전처리 정보를 제공한다.
from torchvision.models import MobileNet_V3_Small_Weights
# mobilenet_v3_small은 mobile/edge용 depthwise convolution 기반 모델 구조를 만든다.
from torchvision.models import mobilenet_v3_small


# 세 난수 계층에 같은 seed를 적용한다.
def set_seed(seed: int) -> None:
    """Python, NumPy, PyTorch의 기본 난수 순서를 고정한다."""

    # Python 표준 random 순서를 고정한다.
    random.seed(seed)
    # NumPy 전역 난수 순서를 고정한다.
    np.random.seed(seed)
    # PyTorch CPU 난수 순서를 고정한다.
    torch.manual_seed(seed)
    # CUDA가 있으면 모든 GPU의 난수 seed도 고정한다.
    if torch.cuda.is_available():
        # manual_seed_all은 visible CUDA device 전체에 seed를 적용한다.
        torch.cuda.manual_seed_all(seed)


# dataset root, transform, batch, shuffle을 받아 loader를 만든다.
def make_loader(
    split_path: Path,
    transform: object,
    batch_size: int,
    shuffle: bool,
    workers: int,
) -> tuple[DataLoader, datasets.ImageFolder]:
    """ImageFolder와 DataLoader를 만들고 class mapping 검사용 dataset도 반환한다."""

    # ImageFolder는 `split/class_name/image.jpg` 구조에서 class index를 만든다.
    dataset = datasets.ImageFolder(split_path, transform=transform)
    # pin_memory는 CUDA로 batch를 복사할 때 page-locked memory를 사용하게 한다.
    use_pinned_memory = torch.cuda.is_available()
    # DataLoader가 batch, shuffle, worker process를 관리한다.
    loader = DataLoader(
        # dataset은 path와 label을 제공하는 ImageFolder다.
        dataset,
        # batch_size는 한 optimizer step에 처리할 image 수다.
        batch_size=batch_size,
        # train만 shuffle해 batch 순서 편향을 줄인다.
        shuffle=shuffle,
        # num_workers는 image decode/transform 병렬 process 수다.
        num_workers=workers,
        # pin_memory는 GPU 사용 때만 켠다.
        pin_memory=use_pinned_memory,
        # 마지막 작은 batch도 평가와 학습 데이터에 포함한다.
        drop_last=False,
    )
    # loader와 class_to_idx를 가진 dataset을 함께 반환한다.
    return loader, dataset


# model, loader, optimizer, loss, device를 받아 한 epoch를 학습한다.
def train_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    loss_function: nn.Module,
    device: torch.device,
) -> float:
    """한 epoch의 sample당 평균 training loss를 반환한다."""

    # train은 dropout과 batch normalization을 학습 동작으로 바꾼다.
    model.train()
    # 전체 loss의 sample 가중 합을 0에서 시작한다.
    total_loss = 0.0
    # 실제 처리한 sample 수를 0에서 시작한다.
    total_samples = 0
    # loader에서 image tensor와 정수 class label batch를 받는다.
    for images, labels in loader:
        # non_blocking은 pinned memory일 때 비동기 GPU copy 가능성을 연다.
        images = images.to(device, non_blocking=True)
        # label도 loss 계산 장치로 옮긴다.
        labels = labels.to(device, non_blocking=True)
        # 이전 batch gradient를 None으로 지워 불필요한 zero write를 줄인다.
        optimizer.zero_grad(set_to_none=True)
        # 현재 image batch의 class logits를 계산한다.
        logits = model(images)
        # CrossEntropyLoss로 정답 class와 logits를 비교한다.
        loss = loss_function(logits, labels)
        # 자동 미분으로 학습 가능한 parameter gradient를 계산한다.
        loss.backward()
        # optimizer가 gradient를 사용해 parameter를 갱신한다.
        optimizer.step()
        # 현재 batch 평균 loss에 sample 수를 곱해 전체 합에 더한다.
        total_loss += loss.item() * images.shape[0]
        # 현재 batch sample 수를 누적한다.
        total_samples += images.shape[0]
    # 전체 sample 수로 나눈 평균 loss를 반환한다.
    return total_loss / total_samples


# inference_mode는 평가 중 gradient graph와 관련 memory를 만들지 않는다.
@torch.inference_mode()
def evaluate(
    model: nn.Module,
    loader: DataLoader,
    device: torch.device,
    class_count: int,
) -> dict[str, object]:
    """전체 정확도와 class별 recall을 계산한다."""

    # eval은 dropout과 batch normalization을 평가 동작으로 바꾼다.
    model.eval()
    # 맞힌 전체 sample 수를 0에서 시작한다.
    total_correct = 0
    # 평가한 전체 sample 수를 0에서 시작한다.
    total_samples = 0
    # 각 class의 true positive 수를 long tensor로 센다.
    class_correct = torch.zeros(class_count, dtype=torch.int64)
    # 각 class의 실제 정답 sample 수를 센다.
    class_total = torch.zeros(class_count, dtype=torch.int64)
    # validation 또는 test loader를 batch 단위로 순회한다.
    for images, labels in loader:
        # image를 model device로 옮긴다.
        images = images.to(device, non_blocking=True)
        # label도 같은 device로 옮긴다.
        labels = labels.to(device, non_blocking=True)
        # argmax는 softmax 없이도 가장 큰 logit class를 고를 수 있다.
        predictions = model(images).argmax(dim=1)
        # batch의 전체 정답 수를 Python int로 누적한다.
        total_correct += int((predictions == labels).sum().item())
        # batch sample 수를 누적한다.
        total_samples += labels.shape[0]
        # 모든 class index를 순회해 recall 분자와 분모를 센다.
        for class_index in range(class_count):
            # mask는 현재 class가 실제 정답인 sample 위치다.
            mask = labels == class_index
            # mask 위치에서 예측도 같은 class인 수를 CPU counter에 더한다.
            class_correct[class_index] += int((predictions[mask] == class_index).sum().item())
            # 현재 class의 실제 sample 수를 분모 counter에 더한다.
            class_total[class_index] += int(mask.sum().item())
    # class별 recall을 JSON 가능한 float list로 만든다.
    recalls = [
        # 해당 class sample이 없으면 0으로 숨기지 않고 NaN을 기록한다.
        float(class_correct[index] / class_total[index])
        if class_total[index] > 0
        else float("nan")
        # 모든 class index에 같은 계산을 적용한다.
        for index in range(class_count)
    ]
    # 전체 accuracy와 class recall을 dictionary로 반환한다.
    return {
        # 전체 sample이 없으면 dataset 구성 오류이므로 division이 드러나게 둔다.
        "accuracy": total_correct / total_samples,
        # class index 순서의 recall list다.
        "class_recall": recalls,
    }


# model과 두 loader를 주어진 epoch만큼 학습하며 validation 최고 state를 반환한다.
def fit_stage(
    stage_name: str,
    model: nn.Module,
    train_loader: DataLoader,
    validation_loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    loss_function: nn.Module,
    device: torch.device,
    class_count: int,
    epochs: int,
) -> dict[str, torch.Tensor]:
    """한 파인튜닝 단계를 실행하고 validation 최고 state_dict를 반환한다."""

    # 최고 validation accuracy를 가능한 값보다 낮은 -1에서 시작한다.
    best_accuracy = -1.0
    # 첫 epoch 전에는 최고 state가 없으므로 현재 model을 깊은 복사한다.
    best_state = copy.deepcopy(model.state_dict())
    # 요청한 epoch 수만큼 train과 validation을 반복한다.
    for epoch in range(epochs):
        # 한 training epoch의 평균 loss를 계산한다.
        loss = train_epoch(model, train_loader, optimizer, loss_function, device)
        # 현재 model을 validation split에서 평가한다.
        metrics = evaluate(model, validation_loader, device, class_count)
        # dictionary에서 validation accuracy를 float로 읽는다.
        accuracy = float(metrics["accuracy"])
        # 이전 최고보다 좋으면 release 후보 state를 갱신한다.
        if accuracy > best_accuracy:
            # 새 최고 정확도를 저장한다.
            best_accuracy = accuracy
            # GPU tensor와 parameter를 포함한 state_dict를 독립 복사한다.
            best_state = copy.deepcopy(model.state_dict())
        # 단계, epoch, loss, validation accuracy를 매 epoch 기록한다.
        print(
            f"stage={stage_name} epoch={epoch + 1}/{epochs} "
            f"loss={loss:.4f} validation_accuracy={accuracy:.4f}"
        )
    # validation 최고 epoch의 parameter state를 반환한다.
    return best_state


# command line에 dataset, artifact, training 설정을 정의한다.
def parse_args() -> argparse.Namespace:
    """실제 image dataset과 training 설정을 읽는다."""

    # ArgumentParser는 help와 type 검사를 제공한다.
    parser = argparse.ArgumentParser(description=__doc__)
    # data-dir은 train/val/test 하위 폴더가 있는 root다.
    parser.add_argument("--data-dir", type=Path, required=True)
    # artifact-dir은 checkpoint, ONNX, metadata 출력 위치다.
    parser.add_argument("--artifact-dir", type=Path, default=Path("artifacts/vision"))
    # head-epochs는 feature extractor를 얼린 첫 단계 반복 수다.
    parser.add_argument("--head-epochs", type=int, default=5)
    # full-epochs는 전체 model을 작은 learning rate로 푸는 반복 수다.
    parser.add_argument("--full-epochs", type=int, default=5)
    # batch-size는 target GPU memory와 image 크기에 맞춰 조정한다.
    parser.add_argument("--batch-size", type=int, default=32)
    # workers는 image decode/transform process 수다.
    parser.add_argument("--workers", type=int, default=4)
    # seed는 split이 이미 고정된 상태에서 학습 초기화 재현에 사용한다.
    parser.add_argument("--seed", type=int, default=42)
    # 실제 명령행 문자열을 parsing한다.
    return parser.parse_args()


# dataset 검사, 두 단계 파인튜닝, test, export, metadata 저장을 연결한다.
def main() -> None:
    """실제 image 분류 release 후보를 학습하고 ONNX artifact를 만든다."""

    # command line 설정을 읽는다.
    args = parse_args()
    # 모든 기본 난수 seed를 고정한다.
    set_seed(args.seed)
    # artifact 폴더가 없으면 부모까지 만든다.
    args.artifact_dir.mkdir(parents=True, exist_ok=True)
    # CUDA가 있으면 GPU, 아니면 CPU device를 선택한다.
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # DEFAULT는 torchvision이 권장하는 현재 사전학습 MobileNetV3-Small weight다.
    weights = MobileNet_V3_Small_Weights.DEFAULT
    # weights.transforms는 weight와 일치하는 resize, crop, normalize를 제공한다.
    evaluation_transform = weights.transforms()
    # 첫 실무 baseline은 train에도 같은 deterministic transform을 써 변수를 줄인다.
    training_transform = weights.transforms()
    # train split loader와 class mapping을 만든다.
    train_loader, train_dataset = make_loader(
        args.data_dir / "train",
        training_transform,
        args.batch_size,
        True,
        args.workers,
    )
    # validation split은 순서를 섞지 않고 공식 전처리를 사용한다.
    validation_loader, validation_dataset = make_loader(
        args.data_dir / "val",
        evaluation_transform,
        args.batch_size,
        False,
        args.workers,
    )
    # test split도 모델 선택에 사용하지 않고 마지막에 한 번 평가한다.
    test_loader, test_dataset = make_loader(
        args.data_dir / "test",
        evaluation_transform,
        args.batch_size,
        False,
        args.workers,
    )
    # 세 split의 class 폴더와 정렬 순서가 정확히 같아야 label 의미가 보존된다.
    if not (
        train_dataset.class_to_idx
        == validation_dataset.class_to_idx
        == test_dataset.class_to_idx
    ):
        # split마다 class가 다르면 학습을 중단한다.
        raise ValueError("train/val/test class_to_idx mappings must match")
    # class_count는 실제 class 폴더 수다.
    class_count = len(train_dataset.classes)
    # 최소 두 class가 있어야 분류 실습이 의미가 있다.
    if class_count < 2:
        # dataset 폴더 구조를 고치도록 명확한 오류를 낸다.
        raise ValueError("at least two class folders are required")
    # ImageNet 사전학습 weight를 가진 경량 MobileNetV3-Small을 만든다.
    model = mobilenet_v3_small(weights=weights)
    # classifier의 마지막 Linear가 받는 feature 수를 읽는다.
    input_features = model.classifier[3].in_features
    # 마지막 1000-class Linear를 실제 dataset class 수의 새 head로 교체한다.
    model.classifier[3] = nn.Linear(input_features, class_count)
    # model parameter와 buffer를 선택한 device로 옮긴다.
    model.to(device)
    # 첫 단계에서는 convolution feature extractor를 모두 얼린다.
    for parameter in model.features.parameters():
        # requires_grad=False이면 backbone gradient와 optimizer update가 생기지 않는다.
        parameter.requires_grad = False
    # multi-class logits를 정수 label과 비교하는 표준 loss다.
    loss_function = nn.CrossEntropyLoss()
    # classifier parameter만 비교적 큰 learning rate로 학습한다.
    head_optimizer = torch.optim.AdamW(model.classifier.parameters(), lr=1e-3)
    # head-only 단계의 validation 최고 state를 얻는다.
    head_state = fit_stage(
        "head",
        model,
        train_loader,
        validation_loader,
        head_optimizer,
        loss_function,
        device,
        class_count,
        args.head_epochs,
    )
    # head 단계 최고 state를 model에 복원한다.
    model.load_state_dict(head_state)
    # 두 번째 단계에서는 feature extractor 전체를 학습 가능하게 푼다.
    for parameter in model.features.parameters():
        # 작은 learning rate로 기존 표현을 천천히 목표 domain에 적응시킨다.
        parameter.requires_grad = True
    # 전체 model optimizer는 head보다 작은 learning rate를 사용한다.
    full_optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4, weight_decay=1e-4)
    # 전체 미세조정 단계의 validation 최고 state를 얻는다.
    best_state = fit_stage(
        "full",
        model,
        train_loader,
        validation_loader,
        full_optimizer,
        loss_function,
        device,
        class_count,
        args.full_epochs,
    )
    # 최종 test 전에 validation 최고 state를 복원한다.
    model.load_state_dict(best_state)
    # 모델을 test evaluation 모드로 고정한다.
    model.eval()
    # 독립 test split을 최종 한 번 평가한다.
    test_metrics = evaluate(model, test_loader, device, class_count)
    # checkpoint는 CPU state로 저장해 GPU가 없는 환경에서도 읽게 한다.
    cpu_state = {
        key: value.detach().cpu()
        for key, value in model.state_dict().items()
    }
    # state, class map, architecture를 checkpoint에 저장한다.
    torch.save(
        {
            "architecture": "mobilenet_v3_small",
            "model_state": cpu_state,
            "class_to_idx": train_dataset.class_to_idx,
        },
        args.artifact_dir / "model.pt",
    )
    # export는 CPU model과 example input으로 수행해 device 의존을 줄인다.
    model.cpu()
    # 공식 MobileNetV3-Small 전처리의 기본 crop 크기 224×224 입력을 만든다.
    example_input = torch.zeros(1, 3, 224, 224, dtype=torch.float32)
    # ONNX export가 실행할 평가 상태를 다시 명시한다.
    model.eval()
    # 검증 가능한 FP32 ONNX 모델을 만든다.
    torch.onnx.export(
        # export할 fine-tuned model이다.
        model,
        # batch 1 RGB example input이다.
        (example_input,),
        # 생성할 model 경로다.
        f=args.artifact_dir / "model.onnx",
        # C++ runtime의 입력 이름을 고정한다.
        input_names=["image"],
        # C++ runtime의 출력 이름을 고정한다.
        output_names=["class_logits"],
        # batch 축만 dynamic으로 허용한다.
        dynamic_axes={"image": {0: "batch"}, "class_logits": {0: "batch"}},
        # 널리 지원되는 ONNX opset 17을 사용한다.
        opset_version=17,
        # 교육 환경의 전통 export 경로를 명시한다.
        dynamo=False,
    )
    # class index 순서와 전처리·평가 결과를 metadata object로 만든다.
    metadata = {
        # architecture는 runtime/model registry 식별에 사용한다.
        "architecture": "mobilenet_v3_small",
        # input contract는 batch×RGB×height×width다.
        "input_shape": [1, 3, 224, 224],
        # RGB 채널 순서를 명시한다.
        "channel_order": "RGB",
        # ImageNet 사전학습 weight의 mean이다.
        "mean": [0.485, 0.456, 0.406],
        # ImageNet 사전학습 weight의 std다.
        "std": [0.229, 0.224, 0.225],
        # 폴더 이름과 class index의 정확한 mapping이다.
        "class_to_idx": train_dataset.class_to_idx,
        # 최종 test accuracy와 class recall이다.
        "test_metrics": test_metrics,
        # dataset root는 장치 고유 절대 경로 대신 사용자가 준 문자열을 기록한다.
        "dataset_root": str(args.data_dir),
        # seed는 같은 초기화와 batch shuffle 재현에 사용한다.
        "seed": args.seed,
    }
    # UTF-8 metadata 파일을 쓰기 모드로 연다.
    with (args.artifact_dir / "metadata.json").open("w", encoding="utf-8") as file:
        # ensure_ascii=False는 한국어 class 이름도 그대로 보존한다.
        json.dump(metadata, file, ensure_ascii=False, indent=2)
    # 최종 독립 test 결과를 console과 CI log에 출력한다.
    print(json.dumps(test_metrics, ensure_ascii=False, indent=2))
    # 생성한 artifact 폴더를 표시한다.
    print(f"saved artifacts to {args.artifact_dir}")


# import 때 학습을 시작하지 않고 CLI 실행 때만 main을 호출한다.
if __name__ == "__main__":
    # 전체 실제 image fine-tuning workflow를 실행한다.
    main()
