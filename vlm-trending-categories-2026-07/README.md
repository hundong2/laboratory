# 2026년 7월 중순 VLM 트렌드 카테고리별 학습 자료

작성일: 2026-07-17

## 출처와 작업 범위

확인 기준일: 2026-07-17

이 폴더는 사용자가 제공한 2026년 7월 12일, 13일, 14일, 15일, 16일 기준 VLM 트렌드 업데이트를 중복 제거하고, 논문을 카테고리별 학습 폴더로 재구성한 자료입니다.

작업 원칙은 다음과 같습니다.

- 사용자가 제공한 일별 Top 5 순위는 "피드에서 언급된 트렌드 스냅샷"으로 보존했습니다.
- 공개 출처에서 확인한 제목, arXiv ID, 최초 공개일, 학회/피드 정보를 따로 기록했습니다.
- "업보트 최상위", "학계 찬사", "SOTA" 같은 표현은 시간과 출처에 따라 달라질 수 있어, 검증 가능한 수치나 논문 초록의 주장과 구분했습니다.
- 일부 항목은 2026년 7월 신작이 아니라 2026년 피드에서 재조명된 이전 논문입니다. 예: VLV Auto-Encoder는 arXiv 2025년 7월, Constructive Apraxia는 arXiv 2024년 9월 공개입니다.

## 폴더 구조

```text
vlm-trending-categories-2026-07/
  README.md
  translation.ko.md
  01_foundations.ipynb
  02_practice.ipynb
  03_advanced.ipynb
  01-document-memory-vlm/
    README.md
    01_foundations.ipynb
  02-unified-generative-vision/
    README.md
    01_foundations.ipynb
  03-spatial-robust-vlm/
    README.md
    01_foundations.ipynb
  04-interactive-world-vla/
    README.md
    01_foundations.ipynb
```

## 한눈에 보기

| 카테고리 | 핵심 질문 | 포함 논문 |
|---|---|---|
| 문서/메모리 VLM | 긴 문서와 원본 레이아웃을 어떻게 잃지 않고 읽을 것인가? | Unlimited OCR, Scalable Visual Pretraining, SCoPE VLM |
| 통합 생성형 비전 | 비전 태스크별 헤드를 생성 공간으로 통합할 수 있는가? | SenseNova-Vision, GenCeption, VLV Auto-Encoder |
| 공간/강건성 VLM | 모델이 텍스트 prior에 끌려가지 않고 실제 픽셀, 경계, 센서 신호를 볼 수 있는가? | Dense Spatial Perception, RE-VLM, Constructive Apraxia, Do Images Speak Louder than Words? |
| 인터랙티브 월드/VLA | VLM이 동영상 세계와 로봇 행동 루프 안에서 작동할 수 있는가? | Vidu S1, Infinite Worlds, EmbodiedGen V2, LingBot-VLA 2.0 |

## 중복 제거된 논문 목록

| 카테고리 | 논문 | 확인된 공개 정보 | 출처 |
|---|---|---|---|
| 문서/메모리 | Unlimited OCR Works | arXiv 2606.23050, 2026-06-22 제출 | https://arxiv.org/abs/2606.23050 |
| 문서/메모리 | Scalable Visual Pretraining for Language Intelligence | arXiv 2607.09657, 2026-07-10 제출 | https://arxiv.org/abs/2607.09657 |
| 문서/메모리 | SCoPE VLM: Selective Context Processing for Efficient Document Navigation in VLMs | EACL 2026 long paper, arXiv 2510.21850 | https://aclanthology.org/2026.eacl-long.6/ |
| 통합 생성형 비전 | Vision as Unified Multimodal Generation | arXiv 2607.06560, SenseNova-Vision | https://arxiv.org/abs/2607.06560 |
| 통합 생성형 비전 | Video Generation Models are General-Purpose Vision Learners | arXiv 2607.09024, GenCeption, ECCV 2026 표기 | https://arxiv.org/abs/2607.09024 |
| 통합 생성형 비전 | Vision-Language-Vision Auto-Encoder | arXiv 2507.07104, 2025년 공개 | https://arxiv.org/abs/2507.07104 |
| 공간/강건성 | Vision Pretraining for Dense Spatial Perception | arXiv 2607.05247, LingBot-Vision | https://arxiv.org/abs/2607.05247 |
| 공간/강건성 | RE-VLM: Event-Augmented VLM for Scene Understanding | arXiv 2605.19329, CVPR 2026 OA 확인 | https://arxiv.org/abs/2605.19329 |
| 공간/강건성 | Constructive Apraxia | arXiv 2410.03551, 2024년 공개 | https://arxiv.org/abs/2410.03551 |
| 공간/강건성 | Do Images Speak Louder than Words? | arXiv 2601.19202, EACL 2026 accepted | https://arxiv.org/abs/2601.19202 |
| 인터랙티브 월드/VLA | Vidu S1 | arXiv 2607.03118, Hugging Face #1 Paper of the day 확인 | https://arxiv.org/abs/2607.03118 |
| 인터랙티브 월드/VLA | Infinite Worlds with Versatile Interactions | arXiv 2607.07534, LingBot-World 2.0 | https://arxiv.org/abs/2607.07534 |
| 인터랙티브 월드/VLA | EmbodiedGen V2 | arXiv 2607.07459, 2026-07-08 제출, 2026-07-12 v2 | https://arxiv.org/abs/2607.07459 |
| 인터랙티브 월드/VLA | From Foundation to Application: Improving VLA Models in Practice | arXiv 2607.06403, LingBot-VLA 2.0 | https://arxiv.org/abs/2607.06403 |

## 날짜별 피드에서의 변화

| 날짜 | 반복적으로 등장한 축 | 새로 부각된 항목 |
|---|---|---|
| 2026-07-12 | 비용 효율, 문서 파싱, 신뢰성 | VLV Auto-Encoder, Constructive Apraxia, SCoPE VLM |
| 2026-07-13 | 문서 메모리, VLA, 공간 지능 | EmbodiedGen V2, LingBot-VLA 2.0 |
| 2026-07-14 | 실시간 world model, 생성형 비전 pretraining | GenCeption, Vidu S1 |
| 2026-07-15 | world model, 센서 강건성 | RE-VLM |
| 2026-07-16 | 문서/비주얼 사전학습, 통합 생성 | Scalable Visual Pretraining, SenseNova-Vision |

## 기초 개념

### VLM과 MLLM

VLM은 이미지를 보고 텍스트로 답하거나, 텍스트 지시를 바탕으로 이미지를 해석하는 모델입니다. MLLM은 더 넓게 이미지, 텍스트, 오디오, 비디오, 행동 신호를 함께 다루는 대형 멀티모달 모델을 가리킵니다. 이 자료에서는 문서 이미지, 비디오, 로봇 행동까지 포함해 넓은 의미의 VLM 트렌드로 다룹니다.

### 비주얼 토큰과 KV 캐시

이미지는 패치나 잠재 벡터로 토큰화됩니다. 고해상도 문서나 긴 비디오는 비주얼 토큰 수가 빠르게 커집니다. 디코더가 긴 텍스트를 생성할 때는 이전 token의 key/value를 저장하는 KV 캐시도 계속 커집니다. Unlimited OCR과 SCoPE VLM은 이 비용을 줄이는 대표적 흐름입니다.

### 네이티브 비주얼 사전학습

문서를 OCR 텍스트로 바꾸면 레이아웃, 수식 배치, 표 구조, 도표 관계가 약해집니다. Scalable Visual Pretraining은 원본 시각 문서 자체를 사전학습 데이터로 쓰자는 흐름입니다.

### 통합 멀티모달 생성

SenseNova-Vision과 GenCeption은 여러 비전 태스크를 전용 헤드가 아니라 통합 생성 공간으로 다루려는 흐름입니다. detection, segmentation, depth, pose 같은 출력을 텍스트, 이미지, 혼합 포맷으로 시리얼라이즈합니다.

### 공간 지능과 강건성

Dense Spatial Perception, RE-VLM, Constructive Apraxia, Do Images Speak Louder than Words?는 모두 "모델이 실제 시각 증거를 얼마나 정확히 쓰는가"를 묻습니다. 핵심은 텍스트 prior, RGB 한계, 기하학 추론 실패, 오정보 취약성을 줄이는 것입니다.

### World Model과 VLA

Vidu S1과 Infinite Worlds는 동적 비디오 세계를 생성하고 상호작용하는 방향입니다. EmbodiedGen V2와 LingBot-VLA 2.0은 그 흐름을 로봇 시뮬레이션과 실제 행동 제어로 확장합니다.

## 핵심 요약

1. 문서 VLM은 "더 긴 컨텍스트"만으로 해결되지 않습니다. 출력 캐시, 선택적 읽기, 원본 레이아웃 보존이 함께 필요합니다.
2. 비전 foundation model은 태스크별 헤드에서 텍스트/이미지 생성 공간으로 모이고 있습니다.
3. 공간 지각은 의미 분류보다 어렵습니다. 경계, 깊이, 이벤트 센서, 텍스트 오정보 견제가 중요합니다.
4. VLM은 정적 이미지 QA에서 실시간 비디오와 행동 루프를 다루는 world model/VLA로 확장되고 있습니다.
5. 날짜별 Top 5는 바뀌지만 반복 등장하는 병목은 메모리, 출력 포맷, 공간 신뢰성, 상호작용 지연입니다.

## 실습 학습 가이드

상위 실습 파일은 카테고리 전체를 가로지르는 공통 능력을 다룹니다.

| 파일 | 목적 |
|---|---|
| `01_foundations.ipynb` | 14개 논문을 카테고리 태그와 날짜별 출현 빈도로 정리 |
| `02_practice.ipynb` | KV 캐시, 선택적 문서 읽기, 통합 출력 스키마, 강건성 평가 toy 계산 |
| `03_advanced.ipynb` | 트렌드 업데이트를 입력하면 카테고리와 후속 학습 경로를 추천하는 미니 파이프라인 |

카테고리별 폴더에는 해당 축만 깊게 읽는 README와 작은 실습 노트북이 들어 있습니다.

## 다음 학습 경로

1. 문서/메모리 VLM부터 시작합니다. 문서 파싱은 실무 적용 가능성이 높고, KV 캐시와 선택적 attention 개념을 배우기 좋습니다.
2. 그 다음 통합 생성형 비전을 학습합니다. 출력 스키마 설계와 평가 지표가 중요합니다.
3. 공간/강건성 VLM은 벤치마크를 직접 설계하는 관점으로 읽습니다. "정답을 맞혔는가"보다 "어떤 modality를 근거로 삼았는가"가 중요합니다.
4. 마지막으로 interactive world/VLA를 학습합니다. 비디오 생성, 시뮬레이션, 로봇 행동 정책이 함께 등장하므로 가장 넓은 배경지식이 필요합니다.

## 확인 필요 사항

- Hugging Face upvote와 Paper of the day는 계속 바뀝니다. 이 문서에는 2026-07-17 확인 시점의 공개 페이지에서 확인 가능한 값만 반영했습니다.
- 사용자가 제공한 일부 공개일은 arXiv 제출일과 하루 이상 차이가 있었습니다. 문서에는 arXiv/ACL/CVF 등 공개 출처 기준 날짜를 우선했습니다.
- 이 자료는 학습용 정리입니다. 특정 모델 사용 여부는 각 저장소의 라이선스, 체크포인트 공개 범위, GPU 요구량을 다시 확인해야 합니다.
