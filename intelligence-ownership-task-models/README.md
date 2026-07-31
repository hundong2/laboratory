# Intelligence Ownership: 업무 특화 모델과 프런티어 모델

작성일: 2026-07-30

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [핵심 요약](#핵심-요약)
- [사례 연구 수치](#사례-연구-수치)
- [상세 정리](#상세-정리)
- [비판적으로 읽기](#비판적으로-읽기)
- [도입 의사결정 프레임워크](#도입-의사결정-프레임워크)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

| 구분                  | URL                                                                                          | 확인 범위                                |
| --------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------- |
| 사용자 제공 공유 링크 | <https://share.google/rK0rNpIzeaAgOXP2K>                                                     | 최종 URL 확인                            |
| 분석 원문             | <https://fermisense.com/when-machines-take-the-wheel/>                                       | 2026-07-27 게시 글 전체                  |
| 공개 full model       | <https://huggingface.co/BosonicJustin/qwen35-9b-catalog>                                     | 파일 구성, 모델 크기, metadata           |
| 공개 LoRA adapter     | <https://huggingface.co/BosonicJustin/qwen35-9b-catalog-adapter>                             | `adapter_config.json`                    |
| 기반 모델             | <https://huggingface.co/Qwen/Qwen3.5-9B>                                                     | 모델 구조, Apache-2.0 라이선스           |
| 학습 프레임워크       | <https://github.com/PrimeIntellect-ai/prime-rl>                                              | 기능, GPU 요구 사항, Apache-2.0 라이선스 |
| 비교 사례             | <https://thinkingmachines.ai/news/learning-to-replicate-expert-judgment-in-financial-tasks/> | Bridgewater 전문가 판단 학습             |
| 비교 사례             | <https://www.harvey.ai/blog/training-a-legal-agent-with-applied-compute>                     | 법률 에이전트 강화학습                   |
| 비교 사례             | <https://www.intercom.com/blog/announcing-fin-apex-the-age-of-vertical-models-is-here/>      | 고객지원 특화 모델                       |

모든 출처의 접근일은 2026-07-30입니다. [translation.ko.md](translation.ko.md)는 저작권이 있는 영문 원문을 그대로 복제하지 않고, 원문의 Part I~VI와 부록 구조를 따른 한국어 번역 요약입니다.

이 자료는 기사에서 보고한 결과를 독립 재현한 것이 아닙니다. 기사, 공개 모델 metadata와 연결된 1차 자료를 대조해 주장·확인 사실·추가 검증 필요 사항을 분리합니다.

## 한눈에 보기

글의 핵심 주장은 다음과 같습니다.

> 반복 횟수가 많고 결과를 객관적으로 채점할 수 있는 회사 고유 업무라면, 범용 프런티어 모델을 매번 호출하는 것보다 작은 공개 가중치 모델을 업무 환경에서 후학습해 운영하는 편이 품질과 비용 모두에서 유리할 수 있다.

제안하는 흐름은 “프런티어 모델을 버리자”가 아닙니다.

```text
프런티어 모델로 프로토타입
  → 실제 입력·결정·수정 trace 축적
  → 업무를 재현하는 평가 환경과 scorer 구축
  → 공개 가중치 기반 모델 SFT/RL
  → 고정된 holdout에서 비교
  → specialist와 frontier를 역할별 라우팅
  → 운영 drift를 감시하며 재학습
```

가장 큰 자산은 모델 파일 하나가 아니라 다음 네 가지가 함께 움직이는 시스템입니다.

1. 회사가 합법적으로 사용할 수 있는 업무 데이터
2. 올바른 결과를 판별하는 평가 루브릭
3. 실제 도구·정책을 재현한 학습 환경
4. 운영 중 품질·비용·drift를 추적하는 체계

## 기초 개념

### 프런티어 모델

가장 높은 범용 능력을 목표로 대규모 학습된 최신 상용 또는 연구 모델입니다. 폭넓은 업무에 강하지만 회사 내부 분류 체계, 정책 예외와 비용 함수를 처음부터 알고 있지는 않습니다.

### 업무 특화 모델

특정 입력, 도구와 판정 기준에 맞춰 후학습된 모델입니다. 일반 능력 일부를 포기하는 대신 좁은 분포에서 정확도, 지연 시간과 단가를 최적화합니다.

### 공개 가중치와 오픈 소스

가중치를 내려받을 수 있다고 항상 오픈 소스인 것은 아닙니다. 모델 카드, 기반 모델과 파생 가중치 각각의 라이선스, 데이터 이용권, 상업적 사용 제한을 확인해야 합니다.

확인 당시 Qwen3.5-9B 기반 모델은 공개적으로 내려받을 수 있었지만 Fermisense 모델 저장소와 adapter에는 모델 카드와 명시적 라이선스 metadata가 없었습니다. 기반 Qwen 모델의 Apache-2.0 표기만으로 파생 artifact의 이용 조건을 임의로 확정하면 안 됩니다.

### SFT와 강화학습

- SFT(Supervised Fine-Tuning): 정답 예시를 모방하도록 학습합니다.
- RL(Reinforcement Learning): 모델이 환경에서 행동하고 scorer가 준 reward를 최대화하도록 학습합니다.
- GRPO(Group Relative Policy Optimization): 여러 생성 결과의 상대적인 reward를 이용해 정책을 갱신하는 강화학습 계열 방법입니다.

### 디지털 트윈

실제 업무의 입력, 도구, 상태 전이와 결과 채점을 모사한 환경입니다. 현실과 충분히 닮아야 하지만 민감 데이터, 부작용과 비용을 통제할 수 있어야 합니다.

## 핵심 요약

### 원문이 제시한 성공 조건

1. 단일 task가 아니라 전체 workflow를 재설계합니다.
2. 실험과 실패 공유에 보상을 줍니다.
3. 회사 고유 context를 모델과 도구에 안전하게 제공합니다.
4. 사용량이 아니라 실제 업무 성과를 측정합니다.
5. AI 예산 안에서 명확한 사업 목표와 단위 경제성을 정합니다.

### 적합한 업무

- 하루 수천~수백만 번 반복됩니다.
- 결과를 규칙, 테스트, schema 또는 전문가 합의로 채점할 수 있습니다.
- 일반 모델이 일부 성공하지만 일관성이 부족합니다.
- 여러 tool call 뒤 하나의 결정으로 끝납니다.
- 오탐과 미탐의 비용이 다릅니다.
- 내부 데이터가 외부 API로 나가면 안 됩니다.

### 부적합하거나 신중해야 할 업무

- 발생 빈도가 낮아 학습·운영 고정비를 회수하기 어렵습니다.
- 정답보다 의견과 논쟁이 중심입니다.
- 정책과 환경이 너무 자주 바뀌어 가중치가 빠르게 낡습니다.
- 데이터 권리나 모델 라이선스가 불명확합니다.
- 실패 비용이 크지만 독립적인 human review와 rollback이 없습니다.

## 사례 연구 수치

다음은 원문 저자가 보고한 catalog integrity 실험 결과입니다.

| 항목                        | 기사 보고값                                                        |
| --------------------------- | ------------------------------------------------------------------ |
| 기반 모델                   | Qwen3.5-9B 계열 9B multimodal model                                |
| 후학습                      | GRPO, 공개 adapter는 LoRA `r=32`, `alpha=64`                       |
| 디지털 트윈 episode         | 177,767개                                                          |
| 분류 체계                   | 약 13,000 category                                                 |
| 평가 표본                   | stratified validation episode 200개                                |
| 오류 비용                   | 실제 위반 미탐을 false alarm보다 7배 강하게 벌점                   |
| base 9B                     | 최대 가능 score의 64.2%                                            |
| best frontier configuration | 76.9%                                                              |
| 후학습 9B                   | 87.3%, strict harness reward 0.626                                 |
| 학습 monitor reward         | step 1,000에서 약 0.671                                            |
| 학습 자원                   | RTX PRO 6000 GPU 2대                                               |
| 학습 시간·비용              | 약 3.5일, GPU 비용 약 $500                                         |
| specialist 추론 비용        | listing 1,000개당 약 $0.50                                         |
| 비교 비용                   | 가장 저렴한 frontier 약 $19, 강한 구성 $34, 가장 비싼 구성 $172/1k |

비용 배수는 어떤 비교 대상을 쓰는지에 따라 달라집니다.

- `$19 ÷ $0.50 = 38×`: 기사에서는 약 40배로 표현합니다.
- `$34 ÷ $0.50 = 68×`: “강한 frontier”와의 비교입니다.
- `$172 ÷ $0.50 = 344×`: 기사에서는 약 340배로 표현합니다.

40M decision/day를 `$34/1k`와 `$0.50/1k`로 연환산하면 각각 약 `$496.4M`과 `$7.3M`입니다. 이는 특정 가격과 트래픽을 그대로 유지한다는 시나리오 계산이며 실제 TCO가 아닙니다.

## 상세 정리

### 1. 왜 prompt와 retrieval만으로 부족할 수 있는가

prompt와 retrieval은 변경되는 사실을 주입하는 데 적합합니다. 그러나 회사의 암묵적 판단, 예외 처리와 비대칭 비용까지 매 요청의 context에 넣으면 token 비용과 관리 복잡도가 커집니다. 특화 모델은 반복되는 판단 규칙 일부를 weights에 압축하려는 접근입니다.

그렇다고 모든 지식을 weights에 넣어서는 안 됩니다.

| 정보 종류                       | 우선 위치                        |
| ------------------------------- | -------------------------------- |
| 자주 바뀌는 가격·재고·정책 원문 | database, search, retrieval tool |
| 안정된 분류 습관·판단 절차      | 후학습 후보                      |
| 사용자별 권한                   | 인증·인가 시스템                 |
| 감사가 필요한 근거              | 원문 evidence와 decision log     |

### 2. scorer가 제품 요구 사항이 되는 이유

모델은 reward로 정의한 것을 최적화합니다. “정확도” 하나로 끝내면 중요한 정책 위반을 놓치거나 불필요한 차단을 남발할 수 있습니다. 원문은 미탐 벌점을 false alarm보다 7배 크게 둬 사업 위험의 비대칭을 표현했습니다.

좋은 scorer는 다음을 분리합니다.

- 최종 판정 정확성
- category와 attribute schema 준수
- 근거 없는 값 생성
- 불필요한 tool call과 비용
- human escalation의 적절성
- 안전·정책 위반

### 3. specialist와 frontier의 혼합

모든 요청을 한 모델에 보내기보다 router를 둘 수 있습니다.

```text
입력
  → 업무 범위·신뢰도 판정
     ├─ 고빈도·검증 가능·안정 분포 → specialist
     ├─ 새로운 유형·낮은 신뢰도   → frontier
     └─ 고위험·검증 불가           → human review
```

frontier는 새 유형 탐색, teacher trace 생성과 예외 처리에 유용하고 specialist는 안정된 대량 흐름을 담당합니다.

### 4. intelligence ownership의 실제 범위

“소유”를 법적·기술적으로 나눠야 합니다.

- weights를 자체 인프라에서 실행할 수 있는가?
- 기반 모델과 adapter 라이선스가 상업적 사용을 허용하는가?
- 학습 데이터와 expert label에 적법한 이용권이 있는가?
- training code, evaluation과 environment를 재현할 수 있는가?
- 특정 GPU, cloud, inference engine에 종속되지 않는가?
- 모델의 결정을 감사하고 이전 version으로 rollback할 수 있는가?

이 조건이 충족되지 않으면 “vendor API를 호출하지 않는다”는 사실만으로 완전한 소유라고 보기 어렵습니다.

## 비판적으로 읽기

### 1. 판매자 작성 사례 연구

원문은 Fermisense가 자사 방법론과 상담 서비스를 설명하는 글입니다. 논문 peer review나 독립 benchmark가 아니며, 결과와 비용은 독립 재현 전까지 저자 보고값으로 다뤄야 합니다.

### 2. 공개 재현 정보의 부족

공개 model과 adapter는 확인되지만 다음 정보가 충분하지 않습니다.

- 전체 training dataset과 split
- 200개 validation episode의 원본과 stratification
- scorer 구현과 achievable ceiling 계산
- frontier별 정확한 model snapshot, 가격 시점과 decoding 설정
- random seed별 평균·분산
- prompt optimization 과정의 holdout 오염 방지
- end-to-end latency, GPU utilization과 serving stack
- 인건비, labeling, evaluation과 재학습을 포함한 TCO

### 3. 작은 평가 표본과 불확실성

평가가 200 episode라면 표본 변동을 무시하면 안 됩니다. 또한 보고된 값은 단순 accuracy가 아니라 가중 reward를 최대 가능 score로 정규화한 수치이므로 일반적인 이항 신뢰구간을 그대로 적용할 수 없습니다. episode-level score와 bootstrap 결과가 있어야 차이를 더 정확히 해석할 수 있습니다.

### 4. reward hacking과 sim-to-real gap

모델은 현실 업무가 아니라 scorer를 공략할 수 있습니다. 디지털 트윈에서 높은 reward를 얻어도 실제 상품 분포, 새로운 사기 패턴과 도구 장애에서는 성능이 떨어질 수 있습니다.

필요한 방어:

- 숨겨진 holdout과 adversarial case
- 시간 순서 기반 test split
- 여러 scorer와 human audit
- shadow deployment와 canary
- out-of-distribution 감지
- 정기적인 policy·taxonomy drift 평가

### 5. 비용 비교의 분모

기사 안에서도 40배, 68배, 340배가 각각 다른 frontier 가격을 분모로 사용합니다. 훈련비 `$500`은 GPU rental만을 뜻하며 데이터 준비, expert labeling, engineering, evaluation, serving redundancy와 운영 인력은 포함하지 않은 것으로 읽어야 합니다.

## 도입 의사결정 프레임워크

### 1단계: task를 명세한다

- 입력과 출력 schema
- 사용할 tool
- 완료 조건
- 실패 종류와 비용
- human escalation 조건

### 2단계: frontier baseline을 만든다

동일한 holdout, tool, turn budget과 scorer로 최소 세 구성을 비교합니다.

1. 단순 prompt
2. 최적화 prompt + retrieval
3. frontier + human fallback

### 3단계: 학습 가능성을 확인한다

- 충분한 episode와 label이 있는가?
- expert 간 합의율이 높은가?
- reward가 실제 사업 목표와 연결되는가?
- train/eval leakage를 막을 수 있는가?

### 4단계: 총소유비용을 계산한다

```text
TCO =
  데이터 준비 + 라벨링 + 학습 GPU + 개발 인력
  + 추론 GPU/API + 평가 + 모니터링 + 재학습
  + 장애·오류·human review 비용
```

### 5단계: 단계적으로 배포한다

```text
offline eval → shadow → low-risk canary → 제한적 자동화 → 확대
```

각 단계에는 품질·비용·latency·안전 rollback gate가 있어야 합니다.

## 용어 정리

| 용어             | 설명                                                                          |
| ---------------- | ----------------------------------------------------------------------------- |
| frontier model   | 높은 범용 능력을 목표로 한 최신 대규모 모델                                   |
| specialist model | 특정 업무 분포에 맞춰 후학습된 모델                                           |
| open-weight      | 가중치를 받을 수 있지만 라이선스·코드·데이터가 모두 공개됐다는 뜻은 아닌 상태 |
| LoRA             | 작은 저랭크 adapter만 학습해 메모리와 저장 비용을 줄이는 PEFT 방법            |
| GRPO             | 그룹 내 생성 결과의 상대 reward로 policy를 학습하는 강화학습 방법             |
| rollout          | 현재 policy가 환경에서 만든 행동·응답 trajectory                              |
| rubric           | 결과를 항목별로 평가하는 명시적 채점 기준                                     |
| scorer           | 출력과 행동을 받아 reward 또는 평가 지표를 계산하는 코드                      |
| digital twin     | 실제 업무 흐름을 안전하게 모사한 학습·평가 환경                               |
| reward hacking   | 실제 목적보다 scorer의 허점을 이용해 높은 reward를 얻는 현상                  |
| sim-to-real gap  | 모의 환경 성능과 실제 운영 성능 사이의 차이                                   |
| TCO              | 초기 구축부터 운영·재학습·오류까지 포함한 총소유비용                          |

## 실습 학습 가이드

모든 노트북은 Python 표준 라이브러리만 사용하며 9B 모델이나 GPU가 필요하지 않습니다.

| 순서 | 파일                                         | 학습 목표                                   |
| ---- | -------------------------------------------- | ------------------------------------------- |
| 1    | [01_foundations.ipynb](01_foundations.ipynb) | 기사 score·비용 배수를 검산하고 분모를 구분 |
| 2    | [02_practice.ipynb](02_practice.ipynb)       | 비대칭 오류 비용이 있는 catalog scorer 설계 |
| 3    | [03_advanced.ipynb](03_advanced.ipynb)       | TCO, break-even, Pareto와 도입 적합성 분석  |

노트북의 데이터는 기사 수치 또는 명시적으로 표시한 toy data입니다. 원문 실험을 재현했다고 주장하지 않습니다.

## 다음 학습 경로

1. 실제 업무 decision 100~500개를 익명화해 evaluation set을 만듭니다.
2. expert 두 명 이상이 독립 labeling하고 합의율을 측정합니다.
3. prompt baseline과 retrieval baseline을 고정합니다.
4. scorer를 코드 리뷰하고 adversarial test를 추가합니다.
5. 작은 공개 가중치 모델에 SFT를 먼저 적용합니다.
6. SFT가 포화되고 reward가 신뢰 가능할 때만 RL을 검토합니다.
7. model card, data card, evaluation report와 rollback 절차를 함께 운영합니다.
