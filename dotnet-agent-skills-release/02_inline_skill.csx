#r "nuget: Microsoft.Agents.AI, 1.13.0"

using System;
using System.Text.Json;
using Microsoft.Agents.AI;

// 학습 목표:
// 1. 실제 Microsoft.Agents.AI API로 code-defined skill을 만듭니다.
// 2. static resource와 typed delegate script를 등록합니다.
// 3. AgentSkillsProvider에 skill을 연결합니다.
// 실행: dotnet script 02_inline_skill.csx
//
// 이 예제는 provider만 구성하며 model endpoint를 호출하지 않습니다.

var unitConverterSkill = new AgentInlineSkill(
    name: "unit-converter",
    description:
        "일반 단위를 변환합니다. mile, kilometer, pound, kilogram 변환 요청에 사용합니다.",
    instructions: """
        1. conversion-table resource에서 올바른 factor를 찾습니다.
        2. 임의의 factor를 만들지 말고 convert script에 value와 factor를 전달합니다.
        3. 원래 단위와 변환 단위를 결과에 함께 표시합니다.
        """)
    .AddResource(
        "conversion-table",
        """
        # Conversion table
        - miles -> kilometers: 1.60934
        - kilometers -> miles: 0.621371
        - pounds -> kilograms: 0.453592
        - kilograms -> pounds: 2.20462
        """)
    .AddScript("convert", (double value, double factor) =>
    {
        double result = Math.Round(value * factor, 4);
        return JsonSerializer.Serialize(new { value, factor, result });
    });

var skillsProvider = new AgentSkillsProvider(unitConverterSkill);

Console.WriteLine("inline skill and provider: OK");
Console.WriteLine("등록된 script는 agent가 run_skill_script를 선택하고 승인을 받은 뒤 실행됩니다.");
Console.WriteLine($"provider type: {skillsProvider.GetType().FullName}");

if (skillsProvider is null)
{
    throw new InvalidOperationException("Provider 생성에 실패했습니다.");
}
