# 양자 소프트웨어 전문인력 학습 가이드

이 가이드는 여섯 직무에 공통인 기반을 먼저 만들고, **주력 트랙 하나 + 보조 트랙 하나**를 선택하게 구성했다. 주 10~12시간 기준으로 공통 40주 뒤 트랙 수업과 capstone을 합친 전문화 패키지 16~24주를 권장한다. 트랙 문서의 짧은 capstone을 확장하려면 [12주 통합 capstone 일정](05_portfolio_and_assessment.md)으로 대체한다. 알고리즘 연구자는 공통 과정을 수치해석·물성 과정과 합친 [48주 통합 경로](02_algorithm_and_science_track.md)를 대신 선택할 수 있으며 두 기간을 중복 합산하지 않는다. 학습 기간보다 각 단계의 통과 기준을 우선한다.

## 1. 시작 전 진단

다음 과제를 외부 답안을 보지 않고 설명하고 구현해 본다.

| 진단 | 통과 증거 | 실패하면 시작할 곳 |
| --- | --- | --- |
| 복소수 2×2 matrix의 eigenvalue와 condition number 계산 | 손 계산과 NumPy 결과가 일치 | 공통 1단계 |
| 1D Poisson equation을 finite difference로 풀고 오차 계산 | grid refinement와 오차 변화 보고 | 공통 1단계 |
| Bell state의 amplitude와 측정 확률 유도 | 정규화와 두 결과 `00`, `11` 설명 | 공통 2단계 |
| finite shots와 물리 noise의 차이 설명 | 서로 다른 실험으로 분리 | 공통 2~3단계 |
| 작은 프로그램에 단위 테스트·seed·환경 기록 추가 | 제3자가 재실행 가능 | 공통 0단계 |
| API job의 timeout·retry·중복 제출 처리 설계 | 상태 전이와 idempotency test | 공통 5단계 |

진단을 통과한 영역은 압축해도 되지만, 결과물을 남기지 않고 “안다”고 판정하지 않는다.

## 2. 전체 학습 순서

1. [공통 기반 40주](01_common_foundations.md)를 통해 수학, 양자 정보, 회로, 알고리즘 평가와 시스템 공학을 익힌다.
2. [노트북 1](01_foundations.ipynb)에서 SDK 없이 상태벡터·gate·Bell state·sampling을 검증한다.
3. [노트북 2](02_practice.ipynb)에서 VQE·QAOA toy model, Poisson baseline과 HHL 타당성 감사를 수행한다.
4. 아래 직무 선택표로 주력·보조 트랙을 정한다.
5. [노트북 3](03_advanced.ipynb)에서 parameter-shift, 안전한 compiler rewrite, hardware-aware 비용과 hybrid job 상태기계를 연결한다.
6. [포트폴리오·평가 기준](05_portfolio_and_assessment.md)에 따라 12주 capstone을 만든다.

## 3. 직무 선택표

| 흥미와 강점 | 권장 주력 | 권장 보조 |
| --- | --- | --- |
| PDE, 수치해석, 물리 모델과 복잡도 | 양자 알고리즘 설계 | 회로 검증 또는 compiler |
| gate, noise, backend와 테스트 | 회로 검증·개발 | compiler 또는 QML |
| 자동미분, kernel, ML 실험 설계 | QML | 회로 검증 |
| API, domain model, 보안·운영 | 소프트웨어 architecture | Quantum-HPC |
| IR, rewrite, LLVM와 hardware mapping | 회로 compiler | 회로 검증 또는 FTQC |
| 분산 시스템, scheduler, C++/GPU/HPC | Quantum-HPC 통합 | architecture 또는 compiler |
| 양자화학·강상관 물질 | 알고리즘 설계의 물성 경로 | 회로 검증 |
| 금융·물류 조합 최적화 | 알고리즘 설계의 최적화 경로 | Quantum-HPC |

- 알고리즘·물성 과정: [02_algorithm_and_science_track.md](02_algorithm_and_science_track.md)
- 회로 검증·QML 과정: [03_circuit_and_qml_track.md](03_circuit_and_qml_track.md)
- architecture·compiler·hybrid 과정: [04_architecture_compiler_hybrid_track.md](04_architecture_compiler_hybrid_track.md)

## 4. 실습 환경

세 기본 노트북은 클라우드 계정과 양자 SDK 없이 실행된다.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
jupyter lab
```

Linux/macOS에서는 활성화 명령만 `source .venv/bin/activate`로 바꾼다. Python은 3.11 이상을 권장한다. 실습마다 다음 metadata를 기록한다.

```text
Python version / package lock / OS
seed / shots / simulator or backend
logical and transpiled circuit metrics
classical baseline / tolerance / wall time
```

Qiskit, PennyLane, Cirq, QIR toolchain은 하나의 환경에 무조건 섞지 않는다. 전문 실습으로 넘어갈 때 SDK별 별도 환경과 lock file을 만든다. 현재 API 경계는 [출처 기록](../sources.md)을 참고하되 설치 당일 공식 문서를 다시 확인한다.

## 5. 주간 학습 리듬

| 활동 | 권장 시간 | 남길 증거 |
| --- | ---: | --- |
| 이론·수식 | 3시간 | 한 페이지 derivation과 가정 목록 |
| 구현 | 4시간 | 실행 코드와 자동 검사 |
| 실험 | 2시간 | 여러 seed, raw metrics, 실패 결과 |
| 읽기·비평 | 2시간 | 원 논문 주장과 실제 조건 대조표 |
| 문서화 | 1시간 | 재현 명령, 결정 기록, 다음 가설 |

매 4주마다 “배운 내용”이 아니라 **재현 가능한 artifact**를 심사한다. 통과하지 못하면 다음 용어로 넘어가기보다 실패 원인을 보완한다.

## 6. 모든 트랙의 공통 품질문

- 고전 기준선과 양자 방법의 입력·출력 계약이 같은가?
- exact reference가 가능한 작은 문제에서 먼저 검증했는가?
- state preparation, readout, shots, postselection과 고전 후처리를 비용에 넣었는가?
- simulator, noisy simulation, QPU, logical FT estimate를 구분했는가?
- 여러 seed와 신뢰구간을 보고했는가?
- version, backend, calibration 시각과 transpilation 결과를 기록했는가?
- 성공하지 않은 설정과 제한 사항도 공개했는가?

하나라도 답할 수 없으면 성능 결론을 보류한다.

## 7. 파일 안내

- [상위 개요](../README.md)
- [출처와 버전 기록](../sources.md)
- [공통 기반](01_common_foundations.md)
- [알고리즘·PDE·물성·최적화](02_algorithm_and_science_track.md)
- [회로 검증·QML](03_circuit_and_qml_track.md)
- [architecture·compiler·Quantum-HPC](04_architecture_compiler_hybrid_track.md)
- [포트폴리오와 평가](05_portfolio_and_assessment.md)
- [기초 노트북](01_foundations.ipynb)
- [응용 노트북](02_practice.ipynb)
- [심화 노트북](03_advanced.ipynb)

첫 목표는 많은 framework를 설치하는 것이 아니다. 작은 문제를 수학적으로 정의하고, 고전 정답과 양자 표현을 같은 기준으로 검증하는 습관을 만드는 것이다.
