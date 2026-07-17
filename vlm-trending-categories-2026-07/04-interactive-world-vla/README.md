# 인터랙티브 월드 모델과 VLA

작성일: 2026-07-17

## 출처와 작업 범위

이 카테고리는 실시간 비디오 생성, 장기 상호작용, 시뮬레이션 환경 생성, 로봇 행동 정책을 다룹니다.

포함 논문:

- Vidu S1: https://arxiv.org/abs/2607.03118
- Infinite Worlds with Versatile Interactions: https://arxiv.org/abs/2607.07534
- EmbodiedGen V2: https://arxiv.org/abs/2607.07459
- From Foundation to Application: Improving VLA Models in Practice: https://arxiv.org/abs/2607.06403

## 한눈에 보기

| 논문 | 병목 | 핵심 아이디어 | 실무 적용 |
|---|---|---|---|
| Vidu S1 | 실시간 비디오 생성 지연 | TurboDiffusion/TurboServe 기반 streaming | 디지털 휴먼, 인터랙티브 비디오 |
| Infinite Worlds | 긴 상호작용 품질 유지 | causal pretraining, agentic harness | 게임/월드 시뮬레이터 |
| EmbodiedGen V2 | 정책 학습용 3D 환경 조립 수작업 | sim-ready 3D world engine | 로봇 시뮬레이션 |
| LingBot-VLA 2.0 | 실제 로봇 적용 간극 | 데이터, 행동 공간, dynamics prediction 개선 | VLA robot policy |

## 기초 개념

### World Model

현재 상태와 행동을 바탕으로 다음 장면이나 환경 상태를 예측하는 모델입니다. 단순 비디오 생성과 달리 상호작용, 지연, 장기 일관성이 중요합니다.

### Agentic Harness

모델을 계획, 실행, 관찰, 수정 루프로 감싸는 실행 구조입니다. Infinite Worlds에서는 pilot agent와 director agent의 역할 분리가 등장합니다.

### Simulation-ready Environment

보기 좋은 3D asset만이 아니라 물리 속성, 충돌, 조작 가능성, task affordance가 들어 있어 정책 학습에 바로 쓸 수 있는 환경입니다.

### VLA

Vision-Language-Action의 약자입니다. 시각 입력과 언어 명령을 받아 로봇 행동을 출력하는 모델 계열입니다.

## 상세 정리

Vidu S1은 실시간 인터랙티브 비디오 생성을 강조합니다. 음성 지시로 캐릭터를 제어하고, 긴 비디오 스트림에서 품질과 프레임레이트를 유지하는 것이 핵심입니다.

Infinite Worlds는 world model에 agentic harness를 결합합니다. 모델이 장면을 생성하는 것뿐 아니라, agent가 행동을 계획하고 장면을 확장하는 루프를 갖습니다.

EmbodiedGen V2는 3D asset을 정책 학습 환경으로 바꾸는 병목을 다룹니다. 생성된 환경이 조작, 내비게이션, mobile manipulation에 바로 쓰일 수 있어야 합니다.

LingBot-VLA 2.0은 foundation model을 실제 로봇 적용으로 옮기는 논문입니다. 다양한 로봇 embodiment와 행동 자유도, 미래 예측 학습이 강조됩니다.

## 용어 정리

| 용어 | 뜻 |
|---|---|
| Interactive video generation | 사용자 입력에 실시간 반응하는 비디오 생성 |
| Closed-loop | 행동, 관찰, 수정이 반복되는 루프 |
| Sim-to-real | 시뮬레이션에서 학습한 정책을 현실 로봇으로 옮기는 과정 |
| Cross-embodiment | 서로 다른 로봇 형태 사이의 일반화 |
| Dynamics prediction | 미래 상태를 예측하는 학습 과제 |

## 실습 학습 가이드

`01_foundations.ipynb`에서는 다음을 실습합니다.

1. world state, action, observation을 작은 dict로 모델링합니다.
2. pilot agent와 director agent가 번갈아 동작하는 루프를 구현합니다.
3. 로봇 action space를 확장할 때 검증해야 할 항목을 체크리스트로 만듭니다.

## 다음 학습 경로

- 비디오 생성 모델의 latency, FPS, drift 평가를 공부합니다.
- Gymnasium, Isaac Sim, Habitat 같은 시뮬레이션 환경 구조를 익힙니다.
- VLA에서는 action representation, proprioception, depth/geometric cue, policy evaluation을 함께 봅니다.
