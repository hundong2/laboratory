# pdf-inspector 원문 핵심 번역 및 해설

작성일: 2026-07-17

## 번역 대상과 범위

- 대상: [pdf-inspector 공식 소개 사이트](https://firecrawl.github.io/pdf-inspector/)
- 보조 대상: [GitHub README](https://github.com/firecrawl/pdf-inspector), [Python 문서](https://github.com/firecrawl/pdf-inspector/blob/main/docs/python.md), [Rust API 문서](https://github.com/firecrawl/pdf-inspector/blob/main/docs/rust-api.md), [Node.js/Bun 문서](https://github.com/firecrawl/pdf-inspector/blob/main/napi/README.md)
- 확인 기준일: 2026-07-17
- 범위: 원문 전체를 그대로 옮기지 않고, 학습과 도입 판단에 필요한 핵심 구조, API 흐름, 성능 주장, 주의사항을 한국어로 번역 및 해설한다.

## 제목

pdf-inspector: PDF를 분류하고 Markdown을 추출하는 OCR 없는 로컬 파서

## 소개

pdf-inspector는 텍스트 기반 PDF와 스캔 PDF를 빠르게 구분하고, 텍스트 기반 PDF에서는 위치 정보를 포함한 텍스트와 깔끔한 Markdown을 추출하는 Rust 라이브러리다. Firecrawl은 OCR이 필요 없는 PDF까지 모두 OCR로 보내는 비용과 지연 시간을 줄이기 위해 이 도구를 만들었다고 설명한다.

핵심 메시지는 "먼저 PDF를 분류하고, 텍스트 기반이면 로컬에서 빠르게 처리하며, 스캔 또는 문제가 있는 페이지만 OCR로 보낸다"는 것이다.

## 주요 기능 번역

### 스마트 분류

문서를 `TextBased`, `Scanned`, `ImageBased`, `Mixed`로 분류한다. content stream을 샘플링해 텍스트 연산자와 이미지 연산자를 확인하고, 신뢰도와 페이지별 OCR 필요 여부를 반환한다.

### 위치 인식 텍스트 추출

단순 문자열이 아니라 글꼴, 좌표, 페이지 번호, 텍스트 크기 같은 메타데이터를 함께 추출한다. 이 정보는 다단 문서의 읽기 순서와 표 구조를 복원하는 데 사용된다.

### Markdown 변환

제목, 글머리표, 번호 목록, 코드 블록, 표, 굵게/기울임, URL 링크, 페이지 구분을 Markdown으로 변환한다. LLM이나 RAG 파이프라인에서 바로 쓰기 쉬운 구조를 목표로 한다.

### 표 감지

PDF drawing operation에서 나온 사각형 정보를 이용하는 방식과 텍스트 정렬을 기반으로 한 휴리스틱 방식을 함께 사용한다. 재무 표, 각주, 페이지를 넘어 이어지는 표 같은 실제 문서 문제를 고려한다.

### CID 폰트와 인코딩 처리

Type0/Identity-H 폰트와 ToUnicode CMap을 처리해 CJK 같은 문자 집합의 텍스트를 복원한다. 인코딩이 깨진 경우에는 자동으로 표시해 OCR fallback을 고려할 수 있게 한다.

### 가벼운 로컬 실행

순수 Rust 코어이며 ML 모델이나 외부 서비스를 요구하지 않는다. 기본 목적은 OCR이나 문서 AI를 대체하는 것이 아니라, 필요 없는 OCR 호출을 줄이는 것이다.

## 벤치마크 해석

공식 소개 사이트는 `opendataloader-bench`의 200개 PDF 코퍼스를 기준으로 직접 텍스트 추출 엔진을 비교한다. 사이트 기준 pdf-inspector는 전체 점수, 읽기 순서, 표 점수, 처리 속도에서 강점을 보인다.

이 결과는 OCR/ML 기반 엔진을 포함한 모든 문서 처리 문제의 절대 우위를 뜻하지 않는다. 직접 텍스트 추출이 가능한 PDF에 한정했을 때 빠르고 구조화 품질이 좋다는 주장으로 이해해야 한다.

## 빠른 시작 흐름

### Python

```bash
pip install pdf-inspector
```

```python
import pdf_inspector

result = pdf_inspector.process_pdf("document.pdf")
print(result.pdf_type)
print(result.markdown)
```

### Node.js/Bun

```bash
npm install @firecrawl/pdf-inspector
```

```javascript
import { readFileSync } from "fs";
import { processPdf } from "@firecrawl/pdf-inspector";

const result = processPdf(readFileSync("document.pdf"));
console.log(result.pdfType);
console.log(result.markdown);
```

### Rust

```bash
cargo add pdf-inspector
```

```rust
use pdf_inspector::process_pdf;

let result = process_pdf("document.pdf")?;
println!("Type: {:?}", result.pdf_type);
```

### CLI

```bash
cargo install pdf-inspector
pdf2md document.pdf
detect-pdf document.pdf --analyze --json
```

## 아키텍처 번역

pdf-inspector의 처리 흐름은 크게 detector와 extractor로 나뉜다.

1. detector는 PDF의 page tree와 content stream을 빠르게 검사해 문서 유형을 판별한다.
2. extractor는 글꼴, 텍스트 연산자, XObject, 링크, 폼 필드, 레이아웃 정보를 읽는다.
3. layout 단계는 컬럼과 줄을 묶고 사람이 읽는 순서로 재정렬한다.
4. tables 단계는 사각형 기반 감지와 휴리스틱 감지를 통해 표를 구성한다.
5. markdown 단계는 제목, 목록, 표, 코드, 링크 같은 구조를 Markdown으로 변환하고 후처리한다.

문서는 한 번 로드되고 분류와 추출 단계가 그 결과를 공유하므로 중복 파싱을 줄인다.

## 스마트 PDF 라우팅 사용 사례

원문이 강조하는 대표 사용 사례는 대량 PDF 파이프라인이다.

1. PDF가 들어온다.
2. pdf-inspector가 빠르게 유형을 분류한다.
3. 텍스트 기반이고 신뢰도가 높으면 로컬에서 Markdown으로 추출한다.
4. 텍스트가 없거나 인코딩 문제가 있는 페이지만 OCR 서비스로 보낸다.

이 방식은 리포트, 논문, 송장, 법률 문서처럼 텍스트 레이어가 있는 PDF가 많은 환경에서 비용과 지연 시간을 줄일 수 있다.

## 도입 시 주의사항

- 스캔 이미지뿐인 PDF는 OCR 없이는 본문을 복원할 수 없다.
- 깨진 텍스트 레이어는 잘못된 추출 결과를 만들 수 있으므로 `has_encoding_issues` 같은 신호를 확인해야 한다.
- 표, 다단, 각주, 캡션, 페이지 머리말/꼬리말은 문서별 편차가 크므로 샘플 문서로 회귀 테스트가 필요하다.
- 벤치마크 수치는 문서 집합, evaluator revision, 하드웨어에 따라 달라진다.
- Python, Rust, Node 패키지 버전이 서로 다르므로 언어별 API 문서를 따로 확인해야 한다.

## 라이선스

GitHub 저장소와 공식 사이트는 MIT 라이선스를 표시한다. MIT 라이선스는 보통 상용/비상용 사용이 모두 가능하지만, 실제 제품에 포함할 때는 저장소의 `LICENSE` 파일과 조직의 오픈소스 정책을 함께 확인해야 한다.
