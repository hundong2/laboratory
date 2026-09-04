$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$today = "2026-09-03"
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)

function Write-Utf8NoBom($path, $content) {
    [System.IO.File]::WriteAllText($path, $content, $utf8NoBom)
}

function ShortText($value, [int] $max = 34) {
    if (-not $value) {
        return ""
    }

    $text = ($value -replace "\s+", " ").Trim()
    if ($text.Length -le $max) {
        return $text
    }

    return $text.Substring(0, [Math]::Max(0, $max - 3)).TrimEnd() + "..."
}

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

    $statusLines = git -C $root submodule status
    foreach ($name in ($map.Keys | Sort-Object)) {
        $path = $map[$name]["path"]
        $url = $map[$name]["url"]

        if ($url -notmatch "github\.com/hundong2/") {
            continue
        }

        $statusLine = $statusLines |
            Where-Object { $_ -match "\s$([regex]::Escape($path))(\s|$)" } |
            Select-Object -First 1

        $sha = ""
        if ($statusLine -match "^[-+ ]?([0-9a-f]{40})") {
            $sha = $Matches[1]
        }

        [pscustomobject]@{
            Name = $name
            Path = $path
            Url = $url
            Sha = $sha
        }
    }
}

function Get-RepoProfile($path) {
    $vision = @("SenseNova-Vision", "TripoSplat", "detectron2", "ijepa", "kimodo", "lightly-studio")
    $ocr = @("GOT-OCR2.0", "Unlimited-OCR", "marker", "tabfm", "image-pipes", "pocket-tts")
    $study = @("transformer-explainer", "Attention-Residuals", "Hands-On-AI-Engineering", "awesome-free-ai-course-notes")
    $eval = @("deepeval", "codex-security", "monoscope", "mousecrack")
    $agent = @("openhuman", "shepherd", "labs-OO-Agents", "orca", "OpenFabrik", "openchamber", "Graft", "graphify")
    $systems = @("modular", "openship", "h3.c", "kimi-k3-in-c", "Maui", "polka")

    if ($vision -contains $path) {
        return @{
            Category = "Vision and perception"
            Core = "Model / vision core"
            CoreSub = "perception pipeline"
            Output = "Predictions / artifacts"
            OutputSub = "boxes, masks, 3D, media"
        }
    }

    if ($ocr -contains $path) {
        return @{
            Category = "OCR, document, and media AI"
            Core = "OCR / parser core"
            CoreSub = "text extraction"
            Output = "Text / structured data"
            OutputSub = "markdown, JSON, audio"
        }
    }

    if ($study -contains $path) {
        return @{
            Category = "Explainability and study"
            Core = "Learning / explainer core"
            CoreSub = "concept pipeline"
            Output = "Lessons / visuals"
            OutputSub = "interactive study"
        }
    }

    if ($eval -contains $path) {
        return @{
            Category = "Evaluation, security, observability"
            Core = "Eval / security core"
            CoreSub = "checks and traces"
            Output = "Reports / findings"
            OutputSub = "metrics and risks"
        }
    }

    if ($agent -contains $path) {
        return @{
            Category = "Agents and platforms"
            Core = "Agent platform core"
            CoreSub = "tools and runtime"
            Output = "Actions / UI state"
            OutputSub = "agent outcomes"
        }
    }

    if ($systems -contains $path) {
        return @{
            Category = "Systems and runtimes"
            Core = "Runtime / systems core"
            CoreSub = "build and execute"
            Output = "Binaries / services"
            OutputSub = "local runtime"
        }
    }

    return @{
        Category = "General repository"
        Core = "Core engine"
        CoreSub = "repository logic"
        Output = "Outputs"
        OutputSub = "repo-specific"
    }
}

function Get-RepoEvidence($repoPath) {
    $readme = Get-ChildItem -Path $repoPath -Filter "README*" -File -ErrorAction SilentlyContinue |
        Select-Object -First 1
    $evidenceFile = ""

    $readmeTitle = ""
    if ($readme) {
        $evidenceFile = $readme.Name
        $titleLine = Select-String -Path $readme.FullName -Pattern "^#\s+" -Encoding UTF8 -ErrorAction SilentlyContinue |
            Select-Object -First 1
        if ($titleLine) {
            $readmeTitle = $titleLine.Line -replace "^#\s+", ""
        }
    }
    else {
        $firstFile = Get-ChildItem -Path $repoPath -File -Force -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -ne ".git" } |
            Select-Object -First 1
        if ($firstFile) {
            $evidenceFile = $firstFile.Name
        }
    }

    $markers = New-Object System.Collections.Generic.List[string]
    $markerFiles = @(
        @("pyproject.toml", "Python"),
        @("setup.py", "Python"),
        @("requirements.txt", "Python deps"),
        @("package.json", "JS/TS"),
        @("Cargo.toml", "Rust"),
        @("CMakeLists.txt", "CMake"),
        @("Makefile", "Make"),
        @("go.mod", "Go"),
        @("uv.lock", "uv"),
        @("pnpm-lock.yaml", "pnpm")
    )

    foreach ($marker in $markerFiles) {
        if (Test-Path (Join-Path $repoPath $marker[0])) {
            $markers.Add($marker[1])
        }
    }

    if (Get-ChildItem -Path $repoPath -Filter "*.sln" -File -ErrorAction SilentlyContinue | Select-Object -First 1) {
        $markers.Add(".NET")
    }

    if (Get-ChildItem -Path $repoPath -Filter "*.csproj" -File -Recurse -Depth 2 -ErrorAction SilentlyContinue | Select-Object -First 1) {
        $markers.Add(".NET")
    }

    $dirs = Get-ChildItem -Path $repoPath -Directory -Force -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -notin @(".git", ".github", ".ruff_cache", "node_modules", "target", "build", "dist") } |
        Select-Object -First 7 -ExpandProperty Name

    [pscustomobject]@{
        ReadmeFile = if ($readme) { $readme.Name } else { "" }
        EvidenceFile = $evidenceFile
        ReadmeTitle = $readmeTitle
        Markers = @($markers | Select-Object -Unique)
        Directories = @($dirs)
    }
}

function New-Component($id, $type, $label, $sublabel, $x, $y, $w = 150, $h = 64, $tag = $null, $sourcePath = $null, $sourceLabel = $null) {
    $component = [ordered]@{
        id = $id
        type = $type
        label = $label
        sublabel = $sublabel
        pos = @($x, $y)
        size = @($w, $h)
    }

    if ($tag) {
        $component.tag = $tag
    }

    if ($sourcePath) {
        $component.sources = @(
            [ordered]@{
                path = $sourcePath
                label = if ($sourceLabel) { $sourceLabel } else { "evidence" }
            }
        )
    }

    return $component
}

function New-Connection($id, $from, $to, $variant = $null) {
    $connection = [ordered]@{
        id = $id
        from = $from
        to = $to
    }

    if ($variant) {
        $connection.variant = $variant
    }

    return $connection
}

$rows = @(Get-SubmoduleRows)

foreach ($row in $rows) {
    $repoPath = Join-Path $root $row.Path
    $archifyDir = Join-Path $repoPath "docs\archify"
    New-Item -ItemType Directory -Force -Path $archifyDir | Out-Null

    $profile = Get-RepoProfile $row.Path
    $evidence = Get-RepoEvidence $repoPath
    $markerText = ShortText ($evidence.Markers -join ", ") 20
    if (-not $markerText) {
        $markerText = "repo-specific"
    }
    $dirText = ShortText ($evidence.Directories -join ", ") 20
    if (-not $dirText) {
        $dirText = "top-level files"
    }
    $readmeSub = ShortText $evidence.ReadmeTitle 22
    if (-not $readmeSub) {
        $readmeSub = if ($evidence.ReadmeFile) { $evidence.ReadmeFile } else { "documentation entry" }
    }

    $diagram = [ordered]@{
        schema_version = 1
        diagram_type = "architecture"
        meta = [ordered]@{
            title = "$($row.Path) Repository Architecture"
            output = "architecture.html"
            quality_profile = "showcase"
            repository = [ordered]@{
                url = $row.Url
                revision = $row.Sha
            }
            viewBox = @(1300, 720)
            views = @(
                [ordered]@{
                    id = "primary-path"
                    label = "Primary runtime path"
                    focus = @("developer", "repo_docs", "setup", "entrypoints", "core", "outputs")
                    note = "Follow how a learner moves from docs to setup, entrypoints, core logic, and outputs."
                },
                [ordered]@{
                    id = "code-evidence"
                    label = "Code evidence"
                    focus = @("repo_docs", "setup", "entrypoints", "inputs", "core", "tests")
                    note = "Use README, dependency markers, top directories, and tests as the first evidence pass."
                },
                [ordered]@{
                    id = "runtime-unknowns"
                    label = "Runtime unknowns"
                    focus = @("external_assets", "core", "outputs")
                    note = "Treat weights, datasets, credentials, hosted APIs, and hardware needs as repo-specific unknowns."
                }
            )
        }
        components = @(
            (New-Component "developer" "external" "Developer / learner" "reads and runs" 40 300 150 64),
            (New-Component "repo_docs" "frontend" "README and docs" $readmeSub 240 300 155 64 $null $evidence.EvidenceFile "repo docs"),
            (New-Component "setup" "cloud" "Setup and deps" $markerText 440 300 150 64),
            (New-Component "entrypoints" "backend" "Entry points" $dirText 640 300 150 64),
            (New-Component "core" "backend" $profile.Core $profile.CoreSub 840 300 170 64 $profile.Category),
            (New-Component "outputs" "frontend" $profile.Output $profile.OutputSub 1060 300 155 64),
            (New-Component "inputs" "database" "Inputs and config" "files, flags, params" 640 110 150 64),
            (New-Component "tests" "security" "Tests / evaluation" "expected behavior" 840 510 170 64),
            (New-Component "external_assets" "external" "External assets" "weights, data, APIs" 1060 510 155 64 "unknown")
        )
        boundaries = @(
            [ordered]@{
                kind = "region"
                label = "Repository boundary: $($row.Path)"
                wraps = @("repo_docs", "setup", "entrypoints", "inputs", "core", "outputs", "tests")
            },
            [ordered]@{
                kind = "security-group"
                label = "Repo-specific runtime requirements"
                wraps = @("external_assets")
            }
        )
        connections = @(
            (New-Connection "developer-to-docs" "developer" "repo_docs" "emphasis"),
            (New-Connection "docs-to-setup" "repo_docs" "setup"),
            (New-Connection "setup-to-entrypoints" "setup" "entrypoints"),
            (New-Connection "entrypoints-to-core" "entrypoints" "core" "emphasis"),
            (New-Connection "core-to-outputs" "core" "outputs" "emphasis"),
            (New-Connection "inputs-to-entrypoints" "inputs" "entrypoints" "dashed"),
            (New-Connection "core-to-tests" "core" "tests" "security"),
            (New-Connection "assets-to-core" "external_assets" "core" "dashed")
        )
    }

    $jsonPath = Join-Path $archifyDir "architecture.json"
    $htmlPath = Join-Path $archifyDir "architecture.html"
    $readmePath = Join-Path $archifyDir "README.md"

    $json = $diagram | ConvertTo-Json -Depth 20
    Write-Utf8NoBom $jsonPath $json

    $prompt = @"
Use Archify to create a high-level architecture diagram for $($row.Path).
Inspect repository evidence before finalizing the diagram. Use README,
dependency files, configuration files, entrypoint scripts, and tests as evidence.

Describe users, core components, primary runtime path, external dependencies,
and repository boundaries. Keep one obvious primary path across 8-12 components.
Mark unknown model weights, datasets, API keys, hardware, or hosted services
instead of inventing them.

Optimize the diagram for code understanding: show where configuration enters,
where data is loaded, where the main model or engine runs, where evaluation or
UI rendering happens, and where outputs are written or displayed.
"@

    $readme = @"
# $($row.Path) Archify Architecture

작성일: $today

## 목차

- [산출물](#산출물)
- [출처와 근거](#출처와-근거)
- [적용 프롬프트](#적용-프롬프트)
- [다이어그램 읽는 법](#다이어그램-읽는-법)
- [Unknowns](#unknowns)

## 산출물

- [architecture.json](architecture.json)
- [architecture.html](architecture.html)
- [architecture.visual-check.json](architecture.visual-check.json)
- [architecture.visual-check.html](architecture.visual-check.html)
- ``architecture.visual-check.1440x900.light.png``
- ``architecture.visual-check.1440x900.dark.png``
- ``architecture.visual-check.2048x1320.light.png``
- ``architecture.visual-check.2048x1320.dark.png``

## 출처와 근거

- Repository URL: $($row.Url)
- Checkout SHA: $($row.Sha)
- README file: $($evidence.ReadmeFile)
- Evidence file: $($evidence.EvidenceFile)
- README title: $($evidence.ReadmeTitle)
- Dependency markers: $($evidence.Markers -join ", ")
- Top-level directories: $($evidence.Directories -join ", ")
- Category: $($profile.Category)

## 적용 프롬프트

~~~~text
$prompt
~~~~

## 다이어그램 읽는 법

주 경로는 ``Developer / learner -> README and docs -> Setup and deps -> Entry points -> $($profile.Core) -> $($profile.Output)``이다.

상단의 ``Inputs and config``는 설정 파일, CLI 옵션, 데이터 입력이 어디서 들어오는지 확인하는 위치다. 하단의 ``Tests / evaluation``은 동작을 검증하는 경로이며, ``External assets``는 모델 가중치, 데이터셋, API 키, 하드웨어 요구사항처럼 레포별로 확인해야 하는 실행 전제다.

## Unknowns

- 이 다이어그램은 README, dependency marker, top-level directory를 근거로 한 1차 구조도다.
- 실제 call graph, 모델 내부 연산, 배포 토폴로지는 레포별 세부 분석으로 따로 내려가야 한다.
- weights, datasets, credentials, hosted APIs, GPU/OS 요구사항은 실행 전에 원문 README와 설정 파일을 다시 확인해야 한다.
"@

    Write-Utf8NoBom $readmePath $readme

    [pscustomobject]@{
        Path = $row.Path
        Json = $jsonPath
        Html = $htmlPath
        Category = $profile.Category
    }
}
