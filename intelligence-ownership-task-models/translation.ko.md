# 「The Rise of Intelligence Ownership」 한국어 번역 요약

작성일: 2026-07-30

## 원문 정보

- 전체 제목: The Rise of Intelligence Ownership: a task-trained open source model vs the frontier
- 저자: Justinas Zaliaduonis, Joris Zilinskis, Fabian Hildesheim, Joel Hainzl, Gediminas Pazera
- 게시일: 2026-07-27
- 원문 URL: <https://fermisense.com/when-machines-take-the-wheel/>
- 사용자 제공 URL: <https://share.google/rK0rNpIzeaAgOXP2K>
- 원문 언어: 영어
- 접근일: 2026-07-30

## 번역 및 접근 범위

원문 전체를 확인했습니다. 이 파일은 원문의 Part I~VI와 부록 흐름, 핵심 수치와 주장을 보존한 한국어 번역 요약입니다. 저작권이 있는 글을 문장 단위로 전재하지 않았으며, 그래프·이미지와 긴 사례 설명은 의미 중심으로 재구성했습니다.

원문은 Fermisense의 자체 실험과 서비스를 소개하는 사례 연구입니다. 아래의 실험 결과는 독립 검증 사실이 아니라 원문 저자의 보고로 표시합니다.

## 제목과 도입

### Intelligence Ownership의 부상

글은 AI-first 전략으로 성과를 내는 기업들의 공통점을 묻습니다. 저자들은 catalog 검수 workflow에서 동일한 tool, image와 scorer를 사용했을 때 GRPO로 후학습한 9B 공개 가중치 모델이 테스트한 모든 frontier 구성보다 높은 점수를 기록했다고 보고합니다.

보고된 추론 비용은 listing 1,000개당 약 `$0.50`입니다. 비교 대상에 따라 가장 저렴한 frontier보다 약 40배, 가장 비싼 구성보다 약 340배 저렴하다고 설명합니다.

## Part I. 모두가 같은 질문을 했다

ChatGPT 이후 기업은 “AI가 우리를 위해 무엇을 할 수 있는가?”를 물었습니다. 초기에는 요약과 초안처럼 사람이 검토하는 저위험 업무에서 시작했고, 이후 software 개발, content 생성과 내부 knowledge·tool을 연결한 company brain으로 범위가 넓어졌습니다.

투자와 token 사용이 늘었지만 조직 전체의 측정 가능한 성과는 제한적이었습니다. 저자들은 높은 AI 투자 기업과 그렇지 않은 기업의 성장 차이를 인용하며, 성과를 만드는 다섯 방향을 제시합니다.

### 1. task가 아니라 process를 재설계한다

기존 사람 중심 workflow에 model만 추가하면 승인, 검토와 handoff 병목이 그대로 남습니다. AI-first 전환은 누가 무엇을 승인하고 언제 사람이 개입하는지까지 다시 설계해야 합니다.

### 2. 실험에 보상한다

model, tool과 best practice가 빠르게 변하므로 성공만 보고하는 문화로는 개선이 어렵습니다. 실패와 반복 문제를 공유하고 새로운 구성을 시험하도록 장려해야 합니다.

### 3. 맞춤형 business context를 제공한다

prompt와 retrieval은 호출 시점에 context를 주입하지만, 데이터 접근, 권한 통제, 검색 품질과 context window 관리를 위한 별도 engineering이 필요합니다.

### 4. 사용량과 영향을 측정한다

AI가 실제로 무엇을 바꾸었는지 답하려면 자체 데이터로 평가해야 합니다. 성능, decision cost와 효율 영향을 추적하지 않으면 주관적 인상 이상의 주장을 하기 어렵습니다.

### 5. AI 예산 안에서 명확한 사업 목표를 둔다

token 단가 모델은 사용량과 함께 비용이 증가합니다. 저자들은 대규모 사용 시 예산 예측이 어려워지고 현재 API 가격도 장기적으로 유지된다고 보장할 수 없다고 지적합니다.

### Part I 요지

저자들은 마지막 세 문제, 즉 context, 측정과 예산을 해결하는 방법으로 회사 고유 data와 scorer를 사용한 공개 가중치 모델의 강화학습을 제안합니다.

## TL;DR

원문이 강조하는 수치는 다음과 같습니다.

- AI 지출 상위 사분위 기업의 2022-11~2025-12 revenue가 약 2.2배가 되었다는 Ramp 데이터
- 공개 가중치 모델, 독점 task data, 채점 가능한 workflow를 결합한 playbook
- 후학습 9B가 최대 가능 score의 87.3%에 도달했다는 자체 평가
- best frontier 76.9%, 학습 전 base 64.2%
- 강한 frontier와 비교한 decision당 비용 우위 약 68배

## Part II. 앞서는 기업은 무엇이 다른가

저자들은 특정 회사 환경에서 반복되는 workflow를 학습한 모델이, 그 회사를 본 적 없는 범용 모델보다 더 높은 성능을 낼 가능성이 크다고 주장합니다. 범용 능력을 모두 유지할 필요가 없어 더 작은 모델을 사용하고 inference 비용을 낮출 수 있다는 설명입니다.

이는 ChatGPT나 Claude를 해지하라는 뜻이 아닙니다. frontier model로 prototype과 baseline을 만들고, 그 과정에서 input, decision과 correction trace를 모은 뒤 specialist 학습에 활용합니다.

변하는 가격·재고·정책은 tool에 남겨 두고, 반복되는 판단 방법은 weights에 학습시킵니다. 필요하면 frontier와 specialist가 서로를 tool처럼 호출하는 혼합 구조를 사용합니다.

### 외부 사례

- Bridgewater: 내부 투자 전문가의 문서 판단 label을 학습해 best frontier보다 오류가 약 30% 적었다고 보고
- Harvey: 법률 rubric에서 frontier model보다 높은 성능의 open-weight legal agent를 보고
- Intercom: 대규모 고객지원 interaction으로 vertical model을 후학습해 더 낮은 비용과 높은 해결률을 보고

## Part III. Catalog Integrity Agent 사례

전자상거래 catalog는 상품 category, attribute, brand와 policy 판정이 정확해야 합니다. 잘못된 판정은 검색·추천 품질 저하, 사기 노출 또는 과도한 검수 queue로 이어집니다.

저자들이 만든 agent는 다음 순서로 동작합니다.

1. product taxonomy 검색
2. brand 등록·보호 여부 확인
3. category별 attribute schema 조회
4. category, attribute와 allowed/flagged 판정 확정
5. 근거가 약하거나 위험이 높으면 human review로 escalation

실제 위반을 놓치는 오류는 정상품을 잘못 flag하는 오류보다 7배 큰 penalty를 주었다고 설명합니다.

## Part IV. 모델이 연습하는 디지털 트윈

저자들은 Amazon Berkeley Objects의 image와 listing data를 바탕으로 177,767개 review episode를 만들었다고 보고합니다. 불일치 image, 충돌하는 brand claim, policy case와 어려운 정상 사례를 합성해 알려진 정답을 붙였습니다.

환경은 약 13,000개 category taxonomy 검색, brand 확인과 attribute schema 조회 tool을 제공합니다. scorer는 최종 판정, category, attribute 근거, policy 위반과 불필요한 tool call을 평가합니다.

### Frontier benchmark

다섯 frontier model을 200개 stratified validation episode에서 같은 tool, image, scorer와 turn budget으로 비교했습니다. 각 model은 단순 prompt와 약 2,800자 optimized instruction 구성으로 평가됐습니다.

저자 보고에 따르면 best frontier 구성은 최대 가능 score의 76.9%, 후학습 9B는 87.3%였습니다. optimized instruction은 model에 따라 input token 비용을 28~55% 늘렸지만 frontier 구성들은 비슷한 score 구간에서 정체됐다고 설명합니다.

## Part V. 학습 세부 사항

학습에는 RTX PRO 6000 GPU 두 대가 사용됐습니다. 한 대는 rollout 생성, 다른 한 대는 gradient update를 담당했으며 `prime-rl`이 infrastructure로 사용됐습니다.

전체 run은 optimizer 1,000 step, 약 3.5일, GPU rental 약 `$500`으로 보고됩니다. 약 250 step에서 frontier score 구간을 넘어섰다고 설명합니다.

최종 strict benchmark reward는 `0.626`, training monitor의 sampled rollout 평가는 약 `0.671`입니다. 두 수치는 evaluation harness가 다르므로 직접 같은 값으로 취급하면 안 됩니다.

### 품질과 비용

저자들은 후학습이 base 9B보다 정규화 score를 약 23 percentage point 높이면서 추론 비용은 listing 1,000개당 약 `$0.50`로 유지됐다고 보고합니다.

비교 대상 frontier 가격은 약 `$19`, `$34`, `$172/1k`로 서로 다릅니다. 이에 따라 비용 우위도 약 38배, 68배, 344배로 달라집니다.

## Part VI. Intelligence Ownership은 무엇을 할 수 있는가

저자들은 적합한 workflow를 다음처럼 정리합니다.

- 높은 빈도로 반복되어 단가와 오류가 큰 비용이 됨
- 결과를 rule, test 또는 rubric으로 확인 가능
- expert가 올바른 결과에 합의 가능
- model이 일부 성공하지만 일관성이 부족
- 여러 reasoning과 tool call 뒤 하나의 검증 가능한 결정으로 끝남
- 회사 고유 tool, schema와 policy를 사용
- 오류 유형별 비용이 다름
- 민감 data를 자체 경계 밖으로 보낼 수 없음

반대로 빈도가 낮거나 결과를 객관적으로 확인하기 어려운 업무는 frontier model 또는 human review가 더 적합할 수 있습니다. 변경되는 사실의 문제라면 fine-tuning보다 retrieval을 먼저 고려해야 합니다.

## 부록. 여러 산업의 specialist 사례

원문은 software engineering, 고객 통화 요약, 채용 matching, 의료 coding, 전화 상담, email support, 검색, 범죄 기록 분류 등 여러 기업의 자체 보고 사례를 모읍니다.

이 표의 수치는 각 기업이 선택한 task, rubric, frontier baseline과 비용 구조가 서로 다릅니다. 하나의 통합 benchmark처럼 직접 순위를 매기기보다, “좁고 검증 가능한 task에서 후학습 모델이 유리할 수 있다”는 사례 모음으로 읽는 편이 안전합니다.

## 검수 및 사실 확인 메모

### 확인된 공개 artifact

- full model: `BosonicJustin/qwen35-9b-catalog`
- adapter: `BosonicJustin/qwen35-9b-catalog-adapter`
- adapter base: `Qwen/Qwen3.5-9B`
- adapter 형식: LoRA, `r=32`, `lora_alpha=64`
- target module: attention projection과 MLP projection 계열
- Qwen3.5-9B 기반 모델 라이선스: Apache-2.0
- 학습 framework `prime-rl`: Apache-2.0

### 확인하지 못한 항목

Fermisense full model과 adapter 저장소에는 접근일 현재 model card와 명시적 license metadata가 없습니다. training dataset, 전체 scorer, split과 frontier evaluation log도 공개 페이지에서 확인하지 못했습니다.

따라서 가중치를 실제 사용하기 전에 저자에게 license와 데이터 이용 조건을 확인해야 하며, 원문의 품질·비용 수치는 독립 평가 set에서 재검증해야 합니다.

## 함께 볼 자료

- [분석 및 실습 가이드](README.md)
- [수치 검산 실습](01_foundations.ipynb)
- [비대칭 scorer 실습](02_practice.ipynb)
- [TCO와 도입 판단 실습](03_advanced.ipynb)
