<!-- rumdl-disable MD013 -->

# Submodule Code Architecture Analysis Prompt

이 문서는 `AGENTS.md`의 `GitHub Repository Workflow`가 호출하는 재사용 가능한 Archify 작업 프롬프트다. 단일 GitHub 저장소를 submodule로 추가하고 한국어 번역·가이드·예제를 완성한 뒤, 해당 submodule의 실제 코드 증거를 바탕으로 `docs/archify/`에 탐색 가능한 아키텍처 문서를 생성할 때 사용한다.

## 사용 변수

아래 값을 실행 전에 실제 값으로 치환한다.

| 변수 | 의미 |
| --- | --- |
| `<SUBMODULE_PATH>` | 상위 저장소 기준 submodule 경로 |
| `<REPOSITORY_URL>` | `.gitmodules`와 `git remote get-url origin`으로 확인한 URL |
| `<REVISION>` | submodule에서 확인한 40자리 `git rev-parse HEAD` |
| `<ARCHIFY_SKILL_ROOT>` | 현재 세션에 제공된 `archify` 스킬의 `SKILL.md`가 있는 디렉터리 |

## 재사용 프롬프트

```text
현재 작업 대상은 Git submodule `<SUBMODULE_PATH>`이다.

목표:
이 저장소의 실제 코드 아키텍처를 분석하고, Archify 스킬을 사용해 저장소 내부 `docs/archify/`에 검증된 대화형 아키텍처 문서를 만든다. 일반적인 예시 아키텍처를 그리는 작업이 아니다. 현재 revision의 코드, 설정, 빌드 및 배포 증거로 확인한 구성요소와 관계만 표현한다.

필수 선행 절차:
1. 현재 세션에 제공된 `archify` 스킬의 `SKILL.md`를 처음부터 끝까지 읽고 그대로 따른다.
2. Architecture 유형을 사용한다. `schemas/common.schema.json`, `schemas/architecture.schema.json`, Architecture 예제 하나를 읽는다.
3. 실제 저장소 증거를 사용하는 작업이므로 Archify의 repository evidence 및 delivery contract 지침도 읽는다.
4. submodule 내부의 `AGENTS.md`나 동등한 지침이 있으면 함께 준수한다.
5. 작업 시작 시 저장소 URL `<REPOSITORY_URL>`과 40자리 revision `<REVISION>`을 다시 확인한다. 불일치하면 추측하지 말고 실제 값으로 갱신한다.

코드 증거 조사:
1. README의 설명만으로 구조를 추론하지 않는다. `rg --files`, 빌드 manifest, package metadata, 실행 진입점, 라우팅·CLI·서비스 등록, 핵심 모듈, 저장소·캐시, 메시지 전송, 외부 API, 설정, 배포 파일과 테스트를 직접 조사한다.
2. 다음 질문에 파일 경로와 가능한 경우 시작 줄 번호로 답한다.
   - 사용자는 어떤 진입점으로 시스템을 호출하는가?
   - 요청이나 작업은 어떤 핵심 모듈 순서로 흐르는가?
   - 상태는 어디에 저장되고 어떤 경계에서 직렬화되는가?
   - 외부 시스템, 네트워크, 파일 시스템, 데이터베이스, 큐와 어디서 연결되는가?
   - 인증·권한·입력 검증·비밀·샌드박스 같은 신뢰 경계는 어디인가?
   - 빌드, 테스트, 배포는 런타임 구조를 어떻게 입증하는가?
3. 파일이 같은 폴더에 있다는 이유만으로 런타임 호출 관계를 만들지 않는다. import, 함수 호출, 등록, 설정 또는 테스트로 확인한 관계만 사용한다.
4. 확인할 수 없는 구성요소, 포트, 프로토콜, 배포 환경, 소유권은 만들지 않는다. 불확실성은 `docs/archify/README.md`의 제한 사항에 적는다.

산출물:
1. `<SUBMODULE_PATH>/docs/archify/architecture.json`
   - `diagram_type`은 `architecture`, `schema_version`은 Architecture schema가 요구하는 값이다.
   - `meta.quality_profile`은 반드시 `showcase`다.
   - `meta.repository.url`과 `meta.repository.revision`에 확인한 URL과 40자리 commit을 기록한다.
   - 작성 언어는 한국어다. 코드 식별자, 공식 제품명, 프로토콜과 경로는 원문을 유지한다.
   - 한국어는 지원 locale이 아니므로 `meta.locale`을 생략한다. 고정 Viewer UI와 `<html lang>`이 영어로 fallback한다는 점을 `docs/archify/README.md`에 공개한다.
   - 하나의 명확한 왼쪽→오른쪽 주 경로와 가까운 짧은 분기를 사용한다.
   - 주요 node는 6~12개를 목표로 한다. 복잡한 저장소는 모든 파일을 넣지 말고 대표 런타임 경로로 범위를 명시한다.
   - 각 component의 `sources`에 실제 상대 경로와 확인한 줄 번호를 최대 3개까지 기록한다.
   - 관계 label은 호출, 데이터, 프로토콜, 동기·비동기 또는 경계 통과 의미가 있을 때 보존한다.
   - 실제로 확인한 신뢰·프로세스·배포 경계만 boundary로 표현한다.
   - 명시적으로 요청되지 않은 subtitle, animation, visual preset, engineering profile은 넣지 않는다.
   - 처음에는 자동 routing을 사용하고 validator가 구체적으로 요구할 때만 geometry control을 하나씩 추가한다.
2. `<SUBMODULE_PATH>/docs/archify/architecture.html`
   - 최종 고정 JSON을 Archify `deliver`로 생성한 self-contained HTML이다.
3. `<SUBMODULE_PATH>/docs/archify/README.md`
   - 분석 대상 URL과 revision, 분석 범위, 핵심 진입점과 런타임 흐름, 구성요소별 코드 근거, 신뢰 경계, 제외·불확실 사항을 한국어로 설명한다.
   - `architecture.html`과 `architecture.json`을 링크한다.
   - validation, specification/artifact SHA-256, browser evidence, perceptual visual review, correction rounds를 기록한다.
4. `visual-check`가 만든 JSON, contact sheet와 light/dark PNG sidecar는 `docs/archify/`에 함께 둔다. 환경상 browser evidence가 skipped/failed이면 상태를 그대로 기록하고 성공으로 바꾸지 않는다.

Archify 실행 계약:
1. 먼저 `docs/archify/architecture.json` 후보를 작성한다. 후보를 만들기 전에 renderer/validator 내부 구현을 읽지 않는다.
2. 첫 후보가 생긴 직후 packaged update checker를 지침대로 한 번 실행한다. 업데이트는 알림만 처리하고 임의 설치하지 않는다.
3. 후보를 수정할 때마다 다음을 실행한다. `<ARCHIFY_SKILL_ROOT>`에서 실행하거나 절대 경로를 사용한다.

   node bin/archify.mjs validate architecture <SUBMODULE_PATH>/docs/archify/architecture.json --repo-root <SUBMODULE_PATH> --quality showcase --json

4. 9/9 artifact checks, composition error 0, warning 0이 아니면 통과로 간주하지 않는다. diagnostic의 정확한 subject와 supportedFixes만 따라 한 번에 하나의 문제를 고친다.
5. 최종 validation 통과 뒤 JSON을 더 수정하지 말고 한 번만 최종 전달한다.

   node bin/archify.mjs deliver architecture <SUBMODULE_PATH>/docs/archify/architecture.json <SUBMODULE_PATH>/docs/archify/architecture.html --repo-root <SUBMODULE_PATH> --quality showcase --json

6. deliver가 exit 0인 현재 산출물에만 다음을 실행한다.

   node bin/archify.mjs visual-check <SUBMODULE_PATH>/docs/archify/architecture.html --json

7. 자동 browser evidence와 별개로 생성된 contact sheet 또는 light/dark screenshot을 이미지 도구로 실제 확인한다. 두 테마, node·card 잘림, 관계선 교차, label 충돌, 빈 하단 영역과 1440×900·1600×1000·1920×1080·2048×1320 containment를 검토한다.
8. 시각 결함을 고쳤다면 validate와 deliver를 다시 수행한다. 시각 수정은 최대 두 차례다.
9. `deliver`, `visual-check`, 사람/이미지 기반 perceptual review를 서로 다른 증거로 보고한다. 실행하지 않은 검증을 통과했다고 쓰지 않는다.

연결과 완료 조건:
1. 원본 `README.md`, 한국어 번역 README, `guide/README.md`에서 `docs/archify/README.md` 또는 `docs/archify/architecture.html`을 찾을 수 있게 링크한다.
2. `git diff --check`, 저장소 관련 테스트, Markdown 링크 검사를 실행한다.
3. `docs/archify/README.md`에 다음 handoff를 실제 receipt 값으로 기록한다.

   diagram_type: architecture
   output: <absolute architecture.html path>
   specification_sha256: <receipt value>
   artifact_sha256: <receipt value>
   validation: 9/9 showcase, 0 errors, 0 warnings
   browser_evidence: passed|failed|skipped
   visual_review: passed|skipped (image reader unavailable)|failed
   correction_rounds: 0|1|2

4. submodule 작업 커밋에는 번역, 가이드, 예제뿐 아니라 `docs/archify/`와 README 링크도 함께 포함한다. 상위 저장소에서는 push된 submodule commit을 가리키는 gitlink를 갱신한다.
```

## 적용 원칙

- 이 프롬프트는 새로 처리하는 단일 GitHub submodule 저장소마다 사용한다.
- 기존 submodule 전체에 소급 적용하려면 각 원격 저장소를 변경하므로 별도 명시 요청과 범위 합의가 필요하다.
- 여러 URL 묶음에서 GitHub 저장소를 분석만 하는 `Mixed URL Bundle Workflow`에는 적용하지 않는다.
- 저장소가 문서·데이터 전용이라 실행 아키텍처가 존재하지 않으면 허구의 diagram을 만들지 않는다. 확인 가능한 정보 흐름으로 `dataflow`가 더 적합한 경우 사용자에게 전환 근거를 설명하고, 명시된 범위 안에서만 유형을 바꾼다.
