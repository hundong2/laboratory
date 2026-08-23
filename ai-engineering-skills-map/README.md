<!-- rumdl-disable-file MD013 -->

# Andrew Ng의 AI Engineering Skills Map

작성일: 2026-08-22

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [네 가지 핵심 역량](#네-가지-핵심-역량)
- [역량 간 연결](#역량-간-연결)
- [개인 학습 로드맵](#개인-학습-로드맵)
- [조직과 채용에서의 활용](#조직과-채용에서의-활용)
- [비판적으로 읽기](#비판적으로-읽기)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 원문 X 게시물: <https://x.com/AndrewYNg/status/2088302050706686198?s=20>
- 연결된 X Article ID: `2088296780983107584`
- 저자: Andrew Ng
- 게시 시각: 2026-08-14 16:29:42 UTC
- 원문 언어: 영어
- 확인일: 2026-08-22
- 접근 상태: X 원문 UI는 본문을 직접 반환하지 않았지만 공식 oEmbed에서 저자·게시 링크·짧은 소개를, 공개 text extraction에서 장문 본문을 확인했다. 연결된 `/i/article/` URL은 비로그인 요청에서 404였다.
- 번역 범위: 저작권이 있는 전문을 복제하지 않고 논지와 section 흐름을 보존한 [한국어 번역 요약](translation.ko.md)을 제공한다.

저자는 10,000개가 넘는 채용 공고, AI 전문가·채용 관리자·recruiter와의 수십 회 구조화 interview, 설문과 다른 online data를 종합했다고 설명한다. 원자료, sampling, coding scheme, cluster 분석과 통계치는 게시물에 제시되지 않았으므로 이 문서는 네 역량의 실용성을 분석하되 연구 결과를 독립 검증된 순위로 단정하지 않는다.

## 한눈에 보기

AI가 software를 만드는 방식을 바꾸면서 특정 직함의 “AI Engineer”만이 아니라 full-stack, data, DevOps, ML 등 모든 developer에게 AI engineering 역량이 필요하다는 것이 글의 출발점이다.

핵심 역량은 네 가지다.

1. **AI application 구축과 배포**
2. **Software engineering fundamentals**
3. **Coding agent 활용**
4. **Shaping the build** — 무엇을 왜 만들지 정의하고 추진하는 능력

그리고 네 영역을 가로지르는 기반은 **지속적 학습 mindset**이다.

```text
고객·사업 문제를 이해하고 build를 shaping
                  ↓
      명확한 spec·risk·success metric
                  ↓
software fundamentals ←→ coding agent 활용
                  ↓
AI application 구축·eval·배포·운영
                  ↓
        사용자 feedback과 error analysis
                  └───────────────↺
```

## 기초 개념

### AI engineering skill과 직함

직함은 조직의 역할 분류지만 skill은 실제 문제를 해결하는 능력이다. cloud가 거의 모든 developer의 기본 소양이 됐지만 모두가 cloud engineer는 아닌 것처럼, AI engineering도 여러 직무에 퍼지는 횡단 역량으로 볼 수 있다.

### 비결정적 output

전통적 software 함수는 같은 input에서 비교적 예측 가능한 output을 내는 반면 LLM·ML system은 prompt, data, sampling, model version과 context에 따라 달라질 수 있다. 따라서 example unit test만으로 충분하지 않고 dataset 기반 eval, 통계, monitoring과 governance가 필요하다.

### 역량과 도구 지식의 차이

특정 framework의 API를 외우는 것은 단기 지식이다. 요구 사항을 분해하고 trade-off를 설명하며 evidence로 품질을 개선하는 능력은 도구가 바뀌어도 남는다. skills map은 제품 목록이 아니라 반복 가능한 engineering behavior로 해석해야 유용하다.

## 네 가지 핵심 역량

### 1. AI application 구축과 배포

필요한 기반:

- LLM과 token·context·sampling의 기본 원리
- context engineering과 structured output
- RAG의 retrieval, indexing, grounding과 citation
- agentic workflow, tool contract와 state
- machine learning/deep learning의 기본 개념
- offline/online eval과 error analysis
- latency, cost, reliability, privacy와 governance
- deployment, monitoring, rollback과 incident response

가장 중요한 구분은 demo를 만드는 능력과 신뢰할 수 있는 system을 운영하는 능력이다. 후자는 실패 유형을 정의하고 representative dataset에서 측정하며 개선 전후 차이를 검증해야 한다.

### 2. Software engineering fundamentals

AI가 code를 빠르게 생성해도 architecture와 trade-off 책임은 사라지지 않는다.

- 자료구조, algorithm과 complexity
- interface, abstraction, modularity와 dependency
- database와 consistency·transaction
- concurrency, distributed system과 queue
- test pyramid, observability와 debugging
- security, privacy와 threat modeling
- version control, CI/CD와 release discipline
- cost, scale, reliability와 performance trade-off

fundamentals가 약하면 coding agent의 빠른 output을 평가하지 못하고 잘못된 선택에 정교한 언어로 개입하기 어렵다.

### 3. Coding agent 활용

효과적인 사용은 prompt 한 번을 잘 쓰는 것보다 작업 loop를 설계하는 능력에 가깝다.

1. 목표, 범위, 제약과 acceptance criterion 제공
2. repository·runtime·test 같은 필요한 context 제공
3. plan과 실행의 크기를 risk에 맞게 조절
4. test, lint, type check, benchmark와 review를 verifier로 제공
5. 중간 결과를 읽고 필요한 지점에서만 개입
6. production database·secret·배포 같은 위험 행동 제한
7. 도구와 workflow 변화를 작은 실험으로 지속 평가

agent가 autonomous하게 loop를 닫도록 하되 권한과 evidence 없이 성공을 선언하지 못하게 해야 한다. 여러 agent orchestration은 dependency와 merge cost가 실제 병렬 이득보다 작을 때만 사용한다.

### 4. Shaping the build

agent가 명확한 spec을 구현하는 능력이 높아질수록 engineer의 차별점은 spec 이전 단계로 이동한다.

- 고객 문제와 business context 발견
- solution보다 outcome을 먼저 정의
- assumption과 가장 큰 불확실성 식별
- MVP로 빠르게 학습할 시점과 천천히 설계할 시점 구분
- success metric, guardrail과 중단 조건 정의
- design·product·operations와 함께 scope 결정
- 책임 있는 실행과 project ownership

shaping은 단순 product management가 아니다. 기술적 가능성, 사용자 가치, 위험과 delivery cost를 함께 이해해 “무엇을 만들 것인가”를 바꾸는 engineering 활동이다.

## 역량 간 연결

네 영역은 독립 checkbox가 아니다.

- 좋은 product sense 없이 만든 eval은 중요하지 않은 metric을 최적화할 수 있다.
- software fundamentals 없이 agent를 쓰면 빠르게 technical debt를 만든다.
- eval 없이 AI application을 배포하면 변화하는 output을 통제할 수 없다.
- coding agent를 활용하지 않으면 검증 가능한 prototype과 실험을 만드는 속도에서 뒤처질 수 있다.
- build를 잘 shaping해도 production operation 능력이 없으면 사용자 가치로 이어지지 않는다.

따라서 학습 계획은 네 축을 번갈아 적용하는 project 중심 방식이 좋다.

## 개인 학습 로드맵

### 1–3주: 기본 loop

- 작은 LLM application 하나를 만든다.
- 30개 이상의 representative example과 expected property를 정의한다.
- error taxonomy를 만들고 baseline을 측정한다.
- Git, test, logging, secret 관리와 README를 갖춘다.

### 4–6주: context와 retrieval

- RAG 또는 tool-use workflow를 추가한다.
- retrieval와 generation 오류를 분리해 평가한다.
- latency·token·실패율을 기록한다.
- coding agent에게 작은 task를 주고 verifier 기반 workflow를 반복한다.

### 7–9주: production discipline

- API schema, authentication, rate limit과 timeout을 설계한다.
- versioned prompt/model/config와 rollback을 만든다.
- red-team case, privacy와 prompt injection을 평가한다.
- CI에서 deterministic check와 AI eval subset을 실행한다.

### 10–12주: shaping과 사용자 검증

- 실제 사용자 3–5명의 workflow를 관찰한다.
- 문제 statement와 성공·guardrail metric을 다시 쓴다.
- 가장 위험한 assumption을 검증하는 MVP를 배포한다.
- 결과를 근거로 build, pivot 또는 stop을 결정한다.

## 조직과 채용에서의 활용

### 역량 rubric

| 수준 | 관찰 가능한 행동 |
|---:|---|
| 0 | 용어를 접하지 않음 |
| 1 | 안내를 따라 toy example 실행 |
| 2 | 제한된 범위의 기능을 만들고 기본 test 수행 |
| 3 | trade-off를 설명하며 production 수준으로 운영 |
| 4 | 새로운 상황에서 원칙을 적용하고 팀의 기준을 개선 |

채용에서는 framework trivia보다 work sample을 사용한다. 예를 들어 작은 AI feature와 고의적 failure dataset을 제공하고 candidate가 error를 분류하고 architecture와 rollout plan을 설명하게 할 수 있다.

### 조직 역량 matrix의 주의점

- self-rating만으로 승진·보상을 결정하지 않는다.
- 직무별로 필요한 깊이가 다름을 인정한다.
- 도구 brand보다 행동과 evidence를 평가한다.
- accessibility와 학습 기회 차이를 고려한다.
- map을 고정된 정답이 아니라 정기적으로 versioning한다.

## 비판적으로 읽기

### 강점

- AI tool 사용을 software fundamentals의 대체재로 보지 않는다.
- eval/error analysis를 AI application engineering의 핵심에 둔다.
- coding agent의 context, verifier, autonomy와 risk를 함께 다룬다.
- engineer가 product·business 맥락과 project ownership을 가져야 한다고 본다.

### 확인이 필요한 점

- 10,000개 채용 공고의 국가, 기간, 직무 구성과 중복 제거 방식이 공개되지 않았다.
- interview·survey의 참여자 선정과 질문·coding 방법이 제시되지 않았다.
- “가장 중요”를 빈도, 미래 성장성, 채용 난도 중 무엇으로 계산했는지 불명확하다.
- 기술 시장이 빠르게 변하므로 2026년의 map을 다른 지역·산업에 그대로 적용할 수 없다.

따라서 조직은 이 map을 hypothesis와 공통 언어로 사용하고 자체 role·incident·project data로 보정해야 한다.

## 용어 정리

| 용어 | 의미 |
|---|---|
| Context engineering | model이 작업하는 데 필요한 instruction, data, tool과 state를 설계하는 활동 |
| RAG | 외부 자료를 검색해 model context에 제공하는 retrieval-augmented generation |
| Agentic workflow | model이 tool과 state를 사용해 여러 단계의 목표를 수행하는 흐름 |
| Eval | AI system의 품질·안전·비용을 dataset과 metric으로 측정하는 절차 |
| Error analysis | 실패 사례를 유형화하고 다음 개선의 우선순위를 찾는 과정 |
| Verifier | test, lint, schema, benchmark처럼 결과의 조건 충족을 확인하는 장치 |
| Spec | 목표, 범위, 제약, interface와 acceptance criterion을 명시한 계약 |
| MVP | 핵심 assumption을 최소 비용으로 검증하는 minimum viable product |
| Vibe coding | 생성된 code의 trade-off와 동작을 충분히 이해·검증하지 않고 감각적으로 개발하는 방식 |

## 실습 학습 가이드

1. [01_foundations.ipynb](01_foundations.ipynb): 네 역량 self-assessment와 project 기반 gap 우선순위
2. [02_practice.ipynb](02_practice.ipynb): AI application의 eval·error analysis loop
3. [03_advanced.ipynb](03_advanced.ipynb): coding agent readiness gate와 build-shaping portfolio

notebook은 외부 API 없이 Python standard library로 실행된다. 자동 점수는 reflection을 돕는 도구이지 실제 채용·성과 평가가 아니다.

## 다음 학습 경로

1. 작은 AI application을 end-to-end로 운영
2. software architecture와 distributed systems 기초
3. eval dataset design, calibration과 statistical testing
4. agent tool security와 least privilege
5. product discovery, user interview와 experiment design
6. incident review와 continuous learning cadence

[한국어 번역 요약](translation.ko.md)에서 원문의 논지를 section별로 이어서 볼 수 있다.
