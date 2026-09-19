# Efficient, Property-Aligned Fan-Out Retrieval via RL-Compiled Diffusion - 문장 대조 한국어 번역

## 논문 메타데이터

| 항목 | 내용 |
|---|---|
| 원문 제목 | Efficient, Property-Aligned Fan-Out Retrieval via RL-Compiled Diffusion |
| 한국어 제목 | RL로 컴파일한 확산 모델을 통한 효율적 속성 정렬 팬아웃 검색 |
| 저자 | Pengcheng Jiang, Judith Yue Li, Moonkyung Ryu, R. Lily Hu, Kun Su, Zhong Yi Wan, Liam Hebert, Hao Peng, Jiawei Han, Dima Kuzmin, Craig Boutilier |
| 출판처 | Proceedings of the 43rd International Conference on Machine Learning (ICML-26), Seoul, South Korea (2026) - Google Research 게재 정보 기준 |
| 번역 기준 원문 | arXiv:2603.06397v1 [cs.IR], 2026-03-06 제출본 |
| DOI | [10.48550/arXiv.2603.06397](https://doi.org/10.48550/arXiv.2603.06397) |
| 원문 URL | [초록](https://arxiv.org/abs/2603.06397v1) · [PDF](https://arxiv.org/pdf/2603.06397v1) · [실험적 HTML](https://arxiv.org/html/2603.06397v1) · [Google Research 게재 정보](https://research.google/pubs/efficient-property-aligned-fan-out-retrieval-via-rl-compiled-diffusion/) |
| 원문 언어 | 영어 |
| 접근일 | 2026-09-19 |
| 라이선스 | [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) |

이 번역은 CC BY 4.0에 따라 원저자와 출처를 표시하고 작성한 한국어 번역물이다. 해석 오류의 책임은 번역자에게 있으며, 연구 주장의 주체는 원저자다. 학술 인용에는 위 원문을 사용해야 한다.

## 번역·접근 범위

| 원문 구간 | 상태 | 비고 |
|---|---|---|
| 제목·초록 | 완료 | arXiv v1 PDF, HTML, TeX 대조 |
| 1 Introduction | 완료 | Figure 1·2 캡션 포함 |
| 2 Method: R4T | 완료 | 수식 (1)~(9) 보존 및 기호 해설 포함 |
| 3 Experiments | 완료 | Table 1·2, Figure 3~5 캡션과 핵심 시각 정보 포함 |
| 4 Related Work | 완료 | 본문 인용 키의 저자·연도 보존 |
| 5 Conclusion·Impact Statement | 완료 | 윤리·사회적 영향 포함 |
| Appendix A~F | 완료 | 평가 지표, 데이터 생성, 원문 프롬프트, 구현 세부사항, Table 3, Figure 6 포함 |
| References | 해당 없음 | 서지 레코드는 번역하지 않았으며 본문 인용만 보존 |

> **판독·편집 메모:** 텍스트는 공식 TeX 소스를 우선하고 24쪽 PDF와 실험적 HTML을 대조했다. 원문에 있는 `RK training`, `ivnovles`, `RT4`, `variancee` 등의 오탈자는 원문 블록에서 고치지 않았고 해당 위치에 번역자 주를 달았다. 본문의 OAR 평가 지표 절은 심판 모델을 Gemini-2.5-Pro라고 하지만 Appendix B는 Gemini-2.5-Flash라고 적어 서로 불일치한다. Table 2는 이와 별도로 넓은 질의 생성 모델을 Gemini-2.5-Pro라고 명시한다. 실제 심판 설정은 공개 원문만으로 확정할 수 없다.

## 읽기 전 핵심 배경

- **집합값 검색(set-valued retrieval)**: 하나의 정답 문서가 아니라 서로 조화를 이루는 여러 결과의 집합을 반환한다. 개별 항목의 관련도만으로는 집합 전체의 다양성·포괄성·상보성을 평가하기 어렵다.
- **팬아웃 검색(fan-out retrieval)**: 넓은 질의를 여러 하위 질의로 분해하고 각 하위 질의를 검색한 뒤 결과를 합친다.
- **목적 전환기(objective transducer)**: 이 논문에서 강화학습은 서비스 시점의 검색 엔진이 아니라, 복잡한 보상 함수를 좋은 학습 표적으로 변환하는 일회성 데이터 컴파일 단계다.
- **확산 기반 생성 검색(diffusion-based generative retrieval)**: 임베딩 집합에 잡음을 넣고 제거하는 과정을 학습하여 여러 검색 방향을 병렬로 생성한다.
- **비분해 가능 목적(non-decomposable objective)**: 집합 전체를 함께 봐야 값이 정해져 각 항목 점수의 단순 합으로 환원하기 어려운 목적이다.

---

## 제목

**S001 — Original**

Efficient, Property-Aligned Fan-Out Retrieval via RL-Compiled Diffusion

**S001 — 한국어**

RL로 컴파일한 확산 모델을 통한 효율적 속성 정렬 팬아웃 검색

- **용어·약어 해설**
  - **RL (Reinforcement Learning, 강화학습)**: 보상 신호를 최대화하도록 정책을 학습하는 방법이다. 이 논문에서는 복잡한 집합 수준 목적을 학습 데이터로 변환하는 데 한 번 사용한다.
  - **property-aligned(속성 정렬)**: 검색 결과가 단순 관련도를 넘어 다양성, 정렬성, 근거성처럼 사용자가 지정한 집합 속성과 부합함을 뜻한다.

## Abstract

**S002 — Original**

Many modern retrieval problems are set-valued: given a broad intent, the system must return a collection of results that optimizes higher-order properties (e.g., diversity, coverage, complementarity, coherence) while remaining grounded with respect to a fixed database.

**S002 — 한국어**

현대의 많은 검색 문제는 집합값 문제다. 즉, 넓은 의도가 주어지면 시스템은 고정된 데이터베이스에 근거를 둔 채 다양성, 포괄성, 상보성, 일관성과 같은 고차 속성을 최적화하는 결과 모음을 반환해야 한다.

- **용어·약어 해설**
  - **groundedness(근거성)**: 생성한 질의나 결과가 실제 대상 데이터베이스에 존재하는 콘텐츠와 의미적으로 연결되는 정도다.
  - **complementarity(상보성)**: 여러 결과가 중복되기보다 서로 다른 역할을 하며 집합 전체를 완성하는 성질이다.

**S003 — Original**

Set-valued objectives are typically non-decomposable and are not captured by existing supervised (query, content) datasets which only prioritize top-1 retrieval.

**S003 — 한국어**

집합값 목적은 일반적으로 비분해 가능하며, 상위 1개 검색만 우선하는 기존의 지도학습용 `(질의, 콘텐츠)` 데이터셋으로는 이를 포착할 수 없다.

**S004 — Original**

Consequently, fan-out retrieval is often employed to generate diverse subqueries to retrieve item sets.

**S004 — 한국어**

따라서 다양한 하위 질의를 생성해 항목 집합을 검색하는 팬아웃 검색이 흔히 사용된다.

- **용어·약어 해설**
  - **fan-out retrieval(팬아웃 검색)**: 하나의 넓은 질의를 여러 검색 방향으로 펼쳐 병렬 또는 반복 검색하는 방식이다.

**S005 — Original**

While reinforcement learning (RL) can optimize set-level objectives via interaction, deploying an RL-tuned LLM for fan-out retrieval is prohibitively expensive at inference time.

**S005 — 한국어**

강화학습은 상호작용을 통해 집합 수준 목적을 최적화할 수 있지만, RL로 조정한 LLM을 팬아웃 검색에 배포하면 추론 시점 비용이 감당하기 어려울 만큼 커진다.

- **용어·약어 해설**
  - **LLM (Large Language Model, 대규모 언어 모델)**: 여기서는 넓은 질의를 여러 하위 질의로 자동 분해하는 정책 역할을 한다.

**S006 — Original**

Conversely, diffusion-based generative retrieval enables efficient single-pass fan-out in embedding space, but requires objective-aligned training targets.

**S006 — 한국어**

반대로 확산 기반 생성 검색은 임베딩 공간에서 효율적인 단일 패스 팬아웃을 가능하게 하지만, 목적에 정렬된 학습 표적이 필요하다.

**S007 — Original**

To address these issues, we propose R4T (Retrieve-for-Train), which uses RL once as an objective transducer in a three-step process: (i) train a fan-out LLM with composite set-level rewards, (ii) synthesize objective-consistent training pairs, and (iii) train a lightweight diffusion retriever to model the conditional distribution of set-valued outputs.

**S007 — 한국어**

이 문제를 해결하기 위해 저자들은 R4T(Retrieve-for-Train)를 제안한다. R4T는 RL을 목적 전환기로 한 번만 사용해 (i) 복합 집합 수준 보상으로 팬아웃 LLM을 학습하고, (ii) 목적과 일치하는 학습 쌍을 합성하며, (iii) 집합값 출력의 조건부 분포를 모델링하는 경량 확산 검색기를 학습하는 3단계 절차다.

- **용어·약어 해설**
  - **R4T (Retrieve-for-Train, 학습을 위한 검색)**: RL 정책이 보상을 만족하는 검색 행동을 발견하고, 그 행동을 합성 데이터로 컴파일하여 더 가벼운 검색기에 전달하는 프레임워크다.
  - **objective transducer(목적 전환기)**: 보상으로 표현된 목적을 지도학습 가능한 데이터 분포로 바꾸는 역할을 가리키는 저자들의 표현이다.

**S008 — Original**

Across large-scale fashion and music benchmarks consisting of curated item sets, we show that R4T improves retrieval quality relative to strong baselines while reducing query-time fan-out latency by an order of magnitude.

**S008 — 한국어**

엄선된 항목 집합으로 이루어진 대규모 패션 및 음악 벤치마크에서 R4T는 강력한 기준선보다 검색 품질을 높이는 동시에 질의 시점 팬아웃 지연 시간을 한 자릿수 차수, 즉 대략 10배 규모로 줄였다.

## 1 Introduction

**S009 — Original**

Retrieval systems are increasingly expected to return sets of results rather than a single best match.

**S009 — 한국어**

검색 시스템에는 단 하나의 최적 일치 항목이 아니라 결과 집합을 반환하라는 요구가 점점 커지고 있다.

**S010 — Original**

In many real-world applications, the desired output is a collection that jointly satisfies higher-order properties: a search interface may expand a broad query into multiple intents to improve coverage; a recommender may produce a slate that is diverse yet coherent; and a bundling system may retrieve complementary items that collectively meet the demands of complex queries.

**S010 — 한국어**

많은 실제 응용에서 원하는 출력은 고차 속성을 함께 만족하는 모음이다. 검색 인터페이스는 포괄성을 높이기 위해 넓은 질의를 여러 의도로 확장할 수 있고, 추천기는 다양하면서도 일관된 슬레이트를 만들 수 있으며, 번들링 시스템은 복잡한 질의의 요구를 함께 충족하는 상보적 항목을 검색할 수 있다.

**S011 — Original**

These requirements have motivated generative retrieval formulations, where candidates are produced by a model rather than simply selected (e.g., using only nearest-neighbor similarity) (Tay et al., 2022; Tomasi et al., 2025; Deffayet et al., 2023).

**S011 — 한국어**

이러한 요구는 후보를 단순히 선택하는 방식, 예를 들어 최근접 이웃 유사도만 사용하는 방식이 아니라 모델이 후보를 생성하는 생성 검색 정식화를 촉진했다(Tay et al., 2022; Tomasi et al., 2025; Deffayet et al., 2023).

**S012 — Original**

A central challenge is that many of these problems are set-valued and non-decomposable.

**S012 — 한국어**

핵심 난점은 이러한 문제 중 다수가 집합값이며 비분해 가능하다는 데 있다.

**S013 — Original**

Unlike classical retrieval tasks with a single, labelable correct item, fan-out retrieval often admits no unique ground truth: many different item sets can be valid for the same broad intent.

**S013 — 한국어**

라벨을 붙일 수 있는 단일 정답 항목이 존재하는 고전적 검색과 달리, 팬아웃 검색에는 유일한 정답이 없는 경우가 많다. 같은 넓은 의도에도 서로 다른 여러 항목 집합이 모두 타당할 수 있다.

**S014 — Original**

As a result, retrieval quality is defined by set-level properties (e.g., diversity, intent coverage, complementarity, and stylistic coherence), while still requiring strict groundedness to the target database.

**S014 — 한국어**

따라서 검색 품질은 다양성, 의도 포괄성, 상보성, 스타일 일관성과 같은 집합 수준 속성으로 정의되는 동시에 대상 데이터베이스에 대한 엄격한 근거성도 요구한다.

**S015 — Original**

This makes the standard supervised paradigm more challenging in practice: collecting property-aligned (query, content) pairs that explicitly encode these set-level objectives is costly, subjective, and frequently infeasible, especially for domain-specific or customized corpora.

**S015 — 한국어**

이 때문에 표준 지도학습 패러다임은 실제로 더 어려워진다. 이러한 집합 수준 목적을 명시적으로 담은 속성 정렬 `(질의, 콘텐츠)` 쌍을 수집하는 일은 비용이 많이 들고 주관적이며, 특히 도메인 특화 또는 맞춤형 말뭉치에서는 흔히 실행 불가능하다.

**S016 — Original**

Reinforcement learning (RL) is a natural framework for optimizing such behaviors through reward-driven interaction with a database (Zhang et al., 2025a; Jiang et al., 2025b), and recent work shows RL can shape retrieval policies beyond pointwise relevance (Jiang et al., 2025a; Jiang et al., 2025c).

**S016 — 한국어**

강화학습은 데이터베이스와 보상 주도로 상호작용하며 이러한 행동을 최적화하기에 자연스러운 프레임워크이고(Zhang et al., 2025a; Jiang et al., 2025b), 최근 연구는 RL이 점별 관련도를 넘어 검색 정책을 형성할 수 있음을 보였다(Jiang et al., 2025a; Jiang et al., 2025c).

**S017 — Original**

However, directly deploying RL-trained language models at inference time is often impractical: autoregressive fan-out generation with repeated retrieval calls incurs substantial latency, and set-level rewards can exhibit high-variance and are prone to shortcut exploitation.

**S017 — 한국어**

하지만 RL로 학습한 언어 모델을 추론 시점에 직접 배포하는 것은 대개 비현실적이다. 반복 검색 호출을 수반하는 자기회귀 팬아웃 생성은 상당한 지연을 일으키며, 집합 수준 보상은 분산이 클 수 있고 지름길 악용에도 취약하다.

**S018 — Original**

These issues complicate stable deployment and motivate separating reward-driven optimization from inference-time retrieval.

**S018 — 한국어**

이 문제들은 안정적 배포를 어렵게 하므로 보상 주도 최적화와 추론 시점 검색을 분리할 필요가 있다.

**S019 — Original**

In parallel, diffusion-based generative retrieval enables efficient, non-autoregressive sampling in embedding space (Bao et al., 2025; Guinot et al., 2025; Tomasi et al., 2025).

**S019 — 한국어**

한편 확산 기반 생성 검색은 임베딩 공간에서 효율적인 비자기회귀 샘플링을 가능하게 한다(Bao et al., 2025; Guinot et al., 2025; Tomasi et al., 2025).

**S020 — Original**

This shifts retrieval from heavy, “System 2” autoregressive generation to parallel “System 1” sampling, allowing entire result "slates" or "bundles" to be generated in a single pass.

**S020 — 한국어**

이는 검색을 무거운 '시스템 2' 자기회귀 생성에서 병렬 '시스템 1' 샘플링으로 전환하여 전체 결과 슬레이트나 번들을 한 번의 패스로 생성하게 한다.

**S021 — Original**

By modeling retrieval as a denoising process, these systems can generate an entire “slate” or “bundle” of results in a single pass.

**S021 — 한국어**

검색을 잡음 제거 과정으로 모델링하면 이러한 시스템은 전체 결과 슬레이트나 번들을 단일 패스로 생성할 수 있다.

**S022 — Original**

Yet diffusion retrievers critically depend on large amounts of property-aligned training targets, precisely the resource that is scarce or ambiguous in non-decomposable, set-valued retrieval tasks.

**S022 — 한국어**

그러나 확산 검색기는 대량의 속성 정렬 학습 표적에 결정적으로 의존하며, 바로 이 자원이 비분해 가능한 집합값 검색 과제에서는 부족하거나 모호하다.

**S023 — Original**

In this paper, we address this bottleneck, which emerges because retrieval objectives have become richer than the supervision available to train efficient fan-out retrievers under those objectives.

**S023 — 한국어**

이 논문은 검색 목적이 그 목적 아래에서 효율적인 팬아웃 검색기를 학습할 수 있는 지도 신호보다 더 풍부해지면서 생긴 병목을 다룬다.

**S024 — Original**

Our key idea is to use RL not as the deployed inference mechanism, but as a one-time objective transducer that converts complex set-level reward specifications into scalable supervision for training the retriever.

**S024 — 한국어**

핵심 아이디어는 RL을 배포된 추론 메커니즘으로 쓰는 대신, 복잡한 집합 수준 보상 명세를 검색기 학습용 확장 가능한 지도 신호로 변환하는 일회성 목적 전환기로 사용하는 것이다.

**S025 — Original**

Specifically, we develop R4T (Retrieve for Train), a method that operates in three stages: (1) we train a fan-out policy implemented as a language model using RL with composite rewards that explicitly encode desired set-level properties; (2) we use the optimized policy to synthesize objective-consistent training data by harvesting and filtering successful trajectories; and (3) we train a lightweight, single-pass generative retriever on this synthesized data.

**S025 — 한국어**

구체적으로 저자들은 세 단계로 작동하는 R4T를 개발한다. (1) 원하는 집합 수준 속성을 명시적으로 인코딩한 복합 보상으로 언어 모델 기반 팬아웃 정책을 RL 학습하고, (2) 성공한 궤적을 수집·필터링하여 목적과 일치하는 학습 데이터를 합성하며, (3) 이 합성 데이터로 경량 단일 패스 생성 검색기를 학습한다.

**S026 — Original**

In our instantiation, this retriever is a coherent embedding-based diffusion model that performs efficient, controllable fan-out retrieval at inference time.

**S026 — 한국어**

이 논문의 구현에서 검색기는 추론 시점에 효율적이고 제어 가능한 팬아웃 검색을 수행하는 일관 임베딩 기반 확산 모델이다.

### Contributions

**S027 — Original**

We make three primary contributions.

**S027 — 한국어**

저자들의 주요 기여는 세 가지다.

**S028 — Original**

First, we present a general framework for compiling reward-optimized behaviors over set-valued, non-decomposable retrieval objectives into data for supervised training.

**S028 — 한국어**

첫째, 집합값·비분해 가능 검색 목적에 대해 보상 최적화된 행동을 지도학습 데이터로 컴파일하는 일반 프레임워크를 제시한다.

**S029 — Original**

Second, we instantiate this framework using Soft-GRPO for fan-out policy optimization and coherent embedding-based diffusion for single-pass generation at inference time.

**S029 — 한국어**

둘째, 팬아웃 정책 최적화에는 Soft-GRPO를, 추론 시점 단일 패스 생성에는 일관 임베딩 기반 확산을 사용해 프레임워크를 구체화한다.

**S030 — Original**

Third, we demonstrate the effectiveness of R4T in two distinct regimes: open-ended abstract retrieval (OAR), where no ground truth exists and quality is defined by reward-specified set-level properties over collection-level outputs; and weakly supervised compositional retrieval (WSCR), where each query admits many valid item sets and supervision is provided via weak reference sets.

**S030 — 한국어**

셋째, R4T의 효과를 두 가지 체제에서 보인다. 개방형 추상 검색(OAR)은 정답이 없고 모음 수준 출력에 대한 보상 명세 집합 속성으로 품질을 정의하며, 약지도 구성 검색(WSCR)은 질의마다 타당한 항목 집합이 여러 개이고 약한 참조 집합으로 지도 신호를 제공한다.

- **용어·약어 해설**
  - **OAR (Open-Ended Abstract Retrieval, 개방형 추상 검색)**: 유일한 참조 집합 없이 넓은 테마에 맞는 다양한 컬렉션을 찾는 과제다.
  - **WSCR (Weakly Supervised Compositional Retrieval, 약지도 구성 검색)**: 하나의 참조 집합을 약한 단서로 삼아 여러 상보적 항목을 조합하는 검색 과제다.

**S031 — Original**

Across both settings, R4T improves retrieval quality over strong fan-out baselines while maintaining the efficient inference needed for production-level deployment.

**S031 — 한국어**

두 설정 모두에서 R4T는 프로덕션 배포에 필요한 효율적 추론을 유지하면서 강력한 팬아웃 기준선보다 검색 품질을 높인다.

### Figure 1·2

**S032 — Original**

Figure 1: Overview of the R4T.

**S032 — 한국어**

그림 1: R4T 개요.

**S033 — Original**

Step 1 (§2.3) trains a fan-out language model (FOLM) using RL to produce property-aligned sub-queries.

**S033 — 한국어**

1단계(§2.3)는 RL로 팬아웃 언어 모델(FOLM)을 학습하여 속성에 정렬된 하위 질의를 생성한다.

- **용어·약어 해설**
  - **FOLM (Fan-Out Language Model, 팬아웃 언어 모델)**: 넓은 질의를 여러 하위 질의로 분해하는 정책 모델이다.

**S034 — Original**

Step 2 (§2.4) uses the trained FOLM to synthesize $(q,c)$ supervision data.

**S034 — 한국어**

2단계(§2.4)는 학습된 FOLM으로 $(q,c)$ 지도 데이터를 합성한다.

**S035 — Original**

Step 3 (§2.5) trains a diffusion-based fan-out retriever that samples content embeddings directly from query embeddings.

**S035 — 한국어**

3단계(§2.5)는 질의 임베딩에서 콘텐츠 임베딩을 직접 샘플링하는 확산 기반 팬아웃 검색기를 학습한다.

**S036 — Original**

Figure 2: Illustration of rewards used in OAR.

**S036 — 한국어**

그림 2: OAR에 사용하는 보상의 도해.

## 2 Method: R4T

**S037 — Original**

We introduce R4T (Retrieve-for-Train), a framework for training set-valued generative retrievers under non-decomposable objectives.

**S037 — 한국어**

저자들은 비분해 가능 목적 아래에서 집합값 생성 검색기를 학습하는 프레임워크 R4T를 소개한다.

**S038 — Original**

The central idea is to use reinforcement learning (RL) once as an objective transducer; rather than deploying an RL-tuned language model at inference time, we use RL to discover reward-aligned fan-out behaviors and convert them into scalable supervision for a lightweight, single-pass retriever.

**S038 — 한국어**

중심 아이디어는 강화학습을 목적 전환기로 한 번 사용하는 것이다. RL 조정 언어 모델을 추론 시점에 배포하는 대신, RL로 보상에 정렬된 팬아웃 행동을 발견하고 이를 경량 단일 패스 검색기를 위한 확장 가능한 지도 신호로 바꾼다.

### Problem Setup: Set-Valued Fan-out Retrieval

**S039 — Original**

We work in a setting where, given a broad query $q$, our retrieval system returns a set of results from a fixed database $\mathcal{D}$.

**S039 — 한국어**

넓은 질의 $q$가 주어졌을 때 검색 시스템이 고정 데이터베이스 $\mathcal{D}$에서 결과 집합을 반환하는 설정을 다룬다.

**S040 — Original**

To handle the set-based nature of retrieval, we consider a fan-out formulation, where a policy first generates $k$ sub-queries $Q=\{q_1,\ldots,q_k\}$, and a fixed retriever $R(\cdot)$ executes each sub-query to retrieve candidate results.

**S040 — 한국어**

검색의 집합적 성격을 다루기 위해 정책이 먼저 $k$개 하위 질의 $Q=\{q_1,\ldots,q_k\}$를 생성하고, 고정 검색기 $R(\cdot)$가 각 하위 질의를 실행해 후보 결과를 가져오는 팬아웃 정식화를 사용한다.

**S041 — Original**

Let $\mathcal{C}_i=R(q_i,\mathcal{D})$ denote the retrieved candidates for sub-query $q_i$, and $\mathcal{R}(Q)=\bigcup_{i=1}^k\mathcal{C}_i$ the union of the fan-out results.

**S041 — 한국어**

$\mathcal{C}_i=R(q_i,\mathcal{D})$를 하위 질의 $q_i$의 검색 후보라 하고, $\mathcal{R}(Q)=\bigcup_{i=1}^k\mathcal{C}_i$를 팬아웃 결과의 합집합이라 하자.

**S042 — Original**

Crucially, we assume that result quality is defined by set-level properties, such as diversity, coverage, or complementarity, which are generally non-decomposable and, moreover, admit multiple (non-unique) correct results.

**S042 — 한국어**

중요하게도 결과 품질은 다양성, 포괄성, 상보성과 같은 집합 수준 속성으로 정의된다고 가정하며, 이 속성들은 일반적으로 비분해 가능하고 여러 개의 비유일한 정답 결과를 허용한다.

**S043 — Original**

The latter property poses challenges for ground-truth supervision.

**S043 — 한국어**

뒤의 비유일성은 정답 기반 지도학습을 어렵게 한다.

### 2.1 R4T Overview

**S044 — Original**

R4T consists of three principle stages.

**S044 — 한국어**

R4T는 세 가지 주요 단계로 구성된다.

> **번역자 주:** 원문은 `principle stages`라고 쓰지만 문맥상 `principal stages`(주요 단계)의 오탈자로 보인다.

**S045 — Original**

The first is RL policy optimization, where we train a fan-out language model (FOLM) $\pi_\theta$ to generate sub-queries whose database interactions maximize some task-specific set-level reward (we discuss various rewards below).

**S045 — 한국어**

첫 단계는 RL 정책 최적화로, 데이터베이스와 상호작용했을 때 과제별 집합 수준 보상을 최대화하는 하위 질의를 생성하도록 FOLM $\pi_\theta$를 학습한다.

**S046 — Original**

The second phase is synthetic supervision, in which we run the optimized FOLM policy to collect high-reward trajectories and convert them into a synthetic dataset of set-valued targets.

**S046 — 한국어**

두 번째 단계는 합성 지도학습으로, 최적화된 FOLM 정책을 실행해 고보상 궤적을 모으고 이를 집합값 표적의 합성 데이터셋으로 변환한다.

**S047 — Original**

In the final stage, compiled deployment trains a lightweight generative retriever to model the conditional distribution of set-valued targets given the query, enabling efficient single-pass fan-out at inference time.

**S047 — 한국어**

마지막 컴파일 배포 단계에서는 질의가 주어졌을 때 집합값 표적의 조건부 분포를 모델링하도록 경량 생성 검색기를 학습해 추론 시 효율적인 단일 패스 팬아웃을 가능하게 한다.

**S048 — Original**

We detail each of these stages below (see Figure 1 for an graphical depiction).

**S048 — 한국어**

아래에서 각 단계를 자세히 설명한다(도식은 그림 1 참조).

> **번역자 주:** 원문의 `an graphical`은 문법상 `a graphical`의 오탈자다.

#### Two deployment variants: R4T-FOLM vs. R4T-Diffusion

**S049 — Original**

R4T separates reward-driven discovery of fan-out behaviors from efficient inference-time fan-out.

**S049 — 한국어**

R4T는 보상 주도의 팬아웃 행동 발견과 효율적인 추론 시점 팬아웃을 분리한다.

**S050 — Original**

We therefore evaluate two deployment variants that share the same RL optimization stage but differ in how fan-out is executed at test time.

**S050 — 한국어**

따라서 같은 RL 최적화 단계를 공유하지만 시험 시 팬아웃 실행 방식이 다른 두 배포 변형을 평가한다.

**S051 — Original**

R4T-FOLM (RL-tuned fan-out language model).

**S051 — 한국어**

R4T-FOLM(RL 조정 팬아웃 언어 모델).

**S052 — Original**

We directly deploy the RL-optimized FOLM $\pi_{\theta^\ast}$ at inference time to generate $k$ sub-queries $Q=\{q_1,\ldots,q_k\}\sim\pi_{\theta^\ast}(\cdot\mid q)$, whose retrieved results are aggregated into $\mathcal{R}(Q)=\bigcup_{i=1}^kR(q_i,\mathcal{D})$.

**S052 — 한국어**

추론 시 RL로 최적화한 FOLM $\pi_{\theta^\ast}$를 직접 배포해 $k$개 하위 질의 $Q=\{q_1,\ldots,q_k\}\sim\pi_{\theta^\ast}(\cdot\mid q)$를 생성하고, 검색 결과를 $\mathcal{R}(Q)=\bigcup_{i=1}^kR(q_i,\mathcal{D})$로 합친다.

**S053 — Original**

This variant reflects the quality of reward-optimized fan-out but incurs the cost of autoregressive generation and repeated retrieval calls.

**S053 — 한국어**

이 변형은 보상 최적화 팬아웃의 품질을 그대로 보여주지만 자기회귀 생성과 반복 검색 호출 비용을 부담한다.

**S054 — Original**

R4T-Diffusion (RL-distilled diffusion retriever).

**S054 — 한국어**

R4T-Diffusion(RL로 증류한 확산 검색기).

**S055 — Original**

We distill the reward-aligned fan-out behavior of $\pi_{\theta^\ast}$ into a lightweight diffusion model $D_\phi$ trained on synthetic supervision (Section 2.4).

**S055 — 한국어**

$\pi_{\theta^\ast}$의 보상 정렬 팬아웃 행동을 합성 지도 데이터로 학습한 경량 확산 모델 $D_\phi$에 증류한다(§2.4).

**S056 — Original**

At inference time, $D_\phi$ generates $L$ retrieval directions in a single non-autoregressive pass, $\mathbf{Z}_0\sim p_\phi(\mathbf{Z}\mid z_q)$, which are mapped to database contents via nearest-neighbor retrieval.

**S056 — 한국어**

추론 시 $D_\phi$는 단일 비자기회귀 패스로 $L$개 검색 방향 $\mathbf{Z}_0\sim p_\phi(\mathbf{Z}\mid z_q)$를 생성하고, 최근접 이웃 검색으로 이를 데이터베이스 콘텐츠에 매핑한다.

**S057 — Original**

This variant evaluates whether reward-optimized fan-out can be retained under efficient single-pass inference.

**S057 — 한국어**

이 변형은 효율적인 단일 패스 추론에서도 보상 최적화 팬아웃을 유지할 수 있는지 평가한다.

**S058 — Original**

Comparing these variants disentangles the benefits of reward-optimized fan-out from the cost of deploying it, directly testing whether RL-discovered behaviors can be distilled for efficient inference.

**S058 — 한국어**

두 변형의 비교는 보상 최적화 팬아웃의 이점과 배포 비용을 분리하며, RL이 발견한 행동을 효율적 추론용으로 증류할 수 있는지 직접 시험한다.

### 2.2 Set-Level Objectives and Rewards

**S059 — Original**

A key component of R4T is the ability specifying set-level objectives as rewards to be used in FOLM policy optimization (Stage 1).

**S059 — 한국어**

R4T의 핵심 구성 요소는 집합 수준 목적을 FOLM 정책 최적화(1단계)에 사용할 보상으로 지정하는 능력이다.

> **번역자 주:** 원문 `the ability specifying`은 문법상 `the ability to specify`가 자연스럽다.

**S060 — Original**

We study two regimes that capture common set-valued retrieval needs.

**S060 — 한국어**

일반적인 집합값 검색 요구를 포착하는 두 체제를 연구한다.

#### 2.2.1 Open-Ended Abstract Retrieval

**S061 — Original**

Open-ended abstract retrieval (OAR) targets open-ended exploration where no unique ground truth set exists.

**S061 — 한국어**

OAR은 유일한 정답 집합이 존재하지 않는 개방형 탐색을 대상으로 한다.

**S062 — Original**

Given a broad query $q$ (e.g., a theme or scenario), the goal is to retrieve a set of collection-level or abstract results that are (i) diverse (i.e., cover multiple interpretations), (ii) well-aligned with $q$, and (iii) grounded with respect to the database.

**S062 — 한국어**

테마나 상황 같은 넓은 질의 $q$가 주어졌을 때 목표는 (i) 여러 해석을 포괄하여 다양하고, (ii) $q$와 잘 정렬되며, (iii) 데이터베이스에 근거한 모음 수준 또는 추상적 결과 집합을 검색하는 것이다.

**S063 — Original**

We define a composite reward $\mathcal{R}_{\text{abs}}$ over a generated fan-out set $Q$ as follows:

**S063 — 한국어**

생성된 팬아웃 집합 $Q$에 대한 복합 보상 $\mathcal{R}_{\text{abs}}$를 다음과 같이 정의한다.

$$
\mathcal{R}_{\text{abs}}(q,Q)=\lambda_g r_{\text{ground}}(Q)+\lambda_d r_{\text{div}}(Q)+\lambda_a r_{\text{align}}(q,Q). \tag{1}
$$

**수식 해설:** $\lambda_g,\lambda_d,\lambda_a$는 각각 근거성, 다양성, 정렬성 보상의 혼합 가중치다. 세 하위 보상을 하나의 스칼라 RL 보상으로 결합한다.

**S064 — Original**

This reward uses subrewards $r_{\text{ground}}$, $r_{\text{div}}$ and $r_{\text{align}}$, to capture groundedness, diversity and alignment, respectively, each contributing according to their mixture weights ($lambda$).

**S064 — 한국어**

이 보상은 하위 보상 $r_{\text{ground}}$, $r_{\text{div}}$, $r_{\text{align}}$로 각각 근거성, 다양성, 정렬성을 포착하며 각 항은 혼합 가중치에 따라 기여한다.

> **번역자 주:** 원문은 LaTeX 명령의 역슬래시가 빠진 `$lambda$`로 적혀 있으나 수식 (1)의 $\lambda$를 뜻한다.

**S065 — Original**

To capture diversity of the results set, we measure the semantic breadth of the fan-out using the Vendi Score (Friedman and Dieng, 2022) computed on representatives of each sub-query (e.g., top-1 retrieved item per sub-query), that is,

**S065 — 한국어**

결과 집합의 다양성을 포착하기 위해 각 하위 질의의 대표 항목, 예를 들어 하위 질의별 상위 1개 검색 항목에 계산한 Vendi Score로 팬아웃의 의미적 폭을 측정한다(Friedman and Dieng, 2022).

$$
r_{\text{div}}(Q)=\operatorname{Vendi}(\{e_{\text{content}}(c_i^\star)\}_{i=1}^{k}). \tag{2}
$$

**S066 — Original**

where $c_i^\star$ is a representative retrieved item for $q_i$ and $e_{\text{content}}(\cdot)$ is the content encoder that embeds database items.

**S066 — 한국어**

여기서 $c_i^\star$는 $q_i$의 대표 검색 항목이고, $e_{\text{content}}(\cdot)$는 데이터베이스 항목을 임베딩하는 콘텐츠 인코더다.

- **용어·약어 해설**
  - **Vendi Score(벤디 점수)**: 유사도 행렬의 고윳값 분포에 기반해 표본 집합의 유효 다양성을 측정한다. 이 논문에서는 값이 클수록 검색 방향이 의미적으로 더 다양함을 뜻한다.

**S067 — Original**

To ensure groundedness, we encourage sub-queries to stay on the database manifold (induced by the embedding space) by penalizing the distance between each sub-query embedding and its nearest neighbor in the database, namely,

**S067 — 한국어**

근거성을 보장하기 위해 각 하위 질의 임베딩과 데이터베이스 내 최근접 이웃 사이 거리를 벌점으로 주어 하위 질의가 임베딩 공간이 유도한 데이터베이스 다양체 위에 머물도록 유도한다.

$$
r_{\text{ground}}(Q)=1-\frac{1}{k}\sum_{i=1}^{k}\min_{c\in\mathcal{D}}\lVert e_{\text{text}}(q_i)-e_{\text{content}}(c)\rVert_2. \tag{3}
$$

**S068 — Original**

where $e_{\text{text}}(q_i)$ is a query embedding.

**S068 — 한국어**

여기서 $e_{\text{text}}(q_i)$는 질의 임베딩이다.

**수식 해설:** 최근접 콘텐츠와의 $L_2$ 거리가 작을수록 $r_{\text{ground}}$가 커진다. 임베딩 정규화와 거리 범위에 관한 추가 명시는 원문에 없다.

**S069 — Original**

Finally, alignment is used to prevent semantic drift from the intent of the original query $q$ by anchoring each sub-query to $q$ with the following reward:

**S069 — 한국어**

마지막으로 각 하위 질의를 원 질의 $q$에 고정하는 다음 보상을 사용해 원래 의도에서의 의미적 표류를 막는다.

$$
r_{\text{align}}(q,Q)=\frac{1}{k}\sum_{i=1}^{k}\cos(e_{\text{text}}(q_i),e_{\text{text}}(q)). \tag{4}
$$

**수식 해설:** 각 하위 질의와 원 질의 임베딩의 코사인 유사도를 평균한다. 지나치게 높은 정렬성만 추구하면 하위 질의가 원 질의의 재진술로 붕괴할 수 있다.

**S070 — Original**

We set $\lambda_g=0.6$ and $\lambda_d=\lambda_a=0.2$ by default.

**S070 — 한국어**

기본값은 $\lambda_g=0.6$, $\lambda_d=\lambda_a=0.2$로 설정한다.

**S071 — Original**

Figure 2 illustrates the rewards used for OAR tasks.

**S071 — 한국어**

그림 2는 OAR 과제에 사용하는 보상을 보여준다.

#### 2.2.2 Weakly Supervised Compositional Retrieval

**S072 — Original**

Weakly supervised compositional retrieval (WSCR) targets settings where each query admits many valid item sets, but we have weak reference sets that represent one plausible realization.

**S072 — 한국어**

WSCR은 질의마다 타당한 항목 집합이 여러 개지만, 그중 하나의 가능한 실현을 나타내는 약한 참조 집합이 있는 설정을 대상으로 한다.

**S073 — Original**

Each query $q$ is paired with a reference set $\mathcal{Y}=\{y_1,\ldots,y_m\}$; importantly, $\mathcal{Y}$ is not assumed to be the unique correct query response.

**S073 — 한국어**

각 질의 $q$는 참조 집합 $\mathcal{Y}=\{y_1,\ldots,y_m\}$와 짝을 이루며, 중요한 점은 $\mathcal{Y}$를 유일하게 올바른 질의 응답으로 가정하지 않는다는 것이다.

**S074 — Original**

We define a reference-set-based coverage reward for a fan-out set $Q$ as follows:

**S074 — 한국어**

팬아웃 집합 $Q$에 대한 참조 집합 기반 포괄성 보상을 다음과 같이 정의한다.

$$
\mathcal{R}_{\text{set}}(q,Q;\mathcal{Y})=\frac{|\mathcal{Y}\cap\mathcal{R}(Q)|}{|\mathcal{Y}|}. \tag{5}
$$

**수식 해설:** 팬아웃 결과 합집합 $\mathcal{R}(Q)$이 참조 집합 $\mathcal{Y}$의 항목을 얼마나 포함했는지 비율로 측정한다.

**S075 — Original**

This reward encourages the policy to generate complementary sub-queries whose union spans different semantic components reflected in $\mathcal{Y}$, rather than memorizing a fixed target.

**S075 — 한국어**

이 보상은 정책이 고정 표적을 암기하는 대신, 합집합으로 $\mathcal{Y}$에 반영된 서로 다른 의미 구성 요소를 포괄하는 상보적 하위 질의를 생성하도록 장려한다.

### 2.3 Fan-Out LM Training via Soft-GRPO

**S076 — Original**

The first stage of R4T is RK training of the fan-out language model (FOLM).

**S076 — 한국어**

R4T의 첫 단계는 팬아웃 언어 모델(FOLM)의 `RK` 학습이다.

> **번역자 주:** 원문 PDF·TeX 모두 `RK training`으로 표기한다. 문맥과 절 제목상 `RL training`의 오탈자일 가능성이 높지만 원문을 임의 수정하지 않았다.

**S077 — Original**

Given an input query $q$, the FOLM $\pi_\theta$ generates a set of candidate sub-queries $Q=\{q_1,\dots,q_k\}$.

**S077 — 한국어**

입력 질의 $q$가 주어지면 FOLM $\pi_\theta$는 후보 하위 질의 집합 $Q=\{q_1,\dots,q_k\}$를 생성한다.

**S078 — Original**

These sub-queries are executed by a frozen dense retriever $R(\cdot)$ to obtain candidate documents $\mathcal{C}_i=R(q_i,\mathcal{D})$.

**S078 — 한국어**

동결된 밀집 검색기 $R(\cdot)$가 이 하위 질의를 실행해 후보 문서 $\mathcal{C}_i=R(q_i,\mathcal{D})$를 얻는다.

**S079 — Original**

We assign a reward to each sampled fan-out output using the relevant task objective (as defined in Section 2.2).

**S079 — 한국어**

§2.2에서 정의한 해당 과제 목적을 사용해 샘플링된 각 팬아웃 출력에 보상을 부여한다.

**S080 — Original**

To optimize $\pi_\theta$, we employ group relative policy optimization (GRPO).

**S080 — 한국어**

$\pi_\theta$를 최적화하기 위해 그룹 상대 정책 최적화(GRPO)를 사용한다.

- **용어·약어 해설**
  - **GRPO (Group Relative Policy Optimization, 그룹 상대 정책 최적화)**: 같은 입력에서 여러 출력을 샘플링하고 그룹 내부 보상 평균·표준편차로 상대적 이점을 계산하는 정책 최적화 방식이다.

**S081 — Original**

For a query $q$, we sample a set of $G$ outputs $\{o_1,\dots,o_G\}$ and compute advantages using group statistics:

**S081 — 한국어**

질의 $q$마다 $G$개 출력 집합 $\{o_1,\dots,o_G\}$를 샘플링하고 그룹 통계로 이점을 계산한다.

$$
A_i=\frac{r_i-\mu_G}{\sigma_G+\epsilon},\qquad
\mu_G=\frac{1}{G}\sum_{j=1}^{G}r_j. \tag{6}
$$

**수식 해설:** $r_i$는 출력 $i$의 보상, $\mu_G$와 $\sigma_G$는 그룹 보상의 평균과 표준편차, $\epsilon$은 0으로 나누는 것을 막는 작은 상수다. 평균보다 좋은 출력은 양의 이점을 얻는다.

#### Soft-PPO Regularization

**S082 — Original**

To stabilize open-ended generation, we adopt soft PPO (Zhang et al., 2025b; Becker et al., 2025; Liang et al., 2025), which augments GRPO with both forward and reverse KL penalties between the active policy $\pi_\theta$ and the sampling policy $\pi_{\text{old}}$:

**S082 — 한국어**

개방형 생성을 안정화하기 위해 활성 정책 $\pi_\theta$와 샘플링 정책 $\pi_{\text{old}}$ 사이의 정방향·역방향 KL 벌점을 모두 GRPO에 더하는 soft PPO를 사용한다(Zhang et al., 2025b; Becker et al., 2025; Liang et al., 2025).

$$
\begin{aligned}
\mathcal{J}(\theta)=\mathbb{E}_{\pi_{\text{old}}}\big[
\mathcal{L}_{\text{GRPO}}
&-\beta_1\mathbb{D}_{\text{KL}}(\pi_\theta\Vert\pi_{\text{old}})\\
&-\beta_2\mathbb{D}_{\text{KL}}(\pi_{\text{old}}\Vert\pi_\theta)
\big].
\end{aligned} \tag{7}
$$

**수식 해설:** 정방향 KL은 새 정책이 이전 정책에서 벗어나는 방향을, 역방향 KL은 이전 정책이 새 정책에서 지지되지 않는 방향을 각각 억제한다. $\beta_1,\beta_2$가 두 규제 강도를 정한다.

**S083 — Original**

In practice we implement this as:

**S083 — 한국어**

실제로는 다음과 같이 구현한다.

$$
\begin{aligned}
\mathcal{L}(\theta)=\mathbb{E}_t\Big[
&-\min\big(\rho_tA_t,\operatorname{clip}(\rho_t,1-\epsilon,1+\epsilon)A_t\big)\\
&+\beta_1\rho_t\big(\log\pi_\theta(o_t)-\log\pi_{\text{old}}(o_t)\big)\\
&+\beta_2\big(-\log\pi_\theta(o_t)\big)
\Big].
\end{aligned} \tag{8}
$$

**S084 — Original**

where $\rho_t=\pi_\theta/\pi_{\text{old}}$ is the importance ratio.

**S084 — 한국어**

여기서 $\rho_t=\pi_\theta/\pi_{\text{old}}$는 중요도 비율이다.

**수식 해설:** 첫 항은 PPO의 클리핑된 정책 손실이고, 뒤의 두 항은 양방향 정책 이탈을 억제하는 soft-PPO 규제다. 원문 구현식의 마지막 항은 $-\log\pi_\theta(o_t)$로 제시되어 있다.

### 2.4 Synthetic Supervision

**S085 — Original**

The second phase of R4T ivnovles the generation of a synthetic dataset used to train the retrieval model,

**S085 — 한국어**

R4T의 두 번째 단계는 검색 모델 학습에 사용할 합성 데이터셋 생성을 포함한다.

> **번역자 주:** 원문은 `ivnovles`라고 쓰며 `involves`의 오탈자로 보인다. 또한 원문 문장은 쉼표로 끝나 다음 문장과 비문법적으로 이어진다.

**S086 — Original**

The FOLM $\pi_{\theta^\ast}$ serves as a behavior generator that induces a distribution over fan-out retrieval patterns shaped by the reward.

**S086 — 한국어**

FOLM $\pi_{\theta^\ast}$는 보상이 형성한 팬아웃 검색 패턴의 분포를 유도하는 행동 생성기 역할을 한다.

**S087 — Original**

For each query $q$, we sample fan-out outputs from $\pi_{\theta^\ast}$ and execute retrieval against the fixed database.

**S087 — 한국어**

각 질의 $q$에 대해 $\pi_{\theta^\ast}$에서 팬아웃 출력을 샘플링하고 고정 데이터베이스를 대상으로 검색을 실행한다.

**S088 — Original**

We use the FOLM generations as supervision, allowing the downstream model to learn the full distribution of behaviors induced by the RL process above.

**S088 — 한국어**

FOLM의 생성 결과를 지도 신호로 사용하여 다운스트림 모델이 위 RL 과정에서 유도된 행동의 전체 분포를 학습하게 한다.

**S089 — Original**

To train a downstream model that generates multiple retrieval embeddings in a single forward pass, we represent each fan-out result as a coherent target tensor $\mathbf{Z}_{\text{target}}\in\mathbb{R}^{L\times d}$.

**S089 — 한국어**

한 번의 순전파로 여러 검색 임베딩을 생성하는 다운스트림 모델을 학습하기 위해 각 팬아웃 결과를 일관 표적 텐서 $\mathbf{Z}_{\text{target}}\in\mathbb{R}^{L\times d}$로 표현한다.

**수식 해설:** $L$은 한 표적 집합에 담긴 검색 방향 수이고 $d$는 각 임베딩 차원이다. 따라서 행 하나가 검색 방향 하나를 나타낸다.

**S090 — Original**

Each row of $\mathbf{Z}_{\text{target}}$ corresponds to one retrieval direction discovered by the FOLM.

**S090 — 한국어**

$\mathbf{Z}_{\text{target}}$의 각 행은 FOLM이 발견한 하나의 검색 방향에 대응한다.

**S091 — Original**

The construction of $\mathbf{Z}_{\text{target}}$ depends on the optimization objective.

**S091 — 한국어**

$\mathbf{Z}_{\text{target}}$의 구성은 최적화 목적에 따라 달라진다.

**S092 — Original**

For OAR tasks, the objective emphasizes the production of diverse and grounded retrieved results.

**S092 — 한국어**

OAR 과제의 목적은 다양하고 근거 있는 검색 결과 생성에 중점을 둔다.

**S093 — Original**

Accordingly, we construct $\mathbf{Z}_{\text{target}}$ from the embeddings of the retrieved contents $\{z_{c_1},\ldots,z_{c_L}\}$ corresponding to the fan-out outputs.

**S093 — 한국어**

이에 따라 팬아웃 출력에 해당하는 검색 콘텐츠 임베딩 $\{z_{c_1},\ldots,z_{c_L}\}$로 $\mathbf{Z}_{\text{target}}$를 구성한다.

**S094 — Original**

This formulation directly distills the distribution over database-grounded collections induced by the RL-trained policy.

**S094 — 한국어**

이 정식화는 RL 학습 정책이 유도한 데이터베이스 근거 모음의 분포를 직접 증류한다.

**S095 — Original**

For WSCR tasks, the objective emphasizes discovery of complementary search directions that jointly cover a reference set.

**S095 — 한국어**

WSCR 과제의 목적은 함께 참조 집합을 포괄하는 상보적 검색 방향의 발견에 중점을 둔다.

**S096 — Original**

In this case, we construct $\mathbf{Z}_{\text{target}}$ from the embeddings of the optimized sub-queries generated by the FOLM, $\{e_{\text{text}}(q_1),\ldots,e_{\text{text}}(q_L)\}$.

**S096 — 한국어**

이 경우 FOLM이 생성한 최적화 하위 질의의 임베딩 $\{e_{\text{text}}(q_1),\ldots,e_{\text{text}}(q_L)\}$로 $\mathbf{Z}_{\text{target}}$를 구성한다.

**S097 — Original**

This choice allows the downstream model to internalize the search decomposition strategy learned by RL.

**S097 — 한국어**

이 선택은 다운스트림 모델이 RL이 학습한 검색 분해 전략을 내재화하게 한다.

**S098 — Original**

Because set-valued retrieval is order-agnostic, we randomly permute the rows of $\mathbf{Z}_{\text{target}}$ during training to encourage permutation robustness.

**S098 — 한국어**

집합값 검색은 순서와 무관하므로 학습 중 $\mathbf{Z}_{\text{target}}$의 행을 무작위로 순열화하여 순열 견고성을 장려한다.

**S099 — Original**

The resulting synthetic dataset is $\mathcal{T}_{\text{syn}}=\{(z_q,\mathbf{Z}_{\text{target}})\}$, which captures the full fan-out retrieval distribution induced by the reward-optimized policy.

**S099 — 한국어**

그 결과 얻는 합성 데이터셋은 $\mathcal{T}_{\text{syn}}=\{(z_q,\mathbf{Z}_{\text{target}})\}$이며, 보상 최적화 정책이 유도한 전체 팬아웃 검색 분포를 포착한다.

### 2.5 Diffusion for Single-Pass Fan-out

**S100 — Original**

The final phase of RT4 is the training of a generative retriever $D_\phi$ to model $p(\mathbf{Z}_{\text{target}}\mid z_q)$.

**S100 — 한국어**

`RT4`의 마지막 단계는 $p(\mathbf{Z}_{\text{target}}\mid z_q)$를 모델링하도록 생성 검색기 $D_\phi$를 학습하는 것이다.

> **번역자 주:** 원문은 `RT4`라고 표기하지만 논문 전체의 방법명은 `R4T`이므로 오탈자로 보인다.

**S101 — Original**

We adopt the variancee exploding (VE) diffusion formulation of Song et al. (2020) within the EDM framework (Karras et al., 2022).

**S101 — 한국어**

EDM 프레임워크(Karras et al., 2022) 안에서 Song et al. (2020)의 분산 폭발(VE) 확산 정식화를 채택한다.

> **번역자 주:** 원문의 `variancee exploding`은 `variance exploding`의 오탈자다.

- **용어·약어 해설**
  - **VE (Variance Exploding, 분산 폭발)**: 순방향 과정에서 데이터에 더하는 잡음의 분산이 시간에 따라 증가하는 확산 설정이다.
  - **EDM (Elucidating the Design Space of Diffusion-Based Generative Models)**: 잡음 수준별 사전조건화와 가중 방식을 체계화한 확산 모델 설계 프레임워크다.

**S102 — Original**

The denoiser $D_\phi(\mathbf{Z}_t;\sigma,z_q)$ is trained to recover clean targets from noisy inputs using the loss

**S102 — 한국어**

잡음 제거기 $D_\phi(\mathbf{Z}_t;\sigma,z_q)$는 다음 손실을 사용해 잡음 입력에서 깨끗한 표적을 복원하도록 학습된다.

$$
\mathcal{L}_{\text{diff}}=
\mathbb{E}_{\sigma,\epsilon}\left[
\lambda(\sigma)\left\lVert
D_\phi(\mathbf{Z}_{\text{target}}+\sigma\epsilon;\sigma,z_q)-\mathbf{Z}_{\text{target}}
\right\rVert^2
\right]. \tag{9}
$$

**S103 — Original**

where $\lambda(\sigma)=(\sigma^2+\sigma_{\text{data}}^2)/(\sigma\cdot\sigma_{\text{data}})^2$ balances contributions across noise levels.

**S103 — 한국어**

여기서 $\lambda(\sigma)=(\sigma^2+\sigma_{\text{data}}^2)/(\sigma\cdot\sigma_{\text{data}})^2$는 잡음 수준별 기여를 균형 있게 조정한다.

**수식 해설:** $\epsilon$은 잡음, $\sigma$는 잡음 크기, $\sigma_{\text{data}}$는 데이터 표준편차다. 모델은 질의 임베딩 $z_q$를 조건으로 $L\times d$ 표적 텐서 전체를 동시에 복원한다.

#### Architecture

**S104 — Original**

The denoiser is instantiated as a transformer (Peebles and Xie, 2023; Tomasi et al., 2025) tailored for structural coherence, adopting the preconditioning scheme proposed by Karras et al. (2022).

**S104 — 한국어**

잡음 제거기는 구조적 일관성에 맞춘 Transformer로 구현하며(Peebles and Xie, 2023; Tomasi et al., 2025), Karras et al. (2022)의 사전조건화 방식을 채택한다.

**S105 — Original**

The query embedding $z_q$ is injected via cross-attention.

**S105 — 한국어**

질의 임베딩 $z_q$는 교차 어텐션으로 주입한다.

**S106 — Original**

We use classifier-free guidance (CFG) (Ho and Salimans, 2022) by randomly dropping $z_q$ during training.

**S106 — 한국어**

학습 중 $z_q$를 무작위로 제거하는 방식으로 분류기 없는 가이던스(CFG)를 사용한다(Ho and Salimans, 2022).

- **용어·약어 해설**
  - **CFG (Classifier-Free Guidance, 분류기 없는 가이던스)**: 조건부·무조건부 예측을 조합하여 외부 분류기 없이 조건 준수 강도를 조절한다.

**S107 — Original**

At inference time, we solve the probability flow stochastic differential equation to generate $\mathbf{Z}_0$, which is sliced into $L$ embeddings and mapped to database contents via nearest-neighbor retrieval.

**S107 — 한국어**

추론 시 확률 흐름 확률미분방정식을 풀어 $\mathbf{Z}_0$를 생성하고, 이를 $L$개 임베딩으로 나눈 다음 최근접 이웃 검색으로 데이터베이스 콘텐츠에 매핑한다.

---

## 3 Experiments

### 3.1 Experimental Setup

**S108 — Original**

We evaluate R4T on both OAR (no ground-truth; property-defined quality) and WSCR (weak reference sets; coverage-oriented) tasks, with objectives as defined in Section 2.2.

**S108 — 한국어**

§2.2에서 정의한 목적을 사용해 R4T를 OAR(정답 없음, 속성으로 품질 정의)과 WSCR(약한 참조 집합, 포괄성 지향) 과제 모두에서 평가한다.

#### Datasets

**S109 — Original**

We evaluate R4T on two diverse real-world datasets that reflect distinct retrieval modalities (text-to-image, text-to-music) and domains.

**S109 — 한국어**

서로 다른 검색 모달리티(텍스트-이미지, 텍스트-음악)와 도메인을 반영하는 두 가지 실제 데이터셋에서 R4T를 평가한다.

**S110 — Original**

The first is Polyvore, a large-scale fashion benchmark (Han et al., 2017) comprised of user-curated outfits.

**S110 — 한국어**

첫 번째는 사용자가 구성한 의상으로 이루어진 대규모 패션 벤치마크 Polyvore다(Han et al., 2017).

**S111 — Original**

Each outfit functions as a ground-truth item set, containing compatible fashion products across diverse categories (e.g., tops, bottoms, shoes, accessories).

**S111 — 한국어**

각 의상은 상의, 하의, 신발, 액세서리 등 여러 범주의 서로 어울리는 패션 제품을 담은 정답 항목 집합 역할을 한다.

**S112 — Original**

The dataset provides rich multimodal features, including product images and textual metadata, which we use to evaluate both multimodal groundedness and set coherence.

**S112 — 한국어**

이 데이터셋은 제품 이미지와 텍스트 메타데이터를 포함한 풍부한 멀티모달 특징을 제공하며, 이를 멀티모달 근거성과 집합 일관성 평가에 사용한다.

**S113 — Original**

The candidate retrieval pool sizes are 21,888 (collections/abstracts) and 142,472 (items) for Task 1 and Task 2, respectively.

**S113 — 한국어**

후보 검색 풀의 크기는 과제 1에서 21,888개 모음/추상 항목, 과제 2에서 142,472개 항목이다.

**S114 — Original**

Music, our second dataset, is a proprietary industrial dataset consisting of expert-generated music playlists.

**S114 — 한국어**

두 번째 Music 데이터셋은 전문가가 만든 음악 재생목록으로 구성된 비공개 산업 데이터셋이다.

**S115 — Original**

Each playlist represents a coherent sequence of tracks, serving as a ground-truth set for retrieval.

**S115 — 한국어**

각 재생목록은 일관된 트랙 순서를 나타내며 검색의 정답 집합 역할을 한다.

**S116 — Original**

This dataset evaluates the model's ability to model thematic consistency and intent coverage in the music domain.

**S116 — 한국어**

이 데이터셋은 음악 도메인에서 주제 일관성과 의도 포괄성을 모델링하는 능력을 평가한다.

**S117 — Original**

The candidate retrieval pool size is 8,522 (playlist embeddings) for Task 1.

**S117 — 한국어**

과제 1의 후보 검색 풀은 재생목록 임베딩 8,522개다.

**S118 — Original**

Details of broad query generation are provided in Appendix C.

**S118 — 한국어**

넓은 질의 생성 세부사항은 부록 C에 제시한다.

#### Retrieval Backbone

**S119 — Original**

We adopt dataset-specific embedding backbones to enable efficient fan-out in a shared embedding space.

**S119 — 한국어**

공유 임베딩 공간에서 효율적인 팬아웃을 가능하게 하도록 데이터셋별 임베딩 백본을 채택한다.

**S120 — Original**

For Polyvore, we use a CLIP-based image-text encoder trained with matryoshka representation learning (Kusupati et al., 2022), which supports multimodal retrieval while allowing flexible embedding truncation.

**S120 — 한국어**

Polyvore에는 마트료시카 표현 학습으로 훈련된 CLIP 기반 이미지-텍스트 인코더를 사용한다(Kusupati et al., 2022). 이 인코더는 임베딩을 유연하게 잘라 쓰면서 멀티모달 검색을 지원한다.

- **용어·약어 해설**
  - **CLIP (Contrastive Language-Image Pre-training)**: 이미지와 텍스트를 공동 임베딩 공간에 정렬하는 대조학습 모델이다.
  - **matryoshka representation learning(마트료시카 표현 학습)**: 긴 임베딩의 앞부분만 잘라 사용해도 유용하도록 여러 차원의 중첩 표현을 함께 학습한다.

**S121 — Original**

Unless otherwise specified, we use an embedding dimension of 128 to balance retrieval accuracy and efficiency in our main experiments.

**S121 — 한국어**

별도 언급이 없으면 주요 실험에서 검색 정확도와 효율의 균형을 위해 임베딩 차원을 128로 사용한다.

**S122 — Original**

For the music dataset, we employ MuLan (Huang et al., 2022), a joint music-text embedding model trained on large-scale audio-language pairs, and perform retrieval directly in the MuLan embedding space.

**S122 — 한국어**

음악 데이터셋에는 대규모 오디오-언어 쌍으로 학습한 음악-텍스트 공동 임베딩 모델 MuLan을 사용하고(Huang et al., 2022), MuLan 임베딩 공간에서 직접 검색한다.

#### Baselines

**S123 — Original**

We compare R4T against three baselines.

**S123 — 한국어**

R4T를 세 기준선과 비교한다.

**S124 — Original**

The No Fan-out baseline directly retrieves $n\times k$ content items using the original query without any sub-query expansion.

**S124 — 한국어**

No Fan-out 기준선은 하위 질의 확장 없이 원 질의로 $n\times k$개의 콘텐츠 항목을 직접 검색한다.

**S125 — Original**

This represents the traditional dense retrieval approach and serves as a lower bound for fan-out methods.

**S125 — 한국어**

이는 전통적인 밀집 검색 방식을 나타내며 팬아웃 방법의 하한 역할을 한다.

**S126 — Original**

A second baseline, Zero-shot Fan-out uses the base language model (before RL training) to generate $k$ sub-queries without any task-specific optimization.

**S126 — 한국어**

두 번째 기준선 Zero-shot Fan-out은 과제별 최적화 없이 RL 학습 전 기본 언어 모델로 $k$개 하위 질의를 생성한다.

**S127 — Original**

Each sub-query retrieves $n$ items, resulting in $n\times k$ total items.

**S127 — 한국어**

각 하위 질의가 $n$개 항목을 검색하므로 총 항목 수는 $n\times k$개다.

**S128 — Original**

We test several variants of the Zero-shot Fan-out baseline with different language models used for sub-query generation: (a) Gemini-2.5-Flash (Comanici et al., 2025), a large-scale proprietary model with strong zero-shot capabilities; (b) Gemma3-4B (Team et al., 2025), a smaller open-source model (4B parameters); and (c) Qwen3-4B (Yang et al., 2025), another competitive open-source model (4B parameters).

**S128 — 한국어**

하위 질의 생성 모델을 달리한 여러 Zero-shot Fan-out 변형을 시험한다. (a) 강한 제로샷 능력을 지닌 대규모 비공개 모델 Gemini-2.5-Flash(Comanici et al., 2025), (b) 더 작은 40억 매개변수 오픈소스 모델 Gemma3-4B(Team et al., 2025), (c) 또 다른 경쟁력 있는 40억 매개변수 오픈소스 모델 Qwen3-4B(Yang et al., 2025)다.

**S129 — Original**

Best-of-N is our the third baseline, a strong baseline that performs fan-out $N$ times using the zero-shot model and selects the best result according to our training rewards.

**S129 — 한국어**

세 번째 기준선 Best-of-N은 제로샷 모델로 팬아웃을 $N$번 수행하고 학습 보상에 따라 최상의 결과를 선택하는 강력한 기준선이다.

> **번역자 주:** 원문의 `our the third baseline`은 중복된 관사 표현이다.

**S130 — Original**

We set $N=5$.

**S130 — 한국어**

$N=5$로 설정한다.

**S131 — Original**

We compare two variants of our method, R4T-(FOLM/Diffusion).

**S131 — 한국어**

제안 방법의 두 변형 R4T-FOLM과 R4T-Diffusion을 비교한다.

**S132 — Original**

R4T first trains the fan-out language model using RL with task-specific rewards, synthesizes training data, and trains a diffusion-based retriever.

**S132 — 한국어**

R4T는 먼저 과제별 보상으로 팬아웃 언어 모델을 RL 학습하고, 학습 데이터를 합성한 뒤 확산 기반 검색기를 학습한다.

**S133 — Original**

At inference time, the diffusion retriever directly samples $k$ content embeddings from the query embedding.

**S133 — 한국어**

추론 시 확산 검색기는 질의 임베딩에서 $k$개 콘텐츠 임베딩을 직접 샘플링한다.

**S134 — Original**

For all fan-out baselines and R4T, we report results with $k=10$ sub-queries.

**S134 — 한국어**

모든 팬아웃 기준선과 R4T에서 $k=10$개 하위 질의를 사용한 결과를 보고한다.

#### Evaluation Metrics

**S135 — Original**

We evaluate set-valued retrieval using task-specific metrics.

**S135 — 한국어**

과제별 지표를 사용해 집합값 검색을 평가한다.

**S136 — Original**

For OAR tasks, where no ground-truth sets exist, we employ LLM-as-a-Judge evaluation using Gemini-2.5-Pro to assess three dimensions: collection diversity, query-collection alignment, and groundedness.

**S136 — 한국어**

정답 집합이 없는 OAR 과제에는 Gemini-2.5-Pro를 심판으로 쓰는 LLM-as-a-Judge 평가를 사용해 모음 다양성, 질의-모음 정렬성, 근거성의 세 차원을 평가한다.

> **번역자 주:** 본문은 Gemini-2.5-Pro라고 적지만 Appendix B(S273)는 Gemini-2.5-Flash라고 적는다. 이는 재현에 영향을 주는 원문 내부 불일치이며 공개 자료만으로 실제 심판 모델을 확정할 수 없다.

**S137 — Original**

Each dimension is scored on a 5-point Likert scale, following prior work showing strong correlation with human judgments (Zheng et al., 2023).

**S137 — 한국어**

인간 판단과 강한 상관을 보인 선행 연구를 따라 각 차원을 5점 리커트 척도로 채점한다(Zheng et al., 2023).

**S138 — Original**

For WSCR tasks, we report reference-based coverage metrics (Recall@5K and Hit@5K) together with the Vendi Score to measure diversity and generation stability.

**S138 — 한국어**

WSCR 과제에서는 참조 기반 포괄성 지표 Recall@5K·Hit@5K와 함께 다양성 및 생성 안정성을 측정하는 Vendi Score를 보고한다.

**S139 — Original**

Since reference sets represent one plausible realization of the query intent rather than exhaustive ground truth, recall is interpreted as a proxy for semantic coverage rather than binary correctness.

**S139 — 한국어**

참조 집합은 완전한 정답이 아니라 질의 의도의 가능한 실현 하나를 나타내므로 재현율은 이진 정답 여부가 아니라 의미 포괄성의 대리 지표로 해석한다.

**S140 — Original**

Full evaluation protocols, prompt templates, and metric definitions are provided in Appendices B, D, and E.

**S140 — 한국어**

전체 평가 절차, 프롬프트 템플릿, 지표 정의는 부록 B, D, E에 제시한다.

### Table 1: OAR 결과

**S141 — Original**

Performance on Task 1: Open-Ended Abstract Retrieval (OAR).

**S141 — 한국어**

과제 1: 개방형 추상 검색(OAR) 성능.

| 계열·방법 | Polyvore 근거성 | 다양성 | 정렬성 | 평균 | Music 근거성 | 다양성 | 정렬성 | 평균 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| No Fan-out | 22.4 | 34.4 | 21.4 | 26.1 | 48.8 | 20.0 | 41.8 | 36.9 |
| Gemini-2.5-Flash Zero-shot | 24.0 | 47.0 | 23.6 | 31.5 | 45.8 | 45.2 | 44.4 | 45.1 |
| Gemini-2.5-Flash Best-of-N | 26.1±1.6 | 52.2±2.3 | 25.2±1.9 | 34.5±1.8 | 48.2±2.1 | 48.4±2.6 | 49.0±2.0 | 48.5±2.2 |
| Gemma3-4B Zero-shot | 28.4 | 56.0 | 31.2 | 38.5 | 49.8 | 42.6 | 51.8 | 48.1 |
| Gemma3-4B Best-of-N | 28.9±1.5 | 61.0±2.1 | 32.7±1.7 | 40.9±1.6 | 51.4±2.0 | 43.2±2.3 | 53.0±1.9 | 49.2±2.1 |
| R4T-FOLM (Gemma) | **30.8±1.9** | **76.8±2.7** | **39.8±2.3** | 49.1±2.1 | **63.1±2.2** | **49.2±2.4** | **62.0±2.0** | 58.1±2.2 |
| R4T-Diffusion (Gemma) | 해당 없음 | 74.3±3.4 | 37.6±2.8 | 해당 없음 | 해당 없음 | 46.7±3.1 | 59.6±2.6 | 해당 없음 |
| Qwen3-4B Zero-shot | 23.8 | 37.0 | 23.4 | 28.1 | 42.0 | 38.8 | 41.2 | 40.7 |
| Qwen3-4B Best-of-N | 27.0±1.8 | 40.3±2.5 | 24.0±1.9 | 30.4±1.7 | 44.0±2.2 | 40.3±2.7 | 43.7±2.1 | 42.7±2.3 |
| R4T-FOLM (Qwen) | **37.0±2.1** | 62.8±2.9 | **28.0±2.0** | 42.6±2.2 | **48.2±2.3** | **44.8±2.5** | 49.4±2.1 | 47.5±2.2 |
| R4T-Diffusion (Qwen) | 해당 없음 | **65.0±3.6** | 27.4±2.7 | 해당 없음 | 해당 없음 | 44.5±3.0 | **52.0±2.8** | 해당 없음 |

**S142 — Original**

Results are reported as mean $\pm$ standard deviation.

**S142 — 한국어**

결과는 평균 $\pm$ 표준편차로 보고한다.

**S143 — Original**

Bold denotes the best performance within each model family.

**S143 — 한국어**

굵은 글씨는 각 모델 계열에서 가장 좋은 성능을 뜻한다.

**S144 — Original**

R4T consistently outperforms fan-out baselines across datasets and metrics.

**S144 — 한국어**

R4T는 데이터셋과 지표 전반에서 팬아웃 기준선을 일관되게 능가한다.

**S145 — Original**

Note that Groundedness is not applicable to R4T-Diffusion (indicated by “\”) due to the absence of intermediate sub-query.

**S145 — 한국어**

R4T-Diffusion에는 중간 하위 질의가 없으므로 근거성 지표를 적용할 수 없으며 원표에서는 `\`로 표시한다.

### Table 2: WSCR 결과

**S146 — Original**

Performance on Task 2: Weakly Supervised Compositional Retrieval (WSCR).

**S146 — 한국어**

과제 2: 약지도 구성 검색(WSCR) 성능.

| 검색 계열·방법 | Recall@5K | Hit@5K | VS |
|---|---:|---:|---:|
| LLM 기반 - Gemini-2.5-Flash | 15.7 | 52.1 | 33.4 |
| LLM 기반 - Gemma3-4B | 6.0 | 25.9 | 44.2 |
| LLM 기반 - Qwen3-4B | 10.1 | 33.9 | 46.4 |
| LLM 기반 - R4T-FOLM (Gemma) | 16.9 | 54.4 | 40.5 |
| LLM 기반 - R4T-FOLM (Qwen) | **20.9** | **64.6** | **27.5** |
| 확산 기반 - R4T-Diffusion (Gemma) | 15.0 | 54.1 | 46.2 |
| 확산 기반 - R4T-Diffusion (Qwen) | **16.5** | **57.5** | **34.7** |

**S147 — Original**

We use an LLM (Gemini-2.5-Pro) to generate a broad query for each outfit in Polyvore, and set the items in each as the ground truths.

**S147 — 한국어**

LLM(Gemini-2.5-Pro)으로 Polyvore의 각 의상에 대한 넓은 질의를 만들고, 각 의상의 항목을 정답으로 설정한다.

**S148 — Original**

For diversity evaluation with normalized Vendi Score, we set temperature=0.9 for LLM-based retrieval, and set #samples=5 (i.e., $5\times10=50$ sub-queries in total) for all the methods.

**S148 — 한국어**

정규화 Vendi Score를 이용한 다양성 평가에서 LLM 기반 검색의 temperature는 0.9로 설정하고, 모든 방법의 샘플 수는 5, 즉 총 $5\times10=50$개 하위 질의로 설정한다.

> **번역자 주:** Table 2의 질의 생성 모델은 Gemini-2.5-Pro로 명시된다. Appendix B의 심판 모델 Gemini-2.5-Flash와는 역할도 다를 수 있지만, 본문 S136의 심판 모델 Pro와 Appendix B의 Flash 불일치는 별도로 남는다.

### Figure 4: 보상 및 학습 곡선

**S149 — Original**

Reward & Scores over Time (FOLM Training) for Open-Ended Abstract Retrieval.

**S149 — 한국어**

개방형 추상 검색의 시간 경과에 따른 보상과 점수(FOLM 학습).

| 패널 | Original subcaption | 한국어 |
|---|---|---|
| (a) | Ablation w/ Gemma3-4B | Gemma3-4B를 사용한 절제 실험 |
| (b) | Reward: Gemma vs Qwen | 보상: Gemma와 Qwen 비교 |
| (c) | Scores over Time (Gemma) | 시간 경과에 따른 점수(Gemma) |
| (d) | Qwen $\lambda_g:\lambda_d:\lambda_a=6:2:2$ | Qwen 보상 비율 $6:2:2$ |
| (e) | Qwen $\lambda_g:\lambda_d:\lambda_a=4:3:3$ | Qwen 보상 비율 $4:3:3$ |
| (f) | Qwen $\lambda_g:\lambda_d:\lambda_a=2:4:4$ | Qwen 보상 비율 $2:4:4$ |

### 3.2 Main Results

**S150 — Original**

Table 1 and Table 2 summarize the performance of all methods on the OAR and WSCR tasks.

**S150 — 한국어**

표 1과 표 2는 OAR 및 WSCR 과제에서 모든 방법의 성능을 요약한다.

**S151 — Original**

We highlight several consistent patterns that clarify both the strengths and limitations of existing fan-out strategies, as well as the advantages of R4T.

**S151 — 한국어**

기존 팬아웃 전략의 강점과 한계, R4T의 장점을 분명히 보여주는 몇 가지 일관된 패턴을 강조한다.

#### Fan-out is necessary but not sufficient

**S152 — Original**

Across all datasets and base models, zero-shot fan-out consistently outperforms the No Fan-out baseline that retrieves directly using the original query.

**S152 — 한국어**

모든 데이터셋과 기본 모델에서 제로샷 팬아웃은 원 질의로 직접 검색하는 No Fan-out 기준선을 일관되게 능가한다.

**S153 — Original**

This confirms the long-standing hypothesis that query expansion improves coverage of diverse semantic facets (Carpineto and Romano, 2012).

**S153 — 한국어**

이는 질의 확장이 다양한 의미 측면의 포괄성을 높인다는 오래된 가설을 확인한다(Carpineto and Romano, 2012).

**S154 — Original**

However, zero-shot fan-out exhibits clear weaknesses.

**S154 — 한국어**

하지만 제로샷 팬아웃에는 명확한 약점이 있다.

**S155 — Original**

Generated sub-queries often drift off the database manifold or collapse into near-duplicate expressions, leading to limited groundedness and redundant retrieval results.

**S155 — 한국어**

생성된 하위 질의는 데이터베이스 다양체에서 벗어나거나 거의 중복된 표현으로 붕괴하는 경우가 많아 근거성이 떨어지고 검색 결과가 중복된다.

**S156 — Original**

These effects are particularly visible in the OAR task, where no ground truth constrains exploration.

**S156 — 한국어**

탐색을 제한하는 정답이 없는 OAR 과제에서 이러한 현상이 특히 두드러진다.

#### Reward-aware selection improves quality but does not scale

**S157 — Original**

The Best-of-N baseline substantially improves over zero-shot fan-out by selecting high-reward fan-out instances.

**S157 — 한국어**

Best-of-N 기준선은 고보상 팬아웃 사례를 선택하여 제로샷 팬아웃보다 크게 향상된다.

**S158 — Original**

This demonstrates that the reward functions we design are meaningful signals for shaping retrieval behavior.

**S158 — 한국어**

이는 설계한 보상 함수가 검색 행동을 형성하는 데 의미 있는 신호임을 보여준다.

**S159 — Original**

However, Best-of-N requires multiple independent fan-out executions per query, resulting in an order-of-magnitude increase in inference cost.

**S159 — 한국어**

그러나 Best-of-N은 질의마다 여러 번 독립적으로 팬아웃을 실행해야 하므로 추론 비용이 한 자릿수 차수만큼 증가한다.

**S160 — Original**

As a result, its gains come at the expense of latency and scalability, limiting its applicability in practical systems.

**S160 — 한국어**

따라서 성능 향상은 지연 시간과 확장성을 대가로 얻어지며 실제 시스템에서의 적용 가능성이 제한된다.

#### R4T consistently dominates the accuracy-efficiency frontier

**S161 — Original**

R4T achieves the strongest overall performance across datasets, tasks, and base models.

**S161 — 한국어**

R4T는 데이터셋, 과제, 기본 모델 전반에서 가장 강한 종합 성능을 달성한다.

**S162 — Original**

Notably, R4T outperforms Best-of-N while requiring only a single inference pass at deployment time.

**S162 — 한국어**

특히 R4T는 배포 시 한 번의 추론 패스만 필요하면서 Best-of-N보다 우수하다.

**S163 — Original**

This result highlights the core advantage of R4T: reinforcement learning is used to discover high-quality fan-out behaviors once, and these behaviors are then distilled into a lightweight diffusion-based retriever.

**S163 — 한국어**

이 결과는 R4T의 핵심 장점을 보여준다. 강화학습은 고품질 팬아웃 행동을 한 번 발견하는 데 사용되고, 그 행동은 경량 확산 기반 검색기에 증류된다.

**S164 — Original**

The RL-trained FOLM learns to generate sub-queries that balance diversity, alignment, and groundedness, while the diffusion model faithfully captures this distribution in embedding space, enabling efficient and controllable fan-out retrieval.

**S164 — 한국어**

RL 학습 FOLM은 다양성·정렬성·근거성의 균형을 이루는 하위 질의를 생성하도록 학습하며, 확산 모델은 이 분포를 임베딩 공간에서 충실히 포착하여 효율적이고 제어 가능한 팬아웃 검색을 가능하게 한다.

#### Reward Hacking in OAR

**S165 — Original**

Careful reward design is crucial for realizing R4T’s performance gains.

**S165 — 한국어**

R4T의 성능 향상을 실현하려면 신중한 보상 설계가 중요하다.

**S166 — Original**

We perform an ablation on the OAR task (Figure 4) to analyze how different reward components shape fan-out behavior.

**S166 — 한국어**

서로 다른 보상 구성 요소가 팬아웃 행동을 어떻게 형성하는지 분석하기 위해 OAR 과제에서 절제 실험을 수행한다(그림 4).

**S167 — Original**

Without a diversity term, the reward is easily exploited.

**S167 — 한국어**

다양성 항이 없으면 보상이 쉽게 악용된다.

**S168 — Original**

Training with only the groundedness reward, the policy converges to degenerate, nonsensical strings (e.g., “line ending line ending line ending”), which happen to minimize embedding distance to a specific database item.

**S168 — 한국어**

근거성 보상만으로 학습하면 정책은 우연히 특정 데이터베이스 항목과의 임베딩 거리를 최소화하는 퇴화된 무의미 문자열, 예를 들어 “line ending line ending line ending”으로 수렴한다.

**S169 — Original**

When trained with both groundedness and alignment, collapse occurs even faster, as the policy simply repeats paraphrases of the original query, trivially maximizing alignment while ignoring semantic dispersion.

**S169 — 한국어**

근거성과 정렬성을 함께 학습하면 붕괴가 더 빨리 일어난다. 정책이 원 질의의 바꿔쓰기를 반복하여 의미 분산은 무시한 채 정렬성을 손쉽게 최대화하기 때문이다.

**S170 — Original**

By contrast, jointly optimizing groundedness, alignment, and diversity prevents such collapse and yields stable GRPO training.

**S170 — 한국어**

반대로 근거성·정렬성·다양성을 함께 최적화하면 이러한 붕괴를 막고 안정적인 GRPO 학습을 얻는다.

**S171 — Original**

Figures 4(d-f) further illustrate how reward weighting affects training dynamics.

**S171 — 한국어**

그림 4(d-f)는 보상 가중치가 학습 동역학에 미치는 영향을 더 보여준다.

**S172 — Original**

When groundedness dominates, diversity increases but alignment degrades, indicating an overemphasis on database proximity at the expense of semantic fidelity.

**S172 — 한국어**

근거성이 지배적이면 다양성은 증가하지만 정렬성은 악화되며, 이는 의미 충실성을 희생해 데이터베이스 근접성을 지나치게 강조했음을 나타낸다.

**S173 — Original**

Conversely, emphasizing alignment and diversity suppresses exploration, limiting coverage across alternative interpretations or intents.

**S173 — 한국어**

반대로 정렬성과 다양성을 강조하면 탐색이 억제되어 대안적 해석이나 의도에 대한 포괄성이 제한된다.

**S174 — Original**

A balanced weighting yields stable convergence of all three scores, highlighting an inherent trade-off between exploration and semantic fidelity.

**S174 — 한국어**

균형 잡힌 가중치는 세 점수를 모두 안정적으로 수렴시키며 탐색과 의미 충실성 사이의 본질적 절충을 드러낸다.

**S175 — Original**

Together, these results show that diversity and alignment act as mutual counter-anchors, forcing the policy into a balanced region of the reward landscape where shortcut solutions are ineffective and high reward can only be achieved by generating meaningful, database-grounded sub-query variations.

**S175 — 한국어**

종합하면 다양성과 정렬성은 서로의 맞은편 닻으로 작용해 정책을 보상 지형의 균형 영역으로 밀어 넣는다. 이 영역에서는 지름길 해법이 효과가 없고 의미 있으면서 데이터베이스에 근거한 하위 질의 변형을 생성해야만 높은 보상을 얻을 수 있다.

#### Set Retrieval Behavior

**S176 — Original**

Table 2 reveals a clear trade-off between reference-based coverage and diversity across retrieval paradigms.

**S176 — 한국어**

표 2는 검색 패러다임 전반에서 참조 기반 포괄성과 다양성 사이의 명확한 절충을 보여준다.

**S177 — Original**

Among LLM-based methods, higher Recall@5K and Hit@5K are often accompanied by lower Vendi Scores, indicating that autoregressive fan-out tends to concentrate retrieval around a small number of dominant semantic modes when optimized for reference overlap.

**S177 — 한국어**

LLM 기반 방법에서는 Recall@5K와 Hit@5K가 높을수록 Vendi Score가 낮은 경우가 많다. 이는 참조 중첩을 최적화할 때 자기회귀 팬아웃이 소수의 지배적 의미 모드 주변에 검색을 집중시키는 경향을 나타낸다.

**S178 — Original**

This behavior is consistent with recent findings on the use RL for language models, which show that stronger reward optimization typically reduces output entropy and encourages mode collapse (Cui et al., 2025).

**S178 — 한국어**

이 행동은 언어 모델에 RL을 사용한 최근 연구 결과와 일치한다. 더 강한 보상 최적화는 대개 출력 엔트로피를 낮추고 모드 붕괴를 촉진한다(Cui et al., 2025).

> **번역자 주:** 원문 `on the use RL`은 `on the use of RL`의 오탈자로 보인다.

**S179 — Original**

By contrast, zero-shot LLM baselines and diffusion-based retrieval exhibit higher diversity, reflecting broader exploration of the semantic space across inference runs.

**S179 — 한국어**

반면 제로샷 LLM 기준선과 확산 기반 검색은 더 높은 다양성을 보여 여러 추론 실행에서 의미 공간을 더 폭넓게 탐색한다.

**S180 — Original**

Importantly, lower recall in these cases does not necessarily imply lower retrieval quality.

**S180 — 한국어**

중요하게도 이러한 경우 낮은 재현율이 반드시 낮은 검색 품질을 뜻하지는 않는다.

**S181 — Original**

The reference sets do not reflect an “exhaustive ground” truth, but rather represent only just one (of potentially many) plausible realization of the query intent.

**S181 — 한국어**

참조 집합은 완전한 정답을 반영하는 것이 아니라 질의 의도의 잠재적으로 많은 타당한 실현 중 단 하나만 나타낸다.

> **번역자 주:** 원문의 `exhaustive ground truth`와 `only just one ... realization` 표현은 어색하지만 의미를 보존했다.

**S182 — Original**

Greater diversity therefore suggests that the model may be uncovering alternative, equally valid interpretations that are not captured by the reference items.

**S182 — 한국어**

따라서 더 높은 다양성은 모델이 참조 항목에 담기지 않은, 동등하게 타당한 대안 해석을 발견하고 있을 가능성을 시사한다.

**S183 — Original**

R4T shifts this trade-off in a favorable direction.

**S183 — 한국어**

R4T는 이 절충을 더 유리한 방향으로 옮긴다.

**S184 — Original**

While R4T-FOLM improves reference coverage at the cost of reduced diversity, R4T-Diffusion preserves much of the diversity inherent to diffusion-based generation while substantially improving coverage.

**S184 — 한국어**

R4T-FOLM은 다양성 감소를 대가로 참조 포괄성을 높이는 반면, R4T-Diffusion은 포괄성을 크게 높이면서 확산 기반 생성 고유의 다양성을 상당 부분 보존한다.

**S185 — Original**

This indicates that distilling reward-aligned behaviors into a diffusion prior offers a practical way to balance coverage and semantic richness for set-valued retrieval under weak supervision.

**S185 — 한국어**

이는 보상 정렬 행동을 확산 사전분포에 증류하는 것이 약지도 집합값 검색에서 포괄성과 의미적 풍부함의 균형을 잡는 실용적 방법임을 보여준다.

### 3.3 Qualitative Example

**S186 — Original**

Figure 3 and Figure 6 show qualitative results from the OAR task on Polyvore for two broad queries, “Bohemian festival style” and “Labor day picnic outfit”.

**S186 — 한국어**

그림 3과 그림 6은 “Bohemian festival style”과 “Labor day picnic outfit”이라는 두 넓은 질의에 대한 Polyvore OAR 과제의 정성 결과를 보여준다.

**S187 — Original**

These examples illustrate how the joint use of groundedness, alignment, and diversity rewards guides R4T to produce meaningful and varied sub-query decompositions.

**S187 — 한국어**

이 예들은 근거성·정렬성·다양성 보상을 함께 사용하면 R4T가 의미 있고 다양한 하위 질의 분해를 만들도록 어떻게 유도되는지 보여준다.

**S188 — Original**

For the “Bohemian festival style” query, R4T generates sub-queries that branch into distinct thematic directions such as “bohemian festival dress”, “straw boots festival style”, and “lace bohemian festival”.

**S188 — 한국어**

“Bohemian festival style” 질의에서 R4T는 “bohemian festival dress”, “straw boots festival style”, “lace bohemian festival”처럼 서로 다른 주제 방향으로 갈라지는 하위 질의를 생성한다.

**S189 — Original**

Each sub-query retrieves a visually coherent yet semantically distinct group of items, indicating strong diversity while remaining consistent with the overall style.

**S189 — 한국어**

각 하위 질의는 시각적으로 일관되면서 의미적으로는 구별되는 항목 그룹을 검색하여 전체 스타일과 일치하는 동시에 높은 다양성을 보인다.

**S190 — Original**

In contrast, baseline models such as Qwen-4B often produce near-synonymous variations of the same expression, for example “bohemian festival style” and “bohemian festival fashion”, which leads to more homogeneous retrieval results.

**S190 — 한국어**

반대로 Qwen-4B 같은 기준 모델은 “bohemian festival style”과 “bohemian festival fashion”처럼 같은 표현의 거의 동의어인 변형을 자주 만들어 더 동질적인 검색 결과로 이어진다.

> **번역자 주:** 실험 설정과 표에는 모델명이 `Qwen3-4B`이나 이 문장은 `Qwen-4B`로 적는다. 원문 내부 모델명 불일치다.

**S191 — Original**

A similar trend is observed for the “Labor day picnic outfit” query.

**S191 — 한국어**

“Labor day picnic outfit” 질의에서도 비슷한 경향이 관찰된다.

**S192 — Original**

R4T decomposes the query into complementary facets such as bohemian, minimalist, and jumpsuit styles, retrieving outfits that differ in silhouette, color palette, and accessory choices while remaining appropriate for the seasonal picnic context.

**S192 — 한국어**

R4T는 질의를 보헤미안, 미니멀리스트, 점프슈트 스타일 같은 상보적 측면으로 분해하여 계절 피크닉 맥락에 적합하면서도 실루엣, 색상 팔레트, 액세서리 선택이 서로 다른 의상을 검색한다.

**S193 — Original**

Gemini-2.5-Flash, although capable of generating syntactically diverse sub-queries, tends to retrieve sets that are more uniform and exhibit limited semantic coverage.

**S193 — 한국어**

Gemini-2.5-Flash는 구문적으로 다양한 하위 질의를 생성할 수 있지만, 더 균일하고 의미 포괄성이 제한된 집합을 검색하는 경향이 있다.

**S194 — Original**

Overall, these qualitative results highlight the role of the three reward components in shaping retrieval behavior.

**S194 — 한국어**

전반적으로 이 정성 결과는 세 보상 구성 요소가 검색 행동을 형성하는 역할을 강조한다.

**S195 — Original**

Groundedness encourages each sub-query to correspond to real items in the database, alignment preserves consistency with the original query intent, and diversity promotes exploration of multiple valid interpretations.

**S195 — 한국어**

근거성은 각 하위 질의가 데이터베이스의 실제 항목에 대응하도록 하고, 정렬성은 원 질의 의도와의 일관성을 보존하며, 다양성은 여러 타당한 해석의 탐색을 촉진한다.

**S196 — Original**

Together, these objectives allow R4T to generate rich query decompositions that translate into diverse and relevant retrieval.

**S196 — 한국어**

이 목적들을 함께 사용하면 R4T는 다양하고 관련성 높은 검색으로 이어지는 풍부한 질의 분해를 생성할 수 있다.

**S197 — Original**

Figure 3: Qualitative comparison on the Polyvore dataset for the open-ended abstract retrieval task given the broad query “Bohemian festival style”.

**S197 — 한국어**

그림 3: 넓은 질의 “Bohemian festival style”이 주어진 Polyvore 개방형 추상 검색 과제의 정성 비교.

**S198 — Original**

R4T generates semantically distinct, on-topic sub-queries that retrieve diverse outfit collections, while the Qwen3-4B zero-shot baseline produces largely paraphrastic sub-queries, leading to more homogeneous results.

**S198 — 한국어**

R4T는 주제에 맞으면서 의미적으로 구별되는 하위 질의를 생성해 다양한 의상 모음을 검색하지만, Qwen3-4B 제로샷 기준선은 대부분 바꿔쓰기 수준의 하위 질의를 만들어 더 동질적인 결과를 낸다.

**S199 — Original**

Figure 6: Examples of generated subqueries and retrieved images from Polyvore dataset given a broad query “Labor day picnic outfit” for the open-ended abstract retrieval task.

**S199 — 한국어**

그림 6: 개방형 추상 검색 과제에서 넓은 질의 “Labor day picnic outfit”이 주어졌을 때 Polyvore 데이터셋에서 생성한 하위 질의와 검색 이미지 예시.

> **그림 읽기:** 그림 6의 R4T 행은 `bohemian labor day picnic outfit`, `minimalist labor day picnic outfit`, `labor day picnic jumpsuit`처럼 스타일 축을 분리한다. Gemini-2.5-Flash 행은 `casual`, `stylish`, `comfortable` 변형을 보여준다. 그림은 결과 이미지를 포함하므로 이 문서에서는 캡션과 식별 가능한 질의 라벨만 대조했다.

### 3.4 Efficiency Analysis

**S200 — Original**

To evaluate inference-time efficiency, we benchmark the latency of query fan-out for R4T against autoregressive LLM-based fan-out baselines.

**S200 — 한국어**

추론 시점 효율을 평가하기 위해 R4T의 질의 팬아웃 지연 시간을 자기회귀 LLM 기반 팬아웃 기준선과 벤치마크한다.

**S201 — Original**

We compare a diffusion-based retriever that generates all $k=10$ retrieval directions in a single forward pass with autoregressive models that sequentially generate sub-queries and invoke retrieval.

**S201 — 한국어**

한 번의 순전파로 $k=10$개 검색 방향을 모두 생성하는 확산 기반 검색기와 하위 질의를 순차 생성하고 검색을 호출하는 자기회귀 모델을 비교한다.

**S202 — Original**

Wall-clock latency is measured across varying batch sizes.

**S202 — 한국어**

여러 배치 크기에서 실제 경과 시간을 측정한다.

**S203 — Original**

Figure 5: Efficiency comparison between Autoregressive LLM and Diffusion Model for query fan-out ($k=10$) generation.

**S203 — 한국어**

그림 5: 질의 팬아웃($k=10$) 생성에서 자기회귀 LLM과 확산 모델의 효율 비교.

**S204 — Original**

Note that the x-axis follows a logarithmic scale (doubling at each step).

**S204 — 한국어**

x축은 각 단계에서 두 배가 되는 로그 척도다.

**S205 — Original**

The Diffusion Model demonstrates superior scalability and lower latency, maintaining sub-second performance for small batches and achieving an order-of-magnitude speedup at larger batch sizes.

**S205 — 한국어**

확산 모델은 작은 배치에서 1초 미만 성능을 유지하고 큰 배치에서 한 자릿수 차수의 속도 향상을 달성하여 더 우수한 확장성과 낮은 지연 시간을 보인다.

**S206 — Original**

Figure 5 illustrates the wall-clock time required for fan-out generation.

**S206 — 한국어**

그림 5는 팬아웃 생성에 필요한 실제 경과 시간을 보여준다.

**S207 — Original**

The autoregressive LLM is dominated by high constant overheads at smaller batch sizes, taking approximately 1.46 seconds even for a batch of 8, before scaling linearly to nearly 50 seconds at a batch size of 1024.

**S207 — 한국어**

자기회귀 LLM은 작은 배치에서 큰 상수 오버헤드의 영향을 받아 배치 8에서도 약 1.46초가 걸리고, 배치 크기 1024에서는 거의 50초까지 선형으로 늘어난다.

**S208 — Original**

In contrast, our diffusion model, containing only 53.9M parameters, leverages non-autoregressive generation in the embedding space to process the small batch in just 0.07 seconds and the largest batch in 4.21 seconds.

**S208 — 한국어**

반면 매개변수가 53.9M개뿐인 확산 모델은 임베딩 공간의 비자기회귀 생성을 활용해 작은 배치를 0.07초, 가장 큰 배치를 4.21초에 처리한다.

**S209 — Original**

This compact architecture drastically reduces deployment memory overhead while delivering a consistent $12\times$-$20\times$ speedup, confirming that transforming the fan-out burden from a heavy autoregressive System 2 to a lightweight System 1 diffusion prior is essential for practical, real-time retrieval applications.

**S209 — 한국어**

이 소형 아키텍처는 배포 메모리 오버헤드를 크게 줄이면서 일관되게 $12\times$-$20\times$ 속도 향상을 제공한다. 이는 팬아웃 부담을 무거운 자기회귀 시스템 2에서 경량 시스템 1 확산 사전분포로 전환하는 것이 실용적 실시간 검색 응용에 필수적임을 확인한다.

## 4 Related Work

### Generative Retrieval

**S210 — Original**

Recent work has explored formulating retrieval as a generation task.

**S210 — 한국어**

최근 연구는 검색을 생성 과제로 정식화하는 방법을 탐구했다.

**S211 — Original**

DSI (Tay et al., 2022) trains sequence-to-sequence models to generate document identifiers (docids) directly from queries, treating the entire corpus as model memory.

**S211 — 한국어**

DSI(Tay et al., 2022)는 전체 말뭉치를 모델 메모리로 취급하고 질의에서 문서 식별자(docid)를 직접 생성하도록 시퀀스-투-시퀀스 모델을 학습한다.

**S212 — Original**

NCI (Wang et al., 2022) extends this with improved indexing strategies, while SEAL (Bevilacqua et al., 2022) generates n-grams for passage retrieval.

**S212 — 한국어**

NCI(Wang et al., 2022)는 개선된 인덱싱 전략으로 이를 확장하고, SEAL(Bevilacqua et al., 2022)은 구절 검색을 위한 n-그램을 생성한다.

**S213 — Original**

More recent work has explored semantic identifiers (Li et al., 2023), learning to rank in generative retrieval (Li et al., 2024), and scalable approaches for large corpora (Pradeep et al., 2023; Zeng et al., 2024).

**S213 — 한국어**

더 최근 연구는 의미 식별자(Li et al., 2023), 생성 검색의 순위 학습(Li et al., 2024), 대규모 말뭉치를 위한 확장 가능한 방법(Pradeep et al., 2023; Zeng et al., 2024)을 탐구했다.

**S214 — Original**

Our work differs by generating in embedding space rather than discrete token space, enabling smoother interpolation and multimodal retrieval.

**S214 — 한국어**

이 연구는 이산 토큰 공간이 아니라 임베딩 공간에서 생성하여 더 매끄러운 보간과 멀티모달 검색을 가능하게 한다는 점이 다르다.

**S215 — Original**

Unlike prior generative retrieval systems that require extensive human-labeled supervision, we synthesize training data through RL.

**S215 — 한국어**

대규모 인간 라벨 지도 데이터가 필요한 기존 생성 검색 시스템과 달리 RL로 학습 데이터를 합성한다.

### Query Expansion and Reformulation

**S216 — Original**

Query expansion has a long history in information retrieval (Carpineto and Romano, 2012; Azad and Deepak, 2019), with classic techniques including pseudo-relevance feedback (Rocchio, 1971) and term co-occurrence analysis.

**S216 — 한국어**

질의 확장은 정보 검색에서 오랜 역사를 지니며(Carpineto and Romano, 2012; Azad and Deepak, 2019), 고전적 기법에는 의사 관련성 피드백(Rocchio, 1971)과 용어 동시출현 분석이 있다.

**S217 — Original**

Modern approaches leverage neural language models for query reformulation (Nogueira and Cho, 2019), with recent work exploring LLM-based query generation (Ma et al., 2023) and multi-query decomposition for complex information needs.

**S217 — 한국어**

현대 방법은 질의 재구성에 신경 언어 모델을 활용하고(Nogueira and Cho, 2019), 최근에는 LLM 기반 질의 생성(Ma et al., 2023)과 복잡한 정보 요구를 위한 다중 질의 분해를 탐구한다.

**S218 — Original**

However, these methods typically operate in a two-stage retrieve-then-rerank pipeline and do not explicitly ground expansions in the target database.

**S218 — 한국어**

그러나 이러한 방법은 대개 검색 후 재순위화하는 2단계 파이프라인으로 작동하며 확장 질의를 대상 데이터베이스에 명시적으로 근거시키지 않는다.

**S219 — Original**

Our fan-out approach differs by training query expansion to optimize database-specific retrieval properties through reinforcement learning.

**S219 — 한국어**

이 논문의 팬아웃 방식은 강화학습을 통해 데이터베이스별 검색 속성을 최적화하도록 질의 확장을 학습한다는 점이 다르다.

### Reinforcement Learning for Retrieval

**S220 — Original**

Recent work has begun applying RL to information retrieval tasks.

**S220 — 한국어**

최근 연구는 정보 검색 과제에 RL을 적용하기 시작했다.

**S221 — Original**

DeepRetrieval (Jiang et al., 2025a) and s3 (Jiang et al., 2025c) use RL to train search agents that interact with real search engines, demonstrating that reward-driven optimization can encode fine-grained retrieval objectives.

**S221 — 한국어**

DeepRetrieval(Jiang et al., 2025a)과 s3(Jiang et al., 2025c)는 실제 검색 엔진과 상호작용하는 검색 에이전트를 RL로 학습하여 보상 주도 최적화가 세밀한 검색 목적을 인코딩할 수 있음을 보였다.

**S222 — Original**

Zhou et al. (2023) explores RL from relevance feedback for generative retrieval.

**S222 — 한국어**

Zhou et al. (2023)은 생성 검색을 위한 관련성 피드백 기반 RL을 탐구한다.

**S223 — Original**

However, these methods use RL for direct inference, incurring high computational costs at query time.

**S223 — 한국어**

그러나 이러한 방법은 직접 추론에 RL을 사용하므로 질의 시점 계산 비용이 높다.

**S224 — Original**

We instead use RL as a data generation engine, amortizing the cost across inference queries by synthesizing training data once and then deploying an efficient diffusion-based retriever.

**S224 — 한국어**

대신 RL을 데이터 생성 엔진으로 사용하여 학습 데이터를 한 번 합성한 뒤 효율적인 확산 기반 검색기를 배포함으로써 비용을 여러 추론 질의에 분산한다.

### Diffusion Models for Retrieval

**S225 — Original**

Diffusion probabilistic models (Ho et al., 2020; Song et al., 2020) have shown strong performance in generative modeling across multiple domains.

**S225 — 한국어**

확산 확률 모델은 여러 도메인의 생성 모델링에서 강한 성능을 보였다(Ho et al., 2020; Song et al., 2020).

**S226 — Original**

Recent work has adapted diffusion models to retrieval tasks.

**S226 — 한국어**

최근 연구는 확산 모델을 검색 과제에 적용했다.

**S227 — Original**

Diff4Steer (Bao et al., 2025) applies diffusion priors to music retrieval with semantic guidance, while GDRetriever (Guinot et al., 2025) develops controllable generative text-music retrieval.

**S227 — 한국어**

Diff4Steer(Bao et al., 2025)는 의미 가이던스를 적용한 음악 검색에 확산 사전분포를 사용하고, GDRetriever(Guinot et al., 2025)는 제어 가능한 생성형 텍스트-음악 검색을 개발한다.

**S228 — Original**

These works demonstrate that sampling in embedding space enables flexible multi-hypothesis generation.

**S228 — 한국어**

이 연구들은 임베딩 공간의 샘플링이 유연한 다중 가설 생성을 가능하게 함을 보여준다.

**S229 — Original**

Our work extends this paradigm by addressing the training data bottleneck: rather than relying on human supervision, we synthesize property-aligned training data through RL-guided generation.

**S229 — 한국어**

이 연구는 학습 데이터 병목을 해결하여 이 패러다임을 확장한다. 인간 지도에 의존하는 대신 RL 유도 생성으로 속성 정렬 학습 데이터를 합성한다.

### Synthetic Data Generation

**S230 — Original**

Synthetic data generation has emerged as a powerful technique for addressing data scarcity and privacy concerns in machine learning (Lu et al., 2024; Goyal and Mahmoud, 2024).

**S230 — 한국어**

합성 데이터 생성은 기계학습의 데이터 부족과 개인정보 문제를 해결하는 강력한 기법으로 부상했다(Lu et al., 2024; Goyal and Mahmoud, 2024).

**S231 — Original**

Techniques range from rule-based systems to deep generative models including GANs (Goodfellow et al., 2014) and VAEs (Kingma and Welling, 2013).

**S231 — 한국어**

기법은 규칙 기반 시스템부터 GAN(Goodfellow et al., 2014)과 VAE(Kingma and Welling, 2013)를 포함한 심층 생성 모델까지 다양하다.

**S232 — Original**

Recent work has explored using LLMs to generate training data for various tasks (Chen et al., 2023), including instruction tuning and task-specific fine-tuning.

**S232 — 한국어**

최근 연구는 지시 조정과 과제별 미세조정을 포함한 여러 과제의 학습 데이터를 LLM으로 생성하는 방법을 탐구했다(Chen et al., 2023).

**S233 — Original**

In retrieval, synthetic queries have been generated for training dense retrievers (Ma et al., 2021), but typically without property-specific control.

**S233 — 한국어**

검색 분야에서는 밀집 검색기 학습용 합성 질의를 생성해 왔지만(Ma et al., 2021), 대개 속성별 제어는 없었다.

**S234 — Original**

Our work uniquely combines RL-based data synthesis with diffusion-based retrieval, enabling controllable generation of property-aligned training pairs.

**S234 — 한국어**

이 연구는 RL 기반 데이터 합성과 확산 기반 검색을 독특하게 결합해 속성 정렬 학습 쌍을 제어 가능하게 생성한다.

### Multimodal Retrieval

**S235 — Original**

Cross-modal retrieval systems (Wang et al., 2023) aim to bridge semantic gaps between different modalities such as text, images, and audio.

**S235 — 한국어**

교차 모달 검색 시스템은 텍스트, 이미지, 오디오 같은 서로 다른 모달리티 사이의 의미 간극을 메우는 것을 목표로 한다(Wang et al., 2023).

**S236 — Original**

Vision-language models like CLIP (Radford et al., 2021) and CLAP (Wu et al., 2023) learn joint embedding spaces for retrieval.

**S236 — 한국어**

CLIP(Radford et al., 2021)과 CLAP(Wu et al., 2023) 같은 비전-언어 모델은 검색을 위한 공동 임베딩 공간을 학습한다.

**S237 — Original**

Recent work has explored generative approaches for multimodal retrieval (Wu et al., 2024), including retrieval-augmented generation for multimodal tasks.

**S237 — 한국어**

최근 연구는 멀티모달 과제를 위한 검색 증강 생성을 포함해 멀티모달 검색의 생성 접근법을 탐구했다(Wu et al., 2024).

**S238 — Original**

Our framework operates on top of frozen multimodal encoders, demonstrating that RL-guided data synthesis can enhance retrieval across modalities without modifying the underlying embedding space.

**S238 — 한국어**

이 프레임워크는 동결된 멀티모달 인코더 위에서 작동하며, 기반 임베딩 공간을 수정하지 않고도 RL 유도 데이터 합성이 모달리티 전반의 검색을 향상할 수 있음을 보여준다.

## 5 Conclusion

**S239 — Original**

We present R4T, a reinforcement learning-based framework for synthesizing training data for generative retrieval.

**S239 — 한국어**

생성 검색을 위한 학습 데이터를 합성하는 강화학습 기반 프레임워크 R4T를 제시했다.

**S240 — Original**

By training a fan-out language model with property-specific rewards and using it to generate supervision for a diffusion-based retriever, we enable controllable fan-out retrieval without human-labeled data.

**S240 — 한국어**

속성별 보상으로 팬아웃 언어 모델을 학습하고 이를 확산 기반 검색기의 지도 신호 생성에 사용하여 인간 라벨 데이터 없이 제어 가능한 팬아웃 검색을 실현한다.

**S241 — Original**

Experiments on fashion product benchmark demonstrate that R4T outperforms strong baselines while maintaining efficient inference.

**S241 — 한국어**

패션 제품 벤치마크 실험은 R4T가 효율적인 추론을 유지하면서 강력한 기준선을 능가함을 보여준다.

> **번역자 주:** 원문 결론은 단수 `fashion product benchmark`만 언급하지만 본문 실험에는 패션 Polyvore와 비공개 음악 데이터셋이 모두 포함된다.

**S242 — Original**

Our work opens new directions for training generative retrieval systems in specialized domains where supervision is scarce.

**S242 — 한국어**

이 연구는 지도 데이터가 부족한 전문 도메인에서 생성 검색 시스템을 학습하는 새로운 방향을 연다.

**S243 — Original**

Limitations are discussed in Appendix A.

**S243 — 한국어**

한계는 부록 A에서 논의한다.

## Impact Statement

**S244 — Original**

This work addresses the growing gap between increasingly rich retrieval objectives and the limited supervision available to train efficient retrieval systems under those objectives.

**S244 — 한국어**

이 연구는 갈수록 풍부해지는 검색 목적과 그 목적 아래에서 효율적인 검색 시스템을 학습하는 데 이용 가능한 제한된 지도 신호 사이의 커지는 간극을 다룬다.

**S245 — Original**

By using reinforcement learning as an objective transducer and compiling the resulting behaviors into a lightweight diffusion-based retriever, R4T enables controllable, set-valued retrieval without requiring human-labeled data.

**S245 — 한국어**

강화학습을 목적 전환기로 사용하고 그 결과 행동을 경량 확산 기반 검색기에 컴파일함으로써 R4T는 인간 라벨 데이터 없이 제어 가능한 집합값 검색을 가능하게 한다.

**S246 — Original**

This design has several potential positive impacts.

**S246 — 한국어**

이 설계에는 몇 가지 잠재적 긍정 효과가 있다.

**S247 — Original**

From a systems perspective, R4T provides a practical pathway for deploying retrieval models that optimize higher-order properties such as diversity, coverage, and complementarity while maintaining low inference latency.

**S247 — 한국어**

시스템 관점에서 R4T는 낮은 추론 지연을 유지하면서 다양성, 포괄성, 상보성 같은 고차 속성을 최적화하는 검색 모델을 배포할 실용적 경로를 제공한다.

**S248 — Original**

This is particularly relevant for real-world applications where fan-out retrieval is desirable but autoregressive generation is prohibitively expensive, including recommendation systems, creative search, and exploratory information access.

**S248 — 한국어**

이는 팬아웃 검색이 바람직하지만 자기회귀 생성 비용이 지나치게 큰 추천 시스템, 창의적 검색, 탐색적 정보 접근 같은 실제 응용에 특히 적합하다.

**S249 — Original**

By separating reward-driven discovery from inference-time deployment, our framework supports scalable and customizable retrieval without repeated online optimization.

**S249 — 한국어**

보상 주도 발견을 추론 시점 배포와 분리하여 반복적인 온라인 최적화 없이 확장 가능하고 맞춤화 가능한 검색을 지원한다.

**S250 — Original**

From a research perspective, this work contributes a general paradigm for transforming non-decomposable, set-level objectives into trainable supervision.

**S250 — 한국어**

연구 관점에서는 비분해 가능한 집합 수준 목적을 학습 가능한 지도 신호로 변환하는 일반 패러다임을 기여한다.

**S251 — Original**

The idea of using RL to synthesize objective-aligned training data may extend beyond retrieval to other structured generation tasks where ground truth is ambiguous or subjective, such as planning, design, and creative generation.

**S251 — 한국어**

RL로 목적 정렬 학습 데이터를 합성하는 아이디어는 검색을 넘어 계획, 설계, 창의적 생성처럼 정답이 모호하거나 주관적인 다른 구조화 생성 과제로 확장될 수 있다.

**S252 — Original**

We hope this encourages further exploration of compiled approaches that combine interactive learning with efficient generative models.

**S252 — 한국어**

이 연구가 상호작용 학습과 효율적인 생성 모델을 결합한 컴파일 접근법을 더 탐구하도록 촉진하기를 바란다.

### Ethical Considerations and Societal Impact

**S253 — Original**

Because retrieval behaviors are shaped by explicitly designed reward functions, careless reward specification could encode or amplify biases present in training data, potentially leading to unfair representation in applications like recommendation systems or content discovery.

**S253 — 한국어**

검색 행동은 명시적으로 설계한 보상 함수에 의해 형성되므로 부주의한 보상 명세가 학습 데이터의 편향을 인코딩하거나 증폭하여 추천 시스템이나 콘텐츠 발견 응용에서 불공정한 대표성을 낳을 수 있다.

**S254 — Original**

The RL-based synthesis approach may propagate such biases at scale through synthetic training data.

**S254 — 한국어**

RL 기반 합성 접근법은 합성 학습 데이터를 통해 이러한 편향을 대규모로 전파할 수 있다.

**S255 — Original**

While our experiments focus on benign domains (fashion, music), the same techniques could be applied to sensitive contexts where retrieval biases may have significant consequences.

**S255 — 한국어**

실험은 패션과 음악이라는 무해한 도메인에 초점을 두지만, 같은 기법이 검색 편향의 결과가 중대할 수 있는 민감한 맥락에 적용될 수 있다.

**S256 — Original**

Responsible deployment requires domain-specific bias audits, inclusive design practices, and appropriate oversight mechanisms.

**S256 — 한국어**

책임 있는 배포에는 도메인별 편향 감사, 포용적 설계 관행, 적절한 감독 메커니즘이 필요하다.

**S257 — Original**

We view R4T as a tool for controlled retrieval design that must be accompanied by safeguards rather than a substitute for human judgment and ethical oversight.

**S257 — 한국어**

저자들은 R4T를 인간의 판단과 윤리적 감독을 대체하는 수단이 아니라 안전장치와 함께 사용해야 하는 제어형 검색 설계 도구로 본다.

## Appendix A. Limitations

**S258 — Original**

Despite its effectiveness, R4T has several limitations that suggest directions for future work.

**S258 — 한국어**

R4T는 효과적이지만 향후 연구 방향을 시사하는 몇 가지 한계가 있다.

**S259 — Original**

First, the reinforcement learning stage requires repeated interaction with a frozen retriever and explicit reward computation.

**S259 — 한국어**

첫째, 강화학습 단계에는 동결된 검색기와의 반복 상호작용 및 명시적 보상 계산이 필요하다.

**S260 — Original**

While this cost is amortized at deployment time, the upfront training overhead may be substantial for extremely large or frequently changing databases.

**S260 — 한국어**

이 비용은 배포 시점에 분산되지만, 매우 크거나 자주 변하는 데이터베이스에서는 초기 학습 오버헤드가 상당할 수 있다.

**S261 — Original**

Future work could explore more sample-efficient RL methods, partial retriever updates, or offline approximations to reduce this cost.

**S261 — 한국어**

향후 연구에서는 이 비용을 줄이기 위해 표본 효율이 더 높은 RL 방법, 검색기 부분 업데이트, 오프라인 근사를 탐구할 수 있다.

**S262 — Original**

Second, R4T assumes that desired retrieval properties can be reasonably expressed as explicit reward functions.

**S262 — 한국어**

둘째, R4T는 원하는 검색 속성을 명시적 보상 함수로 합리적으로 표현할 수 있다고 가정한다.

**S263 — Original**

Although we show that combining groundedness, alignment, and diversity yields stable behavior, some user preferences, such as subjective notions of creativity, novelty, or cultural sensitivity, may be difficult to encode in scalar rewards.

**S263 — 한국어**

근거성·정렬성·다양성의 결합이 안정적 행동을 낳음을 보였지만, 창의성·참신성·문화적 민감성의 주관적 개념 같은 일부 사용자 선호는 스칼라 보상으로 인코딩하기 어려울 수 있다.

**S264 — Original**

Learning reward functions from user feedback or preference data is a promising direction to address this limitation.

**S264 — 한국어**

사용자 피드백이나 선호 데이터에서 보상 함수를 학습하는 것은 이 한계를 해결할 유망한 방향이다.

**S265 — Original**

Third, our evaluation relies in part on LLM-as-a-Judge for assessing open-ended retrieval quality.

**S265 — 한국어**

셋째, 개방형 검색 품질 평가의 일부를 LLM-as-a-Judge에 의존한다.

**S266 — Original**

While prior work suggests strong correlation with human judgments, such evaluations may still introduce biases inherited from the judge model and may not fully capture all qualitative aspects of retrieval usefulness.

**S266 — 한국어**

선행 연구가 인간 판단과의 강한 상관을 시사하지만, 이러한 평가는 심판 모델에서 물려받은 편향을 도입할 수 있고 검색 유용성의 모든 정성적 측면을 완전히 포착하지 못할 수 있다.

**S267 — Original**

Incorporating human evaluation or hybrid evaluation protocols would strengthen future studies.

**S267 — 한국어**

인간 평가나 혼합 평가 절차를 포함하면 향후 연구가 더 강해질 것이다.

**S268 — Original**

Finally, our instantiation of R4T focuses on a specific fan-out architecture and diffusion-based retriever.

**S268 — 한국어**

마지막으로 이 논문의 R4T 구현은 특정 팬아웃 아키텍처와 확산 기반 검색기에 초점을 둔다.

**S269 — Original**

Although the framework is general, empirical results may depend on the choice of base language model, embedding space, and diffusion architecture.

**S269 — 한국어**

프레임워크는 일반적이지만 실증 결과는 기본 언어 모델, 임베딩 공간, 확산 아키텍처 선택에 따라 달라질 수 있다.

**S270 — Original**

Extending R4T to other retrieval backbones, modalities, and task settings remains an open area for exploration.

**S270 — 한국어**

R4T를 다른 검색 백본, 모달리티, 과제 설정으로 확장하는 일은 열린 연구 영역이다.

**S271 — Original**

Overall, we view R4T as an initial step toward scalable training of set-valued retrieval systems under complex objectives, rather than a complete solution to all forms of controllable retrieval.

**S271 — 한국어**

전반적으로 저자들은 R4T를 모든 형태의 제어 가능 검색에 대한 완전한 해법이 아니라 복잡한 목적 아래 집합값 검색 시스템을 확장 가능하게 학습하기 위한 첫걸음으로 본다.

## Appendix B. Evaluation Metrics

### B.1 LLM-as-a-Judge Evaluation

**S272 — Original**

For Open-Ended Abstract Retrieval (OAR), retrieval quality is defined by set-level properties that do not admit unique ground-truth targets.

**S272 — 한국어**

개방형 추상 검색(OAR)의 검색 품질은 유일한 정답 표적을 허용하지 않는 집합 수준 속성으로 정의된다.

**S273 — Original**

We therefore adopt LLM-as-a-Judge evaluation using Gemini-2.5-Flash, which supports multimodal inputs (text, images, and audio).

**S273 — 한국어**

따라서 텍스트·이미지·오디오의 멀티모달 입력을 지원하는 Gemini-2.5-Flash를 사용해 LLM-as-a-Judge 평가를 수행한다.

> **번역자 주 - 재현 설정 불일치:** 본문 S136은 Gemini-2.5-Pro를 심판 모델로 명시하지만 이 부록은 Gemini-2.5-Flash라고 한다. Table 2의 Gemini-2.5-Pro는 넓은 질의 생성 역할로도 언급된다. 공개 arXiv v1만으로 OAR 심판에 실제 사용한 모델을 확정할 수 없으므로 재현 전에 저자 확인이나 코드·설정 공개본 확인이 필요하다.

**S274 — Original**

This evaluation paradigm has been shown to correlate well with human judgments for retrieval quality assessment (Zheng et al., 2023).

**S274 — 한국어**

이 평가 패러다임은 검색 품질 평가에서 인간 판단과 높은 상관을 보이는 것으로 알려졌다(Zheng et al., 2023).

**S275 — Original**

We evaluate three dimensions.

**S275 — 한국어**

세 가지 차원을 평가한다.

**S276 — Original**

Collection Diversity: The degree to which retrieved collections span distinct semantic interpretations of the broad query.

**S276 — 한국어**

모음 다양성: 검색된 모음이 넓은 질의의 서로 다른 의미 해석을 얼마나 포괄하는지 나타낸다.

**S277 — Original**

Query-Collection Alignment: How well the retrieved collections collectively reflect the intent of the original query.

**S277 — 한국어**

질의-모음 정렬성: 검색된 모음 전체가 원 질의의 의도를 얼마나 잘 반영하는지 나타낸다.

**S278 — Original**

Groundedness: How accurately each retrieved collection corresponds to its generating sub-query.

**S278 — 한국어**

근거성: 검색된 각 모음이 이를 생성한 하위 질의에 얼마나 정확히 대응하는지 나타낸다.

**S279 — Original**

For each dimension, the LLM judge assigns a score on a 5-point Likert scale (1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent), along with a brief justification.

**S279 — 한국어**

LLM 심판은 각 차원에 대해 5점 리커트 척도(1=나쁨, 2=보통 이하, 3=좋음, 4=매우 좋음, 5=탁월함)의 점수와 짧은 근거를 부여한다.

**S280 — Original**

To reduce evaluation bias, we randomize item order, apply explicit evaluation criteria, require explanations for each score, and avoid any mention of the retrieval method in the prompts.

**S280 — 한국어**

평가 편향을 줄이기 위해 항목 순서를 무작위화하고, 명시적 평가 기준을 적용하며, 각 점수의 설명을 요구하고, 프롬프트에서 검색 방법을 전혀 언급하지 않는다.

**S281 — Original**

Complete prompt templates are provided in Appendix E.

**S281 — 한국어**

전체 프롬프트 템플릿은 부록 E에 제시한다.

### B.2 WSCR Metrics

**S282 — Original**

For Weakly Supervised Compositional Retrieval (WSCR), we evaluate retrieval quality using reference-based coverage metrics and a diversity measure.

**S282 — 한국어**

약지도 구성 검색(WSCR)에서는 참조 기반 포괄성 지표와 다양성 척도로 검색 품질을 평가한다.

**S283 — Original**

Each query is associated with a reference item set that represents one plausible realization of the intended semantics, rather than an exhaustive or uniquely correct target.

**S283 — 한국어**

각 질의에는 완전하거나 유일하게 올바른 표적이 아니라 의도한 의미의 가능한 실현 하나를 나타내는 참조 항목 집합이 연결된다.

**S284 — Original**

Accordingly, recall-based metrics are interpreted as proxies for semantic coverage rather than strict correctness.

**S284 — 한국어**

따라서 재현율 기반 지표는 엄격한 정답 여부가 아니라 의미 포괄성의 대리 지표로 해석한다.

#### Recall@5K

**S285 — Original**

Recall@5K measures the fraction of reference items retrieved within the candidate pool.

**S285 — 한국어**

Recall@5K는 후보 풀 안에서 검색된 참조 항목의 비율을 측정한다.

**S286 — Original**

We retrieve 500 candidates for each of the $k=10$ sub-queries (or generated embeddings), yielding a pool of 5,000 items per inference pass.

**S286 — 한국어**

$k=10$개 하위 질의 또는 생성 임베딩 각각에서 후보 500개를 검색하여 추론 패스마다 5,000개 항목의 풀을 만든다.

#### Hit@5K

**S287 — Original**

Hit@5K measures the percentage of queries for which at least one reference item appears in the retrieved candidate pool, capturing whether any semantic facet of the reference realization is recovered.

**S287 — 한국어**

Hit@5K는 검색 후보 풀에 참조 항목이 하나 이상 나타나는 질의의 비율을 측정하여 참조 실현의 의미 측면 중 하나라도 복원했는지 포착한다.

#### Vendi Score

**S288 — Original**

To assess diversity and generation stability, we perform $N=5$ independent inference runs per query.

**S288 — 한국어**

다양성과 생성 안정성을 평가하기 위해 질의마다 $N=5$회의 독립 추론을 수행한다.

**S289 — Original**

For each run, we compute a representative embedding by averaging the constituent sub-query embeddings.

**S289 — 한국어**

각 실행에서 구성 하위 질의 임베딩을 평균하여 대표 임베딩을 계산한다.

**S290 — Original**

The Vendi Score (Friedman and Dieng, 2022) is computed across these embeddings to quantify semantic variance across runs.

**S290 — 한국어**

이 임베딩들 사이의 Vendi Score를 계산해 실행 간 의미적 변이를 정량화한다(Friedman and Dieng, 2022).

## Appendix C. Broad Query Generation

**S291 — Original**

To evaluate R4T across diverse retrieval regimes, we construct two types of synthetic broad queries corresponding to the two tasks studied in this paper: (1) Open-Ended Abstract Retrieval (OAR) and (2) Weakly Supervised Compositional Retrieval (WSCR).

**S291 — 한국어**

다양한 검색 체제에서 R4T를 평가하기 위해 논문의 두 과제, (1) 개방형 추상 검색(OAR)과 (2) 약지도 구성 검색(WSCR)에 해당하는 두 종류의 합성 넓은 질의를 구성한다.

**S292 — Original**

This appendix describes the query construction procedures used for each task.

**S292 — 한국어**

이 부록은 각 과제에 사용한 질의 구성 절차를 설명한다.

### C.1 OAR: Broad Query Generation

**S293 — Original**

Broad queries for OAR are open-ended, exploratory textual prompts that describe general themes, styles, or scenarios without specifying concrete items.

**S293 — 한국어**

OAR의 넓은 질의는 구체적인 항목을 지정하지 않고 일반적인 테마, 스타일, 상황을 묘사하는 개방형 탐색 텍스트 프롬프트다.

**S294 — Original**

These queries are designed to elicit diverse, collection-level retrieval outputs that admit multiple valid interpretations, consistent with the absence of ground-truth supervision in OAR.

**S294 — 한국어**

이 질의는 OAR에 정답 지도 신호가 없다는 특성에 맞게 여러 타당한 해석을 허용하는 다양한 모음 수준 검색 출력을 유도하도록 설계한다.

**S295 — Original**

We adopt a multi-template generation strategy to ensure broad coverage of semantic intents and query styles.

**S295 — 한국어**

의미 의도와 질의 스타일을 폭넓게 포괄하기 위해 다중 템플릿 생성 전략을 채택한다.

**S296 — Original**

Queries are generated using a large language model with diverse prompt templates targeting different aspects of abstraction, including: aesthetic themes (e.g., “bohemian festival style”), activity-based scenarios (e.g., “weekend brunch outfit”), seasonal contexts (e.g., “summer vacation vibes”), lifestyle identities (e.g., “sustainable living”), mood expressions (e.g., “confident and bold”), cultural trends (e.g., “cottagecore aesthetic”), functional needs (e.g., “travel essentials”), and hybrid combinations (e.g., “vintage meets modern”).

**S296 — 한국어**

질의는 서로 다른 추상화 측면을 겨냥한 다양한 프롬프트 템플릿과 LLM으로 생성한다. 여기에는 미적 테마(“bohemian festival style”), 활동 기반 상황(“weekend brunch outfit”), 계절 맥락(“summer vacation vibes”), 라이프스타일 정체성(“sustainable living”), 기분 표현(“confident and bold”), 문화적 유행(“cottagecore aesthetic”), 기능적 요구(“travel essentials”), 혼합 조합(“vintage meets modern”)이 포함된다.

#### OAR 넓은 질의 생성 프롬프트

**S297 — Original**

System: You are a creative query generator for a retrieval system.

**S297 — 한국어**

시스템: 당신은 검색 시스템을 위한 창의적인 질의 생성기다.

**S298 — Original**

User: Generate 100 diverse, creative broad queries for a fashion/music retrieval system.

**S298 — 한국어**

사용자: 패션/음악 검색 시스템을 위한 다양하고 창의적인 넓은 질의 100개를 생성하라.

**S299 — Original**

Each query should be 2--6 words describing a general theme, aesthetic, or scenario.

**S299 — 한국어**

각 질의는 일반적인 테마, 미학 또는 상황을 묘사하는 2~6개 단어여야 한다.

**S300 — Original**

Queries should be open-ended and exploratory.

**S300 — 한국어**

질의는 개방적이고 탐색적이어야 한다.

**S301 — Original**

Focus on high-level themes rather than specific items.

**S301 — 한국어**

구체적 항목보다 상위 수준 테마에 집중하라.

**S302 — Original**

Use natural, conversational language.

**S302 — 한국어**

자연스럽고 대화체인 언어를 사용하라.

**S303 — Original**

Avoid brand names or concrete product references.

**S303 — 한국어**

브랜드 이름이나 구체적 제품 언급을 피하라.

**S304 — Original**

Each query should admit multiple valid interpretations.

**S304 — 한국어**

각 질의는 여러 타당한 해석을 허용해야 한다.

**S305 — Original**

Return only a JSON array of query strings.

**S305 — 한국어**

질의 문자열의 JSON 배열만 반환하라.

**S306 — Original**

After generation and deduplication, we obtain 43,874 unique broad queries for the OAR task.

**S306 — 한국어**

생성 및 중복 제거 후 OAR 과제용 고유 넓은 질의 43,874개를 얻는다.

**S307 — Original**

These queries are randomly split into train/validation/test sets with an $8{:}1{:}1$ ratio.

**S307 — 한국어**

이 질의를 $8{:}1{:}1$ 비율로 학습/검증/시험 세트에 무작위 분할한다.

**S308 — Original**

For each query, we generate training supervision using the Fan-Out Language Model (FOLM) with temperature $0.9$ and a sample size of $128$ to synthesize targets for diffusion model training.

**S308 — 한국어**

각 질의에 대해 temperature $0.9$, 표본 크기 $128$로 FOLM을 사용해 확산 모델 학습 표적이 될 지도 데이터를 생성한다.

### C.2 Broad Query Generation for WSCR

**S309 — Original**

Broad queries for WSCR are constructed in a fundamentally different manner from OAR.

**S309 — 한국어**

WSCR의 넓은 질의는 OAR과 근본적으로 다른 방식으로 구성한다.

**S310 — Original**

Instead of being generated independently, each WSCR query is derived from an existing item set and serves as a weak, reference-based description of one plausible compositional realization of a user intent.

**S310 — 한국어**

각 WSCR 질의는 독립적으로 생성되지 않고 기존 항목 집합에서 도출되며, 사용자 의도를 구성적으로 실현할 수 있는 사례 하나에 대한 약한 참조 기반 설명 역할을 한다.

**S311 — Original**

Concretely, we start from curated item sets (e.g., outfits in Polyvore), each consisting of multiple complementary items.

**S311 — 한국어**

구체적으로 여러 상보적 항목으로 구성된 엄선된 항목 집합, 예를 들어 Polyvore 의상에서 시작한다.

**S312 — Original**

Given the item names within a set, we prompt a large language model to generate a concise, outfit-level query that captures the overall style, aesthetic, or occasion of the set, without enumerating individual items.

**S312 — 한국어**

집합 안의 항목 이름을 LLM에 주고 개별 항목을 나열하지 않으면서 집합 전체의 스타일, 미학 또는 상황을 포착하는 간결한 의상 수준 질의를 생성하게 한다.

**S313 — Original**

The resulting query functions as a high-level semantic abstraction of the item composition, rather than a uniquely correct label.

**S313 — 한국어**

결과 질의는 유일하게 올바른 라벨이 아니라 항목 구성의 상위 수준 의미 추상화 역할을 한다.

**S314 — Original**

This process yields pairs of the form $(q,\mathcal{Y})$, where $q$ is a broad query and $\mathcal{Y}$ is one plausible reference item set.

**S314 — 한국어**

이 과정은 넓은 질의 $q$와 가능한 참조 항목 집합 하나인 $\mathcal{Y}$로 이루어진 $(q,\mathcal{Y})$ 형식의 쌍을 만든다.

**S315 — Original**

Importantly, $\mathcal{Y}$ is not treated as ground truth: many alternative item sets may equally satisfy the semantics of $q$.

**S315 — 한국어**

중요하게도 $\mathcal{Y}$를 정답으로 취급하지 않는다. 여러 대안 항목 집합이 $q$의 의미를 똑같이 만족할 수 있다.

**S316 — Original**

These query-set pairs therefore constitute weak supervision suitable for WSCR.

**S316 — 한국어**

따라서 이 질의-집합 쌍은 WSCR에 적합한 약지도 신호를 이룬다.

#### WSCR: 항목 집합에서 넓은 질의 생성 프롬프트

**S317 — Original**

System: You are a query generator for outfit-level retrieval.

**S317 — 한국어**

시스템: 당신은 의상 수준 검색을 위한 질의 생성기다.

**S318 — Original**

User: Given the following fashion items in an outfit, generate a broad outfit-level search query that describes the overall style or theme of the outfit.

**S318 — 한국어**

사용자: 다음 의상에 포함된 패션 항목이 주어졌을 때, 의상의 전체 스타일이나 테마를 설명하는 넓은 의상 수준 검색 질의를 생성하라.

**S319 — Original**

The query should be: 2--8 words; broad and general (do not list specific item details); focused on overall style, aesthetic, or occasion; suitable for searching for similar outfits.

**S319 — 한국어**

질의는 2~8개 단어이고, 구체적 항목의 세부사항을 나열하지 않는 넓고 일반적인 표현이며, 전체 스타일·미학·상황에 초점을 맞추고, 비슷한 의상을 검색하기에 적합해야 한다.

**S320 — Original**

Items: `- [item name 1]`, `- [item name 2]`, `...`

**S320 — 한국어**

항목: `- [항목 이름 1]`, `- [항목 이름 2]`, `...`

**S321 — Original**

Return only the query text.

**S321 — 한국어**

질의 텍스트만 반환하라.

#### Training and Test Set Augmentation

**S322 — Original**

System: You are an outfit composer and query generator.

**S322 — 한국어**

시스템: 당신은 의상 구성자이자 질의 생성기다.

**S323 — Original**

User: Given a list of fashion items, select multiple sets of exactly 10 items each.

**S323 — 한국어**

사용자: 패션 항목 목록이 주어지면 정확히 10개 항목으로 이루어진 여러 집합을 선택하라.

**S324 — Original**

Each set should form a coherent outfit with a distinct style.

**S324 — 한국어**

각 집합은 서로 구별되는 스타일의 일관된 의상을 이루어야 한다.

**S325 — Original**

For each set, generate a broad outfit-level query (2--8 words) describing the overall style or occasion.

**S325 — 한국어**

각 집합에 대해 전체 스타일이나 상황을 설명하는 2~8개 단어의 넓은 의상 수준 질의를 생성하라.

**S326 — Original**

Each set must contain exactly 10 items.

**S326 — 한국어**

각 집합은 정확히 10개 항목을 포함해야 한다.

**S327 — Original**

Sets should differ in style or occasion.

**S327 — 한국어**

집합들은 스타일이나 상황이 서로 달라야 한다.

**S328 — Original**

Queries should be broad and not enumerate item details.

**S328 — 한국어**

질의는 넓어야 하며 항목 세부사항을 열거해서는 안 된다.

**S329 — Original**

Return the selected item indices and the corresponding queries in a structured format.

**S329 — 한국어**

선택한 항목 인덱스와 해당 질의를 구조화된 형식으로 반환하라.

**S330 — Original**

To increase coverage and reduce overfitting to specific reference realizations, we further augment the WSCR data using structured item-set recomposition guided by a language model.

**S330 — 한국어**

포괄성을 높이고 특정 참조 실현에 대한 과적합을 줄이기 위해 언어 모델이 안내하는 구조화된 항목 집합 재구성으로 WSCR 데이터를 추가 증강한다.

**S331 — Original**

For each original item set, we construct a candidate pool of $50$ items consisting of the original set plus randomly sampled items from the global item pool.

**S331 — 한국어**

각 원본 항목 집합마다 원본 집합과 전역 항목 풀에서 무작위 샘플링한 항목으로 구성된 50개 항목의 후보 풀을 만든다.

**S332 — Original**

A language model is prompted in a single call to select multiple ($8$) distinct subsets of $10$ items, each forming a coherent outfit with a different style.

**S332 — 한국어**

언어 모델에 한 번 호출하여 각각 다른 스타일의 일관된 의상을 이루는 10개 항목의 서로 다른 부분집합 8개를 선택하게 한다.

**S333 — Original**

For each subset, a corresponding broad query is generated.

**S333 — 한국어**

각 부분집합에 해당하는 넓은 질의를 생성한다.

**S334 — Original**

For each test item set, we sample multiple seed subsets containing $3$--$60\%$ of the original items.

**S334 — 한국어**

각 시험 항목 집합에서 원본 항목의 $3$~$60\%$를 포함하는 여러 시드 부분집합을 샘플링한다.

**S335 — Original**

For each seed, a language model selects additional items from a $30$-item candidate pool to form complete $10$-item outfits, each accompanied by a broad query.

**S335 — 한국어**

각 시드마다 언어 모델이 30개 항목 후보 풀에서 추가 항목을 선택해 완전한 10개 항목 의상을 만들고 각각에 넓은 질의를 붙인다.

**S336 — Original**

This procedure produces multiple plausible compositional realizations for a single query while preserving partial overlap with the original set.

**S336 — 한국어**

이 절차는 원본 집합과의 부분적 중첩을 유지하면서 하나의 질의에 여러 가능한 구성 실현을 만든다.

**S337 — Original**

Across all splits, this procedure yields 84,704 unique broad queries for WSCR.

**S337 — 한국어**

모든 분할에서 이 절차는 WSCR용 고유 넓은 질의 84,704개를 만든다.

**S338 — Original**

The resulting dataset is split into train/validation/test sets using an $8{:}1{:}1$ ratio.

**S338 — 한국어**

결과 데이터셋은 $8{:}1{:}1$ 비율로 학습/검증/시험 세트에 분할한다.

**S339 — Original**

As in OAR, diffusion model training targets are generated by running the Fan-Out Language Model (FOLM) with temperature $0.9$ and a sample size of $128$ per query over the training set.

**S339 — 한국어**

OAR과 마찬가지로 학습 세트의 각 질의에 대해 temperature $0.9$, 표본 크기 $128$로 FOLM을 실행하여 확산 모델 학습 표적을 생성한다.

**S340 — Original**

Overall, this construction ensures that WSCR evaluates retrieval under weak, reference-based supervision, where success is measured by compositional coverage rather than exact set matching.

**S340 — 한국어**

전반적으로 이 구성은 WSCR이 정확한 집합 일치가 아니라 구성적 포괄성으로 성공을 측정하는 약한 참조 기반 지도 아래 검색을 평가하도록 보장한다.

## Appendix D. Query Fan-out Prompts

### OAR 질의 팬아웃 프롬프트

**S341 — Original**

You are a Query Writer. Given a broad query, your task is to create a list of queries which are diverse but cover the same topic as the broad query (better adding/changing one to three words). These queries will be used to search a fashion dataset.

**S341 — 한국어**

당신은 질의 작성자다. 넓은 질의가 주어지면 다양하면서도 그 넓은 질의와 같은 주제를 포괄하는 질의 목록을 만들어야 한다. 한 단어에서 세 단어를 추가하거나 바꾸는 편이 좋다. 이 질의는 패션 데이터셋 검색에 사용된다.

**S342 — Original**

You should show your thinking process in `<think> </think>` tags. You MUST return the final list of queries in JSON format in `<queries> </queries>` tags.

**S342 — 한국어**

사고 과정을 `<think> </think>` 태그 안에 보여야 한다. 최종 질의 목록은 반드시 `<queries> </queries>` 태그 안에 JSON 형식으로 반환해야 한다.

**S343 — Original**

For example:

```text
<think>
[thinking process]
</think>
<queries>
[
    "query1",
    "query2",
    "query3",
    ... (up to 10 queries)
]
</queries>
```

**S343 — 한국어**

예시:

```text
<think>
[사고 과정]
</think>
<queries>
[
    "질의1",
    "질의2",
    "질의3",
    ... (최대 10개 질의)
]
</queries>
```

**S344 — Original**

The broad query is: `<broad_query>{broad_query}</broad_query>`

**S344 — 한국어**

넓은 질의: `<broad_query>{broad_query}</broad_query>`

> **재현 주의:** 프롬프트가 모델에게 숨은 사고 과정을 출력하도록 요구한다. 최신 모델 API에서는 정책이나 제품 사양에 따라 이 요구가 무시되거나 요약된 근거만 반환될 수 있다. 검색 실험을 재현할 때는 최종 `<queries>` JSON만 파싱 가능하도록 구현하는 편이 안전하다.

### WSCR 질의 팬아웃 프롬프트

**S345 — Original**

You are a Query Writer. Your task is to create a list of queries for a broad query given by me to retrieve a set of items from a fashion dataset to form an outfit.

**S345 — 한국어**

당신은 질의 작성자다. 내가 제공한 넓은 질의에 대해 패션 데이터셋에서 의상을 구성할 항목 집합을 검색하는 질의 목록을 만들어야 한다.

**S346 — Original**

You should show your thinking process in `<think> </think>` tags. You MUST return the final list of queries in JSON format in `<queries> </queries>` tags.

**S346 — 한국어**

사고 과정을 `<think> </think>` 태그 안에 보여야 한다. 최종 질의 목록은 반드시 `<queries> </queries>` 태그 안에 JSON 형식으로 반환해야 한다.

**S347 — Original**

For example:

```text
<think>
[thinking process]
</think>
<queries>
[
    "query1",
    "query2",
    "query3",
    ... (up to 10 queries)
]
</queries>
```

**S347 — 한국어**

예시:

```text
<think>
[사고 과정]
</think>
<queries>
[
    "질의1",
    "질의2",
    "질의3",
    ... (최대 10개 질의)
]
</queries>
```

**S348 — Original**

The broad query is: `<broad_query>{broad_query}</broad_query>`

**S348 — 한국어**

넓은 질의: `<broad_query>{broad_query}</broad_query>`

## Appendix E. LLM Judge Evaluation Prompts

**S349 — Original**

In this section, we provide the detailed prompts used for LLM-as-a-Judge evaluation.

**S349 — 한국어**

이 절에서는 LLM-as-a-Judge 평가에 사용한 상세 프롬프트를 제시한다.

**S350 — Original**

Our prompts are carefully designed to minimize bias and maximize fairness through several strategies.

**S350 — 한국어**

프롬프트는 여러 전략으로 편향을 최소화하고 공정성을 극대화하도록 신중하게 설계했다.

**S351 — Original**

Randomization: Items are presented in random order to avoid position bias.

**S351 — 한국어**

무작위화: 위치 편향을 피하기 위해 항목을 무작위 순서로 제시한다.

**S352 — Original**

Objective Criteria: We provide clear, measurable evaluation dimensions.

**S352 — 한국어**

객관적 기준: 명확하고 측정 가능한 평가 차원을 제공한다.

**S353 — Original**

Explanation Requirement: The judge must provide reasoning for scores.

**S353 — 한국어**

설명 요구: 심판은 점수의 근거를 제시해야 한다.

**S354 — Original**

Method Agnostic: No mention of retrieval methods or systems.

**S354 — 한국어**

방법 독립성: 검색 방법이나 시스템을 언급하지 않는다.

**S355 — Original**

Calibration Examples: We include anchor examples for score calibration.

**S355 — 한국어**

보정 예시: 점수 보정을 위한 기준 예시를 포함한다.

**S356 — Original**

Structured Output: JSON format ensures consistent score extraction.

**S356 — 한국어**

구조화 출력: JSON 형식으로 일관된 점수 추출을 보장한다.

### OAR - Collection Diversity Evaluation

**S357 — Original**

System Prompt: You are an expert evaluator assessing the diversity of retrieved content items. You will be shown a set of items (product images or text descriptions) and asked to evaluate how diverse they are in terms of semantic content, themes, and categories.

**S357 — 한국어**

시스템 프롬프트: 당신은 검색된 콘텐츠 항목의 다양성을 평가하는 전문 평가자다. 제품 이미지 또는 텍스트 설명으로 이루어진 항목 집합을 보고 의미 내용, 테마, 범주 측면에서 얼마나 다양한지 평가한다.

**S358 — Original**

User Prompt: `Original Query: {query}`; `Retrieved Items: [Images/text are presented in random order]`.

**S358 — 한국어**

사용자 프롬프트: `원 질의: {query}`; `검색 항목: [이미지/텍스트가 무작위 순서로 제시됨]`.

**S359 — Original**

Please evaluate the diversity of this retrieved set on a scale of 1-5.

**S359 — 한국어**

이 검색 집합의 다양성을 1~5점 척도로 평가하라.

**S360 — Original**

5 (Excellent): Excellent diversity. The set of [Image/audio] provides a comprehensive and creative exploration of the query with minimal redundancy.

**S360 — 한국어**

5(탁월함): 다양성이 탁월하다. [이미지/오디오] 집합이 중복을 최소화하면서 질의를 포괄적이고 창의적으로 탐색한다.

**S361 — Original**

4 (Very Good): Strong variety. The [Image/audio] are mostly distinct and cover different facets of the query well.

**S361 — 한국어**

4(매우 좋음): 다양성이 강하다. [이미지/오디오] 대부분이 서로 구별되며 질의의 여러 측면을 잘 포괄한다.

**S362 — Original**

3 (Good): Decent variety. The [Image/audio] explore several different ideas or aspects of the query. Some overlap is present but acceptable. (This is the expected 'good' result).

**S362 — 한국어**

3(좋음): 다양성이 괜찮다. [이미지/오디오]가 질의의 서로 다른 여러 아이디어나 측면을 탐색한다. 일부 중첩이 있지만 허용할 만하다. 이것이 기대하는 '좋음' 결과다.

**S363 — Original**

2 (Fair): Some repetition. The [Image/audio] show 2-3 distinct ideas, but many are redundant.

**S363 — 한국어**

2(보통 이하): 일부 반복이 있다. [이미지/오디오]가 2~3개의 구별되는 아이디어를 보여주지만 다수가 중복된다.

**S364 — Original**

1 (Poor): Highly redundant. The [Image/audio] are all very similar, exploring only one idea.

**S364 — 한국어**

1(나쁨): 중복이 심하다. [이미지/오디오]가 모두 매우 비슷하며 하나의 아이디어만 탐색한다.

**S365 — Original**

Response Format:

```json
{
  "score": "<1-5>",
  "reasoning": "<brief explanation of your score>",
  "categories_observed": ["<category 1>", "<category 2>", "..."]
}
```

**S365 — 한국어**

응답 형식:

```json
{
  "score": "<1-5>",
  "reasoning": "<점수에 대한 짧은 설명>",
  "categories_observed": ["<관찰 범주 1>", "<관찰 범주 2>", "..."]
}
```

**S366 — Original**

Important: Focus on semantic diversity, not visual or stylistic similarity. Consider whether the items explore different facets or interpretations of the original query.

**S366 — 한국어**

중요: 시각적 또는 스타일적 유사성이 아니라 의미 다양성에 집중하라. 항목들이 원 질의의 서로 다른 측면이나 해석을 탐색하는지 고려하라.

### OAR - Query-Collection Alignment Evaluation

**S367 — Original**

System Prompt: You are an expert evaluator assessing how well a set of retrieved [Image/audio] collectively aligns with an original query.

**S367 — 한국어**

시스템 프롬프트: 당신은 검색된 [이미지/오디오] 집합 전체가 원 질의와 얼마나 잘 정렬되는지 평가하는 전문 평가자다.

**S368 — Original**

User Prompt: You will be shown sub-queries and their representative [Image/audio]. Please evaluate how well this entire set of [Image/audio] represents the original query.

**S368 — 한국어**

사용자 프롬프트: 하위 질의와 각각을 대표하는 [이미지/오디오]가 제시된다. 이 [이미지/오디오] 전체 집합이 원 질의를 얼마나 잘 나타내는지 평가하라.

**S369 — Original**

`Original Query: {query}`; `Retrieved Items: [Images/audio are presented in random order]`.

**S369 — 한국어**

`원 질의: {query}`; `검색 항목: [이미지/오디오가 무작위 순서로 제시됨]`.

**S370 — Original**

Please evaluate the overall alignment of this [Image/audio] set to the Original Query on a scale of 1-5.

**S370 — 한국어**

이 [이미지/오디오] 집합과 원 질의의 전반적 정렬성을 1~5점 척도로 평가하라.

**S371 — Original**

5 (Excellent): Perfectly relevant. The set of [Image/audio] perfectly captures the full meaning and intent of the original query.

**S371 — 한국어**

5(탁월함): 완벽하게 관련된다. [이미지/오디오] 집합이 원 질의의 전체 의미와 의도를 완벽하게 포착한다.

**S372 — Original**

4 (Very Good): Highly relevant. All [Image/audio] are clearly related to the query and capture its intent well.

**S372 — 한국어**

4(매우 좋음): 관련성이 높다. 모든 [이미지/오디오]가 질의와 분명히 관련되며 의도를 잘 포착한다.

**S373 — Original**

3 (Good): Relevant. The set of [Image/audio] clearly relates to the original query. Most images are on-topic. (This is the expected 'good' result).

**S373 — 한국어**

3(좋음): 관련된다. [이미지/오디오] 집합이 원 질의와 분명히 관련되고 대부분의 이미지가 주제에 맞는다. 이것이 기대하는 '좋음' 결과다.

**S374 — Original**

2 (Fair): Weakly relevant. A few [Image/audio] relate to the query, but the set as a whole is off-topic or misses the main idea.

**S374 — 한국어**

2(보통 이하): 관련성이 약하다. 일부 [이미지/오디오]만 질의와 관련되고 집합 전체는 주제에서 벗어나거나 핵심 아이디어를 놓친다.

**S375 — Original**

1 (Poor): Mostly irrelevant. The set of [Image/audio], as a whole, does not seem related to the original query.

**S375 — 한국어**

1(나쁨): 대부분 관련이 없다. [이미지/오디오] 집합 전체가 원 질의와 관련 없어 보인다.

**S376 — Original**

Response Format:

```json
{
  "score": "<1-5>",
  "reasoning": "<brief explanation of your score>",
  "relevant_items_count": "<number>",
  "total_items_count": "<number>"
}
```

**S376 — 한국어**

응답 형식:

```json
{
  "score": "<1-5>",
  "reasoning": "<점수에 대한 짧은 설명>",
  "relevant_items_count": "<관련 항목 수>",
  "total_items_count": "<전체 항목 수>"
}
```

**S377 — Original**

Important: Judge the set as a whole. Do these [Image/audio] give you a good understanding of the original query?

**S377 — 한국어**

중요: 집합 전체를 판단하라. 이 [이미지/오디오]를 통해 원 질의를 잘 이해할 수 있는가?

### OAR - Groundedness Evaluation

**S378 — Original**

System Prompt: You are an expert evaluator assessing how well a retrieved [Image/audio] matches its intermediate sub-query.

**S378 — 한국어**

시스템 프롬프트: 당신은 검색된 [이미지/오디오]가 중간 하위 질의와 얼마나 잘 일치하는지 평가하는 전문 평가자다.

**S379 — Original**

User Prompt: You will be shown sub-queries that were generated to retrieve items, along with the items actually retrieved for each sub-query.

**S379 — 한국어**

사용자 프롬프트: 항목 검색을 위해 생성한 하위 질의와 각 하위 질의에서 실제로 검색된 항목이 함께 제시된다.

**S380 — Original**

`Sub-query 1: {subquery_1}`; `Retrieved Item 1: [Image/audio]`; `Sub-query 2: {subquery_2}`; `Retrieved Item 2: [Image/audio]`; `... [repeat for all $k$ sub-queries]`.

**S380 — 한국어**

`하위 질의 1: {subquery_1}`; `검색 항목 1: [이미지/오디오]`; `하위 질의 2: {subquery_2}`; `검색 항목 2: [이미지/오디오]`; `... [$k$개 하위 질의 전체에 반복]`.

**S381 — Original**

For each sub-query and its retrieved item, evaluate the groundedness on a scale of 1-5.

**S381 — 한국어**

각 하위 질의와 그 검색 항목의 근거성을 1~5점 척도로 평가하라.

**S382 — Original**

5 (Excellent): Perfect match. The [Image/audio] is a perfect, textbook example of its sub-query.

**S382 — 한국어**

5(탁월함): 완벽하게 일치한다. [이미지/오디오]가 하위 질의의 교과서적인 완벽한 예다.

**S383 — Original**

4 (Very Good): Strong match. The [Image/audio] clearly and specifically illustrates the sub-query's concept.

**S383 — 한국어**

4(매우 좋음): 강하게 일치한다. [이미지/오디오]가 하위 질의의 개념을 명확하고 구체적으로 보여준다.

**S384 — Original**

3 (Good): Good match. The [Image/audio] is a clear and reasonable example of its sub-query. (This is the expected 'good' result).

**S384 — 한국어**

3(좋음): 잘 일치한다. [이미지/오디오]가 하위 질의의 명확하고 합리적인 예다. 이것이 기대하는 '좋음' 결과다.

**S385 — Original**

2 (Fair): Weakly related. The [Image/audio] is on the general topic (e.g., `schoolcore') but fails to show the sub-query's specific concept (e.g., `velvet').

**S385 — 한국어**

2(보통 이하): 약하게 관련된다. [이미지/오디오]가 일반 주제, 예를 들어 `schoolcore`에는 맞지만 하위 질의의 구체적 개념, 예를 들어 `velvet`은 보여주지 못한다.

**S386 — Original**

1 (Poor): Total mismatch. The [Image/audio] is completely unrelated to its sub-query.

**S386 — 한국어**

1(나쁨): 완전히 불일치한다. [이미지/오디오]가 하위 질의와 전혀 관련 없다.

**S387 — Original**

Response Format:

```json
{
  "per_subquery_scores": [
    {
      "subquery": "<subquery_text>",
      "score": "<1-5>",
      "reasoning": "<brief explanation>"
    },
    "..."
  ],
  "average_score": "<1-5>"
}
```

**S387 — 한국어**

응답 형식:

```json
{
  "per_subquery_scores": [
    {
      "subquery": "<하위 질의 텍스트>",
      "score": "<1-5>",
      "reasoning": "<짧은 설명>"
    },
    "..."
  ],
  "average_score": "<1-5>"
}
```

**S388 — Original**

Important: You are NOT judging alignment to the original query. You are ONLY judging if the [Image/audio] for `Sub-query 1' matches `Sub-query 1'.

**S388 — 한국어**

중요: 원 질의와의 정렬성을 판단하는 것이 아니다. 오직 `하위 질의 1`의 [이미지/오디오]가 `하위 질의 1`과 일치하는지만 판단한다.

## Appendix F. Implementation Details

### Fan-Out LM (FOLM)

**S389 — Original**

We initialize the Fan-Out LM using a standard instruction-tuned checkpoint.

**S389 — 한국어**

표준 지시 조정 체크포인트로 팬아웃 LM을 초기화한다.

**S390 — Original**

Training utilizes the GRPO algorithm with Soft-PPO regularization, where KL penalties are applied directly to the per-token loss.

**S390 — 한국어**

학습에는 Soft-PPO 규제를 결합한 GRPO 알고리즘을 사용하며 KL 벌점은 토큰별 손실에 직접 적용한다.

**S391 — Original**

The policy is optimized to generate $k$ sub-queries that maximize task-specific set-level rewards, including diversity, groundedness, and alignment.

**S391 — 한국어**

정책은 다양성, 근거성, 정렬성을 포함한 과제별 집합 수준 보상을 최대화하는 $k$개 하위 질의를 생성하도록 최적화한다.

**S392 — Original**

We use a learning rate of $1\times10^{-7}$ and a global batch size of 512.

**S392 — 한국어**

학습률은 $1\times10^{-7}$, 전역 배치 크기는 512를 사용한다.

**S393 — Original**

Training was conducted on a TPUv6e-16 Ghostlite Pod (consisting of 16 accelerator cores).

**S393 — 한국어**

학습은 가속기 코어 16개로 구성된 TPUv6e-16 Ghostlite Pod에서 수행했다.

### Supervision Synthesis

**S394 — Original**

Following RL optimization, we use the trained FOLM to synthesize objective-consistent training pairs.

**S394 — 한국어**

RL 최적화 후 학습된 FOLM으로 목적과 일치하는 학습 쌍을 합성한다.

**S395 — Original**

For each query, we generate 128 samples at a temperature of 0.9 to capture the reward-shaped distribution of fan-out behaviors.

**S395 — 한국어**

각 질의에서 temperature 0.9로 표본 128개를 생성해 보상이 형성한 팬아웃 행동 분포를 포착한다.

**S396 — Original**

This data generation stage was performed on a TPUv6e-4 Ghostlite Pod (4 accelerator cores).

**S396 — 한국어**

이 데이터 생성 단계는 가속기 코어 4개의 TPUv6e-4 Ghostlite Pod에서 수행했다.

### Diffusion Training

**S397 — Original**

The diffusion model employs a Transformer backbone adapted for continuous inputs, where the input is a concatenated sequence of target embeddings $Z_{target}\in\mathbb{R}^{L\times d}$.

**S397 — 한국어**

확산 모델은 연속 입력에 맞춘 Transformer 백본을 사용하며, 입력은 표적 임베딩을 연결한 시퀀스 $Z_{target}\in\mathbb{R}^{L\times d}$다.

**S398 — Original**

The model is trained to predict $Z_0$ directly using a Variance Exploding (VE) formulation within the EDM framework.

**S398 — 한국어**

모델은 EDM 프레임워크 안의 분산 폭발(VE) 정식화로 $Z_0$를 직접 예측하도록 학습한다.

**S399 — Original**

We utilize a Diffusion Transformer with a hidden dimension of 1024 and an MLP dimension of 1024, optimized with a warmup cosine decay schedule over $10\times10^6$ steps.

**S399 — 한국어**

은닉 차원 1024, MLP 차원 1024인 Diffusion Transformer를 사용하고 $10\times10^6$ 스텝 동안 워밍업 코사인 감쇠 스케줄로 최적화한다.

**S400 — Original**

At inference, the model generates $L$ embeddings in a single pass using a SDE solver for 256 steps, which are then mapped to database contents via nearest-neighbor retrieval.

**S400 — 한국어**

추론 시 모델은 SDE 솔버를 256스텝 사용해 단일 패스로 $L$개 임베딩을 생성한 뒤 최근접 이웃 검색으로 데이터베이스 콘텐츠에 매핑한다.

- **용어·약어 해설**
  - **SDE (Stochastic Differential Equation, 확률미분방정식)**: 확산 과정의 연속시간 확률 동역학을 기술한다. 여기서는 잡음에서 표적 임베딩 집합으로 이동하는 수치 적분에 사용한다.

**S401 — Original**

This training was conducted on a TPUv6e-16 Ghostlite Pod (16 accelerator cores).

**S401 — 한국어**

이 학습은 가속기 코어 16개의 TPUv6e-16 Ghostlite Pod에서 수행했다.

**S402 — Original**

The specific parameters used for our experiments are detailed in Table 3.

**S402 — 한국어**

실험에 사용한 구체적 매개변수는 표 3에 제시한다.

**S403 — Original**

Table 3: Implementation Hyperparameters for R4T.

**S403 — 한국어**

표 3: R4T 구현 하이퍼파라미터.

| 구분 | Parameter | Value |
|---|---|---|
| Fan-Out LM (RL Training) | Optimizer | AdamW ($\beta_1=0.9$, $\beta_2=0.95$) |
|  | Learning Rate | $1\times10^{-7}$ |
|  | Global Batch Size | 512 |
|  | Micro-batch Size | 64 |
|  | Grad. Accum. Steps | 8 |
|  | Max Seq. Length | 1024 |
|  | Group Size ($G$) | 8 |
|  | Clip Epsilon ($\epsilon$) | 0.2 |
|  | Forward KL Coeff. ($\beta_1$) | 0.05 |
|  | Reverse KL Coeff. ($\beta_2$) | 0.05 |
|  | Reward Norm. | Group-Standardized |
|  | Advantage Est. | Group-Relative |
| Diffusion Training | Model Type | Coherent Transformer |
|  | Seq. Length ($L$) | 12 |
|  | Embed. Dim ($d$) | 128 |
|  | Hidden Dim | 1024 |
|  | MLP Dim | 1024 |
|  | Heads | 16 |
|  | Layers | 6 |
|  | Dropout / Attn. Dropout | 0.1 |
|  | Optimizer | Adam |
|  | Schedule | Warmup Cosine Decay |
|  | Peak LR | $3\times10^{-4}$ |
|  | Warmup Steps | 20,000 |
|  | Total Steps | $10\times10^6$ |
|  | Batch Size | 512 |
|  | EMA Decay | 0.9999 |
|  | Scheme | Variance Exploding |
|  | Weighting | EDM |
|  | Noise Schedule | Tangent |
|  | Range $[\sigma_{\min},\sigma_{\max}]$ | $[10^{-4},80.0]$ |
|  | Data Std ($\sigma_{\text{data}}$) | 0.088 |
|  | Cond. Drop ($p_{\text{drop}}$) | 0.1 |
|  | CFG Strength | 0.1 |
|  | Steps | 256 |

> **표 읽기:** FOLM의 AdamW 모멘트 계수 $\beta_1,\beta_2$와 Soft-PPO의 정·역방향 KL 계수 $\beta_1,\beta_2$는 같은 기호를 재사용하지만 서로 다른 하이퍼파라미터다. 구현에서는 이름 충돌을 피해야 한다. 또한 방법 절 S107은 “probability flow stochastic differential equation”이라고 표현하는데, 일반적으로 probability-flow는 ODE로 불리므로 구현 재현 시 실제 솔버 정의를 확인해야 한다.

## 약어 및 기술 용어 사전

| 원어·약어 | 한국어 | 이 논문에서의 의미 | 최초 등장 |
|---|---|---|---|
| RL (Reinforcement Learning) | 강화학습 | 집합 수준 보상을 만족하는 팬아웃 행동을 발견해 합성 데이터로 바꾸는 일회성 최적화 단계 | S001 |
| property-aligned | 속성 정렬 | 다양성·포괄성·상보성·정렬성·근거성 등 명시한 검색 속성과 결과가 부합하는 상태 | S001 |
| set-valued retrieval | 집합값 검색 | 하나의 정답이 아니라 결과 집합 전체를 출력·평가하는 검색 | S002 |
| groundedness | 근거성 | 생성된 검색 방향 또는 결과가 고정 데이터베이스의 실제 콘텐츠에 대응하는 정도 | S002 |
| fan-out retrieval | 팬아웃 검색 | 하나의 넓은 질의를 여러 하위 질의나 임베딩 방향으로 펼치는 검색 | S004 |
| LLM (Large Language Model) | 대규모 언어 모델 | 하위 질의 집합을 생성하는 팬아웃 정책 및 일부 평가의 심판 | S005 |
| R4T (Retrieve-for-Train) | 학습을 위한 검색 | RL 행동을 합성 지도 데이터로 컴파일하고 경량 검색기에 증류하는 제안 프레임워크 | S007 |
| objective transducer | 목적 전환기 | 보상 명세를 지도학습 가능한 표적 분포로 변환하는 RL의 역할 | S007 |
| OAR (Open-Ended Abstract Retrieval) | 개방형 추상 검색 | 정답 집합 없이 다양성·정렬성·근거성으로 평가하는 탐색 검색 | S030 |
| WSCR (Weakly Supervised Compositional Retrieval) | 약지도 구성 검색 | 가능한 참조 집합 하나를 약한 지도 신호로 삼는 구성 검색 | S030 |
| FOLM (Fan-Out Language Model) | 팬아웃 언어 모델 | 넓은 질의에서 여러 하위 질의를 생성하는 RL 정책 | S033 |
| non-decomposable objective | 비분해 가능 목적 | 항목별 독립 점수의 단순 합으로 환원하기 어려운 집합 전체 목적 | S037 |
| Vendi Score | 벤디 점수 | 임베딩 집합 또는 실행 간 의미적 다양성을 재는 스펙트럼 기반 지표 | S065 |
| GRPO (Group Relative Policy Optimization) | 그룹 상대 정책 최적화 | 동일 입력의 출력 그룹 안에서 상대 보상으로 이점을 계산하는 정책 최적화 | S080 |
| PPO (Proximal Policy Optimization) | 근접 정책 최적화 | 정책 비율을 클리핑해 큰 정책 갱신을 제한하는 알고리즘 | S082 |
| KL divergence | KL 발산 | 활성 정책과 샘플링 정책 사이 분포 차이를 제한하는 규제량 | S082 |
| VE (Variance Exploding) | 분산 폭발 | 잡음 분산이 증가하는 확산 정식화 | S101 |
| EDM | 확산 모델 설계공간 해설 프레임워크 | 잡음 수준별 사전조건화와 손실 가중을 제공하는 확산 프레임워크 | S101 |
| CFG (Classifier-Free Guidance) | 분류기 없는 가이던스 | 조건부·무조건부 예측을 조합해 조건 반영 강도를 조절하는 기법 | S106 |
| CLIP | 대조 언어-이미지 사전학습 | Polyvore 이미지와 텍스트를 공동 임베딩하는 백본 | S120 |
| MuLan | 음악-언어 공동 임베딩 | 비공개 음악 데이터의 텍스트-음악 검색 백본 | S122 |
| Recall@5K | 5천 후보 재현율 | 후보 5,000개 안에 포함된 참조 항목의 비율 | S138 |
| Hit@5K | 5천 후보 적중률 | 후보 5,000개 안에서 참조 항목을 하나 이상 찾은 질의의 비율 | S138 |
| LLM-as-a-Judge | LLM 심판 평가 | 멀티모달 결과 집합을 5점 척도로 평가하는 자동 평가 방식 | S136 |
| SDE (Stochastic Differential Equation) | 확률미분방정식 | 확산 샘플링 동역학을 기술하고 수치적으로 푸는 방정식 | S400 |
| EMA (Exponential Moving Average) | 지수이동평균 | 확산 모델 매개변수의 안정적 평가 복사본을 유지하는 기법 | Table 3 |

## 번역 검수 기록

- **원문 확인:** arXiv v1 PDF 24쪽, 공식 TeX 소스, 실험적 HTML을 대조했다. 제목·저자·제출일·식별자·CC BY 4.0은 arXiv landing page에서 확인했고, ICML-26 게재 정보는 Google Research 공식 게재 페이지에서 확인했다.
- **범위:** 초록, 본문 §1~§5, Impact Statement, Appendix A~F의 서술·프롬프트·표·그림 캡션을 번역했다. References의 서지 목록은 원형 보존 원칙에 따라 반복 수록하지 않았다.
- **문장 정렬:** S001~S403을 전역 단조 증가시켰으며 각 `Original` 블록 바로 뒤에 같은 ID의 `한국어` 블록을 배치했다.
- **수식·수치:** 식 (1)~(9), $\lambda_g=0.6$, $\lambda_d=\lambda_a=0.2$, $k=10$, 표 1~3의 수치와 단위를 원문과 대조했다. 표의 `\` 표기는 의미를 풀어 `해당 없음`으로 표시했다.
- **원문 오탈자 보존:** `principle`, `an graphical`, `$lambda$`, `RK training`, `ivnovles`, `RT4`, `variancee`, `our the third`, `use RL`, `Qwen-4B` 등은 원문 블록에 그대로 두거나 원문의 문구를 보존하고 번역자 주에서 가능한 의도를 설명했다.
- **재현 경고:** OAR 심판 모델이 본문에는 Gemini-2.5-Pro, Appendix B에는 Gemini-2.5-Flash로 적혀 있다. 확정적으로 보정하지 않았으며 재현 시 저자 또는 공개 설정 확인이 필요하다.
- **그림 처리:** 시각 자료 자체를 복제하지 않고 Figure 1~6의 캡션, 핵심 축·질의 라벨 및 본문 해석을 번역했다. Figure 6은 TeX에서 문서 끝에 입력되지만 본문 §3.3의 논리적 위치에 설명했다.
- **해석 원칙:** `may`, `could`와 같은 가능성 표현을 확정형으로 강화하지 않았고, 비공개 Music 데이터와 공개되지 않은 구체 구현에 대해서는 논문 주장을 넘어 추정하지 않았다.
