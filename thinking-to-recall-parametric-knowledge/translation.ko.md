# Thinking to Recall PyTorchKR 글 한국어 재구성본

작성일: 2026-07-23

## 원문 정보

- 입력 URL: [https://share.google/FfvIyuh2tx7vXXvUe](https://share.google/FfvIyuh2tx7vXXvUe)
- 최종 확인 URL: [https://discuss.pytorch.kr/t/thinking-to-recall-llm-feat-google-colm-2026/11271](https://discuss.pytorch.kr/t/thinking-to-recall-llm-feat-google-colm-2026/11271)
- 원문 제목: `Thinking to Recall: 추론이 어떻게 LLM의 잠든 지식을 깨우는지에 대한 연구 (feat. Google, COLM 2026)`
- 원문 언어: 한국어
- 접근일: 2026-07-23
- 원문 논문: [https://arxiv.org/abs/2603.09906](https://arxiv.org/abs/2603.09906)
- Google Research 블로그: [https://research.google/blog/thinking-to-recall-how-reasoning-unlocks-parametric-knowledge-in-llms/](https://research.google/blog/thinking-to-recall-how-reasoning-unlocks-parametric-knowledge-in-llms/)

원문이 이미 한국어이므로 이 파일은 직역 번역이 아니라, PyTorchKR 글의 섹션 흐름을 유지한 교정·재구성 학습본이다. 원문의 의미와 수치를 보존하되, 전체 글을 그대로 복제하지 않고 학습자가 바로 복습할 수 있는 구조로 정리했다.

## Thinking to Recall 연구 소개

이 연구는 단순한 사실 질문에도 reasoning이 왜 도움이 되는지 묻는다. 일반적으로 CoT는 수학, 코드, 다중 홉 질문처럼 여러 단계가 필요한 문제에 어울린다고 생각한다. 그러나 이 논문은 계산이나 논리 분해가 거의 필요 없는 단일 홉 사실 질문에서도 reasoning을 켜면 모델이 더 많은 정답을 회상한다는 점을 보인다.

핵심 주장은 다음과 같다. LLM은 어떤 사실을 파라미터 안에 가지고 있어도, 곧바로 답하라고 하면 그 사실을 꺼내지 못할 수 있다. reasoning trace는 이 잠든 지식을 회상하도록 돕는 장치로 작동한다.

연구진은 Google Research, Technion, Tel Aviv University 소속이며, 논문은 COLM 2026 accepted paper로 확인된다.

## 배경: 추론은 복잡한 문제에만 필요한가

CoT는 복잡한 문제를 작은 단계로 나누어 해결하는 데 효과적이다. 하지만 다음과 같은 질문에는 분해할 논리 단계가 거의 없다.

```text
Mary Engle Pennington은 몇 년도에 National Inventors Hall of Fame에 헌액되었는가?
```

이 질문은 모델의 가중치 안에 사실이 있으면 맞히고, 없으면 틀리는 문제처럼 보인다. 그래서 reasoning이 도움이 된다는 사실은 직관적이지 않다.

논문의 발상 전환은 reasoning을 "문제 풀이 과정"으로만 보지 않는 것이다. reasoning은 모델이 자기 내부의 기억을 더 잘 탐색하게 만드는 생성 과정일 수 있다.

## 기존 관점과 다른 점

기존 연구는 주로 복잡한 문제에서 CoT 또는 RL로 학습된 reasoning model이 얼마나 성능을 올리는지 보았다. 이런 경우 이득은 이미 접근 가능한 정답의 확률을 더 높이는 probability sharpening으로도 설명될 수 있다.

이 논문은 두 가지 방식으로 문제를 분리한다.

1. reasoning ON/OFF가 가능한 같은 모델을 사용해 파라메트릭 지식 자체를 고정한다.
2. `pass@1`만 보지 않고 큰 `k`까지 포함한 `pass@k`로 모델 출력 분포 안의 정답 가능성을 본다.

이렇게 하면 reasoning이 단순히 가장 그럴듯한 답의 순위를 바꾸는지, 아니면 정답에 도달 가능한 경계 자체를 넓히는지 관찰할 수 있다.

## 추론은 파라메트릭 지식의 경계를 넓힌다

실험은 Gemini-2.5 Flash, Gemini-2.5 Pro, Qwen3-32B를 대상으로 한다. 데이터셋은 SimpleQA Verified와 EntityQuestions다. 둘 다 closed-book QA이며, 외부 검색 없이 모델의 내부 지식으로 답해야 한다.

결과는 일관된다. reasoning을 켠 경우 pass@k가 reasoning을 끈 경우보다 높다. 특히 큰 k에서도 격차가 유지되거나 더 커진다. 이는 reasoning ON이 단순히 top-1 답을 다듬는 것이 아니라, 모델 출력 분포 안에 없던 정답 경로를 열어 주는 효과가 있음을 시사한다.

논문은 reasoning 효과를 요약하기 위해 `Omega`라는 지표도 정의한다. 이 지표는 pass@k의 상대 개선을 큰 k에 더 큰 가중치로 평균한다. PyTorchKR 글은 강한 모델일수록 `Omega`가 작아지는 경향을 설명한다. 더 강한 모델은 reasoning 없이도 지식을 잘 꺼내므로 reasoning이 보완할 여지가 작다는 해석이다.

또한 SimpleQA Verified에서 복잡 질문과 단순 질문을 나눠 비교했을 때, 복잡 질문에서만 reasoning 이득이 커지지는 않았다. 따라서 이 실험의 핵심 이득은 문제 분해보다는 회상 촉진으로 보는 편이 더 자연스럽다.

## 메커니즘 1: 연산 버퍼

첫 번째 메커니즘은 computational buffer다. 모델이 reasoning trace를 생성하면 토큰마다 추가 forward pass가 일어난다. 이 과정은 의미 있는 사고가 아니더라도 모델에게 더 많은 latent computation 시간을 줄 수 있다.

논문은 자연 reasoning trace를 의미 없는 반복 문자열로 대체한다. 예를 들어 `Let me think` 같은 더미 문장을 원래 trace 길이에 맞춰 반복한 뒤, 최종 답을 생성하게 한다.

결과적으로 의미 없는 더미 trace도 reasoning OFF보다 성능을 높인다. PyTorchKR 글은 SimpleQA Verified와 EntityQuestions에서 pass@1이 더미 trace 조건으로 상승한 수치를 소개한다. 이는 추가 연산 시간 자체가 회상에 도움이 된다는 강한 근거다.

하지만 한계도 있다. 더미 trace를 너무 길게 만들면 성능이 계속 오르지 않고 정체하거나 오히려 하락한다. 또한 순수 더미 연산만으로는 자연 reasoning trace의 성능에 도달하지 못한다. 따라서 연산 버퍼는 reasoning 이득의 일부만 설명한다.

## 메커니즘 2: 사실 프라이밍

두 번째 메커니즘은 factual priming이다. 자연 reasoning trace를 보면 모델이 논리적 증명을 쓰기보다, 질문과 관련된 사실을 먼저 떠올리는 경우가 많다.

인간 인지의 spreading activation처럼, 어떤 개념을 떠올리면 관련 개념들이 더 쉽게 활성화될 수 있다. 논문은 LLM도 비슷하게 관련 사실을 먼저 생성하면서 목표 사실로 가는 의미적 다리를 놓는다고 해석한다.

이를 검증하기 위해 연구진은 reasoning trace에서 구체적인 사실만 추출한다. 이때 질문에 이미 있는 정보, 단순 filler, 검색 계획, 정답을 직접 드러내는 문장은 제거한다. 그런 다음 추출된 사실 목록만 제공하고 답을 다시 생성한다.

결과적으로 사실 목록은 reasoning 이득의 상당 부분을 회복한다. reasoning을 끈 상태에서도 관련 사실을 추가 문맥으로 제공하면 성능이 오른다. 이는 사실 자체가 회상을 돕는다는 점을 보여 준다.

## 사례: 네팔의 10대 국왕

PyTorchKR 글은 "네팔의 10대 국왕은 누구인가?" 사례를 소개한다. reasoning을 끄면 모델은 틀린 답을 내지만, reasoning을 켜면 이전 국왕들을 차례로 떠올리다가 정답에 도달한다.

중요한 점은 사실 목록에서 정답을 직접 드러내는 문장을 제거해도, 앞선 관련 사실들만으로 정답 회상이 가능했다는 것이다. 이는 factual priming이 단순 정답 누출이 아니라 관련 지식 활성화로 작동할 수 있음을 보여 준다.

## 자기 회상의 함정: 환각

Factual priming은 모델이 직접 중간 사실을 생성한다는 점에서 위험하다. 중간 사실이 틀리면 그 잘못된 문맥이 최종 답에도 영향을 준다.

논문은 reasoning trace에서 추출한 중간 사실을 검색 가능한 verifier로 독립 검증한다. 그리고 모든 중간 사실이 맞는 clean trace와 하나라도 틀린 hallucinated trace를 나눈다.

결과적으로 clean trace는 hallucinated trace보다 최종 정답률이 훨씬 높다. 같은 질문 안에서 비교해도 환각이 섞인 trace가 체계적으로 나쁘다. 따라서 reasoning은 사실을 떠올리면 도움이 되지만, 잘못된 사실을 떠올리면 오히려 해로울 수 있다.

## 분석에서 실전으로

논문은 test-time selection을 제안한다. 한 질문에 대해 여러 reasoning trajectory를 생성한 뒤, 사실을 포함한 trace, 더 나아가 모든 사실이 검증된 trace를 우선 선택한다.

PyTorchKR 글은 이 선택 전략이 SimpleQA Verified와 EntityQuestions에서 기대 정확도를 높였다고 정리한다. 특히 "Only Correct Facts" 조건이 단순 전체 샘플보다 더 나은 결과를 보인다.

훈련 단계에서는 이를 process reward로 구현할 수 있다. 최종 답만 맞히는 모델이 아니라, 중간에 사실적으로 뒷받침되는 단계를 생성하는 모델을 보상하는 방향이다.

## 결론

이 연구는 reasoning이 단순한 문제 분해 도구가 아니라, LLM 내부의 파라메트릭 지식을 드러내는 회상 장치일 수 있음을 보여 준다.

핵심 메커니즘은 두 가지다.

- 추가 토큰 생성이 더 많은 latent computation을 제공하는 연산 버퍼
- 관련 사실 생성이 목표 사실 회상을 돕는 사실 프라이밍

하지만 reasoning trace의 중간 사실이 환각이면 최종 답도 더 불안정해진다. 따라서 앞으로의 연구와 학습 레시피는 단순히 더 길게 생각하게 만드는 것보다, 검증 가능한 사실을 정확하게 떠올리는 reasoning을 장려해야 한다.

## 학습자 체크포인트

- `pass@1`과 `pass@k`의 차이를 설명할 수 있는가?
- reasoning ON/OFF 비교가 왜 파라메트릭 지식을 고정하는 데 도움이 되는가?
- 더미 trace 실험이 computational buffer를 어떻게 분리하는가?
- factual priming이 단순 정답 누출과 어떻게 다른가?
- 중간 사실 환각이 최종 답을 왜 오염시키는가?
- process reward를 설계한다면 어떤 중간 단계를 보상해야 하는가?
