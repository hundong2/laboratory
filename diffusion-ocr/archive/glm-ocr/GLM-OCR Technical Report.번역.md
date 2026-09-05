# GLM-OCR Technical Report - 문장 대조 번역과 절별 해설

## 논문 metadata

- 원문 제목: **GLM-OCR Technical Report**
- 저자: Shuaiqi Duan, Yadong Xue, Weihan Wang, Zhe Su, Huan Liu, Sheng Yang, Guobing Gan, Guo Wang, Zihan Wang, Shengdong Yan, Dexin Jin, Yuxuan Zhang, Guohong Wen, Yanfeng Wang, Yutao Zhang, Xiaohan Zhang, Wenyi Hong, Yukuo Cen, Da Yin, Bin Chen, Wenmeng Yu, Xiaotao Gu, Jie Tang
- 출판처/연도: arXiv preprint (cs.CL), 2026
- 식별자: arXiv:2603.10910, DOI 10.48550/arXiv.2603.10910
- 원문: <https://arxiv.org/abs/2603.10910>
- 사용 버전: v2 (2026-03-16)
- 원문 언어: 영어
- 접근일: 2026-09-05
- 라이선스: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- 변경 고지: 원 논문의 일부를 한국어 번역하고 나머지를 학습용 절별 해설로 재구성했다.

[분석 README로 돌아가기](README.md)

## 번역·접근 범위

| 구간 | 상태 | 처리 |
|---|---|---|
| 제목·Abstract | 부분 번역 | 핵심 문장 5개 대조 |
| 1 Introduction | 부분 번역 | 핵심 수치·주장 상세 해설 |
| 2 Methodology | 부분 번역 | architecture/task/MTP 해설 |
| 3 Evaluation | 부분 번역 | 공개·사내 표 수치 해설 |
| 4 Inference and Deployment | 부분 번역 | page throughput와 지원 stack 해설 |
| 5 Intended Use Cases | 부분 번역 | prompt·SDK 사용 구분 |
| 6 Limitations | 부분 번역 | 명시적 한계 전체 요약 |
| 7 Conclusion | 부분 번역 | 결론 요약 |
| References | 원문 확인 | 서지 레코드 미복제 |

v2 PDF 17/17쪽과 표 1-6, 그림 1-7을 확인했다. CC BY 4.0 조건을 따르지만 이 문서는 전문 번역이 아니다.

## 읽기 전 핵심 배경

OCR 제품의 지연은 모델 decoder뿐 아니라 layout detection, crop, scheduling, merge, serialization에서 결정된다. GLM-OCR은 decoder 수준 MTP와 page 수준 region parallelism을 분리해 최적화한다. 이 구조를 이해하지 않으면 `tokens/step`, `tokens/s`, `pages/s`라는 서로 다른 측정치를 혼동하기 쉽다.

## 문장 대조 번역

### Abstract

**S001 — Original**

GLM-OCR is an efficient 0.9B-parameter compact multimodal model designed for real-world document understanding.

**S001 — 한국어**

(GLM-OCR은 실제 환경의 문서 이해를 위해 설계된 효율적인 0.9B parameter compact multimodal model이다.)

- **용어·약어 해설**
  - **0.9B**: 약 9억 parameter를 뜻하며 0.4B vision encoder와 0.5B language decoder로 구성된다.

**S002 — Original**

It combines a 0.4B-parameter CogViT visual encoder with a 0.5B-parameter GLM language decoder, achieving a strong balance between computational efficiency and recognition performance.

**S002 — 한국어**

(0.4B CogViT vision encoder와 0.5B GLM language decoder를 결합해 계산 효율과 인식 성능의 균형을 노린다.)

**S003 — Original**

To address the inefficiency of standard autoregressive decoding in deterministic OCR tasks, GLM-OCR introduces a Multi-Token Prediction (MTP) mechanism that predicts multiple tokens per step.

**S003 — 한국어**

(결정적 OCR 과제에서 표준 자기회귀 디코딩이 비효율적인 문제를 다루기 위해, GLM-OCR은 step마다 여러 토큰을 예측하는 Multi-Token Prediction(MTP)을 도입한다.)

- **용어·약어 해설**
  - **MTP (Multi-Token Prediction, 다중 토큰 예측)**: 서로 다른 future offset을 담당하는 보조 head가 다음 여러 토큰을 함께 제안한다.

**S004 — Original**

At the system level, a two-stage pipeline is adopted: PP-DocLayout-V3 first performs layout analysis, followed by parallel region-level recognition.

**S004 — 한국어**

(시스템 수준에서는 PP-DocLayout-V3가 먼저 layout analysis를 수행하고 이어서 region-level recognition을 병렬 처리하는 2단계 pipeline을 사용한다.)

**S005 — Original**

Its compact architecture and structured generation make it suitable for both resource-constrained edge deployment and large-scale production systems.

**S005 — 한국어**

(compact architecture와 structured generation 덕분에 자원이 제한된 edge deployment와 대규모 production system 모두에 적합하다고 저자들은 설명한다.)

### Figure 2 caption 핵심

**S006 — Original**

This system supports two primary tasks: Document Parsing and Key Information Extraction.

**S006 — 한국어**

(이 시스템은 Document Parsing과 Key Information Extraction이라는 두 가지 주요 과제를 지원한다.)

## 절별 한국어 해설

### 1. Introduction

기존 OCR pipeline은 plain text에는 효과적이지만 복잡한 layout·format·생산 요구에서 rule과 module 사이 오류가 쌓인다. 반면 대형 MLLM은 통합성이 좋지만 parameter, memory, AR latency가 크다. GLM-OCR은 정확도만이 아니라 throughput·latency·integration·domain adaptation을 함께 설계 목표로 둔다.

MTP는 학습 시 10 token future를 예측하고 추론에서 평균 5.2 token/step을 생성해 약 50% throughput improvement를 가져왔다고 보고한다. 이는 한 번에 항상 10개를 확정한다는 뜻이 아니다. candidate 중 유효한 prefix 길이가 입력마다 달라진다.

### 2. Methodology

#### 2.1 Model overview

CogViT가 image embedding을 만들고 connector가 language embedding space의 prefix token으로 투영한다. GLM decoder는 Markdown/JSON을 생성한다. MTP auxiliary layer들은 parameter를 공유해 memory overhead를 낮춘다.

Document Parsing은 layout detector가 paragraph/table/formula region을 나누고 core가 각 crop을 독립 처리한다. merge 단계가 reading order와 structured output을 복원한다. KIE는 전체 이미지와 task-specific schema prompt를 core에 넣으며 explicit crop을 사용하지 않는다. 두 과제는 모두 visual-conditioned structured generation이지만 preprocessing이 다르다.

#### 2.2 Training recipe

| 단계 | 핵심 데이터 | 목적 |
|---|---|---|
| 1 Vision encoder | image-text, grounding/retrieval | MIM+CLIP와 larger ViT distillation |
| 2.1 Pretrain | image-text, parsing, grounding, VQA | vision-language alignment |
| 2.2 Pretrain+MTP | parsing, grounding, VQA | multi-token generation 적응 |
| 3 SFT+MTP | text/formula/table/KIE | task specialization |
| 4 RL | 같은 OCR task rollout | 구조·정확도 개선 |

RL reward는 text=NED, formula=CDM+구조 validity, table=TEDS+tag closure, KIE=field F1+JSON validation이다. 모든 과제에 repetition과 malformed structure penalty를 둔다.

### 3. Evaluation

공개 benchmark에서 OmniDocBench v1.5 Overall `94.62`로 PaddleOCR-VL-1.5 `94.50`보다 조금 높다. 세부적으로 GLM-OCR은 table TEDS/TEDS-S `93.96/96.39`가 강하지만 text edit은 `0.040` 대 `0.035`, formula CDM은 `93.90` 대 `94.21`로 PaddleOCR-VL-1.5가 근소 우세다. 단일 Overall만 보면 이런 trade-off가 가려진다.

공개 표의 주요 값은 OCRBench Text `94.0`, UniMERNet `96.5`, PubTabNet `85.2`, TEDS_TEST `86.0`, Nanonets-KIE `93.7`, Handwritten-KIE `86.1`이다.

사내 평가에서 open-weight 비교군 중 6개 과제 중 5개를 선도했다고 보고한다. seal `90.5`, real-world table `91.5`, receipt KIE `94.5`가 두드러진다. 그러나 data split·annotation·외부 재현 protocol이 공개 benchmark만큼 투명하지 않으므로 독립 검증된 수치로 취급하면 안 된다.

### 4. Inference and Deployment

vLLM, SGLang, Ollama와 SDK를 지원한다. single replica·single concurrency에서 image `0.67/s`, PDF `1.86 pages/s`이며 PaddleOCR-VL-1.5는 `0.39/s`, `1.22 pages/s`였다. 구체 hardware가 표 주변에 적혀 있지 않아 다른 환경 예측에 그대로 쓰기 어렵다. MaaS API와 LLaMA-Factory full fine-tuning 경로도 제공한다.

### 5. Intended Use Cases

- SDK: complex document를 layout 분할부터 merge까지 처리하는 end-to-end parsing.
- Base model: text/table/formula crop을 prompt로 직접 인식.
- KIE: 원하는 JSON schema를 prompt에 명시해 invoice·receipt field를 추출.

표는 HTML, 수식은 LaTeX, KIE는 JSON처럼 task별 output contract가 다르므로 downstream validator를 함께 두는 것이 중요하다.

### 6. Limitations

1. layout detector 오류가 region recognition과 reading order에 전파된다.
2. cross-page·불규칙 multi-column에서 merge가 불완전할 수 있다.
3. 저해상도·왜곡, 매우 복잡한 수식·표, 저자원 언어에서 학습 분포 한계가 있다.
4. whitespace와 line break 등 formatting variation을 완전히 제거하지 못한다.
5. KIE는 prompt와 schema가 모호하면 누락·중복 field가 생길 수 있다.

### 7. Conclusion

저자들의 결론은 parameter scale을 늘리는 대신 layout-aware preprocessing, multi-token decoding, structured reward를 task 구조에 맞추면 작은 모델도 실용적인 효율-정확도 균형을 낼 수 있다는 것이다. 향후 과제로 extreme layout, multilingual coverage, structured-output consistency를 든다.

## 그림·표를 읽는 법

- Figure 2에서 Document Parsing은 detector를 거치고 KIE는 direct full-image prompt 경로다.
- Table 3은 여러 dataset의 metric scale을 0-100처럼 통일해 제시하지만 각 benchmark 정의는 다르므로 행간 값을 직접 평균내면 안 된다.
- Table 4의 Overall은 text·formula·table·order 세부 지표와 방향이 다르다. `↓`인 edit를 “높을수록 좋다”로 잘못 읽지 않는다.
- Table 6의 image/s와 PDF pages/s는 pipeline 단위가 다르다.

## 약어 및 기술 용어 사전

| 원어 | 한국어 | 의미 | 최초 등장 |
|---|---|---|---|
| OCR | 광학 문자 인식 | 문서의 문자·구조 복원 | S001 |
| MTP | 다중 토큰 예측 | 한 step에 여러 future token 후보 생성 | S003 |
| KIE | 핵심 정보 추출 | 지정 field를 구조화해 추출 | S006 |
| MLLM | 멀티모달 대규모 언어 모델 | vision-language 통합 생성 모델 | 배경 |
| MIM | 마스킹 이미지 모델링 | 가린 image patch를 학습하는 objective | Training |
| CLIP | 대조적 언어-이미지 사전학습 | image-text representation 정렬 | Training |
| SFT | 지도 미세조정 | 정답 pair로 task adaptation | Training |
| GRPO | Group Relative Policy Optimization | rollout group의 상대 reward로 최적화 | Training |
| NED | 정규화 편집 거리 | text 오류 지표 | Training |
| CDM | 수식 평가 지표 | formula 일치도 | Training |
| TEDS | 트리 편집 유사도 | table 구조·내용 유사도 | Training |

## 번역 검수 기록

- v2 PDF 17/17쪽을 렌더링해 표·그림·본문·참고문헌 페이지를 확인했다.
- 0.9B 구성, 평균 5.2 token/step, 약 50%, OmniDocBench `94.62`, throughput `0.67/1.86`을 원문 표와 대조했다.
- 공개 benchmark와 in-house 결과를 구분하고, hardware 미기재·pipeline 범위 차이를 표시했다.
- 문장 대조는 S001-S006이며 나머지는 절별 해설이다.
