# Stacked pull requests are now in public preview - 한국어 번역 요약

작성일: 2026-07-31

## 원문 정보

- 원문 제목: Stacked pull requests are now in public preview
- 한국어 제목: Stacked Pull Requests 공개 미리보기 시작
- 유형: GitHub Changelog Release
- 게시일: 2026-07-30
- 원문 언어: 영어
- 최종 URL: [GitHub Changelog](https://github.blog/changelog/2026-07-30-stacked-pull-requests-are-now-in-public-preview/)
- 접근일: 2026-07-31

[한국어 학습 README로 돌아가기](README.md)

## 번역 범위

이 파일은 저작권이 있는 GitHub Changelog 전문을 복제하지 않는다. 원문의 section 순서, 기능 범위, command와 rollout 일정을 유지한 한국어 번역 요약이다. CLI 세부사항은 2026-07-31 현재 GitHub 공식 Docs와 교차 확인했다.

## 공개 미리보기 발표

Stacked pull request는 큰 변경을 작고 review 가능한 여러 PR로 나눈다. 각 PR은 전체 변경에서 집중된 하나의 layer이며 dependency 순서로 이어진다. 팀은 layer마다 review와 check를 독립적으로 수행한 뒤 준비된 범위를 한 번에 merge할 수 있다.

이 기능은 하나의 거대한 PR을 오래 review하거나 여러 branch를 사람이 계속 rebase해야 했던 마찰을 줄이는 것이 목표다.

팀은 다음과 같이 사용할 수 있다.

- 작고 좁은 PR을 병렬 review해 큰 변경을 계속 진행한다.
- 각 layer의 집중 review와 기존 branch protection을 함께 사용해 `main` 품질을 지킨다.
- 전체 stack 또는 bottom부터 이어진 일부 layer를 merge한다.

GitHub에 기본 통합되므로 기존 review, check, merge requirement가 그대로 적용된다.

## CLI extension으로 시작하기

다음 command로 공식 extension을 설치한다.

```bash
gh extension install github/gh-stack
```

현재 공식 Quickstart는 GitHub CLI 2.90.0 이상과 Git 2.20 이상, `gh auth login`, push 가능한 repository를 요구한다.

기본 과정:

```bash
gh stack init feature-auth
# code 작성, stage, commit

gh stack add feature-api
# 다음 layer 작성과 commit

gh stack push
gh stack submit
gh stack view
```

첫 branch는 기본적으로 `main`을 target한다. 다음 branch는 그 아래 branch를 base로 삼는다. `submit`하면 GitHub가 올바른 base로 PR을 만들고 stack으로 연결한다.

## terminal 또는 github.com에서 stack 만들기

GitHub 웹, GitHub CLI, GitHub Mobile, coding agent에서 stack을 사용할 수 있다. 첫 변경의 branch와 PR을 만든 뒤 그 위에 branch와 PR을 추가한다. 각 PR은 바로 아래 layer를 target한다.

웹에서는 첫 PR 이후 다음 PR의 base를 첫 PR branch로 선택하고 `Create stack`을 사용한다. 이미 base chain이 맞는 열린 PR이 있으면 GitHub가 stack 전환을 제안할 수 있다.

모든 branch는 같은 repository에 있어야 하며 cross-fork stack은 지원하지 않는다.

## 각 layer 독립 review

stack 안의 PR을 열면 현재 layer만의 diff를 볼 수 있다. PR 상단 stack map은 현재 변경이 전체 작업에서 어디에 있는지와 다른 layer의 상태를 보여준다.

reviewer는 서로 다른 layer를 병렬로 확인할 수 있다. lower layer에서 review 수정이 발생하면 그 branch에서 고치고 위 branch들을 cascading rebase한다.

```bash
gh stack checkout BRANCH-NAME
# 수정, stage, commit
gh stack rebase --upstack
gh stack push
```

## 한 번에 merge

최신 ready PR을 merge하면 그 PR과 아래의 모든 unmerged layer가 bottom-up 순서로 하나의 작업처럼 들어간다. lower layer까지만 선택하면 그 아래 범위만 merge되고 위 PR은 열린 상태로 남는다. GitHub는 남은 첫 PR을 새 base에 맞춰 자동 rebase하고 retarget한다.

기존 branch protection과 required check는 stack의 최종 base인 `main` 등에 대해 계속 적용된다.

stack merge 규칙:

- lowest unmerged PR부터 이어지는 연속 group만 merge할 수 있다.
- mid-stack PR만 고립해서 merge할 수 없다.
- 아래 PR은 모두 승인과 check 통과가 필요하다.
- history가 linear해야 한다.
- auto-merge는 현재 지원하지 않는다.

## Merge queue

stack은 merge queue를 지원한다. PR은 올바른 순서로 queue에 추가된다. 아래 PR이 queue에서 제거되면 위 PR도 함께 제거된다.

발표일 기준 merge queue 지원은 여러 주에 걸쳐 점진적으로 rollout된다. repository마다 활성화 시점이 다를 수 있다.

## Rollout과 feedback

Stacked PR 공개 미리보기는 2026-07-30부터 모든 repository에 며칠 동안 순차 rollout된다. public preview이므로 command, UI와 API는 변경될 수 있다.

GitHub는 공식 stacked PR 문서와 feedback discussion을 제공한다. 실제 도입 전 현재 문서, known issue, repository의 merge queue 지원 상태를 확인해야 한다.

## 공식 문서에서 보완한 운영 정보

### Rebase와 signed commit

웹에서 server-side cascading rebase를 실행할 수 있지만 생성된 commit은 signed commit이 아니다. signed commit requirement가 있으면 `gh stack rebase`와 `gh stack push`를 사용한다.

### CI metadata

GitHub Actions에서 `github.event.pull_request.stack`으로 number, size, position, base ref와 SHA를 읽는다. 모든 layer가 stack base를 target하는 것처럼 workflow가 실행되므로 큰 stack은 CI 사용량을 늘릴 수 있다.

top layer 조건:

```yaml
if: >-
  github.event.pull_request.stack != null &&
  github.event.pull_request.stack.position == github.event.pull_request.stack.size
```

### Local metadata와 동기화

`gh stack`은 순서 정보를 `.git/gh-stack` JSON에 저장하며 repository에는 commit하지 않는다. merge 뒤 다음 command로 trunk와 remaining branch, remote PR 상태를 동기화할 수 있다.

```bash
gh stack sync --prune
```

## 번역 검수 기록

- 2026-07-31에 Google 공유 링크를 GitHub Changelog 최종 URL로 확인했다.
- 발표일, public preview rollout, merge queue의 점진 배포, existing protection 적용 범위를 공식 문서와 대조했다.
- CLI 2.90.0 이상, Git 2.20 이상, same-repository 제약, auto-merge 미지원, unsigned server-side rebase를 보완했다.
- preview 기능을 이미 모든 계정에서 즉시 사용할 수 있다고 과장하지 않았다.
