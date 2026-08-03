# V-JEPA 논문 분석과 비디오 표현 학습 실습

작성일: 2026-08-03

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [핵심 요약](#핵심-요약)
- [상세 정리](#상세-정리)
- [실험 결과](#실험-결과)
- [한계와 재현 주의점](#한계와-재현-주의점)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 논문: [Revisiting Feature Prediction for Learning Visual Representations from Video](https://arxiv.org/abs/2404.08471v1)
- 저자: Adrien Bardes, Quentin Garrido, Jean Ponce, Xinlei Chen, Michael Rabbat,
  Yann LeCun, Mahmoud Assran, Nicolas Ballas
- 출판 정보: arXiv preprint, 2024
- 식별자: arXiv:2404.08471, DOI: 10.48550/arXiv.2404.08471
- 사용 버전: arXiv v1, 2024-02-15 제출본(PDF 표기일 2024-04-15), 23쪽
- 원문 언어: 영어
- 접근일: 2026-08-03
- 라이선스: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

PDF 23쪽의 본문·표·그림·부록을 확인했습니다.
[`Revisiting Feature Prediction for Learning Visual Representations from Video.번역.md`](Revisiting%20Feature%20Prediction%20for%20Learning%20Visual%20Representations%20from%20Video.번역.md)는
원 저자와 CC BY 4.0을 표시한 한국어 번역·해설입니다. 원문 직접 재현은 짧은
핵심 문장으로 제한하고 나머지는 section별 상세 해설로 제공합니다.

## 한눈에 보기

V-JEPA는 text, pretrained image encoder, negative sample, pixel reconstruction과
사람 label 없이 **가려진 비디오 영역의 feature**를 예측해 visual representation을
학습합니다.

```text
video clip → 3D tokens
  ├─ visible x → x-encoder Eθ → predictor Pφ(+ 위치 mask token) → 예측 ŝM
  └─ 전체 clip → y-encoder Eθ̄ → target 위치 선택 → 목표 sM

L = masked token의 평균 L1(ŝM, stop-gradient(sM))
θ, φ: gradient descent / θ̄: θ의 EMA
```

MC-JEPA가 optical flow와 content objective를 결합한 multi-task 모델이라면,
V-JEPA는 feature prediction 하나만으로 appearance와 motion task에 모두 쓸 수
있는 frozen representation을 학습하는 데 초점을 둡니다.

## 기초 개념

### 시공간 token

16-frame clip을 공간 `16×16` pixel, 시간 2 frame 단위의 3D patch로 나눕니다.
224 해상도에서는 `8×14×14=1,568` token입니다. 3D sinusoidal positional
embedding으로 시간과 공간 위치를 표시합니다.

### Frozen evaluation

사전학습 encoder weight를 고정하고 작은 task head만 학습합니다. full
fine-tuning보다 representation 자체의 재사용성을 더 직접적으로 측정하지만,
head의 구조와 pooling 방식에도 영향을 받습니다.

### Feature prediction과 pixel reconstruction

pixel reconstruction은 색·질감 같은 모든 세부를 복원해야 합니다. feature
prediction은 target encoder가 보존한 예측 가능한 추상 정보를 맞추므로 의미와
motion에 집중할 가능성이 있습니다. 다만 target 표현이 나쁘거나 collapse하면
학습 목표도 쓸모없어집니다.

## 핵심 요약

1. **stand-alone objective:** feature prediction 외의 supervision을 사용하지
   않습니다.
2. **3D multi-block mask:** short-range 8개와 long-range 2개 block mask를
   각각 구성해 한 clip당 두 예측 문제를 만듭니다.
3. **높은 mask ratio:** block을 시간 전체에 반복하고 합집합을 취해 평균 약
   90%를 가려 정보 누설을 줄입니다.
4. **EMA target:** 전체 clip을 보는 y-encoder의 출력에서 target을 선택하고,
   x-encoder는 visible token만 봅니다.
5. **attentive probe:** frozen feature의 단순 평균 대신 학습 가능한 cross-attention
   pooling을 사용해 task 관련 token을 모읍니다.
6. **sample efficiency:** 90K iteration, 약 270M clip 처리로 기존 pixel prediction
   방법보다 훨씬 적은 sample을 보고 경쟁력 있는 결과를 보고합니다.

## 상세 정리

### 1. Training objective

naive regression은 encoder가 모든 입력에 상수 표현을 내는 trivial solution을
허용합니다. V-JEPA는 target branch stop-gradient, x-encoder의 EMA인 y-encoder,
별도 predictor를 결합합니다.

```text
min_(θ,φ) ||Pφ(Eθ(x), Δy) - sg(Eθ̄(y))||₁
```

L1 predictor의 최적점은 조건부 median입니다. 논문은 predictor가 target보다
빠르게 적응해 근사 최적 상태를 유지하면 encoder가 조건부 median absolute
deviation을 줄이기 위해 video 정보를 보존하도록 압력을 받는다는 직관을
제시합니다. 이는 특정 가정 아래의 동기이며 collapse 불가능성을 보편적으로
증명한 것은 아닙니다.

### 2. 3D multi-block masking

두 mask는 독립적인 예측 문제입니다.

- short-range: frame 면적 15% block 8개
- long-range: frame 면적 70% block 2개
- aspect ratio: 0.75~1.5
- 각 공간 block을 clip의 전체 시간축에 반복
- 겹칠 수 있는 block의 합집합이 평균 약 90% mask ratio를 형성
- `x`: mask complement, `y`: masked target region

낮은 시공간 coverage는 복사가 가능한 쉬운 문제가 되어 downstream 성능을
떨어뜨렸습니다. 같은 90% ratio에서도 하나의 큰 block보다 여러 block을 합치는
편이 좋았고, short/long mask 두 개가 하나보다 좋았습니다.

### 3. Network parameterization

- x/y encoder: ViT-L/16 또는 ViT-H/16
- tokenization: kernel `2×16×16`, temporal stride 2, spatial stride 16의 3D conv
- predictor: 12 transformer blocks, embedding dimension 384
- mask token: 공유 학습 vector + absolute 3D sin-cos position embedding
- x-encoder input에서 masked token 제거
- y-encoder는 전체 clip 처리 후 출력에서 unmasked token 제거
- loss: target token별 평균 L1

### 4. Pretraining

VideoMix2M은 HowTo100M, Kinetics-400/600/700, Something-Something-v2를 합치고
평가 validation overlap을 제거한 약 2M video 모음입니다.

- 16 frames, frame stride 4, 평균 약 3초
- 224 또는 384 spatial resolution
- 90,000 iterations
- batch 3,072(ViT-L/H 224) 또는 2,400(ViT-H 384)
- A100 80GB, bfloat16
- y-encoder EMA momentum 0.998→1.0
- learning-rate·weight-decay·EMA schedule을 112,500 iteration 기준으로 만든 뒤
  90,000에서 잘라 마지막 25%의 급격한 변화를 피함

### 5. Attentive probing

unnormalized prediction objective가 linearly separable subspace를 보장하지 않으므로,
학습 가능한 query가 frozen token을 cross-attention으로 pooling합니다. 논문의
probe는 12 heads×12 dimensions이며 그 뒤 LayerNorm과 linear classifier를 둡니다.
average pooling보다 K400 +17.0, SSv2 +16.1 points를 보고했으므로 baseline 비교에도
같은 probe를 적용해야 합니다.

## 실험 결과

### Feature target vs pixel target

ViT-L/16, VideoMix2M, 90K iterations, batch 3,072의 통제 비교입니다.

| target | K400 frozen | SSv2 frozen | IN1K frozen | K400 fine-tune |
|---|---:|---:|---:|---:|
| pixels | 68.6 | 66.0 | 73.3 | 85.4 |
| features | 73.7 | 66.2 | 74.8 | 85.6 |

frozen K400과 IN1K에서는 feature target 이득이 뚜렷하지만 SSv2와 full fine-tuning
차이는 작습니다. “항상 크게 우월하다”보다 protocol별 효과가 다르다고 읽어야
합니다.

### Masking ablation

| mask | K400 | SSv2 | IN1K |
|---|---:|---:|---:|
| random tube 90% | 51.5 | 46.4 | 55.6 |
| causal multi-block, 첫 6 frames | 61.3 | 49.8 | 66.9 |
| causal multi-block, 첫 12 frames | 71.9 | 63.6 | 72.2 |
| 전체 clip multi-block | 72.9 | 67.4 | 72.8 |

전체 clip의 시공간 context를 쓰는 multi-block이 가장 좋았습니다. 따라서 이
연구의 V-JEPA는 엄격한 future prediction 모델이 아니라 masked representation
prediction 모델입니다.

### Large models

- ViT-H/16 224: K400 82.0, SSv2 71.4, AVA 25.8, IN1K 75.9
- ViT-H/16 384: K400 81.9, SSv2 72.2, AVA 25.0, IN1K 77.4
- 논문 초록의 IN1K 77.9는 더 깊은 two-layer attentive probe 결과로, Table 6의
  one-layer protocol 77.4와 구분해야 합니다.

V-JEPA는 motion 의존도가 높은 SSv2에서 image-pretrained model보다 강했지만,
appearance 중심 K400·IN1K에서는 DINOv2 같은 대규모 image model이 더 높았습니다.

### Label efficiency와 temporal coverage

label 5%의 V-JEPA-H/16 결과는 K400 68.2, SSv2 54.0입니다. label 감소 시
pixel reconstruction baseline보다 성능 저하가 작았습니다. K400에서 1 clip
73.7에서 8 clips 80.9로 오르므로 pretraining뿐 아니라 evaluation temporal
coverage도 중요한 변수입니다.

## 한계와 재현 주의점

논문에는 별도의 limitations 절이 없습니다. 다음은 결과와 설정에서 도출한
**분석상 한계**입니다.

- VideoMix2M은 공개 dataset 결합이지만 web-scale image dataset보다 시각 다양성이
  제한적이라고 저자도 논의합니다.
- 16-frame short clip 학습은 장기 인과·계획·상호작용을 직접 모델링하지 않습니다.
- 전체 시간축을 활용하는 기본 mask는 online future-only prediction을 검증하지
  않습니다.
- attentive probe가 큰 성능 향상을 만들므로 “frozen encoder” 결과도 완전히
  선형인 평가는 아닙니다.
- 2M video와 매우 큰 global batch는 재현 비용이 높습니다.
- 여러 public dataset을 결합할 때 중복 제거, 이용 조건, 인물 privacy와 편향을
  별도로 관리해야 합니다.
- feature visualization의 diffusion decoder는 사후 해석 도구이며 V-JEPA 자체가
  pixel 생성 모델이라는 뜻이 아닙니다.

재현 시 clip sampling FPS, frame stride, spatial crop, mask seed, token count,
effective batch, sample seen, EMA와 잘린 schedule, probe architecture와 multi-view
inference를 함께 기록하세요.

## 용어 정리

| 용어 | 의미 |
|---|---|
| V-JEPA | video feature prediction만으로 학습하는 JEPA 모델군 |
| x-encoder | visible token을 처리하며 gradient로 갱신되는 encoder |
| y-encoder | 전체 clip을 처리하고 x-encoder EMA로 갱신되는 target encoder |
| multi-block mask | 여러 연속 공간 block의 합집합을 시간축 전체에 적용한 mask |
| tube masking | 같은 공간 patch mask를 모든 frame에 반복하는 방식 |
| attentive probe | 학습 가능한 query의 cross-attention으로 frozen token을 pooling하는 평가 head |
| K400 | Kinetics-400 action recognition benchmark |
| SSv2 | motion·시간 순서 이해가 중요한 Something-Something-v2 benchmark |
| AVA | spatio-temporal action localization benchmark |
| sample seen | 여러 epoch와 반복을 포함해 학습 중 처리한 sample 총수 |

## 실습 학습 가이드

- [`01_foundations.ipynb`](01_foundations.ipynb): short/long-range 3D multi-block
  mask와 실제 masking ratio를 구현합니다.
- [`02_practice.ipynb`](02_practice.ipynb): L1 predictor의 median 성질과 EMA target
  update를 실험합니다.
- [`03_advanced.ipynb`](03_advanced.ipynb): attentive pooling, masking ablation,
  label·temporal coverage를 분석합니다.

모두 외부 package 없이 실행하는 toy reproduction이며 논문 결과 재현이 아닙니다.

## 다음 학습 경로

1. [논문 번역·해설](Revisiting%20Feature%20Prediction%20for%20Learning%20Visual%20Representations%20from%20Video.번역.md)을 읽습니다.
2. 세 notebook에서 mask block 수·크기, EMA momentum과 query를 바꿉니다.
3. I-JEPA, MC-JEPA, V-JEPA를 target과 objective 기준으로 비교합니다.
4. 작은 video dataset에서 pixel reconstruction과 feature prediction을 같은
   architecture·sample budget으로 비교합니다.
5. average pooling, linear probe, attentive probe와 full fine-tuning을 분리해
   보고합니다.
