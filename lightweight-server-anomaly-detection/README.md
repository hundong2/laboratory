# 서버 이상징후 탐지를 위한 오픈 경량 모델

작성일: 2026-07-24

## 출처와 작업 범위

이 문서는 서버의 메트릭, 로그, 네트워크 흐름과 추적 정보를 이용해 이상징후를 찾는 오픈소스 경량 모델을 조사하고, 작은 환경에서도 실행할 수 있는 실습을 제공한다.

주요 확인 자료와 확인일은 다음과 같다.

- [River 공식 저장소](https://github.com/online-ml/river) 및 [HalfSpaceTrees 문서](https://riverml.xyz/latest/api/anomaly/HalfSpaceTrees/) — 2026-07-24
- [scikit-learn IsolationForest 문서](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html) — 2026-07-24
- [Drain3 공식 저장소](https://github.com/logpai/Drain3) — 2026-07-24
- [LogAI 공식 저장소](https://github.com/salesforce/logai) — 2026-07-24
- [Loglizer 공식 저장소](https://github.com/logpai/loglizer) — 2026-07-24
- [Kitsune/KitNET 논문](https://arxiv.org/abs/1802.09089) 및 [공식 구현](https://github.com/ymirsky/Kitsune-py) — 2026-07-24
- [Salesforce Merlion 저장소](https://github.com/salesforce/Merlion) — 2026-07-24
- 영문 공식 자료 한국어 정리: [translation.ko.md](translation.ko.md)

“경량”은 절대적인 모델 크기가 아니라 단일 서버 또는 작은 관측 파이프라인에서 CPU 중심으로 운용 가능하고, 데이터 한 건씩 갱신하거나 제한된 메모리로 학습할 수 있다는 의미로 사용한다. 실제 자원 사용량은 feature 수, window, tree 수와 로그 발생량에 따라 측정해야 한다.

## 한눈에 보기

### 결론

오픈 경량 모델은 있다. 가장 현실적인 시작점은 다음 조합이다.

```text
Prometheus/OpenTelemetry 메트릭 ─┐
                                ├─ 경량 점수화 ─ 지속 조건 ─ 알림
Drain3 로그 템플릿·전이 ────────┤
                                └─ 배포·점검 시간 억제
```

- **실시간 메트릭**: River `HalfSpaceTrees`
- **주기적인 배치 분석**: scikit-learn `IsolationForest`
- **로그**: Drain3로 템플릿화한 뒤 빈도·전이·카운터 이상 탐지
- **네트워크 패킷/flow**: KitNET
- **로그 의미 분석이 꼭 필요할 때**: DeepLog 또는 NeuralLog

범용 사전학습 모델 하나를 내려받아 모든 서버에 바로 적용하는 방식은 권장하지 않는다. 정상 상태와 배포 패턴이 조직마다 다르므로, 대부분의 이상 탐지기는 해당 환경의 정상 구간으로 calibration하거나 학습해야 한다.

## 모델 후보 비교

| 후보 | 입력 | 방식 | 상대 자원 | 온라인 학습 | 추천도 |
|---|---|---|---|---|---|
| Median/MAD, EWMA, CUSUM | 개별 메트릭 | 통계 기준선 | 매우 낮음 | 가능 | 첫 기준선 |
| River HalfSpaceTrees | 다변량 메트릭 | streaming isolation tree | 낮음 | 가능 | 실시간 추천 |
| scikit-learn IsolationForest | 다변량 메트릭·집계 로그 | tree ensemble | 낮음~중간 | 기본 구현은 batch | 배치 추천 |
| PyOD HBOS/ECOD/COPOD | 표 형태 feature | histogram/empirical distribution | 낮음 | 모델별 상이 | 빠른 비교 |
| Drain3 + 빈도/전이 | 원시 로그 | template mining + 통계 | 매우 낮음 | 가능 | 로그 추천 |
| LogAI | 로그·시계열 | 여러 모델을 묶는 toolkit | 설정에 따라 다름 | 모델별 상이 | prototype |
| KitNET | network feature | 작은 autoencoder ensemble | 낮음 | 가능 | 네트워크 전용 |
| DeepLog | 로그 event sequence | LSTM next-event prediction | 중간 | 추가 구현 필요 | 문맥 필요 시 |
| NeuralLog | raw log sequence | language model + Transformer | 높음 | 주로 batch | 정확도 연구용 |
| Merlion | 시계열 | 통계·tree·deep model toolkit | 다양 | 모델별 상이 | 신규 도입 주의 |

Merlion은 기능이 풍부하지만 공식 GitHub 저장소가 2026-03-11 archive되어 read-only다. 기존 사용자는 참고할 수 있으나 신규 운영 표준으로 채택하기 전 유지보수 계획을 확인해야 한다.

## 기초 개념

### 이상징후는 데이터 종류마다 다르다

| 신호 | 예시 | 잘 잡는 이상 |
|---|---|---|
| 메트릭 | CPU, memory, p95 latency, error rate | spike, level shift, 점진적 악화 |
| 로그 | template, severity, event sequence | 새 오류, 비정상 순서, 발생량 급증 |
| trace | span latency, dependency edge, status | 특정 구간 병목, 새 실패 경로 |
| network flow | packet size, protocol, connection rate | scan, flood, exfiltration 패턴 |

한 모델에 raw 데이터를 모두 넣기보다 각 신호에서 설명 가능한 feature를 만든 뒤 점수를 결합하는 편이 경량이다.

### Point anomaly, contextual anomaly, collective anomaly

- **Point anomaly**: 한 시점의 CPU 99%처럼 개별 값이 튄다.
- **Contextual anomaly**: CPU 70%가 낮 시간에는 정상이지만 새벽에는 비정상이다.
- **Collective anomaly**: 개별 로그는 정상이어도 `retry → timeout → failover` 순서가 반복되면 이상이다.

IsolationForest나 HalfSpaceTrees는 주로 다변량 point anomaly에 강하다. 계절성과 event sequence는 시간 feature, lag, rolling statistic 또는 별도 전이 모델을 추가해야 한다.

### Unsupervised가 곧 무학습은 아니다

label이 없어도 정상 분포를 익히는 기간이 필요하다.

1. 정상으로 추정되는 warm-up 구간을 모은다.
2. feature 범위와 결측·이상 값을 정리한다.
3. anomaly score 분포에서 threshold를 정한다.
4. 경보 이후 데이터를 무조건 재학습하지 않는다.
5. 운영자 판정으로 false positive와 miss를 기록한다.

장애 데이터를 정상으로 학습하면 **model contamination**이 생긴다. 경보 점수가 높은 관측치는 학습에서 제외하거나, 확정된 정상 데이터만 지연 반영하는 장치가 필요하다.

## 핵심 요약

### River HalfSpaceTrees

River는 BSD-3-Clause 라이선스의 online machine learning 라이브러리다. 2026-07-24 기준 최신 공식 release는 0.25.0이며 Python 3.11 이상을 대상으로 한다.

`HalfSpaceTrees`는 Isolation Forest의 online 변형이다.

- 한 건씩 `score_one()`과 `learn_one()`을 호출한다.
- 기본 tree 수는 10, height는 8, window size는 250이다.
- feature는 기본적으로 0~1 범위를 가정하므로 scaler나 명시적 `limits`가 필요하다.
- 흩어진 anomaly에는 유용하지만, anomaly가 한 window에 빽빽하게 몰리면 성능이 떨어질 수 있다.
- tree 수에는 선형, height에는 지수적으로 계산량이 증가한다.

서버 지표에서는 CPU 0~100, error rate 0~1처럼 물리적 범위를 `limits`로 주면 해석이 쉽다.

### IsolationForest

IsolationForest는 무작위 split으로 관측치를 고립시킨다. 적은 split만으로 고립되는 관측치를 anomaly로 본다.

장점:

- label 없이 다변량 feature를 처리한다.
- CPU만으로도 시작하기 쉽다.
- scikit-learn의 안정적인 API와 pipeline을 이용할 수 있다.

주의:

- 기본 구현은 새 데이터 한 건씩 갱신하는 streaming model이 아니다.
- 오염률 `contamination`과 threshold 선택이 경보량을 크게 바꾼다.
- 계절성은 시간대, 요일, rolling baseline 같은 feature로 표현해야 한다.

### Drain3

Drain3는 MIT 라이선스의 streaming log template miner다. 고정 깊이 parse tree로 raw log를 template cluster에 매핑한다.

```text
connected to 10.0.0.1
connected to 192.168.0.1
→ connected to <:IP:>
```

Drain3 자체는 anomaly detector가 아니다. 다음 feature를 만들기 위한 전처리기다.

- 새 template 등장 여부
- template별 초당 발생량
- `ERROR/WARN` 비율
- template 전이 확률
- parameter 값의 범위

`max_clusters`와 LRU eviction으로 무한한 로그 stream에서 메모리를 제한할 수 있고, file·Kafka·Redis persistence를 지원한다.

### KitNET

KitNET은 작은 autoencoder 여러 개로 network feature를 나눠 학습하고, reconstruction error를 anomaly score로 사용한다. Kitsune 논문은 Raspberry Pi에서도 동작하는 online NIDS를 목표로 했다.

적합한 경우:

- packet/flow feature를 지속적으로 받을 수 있다.
- 정상 traffic warm-up을 확보할 수 있다.
- 공격 유형 label보다 알려지지 않은 deviation을 찾고 싶다.

메트릭과 일반 application log를 위한 첫 선택은 아니다.

### DeepLog와 NeuralLog

DeepLog는 LSTM으로 다음 log event를 예측하고 정상 순서에서 벗어난 event를 찾는다. NeuralLog는 log parser를 생략하고 사전학습 언어 모델의 semantic vector와 Transformer를 사용한다.

다음 상황에서 고려한다.

- 같은 template가 많지만 순서 문맥이 핵심이다.
- parser가 의미 차이를 자주 지운다.
- GPU 또는 충분한 batch inference 자원이 있다.
- label·benchmark와 재학습 체계를 운영할 수 있다.

이 저장소의 [NeuralLog 학습 자료](../neurallog-log-anomaly-detection/README.md)에서 더 자세히 볼 수 있다.

## 권장 아키텍처

### 1단계: 작은 서버 한 대

```text
node_exporter/process metrics
  → 10~30초 집계
  → Median/MAD 또는 EWMA
  → 2~3회 지속 시 alert
```

처음부터 machine learning을 넣지 않는다. 계절성이 약하고 metric 수가 적으면 통계 기준선이 더 설명 가능하다.

### 2단계: 다변량 실시간 탐지

```text
cpu, memory, disk, latency, error rate
  → validation / clipping
  → HalfSpaceTrees.score_one
  → threshold + persistence
  → 정상으로 판단된 data만 learn_one
```

### 3단계: 로그 결합

```text
raw log
  → timestamp/hostname/severity 분리
  → Drain3 template ID
  → count, new-template, transition surprise
  → metric score와 fusion
```

### 4단계: 운영 피드백

```text
alert → incident 여부 판정 → threshold/feature 수정
      → 배포·점검 window 등록
      → drift 검토 후 명시적 retraining
```

## Feature 설계

### 메트릭

- `cpu_pct`, `memory_pct`, `disk_usage_pct`
- `p95_latency_ms`, `request_rate`, `error_rate`
- connection pool 사용률, queue depth
- 이전 시점 대비 변화량 `delta`
- 5분·1시간 rolling mean과 표준편차
- 같은 요일·시간대 baseline과의 차이

### 로그

- template별 count와 증가율
- 새 template 여부
- `ERROR / total`, `WARN / total`
- 이전 template에서 현재 template로의 transition surprise
- 같은 request/session 안 event 수와 길이

### cardinality 주의

request ID, UUID, IP, container ID를 그대로 feature로 쓰면 cardinality가 폭발한다. 구조화 필드는 별도 보존하되 모델 입력에서는 masking, hashing 또는 집계를 사용한다.

## Threshold와 경보 정책

모델이 반환하는 것은 보통 anomaly score이며 alert 자체가 아니다.

권장 정책:

1. 정상 calibration score의 99~99.9 percentile에서 시작한다.
2. 2~3회 연속 초과 또는 5분 중 3회 초과를 요구한다.
3. error budget, SLO burn rate와 함께 본다.
4. 배포·점검 window는 suppress하거나 별도 label로 기록한다.
5. 한 incident 동안 같은 원인의 alert를 묶는다.

고정 `contamination=0.01`은 “항상 1%가 장애”라는 뜻이 될 수 있다. 실제 alert budget과 incident 빈도에 맞춰 threshold를 검증해야 한다.

## 평가 방법

### 데이터 분할

시간 순서를 보존한다.

```text
과거 정상 warm-up → calibration → 미래 test
```

random shuffle split은 미래 정보를 과거로 누출할 수 있다.

### 지표

- event precision / recall / F1
- incident 단위 recall
- false alerts per day
- mean time to detect
- 한 incident 동안 중복 alert 수
- score 계산 latency와 memory

point-adjusted F1만 높이면 긴 장애 구간에서 한 번만 맞혀도 과대평가될 수 있다. incident-level metric과 경보량을 함께 보고한다.

## 용어 정리

| 용어 | 설명 |
|---|---|
| Anomaly score | 관측이 정상 분포에서 얼마나 벗어났는지 나타내는 연속값 |
| Threshold | anomaly score를 alert 후보로 바꾸는 경계값 |
| Warm-up | 모델이 정상 기준선을 익히는 초기 구간 |
| Calibration | score 분포와 alert budget을 이용해 threshold를 정하는 과정 |
| Contamination | 장애나 공격 데이터가 정상 학습 데이터에 섞이는 현상 |
| Concept drift | 시간에 따라 정상 데이터의 분포가 달라지는 현상 |
| Persistence gate | 여러 관측에서 이상이 지속될 때만 alert를 확정하는 규칙 |
| Template mining | raw log의 고정 문장과 가변 parameter를 분리해 event 유형을 만드는 과정 |
| Transition surprise | 이전 event 다음에 현재 event가 나타날 확률이 낮을수록 커지는 점수 |
| Shadow mode | 경보를 운영자에게 paging하지 않고 탐지 결과만 기록하는 검증 단계 |
| Incident | 사용자 영향이나 조치가 필요한 하나의 장애 사건 |
| Alert budget | 일정 기간 운영팀이 처리할 수 있도록 허용한 최대 경보량 |

## 운영 위험과 대응

| 위험 | 증상 | 대응 |
|---|---|---|
| 정상 변화 | 배포 후 false positive 급증 | 배포 label, 단계적 재학습 |
| contamination | 장애가 더 이상 alert되지 않음 | 고득점 관측 학습 제외 |
| 계절성 | 매일 같은 시간 alert | 시간대 baseline, seasonal feature |
| alert storm | 한 장애에 수백 alert | persistence, grouping, cooldown |
| silent failure | collector 중단을 정상으로 오인 | missing-data alert 별도 운영 |
| template explosion | 로그 cluster 수 급증 | masking, `max_clusters`, schema 수정 |
| 보안 우회 | 공격자가 정상 패턴을 천천히 학습시킴 | delayed learning, 승인된 retraining |

## 최소 도입안

1. 핵심 서비스 하나와 metric 5~10개를 고른다.
2. 2주 이상의 정상·장애·배포 구간을 모은다.
3. MAD 기준선과 HalfSpaceTrees를 shadow mode로 함께 돌린다.
4. 하루 alert budget을 정하고 threshold를 맞춘다.
5. Drain3 template count와 metric score를 결합한다.
6. 2~4주 운영자 feedback 이후 paging 연결을 검토한다.

모델 score만으로 서버를 자동 재시작하거나 traffic을 차단하지 않는다. 먼저 관찰, ticket 생성, 사람 승인 순으로 자동화 수준을 올린다.

## 실습 학습 가이드

설치:

```bash
python -m pip install -r requirements.txt
```

1. [01_foundations.ipynb](01_foundations.ipynb)
   - 외부 패키지 없이 rolling median/MAD detector를 만든다.
   - warm-up, spike, persistence와 precision/recall을 배운다.
2. [02_practice.ipynb](02_practice.ipynb)
   - River `HalfSpaceTrees`로 CPU·memory·latency·error rate stream을 점수화한다.
   - calibration percentile과 contamination 방지 학습을 구현한다.
3. [03_advanced.ipynb](03_advanced.ipynb)
   - 로그 template 전이 surprise와 metric score를 결합한다.
   - maintenance성 희귀 로그와 실제 장애를 구분하는 persistence gate를 만든다.

실습은 합성 데이터이므로 좋은 점수가 실제 서버 성능을 보장하지 않는다. 다음 단계에서는 OpenTelemetry 또는 Prometheus export 데이터를 같은 feature schema로 변환한다.

## 다음 학습 경로

1. Prometheus query 결과를 1분 feature row로 변환한다.
2. 배포·점검·incident label을 함께 저장한다.
3. MAD, HalfSpaceTrees, IsolationForest를 동일 시간 분할에서 비교한다.
4. Drain3 template count를 추가해 false alert가 줄어드는지 확인한다.
5. request/session 단위 문맥이 필요하면 DeepLog를 비교한다.
6. parser 손실이 크고 자원이 충분하면 NeuralLog를 검토한다.
7. shadow mode에서 memory, CPU, alerts/day를 측정한 뒤 production paging을 결정한다.

## 참고 자료

- [River: online machine learning](https://github.com/online-ml/river)
- [River HalfSpaceTrees](https://riverml.xyz/latest/api/anomaly/HalfSpaceTrees/)
- [scikit-learn IsolationForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)
- [Drain3](https://github.com/logpai/Drain3)
- [LogAI](https://github.com/salesforce/logai)
- [Loglizer](https://github.com/logpai/loglizer)
- [Kitsune: An Ensemble of Autoencoders for Online Network Intrusion Detection](https://arxiv.org/abs/1802.09089)
- [DeepLog PyTorch implementation](https://github.com/Thijsvanede/DeepLog)
- [NeuralLog 학습 자료](../neurallog-log-anomaly-detection/README.md)
