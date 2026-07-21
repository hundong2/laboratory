# 추론 흔적에서 재사용 가능한 모듈로

작성일: 2026-07-21

## 출처와 작업 범위

- 원문: [From Reasoning Traces to Reusable Modules: Understanding Compositional Generalization in Language Model Reasoning](https://arxiv.org/html/2606.18089v2)
- arXiv: `2606.18089v2` (`cs.LG`)
- 원문 버전 날짜: 2026-07-05
- 원문 언어: 영어
- 확인일: 2026-07-21
- 라이선스: CC BY 4.0
- 저자: Lingjing Kong, Xin Liu, Guangyi Chen 외
- 번역 자료: [translation.ko.md](translation.ko.md)

이 문서는 논문의 핵심 이론, 실험과 실무적 의미를 한국어 학습 자료로 재구성합니다. 수식의 완전한 증명과 부록 전체를 복제하지 않고, 핵심 가정과 결론을 이해하고 작은 합성 실험으로 확인하는 데 초점을 둡니다.

## 한눈에 보기

논문의 중심 질문은 다음과 같습니다.

> 왜 SFT 뒤에 RL을 수행하면, 학습에서 보지 못한 새로운 추론 단계 조합에 더 잘 일반화하는가?

저자들은 추론 trace를 재사용 가능한 두 종류의 원자 모듈이 계층적으로 선택되는 과정으로 봅니다.

- **skill**: 덧셈, 치환, 문자열 변환처럼 국소 상태를 바꾸는 연산
- **routing mechanism**: 이전 결과, 더 오래된 중간 결과, 분기 중 어떤 정보를 다음 skill에 넘길지 정하는 연결 규칙

논문의 해석은 다음과 같습니다.

1. SFT는 올바른 합성 trace 안에서 필요한 원자 모듈의 재료를 제공합니다.
2. canonical trace만 모방하면 skill과 routing이 자주 등장하는 문맥에 얽힌 채 남을 수 있습니다.
3. RL rollout과 검증 가능한 보상은 SFT가 보여 주지 않은 성공 경로의 국소 사건을 더 자주 노출합니다.
4. 이렇게 식별된 모듈은 학습에서 국소 interface가 관찰된 경우 새로운 전체 조합으로 재결합할 수 있습니다.

핵심은 “RL이 무에서 새로운 능력을 만든다”가 아니라, **SFT가 제공한 합성 재료를 RL이 분해하고 interface를 탐색해 재사용 가능하게 한다**는 주장입니다.

## 기초 개념

### SFT와 RL

**지도 미세조정(SFT)**은 문제와 모범 응답 쌍을 모방하도록 모델을 학습합니다. 안정적인 출발점을 제공하지만, 문제마다 하나의 정형화된 reasoning trace만 주어지면 모델은 단계 자체보다 전체 template을 외울 수 있습니다.

**강화학습(RL)**은 모델이 여러 trajectory를 생성하게 하고 최종 정답과 같은 reward로 성공 경로의 확률을 높입니다. 논문에서 RL의 이점은 단순 정답 강화에 그치지 않고, rollout support를 넓혀 모듈을 구별하는 국소 사건을 관찰하게 하는 데 있습니다.

### 합성 일반화

훈련에서 본 원자 요소를 새로운 조합으로 사용할 수 있는 능력입니다. 예를 들어 `reverse`, `rotate`, `duplicate`를 각각 또는 일부 조합으로 배웠을 때, 처음 보는 순서와 연결 방식으로도 정확히 실행하는지 평가합니다.

### 학습 support

support는 학습 분포가 실제로 양의 확률로 보여 주는 문제와 trace의 집합입니다. SFT 정답 trace 바깥에도 유효한 해결 경로가 있지만, SFT가 이를 보여 주지 않으면 무한한 SFT 데이터만으로도 존재를 확인할 수 없습니다.

### 식별 가능성

관찰된 trace 분포만으로 숨은 모듈과 연결 구조를 상태 이름의 치환까지 복원할 수 있는지를 뜻합니다. 논문의 Theorem 3.1은 faithfulness, 제한된 선택 집합, neighborhood coverage, 관찰 가능한 module signature 등의 충분조건을 제시합니다.

### local witness

새로운 전체 조합에서 여러 모듈이 만나는 국소 interface가 훈련 중 호환 가능한 형태로 한 번이라도 관찰됐음을 증명하는 사례입니다. Theorem 3.4는 필요한 모든 국소 family에 witness가 있으면 학습한 제약을 모순 없이 결합할 수 있다고 설명합니다.

## 핵심 요약

### SFT와 RL의 비대칭적 분업

| 단계 | 주된 역할 | 부족한 점 |
|---|---|---|
| SFT | 합성 trace 안에서 전체 원자 inventory와 올바른 시작 정책 제공 | canonical trace 밖의 유효한 국소 사건을 관찰하지 못할 수 있음 |
| RL | 도달 가능하고 reward가 구별하는 숨은 사건을 강화해 모듈과 interface 분리 | SFT 정책이 전혀 도달하지 못하는 모듈을 무에서 복원하지 못함 |

RL이 어떤 사건을 풍부하게 하려면 세 조건이 중요합니다.

- 현재 policy가 해당 사건에 양의 확률로 도달할 것
- 사건을 포함한 trace가 더 높은 성공 확률을 가질 것
- SFT가 아직 충분히 보여 주지 않은 trace 질량이 있을 것

### 데이터 설계 결론

- SFT는 모든 원자 모듈을 **합성 trace 속에서** 포함해야 합니다.
- RL은 SFT와 같은 조합을 반복하기보다 SFT support 밖의 새로운 조합을 탐색해야 합니다.
- 원자 skill만 고립해서 보여 주는 것으로는 깊은 조합 일반화가 충분하지 않습니다.
- skill뿐 아니라 중간 정보를 전달하는 routing도 독립적인 학습 대상입니다.

## 상세 정리

### 1. 계층적 잠재 선택 모델

관찰 가능한 문제 descriptor `P`가 숨은 선택 변수 계층 `S`를 유도하고, 이 선택이 관찰 가능한 trace token `D`를 생성한다고 봅니다.

```text
문제 descriptor P
  → 고수준 전략 선택
  → routing과 skill 선택
  → 관찰 가능한 reasoning trace D
```

잠재 노드는 “어떤 모듈을 썼는가”와 “어떻게 연결했는가”를 나타냅니다. 상태 이름 자체는 바뀌어도 되므로 식별은 component-wise relabeling까지 정의됩니다.

### 2. SFT hidden support

한 문제에 유효 trace가 여러 개 있어도 SFT가 일부만 보여 주면, 관찰된 부분을 전체 진실로 간주하는 다른 trace 분포와 실제 분포를 구별할 수 없습니다. 따라서 숨은 부분에만 나타나는 module interface는 SFT 관찰만으로 인증할 수 없습니다. 이는 단순한 표본 부족이 아니라 비식별성 문제입니다.

### 3. RL enrichment

현재 policy가 숨은 국소 사건을 때때로 생성하고, 그 사건이 성공과 양의 상관을 가지면 reward-positive rollout에서 사건의 조건부 빈도가 증가합니다. 이 대비 신호가 평소 함께 붙어 있던 skill과 routing을 분리할 단서를 제공합니다.

하지만 reachability가 0이거나 reward가 해당 사건을 구별하지 못하면 RL update는 이 메커니즘을 만들지 못합니다.

### 4. local witness에 의한 조합

모듈을 식별했다고 모든 조합이 자동으로 가능한 것은 아닙니다. 새로운 문제에서 두 모듈이 처음 만나는 interface가 훈련 중 한 번도 호환 가능하게 관찰되지 않았다면 연결 규칙을 알 수 없습니다. 논문은 각 새로운 국소 family에 훈련 support의 witness가 있으면 계층을 따라 전체 일관된 assignment를 구성할 수 있음을 보입니다.

### 5. 합성 문자열 실험

통제 실험은 다음을 사용합니다.

- 결정적 문자열 변환 함수 24개를 atomic skill로 사용
- 함수 입력 구조 10개를 atomic routing mechanism으로 설계
- 합성 깊이로 난이도 조절
- SFT는 정답 reasoning trace로 학습
- RL은 최종 문자열의 정답 여부만 reward로 사용
- SFT와 RL에서 보지 못한 조합으로 OOD 평가

합성 과제는 실제 수학·코드 benchmark를 대체하려는 것이 아니라, 원자 coverage와 조합 구조를 정확히 조작해 인과적 메커니즘을 분리하기 위한 도구입니다.

### 6. 주요 실험 결과

동일한 SFT 초기화와 300 RL step에서 OOD compound trace 성능은 다음과 같습니다.

| 학습 설정 | 정확도 | SFT 대비 증가 |
|---|---:|---:|
| SFT baseline | 4.8% | - |
| SFT + 원자 모듈 RL | 14.8% | +10.0%p |
| SFT + 합성 trace RL | 42.6% | +37.8%p |

합성 trace RL은 원자 단위 RL보다 27.8%p 높았습니다. 이는 개별 연산뿐 아니라 모듈 사이의 국소 interface를 경험하는 것이 중요하다는 해석과 일치합니다.

원자 skill 8개를 RL 조합에서 제거한 실험에서는 고립된 원자만 다시 넣는 방식보다 해당 원자가 포함된 합성 trace를 다시 넣는 방식이 깊은 조합 성능을 더 잘 회복했습니다. routing mechanism에서도 비슷한 패턴이 나타났고, 더 단순한 낮은 깊이의 routing 조합이 복구에 더 유리했습니다.

SFT와 RL의 조합 집합 관계를 비교하면 seen 성능 차이는 작았지만 unseen 일반화는 크게 달랐습니다. RL 조합이 SFT 조합에 완전히 포함된 경우가 가장 약했고, 두 조합 집합이 분리된 설정이 가장 강했습니다.

SFT에서 원자 4개가 빠진 경우의 unseen 성능도 악화됐습니다.

| 설정 | Unseen depth 2 | Unseen depth 3 |
|---|---:|---:|
| SFT가 모든 원자 포함, SFT만 | 0.30 | 0.22 |
| SFT가 모든 원자 포함, +RL | 0.67 | 0.55 |
| SFT에서 원자 누락, SFT만 | 0.24 | 0.15 |
| SFT에서 원자 누락, +RL | 0.52 | 0.36 |

### 7. 실제 모델의 보완 증거

저자들은 MATH-500, AIME 2024/2025, AMC, GSM8K의 수학 문제 643개에서 Qwen3-4B와 Qwen3-4B-Thinking-2507 trace를 비교했습니다. RL-tuned 모델에서 짧은 추상 skill n-gram 다양성이 더 풍부했으며, 이를 국소 연산이 다른 이웃과 더 유연하게 결합되는 신호로 해석합니다. 이는 통제 실험을 보완하는 정성·표현 수준의 증거이지 전체 이론의 직접 증명은 아닙니다.

## 논문을 읽을 때 주의할 점

- 핵심 인과 실험은 통제된 합성 문자열 변환 과제에 집중합니다.
- 식별 정리는 여러 충분조건을 요구하며 실제 LLM에서 모든 조건이 성립한다고 입증한 것은 아닙니다.
- 짧은 skill n-gram 다양성은 재조합 가능성의 proxy이며 실제 잠재 모듈을 직접 관찰한 것은 아닙니다.
- “SFT와 RL 데이터가 분리될수록 항상 좋다”가 아니라, SFT가 원자 inventory를 먼저 포함하고 RL이 도달 가능하며 검증 가능한 새로운 interface를 탐색해야 한다는 조건부 결론입니다.
- reward hacking이나 잘못된 verifier에서는 reward-positive event가 올바른 모듈 식별로 이어지지 않을 수 있습니다.

## 용어 정리

| 용어 | 뜻 |
|---|---|
| reasoning trace | 중간 추론 단계가 토큰으로 드러난 기록 |
| atomic skill | 국소 상태 변환을 수행하는 재사용 연산 |
| routing mechanism | 어떤 중간 정보를 다음 연산에 전달할지 정하는 규칙 |
| descriptor | 문제의 고수준 제약을 표현하는 관찰 입력 |
| latent selection | 관찰되지 않는 모듈·전략 선택 변수 |
| support | 학습 분포가 실제로 관찰시키는 사례 집합 |
| identifiability | 관찰 분포로부터 숨은 구조를 복원할 수 있는 성질 |
| neighborhood coverage | 모듈을 다른 문맥과 분리할 국소 관찰이 충분한 상태 |
| local witness | 새 interface와 호환되는 국소 구성을 훈련에서 본 증거 |
| OOD composition | 훈련에서 보지 못한 원자 요소의 조합 |
| rollout reachability | 현재 policy가 특정 사건을 생성할 양의 확률을 갖는 조건 |
| reward informativeness | reward가 유용한 사건 포함 여부를 구별하는 조건 |

## 실습 학습 가이드

1. [`01_foundations.ipynb`](01_foundations.ipynb): 문자열 skill과 routing을 분리하고 같은 skill inventory가 다른 trace를 만드는 과정을 확인합니다.
2. [`02_practice.ipynb`](02_practice.ipynb): 합성 trace에서 관찰된 local interface를 수집하고 unseen composition의 witness coverage를 계산합니다.
3. [`03_advanced.ipynb`](03_advanced.ipynb): 논문의 표를 재계산하고 SFT coverage와 SFT–RL overlap을 curriculum 관점에서 진단합니다.

노트북은 Python 표준 라이브러리만 사용합니다. Jupyter가 없어도 각 코드 셀을 일반 Python으로 실행할 수 있습니다.

## 다음 학습 경로

1. 원문 2장에서 skill과 routing의 구분 및 compositional support 정의를 읽습니다.
2. Theorem 3.1의 조건을 “관찰 signature, 제한된 선택, neighborhood coverage” 관점에서 해석합니다.
3. Theorem 3.4의 local witness를 데이터 coverage graph로 바꿔 봅니다.
4. 실무 데이터에서 task를 skill과 routing label로 추상화해 짧은 n-gram 다양성을 비교합니다.
5. SFT는 원자 inventory를 합성 문맥에서 덮고, RL은 검증 가능한 미관찰 interface를 선택하는 curriculum을 설계합니다.
6. 실제 적용에서는 reward hacking, rollout 비용, model drift와 안전성 평가를 별도 gate로 둡니다.

## 참고 링크

- [arXiv HTML v2](https://arxiv.org/html/2606.18089v2)
- [arXiv 초록 페이지](https://arxiv.org/abs/2606.18089)
- [PDF](https://arxiv.org/pdf/2606.18089)
