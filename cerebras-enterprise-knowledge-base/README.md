# Cerebras 엔터프라이즈 지식 베이스 구축

작성일: 2026-07-30

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [전체 아키텍처](#전체-아키텍처)
- [데이터 수집과 공통 스키마](#데이터-수집과-공통-스키마)
- [Slack 처리](#slack-처리)
- [코드와 사용자 정의 데이터 소스](#코드와-사용자-정의-데이터-소스)
- [질의·융합·재정렬](#질의융합재정렬)
- [MCP와 Web UI](#mcp와-web-ui)
- [조직·권한·운영](#조직권한운영)
- [비판적으로 읽기](#비판적으로-읽기)
- [구축 체크리스트](#구축-체크리스트)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 사용자 제공 공유 링크: [Google 공유 링크](https://share.google/Z2Kfbyw2N1VYkj3HX)
- 확인된 최종 X 게시물: [Cerebras - How we built our knowledge base](https://x.com/cerebras/status/2077822555159945507)
- 공식 기술 블로그: [How We Built Our Knowledge Base](https://www.cerebras.ai/blog/how-we-built-our-knowledge-base)
- 저자: Isaac Tai, Daniel Kim, Mike Gao
- 공식 글 게시일: 2026-07-15
- X 게시일: 2026-07-16
- 원문 언어: 영어
- 확인일: 2026-07-30
- 접근 범위: X Article 전체와 동일 내용을 제공하는 Cerebras 공식 기술 블로그 전체

저작권이 있는 기술 블로그를 전문 복제하지 않고 원문의 구조, 수치, 수식과 기술 선택을 보존한 한국어 번역 요약을 [translation.ko.md](translation.ko.md)에 제공한다.

## 한눈에 보기

Cerebras Knowledge는 사내 정보를 한 도구로 강제 이동하지 않는다. Slack, wiki, code repository, incident, custom database처럼 정보가 원래 생성되는 장소에서 직접 수집하고 공통 증거 스키마로 연결한다.

공식 글 기준 출시 약 3개월 뒤 하루 15,000건 이상 질문을 처리하며 사람, 자동화, agent가 함께 사용했다. 이 수치는 2026-07-15 시점의 운영 현황이며 현재 수치로 일반화하면 안 된다.

```text
Slack / Wiki / Code / Incidents / Custom DB
              |
      connector + distillation
              |
  PostgreSQL 공통 embeddings table
  raw summary + vector + metadata + ACL
              |
  lexical / vector / IDF / recency / code grep
              |
       RRF -> dedup -> reranker
              |
  context expansion -> evidence packet
              |
    MCP client 또는 Web UI synthesis
```

핵심 교훈은 하나의 검색 방식이나 하나의 "single source of truth"를 믿지 않는 것이다. 여러 retriever의 약점을 서로 보완하고, 최종 답보다 인용 가능한 evidence packet을 먼저 만든다.

## 기초 개념

### Enterprise RAG

사내 문서와 대화를 검색해 LLM 답변의 근거로 제공하는 시스템이다. 일반적인 데모와 달리 실제 운영에서는 접근 권한, 삭제·수정 전파, 최신성, 중복, 감사 기록이 검색 정확도만큼 중요하다.

### Lexical search와 semantic search

- lexical search는 오류 문자열, flag, hostname처럼 정확한 token 일치에 강하다.
- semantic search는 서로 다른 표현의 질문과 답을 연결하는 데 강하다.
- 어느 하나만 사용하면 exact identifier를 놓치거나 의미 없는 짧은 문장이 상위에 오는 문제가 생긴다.

### Retrieval fusion과 reranking

retrieval fusion은 서로 점수 체계가 다른 여러 순위 목록을 하나로 합친다. reranking은 합쳐진 소수 후보를 실제 질문과 다시 비교해 정밀한 순서를 만든다.

### Evidence-first architecture

검색 계층은 최종 답을 직접 만들기보다 source ID, timestamp, score, recency, 주변 문맥을 포함한 증거를 반환한다. Web UI나 MCP client가 이를 이용해 인용과 caveat가 있는 답을 조립한다.

## 전체 아키텍처

### 세 가지 책임

1. 내부 데이터를 수집하고 저장하는 platform
2. 저장된 데이터를 질의하는 platform
3. 인증·인가, 감사, analytics를 강제하는 계층

핵심 저장소는 여러 source의 embedding, 정규화된 summary, metadata를 담는 단일 PostgreSQL table이다. 공식 그림은 pgvector의 3,072차원 vector와 HNSW index를 나타내지만 embedding model 이름과 정확한 database schema는 공개하지 않는다.

### 설계 원칙

- 기존 업무 행동을 바꾸지 않는다.
- source마다 connector는 다르지만 출력 row interface는 같게 만든다.
- 저장된 모든 row는 동일한 query surface에서 즉시 검색할 수 있게 한다.
- retrieval primitive는 작고 구조화하며 가능한 한 LLM에 의존하지 않는다.
- 조직 전체를 한 번에 검색하지 않고 project scope를 기본값으로 둔다.

## 데이터 수집과 공통 스키마

각 data source는 다음을 정의한다.

- 무엇을 수집할지
- 어떻게 인증하고 연결할지
- 어느 주기로 동기화할지
- 원문을 어떤 검색 단위로 나눌지
- 공통 schema의 metadata와 ACL을 어떻게 채울지

실제 구현을 위한 최소 schema 예:

| 필드 | 목적 |
|---|---|
| `source_type` | Slack, wiki, code, incident, custom DB 구분 |
| `source_id` | 원문과 연결되는 안정적인 식별자 |
| `document` | 검색을 위해 정규화된 본문 |
| `raw_summary` | 사람이 빠르게 읽을 요약 |
| `embedding` | semantic retrieval용 vector |
| `metadata` | channel, repository, author, path, timestamp |
| `project_ids` | 허용된 query scope |
| `acl_principals` | 사용자·그룹 권한 |
| `source_updated_at` | freshness와 삭제 전파 판단 기준 |
| `ingested_at` | pipeline 지연 관측 기준 |

원문은 단일 table을 강조하지만, production에서는 source 원본 상태, sync cursor, tombstone, job 상태를 별도 table로 분리하는 편이 안전하다.

## Slack 처리

### 왜 raw embedding만으로 부족했는가

- 짧은 동의 문장과 긴 기술 설명의 정보 밀도가 크게 다르다.
- 짧은 문장이 cosine similarity에서 긴 해설보다 유리할 수 있다.
- 메시지 의미가 thread의 앞뒤 대화에 의존한다.
- 정확한 오류 문자열은 semantic similarity보다 lexical match가 중요하다.
- 오래된 답은 이미 폐기된 infrastructure를 설명할 수 있다.

그래서 full-text, embedding, IDF, age decay를 함께 사용한다.

### 실시간 수집

Slack bot을 Socket Mode로 실행해 WebSocket event를 받는다. event를 즉시 acknowledge하고 안정적인 event ID로 deduplicate한 뒤 ingest consumer에 전달한다.

새 reply만 독립 저장하지 않는다. parent와 모든 reply를 다시 가져와 thread 전체를 하나의 row로 upsert한다. 이 방식은 participant와 last-activity를 일관되게 만들지만 긴 thread 재수집 비용, edit/delete event, API failure에 대한 별도 처리가 필요하다.

channel마다 독립 data source를 두어 incident channel과 일반 channel의 freshness 요구를 다르게 설정한다.

### Thread distillation

raw content에는 PostgreSQL GIN full-text index를 적용한다. vector retrieval용으로는 LLM이 thread 전체에서 다음을 추출한다.

- 엔지니어가 실제 검색할 한 줄 질문
- 짧은 summary
- resolution
- 언급된 system과 code reference

원문 transcript 자체를 embedding하지 않고 이 정규화 artifact를 embedding한다. 저자들은 정확도가 유의미하게 개선됐다고 보고하지만 평가 세트, metric, 절대 수치는 공개하지 않는다.

### Bursting

thread summary에서 빠지는 중요한 tangent를 찾기 위해 같은 작성자의 연속 메시지를 하나의 burst로 묶는다. thread topic을 앞에 붙여 context를 제공한 뒤 다음 signal의 가중 조합이 threshold를 넘는 burst만 embedding한다.

- corpus IDF 4.0 이상의 희귀 token
- 합친 길이 200자 이상
- reaction이 있는 메시지의 social boost

이 기준은 Cerebras 데이터에 맞춘 heuristic이다. 다른 조직에서는 언어, 메시지 길이, reaction 문화에 맞춰 다시 보정해야 한다.

## 코드와 사용자 정의 데이터 소스

### 코드 repository

Cerebras는 CocoIndex를 이용해 code embedding을 유지한다. 언어별 regex 경계를 큰 단위에서 작은 단위로 적용한다.

```text
class
  -> 너무 크면 method
       -> 너무 크면 block
```

같은 file에서 file-level, function-level 등 여러 specificity의 vector가 생길 수 있다. sync metadata와 vector store가 모두 PostgreSQL에 있어 commit마다 변경된 chunk만 다시 embedding한다. 대형 repository는 allowlist와 denylist를 configuration file로 관리하고 team이 직접 onboarding한다.

semantic code search는 `ripgrep`을 대체하지 않는다. exact symbol과 오류 문자열에는 lexical search를, 자연어 질문과 code concept 연결에는 embedding을 사용한다.

### 사용자 정의 source

팀이 작은 Python plugin을 pull request로 제출한다. plugin은 기존 system을 읽고 공통 embedding row shape를 출력한다. 이후 query stack은 source별 특별 처리를 하지 않는다.

운영 환경에서는 plugin의 secret 접근, network egress, resource limit, schema validation, code review와 sandboxing이 필수다.

## 질의·융합·재정렬

### Planner와 tool fan-out

가벼운 LLM planner가 query, active project, index catalog를 보고 필요한 tool을 선택한다.

| 도구 | 역할 |
|---|---|
| `subsystem_index` | file별 LLM summary |
| `search` | Slack, wiki, code 등의 unified vector pipeline |
| `search_slack` | Slack 직접 검색 |
| `search_code` | source repository에 대한 ripgrep |
| `recent_prs` | 관련된 최근 pull request |
| `who_knows` | 주제별로 입증된 expert 탐색 |

executor는 선택된 tool을 병렬 호출하고 결과를 공통 evidence schema로 정규화한다.

### RRF

서로 다른 retriever의 score는 직접 비교하기 어렵다. Reciprocal Rank Fusion(RRF)은 각 목록의 rank만 사용한다.

\[
\operatorname{score}(d)=\sum_l \frac{w_l}{60+\operatorname{rank}_l(d)}
\]

원문의 기본 weight는 1.0, smoothing constant는 60이다. 여러 retriever에서 꾸준히 높은 문서는 한 목록에서만 1위인 문서보다 유리해질 수 있다.

### Dedup, rerank, context expansion

1. 같은 source의 중복 chunk를 합친다.
2. 한 file이 지나치게 많은 slot을 차지하지 않도록 cap을 둔다.
3. 다양한 상위 20개를 만든다.
4. 작은 reranker가 query-document 관련성을 0-10으로 채점한다.
5. 상위 10개만 남긴다.
6. wiki section의 앞뒤 두 section처럼 주변 context를 다시 붙인다.

최종 검색 출력은 여러 retriever에서 융합되고 source 단위로 deduplicate되며 질문에 맞게 rerank된 뒤 주변 맥락이 확장된 evidence packet이다.

## MCP와 Web UI

### MCP

MCP에서는 `search_slack`, `search_code`, `search`, `who_knows` 같은 retrieval primitive를 직접 tool로 노출한다. 입력과 출력은 좁고 구조화하며, tool 자체는 가능한 한 LLM-free로 유지한다.

Claude Code 같은 MCP client가 어떤 tool을 어떤 순서로 호출하고 결과를 답이나 code edit로 조립할지 결정한다. retrieval layer는 특정 agent의 orchestration 정책에 묶이지 않는다.

### Web UI

Web UI는 같은 tool을 end-to-end pipeline으로 묶는다.

1. **Planner**: query와 project를 보고 tool을 선택한다.
2. **Executor**: tool을 병렬 실행하고 score, recency, source hint가 있는 evidence로 정규화한다.
3. **Synthesis**: 질문과 evidence bundle로 인용, caveat, cross-source synthesis가 있는 답을 만든다.

## 조직·권한·운영

### Project scope

전체 corpus 검색은 곧 noise가 된다. project는 특정 Slack channel, repository, database, document space를 묶은 이름 있는 query scope다. 같은 source는 복사 없이 여러 project에서 참조할 수 있다.

onboarding 시 기본 project를 선택하고 user profile에 저장해 새 구성원도 관련성 높은 범위에서 바로 검색하게 한다.

### 반드시 보강할 production control

- source ACL을 row와 chunk까지 전파하고 query 전에 filter한다.
- 답 생성 뒤가 아니라 retrieval 전에 권한을 적용한다.
- membership 변경, 문서 삭제, Slack edit/delete를 빠르게 반영한다.
- source와 answer에 대한 audit log를 남긴다.
- prompt injection이 document에서 planner instruction으로 승격되지 않게 분리한다.
- PII, secret, credential을 index 전에 탐지한다.
- custom connector를 최소 권한 service account로 실행한다.
- stale document와 conflicting evidence를 answer에 표시한다.

## 비판적으로 읽기

1. **정확도 수치가 없다.** thread normalization의 개선을 보고하지만 benchmark, metric, baseline과 절대값은 공개하지 않는다.
2. **latency와 비용이 없다.** 15,000 query/day는 adoption 지표이지 p95 latency, token cost, indexing cost가 아니다.
3. **모델 세부정보가 제한적이다.** embedding, distillation, planner, reranker, synthesis model의 이름과 version이 없다.
4. **권한 구현이 추상적이다.** 인증·인가·audit을 제공한다고 설명하지만 ACL schema와 cache invalidation은 공개하지 않는다.
5. **단일 PostgreSQL의 경계가 없다.** 데이터 규모, vector 수, partitioning, replica, vacuum, HNSW build와 장애 복구 전략이 없다.
6. **heuristic의 이식성이 낮다.** IDF 4.0, 200자, reaction signal은 조직 문화와 언어에 따라 다시 측정해야 한다.
7. **LLM distillation의 손실 가능성이 있다.** summary에 빠진 정보는 burst로 보완하지만 hallucination, 부정 표현 손실, attribution 오류 평가가 필요하다.
8. **보안 위협 분석이 부족하다.** poisoned document, indirect prompt injection, secret leakage, expert ranking의 privacy 문제를 별도 검증해야 한다.

## 구축 체크리스트

### 최소 기능

- [ ] source마다 stable ID, updated time, ACL을 정의한다.
- [ ] raw lexical index와 normalized semantic index를 함께 만든다.
- [ ] edit, delete, permission change를 idempotent하게 처리한다.
- [ ] retrieval 결과를 공통 evidence schema로 정규화한다.
- [ ] RRF와 reranker를 offline evaluation으로 비교한다.
- [ ] citation이 원 source와 정확히 연결되는지 확인한다.

### 운영

- [ ] ingest lag, query latency, no-result rate, stale-hit rate를 측정한다.
- [ ] Recall@K, nDCG, MRR와 answer faithfulness를 분리 측정한다.
- [ ] source별 freshness SLO와 재시도 queue를 둔다.
- [ ] ACL 회귀 테스트와 삭제 전파 테스트를 자동화한다.
- [ ] connector와 LLM prompt/version을 추적한다.
- [ ] feedback을 인기 순위가 아닌 평가용 label로 안전하게 사용한다.

## 용어 정리

| 용어 | 설명 |
|---|---|
| GIN | PostgreSQL full-text 검색에서 inverted index를 제공하는 index 방식 |
| pgvector | PostgreSQL에서 vector type과 유사도 검색을 제공하는 extension |
| HNSW | 근사 최근접 이웃 검색을 위한 graph 기반 index |
| IDF | corpus에서 희귀한 token에 더 큰 가중치를 주는 통계 |
| RRF | 여러 순위 목록을 rank 기반 reciprocal score로 합치는 방법 |
| distillation | 여기서는 raw thread를 검색 가능한 구조화 artifact로 변환하는 LLM 처리 |
| burst | 같은 작성자의 연속 메시지를 묶은 검색 단위 |
| reranker | 후보 문서를 query와 정밀 비교해 다시 순위를 매기는 model |
| evidence packet | source, score, recency, context를 포함한 정규화된 검색 결과 |
| tombstone | 삭제된 source가 index에서 다시 살아나지 않도록 남기는 삭제 표식 |

## 실습 학습 가이드

모든 notebook은 Python 표준 라이브러리만 사용하며 Cerebras 내부 system을 재현했다고 주장하지 않는 toy implementation이다.

1. [01_foundations.ipynb](01_foundations.ipynb): lexical, semantic, recency 순위와 RRF
2. [02_practice.ipynb](02_practice.ipynb): Slack thread distillation, burst, idempotent upsert
3. [03_advanced.ipynb](03_advanced.ipynb): project ACL, planner fan-out, reranking, citation 검사

## 다음 학습 경로

1. 첫 notebook에서 retriever마다 다른 강점을 만든 뒤 RRF의 \(k\)와 weight를 조정한다.
2. 두 번째 notebook에서 edit와 delete event를 추가해 source-of-truth 동기화를 연습한다.
3. 세 번째 notebook에서 권한이 없는 문서가 retrieval과 synthesis 어디에도 나타나지 않는지 공격적으로 테스트한다.
4. 실제 corpus에서 50-200개의 대표 질문과 정답 근거를 사람이 label한다.
5. 검색 recall, reranking quality, citation 정확성, answer faithfulness, latency, 비용을 별도 dashboard로 운영한다.
