# D-FINE-seg: 실시간 객체 검출·인스턴스 분할과 멀티 백엔드 배포

작성일: 2026-07-21

## 출처와 작업 범위

- 논문: [D-FINE-seg: Object Detection and Instance Segmentation Framework with multi-backend deployment](https://arxiv.org/abs/2602.23043)
- 저자: Argo Saakyan, Dmitry Solntsev
- 소속: Veryfi Inc.
- 제출일: 2026-02-26
- 원문 언어: 영어
- 확인일: 2026-07-21 (Asia/Seoul)
- 공식 코드: [ArgoHA/D-FINE-seg](https://github.com/ArgoHA/D-FINE-seg)
- 한국어 번역 요약: [translation.ko.md](translation.ko.md)

이 자료는 arXiv v1의 6페이지 본문을 중심으로 구조, 손실, matching, 평가와 배포를 설명한다. 공식 저장소는 논문 이후 semantic segmentation, CoreML, LiteRT, multi-channel 입력 등 기능이 확장되어 있으므로 논문 기여와 최신 저장소 기능을 구분해 서술한다.

## 한눈에 보기

D-FINE-seg는 실시간 Transformer 객체 검출기 D-FINE에 경량 instance mask branch를 추가한 프레임워크다. 검출 query마다 mask embedding을 만들고, 여러 scale의 encoder feature를 융합한 공통 mask feature map과 dot product해 인스턴스별 mask를 생성한다.

```text
이미지
  → CNN backbone
  → HybridEncoder(FPN + PAN, stride 8/16/32)
  ├→ Transformer decoder → class + bounding box
  └→ mask feature fuser ─┐
       decoder query → mask embedding
                         └→ dot product → instance masks(H/4 × W/4)
```

논문의 두 기여는 다음과 같다.

1. D-FINE용 경량 mask head와 segmentation-aware 학습
2. ONNX, TensorRT와 OpenVINO를 아우르는 학습·export·추론 pipeline

## 기초 개념

### 객체 검출과 분할

- **객체 검출**: 각 객체의 class와 bounding box를 예측한다.
- **Semantic segmentation**: 모든 pixel에 class를 부여하지만 같은 class의 개별 객체를 구분하지 않는다.
- **Instance segmentation**: class와 pixel mask를 예측하면서 같은 class의 객체도 instance별로 구분한다.

논문은 검출과 instance segmentation을 다룬다. 공식 저장소의 semantic segmentation은 이후 확장 기능이다.

### DETR 계열

DETR 계열은 고정된 query 집합이 객체 후보를 표현하고, Hungarian algorithm으로 prediction과 ground truth를 일대일 대응시킨다. 중복 box를 제거하는 NMS 의존을 줄이는 end-to-end 설계가 장점이다.

### D-FINE

D-FINE은 RT-DETR 계열을 바탕으로 다음 핵심 기법을 사용한다.

- **FDR(Fine-grained Distribution Refinement)**: box 좌표를 하나의 고정값으로 바로 예측하기보다 확률 분포를 반복적으로 정제한다.
- **GO-LSD(Global Optimal Localization Self-Distillation)**: 마지막 decoder layer의 localization 지식을 앞 layer로 전달한다.
- **Contrastive denoising**: 노이즈가 들어간 ground-truth query를 복원하며 convergence와 matching 품질을 개선한다.

### Mask 표현

한 이미지에 `K`개 객체가 있다면 정답 mask는 `[K, H, W]`의 binary tensor다. 예측 mask logit은 낮은 해상도에서 계산한 뒤 원본 이미지 크기로 보간하고 threshold로 이진화한다.

## 핵심 요약

1. Mask head는 stride 8/16/32 PAN feature를 공통 channel로 projection하고 stride 8에서 합친 뒤 1/4 해상도로 올린다.
2. Decoder query는 3-layer MLP를 거쳐 instance별 mask embedding이 된다.
3. Mask embedding과 공유 pixel feature의 scaled dot product는 dynamic 1×1 convolution처럼 작동한다.
4. 최종 layer뿐 아니라 intermediate decoder와 denoising query에도 mask supervision을 적용한다.
5. Mask loss는 matched ground-truth box 안에서 BCE와 Dice를 계산하고, matching cost는 full mask의 Dice와 sigmoid focal cost를 사용한다.
6. 보조·denoising supervision과 Hungarian mask cost는 training-only라 inference latency를 늘리지 않는다.
7. 논문 benchmark는 TACO, TensorRT FP16, batch 1, RTX 5070 Ti라는 특정 조건의 결과다.
8. 모델별 기본 confidence threshold가 달라 F1 비교는 하나의 운영점 비교이지 전체 precision-recall curve 비교가 아니다.

## 상세 정리

### Backbone과 HybridEncoder

CNN backbone이 여러 해상도의 feature를 추출하고 HybridEncoder가 FPN+PAN 방식으로 multi-scale feature를 융합한다. D-FINE-seg는 기존 D-FINE의 검출 encoder·decoder를 유지하면서 PAN 출력을 mask branch에 재사용한다.

### 경량 Mask Head

Mask head는 다음 순서로 동작한다.

1. Stride 8/16/32 feature에 각각 1×1 convolution과 GroupNorm을 적용해 공통 256 channel로 맞춘다.
2. Stride 16/32 feature를 bilinear interpolation해 stride 8 크기로 올리고 합한다.
3. 3×3 convolution, GroupNorm, ReLU로 feature를 부드럽게 융합한다.
4. 다시 upsampling과 3×3 convolution을 적용해 입력의 1/4 해상도 mask feature를 만든다.
5. 각 decoder query hidden state를 3-layer MLP로 mask embedding으로 projection한다.
6. Query embedding과 pixel feature를 channel 축으로 dot product해 `[query, H/4, W/4]` logit을 만든다.

Mask DINO가 세부 경계를 위해 stride-4 backbone feature까지 쓰는 것과 달리, 논문 구조는 이미 융합된 HybridEncoder 출력만 사용해 단순성과 latency를 우선한다.

### Auxiliary와 Denoising Supervision

최종 decoder layer만 학습하면 앞 layer의 query가 mask 품질을 직접 배우기 어렵다. D-FINE-seg는 intermediate layer에서도 mask를 생성해 auxiliary loss를 적용한다. Denoising query에도 같은 cropped mask loss를 적용한다.

이 계산은 학습 시간과 메모리를 늘리지만 inference graph에는 포함되지 않는다.

### Box-cropped BCE

Matched ground-truth box의 ROI 안에서 pixel별 binary cross entropy를 계산하고 ROI pixel 수로 정규화한다. 객체 밖의 넓은 background가 loss를 압도하는 문제를 줄인다.

### Box-cropped Dice Loss

Sigmoid probability `p`와 soft target `y`에 대해 다음 형태를 사용한다.

```text
Dice(p, y) = (2Σpy + ε) / (Σp + Σy + ε)
Dice loss = 1 - Dice
```

Ground-truth mask는 mask head 해상도로 bilinear resize해 soft target으로 사용한다. 최종·auxiliary decoder layer에 같은 loss suite를 적용한다.

논문에서 사용한 가중치는 VFL 1, L1 5, GIoU 2, FGL 0.15, DDF 1.5, mask BCE 1, mask Dice 1이다.

### Mask-aware Hungarian Matching

기본 matching cost는 class, box L1, GIoU의 가중합이다. D-FINE-seg는 다음 비용을 추가한다.

- `1 - Dice` mask overlap cost
- Sigmoid focal mask cost

흥미롭게도 training loss는 ground-truth box ROI 안에서 계산하지만 matching mask cost는 mask head 출력 전체 map에서 계산한다. Assignment는 전체 mask 모양을 보고, 최적화 loss는 객체 영역에 집중한다.

### Postprocessing

1. Confidence threshold보다 낮은 instance를 제거한다.
2. 1/4 mask를 원본 이미지 크기로 bilinear resize한다.
3. Mask threshold로 이진화한다.
4. 대응 box 밖의 mask pixel을 0으로 정리한다.

마지막 단계는 box 내부 supervision을 강조한 학습 목표와 일관된다. 다만 실제 객체가 box 경계에 닿거나 annotation이 부정확하면 boundary가 잘릴 수 있어 오류 분석이 필요하다.

## 구현과 배포

논문 시점 프레임워크는 custom dataset 학습, benchmark, export와 optimized inference를 제공한다.

```text
config 설정
  → make train
  → make export
  → make infer / backend별 inference
```

논문은 ONNX, TensorRT와 OpenVINO를 다룬다.

| Backend | 일반적 대상 | 주의점 |
| --- | --- | --- |
| Torch | 개발·검증 | 배포 engine보다 느릴 수 있음 |
| ONNX Runtime | CPU/CUDA 범용 | 지원 operator와 dynamic shape 확인 |
| TensorRT FP16 | NVIDIA GPU | 대상 GPU에서 engine 생성, static shape 조건 확인 |
| OpenVINO FP16/INT8 | Intel CPU/iGPU | calibration과 정확도 저하 검증 |

공식 저장소 최신 버전에는 CoreML, LiteRT, semantic segmentation과 parity self-check도 포함된다. 논문 결과와 후속 기능 benchmark를 혼합하지 않는다.

## 실험 결과 읽기

### 데이터와 조건

- TACO: 1,500개 이미지, 60개 category 중 실제 instance가 있는 59개 class
- Batch ID 기준 86/14 train/validation split
- 입력: 640×640
- D-FINE-seg: 50 epoch, confidence 0.5
- YOLO26: 100 epoch, confidence 0.25
- TensorRT FP16, batch 1
- RTX 5070 Ti 16GB, CUDA 12.8, TensorRT 10.10.0.31

End-to-end latency는 disk image 읽기를 제외하고 preprocessing, GPU transfer, forward와 postprocessing을 포함한다. 각 모델을 10개 sample로 warm-up한 뒤 validation 212개 이미지에서 측정했다.

### 핵심 보고 결과

논문은 N/S/M/L/X 평균에서 segmentation F1이 YOLO26 대비 상대적으로 약 65% 높고 latency overhead는 약 10%라고 보고한다. Detection은 F1이 약 70% 높고 latency overhead는 약 1%라고 보고한다. Mask mAP 평균 상대 개선은 약 41%, box mAP은 약 49%로 제시한다.

그러나 절대 F1과 mAP은 모델 크기별로 다르며 YOLO26-M은 mask mAP에서 D-FINE-seg-M보다 높다. 평균 상대 개선만 보고 모든 size·metric에서 우수하다고 일반화하면 안 된다.

### 비교의 한계

- 두 모델의 epoch와 confidence threshold가 다르다.
- Default threshold F1은 model별 하나의 운영점이며 threshold-free 비교가 아니다.
- 단일 dataset과 한 GPU·software stack 결과다.
- Validation 규모가 212개 이미지로 작다.
- Paper v1은 mask head를 scratch에서 초기화했다고 적지만 최신 저장소는 pretrained segmentation weight 제공을 설명한다.

공정한 재평가에서는 동일 split, 입력, augmentation budget과 export protocol을 유지하고 각 모델의 PR curve, mAP, calibration, peak memory와 latency distribution을 함께 기록한다.

## 용어 정리

| 용어 | 설명 |
| --- | --- |
| Query | DETR decoder에서 객체 후보 하나를 나타내는 학습 표현 |
| PAN/FPN | 여러 해상도 feature를 위·아래 방향으로 융합하는 구조 |
| Mask embedding | Query별 instance mask를 만들기 위한 channel vector |
| BCE | Pixel을 foreground/background로 분류하는 cross entropy |
| Dice | 두 mask의 겹침을 측정하는 지표·loss |
| Hungarian matching | Prediction과 ground truth의 최소 비용 일대일 assignment |
| Auxiliary loss | Intermediate layer에도 직접 적용하는 보조 supervision |
| Denoising query | 노이즈가 들어간 ground truth를 복원하도록 만든 학습 query |
| FP16 | 16-bit floating point로 계산·저장하는 정밀도 |
| INT8 | 8-bit 정수 quantization 형식 |
| End-to-end latency | 전처리, 모델, 후처리를 포함한 요청 처리 시간 |
| Penalized IoU | TP IoU 합을 TP+FP+FN으로 나눠 실패에 0을 부여한 논문 지표 |

## 실습 학습 가이드

- [`01_foundations.ipynb`](01_foundations.ipynb): Box·mask IoU와 TP/FP/FN 기반 precision, recall, F1을 계산한다.
- [`02_practice.ipynb`](02_practice.ipynb): ROI-cropped BCE와 Dice loss를 직접 구현하고 crop 효과를 비교한다.
- [`03_advanced.ipynb`](03_advanced.ipynb): Class·box·mask 비용을 결합한 Hungarian assignment를 작은 예제로 탐구한다.

노트북은 Python 3 표준 라이브러리만 사용해 GPU 없이 실행된다. 논문 모델 자체의 학습·추론은 공식 코드의 `uv sync`, config와 Makefile 흐름을 따른다.

## 다음 학습 경로

1. DETR의 bipartite matching과 RT-DETR의 real-time 설계를 학습한다.
2. D-FINE의 FDR과 GO-LSD 목적함수를 읽는다.
3. Mask DINO의 query-mask dot product와 multi-scale pixel decoder를 비교한다.
4. 공식 저장소에서 동일 이미지에 Torch와 export backend parity를 검사한다.
5. Confidence threshold sweep으로 PR curve와 최적 F1을 다시 계산한다.
6. 다른 instance segmentation dataset에서 정확도·latency trade-off를 재현한다.

## 확인이 필요한 사항

- 논문은 arXiv v1이며 peer review 결과가 아니다.
- 결과는 개발팀의 특정 fine-tuning·hardware 설정에서 보고됐다.
- 최신 공식 저장소는 논문 이후 기능이 추가되어 논문과 일부 설명이 다르다.
- 배포 형식별 operator, dynamic shape와 quantization 지원은 runtime 버전에 따라 달라질 수 있다.
