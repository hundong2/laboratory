# 12가지 JEPA 아키텍처: 모달리티별 비교와 실습

작성일: 2026-08-03

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [12가지 유형 비교](#12가지-유형-비교)
- [상세 정리](#상세-정리)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 주 출처: [Turing Post Korea, 「12가지 유형의 JEPA 아키텍처」](https://turingpost.co.kr/p/12-jepa-types)
- 저자: Ben Eum, Ksenia Se
- 게시일: 2025-05-26
- 원문 언어: 한국어
- 확인일: 2026-08-03
- 확인 범위: 공개된 본문 전체와 본문이 연결한 12개 논문의 공개 metadata 및
  초록

이 폴더는 기사의 전문 복제가 아니라, 원문이 소개한 연구들을 기초부터 비교해
학습할 수 있도록 재구성한 자료입니다. 원문이 이미 한국어이므로
[`translation.ko.md`](translation.ko.md)는 번역 대신 구조를 따른 교정·학습용
재구성본입니다. 개별 논문의 전체 번역이나 결과 재현을 주장하지 않습니다.

## 한눈에 보기

JEPA(Joint-Embedding Predictive Architecture)의 공통 질문은 다음과 같습니다.

> 관측한 context의 표현으로, 보이지 않거나 미래에 나타날 target의 표현을
> 예측할 수 있는가?

픽셀·파형 같은 원시 입력을 그대로 복원하는 대신 latent embedding을 맞춥니다.
따라서 예측하기 어려운 세부 잡음보다 의미, 구조, 동역학처럼 공유되는 정보를
학습하도록 유도할 수 있습니다.

```text
context x ── online encoder fθ ── predictor gφ ── 예측 ẑ
target  y ── target encoder fξ ────────────────── 목표 z
                                              loss(ẑ, stop-grad(z))
                         ξ ← mξ + (1-m)θ  (대표적인 EMA 방식)
```

단, 아래 12개 연구가 이 구조를 똑같이 구현하는 것은 아닙니다. 공유 encoder의
멀티태스크 목적, energy-based 정렬, LLM decoder 결합 등 연구별 차이가
있으므로 “JEPA”라는 이름만으로 세부 구현을 추정해서는 안 됩니다.

## 기초 개념

### 생성적 복원과 latent prediction

- 생성적 복원: 가린 픽셀, 토큰, 파형을 원래 값에 가깝게 복원합니다.
- latent prediction: target encoder가 만든 추상 표현을 predictor가 맞힙니다.
- 장점 후보: 원시 데이터의 불필요한 세부 정보에 쓰는 용량을 줄일 수 있습니다.
- 위험: target과 prediction이 모두 상수에 가까워지는 collapse를 막는 설계가
  필요합니다.

### 무엇이 좋은 target인가

target은 너무 쉬우면 지역적 단서만 외우게 되고, 너무 어려우면 조건부로 예측할
수 없는 잡음을 학습하게 됩니다. 모달리티의 구조에 맞는 masking이 핵심입니다.

- 이미지·3D: 공간적으로 충분히 큰 block
- 비디오·행동: 시간적으로 떨어진 구간 또는 미래 특징
- 오디오: 시간축과 주파수축의 상관관계를 고려한 spectrogram block
- 표: 의미가 서로 다른 feature subset
- EEG/fMRI: channel·ROI와 시간축을 함께 고려한 시공간 block

## 12가지 유형 비교

| 유형 | 입력·영역 | 핵심 예측 또는 결합 | 대표 원문 |
|---|---|---|---|
| I-JEPA | 이미지 | 넓은 context에서 여러 image target block의 표현 예측 | [arXiv:2301.08243](https://arxiv.org/abs/2301.08243) |
| MC-JEPA | 이미지·비디오 | 공유 encoder로 content 표현 학습과 optical flow 추정을 공동 최적화 | [arXiv:2307.12698](https://arxiv.org/abs/2307.12698) |
| V-JEPA | 비디오 | 재구성·텍스트·negative 없이 가린 시공간 특징 예측 | [arXiv:2404.08471](https://arxiv.org/abs/2404.08471) |
| UI-JEPA | 화면 UI 시퀀스 | 가린 UI 활동 표현을 학습하고 LLM decoder로 사용자 의도 예측 | [arXiv:2409.04081](https://arxiv.org/abs/2409.04081) |
| A-JEPA | 오디오 spectrogram | curriculum 방식의 시간·주파수 mask에서 target 표현 예측 | [arXiv:2311.15830](https://arxiv.org/abs/2311.15830) |
| S-JEPA | EEG | 동적 spatial attention으로 channel·공간 표현의 dataset 간 전이 강화 | [arXiv:2403.11772](https://arxiv.org/abs/2403.11772) |
| TI-JEPA | 텍스트·이미지 | energy-based 목적을 통해 두 모달리티를 공유 공간에 정렬 | [arXiv:2503.06380](https://arxiv.org/abs/2503.06380) |
| T-JEPA | 표 데이터 | 한 feature subset에서 다른 subset의 표현 예측 | [arXiv:2410.05016](https://arxiv.org/abs/2410.05016) |
| ACT-JEPA | 관찰·행동 | 관찰과 action chunk의 latent dynamics로 정책 표현 학습 | [arXiv:2501.14622](https://arxiv.org/abs/2501.14622) |
| Brain-JEPA | fMRI 시계열 | ROI×시간 target과 기능적 위치를 함께 모델링 | [arXiv:2409.19407](https://arxiv.org/abs/2409.19407) |
| 3D-JEPA | 3D 장면·표현 | 풍부한 context에서 여러 3D target block 표현 예측 | [arXiv:2409.15803](https://arxiv.org/abs/2409.15803) |
| Point-JEPA | point cloud | 정렬한 point patch 중 context에서 target 표현 예측 | [arXiv:2404.16432](https://arxiv.org/abs/2404.16432) |

> 명칭 주의: 기사에서 말하는 audio-based JEPA는 2023년의 **A-JEPA**입니다.
> 2025년에는 별도의 **Audio-JEPA**(arXiv:2507.02915)도 공개되었습니다. 이름이
> 비슷하지만 같은 논문으로 취급하면 안 됩니다.

## 상세 정리

### 1. 공간 표현: I-JEPA, 3D-JEPA, Point-JEPA

세 연구 모두 공간의 일부에서 다른 일부를 예측하지만 token을 만드는 방식이
다릅니다. I-JEPA는 2차원 image patch, 3D-JEPA는 3D 장면의 구조화된 block,
Point-JEPA는 point cloud를 local patch로 묶고 sequencer로 순서를 부여합니다.
2D raster의 인접성을 point cloud에 그대로 적용할 수 없다는 점이 중요한
차이입니다.

### 2. 시간과 동역학: MC-JEPA, V-JEPA, ACT-JEPA

- MC-JEPA는 content와 optical flow 목적이 서로 도움을 주도록 공동 학습합니다.
- V-JEPA는 비디오의 가린 시공간 영역을 latent space에서 예측하고 frozen
  backbone 평가를 강조합니다.
- ACT-JEPA는 행동을 예측 단위로 넣어 policy representation과 dynamics에
  초점을 맞춥니다. 단순 비디오 예측과 달리 action 선택의 의미가 포함됩니다.

### 3. 구조화·다중모달: UI-JEPA, TI-JEPA, T-JEPA

UI-JEPA는 화면상의 행동 sequence에서 의도 예측으로 이어지고, TI-JEPA는
텍스트와 이미지를 공동 embedding space에 정렬합니다. T-JEPA에서는 열마다
척도와 의미가 다르므로 “인접 patch”보다 어떤 feature subset을 숨길지가 더
중요합니다. 결측 패턴이 label 또는 민감 속성을 누설하지 않는지도 확인해야
합니다.

### 4. 생체신호와 오디오: A-JEPA, S-JEPA, Brain-JEPA

오디오 spectrogram, EEG, fMRI는 모두 시계열이지만 sampling rate와 공간축의
의미가 다릅니다. A-JEPA는 시간·주파수 mask curriculum을 사용합니다. S-JEPA는
EEG electrode의 공간 관계와 dataset 간 차이를 다루고, Brain-JEPA는 fMRI의
ROI(functional region)와 시간축을 교차해 target을 구성합니다. 의료·뇌 데이터의
성능은 cohort, scanner, 인구집단 차이를 포함한 외부 검증 없이는 일반화하면 안
됩니다.

### 5. 어떤 유형을 선택할까

1. 입력의 원자 단위(token/patch)를 정의합니다.
2. context로부터 예측 가능하면서 의미 있는 target 범위를 정합니다.
3. 공간, 시간, feature, modality 중 보존해야 할 구조를 mask에 반영합니다.
4. downstream task가 content, motion, intent, policy 중 무엇을 요구하는지
   결정합니다.
5. 사전학습 loss 외에 linear probe, fine-tuning, 전이와 collapse 지표를 함께
   설계합니다.

## 용어 정리

| 용어 | 설명 |
|---|---|
| joint embedding | context와 target을 비교 가능한 표현 공간에 놓는 방식 |
| predictor | context 표현을 target 위치·조건의 표현으로 변환하는 모듈 |
| target encoder | 학습 목표가 되는 embedding을 만드는 encoder |
| EMA | online encoder의 가중치를 지수이동평균해 target을 천천히 갱신하는 방법 |
| stop-gradient | target branch로 gradient가 흐르지 않게 차단하는 연산 |
| energy-based objective | 호환되는 쌍에는 낮은 energy, 맞지 않는 쌍에는 높은 energy를 부여하는 목적 |
| linear probe | encoder를 고정하고 선형 head만 학습해 표현의 유용성을 측정하는 평가 |
| collapse | 서로 다른 입력이 거의 같은 표현이 되어 정보가 사라지는 현상 |

## 실습 학습 가이드

- [`01_foundations.ipynb`](01_foundations.ipynb): 12개 유형을 데이터 구조와
  목표별로 분류하고 공통 구성 요소를 익힙니다.
- [`02_practice.ipynb`](02_practice.ipynb): grid masking과 latent Smooth L1
  계산을 표준 Python으로 구현합니다.
- [`03_advanced.ipynb`](03_advanced.ipynb): representation collapse 진단과
  실험 설계 checklist를 연습합니다.

세 notebook은 외부 패키지 없이 실행할 수 있는 작은 개념 실습입니다. 실제
논문 모델과 성능을 재현하지 않습니다.

## 다음 학습 경로

1. [사이트 학습용 재구성본](translation.ko.md)으로 12개 연구의 위치를
   파악합니다.
2. 세 notebook을 순서대로 실행해 mask와 latent target의 역할을 익힙니다.
3. 관심 모달리티의 원 논문에서 encoder, target 구성, collapse 방지, 평가
   protocol을 표로 추출합니다.
4. 같은 데이터에서 reconstruction baseline과 latent prediction을 비교합니다.
5. 사전학습 지표와 downstream 전이 성능이 함께 좋아지는지 검증합니다.
