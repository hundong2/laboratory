# Fast-dVLM - 선택 문장 대조 번역과 절별 해설

## 논문 metadata

| 항목 | 내용 |
|---|---|
| 원문 제목 | Fast-dVLM: Efficient Block-Diffusion VLM via Direct Conversion from Autoregressive VLM |
| 저자 | Chengyue Wu; Shiyi Lan; Yonggan Fu; Sensen Gao; Jin Wang; Jincheng Yu; Jose M. Alvarez; Pavlo Molchanov; Ping Luo; Song Han; Ligeng Zhu; Enze Xie |
| 출판처·연도 | arXiv preprint, 2026 |
| 식별자 | arXiv:2604.06832, DOI 10.48550/arXiv.2604.06832 |
| 원문 URL | <https://arxiv.org/abs/2604.06832> |
| 사용 버전 | v2, 2026-04-10 |
| 원문 언어 | 영어 |
| 접근일 | 2026-09-05 |
| 라이선스 | CC BY-NC-ND 4.0 |

[학습 README로 돌아가기](./README.md)

## 번역·접근 범위

NoDerivatives 조건을 존중해 전문 번역을 제공하지 않는다. 핵심을 대표하는 짧은 문장 하나만 대조하고, 나머지는 독립적인 절별 한국어 분석이다. 공식 v2 PDF 20쪽 전체, 표·그림·알고리즘과 부록 A-D를 확인했다.

| 구역 | 상태 | 처리 |
|---|---|---|
| metadata·Abstract | 부분 번역 | 짧은 대조 1개 + 해설 |
| 1 Introduction | 부분 번역 | 문제·기여 해설 |
| 2 Related Work | 부분 번역 | 계보 해설 |
| 3 Methodology | 부분 번역 | 변환·attention·training·inference |
| 4 Experiments | 부분 번역 | 11 tasks·ablation·speed 수치 |
| 5 Conclusion | 부분 번역 | 주장·적용 범위 |
| Appendix A-D | 부분 번역 | data/config/algorithm/case/related work |
| References | 원문 미수록 | 공식 PDF 참조 |

## 읽기 전 핵심 배경

- VLM (Vision-Language Model, 시각-언어 모델): image tokens와 text tokens를 같은 decoder 문맥에서 처리한다.
- block diffusion: block 사이는 causal, block 내부 mask는 bidirectional하게 복원한다.
- direct conversion: 이미 multimodal alignment된 AR VLM 전체를 diffusion objective로 바로 미세조정한다.
- NFE (Number of Function Evaluations, 모델 평가 횟수): generation 중 model forward 수다.

## 선택 문장 대조

### Abstract

**S001 — Original**

We present Fast-dVLM, a block-diffusion-based VLM that enables KV-cache-compatible parallel decoding and speculative block decoding for inference acceleration.

**S001 — 한국어**

(우리는 KV 캐시와 호환되는 병렬 디코딩 및 추론 가속용 추측 블록 디코딩을 지원하는 block-diffusion VLM, Fast-dVLM을 제시한다.)

- **용어·약어 해설**
  - **KV cache(키-값 캐시)**: 이미 확정한 prefix의 attention key/value를 재사용해 반복 계산을 줄인다.
  - **speculative block decoding(추측 블록 디코딩)**: diffusion draft를 causal AR path가 검증해 여러 token을 안전하게 확정한다.

## 절별 한국어 해설

### 1. Introduction

batch 1의 VLM decoding은 매 token마다 weights를 읽는 memory-bandwidth-bound 작업이 되기 쉽다. diffusion은 block 안 여러 token을 동시에 처리해 hardware parallelism을 활용할 수 있지만, vision embeddings와 discrete text, multi-turn boundary, AR capability 보존 문제가 있다. 논문은 변환 경로와 serving stack을 함께 설계 대상으로 삼는다.

### 2. Related Work

LLaDA/Dream의 full-sequence masked diffusion, Block Diffusion/Fast-dLLM의 block causal KV caching, LLaDA-V/MMaDA 등 diffusion VLM, speculative decoding을 연결한다. Fast-dVLM의 차별점은 multimodal pretrained checkpoint의 direct conversion과 block-level self-speculation, SGLang 통합의 결합이다.

### 3. Methodology

#### 3.1 Preliminary

응답을 size `B` block으로 나누고 block 안은 diffusion, block 사이는 autoregression으로 factorize한다. 완료 block의 KV는 cache하고 현재 block만 반복 denoise한다. vision은 continuous embedding이지만 noise 대상은 response text token뿐이다.

#### 3.2 Conversion strategies

two-stage는 text LLM을 diffusion화한 뒤 vision을 결합한다. direct는 Qwen2.5-VL-3B에서 즉시 multimodal diffusion fine-tuning한다. 약 2M multimodal samples와 1 epoch를 맞춘 결과 direct 평균 73.3, two-stage 60.2다. 저자는 multimodal alignment를 처음부터 다시 만들지 않는 이점으로 설명한다.

#### 3.3 Training

`[w_t; x]` dual stream에서 `x=(v,w)`는 clean, `w_t`는 noisy response text다. vision token은 `x`에만 한 번 존재한다. noisy token은 같은 block과 이전 clean context를 보고, clean stream은 causal이다. AR/diffusion loss는 0.5씩 가중한다.

block-size annealing은 작은 span의 denoising부터 학습하고 32까지 키운다. auto-truncation은 multi-turn response 끝에서 block을 잘라 다음 prompt가 정답으로 보이는 leakage를 막는다. vision-efficient concatenation은 H100/context 2048에서 peak memory 15.0%, time 14.2% 감소로 보고됐다.

#### 3.4 Inference

현재 block 첫 token은 causal context에서 생성하고 나머지를 mask로 둔다. MDM은 `tau` 이상 confidence 위치를 병렬 확정한다. linear self-spec은 block draft와 causal verify에 정확히 두 forward를 쓰며 longest matching prefix와 첫 AR correction을 commit한다. quadratic은 `B(B+1)` tokens의 구조화 input으로 verify와 proposal을 합친다.

SGLang은 bidirectional draft와 causal verify를 번갈아 scheduling하고 같은 paged KV cache를 사용한다. SmoothQuant W8A8(FP8)은 별도 시스템 최적화다.

### 4. Experiments

#### 4.1 Setup

Qwen2.5-VL-3B, target block 32, 약 2M samples, 64 H100, BF16/ZeRO-2, global batch 256, peak LR `5e-6`, 1 epoch다. 10 short-answer tasks와 MMMU-Pro-V long-answer를 VLMEvalKit으로 평가한다.

#### 4.2 Main results

10 short-answer 평균은 AR 74.0, MDM 73.3, self-spec 74.0이다. Tokens/NFE는 1.00, 1.95, 2.63이다. MMMU-Pro-V는 26.3, 21.4, 24.6으로 긴 chain-of-thought에서 격차가 남는다.

#### 4.3 Direct vs two-stage

direct는 모든 10축에서 높고 평균 13.1 point 차이다. 제한 예산의 sample efficiency 증거이지 두 전략의 충분히 긴 학습 후 ceiling을 비교한 것은 아니다.

#### 4.4 Ablation

ShareGPT4V subset의 full recipe 평균 57.3에서 causal context 제거 시 44.4, annealing 제거 54.8, auto-truncation 제거 55.2다. causal context가 가장 큰 영향을 보이지만 누적된 pretrained representation과 AR co-training을 동시에 바꾸는 요소라 단일 원인으로 축약하면 안 된다.

#### 4.5 Acceleration

`tau=0.9`는 21.4 accuracy/1.95 token-step, `tau=0.4`는 18.5/2.90이다. linear self-spec은 112.7 TPS로 AR 56.7의 1.98x다. SGLang 319.0, FP8 350.3 TPS까지 누적하면 6.18x지만 MMMU-Pro-V 점수는 23.8로 AR보다 2.5 낮다. quadratic은 Tokens/NFE가 더 높아도 `O(B^2)` input 때문에 모든 block size에서 TPS가 낮았다.

### 5. Conclusion

직접 변환이 제한 budget에서 더 효율적이고, block diffusion과 self-speculation을 production serving에 연결할 수 있다는 결론이다. “11 tasks에서 AR counterpart를 match한다”는 short-answer 평균 중심이며 long-answer와 quantized end-to-end 지표에는 잔여 품질 차이가 있다.

### Appendix A-D

- A: training mixture 약 2M, 64 H100 configuration, 11 benchmark와 protocol.
- B: linear/quadratic self-spec pseudocode. linear 최대 이론 speedup `B/2`, quadratic input cost `O(B^2)`.
- C: math, art, chart, driving, manipulation 정성 사례. safety 검증이 아니라 capability illustration이다.
- D: diffusion LLM/VLM 및 speculative decoding 확장 비교.

## 그림·표 읽기

- Figure 1(c)/Table 4는 각 optimization을 누적한다. 6.18x를 model algorithm 하나의 효과로 읽지 않는다.
- Figure 3의 빈 attention 영역이 label leakage를 막는 핵심이다.
- Table 1-2에서 short-answer 평균과 MMMU-Pro-V long-answer를 분리한다.
- Figure 6은 NFE와 wall-clock TPS의 순위가 다를 수 있음을 보여준다.

## 약어 및 기술 용어 사전

| 원어·약어 | 한국어 | 역할 | 최초 등장 |
|---|---|---|---|
| VLM | 시각-언어 모델 | image와 text를 함께 조건화 | S001 |
| KV cache | 키-값 캐시 | 완료 prefix attention 재사용 | S001 |
| MDM | 마스크 확산 모델 | confidence 기반 block denoising mode | 3.4 |
| NFE | 모델 평가 횟수 | algorithmic decoding cost | 배경 |
| auto-truncation | 자동 경계 절단 | noisy block의 미래 turn 누수 방지 | 3.3 |
| vision-efficient concatenation | 시각 효율 연결 | vision token 중복 제거 | 3.3 |
| SGLang | SGLang serving engine | bidirectional/causal mode scheduling | 3.4 |
| SmoothQuant W8A8 | weight·activation 8-bit 양자화 | FP8 system acceleration | 3.4 |
| Tokens/NFE | 평가당 token 수 | forward-level parallelism | 4 |

## 번역 검수 기록

- arXiv v2, authors, DOI와 CC BY-NC-ND 4.0을 공식 페이지와 대조했다.
- 20쪽 전 페이지 렌더링으로 표 1-4, Figure 1-9, Algorithm 1-2, Appendix A-D를 확인했다.
- S001 한 문장만 직접 대조하고 나머지는 분석적 재구성으로 작성했다.
- 73.3/60.2, 6.18x, 350.3 TPS, 15.0%/14.2% 수치를 PDF와 재확인했다.
- 번역 범위를 `부분 번역`으로 명시하고 ND 조건을 기록했다.
