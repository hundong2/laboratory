<!-- rumdl-disable MD013 -->

# Graph Engineering with Google ADK 2

작성일: 2026-09-11

확인 기준일: 2026-09-11

Google Agent Development Kit(ADK)에서 에이전트의 판단에 모든 실행 흐름을 맡기지 않고, 함수·에이전트·도구를 명시적인 그래프로 조합하는 방법을 학습하는 자료다. 요청 영상 **Graph Engineering with ADK**를 출발점으로 삼고, 버전에 따라 달라질 수 있는 API와 실행 의미는 Google 공식 ADK 문서, Google Codelab, PyPI 배포 정보를 기준으로 교차 확인했다.

- [영상 한국어 번역·해설](translation.ko.md)
- [기초 실습: 노드, 엣지와 Event](01_foundations.ipynb)
- [응용 실습: fan-out, JoinNode와 router](02_practice.ipynb)
- [심화 실습: 재시도, 실패 정책과 호출 예산](03_advanced.ipynb)

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [핵심 요약](#핵심-요약)
- [상세 정리](#상세-정리)
  - [그래프의 구성 요소](#그래프의-구성-요소)
  - [세 가지 오케스트레이션 스타일](#세-가지-오케스트레이션-스타일)
  - [순차·병렬·분기·반복](#순차병렬분기반복)
  - [출력·이벤트·상태·세션](#출력이벤트상태세션)
  - [콜백과 관측성](#콜백과-관측성)
  - [평가와 디버깅](#평가와-디버깅)
  - [배포와 운영](#배포와-운영)
  - [버전 차이](#버전-차이)
  - [영상 설명의 주장을 읽는 범위](#영상-설명의-주장을-읽는-범위)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

### 주 출처

| 출처 | 역할 | 확인 범위 |
| --- | --- | --- |
| [Graph Engineering with ADK 영상](https://www.youtube.com/watch?v=Mzr7byMFy_4) | 요청자가 지정한 주 출처 | 그래프 엔지니어링의 문제의식, 함수와 에이전트의 역할 분리, 병렬 fan-out/fan-in, 결정적 라우팅, 동적 워크플로에 관한 설명 |

### 보조·검증 출처

| 출처 | 확인한 내용 |
| --- | --- |
| [ADK 2 Orchestration: Graph, Collaborative & Dynamic Workflows](https://codelabs.developers.google.com/adk2/instructions?hl=en) | 영상 주제와 연결되는 Marathon Race Day Coach 실습, 그래프·협업·동적 워크플로 비교, `google-adk==2.3.0` 기준 예제와 호출 수 설명 |
| [ADK 2.0 공식 안내](https://adk.dev/2.0/) | Python 2.0 GA 일자, graph runtime 전환, 1.x 호환성과 주요 breaking change |
| [Graph-based agent workflows](https://adk.dev/graphs/) | `Workflow`, node, edge, 정적·동적·template workflow의 역할 |
| [Graph routes](https://adk.dev/graphs/routes/) | 순차 연결, 조건부 route, fan-out/fan-in, `JoinNode`, 조건부 반복 |
| [Dynamic workflows](https://adk.dev/graphs/dynamic/) | `@node`, `ctx.run_node()`, 반복·재귀·동적 폭, checkpoint와 resume |
| [Graph data handling](https://adk.dev/graphs/data-handling/) | 직접 출력 전달, Pydantic schema, event와 state의 사용 구분 |
| [ADK events](https://adk.dev/events/) · [Sessions](https://adk.dev/sessions/) · [State](https://adk.dev/sessions/state/) | 이벤트 수명주기, 상태 범위, 세션과 장기 memory의 차이 |
| [Callbacks](https://adk.dev/callbacks/) · [Observability](https://adk.dev/observability/) | 실행 전후 hook, 정책·로깅·추적 지점 |
| [Agent evaluation](https://adk.dev/evaluate/) · [Evaluation criteria](https://adk.dev/evaluate/criteria/) | 응답과 tool trajectory 평가, evalset·CLI·pytest 기반 회귀 평가 |
| [ADK Web](https://adk.dev/runtime/web-interface/) · [CLI](https://adk.dev/runtime/command-line/) | 로컬 실행, 이벤트·요청·응답·그래프 trace 확인 |
| [Deployment overview](https://adk.dev/deploy/) · [Cloud Run deployment](https://adk.dev/deploy/cloud-run/) | 배포 선택지, 영속 session/artifact service가 필요한 이유 |
| [google-adk PyPI](https://pypi.org/project/google-adk/) · [공식 릴리스](https://github.com/google/adk-python/releases) | 확인일 현재 안정판 `2.8.0`, Python 요구 버전과 빠른 릴리스 주기 |

이 문서는 영상이나 Codelab의 전문을 복제하지 않는다. 핵심 흐름을 한국어 학습 자료로 재구성하고, 버전·비용·신뢰성 주장은 공식 자료로 검증 가능한 범위와 실습 한정 범위를 구분한다. 영상 내용의 한국어 구조화 번역은 [translation.ko.md](translation.ko.md)에 별도로 제공한다.

## 한눈에 보기

ADK의 그래프 엔지니어링은 “에이전트를 많이 배치하는 기법”이 아니라 **어떤 일을 코드가 결정하고 어떤 일만 모델이 추론할지 경계를 설계하는 방법**이다.

```text
사용자 입력
    │
    ▼
결정적 함수 ── fan-out ──┬─ 데이터 조회 A ─┐
                          ├─ 데이터 조회 B ─┼─ JoinNode
                          └─ 데이터 조회 C ─┘
                                             │
                                             ▼
                                  코드 기반 route 선택
                                   ├─ HOT 전략 Agent
                                   ├─ NORMAL 전략 Agent
                                   └─ COLD 전략 Agent
                                             │
                                             ▼
                                       구조화된 결과
```

핵심은 다음 세 문장으로 압축된다.

1. 예측 가능한 처리는 일반 함수로 구현한다.
2. 명확한 규칙은 edge와 코드 route로 표현한다.
3. 언어 이해와 종합처럼 추론이 필요한 부분에만 모델을 사용한다.

이렇게 하면 모델이 처리해야 할 범위를 줄이고 실행 경로를 추적·테스트하기 쉬워진다. 다만 그래프를 사용했다는 사실만으로 환각이 제거되거나 시스템이 production-ready가 되지는 않는다.

## 기초 개념

### ADK란 무엇인가

Google Agent Development Kit는 에이전트, 도구, 세션, 평가와 배포를 코드로 구성하는 오픈소스 프레임워크다. Gemini에 최적화되어 있지만 설계상 모델과 배포 환경에 독립적인 사용을 지향한다. ADK 2.0에서는 에이전트·함수·도구가 모두 workflow graph의 node로 평가되는 **Workflow Runtime**이 도입되었다.

### 프롬프트 흐름과 코드 흐름의 차이

하나의 거대한 프롬프트에 “자료를 찾고, 조건을 판단하고, 경로를 선택하고, 보고서를 써라”라고 요구하면 모델이 입력 자료가 없는 부분까지 그럴듯하게 채울 수 있다. 또한 어떤 규칙으로 분기했는지 단위 테스트하기 어렵다.

반대로 그래프에서는 다음처럼 책임을 나눈다.

| 작업 | 권장 구현 | 이유 |
| --- | --- | --- |
| API 조회, 계산, 형식 변환 | Python 함수 또는 tool | 입력과 출력이 결정적이며 단위 테스트 가능 |
| 온도 임계값 같은 명확한 규칙 | `if`와 route edge | 실행 경로가 명시적이고 재현 가능 |
| 여러 자료를 읽고 자연어 전략 작성 | LLM Agent | 의미 해석과 종합 능력이 필요 |
| 입력에 따라 작업 개수가 달라지는 조사 | dynamic node | 정적 그래프로 미리 크기를 정할 수 없음 |

### 그래프가 곧 지식 그래프는 아니다

여기서 graph는 개체 관계를 저장하는 GraphRAG용 지식 그래프가 아니라 **실행 순서와 데이터 이동을 표현하는 directed execution graph**다. node는 계산 단위이고 edge는 다음 실행 위치를 뜻한다.

## 핵심 요약

- `Workflow(edges=[...])`는 실행 전에 구조를 알 수 있는 흐름을 선언적으로 표현한다.
- 순차 실행은 하나의 edge tuple, 병렬 실행은 fan-out tuple, 합류는 `JoinNode`, 조건 분기는 `Event(route=...)`와 route mapping으로 구성한다.
- node의 반환값은 다음 node의 입력으로 직접 전달하는 것이 기본이다. 공유해야 할 작은 제어 정보만 state에 둔다.
- 입력에 따라 branch 수나 깊이가 달라지면 `@node`와 `ctx.run_node()`를 쓰는 dynamic workflow가 적합하다.
- template `SequentialAgent`, `ParallelAgent`, `LoopAgent`의 개념은 여전히 유용하지만 Python ADK 2.x 신규 코드는 graph 또는 dynamic workflow를 우선 검토한다.
- LLM 호출 감소는 특정 그래프 구조의 결과이지 ADK 전체가 항상 한 번만 호출한다는 보장이 아니다.
- 운영 품질은 graph 외에도 schema 검증, timeout·retry, idempotency, 영속 session, 보안, tracing, 평가와 배포 구성이 함께 갖춰져야 한다.

## 상세 정리

### 그래프의 구성 요소

#### Node

node는 하나의 작업 단위다. ADK 2.x에서는 일반 Python 함수, `Agent`, tool, human-input node, 다른 `Workflow`를 node로 사용할 수 있다. 복잡한 절차를 작은 node로 나누면 각 부분을 독립적으로 테스트하고 교체할 수 있다.

#### Edge

edge는 node 사이의 실행 순서다. `START`는 그래프 진입점을 나타낸다.

```python
root_agent = Workflow(
    name="root_agent",
    edges=[("START", load_data, validate_data, summarize_agent)],
)
```

위 구조에서 각 node의 최종 output은 다음 node의 입력이 된다. 실제 예제에서는 입출력 schema를 선언해 연결 지점의 계약을 검증하는 것이 좋다.

#### Event

node는 단순 값을 반환하거나 `Event`를 내보낼 수 있다. Event는 다음과 같은 용도를 갖는다.

- `output`: 다음 node로 넘길 결과
- `route`: 조건 분기에서 선택한 경로
- `state`: 상태 변경 delta
- `content` 또는 메시지: 사용자에게 보여 줄 중간·최종 정보
- 실행 추적에 필요한 node와 invocation 정보

ADK 2.x에서는 session의 event 목록을 코드로 직접 수정하지 말아야 한다. node에서 event를 반환하거나 yield해야 Runner가 저장, route, streaming과 checkpoint를 일관되게 처리할 수 있다.

### 세 가지 오케스트레이션 스타일

#### 1. Graph workflow: 구조를 미리 그릴 수 있을 때

단계와 분기 후보를 실행 전에 알 수 있는 업무에 적합하다. 승인 절차, 정해진 데이터 파이프라인, 규칙 기반 분류와 보고서 생성이 대표적이다. 실행 경로를 코드와 그래프로 검토할 수 있어 테스트 가능성이 높다.

#### 2. Collaborative workflow: 팀은 알지만 호출할 구성원이 달라질 때

coordinator와 전문 sub-agent 집합은 고정되어 있지만 사용자 요청에 따라 필요한 구성원이 달라지는 경우다. ADK의 `chat`, `task`, `single_turn` 모드는 대화 지속 여부와 결과 반환 방식을 다르게 한다.

- `chat`: 사용자와 지속적으로 대화하며 명시적으로 이전하기 전까지 담당을 유지한다.
- `task`: 필요한 추가 정보를 대화로 수집한 뒤 구조화 결과로 parent에 자동 반환한다.
- `single_turn`: 사용자와 후속 대화하지 않고 한 차례 작업 결과를 parent에 반환하며 병렬 위임에 적합하다.

#### 3. Dynamic workflow: 실행하면서 구조가 정해질 때

입력에 따라 조사 항목이 3개가 될지 20개가 될지 모르거나, 결과에 따라 재귀적으로 세부 조사를 만들어야 할 때 사용한다. `@node`, `ctx.run_node()`, 일반 Python의 반복·조건·재귀로 오케스트레이션한다. 동적이라는 것은 설정 flag 하나가 아니라 **runtime data가 실행 폭과 깊이를 결정하도록 작성한 코드의 성질**이다.

동적 실행에는 반드시 경계를 둬야 한다.

- 최대 반복 횟수와 최대 재귀 깊이
- branch 최대 개수
- 개별 node timeout과 retry 상한
- 호출 예산 또는 token 예산
- 중단과 resume 시 idempotency 정책

### 순차·병렬·분기·반복

#### 순차 실행

선행 단계의 결과가 다음 단계의 입력일 때 사용한다. 모든 node는 같은 순서를 따르므로 가장 이해하고 테스트하기 쉽다.

```text
START → 수집 → 검증 → 추론 → 출력
```

#### 병렬 fan-out과 fan-in

서로 의존하지 않는 조회를 동시에 실행하고 `JoinNode`에서 기다린 뒤 결과를 묶는다.

```text
                 ┌→ weather ─┐
START → fan-out ─┼→ course  ─┼→ JoinNode → strategy
                 └→ history ─┘
```

`JoinNode`는 계산을 수행하는 node라기보다 모든 선행 branch가 완료될 때까지 기다리는 barrier다. 결과 dict의 key는 일반적으로 선행 node 이름이다. 모든 선행 node가 output을 내야 하며, 한 branch의 실패 정책과 retry 위치를 명확히 해야 한다. 병렬 branch가 같은 state key를 동시에 수정하지 않도록 branch별 key나 join 이후의 단일 병합 단계를 사용한다.

#### 결정적 분기

분기 조건이 온도, 상태 코드, 승인 여부처럼 명확하다면 모델에게 선택시키지 않고 함수에서 `Event(route=...)`를 반환한다.

```python
def route_by_temperature(node_input):
    temperature = node_input["weather"]["temp_f"]
    route = "HOT" if temperature >= 70 else "COLD" if temperature <= 40 else "NORMAL"
    return Event(output=node_input, route=route)
```

route mapping에는 예상하지 못한 값을 처리할 기본 경로를 두는 것이 안전하다. 일치하는 route가 없을 때 조용히 실행이 끝나는 형태는 운영 장애를 발견하기 어렵게 만든다.

#### 반복과 재귀

정적 graph에서는 조건부 route가 이전 node로 돌아가는 back-edge로 검토·수정 loop를 만들 수 있다. 무조건 순환은 거부되므로 종료 조건이 있어야 한다. 복잡한 loop와 runtime-sized 재귀는 dynamic workflow로 표현하고 최대 깊이와 횟수를 코드에 둔다.

### 출력·이벤트·상태·세션

#### 직접 output 전달을 우선한다

바로 다음 node만 사용할 데이터는 return 또는 `Event(output=...)`으로 넘긴다. 이 방식은 데이터 의존성이 edge에 드러나고 별도의 전역 상태를 줄인다. Pydantic `input_schema`와 `output_schema`를 사용하면 node 경계에서 자료형을 검증할 수 있다.

#### State는 범위가 있는 작은 공유 저장소다

| key 형식 | 범위 | 예시 |
| --- | --- | --- |
| 접두사 없음 | 현재 session | 현재 대화의 선택 옵션 |
| `user:` | 같은 사용자의 여러 session | 사용자 선호 언어 |
| `app:` | 애플리케이션 전체 | 공통 feature flag |
| `temp:` | 현재 invocation | 중간 제어 값, 임시 카운터 |

state에는 직렬화 가능한 작은 값만 저장한다. 대용량 문서, 이미지와 모델 artifact는 artifact service나 외부 object storage에 둔다.

#### Session과 Memory는 다르다

Session은 한 대화 thread의 event history와 현재 state를 묶는다. Memory는 여러 session에 걸쳐 검색 가능한 장기 정보를 뜻한다. 로컬 실습용 `InMemorySessionService`는 프로세스가 종료되면 사라지므로 운영 영속성의 증거가 아니다.

### 콜백과 관측성

ADK callback은 agent, model, tool 실행 전후에 정책이나 계측을 삽입하는 지점이다.

- before-model: 입력 정책 검사, cache 조회, 요청 로깅
- after-model: 응답 검사, 지표 기록
- before-tool: 인자 검증, 권한 확인, 승인 요구
- after-tool: 반환값 정규화, 오류·지연 기록
- before/after-agent: invocation 단위 계측과 상태 관리

일부 callback은 값을 반환해 원래 단계를 우회하거나 결과를 대체할 수 있으므로 “관찰만 하는 callback”과 “제어를 바꾸는 callback”을 구분해야 한다. 민감 정보는 trace나 prompt log에 그대로 남기지 않는다.

OpenTelemetry 추적을 연결하면 전체 agent run 아래에 model과 tool span을 배치해 지연 시간, 오류와 호출 관계를 볼 수 있다. 그러나 trace를 켰다는 사실만으로 민감 정보 마스킹, 보존 기간과 접근 제어가 해결되지는 않는다.

### 평가와 디버깅

에이전트는 최종 문장만 평가해서는 부족하다. 다음 두 축을 함께 본다.

1. **Trajectory 평가**: 어떤 tool과 node를 어떤 순서로 실행했는가?
2. **Response 평가**: 최종 답변이 정확하고 관련성이 있으며 근거를 보존하는가?

ADK는 `adk web`, `adk eval`, evalset JSON과 pytest 기반 `AgentEvaluator` 흐름을 제공한다. `adk web`의 trace에서는 Event, Request, Response와 Graph를 함께 확인할 수 있다.

권장 테스트 층은 다음과 같다.

- 함수 node 단위 테스트: 입력, 출력, 예외와 경계값
- graph 구조 테스트: route 후보, join 선행 node와 loop 종료 조건
- deterministic trajectory 테스트: 예상 tool·node 순서와 호출 횟수
- model 평가: 의미적 정확성, groundedness, 안전 정책
- 장애 테스트: timeout, 429, 부분 branch 실패, resume와 중복 실행
- 회귀 평가: prompt, model 또는 ADK 버전 변경 전후 evalset 비교

ROUGE 같은 문자열 유사도만으로 자유로운 생성 답변을 판정하면 표현은 다르지만 맞는 답을 실패로 보거나, 문장은 비슷하지만 근거가 잘못된 답을 통과시킬 수 있다. 구조화 assertion, trajectory, rubric 또는 judge 기반 평가를 목적에 맞게 조합한다.

### 배포와 운영

ADK 애플리케이션은 Agent Runtime, Cloud Run, GKE 또는 일반 container 환경에 배포할 수 있다. 배포 명령이 성공한 것과 production-ready는 다른 단계다.

운영 전 최소 확인 항목:

- 영속 `SessionService`와 `ArtifactService`
- 비밀값을 코드·노트북·로그에 남기지 않는 Secret Manager 연동
- 서비스 계정 최소 권한과 인증된 endpoint
- timeout, 제한된 retry, rate limit과 호출 예산
- 외부 쓰기 tool의 idempotency key와 중복 실행 방지
- 입력·출력 schema 및 tool argument 검증
- OpenTelemetry trace, metric, structured log와 경보
- offline evalset과 배포 전후 smoke test
- model·ADK 버전 pinning과 rollback 계획
- 개인정보·prompt·tool 결과의 저장 및 삭제 정책

특히 Cloud Run에서 session/artifact service URI를 지정하지 않아 in-memory 구현으로 동작하면 instance 재생성 시 기록이 사라진다. 여러 instance가 동시에 실행되는 환경에서는 process memory를 공유 상태로 간주해서도 안 된다.

### 버전 차이

| 기준 | ADK 버전 | 의미와 주의점 |
| --- | --- | --- |
| 요청 영상 | ADK 2.0의 graph engineering 관점 | 함수와 Agent를 동등한 graph node로 배치하는 2.0 전환을 설명하는 개념 자료다. 영상의 코드·표현을 최신 API 계약으로 간주하지 않는다. |
| 연결 Google Codelab | `google-adk==2.3.0` 고정 | Codelab은 2.3.0과 2.0.0b1에서 검증되었다. 당시 `mode="task"` Agent는 정적 graph node로 직접 사용할 수 없어 coordinator 또는 `ctx.run_node()` 우회가 필요했다. |
| 현재 확인 환경 | `google-adk==2.8.0` | 2026-09-11 기준 PyPI 최신 안정판이다. `task`의 정적 graph node 지원은 2.5.0부터 달라졌으므로 2.3.0의 모든 제한을 현재 동작으로 일반화하면 안 된다. |

Python ADK 2.0은 2026-05-19 GA가 되었다. 2.0에서 `BaseAgent`가 `BaseNode`의 하위 형식이 되었고, Event schema에 graph 추적용 `node_info`와 `output`이 추가되었다. 1.x용 custom `BaseSessionService`가 고정된 DB column이나 엄격한 JSON schema를 사용한다면 migration이 필요하다.

학습 자료와 노트북은 재현성을 위해 `google-adk==2.8.0`을 기준으로 한다. 공식 저장소의 `main`은 다음 릴리스 기능이 먼저 들어오는 개발 상태이고 PyPI 안내상 릴리스 주기도 빠르므로, 설치 시 무조건 최신판을 받는 방식은 장기 재현에 적합하지 않다.

### 영상 설명의 주장을 읽는 범위

#### “Production-ready”

graph 구조는 실행 경로를 명시하고 테스트 가능한 seam을 제공하므로 production readiness에 도움이 된다. 하지만 영상 또는 Codelab의 데모가 곧 운영 준비 완료를 뜻하지는 않는다. Codelab의 canned weather·course·training data는 실제 외부 시스템의 인증, 지연, schema drift, 장애와 개인정보 문제를 재현하지 않는다. 영속 session, 보안, 관측성, 평가, 장애 복구와 배포 검증을 추가한 뒤에만 특정 환경에 대한 production readiness를 주장할 수 있다.

#### “환각을 없앤다”

함수로 얻은 날씨 값과 코드 기반 route는 모델이 그 값을 임의로 발명할 여지를 줄인다. 이것은 **환각 표면을 축소**하는 효과이지 환각 제거 보장은 아니다.

- 함수가 stale 또는 잘못된 데이터를 반환할 수 있다.
- 모델이 올바른 tool output을 잘못 해석할 수 있다.
- 최종 문장에 입력에 없던 사실을 추가할 수 있다.
- 모델이 호출 여부를 결정하는 tool은 상황에 따라 호출하지 않을 수 있다.

따라서 출처와 timestamp 보존, schema 검증, groundedness 평가, 허용되지 않은 주장 탐지와 안전한 fallback이 필요하다.

#### “Zero cost”

Codelab의 병렬 fetch 함수와 `if` router는 **LLM 호출이 0회인 단계**다. 이것을 전체 시스템 비용 0으로 해석하면 안 된다. strategy Agent는 모델을 호출하고, dynamic 예제는 입력에 따라 여러 번 호출한다. AI Studio free tier도 quota와 제공 정책 안에서만 무료이며 다음 비용은 별개다.

- 외부 API, 데이터베이스와 network egress
- Cloud Run·Agent Runtime 같은 compute
- trace·log·artifact·session storage
- 평가용 모델 또는 judge 호출
- retry와 recursive branch가 늘리는 추가 호출

따라서 비용은 node별 모델 호출 수, token, 외부 서비스와 infrastructure를 함께 계측해야 한다.

#### “정확히 1회 LLM 호출”

Codelab L2b의 “1회”는 **세 개의 fetch와 router는 함수이고, 선택된 strategy Agent 하나만 실행되는 그 예제의 정상 논리 경로**를 뜻한다. 다음 상황까지 exactly-once를 보장한다는 뜻은 아니다.

- SDK 또는 infrastructure retry로 물리적 API 요청이 반복되는 경우
- resume 시 `rerun_on_resume=True` node가 재실행되는 경우
- callback, 평가 judge 또는 후속 Agent를 추가한 경우
- 선택된 Agent가 tool·sub-agent를 추가로 호출하는 경우
- timeout 뒤 응답 성공 여부를 알 수 없어 client가 재시도하는 경우

호출 횟수는 trace에서 실제 model span을 세어 검증해야 한다. 외부 쓰기 작업은 “한 번 호출할 계획”에 의존하지 말고 idempotency key, 처리 기록과 중복 제거로 안전하게 만든다.

## 용어 정리

| 용어 | 의미 |
| --- | --- |
| ADK | Agent Development Kit. 에이전트 개발·오케스트레이션·평가·배포용 Google 오픈소스 프레임워크 |
| Agent | 모델, instruction, tool과 동작 정책을 묶은 실행 단위 |
| Workflow | node와 edge로 실행 흐름을 선언하는 ADK 2.x graph container |
| Node | 함수, Agent, tool, human input 또는 nested Workflow로 표현되는 작업 단위 |
| Edge | node 사이의 실행 순서와 이동 관계 |
| Route | 현재 node가 이름을 지정해 다음 분기 edge를 선택하는 제어 정보 |
| Fan-out | 하나의 선행 지점에서 여러 독립 branch를 병렬로 시작하는 패턴 |
| Fan-in | 여러 branch의 완료를 기다렸다가 결과를 하나로 모으는 패턴 |
| JoinNode | 모든 선행 branch를 기다리고 node 이름 기반 dict로 output을 묶는 합류 node |
| Static graph | 실행 전에 node와 edge 후보를 그릴 수 있는 workflow |
| Dynamic workflow | runtime 입력에 따라 branch 수, 반복 또는 재귀 깊이가 달라지는 workflow |
| Event | 메시지, output, route, state delta와 실행 metadata를 전달·기록하는 기본 단위 |
| State | session/user/app/invocation 범위에서 공유하는 직렬화 가능한 key-value 자료 |
| Session | 하나의 대화 thread에 속한 event history와 state |
| Memory | 여러 session을 넘어 검색·회수할 수 있는 장기 정보 저장 계층 |
| Callback | agent/model/tool 실행 전후에 검사, 제어 또는 관측 로직을 삽입하는 hook |
| Trajectory | 최종 답변에 도달하는 동안 실행한 node·tool과 그 순서 |
| Checkpoint | 완료된 실행 단계를 기록해 중단 뒤 resume할 때 불필요한 재실행을 줄이는 지점 |
| Idempotency | 같은 요청이 중복 실행되어도 결과나 외부 상태가 한 번 실행한 것과 같도록 하는 성질 |

## 실습 학습 가이드

실습은 Python 3.10 이상과 `google-adk==2.8.0`을 기준으로 한다. 세 노트북은 모두 실제 ADK 그래프 API를 사용하지만, 모델 Agent는 결정론적 stub으로 대체해 Gemini API 키와 네트워크 호출 없이 끝까지 실행된다.

### 1. [기초: 노드, 엣지와 Event](01_foundations.ipynb)

- 두 결정론적 Python 함수를 `Workflow`의 순차 edge로 연결한다.
- `START`, 함수 node, `Event(output=...)`와 직접 output 전달을 익힌다.
- `Runner`와 `InMemorySessionService`로 실제 event stream을 수집한다.
- edge 구조, 정규화 결과와 모델 호출 예산을 assertion한다.

### 2. [응용: fan-out, JoinNode와 router](02_practice.ipynb)

- 마라톤 예제의 날씨·코스·체력 조회를 fan-out한다.
- `JoinNode`에서 선행 node 이름을 key로 결과를 모은다.
- 순차 실행 시간과 병렬 실행 시간을 비교한다.
- `DEFAULT_ROUTE`가 있는 결정론적 온도 router를 연결한다.
- HOT/NORMAL/COLD별로 전략 stub 하나만 실행되는지 assertion한다.

### 3. [심화: 재시도, 실패 정책과 호출 예산](03_advanced.ipynb)

- 실제 `RetryConfig`와 node timeout을 설정하고 통제된 일시 오류의 회복을 관찰한다.
- 재시도 중 오류 Event와 최종 성공 Event를 구분한다.
- 필수 branch 실패는 `BLOCKED`, 선택 branch 실패는 `DEGRADED`로 처리한다.
- route 실행 전에 모델 호출 예산을 예약하고 초과를 차단한다.
- 정적 graph, dynamic workflow, autonomous agent의 선택 기준을 검증한다.
- persistence·관측성·보안·idempotency를 포함한 배포 체크리스트를 제공한다.

권장 학습 순서는 `01_foundations.ipynb` → `02_practice.ipynb` → `03_advanced.ipynb`이다. 개념 설명을 먼저 한국어로 확인하려면 [translation.ko.md](translation.ko.md)를 읽는다.

## 다음 학습 경로

1. [공식 graph workflow 문서](https://adk.dev/graphs/)의 순차 예제를 자신의 작은 업무로 바꾼다.
2. [공식 route 문서](https://adk.dev/graphs/routes/)를 따라 fan-out/fan-in과 `DEFAULT_ROUTE`가 필요한 실패 경로를 추가한다.
3. [공식 workflow sample 모음](https://github.com/google/adk-python/tree/main/contributing/samples/workflows)에서 sequence, route, fan-out/fan-in, loop와 state 예제를 비교한다.
4. [Dynamic workflows](https://adk.dev/graphs/dynamic/)를 읽고 runtime 폭과 깊이에 각각 상한을 둔 조사 workflow를 만든다.
5. [Evaluating Agents with ADK Codelab](https://codelabs.developers.google.com/adk-eval/instructions?hl=en)로 golden dataset, trajectory와 CI용 pytest 평가를 구성한다.
6. `adk web`과 OpenTelemetry trace에서 계획한 호출 수와 실제 model span 수가 같은지 확인한다.
7. 영속 session/artifact service와 인증을 구성한 staging 환경에서 timeout, retry, resume와 중복 요청을 검증한다.
8. ADK 또는 model 버전을 올리기 전에 고정 evalset을 다시 실행하고, 변경 사항과 rollback 지점을 기록한다.

최종 목표는 그래프를 복잡하게 만드는 것이 아니다. **결정 가능한 부분은 코드로 고정하고, 모델이 필요한 부분은 좁히며, 모든 경계와 실패를 관찰하고 테스트할 수 있게 만드는 것**이 graph engineering의 핵심이다.
