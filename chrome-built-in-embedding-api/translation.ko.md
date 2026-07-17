# Embedding API 원문 핵심 번역 및 해설

작성일: 2026-07-17

## 번역 대상과 범위

- 대상: [Built-in AI Early Preview Program - Embedding API](https://docs.google.com/document/u/0/d/1ZB6MW8UDczm4V6ej5MorZWqFCYWwLhUs5HKxEdjP35c/mobilebasic)
- 원문 최종 업데이트: 2026-07-16
- 확인 기준일: 2026-07-17
- 범위: 원문 전체를 그대로 옮기지 않고, 학습과 구현에 필요한 핵심 구조, API 흐름, 주의사항을 한국어로 번역 및 해설한다.

## 제목

Chrome Built-in AI Early Preview Program: Embedding API

## 소개

이 문서는 Chrome Built-in AI 기능의 Early Preview Program 참여자가 새로운 Embedding API를 테스트할 수 있도록 안내한다. API와 프로그램에 대한 피드백을 받는 것이 목적이며, 최신 안내를 받으려면 Early Preview Program에 가입하라고 안내한다.

## 초기 설정과 구성

테스트를 시작하려면 최신 Chrome Canary가 필요하다. 원문 기준으로 버전은 `152.0.7943.0`보다 커야 한다. Embedding API를 사용하려면 다음 실험 플래그를 직접 활성화해야 한다.

- `chrome://flags/#semantic-embedder-api`

이 API는 현재 데스크톱 환경인 Linux, macOS, Windows에서만 지원된다.

## Embedding API의 역할

Embedding API는 텍스트 임베딩을 기기 안에서 생성할 수 있게 해 준다. 이를 통해 원문 텍스트를 서버로 보내지 않는 프라이버시 보존형 의미 이해, 낮은 지연 시간, 서버 비용 절감을 기대할 수 있다.

핵심 기능은 다음과 같다.

- `embeddinggemma-300m` 기반의 내장 모델로 임베딩을 생성한다.
- 단일 문자열과 문자열 배열 배치 입력을 지원한다.
- 결과는 `Float32Array` 값으로 반환된다.

## 기본 사용 패턴

API 사용 흐름은 다른 Chrome built-in AI API와 비슷하다.

1. `availability()`로 API와 모델이 사용 가능한지 확인한다.
2. `create()`로 인스턴스를 만든다.
3. 이 API에서는 `embed()`로 텍스트 임베딩을 생성한다.
4. 사용이 끝나면 `destroy()`로 리소스를 해제한다.

처음 사용하는 프로필에서는 모델 다운로드에 몇 초가 걸릴 수 있다. 현재 다운로드 진행률 이벤트는 구현되어 있지 않다. 따라서 `SemanticEmbedder.availability()`가 `available`을 반환하는지 확인한 다음 `SemanticEmbedder.create()`를 호출해야 한다. 그렇지 않으면 생성 호출이 실패할 수 있다.

## `taskType`으로 임베딩 품질 최적화

Embedding API는 사용 목적에 맞게 임베딩을 최적화하기 위한 `taskType` 옵션을 제공한다.

| 값 | 용도 |
| --- | --- |
| `semantic-similarity` | 두 텍스트의 의미 유사도를 평가할 때 사용한다. 검색 용도에는 맞지 않는다. |
| `retrieval-query` | 사용자의 검색 질의를 임베딩할 때 사용한다. |
| `retrieval-document` | 검색 대상 문서 컬렉션을 임베딩해 인덱싱할 때 사용한다. |
| `classification` | 감정 분석, 스팸 탐지처럼 사전 정의된 라벨로 텍스트를 분류할 때 사용한다. |
| `clustering` | 문서 조직화, 시장 조사, 이상 탐지처럼 비슷한 텍스트를 묶을 때 사용한다. |

`taskType`을 지정하지 않으면 API가 기본 태스크를 자동 선택하지 않는다. 대신 원시 문자열 입력을 그대로 임베딩한다. 따라서 검색, 분류, 유사도 비교처럼 목적이 분명한 기능에서는 `taskType`을 명시하는 편이 좋다.

## 결과 구조

`embed()` 메서드는 `EmbedderResult` 형태의 객체를 반환한다. 반환 객체 안에는 `embeddings` 배열이 있고, 각 항목은 `values` 필드를 가진다. `values`는 `Float32Array` 형태의 숫자 벡터다.

배치 입력을 넣으면 입력 문자열 개수만큼 임베딩 항목이 반환된다. 단일 문자열을 넣어도 결과는 배열 구조로 반환되므로 첫 번째 결과는 `result.embeddings[0].values`처럼 꺼낸다.

## 중요한 주의사항: 같은 공간에서 나온 벡터만 비교

임베딩은 반드시 같은 공간에서 만들어진 것끼리만 비교해야 한다. 즉 동일한 모델 버전과 동일한 벡터 공간에서 생성된 벡터만 직접 코사인 유사도 등으로 비교할 수 있다.

원문은 향후 이 관리를 단순화하는 방법을 검토 중이라고 설명한다. 현재 단계에서 개발자는 모델 버전, 차원, 태스크 설정이 달라질 가능성을 직접 고려해야 한다.

## 테스트와 피드백

원문은 다양한 사용 사례에서 API를 테스트해 달라고 요청한다. 특히 다음 항목에 관심이 있다고 밝힌다.

- 테스트 기기에서의 성능
- 유사도 태스크에서의 임베딩 품질
- API 사용 편의성과 ergonomics
- 실제로 만들거나 개선할 수 있는 애플리케이션

기술 문제나 구현 품질 문제는 Chromium issue tracker로, API 설계와 사용성 피드백은 GitHub explainer 저장소로 전달하라고 안내한다.

## FAQ 요약

Early Preview Program에서 탈퇴하려면 안내된 unsubscribe 메일 주소로 메일을 보내면 된다. 새 참여자는 가입 폼을 통해 프로그램에 들어올 수 있다. 이전 업데이트와 설문은 Context Index에서 확인할 수 있다.

## 변경 이력

2026-07-16에 첫 버전이 공개되었다. 같은 날 다운로드 진행률 이벤트가 없으며, 모델 다운로드가 완전히 끝나기 전에는 `create()` 호출이 실패할 수 있다는 설명이 추가되었다.

## 학습자 메모

- 이 API는 정식 안정 API가 아니라 Early Preview API다.
- 브라우저에 전역 객체가 없으면 플래그, Canary 버전, 데스크톱 여부를 먼저 확인한다.
- `availability()`가 `available`이 아니면 모델 다운로드나 정책 조건이 아직 충족되지 않았을 수 있다.
- 실제 제품에서는 벡터를 저장할 때 모델 공간 식별자와 생성 시점을 함께 저장해야 한다.
