# 서버 이상 탐지 오픈소스 공식 자료 한국어 정리

작성일: 2026-07-24

이 문서는 조사에 사용한 영문 공식 문서와 논문의 핵심 내용을 한국어로 재구성한다. 여러 출처를 하나의 전문처럼 합치지 않고, 출처별 범위와 주의점을 구분한다.

## River와 HalfSpaceTrees

- 원문: [River 공식 저장소](https://github.com/online-ml/river)
- API: [HalfSpaceTrees](https://riverml.xyz/latest/api/anomaly/HalfSpaceTrees/)
- 라이선스: BSD-3-Clause

River는 streaming data를 한 건씩 처리하는 online machine learning 라이브러리다. anomaly detection, drift detection, online statistics, preprocessing과 progressive validation을 지원한다.

공식 문서는 online 접근이 필요한 상황을 다음처럼 설명한다.

- 과거 전체 데이터를 다시 읽지 않고 새 관측으로 모델을 갱신해야 한다.
- concept drift에 대응해야 한다.
- event 단위로 데이터가 도착하는 production 흐름을 가깝게 모사해야 한다.

HalfSpaceTrees는 Isolation Forest의 online 변형이다. anomaly가 넓게 흩어진 상황에는 잘 작동하지만 한 window에 조밀하게 모이면 약할 수 있다.

주요 기본값:

- `n_trees=10`
- `height=8`
- `window_size=250`
- feature 범위 `[0, 1]`

feature가 0~1 범위가 아니면 `limits`를 명시하거나 MinMaxScaler를 사용한다. 높은 score는 anomaly를 뜻한다. `learn_one`과 `score_one`의 시간은 tree 수에 선형으로 증가하고, tree height가 커지면 node 수가 지수적으로 증가한다.

## scikit-learn IsolationForest

- 원문: [IsolationForest API](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)

IsolationForest는 tree에서 관측치를 고립시키는 데 필요한 split 수를 이용한다. leaf 깊이가 얕고 적은 split으로 분리되는 관측치는 정상 군집과 멀리 떨어진 것으로 본다. 여러 tree의 평균 anomaly score를 사용한다.

작은 다변량 tabular feature에 적용하기 쉽지만 기본 API는 batch fit이다. 새 데이터마다 model을 조금씩 갱신해야 하는 stream에서는 River 같은 online 구현이 더 자연스럽다.

## Drain3

- 원문: [Drain3 공식 저장소](https://github.com/logpai/Drain3)
- 라이선스: MIT

Drain3는 raw log stream에서 template cluster를 online으로 추출한다. 고정 깊이 parse tree를 사용해 지나치게 깊고 불균형한 tree를 피한다.

주요 기능:

- log 한 줄씩 streaming 처리
- IP, 숫자, email 같은 parameter masking
- file, Kafka, Redis persistence
- 학습과 빠른 inference mode 분리
- `max_clusters`와 LRU eviction을 이용한 memory 제한
- template에서 변수 parameter 추출

정확도를 높이려면 timestamp, hostname, severity 같은 구조화 필드를 먼저 분리하고 자유 형식 message를 입력하는 것이 좋다.

Drain3의 출력에는 cluster ID, cluster size, 전체 cluster 수, template와 변화 유형이 포함된다. 이 값들은 새 template, template count와 event transition을 anomaly feature로 만드는 데 사용할 수 있다.

## LogAI

- 원문: [Salesforce LogAI](https://github.com/salesforce/logai)
- 라이선스: BSD-3-Clause

LogAI는 OpenTelemetry data model과 호환되는 log analytics toolkit이다. log summarization, clustering, anomaly detection, GUI와 benchmark workflow를 제공한다.

Anomaly detection은 크게 두 흐름을 지원한다.

- 일정 시간마다 log count vector를 만들어 ETS 같은 time-series detector에 넣는다.
- logline을 semantic vector로 바꿔 One-Class SVM 같은 outlier detector에 넣는다.

core 설치는 가볍게 유지하고 deep learning, GUI, 개발 의존성을 extra로 분리한다. 특정 경량 model 하나라기보다 여러 log 분석 실험을 같은 interface로 비교하기 위한 framework에 가깝다.

## Loglizer

- 원문: [Loglizer](https://github.com/logpai/loglizer)
- 라이선스: MIT

Loglizer는 log collection, parsing, window 구성, feature extraction과 anomaly detection으로 이어지는 전통적인 pipeline을 제공한다.

구현된 후보에는 logistic regression, decision tree, SVM, LOF, One-Class SVM, Isolation Forest, PCA, invariant mining과 clustering이 있다. 공식 README는 모델이 자동으로 모든 환경에 맞는 것이 아니며 자체 데이터에서 parameter를 조정해야 한다고 강조한다.

## Kitsune와 KitNET

- 논문: [Kitsune: An Ensemble of Autoencoders for Online Network Intrusion Detection](https://arxiv.org/abs/1802.09089)
- 구현: [Kitsune-py](https://github.com/ymirsky/Kitsune-py)

Kitsune는 online network intrusion detection system이며 핵심 anomaly detector가 KitNET이다. KitNET은 feature를 여러 작은 그룹으로 나누고, 각 그룹의 autoencoder와 최종 output autoencoder를 결합한다.

논문은 Raspberry Pi 환경에서 실행하면서 offline detector와 비교 가능한 공격 탐지 성능을 목표로 한다. 이는 network traffic을 위한 연구 결과이며 일반 server metric에 그대로 적용된다는 의미는 아니다.

## DeepLog와 NeuralLog

DeepLog는 log event sequence를 자연어 문장처럼 보고 LSTM으로 다음 event를 예측한다. 실제 event가 model의 top-k 후보에 없으면 anomaly로 판단할 수 있다.

NeuralLog는 parser가 만드는 정보 손실을 줄이기 위해 raw log message의 semantic representation을 만들고 Transformer classifier로 log sequence를 분류한다. 사전학습 언어 모델을 사용하므로 통계 detector나 HalfSpaceTrees보다 무겁다.

## Merlion 유지 상태

- 원문: [Salesforce Merlion](https://github.com/salesforce/Merlion)
- 라이선스: BSD-3-Clause

Merlion은 시계열 anomaly detection, forecasting, change point detection과 benchmark를 하나의 framework로 제공한다. 그러나 공식 저장소는 2026-03-11 archive되어 read-only 상태다. 기능 조사에는 유용하지만 신규 운영 의존성으로 선택할 때는 유지보수 공백을 고려해야 한다.

## 조사 결론

가장 작은 운영 구성을 원하면 다음 순서가 합리적이다.

1. Median/MAD 또는 EWMA로 설명 가능한 기준선을 만든다.
2. 다변량 stream에는 River HalfSpaceTrees를 추가한다.
3. 로그는 Drain3 template count와 transition score로 결합한다.
4. network intrusion이 핵심일 때 KitNET을 별도 평가한다.
5. event sequence의 의미와 문맥이 꼭 필요할 때만 DeepLog·NeuralLog로 확장한다.

경량 detector의 핵심은 model 크기보다 정상 구간 선정, contamination 방지, threshold, persistence와 feedback loop다.
