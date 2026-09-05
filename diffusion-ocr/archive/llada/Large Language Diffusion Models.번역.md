# Large Language Diffusion Models - 선택 문장 대조 번역과 절별 해설

## 논문 metadata

| 항목 | 내용 |
|---|---|
| 원문 제목 | Large Language Diffusion Models |
| 저자 | Shen Nie; Fengqi Zhu; Zebin You; Xiaolu Zhang; Jingyang Ou; Jun Hu; Jun Zhou; Yankai Lin; Ji-Rong Wen; Chongxuan Li |
| 출판처·연도 | arXiv preprint, 2025 |
| 식별자 | arXiv:2502.09992, DOI 10.48550/arXiv.2502.09992 |
| 원문 URL | <https://arxiv.org/abs/2502.09992> |
| 사용 버전 | v3, 2025-10-18 |
| 원문 언어 | 영어 |
| 접근일 | 2026-09-05 |
| 라이선스 | arXiv non-exclusive distribution license 1.0 |

[학습 README로 돌아가기](./README.md)

## 번역·접근 범위

arXiv 배포 라이선스는 일반적인 번역 재배포 허가가 아니다. 따라서 원문은 핵심을 대표하는 짧은 한 문장만 대조하고, 나머지는 수치·수식·논지에 근거한 한국어 해설로 재구성했다. 공식 v3 PDF 33쪽의 본문, 참고문헌, 부록 A-C를 모두 열람했으며 PDF 전 페이지 렌더링으로 다단 순서와 표·그림·부록을 확인했다.

| 구역 | 상태 | 이 파일의 처리 |
|---|---|---|
| 제목·metadata | 완료 | 공식 arXiv와 PDF 대조 |
| Abstract | 부분 번역 | 짧은 핵심 문장 1개 대조, 나머지 해설 |
| 1 Introduction | 부분 번역 | 상세 한국어 해설 |
| 2 Approach | 부분 번역 | 목적식·학습·추론 상세 해설 |
| 3 Experiments | 부분 번역 | 데이터·표 수치·해석 정리 |
| 4 Related Work | 부분 번역 | 연구 계보 해설 |
| 5 Conclusion and Discussion | 부분 번역 | 주장과 한계 분리 |
| Appendix A-C | 부분 번역 | 알고리즘·추가 실험·impact 핵심 해설 |
| References | 원문 미수록 | 서지정보를 복제하지 않고 원문 링크 제공 |

## 읽기 전 핵심 배경

- ARM (Autoregressive Model, 자기회귀 모델): 앞 토큰만 조건으로 다음 토큰을 예측한다.
- MDM (Masked Diffusion Model, 마스크 확산 모델): 토큰을 `[MASK]`로 손상한 뒤 여러 위치를 동시에 복원한다.
- SFT (Supervised Fine-Tuning, 지도 미세조정): prompt-response 정답 쌍으로 instruction following을 학습한다.
- likelihood lower bound: 직접 계산하기 어려운 log-likelihood 대신 최적화하는 변분 하한이다. 음의 부호를 취하면 NLL의 상계가 된다.

## 선택 문장 대조

### Abstract

**S001 — Original**

We challenge this notion by introducing LLaDA, a diffusion model trained from scratch under the pre-training and supervised fine-tuning (SFT) paradigm.

**S001 — 한국어**

(우리는 사전학습과 지도 미세조정(SFT) 패러다임 아래 처음부터 학습한 확산 모델 LLaDA를 도입해 이 통념에 도전한다.)

- **용어·약어 해설**
  - **LLaDA (Large Language Diffusion with mAsking, 마스킹 기반 대규모 언어 확산)**: 저자가 제안한 1B/8B masked diffusion 언어 모델이다.
  - **trained from scratch(처음부터 학습)**: 기존 AR checkpoint를 변환한 것이 아니라 초기화부터 diffusion 목적식으로 사전학습했다는 뜻이다.

## 절별 한국어 해설

### 1. Introduction

논문은 현재 LLM의 능력을 `p(x_i | x_<i)`라는 왼쪽-오른쪽 인수분해의 필연적 결과로 보는 관점을 문제 삼는다. 데이터 분포를 충분히 잘 근사하는 다른 확률 모델도 in-context learning과 instruction following을 얻을 수 있다는 가설을 세우고, masked diffusion을 8B까지 확장해 검증한다. 양방향 의존성은 단순한 속도 수단이 아니라 reversal reasoning에서 다른 귀납 편향을 제공한다.

기여 규모는 8B, 사전학습 2.3T tokens, 약 0.13M H800 GPU-hours, SFT 4.5M pairs다. 자체 ARM과 여섯 과제의 scaling 경향을 비교하고, 15개 base benchmark, post-training benchmark, 중국 고시 역방향 완성을 평가한다.

### 2. Approach

#### 2.1 Probabilistic formulation

각 위치는 독립적으로 확률 `t`만큼 마스크된다. `t=0`은 원문, `t=1`은 완전 마스크다. mask predictor는 손상 문장 `x_t`를 받아 마스크된 모든 위치의 원 토큰을 동시에 예측한다.

```text
L(theta) = -E [ (1/t) sum_i 1[x_t^i = M] log p_theta(x_0^i | x_t) ]
-E_data[log p_theta(x_0)] <= L(theta)
```

첫 식에서 `1/t`는 서로 다른 noise level의 기여를 보정한다. 두 번째 부등식 때문에 목적식은 heuristic 빈칸 채우기가 아니라 likelihood 기반 생성 학습과 연결된다. 다만 `t`가 작을 때 적은 마스크에 큰 가중치가 걸려 estimator variance가 커질 수 있다.

#### 2.2 Pre-training

Transformer는 causal mask를 쓰지 않아 입력 전체를 조건으로 삼는다. 8B 구성은 LLaMA3 8B와 비슷한 규모를 맞추되 grouped-query attention 대신 multi-head attention을 썼다. 저자 설명상 전역 diffusion이 KV caching과 호환되지 않아 KV head 절감의 이점이 없기 때문이다.

데이터는 2.3T tokens의 online corpora, code, math, multilingual 혼합이다. sequence length 4096, AdamW weight decay 0.1, global batch 1280이며 Warmup-Stable-Decay schedule을 사용했다. 전체 데이터 구성과 혼합 비율은 완전히 공개되지 않았다.

#### 2.3 Supervised fine-tuning

prompt는 그대로 두고 response token만 무작위 마스킹한다. 4.5M pairs를 3 epochs 학습한다. mini-batch의 짧은 답변 뒤에는 EOS를 채우고 EOS 자체도 정상 token으로 학습해, 샘플링 후 첫 EOS 이후를 버리는 길이 제어를 가능하게 한다.

#### 2.4 Inference

완전 마스크된 답변 슬롯에서 시작한다. 각 step은 모든 마스크를 예측하고, 예정된 noise level에 맞춰 일부를 다시 마스크한다. 기본 전략은 가장 confidence가 낮은 위치를 remask하는 방식이다. sampling steps가 많으면 대개 더 신중하지만 NFE가 증가한다. 초기 슬롯 길이도 하이퍼파라미터다.

### 3. Experiments

#### 3.1 Scaling

1B에서는 architecture와 data를 맞춘 ARM을 사용했고 더 큰 규모에서는 자원 한계로 크기가 조금 다르다. 저자는 약 `10^20-10^23` FLOPs에서 여섯 downstream 과제의 추세가 경쟁적이며 MMLU·GSM8K에서 특히 강했다고 보고한다. likelihood 자체가 아닌 downstream 성능의 scaling이라는 점이 중요하다.

#### 3.2 Standard benchmarks

대표 base 결과는 MMLU 65.9, BBH 49.7, GSM8K 70.3, MATH 31.4, HumanEval 35.4, CMMLU 69.9다. 같은 구현의 LLaMA3 8B base와 비교하면 과제별 승패가 엇갈린다. LLaDA의 pretraining은 2.3T tokens이고 LLaMA3 8B는 표에 15T로 기록되므로 데이터 효율 주장과 절대 성능 주장을 구분해야 한다.

SFT 뒤에는 instruction following 사례와 일부 benchmark가 향상됐지만 RL alignment는 하지 않았다. 비교 대상에는 RL을 거친 모델이 있어 post-training 통제 비교가 아니다.

#### 3.3 Reversal reasoning

496개 중국 고시 문장 쌍에서 다음 행을 맞히는 forward와 이전 행을 맞히는 reversal을 별도 평가했다. LLaDA-8B Instruct는 51.8/45.6, GPT-4o는 82.7/34.3, Qwen2.5-7B Instruct는 75.9/38.0이다. LLaDA의 forward 절대 점수는 낮지만 방향 간 낙폭이 작고 reversal 절대 점수는 높다. 이것이 “reversal curse를 완전히 해결했다”는 일반 명제가 되려면 더 다양한 언어·관계·평가가 필요하다.

#### 3.4 Case studies

긴 글, multi-turn dialogue, instruction following 샘플을 제시한다. 정성 사례는 가능성을 보여주지만 분포 전체의 신뢰도나 안전성을 정량화하지 않는다.

### 4. Related Work

연속 latent diffusion과 discrete diffusion을 구분하고, D3PM·MDLM 계열의 이론 및 MaskGIT식 반복 복원을 연결한다. 기존 연구가 GPT-2 또는 약 1B 수준에서 likelihood·compute 효율 문제를 다뤘다면 LLaDA는 8B/2.3T 규모의 downstream 능력에 초점을 둔다.

### 5. Conclusion and Discussion

저자의 핵심 결론은 autoregression 없이도 scaling, ICL, instruction following이 나타날 수 있다는 것이다. 제한 사항으로 사용자 지정 generation length, 완전 통제되지 않은 ARM 비교, 초기 단계인 효율·제어 sampler, RL alignment 부재, 더 작은 규모·데이터, 미탐색 multimodality와 agents를 명시한다.

### Appendix A-C

- Appendix A: forward/reverse masked diffusion의 정식화와 training, random-remasking, low-confidence-remasking 알고리즘을 제공한다.
- Appendix B: data filtering, architecture·schedule, classifier-free guidance, sampling 전략, length, benchmark prompt, iGSM, poem completion을 보충한다.
- Appendix C: 잠재적 사회적 영향과 일반 생성 모델 위험을 짧게 논의한다.

## 수식·그림 해설

- Figure 2는 `random masking -> response-only SFT masking -> fully masked reverse sampling`의 세 단계를 한 그림에 놓는다.
- Table 1과 2는 모델의 training tokens, post-training 방식, shot 수가 다르다. 행 하나의 우열보다 비교 조건을 먼저 읽어야 한다.
- `1/t` 목적식은 기대값의 정당성을 주지만 한 번의 mini-batch estimator가 저분산이라는 뜻은 아니다.

## 약어 및 기술 용어 사전

| 원어·약어 | 한국어 | 이 논문에서의 의미 | 최초 등장 |
|---|---|---|---|
| LLaDA | 마스킹 기반 대규모 언어 확산 | 제안한 masked diffusion LM | S001 |
| SFT | 지도 미세조정 | prompt를 보존하고 response를 마스킹해 학습 | S001 |
| ARM | 자기회귀 모델 | 비교 대상인 left-to-right LM | 배경 |
| MDM | 마스크 확산 모델 | 토큰 마스크를 noise state로 쓰는 diffusion | 배경 |
| NLL | 음의 로그우도 | 목적식이 상계하는 평가량 | 2.1 |
| CFG | 분류기 없는 유도 | conditional/unconditional 예측을 섞는 선택 기법 | 부록 |
| KV cache | 키-값 캐시 | AR prefix 계산 재사용; 전역 LLaDA와 비호환 | 2.2 |
| remasking | 재마스킹 | 낮은 confidence 예측을 다음 step에서 다시 풀게 하는 절차 | 2.4 |
| reversal curse | 역전 저주 | `A->B` 학습이 `B->A` 일반화로 이어지지 않는 현상 | 3.3 |

## 번역 검수 기록

- 공식 arXiv metadata와 v3 PDF의 제목·저자·날짜를 대조했다.
- PDF 33쪽을 모두 렌더링해 본문 2단 편집, 표 1-4, Figure 1-3, 부록 A-C와 페이지 경계를 확인했다.
- 원문 인용은 짧은 한 문장으로 제한했고 sentence ID `S001`의 Original/한국어 대응을 검사했다.
- 수치는 PDF 표에서 확인했으며 비교 조건이 다른 모델을 동일 조건처럼 표현하지 않았다.
- 이 파일은 완역이 아니며, 위 범위표의 `부분 번역`을 `완료`로 과장하지 않았다.
