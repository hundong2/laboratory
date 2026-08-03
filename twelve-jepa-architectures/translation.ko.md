# 「12가지 유형의 JEPA 아키텍처」 학습용 한국어 재구성

## 원문 정보와 이용 범위

- 원문: [Turing Post Korea](https://turingpost.co.kr/p/12-jepa-types)
- 제목: 12가지 유형의 JEPA 아키텍처
- 저자: Ben Eum, Ksenia Se
- 게시일: 2025-05-26
- 원문 언어: 한국어
- 접근일: 2026-08-03
- 최종 확인 URL: `https://turingpost.co.kr/p/12-jepa-types`

원문이 이미 한국어이므로 이 파일은 번역본이 아니라, 원문의 제목과 목록 흐름을
따른 **교정·학습용 한국어 재구성본**입니다. 저작권이 있는 짧은 기사의 문장을
그대로 복제하지 않고 핵심 의미를 요약했으며, 자세한 표현과 연결 자료는 원문을
참조해야 합니다.

## 도입: JEPA란 무엇인가

JEPA(Joint-Embedding Predictive Architecture)는 얀 르쿤이 제안해 온 예측형
학습 접근입니다. 다음 token이나 가려진 pixel 자체를 생성하는 대신, 관찰되지
않은 부분 또는 미래 부분의 **표현**을 예측합니다. 목표는 표면적인 패턴 일치를
넘어 입력의 의미와 구조를 포착하는 것입니다.

이 관점에서 핵심은 “무엇을 생성할 것인가”보다 “어떤 추상 수준에서 무엇을
예측할 것인가”입니다. JEPA 계열 연구는 이미지에서 시작해 움직임, 비디오, UI,
오디오, 생체신호, 텍스트-이미지, 표, 로봇 행동과 3D 데이터로 확장됐습니다.

## 12가지 JEPA 유형

### 1. I-JEPA

이미지 일부를 context로 보고 가려진 여러 영역의 latent 표현을 예측하는
비생성형 자기지도학습 방법입니다. 수작업 view augmentation이나 픽셀 복원에
의존하지 않고 의미론적 이미지 표현을 학습하는 데 초점을 둡니다.

- 원 논문: [Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture](https://arxiv.org/abs/2301.08243)

### 2. MC-JEPA

공유 encoder 안에서 이미지·비디오의 content 특징과 motion 정보를 함께
학습합니다. 자기지도 표현 학습 목적과 optical flow 추정 목적을 결합해 두
목표가 서로 보완하도록 설계합니다.

- 원 논문: [MC-JEPA](https://arxiv.org/abs/2307.12698)

### 3. V-JEPA

비디오에서 미래 또는 가려진 시공간 영역의 feature를 예측합니다. 사전학습된
이미지 encoder, text supervision, negative example과 픽셀 재구성 없이 feature
prediction만으로 motion과 appearance에 모두 유용한 표현을 노립니다.

- 원 논문: [Revisiting Feature Prediction for Learning Visual Representations from Video](https://arxiv.org/abs/2404.08471)

### 4. UI-JEPA

레이블 없는 화면 사용자 활동 sequence에서 일부를 가려 추상 embedding을
학습합니다. 이후 LLM decoder를 결합하고 fine-tuning해 사용자의 의도를
예측하는 active perception 문제로 연결합니다.

- 원 논문: [UI-JEPA](https://arxiv.org/abs/2409.04081)

### 5. Audio-based JEPA(A-JEPA)

audio spectrogram을 patch로 나누고 보이는 영역에서 가려진 영역의 표현을
예측합니다. 시간과 주파수의 국소 상관을 고려해 random block에서
time-frequency-aware masking으로 진행하는 curriculum을 사용합니다.

- 원 논문: [A-JEPA: Joint-Embedding Predictive Architecture Can Listen](https://arxiv.org/abs/2311.15830)

### 6. S-JEPA

EEG 데이터의 공간적 관계에 맞춘 표현 학습을 수행합니다. dynamic spatial
attention과 경량 downstream classifier를 통해 서로 다른 EEG dataset으로의
전이를 다루는 것이 특징입니다.

- 원 논문: [S-JEPA](https://arxiv.org/abs/2403.11772)

### 7. TI-JEPA

Text-Image JEPA는 energy-based 사전학습으로 text와 image를 공유 embedding
space에 놓습니다. cross-modal transfer에 유용한 정렬된 표현을 얻는 것이
목표입니다.

- 원 논문: [TI-JEPA](https://arxiv.org/abs/2503.06380)

### 8. T-JEPA

tabular data의 feature 일부를 context로 사용해 다른 feature subset의 latent
표현을 예측합니다. 이미지식 augmentation을 억지로 적용하지 않고, label에
독립적인 표 표현을 학습하려는 접근입니다.

- 원 논문: [T-JEPA](https://arxiv.org/abs/2410.05016)

### 9. ACT-JEPA

자기지도학습과 imitation learning을 연결해 policy representation을 학습합니다.
latent space에서 추상 observation과 action chunk를 다루어 noise와 누적 오차를
줄이고 dynamics를 표현하는 것이 목표입니다.

- 원 논문: [ACT-JEPA](https://arxiv.org/abs/2501.14622)

### 10. Brain-JEPA

fMRI 시계열을 위한 brain dynamics foundation model입니다. brain functional
gradient로 ROI의 위치 관계를 표현하고, ROI와 시간축을 교차하는 spatiotemporal
masking으로 인구통계, 특성, 질병 관련 downstream task에 쓸 표현을 학습합니다.

- 원 논문: [Brain-JEPA](https://arxiv.org/abs/2409.19407)

### 11. 3D-JEPA

3D 데이터에서 하나의 정보가 풍부한 context block과 여러 target block을
선택하고, context로부터 각 target embedding을 예측합니다. 3D scene의 구조적
표현을 label 없이 학습하는 데 초점을 둡니다.

- 원 논문: [3D-JEPA](https://arxiv.org/abs/2409.15803)

### 12. Point-JEPA

point cloud에 joint-embedding prediction을 적용합니다. 경량 sequencer가 local
point patch embedding의 순서를 정하고, context와 target patch를 구성합니다.
거리 계산을 재사용해 학습 효율도 높입니다.

- 원 논문: [Point-JEPA](https://arxiv.org/abs/2404.16432)

## 읽을 때 주의할 점

- “12가지”는 2025년 5월 기사 시점의 설명 목록이지 JEPA 연구 전체를 망라한
  공식 분류 체계가 아닙니다.
- 모든 연구가 동일한 encoder·loss·EMA 방식을 쓰는 것은 아닙니다.
- JEPA는 Transformer의 반대말이 아닙니다. 여러 JEPA 구현이 Transformer를
  구성 모듈로 사용하며, 대조되는 핵심은 주로 원시 입력 생성·복원 목적입니다.
- latent prediction이 자동으로 인간 수준의 이해나 일반 월드 모델을 보장하지
  않습니다. 각 논문의 downstream 평가와 외부 검증을 따로 봐야 합니다.

## 학습 자료로 이동

- [종합 분석과 비교](README.md)
- [기초 분류 실습](01_foundations.ipynb)
- [mask와 latent loss 실습](02_practice.ipynb)
- [collapse 진단과 실험 설계](03_advanced.ipynb)
