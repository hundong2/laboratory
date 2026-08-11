# AgentRadio: 장기 실행 멀티에이전트 협업의 수동 인지

작성일: 2026-08-11

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [연구 질문과 핵심 기여](#연구-질문과-핵심-기여)
- [AgentRadio의 작동 방식](#agentradio의-작동-방식)
- [실험 설계](#실험-설계)
- [핵심 결과](#핵심-결과)
- [해석과 한계](#해석과-한계)
- [재현 시 주의점](#재현-시-주의점)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 논문: [AgentRadio: Passive Awareness for Long-Horizon Multi-Agent Collaboration](https://arxiv.org/abs/2607.28430)
- PDF: [arXiv PDF](https://arxiv.org/pdf/2607.28430)
- 식별자: arXiv:2607.28430v1, DOI `10.48550/arXiv.2607.28430`
- 저자: Xinxing Ren, Qianbo Zang, Ziyan Wang, Caelum Forder, Suman Deb, Peter Carroll, Zekun Guo
- 버전/게시일: v1, 2026-07-30
- 원문 언어: 영어
- 라이선스: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- 접근일: 2026-08-11
- 확인 범위: 9쪽 PDF 전체. 본문, 표 3개, 그림 7개, 알고리즘 1개와 참고문헌을 확인했다.

문장 대조 번역은 [논문 번역본](<AgentRadio - Passive Awareness for Long-Horizon Multi-Agent Collaboration.번역.md>)에서 읽을 수 있다. 핵심 본문은 문장별로 번역했으며, 관련 연구와 참고문헌은 저작물의 구조를 보존하면서 학습용 요약으로 정리했다.

## 한눈에 보기

장시간 코드베이스 조사에서는 여러 에이전트가 일을 나누더라도 한 에이전트의 발견이 다른 에이전트의 조사 방향을 바꿀 수 있다. 기존 방식은 통신을 위해 작업을 멈추거나 정해진 단계가 끝날 때까지 기다린다. AgentRadio는 다음 세 연산을 제공한다.

1. `create_thread`: 이름 있는 대화 스레드 생성
2. `send_message`: 수신자를 기다리지 않고 메시지 전송
3. `wait_for_mention`: 자신을 언급한 메시지를 기다리고 전체 스레드 snapshot 반환

핵심은 세 번째 연산을 에이전트의 foreground step이 아니라 운영체제 background task로 실행하는 것이다. 메시지는 실행 중인 명령을 중단하지 않고 다음 작업 경계에서 드러난다. 논문은 이를 **수동 인지(passive awareness)**라고 부른다.

## 기초 개념

### 장기 실행 에이전트

여러 파일 탐색, 빌드, 실제 데이터 실행, 추적과 증거 종합처럼 수십 분 동안 많은 도구 호출이 필요한 에이전트다. 문맥이 길어질수록 중요한 정보의 위치와 상호작용 길이에 따른 주의력 저하가 문제가 된다.

### 비동기 메시지 전달

송신자와 수신자가 동시에 통신 단계에 들어갈 필요가 없는 방식이다. `send_message`는 즉시 돌아오며, 수신 에이전트는 작업을 계속한다.

### blocking receive와 passive awareness

- **blocking receive**: 메시지를 듣는 행위가 독립된 foreground step이다. 듣는 동안 실제 작업을 못 한다.
- **passive awareness**: 별도 watcher가 mention을 기다린다. 에이전트는 작업을 계속하고 다음 step 경계에서 새 정보를 받는다.

논문의 형식화에서 에이전트 step을 `s1, s2, ...`, step `s_t`에서 보이는 메시지 집합을 `M(t)`라고 한다. blocking 방식에서는 `wait_for_mention`에 step을 써야만 `M`이 커진다. passive 방식에서는 `s_t` 이전에 전송된 메시지가 `M(t)`에 들어오며 듣기 전용 step이 필요 없다.

## 연구 질문과 핵심 기여

연구 질문은 “작업 중 lateral 자연어 통신을 비차단으로 노출하면, 모델이나 에이전트 harness를 바꾸지 않고 장기 코드 이해 성능을 높일 수 있는가?”이다.

핵심 기여는 다음과 같다.

- 기존 coding-agent harness에 붙일 수 있는 비동기 메시지 계층과 세 가지 primitive를 제안한다.
- 네 에이전트가 탐색·분할·실행·검토·제출하는 5단계 프로토콜을 설계한다.
- 두 모델에서 한 조정 요소씩 바꾸는 B0/B1/L1/L2/L3 ablation으로 수동 인지의 독립 효과를 측정한다.
- 124개 과제, 1,306개 rubric에서 난이도별 이득, rubric gain/loss와 실제 중간 경로 수정 사례를 분석한다.

## AgentRadio의 작동 방식

```text
agent foreground:  조사 step -> 도구 실행 -> 다음 step -> ...
background watcher:          wait_for_mention -> 새 mention 저장
message server:     thread / message / mention 상태 유지
                                  |
                                  +-> 다음 step 경계에서 foreground에 노출
```

메시지 서버는 독립 프로세스이며 각 harness는 얇은 shell script 세 개로 접근한다. watcher는 LLM 호출이 아닌 운영체제 프로세스이므로 passive receive 자체가 에이전트 step이나 추가 LLM 호출을 소비하지 않는다. 새 토큰 비용은 실제로 노출되는 메시지에서 발생한다.

### 5단계 프로토콜

| 단계 | 이름 | 핵심 동작 |
|---|---|---|
| P1 | Explore | 네 에이전트가 독립 탐색하고 하위 질문 후보를 만든다. |
| P2 | Divide | assembler가 planning thread를 열고 전원 승인까지 분할안을 협상한다. |
| P3 | Execute | 각자 하위 질문을 조사하며 관련 발견·계획 충돌·장애물을 즉시 worklog에 보낸다. |
| P4 | Review | 각자 증거가 붙은 결과를 게시하고 사실 충돌이나 얇은 증거를 교차 검토한다. |
| P5 | Submit | assembler가 최종안을 작성하고 네 명의 승인을 받은 뒤 제출한다. |

## 실험 설계

### 평가 대상

SWE-Atlas QnA의 124개 질문과 1,306개 rubric을 사용한다. 질문은 11개 production repository, 4개 언어에 걸쳐 있으며 단순 정적 검색만으로 풀 수 없도록 빌드·실행·실제 데이터·실행 추적을 요구한다. 모든 rubric을 통과해야 한 task가 해결된 것으로 센다.

### 비교 구성

| 구성 | 의미 |
|---|---|
| B0 | 단일 Claude Code agent |
| B1 | 단일 agent를 6회 독립 실행하고 best-of-6 선택 |
| L1 | 4 agents + division of labor |
| L2 | L1 + 사전 협상과 사후 교차 검토, blocking receive |
| L3 | L2와 같은 프로토콜 + passive awareness, 완전한 AgentRadio |

모든 비교는 같은 task, harness와 모델 설정에서 한 조정 요소씩 바꾸는 paired comparison이다. Claude Opus 4.6과 open-source model DeepSeek V4 Pro에서 같은 ladder를 반복했다.

## 핵심 결과

| 모델 | B0 | L1 | L2 | L3 | L3 - L2 |
|---|---:|---:|---:|---:|---:|
| Opus 4.6 task accuracy | 32.3% | 39.5% | 51.6% | **62.1%** | +10.5%p |
| DeepSeek V4 Pro task accuracy | 29.0% | 31.4% | 39.5% | **50.8%** | +11.3%p |
| Opus 4.6 rubric pass rate | 84.2% | 86.1% | 91.3% | **93.1%** | +1.8%p |
| DeepSeek V4 Pro rubric pass rate | 81.2% | 83.7% | 85.9% | **90.2%** | +4.3%p |

- L3 대 L2 exact McNemar 결과는 Opus 4.6에서 15승 2패, `p=0.0023`; DeepSeek V4 Pro에서 17승 3패, `p=0.0026`이다.
- Opus 4.6의 L3 비용은 task당 $19.45로 B0의 약 6.6배다. 비슷한 비용의 B1($17.76)은 37.9%에 그쳐, 단순 계산량만으로 L3 결과를 설명하기 어렵다.
- 수동 인지는 Opus 4.6 rubric 47개를 새로 얻고 23개를 잃어 순증가가 24개였다. 메시지는 이득만 주지 않으며 기존 증거 경로에서 주의를 돌리는 손실도 만든다.
- L2가 rubric 5개를 놓친 어려운 task에서는 passive awareness가 task당 평균 2.0개 rubric을 추가했다. 쉬운 near-miss보다 경계 횡단 증거가 많은 어려운 문제에서 이득이 커졌다.

## 해석과 한계

### 무엇을 보여 주는가

MinIO 사례에서 두 계획 모두 server-side logging을 빠뜨렸다. blocking 구성에서는 agent가 정확한 설정을 찾아도 공유하지 않아 11/16에 머물렀지만 passive 구성은 실행 중 발견을 즉시 공유해 16/16을 기록했다. 이는 이미 한 agent가 만들어 낸 발견을 팀 전체 증거로 전환하는 메커니즘을 보여 준다.

### 무엇을 보여 주지 못하는가

- Grafana 사례에서는 어느 agent도 필요한 부정 명제인 “자동으로 선택되지 않는다”를 형성하지 못해 L2와 L3가 모두 5/9였다. 통신은 존재하지 않는 통찰을 만들어 내지 못한다.
- 주요 결과는 SWE-Atlas QnA라는 하나의 codebase-understanding benchmark에 집중한다.
- 4-agent protocol, 지정 모델, 특정 harness와 prompt에 대한 결과이므로 agent 수와 다른 환경에 그대로 일반화할 수 없다.
- 비용은 API 가격과 모델 제공 조건에 따라 바뀐다. 논문의 수치는 2026-07-30 버전의 실험 기록이다.
- L3도 23개 rubric을 잃었다. 메시지 우선순위, 품질 제어와 attention disruption은 후속 설계 과제다.
- 논문은 preprint v1이며 동료평가를 거친 최종 출판본으로 확인되지 않았다.

## 재현 시 주의점

정확한 재현에는 논문의 공개 코드, commit-pinned benchmark image, 동일 모델·temperature·thinking effort, judge와 prompt가 필요하다. 공개 코드가 있어도 상용 모델 snapshot이나 가격이 달라지면 수치가 같지 않을 수 있다. 이 폴더의 notebook은 핵심 메커니즘과 공개 표의 통계를 작은 규모로 검증하는 **toy reproduction**이며 원 논문 결과의 재현을 주장하지 않는다.

재현 보고 시 다음을 함께 기록한다.

- 모델의 정확한 이름과 snapshot, harness version
- agent 수, foreground/background 실행 방식
- thread와 mention 전달 순서, step boundary 정의
- task별 random seed, 실패·timeout 처리
- 모든 task 결과와 rubric-level paired outcome
- token/API 비용과 wall-clock latency

## 실습 학습 가이드

1. [01_foundations.ipynb](01_foundations.ipynb): blocking과 passive message delivery의 step 비용 비교
2. [02_practice.ipynb](02_practice.ipynb): 5단계 protocol과 전원 승인 gate를 작은 상태 기계로 구현
3. [03_advanced.ipynb](03_advanced.ipynb): 공개 ablation 표, exact McNemar 검정과 비용 효율 분석

세 notebook은 Python 표준 라이브러리만 사용한다.

## 다음 학습 경로

1. actor model, message queue와 event loop로 비동기 시스템의 기본을 학습한다.
2. paired experiment, ablation, McNemar test로 동일 task에서 시스템 변경의 효과를 측정한다.
3. 메시지 중요도·중복 제거·provenance를 추가해 attention disruption을 줄이는 설계를 실험한다.
4. 순차성이 강한 task와 분해 가능한 task에서 같은 protocol을 비교해 멀티에이전트가 손해가 되는 경계를 찾는다.
5. 공개 [AgentRadio 코드](https://github.com/Coral-Protocol/AgentRadio)를 논문의 version과 대조해 실제 server·shell primitive 구현을 검토한다.
