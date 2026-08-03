# Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture - 번역·해설

## 논문 metadata

| 항목 | 내용 |
|---|---|
| 원문 제목 | Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture |
| 저자 | Mahmoud Assran, Quentin Duval, Ishan Misra, Piotr Bojanowski, Pascal Vincent, Michael Rabbat, Yann LeCun, Nicolas Ballas |
| 학회 | CVPR 2023 |
| 식별자 | arXiv:2301.08243, DOI: 10.48550/arXiv.2301.08243 |
| 원문 | [arXiv v3](https://arxiv.org/abs/2301.08243v3) |
| 사용 버전 | v3, 2023-04-13, 17쪽 |
| 원문 언어 | 영어 |
| 접근일 | 2026-08-03 |
| 확인 라이선스 | [arXiv non-exclusive distribution license](https://arxiv.org/licenses/nonexclusive-distrib/1.0/) |

## 번역·접근 범위

PDF의 본문과 부록을 모두 확인했지만, 이 라이선스는 논문 전문의 재배포나 번역을
명시적으로 허용하는 오픈 라이선스가 아닙니다. 따라서 저작권 경계를 지키기 위해
짧은 핵심 문장 하나만 문장 대조 형식으로 제공하고 나머지는 절별 한국어
해설·요약으로 전환했습니다. 원문의 수식·표 수치는 필요한 범위에서 설명하며,
그림은 복제하지 않고 읽는 방법만 안내합니다.

| 원문 범위 | 상태 | 이 파일의 처리 |
|---|---|---|
| 제목·metadata | 완료 | 서지 정보 보존 |
| 초록 | 부분 번역 | 핵심 문장 1개 대조, 나머지 요약 |
| 1. Introduction | 완료 | 절별 해설 |
| 2. Background | 완료 | 개념 비교 요약 |
| 3. Method | 완료 | 알고리즘·수식 해설 |
| 4. Related Work | 완료 | 연구군 요약 |
| 5~7. Evaluation/Scalability | 완료 | protocol과 주요 수치 해설 |
| 8. Visualizations | 완료 | 그림 해석 방법 |
| 9. Ablations | 완료 | 주요 표 수치와 의미 |
| 10. Conclusion | 완료 | 주장 범위 요약 |
| Appendix A~E | 완료 | 구현·추가 ablation·시각화 요약 |
| References | 해당 없음 | 서지 목록은 원문 참조 |

## 읽기 전 핵심 배경

- **자기지도학습(self-supervised learning):** label 대신 입력의 일부를 학습
  목표로 사용합니다.
- **joint embedding:** context와 target을 비교 가능한 latent space에 놓습니다.
- **masked image modeling:** 입력 일부를 가리고 복원 또는 표현 예측 문제를
  만듭니다.
- **Vision Transformer(ViT):** 이미지를 patch token sequence로 처리합니다.
- **EMA target encoder:** online encoder를 천천히 추적해 안정적인 target을
  만듭니다.

## 제목

**한국어 제목**

결합 임베딩 예측 아키텍처를 활용한 이미지 자기지도학습

## Abstract

**S001 — Original**

The idea behind I-JEPA is simple: from a single context block, predict the representations of various target blocks in the same image.

**S001 — 한국어**

(I-JEPA의 발상은 단순하다. 하나의 context block에서 같은 이미지에 있는 여러
target block의 표현을 예측한다.)

- **용어·약어 해설**
  - **I-JEPA(Image-based Joint-Embedding Predictive Architecture, 이미지
    기반 결합 임베딩 예측 아키텍처):** 이미지 일부의 latent 표현으로 다른
    영역의 latent 표현을 예측하는 자기지도학습 방법입니다.
  - **context block(문맥 블록):** 모델이 관찰해 예측 근거로 사용하는 영역입니다.
  - **target block(목표 블록):** 내용은 가려져 있고 latent 표현을 맞혀야 하는
    영역입니다.

### 초록 해설

논문은 수작업 data augmentation 없이 의미론적 이미지 표현을 학습하는
비생성형 방법을 제안합니다. 핵심 설계는 충분히 큰 target block과 공간적으로
정보가 풍부한 context block입니다. 연구진은 ViT와 결합했을 때 모델·데이터
규모 확장이 가능하며, 16개 A100 GPU로 ViT-H/14를 72시간 이내 학습해 분류부터
객체 수 세기와 깊이 예측까지 여러 downstream task에서 강한 결과를 얻었다고
보고합니다.

## 1. Introduction 해설

연구의 출발점은 사람과 동물이 언어보다 시각을 통해 방대한 상식과 세계 지식을
학습한다는 관찰입니다. 기존 self-supervised vision 방법은 크게 두 계열입니다.

1. 여러 augmentation view의 표현을 같게 만드는 joint-embedding 방법
2. 손상되거나 가려진 입력을 복원하는 generative 방법

전자는 사람이 정의한 불변성에 의존하고, 후자는 의미 예측에 불필요한 픽셀
세부까지 복원해야 할 수 있습니다. I-JEPA는 latent space에서 예측해 두 한계를
완화하려고 합니다. 논문의 기여는 효율적인 non-generative architecture,
semantic target을 유도하는 multi-block masking, 대형 ViT·dataset에서의 scaling
검증으로 정리할 수 있습니다.

## 2. Background 해설

### Joint-Embedding Architecture

서로 호환되는 두 입력 `x`, `y`를 각각 encoder에 넣고 embedding 사이 거리를
줄입니다. collapse 방지를 위해 negative sample, redundancy reduction,
clustering, 비대칭 encoder 등의 설계가 사용됩니다.

### Generative Architecture

관측 `x`와 위치 등의 조건 `z`에서 원 신호 `y`를 재구성합니다. 이미지에서는
mask token으로 가린 patch 위치를 알려 주고 pixel 또는 token을 복원합니다.

### Joint-Embedding Predictive Architecture

형태는 조건부 생성과 비슷하지만 loss가 입력 공간이 아니라 embedding 공간에
적용됩니다. 예측할 수 없는 세부 정보를 target 표현이 버릴 수 있다는 점이
핵심입니다. I-JEPA는 context/target encoder 비대칭과 EMA를 사용합니다.

## 3. Method 해설

### Target 생성

이미지를 `N`개 patch로 나누고 전체 이미지를 target encoder `f_θ̄`에 넣어
patch-level 표현 `s_y`를 얻습니다. 그 출력에서 target mask `B_i`에 속한 표현을
선택합니다. 기본적으로 target 4개, 면적 비율 0.15~0.20, 종횡비 0.75~1.5를
사용합니다.

### Context 생성

면적 비율 0.85~1.0, 종횡비 1.0인 큰 block 하나를 뽑고 target과 겹치는 patch를
제거합니다. context encoder는 남은 visible patch만 처리하므로 계산을 줄이면서
target의 직접 노출을 막습니다.

### Prediction

좁은 ViT predictor `g_φ`는 context 표현과 target 위치의 mask token을 받습니다.
mask token은 공유 학습 벡터에 positional embedding을 더해 구성합니다. 각 target
block마다 predictor를 적용해 patch별 target 표현을 예측합니다.

### Loss와 EMA

```text
L = (1/M) Σ_i Σ_(j∈B_i) ||ŝ_yj - s_yj||²₂
```

- `M`: target block 수
- `B_i`: `i`번째 target block의 patch index
- `ŝ_yj`: predictor가 만든 patch `j`의 표현
- `s_yj`: target encoder가 만든 patch `j`의 표현
- 입력/출력 shape 예: `[batch, target_patch_count, embedding_dim]`

context encoder와 predictor는 gradient로 갱신합니다. target encoder는
`θ̄ ← mθ̄ + (1-m)θ`의 EMA로 갱신하며 loss의 gradient를 받지 않습니다.

## 4. Related Work 해설

논문은 denoising·colorization, MAE·BEiT·SimMIM 같은 masked reconstruction,
data2vec·CAE 같은 representation prediction, DINO·MSN·iBOT 같은
joint-embedding 계열을 비교합니다. I-JEPA의 구별점은 한 이미지 view, 학습되는
latent target, multi-block mask와 narrow predictor의 결합입니다.

## 5. Image Classification 해설

평가는 ImageNet-1K linear evaluation, label 1% low-shot, CIFAR100·Places205·
iNaturalist18 전이를 포함합니다. encoder를 고정한 linear probe는 표현 자체의
분리 가능성을 보는 지표입니다. I-JEPA ViT-H/14는 ImageNet linear evaluation
79.3을, 448 해상도 ViT-H/16은 81.1을 보고합니다. low-shot에서는 각각 73.3과
77.3입니다.

## 6. Local Prediction Tasks 해설

CLEVR의 object counting과 distance/depth prediction으로 지역 정보가 남아 있는지
평가합니다. ViT-H/14 결과는 Count 86.7, Dist 72.4입니다. 의미론적 표현을
강조하더라도 모든 공간 정보가 제거되는 것은 아니라는 근거지만, 각 baseline과
모델 크기가 같지 않은 비교도 있어 표의 조건을 함께 봐야 합니다.

## 7. Scalability 해설

latent target 계산 때문에 MAE보다 iteration당 약 7% 느리지만, 연구진은 약 5배
적은 iteration에 수렴한다고 보고합니다. ViT-H/14 학습은 약 1,200 GPU-hours로
설명됩니다. ImageNet-22K와 ViT-G/16 확대는 semantic classification에서 이득이
있었지만 local task에서는 일관된 향상이 없었습니다.

## 8. Predictor Visualizations 해설

frozen predictor 출력이 무엇을 담는지 보기 위해 연구진은 별도의 RCDM 기반
decoder를 학습해 pixel sketch로 변환합니다. 여러 random sample에서 공통으로
나타나는 자세와 객체 부위는 predictor 표현에 담긴 정보로, 달라지는 질감과
배경은 버려진 불확실성으로 해석합니다. 이 decoder는 시각화 도구이지 I-JEPA
사전학습 목적의 일부가 아닙니다.

## 9. Ablations 해설

- multi-block mask: ImageNet-1% Top-1 54.2
- rasterized/single-block/random mask: 각각 15.5/20.2/17.6
- representation target: 66.9, pixel target: 40.7
- target encoder 출력 마스킹: 67.3, 입력 마스킹: 56.1
- predictor depth 12: 66.9, depth 6: 64.0
- predictor width 384: 70.7, width 1024: 68.4

이 결과는 target의 semantic level, mask geometry와 predictor 병목이 모두 중요함을
보여 줍니다. 단, 서로 다른 표의 수치는 architecture·epoch·평가 protocol이
다르므로 표 사이 숫자를 직접 우열 비교하면 안 됩니다.

## 10. Conclusion 해설

논문은 latent prediction이 pixel reconstruction보다 빠르게 수렴하고 더 높은
semantic level의 표현을 학습할 수 있다고 결론짓습니다. 또한 사람이 설계한 view
augmentation 없이 joint-embedding representation을 학습하는 경로를 제시합니다.
이는 정적 이미지와 보고된 benchmark 범위의 결론이며 일반적인 세계 이해를
완성했다는 주장은 아닙니다.

## 부록 해설

### A. Implementation Details

backbone별 predictor depth, optimizer와 schedule, augmentation, linear probe 및
fine-tuning protocol을 제공합니다. predictor dimension은 384이고 사전학습에는
`[cls]` token을 쓰지 않습니다. 재현자는 본문 수치뿐 아니라 부록의 평가별
hyperparameter를 보존해야 합니다.

### B. Broader Related Work

contrastive·non-contrastive joint embedding과 generative approach를 더 넓게
정리합니다. I-JEPA가 완전히 독립된 발명이라기보다 기존 representation learning
연구를 latent predictive objective로 조합한 위치를 보여 줍니다.

### C. Additional Ablations

target encoder 마스킹 위치, predictor depth·width, weight decay 등을 비교합니다.
기본 weight decay schedule이 모든 protocol에서 최선은 아니었다는 점은 단일
hyperparameter를 여러 평가에 일반화할 때 주의할 근거입니다.

### D~E. Fine-tuning과 추가 시각화

전체 ImageNet fine-tuning 결과와 RCDM을 이용한 encoder/predictor 시각화를
보충합니다. 시각화는 표현의 가능한 내용을 직관적으로 해석하는 보조 증거이며,
정량 평가를 대체하지 않습니다.

## 수식·그림·표 읽기 가이드

- **Figure 3:** 위쪽은 context encoder와 위치 조건 predictor, 아래쪽은 전체
  이미지를 보는 EMA target encoder입니다. 점선은 예측과 해당 target 표현의
  patch별 L2 대응을 나타냅니다.
- **Figure 4:** target 4개를 먼저 보고, 넓은 context에서 겹침을 제거한 결과를
  읽습니다. 실제 context patch 비율은 초기 block 면적보다 작아집니다.
- **Figure 5:** x축이 log scale GPU-hours이므로 단순한 가로 거리로 배수를
  판단하면 안 됩니다.
- **Figure 6:** 같은 위치의 여러 생성 sample에서 공통 요소와 변동 요소를
  구분해 predictor의 확실성·불확실성을 해석합니다.
- **Table 6~7:** mask geometry와 target space가 low-shot linear probe에 미친
  영향을 보여 주는 핵심 ablation입니다.

## 약어 및 기술 용어 사전

| 원어·약어 | 한국어 | 논문에서의 역할 | 최초 등장 |
|---|---|---|---|
| I-JEPA | 이미지 기반 결합 임베딩 예측 아키텍처 | 제안된 자기지도학습 방법 | S001 |
| context block | 문맥 블록 | predictor가 관측하는 이미지 영역 | S001 |
| target block | 목표 블록 | latent 표현을 예측할 이미지 영역 | S001 |
| ViT | 비전 트랜스포머 | encoder와 predictor backbone | 배경 해설 |
| EMA | 지수이동평균 | target encoder를 안정적으로 갱신 | 배경 해설 |
| MAE | 마스킹 오토인코더 | pixel reconstruction 비교군 | 1절 해설 |
| linear probe | 선형 탐침 평가 | frozen representation의 분리 가능성 측정 | 5절 해설 |
| RCDM | Representation-Conditioned Diffusion Model | predictor 표현을 pixel로 시각화 | 8절 해설 |
| collapse | 표현 붕괴 | 서로 다른 입력 표현이 같아지는 실패 | 2절 해설 |

## 번역 검수 기록

- v3 PDF 17쪽의 본문·부록 section 순서를 확인했습니다.
- PDF page 3의 architecture, page 5의 분류 표, page 15의 추가 ablation을 시각
  렌더링과 추출 text로 대조했습니다.
- 수치에는 architecture·epoch·평가 protocol을 가능한 범위에서 함께 적었습니다.
- 전문 번역 제한과 분석자가 도출한 한계를 명시해 저자 주장과 해설을
  구분했습니다.

## 함께 보기

- [논문 분석 README](README.md)
- [I-JEPA 공식 코드 한국어 가이드](../ijepa/guide/README.md)
- [원문 PDF](https://arxiv.org/pdf/2301.08243v3)
