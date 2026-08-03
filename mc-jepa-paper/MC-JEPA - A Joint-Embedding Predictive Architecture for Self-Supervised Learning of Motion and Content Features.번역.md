# MC-JEPA - A Joint-Embedding Predictive Architecture for Self-Supervised Learning of Motion and Content Features - 번역·해설

## 논문 metadata

| 항목 | 내용 |
|---|---|
| 원문 제목 | MC-JEPA: A Joint-Embedding Predictive Architecture for Self-Supervised Learning of Motion and Content Features |
| 저자 | Adrien Bardes, Jean Ponce, Yann LeCun |
| 출판 정보 | arXiv preprint, 2023 |
| 식별자 | arXiv:2307.12698, DOI: 10.48550/arXiv.2307.12698 |
| 원문 | [arXiv v1](https://arxiv.org/abs/2307.12698v1) |
| 사용 버전 | v1, 2023-07-24, 20쪽 |
| 원문 언어 | 영어 |
| 접근일 | 2026-08-03 |
| 확인 라이선스 | [arXiv non-exclusive distribution license](https://arxiv.org/licenses/nonexclusive-distrib/1.0/) |

## 번역·접근 범위

PDF 전체를 확인했지만 라이선스가 전문 번역·재배포를 허용하는 오픈 라이선스는
아닙니다. 저작권을 준수하기 위해 25단어 이내의 문장 하나만 대조 번역하고,
나머지는 section별 한국어 해설로 제공합니다. 표·그림은 복제하지 않고 핵심
수치와 읽는 방법을 설명합니다.

| 원문 범위 | 상태 | 이 파일의 처리 |
|---|---|---|
| 제목·metadata | 완료 | 서지 정보 보존 |
| Abstract | 완료 | 한국어 요약 |
| 1. Introduction | 완료 | 주장·기여 해설 |
| 2. Related Work | 완료 | 연구군별 요약 |
| 3. Proposed Approach | 완료 | 수식·architecture 해설 |
| 4. Experiments | 완료 | dataset·metric·결과·ablation 해설 |
| 5. Conclusion | 부분 번역 | 문장 1개 대조와 요약 |
| Appendix A~E | 완료 | 구현·hyperparameter·추가 결과 해설 |
| References | 해당 없음 | 원문 서지 목록 참조 |

## 읽기 전 핵심 배경

- **content feature:** 객체와 장면을 식별·구분하는 의미 정보
- **motion feature:** frame 간 위치와 이동을 나타내는 정보
- **optical flow:** 각 pixel이 다음 frame에서 이동한 2차원 벡터
- **multi-task learning:** 여러 목적이 같은 encoder parameter를 공유하는 학습
- **VICReg:** invariance, variance, covariance 항을 쓰는 자기지도학습 목적
- **coarse-to-fine:** 낮은 해상도 예측을 높은 해상도에서 반복 보정하는 방식

## 제목

**한국어 제목**

MC-JEPA: 움직임과 내용 특징의 자기지도학습을 위한 결합 임베딩 예측 아키텍처

## Abstract 해설

기존 visual self-supervised learning은 객체 내용 표현에 집중해 pixel 수준 motion과
위치를 놓치기 쉽고, optical-flow 모델은 대응점은 찾지만 image content를 이해하지
않는다는 문제의식에서 출발합니다. MC-JEPA는 하나의 shared encoder 안에서
content self-supervision과 optical-flow estimation을 공동 최적화합니다. 연구진은
두 목적이 서로 도움을 주어 motion 정보를 포함한 content feature를 학습하며,
flow benchmark와 image/video segmentation에서 경쟁력 있는 결과를 얻었다고
보고합니다.

## 1. Introduction 해설

분류·행동 인식용 global feature와 detection·segmentation용 local feature 연구는
대부분 content를 중심으로 발전했습니다. 반면 optical flow는 synthetic label 의존을
줄이기 위해 photometric consistency 기반 self-supervision을 사용하지만, 의미
표현이 빈약해 downstream transfer가 제한될 수 있습니다.

논문은 다음 기여를 제시합니다.

1. PWC-Net 기반 flow estimation에 backward consistency와 layer별
   variance-covariance regularization을 더한 M-JEPA
2. M-JEPA와 ImageNet VICReg를 shared encoder에서 결합한 MC-JEPA
3. optical flow, image segmentation, video object segmentation을 하나의
   encoder로 평가한 실험

## 2. Related Work 해설

### Self-supervised learning

contrastive, clustering, non-contrastive, covariance regularization 계열과 image·
video representation learning을 정리합니다. MC-JEPA content branch는 VICReg를
직접 사용합니다.

### Optical flow estimation

고전적인 matching·smoothness 최적화, supervised CNN, photometric consistency
기반 unsupervised flow, distillation·geometric constraint·augmentation consistency
연구를 비교합니다.

### Correspondence와 multi-task

pixel/object tracking용 correspondence 학습은 motion을 포착하지만 일반 content
task로의 전이가 약할 수 있습니다. 저자는 shared visual representation에서 image
SSL과 flow estimation을 동시에 학습하는 단순한 multi-task 구성이 드물었다고
봅니다.

## 3. Proposed Approach 해설

### 3.1 Optical Flow - M-JEPA

#### Coarse-to-fine residual flow

```text
f^(l+1) = Fθ(X_t^(l), X_(t+1)^(l), f^(l))
```

각 feature pyramid level에서 현재 flow로 `X_t`를 warp하고 `X_(t+1)`과의 4D
correlation volume을 계산합니다. estimator가 residual을 예측해 점진적으로
해상도와 정밀도를 높입니다.

#### Feature regression과 reconstruction

```text
L_reg = Σ_l ||X_(t+1)^(l) - warp(X_t^(l), f^(l))||²₂
L_rec = d(I_(t+1), warp(I_t, f))
```

`d`는 L1, L2, SSIM의 선형 조합입니다. feature-level prediction과 image-level
photometric consistency를 동시에 사용합니다.

#### Smoothness

image gradient가 작은 위치에서는 flow gradient를 강하게 억제하고, 실제 edge가
있는 곳에서는 제약을 완화합니다. texture가 없거나 반복되는 영역의 모호성을
완화하려는 inductive bias입니다.

#### Cycle consistency

forward flow로 warp한 뒤 backward flow를 적용한 feature가 원 feature와
가까워지도록 합니다. occlusion처럼 양방향 correspondence가 없는 pixel은
compatibility mask로 제외합니다.

#### Variance-covariance regularization

```text
L_vc = variance hinge + covariance off-diagonal penalty
```

각 feature dimension의 표준편차가 임계값 아래로 무너지는 것을 막고, 서로 다른
dimension의 중복을 줄입니다. 논문은 multi-task training의 collapse와 exploding
gradient를 줄이기 위해 여러 encoder layer에 적용합니다.

### 3.2 Multi-task Self-Supervised Learning - MC-JEPA

ImageNet image의 두 augmentation view를 shared encoder와 expander에 넣고 VICReg
`L_ssl`을 계산합니다. 같은 iteration에 video batch의 flow loss도 계산해 합산한
후 encoder·expander·flow estimator에 역전파합니다.

```text
L_total = Σ_(video) (L_rec + L_reg + L_smooth + L_cycle + L_vc)
          + Σ_(image) L_ssl
```

실제 최적화에는 항별 계수가 필요합니다. 특히 motion/content balancing이
segmentation 성능과 flow EPE 사이의 trade-off를 결정합니다.

## 4. Experiments 해설

### 4.1 Datasets와 metrics

- content pretraining: ImageNet-1K
- flow training/evaluation: KITTI, MPI Sintel, FlyingChairs, FlyingThings, HD1K
- image segmentation: Pascal VOC, Cityscapes, ADE20K
- video segmentation/tracking: DAVIS 2017
- EPE: flow vector의 end-point error, 낮을수록 좋음
- mIoU와 `(J&F)_m`: segmentation 품질, 높을수록 좋음

### 4.2 Main results

MC-JEPA는 KITTI train EPE 2.67, Sintel clean/final train EPE 2.81/3.51을
보고합니다. Pascal VOC frozen/fine-tuned mIoU는 67.1/79.9, Cityscapes는
65.5/78.4, ADE20K는 30.8/44.2입니다. DAVIS 2017 `(J&F)_m`은 70.5입니다.

flow 전용 SMURF가 optical-flow benchmark에서 더 낫지만, MC-JEPA는 MCRW보다
좋고 image/video segmentation에서도 강한 결과를 보여 하나의 encoder로 두
종류의 정보를 다루려는 목적을 뒷받침합니다.

### 4.3 Ablations

- 모든 flow dataset을 더하면 flow EPE는 좋아지지만 segmentation 변화는 작아,
  motion supervision의 전이 이득이 특정 flow domain에만 의존하지 않았습니다.
- LayerNorm 없는 estimator는 학습이 붕괴했고 L2 normalization은 flow range를
  직접 제한해 비효율적이었습니다.
- PWC backbone은 flow EPE는 좋았지만 content segmentation이 매우 낮았고,
  ConvNeXt-T가 두 목적의 균형에서 가장 좋았습니다.
- frozen/fine-tuned flow head, epoch alternation보다 batch alternation과 combined
  loss가 좋았습니다.
- flow는 10 epoch 후 시작하는 편이 좋았고, cycle coefficient와 task weight는
  민감했습니다.

## 5. Conclusion

**S001 — Original**

We have introduced MC-JEPA, a multi-task approach to learning of motion and content features with self-supervised learning and optical flow estimation.

**S001 — 한국어**

(우리는 자기지도학습과 optical-flow estimation으로 움직임과 내용 특징을
학습하는 다중 작업 접근법 MC-JEPA를 제안했다.)

- **용어·약어 해설**
  - **MC-JEPA(Motion-Content Joint-Embedding Predictive Architecture,
    움직임-내용 결합 임베딩 예측 아키텍처):** motion과 content 목적이 encoder를
    공유하는 제안 모델입니다.
  - **multi-task learning(다중 작업 학습):** 여러 loss가 공유 parameter를 함께
    갱신하는 학습 방식입니다.

연구진은 motion과 content를 함께 학습한 표현이 flow와 image/video segmentation
전반에 유용하다고 결론짓습니다. 향후에는 더 큰 자연 video, 같은 data domain에서
두 목적의 공동 학습, short/long-range interaction의 계층적 모델링을 제시합니다.

## Appendix 해설

### A. Implementation Details

학습 불안정의 원인은 flow estimator의 norm·gradient 폭발과 NaN 전파였습니다.
LayerNorm, flow range clipping, 별도 learning rate·weight decay가 핵심 안정화
요소입니다. ConvNeXt-T stem을 수정해 6-level feature pyramid를 만듭니다.

### B. Hyper-parameters

8개 V100 32GB, 100 epoch, AdamW, content batch 384, flow batch 8을 사용합니다.
encoder와 flow estimator의 learning rate를 각각 `3e-4`, `1e-4`로 분리합니다.
flow는 epoch 10부터 시작하고 output을 128로 clip합니다. Table 7의 dataset 반복
횟수와 Table 8의 layer별 loss coefficient도 재현에 필수입니다.

### C. Architecture Details

ConvNeXt stem의 kernel과 stride를 나누고 PWC estimator의 마지막 layer를 제외한
각 convolution 뒤에 LayerNorm을 넣습니다. filter factor는 2입니다.

### D. Additional Results

KITTI·Sintel의 occluded/non-occluded EPE와 DAVIS의 region similarity `J_m`, contour
accuracy `F_m`을 분리해 제공합니다. MC-JEPA의 DAVIS 결과는 `J_m=67.0`,
`F_m=74.0`입니다.

### E. Additional Ablation

VC 없음, 마지막 layer만, 모든 layer, warmup epoch를 비교합니다. 모든 layer에
VC를 적용하면 안정성과 성능이 개선됐고 1 epoch warmup이 최종 segmentation에
가장 좋았습니다. 2 epoch warmup은 오히려 성능을 떨어뜨려 “더 긴 안정화가 항상
좋다”는 해석을 경계해야 합니다.

## 수식·그림·표 읽기 가이드

- **Figure 1:** 위쪽 image views와 아래쪽 video frames가 encoder weight를
  공유하지만 서로 다른 objective head로 갑니다.
- **Figure 2:** 6-level feature pyramid, warping, correlation과 residual flow
  refinement를 따라갑니다.
- **Table 1:** EPE는 낮을수록, mIoU와 `(J&F)_m`은 높을수록 좋으므로 화살표를
  확인해야 합니다. 원문 caption의 F1 화살표 표기는 문구상 모순이 있어 실제로는
  error이므로 낮을수록 좋게 읽어야 합니다.
- **Figure 5:** task weight 0.1 부근까지 두 metric이 좋아지지만 이후
  segmentation이 급락하는 trade-off를 봅니다.
- **Table 11:** collapse 방지와 layer별 VC 적용의 효과를 flow와 segmentation
  양쪽에서 읽습니다.

## 약어 및 기술 용어 사전

| 원어·약어 | 한국어 | 논문에서의 역할 | 최초 등장 |
|---|---|---|---|
| MC-JEPA | 움직임-내용 JEPA | motion/content 공동 학습 모델 | S001 |
| SSL | 자기지도학습 | label 없이 content 표현 학습 | S001 |
| optical flow | 광류 | frame 간 pixel 이동과 motion pretext | S001 |
| M-JEPA | 움직임 JEPA | flow branch만 학습하는 변형 | 1절 해설 |
| VICReg | 분산-불변성-공분산 정규화 | content objective와 collapse 방지 | 배경 해설 |
| PWC-Net | Pyramid, Warping, Cost volume network | coarse-to-fine flow estimator 기반 | 3절 해설 |
| EPE | 끝점 오차 | flow 평가 metric | 4절 해설 |
| mIoU | 평균 교집합/합집합 | image segmentation metric | 4절 해설 |
| DAVIS | Densely Annotated VIdeo Segmentation | video object segmentation benchmark | 4절 해설 |

## 번역 검수 기록

- v1 PDF 20쪽의 본문·부록 순서를 확인했습니다.
- architecture·method, main ablation, task balancing, VC ablation과 qualitative
  flow page를 렌더링해 추출 text와 대조했습니다.
- metric 방향, dataset, frozen/fine-tuned protocol을 구분했습니다.
- 논문이 명시한 결과와 분석자가 도출한 한계를 분리했습니다.
- 저작권 경계에 따라 원문 직접 재현은 S001 한 문장으로 제한했습니다.

## 함께 보기

- [논문 분석 README](README.md)
- [12가지 JEPA 비교](../twelve-jepa-architectures/README.md)
- [원문 PDF](https://arxiv.org/pdf/2307.12698v1)
