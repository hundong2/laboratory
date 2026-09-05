# OmniDocBench: Benchmarking Diverse PDF Document Parsing with Comprehensive Annotations — 제한 번역과 상세 해설

## 논문 메타데이터

- 원문 제목: *OmniDocBench: Benchmarking Diverse PDF Document Parsing with Comprehensive Annotations*
- 저자: Linke Ouyang 외 19명
- 출판: CVPR 2025; arXiv v2 (2025-03-25)
- 식별자: `arXiv:2412.07626`, DOI `10.48550/arXiv.2412.07626`
- 원문: <https://arxiv.org/abs/2412.07626>
- 원문 언어: 영어
- 라이선스: arXiv non-exclusive distribution license
- 접근일: 2026-09-05

## 번역·접근 범위

arXiv 배포 라이선스는 번역 개작물의 재배포 허용을 명시하지 않는다. 따라서 원문 한 문장만 대조하고 나머지는 독자적인 한국어 섹션 해설로 제공한다. 공식 PDF 32쪽의 본문·부록·표·그림을 모두 렌더링해 확인했다.

| 구간 | 상태 | 제공 범위 |
|---|---|---|
| 제목·초록 | 부분 번역 | 짧은 대조 인용 1문장과 주장 해설 |
| 1 Introduction | 부분 번역 | 문제 설정과 차별점 해설 |
| 2 Related Work | 부분 번역 | dataset·metric 계보 해설 |
| 3 Dataset | 부분 번역 | 수집·주석·속성 체계 상세 해설 |
| 4 Evaluation | 부분 번역 | 정규화·매칭·지표 해설 |
| 5 Experiments | 부분 번역 | 비교 설정·결과·오류 유형 해설 |
| Appendix/References | 원문 확인 | 추가 통계와 사례를 선별 해설 |

## 읽기 전 핵심 배경

문서 파싱은 글자를 읽는 OCR만이 아니다. 페이지의 영역을 나누고(layout), 각 영역을 text/table/formula/image로 분류하며, 표와 수식의 구조를 복원하고, 사람이 읽는 순서를 직렬화해야 한다. 시스템마다 하나의 문단을 여러 block으로 쪼개는 정도가 달라 단순 1:1 문자열 비교는 불공정할 수 있다.

## 짧은 문장 대조

### Abstract

**S001 — Original**

OmniDocBench sets a new standard for the fair, diverse, and fine-grained evaluation in document parsing.

**S001 — 한국어**

(OmniDocBench는 문서 파싱을 공정하고 다양하며 세밀하게 평가하기 위한 새로운 기준을 제시한다.)

- **용어·약어 해설**
  - **document parsing(문서 파싱)**: PDF 페이지에서 레이아웃, 텍스트, 표, 수식과 읽기 순서를 구조화된 출력으로 복원하는 작업이다.
  - **fine-grained evaluation(세분화 평가)**: 하나의 종합 점수만 보지 않고 요소 유형과 문서 속성별로 오류를 나누어 측정한다.

## 섹션별 상세 해설

### 1. Introduction

기존 벤치마크는 특정 문서 유형, layout detection, OCR text 중 하나에 치우치거나 end-to-end 결과의 형식 차이를 충분히 처리하지 못했다. OmniDocBench는 source diversity, 세밀한 annotation, 통합 evaluation protocol의 세 축으로 이 문제를 다룬다. 비교 대상에는 전통 pipeline parser와 범용 VLM이 함께 포함된다.

### 2. Related Work

관련 연구는 layout analysis dataset, OCR·table·formula 전용 benchmark, 최근의 end-to-end document parser로 나뉜다. 이 논문의 차별점은 각 하위 작업을 새 모델로 해결하는 것이 아니라, 다양한 출력 형식을 공통 표현으로 정규화하고 요소별 지표를 한 프로토콜에 묶은 점이다.

### 3. Dataset construction

#### 3.1 수집과 중복 제거

20만 개가 넘는 PDF를 모아 페이지 이미지를 ResNet50 embedding으로 표현한다. Faiss 기반 유사도 검색과 clustering으로 중복·유사 문서를 줄이고 10개 cluster에서 6,000개 후보를 뽑는다. 사람이 문서 유형과 품질을 검토해 9개 유형, 981쪽으로 균형을 맞춘다.

#### 3.2 주석 체계

19개 layout category는 title, text, table, image, formula 등의 block 역할을 표현한다. 15개 attribute label은 페이지 수준 6개와 bounding-box 수준 9개로, 밀도·열 수·배경·셀 병합·수식 포함처럼 난도를 설명한다. 이 속성 덕분에 평균 점수 뒤에 숨은 실패 조건을 분석할 수 있다.

전체에는 10만 건 이상의 annotation, 2만 건 이상의 block, 7만 건 이상의 span이 있다. 세부적으로 text paragraph 15,979개, image box 989개, table 428개, inline formula 4,009개, footnote marker 357개가 보고된다. 표에는 complex background 142개, formula-containing 81개, merged-cell 150개, vertical 7개가 포함된다.

#### 3.3 품질 관리

자동 모델로 사전 주석한 뒤 annotator가 수정한다. 복잡한 table과 formula는 연구자 세 명이 추가 검토한다. 이는 대규모 수동 작성보다 효율적이지만 사전 모델의 공통 편향이 남을 수 있고, semantic equivalence가 있는 수식·표 표현의 단일 정답 문제도 남는다.

### 4. Evaluation protocol

#### 4.1 출력 정규화

evaluator는 LaTeX table, HTML, display formula, Markdown table, code block 등을 순서대로 추출한다. inline formula는 Unicode로 바꾸고 공백·특수문자를 정규화한다. 순서가 중요한 이유는 같은 구문이 여러 패턴과 겹칠 수 있기 때문이다.

#### 4.2 block matching

정답과 예측의 문자열 유사도를 계산하고 인접 예측 block을 fuzzy merge해 granularity 차이를 완화한다. header, footer, page number, footnote와 일부 caption은 종합 평가에서 제외한다. 그러나 인접 병합만으로는 하나의 정답을 먼 위치의 여러 예측과 대응하거나 table-to-text 변환을 공정하게 처리하기 어렵다. 후속 v1.6의 MGAM은 이 한계를 겨냥한다.

#### 4.3 지표

- normalized edit distance: 삽입·삭제·치환 수를 길이로 정규화하며 낮을수록 좋다.
- TEDS (Tree Edit Distance based Similarity): HTML table tree의 구조·내용 유사도로 높을수록 좋다.
- CDM: formula의 시각·구조적 동등성을 비교하는 지표로 높을수록 좋다.
- BLEU: n-gram 겹침을 보조적으로 본다.
- reading order edit distance: block 내용이 아니라 정답 순서와 예측 순서의 차이를 측정한다.

### 5. Experiments and findings

pipeline 방식과 VLM을 같은 정규화·매칭 뒤 비교한다. text edit distance 예시에서 MinerU는 영어 0.150, 중국어 0.357, Mathpix는 0.191/0.365, Qwen2-VL-72B는 0.252/0.327이다. 언어별 text 열과 문서 유형별 종합 열을 혼용하지 않아야 한다.

문서 유형별 표의 overall edit distance 예시는 MinerU 0.206, Qwen2-VL 0.179다. 평균 하나만 보면 VLM이 앞서 보이지만 세부 분석에서는 pipeline이 standard layout과 high-density page에서 강하고 VLM은 unconventional/degraded page에서 상대적으로 견고하다. newspaper는 해상도와 출력 길이 제약 때문에 VLM에도 어렵다.

### 부록

부록의 속성별 표와 시각 사례는 같은 모델의 실패가 문서 유형보다 세부 속성에 더 밀접할 수 있음을 보여준다. 재현 시 전체 평균만 보고하지 말고 언어, 문서 유형, text density, table complexity별 sample count와 점수를 함께 남겨야 한다.

## 버전 구분: 원 논문과 v1.6

이 파일이 해설하는 원 논문 v2는 981쪽이다. MinerU2.5-Pro에서 사용하는 OmniDocBench v1.6은 Base 1,355쪽과 Hard 296쪽, 총 1,651쪽이며 multi-granularity adaptive matching(MGAM)을 쓴다. dataset 증가와 evaluator 변경이 동시에 일어났으므로 두 버전의 종합 점수는 직접 비교할 수 없다.

## 약어 및 기술 용어 사전

| 원어 | 한국어 | 의미 | 최초 등장 |
|---|---|---|---|
| OCR | Optical Character Recognition, 광학 문자 인식 | 이미지 속 문자 내용을 읽는 하위 작업 | S001 전 배경 |
| VLM | Vision-Language Model, 시각-언어 모델 | 페이지 이미지에서 구조화 출력을 직접 생성하는 모델 | 섹션 1 |
| bbox | bounding box, 경계 상자 | 요소 위치를 나타내는 사각형 좌표 | 섹션 3 |
| TEDS | Tree Edit Distance based Similarity | table HTML tree의 구조·내용 유사도 | 섹션 4 |
| CDM | 수식 평가 지표의 공식 약칭 | rendering/구조를 고려한 formula 일치도 | 섹션 4 |
| Faiss | Facebook AI Similarity Search | 대규모 embedding 근접 검색 도구 | 섹션 3 |
| MGAM | Multi-Granularity Adaptive Matching, 다중 입도 적응 매칭 | 후속 v1.6에서 분할 차이를 다루는 matcher | 버전 구분 |

## 번역 검수 기록

- sentence ID `S001`의 원문과 한국어를 대조했다.
- 직접 인용은 25단어 미만 한 문장으로 제한했다.
- 981쪽 원본과 1,651쪽 v1.6을 명시적으로 구분했다.
- 주요 주석 수와 표 수치를 PDF와 대조했다.
- 32/32쪽 렌더에서 빈 페이지나 잘린 페이지가 없음을 확인했다.

[학습 README로 돌아가기](README.md)
