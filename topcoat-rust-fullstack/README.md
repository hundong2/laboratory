# Topcoat: Rust 풀스택 웹 프레임워크

작성일: 2026-07-30

> 확인 기준: Topcoat `0.5.0`, 공식 `v0.5.0` 태그, Rust `1.95` 이상
>
> 상태: 초기·실험 단계. 파괴적 변경 가능성이 크므로 프로덕션 도입 전 재평가가 필요합니다.

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [핵심 요약](#핵심-요약)
- [상세 정리](#상세-정리)
- [설치와 실행](#설치와-실행)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [프로덕션 도입 체크리스트](#프로덕션-도입-체크리스트)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

| 구분                  | URL                                                                                      | 확인 내용                             |
| --------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------- |
| 사용자 제공 공유 링크 | <https://share.google/iZJRqZnmxHPug3Rj2>                                                 | 최종 URL 확인                         |
| 최종 원문             | <https://news.hada.io/topic?id=31891>                                                    | GeekNews의 한국어 핵심 요약           |
| 공식 저장소           | <https://github.com/tokio-rs/topcoat>                                                    | README, 기능, 로드맵, 라이선스        |
| 공식 API 문서         | <https://docs.rs/topcoat/latest/topcoat/>                                                | `0.5.0` API, 라우터·런타임·shard 동작 |
| 공식 시작 문서        | <https://github.com/tokio-rs/topcoat/blob/v0.5.0/crates/topcoat/docs/getting_started.md> | 설치, CLI, 개발 서버                  |
| 고정 버전 소스        | <https://github.com/tokio-rs/topcoat/tree/v0.5.0>                                        | 예제와 최소 Rust 버전 대조            |

모든 출처의 접근일은 2026-07-30입니다. 공식 `v0.5.0`의 최소 Rust 버전은 `1.95`, edition은 2024, 라이선스는 MIT입니다. 확인 당시 `main`은 `6b4ce946992bc7e667c3d5b2d5f209c3144fe0dc`였지만 이 값은 계속 변경될 수 있습니다.

원문은 이미 한국어이므로 [translation.ko.md](translation.ko.md)는 직역본이 아니라 원문의 구조와 주장을 보존한 교정·학습용 재구성본입니다. 실습 코드는 공식 `v0.5.0` API를 기준으로 작성했지만 현재 환경에 Rust 도구 체인이 없어 실제 컴파일은 수행하지 못했습니다.

## 한눈에 보기

Topcoat는 서버 렌더링, 라우팅, HTML 템플릿, 브라우저 반응성, 에셋, 쿠키·세션 같은 웹 애플리케이션 요소를 Rust 중심으로 묶은 프레임워크입니다.

핵심 아이디어는 다음 세 실행 위치를 한 코드베이스에서 명확히 나누는 것입니다.

```text
초기 요청
  → Rust 서버 컴포넌트가 HTML 생성
  → 브라우저에 HTML + 필요한 JavaScript 표현식 전달

로컬 상호작용
  → $(...)로 변환된 JavaScript가 브라우저에서 signal 갱신
  → 서버 왕복 없음

서버 데이터가 필요한 상호작용
  → procedure 또는 shard HTTP 요청
  → 서버가 계산하거나 일부 HTML을 재렌더링
```

“Wasm이 없다”는 “브라우저 코드가 없다”는 뜻이 아닙니다. `$(...)` 안의 제한된 Rust 표현식을 JavaScript로 변환해 전달한다는 뜻입니다.

## 기초 개념

### 서버 사이드 렌더링

페이지와 컴포넌트는 서버에서 HTML을 만듭니다. 컴포넌트가 `async` 함수이므로 서버 자원이나 데이터베이스를 직접 호출할 수 있습니다. 별도 REST API가 항상 필요하지는 않지만, 권한 검사와 입력 검증 책임이 사라지는 것은 아닙니다.

### `view!` 템플릿

`view!`는 HTML 형태를 유지하면서 Rust 표현식, `if`, `for`, 컴포넌트 호출을 사용할 수 있는 매크로입니다. `topcoat fmt`는 일반 `rustfmt`가 직접 다루기 어려운 매크로 내부까지 포맷합니다.

### signal과 `$(...)`

`signal`은 브라우저의 반응형 상태입니다. `$(...)` 표현식은 최초 서버 렌더에서 Rust로 한 번 평가되고, 대응하는 JavaScript가 브라우저에서 다시 실행됩니다. 모든 Rust 기능을 변환할 수 있는 것이 아니라 문서가 지원하는 제한된 타입·메서드만 사용해야 합니다.

### procedure와 shard

- `#[procedure]`: 브라우저에서 호출할 수 있는 서버 함수입니다.
- `#[shard]`: 인자가 바뀌면 서버에서 컴포넌트를 다시 렌더링하고 해당 HTML 조각을 교체합니다.

둘 다 실질적으로 외부에서 호출 가능한 HTTP 엔드포인트입니다. 클라이언트가 보낸 인자는 조작될 수 있으므로 서버에서 인증·인가·검증해야 합니다.

### 라우팅

`#[page]`, `#[layout]`, `#[route]`, `#[layer]`로 페이지와 API를 선언합니다. `discover()`는 링크 시점에 수집된 항목을 자동 등록하고, `module_router!`는 Rust 모듈 구조에서 URL 구조를 유도할 수 있습니다.

## 핵심 요약

### 강점

- 서버와 브라우저 상호작용을 Rust 중심으로 작성할 수 있습니다.
- 단순 UI 반응에는 서버 왕복이나 Wasm 번들이 필요하지 않습니다.
- 서버 데이터 기반 부분 갱신을 shard로 표현할 수 있습니다.
- HTML과 Rust 제어 흐름을 가까운 형태로 유지합니다.
- 라우팅, 에셋, Tailwind, 쿠키, 세션, 메일 등 선택 가능한 모듈이 넓습니다.
- Topcoat UI 코드를 프로젝트에 복사해 소유하고 수정할 수 있습니다.

### 주의점

- 공식 문서가 명시한 초기·실험 단계 프로젝트입니다.
- 런타임 표현식의 Rust→JavaScript 변환 어휘가 제한적입니다.
- `procedure`와 `shard`는 입력을 신뢰하면 안 되는 API 경계입니다.
- 문서의 세션 기능과 완성된 인증 제품은 다릅니다. 세션 원시 기능은 있지만 더 포괄적인 인증 경험은 로드맵에 남아 있습니다.
- 정적 내보내기, 지역화, OpenAPI, 스트리밍 SSR, 클라이언트 라우팅, 백그라운드 작업 등 여러 기능이 로드맵 단계입니다.
- 빠르게 버전이 올라가므로 예제는 버전을 고정하고 업그레이드 테스트를 거쳐야 합니다.

## 상세 정리

### 1. 요청과 렌더링

`Router`가 요청을 받고 page를 선택합니다. 일치하는 layout과 layer가 경로 접두사 규칙에 따라 적용됩니다. page와 component는 `Result<View>`에 해당하는 결과를 만들고, 오류는 HTTP 응답으로 변환됩니다.

### 2. 라우터 등록 방식

수동 등록은 코드가 장황하지만 등록 순서를 명시적으로 검토할 수 있습니다.

```rust
Router::builder()
    .layout(root_layout)
    .page(home)
    .route(health)
    .build()
```

자동 발견은 짧고 모듈화에 유리합니다.

```rust
Router::builder().discover().build()
```

자동 발견 순서는 안정적이지 않으므로 같은 경로에 여러 layer를 쌓아야 한다면 수동 등록이 더 안전합니다.

### 3. 에셋과 브라우저 런타임

`asset!` 선언은 컴파일된 바이너리에서 수집되고 Topcoat CLI가 에셋 번들을 만듭니다. 브라우저 반응성을 사용할 때는 라우터에 `AssetBundle`을 연결하고 문서 `<head>`에 `topcoat::runtime::script()`를 넣어야 합니다.

### 4. Tailwind와 UI

`tailwind` feature를 활성화하면 Node 없이 Tailwind를 에셋 파이프라인에 연결할 수 있습니다. Topcoat UI는 완전히 감춰진 바이너리 컴포넌트가 아니라 프로젝트로 복사되는 소스 코드이므로 수정 자유도가 높은 대신, 업데이트 병합 책임도 애플리케이션 팀에 있습니다.

### 5. 상태와 보안 경계

shard 내부 signal은 shard가 재렌더링될 때 교체되므로 유지해야 할 상태는 shard 밖에 두고 인자로 전달합니다. procedure·shard 인자, path parameter, query, cookie와 request body는 모두 불신 입력입니다.

서버 함수에서 최소한 다음을 확인해야 합니다.

1. 현재 사용자의 인증 상태
2. 대상 리소스에 대한 인가
3. 길이·형식·범위 검증
4. 속도 제한과 요청 취소
5. CSRF·교차 출처 정책
6. 로그와 오류 응답의 민감 정보

## 설치와 실행

### 1. Rust 준비

Rust `1.95` 이상이 필요합니다.

```bash
rustup update stable
rustc --version
cargo --version
```

### 2. Topcoat CLI 설치

실습과 같은 버전을 사용하도록 고정합니다.

```bash
cargo install topcoat-cli --version 0.5.0 --locked
topcoat --help
```

### 3. 정적 검사

이 폴더에서 실행합니다.

```bash
cargo check --bins
topcoat fmt
cargo fmt --check
```

처음 의존성을 해석한 뒤 생성되는 `Cargo.lock`은 애플리케이션 재현성을 위해 커밋하는 편이 좋습니다.

### 4. 실습 실행

```bash
# 가장 작은 SSR 예제
cargo run --bin 01_foundations

# 브라우저 signal 예제
topcoat dev --bin 02_practice

# 서버 shard와 API route 예제
topcoat dev --bin 03_advanced
```

기본 주소는 <http://127.0.0.1:3000>입니다. 외부 인터페이스에 바인딩하기 전에 방화벽과 인증 여부를 확인하세요.

## 용어 정리

| 용어               | 설명                                                                                                            |
| ------------------ | --------------------------------------------------------------------------------------------------------------- |
| SSR                | 서버가 최초 HTML을 생성하는 서버 사이드 렌더링                                                                  |
| hydration          | 서버 HTML에 브라우저 동작을 연결하는 과정. Topcoat는 일반적인 Wasm hydration 대신 자체 JavaScript 런타임을 사용 |
| signal             | 변경을 추적해 관련 표현식을 다시 계산하는 브라우저 상태                                                         |
| runtime expression | `$(...)`로 쓰며 서버 Rust와 브라우저 JavaScript에서 대응 실행되는 표현식                                        |
| component          | 재사용 가능한 비동기 서버 렌더 함수                                                                             |
| procedure          | 브라우저에서 호출 가능한 비동기 서버 함수                                                                       |
| shard              | 인자 변경 시 서버 재렌더링 후 HTML 조각을 교체하는 컴포넌트                                                     |
| `Cx`               | 요청 범위 데이터와 기능에 접근하는 request context                                                              |
| layout             | 하위 page 결과를 공통 문서 구조로 감싸는 렌더 함수                                                              |
| layer              | 경로 아래의 요청 처리 흐름을 감싸는 함수                                                                        |
| discovery          | 매크로로 선언한 route 등을 링크 시점 수집 정보로 자동 등록하는 방식                                             |

## 실습 학습 가이드

| 순서 | 파일                                                   | 목표                                               |
| ---- | ------------------------------------------------------ | -------------------------------------------------- |
| 1    | [src/bin/01_foundations.rs](src/bin/01_foundations.rs) | 가장 작은 SSR page와 component 실행                |
| 2    | [src/bin/02_practice.rs](src/bin/02_practice.rs)       | signal, 이벤트, bind 속성을 이용한 브라우저 반응성 |
| 3    | [src/bin/03_advanced.rs](src/bin/03_advanced.rs)       | shard, 서버 검색, 입력 제한, API route             |

실습은 같은 `Cargo.toml`을 공유하며 각각 독립된 바이너리입니다. 코드를 읽을 때 “이 줄은 서버에서만 실행되는가, 브라우저에서도 실행되는가, HTTP 경계를 넘는가?”를 계속 표시해 보세요.

## 프로덕션 도입 체크리스트

- [ ] 실험 단계와 파괴적 변경 비용을 조직이 수용할 수 있는가?
- [ ] `Cargo.lock`과 Topcoat 버전을 고정했는가?
- [ ] procedure와 shard마다 인증·인가·입력 검증이 있는가?
- [ ] CSRF, cookie 속성, 세션 회전과 만료를 테스트했는가?
- [ ] 응답 보안 헤더와 오류 정보 노출을 점검했는가?
- [ ] 프록시, TLS, timeout, body 크기, rate limit 정책이 있는가?
- [ ] SSR·shard 실패와 브라우저 JavaScript 비활성 상황을 다루는가?
- [ ] 빌드 산출물과 에셋을 재현 가능하게 배포하는가?
- [ ] 공식 로드맵 기능을 이미 제공되는 기능으로 오인하지 않았는가?
- [ ] 업그레이드 전 통합·E2E·보안 회귀 테스트가 있는가?

## 다음 학습 경로

1. `01_foundations`에서 page와 component의 서버 실행 순서를 추적합니다.
2. `02_practice`에서 `$(...)`에 허용되는 표현식 범위를 바꿔 보며 컴파일 오류를 읽습니다.
3. `03_advanced`에서 shard 인자를 조작하는 요청을 가정하고 검증·인가를 추가합니다.
4. 공식 문서의 `Cx`, memoization, cookie와 session을 순서대로 학습합니다.
5. 수동 라우터와 module router를 각각 구현해 등록 가시성과 생산성을 비교합니다.
6. 작은 내부 도구에서 먼저 평가하고, API 안정성과 운영 기능이 필요한 서비스는 대안을 함께 비교합니다.
