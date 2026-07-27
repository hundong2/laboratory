#nullable enable

using System;
using System.Collections.Generic;
using System.Linq;

// 학습 목표:
// 1. skill tool별 approval 결정을 분리합니다.
// 2. tenant별 skill allowlist와 script hash allowlist를 적용합니다.
// 3. audit event에 필요한 최소 필드를 설계합니다.
// 실행: dotnet script 03_production_guardrails.csx
//
// 실제 Agent Framework middleware 구현이 아니라 production policy를
// dependency 없이 검증하는 교육용 모델입니다.

enum SkillOperation
{
    Load,
    ReadResource,
    RunScript,
}

record SkillRequest(
    string TenantId,
    string ActorId,
    string SkillName,
    string SkillVersion,
    SkillOperation Operation,
    string? ScriptHash = null);

record Decision(bool Allowed, bool RequiresHumanApproval, string Reason);

record AuditEvent(
    DateTimeOffset Timestamp,
    string TenantId,
    string ActorId,
    string SkillName,
    string SkillVersion,
    SkillOperation Operation,
    bool Allowed,
    bool RequiresHumanApproval,
    string Reason);

sealed class SkillPolicy
{
    private readonly IReadOnlyDictionary<string, HashSet<string>> tenantSkills;
    private readonly HashSet<string> trustedScriptHashes;

    public SkillPolicy(
        IReadOnlyDictionary<string, HashSet<string>> tenantSkills,
        IEnumerable<string> trustedScriptHashes)
    {
        this.tenantSkills = tenantSkills;
        this.trustedScriptHashes = trustedScriptHashes.ToHashSet(StringComparer.OrdinalIgnoreCase);
    }

    public Decision Evaluate(SkillRequest request)
    {
        if (!tenantSkills.TryGetValue(request.TenantId, out var skills)
            || !skills.Contains(request.SkillName))
        {
            return new(false, false, "tenant skill allowlist에 없습니다.");
        }

        return request.Operation switch
        {
            SkillOperation.Load =>
                new(true, false, "검토된 skill metadata와 instructions입니다."),

            SkillOperation.ReadResource =>
                new(true, true, "Resource에는 tenant data가 포함될 수 있습니다."),

            SkillOperation.RunScript when request.ScriptHash is null =>
                new(false, false, "Script hash가 없습니다."),

            SkillOperation.RunScript when !trustedScriptHashes.Contains(request.ScriptHash) =>
                new(false, false, "검토된 script hash가 아닙니다."),

            SkillOperation.RunScript =>
                new(true, true, "Script 실행은 human approval과 sandbox가 필요합니다."),

            _ => new(false, false, "지원하지 않는 operation입니다."),
        };
    }
}

var tenantSkills = new Dictionary<string, HashSet<string>>
{
    ["tenant-a"] = new(StringComparer.Ordinal)
    {
        "expense-report",
        "onboarding",
    },
    ["tenant-b"] = new(StringComparer.Ordinal)
    {
        "public-faq",
    },
};

var policy = new SkillPolicy(tenantSkills, new[] { "sha256:reviewed-script-v3" });
var requests = new[]
{
    new SkillRequest(
        "tenant-a", "user-17", "onboarding", "2.0.1", SkillOperation.Load),
    new SkillRequest(
        "tenant-b", "user-22", "expense-report", "2.1.0", SkillOperation.Load),
    new SkillRequest(
        "tenant-a", "user-17", "expense-report", "2.1.0",
        SkillOperation.RunScript, "sha256:unreviewed"),
    new SkillRequest(
        "tenant-a", "user-17", "expense-report", "2.1.0",
        SkillOperation.RunScript, "sha256:reviewed-script-v3"),
};

var auditLog = new List<AuditEvent>();
foreach (var request in requests)
{
    var decision = policy.Evaluate(request);
    auditLog.Add(new(
        DateTimeOffset.UtcNow,
        request.TenantId,
        request.ActorId,
        request.SkillName,
        request.SkillVersion,
        request.Operation,
        decision.Allowed,
        decision.RequiresHumanApproval,
        decision.Reason));

    Console.WriteLine(
        $"{request.TenantId}/{request.SkillName}/{request.Operation}: "
        + $"allowed={decision.Allowed}, approval={decision.RequiresHumanApproval}, "
        + $"reason={decision.Reason}");
}

if (auditLog.Count != 4
    || auditLog[1].Allowed
    || auditLog[2].Allowed
    || !auditLog[3].RequiresHumanApproval)
{
    throw new InvalidOperationException("Guardrail 자체 검증이 실패했습니다.");
}

Console.WriteLine($"audit events: {auditLog.Count}");
