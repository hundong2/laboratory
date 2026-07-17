# 공간/강건성 VLM

작성일: 2026-07-17

## 출처와 작업 범위

이 카테고리는 VLM이 실제 시각 증거, 공간 구조, 센서 신호, 텍스트 오정보를 어떻게 처리하는지 다룹니다.

포함 논문:

- Vision Pretraining for Dense Spatial Perception: https://arxiv.org/abs/2607.05247
- RE-VLM: https://arxiv.org/abs/2605.19329
- Constructive Apraxia: https://arxiv.org/abs/2410.03551
- Do Images Speak Louder than Words?: https://arxiv.org/abs/2601.19202

## 한눈에 보기

| 논문 | 병목 | 핵심 아이디어 | 실무 적용 |
|---|---|---|---|
| Dense Spatial Perception | 의미 중심 표현의 공간 손실 | Masked Boundary Modeling | 로봇, 자율주행, depth |
| RE-VLM | RGB-only VLM의 가혹 환경 취약성 | RGB + event dual stream | 야간, 고속, HDR scene |
| Constructive Apraxia | 기하학적 구성 실패 | 인지 장애형 spatial benchmark | 공간 추론 평가 |
| Do Images Speak Louder? | 텍스트 오정보가 이미지 증거를 override | CONTEXT-VQA와 설득형 prompt 평가 | VLM 신뢰성 검증 |

## 기초 개념

### 공간 지각

물체가 무엇인지 맞히는 것뿐 아니라 어디에 있고, 경계가 어디이며, 얼마나 멀고, 어떤 표면 방향을 갖는지 이해하는 능력입니다.

### Boundary Modeling

객체나 표면이 갈라지는 경계와 깊이 불연속을 학습 목표로 삼는 방식입니다. 경계는 물리적 상호작용과 3D 이해에서 중요한 단서입니다.

### Event Stream

이벤트 카메라는 프레임 전체를 일정 주기로 저장하지 않고, 각 픽셀의 밝기 변화 이벤트를 비동기적으로 기록합니다. 저조도, 빠른 움직임, HDR 상황에서 RGB 프레임을 보완할 수 있습니다.

### Textual Misinformation

이미지 증거와 충돌하는 텍스트 설명이나 설득형 프롬프트입니다. 강건한 VLM은 텍스트가 그럴듯하더라도 이미지 증거를 우선 확인해야 합니다.

## 상세 정리

Dense Spatial Perception은 모델이 semantic label에만 강해지는 문제를 지적합니다. 경계와 형태 불연속을 직접 복원하도록 학습하면 depth와 embodied perception에 유리합니다.

RE-VLM은 센서 modality 자체를 확장합니다. RGB가 실패하는 상황에서 이벤트 스트림을 병렬 인코더로 정렬해 scene understanding을 강화합니다.

Constructive Apraxia는 모델 한계를 드러내는 진단 연구입니다. Ponzo illusion 같은 간단해 보이는 기하학 과제가 최신 모델에도 어려울 수 있음을 보입니다.

Do Images Speak Louder than Words?는 텍스트가 이미지를 이기는 취약성을 다룹니다. 이는 VLM이 실제로 무엇을 근거로 답했는지 평가해야 한다는 교훈을 줍니다.

## 용어 정리

| 용어 | 뜻 |
|---|---|
| Dense spatial perception | 픽셀/패치 수준의 공간 구조 이해 |
| Masked Boundary Modeling | 경계 정보를 가리고 복원하는 자기지도 학습 |
| Event camera | 밝기 변화 이벤트를 기록하는 비동기 센서 |
| Language prior | 모델이 시각 증거보다 텍스트 통계에 의존하는 경향 |
| Robustness | 입력 교란과 충돌 정보에서도 성능을 유지하는 능력 |

## 실습 학습 가이드

`01_foundations.ipynb`에서는 다음을 실습합니다.

1. 작은 label map에서 boundary map을 계산합니다.
2. RGB 프레임과 event stream의 차이를 toy event로 표현합니다.
3. 이미지 근거와 텍스트 오정보가 충돌할 때 간단한 decision rule을 만듭니다.

## 다음 학습 경로

- Depth estimation, surface normal, optical flow, event camera 기초를 학습합니다.
- VQA 정확도만 보지 말고 counterfactual prompt와 modality conflict 평가를 설계합니다.
- 모델 설명에서 "봤다"와 "텍스트로 추론했다"를 분리하는 검증 절차를 만듭니다.
