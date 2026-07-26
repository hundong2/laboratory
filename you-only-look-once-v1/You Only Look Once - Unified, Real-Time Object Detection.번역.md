# You Only Look Once: Unified, Real-Time Object Detection - 문장 대조 번역과 한국어 해설

작성일: 2026-07-26

## 논문 metadata

| 항목 | 내용 |
|---|---|
| 원문 제목 | You Only Look Once: Unified, Real-Time Object Detection |
| 저자 | Joseph Redmon, Santosh Divvala, Ross Girshick, Ali Farhadi |
| 발표 | CVPR 2016, pp. 779-788 |
| 식별자 | arXiv:1506.02640v5, DOI 10.48550/arXiv.1506.02640 |
| 최초 제출 | 2015-06-08 |
| 확인한 버전 | v5, 2016-05-09 |
| 원문 언어 | 영어 |
| 원문 | [arXiv](https://arxiv.org/abs/1506.02640), [PDF](https://arxiv.org/pdf/1506.02640v5), [CVF](https://openaccess.thecvf.com/content_cvpr_2016/html/Redmon_You_Only_Look_CVPR_2016_paper.html) |
| 접근일 | 2026-07-26 |
| 라이선스 표시 | arXiv perpetual non-exclusive distribution license |

## 번역·접근 범위

| section | 상태 | 제공 방식 |
|---|---|---|
| Abstract | 부분 번역 | 짧은 원문 1문장과 즉시 대조 번역, 나머지는 한국어 해설 |
| 1 Introduction | 완료 | 한국어 의미 해설 |
| 2 Unified Detection | 완료 | 한국어 의미 해설·수식·shape |
| 2.1 Network Design | 완료 | 한국어 구조 해설 |
| 2.2 Training | 완료 | 한국어 loss·학습 설정 해설 |
| 2.3 Inference | 완료 | decode·NMS 해설 |
| 2.4 Limitations | 완료 | 원문 한계 해설 |
| 3 Comparison | 완료 | 비교 관점 해설 |
| 4 Experiments | 완료 | 핵심 수치·오류 분석 |
| 5 Real-Time Detection | 완료 | webcam 적용 의미 해설 |
| 6 Conclusion | 완료 | 한국어 의미 해설 |
| References | 해당 없음 | 서지 목록은 원문 링크로 대체 |

### 저작권과 번역 방식

원문 페이지는 논문 텍스트 전체의 번역·재배포를 허용하는 오픈 라이선스를 표시하지 않는다. 따라서 원문 전체를 복제하지 않고 학습 목적의 짧은 문장 대조 예시 하나와 section별 한국어 의미 해설을 제공한다.

전문과 문장 단위로 대조하려면 이 파일과 [공식 PDF](https://arxiv.org/pdf/1506.02640v5)를 함께 연다.

## 읽기 전 핵심 배경

- 당시 detector는 sliding window, region proposal, classifier, box regression, NMS 등이 분리된 pipeline인 경우가 많았다.
- R-CNN 계열은 candidate region을 먼저 만들고 각 region에서 feature와 class를 계산했다.
- YOLO v1은 full image에서 box와 class probability를 한 번에 예측해 pipeline을 joint optimization한다.
- 빠른 대신 localization과 crowded small object에 구조적 약점이 있다.

## 문장 대조 번역

### Abstract

**S001 - Original**

We present YOLO, a new approach to object detection.

**S001 - 한국어**

(우리는 object detection을 위한 새로운 접근법인 YOLO를 제시한다.)

- **용어·약어 해설**
  - **YOLO (You Only Look Once)**: full image에서 box와 class probability를 한 network evaluation으로 예측하는 unified detector다.
  - **object detection(객체 탐지)**: image 속 여러 object의 class와 위치를 함께 예측하는 문제다.

## Section별 한국어 의미 해설

아래 내용은 원문 문장의 복제가 아니라 저자의 주장·수식·수치·한계를 한국어로 풀어쓴 학습용 해설이다.

### Abstract 해설

기존 detector는 classifier를 여러 위치나 region에 적용했다. YOLO는 detection을 spatially separated bounding box와 class probability를 직접 예측하는 regression으로 바꾼다. full image를 입력받은 단일 neural network가 한 evaluation에서 box와 class를 출력하며 전체 pipeline을 detection performance에 맞춰 end-to-end 최적화한다.

base model은 45 FPS, Fast YOLO는 155 FPS를 보고한다. Fast YOLO는 당시 다른 real-time detector보다 높은 mAP를 보였다. YOLO는 높은 속도와 낮은 background false positive가 장점이지만 정확한 localization에서는 더 많은 오류를 냈다. natural image에서 artwork로 domain이 바뀌는 실험에서는 DPM과 R-CNN보다 작은 성능 저하를 보고한다.

### 1. Introduction 해설

object detection은 image에 무엇이 있고 어디에 있는지 판단한다. 빠르고 정확한 detector는 driving, assistive device, responsive robotics에 중요하다.

DPM 같은 방법은 image 전체에서 sliding window classifier를 반복하고, R-CNN은 region proposal을 만든 뒤 각 candidate를 분류한다. 이런 pipeline은 component별로 따로 학습·조정해야 해 느리고 복잡하다.

YOLO는 pixel에서 box coordinate와 class probability로 바로 가는 single regression problem을 정의한다. full image context를 보므로 background patch를 object로 잘못 보는 오류를 줄일 수 있고, feature extraction과 detection objective를 함께 학습할 수 있다.

논문은 장점만 주장하지 않는다. state-of-the-art detector보다 accuracy가 낮고 특히 small object의 precise localization이 어렵다고 미리 밝힌다.

### 2. Unified Detection 해설

#### Grid와 responsibility

input image를 `S×S` cell로 나눈다. object center가 들어간 cell이 그 object를 담당한다. cell마다 `B`개 box와 각 box의 confidence, 그리고 cell 단위의 `C`개 conditional class probability를 예측한다.

$$
\mathrm{output\ shape}
=
S\times S\times(B\cdot5+C)
$$

PASCAL VOC에서는 `S=7`, `B=2`, `C=20`이므로 `7×7×30`이다. raw box는 98개다.

#### Box parameter

- `x, y`: cell boundary에 대한 center offset
- `w, h`: 전체 image size에 대한 normalized width와 height
- confidence: object 존재 가능성과 box IoU를 결합

$$
\mathrm{confidence}
=
\Pr(\mathrm{Object})
\times
\mathrm{IoU}^{\mathrm{truth}}_{\mathrm{pred}}
$$

object가 없으면 target은 0이고, 있으면 responsible predictor의 target은 ground-truth와 현재 prediction의 IoU다.

#### Class-specific score

cell은 object가 있다는 조건 아래 class probability를 예측한다.

$$
\Pr(\mathrm{Class}_i\mid\mathrm{Object})
\times
\Pr(\mathrm{Object})
\times
\mathrm{IoU}^{\mathrm{truth}}_{\mathrm{pred}}
$$

이 곱은 class probability와 localization quality를 하나의 score로 결합한다.

### 2.1 Network Design 해설

architecture는 GoogLeNet에서 영감을 받았다. 24개 convolutional layer 뒤에 2개 fully connected layer가 있으며 `1×1` reduction과 `3×3` convolution을 번갈아 사용한다. final output은 `7×7×30` tensor다.

Fast YOLO는 convolutional layer를 9개로 줄이고 filter 수도 줄인다. network size 이외의 training·test parameter는 같게 두어 speed-accuracy trade-off를 비교한다.

### 2.2 Training 해설

#### Classification pretraining에서 detection으로

ImageNet 1000-class classification으로 앞의 20 convolutional layer를 `224×224` input에서 pretrain한다. 그 뒤 detection용 convolutional layer 4개와 fully connected layer 2개를 추가하고 input을 `448×448`로 높인다.

final layer는 linear activation을 사용하고 나머지는 negative 구간 slope가 0.1인 leaky ReLU를 사용한다.

#### 왜 단순 squared error가 문제인가

localization error와 classification error를 같은 scale로 다루며, object가 없는 수많은 cell의 confidence gradient가 object cell을 압도할 수 있다. 큰 box와 작은 box의 동일한 coordinate 차이도 같은 값으로 계산돼 detection metric과 완전히 정렬되지 않는다.

이를 완화하려고 coordinate loss는 `λ_coord=5`, no-object confidence는 `λ_noobj=0.5`를 사용한다. width와 height에는 square root를 적용한다.

#### Responsible predictor

한 cell의 여러 box predictor 중 ground-truth와 현재 IoU가 가장 높은 predictor만 해당 object의 coordinate와 confidence 책임을 진다. 이 hard assignment는 predictor별 specialization을 유도한다.

#### Loss의 다섯 부분

1. responsible predictor의 `x, y` squared error
2. responsible predictor의 `√w, √h` squared error
3. object가 있는 responsible predictor confidence
4. object가 없는 predictor confidence에 `λ_noobj`
5. object가 있는 cell의 class probability

classification error는 object가 있는 cell에서만, coordinate error는 responsible predictor에서만 계산한다.

#### Training hyperparameter

- 약 135 epoch
- batch size 64
- momentum 0.9
- decay 0.0005
- learning rate를 `10⁻³`에서 `10⁻²`로 점진 증가
- `10⁻²` 75 epoch, `10⁻³` 30 epoch, `10⁻⁴` 30 epoch
- first fully connected layer 뒤 dropout 0.5
- 최대 20% scale·translation augmentation
- HSV exposure·saturation을 최대 1.5배 조절

원문은 초기 learning-rate 증가가 몇 epoch인지 숫자를 명시하지 않으므로 임의로 보완하지 않는다.

### 2.3 Inference 해설

PASCAL VOC 설정에서 image당 98개 box를 한 network evaluation으로 예측한다. grid 구조 때문에 대부분 object는 한 cell의 한 box로 나오지만 큰 object나 cell boundary의 object는 중복 detection이 생길 수 있다.

NMS는 높은 score box를 남기고 많이 겹치는 같은 class box를 제거한다. 논문은 NMS가 2-3% mAP 개선을 제공한다고 보고한다. NMS가 있다는 사실은 YOLO가 post-processing이 전혀 없는 detector라는 뜻이 아님을 보여준다.

### 2.4 Limitations 해설

- cell당 box 2개와 class probability set 1개라는 spatial constraint
- flock of birds처럼 모여 있는 small object를 표현하기 어려움
- 새로운 aspect ratio나 unusual configuration에 약함
- 여러 downsampling layer 때문에 coarse feature로 box를 예측
- squared-error objective와 IoU·average precision 사이의 mismatch
- 가장 큰 error source가 incorrect localization

### 3. 다른 detector와의 비교 해설

#### DPM

sliding window, hand-crafted feature, region classification과 box prediction이 분리된 pipeline이다. YOLO는 feature와 box·class를 하나의 convolutional network에서 joint optimization한다.

#### R-CNN

Selective Search가 약 2,000개 proposal을 만들고 CNN·SVM·box regressor·NMS를 순차 적용한다. YOLO는 98개 raw box만 예측하고 full image context를 사용한다.

#### Faster R-CNN

proposal 단계도 neural network로 바꿔 R-CNN을 빠르게 하지만 논문 당시 비교에서는 YOLO보다 느리고 높은 accuracy를 보였다. 비교의 핵심은 단일 숫자 승패보다 speed-accuracy trade-off다.

#### MultiBox·OverFeat·MultiGrasp

이전 연구도 network로 region 또는 localization을 예측했지만 완전한 general-purpose detection pipeline이 아니거나 local view에 의존했다. YOLO는 multiple class와 multiple object를 full image에서 동시에 예측한다.

### 4. Experiments 해설

#### Real-time system 비교

| model | mAP | FPS |
|---|---:|---:|
| Fast YOLO | 52.7 | 155 |
| YOLO | 63.4 | 45 |
| YOLO VGG-16 | 66.4 | 21 |
| Fast R-CNN | 70.0 | 0.5 |
| Faster R-CNN VGG-16 | 73.2 | 7 |

Fast YOLO는 speed를 크게 높인 대신 mAP가 낮고, VGG-16 backbone은 mAP를 높이지만 real-time threshold 아래로 느려진다.

#### Error analysis

| detector | correct | localization | similar class | other class | background |
|---|---:|---:|---:|---:|---:|
| Fast R-CNN | 71.6% | 8.6% | 4.3% | 1.9% | 13.6% |
| YOLO | 65.5% | 19.0% | 6.75% | 4.0% | 4.75% |

YOLO는 localization error가 많고 Fast R-CNN은 background error가 많다. 두 model의 다른 failure mode를 이용해 결합했을 때 Fast R-CNN 71.8 mAP가 75.0으로 3.2 point 증가했다.

#### VOC 2012

YOLO 단독은 57.9% mAP를 보고한다. bottle, sheep, TV/monitor 같은 small object category에서 경쟁 model보다 낮고 cat·train에서는 상대적으로 높았다. Fast R-CNN과 결합하면 Fast R-CNN 단독보다 2.3 point 향상됐다고 보고한다.

#### Artwork generalization

Picasso와 People-Art dataset에서 person detection을 평가한다. R-CNN은 natural image에서 artwork로 바뀔 때 크게 하락했고 YOLO는 상대적으로 작은 하락을 보였다. 저자들은 full-image context와 object shape·relationship modeling이 도움이 됐다고 해석한다.

이 실험만으로 모든 out-of-distribution 상황에 강하다고 단정하면 안 된다. class, domain, dataset 수가 제한되어 있다.

### 5. Real-Time Detection in the Wild 해설

webcam에 연결해 image capture와 display 시간을 포함해 interactive detection을 시연한다. 각 frame을 독립 처리하지만 연속 화면에서는 tracking처럼 보일 수 있다. 실제 temporal association을 수행하는 tracker와는 구분해야 한다.

### 6. Conclusion 해설

저자들은 full image에서 직접 detection loss를 joint optimization하는 unified model을 제시했다고 정리한다. Fast YOLO는 당시 general-purpose detector 중 매우 빠른 성능을, YOLO는 real-time 조건에서 높은 정확도를 제공했다.

새 domain에도 잘 일반화한다고 평가하지만 동시에 논문 본문은 localization과 small object 한계를 분명히 제시한다. 제품 적용에서는 평균 mAP보다 target hazard와 관련된 failure mode를 더 세밀하게 검증해야 한다.

## 수식·그림 검수 기록

- PDF 10페이지를 PNG로 렌더링하고 page 1, 2, 3, 4, 6, 7, 8을 시각 대조했다.
- Figure 1의 resize → network → threshold 흐름을 확인했다.
- Figure 2의 `S×S×(B×5+C)` tensor와 `7×7×30` 설정을 확인했다.
- Figure 3의 24 convolution + 2 fully connected architecture를 확인했다.
- 식 (3)의 coordinate, size, object, no-object, class loss 항을 확인했다.
- Table 1의 Fast YOLO 155 FPS·52.7 mAP, YOLO 45 FPS·63.4 mAP를 확인했다.
- Figure 4의 YOLO localization 19.0%, background 4.75%를 확인했다.
- Table 3의 VOC 2012 YOLO 57.9 mAP를 확인했다.
- Figure 5·6의 artwork generalization과 qualitative failure example을 확인했다.

## 약어 및 기술 용어 사전

| 원어·약어 | 한국어 | 의미 | 최초 등장 |
|---|---|---|---|
| YOLO | You Only Look Once | single-evaluation unified detector | S001 |
| object detection | 객체 탐지 | 여러 object의 class와 위치를 예측 | S001 |
| bounding box | 경계 상자 | object 위치를 나타내는 직사각형 | Abstract |
| regression | 회귀 | continuous coordinate·score를 직접 예측 | Abstract |
| CNN | 합성곱 신경망 | convolution으로 image feature를 추출 | Introduction |
| DPM | 변형 가능 부품 모델 | part 기반 sliding-window detector | Introduction |
| R-CNN | 영역 기반 CNN | proposal별 feature와 class를 계산 | Introduction |
| region proposal | 영역 제안 | object일 가능성이 있는 candidate box | Introduction |
| end-to-end | 종단간 학습 | 전체 pipeline parameter를 한 objective로 학습 | Abstract |
| grid cell | 격자 셀 | object center responsibility 단위 | 2 |
| IoU | 교집합/합집합 비율 | 두 box overlap 품질 지표 | 2 |
| confidence | 신뢰도 | object 존재와 localization 품질의 결합 값 | 2 |
| conditional class probability | 조건부 class 확률 | object가 있을 때 해당 class일 확률 | 2 |
| class-specific score | class별 score | class probability와 box confidence의 곱 | 2 |
| leaky ReLU | 리키 렐루 | 음수 영역에 작은 slope를 둔 activation | 2.2 |
| responsible predictor | 담당 predictor | ground truth와 현재 IoU가 가장 높은 box head | 2.2 |
| lambda_coord | coordinate loss weight | box coordinate 오차를 강조하는 5 | 2.2 |
| lambda_noobj | no-object loss weight | background confidence 오차를 줄이는 0.5 | 2.2 |
| dropout | 드롭아웃 | 일부 activation을 제거하는 regularization | 2.2 |
| HSV | 색상·채도·명도 계열 색 공간 | exposure·saturation augmentation에 사용 | 2.2 |
| NMS | 비최대 억제 | 겹치는 낮은 score box를 제거 | 2.3 |
| AP | 평균 정밀도 | 한 class의 precision-recall 성능 요약 | 4 |
| mAP | 평균 AP | 여러 class AP의 평균 | Abstract |
| FPS | 초당 frame 수 | throughput 지표 | Abstract |
| false positive | 위양성 | object가 없는데 있다고 예측 | Abstract |
| localization error | 위치 추정 오류 | class는 맞지만 IoU가 기준보다 낮은 오류 | 4.2 |
| PASCAL VOC | 시각 객체 분류 challenge | 논문 detection 학습·평가 dataset | 2.1 |
| ImageNet | 대규모 image classification dataset | backbone pretraining에 사용 | 2.2 |
| domain shift | 도메인 변화 | train과 test 분포가 달라지는 현상 | 4.5 |
| precision-recall curve | 정밀도-재현율 곡선 | threshold별 precision과 recall 관계 | 4.5 |

## 다음 읽기

- [한국어 학습 가이드](README.md)
- [IoU와 confidence 기초](01_foundations.ipynb)
- [grid decode와 NMS](02_practice.ipynb)
- [YOLO loss와 AP](03_advanced.ipynb)
