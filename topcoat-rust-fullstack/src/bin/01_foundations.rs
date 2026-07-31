use topcoat::{
    Result,
    router::{Router, RouterBuilderDiscoverExt, page},
    view::{component, view},
};

/// 가장 작은 Topcoat 애플리케이션입니다.
///
/// `discover()`는 아래의 `#[page]` 항목을 찾아 라우터에 등록합니다.
#[tokio::main]
async fn main() {
    topcoat::start(Router::builder().discover().build())
        .await
        .expect("Topcoat 서버를 시작하지 못했습니다");
}

/// `GET /` 요청을 처리하고 완전한 HTML 문서를 서버에서 렌더링합니다.
#[page("/")]
async fn home() -> Result {
    let learner = "Rust 개발자";

    view! {
        <!DOCTYPE html>
        <html lang="ko">
            <head>
                <meta charset="utf-8">
                <title>"Topcoat 기초 실습"</title>
                topcoat::dev::script()
            </head>
            <body>
                greeting(name: learner)
                <p>"이 HTML은 서버의 Rust 코드가 만들었습니다."</p>
            </body>
        </html>
    }
}

/// 컴포넌트도 비동기 Rust 함수이므로 필요하면 서버 자원을 조회할 수 있습니다.
#[component]
async fn greeting(name: &str) -> Result {
    view! {
        <h1>"안녕하세요, " (name) "!"</h1>
    }
}
