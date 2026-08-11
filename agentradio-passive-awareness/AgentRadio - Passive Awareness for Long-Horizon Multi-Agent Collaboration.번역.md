# AgentRadio: Passive Awareness for Long-Horizon Multi-Agent Collaboration

## 논문 메타데이터

| 항목 | 내용 |
|---|---|
| 원문 제목 | AgentRadio: Passive Awareness for Long-Horizon Multi-Agent Collaboration |
| 저자 | Xinxing Ren, Qianbo Zang, Ziyan Wang, Caelum Forder, Suman Deb, Peter Carroll, Zekun Guo |
| 소속 | Coral AI Labs; SnT, Université du Luxembourg; King's College London; University of Hull |
| 공개 형태 | arXiv preprint |
| 연도/버전 | 2026, arXiv:2607.28430v1 (2026-07-30) |
| DOI | 10.48550/arXiv.2607.28430 |
| 원문 | [abstract](https://arxiv.org/abs/2607.28430) · [PDF](https://arxiv.org/pdf/2607.28430) |
| 원문 언어 | 영어 |
| 접근일 | 2026-08-11 |
| 라이선스 | [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) |

이 문서는 CC BY 4.0 원문을 한국어 학습 목적으로 번역·해설한 것이다. 저자의 주장과 번역자의 설명을 구분하며, 표와 수치는 PDF v1과 대조했다. 전체 분석은 [README](README.md)를 참고한다.

## 번역·접근 범위

| 원문 영역 | 상태 | 비고 |
|---|---|---|
| 제목·초록 | 완료 | 문장 대조 번역 |
| 서론·기여 | 완료 | 문장 대조 번역 |
| 관련 연구 | 부분 번역 | 연구 흐름과 비교축을 번역·요약 |
| AgentRadio 방법·알고리즘 | 완료 | primitive, 형식화, 5단계 protocol 포함 |
| 실험·주요 결과 | 완료 | 표 1~3의 핵심 수치 포함 |
| 분석·사례·결론 | 완료 | 그림 4~7의 해석 포함 |
| 참고문헌 | 해당 없음 | bibliographic record는 원문 PDF 링크로 대체 |

## 읽기 전 핵심 배경

- **foreground(전경)**는 에이전트가 현재 수행 중인 추론이나 도구 호출이다.
- **background watcher(백그라운드 감시자)**는 LLM step을 점유하지 않고 mention을 기다리는 운영체제 프로세스다.
- **passive awareness(수동 인지)**는 작업을 멈추지 않은 채 동료의 메시지를 다음 step 경계에서 알게 되는 능력이다.
- **ablation(절제 실험)**은 시스템 요소를 한 단계씩 추가해 각 요소의 독립 효과를 측정한다.

## 제목과 초록

**S001 — Original**

AgentRadio: Passive Awareness for Long-Horizon Multi-Agent Collaboration.

**S001 — 한국어**

AgentRadio: 장기 실행 멀티에이전트 협업을 위한 수동 인지.

**S002 — Original**

Understanding large codebases is a long-horizon task for Large Language Model (LLM) agents: answering a single question can require building and running the software, tracing execution across files, and synthesizing evidence over tens of minutes.

**S002 — 한국어**

대규모 코드베이스 이해는 대규모 언어 모델(LLM) 에이전트에게 장기 실행 과제다. 질문 하나에 답하기 위해 소프트웨어를 빌드하고 실행하며, 여러 파일을 가로지르는 실행을 추적하고, 수십 분 동안 모은 증거를 종합해야 할 수 있다.

- **용어·약어 해설**
  - **LLM (Large Language Model, 대규모 언어 모델)**: 이 논문에서는 shell과 코드 탐색 도구를 사용하는 coding agent의 추론 엔진이다.
  - **long-horizon task(장기 실행 과제)**: 많은 상호 의존적인 step과 긴 문맥을 필요로 하는 과제다.

**S003 — Original**

On SWE-Atlas QnA, a benchmark of long-horizon questions over production repositories, a single Claude Code agent (Opus 4.6) resolves only 32.3% of tasks.

**S003 — 한국어**

production repository에 관한 장기 질문 benchmark인 SWE-Atlas QnA에서 단일 Claude Code 에이전트(Opus 4.6)는 과제의 32.3%만 해결한다.

**S004 — Original**

Dividing the work among agents with clean contexts mitigates this limitation.

**S004 — 한국어**

깨끗한 문맥을 가진 여러 에이전트에게 작업을 나누면 이 한계를 완화할 수 있다.

**S005 — Original**

However, the subtasks of code comprehension are interdependent.

**S005 — 한국어**

하지만 코드 이해의 하위 과제들은 서로 의존한다.

**S006 — Original**

One agent's findings can rewrite another's task, so agents must coordinate during execution, not only at phase boundaries.

**S006 — 한국어**

한 에이전트의 발견이 다른 에이전트의 과제를 다시 정의할 수 있으므로, 에이전트들은 단계 경계에서만이 아니라 실행 중에도 조정해야 한다.

**S007 — Original**

Existing multi-agent systems support such exchange only between phases, through staged handoffs or synchronized rounds.

**S007 — 한국어**

기존 멀티에이전트 시스템은 단계적 인계나 동기화된 round를 통해 단계 사이에서만 이런 교환을 지원한다.

**S008 — Original**

Communication and work remain mutually exclusive.

**S008 — 한국어**

통신과 작업은 여전히 상호 배타적이다.

**S009 — Original**

A discovery made mid-execution cannot be shared until the next boundary.

**S009 — 한국어**

실행 도중 생긴 발견은 다음 단계 경계까지 공유할 수 없다.

**S010 — Original**

We present AgentRadio, an asynchronous message-passing layer that equips coding-agent harnesses with three primitives: threads, messages, and waiting for mentions.

**S010 — 한국어**

저자들은 coding-agent harness에 thread, message, mention 대기라는 세 primitive를 제공하는 비동기 메시지 전달 계층 AgentRadio를 제시한다.

- **용어·약어 해설**
  - **harness(하네스)**: 모델에 도구, shell, 기억과 실행 loop를 연결하는 agent 실행 기반이다.
  - **primitive(기본 연산)**: 더 복잡한 협업 protocol을 구성하는 최소 동작 단위다.

**S011 — Original**

The last runs as a background task, surfacing teammates' messages without interrupting foreground work, so each agent remains passively aware of its peers and folds new findings into its ongoing task.

**S011 — 한국어**

마지막 연산은 background task로 실행되어 foreground 작업을 중단하지 않고 동료의 메시지를 드러낸다. 그 결과 각 에이전트는 동료를 수동적으로 인지하고 새 발견을 진행 중인 과제에 반영한다.

**S012 — Original**

Under a five-phase protocol of division of labor and negotiation, four agents organized by AgentRadio resolve 62.1% of tasks, 29.8 points above a single agent and above Claude Code with the newer Opus 4.8 (57.2%).

**S012 — 한국어**

분업과 협상의 5단계 protocol에서 AgentRadio로 조직된 네 에이전트는 62.1%의 과제를 해결했다. 단일 에이전트보다 29.8%p 높고, 더 새로운 Opus 4.8을 사용한 Claude Code의 57.2%보다도 높다.

**S013 — Original**

Rubric-level analysis shows the gain growing with task difficulty, consistent with mid-course correction as the underlying mechanism.

**S013 — 한국어**

rubric 수준 분석에서는 과제가 어려워질수록 이득이 커졌으며, 이는 실행 중 경로 수정이 작동 메커니즘이라는 해석과 일치한다.

## 서론과 연구 기여

**S014 — Original**

The tasks handed to LLM agents keep getting longer.

**S014 — 한국어**

LLM 에이전트에게 맡기는 과제는 계속 길어지고 있다.

**S015 — Original**

Benchmarks have moved from single-step question answering to navigating live websites, operating full computer environments, resolving real GitHub issues, carrying out day-long professional work, and replicating entire research papers.

**S015 — 한국어**

benchmark는 한 단계 질문 답변에서 실제 웹사이트 탐색, 완전한 컴퓨터 환경 조작, 실제 GitHub issue 해결, 하루 동안의 전문 업무 수행, 논문 전체 재현으로 이동해 왔다.

**S016 — Original**

Yet an agent's effective attention degrades as its context grows, whether the relevant information changes position, the input merely lengthens, or the interaction stretches over many turns.

**S016 — 한국어**

그러나 관련 정보의 위치가 바뀌든, 입력이 단순히 길어지든, 상호작용이 여러 turn에 걸쳐 늘어나든 문맥이 커질수록 에이전트의 유효한 주의력은 저하된다.

**S017 — Original**

When a single context cannot hold an entire task, the natural remedy is to spread the work across several agents, each starting with a clean context.

**S017 — 한국어**

단일 문맥이 전체 과제를 담을 수 없을 때 자연스러운 해결책은 깨끗한 문맥에서 시작하는 여러 에이전트에게 작업을 분산하는 것이다.

**S018 — Original**

For a long task like codebase understanding, parallel division is intuitively appealing: each agent focuses on a narrower question in a cleaner context.

**S018 — 한국어**

코드베이스 이해 같은 장기 과제에서는 각 에이전트가 더 깨끗한 문맥에서 더 좁은 질문에 집중할 수 있으므로 병렬 분할이 직관적으로 매력적이다.

**S019 — Original**

Yet the subtasks are not independent.

**S019 — 한국어**

그러나 하위 과제들은 독립적이지 않다.

**S020 — Original**

A fact one agent uncovers can redirect what a teammate should be doing.

**S020 — 한국어**

한 에이전트가 밝혀낸 사실은 동료가 해야 할 일을 바꿀 수 있다.

**S021 — Original**

Therefore, negotiation has to happen in real time while the agents are working.

**S021 — 한국어**

따라서 협상은 에이전트들이 작업하는 동안 실시간으로 이루어져야 한다.

**S022 — Original**

Across all of these, an agent that is working cannot also be listening.

**S022 — 한국어**

기존 방식 전반에서는 작업 중인 에이전트가 동시에 듣지 못한다.

**S023 — Original**

To our knowledge, no existing system gives concurrently working agents passive awareness of one another over a lateral, natural-language channel.

**S023 — 한국어**

저자들이 아는 한, 동시에 작업하는 에이전트들이 lateral 자연어 channel을 통해 서로를 수동적으로 인지하게 하는 기존 시스템은 없다.

**S024 — Original**

With AgentRadio, four Claude Code agents outperform one working alone by 29.8 points, a 92% relative gain.

**S024 — 한국어**

AgentRadio를 사용한 네 Claude Code 에이전트는 단독 에이전트보다 29.8%p 높은 성능을 보였으며, 상대 이득은 92%다.

**S025 — Original**

On 124 tasks and 1,306 rubrics, every layer helps on both models, and the passive step alone adds 10.5 points with Opus 4.6 and 11.3 with DeepSeek V4 Pro.

**S025 — 한국어**

124개 과제와 1,306개 rubric에서 모든 계층은 두 모델 모두에 도움을 주었고, 수동 인지 단계만으로 Opus 4.6은 10.5%p, DeepSeek V4 Pro는 11.3%p 증가했다.

**S026 — Original**

The full stack beats compute-matched best-of-6 sampling (37.9% and 31.4% on the Opus 4.6 and DeepSeek V4 Pro).

**S026 — 한국어**

전체 stack은 계산량을 맞춘 best-of-6 sampling을 앞섰다. best-of-6의 성능은 Opus 4.6에서 37.9%, DeepSeek V4 Pro에서 31.4%였다.

## 관련 연구 요약

관련 연구는 멀티에이전트 방식이 항상 유리하지 않음을 강조한다. 분해 가능한 금융 조사에서는 중앙 조정자가 큰 이득을 보였지만, 순차적인 Minecraft 제작 계획에서는 강제 분할이 39.1~70.0% 손실을 냈다. SWE-Atlas QnA는 병렬 탐색으로 나눌 수 있으면서 하위 질문이 상호 의존하고, 단일 agent baseline이 32.3%로 포화와 멀다는 점에서 멀티에이전트에 유리한 조건으로 분류된다. 기존 시스템은 병렬이지만 고립되거나, round 경계에서 동기화되거나, 비동기를 실행 scheduling이나 shared state에만 적용했다. AgentRadio의 차별점은 완성된 coding harness 사이에 lateral 자연어 통신을 추가하고, 작업 중에도 수신 가능하게 만든다는 데 있다.

## AgentRadio 방법

### 통신 primitive

**S027 — Original**

AgentRadio exposes three operations to every agent.

**S027 — 한국어**

AgentRadio는 모든 에이전트에게 세 연산을 제공한다.

**S028 — Original**

`create_thread(name, participants)` opens a named conversation on the message server and returns its identifier.

**S028 — 한국어**

`create_thread(name, participants)`는 message server에서 이름 있는 대화를 열고 그 식별자를 반환한다.

**S029 — Original**

`send_message(thread, content, mentions)` appends a message to a thread and returns immediately, whether or not anyone is listening.

**S029 — 한국어**

`send_message(thread, content, mentions)`는 thread에 메시지를 추가하고 누가 듣고 있는지와 무관하게 즉시 반환한다.

**S030 — Original**

`wait_for_mention(timeout)` blocks until a message mentioning the caller arrives, then returns that message together with a full snapshot of every thread, so the caller never needs a second read to reconstruct context.

**S030 — 한국어**

`wait_for_mention(timeout)`은 호출자를 mention한 메시지가 도착할 때까지 대기한 뒤, 그 메시지와 모든 thread의 전체 snapshot을 함께 반환한다. 따라서 호출자가 문맥을 복원하기 위해 다시 읽을 필요가 없다.

**S031 — Original**

Run in the foreground, it is a blocking receive: the agent stops working in order to listen, which is our blocking baseline.

**S031 — 한국어**

foreground에서 실행하면 이는 blocking receive가 된다. 에이전트는 듣기 위해 작업을 멈추며, 이것이 논문의 blocking baseline이다.

**S032 — Original**

Run as a background task of the harness, it becomes passive awareness: the agent keeps working, and any mention surfaces at the next step boundary.

**S032 — 한국어**

harness의 background task로 실행하면 passive awareness가 된다. 에이전트는 계속 작업하고 mention은 다음 step 경계에서 드러난다.

**S033 — Original**

Everything else, the primitives, the threads, the protocol, stays fixed.

**S033 — 한국어**

primitive, thread, protocol 등 다른 모든 것은 고정된다.

**S034 — Original**

This single-bit difference is what our experiments isolate.

**S034 — 한국어**

실험이 분리해 측정하는 것은 바로 이 한 bit의 차이다.

**S035 — Original**

Blocking receive makes listening a step of its own: M grows only when a step is spent on `wait_for_mention`, so every message heard costs a step of work.

**S035 — 한국어**

blocking receive에서는 듣기가 독립된 step이다. `wait_for_mention`에 step을 쓸 때만 메시지 집합 M이 커지므로, 메시지를 들을 때마다 작업 step 하나를 소비한다.

**S036 — Original**

Passive awareness decouples the two: M(t) contains every message sent before s_t, and no step is spent listening.

**S036 — 한국어**

passive awareness는 둘을 분리한다. `M(t)`는 `s_t` 전에 보낸 모든 메시지를 포함하며, 듣기에 step을 소비하지 않는다.

### 5단계 protocol

**S037 — Original**

We evaluate AgentRadio under a fixed protocol of division of labor and negotiation.

**S037 — 한국어**

저자들은 고정된 분업·협상 protocol 아래에서 AgentRadio를 평가한다.

**S038 — Original**

One agent, agent-1, additionally serves as the assembler.

**S038 — 한국어**

agent-1은 추가로 assembler 역할을 맡는다.

**S039 — Original**

It opens the planning, worklog, and final-answer threads and gates every transition: a phase ends only after agent-1 collects an explicit approval from every agent.

**S039 — 한국어**

assembler는 planning, worklog, final-answer thread를 열고 모든 전환을 통제한다. agent-1이 모든 에이전트의 명시적 승인을 모아야 단계가 끝난다.

**S040 — Original**

Every agent starts its background watcher, independently explores the repository, and drafts the sub-questions it sees.

**S040 — 한국어**

모든 에이전트는 background watcher를 시작하고 repository를 독립적으로 탐색해 자신이 발견한 하위 질문의 초안을 만든다(P1).

**S041 — Original**

The agents pool their Phase-1 findings, negotiate a partition of the sub-questions, and revise it until every agent approves.

**S041 — 한국어**

에이전트들은 P1의 발견을 모아 하위 질문 분할안을 협상하고 모든 에이전트가 승인할 때까지 수정한다(P2).

**S042 — Original**

Under passive awareness, a discovery triggers a worklog post at the moment it is made: a finding that bears on a teammate's sub-question, a contradiction with the agreed plan, an obstacle, or an abandoned dead end.

**S042 — 한국어**

passive awareness에서는 발견한 즉시 worklog 게시가 일어난다. 동료의 하위 질문과 관련된 사실, 합의된 계획과의 충돌, 장애물 또는 포기한 막다른 길이 그 대상이다(P3).

**S043 — Original**

Each agent broadcasts its findings with evidence in its own results thread.

**S043 — 한국어**

각 에이전트는 자기 results thread에서 증거와 함께 발견 내용을 broadcast한다(P4).

**S044 — Original**

The assembler composes the final answer from the approved results, broadcasts the draft for a last round of approvals, and submits.

**S044 — 한국어**

assembler는 승인된 결과로 최종 답을 구성하고, 마지막 승인 round를 위해 초안을 broadcast한 뒤 제출한다(P5).

### 구현

**S045 — Original**

The message server is a standalone process that stores threads, messages, and mentions for a group of agents and implements the three primitives.

**S045 — 한국어**

message server는 에이전트 그룹의 thread, message와 mention을 저장하고 세 primitive를 구현하는 독립 프로세스다.

**S046 — Original**

On the harness side the requirements stay minimal: the harness must only be able to run a shell command as a background task, which mainstream coding harnesses already provide, and the harness itself is never modified.

**S046 — 한국어**

harness 측 요구 사항은 최소한이다. 주류 coding harness가 이미 제공하는 shell command background 실행 기능만 있으면 되며 harness 자체는 수정하지 않는다.

**S047 — Original**

Switching from blocking to passive receive therefore adds no LLM calls, because the watcher is an ordinary operating-system process rather than an agent step: the only new tokens an agent pays for are the messages that surface.

**S047 — 한국어**

따라서 blocking에서 passive receive로 바꾸어도 LLM 호출은 추가되지 않는다. watcher가 agent step이 아니라 일반 운영체제 프로세스이기 때문이다. 추가 token 비용은 에이전트에게 실제로 드러난 메시지뿐이다.

## 실험과 결과

**S048 — Original**

All experiments run on the 124 tasks of SWE-Atlas QnA under the benchmark's rules.

**S048 — 한국어**

모든 실험은 benchmark 규칙에 따라 SWE-Atlas QnA의 124개 과제에서 실행된다.

**S049 — Original**

Task accuracy counts a task as resolved only when every one of its rubrics passes.

**S049 — 한국어**

task accuracy는 해당 과제의 모든 rubric이 통과할 때만 해결된 과제로 센다.

**S050 — Original**

Rubric pass rate counts the share of all 1,306 rubrics passed and moves in finer steps.

**S050 — 한국어**

rubric pass rate는 전체 1,306개 rubric 중 통과한 비율이며 더 세밀하게 변한다.

**S051 — Original**

B0 is a single Claude Code agent.

**S051 — 한국어**

B0는 단일 Claude Code 에이전트다.

**S052 — Original**

B1 repeats B0 six times independently, spending six single-agent budgets, and reports the best of the six complete runs.

**S052 — 한국어**

B1은 B0를 독립적으로 6회 반복해 단일 에이전트 예산의 6배를 쓰고, 완료된 여섯 실행 중 최고 결과를 보고한다.

**S053 — Original**

L1 moves to a team of four Claude Code agents and adds division of labor.

**S053 — 한국어**

L1은 네 Claude Code 에이전트 팀으로 바꾸고 분업을 추가한다.

**S054 — Original**

L2 adds negotiation: every agent first explores independently and publishes its initial findings, one agent then proposes the partition, the team reviews it until everyone approves, and the results are cross-reviewed at the end.

**S054 — 한국어**

L2는 협상을 추가한다. 각 에이전트가 먼저 독립적으로 탐색해 초기 발견을 공개하고, 한 에이전트가 분할안을 제안하며, 전원이 승인할 때까지 팀이 검토하고, 마지막에는 결과를 교차 검토한다.

**S055 — Original**

L3 runs the same protocol under passive awareness, which is the full AgentRadio configuration.

**S055 — 한국어**

L3는 같은 protocol을 passive awareness에서 실행하며, 이것이 완전한 AgentRadio 구성이다.

**S056 — Original**

The step from L2 to L3 changes only the communication mode.

**S056 — 한국어**

L2에서 L3로 갈 때 바뀌는 것은 통신 방식뿐이다.

**S057 — Original**

Division alone lifts the single agent by 7.2 points with Opus 4.6 and 2.4 with DeepSeek.

**S057 — 한국어**

분업만 추가해도 단일 에이전트보다 Opus 4.6은 7.2%p, DeepSeek는 2.4%p 높아진다.

**S058 — Original**

Negotiation adds another 12.1 and 8.1.

**S058 — 한국어**

협상은 각각 12.1%p와 8.1%p를 더한다.

**S059 — Original**

Passive awareness adds a further 10.5 and 11.3.

**S059 — 한국어**

passive awareness는 다시 10.5%p와 11.3%p를 추가한다.

**S060 — Original**

The passive increment is the step our design isolates, and it is statistically solid on the paired task outcomes of the McNemar row.

**S060 — 한국어**

설계가 분리해 측정한 것은 수동 인지의 증가분이며, paired task outcome에 대한 McNemar 검정에서도 통계적으로 유의하다.

- **용어·약어 해설**
  - **McNemar test(McNemar 검정)**: 같은 과제에 적용한 두 시스템의 성공/실패가 서로 다른 경우, 한쪽 방향의 개선이 대칭적 우연인지 검정한다.

**S061 — Original**

The full stack spends $19.45 per task with Opus 4.6 and $2.46 with DeepSeek, about six times a single agent's spend, so the gains could in principle come from budget rather than coordination.

**S061 — 한국어**

전체 stack은 과제당 Opus 4.6에서 19.45달러, DeepSeek에서 2.46달러를 쓰며 단일 에이전트 비용의 약 6배이므로, 원칙적으로 이득이 조정이 아니라 예산에서 왔을 가능성이 있다.

**S062 — Original**

B1 tests this.

**S062 — 한국어**

B1은 이 가능성을 검증한다.

**S063 — Original**

At essentially the same spend the full stack returns a further 24.2 and 19.4 points.

**S063 — 한국어**

거의 같은 비용에서 전체 stack은 best-of-6보다 각각 24.2%p와 19.4%p 더 높은 결과를 낸다.

**S064 — Original**

Four Opus 4.6 agents under AgentRadio also surpass a single agent running the newer Opus 4.8, 62.1% against 57.2%.

**S064 — 한국어**

AgentRadio 아래의 네 Opus 4.6 에이전트는 더 새로운 Opus 4.8을 쓰는 단일 에이전트도 62.1% 대 57.2%로 앞선다.

## 분석과 사례

**S065 — Original**

Division is the noisiest step.

**S065 — 한국어**

분업은 가장 변동이 큰 단계다.

**S066 — Original**

It gains 84 rubrics that the single agent misses and loses 59 that the single agent passes, a net of +25.

**S066 — 한국어**

단일 에이전트가 놓친 rubric 84개를 얻지만 단일 에이전트가 통과한 59개를 잃어 순증가는 25개다.

**S067 — Original**

Negotiation is the largest and the cleanest contributor.

**S067 — 한국어**

협상은 가장 크고 가장 안정적인 기여 요소다.

**S068 — Original**

It adds 100 gross rubrics against 33 lost, a net of +67.

**S068 — 한국어**

rubric 100개를 얻고 33개를 잃어 순증가는 67개다.

**S069 — Original**

Passive awareness gains 47 rubrics and loses 23, a net of +24.

**S069 — 한국어**

passive awareness는 rubric 47개를 얻고 23개를 잃어 순증가는 24개다.

**S070 — Original**

A message that arrives mid-execution can pull an agent off a line of evidence that would have passed a rubric, but the gains outweigh these losses.

**S070 — 한국어**

실행 중 도착한 메시지는 에이전트를 원래 통과했을 증거 경로에서 벗어나게 만들 수 있지만, 이득이 손실보다 크다.

**S071 — Original**

The harder the task is for the blocking protocol, the more passive awareness contributes.

**S071 — 한국어**

blocking protocol에 어려운 과제일수록 passive awareness의 기여가 커진다.

**S072 — Original**

Passive awareness turns discoveries that agents already make, and would otherwise swallow, into team-wide evidence.

**S072 — 한국어**

passive awareness는 에이전트가 이미 만들었지만 원래라면 공유하지 않았을 발견을 팀 전체의 증거로 바꾼다.

**S073 — Original**

It cannot supply a conception that no agent forms.

**S073 — 한국어**

그러나 어떤 에이전트도 형성하지 못한 개념을 새로 공급할 수는 없다.

## 결론

**S074 — Original**

We presented AgentRadio, an asynchronous message-passing layer that equips coding-agent harnesses with three primitives and one new capability: run as a background task, the wait primitive keeps an agent passively aware of its teammates.

**S074 — 한국어**

저자들은 coding-agent harness에 세 primitive와 하나의 새로운 능력을 주는 비동기 메시지 전달 계층 AgentRadio를 제시했다. wait primitive를 background task로 실행하면 에이전트가 동료를 수동적으로 인지한다.

**S075 — Original**

Under a five-phase protocol of division of labor and negotiation, four Claude Code agents organized by AgentRadio raise task accuracy on SWE-Atlas QnA from 32.3% to 62.1% with Opus 4.6 and from 29.0% to 50.8% with DeepSeek V4 Pro.

**S075 — 한국어**

분업과 협상의 5단계 protocol에서 AgentRadio로 조직된 네 Claude Code 에이전트는 SWE-Atlas QnA task accuracy를 Opus 4.6에서 32.3%에서 62.1%로, DeepSeek V4 Pro에서 29.0%에서 50.8%로 높였다.

**S076 — Original**

The passive step survives a paired significance test on both models and pays most where blocking misses worst.

**S076 — 한국어**

수동 인지 단계는 두 모델 모두에서 paired significance test를 통과했으며 blocking 방식이 가장 크게 실패하는 곳에서 가장 큰 효과를 냈다.

**S077 — Original**

It changes neither the model, the harness, nor the protocol, only when agents can hear one another, a single degree of freedom worth more than a model generation.

**S077 — 한국어**

이는 모델, harness, protocol을 바꾸지 않고 에이전트들이 서로를 들을 수 있는 시점만 바꾼다. 저자들의 실험에서는 이 단일 자유도가 모델 한 세대의 차이보다 더 큰 가치가 있었다.

## 표·그림 읽기

- **그림 1**: 단일 Opus 4.6 32.3%, AgentRadio 62.1%, 단일 Opus 4.8 57.2%; 단순 모델 세대 비교가 아니라 팀 구성과 단일 실행의 비교임을 유의한다.
- **그림 2/알고리즘 1**: watcher와 foreground가 분리되고, 네 agent lane이 P1~P5를 통과한다. 실행 중 메시지는 명령을 끊지 않고 다음 step에서 반영된다.
- **표 1**: B0→L1→L2→L3의 동일 task paired ladder다. L3-L2가 passive awareness의 가장 직접적인 효과다.
- **표 2**: 정확도만 아니라 API 비용을 함께 비교한다. B1은 coordination과 compute 증가를 구분하기 위한 대조군이다.
- **표 3**: 30-task subset 3회 실행에서 순서가 유지되지만 전체 124-task 반복은 아니므로 분산 추정 범위가 제한적이다.
- **그림 4**: 각 layer의 순증가 뒤에는 gain과 loss가 동시에 있다. 평균 성능만 보고 개별 task 퇴행을 숨기면 안 된다.
- **그림 5**: L2가 더 많은 rubric을 놓친 task일수록 L3의 task당 gain이 커진다.
- **그림 6/7**: MinIO는 기존 발견의 공유가 성공한 사례, Grafana는 누구도 필요한 개념을 만들지 못해 통신이 도움을 주지 못한 경계 사례다.

## 약어 및 기술 용어 사전

| 원어 | 한국어 | 이 논문에서의 의미 | 최초 등장 |
|---|---|---|---|
| LLM | 대규모 언어 모델 | coding agent의 추론 엔진 | S002 |
| long-horizon task | 장기 실행 과제 | 다수의 도구 호출과 긴 문맥이 필요한 작업 | S002 |
| harness | 하네스 | 모델과 shell·도구·기억을 연결하는 실행 기반 | S010 |
| primitive | 기본 연산 | thread·message·mention 대기 연산 | S010 |
| passive awareness | 수동 인지 | foreground를 멈추지 않고 동료 메시지를 알게 되는 능력 | S011 |
| thread | 스레드 | 이름과 참여자를 가진 공유 대화 | S010 |
| mention | 멘션 | 특정 agent에게 전달되는 메시지 알림 | S010 |
| blocking receive | 차단 수신 | 듣기 위해 foreground step을 소비하는 수신 | S031 |
| step boundary | 단계 경계 | 한 tool call이 끝나고 다음 agent step이 시작되는 지점 | S032 |
| SWE-Atlas QnA | SWE-Atlas 질의응답 | production codebase 이해 benchmark | S003 |
| rubric | 채점 기준 | task 답변이 만족해야 하는 원자적 사실 문장 | S025 |
| ablation | 절제 실험 | 구성 요소를 한 단계씩 바꾸는 인과 비교 | S025 |
| McNemar test | McNemar 검정 | paired binary outcome의 비대칭을 검정하는 방법 | S060 |
| assembler | 조립자 | thread와 phase gate, 최종 답을 관리하는 agent-1 | S038 |

## 번역 검수 기록

- 2026-08-11: arXiv v1 PDF 9쪽을 pypdf로 추출하고 110 DPI PNG로 전 페이지 시각 대조했다.
- 다단 편집의 열 순서, 페이지 7~8에 걸친 결론 문장, 표 1~3 수치와 그림 4~7 caption을 확인했다.
- PDF 렌더링 중 Symbol/ArialUnicode display font 경고가 있었으나 수식·도표·본문은 육안 판독 가능했고, 메타데이터와 텍스트 추출로 특수 문자를 교차 확인했다.
- related work는 부분 번역임을 범위 표에 표시했으며 참고문헌 bibliographic record는 번역하지 않았다.
