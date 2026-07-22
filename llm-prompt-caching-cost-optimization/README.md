# LLM 비용 64% 절감과 캐시 히트율 98% 달성 사례

작성일: 2026-07-22

## 출처와 작업 범위

- 원문: [LLM 비용 64% 절감, 캐시 히트율 98% 달성기](https://techblog.musinsa.com/llm-%EB%B9%84%EC%9A%A9-64-%EC%A0%88%EA%B0%90-%EC%BA%90%EC%8B%9C-%ED%9E%88%ED%8A%B8%EC%9C%A8-98-%EB%8B%AC%EC%84%B1%EA%B8%B0-d568135bd40e)
- 부제: 메트릭 가시성 확보부터 Prompt Caching 도입까지
- 저자: 정다해, 29CM Pricing 팀
- 게시일: 2026-07-07
- 원문 언어: 한국어
- 확인일: 2026-07-22
- 학습용 재구성본: [translation.ko.md](translation.ko.md)
- 추가 검증: [Amazon Bedrock Prompt Caching 공식 문서](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html), [LangChain4j PR #4920](https://github.com/langchain4j/langchain4j/pull/4920)

원문은 Medium 기반 페이지로 일반 텍스트 추출에서는 로그인 셸만 확인됐지만, 렌더링된 `article` 본문 전체를 직접 확인했습니다. 이 자료는 글의 구조와 수치를 보존해 분석하되 원문을 그대로 복제하지 않고 학습 관점으로 재구성합니다.

## 한눈에 보기

29CM는 AWS Bedrock 기반 LLM을 상품 속성 추출, 그룹 평가, 고객 응대 등에 사용했습니다. 비용이 증가했지만 Bedrock 콘솔의 일별 합계만으로는 어느 API가 비용을 만드는지 알 수 없었습니다.

팀은 다음 순서로 문제를 해결했습니다.

```text
API별 토큰·지연·오류 메트릭 구축
  → 전체 토큰의 약 92%를 쓰는 속성 추출 API 발견
  → 요청마다 동일한 15K system prompt 재처리 확인
  → 고정 prefix와 2K 내외의 변동 상품 데이터 분리
  → 1시간 Bedrock Prompt Caching 적용
  → 1주 실측: cache hit 98%, 전체 LLM 청구액 64% 감소
```

가장 중요한 교훈은 “캐시 기능부터 켜라”가 아닙니다. **비용을 endpoint와 token type으로 분해해 병목을 찾고, 고정 prefix를 안정화한 뒤, cache hit와 금액을 함께 검증하라**는 운영 방법론입니다.

## 기초 개념

### 토큰 비용 구조

Prompt caching 전에는 대체로 입력 토큰과 출력 토큰에 각 단가를 곱합니다.

```text
비용 = input_tokens × input_price + output_tokens × output_price
```

캐싱 후에는 입력을 세 종류로 나눠야 합니다.

- `input`: 캐시에서 읽거나 쓰지 않은 일반 입력
- `cache_write`: 새 prefix를 캐시에 적재한 토큰
- `cache_read`: 기존 prefix를 재사용한 토큰

```text
비용 = input × 일반 입력 단가
     + cache_write × 캐시 쓰기 단가
     + cache_read × 캐시 읽기 단가
     + output × 출력 단가
```

모델마다 단가, 최소 cache checkpoint 토큰, 지원 TTL과 checkpoint 수가 다르므로 코드에 고정하지 말고 버전이 관리되는 설정으로 둬야 합니다.

### Prefix caching

Prompt caching은 요청 앞부분의 동일한 token prefix를 재사용합니다. 앞부분이 한 글자라도 달라지면 그 뒤의 cache도 무효화될 수 있습니다.

```text
[tools: 고정] → [system: 고정] → cache point → [messages: 변동]
```

AWS Bedrock 공식 문서상 checkpoint 처리 순서는 `tools → system → messages`입니다. 앞 section이 바뀌면 뒤 section의 cache가 무효화되므로 낮은 변경 빈도의 콘텐츠를 앞에 두는 것이 기본입니다.

### Cache hit rate

글의 98% hit rate는 연속 배치 호출에서 첫 write 이후 대부분 요청이 read였음을 뜻합니다. 그러나 request 기준 hit rate와 token 기준 hit rate는 다를 수 있습니다.

```text
request hit rate = cache hit 요청 수 / cache 대상 요청 수
token hit rate   = cache_read 토큰 / (cache_read + cache_write 토큰)
```

운영에서는 두 값과 실제 비용을 함께 봐야 합니다.

### TTL

TTL은 cache entry의 유효 시간입니다. AWS 문서에 따르면 성공한 hit마다 TTL이 다시 시작됩니다. 요청 간격이 TTL보다 짧게 이어지는 배치에서는 첫 write 뒤 cache가 계속 유지됩니다.

2026-07-22 기준 5분과 1시간 지원 여부는 모델별로 다릅니다. 지원하지 않는 모델에 1시간을 가정하면 안 됩니다.

## 핵심 요약

### 1. 비용보다 가시성이 먼저였다

초기에는 다음 질문에 답할 수 없었습니다.

- 어떤 endpoint가 토큰을 가장 많이 쓰는가?
- input, output, cache read, cache write 비중은 얼마인가?
- 시간대별 호출량과 latency, error는 어떻게 변하는가?

팀은 LangChain4j `ChatModelListener`에서 endpoint, model, token type을 tag로 갖는 Prometheus metric을 만들었습니다. 요청 경로는 servlet filter가 `ThreadLocal`에 넣고, cardinality 폭발을 막기 위해 allowlist 밖 경로는 `other`로 묶었습니다.

### 2. 비용 병목은 단일 API였다

속성 추출 API가 전체 LLM 토큰의 약 92%를 사용했습니다. 한 요청은 대략 다음 구조였습니다.

- 반복되는 system prompt: 약 15K token
- 상품 최대 100개의 변동 데이터: 약 2K token
- 오전 7시부터 오후 2시까지 카테고리별 고빈도 batch

Prompt가 크다는 사실보다 **큰 고정 prompt가 높은 빈도로 반복됐다**는 결합이 핵심 원인이었습니다.

### 3. 최적화 선택은 실측 기반 비용 모델로 했다

LLM에는 codebase에서 호출 패턴과 시나리오를 추출하는 일을 맡겼지만 최종 산술은 맡기지 않았습니다. Grafana 실제 token과 model별 가격표로 결정론적으로 계산하고 Bedrock console과 대조했습니다.

Prompt caching이 첫 선택이 된 이유는 다음과 같습니다.

- 모델 출력 정확도에 영향을 주지 않음
- 코드 변경과 검증 범위가 작음
- 긴 동일 prefix와 연속 호출이라는 workload가 가격 모델에 적합함
- 예측 절감 효과가 충분히 큼

### 4. 캐시 적용 전에 prompt 구조를 바꿨다

- 규칙, 예시, 금지 항목, JSON schema 같은 고정값을 system prompt로 이동
- 상품명, category ID 같은 변동값을 user message로 이동
- 고정 system block 뒤에 cache point 배치

Cache marker 한 줄만 추가하고 dynamic value가 prefix에 남으면 hit rate는 올라가지 않습니다.

### 5. 1주 실측으로 효과를 확인했다

- cache hit rate: 98%
- 전체 LLM 청구액: 64% 감소
- 대상 API만이 아니라 전체 청구액 기준
- simulation과 실측 hit rate 차이: 1%p

단일 API가 전체 토큰의 약 92%였기 때문에 그 API의 입력 비용을 낮추자 전체 비용도 크게 감소했습니다.

## 상세 정리

### 메트릭 설계

예시 metric label은 다음과 같습니다.

| Label | 역할 | 주의점 |
|---|---|---|
| `llm_endpoint` | 비용 귀속 API | raw URL이나 ID를 쓰지 말고 route template allowlist 사용 |
| `llm_model` | model별 단가·성능 비교 | alias보다 실제 model ID 권장 |
| `type` | input/output/cache_read/cache_write | 전체 입력 계산식과 중복 집계 주의 |

함께 수집할 metric:

- token counter
- request count
- latency histogram
- error count와 status/reason
- cache hit request count
- prompt template/version

비용 단가는 application code가 아니라 Grafana 변수나 versioned pricing configuration으로 분리합니다. 단가 변경 때문에 서비스를 재배포하지 않고 과거 metric에도 새 계산식을 시험할 수 있습니다.

### Bedrock token usage 해석

AWS 공식 문서상 caching이 켜진 응답에서 총 입력은 다음처럼 계산합니다.

```text
total input = inputTokens + cacheReadInputTokens + cacheWriteInputTokens
```

`inputTokens`만 그래프로 그리면 cache 적용 전후 traffic 자체가 줄어든 것으로 오해할 수 있습니다. 총 처리량과 청구 종류를 별도 panel로 보여 줘야 합니다.

### Cache warming

대량 병렬 요청을 동시에 보내면 첫 요청의 cache write가 끝나기 전에 나머지가 모두 miss가 될 수 있습니다. 작은 warming request를 먼저 보내 write 완료를 확인한 뒤 batch를 여는 방식이 유효합니다.

안전한 순서:

1. 대표적인 고정 prefix로 warming 호출
2. 응답의 `cacheWriteInputTokens` 확인
3. 다음 호출에서 `cacheReadInputTokens > 0` 확인
4. worker concurrency 개방

### Relocation trick

다음 dynamic value가 system prefix에 숨어 있으면 user message나 cache point 뒤로 옮깁니다.

- timestamp와 request ID
- user ID, session ID
- 매 요청 달라지는 category ID
- 비결정적 순서의 JSON
- 변하는 tool definition 순서

단순 문자열 placeholder도 값이 매번 다르면 prefix는 달라집니다. “placeholder를 썼다”가 아니라 최종 직렬화 byte/token sequence가 같은지 확인해야 합니다.

### 대표 안티패턴

| 안티패턴 | 증상 | 대응 |
|---|---|---|
| system prompt의 timestamp | 매 요청 miss | dynamic message로 이동 |
| 사용자별 system prefix | 사용자마다 별도 cache | 공통 지시와 사용자 context 분리 |
| JSON key 순서 비결정적 | 의미는 같아도 hash 불일치 | stable serializer와 key sort |
| tool 순서 변경 | 뒤 cache 전체 무효화 | stable ordering과 versioning |
| 병렬 cold start | batch 첫 구간 miss 폭증 | warming 후 worker 시작 |
| 최소 token 미달 | 오류 없이 cache read 0 | model card의 최소값 검사 |
| 긴 TTL 무조건 사용 | write premium 낭비 가능 | 호출 간격과 가격으로 선택 |

### LangChain4j 상태 보정

글 작성 당시 설명은 1시간 TTL 지원 PR이 main에 merge됐고 다음 release를 기다리는 상태였습니다. 현재 확인 결과 PR #4920은 2026-04-20 merge된 것이 맞습니다. 실제 배포 artifact에 포함됐는지는 사용하는 LangChain4j version의 release note와 API를 확인해야 하며, “main에 있다”와 “현재 dependency에서 쓸 수 있다”를 구분해야 합니다.

### 비용 절감이 항상 같은 비율로 나오지 않는 이유

64%는 특정 workload의 실측 결과이지 보편 상수가 아닙니다. 절감률은 다음 변수에 따라 달라집니다.

- 전체 비용에서 target endpoint가 차지하는 비중
- 입력 대비 출력 비용 비중
- 고정 prefix와 dynamic suffix의 token 비율
- cache read/write/normal input 단가
- hit rate와 TTL 만료 빈도
- batch concurrency와 warming 성공률
- model별 최소 cache token과 지원 section

## 운영 적용 체크리스트

- [ ] endpoint·model·token type별 metric이 있는가?
- [ ] route label cardinality가 제한되는가?
- [ ] 비용 상위 endpoint를 실제 token으로 찾았는가?
- [ ] 고정 prefix와 dynamic suffix가 분리됐는가?
- [ ] 최종 직렬화 결과가 요청 사이에서 안정적인가?
- [ ] model별 최소 token, TTL, checkpoint 제한을 확인했는가?
- [ ] cache warming이 필요한 concurrency 패턴인가?
- [ ] cache read/write와 request/token hit rate를 모니터링하는가?
- [ ] 비용 simulation을 결정론적 계산으로 검증했는가?
- [ ] 품질, latency, error rate도 함께 비교했는가?
- [ ] prompt에 개인정보·secret이 포함되는지 검토했는가?
- [ ] library main 상태가 아니라 실제 사용 version을 확인했는가?

## 용어 정리

| 용어 | 의미 |
|---|---|
| Prompt Caching | 동일한 prompt prefix의 계산 결과를 재사용하는 기능 |
| KV cache | attention의 key/value 중간 계산을 보관한 cache |
| cache point/checkpoint | cache할 prefix 경계를 지정하는 marker |
| cache write | 새 prefix 계산 결과를 cache에 적재하는 처리 |
| cache read | 저장된 prefix 계산을 재사용하는 처리 |
| TTL | 마지막 성공 hit 이후 cache가 유지되는 시간 |
| hit rate | cache 대상 중 실제 read 재사용에 성공한 비율 |
| cache warming | 병렬 workload 전 cache를 미리 채우는 호출 |
| cardinality | metric label 조합의 고유 값 개수 |
| deterministic pricing | LLM 산술이 아니라 token과 단가로 재현 가능하게 계산한 비용 |

## 실습 학습 가이드

1. [`01_foundations.ipynb`](01_foundations.ipynb): input/output/cache read/write를 분리한 비용 모델과 절감률을 계산합니다.
2. [`02_practice.ipynb`](02_practice.ipynb): dynamic prefix, JSON key 순서, tool 순서가 cache key를 깨는지 실험합니다.
3. [`03_advanced.ipynb`](03_advanced.ipynb): TTL, 요청 간격, 병렬 cold start와 warming이 hit rate에 미치는 영향을 simulation합니다.

모든 notebook은 Python 표준 라이브러리만 사용하며 실제 AWS 요청이나 비용을 발생시키지 않습니다.

## 다음 학습 경로

1. 실제 LLM client listener에서 token usage를 endpoint별로 수집합니다.
2. 상위 비용 endpoint 하나를 골라 prompt의 고정/변동 token을 측정합니다.
3. model별 현재 pricing과 cache 조건을 versioned config로 만듭니다.
4. shadow 또는 소량 traffic에서 cache write/read metric을 검증합니다.
5. warming 유무와 concurrency별 hit rate, latency, 비용을 비교합니다.
6. Prompt caching 다음으로 response/semantic cache, model downsizing, batch inference를 독립적으로 평가합니다.

## 현재성 주의

AWS 지원 모델, 가격, TTL과 최소 token은 변경될 수 있습니다. 이 문서는 2026-07-22 확인 기준이며 배포 전 [Amazon Bedrock 공식 문서](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html)와 pricing page를 다시 확인해야 합니다.
