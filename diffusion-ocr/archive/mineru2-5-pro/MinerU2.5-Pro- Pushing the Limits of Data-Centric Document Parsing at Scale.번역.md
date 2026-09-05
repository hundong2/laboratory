# MinerU2.5-Pro: Pushing the Limits of Data-Centric Document Parsing at Scale — 제한 번역과 상세 해설

## 논문 메타데이터

- 원문 제목: *MinerU2.5-Pro: Pushing the Limits of Data-Centric Document Parsing at Scale*
- 저자: Bin Wang 외 42명
- 출판: technical report; arXiv v2 (2026-04-09)
- 식별자: `arXiv:2604.04771`, DOI `10.48550/arXiv.2604.04771`
- 원문: <https://arxiv.org/abs/2604.04771>
- 원문 언어: 영어
- 라이선스: arXiv non-exclusive distribution license
- 접근일: 2026-09-05

## 번역·접근 범위

번역 개작 재배포 허용이 명시되지 않아 원문 한 문장만 대조하고 나머지는 상세 한국어 해설로 전환했다. 공식 PDF 43쪽 전부를 렌더링하고 본문·부록의 표와 그림을 시각 확인했다.

| 구간 | 상태 | 제공 범위 |
|---|---|---|
| 제목·초록 | 부분 번역 | 대조 인용 1문장과 핵심 주장 해설 |
| 1 Introduction | 부분 번역 | data-centric 문제 설정 해설 |
| 2 Related Work | 부분 번역 | 문서 파서·데이터 엔진 계보 해설 |
| 3 Method | 부분 번역 | DDAS·CMCV·Judge-and-Refine·학습 상세 해설 |
| 4 OmniDocBench v1.6 | 부분 번역 | dataset 확장·MGAM 해설 |
| 5 Experiments | 부분 번역 | 설정·수치·ablation 해설 |
| 6 Limitations/Conclusion | 부분 번역 | 한계와 결론 해설 |
| Appendix/References | 원문 확인 | 추가 결과와 사례를 선별 해설 |

## 읽기 전 핵심 배경

coarse-to-fine document parser는 전체 페이지를 낮은 해상도로 훑어 element 위치를 찾고, 개별 crop만 높은 해상도로 다시 인식한다. 이 방식은 긴 고해상도 페이지를 한 번에 처리할 때의 visual token 폭증을 피한다. Data-centric improvement는 architecture보다 수집·선별·label 검증·학습 순서의 개선을 우선한다.

## 짧은 문장 대조

### Abstract

**S001 — Original**

Without any architectural modification, MinerU2.5-Pro achieves 95.69 on OmniDocBench v1.6.

**S001 — 한국어**

(MinerU2.5-Pro는 아키텍처를 전혀 수정하지 않고 OmniDocBench v1.6에서 95.69를 달성한다.)

- **용어·약어 해설**
  - **architectural modification(아키텍처 수정)**: vision encoder, language decoder와 coarse-to-fine inference 구조 자체를 바꾸는 일을 뜻한다.
  - **data-centric(데이터 중심)**: 모델 크기나 layer보다 데이터 구성·검증·학습 curriculum을 성능 향상의 주된 수단으로 삼는다.

## 섹션별 상세 해설

### 1. Introduction

저자들은 최근 문서 파서가 architecture 경쟁으로 빠르게 향상됐지만, 고품질 hard data가 부족하고 benchmark의 matching granularity 편향이 남았다고 본다. MinerU2.5-Pro는 MinerU2.5 1.2B architecture를 고정한 채 scalable data engine, progressive training, expanded benchmark를 함께 설계한다.

### 2. Related Work

관련 연구는 pipeline OCR, end-to-end VLM parser, synthetic/auto-labeled data, preference·reinforcement post-training으로 정리된다. Pro의 차이는 여러 parser의 task-specific consensus와 render-based visual judge를 데이터 생산 단계에 결합하고, 같은 hard data를 supervised와 GRPO 단계로 이어 쓴다는 점이다.

### 3. Data-centric pipeline

#### 3.1 기본 모델

약 675M parameter NaViT vision encoder와 Qwen2 0.5B decoder를 합친 약 1.2B 모델이다. 저해상도 global page에서 layout을 예측하고, crop별 high-resolution recognition을 수행한다. Pro 개선 전후 architecture가 같기 때문에 ablation 증분을 데이터·학습 변화에 귀속하기 쉽다.

#### 3.2 DDAS

DDAS (Diversity-and-Difficulty-Aware Sampling)는 먼저 embedding cluster로 내용·형식 다양성을 확보하고 Easy/Medium/Hard 비율을 조정한다. 무작위 대규모 수집에서 흔한 쉬운 text page가 대부분을 차지하는 문제를 막는다. 실제 재현에서는 cluster 크기의 역수 가중만 사용하면 희귀 noise를 과대 선택할 수 있어 최소 품질 gate와 weight cap이 필요하다.

#### 3.3 CMCV

CMCV (Cross-Model Consistency Validation)는 MinerU2.5, PaddleOCR-VL, Qwen3-VL-30B의 예측을 비교한다. text에는 edit similarity, table에는 TEDS, formula에는 CDM처럼 task별 metric을 사용해 합의 정도를 정한다. 높은 합의는 자동 label을 신뢰할 근거가 되지만, 세 모델이 같은 오류를 내면 합의가 정확성을 보장하지 않는다.

#### 3.4 Judge-and-Refine

Hard table·formula output을 HTML/LaTeX에서 image로 다시 render한다. Qwen3-VL-235B가 원 crop과 렌더 결과를 시각 비교해 수정하고, 남은 불확실 사례는 expert annotation으로 넘긴다. 이 폐루프는 문자열은 달라도 시각적으로 같은 식과 표를 다루는 데 유용하지만 renderer 자체의 차이가 judge 입력을 바꿀 수 있다.

### 4. Progressive training

Stage 1은 65.5M sample로 breadth를 학습한다. 구성은 text 21M, layout 14M, formula 13M, table 11.5M, image analysis 6M이다. Stage 2는 3.9M으로 task ratio를 조절하고 192K human-labeled hard sample 및 replay data를 사용한다. Stage 3는 같은 규모 192K에서 GRPO를 적용하며 group size는 16이다.

reward는 task에 맞춰 normalized edit similarity, CDM, TEDS, IoU 등을 사용한다. 여러 reward의 scale이 다르므로 구현에서 정규화·clipping·빈 출력 처리를 고정해야 한다. 표의 공통 설정은 sequence length 8,192, 최대 image token $2048\times28\times28$, 단계별 batch size 256/128/512, 각 1 epoch다.

### 5. OmniDocBench v1.6와 MGAM

v1.6은 Base 1,355쪽에 Hard 296쪽을 더한 1,651쪽이다. Hard set은 모든 training에서 제외했다고 보고한다. 원 OmniDocBench v2의 981쪽보다 크고, dataset뿐 아니라 matching algorithm도 바뀐다.

MGAM은 먼저 직접 bipartite matching을 시도한다. match가 나쁜 예측 block을 작은 조각으로 나누고, $n$개 연속 조각 사이의 $n-1$개 경계를 자를지 말지 선택하여 $2^{n-1}$개 partition을 열거한다. 각 partition의 matching score를 비교해 가장 좋은 granularity를 채택한다. dense text와 table-to-text도 비교 가능한 표현으로 바꾼다.

이 방식은 segmentation 차이에 대한 벌점을 줄이지만 partition 탐색 범위와 score 선택이 benchmark 특성에 맞춰질 위험이 있다. evaluator 버전과 최대 partition 크기를 반드시 기록해야 한다.

### 6. Experiments

Full overall은 MinerU2.5 92.98에서 Pro 95.69로 2.71점 오른다. Hard subset은 강한 비교 모델의 92.01보다 2.07점 높은 94.08이다. 세부적으로 text edit 0.036, formula CDM 97.29, table TEDS 93.42, TEDS-S 95.92, reading-order edit 0.120이 보고된다.

progressive ablation은 baseline 92.98, Stage 1 뒤 94.29(+1.31), Stage 2 뒤 95.25(+0.96), Stage 3 뒤 95.69(+0.45)다. 증분이 누적되어 있으므로 Stage 3 단독 효과로 2.71을 주장할 수 없다. component 표의 text edit 0.019 대 0.028, table overall TEDS 91.10과 TEDS-S 94.48도 서로 다른 집계 열임을 유지해야 한다.

### 7. Limitations and conclusion

저자들은 semantic equivalence가 있는 format과 structure ambiguity, 부족한 vertical-domain set, annotation precision 상한을 한계로 든다. 현재 지표는 hierarchy, figure reference, cross-page continuity도 충분히 평가하지 않는다. 따라서 95점대 overall이 완전한 문서 이해를 뜻하지 않는다.

## Trillion Labs 결과를 읽는 법

블로그는 같은 v1.6 1,651쪽을 사용했다고 설명하지만 AR 95.57을 보고해 이 보고서의 95.69와 0.12 차이가 난다. 공개 코드·checkpoint·evaluator revision과 decoding 설정의 차이일 수 있다. 블로그의 변환 모델 95.16은 teacher 대비 품질 보존을 보는 별도 실험이며, 이 논문의 data-centric ablation과 동일한 비교가 아니다.

## 약어 및 기술 용어 사전

| 원어 | 한국어 | 의미 | 최초 등장 |
|---|---|---|---|
| DDAS | Diversity-and-Difficulty-Aware Sampling, 다양성·난도 인지 표집 | cluster와 난도를 함께 고려하는 데이터 선택 | 섹션 3 |
| CMCV | Cross-Model Consistency Validation, 모델 간 일관성 검증 | 여러 parser의 task별 합의로 label을 검증 | 섹션 3 |
| GRPO | Group Relative Policy Optimization, 그룹 상대 정책 최적화 | 그룹 내 reward를 비교하는 강화학습 방식 | 섹션 4 |
| MGAM | Multi-Granularity Adaptive Matching, 다중 입도 적응 매칭 | block 분할 차이를 partition 탐색으로 완화 | 섹션 5 |
| TEDS | Tree Edit Distance based Similarity | table tree의 구조·내용 유사도 | 섹션 3 |
| CDM | 수식 평가 지표의 공식 약칭 | formula의 구조·시각적 일치도 | 섹션 3 |
| IoU | Intersection over Union, 교집합/합집합 비율 | layout bbox의 겹침 정도 | 섹션 4 |
| NaViT | Native Resolution Vision Transformer | 다양한 원본 해상도를 다루는 vision encoder 계열 | 섹션 3 |

## 번역 검수 기록

- `S001` 원문·한국어의 1:1 대응을 확인했다.
- 직접 인용은 25단어 미만 한 문장으로 제한했다.
- 단계별 data scale, 주요 점수와 ablation을 PDF 표와 대조했다.
- 원본 OmniDocBench 981쪽과 v1.6 1,651쪽을 구분했다.
- 43/43쪽 렌더에서 빈 페이지와 잘린 페이지가 없음을 확인했다.

[학습 README로 돌아가기](README.md)
