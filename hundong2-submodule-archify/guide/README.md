# hundong2 Submodule Archify Guide

작성일: 2026-09-03

## 목차

- [목표](#목표)
- [1단계: inventory 확인](#1단계-inventory-확인)
- [2단계: 레포 하나 고르기](#2단계-레포-하나-고르기)
- [3단계: 코드 이해용 Archify 프롬프트 만들기](#3단계-코드-이해용-archify-프롬프트-만들기)
- [4단계: 상세 다이어그램으로 확장](#4단계-상세-다이어그램으로-확장)
- [5단계: 전체 레포에 재적용](#5단계-전체-레포에-재적용)

## 목표

이 가이드는 현재 작업공간에 submodule로 들어온 hundong2 fork 레포들을 훑고, 관심 레포 하나를 골라 더 자세한 Archify 다이어그램으로 내려가는 절차를 정리한다.

포인트는 단순한 예쁜 그림이 아니다. README, 설정 파일, 실행 엔트리포인트, 테스트 경로를 근거로 잡고, 코드가 어떤 입력에서 어떤 핵심 컴포넌트를 지나 어떤 산출물을 내는지 추적하는 것이다.

## 1단계: inventory 확인

다음 스크립트는 루트 `.gitmodules`와 `git submodule status`를 읽어서 hundong2 top-level submodule만 Markdown 표로 출력한다.

```powershell
powershell -ExecutionPolicy Bypass -File hundong2-submodule-archify/guide/01_inventory.ps1
```

출력에서 먼저 볼 것:

- `Path`: 로컬 submodule 경로
- `Url`: hundong2 fork URL
- `Sha`: 현재 루트 저장소가 가리키는 checkout commit
- `ReadmeTitle`: README 첫 제목

## 2단계: 레포 하나 고르기

레포를 고를 때는 다음 파일을 먼저 본다.

```powershell
Get-ChildItem <repo-path> -Force | Select-Object Name
Get-ChildItem <repo-path> -Filter "README*" -File
rg -n "install|quickstart|usage|train|eval|demo|serve|test" <repo-path>/README*
```

그 다음 package manager와 실행 방식을 확인한다.

```powershell
Get-ChildItem <repo-path> -Include pyproject.toml,setup.py,requirements.txt,package.json,CMakeLists.txt,*.sln -File -Recurse
```

## 3단계: 코드 이해용 Archify 프롬프트 만들기

레포별 상세 다이어그램을 만들 때는 이 템플릿을 사용한다.

```text
Use Archify to create a high-level architecture diagram for <repo-path>.
Inspect repository evidence before finalizing the diagram. Use README,
dependency files, configuration files, entrypoint scripts, and tests as evidence.

Describe users, core components, primary runtime path, external dependencies,
and repository boundaries. Keep one obvious primary path across 8-12 components.
Mark unknown model weights, datasets, API keys, hardware, or hosted services
instead of inventing them.

Optimize the diagram for code understanding: show where configuration enters,
where data is loaded, where the main model or engine runs, where evaluation or
UI rendering happens, and where outputs are written or displayed.
```

## 4단계: 상세 다이어그램으로 확장

권장 확장 순서:

1. README 기반 전체 구조도
2. 실행 엔트리포인트 중심 workflow
3. 데이터 로딩에서 모델 호출까지 dataflow
4. API 서버나 UI가 있으면 request sequence
5. 테스트·평가·배포 경로가 있으면 별도 workflow

각 단계에서 모르는 것은 `Unknown`으로 남긴다. 특히 가중치, 데이터셋, 외부 API, GPU 요구사항은 README에 적혀 있더라도 실제 실행 전에는 별도 확인이 필요하다.

## 5단계: 전체 레포에 재적용

이번 작업에서 사용한 반복 스크립트는 아래 순서로 실행한다.

```powershell
powershell -ExecutionPolicy Bypass -File hundong2-submodule-archify/guide/02_generate_repo_architecture.ps1
powershell -ExecutionPolicy Bypass -File hundong2-submodule-archify/guide/03_run_archify_delivery.ps1
```

첫 번째 스크립트는 `.gitmodules`의 `github.com/hundong2/*` top-level submodule을 찾아 `docs/archify/architecture.json`과 `docs/archify/README.md`를 만든다. 두 번째 스크립트는 각 JSON을 `validate`, `deliver`, `visual-check` 순서로 처리하고, 전체 결과를 `hundong2-submodule-archify/repo-archify-run.json`에 저장한다.
