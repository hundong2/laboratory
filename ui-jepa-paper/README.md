# UI-JEPA 논문 분석과 UI 의도 추론 실습

작성일: 2026-08-03

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [핵심 요약](#핵심-요약)
- [상세 정리](#상세-정리)
- [실험 결과 읽기](#실험-결과-읽기)
- [한계와 재현 주의점](#한계와-재현-주의점)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 원문: [UI-JEPA: Towards Active Perception of User Intent through Onscreen User Activity](https://arxiv.org/abs/2409.04081v3)
- 저자: Yicheng Fu, Raviteja Anantha, Prabal Vashisht, Jianpeng Cheng, Etai Littwin
- 식별자: arXiv:2409.04081, DOI: 10.48550/arXiv.2409.04081
- 버전: v3, 2024-10-02, 16쪽
- 원문 언어: 영어
- 접근일: 2026-08-03
- 라이선스: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- 확인 범위: arXiv metadata, HTML full text, 공식 PDF 본문·그림·표·부록

번역과 section별 해설은 [논문 번역 파일](UI-JEPA%20-%20Towards%20Active%20Perception%20of%20User%20Intent%20through%20Onscreen%20User%20Activity.번역.md)에서 볼 수 있습니다. 원 저자를 표시하고 번역·요약·표 재구성과 실습을 추가한 2차 자료이며, 원 저자의 보증을 뜻하지 않습니다.

## 한눈에 보기

UI-JEPA는 스마트폰 화면 활동 video를 보고 사용자의 의도를 text로 요약합니다. 핵심은 거대한 MLLM 하나에 모든 일을 맡기지 않고 다음 두 단계를 분리하는 것입니다.

```text
unlabeled UI video
  -> JEPA tuning: 가린 frame·patch의 feature 예측
  -> UI 전용 video encoder

labeled UI video + optional OCR
  -> frozen video encoder -> dense projection
  -> Phi-3 decoder의 LoRA adapter 학습
  -> intent text
```

JEPA 단계는 label 없는 UI video로 시간적 표현을 적응시키고, 언어 단계는 적은 video-text pair로 그 표현을 의도 문장에 연결합니다. 화면에는 고정 방향, 작은 글자, 갑작스러운 화면 전환이 있으므로 일반 자연 video의 augmentation과 masking을 그대로 쓰지 않는다는 점이 핵심 설계 선택입니다.

## 기초 개념

### 사용자 의도와 UI action sequence

한 장의 screenshot은 현재 상태만 보여 줍니다. 반면 앱 열기, 검색, 항목 선택, 결제처럼 이어지는 frame은 사용자가 무엇을 하려는지 보여 줍니다. UI-JEPA는 16개 frame을 전체 video 길이에 걸쳐 균등 sampling해 이 순서를 압축합니다.

### JEPA와 feature prediction

JEPA(Joint Embedding Predictive Architecture)는 pixel을 복원하는 대신 가려진 부분의 target embedding을 예측합니다. UI-JEPA에서는 context encoder인 x-encoder, EMA로 갱신되는 y-encoder, predictor가 사용됩니다. 의미와 무관한 pixel 세부보다 화면 전환의 추상적 관계를 학습하려는 선택입니다.

### Temporal masking

V-JEPA의 spatial multi-block mask에 더해 frame 전체를 가립니다. 한 token tubelet이 실제 두 frame을 포괄하므로 논문의 temporal masking에서 말하는 한 “frame”은 2-frame hyper-frame입니다. discrete masking 6개가 두 split에서 가장 좋은 결과를 보였습니다.

### LoRA와 hybrid embedding

384x384의 16 frame을 16x16 patch, tubelet 2로 token화한 video embedding을 dense layer로 LM 차원에 투영합니다. 약 3B급 Phi-3의 전체 weight 대신 LoRA adapter와 projection을 학습합니다. 논문 표의 전체 model 표기는 video encoder를 포함해 4.4B입니다.

## 핵심 요약

1. UI-JEPA는 JEPA-tuned ViT와 decoder-only Phi-3를 결합한 video-to-text 모델입니다.
2. IIW(Intent in the Wild)는 열린 의도와 noise를, IIT(Intent in the Tame)는 10개 구조화된 의도를 다룹니다.
3. IIW few-shot Intent Similarity는 UI-JEPA 384가 64.50으로 GPT-4 Turbo 63.36과 비슷하고 Claude 3.5 Sonnet 64.76에 근접합니다.
4. IIT few-shot에서 OCR을 붙인 UI-JEPA는 Intent Similarity 82.03으로 비교군 중 가장 높지만, IIT zero-shot에서는 34.99로 Claude 56.82보다 크게 낮습니다.
5. crop·flip과 video embedding에 추가 position ID를 넣는 것은 대체로 성능을 낮췄습니다.
6. 저자 보고상 IIW에서 계산 비용은 50.5배 낮고 latency는 6.6배 개선됩니다. 다만 폐쇄형 모델의 구조·규모는 추정이며 deployment 조건이 완전히 동등하지 않습니다.

## 상세 정리

### 1. 연구 질문과 기여

연구 질문은 “label이 적을 때도 UI video의 시간 정보를 이용해 가볍고 private한 의도 인식기를 만들 수 있는가?”입니다. 논문은 UI-JEPA framework, IIW·IIT dataset, few/zero-shot baseline, UI 특화 temporal masking을 기여로 제시합니다.

PDF에는 ACM template의 2018·placeholder DOI 문구가 남아 있습니다. 이는 실제 venue 정보가 아니므로 이 자료는 검증 가능한 arXiv preprint로만 기록합니다.

### 2. 두 단계 학습

**JEPA tuning**에서는 pretrained ViT를 UI video에 적응시킵니다. x-encoder에는 unmasked token만 넣고 y-encoder는 전체 video에서 target token을 만듭니다. predictor는 context feature와 위치가 붙은 mask token을 받아 target feature를 예측합니다. y-encoder는 x-encoder의 EMA이며 gradient로 직접 갱신하지 않습니다.

**LM fine-tuning**에서는 x-encoder를 고정합니다. video embedding을 dense projection한 뒤 text embedding과 연결하고, Phi-3의 LoRA adapter를 학습합니다. loss는 video prefix가 아닌 intent text 부분에만 적용됩니다. OCR을 쓸 때 video, OCR text, intent 사이에 separator를 둡니다.

### 3. UI 특화 data strategy

- 16개 frame을 처음부터 끝까지 균등 sampling하는 flexible stride를 사용합니다.
- 16 frame 미만 video는 JEPA tuning과 fine-tuning에서 제외합니다.
- 화면 방향과 상·하단 알림 같은 정보가 깨질 수 있어 augmentation을 사용하지 않습니다.
- short-range 8 block(공간 비율 0.15), long-range 2 block(0.7)에 temporal block(공간 1.0, 시간 0.75)을 추가합니다.
- video embedding 자체에 3D 위치 정보가 있으므로 LM 앞에서 추가 position ID를 붙이지 않습니다.

### 4. Dataset

| Dataset | 성격 | train | few-shot eval | zero-shot eval | 범주 |
|---|---|---:|---:|---:|---:|
| IIW | 수동 기록, 열린·비어휘화 의도 | 1,274 | 344 | 87 | 219 |
| IIT | iOS macro graph로 생성, 어휘화 의도 | 682 | 187 | 45 | 10 |

IIW 표의 합은 1,705로 초록의 1.7K와 맞습니다. 본문에는 1.6K 및 평균 749 frame, Table 2에는 평균 723 frame으로 표기가 엇갈립니다. IIT은 914개로 일치합니다. 재현 시 dataset release와 split manifest를 기준으로 재확인해야 합니다.

### 5. 평가 지표

- **SBERT cosine similarity:** 문장 의미 embedding의 cosine 유사도
- **ROUGE-1/2/L:** unigram, bigram, 최장 공통 subsequence 기반 겹침
- **Intent Similarity:** 정규화한 위 네 점수의 단순 평균

Intent Similarity는 이 논문이 정의한 복합 지표입니다. 문장 품질, factual correctness, 행동 완료 여부를 사람이 직접 평가한 지표는 아니며, 비어휘화된 IIW와 구체적 entity가 필요한 IIT의 난이도도 다릅니다.

## 실험 결과 읽기

### IIW

| Split | Model | Intent Similarity |
|---|---|---:|
| few-shot | UI-JEPA 384 + Phi | 64.50 |
| few-shot | Claude 3.5 Sonnet | 64.76 |
| few-shot | GPT-4 Turbo | 63.36 |
| zero-shot | UI-JEPA 384 + Phi | 52.16 |
| zero-shot | Claude 3.5 Sonnet | 60.35 |
| zero-shot | GPT-4 Turbo | 58.24 |

“대형 MLLM보다 우수”라는 초록의 평균 개선 주장은 dataset·split을 합친 저자 집계입니다. IIW zero-shot만 보면 UI-JEPA가 두 폐쇄형 모델보다 낮으므로 split별 표를 함께 봐야 합니다.

### IIT와 OCR

| Split | OCR | Model | Intent Similarity |
|---|---|---|---:|
| few-shot | 없음 | UI-JEPA | 71.55 |
| few-shot | 있음 | UI-JEPA | 82.03 |
| zero-shot | 없음 | UI-JEPA | 38.13 |
| zero-shot | 있음 | UI-JEPA | 34.99 |

OCR은 IIT few-shot에는 크게 도움을 주지만 zero-shot에는 오히려 악화됩니다. 저자는 UI-JEPA의 OCR 단계가 latency를 13.5% 늘리고 성능을 14.4% 높인다고 보고하지만, 이는 유리한 few-shot 조건의 trade-off로 읽어야 합니다.

### Ablation

- flip은 few-shot에서 +0.42%이지만 zero-shot에서 -3.69%로 저하됩니다.
- crop과 flip+crop은 대체로 성능을 낮춥니다.
- video embedding 추가 position ID는 few-shot 63.52 -> 61.84, zero-shot 52.16 -> 50.15로 낮춥니다.
- unlabeled JEPA-tuning data를 25%에서 100%로 늘리면 특히 full data에서 개선됩니다.
- short + long + temporal mask가 가장 좋고, discrete hyper-frame 6개 mask가 선택됩니다.

## 한계와 재현 주의점

- IIT zero-shot sample은 45개뿐이라 분산과 category별 편차를 함께 보고해야 합니다.
- UI-JEPA는 낯선 앱 zero-shot에서 대형 MLLM보다 크게 뒤집니다.
- 세밀한 text·entity는 JEPA embedding만으로 부족하고 OCR 품질에 의존합니다.
- random initialization에서 JEPA tuning한 encoder는 좋지 않아 대규모 video pretraining이 선행되어야 합니다.
- audio modality는 평가하지 않았습니다.
- IIW/IIT 공개 상태와 정확한 split manifest는 논문 작성 당시 “곧 공개”로 표현되어 있어 실제 재현 전 확인이 필요합니다.
- Claude는 입력 크기 제한 시 16장 중 홀수 frame 8장만 사용했고, privacy 등의 이유로 응답하지 않은 사례를 저자가 metric에서 수동 제외했습니다. 따라서 완전히 동일한 입력·실패 처리 비교가 아닙니다.
- GPT-4 Turbo 880B, Claude >70B는 공개 정보에 기반한 추정치이며 공식 parameter count가 아닙니다.
- Table 9의 predictor embedding dimension 12는 V-JEPA 관행과 비교하면 비정상적으로 작아 오기 가능성이 있습니다. 원문 그대로 기록하되 구현 전 code/config 확인이 필요합니다.
- A100 80GB, bfloat16, batch 4(언어 fine-tuning은 1)라는 설정은 “모바일에서 학습”이 아니라 경량 inference 지향입니다.

## 용어 정리

| 용어 | 뜻 |
|---|---|
| UI-JEPA | UI video를 JEPA objective로 적응시킨 encoder와 LM decoder의 결합 |
| IIW | Intent in the Wild, 열린 UI 의도 dataset |
| IIT | Intent in the Tame, 10개 구조화 의도 dataset |
| MLLM | Multimodal Large Language Model, 여러 modality를 처리하는 대형 언어 모델 |
| EMA | Exponential Moving Average, target encoder를 천천히 갱신하는 방식 |
| LoRA | Low-Rank Adaptation, 적은 추가 parameter로 LM을 미세조정하는 방법 |
| OCR | Optical Character Recognition, 화면 text 추출 |
| delexicalized intent | 이름·시간 같은 구체 entity를 제거한 고수준 의도 |
| zero-shot | 학습에서 보지 못한 category·app에 대한 평가 |

## 실습 학습 가이드

- [`01_foundations.ipynb`](01_foundations.ipynb): 16-frame sampling과 spatial/temporal mask를 구현합니다.
- [`02_practice.ipynb`](02_practice.ipynb): video·OCR·text hybrid sequence와 text-only loss mask를 구성합니다.
- [`03_advanced.ipynb`](03_advanced.ipynb): Intent Similarity 계산, split별 결과와 비용·latency 주장을 비판적으로 분석합니다.

세 notebook은 외부 package 없이 실행되는 toy reproduction입니다. 실제 ViT·Phi-3 학습이나 원 논문 성능 재현을 주장하지 않습니다.

## 다음 학습 경로

1. [V-JEPA 논문 분석](../v-jepa-paper/README.md)에서 원래 video feature prediction을 익힙니다.
2. [I-JEPA 논문 분석](../i-jepa-paper/README.md)에서 joint embedding의 image 기반 원리를 복습합니다.
3. 실제 실험에서는 privacy-safe UI video, OCR redaction, app 단위 split을 먼저 설계합니다.
4. category별 bootstrap confidence interval과 사람 평가를 추가해 작은 zero-shot split을 보완합니다.
5. 동일 hardware, 동일 frame 수, 동일 실패 처리로 on-device latency와 energy를 다시 측정합니다.
