# .NET Agent Skills 정식 출시

작성일: 2026-07-27

## 출처와 작업 범위

- 원문: [Agent Skills for .NET Is Now Released](https://devblogs.microsoft.com/agent-framework/agent-skills-for-net-is-now-released/)
- 게시일: 2026-07-07
- 저자: Sergey Menshykh, Principal Software Engineer
- 원문 언어: 영어
- 최종 URL: `https://devblogs.microsoft.com/agent-framework/agent-skills-for-net-is-now-released/`
- 접근일: 2026-07-27
- 보조 자료:
  - [Microsoft Learn - Agent Skills](https://learn.microsoft.com/en-us/agent-framework/agents/skills)
  - [Microsoft Agent Framework GitHub](https://github.com/microsoft/agent-framework)
  - [Agent Skills specification](https://agentskills.io/)

이 폴더는 블로그 원문의 구조를 따른 [한국어 번역 요약](translation.ko.md), 개념 분석, C# 실습을 제공한다. API와 NuGet package는 변경될 수 있으므로 버전 관련 설명은 접근일 기준이다.

## 한눈에 보기

Microsoft Agent Framework의 .NET Agent Skills API가 experimental preview를 벗어났다. `[Experimental]` attribute가 제거됐으며, 팀은 지침·참고 문서·script를 독립적인 skill package로 만들고 여러 agent에서 재사용할 수 있다.

이번 발표의 핵심은 “skill을 만들 수 있다”보다 “운영 환경에서 통제할 수 있다”에 있다.

- Agent는 필요한 skill만 단계적으로 불러 context 사용량을 줄인다.
- File, class, inline code의 세 방식으로 skill을 작성한다.
- `load_skill`, `read_skill_resource`, `run_skill_script`는 기본적으로 승인이 필요하다.
- File script 실행은 사용자가 제공한 runner에 위임되므로 sandbox와 제한을 직접 설계한다.
- Filter, cache와 공개 source pipeline으로 tenant·agent별 노출 범위를 통제한다.

> 안정화 범위 주의: 일반 .NET Agent Skills API는 정식 출시됐지만 Microsoft Learn이 설명하는 MCP skill source는 여전히 experimental API다. “Agent Skills 전체의 모든 integration이 안정화됐다”고 확대 해석하면 안 된다.

## 기초 개념

### Agent Skill이란?

Agent Skill은 특정 업무 영역을 처리하는 데 필요한 다음 요소를 하나로 묶은 이식 가능한 package다.

- 지침: 판단 규칙, 단계, 예외 처리와 출력 형식
- 참고 자료: 정책, FAQ, template, 표와 schema
- 선택적 script: 검증, 변환, 조회 같은 실행 코드
- metadata: 이름, 설명, license, compatibility와 사용자 정의 항목

도구(tool)가 “한 번 호출할 수 있는 행동”이라면 skill은 “한 업무 영역을 처리하는 지식과 자원”에 가깝다.

### Progressive disclosure

```text
1. Advertise  -> 이름과 설명만 agent에 알림
2. Load       -> 작업이 맞을 때 SKILL.md 지침 로드
3. Read       -> 필요한 reference·asset만 읽기
4. Run        -> 필요하고 승인된 script만 실행
```

모든 정책 문서를 system prompt에 항상 넣지 않으므로 context를 아낄 수 있다. 반대로 description이 모호하면 agent가 적절한 skill을 선택하지 못하므로 이름과 설명이 routing 계약의 일부가 된다.

## Skill 구조

```text
skills/
└── expense-report/
    ├── SKILL.md
    ├── references/
    │   └── POLICY.md
    ├── assets/
    │   └── report-template.md
    └── scripts/
        └── validate.csx
```

`SKILL.md`는 YAML frontmatter와 Markdown 지침으로 구성한다.

```md
---
name: expense-report
description: 회사 경비 규정에 따라 경비 보고서를 검토한다. 환급, 지출 한도, 제출 절차 질문에 사용한다.
license: Proprietary
compatibility: Contoso 내부 정책 저장소 접근 필요
metadata:
  owner: finance-platform
  version: "2.1"
---

# 경비 보고서 검토

1. references/POLICY.md에서 해당 비용 범주를 확인한다.
2. 불명확한 영수증은 승인하지 말고 추가 정보를 요청한다.
3. 지급 전에는 사람의 최종 승인을 요구한다.
```

이름은 lowercase letter, number, hyphen을 사용하고 directory 이름과 맞춰야 한다. Description에는 무엇을 하는지뿐 아니라 언제 사용해야 하는지까지 넣는다.

## 세 가지 작성 방식

| 방식 | 적합한 상황 | 장점 | 주의점 |
|---|---|---|---|
| File-based | 비개발자와 공동 관리, shared repository | Markdown 중심, diff와 review 용이 | file trust, path, script sandbox 필요 |
| Class-based | NuGet package 배포, typed DI와 재사용 | C# type·attribute·package workflow 활용 | in-process script의 권한 경계 검토 |
| Code-defined | runtime 생성, closure·session state 사용 | 동적 resource와 delegate script | application code와 skill 변경이 결합 |

모든 방식은 `AgentSkillsProvider` 뒤에서 같은 runtime interface로 agent에 노출된다.

## 핵심 구성 요소

### Provider

`AgentSkillsProvider`는 skill 목록을 system context에 광고하고 세 가지 tool을 등록한다.

- `load_skill`
- `read_skill_resource`
- `run_skill_script`

### Source

Skill은 filesystem, `AgentInlineSkill`, `AgentClassSkill<T>`, MCP source 등에서 올 수 있다.

### Builder

`AgentSkillsProviderBuilder`는 여러 source를 조합하고 deduplication, caching, filtering을 적용한다.

```csharp
var provider = new AgentSkillsProviderBuilder()
    .UseFileSkill(Path.Combine(AppContext.BaseDirectory, "skills"))
    .UseSkill(inlineSkill)
    .UseFilter(context => IsAllowedForTenant(context))
    .Build();
```

구체적인 overload와 filter context는 설치한 package 버전의 API 문서를 확인해야 한다.

## 기본 연결 흐름

공식 블로그 예시는 Azure OpenAI Responses client와 file skill provider를 결합한다.

```csharp
var skillsProvider = new AgentSkillsProvider(
    Path.Combine(AppContext.BaseDirectory, "skills"),
    SubprocessScriptRunner.RunAsync);

AIAgent agent = new AzureOpenAIClient(
        new Uri(endpoint),
        new DefaultAzureCredential())
    .GetResponsesClient()
    .AsAIAgent(
        new ChatClientAgentOptions
        {
            Name = "MyAgent",
            ChatOptions = new() { Instructions = "You are a helpful assistant." },
            AIContextProviders = [skillsProvider],
        },
        model: deploymentName);
```

실제 실행에는 model provider에 맞는 package와 인증이 필요하다. 운영 환경에서는 `DefaultAzureCredential`의 여러 fallback을 무심코 허용하기보다 Managed Identity처럼 의도한 credential을 명확히 선택하는 편이 안전하다.

## 운영 통제

### Human-in-the-loop

세 skill tool은 기본적으로 approval 대상이다. 신뢰가 확인된 읽기 작업만 자동 승인하고, script 실행이나 외부 변경은 별도 승인을 유지하는 방식이 안전하다.

### Script 실행 경계

- Class-based와 code-defined script는 process 안에서 delegate로 실행된다.
- File-based script는 제공한 runner가 실행한다.
- 기본 `SubprocessScriptRunner`는 데모에 편리하지만 production sandbox가 아니다.

운영 runner에는 다음이 필요하다.

- 허용 확장자·directory·script hash allowlist
- 별도 identity와 최소 filesystem/network 권한
- CPU, memory, output size와 wall-clock timeout
- 인자 schema 검증과 shell string 결합 금지
- stdout/stderr, exit code, actor, tenant, skill version audit
- container 또는 격리 process

### Filtering

하나의 shared skill library를 모든 agent와 tenant에 그대로 노출하지 않는다. Role, tenant, data classification, deployment stage를 기준으로 노출 대상을 결정한다.

### Caching

Skill resolution 결과를 재사용해 성능을 높일 수 있다. Tenant별 다른 skill set을 제공하면 cache key에도 tenant와 policy version을 포함해 서로의 metadata가 섞이지 않게 한다.

## Skill과 Workflow 선택

| 질문 | Skill | Workflow |
|---|---|---|
| 실행 순서를 AI가 적응적으로 정해도 되는가? | 적합 | 명시적 순서가 필요하면 부적합 |
| 실패 후 중간 지점에서 재개해야 하는가? | 한 turn 재시도 중심 | checkpoint·resume에 적합 |
| 결제·메일 발송 같은 side effect가 있는가? | 낮은 위험·idempotent 작업 | 고위험 side effect에 적합 |
| 업무가 하나의 집중된 domain인가? | 적합 | 여러 agent·승인·단계 조정에 적합 |

판단의 핵심은 “AI가 방법을 선택해도 되는가”와 “실행 순서를 반드시 보장해야 하는가”다.

## 일반적인 사용 사례

- HR·경비·보안 정책을 한 번 작성해 여러 employee agent에서 재사용
- Support playbook을 단계·자료·진단 script와 함께 package화
- 팀별 skill을 내부 NuGet 또는 shared repository로 독립 배포
- Tenant와 role에 맞는 skill subset만 노출
- 정책 답변에 사용한 skill version과 reference를 audit

## 자주 발생하는 문제

### Agent가 skill을 선택하지 않는다

- Description에 실제 사용자 표현과 trigger를 포함한다.
- 너무 넓은 skill은 domain별로 나눈다.
- 이름·description이 비슷한 skill의 우선순위를 명확히 한다.

### Resource를 읽지 않고 답한다

- `SKILL.md`에 답변 전 필수 reference를 명시한다.
- Reference가 너무 길면 decision table과 상세 규정을 분리한다.
- 답변에 source·version을 포함하도록 지침을 작성한다.

### Script가 위험한 권한으로 실행된다

- Runner를 application identity와 분리한다.
- 승인과 allowlist 없이 arbitrary path를 실행하지 않는다.
- Script input과 output을 untrusted data로 취급한다.

### Cache 때문에 오래된 정책이 사용된다

- Skill content hash 또는 policy version을 cache key에 포함한다.
- 변경 시 cache invalidation과 rollback 절차를 둔다.

## 실습 학습 가이드

1. [01_skill_structure.csx](01_skill_structure.csx)
   - metadata 규칙과 progressive disclosure를 dependency 없이 연습
2. [02_inline_skill.csx](02_inline_skill.csx)
   - 실제 `Microsoft.Agents.AI` package로 inline skill과 provider 구성
3. [03_production_guardrails.csx](03_production_guardrails.csx)
   - tenant filter, approval, script allowlist와 audit policy 실습

실행:

```powershell
dotnet script 01_skill_structure.csx
dotnet script 02_inline_skill.csx
dotnet script 03_production_guardrails.csx
```

두 번째 예제는 NuGet package를 처음 복원할 때 네트워크가 필요하다. Model endpoint나 API key를 사용하지 않으므로 실제 LLM 호출 비용은 발생하지 않는다.

## 다음 학습 경로

1. File skill에 `references/`, `assets/`, `scripts/`를 추가하고 실제 discovery를 확인한다.
2. Class-based skill을 별도 project와 internal NuGet package로 분리한다.
3. Tool approval middleware에서 read와 execute의 정책을 다르게 설정한다.
4. Sandboxed script runner에 timeout, output limit와 audit event를 구현한다.
5. Skill version 변경, cache invalidation, rollback과 tenant isolation test를 자동화한다.
