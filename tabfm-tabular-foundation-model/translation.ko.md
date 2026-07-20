# 「Introducing TabFM」 한국어 번역 요약

작성일: 2026-07-21

- 원문: [Introducing TabFM: A zero-shot foundation model for tabular data](https://research.google/blog/introducing-tabfm-a-zero-shot-foundation-model-for-tabular-data/)
- 저자: Weihao Kong, Abhimanyu Das, Google Research
- 게시일: 2026-06-30
- 원문 언어: 영어
- 접근일: 2026-07-21

> 원문의 구조, 주요 주장과 수치를 보존한 한국어 번역 요약이다. 저작권을 존중해 원문 전체를 문장 단위로 복제하지 않는다.

## TabFM 소개

TimesFM 이후 시계열 예측에서 나타난 zero-shot 접근을 일반 표 데이터로 확장한다. TabFM은 분류와 회귀 과정을 단순화하기 위해 설계한 표 데이터 foundation model이다.

표 데이터는 기업 데이터 인프라의 중심이며 고객 이탈, 금융 사기와 같은 많은 핵심 예측 애플리케이션을 구동한다. AdaBoost, XGBoost, random forest 같은 지도학습 트리 알고리즘이 오랫동안 구조화 데이터에서 강력한 성능을 보였다.

그러나 전통적 모델의 실제 배포 수명주기는 `.fit()` 한 번으로 끝나지 않는다. 신뢰할 만한 신호를 얻기 위해 하이퍼파라미터 최적화와 도메인 특화 특성 공학에 많은 시간이 들어간다.

LLM의 in-context learning은 모델 가중치를 갱신하지 않고 입력 문맥의 예시와 지시에서 새 과제를 학습하는 zero-shot 예측 능력을 보여줬다. TabFM은 표 분류·회귀를 ICL 문제로 정의해 데이터셋별 모델 훈련, 하이퍼파라미터 tuning과 복잡한 특성 공학을 줄인다. 이전에 보지 못한 표에 단일 forward pass로 예측을 생성하는 것이 목표다.

## 작동 방식

전통적 ML은 특정 데이터셋 분포에 맞게 모델 파라미터를 업데이트한다. TabFM은 레이블이 있는 과거 훈련 사례와 예측 대상 테스트 행을 하나의 통합 문맥으로 받는다. 추론 시 행과 열의 관계를 해석해 새 행을 예측한다.

표를 ICL에 적용하는 일은 자연어 tokenization보다 어렵다. 일반 언어 모델은 순서가 있는 1차원 시퀀스를 처리하지만, 표는 2차원이며 본질적으로 순서 의미가 약하다. 행 또는 열을 바꿔도 대응 관계를 함께 유지하면 표의 의미는 변하지 않아야 한다.

TabFM은 TabPFN과 TabICL 계열의 장점을 결합한 hybrid 구조를 사용하며 세 가지 핵심 메커니즘을 갖는다.

### 행·열 교대 attention

원시 표를 다층 attention 모듈로 처리한다. 열과 행 방향 attention을 교대로 적용해 특성 상호작용과 사례 간 의존성을 표현한다. 이 깊은 문맥화는 수작업 특성 생성이 담당하던 관계 학습을 모델 내부에서 수행한다.

### 행 압축

각 행의 교차 attention 정보를 하나의 조밀한 벡터 표현으로 압축한다.

### In-context learning

전용 Transformer가 압축된 행 embedding 시퀀스를 처리한다. 원시 격자가 아니라 행 벡터 사이에서 attention을 수행해 계산 비용을 크게 줄이고 더 큰 데이터셋에서도 효율적인 예측을 목표로 한다.

## 대규모 합성 데이터 훈련

Foundation model은 보통 대용량의 다양한 데이터와 고용량 신경망을 사용한다. 하지만 산업 표는 독점 schema와 민감 정보가 포함되어 공개하기 어렵기 때문에 대규모 고품질 공개 데이터가 부족하다.

합성 표는 임의로 크게 생성할 수 있어 이 규모의 사전학습에서 현실적인 대안이 된다. TabFM은 다양한 임의 함수를 포함하는 구조적 인과 모델(SCM)로 동적 생성한 수억 개의 합성 데이터셋만을 사용해 훈련됐다.

이 생성 과정은 실제 표에서 볼 수 있는 여러 분포와 복잡한 특성 관계를 포괄하려 한다. 개발팀은 이를 통해 보지 못한 실제 표에도 일반화한다고 보고한다.

## 성능과 benchmark

기존 최신 방법과 비교하기 위해 TabArena에서 평가했다. TabArena는 모델 간 승률로 Elo 점수를 계산하는 살아 있는 benchmark다. 평가는 38개 분류 데이터셋과 13개 회귀 데이터셋, 약 700~150,000개 표본 범위를 포함한다.

두 설정을 비교했다.

- **TabFM**: tuning이나 교차검증 없이 단일 forward pass로 예측하는 기본 모델
- **TabFM-Ensemble**: 교차 특성과 SVD 특성을 추가하고 비음수 최소제곱으로 32개 ensemble의 가중치를 구한다. 분류에서는 Platt scaling 보정도 사용한다.

개발팀은 기본 TabFM과 ensemble 설정 모두 경쟁력 있는 Elo 결과를 보였으며, 자세한 fold metric과 baseline별 승률은 공식 GitHub에 공개했다고 설명한다.

## 결론

TabFM은 표 예측을 in-context learning 문제로 다시 정의한다. Hybrid attention 구조와 대규모 합성 데이터를 통해 복잡한 특성 상호작용을 모델 내부에서 처리하며 수동 특성 공학, 하이퍼파라미터 최적화와 반복적인 모델 훈련의 병목을 줄인다.

Google은 TabFM을 BigQuery에 통합해 향후 `AI.PREDICT` SQL 명령으로 회귀와 분류를 수행할 수 있게 할 예정이라고 게시 시점에 밝혔다. 이 내용은 미래 제공 계획이므로 실제 사용 시 최신 BigQuery 문서를 확인해야 한다.

## 공식 모델 카드로 보완한 적용 범위

원문 블로그 외에 공식 모델 카드에는 다음 조건이 명시되어 있다.

- 숫자형·범주형 열이 섞인 표 지원
- 이진 및 최대 10개 클래스의 다중 분류
- 연속 목표 회귀
- 훈련 행이 문맥에 들어가므로 행 수에 따라 메모리 사용 증가
- 약 500개 특성까지 최적화
- 실제 고위험 도메인과 소수 집단에서 별도 검증 필요
- 모델 가중치는 비상업적 라이선스, 소스 코드는 Apache 2.0
- 정식 지원 Google 제품이 아님

## 감사의 말

이 프로젝트는 Erez Louidor Ilan, Taman Narayan, Shuxin Nie, Rajat Sen, Yichen Zhou, Joe Toth, Deqing Fu, Samet Oymak과의 공동 작업이다. 그래픽 디자인은 Kimberly Schwede가 담당했다.
