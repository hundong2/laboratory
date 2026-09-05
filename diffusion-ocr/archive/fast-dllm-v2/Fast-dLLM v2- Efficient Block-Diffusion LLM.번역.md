# Fast-dLLM v2: Efficient Block-Diffusion LLM — 제한 번역과 해설

## 논문 메타데이터

- 원문 제목: Fast-dLLM v2: Efficient Block-Diffusion LLM
- 저자: Chengyue Wu, Hao Zhang, Shuchen Xue, Shizhe Diao, Yonggan Fu, Zhijian Liu, Pavlo Molchanov, Ping Luo, Song Han, Enze Xie
- 출판처·연도: arXiv preprint, 2025
- 식별자: arXiv:2509.26328v1; DOI 10.48550/arXiv.2509.26328
- 원문: [abstract](https://arxiv.org/abs/2509.26328), [PDF v1](https://arxiv.org/pdf/2509.26328v1)
- 사용 버전: v1, 2025-09-30
- 원문 언어: 영어
- 접근일: 2026-09-05
- 라이선스: [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)

[학습용 분석 README로 돌아가기](README.md)

## 번역·접근 범위

CC BY-NC-ND 4.0의 NoDerivatives 조건은 번역물의 배포를 허용하지 않는다. 따라서 아래에는 짧은 핵심 문장 하나만 대조하고, 나머지는 원문의 표현을 복제하지 않은 한국어 해설로 제공한다. 이는 완역본이 아니다. PDF 17쪽과 arXiv HTML의 본문·수식·표·부록을 확인했다.

| 원문 구간 | 상태 | 처리 방식 |
| --- | --- | --- |
| 제목·메타데이터 | 완료 | 서지 정보 확인 |
| 초록 | 부분 번역 | 짧은 문장 대조 + 전체 해설 |
| 1 Introduction | 부분 번역 | 상세 한국어 해설 |
| 2 Related Work | 부분 번역 | 계보와 차이 요약 |
| 3 Methodology | 부분 번역 | 수식·알고리즘 중심 해설 |
| 4 Experiments | 부분 번역 | 설정·핵심 수치 해설 |
| 5 Conclusion | 부분 번역 | 주장과 조건 요약 |
| 부록 A–C | 부분 번역 | 구현·attention·case study 범위 해설 |
| 참고문헌 | 원문 미수록 | 핵심 연결 논문만 링크 |

## 읽기 전 핵심 배경

- AR LLM은 다음 토큰을 예측하므로 KV cache에 잘 맞지만 생성 step이 직렬이다.
- masked diffusion LLM은 여러 토큰을 동시에 복원할 수 있지만 양방향 attention 때문에 캐시 재사용이 어렵다.
- block diffusion은 두 극단 사이의 설계점이다. 이전 블록은 고정 prefix, 현재 블록만 반복 복원한다.
- 이 논문에서 “lossless adaptation”은 benchmark 성능을 보존한다는 경험적 표현이지 동일한 출력 분포의 수학적 보장이 아니다.

## 문장 대조 번역

### Abstract

**S001 — Original**

Fast-dLLM v2 achieves up to 2.5× speedup over standard AR decoding without compromising generation quality.

**S001 — 한국어**

(Fast-dLLM v2는 생성 품질을 떨어뜨리지 않으면서 표준 AR 디코딩 대비 최대 2.5배의 가속을 달성한다.)

- **용어·약어 해설**
  - **AR (Autoregressive, 자기회귀)**: 이전에 확정된 토큰을 조건으로 다음 한 토큰을 생성하는 방식이다.
  - **dLLM (diffusion Large Language Model, 확산 대규모 언어 모델)**: 마스크된 여러 위치를 반복적으로 복원한다.
  - **speedup(가속비)**: 같은 기준 구현의 시간 또는 처리량과 비교한 비율이다. 하드웨어와 batch 조건을 함께 봐야 한다.

## 섹션별 한국어 해설

### 초록

저자들은 순차 decoding이 AR LLM의 병목이라고 규정한다. 제안 모델은 Qwen2.5 기반 AR checkpoint를 블록 확산 모델로 바꾸며, 약 10억 토큰만 사후학습한다. Dream의 약 5800억 토큰 적응과 비교해 약 500분의 1이라는 주장이다. 상보 attention view로 AR 표현을 보존하고, 블록·sub-block 계층 캐시로 병렬 생성의 비용을 줄인다.

### 1. 서론

완전 양방향 dLLM은 KV cache와 가변 길이 처리에서 불리하고 실제 latency가 AR보다 느릴 수 있다. 반면 블록 확산은 블록 간에는 인과적으로 움직이므로 완료 블록을 캐시할 수 있고, 현재 블록 안에서만 양방향 복원을 한다. 기존 BD3-LM은 작은 모델과 전통 LM 지표 중심이어서 7B급 instruction model의 품질·처리량이 충분히 검증되지 않았다는 것이 연구 공백이다.

세 기여는 다음과 같다.

1. AR 친화적인 block-wise attention과 약 10억 토큰의 post-training 레시피.
2. block cache, DualCache, block-wise parallel decoding을 묶은 추론 경로.
3. 1.5B·7B 모델과 코드·수학·지식·지시 수행 benchmark에서 품질과 처리량을 함께 평가한 실험.

### 2. 관련 연구

이 논문은 discrete diffusion의 D3PM·CTMC·SEDD, 대규모 masked diffusion인 LLaDA·Dream, block diffusion인 SSD-LM·AR-Diffusion·BD3-LM·SDAR·D2F를 연결한다. 가속 계보에서는 DualCache, dKV-Cache, dLLM-Cache, sparse cache, entropy-bounded unmasking, confidence decoding, draft-and-verify를 비교한다.

차별점은 새로운 diffusion 원리 자체보다 “기존 AR 모델을 적은 데이터로 바꾸고 실제 캐시 계층을 구성하는 법”에 있다.

### 3. 방법

#### 3.1 masked diffusion 손실

원문 손실은 다음과 같다.

$$
\mathcal{L}(\theta)=-\mathbb{E}_{t,x_0,x_t}\left[
\frac{1}{t}\sum_{i=1}^{L}\mathbf{1}[x_t^i=\texttt{[MASK]}]
\log p_\theta(x_0^i\mid x_t)\right].
$$

$t\sim U(0,1)$은 마스크 비율을 정하고, 지시 함수가 1인 위치만 loss에 들어간다. 직관적으로는 다양한 손상 수준에서 원래 토큰을 맞히는 denoising 훈련이다.

#### 3.2 블록 적응

샘플을 block size $D$의 배수로 padding하고 길이 $L$인 고정 context로 pack한다. 각 block에 마스크 $m$과 여집합 $\bar m$을 적용한 두 view를 만들어 모든 위치가 masked supervision을 받게 한다. 가려진 토큰 $x_i$는 $i-1$ 위치의 logit으로 예측해 pretrained AR 모델의 next-token 정렬을 유지한다.

블록 손실은 다음 구조다.

$$
\mathcal{L}_{\text{block}}(\theta)=-\mathbb{E}_{x,m}
\sum_{i=1}^{L}\mathbf{1}[x_t^i=\texttt{[MASK]}]
\log p_\theta(x_0^i\mid x_{<i},x_{\text{block}(i)}).
$$

$x_{<i}$는 이전 블록의 clean prefix이고, $x_{\text{block}(i)}$는 현재 블록 전체다. attention은 앞 블록에 인과적이고 현재 블록 안에서 양방향이다.

#### 3.3 추론

완료 블록의 KV는 block-level cache에 보존한다. 현재 블록은 confidence threshold를 넘는 위치를 동시에 확정하고 나머지만 반복한다. DualCache는 현재 block의 이미 확정된 부분과 아직 마스크인 부분을 분리해 재계산을 줄인다. 서로 다른 목표 길이는 block 단위 padding으로 batch schedule을 맞춘다.

### 4. 실험

Qwen2.5-Instruct 1.5B와 7B를 LLaMA-Nemotron post-training data로 학습했다. 1.5B는 6,000 step·약 8시간, 7B는 2,500 step·약 12시간이며 64×A100과 batch 256을 사용했다. 기본 block은 32, sub-block은 8이다.

대표 수치는 다음과 같다.

| 비교 | 논문 보고값 | 읽는 법 |
| --- | ---: | --- |
| 1.5B 평균 | 45.0 | NTP 재학습 baseline 44.3 대비 +0.7 |
| 7B 평균 | 60.3 | Qwen2.5-7B-Nemo-FT 59.6 대비 +0.7 |
| GSM8K threshold 0.9 | 39.1 → 101.7 token/s | 해당 sweep에서 2.6배, 작은 정확도 하락 |
| batch 64 A100 | 최대 1.5배 | Qwen2.5-7B-Instruct 대비 |
| batch 64 H100 | 최대 1.8배 | 병렬 하드웨어에서 이점 증가 |
| `naive → +pad → +pad+CM` 평균 | 41.3 → 42.2 → 45.0 | padding과 상보 마스크의 누적 효과 |

sub-block을 키우면 forward pass 수가 줄어 처리량은 높아지지만 정확도가 다소 떨어진다. cache는 batch가 커서 compute-bound가 될 때 유용했고 작은 batch에서는 이득이 미미했다.

### 5. 결론

논문의 핵심 결론은 block diffusion이 “AR 또는 diffusion”의 이분법이 아니라 실용적인 중간점이 될 수 있다는 것이다. 다만 최대 가속은 보편 상수가 아니다. threshold, batch, GPU, block 크기, cache 구현과 평가 task가 결과를 결정한다.

### 부록 A. 구현 세부사항

부록은 LLaMA-Nemotron subset, 8,192 context, block size 32, sub-block size 8, 학습률·step을 명시한다. attention diagram은 noisy/clean view가 서로 다른 연결을 갖고, inference에서는 현재 블록 내부 양방향·과거 블록 인과 연결만 남는 것을 보여준다. 재현 시 mask tensor의 행/열 의미와 loss 대상 위치를 unit test해야 한다.

### 부록 B. 사례

단일·다중 대화 사례는 모델이 산술, 코드, 대화 문맥을 생성할 수 있음을 정성적으로 보인다. 사례가 benchmark 평균이나 안전성을 대신하지 않으며 cherry-picking 가능성을 통제한 평가도 아니다.

### 부록 C. LLM 사용 고지

저자들은 원고 작성 중 언어 교정·표현 개선에 LLM을 사용했다고 밝힌다. 연구 방법이나 수치의 근거는 논문의 실험이어야 하며, 이 고지는 결과 검증을 대체하지 않는다.

## 수식·그림·표 읽기

- Figure 2: 두 complementary view에서 녹색 loss 위치가 서로 보완되는지 본다.
- Figure 3: 완료 block cache와 현재 block refinement의 경계를 구분한다.
- Figure 4: confidence threshold가 낮아질수록 token/s가 늘지만 정확도 곡선도 함께 확인한다.
- Figure 5–6: batch가 큰 compute-bound 영역에서 cache 효과가 커지는지 본다.
- Table 3–4: 학습 block과 추론 block/sub-block 설정 불일치가 품질을 낮춘다는 증거다.

## 약어 및 기술 용어 사전

| 원어 | 한국어 | 논문에서의 의미 | 최초 등장 |
| --- | --- | --- | --- |
| AR | 자기회귀 | 이전 토큰만 조건으로 다음 토큰을 생성하는 기준 방식 | S001 |
| dLLM | 확산 대규모 언어 모델 | 여러 마스크 위치를 반복 복원하는 생성 모델 | S001 |
| block diffusion | 블록 확산 | 블록 사이는 인과적, 블록 안은 양방향인 혼합 구조 | 배경 |
| NTP | 다음 토큰 예측 | AR 모델의 기본 학습 목표이자 비교 baseline | 4장 해설 |
| CM | 상보 마스크 | $m$과 $1-m$을 함께 학습하는 전략 | 3장 해설 |
| KV cache | 키-값 캐시 | 완료 prefix의 attention 계산을 재사용 | 3장 해설 |
| DualCache | 이중 캐시 | 현재 block의 prefix·suffix 계산을 재사용 | 3장 해설 |
| SFT | 지도 미세조정 | instruction data로 block diffusion에 적응 | 4장 해설 |

## 번역 검수 기록

- 2026-09-05: arXiv v1 metadata와 CC BY-NC-ND 4.0 링크 확인.
- 2026-09-05: PDF 17/17쪽 렌더링 및 contact sheet 시각 확인.
- 2026-09-05: 수식의 mask 지시 함수, 조건부 문맥, 수치·단위를 arXiv HTML과 PDF에서 대조.
- 전문 번역이 아니며 license 경계를 넘어서는 원문 복제는 포함하지 않음.
