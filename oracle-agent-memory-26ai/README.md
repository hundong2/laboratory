# Oracle AI Database 26ai로 만드는 3계층 Agent Memory

작성일: 2026-08-11

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [아키텍처](#아키텍처)
- [구현 핵심](#구현-핵심)
- [운영·보안 주의점](#운영보안-주의점)
- [실습](#실습)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 원문: [How I Taught an AI to Sound Like Me: Agent Memory with Oracle AI Database](https://blogs.oracle.com/developers/how-i-taught-an-ai-to-sound-like-me-agent-memory-with-oracle-database-26ai)
- 저자: Wojtek Pluta, Director, Technical Product Marketing
- 게시일: 2026-07-22 · 원문 표시: 13 minute read
- 원문 언어: 영어 · 접근일: 2026-08-11
- 공식 companion code: [oracle-agent-memory](https://github.com/oracle-devrel/oracle-ai-developer-hub/tree/main/apps/oracle-agent-memory)
- 확인 범위: 브라우저로 본문, 표, flowchart, SQL·TypeScript 예제, FAQ와 요약 전체를 확인했다. 직접 HTTP 요청에서는 일시적인 Oracle 403 오류가 있었으나 브라우저 렌더링은 정상 접근됐다.
- 번역 자료: [translation.ko.md](translation.ko.md)

## 한눈에 보기

stateless LLM은 사용자의 과거 글, 문장 리듬과 금기 표현을 모른다. 글은 prompt를 계속 키우는 대신 세 종류의 메모리를 데이터베이스에 저장한다.

| 계층 | 저장 내용 | 생성 시 역할 |
|---|---|---|
| Episodic | 과거 게시물과 embedding | 같은 사용자·platform의 유사 글 K개를 few-shot 예제로 검색 |
| Semantic | 문체를 설명하는 JSON profile | tone, 구조, signature phrase, 금기어를 system prompt에 주입 |
| Reflective | 최근 글이 profile을 어떻게 바꿨는지에 대한 diff와 snapshot | 작은 근거 기반 변경으로 profile을 점진적으로 갱신·rollback |

핵심 주장은 prompt가 아니라 prompt에 넣을 올바른 메모리가 어렵다는 것이다.

## 기초 개념

- **embedding**: 텍스트 의미를 고정 길이 숫자 vector로 바꾼 표현이다.
- **cosine distance**: vector 방향 차이를 이용해 의미적 유사도를 측정한다.
- **HNSW**: 대규모 vector에서 근사 최근접 이웃을 빠르게 찾는 graph index다.
- **hybrid filter**: vector 유사도와 `user_id`, `platform`, 삭제 여부 같은 SQL 조건을 함께 적용한다.
- **profile thrashing**: 최근 소수 사례에 과민 반응해 profile이 크게 흔들리는 현상이다.

## 아키텍처

```text
topic + platform
       |
       v
generatePost()
  |-- style_profile JSON 조회 ---------- semantic memory
  |-- topic embedding + vector 검색 ---- episodic memory
  `-- profile + examples로 LLM 1회 호출
       |
  사용자가 편집·게시
       |
  posts에 content + embedding 저장
       |
  새 글 K개마다 conservative diff 생성 -- reflective memory
       `-- profile 갱신 + reflections audit log
```

Oracle AI Database 한 query engine에서 관계형 행, `JSON`, `VECTOR`와 filter를 처리한다는 점이 원문 설계의 장점이다.

## 구현 핵심

### 스키마

- `posts`: `content CLOB`, `embedding VECTOR(1024, FLOAT32)`, 사용자·platform·soft-delete metadata
- `style_profile`: 사용자별 `profile JSON`, version과 갱신 시각
- `reflections`: 입력 post ID window, structured diff, 적용 후 profile snapshot

`VECTOR(1024, FLOAT32)`는 글에서 사용한 `cohere.embed-english-v3.0` 출력과 맞춘 값이다. embedding model을 바꾸면 차원을 반드시 함께 바꿔야 한다.

### 검색

`VECTOR_DISTANCE(..., COSINE)`으로 거리를 계산하면서 같은 사용자와 platform, `is_deleted = 0`을 filter한다. `FETCH APPROX FIRST :k ROWS ONLY`는 HNSW 근사 검색을 사용할 수 있게 한다. 작은 데이터에서는 exact scan도 가능하지만 규모가 커지면 index·recall·latency를 함께 측정해야 한다.

### profile 생성과 성찰

초기 N개 게시물로 구체적인 JSON style profile을 만든다. 이후 최근 K개(글의 예시는 5개)를 기존 profile과 비교하되 전체 overwrite 대신 additions/removals/rationale diff를 요구한다. diff와 `profile_after`를 기록하면 잘못 배운 문체를 이전 snapshot으로 rollback할 수 있다.

## 운영·보안 주의점

- LLM의 JSON 출력은 schema validation 후 transaction 안에서 적용한다. DB type 검증만으로 의미 오류를 막을 수 없다.
- bind variable을 사용하고 사용자별 row-level 접근 제어를 적용한다.
- 게시물은 개인정보·비공개 정보일 수 있다. embedding도 정보 유출 대상이므로 암호화, 보존 기간, 삭제 전파를 설계한다.
- prompt injection이 과거 게시물에 들어갈 수 있다. retrieved content를 명령이 아닌 인용 데이터로 분리한다.
- reflection은 자동 적용 전 diff 크기, 근거 post와 금지 field를 검증하고 audit log를 보존한다.
- 글에 제시된 OCI model ID, 가격·무료 tier와 API 형식은 2026-07-22 기준이며 현재 제공 여부를 공식 문서에서 다시 확인해야 한다.
- 타인의 문체를 동의 없이 사칭하거나 오해를 유발하는 자동 게시에 사용하지 않는다. 생성 사실 표기와 사람의 최종 검토를 권장한다.

## 실습

외부 package와 cloud 없이 실행되는 toy lab이다. 원문 production 결과를 재현한다고 주장하지 않는다.

1. [01_foundations.ipynb](01_foundations.ipynb): bag-of-words embedding과 cosine search로 episodic memory 이해
2. [02_practice.ipynb](02_practice.ipynb): style profile을 만들고 profile+example prompt 조립
3. [03_advanced.ipynb](03_advanced.ipynb): conservative reflection diff, validation, version과 rollback 구현

## 다음 학습 경로

1. toy embedding을 실제 embedding API와 Oracle `VECTOR` bind로 교체한다.
2. exact와 HNSW의 recall@K, p95 latency, 비용을 측정한다.
3. JSON Schema 검증, optimistic locking과 idempotent reflection job을 추가한다.
4. 문체 유사도뿐 아니라 사실성·독창성·금기 준수와 사람 선호를 평가한다.
