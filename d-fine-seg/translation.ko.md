# 「D-FINE-seg」 논문 한국어 번역 요약

작성일: 2026-07-21

- 원문: [arXiv:2602.23043](https://arxiv.org/abs/2602.23043)
- 제목: D-FINE-seg: Object Detection and Instance Segmentation Framework with multi-backend deployment
- 저자: Argo Saakyan, Dmitry Solntsev
- 제출일: 2026-02-26
- 원문 언어: 영어
- 확인일: 2026-07-21

> 논문의 섹션 흐름, 핵심 방법과 수치를 보존한 한국어 번역 요약이다. 원문 전문을 문장 단위로 복제하지 않는다.

## 초록

Transformer 기반 실시간 객체 검출기는 정확도와 latency 사이에서 강한 균형을 보이며 D-FINE은 최근 뛰어난 구조 중 하나다. 하지만 Transformer 기반 실시간 instance segmentation은 상대적으로 드물다.

D-FINE-seg는 D-FINE에 경량 mask head, segmentation-aware 학습, box 영역 안의 BCE·Dice mask loss, auxiliary·denoising mask supervision과 조정된 Hungarian matching cost를 추가한다. TACO 데이터셋의 통일된 TensorRT FP16 end-to-end protocol에서 Ultralytics YOLO26보다 높은 F1을 보고하면서 경쟁력 있는 latency를 유지한다.

두 번째 기여는 객체 검출과 instance segmentation을 ONNX, TensorRT, OpenVINO로 학습·export·최적화 추론하는 end-to-end pipeline이다. 프레임워크는 Apache 2.0으로 공개됐다.

## 1. 서론

Instance segmentation은 실시간 computer vision에서 중요한 과제다. DETR 계열은 decoder가 bounding box를 일대일로 직접 출력해 NMS 의존을 줄이는 장점이 있다. 하지만 instance mask를 위해 무거운 head를 붙이면 latency가 커질 수 있다.

저자들은 D-FINE을 경량 mask head로 확장하면서 낮은 latency와 server·edge용 format export를 유지할 수 있음을 보인다. 주요 기여는 다음과 같다.

- D-FINE encoder 출력용 경량 mask head
- Loss, matcher, auxiliary와 denoising supervision을 포함한 segmentation-aware 학습
- 재현 가능한 multi-backend 배포 protocol

## 2. 관련 연구

D-FINE-seg의 검출 기반은 RT-DETR에서 발전한 D-FINE이다. Mask head는 Mask DINO의 query embedding과 pixel feature dot product 방식에서 영감을 받았다. Mask2Former는 masked attention으로 segmentation 과제를 통합했고, SAM은 promptable segmentation이라는 다른 사용 사례를 보여줬다.

실시간 Transformer instance segmentation은 검출보다 연구가 적다. Export와 배포에는 ONNX, TensorRT와 OpenVINO를 사용한다.

## 3. 방법

### D-FINE 검출 기반

D-FINE의 FDR은 고정 좌표를 바로 예측하는 대신 box 확률 분포를 반복 정제해 localization을 높인다. GO-LSD는 마지막 decoder layer의 지식을 앞 layer로 전달하는 self-distillation 역할을 한다.

전체 구조는 CNN backbone, FPN+PAN multi-scale 융합을 수행하는 HybridEncoder, contrastive denoising이 포함된 Transformer decoder로 구성되며 N/S/M/L/X 크기를 제공한다.

### 3.1 Mask head 구조

Ground-truth mask는 객체 수 `K`에 대해 `[K, H, W]` binary tensor로 준비한다. Mask head는 HybridEncoder의 stride 8/16/32 PAN feature를 받는다.

1. Scale별 1×1 projection과 GroupNorm으로 256 channel에 맞춘다.
2. 더 작은 feature를 stride 8 크기로 bilinear upsample하고 합한다.
3. 3×3 convolution, GroupNorm, ReLU를 적용한다.
4. Upsampling과 3×3 convolution으로 입력의 1/4 해상도에 도달한다.

각 decoder query hidden state는 3-layer MLP를 거쳐 mask embedding이 된다. Mask logit은 query별 embedding과 이미지 공통 mask feature map의 scaled dot product로 계산하며 channel 방향 dynamic 1×1 convolution과 같다. H/4×W/4 logit은 postprocessing에서 원본 크기로 복원한다.

Mask DINO와 달리 stride-4 backbone feature를 mask head에 직접 넘기지 않고 이미 융합된 PAN 출력만 사용한다.

### 3.2 Auxiliary와 Denoising Mask Supervision

최종 decoder layer뿐 아니라 intermediate layer에서도 mask logit을 계산해 auxiliary output으로 학습한다. Denoising query도 mask를 생성하고 동일한 cropped mask loss로 supervision한다. 이는 학습 시간·메모리만 늘리고 inference latency에는 영향을 주지 않는다.

### 3.3 Loss 함수

기존 D-FINE은 classification용 VFL 또는 focal loss, box용 L1·GIoU, D-FINE 전용 FGL·DDF loss를 사용한다. Instance segmentation에는 다음을 더한다.

- Matched ground-truth box ROI 안에서 계산하고 ROI 면적으로 정규화한 mask BCE
- Sigmoid probability에 대한 box-cropped Dice loss

Ground-truth mask를 mask head 해상도로 bilinear resize해 soft target으로 사용하고 matched instance별로 평균한다. 최종·intermediate decoder layer에 전체 loss를 적용한다.

가중치는 VFL 1, L1 5, GIoU 2, FGL 0.15, DDF 1.5, mask BCE 1, mask Dice 1이다.

### 3.4 Hungarian Matcher

기본 class, box L1, GIoU cost에 예측 mask와 resize된 ground-truth mask의 `1-Dice` 및 sigmoid focal mask cost를 추가한다. Training loss가 ROI crop 안에서 계산되는 것과 달리 matching mask cost는 mask head 출력 전체 map에서 계산한다.

### 3.5 후처리

낮은 confidence instance 제거, 원본 크기로 mask resize, threshold 이진화, 대응 bounding box 밖 pixel 제거 순서로 처리한다.

## 4. 구현

프레임워크는 custom dataset 학습, benchmark, export와 object detection·instance segmentation 추론을 제공한다. D-FINE 구조·loss·matcher를 채택했지만 나머지 pipeline과 segmentation head는 새로 구현했다.

논문 시점에는 mask head pretrained weight가 없어 backbone과 검출 부분은 COCO checkpoint로 시작하고 mask head는 scratch에서 학습했다. COCO mask pretraining은 향후 과제로 제시한다.

주요 기능에는 단일 config, backbone·decoder별 learning rate, mosaic augmentation, EMA checkpoint, gradient accumulation, DDP, mask-aware validation, RLE 기반 memory-efficient mask, WandB logging, format·batch·quantization benchmark와 annotation 오류 분석이 포함된다.

ONNX, TensorRT, OpenVINO export, FP16, OpenVINO INT8 quantization과 format별 inference code를 제공한다.

## 5. 실험

### Protocol

두 모델 모두 COCO pretrained weight에서 fine-tuning했다. Fixed confidence threshold에서 F1, precision, recall, IoU를 측정했다. TensorRT FP16으로 변환한 같은 모델에서 정확도와 latency를 동시에 측정했다.

End-to-end latency는 disk 읽기를 제외하고 resize, normalization, GPU transfer, forward, box scaling, mask resize와 cleanup을 포함한다. GPU 동기화 전후 시간을 측정하며 raw engine latency도 따로 보고한다.

### Metric

Ground truth와 prediction을 일대일 matching한다. Class가 같고 box 또는 mask IoU가 0.5보다 크면 TP다. 한 ground truth에 여러 prediction이 겹치면 가장 높은 IoU 하나만 TP이고 나머지는 FP다. Class mismatch는 FP 하나와 FN 하나로 계산한다.

Penalized IoU는 class-correct TP의 IoU 합을 `TP+FP+FN`으로 나눠 FP·FN에 0의 기여를 부여한다.

### TACO와 설정

TACO의 1,500개 이미지와 실제 instance가 있는 59개 waste class를 사용했다. Batch ID 기준 86/14 split으로 누수를 줄였고 validation은 212개 이미지다.

입력은 640×640이다. YOLO26은 100 epoch와 confidence 0.25, D-FINE-seg는 50 epoch와 confidence 0.5를 사용했다. 두 모델 모두 TensorRT FP16, batch 1이며 RTX 5070 Ti 16GB와 CUDA 12.8 환경에서 측정했다.

### 결과

논문은 segmentation에서 N/S/M/L/X 평균 F1 상대 개선 약 65%, latency overhead 약 10%를 보고한다. Detection에서는 F1 상대 개선 약 70%, latency overhead 약 1%를 보고한다.

COCO-style AP에서는 D-FINE-seg가 평균적으로 mask mAP 약 41%, D-FINE이 box mAP 약 49% 높았다고 보고한다. 단 YOLO26-M의 mask AP는 D-FINE-seg-M보다 높았다.

TensorRT FP16은 S 모델에서 Torch FP32보다 큰 latency 감소를 보이면서 F1을 거의 유지했다. Intel N150 OpenVINO INT8은 더 빠르지만 FP16·FP32보다 F1이 낮아 quantization trade-off를 보여준다.

## 6. 결론

TACO fine-tuning 설정에서 D-FINE-seg는 fixed-threshold F1과 정확도-latency 균형에서 YOLO26보다 좋은 결과를 보고했다. AP에서도 의미 있는 차이가 있었고 검출 D-FINE은 강한 결과를 보였다.

Apache 2.0 framework는 custom dataset 학습, 객체 검출·instance segmentation, 여러 hardware용 export와 추론을 지원한다. 다만 결과가 하나의 데이터셋과 특정 fine-tuning 설정에 제한되므로 다른 데이터셋·배포 조건에서의 평가가 후속 과제다.
