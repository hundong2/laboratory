# Nemotron-Labs-Diffusion - 선택 문장 대조 번역과 절별 해설

## 논문 metadata

| 항목 | 내용 |
|---|---|
| 원문 제목 | Nemotron-Labs-Diffusion: A Tri-Mode Language Model Unifying Autoregressive, Diffusion, and Self-Speculation Decoding |
| 저자 | Yonggan Fu; Lexington Whalen; Abhinav Garg; Chengyue Wu; Maksim Khadkevich; Nicolai Oswald; Enze Xie; Daniel Egert; Sharath Turuvekere Sreenivas; Shizhe Diao; Chenhan Yu; Ye Yu; Weijia Chen; Sajad Norouzi; Jingyu Liu; Shiyi Lan; Ligeng Zhu; Jin Wang; Jindong Jiang; Morteza Mardani; Mehran Maghoumi; Song Han; Ante Jukić; Nima Tajbakhsh; Jan Kautz; Pavlo Molchanov |
| 출판처·연도 | arXiv preprint, 2026 |
| 식별자 | arXiv:2607.05722, DOI 10.48550/arXiv.2607.05722 |
| 원문 URL | <https://arxiv.org/abs/2607.05722> |
| 사용 버전 | v1, 2026-07-07 |
| 원문 언어 | 영어 |
| 접근일 | 2026-09-05 |
| 라이선스 | Creative Commons Attribution 4.0 International (CC BY 4.0) |

[학습 README로 돌아가기](./README.md)

## 번역·접근 범위

CC BY 4.0 원문이지만 이 아카이브는 전문 대체물이 아니라 검증 가능한 학습 자료를 목표로 한다. 핵심 문장 한 개를 즉시 대조하고, 나머지는 PDF 전체를 근거로 절별 해설한다. v1 PDF 21쪽 전체와 부록 A-C를 확인했다.

| 구역 | 상태 | 처리 |
|---|---|---|
| metadata·Abstract | 부분 번역 | 짧은 핵심 문장 대조 + 상세 요약 |
| 1 Introduction | 부분 번역 | 연구 질문·기여 해설 |
| 2 Tri-Mode LM Training | 부분 번역 | 목적식·attention·ablation 해설 |
| 3 Tri-Mode LM Inference | 부분 번역 | 3 mode·LoRA·quadratic 해설 |
| 4 Speed-of-Light Analysis | 부분 번역 | 정의·수치·비교 한계 해설 |
| 5 Model Family | 부분 번역 | base/instruct/VLM recipe |
| 6 Evaluation and Analysis | 부분 번역 | 표와 시스템 결과 |
| 7 Related Work | 부분 번역 | 연구 계보 |
| 8 Insights and Future Directions | 부분 번역 | 저자 통찰·열린 문제 |
| Appendix A-C | 부분 번역 | sampler/LoRA/quadratic 보충 |
| References | 원문 미수록 | 원문 PDF 참조 |

## 읽기 전 핵심 배경

- tri-mode: 동일 weights가 AR, diffusion, self-speculation의 세 inference path를 제공한다.
- TPF (Tokens Per Forward, forward당 토큰): 모델 forward 한 번당 확정된 평균 token 수다.
- MTP (Multi-Token Prediction, 다중 토큰 예측): 별도 prediction heads로 미래 여러 token을 제안한다.
- self-speculation: 별도 작은 drafter 없이 같은 모델의 다른 mode가 draft와 verify를 나눈다.

## 선택 문장 대조

### Abstract

**S001 — Original**

We introduce Nemotron-Labs-Diffusion, a tri-mode language model (LM) that unifies AR, diffusion, and self-speculation decoding within a single architecture.

**S001 — 한국어**

(우리는 하나의 아키텍처 안에서 AR, 확산, 자기 추측 디코딩을 통합한 3중 모드 언어 모델 Nemotron-Labs-Diffusion을 제안한다.)

- **용어·약어 해설**
  - **AR (Autoregressive, 자기회귀)**: 앞 token에 조건부로 다음 token을 만드는 경로다.
  - **self-speculation(자기 추측 디코딩)**: 이 논문에서는 diffusion path가 draft하고 AR path가 검증한다.

## 절별 한국어 해설

### 1. Introduction

논문은 diffusion LM의 낮은 학습 효율과 실제 sampler 성능, MTP 대비 불분명한 시스템 이득을 문제로 든다. AR과 diffusion을 대체재로 보지 않고 `causal next-token prior + bidirectional lookahead`의 보완재로 본다. 하나의 model을 deployment concurrency에 맞춰 mode-switch하는 것이 핵심 제품 관점이다.

### 2. Tri-Mode LM Training

#### 2.1 Objectives

```text
L(theta) = L_AR(theta) + alpha L_diff(theta), alpha = 0.3
```

block `b`의 noisy token은 같은 block 및 이전 clean prefix를 조건으로 원 token을 복원한다. Stage 1은 pure AR, Stage 2는 joint training이다. alpha sweep 0.1-1.0에서 저자 실험상 AR과 diffusion 평균이 모두 0.3 부근에서 가장 높아 두 loss가 capacity를 제로섬으로 다투지 않는다고 해석한다.

#### 2.2 Attention

한 sample의 clean/noisy view를 연결한다. clean stream은 strict causal, noisy stream은 block 내부 bidirectional, noisy-to-clean은 이전 block만 허용한다. 이 구성으로 한 forward-backward 안에서 AR loss와 diffusion loss를 계산하면서 label leakage를 막는다.

#### 2.3 Training ablation

Ministral3-8B base에서 25B tokens continued pretraining한 누적 ablation은 평균 54.23 -> 56.35 -> 57.06 -> 62.80 -> 70.28을 보인다. global average는 mask 수가 적은 sample이 큰 `1/t` loss를 독점하지 않게 한다. rank별 다른 mask ratio는 batch의 noise-level coverage를 넓힌다. 가장 큰 증가가 two-stage와 AR loss에서 나타났다.

#### 2.4 Mutual impact

alpha를 올리면 한 mode가 오르고 다른 mode가 내리는 단순 trade-off가 나타나지 않았다. 저자는 diffusion loss가 미래 계획을 드러내고 AR loss가 자연어 순서를 anchor한다고 해석한다. 단, 제한된 alpha grid와 benchmark의 관찰이며 인과 기전을 완전히 증명한 것은 아니다.

### 3. Tri-Mode LM Inference

#### Mode 1 - AR

표준 causal KV cache로 한 token씩 생성한다. high-concurrency에서 batching으로 GPU를 충분히 채울 수 있을 때 적합하다.

#### Mode 2 - block-wise diffusion

현재 block을 mask로 두고 confidence threshold 또는 trained sampler가 안전하다고 본 위치를 병렬 commit한다. 완료 block은 KV cache에 들어간다. sampler가 threshold를 낮추면 TPF는 늘 수 있으나 conditional context가 바뀌어 오류가 날 수 있다.

#### Mode 3 - self-speculation

diffusion mode가 `k` token draft를 만든 뒤 AR mode가 causal logits로 왼쪽부터 검증한다. longest accepted prefix만 확정하므로 AR greedy path를 보존할 수 있다. 한 cycle에 draft와 verify 두 forward가 필요하다.

LoRA-enhanced variant는 diffusion draft path의 `o_proj`만 약 36M parameters로 조정한다. quadratic variant는 한 forward 안에 여러 acceptance point를 펼치지만 `O(k^2)` input cost를 지닌다.

### 4. Speed-of-Light Analysis

SOL은 diffusion model 자체가 한 position씩 serial denoise했을 때 얻는 target을 기준으로 한다. recursive dynamic compaction은 confidence순 match 중 target을 바꾸지 않는 최대 subset을 탐색한다. block 32의 713 SPEED-Bench samples에서 평균 acceptance 7.60, multilingual 11.26, coding 10.24를 보고했다.

linear self-speculation은 acceptance가 SOL에 가깝지만 두 forward 비용과 prefix-only 제한 때문에 real TPF가 3.41이었다. SOL의 6.02는 76.5% 더 높다. 그러나 SOL은 AR target이 아니라 diffusion serial target을 보존하고 비현실적으로 비싼 search를 쓰므로, 이는 연구 상한이지 바로 배포 가능한 1.765x 속도 향상이 아니다.

### 5. Model Family

3B/8B/14B base 및 instruct, 8B VLM을 만든다. 8B base는 Stage 1 1T AR tokens와 Stage 2 300B joint tokens, length 4096로 continued pretraining했다. instruct는 45B SFT tokens, length 16K로 joint train한다. VLM은 vision encoder와 2-layer MLP projector를 합치고 LM backbone의 tri-mode 능력을 유지한다.

### 6. Evaluation and Analysis

NLD-8B instruct 10-task 평균은 AR 63.61, diffusion 63.18, linear SS 62.81, quadratic SS 64.04다. TPF는 1.00/2.57/5.99/6.38이다. 단일 H100 PyTorch와 GB200 SGLang 등 시스템이 섞이므로 동일 표 안의 algorithmic TPF와 실제 throughput plot을 분리해 읽어야 한다.

SGLang 배포에서 low concurrency self-speculation이 유리하고 high concurrency에서는 AR batching과 격차가 줄었다. category별 acceptance는 structured coding/math/multilingual에서 높았다. 이는 OCR의 표·수식 출력이 diffusion draft와 잘 맞는다는 Trillion Labs 관찰과 연결된다.

### 7. Related Work

LLaDA/Dream masked diffusion, Block Diffusion/Fast-dLLM 계열의 block factorization, joint AR-diffusion, speculative decoding/Eagle3 계열과 비교한다. 차이는 하나의 모델군을 세 mode로 실제 배포하고 SOL 분석까지 묶었다는 점이다.

### 8. Insights and Future Directions

저자는 joint training에서 tri-mode가 자연스럽게 나오며, variance reduction과 충분히 강한 AR initialization이 중요하다고 정리한다. 열린 문제는 (1) confidence sampler와 SOL의 격차, (2) prefix가 아닌 비연속 위치의 안전 검증, (3) token-level을 넘어 segment/paragraph 수준의 병렬성이다.

### Appendix A-C

diffusion sampler 세부, LoRA-enhanced linear SS의 loss와 active-position mask, quadratic SS attention layout을 보충한다. 특히 LoRA 학습은 accepted prefix와 첫 rejected position에만 loss를 두어 실제 cache-rebuild 지점과 맞춘다.

## 수식·그림·표 읽기

- Figure 1: mode별 accuracy-throughput와 concurrency curve를 구분한다.
- Figure 3: clean/noisy attention의 세 관계와 leakage 차단을 읽는다.
- Table 5: 같은 NLD checkpoint의 mode별 accuracy/TPF가 핵심 통제 비교다.
- Figure 7/Table 4: SOL acceptance와 real TPF는 분모가 다르므로 같은 값으로 취급하지 않는다.

## 약어 및 기술 용어 사전

| 원어·약어 | 한국어 | 역할 | 최초 등장 |
|---|---|---|---|
| NLD | Nemotron-Labs-Diffusion | 제안 tri-mode model family | S001 |
| AR | 자기회귀 | causal generation 및 verifier | S001 |
| self-speculation | 자기 추측 디코딩 | diffusion draft + AR verify | S001 |
| MTP | 다중 토큰 예측 | 비교 대상 auxiliary-head acceleration | 배경 |
| TPF | forward당 토큰 | algorithmic parallelism 지표 | 배경 |
| SOL | 속도 상한 분석 | diffusion serial target의 안전 병렬 commit 상한 | 4 |
| LoRA | 저랭크 적응 | draft path를 verifier에 맞추는 소형 adapter | 3 |
| global loss averaging | 전역 손실 평균 | batch token을 동일 가중해 variance 완화 | 2 |
| recursive dynamic compaction | 재귀 동적 압축 | SOL의 안전 subset 탐색 | 4 |

## 번역 검수 기록

- arXiv v1 metadata, CC BY 4.0 링크, PDF title/authors를 대조했다.
- 21쪽 전체를 렌더링해 Figure 1-12, Table 1-10, Appendix A-C의 배치를 확인했다.
- 인용문은 S001 한 개이며 Original 직후 동일 ID의 한국어 문장이 있다.
- 76.5%, 6.02/3.41 TPF, 3B/8B/14B, alpha=0.3을 PDF 표·본문과 재확인했다.
- SOL과 실제 sampler, diffusion target과 AR target의 차이를 명시했다.
