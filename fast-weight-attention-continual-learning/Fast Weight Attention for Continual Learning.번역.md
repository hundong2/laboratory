<!-- rumdl-disable MD013 MD036 -->

# 계속학습을 위한 빠른 가중치 어텐션 - 한국어 해설 번역

## 학습 자료 바로가기

- [논문 분석 및 학습 개요](README.md)
- [기초 실습: fast-weight memory와 시간 정렬](01_foundations.ipynb)
- [응용 실습: Falcon-1·2 온라인 회귀](02_practice.ipynb)
- [심화 실습: Falcon-3형 sliding regression과 chunk affine 동치](03_advanced.ipynb)

## 논문 메타데이터

| 항목 | 내용 |
|---|---|
| 원문 제목 | *Fast Weight Attention for Continual Learning* |
| 저자 | Yifan Zhang, Steve Ta, Jasper Zhang, Jichen Feng, Shuzhen Li, Yongxin Zhang, Yifeng Liu, Huizhuo Yuan, Mengdi Wang, Quanquan Gu, Andrew Chi-Chih Yao |
| 소속 | ByteDance Seed, Princeton University, Tsinghua University, Hyperbolic Labs. PDF에는 UCLA도 소속 번호 4로 표시되지만 저자 이름의 위첨자에는 번호 4가 연결되어 있지 않다. |
| 교신 저자 | Mengdi Wang, Quanquan Gu, Andrew Chi-Chih Yao |
| 문서 유형 | arXiv 사전 공개 논문(preprint) |
| 주 분류 | Machine Learning (`cs.LG`) |
| 교차 분류 | Computation and Language (`cs.CL`), Machine Learning (`stat.ML`) |
| arXiv 식별자 | `arXiv:2608.27763v1` |
| 제출일 | 2026-08-27 22:55:11 UTC |
| 원고 내부 날짜 | 2026-03-09. arXiv 제출일과 다른 원고 자체의 날짜이다. |
| DOI | <https://doi.org/10.48550/arXiv.2608.27763> - 확인일 현재 arXiv 페이지에는 DataCite 등록 대기 상태로 표시된다. |
| 원문 URL | <https://arxiv.org/abs/2608.27763>, <https://arxiv.org/pdf/2608.27763> |
| 프로젝트 페이지 | <https://github.com/yifanzhang-pro/fast-weight-attention> |
| 사용한 버전 | v1 공식 PDF 54쪽과 v1 TeX 원문 |
| 원문 언어 | 영어 |
| 확인일 | 2026-09-05 |
| 라이선스 | [arXiv 비독점 배포 라이선스](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html) |

> **저작권 및 번역 범위:** 이 논문의 arXiv 라이선스는 저자가 arXiv에 배포권을 부여한 것이며, 제3자에게 개작물의 자유로운 배포를 허용하는 오픈 라이선스가 아니다. 따라서 이 파일은 영어 전문을 복제하는 문장별 완역이 아니다. 공식 제목과 서지정보, 기술적으로 필요한 수식, 25단어 이내의 짧은 대조 예시 한 문장만 원문 형태로 제시하고, 나머지는 원문의 섹션 순서를 따르는 한국어 해설 번역으로 작성했다. 저자의 주장과 번역자의 해석은 명시적으로 구분한다.

## 번역 및 접근 범위

| 원문 범위 | 상태 | 이 문서에서 제공하는 범위 |
|---|---|---|
| 제목·저자·서지정보 | 완료 | arXiv 레코드, PDF 첫 쪽, TeX 원문을 대조했다. |
| 초록 | 완료 - 해설 번역 | 전체 논지를 한국어로 재구성하고 짧은 문장 대조 예시 1개를 제공한다. |
| 1. 서론 | 완료 - 해설 번역 | 문제 설정, 시간 정렬의 차이, 네 가지 기여를 설명한다. |
| 2. 배경 | 완료 - 해설 번역 | SSM, 선형 어텐션, Delta Network를 설명한다. |
| 3. 자기회귀 다음 잠재표현 예측 | 완료 - 해설 번역 | 순간 ridge 목적, OGD, 인과 경계, 국소 하강 보장을 다룬다. |
| 4. Falcon: Fast Weight Attention | 완료 - 해설 번역 | Falcon-1/2/3과 Falcon-1A/2A/3A, 정규화, 병렬화를 다룬다. |
| 5. 실험 | 완료 - 해설 번역 | 언어 모델링과 가변 자릿수 덧셈의 조건·수치를 해석한다. |
| 6. 관련 연구 | 완료 - 해설 번역 | 효율적 시퀀스 모델, fast weight, 적응 필터, 내부 최적화 관점을 정리한다. |
| 7. 결론 | 완료 - 해설 번역 | 기여의 범위와 실증적 결론을 구분한다. |
| 부록 A-H | 완료 - 기술 해설 | RLS, 구현·경계 규칙, WY 병렬화, ParallelFlow를 요약한다. 알고리즘 원문은 재수록하지 않는다. |
| 그림 1-11 | 완료 - 해석 | 그림이 비교하는 대상과 읽는 방법을 설명한다. |
| 표 1-4 | 완료 - 해석 | 핵심 수치와 비교 범위를 보존해 해석한다. |
| 참고문헌 | 해당 없음 | 저자·제목·연도 목록은 복제하지 않고 본문에서 필요한 연구 계보만 설명한다. |
| 영어 전문 문장 대조 | 저작권상 제한 | 아래 `S001` 한 문장만 제공한다. 그 외 섹션은 한국어 해설 번역이다. |

### 식별자 규칙

- `S001`은 영어 원문과 한국어를 직접 잇는 유일한 문장 대조 단위다.
- `K001` 이후는 원문의 논리와 수치를 보존해 재구성한 **한국어 해설 번역 단위**다. 영어 원문 한 문장과 1:1로 대응한다는 뜻이 아니다.
- 수식 번호 `E1` 이후는 이 학습 문서에서 참조하기 위한 번호이며, 원 논문의 식 번호와 같지 않을 수 있다.

## 읽기 전 핵심 배경

1. **Fast weight(빠른 가중치)**는 모델의 학습된 장기 파라미터와 달리, 한 시퀀스를 처리하는 동안 입력에 따라 즉시 갱신되는 상태다. 이 논문에서는 행렬 $\mathbf S_t$가 그 역할을 한다.
2. **계속학습(continual learning)** 관점에서는 토큰 하나가 들어올 때마다 작은 학습 예제가 하나씩 도착한다. 새 정보를 기록하면서 이전 정보를 얼마나 유지할지가 가소성·망각의 문제다.
3. **선형 어텐션(linear attention)**은 키-값 외적을 누적한 행렬 상태를 사용하여 표준 self-attention의 시퀀스 길이에 대한 이차 비용을 피한다.
4. **Delta rule**은 새 값을 단순히 더하는 대신 현재 예측 오차를 이용해 상태를 수정한다. 적응 필터의 LMS/NLMS와 연결된다.
5. 이 논문의 핵심은 새로운 블록을 하나 더 쌓는 데 있지 않다. **어느 시점의 특징을 어느 시점의 목표와 묶어 fast memory를 학습할 것인가**를 명시하고, 그 목적에 맞는 정규화 갱신을 유도하는 데 있다.

## 짧은 문장 대조 예시

아래 영어 본문은 14단어다. 공식 제목을 포함해도 이 파일에서 직접 재현하는 영어 문장성 원문은 25단어를 넘지 않는다.

**S001 — Original**

This framework separates temporal alignment, plasticity, forgetting, and bounded rehearsal in recurrent sequence models.

**S001 — 한국어**

(이 틀은 순환 시퀀스 모델에서 시간 정렬, 가소성, 망각, 제한된 리허설을 서로 분리해 다룬다.)

- **용어·약어 해설**
  - **시간 정렬(temporal alignment)**: 어떤 시점의 write feature와 어떤 시점의 target을 하나의 온라인 학습 쌍으로 삼는지 정하는 규칙이다.
  - **가소성(plasticity)**: 새 입력에 맞추어 fast memory를 얼마나 크게 바꾸는지를 뜻한다.
  - **제한된 리허설(bounded rehearsal)**: Falcon-3 계열처럼 고정 크기 창 안의 최근 예제를 다시 사용하되, 메모리 사용량이 시퀀스 길이에 따라 무한히 늘지 않게 하는 방식이다.

## 섹션별 한국어 해설 번역

### 초록

**K001 - 저자 주장 해설 번역**

저자들은 recurrent fast-weight memory와 선택적 SSM이 계속 길어지는 문맥을 고정 크기 상태로 압축한다는 점에서, 상태 전이를 하나의 온라인 학습 규칙으로 볼 수 있다고 출발한다. 논문은 갱신한 뒤 읽는 RAW(read-after-write) 자기회귀 의미론을 채택한다. 이때 시점 $t$에서 새로 확인된 목표 $\mathbf v_t$를, 그 목표를 예측할 때 이미 이용 가능했던 이전 키의 특징 $\phi(\mathbf k_{t-1})$와 묶는다.

같은 시점의 $\phi(\mathbf k_t)$와 $\mathbf v_t$를 묶는 통상적인 방식도 인과적일 수 있다. 저자들의 주장은 그것이 비인과적이라는 것이 아니라, **prefix 예측에서 유도되는 fast-memory 내부 목적과는 다른 목적을 최적화한다**는 것이다. 이 구분을 바탕으로 제곱오차 회귀 목적과 음의 내적 목적에 대해 정규화된 1차 갱신을 유도한다.

회귀 계열은 scalar NLMS를 쓰는 Falcon-1, value 열마다 다른 gain을 쓰는 Falcon-2, 최근 창을 mini-batch로 쓰는 Falcon-3이다. 뒤에 `A`가 붙은 Falcon-1A/2A/3A는 이에 대응하는 내적 목적 변형이다. 저자들은 순차 재귀형, mask 기반 병렬형, chunk 병렬형을 연결하고 양의 decay를 수치적으로 안정되게 다루는 재정규화 방법을 제시한다. 실험 결론은 모든 지표에서 일관되게 최고라는 주장이 아니라, 선택한 변형들이 언어 모델 품질을 경쟁력 있게 유지하면서 가변 자릿수 덧셈의 길이 외삽을 개선했다는 제한된 주장이다.

### 1. 서론

**K002 - 문제 설정**

Transformer의 self-attention은 전역 의존성을 잘 포착하지만 길이 $N$에 대해 $\mathcal O(N^2)$의 계산·메모리 비용을 갖는다. 긴 문맥에서는 attention 행렬뿐 아니라 늘어나는 KV cache의 메모리 이동도 병목이 된다. SSM과 fast-weight 모델은 전체 과거를 보관하는 대신 고정 크기 recurrent state로 압축하여 학습 시 선형 비용과 추론 시 step당 상수 상태를 지향한다.

저자들은 긴 문맥 처리를 효율성 문제이면서 계속학습 문제로 본다. 모델은 새로운 증거를 즉시 결합해야 하지만 기존 기억을 파괴해서는 안 된다. KV cache는 빠른 기억을 외부 목록처럼 늘려 가는 반면, recurrent 모델의 상태 갱신식은 그 자체가 작은 내부 학습 알고리즘이다. 따라서 갱신에 넣는 feature와 target의 시간 관계가 목적을 결정한다.

**K003 - 정렬 차이와 기여**

표준 인덱싱에서 같은 시점 결합은 $(\phi(\mathbf k_t),\mathbf v_t)$이고, 이 논문의 다음 잠재표현 정렬은 $(\phi(\mathbf k_i),\mathbf v_{i+1})$이다. RAW 표기로 바꾸면 후자는 $(\phi(\mathbf k_{t-1}),\mathbf v_t)$가 된다. 논문은 다음 네 가지를 기여로 제시한다.

1. RAW 자기회귀 모델에서 prefix 예측 목적이 유도하는 fast-memory 학습 쌍을 명시한다.
2. 회귀 쓰기를 scalar, 열별, sliding-window로 확장하고 gain $\beta$, ridge $\lambda_t$, 실제 step size $\eta_t$의 역할을 분리한다.
3. 동일한 가소성·망각 의미를 갖는 내적 목적 변형을 유도하되, 내적 계열의 energy denominator가 곡률 보장이 아니라 write 크기 제어라는 차이를 밝힌다.
4. 재귀식을 chunk 병렬 학습이 가능한 형태로 바꾸고 언어 모델링과 산술 외삽에서 대표 변형을 평가한다.

### 2. 배경

#### 2.1 상태공간 모델

**K004 - SSM과 SSD**

연속시간 선형 상태공간 모델은 입력 $x(t)$를 압축 상태 $\mathbf h(t)$로 흡수하고 출력 $y(t)$를 읽는다. 계수는 고정·시변·데이터 의존일 수 있지만, 계수가 주어졌을 때 숨은 상태에 대한 동역학은 선형이다. Mamba 같은 선택적 SSM은 입력에 따라 $\mathbf B$, $\mathbf C$, step 간격을 만들고, Mamba-2는 전이 구조를 단순화하여 SSM recurrence와 특정 인과적 linear attention 사이의 SSD(Structured State Space Duality)를 보인다. 이 이중성은 고정 상태 추론을 유지하면서 행렬곱 중심의 chunk 병렬 학습을 가능하게 한다.

#### 2.2 선형 어텐션

**K005 - 누적 상태와 한 칸 이동한 write stream**

선형 어텐션은 kernel feature map $\phi$를 이용해 query-key 유사도를 내적으로 표현하고, 곱셈 순서를 바꾸어 키-값 외적의 합을 recurrent state에 저장한다. 양수 feature에서 분모까지 누적하면 정규화된 attention 형태가 되며, 분모를 없애면 SSM/SSD에서 흔한 내적 read가 된다.

표준 write stream은 현재 키 특징을 현재 값과 묶지만, 논문의 prefix 목적은 write feature를 한 칸 이동한다. 즉 첫 항에는 데이터 write가 없도록 $\mathbf x_1=\mathbf0$을 두고, 이후 $\mathbf x_t=\phi(\mathbf k_{t-1})$를 사용한다. 정규화 분모가 없는 경우 state 크기와 기억 시간은 명시적 decay 및 gain이 제어한다. 서명 있는 feature를 사용하는 정규화 분모는 0이나 음수가 될 수 있으므로 단순한 양의 안정화 상수만으로 안전성이 보장되지 않는다.

#### 2.3 Delta Network

**K006 - 오차 기반 상태 편집**

Delta Network는 현재 키로부터 현재 값을 복원하는 제곱오차의 gradient step으로 fast state를 갱신한다. 순수 Hebbian 누적과 달리, 현재 key 방향에서 기존 예측을 먼저 줄이고 새 target을 기록하는 rank-one edit가 발생한다. 특정 step size에서는 그 방향에 대한 직교 투영이 되지만 일반적인 step에서는 단순히 목표 방향으로 제한된 편집을 수행한다. 이 논문은 그 구조를 유지하면서 feature-target의 시간 정렬과 step 정규화를 다시 유도한다.

### 3. 자기회귀 다음 잠재표현 예측

**K007 - 내부 목적과 인과 경계**

상태 $\mathbf S$를 prefix write feature $\mathbf x_t$에서 새 목표 $\mathbf y_t$를 예측하는 온라인 선형 모델로 해석한다. 순간 목적은 예측 제곱오차와 ridge penalty의 합이다. 이 목적은 외부 언어 모델 likelihood에 별도로 더하는 supervised loss가 아니라, forward pass 안에서 fast-memory write rule을 정의하는 내부 목적이다. 학습은 이 갱신을 통해 역전파되므로 query, key, value와 gain·ridge를 만드는 느린 파라미터가 유용한 내부 학습 규칙을 익힌다.

RAW에서는 토큰 $t$를 본 후 $\mathbf S_t$를 갱신하고 그 상태를 읽어 $t+1$을 예측한다. fast-memory 자체가 $\mathbf y_t$를 맞히기 위해 사용한 예측은 갱신 전 상태 $\mathbf S_{t-1}$에 기반하지만, 모델의 시점 $t$ 출력은 갱신 후 상태 $\mathbf S_t$에 기반한다. 두 양을 혼동하면 인덱스가 뒤섞인다. 경계에서는 $\mathbf x_1=\mathbf0$뿐 아니라 $\eta_1=0$을 두어, 이전 segment에서 전달된 state가 데이터 write도 없이 ridge 때문에 감소하는 것을 막는다.

**K008 - 온라인 경사하강과 국소 안정성**

저자들은 목적의 local smoothness가 $L_t=\lVert\mathbf x_t\rVert_2^2+\lambda_t$임을 이용해 $\eta_t=\beta_t/(L_t+\varepsilon)$를 선택한다. $0<\beta_t<2$이고 clamp가 개입하지 않으면 한 step 뒤의 **같은 순간 목적**이 감소한다. 이 보장은 시점마다 달라지는 누적 온라인 손실이나 외부 autoregressive 학습 목적이 단조 감소한다는 뜻은 아니다. 분모가 0인 퇴화 경우에는 gradient도 0이므로 update를 no-op으로 정의한다.

**K009 - 기존 Delta rule과의 관계**

회귀 식에 $\mathbf x_t=\phi(\mathbf k_{t-1})$, $\mathbf y_t=\mathbf v_t$를 넣으면 Delta Network와 같은 형태를 얻되 key가 한 칸 이동한다. 다시 $\mathbf k_t$를 쓰면 기존 unshifted Delta rule이 된다. 회귀 계열에서 feature energy는 Hessian의 local smoothness와 직접 연결된다. 반면 내적 목적의 energy normalization은 수학적 곡률 조건이 아니라 additive write의 크기를 안정화하는 장치다.

### 4. Falcon 계열

#### 4.1 계열의 공통 의미

**K010 - 이름과 제어 변수**

모든 변형은 $\mathbf x_t=\phi(\mathbf k_{t-1})$, $\mathbf y_t=\mathbf v_t$를 사용하고 갱신한 상태에서 $\mathbf o_t=\mathbf S_t^\top\phi(\mathbf q_t)$를 읽는다. 숫자 `1/2/3`은 각각 scalar 동역학, value 열별 동역학, sliding-window 동역학을 뜻한다. 접미사 `A`는 squared-error 회귀 대신 음의 내적 목적을 사용한다는 뜻이다.

- $\beta_t$: 무차원 gain이며 학습할 가소성 제어다.
- $\lambda_t$: 실제 recurrence에 들어가는 ridge/shrinkage 계수다.
- $\eta_t$: normalization statistic을 반영한 실제 step size다.
- $\alpha_t=\eta_t\lambda_t$: 유도된 decay fraction이다.
- $\gamma_t=1-\alpha_t$: 이전 상태가 남는 carry다.

#### 4.2 Scaling과 정규화

**K011 - RMSNorm과 양의 decay**

fast-weight read와 write는 query/key norm에 직접 민감하다. 논문은 일반적으로 query와 key projection에 RMSNorm을 적용하고 value normalization은 기본적으로 끈다. RMSNorm 뒤 벡터의 제곱 norm은 대략 feature 차원 크기가 되므로 mixed precision에서 $\ell_2$ 단위 norm보다 좌표 크기를 지나치게 작게 만들지 않는다.

구현은 경우에 따라 무차원 base ridge $\bar\lambda_t$를 local energy $E_t$와 곱해 실제 $\lambda_t$를 만든다. 이때 $\eta$, decay fraction, rank-one edit를 같은 scale에 맞출 수 있다. 병렬 unroll에서 $\log\gamma_t$를 계산하려면 $\gamma_t>0$이어야 하므로 $\alpha_t$를 $1-\varepsilon_\gamma$ 아래로 clamp한다. clamp가 활성화되면 원래 $\lambda_t$에 대한 정확한 gradient step이 아니라 유효 계수 $\tilde\lambda_t=\alpha_t/\eta_t$를 쓰는 안전한 대체 recurrence로 해석해야 한다.

#### 4.3 회귀 계열: Falcon-1과 Falcon-2

**K012 - Falcon-1**

Falcon-1은 모든 value channel이 같은 scalar $\eta_t$를 공유하는 NLMS-stabilized ridge update다. residual $\mathbf r_t=\mathbf y_t-\mathbf S_{t-1}^\top\mathbf x_t$가 크면 새 target에 맞추어 해당 feature 방향을 크게 고치고, ridge 항은 전체 state를 줄여 명시적 망각을 준다. 같은 state를 읽는 여러 output 열의 변화율이 공유되기 때문에 병렬 구현에서 하나의 triangular system을 여러 right-hand side에 재사용할 수 있다.

**K013 - Falcon-2**

Falcon-2는 $d_v$개의 value 열마다 gain $\beta_{j,t}$와 실제 step $\eta_{j,t}$를 둔다. 제곱오차가 열별로 분리되므로 각 열을 독립 scalar update로 볼 수 있으며, 각 $\beta_{j,t}$가 $(0,2)$에 있으면 unclamped update의 국소 하강 논리를 열별로 적용할 수 있다. 표현력은 커지지만 chunk마다 value 열별 triangular system을 구성해야 해 Falcon-1보다 rate-dependent system build 비용이 크다. 저자들은 공통 Gram matrix와 batched WY 표현을 사용하고, 두 residual 경로를 합쳐 forward의 triangular solve 한 번을 줄인다.

#### 4.4 내적 계열: Falcon-1A와 Falcon-2A

**K014 - additive write와 energy-normalized gain**

음의 내적 목적은 state의 예측과 target이 같은 방향이 되도록 한다. ridge가 0이면 목적에는 유한한 최소점이 없고 gradient step은 단순 additive Hebbian write가 된다. Falcon-1A는 scalar gain, Falcon-2A는 value 열별 gain을 쓴다. 회귀 loss의 Hessian에는 $\lVert\mathbf x_t\rVert^2$가 들어가지만 내적 목적의 Hessian은 ridge가 있을 때 $\lambda_t\mathbf I$뿐이다. 그럼에도 저자들이 feature energy를 denominator에 남겨 둔 것은 curvature matching이 아니라 write 폭주를 막고 $\lambda_t\to0$에서도 의미 있는 scale을 주기 위해서다.

#### 4.5 Sliding-window 회귀: Falcon-3

**K015 - 최근 $B$개를 이용하는 제한된 리허설**

Falcon-3는 시점마다 최대 $B$개의 인과적 쌍을 활성 창 $\mathcal I_t$에 두고, 갱신 전 state에서 계산한 모든 residual의 평균으로 한 번의 mini-batch gradient step을 수행한다. 합이 아니라 평균을 쓰므로 nominal window $B$가 커졌다는 이유만으로 주입량과 decay가 선형 증가하지 않는다. step size denominator에는 창 평균 covariance의 최대 고윳값 $\mu_t^{(B)}$를 사용한다. $d_x\times d_x$ covariance를 직접 만들 필요 없이 작은 $B_t\times B_t$ Gram matrix에서 이 값을 구하거나 power iteration으로 근사할 수 있다.

길이 축 병렬화를 위해 각 창을 폭 $B$로 zero-padding하면 recurrence가 고정 rank-$B$ affine update가 된다. 저자들은 ParallelFlow의 `tensorInv`로 chunk 내부 low-rank interaction을 풀고, chunk 경계의 affine map을 순차 또는 associative scan으로 전달한다. 다른 segment에서 정확히 이어 처리하려면 state만으로는 부족하고 마지막 $B-1$개의 인과 쌍도 함께 전달해야 한다.

#### 4.6 Sliding-window 내적: Falcon-3A와 mask 병렬형

**K016 - sliding additive memory**

Falcon-3A는 같은 창을 쓰되 residual regression이 아니라 창 평균 cross-covariance를 state에 더한다. step size는 창의 평균 write energy로 정규화한다. $B=1$이면 scalar non-sliding Falcon-1A가 되고, ridge가 0이면 순수 additive write가 된다.

이 recurrence를 시간축으로 풀면 초기 state가 decay되는 경로와 과거 각 value가 query-key 내적 및 구조화 mask를 통해 출력으로 오는 경로로 분해된다. 따라서 recurrent 계산과 masked linear-attention 계산이 동등하며, chunk별 log-space decay와 인과 mask를 이용해 시퀀스 방향의 벡터화가 가능하다. 여기서 mask는 단순한 local attention window가 아니라, 각 과거 write가 여러 sliding update에 재사용되고 이후 decay를 거쳐 현재에 미치는 총 계수를 담는다.

### 5. 실험

#### 5.1 실험 설계

**K017 - 비교 범위**

언어 모델은 124M-130M 파라미터 규모이며 FineWeb-Edu에서 sequence length 1,024, global batch 480, 100,000 optimization step으로 학습했다. 총 처리량은 약 49.2B tokens로, 표 caption의 50B-token budget은 반올림된 표현이다. Transformer baseline은 RoPE와 SwiGLU를 쓰는 LLaMA형이고, recurrent baseline은 RetNet/LightningAttn, Mamba-2, DeltaNet, Gated DeltaNet이다.

실험은 Falcon-1A와 Falcon-3A를 중심으로 하고 Falcon-1.3을 회귀 ablation으로 포함한다. 정의된 전체 계열을 모두 비교한 것이 아니다. 특히 Falcon-2, Falcon-2A, sliding regression Falcon-3은 main table에서 별도 benchmark하지 않았다. 지표는 held-out perplexity와 8개 downstream task의 zero-shot/one-shot accuracy이며, 산술 실험은 별도의 통제된 기억·외삽 진단이다.

#### 5.2 언어 모델링 결과

**K018 - 경쟁력은 보이지만 일률적 우위는 아님**

FineWeb-Edu perplexity에서는 Falcon-1.3이 17.10으로 전체 최저이고, 가장 강한 recurrent baseline인 Gated DeltaNet은 17.32, 평가된 내적 계열 중 가장 좋은 Falcon-1A.3은 17.40이다. 그러나 WikiText 계열과 LAMBADA 열에서는 Gated DeltaNet이 각각 30.99와 46.70으로 가장 좋은 recurrent 값을 보인다. 따라서 제안 방법이 모든 corpus perplexity에서 이겼다고 읽어서는 안 된다.

8개 downstream task의 평균에서 Falcon-1A.2는 zero-shot 49.30으로 표에 실린 모델 중 최고다. one-shot에서는 Transformer가 49.67로 전체 최고이고, Falcon-1.3은 49.54로 recurrent 모델 중 최고다. 개별 task의 최상위 모델은 달라서 평균 차이가 작을 때 단일 숫자만으로 일반적 우위를 단정하기 어렵다. scalar inner-product ablation 안에서는 QK-RMSNorm이 QK-$\ell_2$ normalization보다 FineWeb-Edu perplexity를 개선했고, 문맥 조건부 $\eta$가 대응하는 문맥 조건부 $\beta$ 설정보다 평균 accuracy를 높였다.

#### 5.3 가변 자릿수 덧셈

**K019 - 길이 외삽 진단**

입력은 같은 자릿수의 두 수를 더하는 prompt이고, 출력은 합의 자릿수를 역순으로 생성한다. 낮은 자리부터 내보내므로 carry 전달과 순차 기억을 제어된 방식으로 시험할 수 있다. 학습 자릿수는 1-32에서 균등 표집하고 target suffix에만 next-token loss를 준다. 표의 OOD 수치는 33-48자리 target suffix에 대한 **teacher-forced accuracy** 평균이다.

Falcon-3A.3이 평균 87.2로 가장 높고 Falcon-1A.3이 85.9, RetNet/LightningAttn이 82.9, Transformer가 65.8이다. 48자리 accuracy는 Falcon-3A.3과 Falcon-1A.3이 각각 69.0, Transformer가 49.0이다. 저자도 이를 논문의 주된 결과가 아니라 fast-state의 저장과 carry propagation을 분리해 보는 보조 증거로 규정한다. Teacher forcing을 사용했으므로 자유 생성 전체 시퀀스 정확도와 동일한 지표로 해석해서는 안 된다.

### 6. 관련 연구

**K020 - 연구 계보와 차별점**

저자들은 효율적 시퀀스 모델 계보를 linear attention, Performer, Hyena, RetNet, RWKV, S4, Mamba와 SSD로 연결한다. 기존 연구가 subquadratic 계산, hardware utilization, 선택적 동역학에 초점을 두었다면 이 논문은 state write를 유도하는 **내부 목적과 시간 정렬**을 전면에 둔다.

Fast Weight Programmer와 Delta Network 계보에서는 outer-product memory와 value reconstruction error 기반 edit를 이어받고, Gated DeltaNet과는 explicit state decay라는 공통점이 있다. 적응 필터 관점에서는 LMS/NLMS의 scale-robust first-order update를 가져오며, exact cumulative ridge를 계산하는 RLS는 더 비싸고 병렬화하기 어렵다는 비교 기준으로 사용한다. Test-Time Training, MesaNet, Titans, ATLAS와는 forward pass 내부에서 state를 최적화한다는 관점을 공유하지만, Falcon은 고정 크기 선형 state, 한 번의 인과적 갱신, next-latent 정렬, SSD식 chunk parallelism으로 범위를 제한한다.

### 7. 결론

**K021 - 결론의 정확한 강도**

논문은 recurrent sequence model을 명시적 fast-memory 목적을 갖는 온라인 계속학습기로 재해석한다. regression과 inner-product 두 목적, scalar·열별·sliding-window 세 시간/채널 구조를 조합하여 여섯 변형을 하나의 표기 아래 둔다. 이 구성은 시간 정렬, 새 정보 수용 정도, 전역 shrinkage, 최근 예제 재사용을 독립적으로 논의하게 해 준다.

실증적으로 입증된 범위는 대표 scalar 회귀 변형과 scalar/sliding inner-product 변형이 약 130M 규모 언어 모델링에서 경쟁력을 유지하고, 선택된 내적 변형이 통제된 덧셈 과제에서 길이 외삽을 개선했다는 것이다. 모든 Falcon 변형의 우위, 대규모 모델로의 scaling, 실제 장문 자연어에서의 우월성까지 입증한 것은 아니다.

## 부록 해설

### 부록 A. 추가 배경

**K022 - RLS, 1차 online ridge, SSM 이산화**

RLS(Recursive Least Squares)는 고정 ridge와 0 prior mean 조건에서 누적 ridge regression의 정확한 해를 matrix inversion lemma로 갱신한다. step당 비용은 $\mathcal O(d_x^2+d_xd_v)$이며 inverse covariance를 유지해야 한다. 논문의 Falcon recurrence는 시변 $\lambda_t$를 쓰는 1차 근사이므로 RLS의 exact solution과 같다고 주장하지 않는다. 부록은 비교를 위해 batch size 1의 online ridge pseudocode도 제시한다.

SSM 이산화 부분은 연속시간 선형계를 zero-order hold로 정확히 이산화하는 식과, $\lVert\Delta_t\mathbf A_t\rVert$가 작을 때의 1차 근사를 구분한다. 이 설명은 selective SSM의 recurrence가 어디서 오는지 배경을 제공하지만 Falcon을 특정 연속시간 물리계의 정확한 이산화라고 주장하지는 않는다.

### 부록 B. 실험 설정

**K023 - 재현에 필요한 주요 조건**

모든 언어 모델 run은 bfloat16, AdamW, tied input/output embedding, Pre-Norm RMSNorm, bias 없음, dropout 없음으로 수행했다. $\mu$P 방식 폭 scaling, base learning rate $10^{-3}$의 cosine decay, warmup 2,000 step, AdamW 계수 $(0.9,0.95)$, weight decay 0.1, gradient clipping 1.0을 사용했다. 각 run은 NVIDIA H100 또는 H200 GPU 4개가 있는 단일 node에서 수행했다. 이 hardware 조건은 재현 비용과 mixed-precision 안정성 판단에 중요하다.

### 부록 C. 구현 세부사항

**K024 - scaling, signed denominator, gate 의미**

정규화된 linear-attention 변형은 numerator state와 denominator state에 같은 carry와 write gain을 적용한다. nonnegative feature에서는 양의 carry clamp가 attention-like denominator를 유지하는 데 도움이 되지만 signed feature에서는 denominator가 여전히 0 또는 음수가 될 수 있다. 논문의 signed-feature 기본 해석이 denominator-free인 이유다.

Falcon의 $\beta$는 dimensionless plasticity gain이고 $\eta$는 정규화된 실제 step이다. Gated DeltaNet의 독립 gate $g_t$와 달리 Falcon의 carry $\gamma_t$는 $\eta_t\lambda_t$에서 유도된다. 따라서 두 방식 모두 state decay를 제공하지만 Falcon은 이를 내부 ridge 목적과 묶는다.

**K025 - RAW/RBW와 segment 경계**

RBW(read-before-write)는 이전 state를 읽어 현재 token을 예측한 뒤 write하고, RAW는 현재 token을 본 뒤 write하여 다음 token 예측에 사용한다. `shifted/unshifted`는 이 read/write 순서와 별개의 축이다. 원 논문의 2x2 그림은 두 축을 나눠 보지 않으면 같은 식을 다른 인과 의미로 잘못 해석할 수 있음을 보여 준다.

$\mathbf x_1=0$, $\eta_1=0$이라는 feature-space sentinel은 새 시퀀스뿐 아니라 segment를 이어 처리할 때 중요하다. Falcon-3/3A는 정확한 continuation을 위해 최종 행렬 state와 마지막 $B-1$쌍을 함께 보존해야 한다. state만 저장하면 새 segment의 첫 창에서 필요한 rehearsal example이 사라진다.

**K026 - 수치 안정성과 구현 주의**

양의 decay product는 긴 시퀀스에서 underflow/overflow가 나기 쉬우므로 chunk 내부에서 `log1p(-alpha)`의 누적합을 fp32로 계산하고 local scale을 복원한다. 고정된 attention stabilizer가 있는 정규화 ratio는 state와 normalizer를 재정규화한 뒤 stabilizer까지 같은 scale로 다루지 않으면 정확한 동등성이 깨질 수 있다. denominator-free recurrence는 이 ratio caveat의 영향을 받지 않는다.

부록은 optional short convolution을 causal하게 사용해야 하며 shift 전에 feature를 만들었다면 segment 경계 state도 일치시켜야 한다고 강조한다. 또한 $\beta>1$에서 rank-one 방향의 계수가 음수로 바뀔 수 있으므로 local descent 범위 안에 있다고 해서 항상 단순한 convex averaging으로 해석할 수는 없다.

### 부록 D. Falcon-3A mask와 backward pass

**K027 - 구조화 mask와 미분 경로**

Falcon-3A의 mask coefficient는 한 write가 포함되는 sliding window, 그 시점의 $\eta/B_t$, 이후 시점까지의 carry product를 모두 합친다. log-space 누적 decay와 chunk-local renormalization을 이용하면 $L\times L$ dense mask를 그대로 만들지 않고 chunk 단위로 평가할 수 있다. backward는 output/state 경로뿐 아니라 normalized step size의 $\beta$, $\lambda$, energy statistic과 clamp mask를 거슬러 미분한다. clamp된 위치에서는 min 연산을 통한 decay-gradient가 0이 되는 구현 선택을 명시한다.

### 부록 E. DeltaNet WY 병렬화

**K028 - recurrence를 triangular solve로 바꾸기**

rank-one affine recurrence를 chunk 안에서 WY 형태로 묶으면 과거 edit 사이의 interaction이 strictly lower-triangular Gram 구조로 나타난다. forward는 한 개의 residual triangular solve로 history projection과 value injection을 결합할 수 있고, backward는 이 solve와 matrix products를 역방향으로 미분한다. 이 동등성은 $\lambda=0$의 기본 rank-one 경우에서 명시적으로 유도되며, ridge가 있을 때는 positive-decay 재정규화로 같은 kernel을 재사용한다.

### 부록 F. Falcon-2 병렬 구현

**K029 - 열별 rate와 shared geometry**

Falcon-2의 각 value 열은 다른 $\eta_{t,j}$와 $\gamma_{t,j}$를 갖지만 write feature의 Gram geometry는 공유한다. 따라서 key Gram matrix는 한 번 계산하고, 열마다 달라지는 lower-triangular system은 batched solve로 처리한다. residual 두 경로를 하나의 right-hand side로 합치는 one-TriSolve reduction은 recurrence나 asymptotic complexity를 바꾸지 않으면서 forward kernel 호출을 줄인다. 다만 열별 system build 자체는 여전히 $d_v$에 비례한다.

### 부록 G. 공유 동역학 Falcon

**K030 - Falcon-1의 계산상 장점**

모든 value 열이 scalar rate를 공유하면 열별 triangular matrix를 따로 만들 필요가 없다. Falcon-1은 하나의 $C\times C$ system을 구성·factorize하고 $d_v$개의 right-hand side를 한 번에 푼다. solve의 산술량은 여전히 $\mathcal O(d_vC^2)$이지만, rate-dependent system build가 $\mathcal O(d_vC^2)$에서 $\mathcal O(C^2)$로 줄어 GPU에서 더 다루기 좋은 형태가 된다. 이 차이는 표현력과 kernel 효율 사이의 명시적 trade-off다.

### 부록 H. Falcon-3 ParallelFlow 구현

**K031 - rank-$B$ affine flow**

Falcon-3의 sliding regression은 폭 $B$로 padding한 뒤 매 시점 rank-$B$인 affine recurrence가 된다. `tensorInv`는 시간과 rank를 함께 펼친 구조화 causal system에 두 right-hand side를 적용해 local propagator와 value injection을 얻는다. 같은 시점의 rank component끼리는 solve 안에서 상호작용하지 않아 모든 residual이 갱신 전 state에서 평가되는 mini-batch 의미를 보존한다.

각 chunk는 $\mathbf S_{\mathrm{out}}=\mathbf M^{(k)}\mathbf S_{\mathrm{in}}+\mathbf b^{(k)}$라는 affine map으로 요약되고, 이 map의 합성은 associative하다. 그러므로 경계 전달을 단순 순차 loop 또는 associative scan으로 구현할 수 있다. 저자들은 작은 창, 예를 들어 $B=4$에서는 rank overhead가 제한적이며 full $\mathcal O(L^2)$ attention보다 저렴하다고 설명한다. 이는 discrete recurrence 수준에서의 정확한 변환이며, 실제 wall-clock 우위는 별도의 benchmark가 필요하다.

## 핵심 수식과 직관

### E1. 인과적 다음 잠재표현 학습 쌍

$$
\mathbf x_t=\phi(\mathbf k_{t-1})\in\mathbb R^{d_x},\qquad
\mathbf y_t=\mathbf v_t\in\mathbb R^{d_v},\qquad
\mathbf S_t\in\mathbb R^{d_x\times d_v}.
$$

- $\phi$: raw key를 fast-memory write space로 보내는 feature map이다.
- $\mathbf S^\top\mathbf x$: $d_x$차원 feature를 $d_v$차원 target으로 예측한다.
- 핵심은 $t$의 target을 $t-1$ key feature와 묶는 한 칸 이동이다.

### E2. 순간 ridge-regression 목적

$$
\ell_t(\mathbf S)
=\frac12\lVert\mathbf S^\top\mathbf x_t-\mathbf y_t\rVert_2^2
+\frac{\lambda_t}{2}\lVert\mathbf S\rVert_F^2,
\qquad \lambda_t\ge0.
$$

첫 항은 fast memory의 현재 예측 오차이고 둘째 항은 state 전체를 줄이는 ridge penalty다. 이 식은 outer language-model loss가 아니라 write rule을 정의하는 내부 목적이다.

### E3. Falcon-1의 online gradient update

$$
\mathbf r_t=\mathbf y_t-\mathbf S_{t-1}^\top\mathbf x_t,
$$

$$
\mathbf S_t
=(1-\eta_t\lambda_t)\mathbf S_{t-1}
+\eta_t\mathbf x_t\mathbf r_t^\top.
$$

- $\mathbf r_t\in\mathbb R^{d_v}$이므로 $\mathbf x_t\mathbf r_t^\top$은 state와 같은 $d_x\times d_v$ rank-one 행렬이다.
- 첫 경로는 global shrinkage, 둘째 경로는 current feature 방향의 error correction이다.

### E4. NLMS step size와 국소 하강

$$
\eta_t=\frac{\beta_t}{\lVert\mathbf x_t\rVert_2^2+\lambda_t+\varepsilon},
\qquad 0<\beta_t<2.
$$

분모는 회귀 목적의 local smoothness scale에 안정화 상수를 더한 것이다. $L$-smooth 함수에 $0<\eta<2/L$인 gradient step을 적용하면

$$
f(\mathbf S^+)\le f(\mathbf S)
-\frac{\eta(2-\eta L)}{2}\lVert\nabla f(\mathbf S)\rVert_F^2
$$

가 성립한다. 이 결과는 해당 시점의 동일한 $f$에 대한 one-step descent이며 전체 학습 안정성 정리가 아니다.

### E5. Falcon-2의 열별 update

$$
\eta_{j,t}=\frac{\beta_{j,t}}
{\lVert\mathbf x_t\rVert_2^2+\lambda_t+\varepsilon},
\qquad \boldsymbol\eta_t\in\mathbb R^{d_v},
$$

$$
\mathbf S_t
=\mathbf S_{t-1}
\left(\mathbf I_{d_v}-\lambda_t\operatorname{Diag}(\boldsymbol\eta_t)\right)
+\mathbf x_t(\boldsymbol\eta_t\odot\mathbf r_t)^\top.
$$

오른쪽 곱의 diagonal matrix가 state 열마다 다른 decay를 주고, Hadamard product가 residual 열마다 다른 correction 크기를 준다.

### E6. 내적 목적과 Falcon-1A/2A

$$
\ell_t^{\mathrm{ip}}(\mathbf S)
=-\langle\mathbf S^\top\mathbf x_t,\mathbf y_t\rangle
+\frac{\lambda_t}{2}\lVert\mathbf S\rVert_F^2.
$$

$$
\mathbf S_t^{\text{Falcon-1A}}
=(1-\eta_t\lambda_t)\mathbf S_{t-1}
+\eta_t\mathbf x_t\mathbf y_t^\top,
$$

$$
\mathbf S_t^{\text{Falcon-2A}}
=\mathbf S_{t-1}
\left(\mathbf I_{d_v}-\lambda_t\operatorname{Diag}(\boldsymbol\eta_t)\right)
+\mathbf x_t(\boldsymbol\eta_t\odot\mathbf y_t)^\top.
$$

residual이 없다는 점이 회귀 계열과의 핵심 차이다. $\lambda=0$이면 순수 additive write이며 목적 자체는 아래로 유계가 아니다.

### E7. Falcon-3의 sliding regression

$\mathcal I_t$를 최근 최대 $B$개 인과 쌍의 index 집합, $B_t=|\mathcal I_t|$라 하면

$$
\bar{\mathbf C}_t^{(B)}
=\frac1{B_t}\sum_{j\in\mathcal I_t}\mathbf x_j\mathbf x_j^\top
\in\mathbb R^{d_x\times d_x},
$$

$$
\bar{\mathbf N}_t^{(B)}
=\frac1{B_t}\sum_{j\in\mathcal I_t}\mathbf x_j\mathbf v_j^\top
\in\mathbb R^{d_x\times d_v}.
$$

$$
\mathbf S_t
=\left(\mathbf I-\eta_t(\bar{\mathbf C}_t^{(B)}+\lambda_t\mathbf I)\right)\mathbf S_{t-1}
+\eta_t\bar{\mathbf N}_t^{(B)}.
$$

동일한 식을 residual 평균으로 쓰면 모든 residual이 $\mathbf S_{t-1}$에서 함께 평가된 mini-batch step이라는 사실이 드러난다.

### E8. 창의 smoothness에 맞춘 Falcon-3 step

$\mathbf X_t\in\mathbb R^{d_x\times B_t}$가 창의 write feature를 열로 쌓은 행렬이면

$$
\mu_t^{(B)}
=\lambda_{\max}(\bar{\mathbf C}_t^{(B)})
=\frac{\lambda_{\max}(\mathbf X_t^\top\mathbf X_t)}{B_t},
$$

$$
\eta_t=\frac{\beta_t}{\mu_t^{(B)}+\lambda_t+\varepsilon}.
$$

큰 $d_x\times d_x$ 행렬 대신 작은 Gram matrix $\mathbf X_t^\top\mathbf X_t\in\mathbb R^{B_t\times B_t}$를 사용할 수 있다. 창의 합이 아닌 평균을 쓰기 때문에 $B$ 자체가 update scale을 선형 증폭시키지 않는다.

### E9. Falcon-3A의 창 평균 내적 write

$$
\bar E_t^{(B)}=\frac1{B_t}\sum_{j\in\mathcal I_t}\lVert\mathbf x_j\rVert_2^2,
\qquad
\eta_t=\frac{\beta_t}{\bar E_t^{(B)}+\lambda_t+\varepsilon},
$$

$$
\mathbf S_t=(1-\eta_t\lambda_t)\mathbf S_{t-1}
+\eta_t\bar{\mathbf N}_t^{(B)}.
$$

$\bar E_t^{(B)}$는 inner-product 목적의 Hessian smoothness가 아니라 additive write의 energy normalizer다.

### E10. 양의 decay clamp

$$
\alpha_t^{\mathrm{raw}}=\eta_t\lambda_t,
\qquad
\alpha_t=\min(\alpha_t^{\mathrm{raw}},1-\varepsilon_\gamma),
\qquad
\gamma_t=1-\alpha_t\in[\varepsilon_\gamma,1].
$$

이 식은 $\log\gamma_t=\operatorname{log1p}(-\alpha_t)$를 안전하게 계산하도록 한다. clamp가 켜지면 이 recurrence는 원래 ridge 계수의 정확한 gradient step이 아니라 양의 carry를 보장하는 surrogate다.

### E11. Falcon-3A의 masked parallel form

적절한 decay/window coefficient 행렬 $\mathbf M\in\mathbb R^{L\times L}$와 누적 carry $\boldsymbol\delta$를 쓰면

$$
\mathbf O
=\operatorname{Diag}(\boldsymbol\delta)\mathbf Q\mathbf S_0
+\left(\mathbf Q\mathbf X^\top\odot\mathbf M\right)\mathbf V.
$$

- $\mathbf Q,\mathbf X\in\mathbb R^{L\times d_x}$
- $\mathbf V,\mathbf O\in\mathbb R^{L\times d_v}$
- $\mathbf M$은 causal window, 각 update의 $\eta/B_t$, 이후 carry product를 함께 담는다.

이 식은 recurrent fast-weight read가 구조화된 masked attention으로도 계산될 수 있음을 보여 준다. 일반적인 고정 폭 local-attention mask와 동일하다고 단순화하면 안 된다.

## 그림 해설

| 그림 | 한국어 해설 | 읽는 핵심 |
|---|---|---|
| 그림 1 | Falcon-1, Falcon-2, Falcon-3의 한 step 비교 | 세 방법 모두 갱신 후 state를 읽는다. 차이는 scalar rate, 열별 rate, 최근 창 residual 평균이다. |
| 그림 2 | 분모 없는 linear attention의 재귀·전체 병렬·chunk 병렬 동등성 | 단순 outer-product 누적도 causal mask와 chunk state propagation으로 바꿀 수 있다는 배경 그림이다. |
| 그림 3 | same-step 목적과 next-latent 목적, scalar/열별/sliding 갱신의 개념도 | same-step이 비인과적인 것이 아니라 다른 내부 목적이라는 점, $\phi(\mathbf k_{t-1})\to\mathbf v_t$ 정렬이 Falcon의 기준이라는 점을 본다. |
| 그림 4 | Falcon-1 rank-one kernel의 recurrent, WY parallel, chunk-wise 표현 | 같은 recurrence를 triangular solve로 재배열한 것이며, 별도의 근사 모델 세 개가 아니다. |
| 그림 5 | Falcon-2와 batched WY kernel의 세 표현 | Gram geometry는 공유하지만 value 열마다 learning-rate system이 달라 batched solve가 필요하다. |
| 그림 6 | Falcon-1A, 2A, 3A 비교 | residual 대신 target을 직접 쓰는 inner-product 계열에서 scalar, 열별, sliding 차이를 보여 준다. |
| 그림 7 | Falcon-1A의 recurrent·masked·chunk 표현 | additive state recurrence가 causal masked attention으로 unroll되는 과정을 본다. |
| 그림 8 | Falcon-2A의 세 표현 | decay와 write coefficient가 value 열별이므로 mask/decay도 채널 의존적이다. |
| 그림 9 | Falcon-3의 recurrent·ParallelFlow·chunk 표현 | sliding residual update를 rank-$B$ driver로 묶고 chunk boundary의 affine state를 전달한다. |
| 그림 10 | Falcon-3A의 recurrent·masked·chunk 표현 | 과거 한 쌍이 여러 window update에 반복 참여하는 계수를 구조화 mask에 모은다. 원문 논리상 4절 그림이지만 LaTeX float 배치로 PDF 31쪽의 참고문헌 뒤에 나타난다. |
| 그림 11 | RAW/RBW와 shifted/unshifted의 2축 시간 규칙 | read/write 순서와 feature-target index 이동은 서로 다른 선택이다. 논문의 선택은 RAW+shifted다. |

그림 2와 4-10은 주로 **수학적으로 같은 계산의 세 구현 관점**을 설명한다. 시각적으로 비슷하다는 사실을 세 가지 독립 실험의 일치로 오해하면 안 된다. 그림 11의 아래 2x2 칸은 실험 수치를 제공하는 표가 아니라 timing convention을 분리하기 위한 설계도다.

## 표 결과 해설

### 표 1. 약 130M 모델의 perplexity

낮을수록 좋다.

| 모델 | Wiki | LMB. | FineEdu |
|---|---:|---:|---:|
| Transformer 124M | 33.25 | 47.43 | 17.38 |
| RetNet/LightningAttn 130M | 36.86 | 65.16 | 18.79 |
| Mamba-2 130M | 34.53 | 48.74 | 17.70 |
| DeltaNet 130M | 34.19 | 52.84 | 17.84 |
| Gated DeltaNet 130M | **30.99** | **46.70** | 17.32 |
| Falcon-1A.3 130M | 34.02 | 49.84 | 17.40 |
| Falcon-1.3 130M | 33.00 | 48.70 | **17.10** |

해석: FineEdu에서는 Falcon-1.3이 가장 좋지만 Wiki와 LMB.에서는 Gated DeltaNet이 recurrent 최상위다. Falcon-1.3의 FineEdu 이득은 Gated DeltaNet 대비 0.22 perplexity이고, Transformer 대비 0.28이다. 다른 corpus의 순위가 다르므로 전반적인 지배 관계는 아니다.

### 표 2. 8개 downstream task 평균

높을수록 좋다. 아래는 해석에 필요한 대표 평균이며 원 표는 PIQA, HellaSwag, WinoGrande, ARC-easy, ARC-challenge, OpenBookQA, Social IQA, SciQ를 각각 제시한다.

| 모델 | Zero-shot 평균 | One-shot 평균 |
|---|---:|---:|
| Transformer | 48.16 | **49.67** |
| Mamba-2 | 48.80 | 49.16 |
| Gated DeltaNet | 48.78 | 48.57 |
| Falcon-1A.2 | **49.30** | 49.20 |
| Falcon-3A.3 | 49.00 | 49.03 |
| Falcon-1.3 | 49.18 | **49.54** (recurrent 중) |

해석: zero-shot 평균의 최고와 recurrent one-shot 최고가 서로 다른 Falcon 변형이다. 차이는 작고 개별 task의 우승 모델도 분산된다. 반복 seed의 분산이나 신뢰구간이 표에 없으므로 0.x point 차이를 통계적으로 확정된 우위로 해석할 수 없다.

### 표 3. 33-48자리 덧셈 길이 일반화

높을수록 좋다. `Mean`은 33-48자리 teacher-forced target-suffix accuracy 평균이다.

| 모델 | 학습 범위 validation | 33-48자리 Mean | 33자리 / 48자리 |
|---|---:|---:|---:|
| Transformer | 100.0 | 65.8 | 97.0 / 49.0 |
| RetNet/LightningAttn | 99.7 | 82.9 | 99.0 / 63.0 |
| Mamba-2 | 100.0 | 75.2 | 100.0 / 51.0 |
| Falcon-1A.1 | 100.0 | 80.6 | 100.0 / 59.0 |
| Falcon-1A.2 | 100.0 | 85.2 | 100.0 / 63.0 |
| Falcon-1A.3 | 99.8 | 85.9 | 100.0 / 69.0 |
| Falcon-3A.3 | 99.9 | **87.2** | 100.0 / 69.0 |
| Falcon-1.3 | 100.0 | 68.8 | 100.0 / 48.0 |

해석: 같은 계열 안에서도 regression Falcon-1.3은 언어 모델 perplexity와 달리 산술 외삽에서 약하다. 개선은 `Falcon`이라는 이름 전체가 아니라 평가된 inner-product 설정, 정규화, sliding rehearsal의 조합에 연관된다. Falcon-3A.3은 Transformer보다 Mean 21.4 point 높지만 free-running exact-match 결과가 아니라 teacher-forced token accuracy다.

### 표 4. chunk당 이론 복잡도

| 계산 | Falcon-2 | Falcon-1 |
|---|---:|---:|
| Gram matrix | $\mathcal O(dC^2)$ | $\mathcal O(dC^2)$ |
| rate-dependent system build | $\mathcal O(d_vC^2)$ | $\mathcal O(C^2)$ |
| forward residual triangular solve | $\mathcal O(d_vC^2)$ | $\mathcal O(d_vC^2)$ |
| state update / output projection | $\mathcal O(dd_vC)$ | $\mathcal O(dd_vC)$ |

해석: Falcon-1의 장점은 solve의 big-O를 없애는 것이 아니라, $d_v$개의 다른 system을 구성·factorize하는 비용을 하나의 shared system으로 줄이고 multi-RHS solve를 가능하게 하는 데 있다. 실제 속도·메모리 이득은 GPU kernel, $C,d,d_v$, batch size에 따라 달라지며 논문의 main results에는 wall-clock 표가 없다.

## 한계와 주의점

원문에는 독립된 `Limitations` 절이 없다. 아래 첫 목록은 본문과 부록에서 저자들이 직접 한정한 내용을 모은 것이고, 둘째 목록은 공개된 v1만으로 확인 가능한 증거 범위를 번역자가 별도로 점검한 것이다.

### 저자가 명시적으로 제한한 주장

1. **국소 하강 보장만 있음:** per-step descent lemma는 그 시점의 unclamped 순간 목적에 대한 결과다. 누적 online loss나 outer autoregressive objective가 단조 감소한다는 보장이 아니다.
2. **clamp는 surrogate:** positive-decay clamp가 활성화되면 원래 ridge 계수에 대한 정확한 gradient update가 아니다.
3. **signed normalization 위험:** signed feature에서 정규화 분모는 0 또는 음수가 될 수 있다. 양의 stabilizer 하나만으로 안전하지 않다.
4. **대표 변형만 평가:** Falcon-2, Falcon-2A, Falcon-3은 정의되지만 main table에서 독립 평가되지 않는다.
5. **산술은 보조 증거:** variable-digit addition은 저장·carry를 보는 통제 실험이며 논문의 주 결과로 제시되지 않는다.
6. **sliding continuation state:** Falcon-3/3A를 segment 경계에서 정확히 이어 가려면 행렬 state 외에 최근 $B-1$개의 쌍이 필요하다.

### 번역자 검토에 따른 추가 한계

아래는 저자의 명시적 문장을 번역한 것이 아니라, 공개된 v1의 증거 범위를 바탕으로 한 검토 의견이다.

1. **규모와 domain:** 언어 모델 실험은 약 130M 파라미터와 FineWeb-Edu 중심이다. 수십억 파라미터 모델, 실제 장문 검색·코딩·멀티모달 과제로 일반화되는지는 아직 알 수 없다.
2. **효율 실측 부족:** chunk 병렬 알고리즘과 asymptotic complexity는 상세하지만, 표준화된 throughput, latency, peak memory, kernel utilization 비교가 main table에 없다.
3. **통계 불확실성:** downstream 평균과 perplexity 표에 반복 seed의 표준편차·신뢰구간이 제시되지 않는다.
4. **teacher forcing:** 덧셈 OOD 결과는 teacher-forced suffix accuracy이므로 자기 오류가 다음 token으로 누적되는 자유 생성과 차이가 있다.
5. **비교 범위의 빈칸:** per-column 및 sliding regression 변형의 품질·속도 trade-off가 실험적으로 완결되지 않았다.
6. **paper-only 재현 정보:** 정확한 layer 수, hidden/head 구성, tokenizer, data split, 평가 harness 버전, 덧셈 표본 수가 v1 본문에 모두 명시되지는 않는다. 프로젝트 코드와 실행 configuration을 함께 고정해야 정확한 재현을 판단할 수 있다.
7. **v1 문서 교차참조 오류:** PDF 26쪽은 small/medium 결과를 “Tables 2 and ??”로 가리키지만 실제 v1 PDF와 TeX에는 small-model 표만 있고 `tab:accuracy_results_medium` label이 정의되지 않는다. medium-model 결과를 임의로 추정해서는 안 된다.
8. **날짜·소속 표기 주의:** PDF 내부 날짜 2026-03-09는 arXiv 제출일 2026-08-27과 다르며, 소속 4번 UCLA는 저자 위첨자에 연결되지 않는다. 서지 인용에는 arXiv 제출 이력을 우선하는 편이 안전하다.

## 약어 및 기술 용어 사전

| 원어·약어 | 한국어 | 이 논문에서의 의미와 역할 | 최초 등장 단위 |
|---|---|---|---|
| continual learning | 계속학습 | 고정 state가 token마다 새 예제를 받아들이면서 이전 정보를 유지하는 문제 설정 | S001 |
| temporal alignment | 시간 정렬 | write feature와 target의 시점 관계 | S001 |
| plasticity | 가소성 | gain $\beta$가 제어하는 fast-memory 변화 정도 | S001 |
| bounded rehearsal | 제한된 리허설 | 고정 폭 sliding window에서 최근 쌍을 재사용하는 방식 | S001 |
| fast weight | 빠른 가중치 | forward pass 안에서 즉시 갱신되는 행렬 state $\mathbf S_t$ | K001 |
| SSM | 상태공간 모델(State Space Model) | 긴 입력을 고정 크기 latent state로 압축하는 recurrent 모델 | K001 |
| RAW | 갱신 후 읽기(Read After Write) | token $t$를 write한 $\mathbf S_t$로 $t+1$을 예측하는 timing | K001 |
| RBW | 읽은 후 갱신(Read Before Write) | $\mathbf S_{t-1}$로 현재 위치를 읽은 뒤 state를 갱신하는 timing | K025 |
| KV cache | 키-값 캐시(Key-Value cache) | Transformer가 과거 attention 정보를 길이에 비례해 저장하는 외부 fast memory | K002 |
| linear attention | 선형 어텐션 | kernel feature와 outer-product state로 길이 이차 attention을 재배열하는 방식 | K002 |
| SSD | 구조화 상태공간 이중성(Structured State Space Duality) | 특정 SSM recurrence와 causal linear attention의 계산 동등성 | K004 |
| Delta Network | 델타 네트워크 | value reconstruction residual의 gradient로 state를 rank-one 편집하는 모델 | K006 |
| Hebbian write | 헤비안 쓰기 | feature-target outer product를 residual 없이 더하는 연관 기억 update | K006 |
| ridge regression | 릿지 회귀 | 제곱오차에 $L_2$ state penalty를 더한 내부 목적 | K007 |
| OGD | 온라인 경사하강(Online Gradient Descent) | 도착한 local example마다 한 번의 gradient step을 수행하는 방식 | K007 |
| NLMS | 정규화 최소평균제곱(Normalized Least Mean Squares) | feature energy로 LMS step을 정규화하는 적응 필터 규칙 | K008 |
| local smoothness | 국소 평활도 | 안전한 step-size 범위를 결정하는 순간 목적 gradient의 Lipschitz scale | K008 |
| RMSNorm | 제곱평균제곱근 정규화(Root Mean Square Normalization) | query/key coordinate scale을 안정화하는 정규화 | K011 |
| VNorm | 값 정규화(Value Normalization) | value vector의 선택적 normalization. 논문 기본 설정에서는 꺼짐 | K011 |
| Gram matrix | 그람 행렬 | 창 또는 chunk feature의 내적으로 만든 작은 행렬 | K013 |
| WY representation | WY 표현 | rank-one update의 연속을 triangular system과 low-rank factor로 묶는 표현 | K013 |
| TriSolve | 삼각행렬 풀이(Triangular Solve) | WY 형태에서 causal interaction을 푸는 핵심 연산 | K013 |
| inner-product objective | 내적 목적 | 예측과 target 정렬을 키우며 residual 없이 additive write를 유도하는 목적 | K014 |
| sliding window | 슬라이딩 창 | 최근 최대 $B$개 local example의 active set | K015 |
| ParallelFlow | ParallelFlow | low-rank affine recurrence를 chunk-local flow와 associative boundary scan으로 계산하는 틀 | K015 |
| RLS | 재귀 최소제곱(Recursive Least Squares) | cumulative ridge solution을 inverse covariance로 정확히 갱신하는 고비용 기준법 | K022 |
| LMS | 최소평균제곱(Least Mean Squares) | 순간 제곱오차 gradient를 쓰는 고전적 적응 필터 update | K020 |
| TTT | 테스트 시간 학습(Test-Time Training) | 추론 중 내부 목적의 gradient로 일부 상태·파라미터를 적응시키는 관점 | K020 |
| $\mu$P | maximal update parameterization | 모델 폭 변화에 따른 hyperparameter scaling을 맞추는 학습 설정 | K023 |
| CDE | 제어 미분방정식(Controlled Differential Equation) | ParallelFlow가 matrix recurrence를 연속시간 flow 관점으로 해석할 때 쓰는 틀 | K031 |
| `tensorInv` | 구조화 tensor 역풀이 | 시간×rank causal system에 여러 right-hand side를 적용하는 ParallelFlow 연산 | K031 |

## 번역 검수 기록

| 검수 항목 | 결과 |
|---|---|
| 메타데이터 | 공식 arXiv abstract 페이지, PDF 첫 쪽, TeX 저자 블록을 대조했다. 저자 11명, v1, 제출 시각, 분류, DOI를 확인했다. |
| 사용 원문 | `fast-weight-attention-2608.27763v1.pdf` SHA-256 `47D82ADEFBEFE702A9B53C59F460C52412243A7A5C5B02DDB59C06E8FD32D9D7` |
| 사용 TeX | `main_seed.tex` SHA-256 `9A204BD174EEC1555C2EC243C39CC7A871426522F209821E260576C171712D02` |
| PDF 구조 | 54쪽, 암호화 없음, arXiv GenPDF 생성본임을 확인했다. |
| 시각 확인 | 공동 검수에서 PDF 1, 2, 5, 6, 8, 25-29, 35, 37, 43, 50, 54쪽을 이미지로 렌더링해 저자·초록, 배경 수식, 계열 개요, 병렬식, 실험 표, timing 그림, 부록 수식과 마지막 쪽을 확인했다. |
| 수식 | TeX의 차원 표기와 PDF 렌더링을 대조하고 scalar/열별/window update의 행렬 방향을 확인했다. |
| 표 수치 | 표 1-3의 caption, 방향(높을수록/낮을수록), 대표 수치를 PDF와 TeX에서 교차 확인했다. 표 4의 complexity 항도 확인했다. |
| 가능성·한정 표현 | “경쟁력 유지”, “보조 증거”, “대표 변형”을 일률적 우위나 전체 계열 검증으로 강화하지 않았다. |
| 저작권 경계 | 영어 전문을 재현하지 않았다. 직접 대조 인용은 `S001` 14단어 한 문장으로 제한했다. |
| 원문 이상 | unresolved `tab:accuracy_results_medium` 참조, 원고 내부 날짜와 제출일 차이, 연결되지 않은 소속 번호 4를 기록했다. |
| OCR 상태 | text-native PDF와 공식 TeX를 사용했으므로 OCR 복원은 사용하지 않았다. 판독 불확실 문장은 없다. |

## 원문과 함께 읽는 순서

1. 먼저 이 문서의 `E1-E4`로 정렬과 scalar NLMS update를 이해한다.
2. 원문 그림 1과 그림 11에서 scalar/열별/window 및 RAW/RBW 축을 분리해 본다.
3. `E5-E10`으로 여섯 Falcon 변형을 비교한다.
4. 원문 그림 4-10은 새 모델 목록이 아니라 같은 recurrence의 recurrent/parallel/chunk 표현임을 염두에 두고 읽는다.
5. 표 1-3은 전체 우승 횟수보다 **어느 설정이 어느 과제에서 유리한가**를 중심으로 읽는다.
6. 구현을 시도할 때는 경계 sentinel, positive decay, fp32 log-prefix, sliding tail $B-1$ 보존을 먼저 테스트한다.
