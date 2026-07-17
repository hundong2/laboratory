# pdf-inspector 오픈소스 정리

작성일: 2026-07-17

## 출처와 작업 범위

- 입력 URL: [pdf-inspector 공식 소개 사이트](https://firecrawl.github.io/pdf-inspector/)
- GitHub 저장소: [firecrawl/pdf-inspector](https://github.com/firecrawl/pdf-inspector)
- 보조 문서:
  - [Rust API 문서](https://github.com/firecrawl/pdf-inspector/blob/main/docs/rust-api.md)
  - [Python 문서](https://github.com/firecrawl/pdf-inspector/blob/main/docs/python.md)
  - [Node.js/Bun 문서](https://github.com/firecrawl/pdf-inspector/blob/main/napi/README.md)
- 확인 기준일: 2026-07-17
- 작업 범위: pdf-inspector를 오픈소스 활용 관점에서 카테고리별로 요약하고, 구조, API, 설치 방식, 벤치마크, 적합한 사용 사례를 한국어로 정리한다.

원문과 주요 참고 문서는 영어이므로 `translation.ko.md`에 핵심 구조를 한국어로 번역 및 해설했다.

## 한눈에 보기

`pdf-inspector`는 Firecrawl이 만든 Rust 기반 PDF 분류 및 텍스트 추출 라이브러리다. 핵심 목적은 모든 PDF를 무조건 OCR에 보내지 않고, 먼저 문서가 텍스트 기반인지 스캔 이미지 기반인지 빠르게 판별한 뒤 텍스트 기반 PDF는 로컬에서 바로 Markdown으로 변환하는 것이다.

공식 소개 사이트 기준으로 `classify_pdf()`는 보통 수십 ms 수준에서 PDF 유형을 판별하고, 텍스트 기반 PDF에서는 위치 정보, 글꼴 정보, 다단 레이아웃, 표 구조를 고려해 Markdown을 생성한다. OCR, ML 모델, 외부 서비스를 기본 요구하지 않는 순수 로컬 파서라는 점이 가장 큰 특징이다.

## 카테고리별 분류

| 카테고리 | 분류 | 핵심 내용 |
| --- | --- | --- |
| 문서 처리 | PDF 분류 | `TextBased`, `Scanned`, `ImageBased`, `Mixed` 유형을 판별한다. |
| 문서 처리 | 텍스트 추출 | 텍스트의 X/Y 좌표, 글꼴, 크기, 굵게/기울임 같은 위치 기반 정보를 함께 추출한다. |
| 문서 변환 | Markdown 변환 | 제목, 목록, 코드 블록, 표, 링크, 페이지 구분을 Markdown으로 변환한다. |
| 레이아웃 분석 | 표/다단 감지 | PDF drawing operation 기반 사각형 표 감지와 텍스트 정렬 기반 휴리스틱을 함께 사용한다. |
| 라우팅 | OCR 비용 절감 | 텍스트가 없는 페이지만 OCR 대상으로 보내는 페이지 단위 라우팅을 지원한다. |
| 런타임 | Rust 코어 | 핵심 엔진은 Rust로 구현되어 있고 `lopdf`를 기반으로 PDF를 파싱한다. |
| 바인딩 | Python | `pip install pdf-inspector`로 사용하며 PyO3 기반 네이티브 바인딩을 제공한다. |
| 바인딩 | Node.js/Bun | `@firecrawl/pdf-inspector` 패키지와 napi-rs 기반 바이너리를 제공한다. |
| 도구 | CLI | `pdf2md`, `detect-pdf` 명령으로 변환과 분류를 파이프라인에 붙일 수 있다. |
| 라이선스 | MIT | 상용/비상용 프로젝트에 비교적 자유롭게 붙일 수 있는 MIT 라이선스다. |

## 현재 패키지 현황

확인 기준일의 공개 패키지 레지스트리 기준 버전은 다음과 같다.

| 생태계 | 패키지 | 확인 버전 | 설치 |
| --- | --- | --- | --- |
| Rust | `pdf-inspector` | `0.1.6` | `cargo add pdf-inspector` |
| Python | `pdf-inspector` | `0.2.5` | `pip install pdf-inspector` |
| Node.js | `@firecrawl/pdf-inspector` | `1.11.1` | `npm install @firecrawl/pdf-inspector` |

버전 번호가 생태계별로 다르므로, 실제 프로젝트에 도입할 때는 사용하는 언어의 레지스트리와 GitHub release/commit을 함께 확인하는 편이 안전하다.

## 기초 개념

### 텍스트 기반 PDF

텍스트 기반 PDF는 PDF 내부에 실제 글자 정보가 들어 있는 문서다. 화면에는 이미지처럼 보이더라도 내부 content stream에 `Tj`, `TJ` 같은 텍스트 출력 연산자가 있으면 프로그램이 글자를 직접 읽을 수 있다. 이런 문서는 OCR 없이 빠르게 추출할 수 있다.

### 스캔 PDF

스캔 PDF는 페이지가 이미지로만 들어 있는 문서다. 내부에 텍스트 레이어가 없으면 일반 텍스트 추출기로는 내용을 읽을 수 없다. 이 경우 OCR이 필요하다.

### Mixed PDF

일부 페이지에는 텍스트가 있고 일부 페이지는 이미지뿐인 문서다. `pdf-inspector`의 라우팅 관점에서는 전체 문서를 OCR로 보내는 대신 텍스트가 없는 페이지만 OCR 대상으로 분리할 수 있다는 점이 중요하다.

### Position-aware extraction

단순히 문자열만 뽑는 것이 아니라 각 텍스트 조각의 좌표, 폭, 높이, 글꼴, 페이지 정보를 함께 다루는 방식이다. 이 정보가 있어야 다단 문서의 읽기 순서, 표의 행/열, 제목 계층 같은 구조를 복원할 수 있다.

## 핵심 요약

- PDF를 빠르게 분류해서 OCR이 필요한 문서와 로컬 추출 가능한 문서를 나눈다.
- 텍스트 기반 PDF에서는 OCR 없이 Markdown을 생성한다.
- 문서 전체가 아니라 페이지 단위로 `pages_needing_ocr`를 제공해 하이브리드 OCR 파이프라인에 적합하다.
- Rust 코어를 중심으로 Python, Node.js/Bun, CLI 인터페이스를 제공한다.
- 외부 API 호출이나 ML 모델 없이 실행되므로 비용, 지연 시간, 데이터 반출 리스크를 줄일 수 있다.
- 표, 다단, CID 폰트, RTL 텍스트, 깨진 인코딩 감지 같은 실제 PDF 처리 문제를 고려한다.
- 한계는 명확하다. 텍스트 레이어가 없거나 깨진 PDF, 시각적 의미 해석이 필요한 문서는 OCR/문서 AI가 필요하다.

## 상세 정리

### 1. 분류 방식

`pdf-inspector`는 전체 PDF를 무겁게 로드하기 전에 xref table과 page tree를 읽고, 선택된 페이지의 content stream에서 텍스트 연산자와 이미지 연산자를 확인한다. 기본 전략은 텍스트 기반 PDF를 빠르게 통과시키기 위한 `EarlyExit`이고, 더 정확한 Mixed/Scanned 판별이 필요하면 `Full`, 대형 문서에는 `Sample(n)`, 특정 페이지만 검사하려면 `Pages(vec)` 전략을 쓴다.

분류 결과에는 문서 유형, 신뢰도, 페이지 수, OCR이 필요한 페이지 목록이 포함된다. 이 구조는 대량 PDF 처리에서 "먼저 싸게 분류하고, 꼭 필요한 부분만 비싼 OCR로 보낸다"는 의사결정에 맞춰져 있다.

### 2. 추출과 Markdown 변환

추출 파이프라인은 글꼴, content stream, XObject, 링크, AcroForm 필드, 레이아웃 정보를 읽어 `TextItem`과 표 후보를 구성한다. 이후 줄 그룹화, 컬럼 감지, 읽기 순서 재정렬, 표 감지, 제목/목록/코드/캡션 분류를 거쳐 Markdown으로 변환한다.

Markdown 변환에서 다루는 요소는 제목, 굵게/기울임, 글머리표와 번호 목록, 코드 블록, 표, 금융형 숫자 표, 캡션, 위첨자/아래첨자, URL 링크, 하이픈 줄바꿈 복원, 페이지 번호 제거, 목차 dot leader 축약 등이다.

### 3. 아키텍처

저장소 구조는 대략 다음 역할로 나뉜다.

| 영역 | 역할 |
| --- | --- |
| `src/lib.rs` | 공개 Rust API, 옵션 빌더, 편의 함수 |
| `src/detector.rs` | 빠른 PDF 유형 감지 |
| `src/extractor/` | 텍스트와 레이아웃 추출 파이프라인 |
| `src/tables/` | 표 감지, 그리드 구성, Markdown 표 생성 |
| `src/markdown/` | Markdown 변환과 후처리 |
| `src/python.rs` | PyO3 기반 Python 바인딩 |
| `napi/` | Node.js/Bun용 napi-rs 바인딩 |
| `src/bin/` | `pdf2md`, `detect-pdf` CLI |

중요한 설계 포인트는 문서를 한 번 로드한 뒤 분류와 추출이 같은 파싱 결과를 공유한다는 점이다. 이 방식은 중복 I/O와 중복 파싱을 줄인다.

### 4. 인터페이스별 사용

#### Python

```python
import pdf_inspector

result = pdf_inspector.process_pdf("document.pdf")
print(result.pdf_type)
print(result.confidence)
print(result.markdown)
```

Python에서는 `process_pdf`, `detect_pdf`, `classify_pdf`, `extract_text`, `extract_text_with_positions`, `extract_text_in_regions`, `extract_pages_markdown` 같은 함수를 사용할 수 있다.

#### Node.js/Bun

```javascript
import { readFileSync } from "fs";
import { processPdf, classifyPdf } from "@firecrawl/pdf-inspector";

const pdf = readFileSync("document.pdf");
const result = processPdf(pdf);
console.log(result.pdfType);
console.log(result.markdown);
```

Node.js 쪽은 버퍼 기반 API가 중심이며, region-based extraction도 제공해 렌더링된 페이지에서 검출한 영역 좌표를 바탕으로 PDF 내부 텍스트를 뽑는 하이브리드 파이프라인에 붙이기 좋다.

#### Rust

```rust
use pdf_inspector::process_pdf;

let result = process_pdf("document.pdf")?;
println!("Type: {:?}", result.pdf_type);
if let Some(markdown) = &result.markdown {
    println!("{}", markdown);
}
```

Rust에서는 `PdfOptions`, `ProcessMode`, `DetectionConfig`, `ScanStrategy`를 통해 탐지 전략, 처리 모드, 페이지 필터를 조정할 수 있다.

#### CLI

```bash
cargo install pdf-inspector
pdf2md document.pdf
pdf2md document.pdf --json
pdf2md document.pdf --select-pages 1,3,5-10
detect-pdf document.pdf --analyze --json
```

CLI는 배치 변환, 데이터 파이프라인, CI 검증, OCR 라우팅 전처리 단계에 붙이기 쉽다.

### 5. 벤치마크 해석

공식 소개 사이트는 `opendataloader-bench` 200개 PDF 코퍼스에서 직접 텍스트 추출 엔진끼리 비교한 결과를 제공한다. 사이트 기준 `pdf-inspector`는 Overall `0.875`, Reading order `0.915`, Tables `0.814`, Headings `0.788`, 200문서 처리 시간 `2.8s`로 표시되어 있다. 같은 계열 도구 중 읽기 순서와 표 구조 복원에서 강점을 강조한다.

다만 GitHub README, 패키지 README, 소개 사이트의 벤치마크 수치가 업데이트 시점에 따라 다르게 보일 수 있다. 실제 의사결정에서는 같은 코퍼스, 같은 evaluator revision, 같은 하드웨어에서 직접 비교해야 한다.

### 6. 잘 맞는 사용 사례

- 연구 논문, 리포트, 계약서, 청구서, 재무 문서처럼 텍스트 레이어가 있는 PDF를 Markdown으로 빠르게 바꾸는 작업
- 대량 PDF 수집 파이프라인에서 OCR 비용을 줄이기 위한 사전 분류 단계
- LLM/RAG 파이프라인에 넣기 전 문서를 구조화된 Markdown으로 정리하는 단계
- 문서별 또는 페이지별로 OCR 필요 여부를 판별하는 라우터
- 로컬 처리와 데이터 반출 최소화가 중요한 내부 문서 처리

### 7. 주의할 한계

- 스캔 이미지뿐인 PDF의 본문 텍스트는 OCR 없이는 복원할 수 없다.
- 텍스트 레이어가 있어도 인코딩이 깨져 있거나 글리프 매핑이 비정상인 문서는 품질이 떨어질 수 있다.
- 시각적 표, 도장, 서명, 체크박스, 차트 의미 해석은 전용 OCR/비전 모델이 더 적합할 수 있다.
- 벤치마크 수치는 문서 집합과 평가 방식에 크게 좌우된다.
- 패키지 버전과 API는 빠르게 바뀔 수 있으므로 도입 전 잠금 버전과 회귀 테스트가 필요하다.

## 용어 정리

| 용어 | 뜻 |
| --- | --- |
| OCR | 이미지 속 글자를 인식해 텍스트로 바꾸는 기술 |
| Content stream | PDF 페이지의 그리기/텍스트 출력 명령이 들어 있는 내부 스트림 |
| `Tj`/`TJ` | PDF에서 텍스트를 출력할 때 쓰이는 대표 연산자 |
| `Do` | 이미지나 XObject를 그릴 때 쓰이는 PDF 연산자 |
| CID font | CJK 등 대규모 문자 집합을 위해 쓰이는 PDF 폰트 방식 |
| ToUnicode CMap | 글리프 코드를 실제 유니코드 문자로 매핑하는 정보 |
| Reading order | PDF 화면 배치에서 사람이 읽는 순서를 복원한 순서 |
| TEDS | 표 구조 유사도를 평가하는 지표 |
| NID | 읽기 순서 품질 평가에 쓰이는 지표 |
| PyO3 | Rust 코드를 Python 확장 모듈로 노출하는 도구 |
| napi-rs | Rust로 Node.js 네이티브 애드온을 만드는 도구 |

## 실습 학습 가이드

| 파일 | 목적 |
| --- | --- |
| `01_foundations.ipynb` | PDF가 텍스트 기반인지 스캔 기반인지 판별하는 핵심 신호를 작은 Python 예제로 이해한다. |
| `02_practice.ipynb` | `pdf-inspector`를 실제 파이프라인에 붙인다고 가정하고 분류, Markdown 변환, OCR 라우팅 코드를 연습한다. |
| `03_advanced.ipynb` | 페이지 단위 OCR 라우팅, 비용/지연 시간 절감, scan strategy 선택을 시뮬레이션한다. |

## 다음 학습 경로

1. PDF 내부 구조: xref table, page tree, content stream, text operator를 먼저 학습한다.
2. Rust PDF 파싱: `lopdf`가 PDF 객체와 stream을 다루는 방식을 살펴본다.
3. 문서 레이아웃 복원: 줄 그룹화, 컬럼 감지, 표 grid 추론 알고리즘을 공부한다.
4. OCR 라우팅 설계: 텍스트 기반 추출과 OCR/문서 AI를 언제 섞을지 정책을 만든다.
5. RAG 전처리: Markdown 품질이 청킹, 임베딩, 검색 정확도에 어떤 영향을 주는지 평가한다.
