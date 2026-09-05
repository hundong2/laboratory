# DODO: Discrete OCR Diffusion Models - 문장 대조 번역과 절별 해설

## 논문 metadata

- 원문 제목: **DODO: Discrete OCR Diffusion Models**
- 저자: Sean Man, Gilad Deutch, Roy Ganz, Roi Ronen, Shahar Tsiper, Shai Mazor, Niv Nayman
- 출판처/연도: arXiv preprint (cs.CV), 2026
- 식별자: arXiv:2602.16872, DOI 10.48550/arXiv.2602.16872
- 원문: <https://arxiv.org/abs/2602.16872>
- 사용 버전: v2 (2026-05-27)
- 원문 언어: 영어
- 접근일: 2026-09-05
- 라이선스: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- 변경 고지: 이 문서는 원 논문의 일부 문장을 한국어로 번역하고 나머지를 학습용으로 재구성한 2차 저작물이다. 저자·제목·원문 링크를 위에 표시했다.

[분석 README로 돌아가기](README.md)

## 번역·접근 범위

| 구간 | 상태 | 이 문서의 처리 |
|---|---|---|
| 제목·초록 | 부분 번역 | 핵심 6문장을 문장 대조 번역 |
| 1 Introduction | 부분 번역 | 핵심 주장 대조 + 전체 절 해설 |
| 2 Related Work | 부분 번역 | 분야 계보 해설 |
| 3 Preliminaries | 부분 번역 | 주요 수식 보존·기호 설명 |
| 4 Method | 부분 번역 | block factorization과 실패 양상 상세 해설 |
| 5 Experiments | 부분 번역 | 설정·표 수치 상세 해설 |
| 6 Ablation | 부분 번역 | 핵심 표와 인과 해석 |
| 7 Conclusion/Limitations | 부분 번역 | 결론·한계 해설 |
| 참고문헌 | 원문 확인 | 서지 레코드는 번역·복제하지 않음 |
| 부록 A-D | 부분 번역 | attention, sampler, 세부 결과, 정성 예시 해설 |

원문 PDF 15쪽 전체와 모든 표·그림 배치를 확인했다. CC BY 4.0이 번역·개작을 허용하지만, 현재 파일은 전문 번역이라고 주장하지 않는다.

## 읽기 전 핵심 배경

AR은 `p(x_1:L)=Π_l p(x_l|x_<l)`로 한 토큰씩 생성한다. MDM은 일부 토큰이 가려진 시퀀스에서 여러 위치를 한 번에 복원한다. OCR에서는 이미지가 답을 강하게 제한하므로 병렬 예측이 유리하지만, 한 번 잘못 공개한 토큰을 되돌리지 않는 sampler에서는 길이와 위치 오류가 누적될 수 있다. DODO의 핵심은 병렬성 자체보다 **병렬화 범위를 블록으로 제한하는 구조**다.

## 문장 대조 번역

### Abstract

**S001 — Original**

Optical Character Recognition (OCR) is a fundamental task for digitizing information, serving as a critical bridge between visual data and textual understanding.

**S001 — 한국어**

(광학 문자 인식(OCR)은 정보를 디지털화하는 기본 과제로서, 시각 데이터와 텍스트 이해를 잇는 핵심 다리 역할을 한다.)

- **용어·약어 해설**
  - **OCR (Optical Character Recognition, 광학 문자 인식)**: 이 논문에서는 단순 글자 검출뿐 아니라 문서를 구조화된 토큰열로 전사하는 과제를 뜻한다.

**S002 — Original**

While modern Vision-Language Models (VLM) have achieved high accuracy in this domain, they predominantly rely on autoregressive decoding, which becomes computationally expensive and slow for long documents as it requires a sequential forward pass for every generated token.

**S002 — 한국어**

(현대의 시각-언어 모델(VLM)은 이 영역에서 높은 정확도를 달성했지만, 대부분 자기회귀 디코딩에 의존하며 생성 토큰마다 순차 forward pass가 필요하므로 긴 문서에서는 계산 비용이 커지고 느려진다.)

- **용어·약어 해설**
  - **VLM (Vision-Language Model, 시각-언어 모델)**: 이미지 특징을 텍스트 토큰 생성과 결합하는 모델이다.
  - **autoregressive decoding(자기회귀 디코딩)**: 앞에서 확정한 토큰을 조건으로 다음 한 토큰을 예측한다.

**S003 — Original**

We identify a key opportunity to overcome this bottleneck: unlike open-ended generation, OCR is a highly deterministic task where the visual input strictly dictates a unique output sequence, theoretically enabling efficient, parallel decoding via diffusion models.

**S003 — 한국어**

(저자들은 이 병목을 넘을 핵심 기회를 찾는다. 개방형 생성과 달리 OCR은 시각 입력이 사실상 하나의 출력열을 엄격히 결정하는 매우 결정적인 과제이므로, 이론적으로 확산 모델을 통한 효율적인 병렬 디코딩이 가능하다.)

**S004 — Original**

However, we show that existing masked diffusion models fail to harness this potential; those introduce structural instabilities that are benign in flexible tasks, like captioning, but catastrophic for the rigid, exact-match requirements of OCR.

**S004 — 한국어**

(그러나 기존 마스킹 확산 모델은 이 잠재력을 살리지 못한다. 캡셔닝처럼 유연한 과제에서는 가벼운 구조 불안정성이 OCR의 엄격한 exact-match 요구에서는 치명적이기 때문이다.)

- **용어·약어 해설**
  - **MDM (Masked Diffusion Model, 마스킹 확산 모델)**: 토큰을 마스크로 바꾸는 순방향 과정과 이를 복원하는 역과정을 학습한다.

**S005 — Original**

To bridge this gap, we introduce DODO, the first VLM to utilize block discrete diffusion and unlock its speedup potential for OCR.

**S005 — 한국어**

(이 간극을 메우기 위해 저자들은 블록 이산 확산을 사용해 OCR의 가속 잠재력을 여는 최초의 VLM인 DODO를 제안한다.)

**S006 — Original**

By decomposing generation into blocks, DODO mitigates the synchronization errors of global diffusion.

**S006 — 한국어**

(DODO는 생성을 블록으로 분해해 전역 확산의 동기화 오류를 완화한다.)

### Introduction 핵심 문장

**S007 — Original**

Conditioned on the image, the posterior distribution is effectively unimodal, meaning the visual input strictly dictates a single valid sequence.

**S007 — 한국어**

(이미지가 조건으로 주어지면 사후분포는 사실상 단봉형이며, 이는 시각 입력이 하나의 유효한 토큰열을 엄격히 결정한다는 뜻이다.)

**S008 — Original**

By bounding the inference horizon and conditioning on a committed prefix, we eliminate the risk of long-range alignment drift and enable dynamic length adaptation without requiring a perfect global estimate.

**S008 — 한국어**

(추론 범위를 제한하고 확정된 접두사를 조건으로 삼음으로써 장거리 정렬 드리프트 위험을 줄이고, 완벽한 전역 길이 추정 없이도 동적 길이 적응을 가능하게 한다.)

### Figure 4 caption

**S009 — Original**

In standard full diffusion, MDM sampling is applied globally to the entire sequence.

**S009 — 한국어**

(표준 full diffusion에서는 MDM 샘플링을 전체 시퀀스에 전역적으로 적용한다.)

**S010 — Original**

In contrast, block diffusion restricts parallel sampling to discrete windows, processing blocks sequentially from left to right.

**S010 — 한국어**

(반대로 block diffusion은 병렬 샘플링을 분리된 창으로 제한하고 블록을 왼쪽에서 오른쪽으로 순차 처리한다.)

## 절별 한국어 해설

### 1. Introduction

논문은 OCR과 캡셔닝의 출력 공간을 구분한다. 캡셔닝은 표현이 달라도 의미가 맞을 수 있지만 OCR은 문자·순서·구조 태그까지 정답과 맞아야 한다. 이 낮은 조건부 엔트로피는 동시에 여러 토큰을 맞힐 기회를 주지만, 잘못된 길이와 절대 위치를 나중에 다른 표현으로 보상할 수 없게도 만든다.

### 2. Related Work

전문 OCR VLM은 대부분 AR이다. D3PM·MDLM 계열은 이산 토큰 확산의 기반을 제공했고, BD3-LM은 블록 사이 AR·블록 안 확산이라는 중간점을 만들었다. Dimple, LaViDa, LLaDA-V는 멀티모달 확산을 시도했으나 논문 기준 dense OCR에서 높은 오류를 보였다. DODO의 차이는 OCR 전용 데이터만이 아니라 multimodal block-causal training을 함께 적용한 점이다.

### 3. Preliminaries와 수식

OCR 목표는 이미지 `I`와 선택적 문맥 `c`에서 직렬화·토큰화된 `x_1:L`을 찾는 것이다.

```text
log p_theta(x_1:L | I,c) = Σ_l log p_theta(x_l | x_<l,I,c)        (1)
q_t|0(x_t | x_0) = Π_i Cat(x_t^i; alpha_t e_(x_0^i) + (1-alpha_t)e_[M])  (2)
```

식 (1)은 AR이 `L`번의 순차 의존을 갖는다는 뜻이다. 식 (2)는 각 위치를 확률 `1-alpha_t`로 독립 마스킹한다. `alpha_0=1`, `alpha_1=0`이므로 시간 `t`가 커질수록 더 많이 가려진다. 역과정은 매 step에서 공개할 위치를 정한 뒤 해당 토큰을 예측한다.

### 4. Method

전역 canvas의 두 실패는 다음과 같다.

- **Length mismatch**: canvas가 짧으면 잘리고 길면 빈 공간을 채우려 환각한다.
- **Positional anchoring**: 표 머리글 같은 조각을 잘못된 절대 위치에 먼저 확정하면 뒤 토큰을 밀거나 당길 수 없다.

DODO는 `L=B L'`로 나누고 다음 factorization을 사용한다.

```text
p_theta(x_1:L | I,c) = Π_(b=1..B) p_theta(x^(b) | x^(<b),I,c)    (5)
```

블록 내부에서는 병렬 diffusion을 수행하지만, 블록 경계에서는 이전 접두사가 정렬 anchor가 된다. block-level EOS로 전체 길이를 동적으로 조절한다.

### 5. Experiments

Qwen2.5-VL-3B를 `olmOCR-mix-1025` 약 270K pair로 미세조정했다. 최대 토큰 길이 8,192, 200K step, A100 40GB 8장이다. OmniDocBench 290개 영어 문서와 Fox-Page-EN 112쪽에서 NED와 TPS를 측정했다. DODO의 main NED는 `0.069/0.038`, TPS는 `103.69`다. 이는 논문 설정 안에서의 비교이며 다른 tokenizer·출력 포맷에 그대로 일반화하면 안 된다.

### 6. Ablation

핵심은 training-time block structure다. global train + global inference는 최대 길이 8,192에서 NED `0.834`, global train + 32-block inference는 `0.951`, block train + 32-block은 `0.067`이었다. 즉 추론 창만 작게 자르는 것으로는 해결되지 않는다.

block-causal exact cache는 빠르지만 큰 블록에서 NED가 악화된다. 양방향 no-cache는 과거 표현을 현재 블록에 맞춰 갱신해 블록 256에서 `0.057`까지 좋아지지만 `42.8 TPS`로 느리다. confidence threshold `0.99`는 높은 정확도를 유지하는 기본 sampler로 선택됐다.

### 7. Conclusion과 Limitations

DODO는 완전 비순차 모델이 아니라 블록 수준에서는 AR인 semi-autoregressive 구조다. 논문이 보고한 실용적 결론은 병렬화 범위를 무한히 키우는 것이 아니라, 오류를 국소화할 블록과 cache 가능한 인과 구조를 고르는 것이다. 명시된 한계는 exact cache가 static history를 강제해 큰 블록 정확도를 제한한다는 점이다.

### 부록

- Appendix A: 양방향과 block-causal attention mask를 시각화한다.
- Appendix B: confidence threshold와 fixed top-k를 비교하며 high-fidelity 구간에서는 threshold `0.99`를 선택한다.
- Appendix C: 길이·문서 유형별 NED를 제시한다. 4,096+ 토큰에서 DODO `0.079`, Qwen2.5-VL-7B `0.185`다.
- Appendix D: 병렬로 확정된 토큰의 step heatmap을 포함한 정성 예시다.

## 수식·그림을 읽는 법

- Figure 1의 같은 색 토큰은 같은 forward에서 확정됐다. 148 토큰을 20회에 해결한 예시는 평균 약 7 token/step이라는 직관을 준다.
- Figure 3은 이미지가 “Eiffel/Great Wall” 같은 언어적 선택지를 직접 정하므로 병렬 예측 충돌이 줄어드는 상황을 보여준다.
- Figure 6의 `<0.1 steps/token`은 AR의 1 step/token보다 순차 깊이가 작다는 뜻이지, 각 diffusion forward가 AR forward와 같은 비용이라는 뜻은 아니다.

## 약어 및 기술 용어 사전

| 원어 | 한국어 | 의미 | 최초 등장 |
|---|---|---|---|
| OCR | 광학 문자 인식 | 이미지에서 정확한 구조화 텍스트를 복원 | S001 |
| VLM | 시각-언어 모델 | 이미지 조건부 텍스트 모델 | S002 |
| AR | 자기회귀 | 이전 토큰에 조건화한 순차 생성 | S002 |
| MDM | 마스킹 확산 모델 | 마스크 토큰을 반복 복원하는 이산 확산 | S004 |
| block discrete diffusion | 블록 이산 확산 | 블록 사이는 순차, 내부는 병렬 복원 | S005 |
| NED | 정규화 편집 거리 | 길이를 보정한 전사 오류율 | 절별 해설 |
| TPS | 초당 토큰 수 | 추론 처리량 지표 | 절별 해설 |
| KV cache | 키-값 캐시 | 고정 접두사 attention 상태 재사용 | S008 |
| carry-over unmasking | 공개 토큰 유지 | 공개한 토큰을 다시 수정하지 않는 규칙 | 배경 |

## 번역 검수 기록

- v2 PDF 15/15쪽 렌더링 확인, 본문·표·수식·부록의 페이지 순서를 대조했다.
- `0.069`, `103.69 TPS`, `p=0.99`, block 32/256, 8,192 tokens, 270K pairs 등 핵심 수치를 PDF 표와 재확인했다.
- 원문의 가능성 표현과 저자 주장에는 “논문은/저자들은/보고했다”를 붙여 외부 검증 사실과 구분했다.
- 문장 대조는 S001-S010에 한정되며 전문 번역이 아니다.
