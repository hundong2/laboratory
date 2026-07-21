# 논문 한국어 번역 요약

원문: [From Reasoning Traces to Reusable Modules: Understanding Compositional Generalization in Language Model Reasoning](https://arxiv.org/html/2606.18089v2)

- 원문 언어: 영어
- 대상 버전: arXiv:2606.18089v2, 2026-07-05
- 확인일: 2026-07-21
- 라이선스: CC BY 4.0

이 문서는 원문의 주요 섹션 흐름, 핵심 주장, 정리의 의미와 실험 수치를 보존한 한국어 번역 요약입니다. 완전한 수식과 증명은 원문을 함께 확인하세요.

## 제목

**추론 흔적에서 재사용 가능한 모듈로: 언어 모델 추론의 합성 일반화 이해하기**

## 초록

SFT와 RL을 결합하는 사후 학습 pipeline은 LLM을 견고한 추론 모델로 만드는 핵심 방식이 됐다. 저자들은 이 성공이 합성 일반화에서 비롯된다고 주장하며 이를 계층적 잠재 선택 모델로 형식화한다.

이 모델에서 reasoning trace는 재사용 가능한 원자 모듈을 선택하는 이산 잠재 변수의 cascade로 생성된다. 원자 모듈에는 국소 연산을 수행하는 skill과, 중간 정보를 선택·재사용·조합하는 routing mechanism이 포함된다.

SFT와 RL은 비대칭적이지만 보완적인 역할을 한다. SFT는 합성 trace 안에 원자 모듈 재료를 제공하고, RL은 trace를 분해해 숨은 원자 모듈을 식별하고 합성 일반화를 가능하게 한다. 통제 실험은 RL이 SFT의 compound trace에서 원자를 추출해 새로운 구성에 재조합할 수 있음을 보여 준다. 고립된 원자 모듈보다 compound trace 훈련이 더 강한 일반화를 만들며, 효과적인 protocol은 SFT가 합성 trace로 전체 원자 inventory를 덮고 RL은 SFT support 바깥의 새로운 조합에 집중하는 것이다.

## 1. 서론

SFT만 사용한 모델은 소수의 정형화된 golden trace를 모방하다 익숙한 단계를 낯선 방식으로 다시 연결해야 할 때 성능이 떨어질 수 있다. 반면 SFT 뒤의 RL은 OOD 조합에서 더 안정적이지만, 두 단계가 각각 무엇을 제공하는지는 명확하지 않았다.

저자들은 reasoning을 문제 descriptor가 재사용 모듈의 계층을 선택하는 잠재 변수 과정으로 모델링한다. SFT trace는 필요한 모듈을 포함하지만 skill과 routing이 거의 결정적으로 함께 나타나 통계적으로 얽힐 수 있다. Reward를 사용한 RL trajectory variation은 compound trace를 분해할 국소 차이를 만든다.

기여는 세 가지다.

1. skill과 routing을 분리하는 계층적 잠재 선택 모델
2. 숨은 모듈 계층의 식별 충분조건과 local witness 기반 조합 정리
3. 합성 문자열 변환 개입 실험과 SFT/RL 데이터 curriculum 지침

## 2. 계층적 잠재 선택 모델로서의 추론

### 2.1 모델

자연어 문제는 고수준 제약을 담은 descriptor `P`로 본다. 그 아래 이산 잠재 변수 `S`의 계층이 어떤 모듈을 쓰고 어떻게 조합할지 정한다. 최하단에는 관찰 가능한 reasoning trace token `D`가 있다.

원자 모듈은 두 종류다.

- **skill**: 덧셈, 미분, 치환, 비교와 같은 국소 변환
- **routing mechanism**: 이전 결과 전달, 과거 가정 회수, 다음 부분식 선택, 분기와 반복 같은 정보 흐름

### 2.2 합성 일반화와 잠재 구조 식별

훈련 descriptor support보다 큰 조합 공간에서 실제 conditional trace 분포를 맞추는 것을 합성 일반화라고 정의한다. 숨은 `S`를 직접 볼 수 없으므로 학습은 실제 잠재 모듈처럼 동작하는 표현과 dependency를 식별해야 한다.

## 3. 이론: 식별에서 조합으로

### 3.1 식별

Theorem 3.1은 faithfulness, rank faithfulness, 제한된 선택 집합, 가장 거친 결정적 선택, neighborhood coverage, 관찰 가능한 module signature 조건 아래 잠재 변수와 adjacency를 상태 이름의 component-wise relabeling까지 식별할 수 있다고 말한다.

SFT는 올바른 합성 trace라는 재료를 제공하지만, 각 prompt의 유효 trace 중 일부만 보여 주면 숨은 trace support에 있는 식별 핵심 사건을 인증할 수 없다. 실제 trace 법칙과 “보이는 trace만 전부”라고 가정한 대체 법칙이 같은 SFT 관찰을 만들 수 있기 때문이다.

RL rollout이 어떤 숨은 사건에 도달 가능하고 그 사건을 포함한 trace가 더 높은 reward를 받으면 reward-positive rollout에서 해당 사건이 풍부해진다. 이 support expansion이 얽힌 compound trace를 국소적으로 식별 가능한 선택으로 분해한다.

### 3.2 조합

식별만으로 새로운 조합이 보장되지는 않는다. 낯선 prompt가 여러 모듈을 새로운 interface에서 만나게 할 수 있기 때문이다. Theorem 3.4는 새로운 조합의 모든 국소 parent–children family에 훈련에서 관찰된 호환 값, 즉 local witness가 있으면 국소 제약을 모순 없이 전체 조합으로 연결할 수 있다고 설명한다.

## 4. 실험 결과

### 4.1 설정

저자들은 결정적 문자열 변환 함수 24개를 atomic skill로, 함수 입력 구조 10개를 atomic routing mechanism으로 사용한다. 합성 깊이가 난이도를 조절한다. SFT는 정답 CoT trace로 학습하고, RL은 최종 문자열 정답에서만 reward를 받는다. 평가는 두 학습 단계 모두에서 보지 못한 조합을 대상으로 한다.

### 4.2 발견 1: RL의 원자 분해와 재조합

SFT와 RL 모두 고정 깊이의 compound trace만 보고, 원자 함수와 더 깊은 unseen composition으로 평가했다. SFT는 깊이가 커질수록 빠르게 하락했지만 RL 모델은 더 높은 정확도를 유지했다.

동일 SFT 초기화와 300 RL step의 OOD 정확도는 SFT 4.8%, atomic-module RL 14.8%, compound-trace RL 42.6%였다. Compound RL은 원자 연산뿐 아니라 모듈 interface를 노출하기 때문에 atomic-only RL보다 27.8%p 높았다.

### 4.3 발견 2: 조합 가능성에는 합성 경험이 필요하다

RL corpus에서 atomic skill 8개와 이를 포함한 조합을 제거했다. 누락 원자를 고립된 예제로 다시 넣는 것만으로는 깊은 조합 성능이 잘 회복되지 않았다. 누락 원자를 포함한 합성 trace를 다시 넣어야 큰 폭으로 회복됐다. 원자 지식은 필요하지만, 재조합을 배우려면 합성 문맥에서 만나야 한다.

### 4.4 발견 3: skill과 routing의 공통 학습 메커니즘

Routing mechanism 하나를 RL에서 제거하면 해당 routing을 사용하는 unseen 조합 성능이 떨어졌다. 그 routing이 포함된 조합을 다시 주입하면 성능이 회복됐고, 더 단순한 낮은 깊이 조합이 깊은 조합보다 복구에 효과적이었다. Skill과 routing 모두 적절한 합성 문맥에서 재사용 가능성을 학습한다.

### 4.5 발견 4: SFT와 RL 데이터 관계

SFT와 RL 조합 집합의 포함·부분 중첩·분리 관계를 비교했다. Seen 조합에서는 차이가 작았지만 unseen 조합에서는 큰 차이가 났다. RL 조합이 SFT에 완전히 포함된 설정이 가장 약했고, 두 집합이 분리된 설정이 가장 강했다. RL이 supervised pattern 바깥을 탐색할 때 일반화 이점이 컸다.

다만 SFT가 전체 원자 inventory를 먼저 포함해야 한다. SFT에서 원자 4개가 누락되면 RL이 전체 원자를 사용해도 OOD 성능이 낮아졌다. 또한 SFT에서도 고립 원자보다 합성 trace를 사용하는 편이 더 강했다.

**결론적 curriculum:** SFT는 모든 원자 모듈을 합성 trace에서 덮고, RL은 SFT support 밖의 진짜 새로운 조합을 목표로 해야 한다.

### 4.6 오픈소스 모델의 보완 증거

수학 문제 643개에서 Qwen3-4B와 Qwen3-4B-Thinking-2507의 trace를 추상 skill sequence로 변환했다. RL-tuned 모델은 짧은 skill n-gram에서 더 풍부한 다양성을 보였다. 이는 국소 reasoning operation이 여러 이웃 연산과 더 유연하게 재결합된다는 통제 실험의 signature와 일치한다.

## 5. 결론

문제는 모듈식 결정을 선택하는 숨은 계층을 유도하고, 이 계층이 관찰 가능한 합성 trace를 만든다. SFT는 원자 inventory를 담은 합성 trace를 제공하고, RL은 reward 아래 다시 sampling해 supervised 분포에서 얽혀 있던 식별 핵심 국소 사건을 풍부하게 한다.

실무적으로 SFT와 RL 데이터 분포 자체를 curriculum hyperparameter로 취급해야 한다. SFT 규모와 RL learning rate만 별개로 조정할 것이 아니라, SFT의 원자 coverage와 RL의 미관찰 interface 탐색을 함께 설계해야 한다.

## 한계와 미래 연구

통제 실험은 합성 구조를 정밀하게 조작하기 위해 의도적으로 단순화됐다. 수학, 코드, 도구 사용처럼 풍부한 domain에서 같은 방법을 확장해야 한다. 현재 policy가 실현하는 국소 interface를 추적하고 식별 이득이 큰 영역으로 RL 탐색을 자동 유도하는 adaptive curriculum도 열린 문제다.

## 부록 핵심

- 관련 연구: trace 길이, 탐색, 잠재 표현, SFT/RL 역할에 관한 기존 연구와 차별점
- 식별 이론: nonnegative rank와 조건부 독립을 이용한 계층 복원 증명
- support 분석: SFT 비식별성과 RL reward enrichment의 정식 정리
- 실험 세부: 합성 데이터 생성, SFT/RL 설정, 재주입 개입과 장기 수렴
- 구체적 예: 대수 reasoning에서 skill, routing, local witness 해석
- 표현 분석: sparse autoencoder와 skill 표현 분석
- 민감도: RL hyperparameter 변화에 대한 결과 점검

## 번역 시 주의

원문의 HTML 수식 일부는 접근성 변환 과정에서 기호가 생략되어 보일 수 있습니다. 수식 번호, 정확한 확률 분포 정의와 증명은 [원문 HTML](https://arxiv.org/html/2606.18089v2) 또는 [PDF](https://arxiv.org/pdf/2606.18089)를 확인하세요.
