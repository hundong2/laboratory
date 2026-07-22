# 원문 한국어 학습용 재구성본

원문: [LLM 비용 64% 절감, 캐시 히트율 98% 달성기](https://techblog.musinsa.com/llm-%EB%B9%84%EC%9A%A9-64-%EC%A0%88%EA%B0%90-%EC%BA%90%EC%8B%9C-%ED%9E%88%ED%8A%B8%EC%9C%A8-98-%EB%8B%AC%EC%84%B1%EA%B8%B0-d568135bd40e)

- 원문 언어: 한국어
- 저자: 정다해
- 게시일: 2026-07-07
- 확인일: 2026-07-22

원문이 한국어이므로 이 파일은 직역본이 아니라 원문의 섹션 흐름, 수치와 기술적 의미를 보존한 교정·학습용 재구성본입니다. 원문 이미지와 세부 표현은 링크에서 확인하세요.

## 들어가며

29CM는 상품 속성 추출, 그룹 평가, 고객 응대 등에 AWS Bedrock LLM을 사용합니다. 운영 비용은 계속 늘었지만 Bedrock console은 일별 token과 비용 합계만 보여 줘 어떤 API가 원인인지 분리하기 어려웠습니다.

팀은 먼저 metric 가시성을 만들고 비용 원인을 찾은 다음 Prompt Caching을 적용했습니다. 모든 최적화 뒤 1주 측정에서 전체 LLM 청구액은 64% 줄었고 cache hit rate는 98%였습니다.

## 1. 문제 정의: 비용은 보이지만 원인은 보이지 않았다

초기 정보는 일별 input/output token과 비용 합계, 그리고 어떤 API가 LLM을 부르는지에 대한 code 수준 추정뿐이었습니다. 다음을 알 수 없었습니다.

- token 사용량 상위 API
- input, output, cache read, cache write 비중
- 시간대별 호출량과 분포

따라서 첫 문제는 비용 자체가 아니라 가시성이었습니다.

## 2. API별 token metric dashboard

Bedrock 호출별로 다음 metric을 추적했습니다.

- API별 input/output/cache read/cache write token
- API별 request count, response time, error count

LangChain4j `ChatModelListener`에서 응답 metadata의 model name과 token usage를 읽어 Prometheus counter를 증가시켰습니다. Servlet filter가 현재 endpoint를 `ThreadLocal`에 넣어 LLM 호출과 연결했습니다.

Metric label 폭증을 막기 위해 승인한 route만 이름을 남기고 그 밖의 경로는 `other`로 묶었습니다. 비용 계산은 code에서 분리해 Grafana의 token 단가 변수로 처리했습니다.

## 3. 단일 API가 token 대부분을 사용

Dashboard를 endpoint별로 나누자 속성 추출 API 하나가 전체 LLM token의 약 92%를 차지했습니다. 다른 endpoint를 모두 합쳐도 10% 미만이었습니다.

## 4. 반복되는 15K system prompt

속성 추출 API는 매일 오전 7시부터 오후 2시 사이 카테고리별 batch에서 고빈도로 호출됐습니다. 한 번에 상품 최대 약 100개, 약 2K token의 변동 데이터를 처리했습니다.

문제는 매번 약 15K token의 동일한 system prompt가 앞에 붙는 구조였습니다. 이 prompt에는 추출 규칙, 예시, 금지 항목과 output JSON schema가 들어 있었습니다.

```text
요청 = 동일 system prompt 약 15K + 변동 상품 데이터 약 2K
```

큰 prompt와 높은 호출 빈도가 결합하면서 비용 대부분을 만들었습니다.

## 5. AI 기반 비용 simulation

검토한 일반적 선택지는 Prompt Caching, model downsizing, Batch API 등이었습니다. LLM에는 repository source에서 호출 pattern과 scenario를 추출하게 했지만 최종 산술은 맡기지 않았습니다.

최종 비용은 dashboard의 실제 token에 model별 단가를 곱해 결정론적으로 계산하고 Bedrock console과 대조했습니다. Simulation은 옵션별 예상 절감률, 우선순위와 옵션 의존성을 비교하는 데 사용했습니다.

Prompt Caching을 첫 단계로 선택한 이유:

- 정확도 변화가 없어 검증 부담이 작음
- code 변경량이 작음
- 동일한 긴 prefix가 고빈도로 반복되는 workload와 잘 맞음
- 단독 예상 절감률이 충분히 큼

## 6. Prompt 구조 분리와 cache point

### 6.1 고정값과 변동값 분리

Prefix cache가 작동하려면 요청 시작 부분이 같아야 합니다.

- 고정 규칙, 지시, 예시, schema는 system prompt에 배치
- 상품명, category ID와 사용자 입력은 message prompt에 배치

이 분리가 완료된 뒤 고정 system block 뒤에 cache point를 넣었습니다.

### 6.2 Bedrock Converse API

핵심 설정은 cache point의 type과 TTL입니다.

```kotlin
val cachePoint = SystemContentBlock.builder()
    .cachePoint(
        CachePointBlock.builder()
            .type(CachePointType.DEFAULT)
            .ttl(CacheTTL.VALUE_1_H)
            .build()
    )
    .build()
```

1시간 안에 동일 prefix 호출이 이어지고 hit가 발생하면 TTL이 갱신됩니다. 이 workload는 연속 batch 특성상 1시간 TTL이 적합하다고 판단했습니다.

작업 당시 LangChain4j의 Bedrock module은 TTL 없는 cache point만 만들어 기본 5분만 사용할 수 있었습니다. 팀은 1시간 TTL을 설정하도록 PR #4920을 기여했고 main에 merge됐습니다. 2026-07-22에도 PR의 merge 상태는 확인되지만, 실제 사용자는 자신의 dependency release에 포함됐는지 별도 확인해야 합니다.

## 7. 결과

적용 뒤 1주일 측정 결과:

- cache hit rate 98%
- 전체 LLM 청구액 64% 감소
- simulation과 실측 hit rate 차이 1%p

배치 첫 호출이나 만료 뒤 첫 호출이 cache write를 수행하고, 이어지는 호출은 hit마다 TTL을 갱신하며 cache read를 사용했습니다. 속성 추출 API가 원래 전체 token의 약 92%였으므로 단일 API의 input 비용 감소가 전체 청구액 감소로 이어졌습니다.

## 8. Prompt Caching 활용 pattern

1. system prompt caching
2. tool definition caching
3. multi-turn history caching
4. RAG reference document caching
5. 병렬 요청 전 cache warming
6. system의 dynamic value를 message로 옮기는 relocation

29CM 사례는 첫 번째 pattern을 사용했습니다. 병렬 workload는 첫 write 전 다른 요청이 동시에 miss하지 않도록 warming call이 유용합니다. Timestamp, request ID 같은 값이 system에 있다면 message로 옮겨 cache key를 안정화합니다.

## 9. Cache를 깨뜨리는 anti-pattern

- system prompt에 timestamp나 user ID 포함
- JSON key 순서가 매번 달라짐
- 첫 cache write 전에 병렬 요청 동시 발사
- tool definition 순서 변경
- model별 최소 cache token 미달

공통 원칙은 변경이 적은 콘텐츠를 앞에, 변경이 잦은 콘텐츠를 뒤에 배치하는 것입니다.

## 10. 다음 단계

Prompt caching은 첫 번째 비용 절감 lever입니다. 호출 결과 자체의 caching, model downsizing, Batch API 같은 단계를 누적할 수 있습니다. 원문의 simulation에서는 다섯 단계를 모두 적용하면 90% 이상 절감 가능성을 예상했지만, 이는 예측이므로 각 단계마다 실제 metric으로 검증해야 합니다.

## 11. 마무리

네 가지 교훈으로 정리할 수 있습니다.

1. Endpoint와 token type별 가시성을 먼저 만든다.
2. Prompt caching 전에 고정 system과 변동 message를 분리한다.
3. Cache read/write와 hit rate를 반드시 monitoring한다.
4. LLM은 scenario 발굴에 사용하고 비용 산술은 결정론적으로 검증한다.

## 확인 기준일 보정

AWS 공식 문서상 cache checkpoint의 최소 token, 최대 개수와 TTL은 model별로 다릅니다. 성공한 cache hit는 TTL을 갱신하며 1시간 TTL은 일부 model에서만 지원됩니다. 또한 cache read/write token이 도입되면 총 입력은 `input + cache_read + cache_write`로 계산해야 합니다. 배포 시점의 공식 model card와 pricing을 다시 확인하세요.
