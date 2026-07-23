# Understanding Reasoning from Pretraining to Post-Training 한국어 번역 요약

작성일: 2026-07-23

## 원문 정보

- AlphaXiv URL: [https://www.alphaxiv.org/abs/2607.16097](https://www.alphaxiv.org/abs/2607.16097)
- AlphaXiv Overview: [https://www.alphaxiv.org/overview/2607.16097](https://www.alphaxiv.org/overview/2607.16097)
- arXiv URL: [https://arxiv.org/abs/2607.16097](https://arxiv.org/abs/2607.16097)
- PDF URL: [https://pdfs.assets.alphaxiv.org/2607.16097v1.pdf](https://pdfs.assets.alphaxiv.org/2607.16097v1.pdf)
- 제목: `Understanding Reasoning from Pretraining to Post-Training`
- 원문 언어: 영어
- 접근일: 2026-07-23
- 제출일: 2026-07-17
- 저자: Jingyan Shen, Ang Li, Salman Rahman, Yifan Sun, Micah Goldblum, Matus Telgarsky, Pavel Izmailov

이 문서는 AlphaXiv와 arXiv에서 확인한 논문 구조를 따라 작성한 한국어 학습용 번역 요약이다. 원문 전문을 그대로 복제하지 않고, 핵심 섹션 흐름과 수식·수치·용어를 보존해 재구성했다.

## 초록

강화학습(RL)은 복잡한 추론 과제에서 대규모 언어 모델(LLM)을 개선하는 핵심 수단이 되었다. 하지만 RL 포스트 트레이닝은 그 앞에 있는 사전학습과 분리되어 연구되는 경우가 많았다. 이 때문에 두 질문이 남아 있다.

첫째, 모델 크기와 데이터 같은 사전학습 선택은 RL compute의 수익률을 어떻게 바꾸는가? 둘째, RL은 실제로 모델 정책에 무엇을 하는가?

표준 LLM 환경에서 이 질문을 연구하기는 어렵다. 사전학습 말뭉치는 크고 통제하기 어렵고, 사전학습과 RL의 영향을 분리하기 어렵고, 두 단계를 모두 체계적으로 sweep하기에는 compute 비용이 너무 크다.

논문은 이 문제를 해결하기 위해 체스를 통제 가능한 테스트베드로 사용한다. 인간 체스 게임으로 5M-1B 파라미터 언어 모델을 사전학습하고, 합성 reasoning trace로 SFT를 수행한 뒤, 정답 보상이 검증 가능한 체스 퍼즐에서 RL을 실행한다.

이 프레임워크에서 post-RL 성능은 사전학습 loss로 잘 예측되고, RL reward 곡선의 기울기는 사전학습 토큰 수와 거의 선형적으로 개선된다. 또한 RL은 SFT 정책을 단순히 날카롭게 만드는 것만이 아니다. 쉬운 퍼즐에서는 SFT가 이미 선호한 정답 수를 강화하지만, 어려운 퍼즐에서는 SFT에서 거의 보이지 않던 정답 수를 표면으로 끌어올리기도 한다.

마지막으로 수학 도메인 텍스트로 사전학습한 1B 언어 모델에서도 유사한 패턴이 확인된다. 더 오래 사전학습한 체크포인트는 더 높은 post-RL 성능에 도달하고 RL에서 더 빨리 개선된다. 논문은 사전학습과 RL 사이의 접점을 정량적으로 설명하는 틀과, 전체 pretraining-to-post-training 파이프라인에서 추론을 연구할 수 있는 통제된 테스트베드를 제공한다.

## 1. 서론

표준 LLM 학습 파이프라인은 대규모 사전학습 이후 SFT와 RL 같은 포스트 트레이닝을 수행한다. 최근에는 compute를 어디에 더 투자해야 하는지에 대한 두 관점이 갈라지고 있다.

하나는 더 큰 모델, 더 많은 데이터, 더 긴 사전학습으로 강한 pretrained prior를 만드는 관점이다. 다른 하나는 환경 상호작용과 결과 기반 보상으로 직접 경험을 쌓게 하는 RL 중심 관점이다.

LLM 추론에서는 완전한 experience-only 접근이 아직 어렵다. 행동 공간이 매우 크고, 무작위 초기 정책이 받을 수 있는 보상은 극도로 희소하기 때문이다. 따라서 실제 RL은 사전학습된 prior에서 시작한다. 중요한 질문은 "prior가 필요한가"가 아니라 "얼마나 좋은 prior가 필요한가"이다.

논문은 체스를 통해 이 질문을 통제한다. 체스는 행동 공간이 명확하고, 각 수를 검증할 수 있으며, 데이터 품질과 양을 조절하기 쉽다. 그래서 사전학습 규모와 RL compute를 동시에 바꾸는 실험이 가능하다.

## 2. 프레임워크: 추론 테스트베드로서의 체스

논문의 테스트베드는 세 단계로 구성된다.

| 단계 | 내용 |
| --- | --- |
| 사전학습 | Lichess 인간 게임 이동 시퀀스로 next-token prediction 학습 |
| SFT | 체스 퍼즐에 대해 합성 reasoning trace와 정답 continuation 학습 |
| RL | 검증 가능한 퍼즐 환경에서 GRPO로 최적화 |

### 체스 표현

각 수는 기물, 출발 칸, 도착 칸, 특수 플래그로 표현된다. 유효한 수열 prefix는 하나의 체스판 상태를 결정한다. 논문은 전체 vocabulary 크기를 81로 둔다.

### 합성 reasoning trace

논문은 체스 모델의 chain-of-thought를 자연어가 아니라 체스 수열로 만든다. 입력 board state에서 proposal policy가 여러 continuation을 샘플링하고, 공통 prefix를 합쳐 검색 트리를 만든 뒤, 루트-리프 경로를 depth-first 순서로 직렬화한다. 모델은 이 trace를 생성한 뒤 정답 continuation에 commit하도록 SFT된다.

### RL 보상

RL은 binary outcome reward를 사용한다. 모델이 solution line의 모든 solver move를 정확히 맞히면 보상 1, 한 수라도 틀리면 보상 0이다. 따라서 퍼즐 풀이를 multi-step interactive decision problem으로 볼 수 있다.

### 실험 설정

논문은 Lichess 2022 Blitz/Rapid 인간 게임에서 54B-token 사전학습 corpus를 만들고, 156K개의 품질 필터링된 Lichess 퍼즐을 포스트 트레이닝에 사용한다. 평가는 1,480개의 tactical puzzle benchmark에서 수행된다. 모델은 dense Qwen3 기반 구조이며 5M부터 1B까지 10개 scale을 사용한다.

## 3. Scaling Analysis: 사전학습에서 포스트 트레이닝으로

논문은 두 질문을 분석한다.

1. 고정 compute에서 사전학습과 RL compute를 어떻게 나눠야 하는가?
2. 모델 크기, 토큰 수, 사전학습 loss 같은 pretraining property가 RL scaling을 예측할 수 있는가?

### Pre-RL scaling

사전학습 compute를 6.5e16부터 6.5e19 FLOPs까지 sweep하고, 모델 크기도 10개 scale로 바꾼다. 결과적으로 같은 FLOPs에서도 최적의 parameter-token allocation이 존재하며, 이 optimum은 인간 게임 validation loss와 puzzle pass@1/pass@16을 잘 따라간다.

### Compute allocation

총 compute와 모델 크기가 고정되어 있으면, 더 오래 사전학습할수록 초기화는 좋아지지만 RL에 쓸 compute는 줄어든다. 논문은 각 선택의 최종 성능을 비교해 fixed-budget frontier를 만든다.

관찰 결과 pass@1에서는 RL이 일관되게 성능을 올렸고, frontier에서 RL compute 비율은 총 compute가 커질수록 증가했다. 예를 들어 20M 모델에서는 frontier상의 RL 비율이 약 5%에서 32%로 커졌다.

반면 pass@16에서는 RL 이득이 작거나 mixed했다. 여러 후보 중 하나라도 맞는 능력은 추가 RL보다 추가 사전학습에서 더 이득을 볼 때가 있었다.

### Joint pretraining-RL scaling law

논문은 초기 비포화 구간의 RL 곡선을 log-linear하게 근사한다.

```text
R_N,T(C) = R_ref_N,T + B_N,T * (log10(C) - log10(C_ref))
```

이후 `R_ref`와 `B`를 사전학습 특성으로 예측한다. 낮은 사전학습 validation loss는 특정 RL compute에서 높은 pass@1 성능을 강하게 예측한다. 또한 RL slope `B`는 `log10(T)`와 양의 상관을 보인다. 모델 크기 `N`도 보정 역할을 하지만, 논문에서는 토큰 수의 계수가 더 컸다.

최종적으로 논문은 다음 형태의 scaling law를 제시한다.

```text
R(C_RL, N, T) =
  f(L_pt(N, T)) + g(N, T) * (log10(C_RL) - log10(C_ref))
```

이 식은 사전학습 loss와 RL compute를 연결해, 특정 훈련 recipe의 post-RL reward를 예측하는 용도로 사용된다.

## 4. RL 동안 정책은 어떻게 변하는가

논문은 RL이 SFT 정책을 단순히 temperature scaling처럼 날카롭게 만드는지 확인한다. 평균적으로는 sharpening 신호가 있지만, 상태별로 보면 설명력이 충분하지 않다. 그래서 논문은 정답 수가 SFT와 RL 정책의 top-k 집합 사이에서 어떻게 이동하는지 분석한다.

### 세 가지 주요 변화

| 유형 | 의미 |
| --- | --- |
| Ground-truth amplification | 정답 수가 이미 SFT top-k 안에 있고 RL이 더 강화한다. |
| Tail discovery | 정답 수가 SFT에서는 낮은 확률 꼬리에 있었지만 RL 후 top-k로 올라온다. |
| Wrong-mode amplification | 정답은 top-k 밖에 남아 있고, 기존의 틀린 고확률 후보가 더 강화된다. |

쉬운 퍼즐에서는 ground-truth amplification이 지배적이다. 어려운 퍼즐에서는 tail discovery와 wrong-mode amplification이 모두 증가한다. 따라서 RL은 correct mode를 강화하고 일부 correct tail move를 발견하지만, harder task에서는 wrong mode도 강화한다.

이 결과는 RL이 pass@1을 개선하면서도 pass@k를 일관되게 개선하지 못하는 이유를 설명한다. 단일 최고 후보를 맞히는 능력과 후보 coverage를 넓게 유지하는 능력은 다르다.

### CoT search dynamics

논문은 reasoning trace를 prefix tree로 복원해 RL 전후의 search behavior를 분석한다. RL은 주로 탐색의 폭을 넓힌다. width-to-depth ratio와 branching factor가 증가하고, 모델의 자기 수와 상대 수 예측 품질도 개선된다.

하지만 최대 탐색 깊이는 크게 늘지 않는다. 특히 SFT에서 본 것보다 훨씬 깊은 continuation이 필요한 경우에는 여전히 어려움을 겪는다. 이는 RL이 candidate generation과 selection은 빠르게 개선하지만 long-horizon search 자체를 자동으로 크게 늘리지는 못한다는 해석으로 이어진다.

## 5. 수학 도메인 전이

체스 결과가 너무 특수한지 확인하기 위해 논문은 1B OLMo-2 모델을 수학 도메인 텍스트로 사전학습한다. corpus는 Nemotron-CC-Math-v1과 Dolma3 혼합이며, 10B부터 200B 토큰 사이의 14개 checkpoint를 만든다.

이후 NuminaMath-CoT로 SFT하고, GSM8K, MATH, DeepScaler 기반 학습 문제에서 RL을 수행한다. 결과는 체스와 비슷했다. 낮은 사전학습 loss는 높은 post-RL 성능을 예측했고, pretraining token 수가 많을수록 RL reward curve의 slope가 커졌다.

## 6. 관련 연구

논문은 RL for reasoning, scaling law, compute allocation 연구와 연결된다. 기존 연구는 RL이 base model의 기존 reasoning pattern을 강화한다는 관점, RL이 pretrained skill을 조합해 새 능력을 만든다는 관점, 두 현상이 문제 영역에 따라 모두 나타난다는 관점을 제시했다.

이 논문은 체스라는 통제된 환경에서 각 수의 정책 분포와 reasoning trace를 직접 볼 수 있게 하여, RL의 효과를 난이도별로 나누어 분석한다.

## 7. 결론

논문은 체스를 테스트베드로 사용해 사전학습이 RL dynamics에 미치는 영향과 RL이 상속받은 정책을 어떻게 바꾸는지 연구했다. 주요 결론은 다음과 같다.

- 사전학습 loss는 post-RL 성능 수준을 예측한다.
- 사전학습 데이터 규모는 RL improvement slope와 밀접하게 연결된다.
- 총 compute가 커질수록 최적 frontier에서 RL 비율은 증가하는 경향이 있다.
- 그러나 약한 사전학습 checkpoint에서 너무 일찍 RL을 시작하면 이득이 제한된다.
- RL은 균일한 sharpening이 아니며, 쉬운 문제에서는 정답 강화, 어려운 문제에서는 tail discovery와 wrong-mode amplification을 동시에 보인다.
- 수학 도메인에서도 유사한 패턴이 관찰되어 체스 밖으로의 확장 가능성을 제시한다.

후속 연구 방향은 언제 사전학습에서 RL로 전환할지, wrong-mode amplification을 어떻게 줄일지, 고정된 두 단계 recipe 대신 사전학습과 RL을 더 유연하게 섞는 전략을 어떻게 설계할지에 있다.
