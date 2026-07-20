# TabFM: 표 데이터용 Zero-shot Foundation Model

작성일: 2026-07-21

## 출처와 작업 범위

- 원문: [Introducing TabFM: A zero-shot foundation model for tabular data](https://research.google/blog/introducing-tabfm-a-zero-shot-foundation-model-for-tabular-data/)
- 저자: Weihao Kong, Abhimanyu Das (Google Research)
- 원문 게시일: 2026-06-30
- 원문 언어: 영어
- 확인일: 2026-07-21 (Asia/Seoul)
- 공식 코드: [google-research/tabfm](https://github.com/google-research/tabfm)
- 공식 모델 카드: [google/tabfm-1.0.0-pytorch](https://huggingface.co/google/tabfm-1.0.0-pytorch)
- 한국어 번역 요약: [translation.ko.md](translation.ko.md)

이 자료는 Google Research 블로그의 소개 내용을 한국어 학습 자료로 재구성하고, 공식 코드와 모델 카드에서 설치 방법, 구조, 적용 범위, 라이선스와 한계를 보완했다. 성능 수치는 개발팀이 보고한 TabArena 결과이며, 실제 도메인에서는 별도 검증이 필요하다.

## 한눈에 보기

TabFM은 표 데이터의 분류와 회귀를 위한 사전학습 foundation model이다. 새 데이터셋마다 모델 파라미터를 학습하는 대신, 레이블이 있는 훈련 행과 예측할 테스트 행을 하나의 문맥으로 입력한다. 모델은 한 번의 forward pass에서 행·열 관계를 해석하고 테스트 행의 값을 예측한다.

```text
전통적 표 ML
데이터 → 특성 공학 → 하이퍼파라미터 탐색 → 데이터셋별 학습 → 예측

TabFM
훈련 행 + 테스트 행 → 사전학습 모델의 in-context 추론 → 예측
```

Zero-shot은 “데이터를 전혀 보지 않는다”는 뜻이 아니다. 새 데이터셋에 맞춰 가중치를 업데이트하지 않는다는 뜻이며, 예측 시 레이블이 있는 훈련 행을 문맥으로 제공한다.

## 기초 개념

### 표 데이터

각 행은 고객이나 거래 같은 사례이고 각 열은 나이, 지역, 금액 같은 특성이다. 숫자형과 범주형 열이 섞일 수 있고, 목표 열은 분류 클래스 또는 연속값이다.

표에는 자연어와 다른 대칭성이 있다. 일반적으로 행 순서를 바꾸거나 열과 열 이름을 함께 재배치해도 데이터의 의미는 변하지 않아야 한다. 따라서 1차원 순서를 전제로 하는 일반 Transformer를 그대로 적용하기 어렵다.

### 분류와 회귀

- **분류**: 이탈 여부, 사기 유형처럼 유한한 클래스 예측
- **회귀**: 집값, 수요량처럼 연속적인 수치 예측

공식 TabFM 1.0.0 모델 카드는 이진·다중 분류와 회귀를 지원하며, 분류는 최대 10개 클래스라는 구조적 제한을 명시한다.

### In-context learning

모델 가중치를 바꾸지 않고 입력 문맥의 예시에서 현재 과제의 규칙을 추론한다. TabFM의 문맥에는 `X_train`, `y_train`, `X_test`가 들어간다. 라이브러리의 `fit()`은 scikit-learn 인터페이스를 맞추고 범주 인코더·수치 스케일러를 준비하지만, 새 데이터셋용 신경망 가중치를 학습하는 전통적 fit과는 다르다.

### Foundation model

다양한 과제 분포에서 사전학습해 여러 downstream 과제에 재사용하는 모델이다. TabFM은 실제 산업 테이블 대신 구조적 인과 모델(SCM)로 생성한 수억 개의 합성 데이터셋에서 학습한 것으로 설명된다.

## 핵심 요약

1. TabFM은 표 예측을 데이터셋별 훈련이 아닌 in-context learning 문제로 바꾼다.
2. 행·열 교대 attention으로 특성과 사례의 상호작용을 문맥화한다.
3. 각 행을 조밀한 벡터로 압축한 뒤 ICL Transformer가 훈련 행을 문맥으로 테스트 행을 예측한다.
4. SCM 기반 합성 데이터는 실제 표 부족, 개인 정보와 라이선스 문제를 피하면서 다양한 인과 구조를 제공한다.
5. 기본 TabFM은 tuning과 교차검증 없이 단일 forward pass를 사용하고, ensemble 변형은 추가 특성과 보정·혼합을 사용한다.
6. Zero-shot 편의성이 모든 데이터셋에서 task-specific 모델보다 우수함을 보장하지는 않는다.
7. 모델 가중치는 비상업적 라이선스이고 소스 코드는 Apache 2.0이므로 사용 목적별 라이선스 확인이 필수다.

## 상세 정리

### 기존 표 ML의 병목

XGBoost, random forest와 AdaBoost 같은 트리 계열 방법은 구조화 데이터에서 강력하다. 하지만 안정적인 운영 모델을 만들려면 누락값 처리, 범주 인코딩, 특성 교차, 하이퍼파라미터 탐색, 교차검증과 보정이 필요하다. 이 과정은 단순한 `.fit()` 한 번보다 훨씬 넓다.

TabFM은 이런 반복 작업의 일부를 대규모 사전학습에 흡수하려 한다. 사용자는 새 표와 label 예시를 문맥으로 제공하고 사전학습 모델을 그대로 실행한다.

### 구조 1: 행·열 교대 attention

먼저 표의 셀을 표현한 뒤 열 방향과 행 방향 attention을 교대로 적용한다.

- 열/특성 관계: 소득과 부채, 면적과 지역처럼 한 행 안의 상호작용
- 행/사례 관계: 비슷한 사례, 클래스별 패턴과 조건부 분포

공식 모델 카드는 cell을 Fourier feature와 그룹별 선형 projection으로 embedding하고, induced self-attention과 row-level attention을 사용한다고 설명한다.

### 구조 2: 행 압축

충분히 문맥화된 한 행의 여러 셀을 CLS token 기반의 조밀한 벡터로 요약한다. 원시 `행 × 열` 격자를 그대로 후속 Transformer에 넣는 대신 행 단위 표현을 사용해 계산량을 줄인다.

### 구조 3: ICL Transformer

압축된 행 벡터 시퀀스에 causal Transformer를 적용한다. 훈련 행의 특성과 label을 문맥으로 보고, 테스트 행의 출력 분포를 만든다. 공식 1.0.0 모델 카드에는 24개 ICL Transformer block, embedding dimension 256, 8개 attention head가 기재되어 있다.

### 합성 데이터와 SCM

고품질 산업 표는 스키마, 영업 비밀과 개인 정보 때문에 대규모 공개가 어렵다. TabFM은 다양한 임의 함수가 포함된 SCM으로 표와 label 관계를 동적으로 생성한다.

예를 들어 다음 인과 구조를 무작위로 바꿀 수 있다.

```text
연령 → 소득 → 구매
지역 ────────┘
노이즈 → 관찰 오차
```

함수 형태, 변수 유형, 노이즈, 결측과 상호작용을 다양화하면 모델이 특정 열 이름을 암기하기보다 여러 표 생성 과정을 추론하도록 유도할 수 있다. 그러나 합성 prior가 실제 도메인 구조를 충분히 포함하지 않으면 성능 격차가 생긴다.

### 기본 모델과 ensemble

- **TabFM**: tuning·교차검증 없이 단일 forward pass
- **TabFM-Ensemble**: 교차 특성, SVD 특성, 32개 예측의 비음수 최소제곱 혼합을 사용하고 분류에서는 Platt scaling으로 보정

따라서 “TabFM이 단일 forward pass로 모든 비교 모델을 이겼다”는 식으로 두 설정을 혼동하면 안 된다. 기본 zero-shot과 추가 계산을 쓰는 ensemble을 분리해 비교해야 한다.

### TabArena 평가

소개 글은 38개 분류 데이터셋과 13개 회귀 데이터셋, 700~150,000개 표본 범위의 TabArena를 사용했다고 밝힌다. TabArena는 head-to-head 승률에 기반한 Elo 점수를 제공한다.

Elo는 모델의 상대 순위를 요약하지만 다음 정보도 함께 봐야 한다.

- 데이터셋별 metric과 분산
- 기본값 모델인지 tuning·ensemble 모델인지
- 시간, GPU 메모리와 총 계산 예산
- 결측, 범주 cardinality와 class imbalance
- 데이터 누수 방지와 fold 구성

### 공식 설치와 최소 예제

공식 저장소 기준 Python 3.11 이상이 필요하며 JAX 또는 PyTorch backend를 선택한다.

```bash
git clone https://github.com/google-research/tabfm.git
cd tabfm

# PyTorch backend
pip install -e .[pytorch]
```

Hugging Face 패키지 설치 방식은 다음과 같다.

```bash
pip install "tabfm[pytorch]"
```

분류 예시:

```python
from tabfm import TabFMClassifier, tabfm_v1_0_0_pytorch

model = tabfm_v1_0_0_pytorch.load(model_type="classification")
classifier = TabFMClassifier(model=model)
classifier.fit(X_train, y_train)
probabilities = classifier.predict_proba(X_test)
```

회귀에서는 `TabFMRegressor`와 `model_type="regression"`을 사용한다. 실제 실행에는 모델 가중치 다운로드, 충분한 메모리와 backend 호환성이 필요하다.

## 한계와 운영 주의사항

### 기술적 한계

- 분류는 최대 10개 클래스
- 모든 훈련 행이 문맥에 들어가므로 행 수에 따라 메모리 사용 증가
- 약 500개 특성까지 최적화됐으며 매우 넓은 표에서는 저하 가능
- 이미지, 음성, 원시 텍스트, 그래프와 시퀀스용 모델이 아님
- 모든 데이터셋에서 개별 tuning 모델을 이긴다고 보장하지 않음

### 평가와 책임

합성 데이터만으로 훈련됐으므로 특정 실제 도메인, 소수 집단과 극단 분포의 성능은 충분히 특성화되지 않았다. 의료, 금융, 채용처럼 영향이 큰 영역에서는 대표성 있는 held-out 데이터로 subgroup metric, calibration, 오류 비용과 drift를 검증해야 한다.

### 라이선스

공식 모델 카드 확인 시점 기준 모델 가중치는 `TabFM Non-Commercial License v1.0`, 소스 코드는 Apache 2.0이다. 상업적 사용 가능성을 소스 코드 라이선스만 보고 판단하면 안 된다. 모델 가중치 라이선스와 배포 목적을 별도로 검토한다.

## 용어 정리

| 용어 | 설명 |
| --- | --- |
| Tabular data | 행과 열로 구성된 구조화 데이터 |
| Zero-shot | 새 과제 전용 가중치 업데이트 없이 추론하는 설정 |
| ICL | 입력에 제공된 예시로 현재 과제 규칙을 추론하는 방식 |
| Row attention | 한 행 안에서 열·특성 관계를 문맥화하는 attention |
| Column attention | 여러 행에 걸친 같은 특성 또는 사례 관계를 다루는 attention |
| Row compression | 한 행의 셀 표현을 하나 또는 소수 벡터로 요약하는 과정 |
| SCM | 변수 간 인과 구조와 생성 함수를 정의하는 구조적 인과 모델 |
| Cross feature | 둘 이상의 원본 특성을 조합한 파생 특성 |
| SVD | 행렬을 저차원 성분으로 분해하는 기법 |
| Platt scaling | 분류 score를 확률로 보정하는 방법 |
| Elo | 두 모델의 대결 결과에서 상대적 강도를 추정하는 rating |

## 실습 학습 가이드

- [`01_foundations.ipynb`](01_foundations.ipynb): 표의 행·열 순열 불변성과 in-context 예측의 기초를 확인한다.
- [`02_practice.ipynb`](02_practice.ipynb): 작은 SCM으로 여러 합성 분류 과제를 만들고 새 과제에 가중치 학습 없이 예측한다.
- [`03_advanced.ipynb`](03_advanced.ipynb): 여러 과제에서 정확도·Brier score·순열 안정성과 문맥 크기 효과를 평가한다.

노트북은 개념 재현을 위해 Python 3 표준 라이브러리만 사용한다. 실제 TabFM 신경망을 재구현하지 않으며, 공식 모델 실행은 위 설치 예제를 따른다.

## 다음 학습 경로

1. 공식 저장소의 classification·regression 예제를 작은 공개 데이터셋에서 실행한다.
2. 동일 fold에서 TabFM 기본 모델과 XGBoost·CatBoost의 기본값 및 tuning 결과를 분리 비교한다.
3. 행 수, 열 수, 범주 cardinality와 결측률에 따른 메모리·성능 변화를 측정한다.
4. 행·열 순열에 대한 예측 안정성과 calibration을 검증한다.
5. 자신의 도메인이 SCM pretraining prior와 다른 지점을 오류 사례로 분석한다.

## 확인이 필요한 사항

- Google Research 글은 BigQuery `AI.PREDICT` 통합을 “향후 몇 주” 일정으로 예고했다. 실제 제공 상태와 문법은 사용 시점의 BigQuery 공식 문서에서 다시 확인해야 한다.
- TabArena 순위는 살아 있는 benchmark이므로 모델·데이터·rating이 변할 수 있다.
- 공식 저장소는 이 모델이 정식 지원 Google 제품이 아니라고 명시한다.
