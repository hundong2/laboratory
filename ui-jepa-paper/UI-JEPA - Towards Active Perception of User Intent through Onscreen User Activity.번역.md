# UI-JEPA - Towards Active Perception of User Intent through Onscreen User Activity - 번역·해설

## 논문 metadata

| 항목 | 내용 |
|---|---|
| 원문 제목 | UI-JEPA: Towards Active Perception of User Intent through Onscreen User Activity |
| 저자 | Yicheng Fu, Raviteja Anantha, Prabal Vashisht, Jianpeng Cheng, Etai Littwin |
| 출판 정보 | arXiv preprint, 2024 |
| 식별자 | arXiv:2409.04081, DOI: 10.48550/arXiv.2409.04081 |
| 원문 | [arXiv v3](https://arxiv.org/abs/2409.04081v3) |
| 사용 버전 | v3, 2024-10-02, 16쪽 |
| 원문 언어 | 영어 |
| 접근일 | 2026-08-03 |
| 라이선스 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

## 저작자 표시와 변경 사항

이 파일은 위 저자들의 원 논문을 한국어 학습용으로 번역·요약·재구성한 자료입니다. 짧은 문장 대조, section별 해설, 용어 설명, 표 해석과 비판적 검토를 추가했습니다. 원 저자나 소속 기관이 이 번역을 보증한다는 의미는 아닙니다.

## 번역·접근 범위

| 원문 범위 | 상태 | 처리 |
|---|---|---|
| 제목·Abstract | 부분 번역 | 짧은 문장 대조와 전체 해설 |
| 1. Introduction | 완료 | 주장·기여 요약 |
| 2. Related Work | 완료 | 연구 흐름별 해설 |
| 3. UI-JEPA Framework | 완료 | 구조·학습·data strategy 해설 |
| 4. Benchmarks | 완료 | IIW·IIT 구성과 표기 불일치 설명 |
| 5. Baselines | 완료 | 평가 지표와 비교 조건 설명 |
| 6. Results | 완료 | main result·ablation 해설 |
| 7. Conclusion and Applications | 완료 | 주장과 응용 요약 |
| 8. Limitations | 완료 | 저자 한계와 추가 비판 |
| Appendix A~C | 완료 | 전처리·학습·LoRA·prompt 해설 |
| References | 해당 없음 | bibliographic record는 원문 참조 |

원문은 CC BY 4.0이지만 이 자료는 원문 전문 복제 대신 학습에 필요한 한 문장만 대조하고 나머지를 상세 한국어 해설로 제공합니다.

## 읽기 전 핵심 배경

- **UI understanding:** 화면 구성 요소뿐 아니라 행동 순서와 task 의미를 이해하는 문제
- **JEPA:** 관측 pixel이 아니라 target encoder의 추상 feature를 예측하는 architecture
- **MLLM:** image·video·text를 함께 처리하는 multimodal large language model
- **few-shot/zero-shot:** 적은 동일 범주 예제가 있는 조건과 해당 범주 예제가 없는 조건
- **intent generation:** 정해진 class 선택이 아니라 자연어로 사용자 목적을 생성하는 task

## 제목 번역

UI-JEPA: 화면상 사용자 활동을 통한 사용자 의도의 능동적 인지를 향하여

## Abstract

**S001 — Original**

Additionally, the lack of high-quality datasets has hindered the development of such lightweight models.

**S001 — 한국어**

(또한 고품질 dataset의 부족은 이러한 경량 모델의 발전을 가로막아 왔다.)

- **용어·약어 해설**
  - **lightweight model(경량 모델):** 여기서는 약 3B급 LM과 video encoder를 결합해 on-device inference를 지향하는 모델입니다.
  - **dataset:** UI action video와 사용자 의도 text가 짝지어진 자료는 수집·annotation 비용과 privacy 문제가 큽니다.

### 초록 전체 해설

UI action sequence에서 의도를 생성하는 기존 MLLM은 크기, compute, latency, privacy 면에서 on-device 사용이 어렵습니다. 저자들은 label 없는 UI video에 masking 기반 self-supervised learning을 적용한 UI-JEPA encoder와, intent prediction용으로 LoRA fine-tuning한 LM decoder를 결합합니다.

IIW는 약 1.7K video와 219 category, IIT은 914 video와 10 category로 구성됩니다. 저자는 두 dataset 평균 Intent Similarity에서 GPT-4 Turbo보다 10.0%, Claude 3.5 Sonnet보다 7.2% 높고, IIW에서 계산 비용 50.5배 감소와 latency 6.6배 개선을 보고합니다. 그러나 개별 zero-shot 표에서는 폐쇄형 모델보다 낮으므로 평균 주장만 떼어 읽으면 안 됩니다.

## 1. Introduction 해설

스마트 기기의 UI는 사람과 application 또는 dialogue agent가 만나는 핵심 표면입니다. 행동과 의도를 추정하면 assistant 실행의 성공 여부를 feedback으로 만들거나, 여러 앱에 걸친 Multimodal Intent State Tracking(MIST)을 구성할 수 있습니다.

UI는 image, text, 구조 metadata와 시간 관계가 함께 필요합니다. 거대한 server-side MLLM 대신 privacy와 latency에 유리한 on-device model을 목표로 하며, 고품질 paired label이 적다는 문제를 JEPA self-supervision으로 보완합니다.

논문의 기여는 IIW·IIT benchmark, UI용 masking strategy, JEPA encoder와 autoregressive LM head의 결합, 폐쇄형 MLLM과의 비교입니다. dataset 공개는 본문에서 “곧 공개”로 적혀 있어 논문만으로 완전 재현 가능한 상태라고 단정할 수 없습니다.

## 2. Related Work 해설

기존 UI model은 component detection이나 static screenshot 이해에 집중해 task 전체의 temporal meaning을 놓치기 쉽습니다. MLLM은 더 풍부하지만 server cost와 privacy 문제가 있습니다. VideoMAE는 masked pixel reconstruction을, I-JEPA와 V-JEPA는 masked embedding prediction을 사용합니다.

UI-JEPA의 차이는 V-JEPA encoder를 UI domain에 맞게 추가 tuning하고, 화면 전체 frame을 가리는 temporal mask를 더하며, dense projection과 LoRA를 통해 intent text를 생성한다는 점입니다.

## 3. The UI-JEPA Framework 해설

### 3.1 Network Parameterization

video 전체에서 16 frame을 균등 sampling하고 384x384로 resize합니다. patch는 16x16, tubelet은 2 frame이므로 한 token은 작은 시공간 cube입니다. ViT video embedding은 dense layer를 거쳐 약 3B parameter Phi-3의 input space로 이동합니다.

LM은 video와 text embedding을 함께 받되 추가 positional embedding은 text input에만 사용합니다. video token은 encoder에서 이미 3D spatial-temporal position을 반영한다는 가정입니다.

### 3.2 Training

첫 단계는 label 없는 UI video의 JEPA tuning입니다. x-encoder에는 context token만 남기고 y-encoder는 target embedding을 만듭니다. predictor는 context embedding과 위치를 포함한 mask token을 사용해 가려진 target을 예측합니다. y-encoder는 x-encoder의 EMA copy입니다.

둘째 단계는 labeled video-intent pair의 LM fine-tuning입니다. x-encoder는 freeze하고 dense projection과 LM의 LoRA adapter를 갱신합니다. output loss는 video prefix를 제외한 text 부분에만 적용합니다.

### 3.3 UI-JEPA Data Strategy

자연 video에서 흔한 random crop과 flip은 UI의 고정 방향, 알림 위치, 작은 text를 손상할 수 있으므로 제거합니다. short·long spatial block에 전체 화면을 시간축 일부에서 가리는 temporal mask를 더해 app 전환 같은 큰 상태 변화를 학습합니다.

### 3.4 Embedding Visualization

IIW 상위 10개 app type의 t-SNE와 silhouette score를 비교합니다. UI-JEPA silhouette은 0.0212로 random -0.1230, VideoMAE 0.0081, V-JEPA 0.0094보다 높습니다. video pair cosine similarity와 intent text pair similarity의 Pearson correlation도 UI-JEPA 0.1267로 가장 높지만 Spearman은 V-JEPA 0.0435가 UI-JEPA 0.0427보다 근소하게 높습니다.

t-SNE 그림은 정성 근거이고 값 자체가 작으므로 강한 semantic alignment의 증명으로 과해석하지 않아야 합니다.

## 4. The UI-JEPA Benchmarks 해설

### 4.1 Intent in the Wild

IIW는 수동으로 복잡한 smartphone interaction을 기록하고 high-level delexicalized intent를 붙입니다. few-shot에는 category당 최소 2개가 있고, zero-shot category는 한 번만 등장하며 서로 겹치지 않습니다.

Table 2는 train 1,274, few-shot 344, zero-shot 87로 총 1,705개와 219 category를 제시합니다. 초록의 1.7K와 일치하지만 본문은 1.6K라고 써서 불일치합니다. 평균 frame도 표 723과 본문 749가 다릅니다.

### 4.2 Intent in the Tame

IIT은 iOS macro를 screen state graph의 edge로 보고, LLM이 만든 staging parameter와 random graph traversal로 실행 경로를 생성합니다. 총 914개 video, 10 intent category이며 zero-shot 평가 45개입니다. label은 구체적 이름·시간을 포함하는 lexicalized intent이고 마지막 frame OCR을 선택적으로 제공합니다.

자동 생성은 scale과 완료 보장에 유리하지만 app·macro·synthetic entity의 편향을 만들 수 있습니다.

## 5. Baselines와 Metrics 해설

Random, VideoMAE, V-JEPA, UI-JEPA encoder를 같은 Phi 계열 decoder와 결합합니다. 폐쇄형 비교군은 GPT-4 Turbo와 Claude 3.5 Sonnet입니다. 모든 model은 원칙적으로 16 frame을 받지만 Claude 입력 byte limit 초과 시 8장만 사용합니다.

SBERT와 ROUGE-1/2/L을 정규화해 평균한 Intent Similarity를 사용합니다. 이는 lexical overlap과 semantic similarity를 결합하지만 실제 의도의 사실성이나 완료 여부를 직접 측정하지는 않습니다.

## 6. Results 해설

### 6.1 Main Results

IIW few-shot에서 UI-JEPA 384의 Intent Similarity 64.50은 Claude 64.76과 거의 같고 GPT-4 Turbo 63.36보다 높습니다. IIW zero-shot에서는 52.16으로 Claude 60.35와 GPT-4 Turbo 58.24보다 낮습니다.

IIT few-shot에서 OCR 없는 UI-JEPA는 71.55, OCR 포함은 82.03입니다. 반면 IIT zero-shot은 OCR 없음 38.13, 있음 34.99로 폐쇄형 model의 약 53~57보다 크게 낮습니다. familiar app의 적은 label에는 강하지만 unseen app generalization은 약하다는 결론입니다.

저자는 IIW에서 cost 50.5배와 latency 6.6배 차이를 보고합니다. 폐쇄형 model의 parameter count는 추정이고 service·hardware 조건이 다르므로 model architecture만의 인과 효과로 보기는 어렵습니다.

### 6.2 Ablation Studies

augmentation 없이 few/zero-shot Intent Similarity는 63.52/52.16입니다. flip은 63.79/50.24, crop은 62.46/표의 delta와 값 정렬에 불명확성이 있으며, 두 augmentation 결합은 60.68/38.02로 악화됩니다. HTML 표 일부의 zero-shot Intent Similarity와 delta가 원 metric 평균과 맞지 않아 PDF 원표를 그대로 인용하되 재계산 검증이 필요합니다.

추가 position ID는 63.52에서 61.84, 52.16에서 50.15로 낮춥니다. unlabeled data를 늘리면 few-shot은 꾸준히 개선되고 zero-shot은 100%에서 뚜렷이 개선됩니다. short + long + temporal masking이 가장 좋으며, contiguous와 discrete를 비교한 결과 discrete hyper-frame 6개 mask를 선택합니다.

## 7. Conclusion and Applications 해설

저자는 UI-JEPA를 효율적·privacy-preserving UI understanding 방법으로 정리합니다. 응용으로 assistant 실행 결과를 판별해 학습 data를 정제하는 User Feedback Learning과, 여러 시점의 의도를 memory에 저장해 tool calling에 쓰는 MIST를 제안합니다.

이 응용은 개념 설계이며 실제 production privacy, consent, retention, failure recovery 평가가 완료됐다는 뜻은 아닙니다. 화면에는 credential·message·건강정보가 포함될 수 있으므로 저장 전 redaction과 최소 수집이 필요합니다.

## 8. Limitations 해설

저자가 밝힌 한계는 세밀한 intent에서 OCR 의존, random encoder JEPA tuning 실패와 대규모 pretraining 필요, zero-shot 열세, audio 미평가입니다.

추가로 dataset 크기가 작고 IIT zero-shot은 45개뿐입니다. Claude가 일부 frame만 받거나 privacy refusal 응답을 metric에서 수동 제외한 조건도 비교 공정성을 제한합니다. “on-device”는 목표와 Phi 선택의 근거이지, 논문 표의 A100 학습이나 모든 target device에서 end-to-end deployment를 입증한 표현은 아닙니다.

## Appendix 해설

### A. Dataset Processing

길이가 다양한 UI video에서 처음부터 끝까지 16 frame을 균등 sampling합니다. 16 frame 미만은 제외합니다. 이는 고정 stride보다 전체 task를 포괄하지만 짧고 중요한 전환을 놓칠 수 있습니다.

### B. Training Details

- 해상도 384, frame 16, augmentation 없음
- IIW JEPA/fine-tuning 4,000/6,000 iteration
- IIT JEPA/fine-tuning 2,000/3,000 iteration
- learning rate 3e-4, EMA momentum 0.998 -> 1.0
- weight decay 0.04 -> 0.4, A100 80GB, bfloat16
- LoRA rank 16, alpha 16, dropout 0.05
- target module: qkv_proj, o_proj, gate_up_proj, down_proj
- NF4 double quantization, bfloat16 compute

Table 9는 predictor embedding dimension을 12로 적습니다. 매우 작은 값이라 오기 가능성을 배제할 수 없으며 공개 code/config가 없으면 원문 이상으로 추정하지 않아야 합니다.

### C. Inference

IIW prompt는 구체 text를 제거한 intent와 app type을 요구하고, IIT prompt는 10개 ending activity 예시를 제공합니다. 이 prompt 차이는 dataset label scheme을 반영합니다. Claude는 byte limit 초과 시 8 frame만 사용하고, privacy 등의 사유로 intent를 내지 않은 응답은 수동 제외했으므로 failure도 포함하는 deployment 평가와는 다릅니다.

## 수식·그림·표 읽기 가이드

- **Figure 2:** 위쪽 JEPA tuning과 아래쪽 LM fine-tuning을 분리해서 읽습니다. inference에는 y-encoder와 predictor가 없습니다.
- **Figure 6:** spatial mask는 모든 frame의 같은 영역을, temporal mask는 선택된 hyper-frame 전체 화면을 가립니다.
- **Tables 3~6:** few/zero-shot과 IIW/IIT를 섞어 평균만 보지 않습니다.
- **Figure 8:** mask 종류 추가의 경향을 보여 주지만 error bar가 없어 차이의 통계적 유의성은 알 수 없습니다.
- **Table 9:** 실제 재현 parameter의 출발점이지만 표기 이상과 dataset 공개 상태를 확인해야 합니다.

Intent Similarity의 개념식은 다음과 같습니다.

$$
I = \frac{\hat{s}_{SBERT} + \hat{s}_{R1} + \hat{s}_{R2} + \hat{s}_{RL}}{4}
$$

각 $\hat{s}$는 $[0,1]$로 맞춘 similarity score입니다. 네 성분을 같은 weight로 평균하므로 낮은 ROUGE-2와 높은 SBERT가 상쇄될 수 있습니다.

## 약어 및 기술 용어 사전

| 원어·약어 | 한국어 | 논문에서의 역할 | 최초 등장 |
|---|---|---|---|
| UI | 사용자 인터페이스 | smartphone 화면 활동의 관측 대상 | S001 전 배경 |
| JEPA | 결합 임베딩 예측 아키텍처 | 가려진 UI 영역의 feature 예측 | S001 전 배경 |
| MLLM | 멀티모달 대형 언어 모델 | 정확하지만 큰 비교 대상 | S001 전 배경 |
| IIW | 야생 환경의 의도 | 열린 UI task dataset | Abstract 해설 |
| IIT | 통제 환경의 의도 | 구조화된 10-category dataset | Abstract 해설 |
| EMA | 지수 이동 평균 | y-encoder weight 갱신 | 3.2 |
| LoRA | 저랭크 적응 | Phi-3 decoder 효율적 fine-tuning | 3.2 |
| OCR | 광학 문자 인식 | 세밀한 화면 text 보조 | 4.2 |
| SBERT | Sentence-BERT | intent 의미 유사도 평가 | 5 |
| ROUGE | 요약 겹침 지표 | 생성 intent의 lexical overlap 평가 | 5 |
| MIST | 멀티모달 의도 상태 추적 | 여러 앱·시점의 의도 memory 응용 | 7 |

## 번역 검수 기록

- arXiv v3 metadata와 16쪽 PDF 제목·저자를 대조했습니다.
- PDF pages 3, 7~10, 12, 14의 architecture, 결과표, masking 그림, 한계와 hyperparameter 표를 시각 확인했습니다.
- dataset 수치 불일치, 표 metric 정렬 의심, 추정 parameter 수를 별도 표시했습니다.
- 원문의 가능성 주장과 저자 보고 수치를 확정적 외부 사실로 바꾸지 않았습니다.
- 전문 번역이 아니라 한 문장 대조와 section별 상세 해설임을 범위 표에 표시했습니다.

## 함께 보기

- [분석 README](README.md)
- [V-JEPA 논문 분석](../v-jepa-paper/README.md)
- [I-JEPA 논문 분석](../i-jepa-paper/README.md)
