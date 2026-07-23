# Thinking to Recall: 추론과 파라메트릭 지식 회상

작성일: 2026-07-23

## 출처와 작업 범위

- 입력 URL: [https://share.google/FfvIyuh2tx7vXXvUe](https://share.google/FfvIyuh2tx7vXXvUe)
- 최종 확인 URL: [https://discuss.pytorch.kr/t/thinking-to-recall-llm-feat-google-colm-2026/11271](https://discuss.pytorch.kr/t/thinking-to-recall-llm-feat-google-colm-2026/11271)
- 페이지 제목: `Thinking to Recall: 추론이 어떻게 LLM의 잠든 지식을 깨우는지에 대한 연구 (feat. Google, COLM 2026) - 읽을거리&정보공유 - PyTorchKR`
- 원문 언어: 한국어
- 접근일: 2026-07-23
- PyTorchKR 게시 정보: 9bow(박정환), 2026-07-22 21:30, 태그 `reasoning`, `factuality`, `paper`, `llm`, `google`, `hallucination`, `chain-of-thought`
- 원문 논문: [Thinking to Recall: How Reasoning Unlocks Parametric Knowledge in LLMs](https://arxiv.org/abs/2603.09906)
- Google Research 블로그: [Thinking to recall: How reasoning unlocks parametric knowledge in LLMs](https://research.google/blog/thinking-to-recall-how-reasoning-unlocks-parametric-knowledge-in-llms/)
- COLM 2026 accepted paper 확인: [COLM 2026 Accepted Papers](https://colmweb.org/AcceptedPapers.html)
- 번역/재구성 자료: [translation.ko.md](translation.ko.md)

이 폴더는 PyTorchKR 글과 원 논문, Google Research 블로그를 바탕으로 추론이 단순 사실 질문에서 LLM의 파라메트릭 지식 회상을 어떻게 돕는지 학습할 수 있게 정리한다. 원문이 한국어이므로 `translation.ko.md`에는 원문 구조를 따른 교정·재구성본을 제공한다.

## 한눈에 보기

이 연구는 "단순 사실 질문에도 왜 reasoning 또는 chain-of-thought가 도움이 되는가?"라는 질문을 다룬다. Mary Engle Pennington의 명예의 전당 헌액 연도처럼 단일 홉 사실 질문은 계산이나 논리 분해가 필요하지 않아 보인다. 모델이 그 사실을 가중치 안에 알고 있으면 답하고, 모르면 틀릴 것처럼 보인다.

그러나 논문은 추론을 켜면 모델이 추론 OFF 상태에서는 사실상 꺼내지 못하던 정답을 더 자주 회상한다고 보고한다. 핵심 설명은 두 가지다.

1. **연산 버퍼**: 추론 토큰을 생성하는 동안 추가 forward pass가 생기고, 모델이 더 많은 latent computation을 수행한다.
2. **사실 프라이밍**: 모델이 관련 사실을 먼저 떠올리며 정답을 회상하기 쉬운 문맥적 다리를 만든다.

동시에 이 메커니즘은 위험하다. 중간 사실이 환각이면 최종 답도 더 자주 틀린다. 따라서 좋은 reasoning은 길기만 한 reasoning이 아니라, 검증 가능한 사실을 포함하고 환각이 적은 reasoning이어야 한다.

## 기초 개념

### 파라메트릭 지식

파라메트릭 지식은 모델이 외부 검색 없이 가중치 안에 저장하고 있는 지식이다. closed-book QA에서 모델은 검색 도구나 문서를 보지 않고 자신의 파라미터에 담긴 정보만으로 답해야 한다.

### 단일 홉 사실 질문

단일 홉 질문은 여러 단계를 거쳐 추론하지 않아도 되는 사실 질문이다. 예를 들어 "어떤 인물이 어느 해에 상을 받았는가?"처럼 답이 하나의 사실로 끝나는 질문이다.

### Chain-of-Thought

Chain-of-Thought(CoT)는 모델이 최종 답을 내기 전 중간 생각 또는 풀이 과정을 생성하게 하는 방식이다. 수학, 코드, 다중 홉 질의응답에서는 문제를 단계적으로 분해하는 장점이 뚜렷하다. 이 연구의 특징은 분해할 단계가 거의 없는 사실 질문에서도 CoT가 이득을 준다는 점을 분석한 것이다.

### Reasoning ON/OFF

논문은 reasoning을 켜고 끌 수 있는 모델을 사용한다. 같은 모델에서 reasoning 모드만 바꾸면 파라메트릭 지식 자체는 거의 고정된 상태로 두고, reasoning trace가 회상에 주는 효과를 비교할 수 있다.

### pass@k

`pass@k`는 k개 답변 샘플 중 하나라도 정답이 있는지 보는 지표다. `pass@1`은 대표 답 하나의 정확도를 보지만, `pass@k`는 모델 출력 분포 어딘가에 정답 경로가 있는지 더 넓게 본다.

## 핵심 요약

- 논문은 Google Research, Technion, Tel Aviv University 연구진의 COLM 2026 accepted paper다.
- arXiv 기준 제출일은 2026-03-10이며, 논문 ID는 `2603.09906`이다.
- 실험 모델은 Gemini-2.5 Flash/Pro, Qwen3-32B이며, reasoning ON/OFF 비교가 가능하다.
- 데이터셋은 SimpleQA Verified와 EntityQuestions를 사용한다.
- reasoning ON은 모든 모델과 데이터셋에서 pass@k를 개선했다.
- 큰 k에서도 격차가 유지되거나 더 커져, reasoning이 단순한 top-1 sharpening을 넘어서 capability boundary를 넓힌다는 해석이 나온다.
- 복잡 질문 subset에서만 이득이 더 큰 것은 아니어서, 문제 분해보다 파라메트릭 회상 촉진이 핵심으로 보인다.
- 의미 없는 더미 문자열을 reasoning trace 길이만큼 넣어도 OFF보다 성능이 올라, 추가 토큰 생성 자체의 연산 버퍼 효과가 확인된다.
- 하지만 더미 길이를 무작정 늘리면 비단조적으로 악화될 수 있고, 자연스러운 reasoning 성능에는 도달하지 못한다.
- 자연스러운 reasoning trace의 핵심은 관련 사실을 먼저 회상하는 factual priming이다.
- 중간 사실 중 하나라도 환각이면 최종 답의 정확도가 크게 떨어진다.
- 여러 reasoning trajectory 중 검증 가능한 사실이 있고 환각이 없는 trace를 우선 선택하면 기대 정확도가 올라간다.

## 상세 정리

### 1. 연구 질문

기존 CoT 설명은 보통 과제 분해에 초점을 둔다. 수학 문제는 계산 단계를 나누고, 코드 생성은 설계와 구현을 나누며, 다중 홉 질문은 필요한 사실을 순서대로 연결한다. 하지만 단일 홉 사실 질문은 이런 설명이 잘 맞지 않는다.

이 연구는 reasoning이 "생각을 논리적으로 전개해서 답을 유도한다"는 좁은 의미를 넘어, 모델 내부 기억을 밖으로 꺼내는 장치일 수 있다고 본다.

### 2. 능력 경계 측정

논문은 `pass@k`를 사용해 모델의 지식 회상 경계를 본다. `pass@1`만 보면 가장 높은 확률의 답만 평가한다. 반면 `pass@k`는 여러 번 샘플링했을 때 정답이 한 번이라도 나오는지 보므로, 정답이 낮은 확률 꼬리에라도 존재하는지 확인할 수 있다.

결과적으로 reasoning ON은 OFF보다 더 많은 정답 경로를 출력 분포 안에 만들었다. 이는 reasoning이 단순히 이미 있는 정답의 순위를 올리는 것보다 더 넓은 효과를 낼 수 있음을 시사한다.

### 3. 연산 버퍼

연산 버퍼 가설은 reasoning trace의 내용이 아니라 길이와 생성 과정 자체가 도움이 된다는 설명이다. 자동회귀 모델은 토큰을 하나 생성할 때마다 새 forward pass를 수행한다. 따라서 더 긴 trace는 더 많은 계산 시간을 제공한다.

논문은 자연 reasoning trace를 의미 없는 반복 문자열로 바꿔도 성능이 OFF보다 높아지는지 테스트한다. 더미 trace가 효과를 보인다는 것은 의미 없는 추가 토큰 생성만으로도 latent computation이 늘어 지식 회상에 도움이 될 수 있음을 보여 준다.

하지만 이 효과는 무제한이 아니다. 더미 길이를 늘리면 일정 지점까지는 좋아지지만 이후 정체되거나 악화된다. 또한 자연 reasoning의 성능에는 도달하지 못한다. 즉 계산 시간은 필요조건에 가깝지만 충분조건은 아니다.

### 4. 사실 프라이밍

자연 reasoning trace를 보면 모델은 논리 증명을 쓰기보다 관련 사실을 떠올리는 경우가 많다. 예를 들어 "네팔의 10대 국왕"을 물으면 이전 국왕들을 떠올리면서 정답으로 이어지는 문맥을 만든다.

논문은 trace에서 구체적 사실만 추출하고, filler나 검색 계획, 정답을 직접 드러내는 문장을 제거한 뒤, 그 사실 목록만 조건으로 넣어 다시 답을 생성한다. 그 결과 사실 목록만으로도 reasoning 이득의 상당 부분이 회복된다.

이는 모델이 자기 자신에게 관련 사실을 검색해 주는 generative self-retrieval을 수행한다는 해석으로 이어진다.

### 5. 환각의 함정

사실 프라이밍은 강력하지만 취약하다. 모델이 중간에 잘못된 사실을 생성하면 그 사실이 다음 문맥을 오염시키고, 최종 답도 틀릴 가능성이 높아진다.

논문은 reasoning trace에서 추출한 중간 사실을 검색 가능 verifier로 검증했다. 결과적으로 clean trace는 hallucinated trace보다 최종 정답률이 높았다. 같은 질문 안에서 비교해도 환각이 섞인 trace는 체계적으로 더 나빴다.

### 6. 신뢰도 향상 방향

연구의 실전적 제안은 test-time selection과 process reward다. 여러 reasoning trajectory를 생성한 뒤, 사실을 포함하고 그 사실이 검증 가능한 trace를 우선 선택하면 기대 정확도가 올라간다.

훈련 단계에서는 factual intermediate step을 장려하는 process reward를 설계할 수 있다. 단순히 긴 reasoning을 보상하는 것이 아니라, 사실적으로 뒷받침되는 reasoning을 보상해야 한다.

## 용어 정리

| 용어 | 의미 |
| --- | --- |
| Parametric knowledge | 모델 가중치 안에 저장된 지식 |
| Closed-book QA | 외부 검색이나 문서 없이 답하는 질의응답 |
| Single-hop question | 하나의 사실로 답할 수 있는 질문 |
| Reasoning trace | 최종 답 전 생성되는 중간 생각 또는 풀이 과정 |
| Chain-of-Thought | 단계별 사고 과정을 생성하게 하는 prompting/학습 방식 |
| R-LLM | reasoning을 생성하도록 학습되었거나 reasoning 모드를 가진 LLM |
| pass@k | k개 샘플 중 하나 이상이 정답일 확률 |
| Capability boundary | 모델 출력 분포 안에서 도달 가능한 능력의 경계 |
| Computational buffer | 추가 토큰 생성이 latent computation 시간을 제공하는 효과 |
| Factual priming | 관련 사실을 먼저 생성해 목표 사실 회상을 쉽게 하는 효과 |
| Generative self-retrieval | 모델이 스스로 관련 사실을 생성해 문맥에 넣는 회상 방식 |
| Hallucination | 사실이 아닌 내용을 그럴듯하게 생성하는 현상 |
| Process reward | 최종 답뿐 아니라 중간 과정의 품질을 보상하는 신호 |

## 실습 학습 가이드

- [01_foundations.ipynb](01_foundations.ipynb): `pass@k`와 reasoning effectiveness `Omega`를 계산하고, reasoning ON/OFF가 능력 경계에 주는 차이를 시각 없이 표로 확인한다.
- [02_practice.ipynb](02_practice.ipynb): 더미 trace 길이에 따른 computational buffer 효과를 toy 모델로 시뮬레이션한다.
- [03_advanced.ipynb](03_advanced.ipynb): 사실 프라이밍, 환각 감사, test-time selection을 작은 데이터로 구현한다.

## 다음 학습 경로

1. Google Research 블로그와 arXiv 논문의 figure를 보며 pass@k 곡선과 `Omega` 정의를 직접 확인한다.
2. SimpleQA Verified, EntityQuestions처럼 closed-book factuality를 평가하는 데이터셋 구조를 비교한다.
3. CoT의 이득을 decomposition, computational buffer, factual priming으로 나눠 실제 모델 로그에서 태깅해 본다.
4. Fact verifier가 틀릴 때 test-time selection이 어떻게 실패하는지 실험한다.
5. Process reward를 설계할 때 "긴 사고"가 아니라 "검증 가능한 중간 사실"을 보상하는 방법을 연구한다.
