# Agent Skills for .NET 정식 출시 - 한국어 번역 요약

작성일: 2026-07-27

- 원문: [Agent Skills for .NET Is Now Released](https://devblogs.microsoft.com/agent-framework/agent-skills-for-net-is-now-released/)
- 게시일: 2026-07-07
- 저자: Sergey Menshykh
- 원문 언어: 영어
- 접근일: 2026-07-27
- 번역 방식: 원문의 제목과 section 흐름을 유지한 한국어 번역 요약

> 저작권이 있는 블로그 전문을 그대로 복제하지 않고 핵심 의미, API 이름, 수치와 code 흐름을 보존해 재구성했다. [상세 분석과 실습](README.md)

## Agent Skills for .NET 정식 출시

이제 .NET agent에 지침, reference document, script로 구성된 재사용 가능한 domain expertise package를 제공할 수 있다. Agent는 작업에 필요할 때만 이를 불러온다.

Microsoft Agent Framework의 .NET Agent Skills는 experimental preview를 벗어났다. `[Experimental]` attribute가 제거됐고 API가 stable 상태가 되었다. 팀은 skill을 독립적으로 만들고 배포한 뒤 어떤 agent에도 조합할 수 있으며, production 배치 전에 필요한 governance control도 사용할 수 있다.

이전의 file-based skill과 script execution을 포함한 authoring mode 소개에서 설명한 기능이 이제 stable API로 제공된다.

## Agent Skills란?

Agent Skills는 agent가 필요할 때 발견하고 사용하는 domain expertise의 open package format이다. File skill은 `SKILL.md`에 metadata와 instructions를 두고, 필요하면 script, reference document와 다른 resource를 함께 둔다. Code 또는 class로 정의할 때도 이에 해당하는 속성을 제공한다.

Context를 아끼기 위해 네 단계의 progressive disclosure를 사용한다.

1. Skill 이름과 설명을 광고한다.
2. 관련 작업을 만났을 때 instructions를 load한다.
3. 필요할 때 resource를 읽는다.
4. 필요하고 허용됐을 때 script를 실행한다.

그 결과 agent의 core instruction을 부풀리지 않고도 specialized capability를 추가할 수 있으며, 한 번 만든 전문 지식을 여러 agent에서 재사용할 수 있다.

## 무엇을 할 수 있는가

### Enterprise policy를 일관되게 적용

HR policy, expense rule, IT security guideline을 skill로 package할 수 있다. Employee agent는 관련 질문이 들어올 때 해당 policy skill만 읽고 답한다. 모든 policy를 항상 context에 넣지 않으면서도 같은 근거와 절차를 반복 적용할 수 있다.

### Support playbook을 반복 가능한 처리 방식으로 전환

Troubleshooting guide를 skill로 만들면 customer issue와 맞는 playbook을 불러 정해진 진단 흐름을 따른다. Agent instance가 달라도 같은 자료와 판단 기준을 사용할 수 있다.

### 여러 팀의 skill을 조합

팀은 shared repository의 directory 또는 내부 NuGet package로 skill을 독립 관리할 수 있다. Agent는 skill description으로 적절한 것을 선택하므로 application에 모든 routing logic을 직접 작성할 필요가 없다.

## Skill을 작성하는 세 가지 방식

### File-based skill

`SKILL.md`, 선택적 script와 reference document를 directory에 둔다. Shared repository에서 관리하거나 developer가 아닌 업무 전문가와 함께 유지하기 좋다.

### Class-based skill

C# class가 instructions, resources와 scripts를 묶는다. 일반 .NET build, DI와 NuGet 배포 workflow를 사용하기 좋다.

### Code-defined skill

Application code에서 직접 skill을 만든다. Runtime에 content를 생성하거나 application state를 capture해야 할 때 유용하다.

세 방식은 같은 provider에 연결되며 runtime에서 agent는 동일한 방식으로 취급한다.

## Production을 위한 기능

### Human-in-the-loop approval

Skills provider는 `load_skill`, `read_skill_resource`, `run_skill_script` 세 tool을 제공한다. 기본값으로 모두 approval이 필요하다. 검토된 낮은 위험 작업만 선택적으로 자동 승인할 수 있다.

### 통제된 script 실행

Class-based와 code-defined script는 process 안에서 실행된다. File-based script는 application이 제공한 runner에 위임된다. 따라서 application owner가 sandbox, resource limit와 audit logging을 책임진다.

### Filtering

Shared library의 일부 skill만 특정 agent에 보일 수 있다. Predicate는 requesting agent나 tenant context를 사용해 노출 대상을 결정할 수 있다.

### Caching

Skill resolution 결과를 재사용할 수 있고 key별 isolation을 적용할 수 있다. 한 provider가 tenant마다 다른 skill set을 제공할 때 유용하다.

### 확장 가능한 source pipeline

기반 source class가 public API가 되어 builder가 맞지 않는 경우 custom pipeline이나 내부 registry integration을 구성할 수 있다.

## 시작하기

필요한 .NET package를 설치한 뒤 skill directory와 script runner로 provider를 만든다. 이를 agent option의 context provider 목록에 넣는다.

```csharp
var skillsProvider = new AgentSkillsProvider(
    Path.Combine(AppContext.BaseDirectory, "skills"),
    SubprocessScriptRunner.RunAsync);

var options = new ChatClientAgentOptions
{
    Name = "MyAgent",
    ChatOptions = new() { Instructions = "You are a helpful assistant." },
    AIContextProviders = [skillsProvider],
};
```

원문은 `AzureOpenAIClient`, `DefaultAzureCredential`, Responses client를 이어 실제 `AIAgent`를 만들고 `RunAsync("Help me with onboarding.")`을 실행하는 예를 제공한다. Endpoint와 deployment name은 환경에 맞게 설정해야 한다.

Production에서는 credential fallback, script subprocess와 external resource를 신뢰된 것으로 가정하지 말고 identity, sandbox와 approval policy를 명시해야 한다.

## 왜 중요한가

Agent Skills는 domain expertise를 package, distribute, govern하는 표준 방식을 제공한다. 팀은 서로 독립적으로 skill을 만들고 builder로 조합하며 중요한 동작에는 사람의 승인을 유지할 수 있다.

.NET API가 stable release가 됐으므로 experimental API 변화에 계속 대응하는 부담을 줄이고 production application의 기반으로 사용할 수 있다.

## 연결 자료

- [Microsoft Learn Agent Skills](https://learn.microsoft.com/en-us/agent-framework/agents/skills)
- [.NET samples](https://github.com/microsoft/agent-framework/tree/main/dotnet/samples)
- [Microsoft Agent Framework Discussions](https://github.com/microsoft/agent-framework/discussions)
- [Agent Skills specification](https://agentskills.io/)

## 번역 검수 메모

- `Agent Skills`, `skill`, `tool`, `workflow`는 API 개념 구분을 위해 원어를 병기했다.
- Tool 이름 `load_skill`, `read_skill_resource`, `run_skill_script`는 변경하지 않았다.
- “stable”은 일반 .NET Agent Skills API에 대한 발표다. MCP-based skill API까지 stable이라는 의미로 확장하지 않았다.
- Script 실행이 기본적으로 안전하다고 번역하지 않았다. 실행 위치와 sandbox 책임을 구분했다.
