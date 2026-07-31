# AREX: Towards a Recursively Self-Improving Agent for Deep Research - 한국어 대조 번역과 해설

## 논문 메타데이터

| 항목 | 내용 |
|---|---|
| 원문 제목 | AREX: Towards a Recursively Self-Improving Agent for Deep Research |
| 한국어 제목 | AREX: 재귀적으로 자기개선하는 Deep Research 에이전트를 향하여 |
| 저자 | Shuqi Lu, Chaofan Li, Kun Luo, Zhang Zhang, Hui Wang, Hongwang Xiao, Lei Xiong, Jiahao Wang, Sen Wang, Xiyan Jiang, Wanli Li, Yuyang Hu, Hongjin Qian, Bingyu Yan, Jianlyu Chen, Ziyi Xia, Yingxia Shao, Kang Liu, Zhicheng Dou, Di He, Chaozhuo Li, Qiwei Ye, Zhongyuan Wang, Zheng Liu |
| 소속 | AREX Team, Beijing Academy of Artificial Intelligence (BAAI) |
| 출판 형태 | arXiv preprint, cs.AI |
| 연도 | 2026 |
| 식별자 | arXiv:2607.21461 |
| DOI | 10.48550/arXiv.2607.21461 |
| 사용 버전 | v2, 2026-07-24 |
| 원문 언어 | 영어 |
| 원문 | [arXiv abstract](https://arxiv.org/abs/2607.21461), [HTML](https://arxiv.org/html/2607.21461), [PDF](https://arxiv.org/pdf/2607.21461) |
| 접근일 | 2026-07-30 |
| 라이선스 표시 | arXiv.org perpetual non-exclusive license |

[한국어 학습 README로 돌아가기](README.md)

## 번역·접근 범위

arXiv의 비독점 배포 라이선스는 arXiv가 원문을 배포할 권한을 뜻하며 제3자에게 전문 재배포나 전문 번역 재배포 권한을 부여하는 오픈 라이선스와 같지 않다. 따라서 이 파일은 저작권 경계를 지키기 위해 짧은 원문 2문장만 즉시 대조하고, 나머지는 논문의 절 순서와 주장, 수식, 수치를 보존한 상세 한국어 해설로 제공한다. 원문 직접 인용은 총 17단어다.

PDF는 20쪽 전체를 확인했고 다단 편집 순서와 7-14쪽의 수식, 표, 그림을 시각적으로 대조했다. 부록과 참고문헌도 확인했으나 참고문헌은 번역하지 않는다.

| 구간 | 상태 | 제공 형식 |
|---|---|---|
| 제목·초록 | 부분 번역 | 짧은 문장 대조 + 상세 해설 |
| 1 Introduction | 완료 | 절별 한국어 해설 |
| 2 Recursive Self-Improvement | 완료 | 수식과 구조를 포함한 상세 해설 |
| 3 Training Data Construction | 완료 | 절별 한국어 해설 |
| 4 Training Pipeline | 완료 | 목적함수와 key step 해설 |
| 5 Experiments | 완료 | 표 수치와 비교 조건 해설 |
| 6 Conclusion | 완료 | 상세 해설 |
| A Related Work | 완료 | 범주별 해설 |
| B Preliminary Exploration | 완료 | 예비 실험 범위 해설 |
| References | 해당 없음 | 서지정보는 원문 링크 참조 |

## 읽기 전 핵심 배경

- **RSI (Recursively Self-Improving, 재귀적 자기개선)**: 현재 결과를 평가한 뒤 부분적으로 검증된 상태를 다음 라운드의 더 작은 연구 문제로 바꾸는 과정이다.
- **제약별 검증(constraint-wise verification)**: 답 전체를 한 번에 참/거짓으로 판단하지 않고 필수 조건을 각각 근거와 함께 검사한다.
- **ACU (Autonomous Context Updating, 자율 컨텍스트 갱신)**: 모델이 긴 기록을 검증된 사실, 탈락 후보, 미해결 제약, 다음 계획 중심으로 재구성한다.
- **agentic mid-training(에이전트형 중간 훈련)**: 사전학습과 최종 정렬 사이에서 도구 호출, 다중 라운드 탐색, 관찰 반영을 학습한다.
- **step-aware RL(단계 인식 강화학습)**: token 수가 아니라 의미 있는 assistant step과 궤적을 계층적으로 평균해 긴 궤적의 편향을 줄인다.

## 문장 대조 번역

### Abstract

**S001 — Original**

Deep research requires agents to find answers that jointly satisfy multiple constraints.

**S001 — 한국어**

(Deep Research에서는 에이전트가 여러 제약을 동시에 만족하는 답을 찾아야 한다.)

- **용어·약어 해설**
  - **Deep Research(심층 연구)**: 검색, 문서 열람, 근거 통합, 검증을 여러 단계 반복하는 에이전트 과제다.
  - **multiple constraints(다중 제약)**: 정답 후보가 시간, 속성, 출처, 관계 같은 여러 필수 조건을 모두 만족해야 한다는 뜻이다.

**S002 — Original**

Discovering such answers is costly.

**S002 — 한국어**

(그러한 답을 발견하는 데는 큰 비용이 든다.)

- **용어·약어 해설**
  - **discovery-verification asymmetry(발견-검증 비대칭)**: 넓은 후보 공간에서 답을 찾기는 어렵지만 특정 후보가 개별 조건을 만족하는지 확인하는 일은 상대적으로 쉽다는 관찰이다.

## 절별 한국어 해설

### 1. Introduction

Deep Research의 병목은 관련 문서를 찾는 것만이 아니다. 유효한 답은 여러 결합 제약을 동시에 만족해야 하며 에이전트는 흩어진 증거와 충돌하는 정보를 통합하고 각 조건의 근거를 확인해야 한다.

기존 접근은 한 검색 궤적을 더 길게 실행하는 경향이 있다. 계산량을 늘리면 탐색 범위는 넓어지지만 초기 오류가 계속 남거나 이미 실패한 방향을 다시 방문하거나 일부 조건만 맞는 후보를 너무 일찍 채택할 수 있다. 저자들은 이를 "검색 시간을 늘리는 문제"가 아니라 "남은 불확실성을 진단해 다음 연구 문제로 바꾸는 문제"로 재정의한다.

검증은 최종 답을 거르는 필터에 머물지 않는다. 임시 답을 부분 검증 상태로 바꾸고 확인된 진전은 보존하며 약하거나 해결되지 않은 주장만 다음 검색 목표로 만든다. 긴 궤적에서는 전체 기록이 중복과 오래된 계획을 쌓지만 무작정 자르면 이후 검증에 필요한 증거가 사라진다. AREX의 ACU는 이 문제를 연구 상태 관리로 다룬다.

### 2. Recursive Self-Improvement

#### 2.1 Overall Framework

AREX-Turbo는 Qwen3.5-4B, AREX-Base는 Qwen3.5-122B-A10B를 backbone으로 사용한다. 시스템은 내부 연구 루프와 외부 자기개선 루프의 이중 구조다.

1. 원 질문 \(x\)에서 첫 연구 목표 \(q^{(1)}\)을 만든다.
2. 내부 루프가 검색하고 증거를 통합해 임시 답, 근거, confidence를 만든다.
3. 외부 루프가 임시 답을 제약별로 감사한다.
4. 충분하면 수락하고, 복구 가능하면 유효한 정보를 보존한 채 세부 목표로 정제하며, 복구 불가능하면 원 문제에서 재시작한다.

#### 2.2 Inner Research Loop

라운드 \(k\), 단계 \(t\)까지의 상호작용은 다음 궤적으로 표현된다.

\[
h_t^{(k)}=[(m_i^{(k)},a_i^{(k)},o_i^{(k)})]_{i=1}^{t}
\]

\(m_i\)는 중간 분석, \(a_i\)는 연구 행동, \(o_i\)는 도구 관찰이다. 정책과 도구 환경은 다음처럼 연결된다.

\[
(m_{t+1}^{(k)},a_{t+1}^{(k)})=\pi_\theta(x,q^{(k)},h_t^{(k)})
\]

\[
o_{t+1}^{(k)}=\mathcal{T}(a_{t+1}^{(k)})
\]

새 증거가 후보를 지지하면 남은 제약으로 이동하고 모순되면 후보를 기각하거나 대안을 찾는다. 출처가 충돌할 때는 권위, 원 출처와의 거리, 시간적 최신성을 우선한다. 후보가 사라지면 검색 공간을 넓히거나 목표를 분해한다.

#### 2.2.1 Autonomous Context Updating

\[
z_t^{(k)}=f_\theta(h_t^{(k)})
\]

ACU가 만드는 상태에는 검증된 발견과 source identifier, 현재 후보, 미해결 제약, 유효성 우려, 기각 후보, 다음 계획이 포함된다. 중복 관찰과 폐기된 결론, 오래된 계획은 제거한다.

가장 최근 갱신 단계가 \(\tau\)라면 유효 컨텍스트는 다음과 같다.

\[
\bar{h}_t^{(k)}
=z_\tau^{(k)}\oplus[(m_i^{(k)},a_i^{(k)},o_i^{(k)})]_{i=\tau+1}^{t}
\]

즉 압축 상태와 갱신 이후 새 기록만 사용한다. 모델은 의미 있는 하위 문제 해결, 주요 후보 탈락, 충돌 해소, 계획 변경 시점에 `update_context`를 스스로 호출한다. 호출하지 않을 수도 있고 한 라운드에 여러 번 호출할 수도 있다.

#### 2.2.2 Structured Answer Externalization

\[
r^{(k)}=F_\theta(\bar{h}_{T_k}^{(k)})
=(y^{(k)},\mathcal{E}^{(k)},s^{(k)})
\]

내부 루프는 임시 답 \(y\), 근거 집합 \(\mathcal{E}\), 0에서 100 사이의 confidence \(s\)를 구조화해 반환한다. 외부 루프가 판단할 수 있도록 답과 증거, 확신을 명시적으로 분리한다.

#### 2.3 Outer Self-Improvement Loop

외부 평가는 다음 상태를 만든다.

\[
g^{(k)}=(v^{(k)},P^{(k)},I^{(k)},q^{(k+1)})
\]

- \(v\): 현재 궤적의 복구 가능 여부
- \(P\): 다음 라운드에 보존할 정보
- \(I\): 남은 문제
- \(q^{(k+1)}\): 다음 목표

confidence가 임계값 이상이면 `ACCEPT`, 미만이면서 복구 가능하면 `REFINE`, 복구 불가능하면 `RESTART`다. 정제할 때는 검증된 발견을 보존하고 남은 문제를 목표로 바꾼다. 재시작할 때는 오염된 궤적을 버리고 원 문제에서 새로 시작한다. 최대 라운드 안에 임계값을 넘지 못하면 완료된 답 중 최고 confidence를 반환한다.

### 3. Training Data Construction

#### 3.1 Recursive Research Task Synthesis

검색 집약형, 추론 집약형, 과학 문헌형의 세 과제 범주를 사용한다. 사람 전문가가 출력 형식, 사용 가능한 출처, 추론 요구, 검증 기준을 담은 template을 만든다.

잠재 답 \(y\)와 검증 가능한 제약을 정의한다.

\[
\mathcal{C}(y)=\{c_1,c_2,\ldots,c_n\}
\]

최종 질문은 답을 직접 드러내지 않는 변환된 제약에서 만든다. 유효 과제는 질문만으로 답을 곧바로 추측할 수 없어야 하고 모든 제약에 공개 증거가 있어야 하며 결합 제약이 답을 유일하게 식별해야 한다. 자동 검증과 독립 rollout으로 애매하거나 너무 쉽거나 해결 불가능한 과제를 제거한다.

#### 3.2 Teacher Trajectory Collection and Quality Control

강한 교사 모델이 AREX와 같은 도구와 환경에서 궤적을 만든다. 품질 관리는 무의미한 반복, 잘못된 추론, 근거 없는 결론, 잘못된 도구 호출을 제거한다. 충분한 증거 전에 답을 맞히거나 인용이 주장과 연결되지 않거나 관찰과 모순되거나 필요한 정보가 빠진 궤적도 버린다. 마지막으로 confidence 임계값을 통과한 궤적만 남긴다.

### 4. Training Pipeline

#### 4.1 Multi-stage Agentic Mid-training

첫 단계는 검색 집약형 다중 라운드 궤적으로 웹 탐색과 도구 사용을 익힌다. 다음 단계는 장기 추론, 가설 비교, 어려운 문제 해결을 강화한다. 그러나 추론 데이터에 지나치게 특화되면 먼저 배운 검색 행동이 약해질 수 있어 마지막에 검색, 추론, 도구 사용을 혼합한 consolidation을 수행한다.

전체 성공 궤적의 모든 token을 동일하게 학습하는 대신 다음 key step을 골라 다시 노출한다.

1. 여러 탐색 뒤 처음 답 관련 증거가 나타난 단계
2. 잘못된 후보나 가설을 처음 기각하고 방향을 전환한 단계
3. 검증된 증거와 미해결 제약, 다음 계획을 남긴 핵심 context update

#### 4.2 Step-aware Reinforcement Learning

각 assistant step의 token 확률비를 기하평균한다.

\[
\rho_{i,j}
=\exp\left(\frac{1}{L_{i,j}}\sum_{k=1}^{L_{i,j}}\log r_{i,j,k}\right)
\]

그 다음 궤적 안의 step을 평균하고 마지막으로 batch의 궤적을 평균한다. 이 계층적 평균은 긴 궤적이 token 수만으로 손실을 지배하는 현상을 줄인다.

그룹 내 결과 보상은 평균과 표준편차로 표준화한다. key-step 보너스는 최종 성공 궤적에만 적용한다.

\[
\tilde{B}_{i,j}=\mathbb{I}[R_i>0]B_{i,j}
\]

\[
A_{i,j}=A_i^{out}+\lambda_{key}\tilde{B}_{i,j}
\]

저자들은 key-step 보너스가 전체 credit assignment를 해결하는 만능 장치가 아니라 최종 정답 보상을 주 신호로 유지하면서 결정적 단계에 작은 우선순위를 더하는 장치라고 설명한다.

### 5. Experiments

#### 5.1 Experimental Setup

BrowseComp, GAIA, xbench-2510, DeepSearchQA, WideSearch-en, HLE with tools의 여섯 benchmark를 평가한다. 공통 도구는 `search`, `visit`, `update_context`, `finish`이고 HLE에는 Python이 추가된다. 사례당 내부 루프 최대 300 turn, 외부 루프 최대 5회다.

#### 5.2 Overall Performance

| 모델 | BrowseComp | GAIA | xbench-2510 | DeepSearchQA | WideSearch-en | HLE(tool) |
|---|---:|---:|---:|---:|---:|---:|
| AREX-Turbo | 70.7 | 81.6 | 57.0 | 78.5 | 68.5 | 40.6 |
| AREX-Base | 82.5 | 85.4 | 71.0 | 89.9 | 82.0 | 52.4 |

AREX-Base는 작은 활성 parameter 수에도 여러 비교 가능한 backbone보다 높은 결과를 보인다. 다만 benchmark별 metric이 다르고 비공개 frontier model의 도구와 budget이 완전히 같다고 보장할 수 없다. HLE에서 별표는 full HLE, 별표 없음은 text-only subset을 뜻해 직접 비교에 주의해야 한다.

#### 5.3 Inference Framework Analysis

BrowseComp 사례의 80.3%에서 ACU가 사용됐다. 128K context에서 평균 25,721 token, 중앙값 25,386 token에 갱신됐고 상한에 도달한 갱신은 0.01%였다. 따라서 대다수 호출은 hard limit 직전이 아니라 연구 상태 전환 때문에 발생했다고 해석한다.

호출 이유는 검색 전략 수정 66.9%, 후보 기각 13.6%, 새 lead 7.2%, 요약 6.4%, 증거/답 검증 5.3%, 기타 0.6%였다. 갱신 내용에는 다음 계획 96.4%, 미해결 제약 95.5%, 기각 후보 81.5%, 검증된 발견 72.1%가 자주 포함됐다.

| 설정 | BrowseComp 정확도 |
|---|---:|
| ACU 없음, 외부 루프 없음 | 59.6 |
| ACU 없음, 외부 루프 있음 | 69.8 |
| ACU 있음, 외부 루프 없음 | 71.4 |
| ACU 있음, 외부 루프 있음 | 82.5 |

confidence 90-100 구간에 들어간 정답 비율은 ACU 없이 89.3%, ACU 사용 시 95.9%였다. 하지만 이 histogram만으로 confidence calibration이 입증되는 것은 아니다.

#### 5.4 Ablation Studies

전체 AREX의 BrowseComp 정확도는 82.5다. 단계적 훈련을 직접 혼합으로 바꾸면 77.5, key-step replay를 같은 budget의 무작위 step replay로 바꾸면 74.1, step-aware objective를 표준 GRPO로 바꾸면 79.4로 낮아진다.

훈련 후 평균 step loss는 일반 0.232, 증거 발견 0.277, 경로 기각/전환 0.298, 핵심 context update 0.300이다. 후자의 세 단계가 일반 단계보다 각각 약 19%, 28%, 29% 높아 결정적 행동이 더 학습하기 어렵다는 근거로 사용된다.

### 6. Conclusion

AREX는 발견-검증 비대칭에서 출발해 검증을 연구 라운드 사이의 상태 전이로 만든다. 검증된 증거는 보존하고 해결되지 않은 주장은 다음 목표로 바꾸며 ACU와 step-aware training으로 긴 궤적을 지원한다. 저자들은 향후 과제로 특정 규칙에 묶이지 않은 일반적인 step utility 추정과 더 세밀한 학습 신호를 제안한다.

### A. Related Work

관련 연구는 세 범주로 정리된다.

1. 도구와 웹 환경을 사용하는 Deep Research 에이전트
2. 후보 순위화나 진행 중 의사결정에 검증을 사용하는 연구
3. 긴 궤적의 memory, context management, credit assignment 연구

AREX의 차별점은 검증, 컨텍스트 갱신, 외부 재귀 루프를 하나의 연구 상태 전이 체계로 결합하고 이를 위한 key-step 중심 훈련을 제안했다는 데 있다.

### B. Preliminary Exploration under a Simplified Setting

122B-A10B backbone에서 ACU, 외부 루프, key-step supervision을 모두 제외한 단순 설정으로 self-distillation을 시험했다. 직접 훈련은 BrowseComp 52.3, self-distillation은 57.1이었다. 저자들도 이 실험이 최종 AREX recipe의 구성 요소를 분리해 입증하지 않으며 교사 편향을 물려받을 수 있다고 명시한다.

## 수식·그림·표 읽기

- **Figure 2**: 내부 루프가 임시 답, 증거, confidence를 만들고 외부 루프가 수락, 정제, 재시작을 선택하는 흐름이다.
- **Equation 4-7**: ACU가 전체 궤적을 압축 상태로 바꾸고 이후 정책이 이 상태와 새 관찰만 사용한다.
- **Equation 8-12**: 답, 증거, confidence를 구조화하고 복구 가능성에 따라 다음 라운드를 구성한다.
- **Table 1**: benchmark마다 metric과 평가 subset이 다르므로 행의 평균을 임의로 계산하지 않는다.
- **Table 2-3**: ACU가 언제 무엇을 저장하는지와 ACU/외부 루프의 조합 효과를 함께 본다.
- **Figure 3**: confidence 구간별 정답/오답 분포이며 calibration curve는 아니다.
- **Figure 4와 Table 4**: 어려운 key step과 훈련 구성 요소의 성능 기여를 연결해 해석한다.

## 약어 및 기술 용어 사전

| 원어 | 한국어 | 의미 | 최초 등장 sentence ID |
|---|---|---|---|
| Deep Research | 심층 연구 | 도구를 사용해 검색, 근거 통합, 검증을 반복하는 장기 과제 | S001 |
| multiple constraints | 다중 제약 | 정답이 동시에 만족해야 하는 여러 필수 조건 | S001 |
| RSI, Recursively Self-Improving | 재귀적 자기개선 | 부분 검증 상태를 다음 연구 문제로 바꾸는 반복 과정 | S001 해설 |
| constraint-wise verification | 제약별 검증 | 각 조건을 독립적인 증거 검사로 나누는 방법 | S001 해설 |
| ACU, Autonomous Context Updating | 자율 컨텍스트 갱신 | 연구 기록을 다음 행동에 필요한 상태로 압축·재구성 | S001 해설 |
| discovery-verification asymmetry | 발견-검증 비대칭 | 후보 발견은 어렵고 주어진 후보 검증은 상대적으로 쉽다는 비대칭 | S002 |
| agentic mid-training | 에이전트형 중간 훈련 | 도구 사용과 다중 라운드 상호작용을 익히는 중간 학습 | S001 해설 |
| key step | 핵심 단계 | 결정적 증거 발견, 오류 기각, 상태 갱신 단계 | S001 해설 |
| step-aware RL | 단계 인식 강화학습 | token, step, trajectory 계층을 구분해 최적화하는 강화학습 | S001 해설 |
| recoverable trajectory | 복구 가능한 궤적 | 유효한 진행을 보존해 정제로 수정할 수 있는 연구 기록 | S001 해설 |
| MoE, Mixture-of-Experts | 전문가 혼합 | 입력마다 일부 expert만 활성화하는 모델 구조 | S001 해설 |
| calibration | 보정 | 예측 confidence와 실제 정답 빈도의 일치 정도 | S001 해설 |

## 번역 검수 기록

- 2026-07-30: arXiv v2 HTML과 20쪽 PDF의 제목, 저자, 절 순서, 수식 번호, 표 수치, 그림 caption을 대조했다.
- 원문 인용은 2문장, 17단어로 제한했다.
- 확률적 표현과 실험 범위를 확정적 사실로 과장하지 않도록 "시사한다", "저자들은 주장한다"를 구분했다.
- HLE full set과 text-only subset의 비교 제한, 부록 self-distillation의 단순화된 조건을 명시했다.
- 전문 문장 대조 번역은 라이선스상 재배포 범위가 명확하지 않아 제공하지 않았다. 권리자가 허용한 원문 파일과 번역 권한이 제공되면 같은 sentence ID 형식으로 확장할 수 있다.
