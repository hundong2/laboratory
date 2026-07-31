# 「Gemini Robotics 2 brings whole body intelligence to robots」 한국어 번역 요약

작성일: 2026-07-31

- 원문: [Google DeepMind 공식 발표](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/)
- 제목: Gemini Robotics 2 brings whole body intelligence to robots
- 저자: Carolina Parada
- 게시일: 2026-07-30
- 원문 언어: 영어
- 접근일: 2026-07-31 (Asia/Seoul)

> 저작권을 존중해 원문 전문을 복제하지 않고, 원문의 섹션 순서·핵심 주장·수치를 보존한 한국어 번역 요약을 제공한다. 제품 상태와 수치는 접근일 기준이다.

## 로봇에 전신 지능을 제공하는 Gemini Robotics 2

DeepMind는 발끝부터 손끝까지 이어지는 지능형 전신 제어, 정교한 조작과 협업을 통해 복잡한 작업을 수행하는 차세대 물리 AI를 소개한다.

기존 로봇은 대체로 좁고 반복적인 작업 순서를 미리 프로그래밍하거나 원격 조종한다. 예측하기 어려운 환경에서 스스로 적응하기 어렵고, 한 로봇 몸체에서 배운 기술을 다른 몸체로 옮기기도 어렵다. Gemini Robotics 2는 다양한 형태와 크기의 로봇이 생각하고 행동하며 안전하게 상호작용하도록 하는 지능 계층을 목표로 한다.

이번 세대는 humanoid가 걷고, 쪼그리며, 몸을 뻗고, 물체를 조작해 어지러운 방을 정리하는 것처럼 전신을 함께 쓰는 작업을 다룬다. 여러 로봇이 협업할 수 있고, 로컬 장치에서 실행하면서 새로운 로봇 몸체에 수 시간 내 적응하는 방향도 포함한다.

## 세 가지 모델

- **Gemini Robotics 2**: 영상과 언어를 motor control로 바꾸는 VLA다. humanoid 전체와 양팔 로봇을 제어하며 손과 그리퍼의 정교한 조작을 지원한다.
- **Gemini Robotics ER 2**: 인간과 소통하고 물리 세계를 이해하며 수 분 동안 이어지는 다단계 작업을 계획하는 VLM 기반 embodied-reasoning agent다. 여러 로봇의 팀 작업도 조정한다.
- **Gemini Robotics On-Device 2**: 로봇 장치에서 로컬로 실행하도록 최적화한 효율적인 VLA다. 수 시간 분량의 데이터로 새로운 embodiment에 빠르게 적응한다.

같은 Gemini Robotics 2 checkpoint가 Apollo 2와 서로 다른 손 구성, Franka Duo의 그리퍼를 제어했다. 공개 결과에서 전신·그리퍼 작업은 중간에서 높은 성공률을 보였지만, 다지 손 조작은 여전히 어렵다고 원문도 명시한다.

## 움직이는 humanoid: 전신 작업 관리

사람을 위해 만들어진 환경에서는 좁고 복잡한 공간에서 몸을 뻗고, 굽히고, 균형을 잡아야 한다. 이전 모델이 주로 humanoid 상체로 탁상 작업을 했다면 이번 모델은 전신 움직임까지 확장한다.

Apptronik Apollo 2에게 물뿌리개를 아래쪽 선반의 초록색 상자에 넣으라고 지시한 예에서 로봇은 테이블로 걸어가 물체를 들고, 선반까지 이동한 뒤 지정된 위치에 내려놓는다. DeepMind는 움직임 속도는 더 개선해야 한다고 밝히면서도 전신 협응이 필요한 실제 작업으로 향하는 단계라고 설명한다.

## 손과 그리퍼의 정교한 조작

Gemini Robotics 2는 서로 다른 말단효과기에서 정교한 조작 능력을 높이는 것을 목표로 한다. Apollo 2의 다섯 손가락, 22-DOF SharpaWave 손으로 매듭을 묶거나 지퍼백을 닫는 동작을 수행하고, Franka Duo의 표준 두 손가락 평행 그리퍼로 촘촘한 포장 같은 작업을 수행한다.

공개 그래프의 다지 손 과제 성공률은 전구 조이기 36%, 풀기 92%, 쓰레기봉투 묶기 44%, 쓰레받기 32%, 지퍼백 40%다. Franka Duo 그리퍼는 일반 pick-and-place 74.2%, 다양한 도구 키팅 78.9%, 정밀 삽입 89.6%였다. 플랫폼과 과제가 달라 숫자끼리 직접 비교할 수는 없으며, DeepMind는 정밀도와 속도를 계속 개선 중이라고 밝힌다.

## 에이전트 추론과 다중 로봇 협업

Gemini Robotics ER 2는 고수준 두뇌 역할을 한다. 사용자 지시를 처리하고 방을 관찰해 필요한 단계를 추론하며, VLA와 함께 행동을 실행하고 완료될 때까지 진행을 추적한다. 이 구성은 새로운 상황과 목표에 일반화하고, 한 단계가 실패했을 때 스스로 수정하는 것을 목표로 한다.

업데이트된 모델은 수백 번의 결정이 포함된 수 분 길이의 작업 순서를 더 안정적으로 실행하고, 작업의 시작과 종료 및 주요 사건이 발생한 시점을 판별한다. 서로 다른 로봇이 소통하며 한 대로 해결하기 어려운 workflow를 나눠 수행하는 다중 로봇 협업도 소개됐다.

## 새로운 로봇에 빠르게 적응하는 온디바이스 모델

네트워크 지연이나 인터넷 연결 없이 동작해야 하는 응용을 위해 Gemini Robotics On-Device 2는 로컬 실행에 최적화됐다. 여러 embodiment를 기본으로 다루며 이전 세대의 motion-transfer 기법을 이어받았다.

DeepMind는 형태, 센서와 자유도가 크게 다른 새 양팔 로봇에도 보통 200개 미만 예시와 수 시간의 적응 시간으로 적용할 수 있다고 설명한다. 발표에서는 Dexmate, SO101과 Trossen 플랫폼에서 다양한 작업을 시연한다.

## 안전하고 책임 있는 로보틱스

DeepMind는 전통적 물리 안전 조치와 AI 안전 framework를 함께 사용하는 다층 접근을 강조한다. Gemini Robotics 2는 불확실한 현실 환경과 사람 곁에서 협업할 때의 안전을 다룬다.

새로운 ASIMOV-Agentic benchmark는 ER agent가 VLA의 불안전한 tool call을 거부하는지, 작업 실행 가능성을 예측하는지, 불확실할 때 먼저 사람의 개입을 요청하는지 평가한다. ER 2는 사람이 가까이 있음을 더 잘 감지하고 안전 tool call을 발생시켜 로봇을 정지시키도록 설계됐다.

## 범용 물리 AI를 향해

DeepMind는 이번 발표를 단일 작업 자동화에서 범용 물리 지능으로 이동하는 과정의 이정표로 설명한다. 목표는 인간과 함께 복잡한 문제를 해결하는 물리 AI다. 다만 현재 VLA와 On-Device 모델은 early-access 중심이며, 시연 결과가 모든 환경에서의 성능이나 안전을 보장하지는 않는다.

## 공개 접근 상태

- Gemini Robotics ER 2: Google AI Studio에서 사용 가능, Gemini Enterprise Agent Platform은 private preview
- Gemini Robotics 2 VLA: private preview 및 early-access partners
- Gemini Robotics On-Device 2: trusted testers / early access

## 번역 검수 메모

- 원문의 주요 섹션, 모델 역할, 플랫폼 이름과 성공률 수치를 대조했다.
- `action`, `tool call`, `embodiment`처럼 구현 범위가 넓은 용어는 의미 손실을 줄이기 위해 원어를 병기했다.
- 홍보 표현은 사실 단정으로 강화하지 않고 “목표”, “설명”, “시연”으로 출처의 주장임을 구분했다.
