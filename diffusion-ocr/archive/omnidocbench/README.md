# OmniDocBench: Benchmarking Diverse PDF Document Parsing with Comprehensive Annotations

작성일: 2026-09-05

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [연구 질문과 기여](#연구-질문과-기여)
- [방법과 데이터](#방법과-데이터)
- [평가와 수치 결과](#평가와-수치-결과)
- [한계와 재현 주의점](#한계와-재현-주의점)
- [Trillion Labs 블로그와의 관계](#trillion-labs-블로그와의-관계)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 원문: [arXiv:2412.07626](https://arxiv.org/abs/2412.07626)
- 사용 버전: v2, 2025-03-25; CVPR 2025 accepted paper
- 식별자: `arXiv:2412.07626`, DOI `10.48550/arXiv.2412.07626`
- 저자: Linke Ouyang 외 19명
- 원문 언어: 영어
- 라이선스: arXiv non-exclusive distribution license
- 접근일: 2026-09-05

공식 PDF 32쪽 전부를 90 DPI PNG로 렌더링해 본문·표·그림·부록을 시각 확인했다. 텍스트는 32/32쪽에서 추출되었고 PDF SHA-256은 `2160acf355867ecdcec5e2d0253f8dd55979b158d9b2ca07089442500e49e562`다. 라이선스가 개작·번역 재배포를 명시적으로 허용하지 않으므로 [한 문장 대조 인용과 상세 섹션 해설](OmniDocBench-%20Benchmarking%20Diverse%20PDF%20Document%20Parsing%20with%20Comprehensive%20Annotations.번역.md)만 제공한다.

## 한눈에 보기

OmniDocBench는 PDF 문서 파싱 시스템을 레이아웃 검출 하나로 평가하지 않고 텍스트, 표, 수식, 읽기 순서까지 세분화해 비교하는 벤치마크다. 원 논문 v2의 공개 평가 세트는 9개 문서 유형, 981쪽이며 19개 layout category와 15개 속성 label을 제공한다.

중요한 버전 주의점이 있다. Trillion Labs 블로그가 사용한 OmniDocBench v1.6은 MinerU2.5-Pro가 확장한 1,651쪽 프로토콜이다. 이 논문의 981쪽 원본과 페이지 수, 매칭 방식, 난이도 구성이 다르므로 점수를 같은 열에 직접 놓으면 안 된다.

## 연구 질문과 기여

연구 질문은 “서로 다른 PDF 파서가 다양한 문서 유형과 요소에서 실제로 얼마나 잘 작동하는지, 특정 변환 형식이나 매칭 규칙에 편향되지 않게 측정할 수 있는가?”다.

기여는 다음과 같다.

1. 20만 개가 넘는 원천 PDF에서 중복을 줄이고 문서 다양성을 층화한 981쪽 평가 세트를 구축했다.
2. layout, span, text, table, formula, reading order를 함께 다루는 10만 건 이상의 주석을 제공했다.
3. 모델 출력의 Markdown·LaTeX·HTML 표현을 정규화하고 인접 요소를 fuzzy merge한 뒤 요소별 지표로 비교하는 end-to-end 평가기를 설계했다.
4. pipeline parser와 vision-language model(VLM)의 강점이 문서 유형·속성에 따라 달라짐을 분석했다.

## 방법과 데이터

### 표본 선정

20만 개 이상의 PDF를 ResNet50 특징으로 표현하고 Faiss 기반으로 중복을 줄인 뒤 10개 cluster에서 약 6,000개 후보를 만든다. 최종적으로 academic paper, textbook, exam paper, slide, newspaper, magazine, note, financial report, government document의 9개 유형이 균형 있게 포함되도록 981쪽을 선정했다.

### 주석 규모

- layout category: 19개
- attribute label: 15개(페이지 수준 6개, bbox 수준 9개)
- 전체 주석: 100,000건 이상
- block 주석: 20,000건 이상, span 주석: 70,000건 이상
- 텍스트 문단 15,979개, 이미지 상자 989개, 표 428개
- inline formula 4,009개, footnote marker 357개
- 표 난점: 복잡 배경 142개, 수식 포함 81개, 병합 셀 150개, 세로형 7개

자동 사전 주석 뒤 사람이 수정하고, 복잡한 표·수식은 연구자 세 명이 추가 검토했다. 이 절차는 품질을 높이지만 사람 간 합의도나 잔여 오류의 상한을 없애지는 않는다.

## 평가와 수치 결과

평가기는 LaTeX table, HTML, display formula, Markdown table, code block 순으로 요소를 추출하고 inline formula를 Unicode 표현으로 통일한다. 인접한 예측 block을 fuzzy merge해 정답 block과 매칭하며 header, footer, page number, footnote, caption 일부는 전체 점수에서 제외한다.

- text·reading order: 정규화 edit distance, 낮을수록 좋음
- table: TEDS는 높을수록, edit distance는 낮을수록 좋음
- formula: CDM·BLEU는 높을수록, edit distance는 낮을수록 좋음

원 논문 표의 예로 text edit distance에서 MinerU는 영어 0.150, 중국어 0.357이고 Mathpix는 0.191, 0.365, Qwen2-VL-72B는 0.252, 0.327이다. 문서 유형별 종합 edit distance 표에서는 MinerU 0.206, Qwen2-VL 0.179가 보고된다. 두 표는 집계 대상과 열 정의가 다르므로 숫자를 서로 대체해 인용하면 안 된다.

분석상 pipeline 방식은 표준 형식과 고밀도 페이지에서 강하고, VLM은 비정형·열화 문서에서 더 견고한 경향이 있다. 반면 신문처럼 고해상도와 긴 출력이 동시에 필요한 문서에서는 VLM의 입력 해상도와 출력 token 한계가 드러난다.

## 한계와 재현 주의점

- 981쪽은 폭넓지만 실제 PDF 생태계에 비하면 작으며 희귀한 hard case가 부족하다.
- 인접 block merge는 segmentation granularity가 다른 시스템을 완전히 공정하게 맞추지 못한다.
- format 정규화의 실패가 OCR 능력과 별개로 점수를 낮출 수 있다.
- 공개 parser 버전, 렌더러, Unicode 정규화, ignore rule을 고정하지 않으면 점수가 달라진다.
- 노트북은 작은 문자열·block 예제로 지표와 매칭 함정을 보여주는 toy reproduction이며 공식 벤치마크 점수를 재현하지 않는다.

## Trillion Labs 블로그와의 관계

[Trillion Labs 글](https://blog.trillionlabs.co/posts/diffusion-ocr/)은 변환 전후 OCR 품질을 OmniDocBench 점수로 비교한다. 다만 글이 명시한 v1.6은 1,651쪽(Base 1,355 + Hard 296)과 MGAM 매칭을 사용하는 MinerU2.5-Pro 시대의 확장판이다. 원 논문 v2의 981쪽·인접 매칭과 동일한 데이터나 evaluator가 아니다.

따라서 블로그의 Overall 95.57/95.16, 표 TEDS 0.934/0.928을 이 논문의 edit distance 표와 직접 비교하지 않는다. 의미 있는 재현은 정확한 dataset revision, evaluator commit, element normalization과 aggregation rule을 함께 고정해야 한다.

## 실습 학습 가이드

- [01_foundations.ipynb](01_foundations.ipynb): 정규화 edit distance와 읽기 순서 점수를 구현한다.
- [02_practice.ipynb](02_practice.ipynb): block 분할이 다른 예측을 인접 병합으로 맞추는 toy evaluator를 만든다.
- [03_advanced.ipynb](03_advanced.ipynb): 문서 속성별 층화 집계와 macro/micro 평균 차이를 살핀다.

## 다음 학습 경로

1. 번역·해설에서 주석 체계와 정규화 순서를 확인한다.
2. 노트북에서 동일 출력도 matching granularity에 따라 점수가 달라짐을 실험한다.
3. 실제 비교에서는 원본 PDF 목록, renderer, parser 버전과 evaluator revision을 실행 기록에 남긴다.
