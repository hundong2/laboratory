# 양자 소프트웨어 전문인력 학습 로드맵

작성일: 2026-09-13

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [핵심 요약](#핵심-요약)
- [상세 정리](#상세-정리)
- [직무별 전문 트랙](#직무별-전문-트랙)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

이 폴더는 사용자가 제시한 여섯 직무와 공통 전문 역량을 하나의 학습 체계로 재구성한 것이다. 특정 채용 공고의 합격을 보장하는 과정이 아니라, **기초 이론 → 검증 가능한 구현 → 한 분야의 깊이 → 시스템 수준 포트폴리오**로 이어지는 역량 기반 로드맵이다.

조사 기준일은 2026-09-13이다. Qiskit, PennyLane, Cirq, QIR, MLIR, CUDA-Q와 클라우드 서비스 API는 계속 바뀌므로 코드를 복사하기 전에 각 공식 문서의 현재 버전과 migration guide를 다시 확인해야 한다. 확인한 공식 문서·원 논문·오픈소스 자료는 [sources.md](sources.md)에 주제별로 정리했다.

범위는 다음과 같다.

- 공통 기반: Python, 수치 선형대수, 확률·통계, 최적화, 양자 정보, 소프트웨어 공학
- 알고리즘: HHL 계열, spectral method, 변분 PDE/QPINN, QLBM, VQE, QAOA, QSCI, SQD
- 과학 계산: DFT, 양자화학, DMFT, DMRG와 양자 알고리즘의 접점
- QML: differentiable quantum circuit, parameter-shift rule, QNN, feature map, quantum kernel
- 시스템: SDK, 회로 검증, compiler IR, MLIR/QIR/OpenQASM, fault tolerance, resource estimation
- 통합: 비동기 Quantum-HPC workflow, API, middleware, cloud, 분산 실행과 관측성

이 자료의 NumPy 실습은 작은 문제에서 원리를 검증하는 **교육용 toy model**이다. 실제 양자 우위, 산업 규모 물성 계산 또는 실제 QPU 성능을 재현했다고 주장하지 않는다.

## 한눈에 보기

처음부터 여섯 직무를 동시에 공부하면 각 분야의 전문 용어만 얕게 훑게 된다. 아래처럼 T자형으로 진행한다.

```text
공통 기반 0 ─ 프로그래밍·수학 진단
    ↓
공통 기반 1 ─ 선형대수·확률·최적화·수치해석
    ↓
공통 기반 2 ─ 양자 상태·측정·얽힘·채널
    ↓
공통 기반 3 ─ 회로·시뮬레이션·노이즈·SDK
    ↓
공통 기반 4 ─ 알고리즘·복잡도·고전 baseline·자원 추정
    ↓
공통 기반 5 ─ 테스트·재현성·API·비동기 workflow
    ├─ A. PDE·물성·최적화 알고리즘 설계
    ├─ B. 양자 회로 검증·개발
    ├─ C. 양자 기계학습
    ├─ D. 양자 소프트웨어 아키텍처
    ├─ E. 양자 회로 컴파일러
    └─ F. Quantum-HPC 하이브리드 통합
```

권장 기본 과정은 주 10~12시간 기준 공통 40주와 트랙 수업·capstone을 합친 전문화 16~24주다. 알고리즘 연구처럼 수치해석·물성 기반을 더 깊게 요구하는 경로는 [48주 통합 과정](guide/02_algorithm_and_science_track.md)을 별도 빠른 경로로 사용할 수 있으며, 공통 40주에 다시 더하는 과정이 아니다. 기간보다 중요한 것은 각 단계의 **통과 기준**이다. 이미 수치해석·양자역학·컴파일러 경험이 있다면 진단 과제를 통과한 단계를 건너뛸 수 있다.

| 단계 | 권장 범위 | 반드시 남길 결과물 | 통과 기준 |
| --- | --- | --- | --- |
| 0. 진단과 도구 | 2주 | Python 환경, Git 저장소, 작은 실험 보고서 | 테스트·seed·환경 정보를 포함해 타인이 재실행 가능 |
| 1. 수학·수치 기반 | 8주 | eigenproblem, 최적화, Poisson 방정식 고전 solver | 오차·조건수·계산량을 설명하고 NumPy 결과를 검증 |
| 2. 양자 정보 | 8주 | statevector, Bell state, density matrix 실습 | 정규화·unitarity·Born rule·partial trace를 코드로 검사 |
| 3. 회로 공학 | 8주 | 두 SDK 중 하나의 주력 구현과 다른 하나의 교차 검증 | ideal·shot·noise 결과를 구분하고 transpilation 전후 비교 |
| 4. 알고리즘 평가 | 8주 | VQE/QAOA와 선형계 toy benchmark | 고전 정답, 입력·출력 비용, shots, depth를 함께 보고 |
| 5. 시스템 공학 | 6주 | provider-neutral job API와 실패 복구 설계 | timeout·retry·idempotency·provenance 테스트 통과 |
| 6. 전문화 | 16~24주 | 아래 트랙 중 1개 주력 capstone | 재현 저장소, 기술 보고서, benchmark, 한계 분석 완성 |

## 기초 개념

### 양자 소프트웨어는 세 층을 동시에 다룬다

1. **문제 층**: PDE, 분자 Hamiltonian, 물류 최적화, 분류처럼 풀고 싶은 도메인 문제다.
2. **알고리즘 층**: 상태 준비, oracle·block encoding, ansatz, 측정, 고전 최적화로 문제를 양자 계산에 맞게 표현한다.
3. **실행 층**: logical circuit를 실제 장치의 gate set과 coupling에 맞게 변환하고, job·queue·결과·오류를 관리한다.

좋은 전문가는 한 층만 아는 사람이 아니라, 자신의 주력 층이 다른 두 층에 만드는 비용과 제약을 설명할 수 있는 사람이다.

### 진짜 비교 단위는 end-to-end다

양자 subroutine의 query complexity만 보고 속도 향상을 단정하면 안 된다. 다음 비용을 모두 적는다.

- 고전 데이터를 양자 상태로 준비하는 비용
- sparse access 또는 block encoding을 만드는 비용
- condition number, 정밀도, 성공 확률에 따른 반복 비용
- shot과 측정 grouping, 오류 완화 비용
- 결과가 양자 상태일 때 필요한 관측량만 읽는지, 전체 해를 복원하는지
- compiler가 삽입한 SWAP, basis translation, scheduling으로 늘어난 depth
- 고전 전처리·후처리, network queue, QPU 대기와 실패 재시도

따라서 모든 프로젝트에는 최소 하나의 강한 고전 baseline과 end-to-end 자원표가 있어야 한다.

### DFT·DMFT·DMRG는 모두 ‘양자 알고리즘’이 아니다

이 세 방법은 물성과 many-body 문제를 이해하고 양자 알고리즘을 검증하는 데 중요한 **고전 계산 방법**이다.

- DFT는 전자 밀도를 중심으로 물질의 electronic structure를 근사한다.
- DMFT는 국소적인 동적 상관을 impurity problem과 self-consistency loop로 다룬다.
- DMRG는 matrix product state를 사용해 특히 1차원·준1차원 강상관계의 저에너지 상태를 효율적으로 근사한다.

양자 화학 workflow에서는 이 결과가 Hamiltonian 생성, active-space 선택, 초기 상태, embedding, 정확도 비교의 기준이 된다. 용어를 나열하기 전에 Hartree–Fock/DFT, second quantization, fermion-to-qubit mapping, exact diagonalization 또는 tensor-network baseline을 먼저 다뤄야 한다.

## 핵심 요약

- **공통 코어를 먼저 이수한다.** 선형대수와 수치해석 없이 HHL·QPINN을, 양자 채널과 noise 없이 회로 검증을, compiler 기본기 없이 MLIR·QIR을 바로 시작하지 않는다.
- **주력 SDK 하나와 비교 SDK 하나를 둔다.** 예를 들어 Qiskit을 주력으로 하되 PennyLane의 자동미분을 비교하거나, Cirq의 noise/device model로 교차 검증한다.
- **전문 트랙은 한 번에 하나만 깊게 간다.** 알고리즘/PDE, 회로 검증, QML, 아키텍처, 컴파일러, HPC 중 하나를 주력으로 정하고 인접 트랙 하나를 보조로 둔다.
- **NISQ와 fault-tolerant 가정을 섞지 않는다.** VQE/QAOA의 실험 조건과 HHL/QPE의 오류보정·입력 oracle 가정은 별도 표로 관리한다.
- **정확성, 자원, 재현성을 함께 평가한다.** energy·accuracy만큼 circuit depth, two-qubit gates, shots, wall time, memory, seed, software version이 중요하다.
- **포트폴리오는 튜토리얼 복사가 아니다.** 문제 정의, baseline, 실패 실험, 검증 oracle, 설계 결정과 한계를 포함해야 한다.

## 상세 정리

### 공통 기반에서 배울 과목

| 영역 | 핵심 내용 | 왜 필요한가 |
| --- | --- | --- |
| Python·과학 계산 | NumPy, SciPy 개념, plotting, typing, pytest, profiling | simulator, optimizer, 실험 자동화의 공통 언어 |
| C++·Rust 선택 | 메모리 모델, build, FFI, concurrency | compiler/runtime/HPC·고성능 middleware에 필요 |
| 선형대수 | complex vector space, tensor product, eigendecomposition, SVD, sparse matrix, condition number | 상태·관측량·Hamiltonian·linear solver의 언어 |
| 확률·통계 | 표본, 추정량, 신뢰구간, hypothesis test, bootstrap | 유한 shot과 noisy benchmark를 해석 |
| 최적화 | convexity, gradient, constrained/discrete optimization, optimizer diagnostics | VQE·QAOA·QNN과 회로 synthesis 평가 |
| 수치해석 | floating-point, interpolation, finite difference, spectral method, ODE/PDE, iterative solver | 양자 PDE 주장의 baseline과 오차 예산 |
| 양자 정보 | pure/mixed state, measurement, channel, entanglement, fidelity, trace distance | 회로가 무엇을 계산하고 noise가 무엇을 바꾸는지 설명 |
| 복잡도 | asymptotic notation, query/gate/sample complexity, reductions | speedup 주장과 병목을 정직하게 평가 |
| 소프트웨어 공학 | versioning, contract, test pyramid, CI, observability, security | 연구 코드를 유지 가능한 시스템으로 전환 |

### 필수 검증 습관

모든 실험에서 다음 표를 채운다.

| 분류 | 기록할 항목 |
| --- | --- |
| 문제 | 입력 크기, sparsity, symmetry, boundary condition, target observable |
| 고전 기준 | algorithm, tolerance, wall time, memory, 정답 또는 reference value |
| 양자 표현 | qubit 수, encoding, ansatz/oracle, 측정 observable |
| 회로 | 논리 gate, transpiled gate, depth, two-qubit gate, ancilla |
| 실행 | simulator/QPU, noise model, shots, seed, backend calibration 시각 |
| 통계 | 평균, 분산·신뢰구간, 여러 seed, 실패·제외 기준 |
| 비용 | QPU 호출, classical compute, network/queue, 예상 금액 또는 quota |
| 결론 | 비교 기준, 유효 범위, 반례·한계, 다음 실험 |

### SDK 선택 원칙

- **Qiskit**: circuit, quantum information, transpiler, provider/primitives와 IBM 생태계를 깊게 볼 때 주력으로 삼기 좋다.
- **PennyLane**: parameterized circuit, autodiff, hybrid QML·quantum chemistry 실험을 ML framework와 연결할 때 유용하다.
- **Cirq**: device-aware circuit, moment, noise channel과 Google 계열 simulator model을 비교 학습할 때 좋다.
- **OpenQASM 3**: gate와 classical control을 교환 가능한 텍스트 표현으로 이해하는 데 사용한다.
- **QIR/MLIR/LLVM**: 언어·중간 표현·최적화 pass·target lowering을 설계하는 compiler 트랙에서 사용한다.

이 도구를 모두 같은 깊이로 익힐 필요는 없다. 주력 SDK로 end-to-end 프로젝트를 만들고, 두 번째 SDK는 작은 회로의 의미와 결과가 일치하는지 확인하는 데 사용한다.

## 직무별 전문 트랙

### A. 양자 알고리즘 설계자

먼저 PDE·물성·최적화 중 하나를 주 도메인으로 고른다. 각 도메인의 고전 solver를 구현하고 오차와 복잡도를 설명한 뒤 양자 encoding을 설계한다.

- PDE: finite difference/spectral baseline → sparse linear system → HHL/QLSA 전제 → variational PDE/QPINN → QLBM
- 물성: HF/DFT → second quantization·active space → VQE/QPE/QSCI/SQD → DMFT/DMRG·embedding과 비교
- 최적화: exact/heuristic baseline → QUBO/Ising 변환 → QAOA/annealing 계열 → approximation ratio·sample complexity
- 필수 산출물: 입력·출력 비용이 포함된 복잡도 표, 고전 대비 오차·자원 benchmark, fault-tolerant resource estimate

상세 과정은 [02_algorithm_and_science_track.md](guide/02_algorithm_and_science_track.md)를 따른다.

### B. 양자 회로 검증 및 개발자

- statevector/unitary/density-matrix 수준의 reference oracle 작성
- shot noise와 physical noise 분리, seed와 confidence interval 관리
- circuit equivalence, permutation/layout, measurement mapping 검증
- basis translation, placement, routing, scheduling 전후 자원 비교
- VQE·QAOA·QSCI·SQD workflow에서 quantum step와 classical step 계약 테스트
- 필수 산출물: property-based circuit test, noisy regression suite, transpiler differential test

### C. 양자 기계학습 전문가

- classical ML의 train/validation/test, leakage, calibration, strong baseline부터 학습
- data encoding과 feature map이 만드는 inductive bias 분석
- DQC/QNN의 parameter-shift gradient와 실행 횟수 계산
- barren plateau, shot noise, optimizer instability를 별도로 진단
- variational model과 quantum kernel을 같은 split·metric·budget에서 비교
- 필수 산출물: 여러 seed와 ablation, classical kernel/NN baseline, 회로 평가 횟수와 wall-time 보고서

B와 C의 상세 과정은 [03_circuit_and_qml_track.md](guide/03_circuit_and_qml_track.md)를 따른다.

### D. 양자 소프트웨어 아키텍처 설계자

- circuit/program, backend capability, job, result, credential을 독립 contract로 모델링
- provider adapter와 domain service를 분리하고 version/capability negotiation 설계
- sync API 위에 async job을 숨기지 않고 queue·cancel·timeout·retry를 명시
- provenance, calibration snapshot, cost, audit log와 secret boundary 설계
- simulator→QPU 전환이 business logic을 바꾸지 않도록 contract test 작성

### E. 양자 회로 컴파일러 개발자

- lexer/parser, AST, SSA, CFG, dataflow, rewrite, legality, lowering의 compiler 기본기
- circuit DAG와 dynamic circuit의 control/data dependency
- OpenQASM 3 → high-level quantum IR → MLIR/QIR/LLVM 계열 → target ISA 흐름
- decomposition, synthesis, placement, routing, scheduling, peephole 최적화
- equivalence와 hardware constraint를 깨지 않는 pass 검증
- Clifford+T, T-count/T-depth, magic-state와 QEC overhead를 포함한 자원 추정

### F. 양자-클래식 통합 개발자

- Python front-end, provider-neutral middle-end, C++/Rust execution service의 역할 분리
- parameter sweep와 Hamiltonian term batching, async future, MPI/GPU/QPU 자원 배치
- scheduler·container·artifact store·telemetry와 QPU queue 연결
- idempotency key, checkpoint, retry budget, partial result, cancellation 설계
- credential·tenant·data residency·공급자 비용의 운영 경계 정의

D~F의 상세 과정은 [04_architecture_compiler_hybrid_track.md](guide/04_architecture_compiler_hybrid_track.md)를 따른다.

## 용어 정리

| 용어 | 뜻과 이 로드맵에서의 역할 |
| --- | --- |
| QPINN | Quantum Physics-Informed Neural Network. PDE residual·초기/경계 조건을 loss에 넣고 parameterized quantum circuit를 함수 근사기로 사용하는 연구 계열이다. 통일된 단일 알고리즘명이 아니므로 논문별 encoding과 gradient 정의를 확인한다. |
| QLBM | Quantum Lattice Boltzmann Method. lattice Boltzmann/transport update를 양자 회로로 표현하는 연구 계열이다. 충돌·streaming·boundary와 readout 비용을 함께 평가한다. |
| HHL/QLSA | 선형계 해에 비례하는 양자 상태를 준비하는 quantum linear systems algorithm 계열이다. 일반적으로 전체 해 벡터를 고전적으로 출력하는 알고리즘이 아니다. |
| Spectral method | 전역 basis로 함수·미분 연산을 근사하는 수치 기법이다. 양자 PDE에서는 선형계·block encoding과 결합되지만 smoothness·conditioning 조건이 중요하다. |
| DFT | Density Functional Theory. 전자 밀도 기반의 고전 electronic-structure 방법이며 양자 계산의 문제·baseline을 제공한다. |
| DMFT | Dynamical Mean-Field Theory. 격자 many-body 문제를 self-consistent impurity problem으로 다루는 고전 계산 framework다. |
| DMRG | Density Matrix Renormalization Group. MPS/MPO tensor network로 저에너지 상태를 근사하는 고전 알고리즘이다. |
| VQE | Variational Quantum Eigensolver. quantum circuit의 expectation을 고전 optimizer가 최소화하는 hybrid eigensolver다. |
| QAOA | Quantum Approximate Optimization Algorithm. alternating cost/mixer circuit의 parameter를 최적화하는 조합 최적화용 variational algorithm이다. |
| QSCI | Quantum-Selected Configuration Interaction. 양자 측정에서 중요한 configuration을 선택하고 고전 부분공간에서 Hamiltonian을 대각화하는 방법 계열이다. |
| SQD | Sample-based Quantum Diagonalization. noisy sample을 회복·선별하고 부분공간 대각화를 반복하는 quantum-centric hybrid workflow다. QSCI와 관련되지만 구현·후처리 절차가 동일한 동의어는 아니다. |
| DQC | 이 로드맵에서는 Differentiable Quantum Circuit을 뜻하며 circuit parameter 또는 입력에 대한 미분을 계산해 end-to-end 학습하는 회로 모델이다. Dynamic Quantum Circuit 또는 Distributed Quantum Computing도 DQC로 줄일 수 있으므로 첫 등장 때 전체 이름을 적는다. |
| PSR | Parameter-Shift Rule. 특정 generator를 가진 gate의 미분을 이동된 parameter에서 측정한 expectation의 선형 결합으로 계산한다. |
| QNN | Quantum Neural Network. parameterized quantum circuit와 측정을 학습 모델로 보는 넓은 명칭이며, 표현력이나 양자 우위를 자동으로 보장하지 않는다. |
| QIR | Quantum Intermediate Representation. LLVM IR 기반으로 quantum program과 runtime interface를 표현하는 사양이다. |
| MLIR | Multi-Level Intermediate Representation. 여러 abstraction level의 dialect와 rewrite/lowering을 구성하는 compiler infrastructure다. |
| ISA | Instruction Set Architecture. backend가 실제로 허용하는 gate, connectivity, timing, classical control 제약의 계약이다. |
| NISQ | 오류보정 없이 noise가 큰 현재·근시기 장치를 가리키는 범주다. fault-tolerant 알고리즘 가정과 분리한다. |
| FTQC | Fault-Tolerant Quantum Computing. logical qubit과 quantum error correction을 사용해 큰 계산의 오류 전파를 제어하는 실행 모델이다. |

## 실습 학습 가이드

시작점은 [guide/README.md](guide/README.md)다.

- [01_common_foundations.md](guide/01_common_foundations.md): 공통 40주 과정과 단계별 통과 기준
- [02_algorithm_and_science_track.md](guide/02_algorithm_and_science_track.md): PDE·물성·최적화 알고리즘 설계
- [03_circuit_and_qml_track.md](guide/03_circuit_and_qml_track.md): 회로 검증과 QML
- [04_architecture_compiler_hybrid_track.md](guide/04_architecture_compiler_hybrid_track.md): architecture·compiler·Quantum-HPC
- [05_portfolio_and_assessment.md](guide/05_portfolio_and_assessment.md): 포트폴리오와 평가 rubric
- [01_foundations.ipynb](guide/01_foundations.ipynb): statevector, gate, Bell state, sampling, 검증
- [02_practice.ipynb](guide/02_practice.ipynb): VQE·QAOA toy model과 PDE/HHL 타당성 점검
- [03_advanced.ipynb](guide/03_advanced.ipynb): parameter-shift, compiler pass, scheduling, hybrid job 상태기계

노트북은 NumPy만으로 실행되며 SDK와 QPU 계정이 없어도 핵심 원리와 검증 습관을 연습할 수 있다. 이후 공식 Qiskit/PennyLane/Cirq 예제로 같은 실험을 옮겨 구현한다.

## 다음 학습 경로

1. [guide/README.md](guide/README.md)의 진단표로 현재 단계를 정한다.
2. 공통 과정에서 부족한 gate만 통과하고, 모든 과목을 무조건 처음부터 반복하지 않는다.
3. 여섯 트랙 중 **주력 하나와 보조 하나**를 선택한다.
4. 세 노트북을 순서대로 실행하고 assertion과 실험표를 자신의 결과로 채운다.
5. [05_portfolio_and_assessment.md](guide/05_portfolio_and_assessment.md)의 capstone을 12주 동안 수행한다.
6. 공식 SDK로 이식한 뒤 simulator, fake/noisy backend, 가능하면 실제 QPU 순으로 검증한다.
7. 최종 보고서에는 성공 결과뿐 아니라 실패한 가정, 고전 baseline과 현재 hardware에서의 한계를 남긴다.

첫 주에 정할 것은 ‘어떤 SDK를 쓸까’가 아니라 ‘어떤 문제를 어떤 observable과 기준으로 검증할까’다. 도구는 그 결정을 구현하는 수단으로 선택한다.
