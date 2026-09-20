<!-- rumdl-disable MD013 -->

# SalesRLAgent: A Reinforcement Learning Approach for Real-Time Sales Conversion Prediction and Optimization — 문장 대조 번역

## 논문 메타데이터

| 항목 | 내용 |
| --- | --- |
| 원문 제목 | SalesRLAgent: A Reinforcement Learning Approach for Real-Time Sales Conversion Prediction and Optimization |
| 저자 | Nandakishor M |
| 소속 | Deepmost Innovations |
| 출판 상태 | arXiv preprint, cs.LG / cs.AI |
| 제출일 | 2025-03-30 |
| 식별자 | arXiv:2503.23303v1 |
| DOI | [10.48550/arXiv.2503.23303](https://doi.org/10.48550/arXiv.2503.23303) |
| 원문 | [초록 페이지](https://arxiv.org/abs/2503.23303) · [HTML](https://arxiv.org/html/2503.23303v1) · [PDF](https://arxiv.org/pdf/2503.23303) |
| 사용한 버전 | v1, 6쪽 PDF 및 arXiv 실험적 HTML 대조 |
| 원문 언어 | 영어 |
| 접근일 | 2026-09-20 |
| 라이선스 | [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) |

파일명에서는 Windows에서 사용할 수 없는 콜론(`:`)을 하이픈(` -`)으로 바꾸었다. CC0 공개 원문을 확인할 수 있어 본문을 문장 대조 형식으로 번역했다. 이 문서는 저자의 주장과 번역자의 검토를 명확히 구분한다.

## 번역·접근 범위

| 구역 | 상태 | 비고 |
| --- | --- | --- |
| 제목·초록·색인어 | 완료 | PDF와 HTML 대조 |
| I. Introduction | 완료 | 목록 포함 |
| II. Related Work | 완료 | 인용 번호 보존 |
| III. Data Generation and Processing | 완료 | 수치와 목록 보존 |
| IV. Reinforcement Learning Architecture | 완료 | Algorithm 1 보존 |
| V. System Integration and Deployment | 완료 | 목록 포함 |
| VI. Results and Evaluation | 완료 | 표 I~III 수치 보존 |
| VII. Discussion and Insights | 완료 | 한계 포함 |
| VIII. Conclusion | 완료 | 목록 포함 |
| Acknowledgment | 완료 | 원문 어조 보존 |
| References | 완료 | 서지 레코드를 원문 그대로 보존 |
| 수식·그림 | 해당 없음 | 본문에 명시적 수식이나 figure가 없고 Algorithm 1과 표 3개만 있음 |
| 부록·보충자료 | 해당 없음 | v1에서 확인되지 않음 |

## 재현성 감사 메모 — 원문 밖의 번역자 주

- 아래의 정확도, A/B 시험 효과, 지연 시간, 학습 시간은 모두 **논문 저자가 보고한 주장**이다. 논문에는 원시 데이터, 코드 링크, 체크포인트, 실험 seed, 데이터 분할 방법, 명명된 RL 알고리즘, 보상 함수식, 네트워크 크기, 통계적 유의성 또는 신뢰구간이 제시되지 않아 이 문서 작성 과정에서 독립적으로 재현하지 못했다.
- 특히 논문은 `conversion probability estimate`를 action으로, 예측 정확도를 reward로 정의하지만 실제 환경 전이와 개입 정책을 구체화하지 않는다. 따라서 공개된 설명만으로는 전통적인 순차 예측과 구별되는 강화학습 문제를 완전히 판정하기 어렵다.
- 2026-09-20 현재 관련 후속 공개물로 [Hugging Face 모델](https://huggingface.co/DeepMostInnovations/sales-conversion-model-reinf-learning), [Hugging Face 데이터셋](https://huggingface.co/datasets/DeepMostInnovations/saas-sales-conversations), [GitHub 저장소](https://github.com/DeepMostInnovations/deepmost)가 확인된다. 그러나 모델 카드의 `100k+`·BGE-M3 1024차원 설명은 논문의 `1.2 million+`·Azure OpenAI 3072차원 설명과 같지 않고, GitHub의 데이터 설명과 데이터셋 카드의 합성 데이터 설명에도 차이가 있다. 버전·구성 차이일 수 있으므로 동일 실험 산출물로 간주하면 안 된다.
- 이 감사 메모는 번역이 아니라 검증 경계를 알리는 보충 설명이다. 아래 대조 번역에서는 원문 주장의 강도를 임의로 바꾸지 않았다.

## 읽기 전 핵심 배경

- **강화학습(reinforcement learning)**은 상태에서 행동을 선택하고 보상을 최대화하도록 정책을 학습하는 틀이다. 행동이 환경과 다음 상태를 바꾸는지, 보상이 어떻게 정의되는지가 핵심이다.
- **전환 예측(conversion prediction)**은 대화나 행동 기록에서 구매·계약 같은 최종 사건의 확률을 추정하는 문제다. 정확도만으로는 확률의 신뢰성을 알 수 없으므로 AUC-ROC, Brier score, log loss와 calibration도 함께 확인하는 것이 바람직하다.
- **합성 데이터(synthetic data)**는 생성 모델이나 규칙으로 만든 데이터다. 실제 고객 데이터의 개인정보 문제를 줄일 수 있지만 생성 모델의 편향, 표현 다양성 부족, 합성-현실 간 분포 이동을 검증해야 한다.
- **메타학습(meta-learning)**은 일반적으로 여러 과제에서 빠르게 적응하는 법을 학습하는 접근이다. 이 논문은 유사도·앙상블 일관성·새로운 패턴 탐지를 묶은 신뢰도 추정을 이 용어로 부르지만, 구체적인 MAML 계열 학습 절차는 제시하지 않는다.

## 문장 대조 번역

### 제목

**S001 — Original**

SalesRLAgent: A Reinforcement Learning Approach for Real-Time Sales Conversion Prediction and Optimization

**S001 — 한국어**

(SalesRLAgent: 실시간 영업 전환 예측 및 최적화를 위한 강화학습 접근법)

### Abstract

**S002 — Original**

Current approaches to sales conversation analysis and conversion prediction typically rely on Large Language Models (LLMs) combined with basic retrieval augmented generation (RAG).

**S002 — 한국어**

(현재 영업 대화 분석과 전환 예측 접근법은 일반적으로 대규모 언어 모델(LLM)에 기본적인 검색 증강 생성(RAG)을 결합하는 방식에 의존한다.)

- **용어·약어 해설**
  - **LLM (Large Language Model, 대규모 언어 모델)**: 대규모 텍스트로 학습해 자연어를 처리하고 생성하는 모델이다.
  - **RAG (Retrieval-Augmented Generation, 검색 증강 생성)**: 외부 지식을 검색한 뒤 검색 결과를 생성 모델의 입력 문맥으로 제공하는 방식이다.

**S003 — Original**

These systems, while capable of answering questions, fail to accurately predict conversion probability or provide strategic guidance in real time.

**S003 — 한국어**

(이러한 시스템은 질문에 답할 수는 있지만 전환 확률을 정확히 예측하거나 실시간 전략 지침을 제공하지 못한다.)

**S004 — Original**

In this paper, we present SalesRLAgent, a novel framework leveraging specialized reinforcement learning to predict conversion probability throughout sales conversations.

**S004 — 한국어**

(이 논문에서는 영업 대화 전 과정에서 전환 확률을 예측하기 위해 특화된 강화학습을 활용하는 새로운 프레임워크 SalesRLAgent를 제시한다.)

- **용어·약어 해설**
  - **RL (Reinforcement Learning, 강화학습)**: 상태와 행동, 보상으로 구성된 상호작용에서 누적 보상을 최대화하는 정책을 학습하는 방법이다. 이 논문은 대화의 매 턴을 상태로 본다.

**S005 — Original**

Unlike systems from Kapa.ai, Mendable, Inkeep, and others that primarily use off-the-shelf LLMs for content generation, our approach treats conversion prediction as a sequential decision problem, training on synthetic data generated using GPT-4O to develop a specialized probability estimation model.

**S005 — 한국어**

(콘텐츠 생성에 주로 기성 LLM을 사용하는 Kapa.ai, Mendable, Inkeep 등의 시스템과 달리, 우리의 접근법은 전환 예측을 순차 의사결정 문제로 취급하고 GPT-4O로 생성한 합성 데이터로 학습하여 특화된 확률 추정 모델을 개발한다.)

**S006 — Original**

Our system incorporates Azure OpenAI embeddings, turn-by-turn state tracking, and meta-learning capabilities to understand its own knowledge boundaries.

**S006 — 한국어**

(우리 시스템은 자체 지식의 경계를 이해하기 위해 Azure OpenAI 임베딩, 턴별 상태 추적, 메타학습 기능을 통합한다.)

- **용어·약어 해설**
  - **embedding(임베딩)**: 텍스트 의미를 계산 가능한 실수 벡터로 표현한 것이다.
  - **meta-learning(메타학습)**: 일반적으로 학습 방법 자체를 학습하는 접근이다. 이 논문에서는 주로 예측 신뢰도를 추정하는 구성 요소를 가리킨다.

**S007 — Original**

Evaluations demonstrate that SalesRLAgent achieves 96.7% accuracy in conversion prediction, outperforming LLM-only approaches by 34.7% while offering significantly faster inference.

**S007 — 한국어**

(평가 결과에 따르면 SalesRLAgent는 전환 예측에서 96.7%의 정확도를 달성해 LLM 전용 접근법보다 34.7% 더 높은 성능을 보이면서 추론 속도도 현저히 빠르다.)

> **번역자 주:** 뒤의 본문은 차이를 `34.7 percentage points`로 표현하므로 여기의 `34.7%`도 상대 향상률이 아니라 **34.7%포인트**를 뜻하는 것으로 읽어야 일관된다.

**S008 — Original**

Furthermore, integration with existing sales platforms shows a 43.2% increase in conversion rates when representatives utilize our system’s real-time guidance.

**S008 — 한국어**

(또한 기존 영업 플랫폼과 통합했을 때, 영업 담당자가 우리 시스템의 실시간 지침을 사용하면 전환율이 43.2% 증가하는 것으로 나타났다.)

**S009 — Original**

SalesRLAgent represents a fundamental shift from content generation to strategic sales intelligence, providing moment-by-moment conversion probability estimation with actionable insights for sales professionals.

**S009 — 한국어**

(SalesRLAgent는 콘텐츠 생성에서 전략적 영업 인텔리전스로의 근본적인 전환을 나타내며, 영업 전문가에게 실행 가능한 통찰과 함께 순간별 전환 확률 추정을 제공한다.)

**S010 — Original**

Index Terms: reinforcement learning, sales conversion prediction, conversation analysis, meta-learning, sequential decision making, real-time guidance, embeddings, sales intelligence

**S010 — 한국어**

(색인어: 강화학습, 영업 전환 예측, 대화 분석, 메타학습, 순차 의사결정, 실시간 지침, 임베딩, 영업 인텔리전스)

### I. Introduction

**S011 — Original**

The sales profession has increasingly embraced AI tools to enhance performance, with numerous platforms now offering chatbots, knowledge assistants, and conversation analytics.

**S011 — 한국어**

(영업 직군은 성과를 높이기 위해 AI 도구를 점점 더 많이 받아들였으며, 이제 많은 플랫폼이 챗봇, 지식 도우미, 대화 분석을 제공한다.)

**S012 — Original**

Despite these advances, existing solutions primarily focus on retrieving information or generating responses rather than providing strategic sales intelligence.

**S012 — 한국어**

(이러한 발전에도 불구하고 기존 솔루션은 전략적 영업 인텔리전스를 제공하기보다 정보 검색이나 응답 생성에 주로 초점을 둔다.)

**S013 — Original**

Most commercial systems from providers like Kapa.ai, Mendable, and Inkeep function essentially as glorified RAG (Retrieval Augmented Generation) systems, connecting Large Language Models (LLMs) to company knowledge bases without truly understanding sales dynamics [1].

**S013 — 한국어**

(Kapa.ai, Mendable, Inkeep 같은 제공업체의 상용 시스템 대부분은 본질적으로 포장된 RAG(검색 증강 생성) 시스템으로 작동하며, 영업 역학을 진정으로 이해하지 못한 채 LLM을 회사 지식 베이스에 연결한다 [1].)

**S014 — Original**

These approaches face several fundamental limitations in sales contexts:

- They cannot accurately predict conversion probability in real time

**S014 — 한국어**

(이러한 접근법은 영업 맥락에서 몇 가지 근본적인 한계에 직면한다.)

- 실시간 전환 확률을 정확히 예측할 수 없다.

**S015 — Original**

They lack turn-by-turn tracking of how conversation dynamics affect likelihood of sale

**S015 — 한국어**

(대화 역학이 판매 가능성에 어떤 영향을 미치는지 턴별로 추적하지 못한다.)

**S016 — Original**

They provide generic rather than strategically-timed guidance

**S016 — 한국어**

(전략적으로 적절한 시점의 지침이 아니라 일반적인 지침을 제공한다.)

**S017 — Original**

They operate reactively to queries rather than proactively guiding sales strategy

**S017 — 한국어**

(영업 전략을 선제적으로 안내하기보다 질의에 반응하는 방식으로 작동한다.)

**S018 — Original**

They have no meta-learning capability to understand the boundaries of their knowledge

**S018 — 한국어**

(자신의 지식 경계를 이해하는 메타학습 기능이 없다.)

**S019 — Original**

In this paper, I present SalesRLAgent, a novel framework that reimagines sales AI as a specialized reinforcement learning system focused on conversion prediction and optimization.

**S019 — 한국어**

(이 논문에서 나는 영업 AI를 전환 예측과 최적화에 초점을 둔 특화 강화학습 시스템으로 새롭게 구상한 프레임워크 SalesRLAgent를 제시한다.)

**S020 — Original**

Rather than treating sales conversations as simple information retrieval problems, SalesRLAgent models them as sequential decision processes where each exchange impacts conversion probability.

**S020 — 한국어**

(SalesRLAgent는 영업 대화를 단순한 정보 검색 문제로 다루는 대신, 각 발화 교환이 전환 확률에 영향을 주는 순차 의사결정 과정으로 모델링한다.)

#### 저자가 제시한 핵심 기여

**S021 — Original**

The key contributions of this work include:

- A reinforcement learning architecture specifically designed for sales conversation analysis and conversion prediction

**S021 — 한국어**

(이 연구의 핵심 기여에는 다음이 포함된다.)

- 영업 대화 분석과 전환 예측을 위해 특별히 설계한 강화학습 아키텍처

**S022 — Original**

A synthetic data generation pipeline leveraging GPT-4O to create diverse and realistic sales conversations

**S022 — 한국어**

(다양하고 현실적인 영업 대화를 만들기 위해 GPT-4O를 활용하는 합성 데이터 생성 파이프라인)

**S023 — Original**

Novel state representation techniques using Azure OpenAI embeddings (3072 dimensions) with sales-specific features

**S023 — 한국어**

(영업 특화 특징과 Azure OpenAI 임베딩(3072차원)을 사용하는 새로운 상태 표현 기법)

**S024 — Original**

A meta-learning approach enabling the system to express confidence in its predictions based on conversation similarity to training data

**S024 — 한국어**

(훈련 데이터와의 대화 유사성에 근거해 시스템이 예측 신뢰도를 표현하도록 하는 메타학습 접근법)

**S025 — Original**

Integration mechanisms providing real-time guidance within existing sales platforms

**S025 — 한국어**

(기존 영업 플랫폼 안에서 실시간 지침을 제공하는 통합 메커니즘)

**S026 — Original**

Extensive comparative evaluation demonstrating significant performance improvements over LLM-based approaches

**S026 — 한국어**

(LLM 기반 접근법보다 유의미한 성능 향상을 보인다는 광범위한 비교 평가)

**S027 — Original**

Our findings show that specialized reinforcement learning models significantly outperform even the most advanced LLM-based systems in sales conversion tasks, with SalesRLAgent achieving 96.7% prediction accuracy compared to 62% for state-of-the-art LLM solutions.

**S027 — 한국어**

(우리의 연구 결과에 따르면 특화 강화학습 모델은 영업 전환 과제에서 가장 진보한 LLM 기반 시스템보다도 훨씬 뛰어나며, 최신 LLM 솔루션의 62%와 비교해 SalesRLAgent는 96.7%의 예측 정확도를 달성한다.)

**S028 — Original**

More importantly, when deployed in real-world sales environments, the system demonstrated a 43.2% improvement in actual conversion rates.

**S028 — 한국어**

(더 중요한 점은 이 시스템을 실제 영업 환경에 배포했을 때 실제 전환율이 43.2% 향상되었다는 것이다.)

> **번역자 주:** S027~S028은 저자의 보고다. 비교 시스템 구성, 데이터 분할, 오차막대와 A/B 시험의 기준 전환율이 공개되지 않아 독립 검증할 수 없다.

### II. Related Work

#### II-A. LLM-Based Sales Assistants

**S029 — Original**

Several commercial platforms have developed LLM-based sales assistants, including Kapa.ai [2], Mendable [3], and Inkeep [4].

**S029 — 한국어**

(Kapa.ai [2], Mendable [3], Inkeep [4] 등 여러 상용 플랫폼이 LLM 기반 영업 도우미를 개발했다.)

**S030 — Original**

These systems primarily utilize APIs from providers like OpenAI, Anthropic, and Google to connect their models with company knowledge bases.

**S030 — 한국어**

(이러한 시스템은 주로 OpenAI, Anthropic, Google 같은 제공업체의 API를 활용해 모델을 회사 지식 베이스와 연결한다.)

- **용어·약어 해설**
  - **API (Application Programming Interface, 응용 프로그램 인터페이스)**: 서로 다른 소프트웨어 구성 요소가 정해진 방식으로 기능과 데이터를 주고받는 접점이다.

**S031 — Original**

While effective for question answering, their architecture fundamentally limits their ability to model the complex, sequential nature of sales conversations [5].

**S031 — 한국어**

(질의응답에는 효과적이지만, 그 아키텍처는 영업 대화의 복잡하고 순차적인 성격을 모델링하는 능력을 근본적으로 제한한다 [5].)

**S032 — Original**

Gong’s revenue intelligence platform [6] offers conversation analytics but relies primarily on pattern recognition rather than predictive modeling.

**S032 — 한국어**

(Gong의 매출 인텔리전스 플랫폼 [6]은 대화 분석을 제공하지만 예측 모델링보다는 주로 패턴 인식에 의존한다.)

**S033 — Original**

Similarly, Chorus.ai [7] provides post-conversation analysis but lacks real-time capabilities.

**S033 — 한국어**

(마찬가지로 Chorus.ai [7]는 대화 후 분석을 제공하지만 실시간 기능이 없다.)

#### II-B. Reinforcement Learning in Conversational AI

**S034 — Original**

Reinforcement Learning (RL) has shown promise in conversational tasks.

**S034 — 한국어**

(강화학습(RL)은 대화 과제에서 가능성을 보여 왔다.)

**S035 — Original**

Work by Li et al. [8] demonstrated how RL can optimize dialogue policies, while Asghar et al. [9] explored using RL for dialogue generation.

**S035 — 한국어**

(Li 등 [8]의 연구는 RL이 대화 정책을 최적화하는 방식을 보였고, Asghar 등 [9]은 대화 생성에 RL을 사용하는 방법을 탐구했다.)

**S036 — Original**

However, these applications focused on general conversational quality rather than the specific dynamics of sales conversion.

**S036 — 한국어**

(그러나 이러한 응용은 영업 전환의 구체적인 역학보다 일반적인 대화 품질에 초점을 맞췄다.)

**S037 — Original**

In the sales domain, Takanobu et al. [10] proposed an RL framework for dialogue policy in task-oriented scenarios but did not address conversion prediction or real-time guidance.

**S037 — 한국어**

(영업 분야에서 Takanobu 등 [10]은 과제 지향 시나리오의 대화 정책을 위한 RL 프레임워크를 제안했지만 전환 예측이나 실시간 지침은 다루지 않았다.)

**S038 — Original**

Henderson et al. [16] highlighted the importance of proper experimental methodology in reinforcement learning applications, which guided our rigorous evaluation approach.

**S038 — 한국어**

(Henderson 등 [16]은 강화학습 응용에서 적절한 실험 방법론의 중요성을 강조했으며, 이는 우리의 엄격한 평가 접근법을 이끌었다.)

#### II-C. Conversion Prediction Models

**S039 — Original**

Traditional conversion prediction models, as surveyed by Sakar et al. [11], typically use classification approaches with features extracted from customer behavior data.

**S039 — 한국어**

(Sakar 등 [11]이 조사한 전통적인 전환 예측 모델은 일반적으로 고객 행동 데이터에서 추출한 특징을 사용하는 분류 접근법을 채택한다.)

**S040 — Original**

The closest work to ours is from Yang et al. [14], who applied deep learning to optimize conversion funnels in e-commerce.

**S040 — 한국어**

(우리 연구와 가장 가까운 연구는 전자상거래의 전환 퍼널을 최적화하기 위해 딥러닝을 적용한 Yang 등 [14]의 연구다.)

**S041 — Original**

However, their approach focused on web navigation rather than complex conversation dynamics, and lacked the meta-learning capabilities we’ve developed for uncertainty estimation.

**S041 — 한국어**

(그러나 그들의 접근법은 복잡한 대화 역학보다 웹 탐색에 초점을 맞췄으며, 우리가 불확실성 추정을 위해 개발한 메타학습 기능이 없었다.)

**S042 — Original**

To the best of my knowledge, no existing system has successfully combined reinforcement learning, Azure OpenAI embeddings, and meta-learning for real-time sales conversion prediction and guidance, making SalesRLAgent a novel contribution to both academic research and practical sales technology.

**S042 — 한국어**

(내가 아는 한, 강화학습, Azure OpenAI 임베딩, 메타학습을 결합해 실시간 영업 전환 예측과 지침을 제공하는 데 성공한 기존 시스템은 없으므로 SalesRLAgent는 학술 연구와 실용적인 영업 기술 모두에 새로운 기여를 한다.)

> **번역자 주:** “내가 아는 한”이라는 저자의 한정 표현을 보존했다. 참고문헌 [8], [10], [14]의 서지 정보에는 문서 끝 검수 기록에 적은 불일치가 있다.

### III. Data Generation and Processing

#### III-A. Dataset Construction

**S043 — Original**

Creating a high-quality dataset of sales conversations presented significant challenges.

**S043 — 한국어**

(고품질 영업 대화 데이터셋을 만드는 일에는 상당한 어려움이 있었다.)

**S044 — Original**

Unlike academic dialogue datasets, real sales conversations contain sensitive information and are rarely publicly available.

**S044 — 한국어**

(학술 대화 데이터셋과 달리 실제 영업 대화에는 민감한 정보가 들어 있으며 공개되는 경우가 드물다.)

**S045 — Original**

To address this challenge, I developed a synthetic data generation approach:

**S045 — 한국어**

(이 문제를 해결하기 위해 나는 다음과 같은 합성 데이터 생성 접근법을 개발했다.)

**S046 — Original**

Synthetic data generation using advanced prompting of GPT-4O

**S046 — 한국어**

(GPT-4O의 고급 프롬프팅을 사용한 합성 데이터 생성)

**S047 — Original**

Carefully designed templates for different sales scenarios across 15 industries

**S047 — 한국어**

(15개 산업의 서로 다른 영업 시나리오를 위해 신중하게 설계한 템플릿)

**S048 — Original**

Programmatic variation of conversation parameters (length, style, objection types)

**S048 — 한국어**

(대화 매개변수(길이, 스타일, 이의 제기 유형)의 프로그램 방식 변형)

**S049 — Original**

Controlled simulation of conversations using multiple LLM agents

**S049 — 한국어**

(여러 LLM 에이전트를 사용한 통제된 대화 시뮬레이션)

**S050 — Original**

Our final dataset comprised over 1.2 million synthetic conversations.

**S050 — 한국어**

(최종 데이터셋은 120만 건이 넘는 합성 대화로 구성되었다.)

**S051 — Original**

I found that the quality of GPT-4O’s output was sufficient to train effective models without requiring actual sales data.

**S051 — 한국어**

(나는 GPT-4O 출력의 품질이 실제 영업 데이터 없이도 효과적인 모델을 훈련하기에 충분하다고 판단했다.)

#### 각 대화에 포함된 항목

**S052 — Original**

Each conversation included:

- Complete conversation transcript

**S052 — 한국어**

(각 대화에는 다음 항목이 포함되었다.)

- 전체 대화 기록

**S053 — Original**

Speaker information (customer vs. sales representative)

**S053 — 한국어**

(화자 정보: 고객 대 영업 담당자)

**S054 — Original**

Conversion outcome (binary)

**S054 — 한국어**

(전환 결과: 이진값)

**S055 — Original**

Timestamped conversion probability at each turn

**S055 — 한국어**

(각 턴의 타임스탬프가 있는 전환 확률)

**S056 — Original**

Simulated customer engagement metrics

**S056 — 한국어**

(시뮬레이션한 고객 참여 지표)

**S057 — Original**

Product/service category and industry

**S057 — 한국어**

(제품·서비스 범주 및 산업)

**S058 — Original**

Conversation lengths varied from 3 to 27 turns, with a median of 8 turns.

**S058 — 한국어**

(대화 길이는 3턴에서 27턴까지였고 중앙값은 8턴이었다.)

**S059 — Original**

The dataset had a roughly balanced distribution of positive (converted) and negative (non-converted) outcomes, with a slight bias toward negative outcomes (56%) that reflects real-world sales dynamics.

**S059 — 한국어**

(데이터셋의 긍정(전환) 결과와 부정(비전환) 결과 분포는 대체로 균형을 이루었지만, 실제 영업 역학을 반영해 부정 결과가 56%로 약간 더 많았다.)

> **번역자 주:** S055의 턴별 전환 확률이 어떤 절차로 정답화되었는지, S059의 56%가 어떤 실제 데이터 근거로 현실을 반영한다고 판단했는지는 논문에 설명되지 않는다.

#### III-B. Data Processing and Embedding

**S060 — Original**

Raw conversation data required substantial preprocessing to create useful training examples for our reinforcement learning approach.

**S060 — 한국어**

(원시 대화 데이터를 강화학습 접근법에 유용한 훈련 예제로 만들려면 상당한 전처리가 필요했다.)

**S061 — Original**

Our pipeline included:

**S061 — 한국어**

(우리의 파이프라인에는 다음 단계가 포함되었다.)

**S062 — Original**

Text cleaning and normalization

**S062 — 한국어**

(텍스트 정제 및 정규화)

**S063 — Original**

Entity standardization across generated conversations

**S063 — 한국어**

(생성된 대화 전반의 개체 표준화)

**S064 — Original**

Conversation segmentation into turns

**S064 — 한국어**

(대화를 턴 단위로 분할)

**S065 — Original**

Feature extraction for each conversation turn

**S065 — 한국어**

(각 대화 턴의 특징 추출)

**S066 — Original**

Embedding generation using Azure OpenAI’s embedding model

**S066 — 한국어**

(Azure OpenAI 임베딩 모델을 사용한 임베딩 생성)

**S067 — Original**

For embeddings, we used Azure OpenAI’s embedding model, which provides 3072-dimensional embeddings that effectively capture semantic relationships.

**S067 — 한국어**

(임베딩에는 의미 관계를 효과적으로 포착하는 3072차원 임베딩을 제공하는 Azure OpenAI 임베딩 모델을 사용했다.)

**S068 — Original**

Honestly, I initially wanted to build a custom embedding model, but after experimenting with the Azure OpenAI model, I found its performance was surprisingly good for our use case, so we stuck with it.

**S068 — 한국어**

(솔직히 처음에는 맞춤형 임베딩 모델을 만들고 싶었지만 Azure OpenAI 모델을 실험한 뒤 우리 사용 사례에서 성능이 놀라울 정도로 좋다는 것을 확인해 그대로 사용했다.)

**S069 — Original**

We processed both:

**S069 — 한국어**

(우리는 다음 두 측면을 모두 처리했다.)

**S070 — Original**

Semantic content (what was said)

**S070 — 한국어**

(의미 내용: 무엇을 말했는가)

**S071 — Original**

Conversational dynamics (how it was said)

**S071 — 한국어**

(대화 역학: 어떻게 말했는가)

**S072 — Original**

This approach used the standard 3072-dimensional embeddings without customization, but with domain-specific feature engineering layered on top.

**S072 — 한국어**

(이 접근법은 맞춤화하지 않은 표준 3072차원 임베딩을 사용하되 그 위에 도메인 특화 특징 공학을 추가했다.)

#### III-C. State Representation Design

**S073 — Original**

A critical innovation in our approach is the state representation used for reinforcement learning.

**S073 — 한국어**

(우리 접근법의 핵심 혁신은 강화학습에 사용하는 상태 표현이다.)

**S074 — Original**

Rather than treating each conversation turn independently, we designed a state representation that captures the evolving dynamics of the conversation:

**S074 — 한국어**

(각 대화 턴을 독립적으로 다루는 대신 대화의 변화하는 역학을 포착하는 상태 표현을 설계했다.)

**S075 — Original**

Conversation history embeddings (weighted by recency and importance)

**S075 — 한국어**

(대화 이력 임베딩: 최신성과 중요도로 가중)

**S076 — Original**

Turn-specific features (speaking time, question density, sentiment)

**S076 — 한국어**

(턴별 특징: 발화 시간, 질문 밀도, 감성)

**S077 — Original**

Customer engagement signals (response time, message length, question asking)

**S077 — 한국어**

(고객 참여 신호: 응답 시간, 메시지 길이, 질문 여부)

**S078 — Original**

Sales technique identification (SPIN selling, value selling, etc.)

**S078 — 한국어**

(영업 기법 식별: SPIN 영업, 가치 영업 등)

- **용어·약어 해설**
  - **SPIN (Situation, Problem, Implication, Need-payoff, 상황·문제·영향·해결가치) selling**: 질문을 네 범주로 구성해 고객의 필요를 발굴하는 영업 방법이다.

**S079 — Original**

Objection and interest detection

**S079 — 한국어**

(이의 제기와 관심 탐지)

**S080 — Original**

The complete state vector combined these elements into a comprehensive representation that enabled our RL agent to accurately model the sales process as a sequential decision problem.

**S080 — 한국어**

(완전한 상태 벡터는 이러한 요소를 종합 표현으로 결합해 RL 에이전트가 영업 과정을 순차 의사결정 문제로 정확히 모델링할 수 있게 했다.)

### IV. Reinforcement Learning Architecture

#### IV-A. Modeling Approach

**S081 — Original**

We formulate the sales conversion prediction task as a sequential decision problem where:

**S081 — 한국어**

(우리는 영업 전환 예측 과제를 다음과 같은 순차 의사결정 문제로 정식화한다.)

**S082 — Original**

States represent the conversation at each turn

**S082 — 한국어**

(상태는 각 턴의 대화를 나타낸다.)

**S083 — Original**

Actions correspond to conversion probability estimates

**S083 — 한국어**

(행동은 전환 확률 추정값에 해당한다.)

**S084 — Original**

Rewards measure the accuracy of these predictions

**S084 — 한국어**

(보상은 이러한 예측의 정확도를 측정한다.)

**S085 — Original**

This formulation allows us to leverage reinforcement learning to train a model that not only predicts final conversion outcomes but tracks conversion probability throughout the conversation.

**S085 — 한국어**

(이러한 정식화 덕분에 강화학습을 활용해 최종 전환 결과를 예측할 뿐 아니라 대화 전반의 전환 확률을 추적하는 모델을 훈련할 수 있다.)

**S086 — Original**

I personally found that this sequential approach captured sales dynamics much more effectively than traditional classification models.

**S086 — 한국어**

(나는 개인적으로 이 순차 접근법이 전통적인 분류 모델보다 영업 역학을 훨씬 더 효과적으로 포착한다는 것을 확인했다.)

**S087 — Original**

Sales conversations often pivot on specific exchanges, and our model learned to identify these critical moments.

**S087 — 한국어**

(영업 대화는 특정 발화 교환을 계기로 전환되는 경우가 많으며, 우리 모델은 이러한 결정적 순간을 식별하도록 학습했다.)

> **번역자 주:** 일반적인 RL에서는 행동이 다음 상태나 보상 분포에 영향을 준다. 논문은 확률 추정치를 행동이라고 부르지만 그 추정치가 환경을 어떻게 바꾸는지, 보상을 어떤 식으로 계산하는지 명시하지 않는다.

#### IV-B. Model Architecture

**S088 — Original**

The core of SalesRLAgent is a reinforcement learning architecture consisting of:

**S088 — 한국어**

(SalesRLAgent의 핵심은 다음으로 구성된 강화학습 아키텍처다.)

**S089 — Original**

A state encoder network that processes Azure OpenAI embeddings and features

**S089 — 한국어**

(Azure OpenAI 임베딩과 특징을 처리하는 상태 인코더 네트워크)

**S090 — Original**

A policy network that estimates conversion probability based on the current state

**S090 — 한국어**

(현재 상태에 근거해 전환 확률을 추정하는 정책 네트워크)

**S091 — Original**

A value network that estimates the expected cumulative reward

**S091 — 한국어**

(기대 누적 보상을 추정하는 가치 네트워크)

**S092 — Original**

A meta-learning module that assesses prediction confidence

**S092 — 한국어**

(예측 신뢰도를 평가하는 메타학습 모듈)

**S093 — Original**

We experimented with several RL algorithms, ultimately finding that a specialized reinforcement learning algorithm with the following characteristics performed best:

**S093 — 한국어**

(우리는 여러 RL 알고리즘을 실험했고, 결국 다음 특성을 지닌 특화 강화학습 알고리즘이 가장 좋은 성능을 냈다는 것을 확인했다.)

**S094 — Original**

Strong policy regularization to prevent overfitting

**S094 — 한국어**

(과적합을 방지하는 강한 정책 정규화)

**S095 — Original**

Conservative policy updates to maintain stability

**S095 — 한국어**

(안정성을 유지하는 보수적 정책 갱신)

**S096 — Original**

Adaptive learning rates based on prediction difficulty

**S096 — 한국어**

(예측 난이도에 따른 적응형 학습률)

**S097 — Original**

Distribution-aware learning to handle uncertainty

**S097 — 한국어**

(불확실성을 다루기 위한 분포 인식 학습)

**S098 — Original**

The model architecture includes several specialized components:

**S098 — 한국어**

(모델 아키텍처에는 여러 특화 구성 요소가 포함된다.)

**S099 — Original**

Algorithm 1 Conversion Probability Estimation

**S099 — 한국어**

(알고리즘 1 전환 확률 추정)

**S100 — Original**

```text
1: function EstimateConversion(conversation, turn)
2:     history <- ExtractHistory(conversation, turn)
3:     embeddings <- GenerateAzureEmbeddings(history)
4:     features <- ExtractFeatures(history)
5:     state <- CombineState(embeddings, features)
6:     policy <- PolicyNetwork(state)
7:     value <- ValueNetwork(state)
8:     confidence <- ConfidenceEstimation(state, policy)
9:     return {probability: policy, confidence: confidence}
10: end function
```

**S100 — 한국어**

```text
1: 함수 EstimateConversion(대화, 턴)
2:     이력 <- ExtractHistory(대화, 턴)
3:     임베딩 <- GenerateAzureEmbeddings(이력)
4:     특징 <- ExtractFeatures(이력)
5:     상태 <- CombineState(임베딩, 특징)
6:     정책 <- PolicyNetwork(상태)
7:     가치 <- ValueNetwork(상태)
8:     신뢰도 <- ConfidenceEstimation(상태, 정책)
9:     반환 {probability: 정책, confidence: 신뢰도}
10: 함수 끝
```

알고리즘은 현재 턴까지의 대화 이력을 임베딩과 수작업 특징으로 바꿔 상태를 만들고, 정책 네트워크의 확률과 별도 신뢰도 추정을 반환한다. `value`는 7행에서 계산되지만 9행 반환값에는 사용되지 않는다. 텐서 크기, 정책·가치 네트워크 구조와 학습 목적 함수는 원문에 없다.

#### IV-C. Meta-Learning for Uncertainty Estimation

**S101 — Original**

A key innovation in SalesRLAgent is its meta-learning capability [15].

**S101 — 한국어**

(SalesRLAgent의 핵심 혁신은 메타학습 기능이다 [15].)

**S102 — Original**

Unlike typical black-box models, our system can estimate its own confidence in predictions based on:

**S102 — 한국어**

(일반적인 블랙박스 모델과 달리 우리 시스템은 다음 요소를 근거로 자체 예측의 신뢰도를 추정할 수 있다.)

**S103 — Original**

Similarity to conversations in the training data

**S103 — 한국어**

(훈련 데이터의 대화와의 유사성)

**S104 — Original**

Consistency of predictions across model ensembles

**S104 — 한국어**

(모델 앙상블 전반의 예측 일관성)

**S105 — Original**

Pattern recognition of conversation structures

**S105 — 한국어**

(대화 구조의 패턴 인식)

**S106 — Original**

Identification of novel elements not present in training

**S106 — 한국어**

(훈련에 없던 새로운 요소의 식별)

**S107 — Original**

This meta-learning component allows SalesRLAgent to know when it doesn’t know—a critical capability for production systems.

**S107 — 한국어**

(이 메타학습 구성 요소는 SalesRLAgent가 자신이 모르는 때를 알게 해 주는데, 이는 프로덕션 시스템에 매우 중요한 기능이다.)

**S108 — Original**

When the system encounters conversations with unfamiliar patterns, it can explicitly communicate lower confidence rather than making potentially misleading predictions.

**S108 — 한국어**

(시스템이 낯선 패턴의 대화를 만나면 오해를 부를 수 있는 예측을 내놓는 대신 더 낮은 신뢰도를 명시적으로 전달할 수 있다.)

**S109 — Original**

I spent countless late nights tuning this meta-learning approach, motivated by early deployments where I noticed the model sometimes made confident but incorrect predictions on unusual conversation patterns.

**S109 — 한국어**

(초기 배포에서 모델이 특이한 대화 패턴에 대해 확신에 차 있지만 틀린 예측을 가끔 내놓는 것을 발견한 뒤, 나는 수없이 밤늦게까지 이 메타학습 접근법을 조정했다.)

**S110 — Original**

The resulting uncertainty estimation has proven invaluable in production systems.

**S110 — 한국어**

(그 결과로 얻은 불확실성 추정은 프로덕션 시스템에서 매우 귀중한 것으로 입증되었다.)

> **번역자 주:** 논문에는 confidence의 정의, calibration 평가, coverage-risk 곡선, 임계값 또는 실제 운영 검증 수치가 없다. “입증되었다”는 저자 서술로 읽어야 한다.

#### IV-D. Training Methodology

**S111 — Original**

Training SalesRLAgent required a carefully designed approach to handle the diverse and sometimes noisy nature of synthetically generated conversation data.

**S111 — 한국어**

(SalesRLAgent를 훈련하려면 합성 생성 대화 데이터의 다양하고 때로는 잡음이 섞인 특성을 다루도록 신중히 설계한 접근법이 필요했다.)

**S112 — Original**

Our training procedure included:

1. Initial supervised learning phase to establish reasonable policy initialization

**S112 — 한국어**

(우리의 훈련 절차에는 다음이 포함되었다.)

1. 합리적인 정책 초기화를 확립하기 위한 초기 지도학습 단계

**S113 — Original**

Reinforcement learning with carefully constructed reward functions

**S113 — 한국어**

(신중하게 구성한 보상 함수를 사용하는 강화학습)

**S114 — Original**

Curriculum learning, starting with simpler conversations

**S114 — 한국어**

(더 단순한 대화부터 시작하는 커리큘럼 학습)

**S115 — Original**

Adversarial training with challenging counter-examples

**S115 — 한국어**

(까다로운 반례를 사용하는 적대적 훈련)

**S116 — Original**

Ensemble techniques to improve robustness

**S116 — 한국어**

(강건성을 높이기 위한 앙상블 기법)

**S117 — Original**

Specialized batch construction to balance conversation types

**S117 — 한국어**

(대화 유형의 균형을 맞추기 위한 특화 배치 구성)

**S118 — Original**

We trained on a standard CPU infrastructure, which honestly surprised me by how well it performed.

**S118 — 한국어**

(우리는 표준 CPU 인프라에서 훈련했으며, 솔직히 그 성능이 매우 좋아 놀랐다.)

**S119 — Original**

The entire training process took approximately 6 hours, which was much faster than I initially expected given the complexity of the model and the size of our dataset.

**S119 — 한국어**

(전체 훈련 과정에는 약 6시간이 걸렸는데, 모델의 복잡성과 데이터셋 크기를 고려할 때 처음 예상했던 것보다 훨씬 빨랐다.)

> **번역자 주:** CPU 모델·코어 수, RAM, 병렬화 방식, 임베딩 사전 계산 여부와 훈련에 실제 사용한 샘플 수가 없어 6시간이라는 수치를 재현할 수 없다.

### V. System Integration and Deployment

#### V-A. Real-time Inference Pipeline

**S120 — Original**

Converting our trained model into a production system required careful engineering.

**S120 — 한국어**

(훈련된 모델을 프로덕션 시스템으로 전환하려면 세심한 엔지니어링이 필요했다.)

**S121 — Original**

The complete inference pipeline includes:

**S121 — 한국어**

(전체 추론 파이프라인에는 다음 단계가 포함된다.)

**S122 — Original**

Conversation capturing and preprocessing

**S122 — 한국어**

(대화 수집 및 전처리)

**S123 — Original**

Incremental embedding generation using Azure OpenAI

**S123 — 한국어**

(Azure OpenAI를 사용하는 증분 임베딩 생성)

**S124 — Original**

State tracking and update

**S124 — 한국어**

(상태 추적 및 갱신)

**S125 — Original**

Probability prediction and confidence estimation

**S125 — 한국어**

(확률 예측 및 신뢰도 추정)

**S126 — Original**

Strategic guidance generation

**S126 — 한국어**

(전략적 지침 생성)

**S127 — Original**

CRM and communication tool integration

**S127 — 한국어**

(CRM 및 커뮤니케이션 도구 통합)

- **용어·약어 해설**
  - **CRM (Customer Relationship Management, 고객 관계 관리)**: 고객·리드·거래·상호작용 정보를 관리하는 업무 시스템이다.

**S128 — Original**

To meet stringent latency requirements (under 100ms), we implemented several optimizations:

**S128 — 한국어**

(엄격한 지연 시간 요구사항(100ms 미만)을 충족하기 위해 여러 최적화를 구현했다.)

**S129 — Original**

Model quantization (8-bit precision with minimal accuracy loss)

**S129 — 한국어**

(모델 양자화: 정확도 손실을 최소화한 8비트 정밀도)

**S130 — Original**

Embedding caching for repeated conversation elements

**S130 — 한국어**

(반복되는 대화 요소를 위한 임베딩 캐싱)

**S131 — Original**

Incremental state updates rather than full recalculation

**S131 — 한국어**

(전체 재계산 대신 증분 상태 갱신)

**S132 — Original**

CPU optimization for multi-user environments

**S132 — 한국어**

(다중 사용자 환경을 위한 CPU 최적화)

**S133 — Original**

Asynchronous guidance generation

**S133 — 한국어**

(비동기 지침 생성)

#### V-B. Advanced Orchestration Layer

**S134 — Original**

A critical component of our system is a sophisticated orchestration layer that handles multi-node context retrieval and processing.

**S134 — 한국어**

(우리 시스템의 핵심 구성 요소는 다중 노드 문맥 검색과 처리를 다루는 정교한 오케스트레이션 계층이다.)

**S135 — Original**

This directed graph architecture routes conversations through specialized processing nodes for contextually relevant information retrieval.

**S135 — 한국어**

(이 방향 그래프 아키텍처는 문맥상 관련 있는 정보를 검색하기 위해 대화를 특화 처리 노드로 라우팅한다.)

**S136 — Original**

Our implementation integrates:

**S136 — 한국어**

(우리 구현은 다음 요소를 통합한다.)

**S137 — Original**

High-performance vector search for similarity matching

**S137 — 한국어**

(유사성 매칭을 위한 고성능 벡터 검색)

**S138 — Original**

Caching layers for optimized retrieval

**S138 — 한국어**

(검색 최적화를 위한 캐시 계층)

**S139 — Original**

State-based workflow orchestration for complex conversation patterns

**S139 — 한국어**

(복잡한 대화 패턴을 위한 상태 기반 워크플로 오케스트레이션)

**S140 — Original**

Dynamic prompt engineering based on conversion probability

**S140 — 한국어**

(전환 확률에 근거한 동적 프롬프트 엔지니어링)

**S141 — Original**

The orchestration architecture enables the system to make sophisticated decisions about what information to retrieve and how to process it, significantly outperforming simple RAG approaches used by competing systems.

**S141 — 한국어**

(오케스트레이션 아키텍처는 어떤 정보를 검색하고 어떻게 처리할지에 대해 시스템이 정교한 결정을 내리게 하며, 경쟁 시스템이 사용하는 단순 RAG 접근법보다 성능이 크게 우수하다.)

#### V-C. CRM and Communication Platform Integration

**S142 — Original**

SalesRLAgent was designed to integrate with existing sales tooling rather than requiring wholesale replacement of infrastructure.

**S142 — 한국어**

(SalesRLAgent는 인프라를 전면 교체하도록 요구하는 대신 기존 영업 도구와 통합하도록 설계되었다.)

**S143 — Original**

We developed connectors for:

**S143 — 한국어**

(우리는 다음을 위한 커넥터를 개발했다.)

**S144 — Original**

Popular CRM platforms (Salesforce, HubSpot, etc.)

**S144 — 한국어**

(널리 쓰이는 CRM 플랫폼: Salesforce, HubSpot 등)

**S145 — Original**

Communication tools (Zoom, Teams, Google Meet)

**S145 — 한국어**

(커뮤니케이션 도구: Zoom, Teams, Google Meet)

**S146 — Original**

Email platforms (Outlook, Gmail)

**S146 — 한국어**

(이메일 플랫폼: Outlook, Gmail)

**S147 — Original**

Chat systems (Slack, Intercom, Drift)

**S147 — 한국어**

(채팅 시스템: Slack, Intercom, Drift)

**S148 — Original**

Integration options include:

**S148 — 한국어**

(통합 옵션에는 다음이 포함된다.)

**S149 — Original**

Real-time overlay for sales representatives

**S149 — 한국어**

(영업 담당자를 위한 실시간 오버레이)

**S150 — Original**

Post-call summary and analytics

**S150 — 한국어**

(통화 후 요약 및 분석)

**S151 — Original**

Manager dashboards for team performance

**S151 — 한국어**

(팀 성과를 위한 관리자 대시보드)

**S152 — Original**

API access for custom integrations

**S152 — 한국어**

(맞춤 통합을 위한 API 접근)

### VI. Results and Evaluation

#### VI-A. Conversion Prediction Accuracy

**S153 — Original**

We evaluated SalesRLAgent against several baseline approaches:

**S153 — 한국어**

(우리는 여러 기준선 접근법과 비교해 SalesRLAgent를 평가했다.)

**S154 — Original**

Traditional ML classifiers (Random Forest, XGBoost)

**S154 — 한국어**

(전통적인 ML 분류기: Random Forest, XGBoost)

**S155 — Original**

LLM-based prediction (GPT-4 with specialized prompting)

**S155 — 한국어**

(LLM 기반 예측: 특화 프롬프팅을 적용한 GPT-4)

**S156 — Original**

Commercial systems (anonymized due to licensing restrictions)

**S156 — 한국어**

(상용 시스템: 라이선스 제한으로 익명화)

**S157 — Original**

Hybrid approaches combining LLMs with traditional ML

**S157 — 한국어**

(LLM과 전통적인 ML을 결합한 하이브리드 접근법)

**S158 — Original**

Table I shows the prediction accuracy across these approaches:

**S158 — 한국어**

(표 I은 이러한 접근법의 예측 정확도를 보여 준다.)

**S159 — Original**

TABLE I: Conversion Prediction Accuracy

| Approach | Accuracy | AUC-ROC |
| --- | ---: | ---: |
| Random Forest | 0.67 | 0.71 |
| XGBoost | 0.69 | 0.74 |
| GPT-4 (zero-shot) | 0.59 | 0.63 |
| GPT-4 (few-shot) | 0.62 | 0.68 |
| Commercial System A | 0.71 | 0.76 |
| Commercial System B | 0.73 | 0.78 |
| Hybrid LLM+ML | 0.75 | 0.81 |
| SalesRLAgent (base) | 0.92 | 0.94 |
| SalesRLAgent (full) | 0.967 | 0.98 |

**S159 — 한국어**

(표 I: 전환 예측 정확도)

| 접근법 | 정확도 | AUC-ROC |
| --- | ---: | ---: |
| Random Forest | 0.67 | 0.71 |
| XGBoost | 0.69 | 0.74 |
| GPT-4 (zero-shot) | 0.59 | 0.63 |
| GPT-4 (few-shot) | 0.62 | 0.68 |
| 상용 시스템 A | 0.71 | 0.76 |
| 상용 시스템 B | 0.73 | 0.78 |
| 하이브리드 LLM+ML | 0.75 | 0.81 |
| SalesRLAgent (base) | 0.92 | 0.94 |
| SalesRLAgent (full) | 0.967 | 0.98 |

- **용어·약어 해설**
  - **AUC-ROC (Area Under the Receiver Operating Characteristic Curve, ROC 곡선 아래 면적)**: 모든 분류 임계값에서 양성과 음성을 구분하는 순위 능력을 요약한 지표다. 1에 가까울수록 구분력이 높다.
  - 이 표는 저자가 보고한 점추정치다. 표본 수, 분할 단위, 반복 수, 분산·신뢰구간이 제시되지 않아 통계적 비교는 할 수 없다.

**S160 — Original**

SalesRLAgent achieved 96.7% accuracy, outperforming the best commercial alternative by 23.7 percentage points and the best LLM approach by 34.7 percentage points.

**S160 — 한국어**

(SalesRLAgent는 96.7%의 정확도를 달성해 가장 좋은 상용 대안보다 23.7%포인트, 가장 좋은 LLM 접근법보다 34.7%포인트 높은 성능을 보였다.)

**S161 — Original**

More importantly, SalesRLAgent demonstrated superior performance in tracking conversion probability throughout conversations, not just predicting final outcomes.

**S161 — 한국어**

(더 중요한 점은 SalesRLAgent가 최종 결과만 예측한 것이 아니라 대화 전반의 전환 확률을 추적하는 데서도 더 우수한 성능을 보였다는 것이다.)

#### VI-B. Real-World Impact on Sales Performance

**S162 — Original**

Beyond technical metrics, we evaluated SalesRLAgent in real-world sales environments through A/B testing.

**S162 — 한국어**

(기술 지표를 넘어, 우리는 A/B 시험으로 실제 영업 환경에서 SalesRLAgent를 평가했다.)

**S163 — Original**

Sales representatives were randomly assigned to use either:

**S163 — 한국어**

(영업 담당자는 다음 중 하나를 사용하도록 무작위 배정되었다.)

**S164 — Original**

Traditional sales tools only (control group)

**S164 — 한국어**

(전통적인 영업 도구만 사용: 대조군)

**S165 — Original**

Traditional tools + SalesRLAgent guidance (test group)

**S165 — 한국어**

(전통적인 도구와 SalesRLAgent 지침 사용: 시험군)

**S166 — Original**

After 90 days across 217 representatives and 12,433 conversations, we observed:

**S166 — 한국어**

(217명의 담당자와 12,433건의 대화를 대상으로 90일이 지난 뒤 다음 결과를 관찰했다.)

**S167 — Original**

43.2% increase in conversion rate for the test group

**S167 — 한국어**

(시험군의 전환율 43.2% 증가)

**S168 — Original**

22% reduction in sales cycle length

**S168 — 한국어**

(영업 주기 길이 22% 감소)

**S169 — Original**

14% improvement in average deal size

**S169 — 한국어**

(평균 거래 규모 14% 개선)

**S170 — Original**

9% increase in customer satisfaction scores

**S170 — 한국어**

(고객 만족도 점수 9% 증가)

**S171 — Original**

Qualitative feedback from sales representatives highlighted several key benefits:

**S171 — 한국어**

(영업 담당자의 정성적 피드백에서는 다음과 같은 주요 이점이 강조되었다.)

**S172 — Original**

Early identification of promising leads, allowing better time allocation

**S172 — 한국어**

(유망한 리드를 조기에 식별해 시간을 더 잘 배분할 수 있음)

**S173 — Original**

Real-time awareness of conversation turning points

**S173 — 한국어**

(대화 전환점을 실시간으로 파악)

**S174 — Original**

Specific guidance on addressing objections

**S174 — 한국어**

(이의 제기 대응에 관한 구체적인 지침)

**S175 — Original**

Increased confidence in forecasting

**S175 — 한국어**

(예측에 대한 확신 증가)

**S176 — Original**

Better alignment between perception and reality of conversation quality

**S176 — 한국어**

(대화 품질에 관한 인식과 현실의 일치도 향상)

> **번역자 주:** 논문은 무작위화 단위와 절차, 군별 인원·대화 수, 사전 기준값, 산업 구성, 오염 방지, 탈락, 신뢰구간, 유의성 검정 또는 효과가 상대 변화인지 절대 변화인지 보고하지 않는다. 따라서 S167~S170만으로 인과 효과의 크기를 검증할 수 없다.

#### VI-C. Inference Performance

**S177 — Original**

For practical sales tools, inference speed is critical.

**S177 — 한국어**

(실용적인 영업 도구에서는 추론 속도가 중요하다.)

**S178 — Original**

We benchmarked SalesRLAgent against LLM-based approaches:

**S178 — 한국어**

(우리는 LLM 기반 접근법과 비교해 SalesRLAgent를 벤치마크했다.)

**S179 — Original**

TABLE II: Inference Performance Comparison

| Approach | Latency (ms) | Throughput (req/s) |
| --- | ---: | ---: |
| GPT-4 (API) | 3450 | 0.3 |
| GPT-3.5 (API) | 980 | 1.0 |
| Claude (API) | 2750 | 0.4 |
| Local LLM | 1650 | 0.6 |
| SalesRLAgent (CPU) | 85 | 12 |

**S179 — 한국어**

(표 II: 추론 성능 비교)

| 접근법 | 지연 시간(ms) | 처리량(req/s) |
| --- | ---: | ---: |
| GPT-4 (API) | 3450 | 0.3 |
| GPT-3.5 (API) | 980 | 1.0 |
| Claude (API) | 2750 | 0.4 |
| 로컬 LLM | 1650 | 0.6 |
| SalesRLAgent (CPU) | 85 | 12 |

**S180 — Original**

SalesRLAgent achieved dramatically faster inference times—85ms compared to seconds for LLM approaches—making it suitable for real-time guidance without disrupting conversation flow.

**S180 — 한국어**

(SalesRLAgent는 LLM 접근법의 수 초에 비해 85ms라는 현저히 빠른 추론 시간을 달성해 대화 흐름을 방해하지 않는 실시간 지침에 적합하다.)

**S181 — Original**

We currently only offer CPU deployment options, which has proven more than sufficient for our throughput needs.

**S181 — 한국어**

(현재는 CPU 배포 옵션만 제공하지만, 이는 우리의 처리량 요구에 충분하고도 남는 것으로 입증되었다.)

> **번역자 주:** 원격 API와 로컬 특화 모델의 지연 시간을 비교했지만 하드웨어, 지역, 네트워크, 동시성, 입력 길이, 워밍업과 임베딩 API 시간을 동일하게 통제했는지 제시되지 않는다. 따라서 표 II는 동일 조건의 공정한 벤치마크로 독립 확인되지 않았다.

#### VI-D. Ablation Studies

**S182 — Original**

To understand the contribution of each component, we conducted ablation studies removing key elements of SalesRLAgent:

**S182 — 한국어**

(각 구성 요소의 기여를 이해하기 위해 SalesRLAgent의 핵심 요소를 하나씩 제거하는 실험을 수행했다.)

**S183 — Original**

TABLE III: Ablation Study Results (Accuracy)

| Configuration | Accuracy |
| --- | ---: |
| Full SalesRLAgent | 0.967 |
| - Azure OpenAI embeddings | 0.89 (-0.077) |
| - Sequential modeling | 0.86 (-0.107) |
| - Meta-learning | 0.94 (-0.027) |
| - Advanced orchestration | 0.92 (-0.047) |
| - Caching optimization | 0.95 (-0.017) |
| - All specializations (basic ML) | 0.68 (-0.287) |

**S183 — 한국어**

(표 III: 구성 요소 제거 실험 결과—정확도)

| 구성 | 정확도 |
| --- | ---: |
| 전체 SalesRLAgent | 0.967 |
| - Azure OpenAI 임베딩 | 0.89 (-0.077) |
| - 순차 모델링 | 0.86 (-0.107) |
| - 메타학습 | 0.94 (-0.027) |
| - 고급 오케스트레이션 | 0.92 (-0.047) |
| - 캐싱 최적화 | 0.95 (-0.017) |
| - 모든 특화 요소(기본 ML) | 0.68 (-0.287) |

**S184 — Original**

These results highlight the significant contribution of sequential modeling and Azure OpenAI embeddings, which together account for the majority of SalesRLAgent’s performance advantage over traditional approaches.

**S184 — 한국어**

(이 결과는 순차 모델링과 Azure OpenAI 임베딩의 상당한 기여를 보여 주며, 이 둘이 전통적인 접근법보다 우수한 SalesRLAgent 성능의 대부분을 설명한다.)

**S185 — Original**

The advanced orchestration and caching optimization also contribute substantially to overall system performance.

**S185 — 한국어**

(고급 오케스트레이션과 캐싱 최적화도 전체 시스템 성능에 크게 기여한다.)

> **번역자 주:** 캐싱은 보통 지연 시간 최적화이지 예측 정확도 구성 요소는 아니다. 표 III의 `- Caching optimization`이 정확도를 0.017 낮춘 이유나 평가 경로가 설명되지 않는다. 각 행이 한 요소만 제거했는지, 재훈련했는지도 명시되지 않는다.

### VII. Discussion and Insights

#### VII-A. Comparative Analysis with Existing Solutions

**S186 — Original**

Through extensive testing, I’ve identified several key advantages of our reinforcement learning approach compared to LLM-based systems like those from Kapa.ai, Mendable, and Inkeep:

**S186 — 한국어**

(광범위한 시험을 통해 나는 Kapa.ai, Mendable, Inkeep 같은 LLM 기반 시스템과 비교한 우리 강화학습 접근법의 몇 가지 핵심 장점을 확인했다.)

**S187 — Original**

Specialized vs. Generic: While LLMs excel at general text generation, they lack the specialized training on sales dynamics that our RL approach provides.

**S187 — 한국어**

(특화 대 범용: LLM은 일반 텍스트 생성에 뛰어나지만 우리 RL 접근법이 제공하는 영업 역학 특화 훈련은 부족하다.)

**S188 — Original**

This specialization results in significantly higher prediction accuracy and more relevant guidance.

**S188 — 한국어**

(이러한 특화는 훨씬 높은 예측 정확도와 더 관련성 높은 지침으로 이어진다.)

**S189 — Original**

Sequential vs. Static: LLM-based systems typically treat each interaction independently, missing the crucial sequential dynamics of sales conversations.

**S189 — 한국어**

(순차 대 정적: LLM 기반 시스템은 일반적으로 각 상호작용을 독립적으로 다루어 영업 대화의 중요한 순차 역학을 놓친다.)

**S190 — Original**

Our RL framework explicitly models how conversations evolve over time.

**S190 — 한국어**

(우리 RL 프레임워크는 대화가 시간에 따라 어떻게 전개되는지 명시적으로 모델링한다.)

**S191 — Original**

Computationally Efficient vs. Resource-Intensive: LLM inference requires significant computational resources and incurs high latency.

**S191 — 한국어**

(계산 효율적 대 자원 집약적: LLM 추론에는 상당한 계산 자원이 필요하고 지연 시간이 길다.)

**S192 — Original**

SalesRLAgent delivers predictions in milliseconds rather than seconds, enabling truly real-time guidance.

**S192 — 한국어**

(SalesRLAgent는 수 초가 아니라 밀리초 단위로 예측을 제공해 진정한 실시간 지침을 가능하게 한다.)

**S193 — Original**

Quantitative vs. Qualitative: LLM systems typically provide qualitative guidance without concrete probability estimates.

**S193 — 한국어**

(정량적 대 정성적: LLM 시스템은 일반적으로 구체적인 확률 추정 없이 정성적 지침을 제공한다.)

**S194 — Original**

SalesRLAgent offers precise conversion probabilities with confidence intervals, enabling more data-driven sales strategies.

**S194 — 한국어**

(SalesRLAgent는 신뢰구간과 함께 정밀한 전환 확률을 제공해 더 데이터 중심적인 영업 전략을 가능하게 한다.)

> **번역자 주:** 논문은 S194에서 신뢰구간을 주장하지만 신뢰구간 계산법, coverage 또는 예시 구간을 제시하지 않는다.

**S195 — Original**

Meta-Learning vs. Black Box: Our system’s meta-learning capability allows it to express uncertainty when appropriate, unlike LLM systems that often present speculation as fact.

**S195 — 한국어**

(메타학습 대 블랙박스: 추측을 사실처럼 제시하는 경우가 많은 LLM 시스템과 달리, 우리 시스템의 메타학습 기능은 적절할 때 불확실성을 표현할 수 있게 한다.)

**S196 — Original**

These differences reflect fundamentally different approaches to sales AI.

**S196 — 한국어**

(이러한 차이는 영업 AI에 대한 근본적으로 다른 접근법을 반영한다.)

**S197 — Original**

While LLM-based systems function primarily as information retrieval and text generation tools, SalesRLAgent operates more like a chess engine for sales—analyzing conversation position, evaluating conversion probability, and recommending optimal moves.

**S197 — 한국어**

(LLM 기반 시스템이 주로 정보 검색 및 텍스트 생성 도구로 기능하는 반면, SalesRLAgent는 대화의 국면을 분석하고 전환 확률을 평가하며 최적의 수를 추천하는 영업용 체스 엔진처럼 작동한다.)

#### VII-B. Limitations and Future Work

**S198 — Original**

Despite its strong performance, SalesRLAgent has several limitations that represent opportunities for future work:

**S198 — 한국어**

(강력한 성능에도 불구하고 SalesRLAgent에는 향후 연구 기회가 되는 몇 가지 한계가 있다.)

**S199 — Original**

Multilingual Support: The current model primarily supports English, with only limited capabilities in other languages.

**S199 — 한국어**

(다국어 지원: 현재 모델은 주로 영어를 지원하며 다른 언어 기능은 제한적이다.)

**S200 — Original**

Expanding to a truly multilingual model presents unique challenges in both data generation and modeling.

**S200 — 한국어**

(진정한 다국어 모델로 확장하려면 데이터 생성과 모델링 모두에서 고유한 문제가 생긴다.)

**S201 — Original**

Multimodal Analysis: The system currently analyzes only text, missing important signals from voice tone, facial expressions, or gestures in video calls.

**S201 — 한국어**

(멀티모달 분석: 현재 시스템은 텍스트만 분석하므로 화상 통화의 목소리 톤, 표정, 몸짓에서 나오는 중요한 신호를 놓친다.)

**S202 — Original**

Incorporating these signals represents a promising direction for improvement.

**S202 — 한국어**

(이러한 신호를 통합하는 것은 개선을 위한 유망한 방향이다.)

**S203 — Original**

Personalization: While the model adapts to conversation dynamics, it does not yet personalize to individual sales representatives’ styles and strengths.

**S203 — 한국어**

(개인화: 모델은 대화 역학에 적응하지만 아직 개별 영업 담당자의 스타일과 강점에 맞춰 개인화하지는 않는다.)

**S204 — Original**

Adding this layer of personalization could further enhance effectiveness.

**S204 — 한국어**

(이 개인화 계층을 추가하면 효과를 더욱 높일 수 있다.)

**S205 — Original**

Causality vs. Correlation: The current model identifies correlations between conversation patterns and outcomes but has limited capability to determine causality.

**S205 — 한국어**

(인과관계 대 상관관계: 현재 모델은 대화 패턴과 결과 사이의 상관관계를 식별하지만 인과관계를 판단하는 능력은 제한적이다.)

**S206 — Original**

Strengthening causal reasoning represents an important frontier.

**S206 — 한국어**

(인과 추론을 강화하는 것은 중요한 개척 과제다.)

**S207 — Original**

Long-term Relationship Modeling: The system currently focuses on individual conversations rather than modeling customer relationships over multiple interactions.

**S207 — 한국어**

(장기 관계 모델링: 현재 시스템은 여러 상호작용에 걸친 고객 관계를 모델링하기보다 개별 대화에 초점을 둔다.)

**S208 — Original**

Extending to relationship-level prediction presents interesting challenges.

**S208 — 한국어**

(관계 수준 예측으로 확장하는 데는 흥미로운 과제가 있다.)

**S209 — Original**

I’m particularly excited about the potential for multimodal analysis, as my preliminary experiments suggest that incorporating audio features could improve accuracy by an additional 2-3% beyond our current 96.7% benchmark.

**S209 — 한국어**

(나는 특히 멀티모달 분석의 잠재력에 기대를 걸고 있는데, 예비 실험에서는 오디오 특징을 통합하면 현재의 96.7% 기준보다 정확도가 추가로 2~3% 향상될 수 있음을 시사하기 때문이다.)

> **번역자 주:** `2-3%`가 상대 백분율인지 퍼센트포인트인지 원문은 명확히 하지 않으며, 예비 실험의 데이터와 결과표도 제공하지 않는다.

### VIII. Conclusion

**S210 — Original**

This paper presented SalesRLAgent, a novel reinforcement learning approach to sales conversion prediction and optimization.

**S210 — 한국어**

(이 논문은 영업 전환 예측 및 최적화를 위한 새로운 강화학습 접근법 SalesRLAgent를 제시했다.)

**S211 — Original**

Unlike existing LLM-based systems that rely on general text generation capabilities, SalesRLAgent treats sales conversations as sequential decision processes, enabling accurate conversion probability tracking and strategic guidance.

**S211 — 한국어**

(일반 텍스트 생성 기능에 의존하는 기존 LLM 기반 시스템과 달리 SalesRLAgent는 영업 대화를 순차 의사결정 과정으로 다뤄 정확한 전환 확률 추적과 전략적 지침을 가능하게 한다.)

#### 저자가 정리한 핵심 혁신

**S212 — Original**

The key innovations in our approach include:

- A reinforcement learning framework specifically designed for sales conversion dynamics

**S212 — 한국어**

(우리 접근법의 핵심 혁신에는 다음이 포함된다.)

- 영업 전환 역학을 위해 특별히 설계한 강화학습 프레임워크

**S213 — Original**

Synthetic data generation using GPT-4O to create diverse training scenarios

**S213 — 한국어**

(다양한 훈련 시나리오를 만들기 위해 GPT-4O를 사용한 합성 데이터 생성)

**S214 — Original**

Azure OpenAI 3072-dimensional embeddings for conversation representation

**S214 — 한국어**

(대화 표현을 위한 Azure OpenAI 3072차원 임베딩)

**S215 — Original**

Advanced orchestration for complex conversation flow management

**S215 — 한국어**

(복잡한 대화 흐름 관리를 위한 고급 오케스트레이션)

**S216 — Original**

Optimized vector similarity search with caching for millisecond-level retrieval

**S216 — 한국어**

(밀리초 단위 검색을 위해 캐싱을 적용한 최적화 벡터 유사도 검색)

**S217 — Original**

Meta-learning capabilities for confidence estimation and uncertainty quantification

**S217 — 한국어**

(신뢰도 추정과 불확실성 정량화를 위한 메타학습 기능)

**S218 — Original**

Real-time integration with existing sales tools and platforms

**S218 — 한국어**

(기존 영업 도구 및 플랫폼과의 실시간 통합)

**S219 — Original**

Our evaluation demonstrated that SalesRLAgent achieves 96.7% accuracy in conversion prediction, significantly outperforming both traditional machine learning approaches and LLM-based alternatives.

**S219 — 한국어**

(우리의 평가에서는 SalesRLAgent가 전환 예측에서 96.7%의 정확도를 달성해 전통적인 머신러닝 접근법과 LLM 기반 대안 모두보다 훨씬 뛰어난 것으로 나타났다.)

**S220 — Original**

More importantly, when deployed in real-world sales environments, the system drove a 43.2% increase in conversion rates and a 22% reduction in sales cycle length.

**S220 — 한국어**

(더 중요한 점은 실제 영업 환경에 배포했을 때 이 시스템이 전환율을 43.2% 높이고 영업 주기 길이를 22% 줄였다는 것이다.)

**S221 — Original**

These results suggest that specialized reinforcement learning approaches have significant advantages over generic LLM solutions for domain-specific applications like sales.

**S221 — 한국어**

(이 결과는 영업 같은 도메인 특화 응용에서 특화 강화학습 접근법이 범용 LLM 솔루션보다 상당한 장점이 있음을 시사한다.)

**S222 — Original**

While large language models excel at general text generation, the complex, sequential nature of sales conversations benefits from the targeted optimization that reinforcement learning provides.

**S222 — 한국어**

(대규모 언어 모델은 일반 텍스트 생성에 뛰어나지만, 영업 대화의 복잡하고 순차적인 성격에는 강화학습이 제공하는 표적 최적화가 유리하다.)

**S223 — Original**

Looking ahead, I believe this work opens new possibilities for AI in sales—moving beyond simple automation and information retrieval toward strategic partnership that enhances human capabilities rather than replacing them.

**S223 — 한국어**

(앞으로 이 연구가 단순한 자동화와 정보 검색을 넘어 인간을 대체하는 대신 인간의 역량을 높이는 전략적 동반자로 나아가는 영업 AI의 새로운 가능성을 연다고 생각한다.)

**S224 — Original**

The future of sales AI lies not in increasingly large language models, but in increasingly specialized intelligence that deeply understands the dynamics of effective selling.

**S224 — 한국어**

(영업 AI의 미래는 갈수록 커지는 언어 모델이 아니라 효과적인 영업의 역학을 깊이 이해하는 갈수록 특화된 지능에 있다.)

### Acknowledgment

**S225 — Original**

I would like to express my sincere gratitude to the team at Deepmost Innovations who endured countless iterations of model design and my incessant whiteboard sessions about reinforcement learning architecture.

**S225 — 한국어**

(수없이 반복된 모델 설계와 강화학습 아키텍처에 관한 끊임없는 화이트보드 세션을 함께 견뎌 준 Deepmost Innovations 팀에 진심으로 감사드린다.)

**S226 — Original**

Special thanks to the anonymous reviewers whose constructive feedback significantly improved this paper, though any remaining errors or oversights are entirely my own.

**S226 — 한국어**

(건설적인 피드백으로 이 논문을 크게 개선해 준 익명의 심사자들에게 특별히 감사드리며, 남아 있는 오류나 누락은 전적으로 나의 책임이다.)

**S227 — Original**

I’d also like to acknowledge OpenAI for providing the GPT-4O model that made our synthetic data generation possible, and Microsoft for the Azure OpenAI embedding model that formed the foundation of our system’s conversational understanding.

**S227 — 한국어**

(합성 데이터 생성을 가능하게 한 GPT-4O 모델을 제공한 OpenAI와 시스템의 대화 이해 기반을 형성한 Azure OpenAI 임베딩 모델을 제공한 Microsoft에도 감사를 표한다.)

**S228 — Original**

Finally, I must acknowledge the thousands of cups of coffee that fueled late-night debugging sessions and the patient family members who supported this work, even when they couldn’t quite understand my excited ramblings about conversion probability distributions at the dinner table.

**S228 — 한국어**

(마지막으로 심야 디버깅 세션을 지탱해 준 수천 잔의 커피와, 저녁 식탁에서 전환 확률 분포를 두고 흥분해 떠드는 말을 제대로 이해하지 못하면서도 이 연구를 지지해 준 인내심 많은 가족에게 감사를 표해야겠다.)

## References

아래 목록은 논문 v1에 인쇄된 서지 레코드를 번역하거나 교정하지 않고 보존한 것이다. 확인 과정에서 발견한 불일치는 다음 절에 별도로 기록한다.

1. L. Gao, X. Ma, J. Lin, and J. Callan, “Precise zero-shot dense retrieval without relevance labels,” in *Proc. 46th Int. ACM SIGIR Conf. Res. Develop. Inf. Retr.*, 2023, pp. 2196–2206.
2. Kapa.ai, “Enterprise knowledge assistant platform,” Kapa.ai, Tech. Rep., 2023. [Online]. Available: https://kapa.ai
3. Mendable, “AI search for technical documentation,” Mendable, Tech. Rep., 2023. [Online]. Available: https://mendable.ai
4. Inkeep, “Conversational AI for customer support,” Inkeep, Tech. Rep., 2023. [Online]. Available: https://inkeep.com
5. T. Zhang et al., “Benchmarking large language models for news summarization,” *arXiv*, 2023, arXiv:2301.13848.
6. Gong, “Revenue intelligence platform methodology,” Gong.io, Tech. Rep., 2022. [Online]. Available: https://gong.io
7. Chorus.ai, “Conversation intelligence for sales teams,” Chorus.ai, Tech. Rep., 2021. [Online]. Available: https://chorus.ai
8. Z. Li, J. Kiseleva, and M. de Rijke, “Guided dialog policy learning: Reward estimation for multi-domain task-oriented dialog,” in *Proc. 2020 Conf. Empir. Methods Natural Lang. Process.*, 2020, pp. 100–120.
9. N. Asghar et al., “Affective neural response generation,” in *Proc. Eur. Conf. Inf. Retr.*, 2017, pp. 154–166.
10. R. Takanobu, H. Zhu, and M. Huang, “Guided dialog policy learning: Reward estimation for multi-domain task-oriented dialog,” in *Proc. 2019 Conf. Empir. Methods Natural Lang. Process.*, 2019, pp. 2308–2319.
11. C. O. Sakar et al., “Real-time prediction of online shoppers’ purchasing intention using multilayer perceptron and LSTM recurrent neural networks,” *Neural Comput. Appl.*, vol. 31, no. 10, pp. 6893–6908, 2019.
12. J. Devlin et al., “BERT: Pre-training of deep bidirectional transformers for language understanding,” in *Proc. NAACL-HLT*, 2019, pp. 4171–4186.
13. N. Reimers and I. Gurevych, “Sentence-BERT: Sentence embeddings using Siamese BERT-networks,” in *Proc. 2019 Conf. Empir. Methods Natural Lang. Process.*, 2019, pp. 3980–3990.
14. Y. Yang, Y. Li, and H. Wang, “Sequential deep learning for online conversion prediction with user behavior,” *Inf. Process. Manage.*, vol. 59, no. 1, p. 102751, 2022.
15. C. Finn, P. Abbeel, and S. Levine, “Model-agnostic meta-learning for fast adaptation of deep networks,” in *Proc. 34th Int. Conf. Mach. Learn.*, 2017, pp. 1126–1135.
16. P. Henderson et al., “Deep reinforcement learning that matters,” in *Proc. AAAI Conf. Artif. Intell.*, vol. 32, no. 1, 2018.

## 후속 공개 구현 감사 — 원문 밖의 번역자 주

논문 v1 제출 뒤 공개된 자료는 재현 가능성을 높이는 단서이지만, v1 결과와 동일한 코드·데이터라는 연결 정보는 확인되지 않았다. 따라서 아래 내용은 **후속 구현에 대한 코드 감사**이며, 논문의 보고 수치가 같은 결함으로 산출되었다고 단정하지 않는다.

- [Hugging Face 모델 저장소](https://huggingface.co/DeepMostInnovations/sales-conversion-model-reinf-learning)의 확인한 revision은 `105963aa…`이며, `train.py`는 논문 v1 제출 뒤인 2025-05-12 추가된 것으로 표시된다.
- 그 스크립트의 상태 구성에는 정답 `outcome`이 포함된다. 또한 확률 이력을 0번째 턴의 주석된 참 확률로 초기화하고, 각 턴에서 하나의 행에 든 전체 대화 임베딩을 재사용하는 흐름이 확인된다. 이 코드 그대로 학습·평가하면 미래 또는 레이블 정보가 특징에 섞이는 **심각한 정보 누수(label/future leakage)**가 발생할 가능성이 높다.
- 같은 구현의 추론 경로는 `outcome=0.5`를 넣는다. 훈련 시 참 outcome을 본 상태와 배포 시 고정값을 보는 상태가 달라져 train–serve skew가 생길 수 있다.
- 이러한 관찰은 공개 후속 스크립트의 위험을 보여 줄 뿐, 그 스크립트가 표 I~III 또는 96.7% 수치를 생성했다는 증거는 아니다. v1 실험 코드, 체크포인트 해시와 데이터 lineage가 공개되어야 직접 연결할 수 있다.

## 약어 및 기술 용어 사전

| 원어·약어 | 한국어 | 이 논문에서의 의미 | 최초 등장 |
| --- | --- | --- | --- |
| AI | 인공지능 | 영업 대화 분석·예측을 자동화하는 기술의 총칭 | S011 |
| API | 응용 프로그램 인터페이스 | 외부 모델 및 영업 도구를 연결하는 프로그램 접점 | S030 |
| A/B testing | A/B 시험 | 대조군과 SalesRLAgent 사용군의 현장 효과를 비교했다고 보고한 시험 | S162 |
| AUC-ROC | ROC 곡선 아래 면적 | 이진 결과를 순위화하는 분류 성능 지표 | S159 |
| confidence | 신뢰도 | 예측이 학습 분포와 얼마나 부합하는지를 나타낸다고 주장하는 출력 | S092 |
| conversion | 전환 | 잠재 고객이 구매·계약 같은 목표 결과에 도달하는 사건 | S002 |
| conversion probability | 전환 확률 | 대화가 최종 전환으로 이어질 가능성의 모델 추정값 | S003 |
| CRM | 고객 관계 관리 | Salesforce·HubSpot 같은 고객·거래 관리 플랫폼 | S127 |
| embedding | 임베딩 | 대화 의미를 담는 3072차원 벡터 표현 | S006 |
| feature engineering | 특징 공학 | 임베딩 위에 영업 도메인 신호를 설계해 추가하는 과정 | S072 |
| LLM | 대규모 언어 모델 | GPT-4 등 범용 텍스트 생성·처리 모델 | S002 |
| meta-learning | 메타학습 | 이 논문에서는 유사도·앙상블·새 패턴으로 신뢰도를 추정하는 모듈 | S006 |
| policy network | 정책 네트워크 | 현재 상태에서 전환 확률을 출력하는 네트워크 | S090 |
| quantization | 양자화 | 모델 가중치·연산 정밀도를 8비트로 낮춰 지연과 메모리를 줄이는 최적화 | S129 |
| RAG | 검색 증강 생성 | 검색된 외부 문맥을 LLM 생성에 결합하는 방식 | S002 |
| RL | 강화학습 | 상태·행동·보상에 근거해 정책을 학습하는 틀 | S004 |
| sequential decision problem | 순차 의사결정 문제 | 현재 대화 상태에 따라 다음 판단을 이어 가는 문제 정식화 | S005 |
| SPIN selling | SPIN 영업 | 상황·문제·영향·해결가치 질문으로 고객 요구를 탐색하는 방법 | S078 |
| state | 상태 | 이력 임베딩과 턴·참여·영업 특징을 결합한 대화 표현 | S073 |
| synthetic data | 합성 데이터 | GPT-4O와 템플릿·다중 에이전트로 만든 영업 대화 | S005 |
| uncertainty estimation | 불확실성 추정 | 모델이 낯선 대화에서 신뢰도를 낮추려는 기능 | S101 |
| value network | 가치 네트워크 | 기대 누적 보상을 추정한다고 설명된 네트워크 | S091 |

## 번역 검수 기록

- **2026-09-20 — 원문 대조:** arXiv v1의 공식 PDF, 실험적 HTML, TeX source를 대조했다. PDF의 2단 편집 순서와 표 I~III, Algorithm 1을 함께 확인했다.
- **범위:** 제목부터 Acknowledgment까지 확인 가능한 본문을 S001~S228로 연결했다. 목록 항목도 독립 의미 단위로 ID를 부여했다. References는 번역하지 않고 인쇄된 서지 레코드 그대로 보존했다.
- **수치 대조:** `1.2 million`, `15 industries`, `3072`, `3–27`, `8`, `56%`, `6 hours`, `100ms`, `8-bit`, 표 I~III, `217`, `12,433`, `90 days`, `43.2%`, `22%`, `14%`, `9%`, `85ms`, `12 req/s`, `2-3%`를 원문과 대조했다.
- **주장 표지:** 논문의 성능·현장 효과·운영 효과를 검증된 사실로 바꾸지 않고 저자의 보고로 번역했으며, 재현에 필요한 정보가 없는 곳에는 별도의 `번역자 주`를 붙였다.
- **서지 감사:** 공식 [ACL Anthology의 Takanobu et al. 2019 레코드](https://aclanthology.org/D19-1010/)는 논문에 인쇄된 참고문헌 [10]의 제목·저자는 맞지만 페이지가 `100–110`이다. 공식 [Li et al. 2020 레코드](https://aclanthology.org/2020.findings-emnlp.209/)의 실제 제목은 “Guided Dialogue Policy Learning without Adversarial Learning in the Loop”, 페이지는 `2308–2317`, 저자 목록도 [8]의 축약 레코드와 다르다. 즉 [8]과 [10]의 제목·저자·페이지 조합이 서로 뒤섞여 있다.
- **서지 감사:** *Information Processing & Management* 59(1)의 article 102751은 [Elsevier 레코드](https://www.sciencedirect.com/science/article/pii/S0306457321002326)에서 “Social media data analytics for business decision making system to competitive analysis”로 확인된다. 따라서 참고문헌 [14]의 제목·저자·article number 조합은 공식 레코드와 일치하지 않아 확인되지 않는다.
- **해석 주의:** 원문에는 명시적인 수식·figure가 없다. `accuracy`와 AUC-ROC 외 probability calibration 지표가 없으며, confidence interval을 제공한다고 서술하지만 계산식과 결과 구간은 없다.
- **기계적 검사 권장:** 모든 `Original` ID에 같은 `한국어` ID가 하나씩 존재하고 ID가 S001부터 S228까지 단조 증가하는지 정규식으로 다시 검사할 수 있다.

[학습·비판적 분석 README로 돌아가기](README.md)
