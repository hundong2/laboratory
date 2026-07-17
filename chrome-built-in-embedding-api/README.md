# Chrome Built-in AI Embedding API

작성일: 2026-07-17

## 출처와 작업 범위

- 입력 URL: [Built-in AI Early Preview Program - Embedding API](https://docs.google.com/document/u/0/d/1ZB6MW8UDczm4V6ej5MorZWqFCYWwLhUs5HKxEdjP35c/mobilebasic)
- 원문 제목: `CHROME / Built-in AI Early Preview Program / Embedding API`
- 원문 작성자: Deepti Bogadi, Ian Zhao, Kenji Baheux
- 원문 최종 업데이트: 2026-07-16
- 확인 기준일: 2026-07-17
- 보조 공식 자료:
  - [Chrome Built-in AI 문서](https://developer.chrome.com/docs/ai/built-in)
  - [Embedding API explainer](https://github.com/explainers-by-googlers/embedding-api)
  - [EmbeddingGemma model card](https://ai.google.dev/gemma/docs/embeddinggemma/model_card)
- 작업 범위: Chrome Canary Early Preview의 `SemanticEmbedder` 기반 Embedding API를 한국어 학습 문서, 번역 요약, 개념 실습, 검색 응용 실습, 실제 브라우저 데모로 정리한다.

원문은 영어 문서이므로 `translation.ko.md`에 핵심 구조와 API 사용 흐름을 한국어로 번역 및 해설했다.

## 한눈에 보기

Chrome의 Built-in AI Embedding API는 브라우저에 내장된 온디바이스 모델로 텍스트 임베딩을 생성하는 Early Preview API다. 개발자는 서버로 원문 텍스트를 보내지 않고도 문장 유사도, 로컬 검색, 분류, 클러스터링 같은 의미 기반 기능을 만들 수 있다.

문서 기준으로 이 API는 데스크톱 Chrome Canary에서만 실험할 수 있으며, `chrome://flags/#semantic-embedder-api` 플래그를 직접 켜야 한다. 초기 사용자 프로필에서는 모델 다운로드가 필요하고, 아직 다운로드 진행률 이벤트가 없으므로 `SemanticEmbedder.availability()`가 `available`을 반환할 때까지 기다린 뒤 `SemanticEmbedder.create()`를 호출해야 한다.

가장 중요한 설계 포인트는 임베딩 벡터가 같은 공간에서 만들어진 경우에만 직접 비교할 수 있다는 점이다. 모델 버전, 차원, 태스크 최적화가 달라지면 같은 숫자 배열처럼 보여도 코사인 유사도를 그대로 비교하면 안 된다.

## 기초 개념

### 임베딩

임베딩은 텍스트를 숫자 벡터로 바꾼 표현이다. 사람에게는 "브라우저에서 모델이 실행된다"와 "온디바이스 AI가 동작한다"가 비슷한 문장으로 보이지만, 컴퓨터는 문자 그대로 비교하면 두 문장이 다르다고 본다. 임베딩은 이런 문장을 의미 공간의 가까운 위치에 놓기 위해 사용된다.

### 코사인 유사도

임베딩 벡터 사이의 유사도를 비교할 때는 코사인 유사도를 자주 쓴다. 두 벡터가 같은 방향을 가리키면 1에 가깝고, 관련이 낮으면 0에 가까워진다. 값의 크기보다 방향을 비교하므로 문장 길이가 조금 달라도 의미 비교에 유리하다.

### 온디바이스 AI

온디바이스 AI는 모델 추론이 서버가 아니라 사용자의 기기에서 일어나는 방식이다. 장점은 낮은 지연 시간, 서버 비용 감소, 민감한 원문 텍스트를 외부로 보내지 않는 프라이버시 개선이다. 단점은 기기 성능, 브라우저 지원 상태, 모델 다운로드와 저장 공간, 버전 관리의 영향을 받는다는 점이다.

### `taskType`

Embedding API는 용도에 맞는 임베딩 품질 최적화를 위해 `taskType`을 제공한다.

| `taskType` | 용도 |
| --- | --- |
| `semantic-similarity` | 두 문장이나 짧은 텍스트의 의미 유사도 비교 |
| `retrieval-document` | 검색 대상 문서 컬렉션을 임베딩해 인덱싱 |
| `retrieval-query` | 사용자의 검색 질의를 실시간 임베딩 |
| `classification` | 감정 분석, 스팸 탐지 같은 라벨 분류 |
| `clustering` | 비슷한 문서를 묶는 군집화 |

원문은 `taskType`을 지정하지 않으면 기본 태스크를 자동 선택하지 않고 입력 문자열을 그대로 임베딩한다고 설명한다. 따라서 실제 기능을 만들 때는 사용 목적에 맞는 값을 명시하는 편이 안전하다.

## 핵심 요약

- API 이름은 원문 예제 기준 `SemanticEmbedder`다.
- 사용 흐름은 `availability()` 확인, `create()`, `embed()`, `destroy()` 순서다.
- 단일 문자열과 문자열 배열 배치 입력을 모두 지원한다.
- 결과는 `Float32Array` 형태의 벡터 배열로 반환된다.
- 초기 모델 다운로드가 완료되기 전에는 `create()`가 실패할 수 있다.
- 현재 문서 기준 다운로드 진행률 이벤트는 아직 없다.
- 현재 지원 대상은 Linux, macOS, Windows 데스크톱이다.
- Early Preview API이므로 Chrome Canary와 실험 플래그가 필요하다.
- 임베딩은 같은 모델 버전과 같은 벡터 공간에서 나온 것끼리만 비교해야 한다.
- 이 API는 벡터 DB나 저장소를 제공하지 않으므로 IndexedDB, OPFS, 서버 DB 등 별도 저장 전략이 필요하다.

## 상세 정리

### 1. 초기 설정

문서 기준으로 테스트에는 Chrome Canary가 필요하며 버전은 `152.0.7943.0`보다 커야 한다. 이후 `chrome://flags/#semantic-embedder-api`에서 Embedding API 플래그를 켠다. 플래그 적용 후에는 브라우저 재시작이 필요할 수 있다.

처음 실행하는 사용자 프로필에서는 내장 모델을 내려받는 시간이 걸린다. 원문은 다운로드 진행률 이벤트가 아직 없으므로 `SemanticEmbedder.availability()`가 `available`을 반환하는지 확인한 뒤 생성해야 한다고 강조한다.

### 2. 기본 사용 흐름

실제 브라우저 코드의 흐름은 다음과 같다.

1. `SemanticEmbedder` 전역 객체가 있는지 확인한다.
2. `await SemanticEmbedder.availability()`로 사용 가능 상태를 확인한다.
3. `await SemanticEmbedder.create()`로 embedder 인스턴스를 만든다.
4. `await semanticEmbedder.embed(text, { taskType })`로 단일 또는 배치 임베딩을 만든다.
5. `result.embeddings[i].values`에서 `Float32Array` 벡터를 꺼낸다.
6. 코사인 유사도, 벡터 검색, 분류 등 애플리케이션 로직에 사용한다.
7. 사용 후 `semanticEmbedder.destroy()`로 리소스를 해제한다.

### 3. 차원과 모델 버전

원문 예제의 결과 구조에는 `Float32Array(256)`이 예시로 등장한다. 반면 EmbeddingGemma 모델 카드는 기본 출력 차원 768과 512, 256, 128로 줄여 쓰는 선택지를 설명한다. Early Preview API의 실제 반환 차원은 구현과 설정에 따라 달라질 수 있으므로 코드에서 차원을 하드코딩하지 말고 `values.length`로 확인하는 방식이 안전하다.

또한 벡터 비교는 같은 임베딩 공간에서 나온 값끼리만 해야 한다. 예를 들어 오늘 만든 문서 벡터와 브라우저 업데이트 후 만든 질의 벡터가 같은 공간인지 확인하지 않고 섞으면 검색 품질이 무너질 수 있다. 실제 제품에서는 모델 또는 벡터 공간 식별자를 저장하고, 바뀌면 인덱스를 다시 만드는 정책이 필요하다.

### 4. 검색 애플리케이션 설계

문서 검색을 만들 때는 문서와 질의를 같은 방식으로 처리하면 안 된다. 컬렉션 문서는 `retrieval-document`, 사용자 질의는 `retrieval-query`로 임베딩하는 것이 의도된 사용법이다. 문서는 미리 청크로 나눠 인덱싱하고, 질의는 사용자가 입력할 때마다 실시간으로 임베딩한다.

브라우저 안에서만 동작하는 개인 문서 검색을 만들 경우 IndexedDB나 OPFS에 문서 ID, 원문 청크, 벡터, 벡터 공간 정보를 함께 저장한다. 서버 비용과 원문 전송은 줄일 수 있지만, 브라우저 저장소 제한과 모델 업데이트 정책을 반드시 고려해야 한다.

### 5. 피드백과 상태

Embedding API explainer는 이 제안이 Chrome Built-in AI 팀의 초기 설계 스케치이며 아직 Chrome에 출시 승인된 상태가 아니라고 설명한다. 따라서 현재 문서의 API 표면은 바뀔 수 있다. 원문은 기술 문제는 Chromium issue tracker로, API 사용성 피드백은 GitHub explainer 저장소 이슈로 전달하라고 안내한다.

## 용어 정리

| 용어 | 뜻 |
| --- | --- |
| Embedding | 텍스트 의미를 숫자 벡터로 표현한 값 |
| Vector space | 벡터들이 놓이는 의미 공간 |
| `SemanticEmbedder` | Chrome Early Preview 문서의 임베딩 생성 전역 API |
| `availability()` | API와 모델 사용 가능 상태를 확인하는 메서드 |
| `create()` | 임베딩 생성 인스턴스를 만드는 메서드 |
| `embed()` | 텍스트를 임베딩 벡터로 바꾸는 메서드 |
| `destroy()` | 사용한 모델 리소스를 명시적으로 해제하는 메서드 |
| `Float32Array` | 32비트 부동소수점 숫자 배열 |
| `taskType` | 임베딩을 어떤 용도에 맞게 최적화할지 지정하는 옵션 |
| `retrieval-query` | 검색 질의를 위한 임베딩 태스크 |
| `retrieval-document` | 검색 대상 문서를 위한 임베딩 태스크 |
| Cosine similarity | 두 벡터의 방향 유사도를 측정하는 방식 |
| IndexedDB | 브라우저 안에 구조화 데이터를 저장하는 Web API |
| OPFS | Origin Private File System, 웹 앱 전용 파일 저장소 |
| Early Preview Program | 정식 출시 전 실험 API를 테스트하고 피드백하는 프로그램 |

## 실습 학습 가이드

- `01_foundations.ipynb`: 임베딩 벡터와 코사인 유사도를 표준 라이브러리만으로 직접 구현한다.
- `02_practice.ipynb`: `SemanticEmbedder`의 생명주기와 `taskType` 차이를 Python 모의 객체로 학습한다.
- `03_advanced.ipynb`: 로컬 문서 검색 인덱스, 질의-문서 태스크 분리, 벡터 공간 버전 검사를 실습한다.
- `semantic_embedder_demo.html`: Chrome Canary와 플래그가 준비된 환경에서 실제 `SemanticEmbedder`를 호출해 보는 브라우저 데모다.

노트북은 외부 패키지를 사용하지 않는다. Jupyter 실행 환경만 있으면 된다. HTML 데모는 Chrome Canary, 데스크톱 환경, `chrome://flags/#semantic-embedder-api` 설정이 필요하다.

## 다음 학습 경로

1. 임베딩 기초: bag-of-words, TF-IDF, neural embedding의 차이를 비교한다.
2. 벡터 검색: 코사인 유사도, top-k 검색, approximate nearest neighbor를 학습한다.
3. 브라우저 저장소: IndexedDB와 OPFS에 벡터 인덱스를 저장하는 방식을 실험한다.
4. 모델 버전 관리: 브라우저 업데이트나 모델 교체 시 인덱스를 무효화하고 재생성하는 정책을 설계한다.
5. 제품 적용: 개인정보가 강한 메모 앱, 로컬 지식 검색, 브라우저 확장, 오프라인 문서 추천 같은 사용 사례를 만든다.
6. 책임 있는 사용: 편향, 언어별 품질 차이, 민감정보 처리, 사용자가 이해할 수 있는 온디바이스 AI 안내를 함께 설계한다.
