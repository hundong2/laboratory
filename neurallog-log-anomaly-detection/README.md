# NeuralLog: 로그 파싱 없는 로그 이상 탐지

작성일: 2026-07-23

## 출처와 작업 범위

- 입력 URL: [https://github.com/LogIntelligence/NeuralLog](https://github.com/LogIntelligence/NeuralLog)
- 최종 확인 URL: [https://github.com/LogIntelligence/NeuralLog](https://github.com/LogIntelligence/NeuralLog)
- 페이지 제목: `GitHub - LogIntelligence/NeuralLog: Log-based Anomaly Detection Without Log Parsing (ASE 2021, Research Track)`
- 원문 언어: 영어
- 접근일: 2026-07-23
- 작업 방식: 사용자가 명시적으로 요청한 대로 clone 또는 git submodule 추가 없이 일반 웹사이트처럼 원격 페이지와 raw 파일만 확인했다.
- GitHub 확인 메타데이터: public repository, main branch, MIT license, Python 100.0%, 39 commits, 최신 main commit `793ba5a44c652bbee32b2c85e422cbcb3722cd73`
- 확인한 원격 파일: `README.md`, `requirements.txt`, `demo/NeuralLog.py`, `neurallog/data_loader.py`, `neurallog/utils.py`, `neurallog/models/transformers.py`, `neurallog/models/positional_encodings.py`, `neurallog/models/logrobust.py`, `neurallog/models/log2vec.py`, `neurallog/models/__init__.py`
- 논문 arXiv: [https://arxiv.org/abs/2108.01955](https://arxiv.org/abs/2108.01955)
- DOI: [10.48550/arXiv.2108.01955](https://doi.org/10.48550/arXiv.2108.01955), ASE DOI [10.1109/ASE51524.2021.9678773](https://doi.org/10.1109/ASE51524.2021.9678773)
- 번역 자료: [translation.ko.md](translation.ko.md)

이 폴더는 NeuralLog 저장소와 논문을 한국어 학습 자료로 재구성한다. 일반 GitHub repository workflow를 따르지 않았으므로 submodule 등록, 내부 README 번역 파일 추가, 원격 저장소 commit/push는 수행하지 않았다.

## 한눈에 보기

NeuralLog는 로그 파싱 없이 원시 로그 메시지를 바로 의미 벡터로 바꾼 뒤, Transformer 기반 분류기로 로그 시퀀스의 이상 여부를 판정하는 방법이다. 기존 로그 이상 탐지는 로그 파서를 통해 로그 템플릿 또는 이벤트 ID를 먼저 만든 다음 머신러닝 모델에 넣는 경우가 많았다. NeuralLog의 문제의식은 이 파싱 단계가 OOV(out-of-vocabulary) 단어와 의미 오해 때문에 중요한 정보를 잃을 수 있다는 데 있다.

저장소 README와 논문 초록 기준 NeuralLog는 네 개 공개 데이터셋에서 모두 0.95 이상의 F1-score를 달성했다고 보고한다. 구현은 Python, TensorFlow 2.4, Hugging Face Transformers, scikit-learn, pandas, numpy를 사용한다.

## 기초 개념

### 로그 이상 탐지

로그 이상 탐지는 시스템 로그에서 장애, 성능 저하, 보안 이벤트, 비정상 상태를 자동으로 찾는 작업이다. 보통 여러 줄의 로그를 하나의 윈도우나 세션으로 묶고, 그 시퀀스가 정상인지 이상인지 분류한다.

### 로그 파싱

로그 파싱은 원시 로그에서 고정 템플릿과 변수 부분을 분리하는 과정이다. 예를 들어 `Disk sda failed at sector 123`과 `Disk sdb failed at sector 456`을 같은 템플릿으로 묶을 수 있다. 이 방식은 해석 가능성이 높지만, 새로운 단어와 변형된 로그 문구가 많으면 파싱 오류가 생긴다.

### OOV와 의미 오해

OOV는 학습 중 보지 못한 단어다. 운영 시스템 로그는 버전 변경, 설정 변경, 새로운 장치명, 새 오류 코드 때문에 계속 변한다. 템플릿 기반 방법은 이런 변화를 별도 이벤트로 잘못 나누거나, 반대로 중요한 의미 차이를 같은 이벤트로 합칠 수 있다.

### 의미 벡터

NeuralLog는 로그 메시지를 BERT, GPT-2, RoBERTa 같은 사전학습 언어 모델로 임베딩한다. 저장소 구현은 token hidden states를 평균 내어 768차원 semantic vector를 만든다. 이 벡터는 템플릿 ID보다 단어 의미와 문맥적 표현을 더 잘 보존하려는 목적을 갖는다.

### Transformer 기반 분류

각 로그 메시지는 하나의 벡터가 되고, 여러 로그 메시지 벡터가 시퀀스가 된다. Transformer Encoder는 self-attention으로 시퀀스 안의 서로 다른 로그 간 관계를 학습한다. NeuralLog 구현은 positional encoding, multi-head attention, feed-forward network, global average pooling, softmax classification으로 구성된다.

## 핵심 요약

- NeuralLog는 로그 파싱을 제거하고 raw log message를 직접 semantic vector로 바꾼다.
- 저장소 README는 전처리, neural representation, Transformer-based classification의 3단계를 제시한다.
- 전처리는 숫자와 특수문자를 줄이고 CamelCase를 나누며 소문자화한다.
- 의미 벡터는 BERT, GPT-2, RoBERTa encoder로 만들 수 있고, 기본 데모는 BERT를 사용한다.
- BGL/Thunderbird/Spirit 같은 supercomputer 로그는 sliding window로 시퀀스를 만들고, window 안에 실패 로그가 하나라도 있으면 anomaly label을 붙인다.
- HDFS는 BlockId 기반 session window를 사용한다.
- 모델은 `PositionEmbedding + TransformerBlock + GlobalAveragePooling1D + Dense(2, softmax)` 구조다.
- 데모는 BGL 로그를 내려받고 `demo/NeuralLog.py`를 실행해 학습과 평가를 수행한다.
- README 결과 표에서 NeuralLog는 HDFS, BGL, Thunderbird, Spirit 모두 F1-score 0.96-0.98 범위를 보인다.
- 구현은 2021년 논문 코드라 Python 3.5-3.8, TensorFlow 2.4 중심이다. 최신 Python/TensorFlow 환경에서는 호환성 조정이 필요할 수 있다.

## 상세 정리

### 1. 왜 로그 파싱을 피하는가

기존 로그 이상 탐지 파이프라인은 보통 `raw log -> parser -> log template/event ID -> sequence model` 구조다. 문제는 parser가 완벽하지 않다는 점이다. 로그 문구가 소프트웨어 버전에 따라 조금만 바뀌어도 새로운 이벤트로 취급하거나, 중요한 단어를 변수로 제거해 의미를 잃을 수 있다.

NeuralLog는 이 중간 단계를 없애고, 로그 메시지 자체를 언어 모델의 입력으로 본다. 숫자와 특수문자 같은 노이즈를 줄이되, 템플릿 추출로 원문 의미를 강하게 압축하지 않는다.

### 2. 데이터 로딩과 윈도우 구성

저장소의 `data_loader.py`는 크게 HDFS용 session loader와 BGL/Thunderbird/Spirit 같은 supercomputer 로그용 sliding-window loader를 제공한다.

HDFS는 BlockId를 정규식으로 추출해 같은 BlockId의 로그들을 하나의 세션으로 묶는다. label 파일이 있으면 `Anomaly`를 1, normal을 0으로 변환한다.

Supercomputer 로그는 한 줄의 첫 문자가 `-`가 아니면 failure log로 취급한다. `window_size`만큼 로그를 묶고, 그 안에 failure log가 있으면 window label을 1로 둔다. `step_size`는 윈도우가 얼마나 이동할지를 정한다.

### 3. 전처리 규칙

구현의 `clean()` 함수는 대략 다음 일을 한다.

- 괄호, 쉼표, 세미콜론 같은 구분 문자를 공백으로 바꾼다.
- 모두 대문자인 단어는 소문자로 바꾼다.
- CamelCase와 연속 대문자를 분리한다.
- 숫자가 포함된 단어를 제거한다.
- punctuation을 제거한다.
- 남은 토큰을 소문자화한다.

이 전처리는 파싱이 아니라 neural encoder가 다루기 쉬운 텍스트 정규화에 가깝다. 다만 숫자와 코드 값이 이상 탐지에 중요한 도메인에서는 숫자 제거가 손실이 될 수 있으므로 실제 적용 전에 검증해야 한다.

### 4. 의미 벡터 생성

저장소는 GPT-2, BERT, RoBERTa encoder 함수를 제공한다. 각 함수는 tokenizer로 로그 문자열을 토큰화하고, Transformer hidden states를 얻은 뒤 sequence 차원 평균을 계산해 768차원 벡터를 반환한다. 오류가 나면 GPT-2 함수는 0 벡터를 반환하는 방어 로직을 가진다.

이 방식은 간단하지만 비용이 크다. 대규모 로그에서는 같은 정규화 메시지를 캐시하는 것이 중요하며, 저장소 구현도 `E` 딕셔너리에 content별 embedding을 저장해 중복 계산을 줄인다.

### 5. 분류 모델

`neurallog/models/transformers.py`의 핵심 구성은 다음과 같다.

| 구성요소 | 역할 |
| --- | --- |
| 입력 | `(max_len, embed_dim)` 형태의 로그 벡터 시퀀스 |
| PositionEmbedding | 순서 정보를 더한다 |
| MultiHeadAttention | 로그들 사이의 문맥 관계를 본다 |
| Feed-forward network | attention 결과를 비선형 변환한다 |
| LayerNorm + Dropout | 안정화와 과적합 완화 |
| GlobalAveragePooling1D | 시퀀스 전체 표현을 하나로 요약 |
| Dense softmax | 정상/이상 2-class 분류 |

데모는 `embed_dim=768`, `max_len=75`, `num_heads=12`, `ff_dim=2048`, `dropout=0.1`을 사용한다.

### 6. 결과 해석

README의 결과 표에서 NeuralLog는 네 데이터셋 모두 강한 F1-score를 보인다.

| Dataset | NeuralLog Precision | NeuralLog Recall | NeuralLog F1 |
| --- | --- | --- | --- |
| HDFS | 0.96 | 1.00 | 0.98 |
| BGL | 0.98 | 0.98 | 0.98 |
| Thunderbird | 0.93 | 1.00 | 0.96 |
| Spirit | 0.98 | 0.96 | 0.97 |

이 결과는 로그 파싱 없이 semantic representation과 Transformer context modeling만으로도 강한 이상 탐지가 가능하다는 논문 주장과 맞닿아 있다. 다만 benchmark 설정, class imbalance, train/test split 방식, 라벨 품질, 로그 시간 순서 leakage 가능성은 실제 재현에서 반드시 점검해야 한다.

### 7. 실행 시 주의점

저장소의 requirements는 TensorFlow 2.4 계열과 오래된 Python 범위를 전제로 한다. 현재 환경에서 그대로 설치하면 최신 Python과 충돌할 수 있다. 또한 `requirements.txt`의 패키지들이 한 줄에 공백으로 적혀 있어, 최신 pip에서는 별도 줄로 정리하는 것이 더 안전할 수 있다.

데모는 BGL 데이터를 Zenodo에서 내려받아 `logs/BGL.log`로 배치한 뒤 `demo/NeuralLog.py`를 실행하는 흐름이다. 실제 학습은 BERT 임베딩 추출과 Transformer 학습 때문에 CPU만으로는 느릴 수 있다.

## 용어 정리

| 용어 | 의미 |
| --- | --- |
| Raw log | 파싱 전 원본 로그 문자열 |
| Log parsing | 원본 로그에서 템플릿과 변수 부분을 분리하는 과정 |
| Log template | 여러 로그가 공유하는 고정 문장 구조 |
| Log event | 파싱된 템플릿 또는 이벤트 ID |
| OOV | 학습 중 보지 못한 단어 |
| Semantic vector | 로그 메시지 의미를 담은 연속 벡터 |
| Sliding window | 연속 로그를 일정 길이로 묶는 방식 |
| Session window | BlockId 같은 식별자로 로그를 묶는 방식 |
| Positional encoding | 시퀀스 순서 정보를 벡터에 더하는 방식 |
| Self-attention | 시퀀스 내부 요소들이 서로를 참조해 표현을 갱신하는 메커니즘 |
| Precision | 이상이라고 예측한 것 중 실제 이상 비율 |
| Recall | 실제 이상 중 모델이 찾아낸 비율 |
| F1-score | precision과 recall의 조화평균 |

## 실습 학습 가이드

- [01_foundations.ipynb](01_foundations.ipynb): 로그 정규화, 파싱 손실 예시, sliding-window 라벨링을 구현한다.
- [02_practice.ipynb](02_practice.ipynb): BERT 대신 deterministic toy semantic vector를 만들어 prototype classifier로 이상 탐지를 실습한다.
- [03_advanced.ipynb](03_advanced.ipynb): positional encoding과 single-head self-attention을 손으로 구현하고, threshold sweep으로 precision/recall/F1 tradeoff를 확인한다.

## 다음 학습 경로

1. NeuralLog 논문 원문에서 OOV와 semantic misunderstanding 실험을 읽는다.
2. Drain, Spell, IPLoM 같은 로그 파서가 어떤 가정으로 템플릿을 만드는지 비교한다.
3. BERT 평균 풀링 대신 Sentence-BERT, domain-adapted log encoder, contrastive pretraining을 적용해 본다.
4. BGL/HDFS 데이터에서 split 방식이 결과에 미치는 영향을 재현한다.
5. 실서비스 적용 전에는 숫자 제거, IP/path 제거, 시간 순서 leakage, class imbalance, concept drift를 별도 실험으로 검증한다.
