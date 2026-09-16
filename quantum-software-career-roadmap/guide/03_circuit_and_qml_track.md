# 양자 회로 검증 개발자·양자 기계학습 전문가 트랙

작성일: 2026-09-13

## 목차

- [과정의 목표와 권장 순서](#과정의-목표와-권장-순서)
- [공통 선수지식과 진단](#공통-선수지식과-진단)
- [SDK와 API 기준 스냅샷](#sdk와-api-기준-스냅샷)
- [트랙 B: 양자 회로 검증 및 개발](#트랙-b-양자-회로-검증-및-개발)
- [트랙 C: 양자 기계학습](#트랙-c-양자-기계학습)
- [공통 실험·평가 계약](#공통-실험평가-계약)
- [포트폴리오와 최종 통과 기준](#포트폴리오와-최종-통과-기준)
- [공식 자료와 원 논문](#공식-자료와-원-논문)

## 과정의 목표와 권장 순서

이 문서는 다음 두 역할을 준비하는 전문 트랙이다.

- **양자 회로 검증 및 개발자**: 회로를 구현하는 데 그치지 않고, 이상적 의미, 유한 shot 통계, noise, transpilation과 실제 backend 제약을 분리해 검증한다.
- **양자 기계학습 전문가**: 미분 가능 양자 회로와 고전 학습기를 연결하고, gradient·trainability·일반화·고전 기준선을 포함한 공정한 실험을 설계한다.

두 트랙을 함께 공부한다면 아래 순서를 권장한다.

    공통 선수지식
      → 회로 표현과 이상적 검증
        → shot·noise·transpilation 검증
          ├─ 회로 트랙: VQE/QAOA → QSCI/SQD → 검증 capstone
          └─ QML 트랙: DQC/PSR → QNN/hybrid → feature map/kernel
                       → barren plateau → 공정한 benchmark capstone

주 10~12시간을 기준으로 각 전문 트랙은 16주 과정이다. 두 트랙을 모두 이수하면 중복되는 회로·통계 단계를 제외해 약 26~28주가 필요하다. 기간을 채우는 것보다 각 단계의 **통과 기준을 증거와 함께 만족하는 것**이 중요하다.

양자 기계학습 지원자도 트랙 B의 1~7주차를 먼저 이수해야 한다. 그렇지 않으면 모델 성능 저하가 feature map, 최적화, shot noise, 물리적 noise, transpilation 중 어디서 생겼는지 분리하기 어렵다.

## 공통 선수지식과 진단

### 필요한 배경

| 영역 | 최소 선수지식 | 진단 과제 |
| --- | --- | --- |
| Python | 함수·클래스·가상환경·NumPy·pytest·plotting | seed와 환경 정보를 기록한 재실행 가능한 작은 수치 실험 |
| 선형대수 | 복소 벡터, 내적, tensor product, unitary, Hermitian, eigenproblem | H·X·CX 행렬로 Bell state를 직접 계산 |
| 확률·통계 | 표본 평균·분산, binomial, 신뢰구간, bootstrap | 100·1,000·10,000 shots의 추정 오차 비교 |
| 양자 정보 | ket/bra, Born rule, 중첩, 얽힘, 측정, density matrix | Bell state의 statevector·density matrix·부분계를 설명 |
| 최적화 | gradient, finite difference, local minimum, constrained/discrete optimization | 간단한 비선형 목적함수를 두 optimizer로 비교 |
| 고전 ML | split, leakage, scaling, loss, SVM, MLP, calibration | 동일 split에서 logistic regression·RBF-SVM·MLP 비교 |
| 소프트웨어 공학 | Git, test pyramid, CI, dependency pinning | 깨지는 사례를 먼저 작성한 regression test |

### 선수 단계 통과 기준

다음을 모두 만족해야 전문 과정으로 이동한다.

1. SDK 없이 NumPy만으로 1·2-qubit state evolution과 Born probability를 구현한다.
2. global phase와 relative phase의 차이를 예제로 설명한다.
3. 순수 상태와 혼합 상태, shot noise와 physical noise를 구분한다.
4. Qiskit의 bit-string 순서가 회로 그림의 qubit 순서와 어떻게 다른지 테스트로 보인다.
5. 한 번의 실행값이 아니라 여러 seed의 평균, 분산 또는 신뢰구간을 보고한다.
6. 고전 ML에서 test set을 모델·hyperparameter 선택에 사용하지 않는다.

공통 이론은 IBM의 [Basics of Quantum Information](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information)과 [Qiskit bit ordering](https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering)을 먼저 학습한다.

## SDK와 API 기준 스냅샷

> **중요:** 아래 버전과 API 경계는 2026-09-13에 확인한 **학습 자료 작성용 스냅샷**이다. 설치 시점에는 반드시 각 프로젝트의 공식 설치 문서, release notes와 migration guide를 다시 확인하고, 실제 사용 버전을 lock 파일과 결과 보고서에 기록한다.

| 도구 | 2026-09-13 확인 스냅샷 | 학습 자료에서의 경계 |
| --- | --- | --- |
| Qiskit SDK | 공식 예제의 권장선은 Qiskit 2.5.2 계열 | V2 Primitive, PUB 입력, **StatevectorEstimator**·**StatevectorSampler** 중심 |
| Qiskit IBM Runtime | 공식 로컬 테스트 예제는 0.47 계열 | 실제 QPU·fake backend·실행 mode는 별도 패키지 |
| Qiskit Aer | 공식 문서는 0.17 계열 | 고성능·density-matrix·noise simulation은 별도 설치 |
| Qiskit Optimization | 공식 문서는 0.7.0 | VQE·QAOA와 일부 optimizer는 **qiskit_optimization** 경로를 우선 |
| Qiskit Machine Learning | 공식 문서는 0.9.1 | QNN, kernel, gradient, **TorchConnector**는 별도 패키지 |
| Qiskit SQD addon | 공식 문서는 0.13.1 | **qiskit-addon-sqd**를 별도 설치 |
| PennyLane | 공식 문서는 0.45.1, Python 3.11 이상 | 문서 표준 별칭은 **import pennylane as qp**, PyTorch·JAX 중심 |
| Cirq | 공식 릴리스 1.7.0, Python 3.11 이상 | core와 **cirq-google** 등 공급자 패키지를 구분 |

### 오래된 예제를 옮길 때 확인할 사항

- Qiskit의 V1 Primitive 예제를 그대로 사용하지 말고 [현재 Primitive 개요](https://quantum.cloud.ibm.com/docs/en/guides/primitives)와 대조한다.
- Qiskit Optimization 0.7은 VQE, QAOA, 일부 optimizer를 자체 package로 옮겼다. [0.7 migration guide](https://qiskit-community.github.io/qiskit-optimization/migration/03_migration_guide_to_v0.7.html)를 따른다.
- Qiskit Machine Learning 0.9는 Qiskit 2.x와 V2 Primitive 중심으로 바뀌었고, 일부 gradient·optimizer·state-fidelity API를 자체 package로 옮겼다. [0.9.1 release notes](https://qiskit-community.github.io/qiskit-machine-learning/release_notes.html)를 확인한다.
- Qiskit Nature처럼 여전히 **qiskit-algorithms**에 의존하는 package도 있으므로 하나의 import 규칙을 모든 프로젝트에 강제하지 않는다.
- PennyLane 0.45 문서는 **qp** 별칭을 쓴다. Python import 별칭은 사용자가 정할 수 있지만 신규 자료는 현재 문서와 같은 표기를 사용한다.
- PennyLane의 TensorFlow 지원과 **KerasLayer**는 제거되었다. 신규 hybrid 학습은 PyTorch 또는 JAX를 기본으로 한다.
- SDK별 가상환경을 분리한다. 하나의 환경에 모든 provider plugin을 무제한 설치하지 않는다.
- credential은 환경 변수나 공식 credential store에 두고 notebook, 로그, Git에 포함하지 않는다.

## 트랙 B: 양자 회로 검증 및 개발

### 1~2주차: 회로 표현과 세 SDK의 실행 의미

#### 학습 내용

- qubit/wire, gate, circuit, parameter, measurement, observable
- Qiskit **QuantumCircuit**, PennyLane **QNode**, Cirq **Circuit**·**Moment**
- tensor order, qubit order, classical register와 measurement key
- parameter binding과 parameter sweep
- statevector simulation과 sampling 실행의 의미 차이
- statevector는 소규모 simulator에서 쓰는 정답 oracle이며 실제 QPU에서 직접 읽는 값이 아니라는 경계

#### 필수 실습

1. Bell, GHZ, phase-kickback, 작은 QFT를 Qiskit·PennyLane·Cirq에서 각각 구현한다.
2. 같은 qubit order로 정규화한 뒤 statevector를 비교한다.
3. measurement를 추가하고 100·1,000·10,000 shots의 histogram을 비교한다.
4. Qiskit **StatevectorEstimator**와 **StatevectorSampler**의 출력 계약을 비교한다.
5. Cirq **simulate()**와 **run(repetitions=...)**의 차이를 테스트한다.
6. PennyLane **shots=None**과 **qp.set_shots(...)**를 비교한다.

#### 제출 증거

- 세 SDK의 dependency lock
- qubit/bit mapping 표
- ideal state와 sample distribution을 검사하는 pytest
- seed, shots, dtype가 포함된 실행 metadata

#### 통과 기준

- ideal unitary 회로가 global phase를 제외하고 같은 상태를 만든다.
- bit-order를 임의로 뒤집지 않고 명시적 mapping 함수와 테스트로 처리한다.
- finite-shot 결과가 exact probability와 완전히 같아야 한다고 주장하지 않는다.
- 측정이 있는 회로와 없는 회로의 검증 방법이 다른 이유를 설명한다.

### 3~4주차: Shot 통계와 Noise 모델

#### 학습 내용

- sample, count, probability, expectation, variance
- shot 수와 표준오차의 관계
- statevector, trajectory, density-matrix simulation
- bit/phase flip, depolarizing, amplitude damping, thermal relaxation, readout error
- gate noise와 measurement noise
- 사용자 정의 toy noise와 backend snapshot 기반 noise의 차이
- simulator noise model은 실제 장비를 완전히 재현하는 것이 아니라는 한계

#### 필수 실습

1. GHZ 회로에 noise channel을 하나씩 추가한다.
2. Qiskit Aer **AerSimulator**, PennyLane **default.mixed**, Cirq **DensityMatrixSimulator**를 비교한다.
3. shot 수와 noise strength를 이중 sweep한다.
4. exact distribution 대비 total variation distance 또는 Hellinger distance를 계산한다.
5. 여러 seed로 평균·표준편차·bootstrap confidence interval을 만든다.
6. readout error와 gate error를 분리한 ablation을 수행한다.

#### 통과 기준

- shot noise와 physical noise의 영향을 별도 그래프로 보고한다.
- seed 하나의 좋은 결과를 대표값으로 선택하지 않는다.
- rare outcome의 기대 count가 작을 때 부적절한 카이제곱 근사를 피하고 bootstrap 또는 적절한 exact 방법을 선택한다.
- 사용한 channel, error rate, shots, simulator method를 결과에 기록한다.

공식 실습 출발점:

- [Qiskit noise model 구축](https://quantum.cloud.ibm.com/docs/en/guides/build-noise-models)
- [Qiskit Aer](https://qiskit.github.io/qiskit-aer/)
- [PennyLane DefaultMixed](https://docs.pennylane.ai/en/stable/code/api/pennylane.devices.DefaultMixed.html)
- [Cirq noisy simulation](https://quantumai.google/cirq/simulate/noisy_simulation)

### 5~7주차: Transpilation과 의미 보존 검증

#### 학습 내용

- target basis gate, coupling map, layout, placement, routing, SWAP, scheduling
- Qiskit staged pass의 init/layout/routing/translation/optimization/scheduling
- Cirq transformer와 target gateset
- PennyLane transform과 **qp.specs**
- logical circuit와 physical/ISA circuit
- transpilation 후 observable에도 layout을 적용해야 하는 이유
- exact transformation과 approximate synthesis의 차이

#### 검증 사다리

1. **정적 검증**: unbound parameter, 지원하지 않는 gate, coupling·target 위반을 검사한다.
2. **Operator 검증**: 작은 unitary 회로는 global phase까지 허용해 원본과 변환본을 비교한다.
3. **State 검증**: basis input과 seeded random input에 대한 state fidelity를 비교한다.
4. **측정 의미 검증**: terminal measurement와 classical-bit permutation을 반영해 분포를 비교한다.
5. **Noise 검증**: 같은 noise 가정과 shot budget에서 여러 반복의 통계량을 비교한다.
6. **자원 회귀 검증**: depth, 1·2-qubit gates, SWAP, circuit size를 전후 비교한다.

#### 필수 실습

- 서로 다른 coupling map과 optimization level 0~3에서 같은 회로를 transpile한다.
- transpiler seed를 바꿔 depth와 2-qubit gate 수 분포를 만든다.
- Qiskit **Operator.equiv** 또는 process fidelity로 작은 회로를 검증한다.
- Cirq **assert_allclose_up_to_global_phase**와 terminal-measurement equivalence helper를 사용한다.
- layout 전후 observable 결과가 잘못 달라지는 실패 테스트를 작성하고 수정한다.
- approximation을 허용한 synthesis와 exact synthesis를 서로 다른 tolerance로 평가한다.

#### 통과 기준

- 대상 backend의 ISA 위반이 0건이다.
- unitary-only 회로는 정한 수치 tolerance 안에서 의미가 보존된다.
- measurement 회로는 qubit·classical-bit permutation을 명시적으로 처리한다.
- transpilation 후 **observable.apply_layout(isa_circuit.layout)**에 해당하는 변환을 빠뜨리지 않는다.
- 최적화가 depth를 줄였다는 사실만으로 알고리즘 결과가 같다고 단정하지 않는다.
- 검증 결과와 resource regression 결과를 별도 항목으로 보고한다.

공식 자료:

- [Qiskit transpilation](https://quantum.cloud.ibm.com/docs/en/guides/transpile)
- [Qiskit Operator API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Operator)
- [Qiskit ISA circuit와 observable layout 예제](https://quantum.cloud.ibm.com/docs/en/guides/hello-world)
- [Cirq circuit transformers](https://quantumai.google/cirq/transform/transformers)
- [Cirq global-phase 비교](https://quantumai.google/reference/python/cirq/testing/assert_allclose_up_to_global_phase)
- [PennyLane circuit inspection](https://docs.pennylane.ai/en/stable/introduction/inspecting_circuits.html)

### 8~11주차: VQE와 QAOA

#### VQE

VQE(Variational Quantum Eigensolver)는 parameterized trial state의 Hamiltonian expectation을 양자 측정으로 추정하고 고전 optimizer로 낮추는 hybrid eigensolver다.

학습 내용:

- Rayleigh–Ritz variational principle
- Hamiltonian의 Pauli decomposition과 commuting measurement group
- initial state, ansatz, observable, Estimator, optimizer
- ansatz error, optimization error, sampling error, device error의 분해
- analytic, finite-shot, noisy 실행 차이

실습:

1. 1-qubit Hamiltonian으로 VQE loop를 library 없이 구현한다.
2. 4~8-qubit Heisenberg chain을 exact diagonalization과 비교한다.
3. 선택 과제로 H₂ active-space Hamiltonian을 사용한다.
4. COBYLA, SPSA와 gradient 기반 optimizer를 여러 seed에서 비교한다.
5. ansatz depth·shots·noise strength ablation을 수행한다.

평가 지표:

- ground-state energy absolute error
- exact eigenstate를 구할 수 있을 때 state fidelity
- optimizer iteration과 circuit evaluation 수
- shots와 confidence interval
- logical/transpiled depth와 2-qubit gate 수
- particle·spin 등의 symmetry violation

화학 문제에서만 약 1.6 mHa의 chemical accuracy를 별도 기준으로 사용할 수 있다. noise가 있는 estimator 결과가 variational upper bound를 위반할 수 있으므로 에너지가 내려갔다는 사실만으로 더 정확해졌다고 단정하지 않는다.

#### QAOA

QAOA(Quantum Approximate Optimization Algorithm)는 조합 최적화 문제를 cost Hamiltonian으로 옮기고 cost·mixer evolution을 번갈아 적용하는 \(p\)-layer parameterized circuit를 고전적으로 최적화한다.

학습 내용:

- QUBO에서 Ising Hamiltonian으로의 변환
- cost·mixer Hamiltonian
- \(p\), \(\gamma\), \(\beta\), initial point
- constrained mixer, warm start와 parameter transfer
- \(p\) 증가에 따른 표현력·회로 깊이·noise trade-off

실습:

1. 4~12-node MaxCut의 brute-force optimum을 만든다.
2. \(p=1,2,3\)과 여러 optimizer·seed·shot 수를 비교한다.
3. exact, finite-shot, noisy, transpiled 실행을 분리한다.
4. 가장 좋은 한 sample뿐 아니라 전체 output distribution을 분석한다.

평가 지표:

- expected objective
- best-sample approximation ratio
- optimum success probability
- feasible-sample ratio
- circuit evaluation, shots, wall time
- \(p\)별 transpiled 2-qubit depth

#### VQE와 QAOA 단계 통과 기준

- 작은 문제의 exact classical answer를 먼저 계산한다.
- 동일한 initial point·seed·budget을 사용한 비교를 제공한다.
- energy 또는 best sample 하나만 보고하지 않는다.
- optimizer, ansatz 또는 \(p\)를 선택하는 데 test 결과를 사용하지 않는다.
- QPU time만이 아니라 mapping·transpilation·classical optimization까지 포함한 비용표를 작성한다.

공식 자료:

- [IBM variational algorithm 과정](https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/variational-quantum-algorithms)
- [Heisenberg-chain VQE](https://quantum.cloud.ibm.com/docs/en/tutorials/spin-chain-vqe)
- [QAOA tutorial](https://quantum.cloud.ibm.com/docs/en/tutorials/quantum-approximate-optimization-algorithm)
- [VQE 원 논문](https://doi.org/10.1038/ncomms5213)
- [QAOA 원 논문](https://arxiv.org/abs/1411.4028)

### 12~14주차: QSCI와 SQD

#### 개념 구분

| 항목 | QSCI | SQD |
| --- | --- | --- |
| 전체 이름 | Quantum-Selected Configuration Interaction | Sample-based Quantum Diagonalization |
| 기본 생각 | trial state를 측정해 중요한 basis configuration을 고른 뒤 그 subspace에서 고전 대각화 | 양자 sample로 만든 subspace에서 대각화하며 필요하면 sample recovery와 자기일관 반복 수행 |
| 양자 역할 | 상태 준비와 computational-basis sampling | 하나 이상의 상태 준비와 sampling |
| 고전 역할 | configuration 선택, projected Hamiltonian 구성·대각화 | postselection, configuration recovery, batching, 반복 대각화·수렴 판단 |
| 대표 평가축 | 선택한 subspace의 품질과 크기 | recovery·반복 수렴, batch 분산, 고전 solver 규모 |
| 관계 | selected-CI 관점의 구체적 hybrid 방법 | QSCI를 포함·확장해 설명할 수 있는 더 넓은 sample 기반 workflow |

둘은 밀접하지만 구현 절차가 항상 같은 동의어는 아니다.

#### 학습 내용

- second quantization, fermion-to-qubit mapping, Slater determinant
- selected CI와 full CI
- trial-state preparation과 computational-basis sampling
- Hamming weight, particle-number symmetry와 postselection
- projected sparse Hamiltonian과 eigensolver
- configuration recovery와 self-consistent iteration
- subspace sparsity 가정과 실패 조건
- quantum sampling 비용과 classical diagonalization 비용의 분리

#### 필수 실습

1. 작은 fermionic 또는 spin Hamiltonian의 exact ground state를 계산한다.
2. exact 또는 근사 trial state에서 sample을 생성한다.
3. QSCI 방식으로 상위 configuration을 골라 projected Hamiltonian을 대각화한다.
4. shot 수와 선택 configuration 수에 따른 energy convergence를 측정한다.
5. bit-flip noise를 추가하고 symmetry postselection과 configuration recovery를 비교한다.
6. Qiskit SQD addon으로 같은 문제의 iterative workflow를 구성한다.
7. subspace dimension별 고전 eigensolver 시간·메모리를 측정한다.

#### 통과 기준

- QSCI와 SQD의 양자 단계와 고전 단계를 각각 도식화한다.
- energy error, selected subspace dimension, shots를 함께 보고한다.
- postselection discard rate와 recovery 전후 오류를 보고한다.
- 여러 batch의 평균·분산과 iteration stopping rule을 기록한다.
- 고전 diagonalization 비용을 숨기지 않는다.
- 작은 문제에서 full-space exact diagonalization과 교차 검증한다.

자료:

- [QSCI 원 논문](https://arxiv.org/abs/2302.11320)
- [Qiskit SQD 개요](https://qiskit.github.io/qiskit-addon-sqd/)
- [SQD quickstart](https://qiskit.github.io/qiskit-addon-sqd/guides/quickstart.html)
- [IBM SQD chemistry tutorial](https://quantum.cloud.ibm.com/docs/en/tutorials/sample-based-quantum-diagonalization)
- [IBM SQD 연구 결과](https://research.ibm.com/publications/chemistry-beyond-the-scale-of-exact-diagonalization-on-a-quantum-centric-supercomputer)

### 15~16주차: 회로 검증 Capstone

다음 두 결과물을 하나의 재현 가능한 저장소로 묶는다.

1. **Cross-SDK circuit conformance harness**
   - Qiskit·PennyLane·Cirq 입력 adapter
   - unitary, state, terminal measurement, noisy distribution 검증
   - qubit·bit permutation 처리
   - 실패를 재현하는 regression fixture
2. **Hardware-aware algorithm benchmark**
   - VQE 또는 QAOA 하나와 QSCI 또는 SQD 하나
   - exact→shot→noise→transpiled 단계별 결과
   - accuracy와 resource를 함께 표시한 report

## 트랙 C: 양자 기계학습

### 1~2주차: 고전 ML 계약과 DQC 용어

#### DQC를 먼저 구분한다

이 트랙의 DQC는 **Differentiable Quantum Circuit, 미분 가능 양자 회로**를 뜻한다. 일부 문서가 **Dynamic Quantum Circuit, 동적 양자 회로**도 DQC로 줄이므로 문서·코드에서는 첫 등장 때 전체 이름을 적는다.

- Differentiable quantum circuit: 회로 parameter 또는 입력에 대한 output expectation의 미분을 계산해 학습한다.
- Dynamic quantum circuit: mid-circuit measurement와 classical feed-forward를 포함한다.

두 개념은 함께 사용될 수 있지만 같은 뜻이 아니다.

#### 학습 내용

- train/validation/test split과 data leakage
- scaling, feature selection, class imbalance
- logistic regression, linear·RBF SVM, 작은 MLP
- task metric, calibration, repeated seed
- parameterized quantum circuit의 입력·parameter·observable
- QML에서 data-loading 비용을 포함해야 하는 이유

#### 필수 실습과 통과 기준

- 하나의 작은 binary dataset에 세 고전 baseline을 구축한다.
- preprocessing은 training fold에서만 fit한다.
- validation으로 model을 선택하고 test는 마지막 한 번만 사용한다.
- accuracy 외 F1 또는 AUROC/AUPRC와 calibration metric을 보고한다.
- 이후의 모든 양자 모델이 사용하는 split과 tuning budget을 고정한다.

IBM의 [Quantum Machine Learning 과정](https://quantum.cloud.ibm.com/learning/en/courses/quantum-machine-learning)을 전체 개요로 사용한다.

### 3~4주차: Parameter-Shift Rule과 Gradient 검증

미분 가능 회로의 대표 출력은 다음처럼 쓸 수 있다.

\[
f(x,\theta)=
\langle 0|U^\dagger(x,\theta) O U(x,\theta)|0\rangle.
\]

Pauli rotation처럼 두 고윳값을 갖는 생성자의 표준 회전 gate는 다음 parameter-shift rule을 사용할 수 있다.

\[
\frac{\partial f}{\partial \theta}
=\frac{1}{2}
\left[
f\left(\theta+\frac{\pi}{2}\right)
-f\left(\theta-\frac{\pi}{2}\right)
\right].
\]

이 두 번 실행 공식은 모든 gate에 보편적으로 적용되지 않는다. generator spectrum에 따라 coefficient와 shift가 여러 개 필요한 generalized PSR을 사용하거나 지원되는 fallback을 선택해야 한다.

#### 학습 내용

- finite difference, simulator backpropagation, adjoint, PSR
- JVP, VJP와 higher-order derivative의 역할
- analytic mode와 finite-shot gradient
- parameter 수에 따른 회로 실행량
- input gradient와 trainable-weight gradient

#### 필수 실습

1. 1~4-qubit 회로에서 손으로 구한 derivative와 PSR을 비교한다.
2. PennyLane **backprop**, **adjoint**, **parameter-shift**, finite difference를 비교한다.
3. shots를 증가시키며 gradient bias·variance와 실행량을 측정한다.
4. Qiskit QNN backward 또는 gradient 결과를 유한차분과 교차 검증한다.
5. 특정 parameter가 실제로 trainable graph에서 끊긴 실패 사례를 테스트한다.

#### 통과 기준

- analytic simulation에서는 reference와 PSR이 정한 엄격한 수치 tolerance 내 일치한다.
- finite shots에서는 단일 gradient가 아니라 반복 추정의 평균·분산을 보고한다.
- simple PSR의 parameter별 실행 수와 전체 batch 비용을 계산한다.
- gradient가 존재한다는 사실과 model이 잘 학습된다는 사실을 구분한다.

공식·원 출처:

- [PennyLane gradients and training](https://docs.pennylane.ai/en/stable/introduction/interfaces.html)
- [PennyLane parameter-shift API](https://docs.pennylane.ai/en/stable/code/api/pennylane.gradients.param_shift.html)
- [Parameter-shift 원 논문](https://doi.org/10.1103/PhysRevA.99.032331)

### 5~8주차: QNN Architecture와 Hybrid 학습

QNN(Quantum Neural Network)은 고전 neural network의 neuron 구조를 그대로 양자화했다는 뜻이 아니다. 여기서는 parameterized circuit와 measurement가 미분 가능한 학습 block을 이루는 넓은 의미로 사용한다.

    classical preprocessing
      → data encoding / feature map
        → trainable ansatz
          → measurement / observable
            → classical head, loss, optimizer

#### 학습 내용

- basis, angle, amplitude encoding과 data re-uploading
- hardware-efficient ansatz와 problem-inspired ansatz
- entanglement topology, depth, parameter sharing
- observable 선택과 output shape
- Qiskit **EstimatorQNN**과 **SamplerQNN**
- PennyLane **QNode**와 PyTorch **TorchLayer** 또는 JAX
- classical encoder·quantum layer·classical head
- mini-batch, gradient accumulation, shot budget

#### 필수 실습

1. 2차원 synthetic binary dataset에 variational quantum classifier를 만든다.
2. 같은 입력을 **EstimatorQNN**과 **SamplerQNN**으로 구현해 출력 의미를 비교한다.
3. PennyLane QNode를 **TorchLayer**로 감싸 hybrid model을 학습한다.
4. exact, finite-shot, noisy 학습을 분리한다.
5. no-entanglement, randomized feature, fixed quantum layer, trainable quantum layer ablation을 수행한다.
6. classical-only head와 parameter 수를 맞춘 작은 MLP를 비교한다.

#### 통과 기준

- input parameter, trainable weight와 output shape 계약을 테스트한다.
- quantum layer까지 gradient가 전달되는지 자동 테스트한다.
- data encoding이 요구하는 qubit·gate·state-preparation 비용을 기록한다.
- 여러 seed에서 loss·task metric·gradient norm을 보고한다.
- 학습 정확도가 높다는 이유만으로 양자적 이점을 주장하지 않는다.

자료:

- [Qiskit Machine Learning](https://qiskit-community.github.io/qiskit-machine-learning/)
- [Qiskit QNN tutorial](https://qiskit-community.github.io/qiskit-machine-learning/tutorials/01_neural_networks.html)
- [Qiskit TorchConnector](https://qiskit-community.github.io/qiskit-machine-learning/tutorials/05_torch_connector.html)
- [PennyLane TorchLayer](https://docs.pennylane.ai/en/stable/code/api/pennylane.qnn.TorchLayer.html)
- [IBM data encoding](https://quantum.cloud.ibm.com/learning/en/courses/quantum-machine-learning/data-encoding)

### 9~11주차: Feature Map과 Quantum Kernel

quantum feature map \(U_\phi(x)\)가 만든 상태를 사용하면 대표적인 fidelity kernel은 다음과 같다.

\[
K(x,y)=|\langle\phi(x)|\phi(y)\rangle|^2.
\]

#### 학습 내용

- classical feature map, kernel trick과 SVM
- fidelity quantum kernel과 trainable kernel
- kernel matrix의 대칭성·positive semidefinite 조건
- finite shots와 noise가 만드는 비-PSD matrix
- kernel-target alignment
- \(O(N^2)\) pair evaluation 비용
- feature map의 inductive bias와 classical simulability
- quantum kernel 결과를 classical SVC·SVR에 연결하는 hybrid workflow

#### 필수 실습

1. angle, Z, ZZ와 사용자 정의 feature map을 비교한다.
2. exact-statevector와 finite-shot kernel matrix를 만든다.
3. eigenvalue spectrum, effective rank와 PSD violation을 분석한다.
4. kernel-target alignment로 trainable feature map을 학습한다.
5. linear·RBF·polynomial SVM과 동일 split·동일 tuning budget으로 비교한다.
6. quantum kernel의 randomized-feature 또는 classically simulated surrogate를 negative control로 둔다.

#### 통과 기준

- kernel-target alignment와 test metric을 구분한다.
- PSD correction 전후 크기와 downstream 결과를 보고한다.
- dataset 크기에 따른 pair 수, shots와 wall time을 계산한다.
- feature map이 데이터 구조와 맞는 이유를 가설로 명시한다.
- 고차원 Hilbert space라는 사실만으로 advantage를 주장하지 않는다.

자료:

- [IBM quantum kernel methods](https://quantum.cloud.ibm.com/learning/en/courses/quantum-machine-learning/quantum-kernel-methods)
- [Qiskit ML kernel API](https://qiskit-community.github.io/qiskit-machine-learning/apidocs/qiskit_machine_learning.kernels.html)
- [PennyLane kernel API](https://docs.pennylane.ai/en/stable/code/qp_kernels.html)
- [PennyLane kernel training demo](https://pennylane.ai/qml/demos/tutorial_kernels_module)
- [Quantum-enhanced feature space 원 논문](https://doi.org/10.1038/s41586-019-0980-2)

### 12~14주차: Barren Plateau와 공정한 평가

#### 학습 내용

- random deep ansatz와 vanishing-gradient landscape
- gradient 평균이 아니라 gradient variance의 qubit·depth scaling
- global cost와 local cost
- noise-induced barren plateau
- expressibility와 trainability의 trade-off
- shallow/local ansatz, identity-block initialization, layerwise training, parameter sharing
- mitigation은 일반적 해결 보장이 아니라 문제별 가설이라는 경계

#### 필수 실습

1. qubit 수 \(n\)과 circuit depth \(L\)을 단계적으로 늘린다.
2. 각 조건에서 최소 30개의 random initialization을 사용한다.
3. PSR로 parameter gradient를 측정한다.
4. \(\log \operatorname{Var}[\partial C/\partial\theta]\)와 \(n\)의 관계를 그린다.
5. global cost와 local cost를 비교한다.
6. noise strength별로 같은 실험을 반복한다.
7. initialization·ansatz·cost locality 완화책을 하나씩 ablation한다.

#### 통과 기준

- 한 개 loss curve 또는 한 초기값으로 barren plateau를 주장하지 않는다.
- gradient variance와 finite-shot measurement floor를 구분한다.
- noise-free plateau와 noise-induced plateau를 구분한다.
- 각 완화책의 accuracy, depth, shot, execution-count trade-off를 보고한다.
- 유리한 seed와 dataset만 선택하지 않고 실패 결과를 포함한다.

원 출처와 실습:

- [Barren plateaus 원 논문](https://doi.org/10.1038/s41467-018-07090-4)
- [Global/local cost 연구](https://doi.org/10.1038/s41467-021-21728-w)
- [Noise-induced barren plateaus](https://www.nature.com/articles/s41467-021-27045-6)
- [PennyLane barren plateau demo](https://pennylane.ai/demos/tutorial_barren_plateaus)
- [PennyLane local cost demo](https://pennylane.ai/demos/tutorial_local_cost_functions)

### 15~16주차: QML Capstone

하나의 작은 공개 dataset 또는 합성 dataset을 정하고 다음 실험을 모두 수행한다.

- logistic regression, RBF-SVM, parameter-matched MLP
- variational QNN
- quantum fidelity kernel
- randomized/no-entanglement/classical-surrogate negative controls
- exact, finite-shot, noisy simulation
- 가능하면 마지막에만 제한된 실제 QPU 실행

최종 보고서는 accuracy 순위가 아니라 다음 질문에 답해야 한다.

1. 어떤 data property가 선택한 encoding과 맞는가?
2. 개선이 quantum block에서 왔는지 preprocessing·tuning 차이에서 왔는가?
3. gradient·kernel matrix가 noise와 shots에 얼마나 안정적인가?
4. 전체 실행 비용과 가장 강한 classical baseline은 무엇인가?
5. 관측된 결과가 제한된 규모의 실험인지, scaling 또는 advantage 주장인지 명확히 구분했는가?

## 공통 실험·평가 계약

### 필수 기록표

| 분류 | 반드시 기록할 항목 |
| --- | --- |
| 환경 | OS, Python, package와 version, lock file |
| 회로 | logical qubits, parameters, gates, depth, 2-qubit gates |
| 변환 | backend target, optimization level, layout, transpiler seed |
| 실행 | simulator/QPU, method, shots, random seed, calibration 시각 |
| 통계 | 반복 수, 평균, 분산·신뢰구간, 제외 기준 |
| 고전 계산 | preprocessing, optimizer, eigensolver, wall time, memory |
| 기준선 | exact answer 또는 강한 classical model과 tuning budget |
| 결론 | 유효 범위, 실패 사례, 제한, 다음 실험 |

### 회로 알고리즘별 핵심 metric

| 대상 | 최소 metric |
| --- | --- |
| 회로 equivalence | global-phase-aware operator/state fidelity, 측정 분포 차이 |
| Transpilation | ISA 위반, depth, 2-qubit gates, SWAP, compile time |
| VQE | energy error, state fidelity, evaluations, shots, symmetry violation |
| QAOA | expected objective, approximation ratio, success·feasibility probability |
| QSCI | energy error, selected subspace dimension, shots, captured support |
| SQD | energy error, recovery iterations, batch variance, discard rate, solver cost |
| QNN | task metric, calibration, gradient norm·variance, circuit executions |
| Quantum kernel | alignment, PSD violation, test metric, pair evaluations, shots |

### 공정한 Classical Baseline 계약

QML 결과에는 최소 다음 비교가 포함되어야 한다.

- linear 또는 logistic model
- RBF-SVM 또는 목적에 맞는 강한 kernel model
- parameter 수가 비슷한 작은 MLP
- quantum circuit의 표현을 흉내 낸 randomized feature 또는 classical surrogate

모든 모델은 같은 train/validation/test split, 같은 preprocessing 정보, 비교 가능한 hyperparameter search와 stopping budget을 사용한다. quantum model만 여러 번 tuning하고 classical baseline은 default 설정으로 두는 비교는 인정하지 않는다.

task metric 외에 다음 end-to-end 비용을 보고한다.

- data encoding과 state preparation
- transpilation과 circuit batching
- shots와 gradient/kernel evaluation 횟수
- classical optimizer·post-processing
- QPU queue·network·retry

실험적 정확도 우위가 곧 계산복잡도상의 quantum advantage는 아니다. 양자 우위를 주장하려면 문제 정의, scaling, 고전 난이도 가정, 최신 classical algorithm·surrogate와 end-to-end 비용까지 별도의 근거가 필요하다. 관련 경계는 [Power of data in quantum machine learning](https://www.nature.com/articles/s41467-021-22539-9)을 참고한다.

## 포트폴리오와 최종 통과 기준

### 권장 포트폴리오

#### 회로 검증 개발자

1. **cross-sdk-circuit-conformance**
   - 세 SDK adapter, bit-order normalization, equivalence tests
2. **hardware-aware-transpilation-benchmark**
   - 여러 target·seed·optimization level의 accuracy/resource 비교
3. **vqe-qaoa-reproducibility-study**
   - exact·shot·noise·transpiled 결과와 여러 optimizer
4. **qsci-sqd-subspace-study**
   - shot·subspace convergence, recovery, 고전 solver scaling

#### QML 전문가

1. **parameter-shift-gradient-auditor**
2. **hybrid-qnn-with-classical-controls**
3. **trainable-quantum-kernel-benchmark**
4. **barren-plateau-reproduction**
5. **fair-qml-benchmark-card**

각 저장소에는 README, 수학적 정의, dependency lock, 실행 명령, 자동 테스트, raw result, plotting script, seed, 실패 사례와 제한 사항이 있어야 한다.

### 평가 Rubric

#### 회로 검증 개발자 — 100점

| 항목 | 배점 |
| --- | ---: |
| 회로·수학 정확성 | 20 |
| 자동 검증과 regression test | 20 |
| transpilation·hardware awareness | 15 |
| shot·noise 통계 해석 | 15 |
| VQE/QAOA/QSCI/SQD 구현·분석 | 20 |
| 재현성·문서화 | 10 |

#### QML 전문가 — 100점

| 항목 | 배점 |
| --- | ---: |
| DQC·PSR 수학과 gradient 검증 | 20 |
| QNN·hybrid architecture | 15 |
| feature map·kernel 이해 | 15 |
| 공정한 classical baseline과 실험 설계 | 20 |
| barren plateau·noise·resource 분석 | 20 |
| 재현성·문서화 | 10 |

80점 이상을 과정 통과, 90점 이상과 코드 구두 방어를 전문가 준비 기준으로 삼는다. 다음 결함이 있으면 총점과 무관하게 재작업한다.

- data leakage
- 작은 문제인데 exact reference가 없음
- SDK version, seed 또는 shots 미기록
- transpilation 후 observable layout 누락
- 한 번의 실행으로 통계적 결론을 냄
- 고전 기준선 없이 quantum 성능을 주장함
- data loading·classical post-processing을 제외하고 end-to-end 이점을 주장함

## 공식 자료와 원 논문

### 회로·실행·검증

- [IBM: Basics of Quantum Information](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information)
- [IBM: Qiskit Primitive](https://quantum.cloud.ibm.com/docs/en/guides/primitives)
- [IBM: Qiskit SDK exact simulation](https://quantum.cloud.ibm.com/docs/en/guides/simulate-with-qiskit-sdk-primitives)
- [IBM: Qiskit transpilation](https://quantum.cloud.ibm.com/docs/en/guides/transpile)
- [IBM: Qiskit local testing mode](https://quantum.cloud.ibm.com/docs/en/guides/local-testing-mode)
- [Google Quantum AI: Cirq basics](https://quantumai.google/cirq/start/basics)
- [Google Quantum AI: Cirq simulation](https://quantumai.google/cirq/simulate/simulation)
- [PennyLane: circuits](https://docs.pennylane.ai/en/stable/introduction/circuits.html)
- [PennyLane: measurements](https://docs.pennylane.ai/en/stable/introduction/measurements.html)

### Variational algorithm·QSCI·SQD

- [IBM: Variational quantum algorithms](https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/variational-quantum-algorithms)
- [IBM: Quantum chemistry with VQE](https://quantum.cloud.ibm.com/learning/en/courses/quantum-chem-with-vqe)
- [Qiskit Optimization minimum eigensolvers](https://qiskit-community.github.io/qiskit-optimization/apidocs/qiskit_optimization.minimum_eigensolvers.html)
- [QSCI 원 논문](https://arxiv.org/abs/2302.11320)
- [Qiskit SQD addon](https://qiskit.github.io/qiskit-addon-sqd/)

### QML·gradient·kernel·trainability

- [IBM: Quantum Machine Learning](https://quantum.cloud.ibm.com/learning/en/courses/quantum-machine-learning)
- [Qiskit Machine Learning 0.9.1](https://qiskit-community.github.io/qiskit-machine-learning/)
- [PennyLane 0.45.1 documentation](https://docs.pennylane.ai/en/stable/)
- [Parameter-shift rule](https://doi.org/10.1103/PhysRevA.99.032331)
- [PennyLane differentiable programming 논문](https://arxiv.org/abs/1811.04968)
- [Quantum-enhanced feature spaces](https://doi.org/10.1038/s41586-019-0980-2)
- [Rigorous quantum kernel speed-up](https://doi.org/10.1038/s41567-021-01287-z)
- [Barren plateaus](https://doi.org/10.1038/s41467-018-07090-4)
- [Cost-function-dependent barren plateaus](https://doi.org/10.1038/s41467-021-21728-w)
