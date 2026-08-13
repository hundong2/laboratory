# 그라운딩 개요 — 한국어 학습용 재구성본

원문: [Google Cloud — Gemini Enterprise Agent Platform 그라운딩 개요](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/grounding/overview?hl=ko)

- 원문은 한국어로 제공된다.
- 원문 최종 업데이트: 2026-08-08 UTC
- 접근일: 2026-08-14
- 이 파일은 원문을 그대로 복제하지 않고 구조를 따른 교정·학습용 한국어 정리본이다.

## 그라운딩 예제

Google Cloud는 “그라운딩 소개” notebook을 Colab, Colab Enterprise, Agent Platform Workbench 또는 [GitHub](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/grounding/intro-grounding-gemini.ipynb)에서 실행할 수 있도록 제공한다. cloud 환경에서 실행할 때는 project, billing, IAM, 지원 region과 API 활성화 상태를 먼저 확인한다.

## 그라운딩이란

생성형 AI에서 그라운딩은 모델 출력을 검증 가능한 정보 source에 연결하는 기능이다. 모델에 특정 data source 접근을 제공하면 답변을 해당 data에 묶어 조작되거나 사실과 다른 콘텐츠가 생성될 가능성을 줄인다. 정확성과 신뢰성이 중요한 업무에서 특히 중요하다.

주요 이점:

- 사실과 다른 내용을 생성하는 hallucination 감소
- 응답을 사용자가 선택한 data source에 연결
- source link 형태의 grounding support를 제공해 감사 가능성 향상

## 지원되는 방식

### Google Search를 사용한 그라운딩

Google 검색 결과를 사용해 모델을 폭넓은 세계 지식과 다양한 주제에 연결한다. 최신 public web 정보가 필요한 질문에 적합하다.

### Google Maps 기반 그라운딩

Google Maps 데이터와 지리정보 context를 사용해 장소 중심 prompt에 더 정확하고 상황에 맞는 답변을 제공한다.

### Agent Search로 그라운딩

RAG를 사용해 모델을 Agent Search에 저장된 website data 또는 문서 집합에 연결한다.

### RAG Engine으로 그라운딩

구성 가능한 managed RAG service인 Gemini Enterprise Agent Platform RAG Engine을 통해 사용자 data로 답변을 그라운딩한다.

### Elasticsearch를 사용한 그라운딩

기존 Elasticsearch index와 Gemini를 연결해 RAG를 수행한다. 기존 ingestion·search·metadata 체계를 재사용하려는 환경에 적합하다.

### Search API로 그라운딩

자체 Search API를 이용해 Gemini를 외부 data source와 연결한다. 결과 schema, timeout, 인증, source ID와 권한 전달을 명확히 설계해야 한다.

### Enterprise Web 그라운딩

규제가 엄격한 산업에 적합한 web index와 compliance control을 사용해 grounded answer를 생성한다.

### Parallel Web Search를 사용한 그라운딩

Gemini를 LLM에 최적화된 web index에 연결해 최신 web 정보를 사용한다.

## 언어와 다음 단계

사용 가능한 언어는 공식 “prompt에 지원되는 언어” 문서에서 확인한다. 서비스별로 지원 language나 품질이 다를 수 있으므로 target language로 별도 평가한다.

도입 전 [책임감 있는 AI 권장사항과 안전 필터](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/responsible-ai?hl=ko)를 함께 검토한다. 그라운딩은 안전 filter, 접근 통제와 사람의 검토를 대체하지 않는다.

## 라이선스 고지

원문 페이지는 별도 표시가 없는 문서 콘텐츠에 CC BY 4.0, code sample에 Apache 2.0이 적용된다고 고지한다. 재사용 시 원문 링크와 해당 license 조건을 확인한다.
