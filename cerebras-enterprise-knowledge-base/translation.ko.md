# How We Built Our Knowledge Base - 한국어 번역 요약

작성일: 2026-07-30

## 원문 정보

- 제목: How We Built Our Knowledge Base
- 공식 페이지 제목: How Cerebras Built Its Enterprise Knowledge Base
- 저자: Isaac Tai, Daniel Kim, Mike Gao
- 게시일: 2026-07-15
- 원문 언어: 영어
- X Article: [Cerebras 게시물](https://x.com/cerebras/status/2077822555159945507)
- 공식 기술 블로그: [Cerebras 원문](https://www.cerebras.ai/blog/how-we-built-our-knowledge-base)
- 접근일: 2026-07-30

[학습 README로 돌아가기](README.md)

## 번역 범위

이 문서는 저작권이 있는 기술 블로그의 전문을 복제하지 않는다. 원문의 section 순서, 핵심 설계, 수치와 수식을 보존한 자연스러운 한국어 번역 요약이다. 그림은 원문에서 확인할 수 있으며 여기서는 그림이 설명하는 data flow를 텍스트로 재구성한다.

## 도입

Cerebras 직원들은 내부 지식 베이스에 매일 15,000개가 넘는 질문을 한다. 출시 약 3개월 만에 널리 사용되는 내부 도구가 됐으며 사람뿐 아니라 자동화와 agent도 이용한다.

조직의 업무는 data center operation, chip design, hardware, training, inference, cloud platform 등으로 넓다. 신규 직원이 계속 합류하면서 "자료가 어디 있는가", "이 분야의 전문가는 누구인가", "이 개념은 무엇인가"와 같은 질문이 반복됐다. Cerebras Knowledge는 사람과 system을 유용한 정보에 연결하기 위해 만들어졌다.

## 정보가 존재하는 장소에서 만나기

조직 정보는 한 platform에 있지 않다. document의 제안 수정, Slack thread, GitHub code reference, Jira status처럼 각 업무에 가장 편한 도구에서 생성된다. 모든 정보를 한 곳으로 옮기려는 single source of truth 전략은 실제로 잘 작동하지 않는다.

Cerebras는 기존 행동을 거의 바꾸지 않는 system을 목표로 했다. 사용자가 정보를 새 system에 다시 기록하게 하지 않고 각 platform에서 직접 추출한다.

## 지식 베이스의 구조

지식 베이스는 세 가지를 제공한다.

1. 내부 data를 수집·저장하는 platform
2. data를 질의하는 platform
3. 인증·인가와 audit, analytics를 강제하는 계층

중심에는 여러 source의 embedding, raw summary, metadata를 담는 하나의 PostgreSQL table이 있다. system은 회사 전체에서 계속 data를 ingest하고 즉시 query 가능한 상태를 유지한다.

source마다 data 정의, 연결 방법, fetch 주기를 기술한다. Slack thread, code repository, document system, custom database에서 온 row도 같은 interface를 따른다. 따라서 공통 table에 들어온 data는 같은 query interface에서 검색할 수 있다.

## Slack

Slack은 최신 engineering discussion이 일어나는 가장 중요한 source였다. raw text를 그대로 embedding하는 방식만으로는 충분하지 않았다.

- 메시지마다 정보 밀도가 크게 다르다.
- 짧은 메시지가 긴 기술 설명보다 cosine similarity에서 높게 나올 수 있다.
- 메시지 의미가 주변 conversation에 의존한다.

그래서 한 Slack thread를 여러 검색 방식에서 동시에 찾을 수 있게 했다.

- **Full-text search**: 오류 문자열, flag, hostname 같은 정확한 token을 찾는다.
- **Embedding search**: 서로 다른 표현의 질문과 답을 연결한다.
- **IDF**: 희귀 token이 포함된 짧고 중요한 메시지를 filler보다 높인다.
- **Age decay**: 관련성이 같다면 더 최근 답을 우선한다.

어떤 scorer 하나도 단독으로 신뢰하지 않는다. 각 검색 방식이 독립 순위를 만들고 query 시점에 이를 융합한다.

### Socket Mode

Slack bot은 Socket Mode에서 persistent WebSocket으로 event를 받는다. Web API를 polling하지 않아 rate limit 소비를 줄인다.

event를 받으면 즉시 acknowledge하고 stable event ID로 중복을 제거한 뒤 ingest consumer가 처리하도록 표시한다. consumer는 새 message만 저장하지 않고 그 message가 속한 thread의 parent와 모든 reply를 다시 가져와 전체 thread를 하나의 row로 upsert한다. participant, content, last activity가 항상 전체 conversation을 반영하게 하기 위해서다.

각 Slack channel은 별도 data source다. busy incident channel처럼 더 높은 freshness가 필요한 곳은 더 자주 ingest할 수 있다.

### Thread와 message

raw Slack text는 PostgreSQL GIN full-text index로 즉시 keyword 검색된다. vector search를 위해서는 LLM이 전체 thread에서 다음 구조를 추출한다.

- 실제 엔지니어가 검색할 한 줄 질문
- 짧은 summary
- resolution
- 관련 system과 code reference

이 정규화 data를 embedding해 공통 table에 저장한다. 원문 transcript는 직접 embedding하지 않는다. 저자들의 실험에서는 일관된 format으로 정규화했을 때 정확도가 크게 개선됐지만 구체적인 평가 수치는 제시하지 않는다.

### Bursting

긴 thread의 중요한 단일 message가 thread summary에서 빠지는 문제를 보완한다. 같은 author의 연속 message를 burst로 묶고 thread topic을 context로 앞에 붙여 embedding한다.

낮은 signal을 막기 위해 weighted signal이 threshold를 넘어야 한다.

- corpus IDF 4.0 이상의 비교적 희귀한 token
- burst 전체 길이 200자 이상
- reaction이 붙은 message의 social boost

조건을 통과한 burst만 thread-level row와 함께 저장한다.

## Code repository

초기에는 code embedding이 필요한지 논쟁했다. exact search에는 grep이 강하지만 대규모 codebase의 semantic search가 가진 장점을 확인한 뒤 도입했다.

일부 내부 repository는 40GB를 넘기 때문에 전체를 매번 다시 embedding하지 않는 것이 핵심이었다.

### CocoIndex로 code embedding 유지

CocoIndex를 이용해 언어별 regex boundary로 code를 큰 구조부터 작은 구조까지 재귀적으로 나눈다. 먼저 class boundary를 시도하고 너무 크면 method, 그 뒤 작은 block으로 내려간다. 한 file이 file-level과 function-level처럼 서로 다른 상세도의 embedding을 여러 개 만들 수 있다.

CocoIndex는 PostgreSQL에 sync metadata를 추적한다. commit마다 변경된 code chunk만 다시 embedding하고 export한다. repository onboarding은 팀이 제출할 수 있는 configuration file로 옮겼으며 file path allowlist와 denylist도 포함한다.

### Custom data source

기존 database를 그대로 사용하려는 팀은 작은 Python plugin을 pull request로 제출한다. plugin은 source system을 읽고 공통 embeddings table과 같은 shape의 row를 만든다.

공통 schema에 맞게 쓰기만 하면 나머지 stack은 바뀌지 않는다. custom data도 Slack, code, document와 함께 검색된다.

## Planning과 tool fan-out

모든 query는 짧은 planning pass로 시작한다. LLM이 어떤 tool과 data source가 관련될지 선택한다.

- `subsystem_index`: file별 LLM summary
- `search`: 여러 source의 unified vector pipeline
- `search_slack`: Slack 직접 검색
- `search_code`: repository에 대한 ripgrep
- `recent_prs`: 관련 최근 pull request
- `who_knows`: 특정 주제에 대한 입증된 expert

planner는 index된 project, source, 각 source의 용도를 설명하는 compact catalog를 본다. query와 active scope를 바탕으로 tool을 선택하고 executor가 병렬 실행한다. 결과를 공통 evidence format으로 정규화해 최종 synthesis LLM에 전달한다.

## Reranking

query와 vocabulary가 비슷하지만 다른 질문에 답하는 문서가 상위에 올 수 있다. reranking 전에 RRF로 서로 다른 검색 목록을 합친다.

\[
\operatorname{score}(d)=\sum_l \frac{w_l}{60+\operatorname{rank}_l(d)}
\]

기본 weight는 1.0, smoothing constant는 60이다. 여러 retriever에서 높은 순위를 얻은 문서가 한 retriever에서만 1위인 문서보다 유리할 수 있다.

그 다음 중복 chunk를 source 단위로 합치고, file별 결과 수를 제한해 다양한 상위 20개를 만든다. 작은 reranker가 원 query와 각 문서의 관련성을 0-10으로 채점하고 상위 10개를 유지한다.

순위가 정해진 뒤 주변 context를 다시 붙인다. wiki section이 match되면 이웃한 두 section을 가져와 heading, precondition, caveat가 chunking 때문에 사라지지 않게 한다.

최종 search 결과는 여러 retriever의 융합, source-level deduplication, 질문 기반 reranking, 주변 context 확장을 거친 evidence packet이다.

## MCP

MCP integration은 하나의 "질문에 답하기" endpoint 뒤에 모든 것을 숨기지 않는다. `search_slack`, `search_code`, `search`, `who_knows` 같은 retrieval primitive를 직접 tool로 제공한다.

tool은 작고 구조화하며 가능한 한 LLM-free다. vector search, lexical search, ripgrep 같은 하나의 pipeline과 가벼운 heuristic을 실행해 raw evidence row를 반환한다.

Claude Code 같은 MCP-compatible agent가 orchestration engine이 된다. 어떤 tool을 어떤 순서로 호출하고 결과를 answer나 code edit로 조립할지 client가 결정한다. retrieval layer는 이 LLM decision에 의존하지 않고 독립적으로 요청을 처리한다.

## Web UI

Web UI에서도 같은 tool을 쓰지만 end-to-end query pipeline으로 연결한다.

1. **Planner**: query와 active project를 보고 retrieval tool을 선택한다.
2. **Executor**: tool을 병렬 호출하고 score, recency, source hint가 있는 공통 evidence schema로 정규화한다.
3. **Synthesis**: typed evidence bundle과 질문을 이용해 citation, caveat, cross-source synthesis가 있는 답을 만든다.

사용자에게는 단순히 질문하고 답을 받는 interface지만 내부에서는 planner, executor, synthesizer가 동작한다.

## 조직

corpus가 커지자 모든 것을 한꺼번에 검색하는 방식은 빠르게 쓸모가 없어졌다. compiler engineer에게 infrastructure runbook이 노출되는 식의 noise가 생겼다.

### Project와 scoped search

project는 query가 실행되는 workspace의 기본 단위다. 특정 Slack channel, code repository, internal database, document space를 팀이나 initiative에 맞게 묶는다.

같은 shared incident channel이나 central repository는 복사하지 않고 여러 project가 참조할 수 있다.

### Onboarding과 기본값

사용자는 onboarding 중 자신의 업무에 맞는 기본 project를 선택하거나 만든다. 이 project는 user profile에 저장되어 query 범위를 자동으로 제한한다. 신규 직원이 중요한 channel이나 repository를 모두 알지 못해도 관련성 높은 답을 얻도록 한다.

## 마무리

이 지식 베이스는 정보를 하나의 rigid system으로 옮기도록 강요하지 않고 정보가 이미 존재하는 장소에서 수집하기 때문에 작동한다. 여러 검색 방식을 결합해 증거를 빠르게 찾고, 실제 기업 data의 다양성을 수용하면서 조직 성장에도 유용한 수준의 구조를 유지한다.

## 번역 검수 메모

- 2026-07-30에 X Article과 Cerebras 공식 기술 블로그의 제목, 저자, section 순서, 수치, RRF 식을 대조했다.
- 원문의 "하루 15,000건 이상", "출시 3개월", "40GB 이상 repository", `IDF >= 4.0`, `200 characters`, RRF `k=60`, 후보 20개와 rerank 후 10개를 보존했다.
- 정확도 향상, 비용, latency, model 종류처럼 원문이 정량화하지 않은 항목은 임의로 보충하지 않았다.
- code와 figure의 의미는 설명했지만 원문 그림과 긴 code block은 복제하지 않았다.
