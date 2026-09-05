# HunyuanOCR-1.5: Making Lightweight OCR VLMs Faster and Better - 문장 대조 번역과 절별 해설

## 논문 metadata

- 원문 제목: **HunyuanOCR-1.5: Making Lightweight OCR VLMs Faster and Better**
- 저자: Gengluo Li, Xingyu Wan, Shangpin Peng, Weinong Wang, Hao Feng, Yongkun Du, Binghong Wu, Zheng Ruan, Zhiqiong Lu, Liang Wu, Pengyuan Lyu, Huawen Shen, Zibin Lin, Shijing Hu, Jieneng Yang, Hongbing Wen, Guanghua Yu, Hong Liu, Bochao Wang, Can Ma, Han Hu, Chengquan Zhang, Yu Zhou
- 출판처/연도: arXiv preprint (cs.CV), 2026
- 식별자: arXiv:2607.04884, DOI 10.48550/arXiv.2607.04884
- 원문: <https://arxiv.org/abs/2607.04884>
- 사용 버전: v2 (2026-08-06)
- 원문 언어: 영어
- 접근일: 2026-09-05
- 라이선스: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- 변경·동일조건 고지: 이 파일은 원 논문의 일부 문장을 번역하고 나머지를 한국어 해설로 재구성한 개작물이며 CC BY-SA 4.0으로 제공한다.

[분석 README로 돌아가기](README.md)

## 번역·접근 범위

| 구간 | 상태 | 처리 |
|---|---|---|
| Abstract | 부분 번역 | 핵심 6문장 대조 |
| 1 Introduction | 부분 번역 | faster/better 논증 해설 |
| 2 Related Work | 부분 번역 | OCR VLM·MTP 계보 요약 |
| 3 Model Design | 부분 번역 | backbone·DFlash 수식 해설 |
| 4 Agentic Data Flow | 부분 번역 | loop와 세 적용 분야 해설 |
| 5 Training Recipe | 부분 번역 | pretrain/SFT/RL 해설 |
| 6 Evaluation Tree | 부분 번역 | 12개 평가 축 해설 |
| 7 Results | 부분 번역 | 속도·capability 표 수치 해설 |
| 8 Conclusion | 부분 번역 | 결론·future work 요약 |
| References | 원문 확인 | 서지 레코드 미복제 |
| Supplement A-E | 부분 번역 | architecture, prompts, annotation, RL, examples 해설 |

v2 PDF 41/41쪽을 확인했다. 이 문서는 상세한 학습판이지만 전문 번역이라고 주장하지 않는다.

## 읽기 전 핵심 배경

speculative decoding은 빠른 draft와 정확한 target을 분리한다. draft가 틀리면 target 검증에서 거절하므로 최종 sampling distribution을 유지할 수 있다. DFlash의 특이점은 draft token을 다시 AR로 한 개씩 만들지 않고 block diffusion으로 한꺼번에 제안한다는 것이다.

## 문장 대조 번역

### Abstract

**S001 — Original**

We present HunyuanOCR-1.5, a lightweight and end-to-end OCR-specialized vision-language model.

**S001 — 한국어**

(저자들은 경량 end-to-end OCR 전문 시각-언어 모델 HunyuanOCR-1.5를 제시한다.)

- **용어·약어 해설**
  - **VLM (Vision-Language Model, 시각-언어 모델)**: 이미지 token을 조건으로 text/structure를 생성한다.
  - **end-to-end OCR**: layout 분리용 외부 model 없이 page image에서 최종 구조화 출력을 직접 생성한다.

**S002 — Original**

Building upon the validated lightweight architecture of HunyuanOCR-1.0, HunyuanOCR-1.5 does not redesign the model backbone, but instead performs a systematic upgrade around two goals: making the model faster and better.

**S002 — 한국어**

(HunyuanOCR-1.5는 검증된 1.0의 경량 architecture를 바탕으로 backbone을 다시 설계하지 않고, 모델을 더 빠르고 더 좋게 만드는 두 목표를 중심으로 체계적으로 개선한다.)

**S003 — Original**

For efficiency, we adapt DFlash inference acceleration to OCR decoding, significantly reducing the decoding latency of long structured outputs while preserving the output distribution.

**S003 — 한국어**

(효율을 위해 DFlash 추론 가속을 OCR decoding에 적용해 output distribution을 보존하면서 긴 구조화 출력의 decoding latency를 크게 줄인다.)

- **용어·약어 해설**
  - **DFlash**: target hidden state 조건의 block-diffusion draft가 candidate block을 병렬 생성하고 target이 검증하는 방식이다.

**S004 — Original**

Powered by DFlash, HunyuanOCR-1.5 achieves a 6.37× speedup in Transformer inference and a 2.14× speedup under vLLM.

**S004 — 한국어**

(DFlash를 사용한 HunyuanOCR-1.5는 Transformers 추론에서 6.37배, vLLM에서 2.14배 가속을 달성했다고 보고한다.)

**S005 — Original**

For capability, we propose Agentic Data Flow, an agent-driven data construction system that transforms model weaknesses into executable data requirements.

**S005 — 한국어**

(능력 개선을 위해 모델 약점을 실행 가능한 데이터 요구사항으로 바꾸는 agent-driven data construction system인 Agentic Data Flow를 제안한다.)

**S006 — Original**

We will release the model weights and training code to the community to promote research, reproduction, and real-world application.

**S006 — 한국어**

(저자들은 연구·재현·실제 적용을 촉진하기 위해 model weight와 training code를 공개할 예정이라고 밝힌다.)

번역자 주: “will release”는 미래 약속이다. 이 문서에서는 별도로 2026-09-05 현재 공식 repository/model 링크가 열리는 것을 확인했지만, 모든 v1.5 training artifact의 완전성을 뜻하지는 않는다.

### Figure 2 caption 핵심

**S007 — Original**

One target forward is performed, K anchors are sampled at random positions, and all K blocks attend in a single pass.

**S007 — 한국어**

(target forward를 한 번 수행하고 무작위 위치에서 K개 anchor를 뽑은 뒤 K개 block을 한 pass에서 함께 attention 계산한다.)

## 절별 한국어 해설

### 1. Introduction

1.0은 compact end-to-end multi-task OCR의 가능성을 보였다. 1.5는 backbone 규모를 키우기보다 deployment 병목인 long AR output과 long-tail capability gap을 겨냥한다. DFlash, PC-side llama.cpp, 4K/128K, multi-image, task-specific RL이 “faster”와 “better”를 각각 담당한다.

### 2. Related Work

general VLM은 OCR 능력이 있어도 매우 크고 reading order·faithful structured output에 특화되지 않았다. modular OCR은 crop으로 local difficulty를 낮추지만 detector error가 전파된다. end-to-end OCR은 전체 page context를 직접 모델링한다. 기존 speculative decoder가 draft도 AR로 만들면 candidate 수만큼 비용이 늘지만 DFlash는 block을 한 번에 제안한다.

### 3.1 Model Architecture

native-resolution Hunyuan-ViT는 원 aspect ratio를 보존하며 최대 resolution을 2K에서 4K로 높였다. adaptive MLP connector가 visual feature를 compact token으로 압축하고 Hunyuan-0.5B+XD-RoPE가 Markdown/HTML/LaTeX 등을 AR 생성한다. document parsing, spotting, IE, QA, ancient script, chart, translation, subtitle를 동일 model에 통합한다.

### 3.2 DFlash

block size `B=16`, anchor 수 `K=16`, decay `gamma=7.0`, 5-layer·90.7M draft다. target은 freeze하며 cached hidden state 앞부분과 같은 block mask token만 보게 한다.

```text
w_k^(j) = I[k>0] I[valid] exp(-max(k-1,0)/gamma)                     (1)
L_DFlash = (1/Z) Σ_j Σ_k w_k^(j) [-log p_theta(y_k^(j)|h_<a_j,m_1:B^(j))]  (2)
```

anchor 자체와 padding은 loss에서 빼고 먼 token은 예측이 어려우므로 exponential decay한다. inference에서 target은 candidate block을 한 번에 검증하고 longest valid prefix를 받아들인다. table HTML처럼 local regularity가 강한 출력에서 acceptance가 길어진다.

### 4. Agentic Data Flow

일반적인 “데이터를 더 모은다”가 아니라 failure taxonomy를 executable requirement로 만든다. agent가 자료 후보를 찾고 tool로 품질을 검사하며 변환/annotation pipeline을 작성하고, engineer가 model evaluation feedback을 다음 loop에 넣는다. 논문은 ancient-script OCR, low-resource multilingual parsing, multi-image QA/complex structured parsing에 이를 적용한다.

이 접근은 자동화가 곧 정답을 뜻하지 않는다. source license, annotation leakage, synthetic artifact, agent tool error를 human gate와 benchmark 분리로 통제해야 한다.

### 5. Training Recipe

pretraining Stage3를 재구성해 4K image와 128K context, multi-image·historical OCR을 포함한다. SFT는 high-quality task data로 안정적 base를 만들고 RL은 document parsing, spotting, QA 등 task별 reward를 결합한다. factuality-oriented parsing reward, consistency-based QA judge, repetition/overlong suppression이 주요 축이다.

### 6. Evaluation Tree

단일 leaderboard가 아니라 기본 OCR, long-tail, structured element, cross-page/cross-lingual, application/reliability로 나눈다. CHAOS-Bench는 page마다 2-3개 단어의 한 글자를 무의미하게 바꾸고, model output이 그 seen text를 whole-word로 보존했는지 page-average recall을 계산한다.

```text
R_i = (1/|P_i|) Σ_(w in P_i) I_hit(w,O_i)
Recall_page = (1/N) Σ_i R_i
```

### 7.1 Inference speed

| framework | AR latency/TPS | DFlash latency/TPS | speedup | acceptance |
|---|---:|---:|---:|---:|
| Transformers | 34.850s / 40.9 | 5.474s / 245.7 | 6.37× | 8.89 |
| vLLM | 3.032s / 466.9 | 1.408s / 1002.3 | 2.14× | 8.36 |

vLLM에서 output이 0-256이면 `1.31×`, 2,048+이면 `2.30×`다. table `2.39×`가 text `1.81×`보다 크다. concurrency 1의 `2.14×`가 32에서는 `1.80×`로 줄어드는 것은 GPU가 이미 포화되면 speculative draft용 idle compute가 적기 때문이다.

### 7.2 Boundary capability

- Chronicles-OCR: archaic `0.54`, mature `0.79`.
- ChartArena 평균: EN `48.9`, ZH `64.1`.
- TableVerse-5K: TEDS `79.37`, TEDS-S `86.05`.
- DUDE validation: `54.64`로 Qwen3.5-0.8B `56.41`에 근접.
- MORE 149 languages Overall: `91.90`.
- CHAOS-Bench: `14.15`, 비교군 `3.02-6.33`; 상대 우위와 별개로 절대 recall은 낮다.

### 7.3 Existing benchmarks

OmniDocBench v1.6 Overall `94.74`, text edit `0.039`, formula `94.50`, table TEDS/TEDS-S `93.67/94.71`, order edit `0.129`다. Spotting overall `71.40`, no-text 1,000장 accuracy `99.8%`다. MMTIT other-to-English/Chinese `76.51/76.01`, DoTA English-to-Chinese `83.69`; IE cards/receipts `92.40/92.55`, subtitle `93.07`, OCRBench `861`을 보고한다.

OmniDocBench가 multi-line formula를 single-line unit으로 나누는 GT matching은 model의 unified begin/end LaTeX 출력과 완전히 맞지 않아 formula capability를 과소평가할 수 있다고 저자들은 지적한다.

### 8. Conclusion and Future Work

결론은 architecture redesign 없이 inference·data·recipe를 함께 바꾸면 lightweight OCR의 효율과 coverage를 넓힐 수 있다는 것이다. future work는 high-resolution visual token redundancy 감소, continuous data-model co-evolution, 긴 복잡 문서 신뢰성 향상이다.

### Supplementary material

- A: vision encoder, connector, language model의 상세 구성.
- B: task별 권장 instruction.
- C: CHAOS annotation에서 실제 단어가 남는 edit를 제거하는 절차.
- D: spotting·structure-aware parsing·repetition reward algorithm과 RL detail.
- E: ancient scripts, chart, table, multi-image 등 qualitative example.

## 그림·표를 읽는 법

- Figure 2의 파란 영역은 각 draft block이 볼 수 있는 target prefix, 초록은 같은 block의 mask query다. 다른 anchor block끼리는 차단된다.
- Table 2의 latency, TPS, page/s는 같은 framework 안에서 비교해야 한다.
- Table 4의 effective acceptance가 단순 block size 16보다 작다는 것은 rejection이 있음을 뜻한다.
- Table 11에서 best `14.15`를 “faithfulness 해결”로 읽지 않는다.

## 약어 및 기술 용어 사전

| 원어 | 한국어 | 의미 | 최초 등장 |
|---|---|---|---|
| VLM | 시각-언어 모델 | 이미지 조건부 텍스트 생성 모델 | S001 |
| OCR | 광학 문자 인식 | 다양한 text-centric visual task 통합 | S001 |
| DFlash | 확산 draft 가속기 | block diffusion draft + target verification | S003 |
| MTP | 다중 토큰 예측 | 여러 future token을 병렬 제안 | Related Work |
| SFT | 지도 미세조정 | high-quality answer로 post-training | Training |
| RL | 강화학습 | task reward로 generation을 개선 | Training |
| IE | 정보 추출 | card/receipt field 추출 | Evaluation |
| VQA | 시각 질의응답 | 이미지 근거 질문 응답 | Evaluation |
| TPS | 초당 토큰 수 | 처리량 | Results |
| CHAOS-Bench | OCR 시퀀스 종합 환각 평가 | seen-text 보존 recall 평가 | Evaluation |
| FlexAttention | 유연 어텐션 kernel/API | K draft block의 block-diagonal mask 구현 | S007 |

## 번역 검수 기록

- v2 PDF 41/41쪽을 두 contact sheet로 확인하고 수식 페이지, 속도·benchmark 표, supplementary 예시를 원본 해상도로 대조했다.
- `B=16`, `K=16`, `gamma=7.0`, 90.7M, speedup `6.37×/2.14×`, Overall `94.74`, CHAOS `14.15`를 재확인했다.
- Transformers/vLLM 및 output length/concurrency 조건을 섞지 않았다.
- S001-S007만 문장 대조이며, 나머지는 절별 한국어 해설이다.
