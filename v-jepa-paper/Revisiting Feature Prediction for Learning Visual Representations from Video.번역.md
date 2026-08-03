# Revisiting Feature Prediction for Learning Visual Representations from Video - 번역·해설

## 논문 metadata

| 항목 | 내용 |
|---|---|
| 원문 제목 | Revisiting Feature Prediction for Learning Visual Representations from Video |
| 저자 | Adrien Bardes, Quentin Garrido, Jean Ponce, Xinlei Chen, Michael Rabbat, Yann LeCun, Mahmoud Assran, Nicolas Ballas |
| 출판 정보 | arXiv preprint, 2024 |
| 식별자 | arXiv:2404.08471, DOI: 10.48550/arXiv.2404.08471 |
| 원문 | [arXiv v1](https://arxiv.org/abs/2404.08471v1) |
| 사용 버전 | v1, 23쪽 |
| 원문 언어 | 영어 |
| 접근일 | 2026-08-03 |
| 라이선스 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

## 저작자 표시와 변경 사항

이 문서는 위 저자들의 원 논문을 한국어 학습용으로 번역·요약·재구성한 2차
자료입니다. 원문을 그대로 복제하지 않고 짧은 대조 문장과 상세 해설을 제공하며,
번역 선택·용어 설명·구조화 표·실습 연결은 이 자료에서 추가했습니다. 원 저자와
Meta가 이 번역을 보증한다는 의미는 아닙니다.

## 번역 범위

| 원문 범위 | 상태 | 이 파일의 처리 |
|---|---|---|
| 제목·Abstract | 부분 번역 | 핵심 문장 대조와 전체 요약 |
| 1. Introduction | 완료 | 주장·기여 해설 |
| 2. Related Works | 완료 | 연구군별 요약 |
| 3. Methodology | 완료 | 수식·mask·network 해설 |
| 4. Design Ablations | 완료 | 표 수치와 protocol 해설 |
| 5. Prior Work Comparison | 완료 | frozen/fine-tuning 비교 |
| 6. Predictor Evaluation | 완료 | 시각화 방법과 경계 |
| 7. Conclusion | 완료 | 주장 범위 요약 |
| Appendix A~E | 완료 | 구현·평가·추가 ablation 해설 |
| References | 해당 없음 | 서지는 원문 참조 |

## 읽기 전 핵심 배경

- **predictive feature principle:** 시간적으로 인접한 감각 표현이 서로 예측
  가능해야 한다는 관점
- **JEPA:** 입력 공간이 아니라 embedding 공간에서 관련 신호를 예측
- **masked video modeling:** video token 일부를 숨겨 self-supervised target 생성
- **EMA teacher:** online encoder를 천천히 추적하는 target encoder
- **frozen evaluation:** backbone을 고정하고 task head만 학습하는 평가

## 제목 번역

비디오 시각 표현 학습을 위한 특징 예측의 재검토

## Abstract

**S001 — Original**

The models are trained on 2 million videos collected from public datasets and are evaluated on downstream image and video tasks.

**S001 — 한국어**

(모델들은 공개 dataset에서 수집한 200만 개 video로 학습되며 downstream image와
video task에서 평가된다.)

- **용어·약어 해설**
  - **downstream task(다운스트림 작업):** 사전학습 표현이 실제 분류·탐지 등에서
    얼마나 유용한지 평가하는 후속 문제입니다.
  - **VideoMix2M:** 여러 공개 video dataset을 결합하고 평가 validation 중복을
    제거한 저자들의 사전학습 모음입니다.

### 초록 전체 해설

논문은 feature prediction 하나만으로 video representation을 학습하는 V-JEPA
모델군을 제시합니다. pretrained image encoder, text, negative example, pixel
reconstruction이나 다른 supervision을 쓰지 않습니다. frozen backbone 평가에서
motion과 appearance task 모두에 유용한 표현을 얻었으며, 가장 큰 ViT-H/16은
K400 81.9%, SSv2 72.2%, IN1K 77.9%를 보고합니다. 마지막 IN1K 값은 본문의
two-layer attentive probe 조건임을 표 비교에서 구분해야 합니다.

## 1. Introduction 해설

연구 질문은 현대적인 Transformer, masked modeling, JEPA, query pooling과 대형
dataset을 결합했을 때 **feature prediction만으로** video의 motion과 appearance를
학습할 수 있는가입니다. 저자들은 다음을 주장합니다.

1. frozen backbone으로 image·video task 전반에 쓸 수 있는 표현을 학습합니다.
2. 비슷한 architecture의 pixel prediction보다 frozen evaluation이 좋고 더 짧은
   training schedule을 사용합니다.
3. label이 적어질수록 pixel reconstruction baseline과의 격차가 커집니다.

SSv2처럼 세밀한 temporal understanding이 필요한 task에서 image-only model보다
강한 반면, appearance로 풀기 쉬운 K400에서는 DINOv2 같은 image model도
강하다는 구분이 중요합니다.

## 2. Related Works 해설

- **Slow features:** 인접 frame 표현이 천천히 변하도록 해 temporal predictability를
  유도합니다.
- **Video representation learning:** contrastive, clustering, multimodal text/audio,
  masked prediction 등 다양한 supervision을 사용해 왔습니다.
- **Pixel prediction:** video MAE 계열은 spatio-temporal mask의 raw pixel을
  복원합니다.
- **Feature prediction:** BYOL·data2vec·I-JEPA 계열의 EMA target과 predictor를
  video modality로 확장합니다.

V-JEPA의 차이는 여러 objective를 섞지 않고 feature prediction 단독 목적을
대규모 video에서 검증한 데 있습니다.

## 3. Methodology: Video-JEPA 해설

### 3.1 Training Objective

video의 visible 영역 `x`에서 masked 영역 `y`의 표현을 예측합니다. predictor는
`y`의 spatio-temporal 위치 `Δy`도 받습니다.

```text
min_(θ,φ) ||Pφ(Eθ(x), Δy) - sg(Eθ̄(y))||₁
```

- `Eθ`: gradient로 학습하는 x-encoder
- `Pφ`: visible representation과 target 위치로 target embedding 예측
- `Eθ̄`: `Eθ`의 EMA인 y-encoder
- `sg`: target branch stop-gradient
- L1: masked target token의 절대 오차 평균

naive shared encoder regression은 상수 표현 collapse를 허용합니다. 논문은
EMA teacher, stop-gradient와 predictor 비대칭으로 이를 막습니다. L1 최적
predictor가 조건부 median이라는 점에서, predictor가 충분히 빠르게 적응하면
encoder가 target의 조건부 median absolute deviation을 줄이기 위해 정보를
보존한다는 이론적 직관을 제시합니다.

### 3.2 Prediction Task

공간적으로 연속된 block을 clip의 모든 frame에 반복해 시간·공간 중복으로 인한
정보 누설을 줄입니다. short mask는 15% block 8개, long mask는 70% block 2개의
합집합이며 둘 다 aspect ratio 0.75~1.5입니다. 겹침 때문에 단순 합보다 작지만
결과 mask ratio는 평균 약 90%입니다.

### 3.3 Network Parameterization

16 frame clip을 시간 2 frame×공간 16×16 pixel의 token으로 만듭니다. x-encoder는
masked token을 제거한 입력만 처리합니다. y-encoder는 전체 clip을 처리하고
출력에서 target token만 고르므로 contextualized target을 제공합니다. predictor는
dimension 384의 12-block narrow Transformer이며, 공유 mask vector에 absolute
3D sin-cos positional embedding을 더합니다.

### 3.4 Data와 Evaluation

VideoMix2M은 HowTo100M, Kinetics 계열과 SSv2를 결합하고 validation overlap을
제거합니다. K400은 action recognition, SSv2는 fine-grained motion, AVA는 action
localization, IN1K·Places205·iNat21은 image appearance transfer를 평가합니다.

## 4. What Matters for Learning Representations from Video?

### 4.1 Features vs Pixels

통제된 ViT-L/16 비교에서 feature target은 pixel target보다 K400 frozen
73.7 대 68.6, IN1K 74.8 대 73.3으로 높았습니다. SSv2 66.2 대 66.0과 K400
fine-tuning 85.6 대 85.4의 차이는 작았습니다. feature prediction의 장점이 특히
frozen transfer에서 나타난다고 해석할 수 있습니다.

### 4.2 Data Distribution

dataset 크기만 아니라 task 관련 diversity가 중요합니다. ViT-L은 VideoMix2M이
평균 성능에서 좋았고, ViT-H에서는 K710+SSv2와 VideoMix2M의 task별 우위가
달랐습니다. 하나의 평균값만으로 data mixture를 결정하기보다 target task별
성능을 봐야 합니다.

### 4.3 Attentive Probing

learnable query의 cross-attention pooling은 average pooling보다 K400 17.0,
SSv2 16.1 points 높았습니다. 이는 backbone 비교에 probe protocol을 통일해야
한다는 뜻이며, attentive probe는 순수 linear probe보다 표현력이 큽니다.

### 4.4 Masking

전체 clip multi-block은 K400/SSv2/IN1K에서 72.9/67.4/72.8로 random tube와
causal mask보다 좋았습니다. 기본 목표는 미래 frame만 보는 causal prediction이
아니며, clip 전체의 visible token에서 masked tube 표현을 복원합니다.

## 5. Comparison with Prior Work 해설

### Pixel Prediction

비슷한 ViT-L/Hiera-L architecture의 VideoMAE, OmniMAE, Hiera와 비교합니다.
V-JEPA는 frozen task 대부분에서 앞섰고 ImageNet에서는 ImageNet으로 직접 학습한
OmniMAE보다 0.3 point 낮았습니다. full fine-tuning은 큰 차이가 아니었지만 훨씬
적은 sample을 처리했습니다.

### State of the Art

V-JEPA-H/16 384는 K400 81.9, SSv2 72.2, IN1K 77.4를 보고합니다. DINOv2는
K400·IN1K에서 더 높지만 SSv2 50.6으로 motion task 격차가 큽니다. 이는 video
pretraining의 장점이 모든 visual task가 아니라 motion-sensitive task에서 특히
크다는 근거입니다.

### Label Efficiency

K400 label 5%에서 V-JEPA-H/16은 68.2, SSv2 label 5%에서는 54.0입니다. label을
줄일 때 VideoMAE·VideoMAEv2·MVD보다 상대 감소가 작았습니다. 각 setting은
3개 random split을 사용했으므로 평균과 표준편차를 함께 읽어야 합니다.

## 6. Evaluating the Predictor 해설

frozen encoder와 predictor의 target 예측을 conditional diffusion decoder로 pixel에
매핑합니다. decoder는 masked 영역의 예측 representation만 받고 visible context는
직접 보지 않습니다. 여러 sample에서 공통인 객체·pose·motion은 representation에
담긴 정보로, 달라지는 세부는 불확실성으로 해석합니다. 이 실험은 사후
visualization이며 V-JEPA를 생성 모델로 바꾸지 않습니다.

## 7. Conclusion 해설

저자들은 feature prediction 단독 목적이 frozen action recognition, temporal action
detection과 image classification에서 강한 범용 표현을 만들었다고 결론짓습니다.
특히 fine-grained motion task와 label이 적은 설정에서 효과가 컸습니다. 이 결론은
VideoMix2M, ViT와 attentive-probe protocol의 실험 범위 안에서 읽어야 합니다.

## Appendix 해설

### A. Extended Related Works

CLIP 계열 weak supervision, DINOv2·I-JEPA 같은 image self-supervision,
VideoMAE·multimodal video 모델의 확장 관계를 정리합니다.

### B. Extended Description

224 해상도 16-frame clip이 3D convolution을 거쳐 `8×14×14=1,568` token이 되는
shape와 `x`/`y` token indexing, predictor·target L1 계산을 명시합니다.

### C. Pretraining Details

90K iteration, 12K warmup, learning rate `6.25e-4`, weight decay `0.04→0.4`,
bfloat16, A100 80GB 조건과 multi-mask 계산 재사용을 설명합니다. y-encoder target은
한 번만 계산하고 x-encoder와 predictor만 mask별로 실행해 비용을 줄입니다.

### D. Evaluation Details

attentive probe, multi-clip temporal coverage, detection와 fine-tuning의 task별
hyperparameter를 제공합니다. K400에서 1 clip보다 8 clips가 V-JEPA 73.7→80.9로
높아 evaluation coverage가 큰 변수임을 보여 줍니다.

### E. Additional Ablations

baseline에도 attentive probe를 적용하고, pretraining data, mask 개수·block
크기·시공간 coverage를 추가 분석합니다. 두 mask, 여러 block, 높은 spatial·
temporal ratio가 기본 설정을 지지합니다.

## 수식·그림·표 읽기 가이드

- **Figure 2:** JEPA의 x/y representation prediction과 위치 조건 `z`를 봅니다.
- **Figure 3:** x input masking과 y output masking의 비대칭을 따라갑니다.
- **Table 1:** feature-vs-pixel 효과가 frozen과 fine-tuning에서 다른 점을 봅니다.
- **Table 4:** causal mask가 아니라 전체 clip multi-block이 기본임을 확인합니다.
- **Table 6:** video model의 motion task와 image model의 appearance task 강점을
  분리합니다.
- **Figure 6:** decoder가 context를 직접 보지 않는 조건을 확인해야 합니다.
- **Figure 8:** mask ratio가 같아도 block 수와 mask 수가 성능을 바꾸는 점을 봅니다.

## 약어 및 기술 용어 사전

| 원어·약어 | 한국어 | 논문에서의 역할 | 최초 등장 |
|---|---|---|---|
| V-JEPA | 비디오 JEPA | feature prediction 단독 사전학습 모델 | 초록 해설 |
| VideoMix2M | 비디오 혼합 200만 | 공개 dataset 기반 사전학습 data | S001 |
| EMA | 지수이동평균 | y-encoder 갱신 | 3절 해설 |
| L1 loss | 절대 오차 손실 | masked feature prediction 목적 | 3절 해설 |
| 3D multi-block | 3차원 다중 블록 mask | 어려운 시공간 예측 문제 구성 | 3절 해설 |
| attentive probe | 주의집중 탐침 | frozen token의 task-adaptive pooling | 4절 해설 |
| K400 | Kinetics-400 | appearance 영향도 있는 action 분류 | 3절 해설 |
| SSv2 | Something-Something-v2 | temporal motion 이해 평가 | 3절 해설 |
| AVA | Atomic Visual Actions | 시공간 action localization | 3절 해설 |

## 번역 검수 기록

- v1 PDF 23쪽의 본문·부록 section 순서를 확인했습니다.
- methodology, feature/pixel 표, prior-work 비교, label efficiency, tokenization과
  mask ablation page를 렌더링해 추출 text와 대조했습니다.
- abstract와 Table 6의 IN1K 수치 차이를 probe protocol로 구분했습니다.
- 원 저자·라이선스·변경 사실을 표시했습니다.
- 저자 주장과 분석상 한계를 분리했습니다.

## 함께 보기

- [논문 분석 README](README.md)
- [I-JEPA 논문 분석](../i-jepa-paper/README.md)
- [MC-JEPA 논문 분석](../mc-jepa-paper/README.md)
- [원문 PDF](https://arxiv.org/pdf/2404.08471v1)
