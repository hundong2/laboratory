$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$gitmodules = Join-Path $root ".gitmodules"

if (-not (Test-Path $gitmodules)) {
    throw "Cannot find .gitmodules at $gitmodules"
}

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
$rows = foreach ($name in ($map.Keys | Sort-Object)) {
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

    $repoPath = Join-Path $root $path
    $readme = Get-ChildItem -Path $repoPath -Filter "README*" -File -ErrorAction SilentlyContinue |
        Select-Object -First 1

    $readmeTitle = ""
    if ($readme) {
        $titleLine = Select-String -Path $readme.FullName -Pattern "^#\s+" -Encoding UTF8 -ErrorAction SilentlyContinue |
            Select-Object -First 1
        if ($titleLine) {
            $readmeTitle = $titleLine.Line -replace "^#\s+", ""
        }
    }

    [pscustomobject]@{
        Path = $path
        Url = $url
        Sha = $sha
        ReadmeTitle = $readmeTitle
    }
}

"| Path | Url | Sha | ReadmeTitle |"
"|---|---|---|---|"
foreach ($row in $rows) {
    "| {0} | {1} | {2} | {3} |" -f $row.Path, $row.Url, $row.Sha, $row.ReadmeTitle
}
