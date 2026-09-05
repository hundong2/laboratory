# 연속 학습을 위한 Fast Weight Attention

작성일: 2026-09-05

이 문서는 논문 **Fast Weight Attention for Continual Learning**을 처음 읽는 사람도
핵심 문제에서 구현상 주의점까지 순서대로 따라갈 수 있도록 정리한 한국어 학습
안내서다. 논문의 제안 계열명은 **Falcon**이며, 이 문서에서 말하는 연속 학습은
주로 한 시퀀스의 forward pass 안에서 고정 크기 fast-memory 상태를 온라인으로
갱신하는 의미다.

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [연구 질문](#연구-질문)
- [기초 개념](#기초-개념)
- [핵심 기여](#핵심-기여)
- [상세 정리](#상세-정리)
  - [시간 정렬: 왜 한 칸 이동하는가](#시간-정렬-왜-한-칸-이동하는가)
  - [Falcon 계열](#falcon-계열)
  - [재귀·마스크·청크 병렬 표현](#재귀마스크청크-병렬-표현)
  - [양의 감쇠 재정규화](#양의-감쇠-재정규화)
- [실험 설정과 결과](#실험-설정과-결과)
- [결과를 읽는 법](#결과를-읽는-법)
- [한계와 재현 주의점](#한계와-재현-주의점)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

| 항목 | 내용 |
|---|---|
| 원문 제목 | *Fast Weight Attention for Continual Learning* |
| 저자 | Yifan Zhang, Steve Ta, Jasper Zhang, Jichen Feng, Shuzhen Li, Yongxin Zhang, Yifeng Liu, Huizhuo Yuan, Mengdi Wang, Quanquan Gu, Andrew Chi-Chih Yao |
| 식별자 | arXiv:2608.27763v1 |
| 공개 형태 | arXiv preprint (2026) |
| DOI | [10.48550/arXiv.2608.27763](https://doi.org/10.48550/arXiv.2608.27763) - 확인일 현재 DataCite 등록 대기 |
| arXiv 제출일 | 2026-08-27 22:55:11 UTC |
| 원고 표기일 | 2026-03-09 |
| 원문 언어 | 영어 |
| 확인일 | 2026-09-05 |
| 공식 초록·메타데이터 | [arXiv abstract v1](https://arxiv.org/abs/2608.27763v1) |
| 공식 PDF | [arXiv PDF v1](https://arxiv.org/pdf/2608.27763v1) |
| 공식 소스 | [arXiv e-print v1](https://export.arxiv.org/e-print/2608.27763v1) |
| 라이선스 | [arXiv non-exclusive distribution license 1.0](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html) |
| 저자 표기 프로젝트 페이지 | [fast-weight-attention](https://github.com/yifanzhang-pro/fast-weight-attention) |

검토에는 공식 v1 PDF 54쪽과 같은 버전의 TeX 원문 전체를 사용했다. 초록,
본문, 실험 표, 알고리즘, 부록의 수식과 구현 주의사항까지 확인했다. 프로젝트
페이지는 논문에 적힌 링크를 기록한 것이며, 이 문서 작성 범위에는 외부 코드의
commit 단위 감사나 실행 재현은 포함하지 않는다. v1에 표시된 라이선스는 arXiv에
배포 권한을 주는 비독점 배포 라이선스이며, 일반적인 공개 파생물 허용 라이선스는
아니다. 따라서 번역 파일은 짧은 대조 예시만 원문과 함께 싣고, 나머지는 원문
section 순서를 보존한 한국어 해설 번역으로 구성한다.

다음 자료로 바로 이동할 수 있다.

- [한국어 해설 번역](<Fast Weight Attention for Continual Learning.번역.md>)
- [기초 실습](01_foundations.ipynb)
- [응용 실습](02_practice.ipynb)
- [심화 실습](03_advanced.ipynb)

## 한눈에 보기

Transformer의 KV cache는 문맥이 길어질수록 커진다. 반면 SSM과 fast-weight
모델은 지나온 문맥을 고정 크기 행렬 상태에 압축한다. 이때 상태 전이식은 단순한
메모리 연산이 아니라, 매 토큰마다 수행되는 **로컬 온라인 학습 규칙**으로 볼 수
있다.

논문은 read-after-write(RAW) 자기회귀 의미론에서 어떤 입력과 목표를 fast
memory에 결합해야 하는지 다시 묻는다. 논문이 다루는 prefix-prediction 목적에
맞는 쌍은 같은 시점의 `(key_t, value_t)`가 아니라 다음과 같다.

$$
\mathbf{x}_t = \phi(\mathbf{k}_{t-1}),
\qquad
\mathbf{y}_t = \mathbf{v}_t.
$$

즉, 현재 새로 드러난 목표 $\mathbf{v}_t$를 **그 목표를 예측할 때 이미 볼 수
있었던 prefix feature** $\phi(\mathbf{k}_{t-1})$에 연결한다. 같은 시점의 결합도
causal하지만, 논문이 정의한 내부 prefix-prediction 목적과는 다른 목적을
최적화한다.

이 정렬 위에서 논문은 회귀 목적의 Falcon-1/2/3과 내적 목적의
Falcon-1A/2A/3A를 유도한다. 숫자 1·2·3은 각각 scalar, per-column,
sliding-window 동역학을 뜻하고, `A`는 inner-product 목적을 뜻한다. 정규화된
step size가 plasticity를 입력 스케일에 맞추고, ridge 항이 forgetting을 제어하며,
재귀식을 마스크 또는 청크 병렬 계산으로 바꾸어 GPU 학습과 연결한다.

## 연구 질문

논문은 다음 질문을 하나의 틀에서 다룬다.

1. RAW 자기회귀 모델에서 fast memory가 학습해야 할 causal 입력·목표 쌍은
   무엇인가?
2. 고정 크기 상태를 온라인 선형 예측기로 보면 Delta/Linear Attention 계열의
   갱신식을 어떤 내부 목적에서 유도할 수 있는가?
3. 입력의 크기에 따라 학습률이 지나치게 달라지지 않도록 NLMS 방식으로
   plasticity를 어떻게 정규화할 것인가?
4. 새 정보를 쓰는 능력, 기존 정보를 잊는 정도, 최근 예제를 다시 쓰는 범위를
   각각 분리해 제어할 수 있는가?
5. 순차적으로 정의한 갱신을 재귀 추론뿐 아니라 masked-parallel 또는
   chunk-parallel 학습으로도 정확하거나 명시된 조건 아래 동등하게 계산할 수
   있는가?

## 기초 개념

### Fast weight와 slow weight

- **Slow weight**는 일반적인 신경망 파라미터다. 데이터셋 학습 중 optimizer로
  갱신되고, 추론 한 번 안에서는 보통 고정된다.
- **Fast weight** $\mathbf{S}_t$는 토큰을 읽는 동안 forward pass 안에서 계속
  갱신되는 상태다. 이 논문에서는 $\mathbf{S}_t\in\mathbb{R}^{d_x\times d_v}$인
  선형 메모리 행렬로 모델링한다.
- outer autoregressive loss는 slow weight를 학습한다. fast-memory용 순간 목적은
  별도의 supervised loss를 더하는 것이 아니라, forward 내부 상태 갱신을
  정의한다. 학습할 때는 이 갱신을 통과해 미분한다.

### Transformer, Linear Attention, SSM

표준 self-attention은 길이 $N$에 대해 attention 행렬 계산이
$\mathcal{O}(N^2)$으로 증가한다. Linear Attention과 선택적 SSM 계열은 문맥을
고정 크기 상태에 누적하여 학습 계산을 선형화하고, 토큰별 재귀 추론을
$\mathcal{O}(1)$ 상태 갱신으로 표현할 수 있다. 대신 무엇을 어떤 규칙으로 상태에
쓸지가 모델 품질과 장기 기억을 좌우한다.

### OGD, LMS, NLMS와 ridge

- **OGD (Online Gradient Descent)**: 새 예제가 들어올 때마다 한 번의 gradient
  step을 수행한다.
- **LMS (Least Mean Squares)**: 선형 예측 오차에 대한 대표적인 1차 온라인
  갱신이다.
- **NLMS (Normalized LMS)**: 입력 에너지로 step size를 나누어 입력 스케일에
  대한 민감도를 줄인다.
- **Ridge regularization** $\lambda_t\|\mathbf{S}\|_F^2/2$: 상태를 줄이는
  항이다. Falcon에서는 전역 forgetting을 만드는 carry와 연결된다.

### 두 내부 목적

회귀 계열은 순간 ridge-regression 목적을 사용한다.

$$
\ell_t(\mathbf{S})=
\frac{1}{2}\|\mathbf{S}^{\top}\mathbf{x}_t-\mathbf{y}_t\|_2^2
+\frac{\lambda_t}{2}\|\mathbf{S}\|_F^2.
$$

반면 `A` 계열은 negative inner-product 목적을 사용한다. 회귀형 write는 이전
예측의 residual을 고치는 반면, 내적형 write는 target outer product를 직접
더한다. 내적 목적에서 $\lambda_t=0$이면 목적 자체는 아래로 유계가 아니므로,
분모는 곡률에 맞춘 보장이라기보다 write magnitude를 안정화하는 장치로 읽어야
한다.

## 핵심 기여

1. **시간 정렬의 명시화**: RAW에서 prefix-prediction에 대응하는 fast-memory
   예제가 $(\phi(\mathbf{k}_{t-1}),\mathbf{v}_t)$임을 분리해 설명한다.
2. **정규화된 회귀 계열**: scalar NLMS인 Falcon-1, value column마다 step size가
   다른 Falcon-2, 최근 창의 mini-batch residual을 쓰는 Falcon-3을 유도한다.
3. **내적 목적 계열**: 같은 plasticity/forgetting 의미를 유지하면서 residual
   대신 직접 write하는 Falcon-1A/2A/3A를 제시한다.
4. **제어 변수의 분리**: dimensionless gain $\beta_t$는 plasticity,
   $\lambda_t$는 shrinkage/forgetting, 실제 step size $\eta_t$는 입력 또는 창의
   통계에 맞춘 정규화 결과로 구분한다.
5. **병렬 표현**: WY/Gram, structured masked attention, ParallelFlow의 low-rank
   affine scan을 이용해 재귀 의미를 청크 병렬 학습과 연결한다.
6. **수치 안정성**: 감쇠 carry가 양수가 되도록 clamp하고, 전역 누적곱 대신
   청크 내부 log-prefix를 사용하는 재정규화를 상세히 제시한다.
7. **제한된 실증**: 대표 변형이 약 50B-token 규모의 소형 언어 모델에서
   경쟁력을 유지하고, variable-digit addition의 길이 외삽에서 개선됨을 보인다.

## 상세 정리

이 절에서는 논문의 핵심을 시간축 의미, 여섯 갱신 규칙, 병렬 계산 형태,
수치 안정성의 순서로 연결한다.

### 시간 정렬: 왜 한 칸 이동하는가

논문은 다음 RAW 순서를 사용한다.

1. 토큰 $t$와 그로부터 계산한 $\mathbf{v}_t$가 새로 드러난다.
2. 이전 prefix에서 만든 write feature $\mathbf{x}_t=\phi(\mathbf{k}_{t-1})$와
   $\mathbf{v}_t$를 fast-memory 학습 예제로 사용한다.
3. $\mathbf{S}_{t-1}$을 $\mathbf{S}_t$로 갱신한다.
4. 갱신된 상태를 읽어 다음 위치를 예측한다.

따라서 내부 fast-memory 예측과 모델의 현재 readout을 구분해야 한다.

$$
\widehat{\mathbf{y}}_t=\mathbf{S}_{t-1}^{\top}\mathbf{x}_t,
\qquad
\mathbf{o}_t=\mathbf{S}_t^{\top}\phi(\mathbf{q}_t).
$$

첫 위치에는 대응할 이전 feature가 없으므로
$\mathbf{x}_1:=\mathbf{0}$, $\eta_1:=0$을 둔다. 이 sentinel이 없으면 실제
데이터 쌍을 쓰지 않는 첫 step에서도 $\lambda_1$ 때문에 전달받은 상태가
감쇠할 수 있다.

중요한 구분은 다음과 같다.

- `(phi(k_t), v_t)` 같은 same-step association도 미래를 보지 않으므로
  causal이다.
- 그러나 논문의 prefix-prediction 내부 목적에서는 $v_t$를 예측할 당시 이용
  가능했던 feature가 `phi(k_{t-1})`이므로 shifted pair가 목적과 정렬된다.
- 논문이 증명하는 descent는 각 시점의 순간 목적에 대한 pointwise 성질이다.
  누적 online loss나 바깥 autoregressive likelihood가 매 step 감소한다는
  의미가 아니다.

### Falcon 계열

공통 표기는 다음과 같다.

$$
\mathbf{x}_t=\phi(\mathbf{k}_{t-1}),\quad
\mathbf{y}_t=\mathbf{v}_t,\quad
\mathbf{r}_t=\mathbf{y}_t-\mathbf{S}_{t-1}^{\top}\mathbf{x}_t.
$$

| 변형 | 내부 목적 | plasticity 형태 | 핵심 write |
|---|---|---|---|
| Falcon-1 | squared-error regression | 모든 value channel이 scalar $\eta_t$ 공유 | 현재 residual의 rank-one correction |
| Falcon-2 | squared-error regression | column별 $\eta_{j,t}$ | 공유 feature 방향, channel별 correction/decay |
| Falcon-3 | windowed regression | scalar $\eta_t$, 창 크기 $B$ | 최근 창 residual gradient의 평균 |
| Falcon-1A | negative inner product | scalar $\eta_t$ | 현재 target outer product 직접 write |
| Falcon-2A | negative inner product | column별 $\eta_{j,t}$ | channel별 gain을 적용한 직접 write |
| Falcon-3A | windowed inner product | scalar $\eta_t$, 창 크기 $B$ | 최근 창 cross-covariance 평균 직접 write |

#### Falcon-1: scalar NLMS 회귀

$$
\mathbf{S}_t=(1-\eta_t\lambda_t)\mathbf{S}_{t-1}
+\eta_t\mathbf{x}_t\mathbf{r}_t^{\top},
\qquad
\eta_t=\frac{\beta_t}{\|\mathbf{x}_t\|_2^2+\lambda_t+\varepsilon}.
$$

$\lambda_t=0$, $\varepsilon=0$인 특별한 경우 고전 NLMS recursion과 정확히
같다. $\beta_t\in(0,2)$는 정규화된 dimensionless gain이다.

#### Falcon-2: column별 적응

Falcon-2는 $\boldsymbol{\eta}_t\in\mathbb{R}^{d_v}$를 사용하여 value channel마다
서로 다른 plasticity와 decay trajectory를 허용한다. 표현력은 늘지만 청크마다
$d_v$개의 rate-dependent triangular system을 풀어야 하므로 Falcon-1보다
메모리 대역폭과 계산 부담이 클 수 있다.

#### Falcon-3: sliding-window 회귀

활성 창 $\mathcal{I}_t$의 크기를 $B_t\le B$라 하면 다음 평균 residual step을
사용한다.

$$
\mathbf{S}_t=(1-\eta_t\lambda_t)\mathbf{S}_{t-1}
+\frac{\eta_t}{B_t}\sum_{j\in\mathcal{I}_t}
\mathbf{x}_j(\mathbf{y}_j-\mathbf{S}_{t-1}^{\top}\mathbf{x}_j)^{\top}.
$$

step size의 분모에는 평균 공분산의 최대 고윳값
$\mu_t^{(B)}=\lambda_{\max}(B_t^{-1}\sum_j\mathbf{x}_j\mathbf{x}_j^\top)$를
사용한다. $B_t\times B_t$ Gram matrix로 구할 수 있어, 의도한 작은 $B$에서는
$d_x\times d_x$ 공분산을 직접 만들 필요가 없다.

#### Falcon-A: residual 없는 내적 write

Falcon-1A는 다음처럼 target을 직접 쓴다.

$$
\mathbf{S}_t=(1-\eta_t\lambda_t)\mathbf{S}_{t-1}
+\eta_t\mathbf{x}_t\mathbf{y}_t^{\top},
\qquad
\eta_t=\frac{\beta_t}{E_t+\lambda_t+\varepsilon},
\quad E_t=\|\mathbf{x}_t\|_2^2.
$$

Falcon-2A는 이를 column별 gain으로 확장한다. Falcon-3A는 창의 평균
cross-covariance $\bar{\mathbf{N}}_t^{(B)}$와 평균 write energy
$\bar E_t^{(B)}$를 사용한다.

$$
\mathbf{S}_t=(1-\eta_t\lambda_t)\mathbf{S}_{t-1}
+\eta_t\bar{\mathbf{N}}_t^{(B)},
\qquad
\eta_t=\frac{\beta_t}{\bar E_t^{(B)}+\lambda_t+\varepsilon}.
$$

$B=1$이면 Falcon-3A는 경계 이후 Falcon-1A로 환원된다.

#### 실험 이름의 `.1`, `.2`, `.3`

가족 번호 1·2·3과 별도로, 실험 표의 소수점 뒤 번호는 다음 구성 ablation을
구분한다.

| suffix | Q/K 정규화 | context-conditioned 항 |
|---|---|---|
| `.1` | $\ell_2$ normalization | $\beta$, $\lambda$ |
| `.2` | $\ell_2$ normalization | $\eta$, $\lambda$ |
| `.3` | RMSNorm | $\eta$, $\lambda$ |

### 재귀·마스크·청크 병렬 표현

같은 수학적 갱신도 목적에 따라 서로 다른 계산 형태가 유리하다.

| 형태 | 역할 | 논문의 구현 관점 |
|---|---|---|
| Recurrent | 토큰별 streaming inference와 참조 구현 | 고정 크기 $\mathbf{S}_t$를 순서대로 갱신하고 RAW readout 계산 |
| Masked-parallel | 재귀를 sequence-parallel attention 계산으로 전개 | Falcon-3A를 decay-weighted causal mask와 window operator의 합성으로 표현 |
| Chunk-parallel | 긴 시퀀스를 GPU 친화적인 청크 단위로 처리 | Falcon-1/2는 WY·Gram, Falcon-3는 ParallelFlow, Falcon-3A는 청크 로컬 masked attention 사용 |

Falcon-1/2의 rank-one 회귀는 한 청크 안에서 WY/Gram 형태로 바꾼다.
Falcon-2는 channel별 작은 triangular system이 필요하고, Falcon-1은 모든 value
channel이 동역학을 공유해 한 system을 여러 right-hand side에 재사용한다.

Falcon-3는 창을 폭 $B$로 zero-padding하면 고정 rank-$B$ affine recurrence가
된다. 논문은 이를 ParallelFlow의 `tensorInv` structured solve와 associative
chunk map에 연결한다. 이 변환은 이산 갱신 수준에서 approximation 없이
Falcon-3 recurrence를 보존한다고 설명한다. 예시 실험에서 언급한 작은 창은
$B=4$다.

Falcon-3A를 펼치면 출력은 들어오는 경계 상태의 decayed-history 항과 다음
structured attention 항의 합이 된다.

$$
\mathbf{O}=
\operatorname{Diag}(\boldsymbol{\delta})\mathbf{Q}\mathbf{S}_0
+(\mathbf{Q}\mathbf{X}^{\top}\odot\mathbf{M})\mathbf{V}.
$$

원래 window operator는 $B$-banded지만 carry를 거쳐 누적된 $\mathbf{M}$은
일반적으로 dense lower-triangular decay tail을 갖는다. 따라서 “sliding
window”가 곧 엄격한 길이-$B$ 기억 절단을 의미하지 않는다.

또한 Falcon-3/3A를 segment 경계에서 정확히 이어가려면 행렬 상태만 넘겨서는
안 된다. 오래된 항을 다음 창에서 정확히 빼기 위해 마지막 $B-1$개의 causal
pair 또는 동등한 rolling-window 표현도 함께 전달해야 한다.

### 양의 감쇠 재정규화

Ridge가 만드는 원래 carry는 $1-\eta_t\lambda_t$다. 긴 시퀀스에서 carry의
누적곱은 mixed precision underflow/overflow에 취약하고, log를 쓰려면 carry가
양수여야 한다. 논문 구현은 다음 파생량을 사용한다.

$$
\alpha_t=\min(\eta_t\lambda_t,1-\varepsilon_\gamma),
\qquad
\gamma_t=1-\alpha_t\ge\varepsilon_\gamma>0,
$$

$$
\log\gamma_t=\operatorname{log1p}(-\alpha_t)
\quad\text{(fp32)}.
$$

핵심 구현 규칙은 다음과 같다.

- 전체 시퀀스의 $c_t=\prod_{r\le t}\gamma_r$를 직접 만들지 않는다.
- 청크 경계에서 log-prefix를 0으로 다시 시작하고 청크 내부 차이만 사용한다.
- no-ridge rank-one kernel로 정확히 환원하려면 step size뿐 아니라 write target도
  이전 누적 감쇠의 역수로 재조정해야 한다. $\eta$만 바꾸면 동등하지 않다.
- clamp가 활성화되면 원래 $\lambda_t$의 gradient step이 아니라
  $\widetilde\lambda_t=\alpha_t/\eta_t$인 effective shrinkage로 해석해야 한다.
  원래 순간 목적에 대한 descent 보장은 clamp 이전 갱신에 해당한다.
- denominator-free read는 이 공통 rescaling에 영향을 받지 않는다. 정규화된
  numerator/denominator read에 고정 $\varepsilon_{\rm attn}$를 그대로 넣으면
  정확한 동등성이 깨질 수 있으므로, 공통 rescaling을 되돌린 뒤 ratio를 만들거나
  stabilizer도 같은 비율로 바꿔야 한다.
- signed feature에서 denominator에 양의 상수만 더한다고 0 또는 음수 분모가
  방지되지는 않는다. 논문은 signed-feature 해석의 기본값으로 denominator-free
  inner-product read를 둔다.

## 실험 설정과 결과

### 언어 모델 학습 설정

- 학습 데이터: FineWeb-Edu
- 모델 크기: Transformer 124M, recurrent 모델 130M
- 학습량: 100,000 optimization step, sequence length 1,024, global batch 480,
  약 49.2B token(논문 표에서는 50B-token budget으로 표기)
- 공통 설정: bfloat16, AdamW, tied input/output embedding, Pre-Norm RMSNorm,
  bias 없음, dropout 없음
- optimizer 세부값: $\mu$P-style width scaling, base learning rate $10^{-3}$,
  cosine decay, 2,000 warmup step, Adam $\beta=(0.9,0.95)$, weight decay 0.1,
  gradient clipping 1.0
- 하드웨어: NVIDIA H100 또는 H200 GPU 4장으로 구성된 단일 node
- 비교 모델: LLaMA-style RoPE/SwiGLU Transformer, RetNet/LightningAttn,
  Mamba-2, DeltaNet, Gated DeltaNet
- 평가: held-out teacher-forced perplexity와 8개 downstream task의 zero-shot 및
  one-shot accuracy

Perplexity 표의 `Wiki.`, `LMB.`, `FineEdu.` 열을 그대로 옮긴 대표 결과다.
낮을수록 좋다. v1 본문은 `LMB.`의 전체 명칭을 이 표 주변에서 풀어 쓰지 않는다.

| 모델 | Wiki. | LMB. | FineEdu. |
|---|---:|---:|---:|
| Transformer 124M | 33.25 | 47.43 | 17.38 |
| Gated DeltaNet 130M | **30.99** | **46.70** | 17.32 |
| Falcon-1A.1 130M | 34.41 | 47.93 | 17.70 |
| Falcon-1A.2 130M | 34.20 | 51.01 | 17.70 |
| Falcon-1A.3 130M | 34.02 | 49.84 | 17.40 |
| Falcon-1.3 130M | 33.00 | 48.70 | **17.10** |

Downstream 평가는 PIQA, HellaSwag, WinoGrande, ARC-Easy, ARC-Challenge,
OpenBookQA, Social IQA, SciQ의 8개 task를 사용하고 단순 평균을 보고한다.
HellaSwag, ARC-Challenge, OpenBookQA는 `lm-evaluation-harness`의 `acc_n`, 나머지는
`acc`를 사용한다.

| 대표 비교 | Zero-shot 평균 | One-shot 평균 |
|---|---:|---:|
| Transformer 124M | 48.16 | **49.67** |
| 가장 높은 recurrent baseline | 48.88 (DeltaNet) | 49.16 (Mamba-2) |
| Falcon-1A.2 | **49.30** | 49.20 |
| Falcon-3A.3 | 49.00 | 49.03 |
| Falcon-1.3 | 49.18 | **49.54** |

Falcon-1A.2가 표에 실린 전체 모델 가운데 zero-shot 평균이 가장 높다.
one-shot에서는 Falcon-1.3이 recurrent 모델 중 가장 높지만, Transformer의
49.67보다는 낮다.

### Variable-digit addition

입력은 동일한 자릿수 $n$의 두 수를 더하는 문자열이며, 출력은 $(n+1)$자리 합을
뒤집어 least-significant digit부터 생성한다. 학습 자릿수는 1부터 32까지
균등하게 뽑고, target suffix에 대해서만 masked next-token log-likelihood를
최적화한다.

평가는 in-distribution validation accuracy와 33~48자리 OOD 구간의
teacher-forced target-suffix accuracy 평균을 사용한다. `Acc@d33/d48`은 각각
33자리와 48자리 결과다.

| 모델 | Validation | OOD 33~48 평균 | Acc@d33/d48 |
|---|---:|---:|---:|
| Transformer | 100.0 | 65.8 | 97.0 / 49.0 |
| RetNet/LightningAttn | 99.7 | 82.9 | 99.0 / 63.0 |
| Mamba-2 | 100.0 | 75.2 | 100.0 / 51.0 |
| Falcon-1A.1 | 100.0 | 80.6 | 100.0 / 59.0 |
| Falcon-1A.2 | 100.0 | 85.2 | 100.0 / 63.0 |
| Falcon-1A.3 | 99.8 | 85.9 | 100.0 / 69.0 |
| Falcon-3A.3 | 99.9 | **87.2** | **100.0 / 69.0** |
| Falcon-1.3 | 100.0 | 68.8 | 100.0 / 48.0 |

Falcon-3A.3이 OOD 평균 87.2로 가장 높고 Falcon-1A.3이 85.9로 뒤를 잇는다.
다만 이는 모델이 직접 생성한 전체 식의 exact-match가 아니라 teacher forcing을
사용한 target-suffix accuracy다.

## 결과를 읽는 법

- 논문 스스로도 언어 모델 결과를 **일률적인 승리**로 해석하지 않는다.
  FineWeb-Edu에서는 Falcon-1.3이 가장 낮은 perplexity를 보였지만 Wiki/LMB에서는
  Gated DeltaNet이 더 낮고, one-shot 전체 평균은 Transformer가 더 높다.
- 설계의 강한 실증 신호는 addition 길이 외삽이다. 특히 inner-product 계열의
  shifted, normalized write가 저장과 carry propagation이 중요한 통제 과제에서
  높은 33~48자리 성능을 보였다.
- 같은 실험에서 regression Falcon-1.3은 OOD 평균 68.8이므로 “회귀 목적이면
  항상 더 좋다” 또는 “Falcon 계열 모두가 같은 개선을 보인다”고 일반화할 수
  없다.
- 언어 모델 표는 품질 비교이지, 논문이 주장하는 선형/청크 병렬 구조의 실제
  wall-clock throughput 또는 peak-memory 우위를 직접 측정한 표가 아니다.

## 한계와 재현 주의점

1. **평가된 계열이 제한적이다.** Falcon-2, Falcon-2A, Falcon-3은 정의와
   병렬화 방법은 있지만 main table에서 개별 benchmark되지 않는다. 실험은
   Falcon-1A/3A와 regression ablation Falcon-1.3에 집중한다.
2. **소형 모델·제한된 도메인이다.** 언어 모델은 124M~130M 규모이고 학습은
   FineWeb-Edu 한 데이터 계열에 집중한다. 더 큰 모델과 다양한 장기 문맥
   과제로의 일반화는 이 결과만으로 확정할 수 없다.
3. **불확실성 보고가 부족하다.** 확인한 v1 실험 표와 setup에는 여러 random
   seed의 평균·표준편차나 신뢰구간이 제시되지 않는다.
4. **Teacher forcing 경계가 있다.** perplexity와 addition OOD 결과는
   teacher-forced 평가다. 자유 생성에서 오류가 누적될 때 같은 정확도가
   유지된다고 볼 수 없다.
5. **재현 설정이 모두 열거되지는 않는다.** 논문은 주요 optimizer와 hardware
   설정을 주지만 tokenizer, 전체 layer/head 차원, 모든 모델별 gate 초기화와
   정확한 data preprocessing을 한 표로 완결해 제시하지 않는다. 프로젝트의
   versioned config와 함께 확인해야 한다.
6. **본문의 table 참조 불일치가 있다.** v1 TeX는 small/medium downstream
   table들을 함께 언급하지만, 확인한 원문에는 `tab:accuracy_results_small`만
   있고 `tab:accuracy_results_medium`의 실제 표는 보이지 않는다. 따라서 이
   문서는 존재하는 124M~130M 표만 보고한다.
7. **clamp는 목적을 바꿀 수 있다.** positive-decay clamp가 작동하면 구현된
   shrinkage는 원래 ridge coefficient가 아닌 effective coefficient를 따른다.
8. **창 상태는 행렬 하나가 아니다.** Falcon-3/3A의 정확한 segment continuation은
   마지막 $B-1$개 pair도 필요하다. 이를 버리면 경계 부근 동역학이 달라진다.
9. **정규화 분모를 조심해야 한다.** signed feature를 쓰는 normalized read는
   분모 부호와 0 통과를 별도로 처리해야 한다.
10. **복잡도와 실측 성능을 구분해야 한다.** 특히 Falcon-2는 channel별 triangular
    solve 비용이 있고, Falcon-3의 `tensorInv` 비용을 $d_x,d_v$ 의존성을 숨긴
    축약 표기만으로 판단하면 안 된다.

## 용어 정리

| 용어 | 뜻과 이 논문에서의 역할 |
|---|---|
| Fast weight | 한 forward pass 안에서 토큰마다 바뀌는 단기 메모리 상태 |
| Continual learning | 여기서는 주로 시퀀스 안에서 새 예제를 계속 결합하는 온라인 상태 학습 |
| SSM | State Space Model. 문맥을 상태 전이로 압축하는 sequence model 계열 |
| SSD | Structured State Space Duality. 선택적 SSM과 structured masked attention을 잇는 관점 |
| RAW | Read After Write. 현재 토큰을 상태에 쓴 뒤 갱신된 상태를 읽는 순서 |
| RBW | Read Before Write. 기존 상태를 먼저 읽고 이후 현재 정보를 쓰는 순서 |
| Next-latent alignment | $\phi(k_{t-1})$를 새로 드러난 $v_t$와 결합하는 prefix 정렬 |
| OGD | Online Gradient Descent. 예제마다 한 번 수행하는 gradient update |
| LMS / NLMS | 최소평균제곱 갱신 / 입력 에너지로 정규화한 LMS |
| Plasticity | fast memory가 새 정보에 얼마나 크게 반응하는지 나타내는 성질. $\beta$가 기본 제어 |
| Ridge / shrinkage | $\lambda$로 상태 크기를 줄여 forgetting을 만드는 정규화 |
| $\eta_t$ | 실제 normalized step size. $\beta$와 local energy/smoothness에서 계산 |
| $\phi(k)$ | raw key를 memory write 공간으로 보내는 feature map |
| Residual write | 기존 메모리 예측 오차 $y-S^\top x$를 고치는 회귀형 write |
| Inner-product write | residual 없이 $xy^\top$를 직접 누적하는 write |
| Sliding window | 최근 $B$개 이하 pair의 평균으로 한 update를 구성하는 bounded rehearsal |
| Gram matrix | feature 내적을 모은 작은 행렬. Falcon-2/3의 병렬 계산과 smoothness 산출에 사용 |
| WY form | rank-one update들의 곱을 청크 단위 triangular solve로 계산하는 표현 |
| ParallelFlow | low-rank affine recurrence를 청크 map과 scan으로 병렬화하는 틀 |
| `tensorInv` | Falcon-3의 time×rank causal interaction을 처리하는 structured triangular solve |
| Teacher forcing | 평가 시 이전 정답 token을 조건으로 다음 token을 채점하는 방식 |

## 실습 학습 가이드

실습은 논문 수치를 재현했다고 주장하는 대신, 작은 배열과 합성 데이터로 수식의
동작과 구현 함정을 검증하는 toy reproduction으로 구성한다.

Python 3.10 이상에서 다음 최소 의존성을 설치한 뒤 Jupyter에서 순서대로 실행한다.

```bash
python -m pip install jupyter numpy matplotlib
jupyter notebook
```

1. [01_foundations.ipynb](01_foundations.ipynb)
   - shifted pair를 직접 만들고 tensor shape와 RAW 시간 정렬 확인
   - 명시적 prefix 합과 recurrent linear-attention state의 수치 동치 검증
   - 미래 교란 인과성 검사와 denominator-free/normalized read 비교
2. [02_practice.ipynb](02_practice.ipynb)
   - 분포가 중간에 바뀌는 synthetic stream에서 Falcon-1/2 NumPy 구현
   - shifted pair와 same-step mismatch의 온라인 예측 오차 비교
   - scalar/per-column step size, state norm과 변화 이후 적응 곡선 분석
3. [03_advanced.ipynb](03_advanced.ipynb)
   - Falcon-3형 sliding regression의 $B=1,4,8$ window ablation
   - 양의 decay clamp가 음수 carry를 막는지 검사
   - 순차 affine recurrence와 chunk 단위 합성 결과의 수치 동치 검증

## 다음 학습 경로

1. 먼저 [한국어 해설 번역](<Fast Weight Attention for Continual Learning.번역.md>)의
   Abstract, Introduction, Autoregressive Next-Latent Prediction을 읽어 RAW와
   shifted pair를 확실히 구분한다.
2. [기초 실습](01_foundations.ipynb)에서 additive fast-weight state를 직접 계산하며
   shifted write, recurrent/prefix 동치와 인과성을 익힌다.
3. Delta Network와 Linear Attention을 각각 squared-error objective와
   inner-product objective로 다시 유도해 두 family의 residual 유무를 비교한다.
4. [응용 실습](02_practice.ipynb)에서 Falcon-1/2를 동일한 toy stream에 적용하고,
   plasticity·forgetting·column별 gain을 독립적으로 바꾼다.
5. [심화 실습](03_advanced.ipynb)에서 sliding regression과 scalar-carry affine
   chunk 합성을 확인한 뒤, 논문 부록의 WY/Gram·structured mask·rank-$B$
   ParallelFlow 구현으로 확장한다.
6. 실제 프로젝트 코드를 재현할 때는 논문 링크의 특정 commit, 환경, tokenizer,
   dataset preprocessing, seed를 고정하고 품질뿐 아니라 throughput, peak memory,
   자유 생성 정확도도 별도로 측정한다.
