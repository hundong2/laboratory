# Fast Inference from Transformers via Speculative Decoding — 제한 번역과 상세 해설

## 논문 메타데이터

- 원문 제목: *Fast Inference from Transformers via Speculative Decoding*
- 저자: Yaniv Leviathan, Matan Kalman, Yossi Matias
- 출판: ICML 2023 Oral; arXiv v2 (2023-05-18)
- 식별자: `arXiv:2211.17192`, DOI `10.48550/arXiv.2211.17192`
- 원문: <https://arxiv.org/abs/2211.17192>
- 원문 언어: 영어
- 라이선스: CC BY 4.0
- 접근일: 2026-09-05

## 번역·접근 범위

CC BY 4.0 원문이지만 이 저장소의 논문 아카이브는 원문 대체물이 되지 않도록 한 문장만 대조 인용하고, 나머지는 한국어 상세 해설로 제공한다. 공식 PDF 13쪽 전체를 렌더링하고 시각·텍스트 대조했으며 부록과 참고문헌까지 확인했다.

| 구간 | 상태 | 제공 범위 |
|---|---|---|
| 제목·초록 | 부분 번역 | 짧은 대조 인용 1문장과 핵심 주장 해설 |
| 1 Introduction | 부분 번역 | 병목과 연구 질문 상세 해설 |
| 2–3 Method | 부분 번역 | 알고리즘·증명 직관·수식 해설 |
| 4 Analysis | 부분 번역 | 기대 토큰·속도식 해설 |
| 5 Experiments | 부분 번역 | 설정과 수치 결과 해설 |
| 6 Discussion | 부분 번역 | 한계·확장 방향 해설 |
| Appendix/References | 원문 확인 | 필요한 증명 전제와 참고 계보만 해설 |

## 읽기 전 핵심 배경

Transformer 생성은 이미 나온 토큰을 KV cache에 저장해도 다음 토큰마다 큰 모델 가중치를 메모리에서 읽는다. batch 1에서는 계산 장치의 병렬 연산 능력보다 메모리 이동이 병목이 되기 쉽다. 추측 디코딩은 작은 모델의 여러 순차 단계를 큰 모델의 한 병렬 검증으로 묶어 이 여유를 사용한다.

## 짧은 문장 대조

### Abstract

**S001 — Original**

Our method can accelerate existing off-the-shelf models without retraining or architecture changes.

**S001 — 한국어**

(이 방법은 재학습이나 아키텍처 변경 없이 기존 기성 모델을 가속할 수 있다.)

- **용어·약어 해설**
  - **off-the-shelf model(기성 모델)**: 새 목적에 맞춰 구조나 가중치를 다시 만들지 않고 이미 배포된 목표 모델을 뜻한다.
  - **architecture change(아키텍처 변경)**: 목표 Transformer의 layer나 attention 구조를 바꾸는 일을 뜻하며, 초안 모델을 옆에 두는 것은 목표 모델 자체의 변경이 아니다.

## 섹션별 상세 해설

### 1. Introduction

저자들은 큰 언어 모델의 자기회귀 추론이 각 단계에서 다음 토큰 하나만 결정하기 때문에 batch가 작을 때 하드웨어 사용률이 낮다고 진단한다. 목표는 추가 계산을 허용하는 대신 순차적인 큰 모델 호출 횟수를 줄이는 것이다. 모델 압축과 달리 목표 모델의 분포를 근사하지 않고 그대로 보존하는 것이 설계 조건이다.

### 2. Speculative sampling

초안 모델 $q$는 현재 prefix에서 $\gamma$개 토큰을 순차 샘플링한다. 목표 모델 $p$는 이 후보를 붙인 전체 prefix에 한 번 forward하여 각 후보 위치와 그 다음 위치의 분포를 동시에 얻는다.

후보 $x_i$의 승인 확률은 다음과 같다.

$$
a_i=\min\left(1,\frac{p_i(x_i)}{q_i(x_i)}\right).
$$

$q_i(x_i)\le p_i(x_i)$이면 항상 승인하고, 초안이 목표보다 그 토큰에 과도한 질량을 준 경우 그 비율만 승인한다. 첫 거절에서는

$$
p'_i(x)=\operatorname{norm}\left(\max(0,p_i(x)-q_i(x))\right)
$$

에서 대체 토큰을 뽑는다. 이미 초안 경로로 받아들인 질량을 제외한 목표 분포의 나머지를 채우는 절차다. 모든 $\gamma$개가 승인되면 목표 모델이 함께 계산한 $(\gamma+1)$번째 토큰을 하나 더 샘플링한다.

Algorithm 1의 핵심 구현 규칙은 첫 거절 이후의 후보를 모두 버리는 것이다. 그 이후 분포는 거절 전과 다른 prefix에 조건화되므로 재사용할 수 없다. EOS가 승인되거나 보정 샘플에서 나오면 즉시 종료해야 한다.

### 3. 정확성의 직관

초안에서 승인되어 특정 토큰 $x$가 나올 질량은 $\min(p(x),q(x))$다. 거절 확률은 $1-\sum_x\min(p(x),q(x))$이고, 잔차 분포는 $[p-q]_+$에 비례한다. 두 경로의 질량을 합하면 각 토큰에 정확히 $p(x)$가 배정된다. 이 한 단계 성질을 prefix마다 반복하면 전체 자기회귀 시퀀스 분포도 목표 모델과 같아진다.

논문의 동일성 보장은 floating-point 구현, 같은 vocabulary와 sampling transform을 전제로 한다. top-k나 top-p를 적용한다면 $p$와 $q$ 각각에 어떤 순서로 적용하는지 명시하고, 승인비와 잔차가 그 최종 분포를 기준으로 계산되어야 한다.

### 4. 효율 분석

평균 토큰 승인률을 $\alpha$라 하면 한 번의 목표 모델 호출로 얻는 기대 토큰 수는

$$
E[T]=1+\alpha+\alpha^2+\cdots+\alpha^\gamma
=\frac{1-\alpha^{\gamma+1}}{1-\alpha}.
$$

여기서 $\alpha=1$이면 극한값은 $\gamma+1$이다. 초안 한 단계 시간을 목표 모델 한 단계 시간으로 나눈 값을 $c$라 할 때 이상화한 가속 비는

$$
S(\alpha,\gamma,c)=
\frac{1-\alpha^{\gamma+1}}{(1-\alpha)(\gamma c+1)}.
$$

$\alpha$가 높아도 $c$가 크면 초안 비용이 이득을 상쇄한다. 반대로 $c$가 거의 0이어도 목표 모델의 $\gamma+1$ 위치 병렬 검증 시간이 한 토큰 forward와 비슷하다는 하드웨어 가정이 깨지면 식이 실제 지연 시간을 과대평가한다.

승인률은 두 분포의 겹침

$$
\alpha=\sum_x\min(p(x),q(x))=1-D_{LK}(p,q)
$$

와 연결된다. $D_{LK}$는 논문이 사용하는 비대칭 이름의 거리 표기이며, 이산 확률분포에서는 총변동거리와 같은 겹침 관계로 읽을 수 있다.

### 5. Experiments

목표 모델은 11B T5-XXL, 초안 후보는 여러 크기의 T5 모델이다. WMT English→German 번역과 CNN/DailyMail 요약을 단일 TPU v4, batch 1에서 측정했다. 가장 작은 T5-small 77M이 초안 품질과 비용의 균형이 좋았다.

- WMT: temperature 0에서 3.4배, temperature 1에서 2.6배
- CNN/DailyMail: temperature 0에서 3.1배, temperature 1에서 2.3배
- 초안/목표 단계 비용비 $c$: 0.05 미만, 많은 설정에서 거의 0

점수 차이가 작다는 관찰뿐 아니라 목표 샘플러와 동일한 분포를 만드는 알고리즘적 보장이 핵심이다. 속도값은 TPU와 batch 1에 종속되므로 다른 장치에서는 $\alpha$, $c$, 병렬 검증 비용을 다시 재야 한다.

### 6. Discussion과 한계

이 방법은 wall-clock latency를 줄이지만 계산 FLOPs를 줄이는 방법은 아니다. 남는 병렬 자원을 전제로 한다. 논문은 텍스트 생성, 고정 초안 모델, 고정 $\gamma$에 초점을 두며 beam search, 동적 초안 길이, 도메인별 초안 선택은 후속 문제로 남긴다.

OCR에서는 이미지 encoder와 긴 visual prefix, crop batching, 출력 문법이 새로운 비용 항목이다. 따라서 논문의 텍스트 전용 속도를 직접 대입하지 말고 end-to-end와 decode-only를 분리해 측정해야 한다.

## 그림·표 읽기 메모

- 방법 개요 그림은 $\gamma$개의 초안 forward와 한 번의 목표 병렬 검증이 시간축에서 어떻게 겹치는지 읽는다.
- 속도 표는 품질 우열표가 아니라 동일 목표 모델을 순차 실행했을 때 대비 지연 시간 비다.
- 초안 모델 크기 ablation은 더 정확한 초안이 반드시 더 빠른 것은 아님을 보여준다. 승인률 증가와 $c$ 증가를 함께 본다.

## 약어 및 기술 용어 사전

| 원어 | 한국어 | 의미 | 최초 등장 |
|---|---|---|---|
| speculative decoding | 추측 디코딩 | 작은 모델의 후보를 큰 모델이 병렬 검증하는 정확 샘플링 방식 | S001 전 배경 |
| draft model | 초안 모델 | 후보 토큰을 저렴하게 생성하는 분포 $q$ | S001 해설 |
| target model | 목표 모델 | 보존하려는 최종 분포 $p$ | S001 해설 |
| acceptance rate $\alpha$ | 승인률 | 초안 후보가 목표 검증을 통과할 평균 확률 | 효율 분석 |
| residual distribution | 잔차 분포 | 첫 거절 시 $[p-q]_+$를 정규화한 보정 분포 | 방법 |
| KV cache | KV 캐시 | 이전 attention key/value를 재사용하는 저장소 | 읽기 전 배경 |
| T5 | Text-to-Text Transfer Transformer | 실험에 사용한 encoder-decoder Transformer 계열 | 실험 |

## 번역 검수 기록

- sentence ID `S001`의 원문·한국어 대응을 확인했다.
- 직접 인용은 25단어 미만 한 문장으로 제한했다.
- 수식의 $p$, $q$, $\alpha$, $\gamma$, $c$ 표기를 PDF와 대조했다.
- 13/13쪽 렌더링에서 잘린 페이지나 빈 페이지가 없음을 확인했다.
- 이 문서는 전문 번역이나 원문 대체물이 아니라 상세 학습 해설이다.

[학습 README로 돌아가기](README.md)
