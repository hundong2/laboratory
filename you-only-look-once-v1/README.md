# YOLO v1 논문 학습 가이드

작성일: 2026-07-26

## 출처와 작업 범위

- 논문: [You Only Look Once: Unified, Real-Time Object Detection](https://arxiv.org/abs/1506.02640)
- 출판 기록: [CVPR 2016 Open Access Repository](https://openaccess.thecvf.com/content_cvpr_2016/html/Redmon_You_Only_Look_CVPR_2016_paper.html)
- 저자: Joseph Redmon, Santosh Divvala, Ross Girshick, Ali Farhadi
- 발표: IEEE Conference on Computer Vision and Pattern Recognition, CVPR 2016, pp. 779-788
- 최초 arXiv 제출: 2015-06-08
- 확인한 버전: arXiv v5, 2016-05-09
- 확인일: 2026-07-26
- 분야: Computer Vision and Pattern Recognition
- 원문 언어: 영어
- PDF 상태: 10페이지, 암호화 없음, 다단 편집·수식·표·그림을 전 페이지 렌더링하고 핵심 페이지 시각 검수

arXiv에는 perpetual non-exclusive distribution license가 표시되어 있으며 논문 텍스트 전체를 재배포할 수 있는 오픈 라이선스로 확인되지는 않았다. 따라서 [번역 자료](You%20Only%20Look%20Once%20-%20Unified,%20Real-Time%20Object%20Detection.번역.md)는 짧은 문장 대조 예시와 section별 한국어 해설로 구성한다.

## 한눈에 보기

YOLO v1의 가장 중요한 아이디어는 object detection을 “후보 영역 생성 → 각 영역 분류 → box 보정”의 여러 단계가 아니라, 전체 image에서 bounding box와 class probability를 한 network가 직접 예측하는 regression 문제로 재구성한 것이다.

처리 흐름은 간단하다.

1. image를 `448×448`로 resize한다.
2. convolutional network를 한 번 실행한다.
3. `7×7×30` prediction tensor를 box·confidence·class probability로 decode한다.
4. class-specific score threshold와 NMS로 최종 detection을 만든다.

이 논문에서 “You Only Look Once”는 image를 한 번만 읽는다는 문자적 뜻보다, detection을 위한 단일 network evaluation과 unified optimization을 강조한다.

## 먼저 구분해야 할 것

### YOLO v1과 현대 YOLO 구현은 같지 않다

이 자료는 2015-2016년의 원 논문 architecture와 loss를 다룬다. 이후 YOLO 계열은 anchor, multi-scale feature, 새로운 assignment와 loss, decoupled head 등 많은 변화를 거쳤다. 최신 library의 `YOLO` class를 실행한 결과를 YOLO v1 재현이라고 부르면 안 된다.

### “End-to-end”에도 post-processing은 있다

논문은 전체 detector를 하나의 network로 joint training한다. 하지만 inference에서는 score threshold와 non-maximal suppression(NMS)을 사용한다. 따라서 제품 latency를 측정할 때 preprocessing, network, decoding, NMS, data transfer를 모두 포함해야 한다.

### FPS는 hardware·batch·pipeline 조건과 함께 읽는다

논문은 Titan X GPU에서 batch processing 없이 base YOLO 45 FPS, Fast YOLO 155 FPS를 보고한다. 이 숫자는 2016년 당시 구현과 hardware 조건의 결과다. 다른 장치에서 network forward만 측정한 FPS와 직접 비교하면 안 된다.

## 기초 개념

### Classification과 detection

- image classification: image 전체에 class label을 부여한다.
- object localization: object 하나의 위치를 box로 찾는다.
- object detection: 여러 object의 class와 box를 동시에 찾는다.

YOLO v1은 detection을 image pixel에서 box coordinate와 class probability로 가는 regression으로 본다.

### Bounding box 표현

각 box predictor는 다섯 값을 낸다.

| 값 | YOLO v1 의미 |
|---|---|
| `x`, `y` | object center가 속한 grid cell 내부의 상대 offset |
| `w`, `h` | 전체 image width·height에 대한 상대 크기 |
| confidence | object 존재 확률과 predicted box IoU를 결합한 값 |

좌표 convention을 섞으면 학습과 평가가 모두 틀어진다. 실습에서는 다음 두 형식을 명시적으로 구분한다.

- center form: `(cx, cy, w, h)`
- corner form: `(x_min, y_min, x_max, y_max)`

### Intersection over Union

$$
\mathrm{IoU}(A,B)
=
\frac{|A\cap B|}{|A\cup B|}
$$

box가 겹치지 않으면 0, 완전히 같으면 1이다. 분모가 0인 invalid box는 조용히 계산하지 않고 입력 오류로 처리해야 한다.

### Grid responsibility

input image를 `S×S` grid로 나눈다. ground-truth object center가 들어간 cell이 그 object를 담당한다. 각 cell은 `B`개 box와 `C`개 conditional class probability를 예측한다.

PASCAL VOC 설정은 다음과 같다.

- `S = 7`
- `B = 2`
- `C = 20`
- output shape: `7 × 7 × (2×5 + 20) = 7 × 7 × 30`
- image당 raw box 수: `7 × 7 × 2 = 98`

한 cell에는 class probability set이 하나뿐이다. 가까이 모인 여러 작은 object나 같은 cell에 중심이 들어가는 서로 다른 class를 표현하기 어렵다는 구조적 한계가 있다.

## Confidence와 class-specific score

논문은 box confidence를 다음처럼 정의한다.

$$
\mathrm{confidence}
=
\Pr(\mathrm{Object})\times
\mathrm{IoU}^{\mathrm{truth}}_{\mathrm{pred}}
$$

test time에는 cell의 conditional class probability와 box confidence를 곱한다.

$$
\Pr(\mathrm{Class}_i\mid\mathrm{Object})
\times
\Pr(\mathrm{Object})
\times
\mathrm{IoU}^{\mathrm{truth}}_{\mathrm{pred}}
$$

이 값은 해당 class가 있을 가능성과 box localization 품질을 함께 나타내는 class-specific score가 된다.

학습 시 object가 없는 cell의 confidence target은 0이다. object가 있으면 responsible predictor의 confidence target은 ground-truth와 prediction의 IoU다.

## Architecture

### Network

- input: `448×448×3`
- 24 convolutional layers
- 2 fully connected layers
- 중간의 `1×1` convolution으로 channel을 줄인 뒤 `3×3` convolution 수행
- final output: `7×7×30`
- hidden activation: leaky ReLU
- final layer: linear activation

$$
\phi(x)=
\begin{cases}
x, & x>0\\
0.1x, & \text{otherwise}
\end{cases}
$$

### Pretraining과 detection fine-tuning

1. ImageNet 1000-class classification으로 앞의 20 convolutional layer를 `224×224`에서 pretrain한다.
2. detection용 convolutional layer 4개와 fully connected layer 2개를 추가한다.
3. 더 세밀한 위치 정보가 필요하므로 input resolution을 `448×448`로 올린다.
4. PASCAL VOC의 box·class annotation으로 전체 network를 detection objective에 맞춰 학습한다.

이 과정은 “classification representation → detection localization” transfer learning의 전형적인 예다. 오늘날 다른 backbone을 사용할 때도 pretrained feature, head 교체, label mapping, resolution, normalization contract를 함께 관리해야 한다.

## YOLO v1 loss

전체 loss는 다섯 부분으로 읽는 편이 쉽다.

### 1. Responsible box의 center coordinate

$$
\lambda_{\mathrm{coord}}
\sum_{i,j}\mathbb{1}_{ij}^{\mathrm{obj}}
\left[
(x_i-\hat{x}_i)^2
+
(y_i-\hat{y}_i)^2
\right]
$$

ground-truth object에 대해 현재 IoU가 가장 높은 predictor만 coordinate loss를 받는다.

### 2. Responsible box의 width와 height

$$
\lambda_{\mathrm{coord}}
\sum_{i,j}\mathbb{1}_{ij}^{\mathrm{obj}}
\left[
(\sqrt{w_i}-\sqrt{\hat{w}_i})^2
+
(\sqrt{h_i}-\sqrt{\hat{h}_i})^2
\right]
$$

큰 box에서 같은 절대 오차가 작은 box보다 덜 중요하도록 square root를 사용한다. 그러나 논문도 이 방식이 small-box localization 문제를 완전히 해결하지 못한다고 설명한다.

### 3. Object가 있는 responsible box confidence

$$
\sum_{i,j}\mathbb{1}_{ij}^{\mathrm{obj}}
(C_i-\hat{C}_i)^2
$$

### 4. Object가 없는 box confidence

$$
\lambda_{\mathrm{noobj}}
\sum_{i,j}\mathbb{1}_{ij}^{\mathrm{noobj}}
(C_i-\hat{C}_i)^2
$$

대부분 cell이 background이므로 이 항이 gradient를 압도하지 않도록 낮은 weight를 준다.

### 5. Object가 있는 cell의 class probability

$$
\sum_i\mathbb{1}_i^{\mathrm{obj}}
\sum_{c\in\mathrm{classes}}
(p_i(c)-\hat{p}_i(c))^2
$$

classification loss는 object가 있는 cell에만 적용한다.

### Loss weight

- `λ_coord = 5`
- `λ_noobj = 0.5`

sum-squared error는 최적화하기 쉽지만 mAP와 완전히 일치하지 않는다. localization과 classification error를 같은 형태의 제곱오차로 취급한다는 한계도 논문이 직접 인정한다.

## Responsible predictor assignment

한 cell이 box 두 개를 예측하더라도 ground-truth object 하나에는 현재 IoU가 가장 높은 predictor 하나만 coordinate·object confidence 책임을 준다.

이 규칙은 predictor가 서로 다른 size, aspect ratio, class에 specialization하도록 유도할 수 있다. 반면 hard assignment가 step마다 바뀌어 target이 불연속적으로 변할 수 있으므로 debug할 때 assignment 결과를 반드시 기록해야 한다.

## Training 설정

- dataset: PASCAL VOC 2007과 2012 train·validation
- 약 135 epoch
- batch size: 64
- momentum: 0.9
- weight decay: 0.0005
- learning rate: `10⁻³`에서 `10⁻²`로 천천히 상승한 뒤 `10⁻²` 75 epoch, `10⁻³` 30 epoch, `10⁻⁴` 30 epoch
- dropout: 첫 fully connected layer 뒤 0.5
- augmentation: 원 image size의 최대 20% random scale·translation
- HSV exposure·saturation: 최대 1.5배 변화

원문은 learning-rate 상승 구간의 정확한 epoch 수를 명시하지 않는다. 재현 문서에서는 이를 임의로 채우지 말고 implementation 또는 공개 configuration과 대조해야 한다.

## Inference

### Decode

1. cell offset `x, y`를 image 전체 center coordinate로 바꾼다.
2. normalized `w, h`를 image 크기로 바꾼다.
3. box confidence와 conditional class probability를 곱한다.
4. threshold보다 낮은 class-specific score를 제거한다.
5. class별 NMS로 중복 box를 제거한다.

### Non-Maximum Suppression

가장 높은 score box를 선택한 뒤 IoU가 threshold보다 큰 같은 class box를 제거한다. 논문은 YOLO v1에서 NMS가 mAP를 2-3% 높였다고 보고한다.

NMS는 network 밖의 algorithm이므로 다음이 release contract에 포함되어야 한다.

- score threshold
- IoU threshold
- class-aware 또는 class-agnostic 여부
- 최대 detection 수
- tie-breaking 규칙
- box coordinate clipping

## 결과를 읽는 법

### PASCAL VOC 2007 속도·정확도

| model | mAP | FPS |
|---|---:|---:|
| Fast YOLO | 52.7 | 155 |
| YOLO | 63.4 | 45 |
| YOLO VGG-16 | 66.4 | 21 |
| Fast R-CNN | 70.0 | 0.5 |
| Faster R-CNN VGG-16 | 73.2 | 7 |

이 표는 당시 detector 간 trade-off를 보여준다. model input, hardware, preprocessing과 measurement가 오늘날 benchmark와 다르므로 현재 순위로 해석하지 않는다.

### Error profile

| detector | correct | localization | background |
|---|---:|---:|---:|
| Fast R-CNN | 71.6% | 8.6% | 13.6% |
| YOLO | 65.5% | 19.0% | 4.75% |

YOLO는 background false positive가 적지만 localization error가 많았다. Fast R-CNN과 YOLO의 error가 상보적이어서 결합 시 Fast R-CNN 71.8 mAP가 75.0으로 3.2 point 증가했다고 보고한다.

### VOC 2012와 artwork

- YOLO 단독 VOC 2012 test mAP: 57.9%
- small object category에서 상대적으로 약함
- Picasso와 People-Art에서 natural image로 학습한 representation의 domain generalization을 평가
- artwork에서는 R-CNN보다 성능 저하가 작았다고 보고

generalization 실험은 흥미롭지만 사람 class 중심의 두 artwork dataset 결과만으로 모든 domain shift에 robust하다고 일반화하면 안 된다.

## 논문의 강점

- detection pipeline을 하나의 regression network로 단순화
- full image context를 joint optimization에 포함
- speed뿐 아니라 mAP와 error category를 함께 분석
- localization과 background error의 trade-off를 정직하게 제시
- 실패가 다른 detector와 상보적일 수 있음을 조합 실험으로 확인
- small object, unusual aspect ratio, coarse feature, loss mismatch 한계를 명시

## 한계

- cell 하나가 class probability set 하나만 가져 crowded scene 표현력이 제한된다.
- 같은 cell에 중심이 들어간 여러 object를 충분히 표현하기 어렵다.
- multiple downsampling으로 small object localization이 어렵다.
- unusual aspect ratio·configuration으로 일반화가 약할 수 있다.
- squared-error loss가 IoU와 average precision을 직접 최적화하지 않는다.
- `7×7` coarse grid와 fully connected detection head가 spatial flexibility를 제한한다.
- main error source가 incorrect localization이라고 논문이 분석한다.

## 로보틱스·임베디드 적용 체크리스트

YOLO v1의 “real-time” 주장만 보고 actuator 경로에 바로 연결하면 안 된다.

- camera timestamp와 inference 결과 timestamp를 보존한다.
- resize가 aspect ratio를 바꾸면 box를 원 image 좌표로 되돌리는 contract를 검증한다.
- small·far object recall을 별도 challenge set으로 측정한다.
- preprocessing, copy, network, decode, NMS를 포함한 p95·p99 latency를 잰다.
- thermal throttling과 장시간 FPS 저하를 측정한다.
- class별 threshold와 cost-sensitive metric을 사용한다.
- stale frame, NaN, invalid box, empty detection의 safe behavior를 정의한다.
- NMS 전후 detection 수와 suppression 이유를 trace 가능하게 기록한다.
- closed-course와 shadow mode에서 false negative의 downstream 영향을 검증한다.

## Fine-tuning 실무 절차

1. target class와 operational design domain을 정의한다.
2. annotation을 `(class, x_min, y_min, x_max, y_max)` canonical format으로 검증한다.
3. image·label pair, class map, split 기준과 checksum을 versioning한다.
4. random image split 대신 sequence·location·device 단위 group split을 사용한다.
5. pretrained backbone과 detection head의 input normalization을 확인한다.
6. target class 수에 맞게 output channel과 class map을 변경한다.
7. grid assignment를 offline script로 시각화해 boundary object를 점검한다.
8. backbone freeze warm-up 뒤 전체 network를 작은 learning rate로 fine-tuning한다.
9. IoU distribution, responsible predictor 비율, object/no-object loss를 따로 logging한다.
10. mAP뿐 아니라 class별 AP, small-object recall, localization error를 평가한다.
11. export 뒤 Python과 target runtime의 decoded box·score를 golden vector로 비교한다.
12. 실제 장치에서 latency·memory·power·temperature와 NMS를 포함해 승인한다.

## 실습 실행 환경

세 notebook은 GPU 없이 NumPy로 실행된다.

```bash
cd you-only-look-once-v1
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install "numpy>=1.26" "jupyterlab>=4"
jupyter lab
```

Windows PowerShell에서는 다음 activate 명령을 사용한다.

```powershell
.\.venv\Scripts\Activate.ps1
```

## 실습 학습 가이드

1. [01_foundations.ipynb](01_foundations.ipynb)
   - box format 변환
   - area·intersection·union·IoU
   - confidence와 class-specific score
2. [02_practice.ipynb](02_practice.ipynb)
   - object center 기반 grid assignment
   - `7×7×30` tensor decoding
   - class-aware NMS
3. [03_advanced.ipynb](03_advanced.ipynb)
   - responsible predictor 선택
   - YOLO v1 multipart loss
   - precision-recall과 11-point AP
   - release gate

toy input으로 수학과 data contract를 재현하며 PASCAL VOC 결과를 재현한다고 주장하지 않는다.

## 권장 학습 순서

1. [문장 대조 번역·한국어 해설](You%20Only%20Look%20Once%20-%20Unified,%20Real-Time%20Object%20Detection.번역.md)
2. 이 README의 `7×7×30` channel layout을 종이에 직접 쓴다.
3. 세 notebook을 순서대로 실행한다.
4. grid boundary에 object center가 있는 test를 추가한다.
5. invalid box와 fully overlapping box를 NMS에 넣어본다.
6. target runtime과 Python의 decode 결과를 같은 tolerance로 비교한다.

## 다음 학습 경로

- IoU-family regression loss: GIoU, DIoU, CIoU
- anchor-based와 anchor-free assignment
- feature pyramid와 multi-scale detection
- focal loss와 class imbalance
- soft-NMS와 weighted box fusion
- COCO mAP의 여러 IoU threshold
- quantization 이후 box·score drift
- tracking-by-detection에서 timestamp와 association
