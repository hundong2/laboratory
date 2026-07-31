# GitHub Stacked Pull Requests 공개 미리보기

작성일: 2026-07-31

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [기존 PR과 무엇이 다른가](#기존-pr과-무엇이-다른가)
- [설치와 첫 stack](#설치와-첫-stack)
- [review와 수정 전파](#review와-수정-전파)
- [merge 규칙](#merge-규칙)
- [CI 최적화](#ci-최적화)
- [운영 주의사항](#운영-주의사항)
- [명령어 요약](#명령어-요약)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 사용자 제공 링크: [Google 공유 링크](https://share.google/DYkLAoYPw3GKq2nJl)
- 확인된 최종 URL: [Stacked pull requests are now in public preview](https://github.blog/changelog/2026-07-30-stacked-pull-requests-are-now-in-public-preview/)
- 발표일: 2026-07-30
- 공식 문서:
  - [Stacked pull requests](https://docs.github.com/en/pull-requests/how-tos/stacked-pull-requests)
  - [Quickstart](https://docs.github.com/en/pull-requests/get-started/stacked-prs-quickstart)
  - [Creating stacked pull requests](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-stacked-pull-requests)
  - [Managing stacked pull requests](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/managing-stacked-pull-requests)
  - [Merging stacked pull requests](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/merging-stacked-pull-requests)
  - [Optimizing CI](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/optimizing-ci-for-stacked-pull-requests)
- CLI extension: [github/gh-stack](https://github.com/github/gh-stack)
- 원문 언어: 영어
- 확인일: 2026-07-31

원문 구조를 따른 한국어 번역 요약은 [translation.ko.md](translation.ko.md)에 있다. 공개 미리보기 기능은 변경될 수 있으므로 실행 전 공식 문서를 다시 확인한다.

## 한눈에 보기

Stacked PR은 큰 변경을 dependency 순서가 있는 작은 PR 여러 개로 나누는 GitHub 기본 기능이다. 각 PR은 바로 아래 layer의 branch를 base로 삼기 때문에 reviewer는 해당 layer의 diff만 본다.

```text
feature-ui       -> PR #3 (base: feature-api)   <- top
feature-api      -> PR #2 (base: feature-auth)
feature-auth     -> PR #1 (base: main)          <- bottom
main             <- trunk
```

2026-07-30 발표 기준으로 모든 repository에 며칠 동안 public preview가 rollout된다. merge queue 지원은 이후 몇 주에 걸쳐 점진 배포된다. 계정에 즉시 표시되지 않을 수 있다.

핵심 효과:

- 작은 diff를 layer별로 독립 review한다.
- 여러 reviewer가 서로 다른 layer를 병렬 review할 수 있다.
- 기존 branch protection, required review, check를 그대로 사용한다.
- bottom부터 연속된 일부 또는 전체 stack을 한 번에 merge한다.
- lower layer 수정은 upstack branch에 cascading rebase로 전파한다.

## 기초 개념

### Stack, trunk, layer

- **stack**: 같은 repository 안에서 서로 의존하는 PR의 순서 있는 chain
- **trunk**: 전체 stack이 최종적으로 향하는 branch, 보통 `main`
- **bottom**: trunk에 가장 가까운 첫 layer
- **top**: trunk에서 가장 먼 마지막 layer
- **upstack**: trunk에서 멀어지는 방향
- **downstack**: trunk로 가까워지는 방향

각 PR의 base는 항상 바로 아래 branch다. 첫 branch만 trunk를 base로 한다.

### 왜 필요한가

큰 PR은 review 시간이 길고 reviewer가 미루기 쉬우며 결함을 놓칠 가능성이 커진다. 단순히 여러 branch로 나누면 base 변경, rebase, PR 연결과 merge 순서를 사람이 관리해야 한다. `gh stack`과 GitHub UI가 이 반복 작업을 자동화한다.

### 좋은 layer의 조건

- 하나의 일관된 논리 변경을 담는다.
- 독립적으로 설명하고 test할 수 있다.
- 아래 layer에만 의존한다.
- 긴 review 설명이 필요할 정도로 크지 않다.
- foundation, API, integration 순으로 dependency가 자연스럽다.

## 기존 PR과 무엇이 다른가

| 항목 | 일반 독립 PR | Stacked PR |
|---|---|---|
| base | 보통 모두 `main` | 바로 아래 layer branch |
| diff | feature 전체 또는 독립 변경 | 해당 layer만 |
| review | PR 단위 | layer별 독립, 병렬 가능 |
| merge | PR별 독립 | bottom부터 연속된 group |
| lower 수정 | 다른 PR에 수동 반영 | cascading rebase |
| UI | 개별 PR | stack map과 layer 위치 표시 |
| CI 기준 | PR base | stack 최종 base를 대상으로 평가 |

Stacked PR은 commit review와도 다르다. 각 layer는 독립 PR이므로 별도 title, discussion, approval, checks를 갖는다.

## 설치와 첫 stack

### 요구사항

- GitHub CLI `gh` 2.90.0 이상
- Git 2.20 이상
- `gh auth login`으로 인증
- push 권한이 있는 GitHub repository
- 모든 stack branch가 같은 repository에 있어야 함

`github/gh-stack` README 일부에는 더 낮은 CLI version 문구가 보일 수 있지만, 2026-07-31 현재 공식 Quickstart의 2.90.0 이상을 기준으로 한다.

### 설치

```bash
gh extension install github/gh-stack
```

AI coding agent가 stack 명령을 이해하도록 공식 skill을 설치할 수도 있다.

```bash
gh skill install github/gh-stack
```

### 기본 흐름

```bash
# 첫 layer branch 생성
gh stack init feature-auth

# 첫 layer 구현과 commit
git add <files>
git commit -m "Add authentication model"

# 위에 다음 layer 추가
gh stack add feature-api
git add <files>
git commit -m "Add authentication API"

gh stack add feature-ui
git add <files>
git commit -m "Add login UI"

# remote push와 PR 생성·연결
gh stack submit

# 전체 상태 확인
gh stack view
```

`gh stack push`는 branch만 push하고 `gh stack submit`은 push와 PR 생성·연결까지 수행한다. `gh stack add -Am "MESSAGE"`를 사용하면 stage, commit, 다음 branch 생성을 한 단계로 줄일 수 있다.

### GitHub 웹에서 만들기

첫 PR은 보통 `main`을 base로 만든다. 다음 PR의 base를 첫 PR branch로 설정하고 `Create stack`을 선택한다. 이미 base/head chain이 맞는 열린 PR이 있으면 GitHub가 stack 변환 banner를 제안할 수 있다.

cross-fork stack은 지원하지 않는다. fork에서 온 PR과 원 repository branch를 하나의 stack으로 묶을 수 없다.

## review와 수정 전파

reviewer는 stack map으로 전체 위치를 파악하지만 현재 PR의 layer diff만 review한다. foundation 의존성이 강하면 bottom부터 review를 요청하고, 서로 독립적인 전문 영역은 병렬 review한다.

lower layer에서 수정이 필요하면 변경이 속한 branch에서 고친다.

```bash
gh stack checkout feature-auth
git add <files>
git commit -m "Address authentication review"

# 현재 branch 위의 모든 layer에 변경 전파
gh stack rebase --upstack
gh stack push
gh stack top
```

잘못된 branch에서 workaround를 만들면 책임 경계와 diff가 흐려진다. 수정은 최초로 그 코드가 도입된 layer에 둔다.

rebase conflict가 나면 파일을 해결하고 `git add` 후 `gh stack rebase --continue`를 실행한다. 처음 상태로 되돌리려면 `gh stack rebase --abort`를 사용한다.

웹의 server-side rebase commit은 signed commit이 아니다. repository가 signed commit을 요구하면 CLI에서 local signature 설정을 사용해 rebase하고 push한다.

## merge 규칙

stack은 bottom부터 위로 merge된다.

- lowest unmerged PR부터 시작하는 연속 group만 merge할 수 있다.
- mid-stack PR 하나만 단독 merge할 수 없다. 그 아래 unmerged PR도 함께 merge된다.
- top PR을 merge하면 준비된 전체 stack이 bottom-up 순서로 들어간다.
- lower 일부만 merge하면 위 PR은 열린 채로 남고 새 bottom이 trunk를 target하도록 자동 rebase·retarget된다.

merge 전 조건:

1. 선택한 PR 아래의 모든 PR이 승인되고 check를 통과해야 한다.
2. stack history가 linear해야 한다.
3. 현재 PR이 stack base인 `main` 등의 branch protection을 만족해야 한다.

### Merge queue

stack 전체를 올바른 순서로 queue에 넣는다. lower PR이 queue에서 제거되면 그 위 PR도 제거된다. merge group 최대 크기를 stack 때문에 최대 50% 초과할 수 있고, 그 buffer에도 안 들어가면 연속 group으로 나뉜다.

2026-07-30 발표에서 merge queue 지원은 수주에 걸쳐 rollout된다고 했으므로 repository별 활성 상태를 확인해야 한다.

### 현재 제한

- auto-merge는 stacked PR에서 지원하지 않는다.
- 기존 REST/GraphQL merge 자동화는 새 stack merge API에 맞게 수정해야 한다.
- 완전히 merge된 stack은 종료되며 새 branch는 새 stack이 된다.

## CI 최적화

각 PR은 직접 base가 아니라 stack의 최종 base, 예를 들어 `main`을 target하는 것처럼 GitHub Actions가 실행된다. 기존 `pull_request` workflow가 모든 layer에서 자동 실행되지만 stack 크기만큼 CI 비용이 늘 수 있다.

사용 가능한 metadata:

| expression | 의미 |
|---|---|
| `github.event.pull_request.stack.number` | repository 안의 stack 번호 |
| `.size` | 전체 PR 수 |
| `.position` | 1부터 시작하는 위치, 1이 bottom |
| `.base.ref` | 전체 stack의 최종 base branch |
| `.base.sha` | base branch HEAD SHA |

top에서만 비싼 integration test를 실행하는 예:

```yaml
- name: Full integration test on top layer
  if: >-
    github.event.pull_request.stack != null &&
    github.event.pull_request.stack.position == github.event.pull_request.stack.size
  run: ./scripts/integration-test.sh
```

non-stack PR도 처리해야 하므로 `stack != null`을 먼저 검사한다. 보안·lint·unit test를 top에만 제한하면 lower layer 결함을 늦게 발견할 수 있다. 빠른 필수 check는 모든 layer, 비싼 end-to-end test는 top 또는 lowest unmerged layer에 두는 방식이 현실적이다.

## 운영 주의사항

### Stack 설계

- 아래 layer가 자주 바뀌면 모든 upstack branch가 rebase되고 CI가 다시 돈다.
- schema migration과 API consumer를 너무 멀리 떼면 중간 layer가 실행 불가능할 수 있다.
- 각 layer가 독립 build/test 가능하도록 compatibility shim이나 feature flag를 고려한다.
- stack을 지나치게 길게 만들면 작은 PR의 장점보다 rebase와 CI 비용이 커진다.

### History와 안전

- `gh stack push`는 rebase branch 갱신에 `--force-with-lease`를 사용한다.
- 다른 사람이 같은 branch를 직접 push하지 않는 ownership 규칙이 필요하다.
- local metadata는 `.git/gh-stack`에 있으며 repository에 commit되지 않는다.
- `gh stack init`은 conflict resolution 재사용을 위해 Git `rerere`를 자동 활성화한다.
- 구조 변경 전 working tree가 깨끗하고 merge queue에 들어간 PR이 없는지 확인한다.

### Sync와 구조 변경

```bash
# fetch, trunk fast-forward, remaining branch rebase·push, PR state sync
gh stack sync --prune

# branch drop, fold, insert, rename, reorder
gh stack modify
```

local과 remote stack 구성이 서로 다른 방향으로 바뀌면 자동 sync하지 못한다. interactive 환경에서는 remote를 source of truth로 선택하거나 remote stack object를 삭제하고 다시 submit할 수 있다. CI 같은 non-interactive 환경에서는 divergence가 발생하면 안전하게 중단된다.

## 명령어 요약

| 명령 | 역할 |
|---|---|
| `gh stack init` | 새 stack과 첫 branch 초기화 |
| `gh stack add` | top에 새 layer branch 추가 |
| `gh stack submit` | branch push, PR 생성, stack 연결 |
| `gh stack push` | stack branch push |
| `gh stack view` | branch, PR, status, commit 확인 |
| `gh stack up/down` | 인접 layer 이동 |
| `gh stack top/bottom` | 끝 layer로 이동 |
| `gh stack checkout` | 지정 branch로 이동 |
| `gh stack rebase` | bottom부터 cascading rebase |
| `gh stack rebase --upstack` | 현재 branch 이상만 rebase |
| `gh stack modify` | stack 구조 대화형 변경 |
| `gh stack sync --prune` | remote 상태 동기화와 merged local branch 정리 |

## 용어 정리

| 용어 | 설명 |
|---|---|
| stacked PR | dependency 순서로 연결된 작은 PR chain |
| trunk | stack이 최종적으로 merge되는 branch |
| layer | stack을 구성하는 하나의 branch와 PR |
| cascading rebase | 아래 branch부터 위 branch까지 차례로 base를 갱신하는 rebase |
| stack map | PR 위치와 다른 layer 상태를 보여주는 GitHub UI |
| contiguous group | lowest unmerged PR부터 끊기지 않고 이어진 merge 대상 |
| upstack | trunk에서 멀어지는 위 방향 |
| downstack | trunk에 가까워지는 아래 방향 |
| rerere | 이전 conflict 해결을 기록하고 재사용하는 Git 기능 |

## 실습 학습 가이드

실습은 remote repository를 변경하지 않는 Python toy simulator다. CLI가 설치되지 않았거나 rollout이 아직 도착하지 않아도 stack 핵심 규칙을 학습할 수 있다.

1. [01_foundations.ipynb](01_foundations.ipynb): branch/base chain과 layer diff 검증
2. [02_practice.ipynb](02_practice.ipynb): lower 수정 전파와 bottom-up merge simulation
3. [03_advanced.ipynb](03_advanced.ipynb): stack metadata 기반 CI 실행 정책과 비용 비교

## 다음 학습 경로

1. toy simulator에서 잘못된 base와 cycle을 만들어 validator가 잡는지 확인한다.
2. 개인 test repository에서 2-layer stack을 만들고 `gh stack view`까지 실행한다.
3. 각 layer에서 unit test가 통과하도록 dependency 경계를 설계한다.
4. review feedback을 bottom layer에 반영하고 `rebase --upstack`의 commit 변화를 관찰한다.
5. Actions metadata를 기록한 뒤 top-only expensive job이 원하는 조건에서만 실행되는지 확인한다.
6. team에 적용할 때 최대 stack 길이, branch ownership, merge queue, rollback 정책을 문서화한다.
