# Gemini Enterprise Agent Platform 그라운딩

작성일: 2026-08-14

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [지원되는 그라운딩 유형](#지원되는-그라운딩-유형)
- [선택 기준](#선택-기준)
- [설계와 실행 흐름](#설계와-실행-흐름)
- [평가·보안·운영](#평가보안운영)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 원문: [그라운딩 개요](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/overview?hl=ko)
- 제품: Gemini Enterprise Agent Platform
- 원문 언어: 한국어
- 원문 최종 업데이트: 2026-08-08 UTC
- 접근일: 2026-08-14
- 확인 범위: 페이지 본문, 지원 방식 8종, 연결 문서, notebook 링크, 언어·책임감 있는 AI 안내와 license 고지
- 라이선스 고지: 문서 콘텐츠 CC BY 4.0, 코드 샘플 Apache 2.0(페이지 고지 기준)
- 학습용 재구성본: [translation.ko.md](translation.ko.md)

이 문서는 현재 제품 기능을 설명하므로 실제 사용 전 공식 페이지에서 지역, 모델, API schema, quota와 가격을 다시 확인한다.

## 한눈에 보기

그라운딩(grounding)은 생성 답변을 검색 결과, 기업 문서, 위치 정보나 외부 검색 API 같은 **확인 가능한 정보 소스**에 연결하는 과정이다. 목적은 단순히 문맥을 더 주는 것이 아니라 다음을 가능하게 하는 데 있다.

- 최신·사내·도메인 정보를 모델 입력에 제공한다.
- 모델 hallucination 가능성을 낮춘다.
- 답변과 근거 link/citation을 연결해 사람이 감사할 수 있게 한다.
- 접근 통제와 규정 준수 범위 안에서 기업 데이터를 사용한다.

그라운딩은 정확성을 보장하지 않는다. 검색이 틀리거나 오래됐거나 권한 필터가 잘못되면 답변도 잘못될 수 있다. 따라서 retrieval과 generation을 따로 평가해야 한다.

## 기초 개념

- **Grounding**: 답변 주장을 외부 근거와 연결하는 전체 과정
- **RAG (Retrieval-Augmented Generation)**: 질문과 관련된 문서를 먼저 검색해 모델 문맥에 넣는 패턴
- **Corpus**: 검색 대상으로 색인한 문서 집합
- **Citation**: 답변의 특정 주장과 source 위치를 연결하는 표시
- **Freshness**: source가 현재 질문에 필요한 최신성을 갖는 정도
- **ACL filtering**: 사용자가 읽을 권한이 있는 문서만 검색 결과에 포함하는 통제

## 지원되는 그라운딩 유형

| 유형 | 대표 목적 | 핵심 데이터 |
|---|---|---|
| [Google Search](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/grounding-with-google-search?hl=ko) | 폭넓은 세계 지식과 최신 웹 정보 | Google 검색 결과 |
| [Google Maps](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/grounding-with-google-maps?hl=ko) | 장소·지리 context가 필요한 답변 | Google Maps 데이터 |
| [Agent Search](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/grounding-with-vertex-ai-search?hl=ko) | website 또는 기업 문서 RAG | Agent Search의 data store |
| [RAG Engine](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview?hl=ko) | ingestion·chunking·retrieval을 구성하는 managed RAG | 사용자가 관리하는 corpus |
| [Elasticsearch](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/grounding-with-elasticsearch?hl=ko) | 기존 Elasticsearch index 재사용 | Elasticsearch 문서 |
| [Search API](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/grounding-with-your-search-api?hl=ko) | 자체 search backend 연결 | 외부 API 결과 |
| [Enterprise Web](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/web-grounding-enterprise?hl=ko) | 규제가 엄격한 환경의 web grounding | compliance control이 적용된 web index |
| [Parallel Web Search](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/grounding-with-parallel?hl=ko) | LLM에 최적화된 web index의 최신 정보 | Parallel Web Search |

## 선택 기준

1. 정보가 public web인지 private enterprise data인지 구분한다.
2. 장소·거리·영업 정보처럼 geospatial context가 핵심이면 Maps를 검토한다.
3. 이미 Elasticsearch나 자체 검색 품질·ACL을 운영 중이면 기존 backend 연결을 우선 검토한다.
4. ingestion부터 관리형으로 구성하려면 Agent Search 또는 RAG Engine을 비교한다.
5. 규제·데이터 사용 조건·residency가 중요하면 Enterprise Web과 각 서비스의 compliance 문서를 확인한다.
6. freshness, latency, cost, citation granularity와 지원 모델을 실제 workload로 측정한다.

## 설계와 실행 흐름

```text
사용자 질문
  -> 인증·권한·query 정책
  -> 검색/grounding source 호출
  -> 결과 정규화·중복 제거·관련성 필터
  -> source ID가 보존된 context 구성
  -> Gemini 응답 생성
  -> claim-citation 정렬과 정책 검사
  -> 답변 + 근거 + 관측 지표 반환
```

source text를 prompt 명령으로 취급하지 말고 untrusted data로 분리한다. 검색 실패와 “관련 문서 없음”을 구분하고, 근거가 부족하면 모델이 추측하는 대신 불확실성을 표시하거나 답변을 보류하게 한다.

## 평가·보안·운영

### 평가

- retrieval recall@K와 precision@K
- 답변의 claim-level faithfulness
- citation coverage와 citation correctness
- 근거 부족 시 abstention 정확도
- ACL 누출 0건, stale source 비율
- p50/p95 latency, token·검색·생성 비용

### 보안

- 사용자 identity를 retrieval 단계까지 전달하고 문서 ACL을 강제한다.
- retrieved document의 prompt injection을 방어한다.
- 질문·검색어·snippet·답변 log에 개인정보와 secret이 남지 않도록 redaction·보존 정책을 둔다.
- 외부 Search API의 timeout, schema validation, allowlist와 TLS를 적용한다.
- citation URL은 사용자가 실제로 접근 가능한 source만 노출한다.

### 운영

index freshness, ingestion 실패, source별 hit rate, empty retrieval과 citation 없는 답변을 monitoring한다. grounding source 장애가 전체 답변을 조용히 ungrounded mode로 바꾸지 않도록 fail-closed 또는 명시적 degraded response 정책을 정한다.

## 실습 학습 가이드

1. [01_foundations.ipynb](01_foundations.ipynb): 작은 corpus에서 lexical retrieval과 권한 filter 구현
2. [02_practice.ipynb](02_practice.ipynb): source ID를 보존해 claim과 citation 연결
3. [03_advanced.ipynb](03_advanced.ipynb): retrieval·citation·abstention 평가와 운영 gate

세 notebook은 Python 표준 라이브러리만 사용하는 toy lab이며 Google Cloud API를 호출하지 않는다.

## 다음 학습 경로

1. 공식 [그라운딩 소개 notebook](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/grounding/intro-grounding-gemini.ipynb)을 검토한다.
2. 사용할 grounding source 한 가지를 선택하고 current API 문서의 model·region·IAM 조건을 확인한다.
3. 실제 질문·정답·허용 source로 evaluation set을 만든다.
4. offline retrieval 평가 후 shadow traffic, 제한된 사용자, 전체 rollout 순으로 확대한다.
5. [책임감 있는 AI](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/responsible-ai?hl=ko)와 안전 filter 정책을 함께 적용한다.
