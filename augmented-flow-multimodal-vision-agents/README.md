<!-- rumdl-disable-file MD013 -->

# Augmented Flow와 멀티모달 비전 학습 에이전트

작성일: 2026-08-22

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [핵심 요약](#핵심-요약)
- [상세 정리](#상세-정리)
- [프로덕션 설계](#프로덕션-설계)
- [평가와 위험 관리](#평가와-위험-관리)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 원문: [The Augmented Flow: Disrupting Corporate Upskilling with Multimodal Vision Agents](https://nickbortolotti.medium.com/the-augmented-flow-disrupting-corporate-upskilling-with-multimodal-vision-agents-8d868a3a970b)
- 저자: Nicolas Bortolotti
- 게시 시각: 2026-08-20 11:57:11 UTC
- 원문 언어: 영어
- 확인일: 2026-08-22
- 접근 상태: Medium 직접 요청은 Cloudflare에 차단됐으나 공개 text extraction 경로에서 제목, 게시 시각, 본문과 코드 예시를 확인했다.
- 번역 범위: 저작권을 고려해 원문 전문을 복제하지 않고 section 흐름과 기술적 주장을 보존한 [한국어 번역 요약](translation.ko.md)을 제공한다.

이 문서는 원문의 제품 아이디어를 분석하고 실제 시스템으로 옮길 때 필요한 신뢰성, 개인정보 보호, 평가와 운영 설계를 보강한다. 원문에 등장하는 제품명과 latency 수치는 저자의 예시이며 이 문서가 독립적으로 재현·보증한 수치가 아니다.

## 한눈에 보기

전통적 기업 교육은 업무를 멈추고 LMS로 이동하게 만든다. 원문이 제안하는 **in-flow learning**은 실제 업무 화면 안에 작은 학습 과제를 표시하고, 에이전트가 DOM과 screenshot을 관찰해 단계 완료를 판정하며, 결과를 자동으로 학습 기록에 연결한다.

```text
업무 화면 + learning capsule
       ↓ observation
DOM/URL 규칙 ── 확정 가능 ──→ 즉시 판정
       │ 불확실
       ↓
local/VPC vision-language model
       ↓ structured decision
안내 UI → 검증된 telemetry → credential 후보
```

좋은 설계의 핵심은 vision model을 모든 단계의 심판으로 쓰는 것이 아니다. 빠르고 설명 가능한 DOM 규칙을 우선하고, 시각·공간적 판단이 필요한 경우에만 제한된 image와 context를 model에 전달해야 한다.

## 기초 개념

### In-flow learning

교육을 실제 작업과 분리된 강의가 아니라 작업 흐름 속의 짧은 목표·피드백으로 제공하는 방식이다. 사용자가 실제 도구를 조작하므로 전이 비용이 낮지만, 업무 감시로 느껴지지 않도록 목적·수집 범위·보존 기간을 명확히 해야 한다.

### Multimodal vision agent

text, screenshot, DOM summary처럼 서로 다른 modality를 함께 해석하는 agent다. 화면 전체 pixel을 보내는 것보다 task 기준, 허용된 element, redacted screenshot을 제공하면 비용과 privacy risk를 낮출 수 있다.

### Deterministic fast-path

URL query, DOM attribute, application state 또는 backend event처럼 명확한 signal로 완료 여부를 판정하는 경로다. 재현 가능하고 빠르며 감사가 쉽다. 단순 문자열 포함 검사만 사용하면 spoofing과 false positive가 생기므로 origin, selector, semantic state와 server-side event를 함께 확인해야 한다.

### Credential telemetry

어떤 사용자가 언제 어떤 기준을 충족했는지 기록한 event다. 관찰 event와 검증된 skill credential을 분리하고, 증거 hash, 평가기 버전과 policy version을 남겨야 한다.

## 핵심 요약

원문은 세 가지 구조적 축을 제안한다.

1. **Learning Capsules**: 실제 UI 안에 표시되는 작고 결과 중심적인 challenge
2. **다층 평가 엔진**: DOM/URL heuristic을 먼저 실행하고 불충분할 때 local vision analysis 사용
3. **자동 telemetry와 credentialing**: 단계 완료 신호를 기업 skill matrix에 연결

backend 예시는 browser extension이 보낸 base64 screenshot과 DOM summary를 받아 heuristic을 수행한 뒤, task·step·criteria·DOM·image를 vision model에 전달한다. model 호출 실패 시 heuristic 결과와 hint를 반환하는 fallback도 보여준다.

## 상세 정리

### Learning capsule 설계

좋은 capsule은 하나의 관찰 가능한 결과에 집중한다.

- 나쁜 목표: “CRM을 이해한다.”
- 좋은 목표: “테스트 고객을 만들고 owner와 next-action을 지정한다.”

각 단계에는 사용자에게 보이는 지시, 기계가 판정할 completion criterion, 실패 시 hint, 수집 가능한 evidence와 금지된 data 범위를 정의한다.

### 다층 판정

권장 순서는 다음과 같다.

1. server-side business event
2. application API 또는 trusted state
3. semantic DOM state
4. URL/navigation signal
5. redacted screenshot 기반 vision model
6. 사람이 확인해야 하는 escalation

원문의 예시는 search 관련 단계에서 URL의 query marker를 찾는다. 이는 설명에는 유용하지만 production에서는 query parameter 존재만으로 실제 과업 성공을 인정하면 안 된다. 올바른 domain, 결과 상태, 필요한 filter와 backend event까지 교차 확인한다.

### Structured output

model의 자유 형식 답변을 그대로 frontend에 보내지 않는다. 최소 schema 예시:

```json
{
  "schema_version": "1.0",
  "step_completed": false,
  "confidence": 0.72,
  "evidence": ["target control visible"],
  "advice": "저장 버튼을 선택하세요.",
  "needs_human_review": false
}
```

JSON schema validation, enum, 길이 제한과 confidence threshold를 적용한다. model의 내부 추론을 저장하기보다 판정에 사용된 짧고 검증 가능한 evidence를 남긴다.

### Fallback의 의미

inference timeout 때 항상 HTTP success를 반환하는 것은 transport 안정성에는 도움이 되지만 판정 의미를 흐릴 수 있다. 다음 상태를 구분하는 편이 안전하다.

- `completed`: 충분한 evidence로 완료
- `not_completed`: 충분한 evidence로 미완료
- `unknown`: model timeout, image 불량 또는 signal 부족
- `needs_review`: 고위험 credential 또는 판정 충돌

`unknown`을 `not_completed`나 heuristic의 추정값으로 감추지 않아야 운영자가 장애를 발견할 수 있다.

## 프로덕션 설계

### Browser extension

- 사용자가 capsule을 시작했을 때만 관찰
- 허용 domain과 selector를 allowlist로 관리
- password, token, email, 채팅과 개인정보 영역을 수집 전 mask
- 전체 screenshot 대신 관심 영역 crop 우선
- observation rate 제한과 사용자 pause 제공
- extension과 backend 사이에 short-lived authentication 사용

### Backend

- request body와 base64 image 크기 제한
- MIME signature 확인과 image decode 격리
- endpoint/model name을 client가 임의 지정하지 못하게 server policy로 고정
- outbound network allowlist와 짧은 timeout
- schema validation 실패 시 `unknown` 처리
- tenant별 encryption, retention과 deletion policy

### Credential pipeline

```text
raw observation
  → policy/consent check
  → evaluator decision
  → evidence digest + evaluator version
  → append-only completion event
  → skill rule aggregation
  → revocable credential
```

한 번의 screenshot 판정만으로 중요한 자격을 발급하지 않는다. 여러 task, 시간에 따른 반복 수행, 업무 시스템의 trusted event와 필요 시 사람 검토를 조합한다.

## 평가와 위험 관리

### Offline 평가

- 단계별 완료/미완료/판단 불가 dataset
- DOM 변화, theme, 해상도, 언어와 accessibility mode 포함
- false accept와 false reject를 별도로 측정
- 규칙 단독, vision 단독, cascade를 같은 dataset에서 비교
- model, prompt, schema와 policy version 고정

### Online 지표

| 영역 | 예시 지표 |
|---|---|
| 학습 | task completion, hint 사용률, 재시도 후 유지율 |
| 품질 | false accept, false reject, unknown, human overturn |
| 성능 | fast-path 비율, p50/p95 latency, timeout |
| 비용 | 단계당 model call, image byte, token과 accelerator time |
| privacy | mask coverage, policy violation, retention deletion SLA |
| 공정성 | 언어·환경·보조기술별 오류율 차이 |

### 주요 위험

- **감시와 신뢰 저하**: 직원 평가와 학습 지원의 경계를 명확히 한다.
- **Prompt injection**: 화면 text를 instruction이 아니라 untrusted evidence로 취급한다.
- **Spoofing**: DOM이나 screenshot만으로 고가치 credential을 발급하지 않는다.
- **자동화 편향**: 언어, 화면 배율과 보조기술 사용자의 오류율을 비교한다.
- **목표 대리화**: 클릭 완료가 실제 역량을 의미하는지 별도 전이 평가를 한다.

## 용어 정리

| 용어 | 의미 |
|---|---|
| LMS | Learning Management System. 강의·진도·평가를 관리하는 시스템 |
| DOM | 브라우저 문서의 구조화된 객체 표현 |
| Multimodal | text, image 등 여러 입력 형식을 함께 처리하는 성질 |
| Fast-path | 값싼 결정적 검사만으로 빠르게 끝내는 실행 경로 |
| Fallback | 주 경로 실패 또는 불확실 시 사용하는 대체 경로 |
| VPC | 격리된 virtual network 환경 |
| Credential | 검증된 학습·기술 성취를 나타내는 발급·검증 가능한 기록 |
| Evidence digest | 원본 증거를 직접 보관하지 않고 무결성 대조에 쓰는 hash |

## 실습 학습 가이드

1. [01_foundations.ipynb](01_foundations.ipynb): DOM fast-path와 판정 지표
2. [02_practice.ipynb](02_practice.ipynb): heuristic과 mock vision agent를 결합한 structured supervisor
3. [03_advanced.ipynb](03_advanced.ipynb): cascade 평가, latency·비용, privacy와 credential event

모든 notebook은 외부 API와 실제 screenshot 없이 실행된다. `mock vision`은 architecture와 평가 contract를 익히기 위한 대역이며 실제 multimodal model 성능을 재현하지 않는다.

## 다음 학습 경로

1. JSON Schema와 typed API contract
2. browser extension의 content script·permission model
3. vision-language model evaluation과 calibration
4. privacy-preserving telemetry와 data retention
5. Open Badges/Verifiable Credentials와 revocation
6. human-in-the-loop 운영과 교육 효과의 causal evaluation

[한국어 번역 요약](translation.ko.md)에서 원문의 section별 흐름을 이어서 볼 수 있다.
