# 공통 기반 40주 과정

이 과정은 여섯 직무가 공유하는 최소 기반이다. 주 10~12시간을 가정하지만, 각 단계의 exit gate를 통과하면 기간을 줄일 수 있다.

## 0단계: 재현 가능한 계산 환경 — 1~2주

### 학습

- Python 가상환경, package pinning과 lock file
- NumPy array, complex dtype, shape와 broadcasting
- Git, 작은 commit, README와 실행 명령
- assertion, unit test, fixture, deterministic random seed
- benchmark에서 wall time, memory, 입력 크기를 기록하는 법

### 실습

1. Hermitian matrix를 생성하고 eigenpair residual `||Av - λv||`를 검사한다.
2. 같은 seed에서 같은 결과가 나오는 작은 Monte Carlo 실험을 만든다.
3. 실패하는 입력과 허용오차를 명시한 테스트를 작성한다.

### 통과 기준

- 깨끗한 환경에서 한 명령으로 실행 가능하다.
- Python과 dependency version, OS, seed가 결과에 기록된다.
- 정상·경계·실패 사례 테스트가 모두 있다.

## 1단계: 수학·수치해석 — 3~10주

### 1~2주: 복소 선형대수

- vector space, inner product, basis, tensor/Kronecker product
- unitary, Hermitian, projector, spectral decomposition, SVD
- sparse matrix, eigenproblem, norm와 condition number

### 3~4주: 확률·통계

- random variable, expectation, variance, Bernoulli·multinomial sampling
- estimator, bias, standard error, confidence interval와 bootstrap
- 여러 seed, multiple comparison과 cherry-picking 방지

### 5~6주: 최적화

- convex/non-convex, gradient와 Hessian, constraint
- gradient descent, quasi-Newton, stochastic·gradient-free optimizer
- discrete optimization, QUBO, local search와 approximation ratio

### 7~8주: 수치해석·PDE

- floating-point error, consistency, stability, convergence
- finite difference, iterative linear solver와 preconditioning
- Fourier/Chebyshev spectral method
- ODE/PDE, initial/boundary condition와 nondimensionalization

### 실습과 gate

- 1D Poisson equation을 finite difference와 spectral baseline으로 풀고 grid별 `L2`, `L∞`, condition number를 비교한다.
- optimizer 세 가지를 같은 evaluation budget에서 비교한다.
- exact eigensolver와 iterative method를 같은 tolerance로 비교한다.
- “더 빠르다”는 결론에 전처리, 초기화와 결과 검사 시간을 포함한다.

통과 기준은 정확한 해 또는 고정밀 reference와의 오차, 수렴 경향과 실패 조건을 설명하는 것이다.

## 2단계: 양자역학·양자 정보 — 11~18주

### 학습 순서

1. ket/bra, amplitude, normalization, global·relative phase
2. Born rule, projective measurement와 expectation value
3. single-qubit Bloch sphere와 Pauli operator
4. composite system과 tensor product
5. entanglement, Bell state, reduced density matrix와 entropy
6. mixed state, quantum channel, Kraus operator
7. no-cloning, teleportation, superdense coding
8. Hamiltonian evolution, phase estimation과 measurement basis

### 실습

- [01_foundations.ipynb](01_foundations.ipynb)을 실행하고 계산을 손으로 다시 유도한다.
- Bell state의 density matrix에서 partial trace를 직접 구현한다.
- shot 수를 바꾸며 표본 오차가 대략 `1/sqrt(shots)`로 감소하는지 여러 seed로 확인한다.
- bit flip, phase flip, depolarizing channel을 density matrix에 적용한다.

### 통과 기준

- global phase와 relative phase를 구분한다.
- pure state와 mixed state, shot noise와 physical noise를 구분한다.
- partial trace와 measurement probability의 shape·index 순서를 테스트한다.
- statevector는 실제 QPU에서 그대로 읽을 수 있는 출력이 아님을 설명한다.

권장 입문 자료는 [IBM Basics of Quantum Information](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information)이다.

## 3단계: 회로·SDK·noise — 19~26주

### 학습

- gate, circuit, register/wire, parameter binding, measurement
- Qiskit 또는 PennyLane 중 주력 하나, Cirq 또는 나머지 SDK 중 비교 하나
- statevector, density-matrix, shot-based simulation의 출력 계약
- bit/qubit ordering과 endianness
- basis gate, coupling map, layout, routing, SWAP, scheduling
- noise channel, readout error와 calibration snapshot

### 실습

1. Bell, GHZ, phase kickback, 작은 QFT를 두 SDK로 구현한다.
2. bit order를 정규화해 state와 distribution을 비교한다.
3. ideal → finite-shot → synthetic noise 순으로 한 요인씩 추가한다.
4. transpilation 전후 unitary/state/distribution과 depth·2-qubit gate 수를 비교한다.
5. random seed와 compiler optimization level을 바꾼 분포를 보고한다.

### 통과 기준

- logical circuit와 ISA circuit를 구분한다.
- 작은 unitary는 global phase까지 허용한 equivalence를 검사한다.
- measurement 회로는 classical-bit mapping을 포함해 통계적으로 비교한다.
- transpiled circuit의 layout을 observable에도 반영해야 함을 설명한다.

SDK 버전과 현재 API는 [출처 기록](../sources.md)을 확인하되, 실습 당일 공식 migration guide를 다시 본다.

## 4단계: 알고리즘과 성능 주장 — 27~34주

### 학습

- query, gate, sample, space complexity의 차이
- phase estimation, amplitude amplification/estimation, Hamiltonian simulation
- VQE, QAOA와 variational loop의 오류 분해
- HHL/QLSA의 sparse access, condition number, precision과 output model
- NISQ physical execution과 fault-tolerant logical algorithm의 차이
- classical dequantization과 강한 baseline의 중요성

### 실습

- [02_practice.ipynb](02_practice.ipynb)의 exact diagonalization·VQE·QAOA를 비교한다.
- 같은 선형계에 direct solver, iterative solver와 “해 상태에서 관측량 추출” 계약을 각각 적는다.
- qubit, ancilla, depth, two-qubit gate, shots, optimizer evaluation을 자원표에 넣는다.

### 통과 기준

- HHL이 일반적으로 전체 해 벡터가 아니라 해에 비례하는 상태를 준비함을 설명한다.
- asymptotic complexity와 현재 작은 구현의 wall time을 혼동하지 않는다.
- state preparation·readout을 제외한 속도 향상 주장을 반려할 수 있다.
- 정확도, 성공 확률과 비용의 trade-off를 여러 입력 크기로 보고한다.

## 5단계: 소프트웨어·시스템 공학 — 35~40주

### 학습

- package architecture, interface segregation, dependency inversion
- circuit/program, backend capability, job, result와 provenance contract
- async queue, timeout, cancellation, retry와 idempotency
- checkpoint, artifact store, structured log, metric와 distributed trace
- credential, least privilege, tenant, data residency와 비용 한도
- parser/AST/SSA/CFG, rewrite, legality, lowering의 compiler 입문
- container, scheduler, MPI/GPU/QPU 자원 배치의 HPC 입문

### 실습

1. simulator와 mock QPU가 같은 `Backend` contract를 구현하게 한다.
2. 중복 idempotency key가 같은 job을 반환하는지 테스트한다.
3. timeout 뒤 재시작해 checkpoint에서 이어지는 workflow를 만든다.
4. gate cancellation pass가 회로 의미를 보존하는지 differential test를 작성한다.
5. backend capability가 맞지 않을 때 compile 전에 명확히 거부한다.

[03_advanced.ipynb](03_advanced.ipynb)은 이 단계의 축소 실습이다.

### 통과 기준

- happy path뿐 아니라 timeout, partial failure, duplicate submit과 cancellation을 테스트한다.
- secret를 circuit/result artifact와 분리한다.
- job 결과가 code·config·backend·calibration·seed에 연결된다.
- compiler rewrite가 legality와 equivalence를 모두 통과한다.

## 공통 졸업 심사

다음 네 artifact를 제출한다.

1. 수학 노트: 핵심 수식, 가정과 작은 손 계산
2. 검증 코드: exact oracle, property/unit/integration test
3. 실험 보고서: 여러 seed, confidence interval, 자원표와 실패 사례
4. architecture note: 입력→compile→execute→result 흐름과 신뢰 경계

아래 항목 중 하나라도 있으면 전문 트랙 진입 전에 재작업한다.

- 고전 reference 없이 작은 quantum result만 제시
- seed, shots, version 또는 backend 미기록
- simulator 결과를 실제 장치 성능으로 서술
- output contract가 다른 방법의 runtime을 직접 비교
- failed experiment 또는 제한 사항을 삭제
