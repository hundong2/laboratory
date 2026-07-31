use std::time::Duration;

use topcoat::{
    Result,
    asset::{AssetBundle, RouterBuilderAssetExt},
    context::Cx,
    router::{Router, RouterBuilderDiscoverExt, page, route},
    runtime::{Event, shard},
    view::{component, view},
};

const MAX_QUERY_CHARS: usize = 64;
const PRODUCTS: [&str; 8] = [
    "cargo book",
    "ferris plush",
    "rust mug",
    "tokio poster",
    "topcoat cap",
    "topcoat sticker",
    "web security book",
    "zero-cost shirt",
];

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
                <title>"Topcoat shard 실습"</title>
                topcoat::dev::script()
                topcoat::runtime::script()
            </head>
            <body>
                product_search()
            </body>
        </html>
    }
}

#[component]
async fn product_search() -> Result {
    view! {
        signal query = String::new();

        <main>
            <h1>"상품 검색"</h1>
            <label for="query">"검색어"</label>
            <input
                id="query"
                :value=$(query.get())
                @input=$(|event: Event| query.set(event.target.value))
            >

            // query signal이 바뀌면 이 shard만 서버에서 다시 렌더링됩니다.
            product_results(query: $(query.get()))
        </main>
    }
}

#[shard]
async fn product_results(cx: &Cx, query: String) -> Result {
    // shard 인자는 클라이언트가 조작할 수 있으므로 서버에서 다시 제한합니다.
    let normalized: String = query
        .trim()
        .chars()
        .take(MAX_QUERY_CHARS)
        .collect::<String>()
        .to_lowercase();
    let products = search_products(cx, &normalized).await;

    view! {
        <section aria-live="polite">
            <h2>"검색 결과"</h2>
            if normalized.is_empty() {
                <p>"검색어를 입력하세요."</p>
            } else if products.is_empty() {
                <p>"일치하는 상품이 없습니다."</p>
            } else {
                <ul>
                    for product in products {
                        // view!의 일반 텍스트 위치를 사용해 HTML 문자열 삽입을 피합니다.
                        <li>(product)</li>
                    }
                </ul>
            }
        </section>
    }
}

/// 실제 환경에서는 DB 질의 timeout, 취소, 인가와 rate limit도 적용해야 합니다.
async fn search_products(_cx: &Cx, query: &str) -> Vec<&'static str> {
    tokio::time::sleep(Duration::from_millis(150)).await;
    PRODUCTS
        .into_iter()
        .filter(|product| product.contains(query))
        .collect()
}

/// page뿐 아니라 일반 API route도 같은 라우터에 등록할 수 있습니다.
#[route(GET "/api/health")]
async fn health() -> Result<&'static str> {
    Ok("ok")
}
