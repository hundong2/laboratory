use topcoat::{
    Result,
    asset::{AssetBundle, RouterBuilderAssetExt},
    router::{Router, RouterBuilderDiscoverExt, page},
    view::{component, view},
};

/// 브라우저 런타임 파일을 제공하려면 에셋 번들을 라우터에 연결해야 합니다.
#[tokio::main]
async fn main() {
    let router = Router::builder()
        .assets(AssetBundle::load().expect("Topcoat 에셋 번들이 필요합니다"))
        .discover()
        .build();

    topcoat::start(router)
        .await
        .expect("Topcoat 서버를 시작하지 못했습니다");
}

#[page("/")]
async fn home() -> Result {
    view! {
        <!DOCTYPE html>
        <html lang="ko">
            <head>
                <meta charset="utf-8">
                <title>"Topcoat 반응성 실습"</title>
                topcoat::dev::script()
                topcoat::runtime::script()
            </head>
            <body>
                counter()
            </body>
        </html>
    }
}

#[component]
async fn counter() -> Result {
    view! {
        // signal의 초기값은 서버에서 평가되고 브라우저의 반응형 상태가 됩니다.
        signal count = 0.0;

        <main>
            <h1>"서버 왕복 없는 카운터"</h1>

            // 클릭 핸들러와 텍스트 갱신은 브라우저에서 실행됩니다.
            <button @click=$(|_event| count.decrement())>"-1"</button>
            <strong>" 현재 값: " $(count.get()) " "</strong>
            <button @click=$(|_event| count.increment())>"+1"</button>

            // bind 속성은 signal이 바뀔 때 DOM 속성을 다시 적용합니다.
            <p :hidden=$(count.get() != 0.0)>
                "값이 0일 때만 이 문장이 보입니다."
            </p>
        </main>
    }
}
