#nullable enable

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

// 학습 목표:
// 1. Agent Skill의 최소 metadata 규칙을 이해합니다.
// 2. progressive disclosure의 네 단계를 코드로 확인합니다.
// 실행: dotnet script 01_skill_structure.csx

record SkillMetadata(
    string DirectoryName,
    string Name,
    string Description,
    string? License = null,
    string? Compatibility = null);

static IReadOnlyList<string> Validate(SkillMetadata skill)
{
    var errors = new List<string>();
    var validName = new Regex("^[a-z0-9]+(?:-[a-z0-9]+)*$");

    if (!validName.IsMatch(skill.Name))
    {
        errors.Add("name은 lowercase letter, number, single hyphen만 사용해야 합니다.");
    }

    if (!StringComparer.Ordinal.Equals(skill.DirectoryName, skill.Name))
    {
        errors.Add("name은 parent directory 이름과 같아야 합니다.");
    }

    if (skill.Name.Length > 64)
    {
        errors.Add("name은 64자를 넘을 수 없습니다.");
    }

    if (string.IsNullOrWhiteSpace(skill.Description) || skill.Description.Length > 1024)
    {
        errors.Add("description은 1~1024자여야 합니다.");
    }

    return errors;
}

var expenseSkill = new SkillMetadata(
    DirectoryName: "expense-report",
    Name: "expense-report",
    Description:
        "회사 경비 규정에 따라 보고서를 검토합니다. 환급, 지출 한도, 제출 절차 질문에 사용합니다.",
    License: "Proprietary",
    Compatibility: "Contoso policy repository access required");

var errors = Validate(expenseSkill);
if (errors.Count != 0)
{
    throw new InvalidOperationException(string.Join(Environment.NewLine, errors));
}

var progressiveDisclosure = new[]
{
    ("Advertise", "이름과 description만 context에 알립니다."),
    ("Load", "관련 작업일 때 SKILL.md instructions를 읽습니다."),
    ("Read", "필요한 reference와 asset만 읽습니다."),
    ("Run", "승인된 script만 실행합니다."),
};

Console.WriteLine($"validated skill: {expenseSkill.Name}");
foreach (var (stage, purpose) in progressiveDisclosure)
{
    Console.WriteLine($"{stage,-9} -> {purpose}");
}

var invalid = expenseSkill with { Name = "Expense--Report" };
var invalidErrors = Validate(invalid);
Console.WriteLine($"invalid example errors: {invalidErrors.Count}");

if (invalidErrors.Count == 0 || progressiveDisclosure.Length != 4)
{
    throw new InvalidOperationException("자체 검증이 실패했습니다.");
}
