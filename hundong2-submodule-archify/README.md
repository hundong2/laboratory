# hundong2 Fork Submodules Archify Diagram

작성일: 2026-09-03

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [개선한 Archify 프롬프트](#개선한-archify-프롬프트)
- [다이어그램 읽는 법](#다이어그램-읽는-법)
- [레포 기능군](#레포-기능군)
- [검증 기록](#검증-기록)
- [실습 가이드](#실습-가이드)
- [남은 확인 사항](#남은-확인-사항)

## 출처와 작업 범위

- 기준 작업공간: `D:/workspace/laboratory`
- 확인 기준일: 2026-09-03
- 사용한 도구: Archify skill v2.17, `node .../archify.mjs doctor`, `validate`, `deliver`, `visual-check`
- 범위: 루트 `.gitmodules`에 등록된 top-level `https://github.com/hundong2/*` submodule 34개
- 제외: `openhuman/vendor/...` 아래의 nested vendor submodule. 포트폴리오 수준의 학습 경로를 흐리므로 구현 의존성으로만 본다.
- 추가 clone/submodule: 없음

## 한눈에 보기

이 산출물은 개별 레포의 상세 내부 구조도가 아니라, 현재 작업공간에 쌓인 hundong2 fork submodule들을 학습자가 어떤 순서로 탐색하면 좋은지 보여주는 고수준 아키텍처 지도다.

핵심 경로는 `Korean learner -> Root README index -> .gitmodules inventory -> GitHub forks -> 기능군별 코드 증거 -> Archify outputs`다. 34개 레포를 모두 한 장에 노드로 펼치면 읽기 어려워지므로, 8-12개 핵심 컴포넌트 안에 기능군을 묶었다.

주요 산출물:

- [architecture.html](architecture.html): Archify standalone HTML 다이어그램
- [architecture.json](architecture.json): Archify 명세
- [architecture.visual-check.html](architecture.visual-check.html): 브라우저 캡처 contact sheet
- [guide/README.md](guide/README.md): 후속 per-repo 분석을 위한 실습 가이드
- `*/docs/archify/architecture.html`: 각 hundong2 top-level submodule 안에 생성한 레포별 Archify 다이어그램

## 개선한 Archify 프롬프트

사용자 제공 프롬프트의 빈칸을 현재 레포 상황에 맞게 채우고, 코드 이해에 필요한 경계와 unknown 처리 규칙을 추가했다.

```text
Use Archify to create a high-level architecture diagram for the current
D:/workspace/laboratory top-level submodules whose .gitmodules URL starts with
https://github.com/hundong2/.

Do not clone repositories, add submodules, or modify fork repositories. Treat
each submodule as code evidence already present in the workspace. Group the 34
repositories into learning-oriented code domains instead of drawing every repo
as its own component.

Show the primary path for a Korean learner:
Korean learner -> Root README index -> .gitmodules inventory -> GitHub fork
evidence -> vision/perception -> OCR/document AI -> explainability/study ->
evaluation/security -> agents/platforms -> systems/runtimes -> Archify outputs.

Represent external dependencies such as model weights, datasets, API keys, and
hardware as a separate unknown runtime boundary. Mark unknowns explicitly
instead of inventing runtime facts. Keep one obvious primary path across 8-12
core components and add guided views for the primary path, code evidence, and
practice outputs.
```

## 다이어그램 읽는 법

- `Root README index`: 루트 `README.md`의 TODO 링크가 학습 진입점 역할을 한다.
- `.gitmodules inventory`: submodule path와 fork URL을 연결하는 실제 근거다.
- `GitHub forks`: hundong2 fork 원격과 로컬 checkout이 만나는 경계다.
- `Vision and perception`에서 `Systems and runtimes`까지는 레포를 기능별로 묶은 코드 이해 레이어다.
- `External assets`: 모델 가중치, 데이터셋, API 키, GPU 요구사항처럼 레포별로 다르고 실행 전에 확인해야 하는 영역이다.
- `Archify outputs`: 이 HTML 다이어그램과 후속 guide 문서가 생성되는 결과 지점이다.

## 레포 기능군

| 기능군 | 포함한 top-level submodule |
|---|---|
| Vision and perception | `SenseNova-Vision`, `TripoSplat`, `detectron2`, `ijepa`, `kimodo`, `lightly-studio` |
| OCR, document, tabular, media AI | `GOT-OCR2.0`, `Unlimited-OCR`, `marker`, `tabfm`, `image-pipes`, `pocket-tts` |
| Explainability and study | `transformer-explainer`, `Attention-Residuals`, `Hands-On-AI-Engineering`, `awesome-free-ai-course-notes` |
| Evaluation, security, observability | `deepeval`, `codex-security`, `monoscope`, `mousecrack` |
| Agents and platforms | `openhuman`, `shepherd`, `labs-OO-Agents`, `orca`, `OpenFabrik`, `openchamber`, `Graft`, `graphify` |
| Systems and runtimes | `modular`, `openship`, `h3.c`, `kimi-k3-in-c`, `Maui`, `polka` |

## Per-Repo Archify 적용

각 top-level hundong2 submodule에 `docs/archify/` 폴더를 만들고 같은 구조의 레포별 아키텍처 산출물을 추가했다.

```text
<submodule>/
  docs/
    archify/
      README.md
      architecture.json
      architecture.html
      architecture.visual-check.json
      architecture.visual-check.html
      architecture.visual-check.1440x900.light.png
      architecture.visual-check.1440x900.dark.png
      architecture.visual-check.2048x1320.light.png
      architecture.visual-check.2048x1320.dark.png
```

전체 34개 대상 모두 `validate`, `deliver`, `visual-check`가 통과했다. 결과 요약은 [repo-archify-run.json](repo-archify-run.json)에 기록했다.

주의: `orca`는 `.gitignore`의 `docs/**`, `polka`는 `.gitignore`의 `docs/` 규칙 때문에 `docs/archify/`가 기본 `git status`에 표시되지 않는다. 파일은 생성되어 있고 검증도 통과했지만, 해당 레포에서 커밋하려면 `git add -f docs/archify/...`가 필요하다.

## 검증 기록

- Archify availability: `doctor` 통과
- Update check: `silent/current`
- Diagram type: `architecture`
- Showcase validation: 9/9 checks, composition `pass`, 0 errors, 0 warnings
- Delivery specification SHA-256: `16d1e855e974b0bb56d45bda8b22652b5cf7ada4b53dbc1379d6d59c3c8316ea`
- Delivery artifact SHA-256: `fe6f15b52729d96368c125a4e2498169dbc3438f250a661951167cbb5fa3244d`
- Browser evidence: `visual-check` pass
- Checked viewports: 1440x900, 1600x1000, 1920x1080, 2048x1320
- Checked themes: light and dark screenshot endpoints
- Visual review: passed by inspecting generated screenshot evidence
- Correction rounds after first visual-check: 1
- Per-repo application: 34/34 validate pass, 34/34 deliver pass, 34/34 browser evidence pass

Archify의 고정 Viewer UI와 `<html lang>`은 한국어 locale을 직접 지원하지 않아 영어로 표시된다. 다이어그램의 작성 내용은 코드 식별자와 레포명을 보존하기 위해 영어 중심으로 두었다.

## 실습 가이드

다음 단계는 [guide/README.md](guide/README.md)를 따른다.

첫 실습은 `.gitmodules`와 checkout 상태를 다시 읽어 현재 submodule inventory를 Markdown 표로 출력하는 것이다.

```powershell
powershell -ExecutionPolicy Bypass -File hundong2-submodule-archify/guide/01_inventory.ps1
```

이후 레포 하나를 고르면 같은 구조로 per-repo 상세 Archify 다이어그램을 만들 수 있다. 예를 들어 `detectron2`는 데이터셋 등록, config, trainer, model zoo, evaluation path를 중심으로 그릴 수 있고, `transformer-explainer`는 tokenizer, embedding, attention, MLP, residual stream, UI rendering path를 중심으로 그릴 수 있다.

## 남은 확인 사항

- 각 레포의 최신 upstream과 fork 차이는 이 포트폴리오 다이어그램에서 확인하지 않았다.
- GPU, model weights, dataset license, API key 요구사항은 레포별 README와 실행 스크립트를 따로 확인해야 한다.
- 정확한 내부 call graph가 필요한 레포는 별도의 per-repo Archify 작업으로 분리하는 편이 낫다.
