param(
    [switch] $SkipVisualCheck
)

$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$archify = "C:/Users/ehdgn/.agents/skills/archify/bin/archify.mjs"
$reportPath = Join-Path $root "hundong2-submodule-archify\repo-archify-run.json"
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)

function Get-SubmoduleRows {
    $pairs = git -C $root config --file .gitmodules --get-regexp "submodule\..*\.(path|url)"
    $map = @{}

    foreach ($line in $pairs) {
        $parts = $line -split " ", 2
        if ($parts.Length -lt 2) {
            continue
        }

        $key = $parts[0]
        $value = $parts[1]

        if ($key -match "^submodule\.(.+)\.(path|url)$") {
            $name = $Matches[1]
            $field = $Matches[2]

            if (-not $map.ContainsKey($name)) {
                $map[$name] = @{}
            }

            $map[$name][$field] = $value
        }
    }

    foreach ($name in ($map.Keys | Sort-Object)) {
        $path = $map[$name]["path"]
        $url = $map[$name]["url"]

        if ($url -notmatch "github\.com/hundong2/") {
            continue
        }

        [pscustomobject]@{
            Name = $name
            Path = $path
            Url = $url
        }
    }
}

function Invoke-JsonCommand($arguments) {
    $raw = & node $archify @arguments 2>&1 | Out-String
    $exit = $LASTEXITCODE
    $parsed = $null

    try {
        $parsed = $raw | ConvertFrom-Json
    }
    catch {
        $parsed = $null
    }

    [pscustomobject]@{
        ExitCode = $exit
        Raw = $raw
        Json = $parsed
    }
}

$rows = @(Get-SubmoduleRows)
$results = New-Object System.Collections.Generic.List[object]
$index = 0

foreach ($row in $rows) {
    $index++
    $jsonPath = Join-Path $root "$($row.Path)\docs\archify\architecture.json"
    $htmlPath = Join-Path $root "$($row.Path)\docs\archify\architecture.html"
    $repoRoot = Join-Path $root $row.Path

    Write-Host "[$index/$($rows.Count)] $($row.Path): validate"
    $validate = Invoke-JsonCommand @("validate", "architecture", $jsonPath, "--quality", "showcase", "--repo-root", $repoRoot, "--json")

    if ($validate.ExitCode -ne 0) {
        $results.Add([pscustomobject]@{
            Path = $row.Path
            Validation = "failed"
            Delivery = "skipped"
            BrowserEvidence = "skipped"
            Error = $validate.Raw
        })
        continue
    }

    Write-Host "[$index/$($rows.Count)] $($row.Path): deliver"
    $deliver = Invoke-JsonCommand @("deliver", "architecture", $jsonPath, $htmlPath, "--quality", "showcase", "--repo-root", $repoRoot, "--json")

    if ($deliver.ExitCode -ne 0) {
        $results.Add([pscustomobject]@{
            Path = $row.Path
            Validation = "passed"
            Delivery = "failed"
            BrowserEvidence = "skipped"
            Error = $deliver.Raw
        })
        continue
    }

    $browserEvidence = "skipped"
    $visualRaw = ""
    if (-not $SkipVisualCheck) {
        Write-Host "[$index/$($rows.Count)] $($row.Path): visual-check"
        $visual = Invoke-JsonCommand @("visual-check", $htmlPath, "--json")
        $visualRaw = $visual.Raw
        if ($visual.ExitCode -eq 0 -and $visual.Json -and $visual.Json.status -eq "pass") {
            $browserEvidence = "passed"
        }
        elseif ($visual.ExitCode -eq 2) {
            $browserEvidence = "skipped"
        }
        else {
            $browserEvidence = "failed"
        }
    }

    $results.Add([pscustomobject]@{
        Path = $row.Path
        Validation = "passed"
        Delivery = "passed"
        BrowserEvidence = $browserEvidence
        SpecificationSha256 = if ($deliver.Json) { $deliver.Json.specification.sha256 } else { "" }
        ArtifactSha256 = if ($deliver.Json) { $deliver.Json.artifact.sha256 } else { "" }
        Error = if ($browserEvidence -eq "failed") { $visualRaw } else { "" }
    })
}

$report = $results | ConvertTo-Json -Depth 20
[System.IO.File]::WriteAllText($reportPath, $report, $utf8NoBom)

$results |
    Select-Object Path, Validation, Delivery, BrowserEvidence |
    Format-Table -AutoSize

$failed = @($results | Where-Object { $_.Validation -ne "passed" -or $_.Delivery -ne "passed" -or $_.BrowserEvidence -eq "failed" })

if ($failed.Count -gt 0) {
    Write-Error "$($failed.Count) Archify target(s) failed. See $reportPath"
}

Write-Host "Report: $reportPath"
