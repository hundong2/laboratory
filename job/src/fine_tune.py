"""작은 PyTorch 센서 모델을 사전학습하고 새 장치 분포에 파인튜닝한다."""

# argparse는 명령행에서 epoch 수와 출력 경로를 바꿀 수 있게 한다.
import argparse
# json은 C++도 읽을 수 있는 모델 메타데이터 파일을 저장하는 데 사용한다.
import json
# random은 Python 표준 난수 seed를 고정하는 데 사용한다.
import random
# Path는 운영체제에 맞는 경로 결합과 폴더 생성을 제공한다.
from pathlib import Path

# NumPy seed도 고정해 실험 재현성을 높인다.
import numpy as np
# torch는 tensor, 자동 미분, 모델 저장 기능을 제공한다.
import torch
# nn은 Linear, ReLU, Module 같은 신경망 구성 요소를 제공한다.
from torch import nn
# DataLoader는 데이터를 작은 batch로 반복하고 TensorDataset은 입력과 정답을 묶는다.
from torch.utils.data import DataLoader, TensorDataset


# 모든 난수 생성기에 같은 seed를 전달해 반복 실행의 차이를 줄인다.
def set_seed(seed: int) -> None:
    """Python, NumPy, PyTorch의 난수 seed를 고정한다."""

    # random.seed는 Python 표준 난수 순서를 고정한다.
    random.seed(seed)
    # np.random.seed는 레거시 NumPy 전역 난수 순서를 고정한다.
    np.random.seed(seed)
    # manual_seed는 CPU와 현재 프로세스의 PyTorch 난수 순서를 고정한다.
    torch.manual_seed(seed)


# nn.Module을 상속하면 parameter 등록, train/eval 전환, state_dict 저장을 사용할 수 있다.
class TinySensorNet(nn.Module):
    """네 개 센서 특성을 세 상태로 분류하는 작은 완전연결 신경망."""

    # num_classes 기본값은 정상·주의·정지 필요의 세 클래스다.
    def __init__(self, num_classes: int = 3) -> None:
        # 부모 nn.Module의 초기화로 하위 layer 추적 기능을 준비한다.
        super().__init__()
        # Sequential은 입력을 나열한 layer 순서대로 전달한다.
        self.backbone = nn.Sequential(
            # 첫 Linear는 네 센서 값을 16개 학습 특징으로 투영한다.
            nn.Linear(4, 16),
            # ReLU는 음수를 0으로 만들어 비선형 표현을 가능하게 한다.
            nn.ReLU(),
            # 두 번째 Linear는 16개 특징을 8개 작은 embedding으로 압축한다.
            nn.Linear(16, 8),
            # 두 번째 ReLU도 모델이 단순 행렬곱 이상의 경계를 배우게 한다.
            nn.ReLU(),
        )
        # classifier는 8차원 embedding을 세 클래스 logits로 바꾸는 교체 가능한 head다.
        self.classifier = nn.Linear(8, num_classes)

    # forward는 model(x)를 호출할 때 PyTorch가 실행하는 계산 경로다.
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """입력 batch를 정규화 전 클래스 점수인 logits로 바꾼다."""

        # backbone으로 재사용 가능한 센서 특징을 추출한다.
        features = self.backbone(x)
        # classifier head로 각 클래스의 logits를 반환한다.
        return self.classifier(features)


# seed와 shift가 달라지면 다른 장치에서 수집한 것 같은 데이터가 만들어진다.
def make_dataset(
    samples_per_class: int,
    seed: int,
    shift: float,
) -> tuple[torch.Tensor, torch.Tensor]:
    """세 상태의 합성 센서 tensor와 정답 tensor를 만든다."""

    # Generator는 이 함수 안에서만 쓰는 재현 가능한 PyTorch 난수 상태다.
    generator = torch.Generator().manual_seed(seed)
    # 각 행은 진동, 온도 변화, 전류, 회전 오차의 클래스 중심이다.
    centers = torch.tensor(
        [
            [0.15, 0.10, 0.20, 0.10],
            [0.55, 0.45, 0.50, 0.40],
            [0.90, 0.85, 0.80, 0.95],
        ],
        dtype=torch.float32,
    )
    # 장치별 calibration 차이를 네 특성에 서로 다르게 적용한다.
    device_shift = torch.tensor([shift, -shift * 0.5, shift * 0.25, shift])
    # 클래스별 입력 tensor를 모을 리스트다.
    feature_blocks: list[torch.Tensor] = []
    # 클래스별 정답 tensor를 모을 리스트다.
    label_blocks: list[torch.Tensor] = []
    # 각 클래스 중심 주변에서 같은 수의 샘플을 생성한다.
    for class_id, center in enumerate(centers):
        # randn은 평균 0, 표준편차 1인 noise를 만든 뒤 0.08을 곱한다.
        noise = torch.randn(samples_per_class, 4, generator=generator) * 0.08
        # 중심, 장치 편향, noise를 합치고 합성 센서 유효 범위로 자른다.
        block = (center + device_shift + noise).clamp(0.0, 1.2)
        # 현재 클래스 입력을 목록에 추가한다.
        feature_blocks.append(block)
        # full은 현재 입력 행 수만큼 class_id를 가진 int64 정답을 만든다.
        label_blocks.append(torch.full((samples_per_class,), class_id, dtype=torch.int64))
    # cat은 클래스별 입력을 첫 번째 축, 즉 행 방향으로 합친다.
    features = torch.cat(feature_blocks, dim=0)
    # 정답도 같은 클래스 순서로 합친다.
    labels = torch.cat(label_blocks, dim=0)
    # randperm은 모든 행을 섞을 무작위 순열을 만든다.
    order = torch.randperm(labels.shape[0], generator=generator)
    # 입력과 정답에 같은 순열을 적용해 짝을 보존한 채 반환한다.
    return features[order], labels[order]


# 학습 입력만으로 계산한 mean과 std를 tuple로 반환한다.
def fit_standardizer(features: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """특성별 학습 평균과 안전한 표준편차를 계산한다."""

    # dim=0은 행을 모아 각 센서 열의 평균을 계산하고 차원 하나는 유지한다.
    mean = features.mean(dim=0, keepdim=True)
    # unbiased=False는 모집단 표준편차를 사용해 NumPy 실습과 정의를 맞춘다.
    std = features.std(dim=0, keepdim=True, unbiased=False)
    # clamp_min은 너무 작은 표준편차를 1e-6으로 제한해 0 나눗셈을 막는다.
    return mean, std.clamp_min(1e-6)


# batch_size와 shuffle을 명시해 학습용 반복자를 만든다.
def make_loader(
    features: torch.Tensor,
    labels: torch.Tensor,
    batch_size: int,
    shuffle: bool,
) -> DataLoader:
    """입력과 정답을 mini-batch로 제공하는 DataLoader를 만든다."""

    # TensorDataset은 같은 첫 차원을 가진 두 tensor를 한 샘플 묶음으로 만든다.
    dataset = TensorDataset(features, labels)
    # num_workers=0은 초보 실습과 작은 데이터에서 별도 worker process를 만들지 않는다.
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, num_workers=0)


# optimizer가 가진 parameter만 갱신하고 loss_function으로 오차를 계산한다.
def train_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    loss_function: nn.Module,
) -> float:
    """한 epoch를 학습하고 샘플당 평균 loss를 반환한다."""

    # train은 dropout, batch normalization 같은 layer를 학습 모드로 바꾼다.
    model.train()
    # 전체 loss 합계를 Python float로 누적한다.
    total_loss = 0.0
    # 전체 샘플 수를 세어 batch 크기가 달라도 정확한 평균을 낸다.
    total_count = 0
    # loader가 features와 labels mini-batch를 차례로 제공한다.
    for features, labels in loader:
        # 이전 batch의 gradient를 지워 누적되지 않게 한다.
        optimizer.zero_grad(set_to_none=True)
        # 현재 batch를 모델에 넣어 logits를 계산한다.
        logits = model(features)
        # CrossEntropyLoss가 logits와 정수 클래스 정답을 비교한다.
        loss = loss_function(logits, labels)
        # backward는 계산 그래프를 따라 각 parameter의 gradient를 계산한다.
        loss.backward()
        # step은 optimizer 규칙에 따라 학습 가능한 parameter를 갱신한다.
        optimizer.step()
        # item으로 autograd 그래프에서 분리한 loss에 batch 행 수를 곱해 누적한다.
        total_loss += loss.item() * features.shape[0]
        # 현재 batch 행 수를 전체 샘플 수에 더한다.
        total_count += features.shape[0]
    # 전체 loss 합을 전체 샘플 수로 나누어 평균을 반환한다.
    return total_loss / total_count


# inference_mode는 gradient 기록을 끄고 평가 메모리와 시간을 줄인다.
@torch.inference_mode()
def evaluate(model: nn.Module, loader: DataLoader) -> float:
    """평가 데이터의 분류 정확도를 반환한다."""

    # eval은 dropout과 batch normalization을 평가 동작으로 바꾼다.
    model.eval()
    # 맞힌 샘플 수를 0에서 시작한다.
    correct = 0
    # 평가한 전체 샘플 수를 0에서 시작한다.
    total = 0
    # 평가 loader를 batch 단위로 순회한다.
    for features, labels in loader:
        # argmax는 logits가 가장 큰 클래스 번호를 고른다.
        predictions = model(features).argmax(dim=1)
        # 예측과 정답 비교의 True 개수를 더한다.
        correct += int((predictions == labels).sum().item())
        # 현재 batch의 정답 수를 전체 수에 더한다.
        total += labels.shape[0]
    # 맞힌 수를 전체 수로 나눈 정확도를 반환한다.
    return correct / total


# argparse Namespace를 반환해 main의 실험 설정을 간단히 유지한다.
def parse_args() -> argparse.Namespace:
    """명령행 인수를 정의하고 읽는다."""

    # ArgumentParser는 --help 메시지와 입력 검사를 자동으로 제공한다.
    parser = argparse.ArgumentParser(description=__doc__)
    # 사전학습 반복 수를 필요할 때 줄이거나 늘릴 수 있게 한다.
    parser.add_argument("--pretrain-epochs", type=int, default=30)
    # head만 학습하는 반복 수를 설정한다.
    parser.add_argument("--head-epochs", type=int, default=12)
    # 전체 모델을 작은 학습률로 미세조정하는 반복 수를 설정한다.
    parser.add_argument("--unfreeze-epochs", type=int, default=12)
    # 모델과 메타데이터를 저장할 폴더를 설정한다.
    parser.add_argument("--artifact-dir", type=Path, default=Path("artifacts"))
    # parse_args는 실제 명령행 문자열을 위 정의에 따라 Namespace로 바꾼다.
    return parser.parse_args()


# main은 데이터 생성부터 모델 저장까지 전체 파인튜닝 실습을 연결한다.
def main() -> None:
    """기준 장치 사전학습, 새 장치 head 학습, 전체 미세조정을 순서대로 수행한다."""

    # 명령행 설정을 읽는다.
    args = parse_args()
    # 실행마다 같은 초기값을 쓰도록 seed를 고정한다.
    set_seed(42)
    # 출력 폴더가 없으면 부모 폴더까지 만들고, 이미 있어도 오류를 내지 않는다.
    args.artifact_dir.mkdir(parents=True, exist_ok=True)
    # 기준 장치에서 수집한 사전학습 데이터를 만든다.
    source_x, source_y = make_dataset(samples_per_class=160, seed=10, shift=0.0)
    # 새 장치에서 수집한 적은 파인튜닝 데이터를 만든다.
    target_train_x, target_train_y = make_dataset(samples_per_class=35, seed=20, shift=0.12)
    # 새 장치의 별도 test 데이터를 다른 seed로 만든다.
    target_test_x, target_test_y = make_dataset(samples_per_class=80, seed=30, shift=0.12)
    # 배포 대상인 새 장치의 train 통계만으로 표준화를 fit한다.
    mean, std = fit_standardizer(target_train_x)
    # 기준 데이터도 최종 배포 전처리와 같은 통계로 변환한다.
    source_x = (source_x - mean) / std
    # 새 장치 train 데이터에 학습 통계를 적용한다.
    target_train_x = (target_train_x - mean) / std
    # 새 장치 test에도 train 통계만 적용해 정보 유출을 막는다.
    target_test_x = (target_test_x - mean) / std
    # 기준 사전학습용 mini-batch loader를 만든다.
    source_loader = make_loader(source_x, source_y, batch_size=64, shuffle=True)
    # 새 장치 파인튜닝용 loader를 만든다.
    target_train_loader = make_loader(target_train_x, target_train_y, batch_size=32, shuffle=True)
    # 평가 순서는 성능에 영향이 없으므로 test loader는 섞지 않는다.
    target_test_loader = make_loader(target_test_x, target_test_y, batch_size=128, shuffle=False)
    # 작은 센서 모델을 무작위 가중치로 생성한다.
    model = TinySensorNet(num_classes=3)
    # CrossEntropyLoss는 multi-class 분류의 표준 logits 손실이다.
    loss_function = nn.CrossEntropyLoss()
    # AdamW는 parameter별 적응 학습률과 weight decay를 제공한다.
    pretrain_optimizer = torch.optim.AdamW(model.parameters(), lr=3e-3, weight_decay=1e-4)
    # 지정한 epoch 수만큼 기준 장치 데이터로 backbone과 head를 함께 학습한다.
    for epoch in range(args.pretrain_epochs):
        # 한 epoch를 학습하고 평균 loss를 받는다.
        loss = train_epoch(model, source_loader, pretrain_optimizer, loss_function)
        # 마지막 epoch와 10 epoch마다 진행 상황을 짧게 표시한다.
        if (epoch + 1) % 10 == 0 or epoch + 1 == args.pretrain_epochs:
            # f-string은 현재 epoch와 소수점 넷째 자리 loss를 문자열에 넣는다.
            print(f"pretrain epoch={epoch + 1} loss={loss:.4f}")
    # 새 장치에 맞는 head를 무작위 초기화해 기존 head의 편향을 제거한다.
    model.classifier = nn.Linear(8, 3)
    # backbone의 모든 parameter를 얼려 head 단계에서 gradient 갱신 대상에서 뺀다.
    for parameter in model.backbone.parameters():
        # requires_grad=False이면 backward가 이 parameter의 gradient를 만들지 않는다.
        parameter.requires_grad = False
    # head parameter만 optimizer에 전달해 첫 파인튜닝 단계를 명확히 한다.
    head_optimizer = torch.optim.AdamW(model.classifier.parameters(), lr=5e-3)
    # 적은 새 장치 데이터로 head만 빠르게 적응시킨다.
    for epoch in range(args.head_epochs):
        # head 전용 optimizer로 한 epoch를 학습한다.
        loss = train_epoch(model, target_train_loader, head_optimizer, loss_function)
        # 마지막 head epoch에서 loss를 표시한다.
        if epoch + 1 == args.head_epochs:
            # 단계 이름을 포함해 로그 해석을 쉽게 한다.
            print(f"head-only epoch={epoch + 1} loss={loss:.4f}")
    # backbone을 다시 풀어 작은 학습률의 전체 미세조정을 준비한다.
    for parameter in model.backbone.parameters():
        # requires_grad=True로 복원하면 이후 backward에서 gradient가 계산된다.
        parameter.requires_grad = True
    # 전체 모델에는 head 단계보다 작은 학습률을 써 기존 특징을 급격히 망가뜨리지 않는다.
    fine_tune_optimizer = torch.optim.AdamW(model.parameters(), lr=5e-4, weight_decay=1e-4)
    # 새 장치 데이터로 전체 모델을 짧게 미세조정한다.
    for epoch in range(args.unfreeze_epochs):
        # 전체 parameter optimizer로 한 epoch를 학습한다.
        loss = train_epoch(model, target_train_loader, fine_tune_optimizer, loss_function)
        # 마지막 미세조정 epoch에서 loss를 표시한다.
        if epoch + 1 == args.unfreeze_epochs:
            # 단계 이름을 포함한 최종 학습 loss를 출력한다.
            print(f"unfrozen epoch={epoch + 1} loss={loss:.4f}")
    # 독립 target test set에서 최종 정확도를 계산한다.
    target_accuracy = evaluate(model, target_test_loader)
    # 모델 state_dict와 구조 재생성에 필요한 정보를 checkpoint로 저장한다.
    torch.save(
        {
            "model_state": model.state_dict(),
            "num_classes": 3,
        },
        args.artifact_dir / "sensor_model.pt",
    )
    # C++ 전처리와 결과 해석에 필요한 모델 계약을 JSON 객체로 만든다.
    metadata = {
        "model_version": "sensor-model-1",
        "input_name": "sensor_features",
        "output_name": "class_logits",
        "input_shape": [1, 4],
        "input_dtype": "float32",
        "feature_names": ["vibration", "temperature_delta", "current", "rotation_error"],
        "class_names": ["normal", "warning", "stop_required"],
        "mean": mean.squeeze(0).tolist(),
        "std": std.squeeze(0).tolist(),
        "target_test_accuracy": target_accuracy,
    }
    # open은 UTF-8 JSON 파일을 쓰기 모드로 열고 with 종료 시 자동으로 닫는다.
    with (args.artifact_dir / "metadata.json").open("w", encoding="utf-8") as file:
        # indent=2는 사람이 diff를 읽기 쉬운 들여쓰기를 적용한다.
        json.dump(metadata, file, ensure_ascii=False, indent=2)
    # acceptance gate에서 확인할 최종 정확도를 표시한다.
    print(f"target test accuracy={target_accuracy:.4f}")
    # 생성한 checkpoint 경로를 표시한다.
    print(f"saved={args.artifact_dir / 'sensor_model.pt'}")


# 모듈 import 때는 학습하지 않고 `python src/fine_tune.py` 실행 때만 main을 호출한다.
if __name__ == "__main__":
    # 전체 파인튜닝 workflow를 시작한다.
    main()
