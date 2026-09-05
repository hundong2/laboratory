# MinerU2.5-Pro: Pushing the Limits of Data-Centric Document Parsing at Scale

작성일: 2026-09-05

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [연구 질문과 기여](#연구-질문과-기여)
- [방법](#방법)
- [데이터·평가와 수치 결과](#데이터평가와-수치-결과)
- [한계와 재현 주의점](#한계와-재현-주의점)
- [Trillion Labs 블로그와의 관계](#trillion-labs-블로그와의-관계)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 원문: [arXiv:2604.04771](https://arxiv.org/abs/2604.04771)
- 사용 버전: v2, 2026-04-09 (최초 제출 2026-04-06)
- 식별자: `arXiv:2604.04771`, DOI `10.48550/arXiv.2604.04771`
- 저자: Bin Wang 외 42명
- 출판 상태: technical report / arXiv preprint
- 원문 언어: 영어
- 라이선스: arXiv non-exclusive distribution license
- 접근일: 2026-09-05

공식 PDF 43쪽 전체를 90 DPI PNG로 렌더링해 본문·표·그림·부록을 시각 확인했다. 텍스트는 43/43쪽에서 추출되었고 PDF SHA-256은 `6f3d6641aad29f79079ea166a5ab2798f3bc46e53a6f23593b8a3107b1b5d5d6`다. 번역 개작 재배포가 명시적으로 허용되지 않아 [한 문장 대조 인용과 섹션별 상세 해설](MinerU2.5-Pro-%20Pushing%20the%20Limits%20of%20Data-Centric%20Document%20Parsing%20at%20Scale.번역.md)을 제공한다.

## 한눈에 보기

MinerU2.5-Pro는 1.2B 규모 MinerU2.5의 architecture를 바꾸지 않고 데이터 선택, hard-case 교정, 단계별 학습과 평가기 개선으로 문서 파싱 성능을 높인 모델이다. 핵심 주장은 “더 큰 모델”이 아니라 “어떤 데이터를 어떻게 골라 검증하고 학습하는가”가 다음 성능 향상을 만든다는 것이다.

기존 coarse-to-fine 구조는 저해상도 전체 페이지에서 layout을 찾은 뒤 각 crop을 고해상도로 인식한다. Pro는 여기에 DDAS, CMCV, Judge-and-Refine, 세 단계 학습과 OmniDocBench v1.6의 MGAM evaluator를 결합한다.

## 연구 질문과 기여

1. architecture 변경 없이 data-centric pipeline만으로 일반·난문서 성능을 함께 높일 수 있는가?
2. 수천만 자동 label의 noise를 여러 모델 합의와 시각적 재검증으로 제어할 수 있는가?
3. parser마다 다른 block granularity를 더 공정하게 평가할 수 있는가?

기여는 65.5M 규모 Stage 1 데이터, 192K human-labeled hard sample을 포함한 Stage 2, 192K GRPO Stage 3, 그리고 1,651쪽 OmniDocBench v1.6과 MGAM이다.

## 방법

### 기본 architecture

모델은 약 675M NaViT vision encoder와 Qwen2 0.5B decoder를 결합한 약 1.2B coarse-to-fine parser다. 전체 페이지를 저해상도로 분석해 영역을 찾고, 필요한 crop을 고해상도로 다시 읽는다. Pro에서도 이 architecture는 바뀌지 않는다.

### DDAS와 CMCV

DDAS (Diversity-and-Difficulty-Aware Sampling)는 cluster 다양성과 Easy/Medium/Hard 난도를 함께 고려해 데이터가 흔한 쉬운 예제에 쏠리지 않게 한다. CMCV (Cross-Model Consistency Validation)는 MinerU2.5, PaddleOCR-VL, Qwen3-VL-30B의 출력을 text edit distance, table TEDS, formula CDM 같은 task metric으로 비교해 자동 label의 신뢰도와 난도를 정한다.

### Judge-and-Refine

Hard sample의 LaTeX·HTML을 다시 렌더링해 원 이미지와 나란히 Qwen3-VL-235B judge가 비교한다. 수정 후에도 불확실한 예제는 전문가가 주석한다. 의미 문자열만 비교하기 어려운 table·formula에서 시각적 폐루프를 만든다는 점이 중요하다.

### 단계별 학습

- Stage 1: 65.5M sample, 1 epoch. text 21M, layout 14M, formula 13M, table 11.5M, image analysis 6M.
- Stage 2: 3.9M sample, 192K human-labeled hard data와 replay, task-specific mixing.
- Stage 3: 192K sample, group size 16의 GRPO; edit/CDM/TEDS/IoU 기반 reward.

최대 sequence length는 8,192, image token 상한은 $2048\times28\times28$로 제시된다. 단계별 batch size는 256/128/512다.

### MGAM

MGAM (Multi-Granularity Adaptive Matching)은 직접 bipartite matching이 실패하면 예측 block을 분할하고, $n$개 조각의 연속 partition $2^{n-1}$개를 열거해 가장 좋은 대응을 고른다. table-to-text처럼 표현 유형이 다른 경우도 공통 text 표현으로 정규화한다.

## 데이터·평가와 수치 결과

OmniDocBench v1.6은 Base 1,355쪽과 training에 사용하지 않은 Hard 296쪽, 총 1,651쪽이다.

- Full overall: MinerU2.5 92.98 → MinerU2.5-Pro 95.69, +2.71
- Hard overall: 강한 비교 기준 92.01 대비 94.08, +2.07
- 세부 지표: text edit 0.036, formula CDM 97.29, table TEDS 93.42, TEDS-S 95.92, reading-order edit 0.120
- 단계 ablation: 92.98 → Stage 1 94.29 (+1.31) → Stage 2 95.25 (+0.96) → Stage 3 95.69 (+0.45)
- component 분석 예: text edit 0.028 → 0.019, table overall TEDS 91.10, TEDS-S 94.48

서로 다른 표의 Full/Hard, overall/component, TEDS/TEDS-S를 섞지 않아야 한다. 높은 점수는 모델 개선과 v1.6 evaluator 설계가 함께 반영된 결과다.

## 한계와 재현 주의점

- 의미가 같은 수식·표도 serialization 형식이나 구조적 모호성 때문에 다르게 평가될 수 있다.
- 의료·법률 같은 vertical domain 평가 세트가 더 필요하다.
- 평가 신뢰도는 annotation precision의 상한을 넘을 수 없다.
- hierarchy, figure reference, cross-page continuity는 현재 점수가 충분히 포착하지 않는다.
- 자동 judge의 공통 편향과 training/evaluation contamination을 별도 감사해야 한다.
- 노트북은 DDAS·CMCV·MGAM을 작은 합성 데이터로 설명하며 65.5M 학습이나 공식 점수를 재현하지 않는다.

## Trillion Labs 블로그와의 관계

[Trillion Labs 블로그](https://blog.trillionlabs.co/posts/diffusion-ocr/)는 MinerU2.5-Pro를 AR teacher/base로 삼아 Fast-dLLM v2식 block diffusion OCR로 변환하고, 이 논문이 정의한 OmniDocBench v1.6 1,651쪽에서 품질·속도를 비교한다. 블로그 수치는 AR Overall 95.57, 변환 모델 95.16이며, 이 보고서의 95.69와 차이가 있다. evaluator revision, 공개 checkpoint, decoding 설정 또는 집계 시점이 다를 수 있으므로 오류로 단정하지 않고 실행 manifest를 확인해야 한다.

이 논문의 핵심은 data-centric 성능 상한이고 블로그의 핵심은 decoding latency다. 블로그의 약 0.32점 변환 손실을 해석할 때 teacher 자체의 dataset/evaluator별 변동과 table TEDS(0.934→0.928)를 함께 봐야 한다.

## 실습 학습 가이드

- [01_foundations.ipynb](01_foundations.ipynb): 여러 parser의 task별 유사도로 CMCV 난도를 분류한다.
- [02_practice.ipynb](02_practice.ipynb): cluster와 난도를 함께 고려한 DDAS toy sampler를 구현한다.
- [03_advanced.ipynb](03_advanced.ipynb): 연속 partition을 열거하는 작은 MGAM matcher와 단계 ablation을 실험한다.

## 다음 학습 경로

1. OmniDocBench 원 논문과 v1.6 변경점을 먼저 구분한다.
2. CMCV threshold와 judge model을 바꿨을 때 데이터 분포가 어떻게 달라지는지 기록한다.
3. 실제 재현은 dataset manifest, checkpoint hash, evaluator commit, renderer와 decoding configuration을 함께 고정한다.
