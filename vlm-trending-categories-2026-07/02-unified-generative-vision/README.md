# 통합 생성형 비전

작성일: 2026-07-17

## 출처와 작업 범위

이 카테고리는 비전 태스크를 전용 헤드가 아니라 텍스트/이미지 생성 공간으로 통합하는 흐름을 다룹니다.

포함 논문:

- Vision as Unified Multimodal Generation: https://arxiv.org/abs/2607.06560
- Video Generation Models are General-Purpose Vision Learners: https://arxiv.org/abs/2607.09024
- Vision-Language-Vision Auto-Encoder: https://arxiv.org/abs/2507.07104

## 한눈에 보기

| 논문 | 병목 | 핵심 아이디어 | 실무 적용 |
|---|---|---|---|
| SenseNova-Vision | 태스크별 헤드 파편화 | detection, depth, pose 등을 생성 공간으로 통합 | 범용 비전 API |
| GenCeption | 전문 모델별 데이터와 구조 의존 | 비디오 생성 backbone을 일반 perception 모델로 사용 | depth, segmentation, pose |
| VLV Auto-Encoder | 대규모 image-text pair와 GPU 비용 | diffusion decoder에서 시각-언어 지식 증류 | 저비용 captioner, pretraining |

## 기초 개념

### 출력 시리얼라이즈

좌표, 마스크, 깊이, 포즈처럼 서로 다른 출력 형식을 모델이 생성할 수 있는 텍스트나 이미지 형식으로 바꾸는 과정입니다. 통합 모델에서는 출력 규약이 모델 구조만큼 중요합니다.

### Unified Multimodal Model

입력과 출력이 텍스트, 이미지, 혼합 포맷을 오갈 수 있는 모델입니다. 자연어 지시와 시각 프롬프트로 태스크를 지정하고, 모델은 약속된 포맷으로 응답합니다.

### Video Generative Pretraining

비디오 생성 모델은 시간, 물체 움직임, 카메라 변화, 장면 구조를 학습합니다. GenCeption은 이 능력이 인식 태스크에도 useful prior가 될 수 있다고 봅니다.

### Knowledge Distillation from Diffusion

이미 학습된 diffusion 모델의 시각-언어 정렬 지식을 작은 VLM 또는 auto-encoder 구조에 옮기는 접근입니다.

## 상세 정리

SenseNova-Vision은 컴퓨터 비전의 다양한 출력을 하나의 생성 모델이 다루게 합니다. 장점은 구조 통합이고, 위험은 출력 형식 오류입니다. 따라서 schema validator와 post-processor가 중요합니다.

GenCeption은 비디오 생성 backbone을 synthesis 도구가 아니라 perception backbone으로 봅니다. 비디오 생성 모델이 가진 spatiotemporal prior를 depth, segmentation, camera pose 같은 태스크에 활용합니다.

VLV Auto-Encoder는 최신 2026년 논문은 아니지만 비용 효율 학습 흐름에서 다시 중요해졌습니다. 핵심은 대규모 paired data 대신 pretrained T2I diffusion decoder를 활용한다는 점입니다.

## 용어 정리

| 용어 | 뜻 |
|---|---|
| Task-specific head | 태스크별 전용 출력 모듈 |
| Serialization | 구조화된 출력을 시퀀스나 이미지 포맷으로 바꾸는 과정 |
| Dense prediction | 픽셀/패치 단위로 예측하는 작업 |
| Diffusion backbone | 이미지/비디오 생성 모델의 주 표현 네트워크 |
| Instruction-response corpus | 지시와 정답 출력을 짝지은 학습 코퍼스 |

## 실습 학습 가이드

`01_foundations.ipynb`에서는 다음을 실습합니다.

1. detection, segmentation, depth, pose 출력을 공통 JSON/텍스트 규약으로 바꿉니다.
2. 생성 결과가 schema를 만족하는지 검증합니다.
3. 태스크별 헤드 방식과 통합 생성 방식의 장단점을 표로 비교합니다.

## 다음 학습 경로

- JSON schema, mask encoding, coordinate normalization을 함께 공부합니다.
- 모델의 zero-shot 성능보다 출력 포맷 안정성과 검증 가능성을 우선 평가합니다.
- 생성 모델을 인식 모델로 재사용하는 경우 데이터 누수와 평가 공정성을 반드시 확인합니다.
