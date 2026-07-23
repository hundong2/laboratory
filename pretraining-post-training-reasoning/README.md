# 사전학습에서 포스트 트레이닝까지의 추론 이해

작성일: 2026-07-23

## 출처와 작업 범위

- 입력 URL: [https://www.alphaxiv.org/abs/2607.16097](https://www.alphaxiv.org/abs/2607.16097)
- 최종 확인 URL: [https://www.alphaxiv.org/abs/2607.16097](https://www.alphaxiv.org/abs/2607.16097)
- AlphaXiv Overview: [https://www.alphaxiv.org/overview/2607.16097](https://www.alphaxiv.org/overview/2607.16097)
- arXiv: [https://arxiv.org/abs/2607.16097](https://arxiv.org/abs/2607.16097)
- PDF: [https://pdfs.assets.alphaxiv.org/2607.16097v1.pdf](https://pdfs.assets.alphaxiv.org/2607.16097v1.pdf)
- 페이지 제목: `Understanding Reasoning from Pretraining to Post-Training`
- 원문 언어: 영어
- 접근일: 2026-07-23
- arXiv 제출일: 2026-07-17
- 저자: Jingyan Shen, Ang Li, Salman Rahman, Yifan Sun, Micah Goldblum, Matus Telgarsky, Pavel Izmailov
- 주제 분류: Machine Learning(cs.LG), Artificial Intelligence(cs.AI), Computation and Language(cs.CL)
- DOI: [10.48550/arXiv.2607.16097](https://doi.org/10.48550/arXiv.2607.16097)
- 원문 연결 자료: 모델·데이터 [huggingface.co/pavelslab-nyu/pre2post-chess](https://huggingface.co/pavelslab-nyu/pre2post-chess), 코드 [github.com/pavelslab-nyu/pre2post-chess](https://github.com/pavelslab-nyu/pre2post-chess)
- 번역 자료: [translation.ko.md](translation.ko.md)

이 폴더는 논문의 핵심을 한국어 학습 자료로 재구성한다. 일반 웹사이트 URL 입력이므로 `translation.ko.md`를 함께 만들었으며, 저작권이 있는 원문은 전문 복제하지 않고 구조를 보존한 번역 요약으로 정리했다.

## 한눈에 보기

이 논문은 "사전학습이 RL 포스트 트레이닝의 성과와 학습 속도를 어떻게 결정하는가"를 체스라는 통제 가능한 환경에서 분석한다. 표준 LLM 학습 파이프라인을 체스에 옮겨, 인간 체스 게임으로 사전학습하고, 합성 reasoning trace로 SFT를 수행한 뒤, 정답 검증이 가능한 체스 퍼즐 환경에서 RL을 적용한다.

핵심 결론은 세 가지다.

1. RL 이후 성능은 사전학습 검증 손실로 강하게 예측된다.
2. RL 보상 곡선의 기울기, 즉 RL compute를 늘렸을 때 성능이 좋아지는 속도는 사전학습 토큰 수와 양의 상관을 보인다.
3. RL은 단순히 SFT 정책을 균일하게 sharpen하지 않는다. 쉬운 퍼즐에서는 이미 선호하던 정답 수를 더 강화하고, 어려운 퍼즐에서는 낮은 확률 꼬리에 있던 정답 수를 끌어올리기도 하지만, 동시에 잘못된 유력 후보를 강화할 수도 있다.

## 기초 개념

### Pretraining

사전학습은 모델이 대규모 데이터에서 다음 토큰을 예측하도록 학습하는 단계다. 이 논문에서는 자연어 대신 인간 체스 게임의 이동 시퀀스를 사용한다. 각 수는 기물, 출발 칸, 도착 칸, 특수 플래그 같은 토큰으로 직렬화된다.

### Post-Training

포스트 트레이닝은 사전학습 모델을 특정 목적에 맞게 다듬는 단계다. 대표적으로 SFT와 RL이 있다. 이 논문은 SFT 이후 검증 가능한 보상을 쓰는 RL이 추론 성능을 어떻게 바꾸는지 본다.

### SFT와 Synthetic Reasoning Trace

SFT는 정답이 있는 데이터를 따라 하도록 모델을 학습시키는 단계다. 논문은 단순히 정답 수만 학습시키지 않고, 여러 가능한 게임 전개를 트리처럼 직렬화한 합성 chain-of-thought를 먼저 생성한 뒤 최종 수를 선택하도록 한다. 체스에서는 이 reasoning trace가 자연어가 아니라 체스 이동 토큰으로 표현된다.

### RL with Verifiable Rewards

검증 가능한 보상을 쓰는 RL은 모델 출력이 정답인지 자동으로 판정할 수 있는 환경에서 강화학습을 수행한다. 체스 퍼즐에서는 각 단계의 최선 수가 정해져 있으므로, 모델이 전체 solution line을 한 번도 틀리지 않고 따라가면 보상 1, 한 수라도 틀리면 보상 0을 준다.

### pass@1과 pass@k

`pass@1`은 모델의 한 번의 대표 답이 맞는지 보는 지표다. `pass@k`는 여러 샘플 중 하나라도 맞는지 보는 지표다. RL은 pass@1을 올리기 쉽지만, 후보 다양성이나 coverage가 줄면 pass@k는 잘 오르지 않거나 악화될 수 있다.

## 핵심 요약

- 연구 질문은 "얼마나 사전학습한 모델이 RL을 더 잘 받는가"와 "RL은 정책 내부에서 무엇을 바꾸는가"이다.
- 자연어 LLM 전체를 대상으로 compute sweep을 하는 것은 비싸고 통제도 어렵기 때문에, 체스를 reasoning 연구용 테스트베드로 사용했다.
- 파이프라인은 인간 체스 게임 사전학습, 합성 reasoning trace 기반 SFT, Lichess 퍼즐 기반 GRPO RL로 구성된다.
- 모델 크기는 5M부터 1B 파라미터까지이며, 사전학습과 RL compute 조합 36개를 스윕했다.
- 사전학습 검증 손실이 낮을수록 고정 RL compute에서 post-RL pass@1이 높았다.
- 사전학습 토큰 수가 많을수록 RL reward 곡선의 로컬 기울기가 대체로 커졌다.
- 고정 총 compute에서 초기에는 사전학습 비중이 중요하지만, 총 compute가 커질수록 RL에 할당하는 최적 비율이 증가하는 경향이 나타났다.
- 쉬운 문제에서 RL은 정답 후보를 강화하는 ground-truth amplification으로 작동했다.
- 어려운 문제에서 RL은 tail discovery와 wrong-mode amplification을 동시에 보였다.
- 수학 도메인의 1B OLMo-2 모델에서도 비슷한 예측 패턴이 관찰되어, 체스 밖으로도 일부 전이될 가능성을 제시했다.

## 상세 정리

### 1. 왜 체스인가

논문은 체스를 "최강 체스 엔진을 만들기 위한 대상"이 아니라 "LLM식 추론 학습을 통제해서 관찰하기 위한 실험실"로 사용한다. 체스는 행동 공간이 명확하고, 각 수의 품질을 엔진이나 퍼즐 정답으로 검증할 수 있으며, Lichess 같은 대규모 인간 게임 데이터가 존재한다.

자연어 추론 과제에서는 한 reasoning step의 정답 여부가 불명확하다. 반대로 체스 퍼즐에서는 특정 board state에서 올바른 move가 정의되어 있어, RL이 어떤 후보의 확률을 어떻게 바꾸는지 더 세밀하게 볼 수 있다.

### 2. 학습 파이프라인

논문은 LLM의 표준 학습 흐름을 체스로 축소한다.

| 단계 | 논문에서의 구현 | 학습 대상 |
| --- | --- | --- |
| Pretraining | 인간 체스 게임 이동 시퀀스 예측 | 합법적이고 그럴듯한 수의 분포 |
| SFT | 합성 reasoning trace와 정답 수 학습 | 가능한 변화를 탐색하고 최종 수를 고르는 형식 |
| RL | 정답 solution line 검증 보상으로 GRPO | 퍼즐을 끝까지 맞히는 정책 |

체스 수는 SAN/UCI 관례를 참고해 토큰화된다. 유효한 prefix는 하나의 board state를 결정하고, 모델은 다음 수를 autoregressive하게 예측한다.

### 3. 합성 reasoning trace

SFT 단계에서는 proposal model이 여러 가능한 게임 continuation을 샘플링한다. 공통 prefix를 합쳐 트리를 만들고, 그 루트-리프 경로를 depth-first 순서로 직렬화한다. 이 직렬화된 트리가 체스 버전의 chain-of-thought 역할을 한다.

이 방식의 의도는 외부 탐색 알고리즘을 inference 때 붙이는 대신, 모델 자체가 "먼저 후보 변화를 생각하고 그다음 최종 수를 둔다"는 형식을 학습하게 만드는 것이다.

### 4. Pretraining-RL Scaling Law

논문은 RL 성능을 다음 구조로 근사한다.

```text
R(C_RL, N, T) = f(L_pt(N, T)) + g(N, T) * (log10(C_RL) - log10(C_ref))
```

여기서 `N`은 모델 크기, `T`는 사전학습 토큰 수, `C_RL`은 RL compute, `L_pt`는 사전학습 검증 손실이다. `f`는 RL 이후 성능 수준을, `g`는 RL compute를 늘릴 때 reward가 증가하는 속도를 나타낸다.

논문 결과에서 낮은 사전학습 손실은 높은 post-RL 성능을 예측했고, `g`는 특히 `log10(T)`와 강하게 연관되었다. 즉 더 오래 사전학습된 모델은 시작점도 좋고 RL을 통해 더 빠르게 개선될 가능성이 있다.

### 5. Compute Allocation Frontier

총 compute가 고정되어 있으면 사전학습을 더 오래 할수록 초기 정책은 좋아지지만, RL에 쓸 compute는 줄어든다. 반대로 일찍 RL을 시작하면 RL step은 많아지지만 초기 정책이 약할 수 있다.

논문은 Pareto frontier를 통해 이 tradeoff를 분석한다. 작은 compute 영역에서는 사전학습 비중이 더 중요하다. 그러나 모델과 총 compute가 커질수록 RL compute 비율이 증가하는 경향이 있다. 20M 모델 예시에서는 frontier상 RL compute ratio가 약 5%에서 32%까지 증가하는 패턴이 보고된다.

다만 이 결과는 pass@1 중심이다. pass@16 같은 다양성 지표에서는 추가 RL보다 추가 사전학습이 더 나은 경우도 있었다.

### 6. RL은 무엇을 바꾸는가

논문은 RL이 단순 temperature scaling처럼 SFT 분포를 균일하게 날카롭게 만드는지 검토한다. 평균적으로 sharpening이 보이긴 하지만, 상태별 변화는 훨씬 복잡했다.

주요 변화 유형은 다음과 같다.

| 변화 유형 | 설명 | 주로 나타나는 상황 |
| --- | --- | --- |
| Ground-truth amplification | SFT가 이미 상위 후보로 보던 정답 수의 확률을 더 키운다. | 쉬운 퍼즐 |
| Tail discovery | 낮은 확률 꼬리에 있던 정답 수를 상위 후보로 끌어올린다. | 어려운 퍼즐 일부 |
| Wrong-mode amplification | 잘못된 유력 후보를 더 강화한다. | 어려운 퍼즐, 정답이 초기 support 밖에 있을 때 |

이 혼합 효과 때문에 RL은 pass@1은 개선할 수 있지만, pass@k를 일관되게 개선하지 못할 수 있다. 정책이 더 자신감 있게 하나의 답을 내는 능력과, 다양한 좋은 후보를 유지하는 능력은 다르다.

### 7. CoT 탐색 동역학

Reasoning trace를 트리로 복원하면 RL 전후의 탐색 구조를 볼 수 있다. 논문은 RL이 주로 탐색 폭을 넓히고 후보 수와 branching factor를 늘렸다고 해석한다. 반면 최대 탐색 깊이는 크게 늘지 않았다.

이는 RL이 후보 생성과 선택을 개선하는 데 강하지만, SFT에서 본 horizon보다 훨씬 깊은 장기 탐색을 자연스럽게 확장하는 데는 한계가 있음을 시사한다.

### 8. 수학 도메인 전이

논문은 체스 결과가 지나치게 좁은 도메인에만 해당하는지 확인하기 위해 수학 텍스트로 사전학습한 1B OLMo-2 모델도 실험했다. 10B부터 200B 토큰까지의 체크포인트에 SFT와 RL을 적용한 결과, 낮은 사전학습 손실이 높은 post-RL 성능을 예측하고, 사전학습 토큰 수가 RL 개선 속도와 연결되는 유사한 패턴이 나타났다.

이는 체스 테스트베드의 정량 구조가 자연어 수학 reasoning에도 일부 적용될 수 있음을 보여 주지만, 논문 역시 더 큰 규모와 다양한 도메인의 후속 검증이 필요하다는 점을 남긴다.

## 용어 정리

| 용어 | 의미 |
| --- | --- |
| Pretraining | 대규모 데이터에서 다음 토큰 예측으로 기본 정책을 학습하는 단계 |
| SFT | 정답 예시를 모방하도록 지도학습하는 포스트 트레이닝 단계 |
| RL | 보상을 이용해 정책을 최적화하는 강화학습 단계 |
| GRPO | Group Relative Policy Optimization. 여러 샘플의 상대적 성과를 이용하는 RL 최적화 방식 |
| Verifiable Reward | 정답 여부를 자동 검증할 수 있는 보상 |
| Synthetic CoT | 인간 주석이 아니라 모델 샘플과 규칙으로 만든 reasoning trace |
| pass@1 | 대표 샘플 하나가 정답일 확률 |
| pass@k | k개 샘플 중 하나 이상이 정답일 확률 |
| Pareto Frontier | 같은 compute에서 더 좋은 선택지가 없는 최적 조합들의 경계 |
| Ground-truth Amplification | 이미 상위권인 정답 후보를 RL이 더 강화하는 현상 |
| Tail Discovery | 낮은 확률 꼬리에 있던 정답 후보를 RL이 끌어올리는 현상 |
| Wrong-mode Amplification | 잘못된 고확률 후보를 RL이 더 강화하는 현상 |

## 실습 학습 가이드

- [01_foundations.ipynb](01_foundations.ipynb): 체스 수 토큰화, pretraining/SFT/RL 파이프라인, compute 추정식 `6NT`를 손으로 이해한다.
- [02_practice.ipynb](02_practice.ipynb): 간단한 joint pretraining-RL scaling law를 구현하고, 총 compute 예산에서 사전학습과 RL의 최적 분배를 탐색한다.
- [03_advanced.ipynb](03_advanced.ipynb): toy policy distribution을 이용해 ground-truth amplification, tail discovery, wrong-mode amplification과 pass@1/pass@k 차이를 시뮬레이션한다.

## 다음 학습 경로

1. Chinchilla scaling law의 `N`, `D`, `C` 관계를 복습한다.
2. GRPO, PPO, DPO의 목적함수 차이를 비교한다.
3. pass@1과 pass@k가 서로 다른 최적화 압력을 만드는 이유를 실험한다.
4. 체스가 아닌 Sudoku, 수학, 코드 테스트처럼 검증 가능한 보상이 있는 도메인에서 같은 분석을 반복해 본다.
5. wrong-mode amplification을 줄이기 위해 entropy 보너스, 후보 coverage, verifier-guided search 같은 방법을 검토한다.
