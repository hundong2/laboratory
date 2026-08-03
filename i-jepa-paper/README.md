# I-JEPA 논문 분석과 재현 실습

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

- 논문: [Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture](https://arxiv.org/abs/2301.08243v3)
- 저자: Mahmoud Assran, Quentin Duval, Ishan Misra, Piotr Bojanowski,
  Pascal Vincent, Michael Rabbat, Yann LeCun, Nicolas Ballas
- 학회: 2023 IEEE/CVF Conference on Computer Vision and Pattern
  Recognition(CVPR 2023)
- 식별자: arXiv:2301.08243, DOI: 10.48550/arXiv.2301.08243
- 사용 버전: arXiv v3, 2023-04-13 개정, 17쪽
- 원문 언어: 영어
- 접근일: 2026-08-03
- 라이선스: arXiv non-exclusive distribution license

PDF 전체 17쪽의 본문, 표, 그림, 부록을 확인했습니다. 라이선스가 전문의
재배포·번역을 허용하는 오픈 라이선스는 아니므로
[`Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture.번역.md`](Self-Supervised%20Learning%20from%20Images%20with%20a%20Joint-Embedding%20Predictive%20Architecture.번역.md)는
짧은 핵심 문장 하나만 대조 번역하고 나머지는 절별 한국어 해설로 제공합니다.

공식 코드의 한국어 자료는 별도 submodule인
[`ijepa/guide/README.md`](../ijepa/guide/README.md)에 있습니다.

## 한눈에 보기

I-JEPA는 레이블이나 사람이 설계한 여러 view augmentation 없이, 한 이미지의
넓은 context에서 여러 target 영역의 **latent representation**을 예측합니다.
가린 픽셀을 복원하지 않기 때문에 예측하기 어려운 저수준 세부 정보보다 객체와
장면의 의미를 담는 표현에 집중하도록 유도합니다.

```text
이미지 y
 ├─ context block x → context encoder fθ → predictor gφ → target 예측 ŝy
 └─ 전체 patch      → target encoder fθ̄ ───────────────→ target sy

손실: target patch의 평균 L2(ŝy, sy)
갱신: θ, φ는 gradient descent / θ̄는 θ의 EMA
```

## 기초 개념

### 자기지도학습

사람이 붙인 class label 대신 입력 자체에서 학습 문제를 만듭니다. I-JEPA에서는
보이는 patch가 입력이고 가린 영역의 target-encoder 표현이 정답 역할을 합니다.

### 생성적 복원과 joint embedding prediction

- MAE 계열은 가린 픽셀을 복원합니다.
- view-invariance 계열은 augmentation한 두 view의 표현을 맞춥니다.
- I-JEPA는 한 view 안에서 context와 target의 표현 관계를 예측합니다.

I-JEPA도 Transformer를 사용합니다. 따라서 “JEPA 대 Transformer”가 아니라
**어떤 학습 목적과 target을 쓰는가**가 구분의 핵심입니다.

### representation collapse

모든 입력이 비슷한 embedding으로 매핑되면 loss는 쉬워져도 정보가 사라집니다.
논문은 context encoder와 target encoder의 비대칭, stop-gradient 성격의 target
branch, EMA 갱신을 사용합니다. 다만 학습 안정성은 mask·optimizer·정규화 등
전체 설계에 의존합니다.

## 핵심 요약

1. **latent target:** target encoder 출력에서 target block을 선택합니다. 입력을
   먼저 가리는 것과 다르며 semantic target을 만드는 핵심입니다.
2. **multi-block mask:** 4개의 비교적 큰 target과 하나의 넓고 분산된 context를
   사용합니다.
3. **위치 조건 predictor:** 공유 mask token에 위치 embedding을 더해 어느 위치의
   target을 예측할지 지정합니다.
4. **EMA teacher:** target encoder는 gradient로 학습하지 않고 context encoder의
   지수이동평균으로 갱신합니다.
5. **효율:** 한 iteration은 MAE보다 약 7% 느리지만 약 5배 적은 iteration에
   수렴해 전체 계산량을 절약했다고 보고합니다.

## 상세 정리

### 1. 입력과 target 구성

이미지를 겹치지 않는 `N`개 patch로 바꾸고 전체 patch를 target encoder에
통과시켜 `s_y = {s_y1, ..., s_yN}`을 얻습니다. 기본 설정은 서로 겹칠 수 있는
target block 4개이며 각 block의 면적 비율은 `(0.15, 0.2)`, 종횡비는
`(0.75, 1.5)` 범위입니다.

중요한 구현 순서는 다음과 같습니다.

```text
전체 이미지 → target encoder → 모든 patch representation → target mask 적용
```

target encoder 입력을 먼저 가리면 target 자체가 충분한 문맥을 보지 못해 표현의
추상 수준이 낮아질 수 있습니다. 부록의 ablation도 출력 마스킹이 입력 마스킹보다
낫다고 보고합니다.

### 2. context 구성

context block은 면적 비율 `(0.85, 1.0)`, 종횡비 `1.0`인 하나의 큰 block으로
샘플링합니다. 독립적으로 뽑은 target과 겹치는 부분을 context에서 제거합니다.
그 결과 context는 정보가 풍부하면서도 target을 직접 노출하지 않습니다.

### 3. predictor와 위치 정보

context encoder 출력과 target 위치별 mask token을 좁은 ViT predictor에
전달합니다. mask token은 공유 학습 벡터에 위치 embedding을 더한 것입니다.
target block이 4개라면 predictor를 target별로 적용합니다.

### 4. 손실과 갱신

target block 집합을 `B_i`, 예측과 목표 patch 표현을 각각 `ŝ_yj`, `s_yj`라 하면
논문의 목적은 다음처럼 정리할 수 있습니다.

```text
L = (1/M) Σ_i Σ_(j∈B_i) ||ŝ_yj - s_yj||²₂
```

- `θ`(context encoder)와 `φ`(predictor): gradient-based optimization
- `θ̄`(target encoder): `θ̄ ← mθ̄ + (1-m)θ`
- target branch: gradient를 받지 않음

### 5. 구현 설정

- backbone과 target encoder: 표준 ViT
- predictor: embedding dimension 384인 좁은 ViT
- predictor depth: ViT-B는 6, ViT-L/H는 12, ViT-G는 16
- 사전학습 중 `[cls]` token을 사용하지 않음
- 평가 시 target encoder 출력을 average pooling해 global representation 생성
- 기본 ImageNet-1K 실험: 224×224, 논문 표에 모델별 300~600 epoch

## 실험 결과

수치는 논문의 해당 protocol 안에서만 비교해야 합니다. 모델 크기, 해상도,
epoch와 평가 방식이 다른 행을 같은 조건처럼 해석하면 안 됩니다.

### ImageNet-1K

| 설정 | protocol | Top-1 |
|---|---|---:|
| I-JEPA ViT-H/14, 300 epoch | linear evaluation | 79.3 |
| I-JEPA ViT-H/16, 448px, 300 epoch | linear evaluation | 81.1 |
| I-JEPA ViT-H/14, 300 epoch | ImageNet-1% | 73.3 |
| I-JEPA ViT-H/16, 448px, 300 epoch | ImageNet-1% | 77.3 |

### 전이와 local task

I-JEPA ViT-H/14의 linear probe 결과는 CIFAR100 87.5, Places205 58.4,
iNaturalist18 47.6입니다. CLEVR에서는 object counting 86.7, distance/depth
prediction 72.4를 보고합니다. 이 값은 task별 평가 설정을 보존해 읽어야 합니다.

### 핵심 ablation

| 비교 | 조건 | Top-1 |
|---|---|---:|
| multi-block mask | ViT-B/16, 300 epoch, ImageNet-1% | 54.2 |
| rasterized mask | 동일 | 15.5 |
| single block mask | 동일 | 20.2 |
| random mask | 동일 | 17.6 |
| target encoder representation | ViT-L/16, ImageNet-1% | 66.9 |
| pixel target | 비교 실험 | 40.7 |
| target output masking | ViT-H/16, 300 epoch | 67.3 |
| target input masking | 동일 | 56.1 |

위 표는 단일 요소의 보편적 우월성을 증명하기보다 해당 구현에서 mask와 latent
target 선택이 성능에 큰 영향을 준다는 근거입니다.

## 한계와 재현 주의점

논문에는 별도의 명시적 limitations 절이 없습니다. 다음은 방법과 실험 범위에서
도출한 **분석상 한계**입니다.

- 정적 이미지 중심 결과이므로 시간적 동역학이나 행동 계획을 직접 검증하지
  않습니다.
- 대표 실험은 ImageNet과 대형 ViT에 의존합니다. 작은 dataset·의료 영상·위성
  영상에서 같은 mask 비율이 최적이라는 보장은 없습니다.
- ViT-G/16 확대가 semantic task에는 도움을 줬지만 local task에는 일관된 향상을
  보이지 않았습니다. 더 큰 모델이 항상 좋은 것은 아닙니다.
- 16개 A100에서 72시간 미만이라는 결과는 hardware, software stack, global
  batch와 통신 환경에 민감합니다.
- predictor 시각화에는 별도의 생성 decoder가 사용됩니다. 시각화 품질을 I-JEPA
  자체의 픽셀 생성 능력으로 해석하면 안 됩니다.
- pretrained representation은 training data의 편향을 포함할 수 있습니다.

재현 시 commit SHA, dataset version, effective batch size, optimizer step 수,
mask seed, 해상도, mixed precision, 평가 protocol을 함께 기록하세요. 공식 설정은
대규모 학습용이므로 먼저 toy 또는 축소 dataset으로 tensor shape와 checkpoint
재시작을 검증해야 합니다.

## 용어 정리

| 용어 | 의미 |
|---|---|
| JEPA | 한 신호의 표현에서 관련 신호의 표현을 예측하는 아키텍처 계열 |
| context block | encoder가 실제로 관찰하는 patch 집합 |
| target block | predictor가 표현을 맞혀야 하는 patch 집합 |
| EMA | 최근 online encoder를 더 반영하되 target을 천천히 변화시키는 갱신 |
| positional mask token | target의 내용 대신 위치를 predictor에 알려 주는 token |
| linear probe | encoder를 고정하고 선형 classifier만 학습하는 표현 평가 |
| low-shot | 적은 label만 사용해 표현의 label 효율을 평가하는 설정 |
| ablation | 구성 요소를 바꿔 성능 변화로 역할을 분석하는 실험 |

## 실습 학습 가이드

- [`01_foundations.ipynb`](01_foundations.ipynb): patch grid에서 논문의
  multi-block context/target mask를 구현합니다.
- [`02_practice.ipynb`](02_practice.ipynb): 작은 latent predictor와 EMA target
  encoder를 표준 Python으로 학습합니다.
- [`03_advanced.ipynb`](03_advanced.ipynb): 논문 ablation 수치와 계산 효율을
  재분석하고 재현 checklist를 만듭니다.

외부 패키지 없이 실행할 수 있는 toy reproduction이며 논문 성능 재현이
아닙니다.

## 다음 학습 경로

1. [저작권 범위 내 논문 번역·해설](Self-Supervised%20Learning%20from%20Images%20with%20a%20Joint-Embedding%20Predictive%20Architecture.번역.md)을 읽습니다.
2. 세 notebook을 순서대로 실행하고 mask scale과 EMA momentum을 바꿉니다.
3. [공식 코드 한국어 가이드](../ijepa/guide/README.md)에서 실제 tensor 흐름을
   대조합니다.
4. 작은 dataset용 설정으로 한 batch smoke test를 수행합니다.
5. pretraining loss뿐 아니라 feature variance, linear probe와 전이 성능을 함께
   기록합니다.
