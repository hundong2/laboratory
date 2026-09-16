<!-- rumdl-disable MD013 -->

# 양자 알고리즘·과학 계산 트랙

작성일: 2026-09-13

이 트랙은 편미분방정식(PDE), 전자구조·다체 물리, 최적화 문제를 대상으로 양자 알고리즘을 설계하고 그 복잡도와 실제 자원 비용을 평가하는 역량을 기르는 과정이다. 목표는 단순히 양자 회로를 실행하는 것이 아니라 다음 질문에 수학·코드·실험 근거로 답할 수 있는 수준이다.

1. 해결하려는 수학적 문제와 요구 출력은 정확히 무엇인가?
2. 가장 강한 고전 수치해법은 무엇이며 어느 범위까지 잘 동작하는가?
3. 양자 알고리즘은 어떤 입력 접근, 희소성, 조건수, 정밀도와 상태 준비 가정을 요구하는가?
4. NISQ 실험과 내결함성 양자컴퓨팅(FTQC) 분석 중 무엇을 수행한 것인가?
5. 데이터 적재, 측정, 고전 후처리와 오류정정까지 포함해도 이점이 남는가?

> **중요:** DFT, DMRG, DMFT는 그 자체가 양자컴퓨터용 알고리즘이 아니다. 각각 밀도범함수 이론, 텐서 네트워크 기반 다체 계산법, 동적 평균장 이론이라는 강력한 **고전 계산 프레임워크**다. 이 트랙에서는 이들을 물성 문제의 핵심 이론이자 양자 알고리즘을 평가할 때 반드시 이겨야 하는 고전 기준선으로 배운다.

## 1. 선수 지식

### 1.1 수학

| 영역 | 반드시 알아야 할 내용 | 준비 완료 기준 |
|---|---|---|
| 복소 선형대수 | 내적공간, 정규직교기저, Hermitian/unitary 행렬, spectral theorem, SVD, Kronecker product | 작은 Hermitian 행렬을 대각화하고 고유기저에서 시간 진화를 설명할 수 있다. |
| 수치 선형대수 | sparse matrix, LU/QR, CG/GMRES, condition number, preconditioner, residual과 forward error | 같은 선형계에서 residual이 작아도 해 오차가 클 수 있는 조건을 실험으로 보인다. |
| 미적분·변분법 | 다변수 미적분, 함수공간, Euler–Lagrange 식, 제약 최적화 | 에너지 범함수에서 정상 조건을 유도할 수 있다. |
| ODE/PDE | 초기·경계조건, elliptic/parabolic/hyperbolic 분류, weak solution 개념 | Poisson·heat·wave equation의 입력·출력·경계조건을 구분한다. |
| 수치 PDE | finite difference/element 기초, consistency·stability·convergence, Fourier/Chebyshev spectral method | 제조해(manufactured solution)로 수렴 차수를 측정한다. |
| 확률·통계 | 표본추정, 분산, Monte Carlo, confidence interval, hypothesis test | 여러 seed와 shot에서 평균·오차막대·신뢰구간을 보고한다. |
| 최적화 | convexity, gradient method, constrained optimization, combinatorial optimization | continuous relaxation과 discrete optimum의 차이를 설명한다. |
| 복잡도 | 점근 표기, worst/average case, query·gate·sample complexity | 한 알고리즘의 전처리, 핵심 계산, 출력 추출 비용을 따로 적는다. |

권장 공개 자료는 [MIT 18.06 Linear Algebra](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/), [MIT 18.085 Computational Science and Engineering I](https://ocw.mit.edu/courses/18-085-computational-science-and-engineering-i-summer-2020/resources/lecture-notes/), Trefethen의 [Spectral Methods in MATLAB](https://people.maths.ox.ac.uk/trefethen/spectral.html)과 [Finite Difference and Spectral Methods for ODE/PDE](https://people.maths.ox.ac.uk/trefethen/pdetext.html)다.

### 1.2 물리·화학

- 파동함수, operator, 측정, Schrödinger equation
- spin과 angular momentum, identical particle
- fermion과 Pauli exclusion principle
- second quantization과 creation/annihilation operator
- Born–Oppenheimer approximation
- 통계역학, Green's function과 Hubbard model의 기초
- 분자 orbital, basis set, Hartree–Fock와 correlation의 의미

추천 출발점은 [MIT 8.04 Quantum Physics I](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2013/)이다. DMFT까지 진행하려면 응집물질물리 또는 다체 양자역학 입문을 병행한다.

### 1.3 양자정보·프로그래밍

- state vector와 density matrix
- tensor product, entanglement, measurement
- quantum circuit, controlled operation, QFT, phase estimation
- Hamiltonian simulation과 amplitude estimation의 개념
- noise channel, error mitigation, quantum error correction의 차이
- Python, NumPy, SciPy, Jupyter, Git
- Qiskit 또는 PennyLane 중 하나
- 물성 트랙에서는 PySCF, OpenFermion과 ITensorMPS 또는 동급 도구

[IBM Basics of Quantum Information](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information)과 [IBM Quantum Learning 과정 목록](https://quantum.cloud.ibm.com/learning/en/courses)을 양자정보 입문 경로로 사용할 수 있다. 더 이론적인 과정은 [MIT 18.435J Quantum Computation](https://ocw.mit.edu/courses/18-435j-quantum-computation-fall-2003/pages/syllabus/)을 참고한다.

### 1.4 시작 전 진단 과제

다음 네 과제를 모두 통과하지 못하면 1~8주차를 압축하지 않는다.

1. NumPy만 사용해 2-qubit Bell state와 reduced density matrix를 만든다.
2. SciPy sparse CG로 2D Poisson equation을 풀고 grid refinement에 따른 오차와 조건수를 그린다.
3. Fourier 또는 Chebyshev differentiation matrix로 1D boundary-value problem을 푼다.
4. 같은 실험을 세 번 재실행해도 결과를 재현하도록 환경, seed, 명령과 산출물을 문서화한다.

## 2. 단계별 학습 과정

아래 표는 공통 기반을 수치해석·물성 심화와 합친 **알고리즘 연구자용 48주 통합 경로**다. [공통 기반 40주](01_common_foundations.md)를 이미 이수한 학습자가 48주를 다시 처음부터 더하는 구조가 아니다. 이 경우 A~D의 중복 영역은 진단 과제로 대체하고 E 이후에서 부족한 단계만 선택한다. 이미 수치해석 또는 다체물리 대학원 과정을 이수했더라도 고전 기준선 구현은 생략하지 않는다.

| 단계 | 권장 주차 | 핵심 학습 | 대표 실습 | 통과 기준 |
|---|---:|---|---|---|
| A. 계산 연구 기반 | 1–4 | Python 과학 계산, Git, 테스트, 재현 가능한 실험, 점근 복잡도 | dense/sparse 행렬 연산 benchmark | 환경 잠금 파일, seed, 테스트, 재실행 명령과 결과표를 제출한다. |
| B. 선형대수·수치해석 | 5–8 | SVD, sparse solver, 조건수, preconditioning, FDM·spectral method | Poisson FDM/CG 대 FFT·Chebyshev | 해 오차, residual, 조건수, 시간·메모리를 구분해 보고한다. |
| C. 양자역학·양자정보 | 9–12 | 상태·측정·얽힘, density matrix, QFT, phase estimation | 작은 상태벡터 simulator와 QPE | 계산기 결과를 행렬 계산과 비교하고 측정 통계를 설명한다. |
| D. 양자 알고리즘 비용모형 | 13–16 | Hamiltonian simulation, oracle, block encoding, LCU, QSVT, amplitude estimation | block-encoding toy matrix | query·logical gate·shot·입출력 비용을 서로 구분한다. |
| E. PDE와 선형계 | 17–20 | PDE 분류, discretization, spectral approximation, sparse linear system | Poisson·heat equation의 고전 solver | 제조해로 수렴 차수를 검증하고 강한 고전 기준선을 확정한다. |
| F. HHL·QLSA | 21–24 | HHL, phase estimation 기반 역행렬, VQLS, QSVT 기반 QLSA | SciPy 대 HHL/VQLS observable | \(N,s,\kappa,\epsilon\), 상태 준비·측정 비용을 포함한다. |
| G. QPINN·변분 PDE | 25–28 | classical PINN, automatic differentiation, variational quantum PDE, parameter-shift | Poisson 또는 Burgers PINN/QPINN | 동일 데이터·optimizer budget·seed·평가지표로 비교한다. |
| H. LBM·QLBM | 29–32 | D1Q3/D2Q9, collision·streaming, boundary, unitary embedding, Carleman | 고전 LBM과 작은 QLBM | reset·측정·비선형 후처리 비용까지 기록한다. |
| I. 전자구조·양자화학 | 33–37 | HF, DFT, second quantization, basis/active space, JW/BK, VQE/QPE | H₂/LiH PySCF→OpenFermion→VQE | HF·DFT·FCI 또는 exact 결과와 회로 결과를 같은 Hamiltonian에서 비교한다. |
| J. DMRG·DMFT | 38–42 | MPS, entanglement, sweep/truncation, impurity mapping, self-consistency | Heisenberg DMRG와 Bethe DMFT | bond dimension·truncation과 DMFT 수렴 조건을 명시한다. |
| K. 양자 최적화 | 43–46 | Ising/QUBO, QAOA, approximation, classical relaxation·heuristic | 3-regular MaxCut benchmark | exact·근사·휴리스틱과 품질·시간을 모두 비교한다. |
| L. 캡스톤·자원추정 | 47–48 | NISQ/FT 구분, logical resource, QEC, T factory, 연구 주장 감사 | 한 알고리즘의 end-to-end audit | 재현 패키지와 제한 사항을 포함한 연구 보고서를 방어한다. |

### 2.1 단계 운영 규칙

- 각 단계는 `이론 노트 → 고전 기준선 → 양자 또는 하이브리드 구현 → 검증 → 비용 감사` 순서로 진행한다.
- 통과 기준을 만족하지 못했으면 다음 단계에서 결과를 누적하지 않는다.
- simulator 결과, 실제 NISQ 장치 결과, logical FT 추정치를 그래프와 표에서 분리한다.
- 모든 성능 비교는 같은 문제 instance, 같은 출력 의미, 같은 허용 오차를 사용한다.
- 작은 한 개 사례에서 얻은 결과로 점근 scaling이나 양자 우위를 주장하지 않는다.

## 3. PDE, HHL, QPINN과 QLBM

### 3.1 먼저 고전 PDE 문제를 고정한다

양자 PDE 회로를 설계하기 전에 다음 problem contract를 작성한다.

- PDE 종류와 domain
- 초기조건과 경계조건
- 계수의 regularity, sparsity와 시간 의존성
- 요구 출력: 전체 field, 특정 지점 값, 적분량, 에너지 또는 다른 observable
- 허용할 discretization·solver·sampling 오차
- 고전 sparse/spectral solver의 시간·메모리·정확도

기초 프로젝트는 다음 순서가 좋다.

1. 1D Poisson equation: finite difference와 Chebyshev collocation 비교
2. 2D Poisson equation: sparse CG와 preconditioner
3. heat equation: explicit/implicit time stepping과 stability
4. advection 또는 wave equation: Fourier spectral method와 dispersion

Spectral method는 매끄러운 해에서 높은 정확도를 낼 수 있으므로 양자 spectral PDE 방법의 필수 고전 기준선이다. grid point 수만 비교하지 말고 boundary 처리, coefficient regularity, transform 비용과 목표 오차를 함께 비교한다.

### 3.2 HHL과 QLSA의 올바른 출력 계약

[Harrow–Hassidim–Lloyd 원 논문](https://arxiv.org/abs/0811.3171)은 희소 선형계 \(A\mathbf{x}=\mathbf{b}\)에 대해 일반적인 고전 배열 \(\mathbf{x}\)를 출력하는 것이 아니라 해에 비례하는 양자 상태 \(|x\rangle\)를 준비하고 그 상태의 observable을 추정하는 문제를 다룬다. 따라서 다음 문장은 서로 다른 주장이다.

- 잘못된 축약: “HHL은 모든 선형계의 전체 해를 지수적으로 빠르게 출력한다.”
- 정확한 표현: “효율적인 입력 oracle/state preparation, 희소성, 양호한 조건수와 필요한 출력이 소수 observable이라는 조건에서 QLSA의 계산 복잡도 이점이 가능하다.”

핵심 학습 항목은 다음과 같다.

1. Hermitian embedding과 eigenvalue inversion
2. phase estimation의 정밀도와 성공 확률
3. \(\kappa\)가 작은 eigenvalue inversion에 미치는 영향
4. postselection/amplitude amplification
5. \(|b\rangle\) 준비와 \(A\) 접근 oracle 또는 block encoding
6. \(|x\rangle\)에서 실제 관심량을 측정하는 비용

[Childs–Kothari–Somma QLSA](https://arxiv.org/abs/1511.02306)는 Fourier/Chebyshev 근사와 LCU로 원래 알고리즘의 정밀도 의존성을 개선한다. [Quantum Singular Value Transformation](https://arxiv.org/abs/1806.01838)은 block-encoded matrix의 singular value에 polynomial transformation을 적용해 pseudoinverse를 포함한 선형대수 연산을 통합적으로 설명한다. 구현 학습에는 [PennyLane HHL 데모](https://pennylane.ai/demos/linear_equations_hhl_qrisp_catalyst)와 [PennyLane VQLS 데모](https://pennylane.ai/demos/tutorial_vqls)를 활용할 수 있다.

#### HHL/VQLS 통과 기준

- SciPy direct solver와 CG/GMRES 중 적절한 기준선을 포함한다.
- 전체 해 벡터를 읽는 비교가 아니라 동일 observable을 비교하는 실험을 별도로 수행한다.
- \(N\), sparsity \(s\), condition number \(\kappa\), 목표 오차 \(\epsilon\)을 sweep한다.
- state preparation, matrix decomposition/block encoding, optimizer, shot과 readout 비용을 별도 표로 적는다.
- [양자 영감을 받은 고전 선형계 알고리즘](https://arxiv.org/abs/1811.04852)처럼 강한 샘플링 접근을 고전 방법에도 주었을 때 결론이 어떻게 바뀌는지 설명한다.

### 3.3 Spectral PDE와 양자 상태 출력

[고정밀 양자 PDE 알고리즘](https://arxiv.org/abs/2002.07868)은 finite-difference Poisson solver와 spectral elliptic PDE 알고리즘을 분석한다. 이 계열의 결과도 해가 양자 상태로 인코딩된다는 점이 중요하다. 격자점 \(N\)개의 값을 모두 고전적으로 복원하는 것은 소수 observable을 얻는 것과 다른 출력 문제다.

학습자는 다음 두 실험을 분리한다.

- `Observable task`: 평균, flux, mode amplitude 등 소수 관심량 추정
- `Field reconstruction task`: 전체 discretized field를 고전 배열로 복원

[Fourier-space quantum PDE circuits](https://journals.aps.org/prresearch/abstract/10.1103/tbzc-w9x8)은 QFT와 QSVT를 이용해 advection, heat, acoustic wave와 Poisson 문제의 회로 구성을 제시한다. 이를 재현할 때는 매끄러운 초기조건, Fourier coefficient 준비, boundary 조건과 readout 범위를 논문의 가정과 일치시킨다.

### 3.4 QPINN과 변분 양자 PDE

QPINN이라는 이름은 문헌에서 서로 다른 구성을 가리킬 수 있으므로 보고서 첫 부분에 다음 중 무엇인지 정의한다.

- 양자 회로가 함수 근사기 역할을 하는 physics-informed hybrid model
- quantum feature map 또는 kernel을 사용하는 PINN
- 변분 양자 상태로 PDE 해를 인코딩하는 방법
- 선형계 양자 알고리즘을 PDE discretization에 적용한 방법

고전 기준선은 [Physics-Informed Neural Networks 원 연구](https://www.sciencedirect.com/science/article/pii/S0021999118307125)와 안정적인 수치 PDE solver다. [Variational quantum simulation of nonlinear PDEs](https://arxiv.org/abs/1907.09032)는 nonlinear term을 다루기 위해 여러 상태 사본을 사용하는 변분 방식을 제시한다. [Continuous-variable QPINN 연구](https://www.frontiersin.org/journals/applied-mathematics-and-statistics/articles/10.3389/fams.2022.1036711/full)는 Poisson 문제의 QPINN workflow를 제공한다. [다변수 PDE QPINN 연구](https://journals.aps.org/prapplied/abstract/10.1103/6nh4-yh2y)는 heat·Poisson 문제와 noisy/photonic hardware proof-of-concept를 다루지만, 확장 가능한 일반 양자 우위를 입증한 것으로 해석해서는 안 된다.

#### QPINN 비교 규칙

- 같은 collocation/test point와 boundary sampling을 사용한다.
- parameter 수만 맞추지 말고 objective evaluation, gradient 회로, shots와 wall time을 보고한다.
- train loss와 독립 grid의 solution error를 분리한다.
- 최소 5개 seed의 중앙값과 분산을 제시한다.
- optimizer, 초기화, noise, barren plateau 징후를 기록한다.
- 해석적 해가 없으면 검증된 고전 solver를 reference solution으로 사용한다.
- “더 적은 parameter”를 곧바로 “더 낮은 총 계산 비용”으로 해석하지 않는다.

### 3.5 LBM과 QLBM

QLBM 전에 고전 lattice Boltzmann method를 구현한다.

1. distribution \(f_i(\mathbf{x},t)\)와 lattice velocity
2. collision과 relaxation time
3. streaming
4. bounce-back 등의 boundary condition
5. density·velocity 같은 macroscopic observable 복원
6. stability와 viscosity 관계

양자화의 핵심 난점은 collision, relaxation, boundary와 nonlinear update가 일반적으로 unitary operation이 아니라는 점이다. 연구마다 ancilla/dilation, linearization, measurement-reset, 고전 후처리 또는 Carleman linearization을 사용하므로 “QLBM”이라는 이름만으로 같은 알고리즘으로 묶지 않는다.

- [Unitary Quantum Lattice Boltzmann Method](https://arxiv.org/abs/2405.13391)는 선형화된 advection–diffusion에서는 측정 전 여러 step을 수행하지만 nonlinear 사례의 범위와 후처리 제약을 구분한다.
- [Potential quantum advantage for LBM](https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.7.013036)은 Carleman-linearized LBM을 분석하며 특정 근사와 조건 아래의 잠재적 이점을 논한다.
- [Bounded Quantum Advantage in LBM](https://journals.aps.org/prxquantum/accepted/10.1103/xysy-q3fp)은 Carleman 수렴, time stepping, condition number, 출력 추출과 gate count를 포함하면 이점이 특정 observable과 오차 영역으로 제한될 수 있음을 보인다.
- [Exact quantum circuits for lattice Boltzmann dynamics](https://arxiv.org/abs/2608.06570)는 명시적 gate 구성을 제시하지만 양자 우위를 주장하지 않으며 state preparation과 readout을 열린 비용으로 남긴다.

#### QLBM 통과 기준

- D1Q3 diffusion 또는 linear advection을 고전 구현으로 검증한다.
- 동일 lattice·경계·step 수의 quantum statevector 결과와 비교한다.
- 한 step 정확도와 장시간 누적 오차를 분리한다.
- ancilla, reset, tomography, postselection과 classical nonlinear update를 센다.
- 전체 field 출력과 소수 macroscopic observable 출력의 비용을 분리한다.
- Navier–Stokes 전체를 양자적으로 효율적으로 풀었다는 표현은 end-to-end 증거가 없으면 사용하지 않는다.

## 4. DFT, 양자화학, DMRG와 DMFT

### 4.1 고전 기준선이라는 위치

다시 강조하면 다음 세 방법은 모두 강력한 고전 계산 방법이다.

| 방법 | 본질 | 잘하는 영역 | 양자 연구에서의 역할 |
|---|---|---|---|
| DFT | 전자 밀도를 기본 변수로 삼는 ground-state 전자구조 이론 | 비교적 큰 분자·고체의 구조와 물성 | HF, post-HF, QPE/VQE 결과를 해석하는 현실적 고전 기준선 |
| DMRG | MPS와 density-matrix truncation에 기반한 variational 다체 계산 | 1D·저얽힘 계, 일부 강상관 active space | “고전적으로 어려움”을 주장하기 전에 비교해야 할 tensor-network 기준선 |
| DMFT | lattice model을 self-consistent quantum impurity problem으로 매핑하는 이론 | 국소 동역학적 상관과 Mott physics | 양자 impurity solver를 끼울 수 있는 고전 outer loop이자 전체 hybrid 비용 기준 |

### 4.2 DFT부터 전자구조를 익힌다

[Hohenberg–Kohn 원 논문](https://journals.aps.org/pr/abstract/10.1103/PhysRev.136.B864)은 ground-state density가 외부 potential과 관측량을 결정하고 정확한 범함수의 최소화가 ground-state energy를 준다는 토대를 제시했다. [Kohn–Sham 원 논문](https://journals.aps.org/pr/abstract/10.1103/PhysRev.140.A1133)은 상호작용 전자 문제를 유효한 one-particle equation과 exchange-correlation functional로 다룬다.

권장 실습 순서는 다음과 같다.

1. H₂, LiH 또는 H₂O의 geometry와 basis set 고정
2. restricted/unrestricted Hartree–Fock
3. LDA, GGA, hybrid DFT 비교
4. basis convergence와 self-consistent field convergence 분석
5. 작은 active space에서 FCI 또는 고정밀 기준 계산

[PySCF DFT 공식 문서](https://pyscf.org/user/dft.html)는 RKS 예제와 LDA/GGA/meta-GGA/hybrid functional의 실제 사용법을 제공한다. DFT energy를 exact many-body ground-state energy와 동일시하지 말고 functional approximation, basis, pseudopotential과 SCF 오차를 구분한다.

### 4.3 양자화학 Hamiltonian과 VQE/QPE

[OpenFermion 전자구조 공식 워크숍](https://quantumai.google/openfermion/tutorials/intro_workshop_exercises)은 PySCF 적분에서 second-quantized fermionic Hamiltonian을 만들고 Jordan–Wigner 또는 Bravyi–Kitaev 변환을 거쳐 qubit Hamiltonian으로 옮기는 과정을 다룬다.

필수 파이프라인은 다음과 같다.

```text
분자 구조·basis
  → one-/two-electron integral
  → Hartree–Fock reference
  → active-space/frozen-core 선택
  → fermionic Hamiltonian
  → qubit mapping과 symmetry reduction
  → exact diagonalization / VQE / fault-tolerant QPE
  → 에너지와 자원 비교
```

[VQE 원 논문](https://www.nature.com/articles/ncomms5213)은 짧은 coherent circuit과 고전 optimizer를 결합한 소규모 proof-of-concept다. VQE 실험에서는 ansatz, optimizer, initial point, measurement grouping, shots, symmetry, noise와 error mitigation을 모두 보고한다.

Fault-tolerant chemistry에서는 QPE의 asymptotic 식만 제시하지 않는다. [FeMoco resource study](https://arxiv.org/abs/1605.03590)는 상태 준비, gate synthesis와 오류정정까지 계산하는 대표적 역사 사례다. 다만 오래된 hardware·code 가정을 현재 예측으로 그대로 재사용하지 말고 현재 도구로 다시 추정한다. [Microsoft Quantum Resource Estimator](https://learn.microsoft.com/en-us/azure/quantum/resource-estimator-batching), [T factory 설명](https://learn.microsoft.com/en-us/azure/quantum/concepts-tfactories), [resource-estimation 출력 설명](https://learn.microsoft.com/en-us/azure/quantum/overview-resource-estimator-output-data)을 이용해 physical error rate와 error-correction scheme에 따른 민감도를 계산할 수 있다.

[양자화학의 일반적 지수 양자 이점에 대한 분석](https://www.nature.com/articles/s41467-023-37587-6)은 ground-state 문제 전반에 보편적인 지수 이점이 있다는 근거가 부족하며, 구조를 이용한 고전 방법도 함께 강해질 수 있음을 지적한다. 따라서 “Hilbert space가 지수적으로 크다”는 사실만으로 계산 이점을 증명할 수 없다.

#### 양자화학 통과 기준

- geometry, basis, charge, spin과 active space를 기록한다.
- qubit Hamiltonian의 term 수와 coefficient를 검증한다.
- 작은 계에서는 exact/FCI, HF와 DFT 결과를 모두 제공한다.
- VQE의 circuit depth, two-qubit gate, measurement setting, shots와 optimizer evaluation을 센다.
- chemical accuracy뿐 아니라 model-space·basis·algorithm·sampling 오차를 분리한다.
- FT 결과에는 logical qubit, T/Toffoli, QEC cycle, physical qubit, runtime과 failure budget을 포함한다.

### 4.4 DMRG와 MPS

[White의 DMRG 원 논문](https://link.aps.org/doi/10.1103/PhysRevLett.69.2863)은 density matrix를 이용한 상태 공간 truncation을 도입했다. [Schollwöck의 MPS 관점 리뷰](https://arxiv.org/abs/1008.3477)는 DMRG가 1차원 저얽힘 ground state에서 강한 이유와 한계를 체계화한다.

[ITensorMPS 공식 DMRG 튜토리얼](https://docs.itensor.org/ITensorMPS/stable/tutorials/DMRG.html)을 따라 Heisenberg chain에서 다음을 측정한다.

- chain length와 boundary condition
- MPS bond dimension과 sweep schedule
- cutoff와 discarded weight
- energy variance와 correlation function
- entanglement entropy
- 작은 chain의 exact diagonalization 오차

분자 active-space에서도 DMRG는 중요한 기준선이다. [White–Martin의 quantum chemistry DMRG](https://arxiv.org/abs/cond-mat/9808118)는 분자 계산 적용의 초기 근거를 제공한다. 양자화학 회로가 수십 qubit을 사용한다는 이유만으로 DMRG보다 어려운 문제라고 가정하지 말고 orbital ordering과 entanglement 구조에 따른 DMRG 비용을 실제로 측정한다.

### 4.5 DMFT와 hybrid quantum impurity solver

[Georges 외 DMFT 리뷰](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.68.13)는 lattice model을 self-consistent impurity problem으로 매핑하고 infinite-coordination limit에서의 관계, Hubbard model과 Mott transition을 설명한다.

먼저 [TRIQS IPT+DMFT 공식 튜토리얼](https://triqs.github.io/triqs/latest/userguide/python/tutorials/ModelDMFT/solutions/01s-IPT_and_DMFT.html)로 고전 loop를 구현한다.

```text
초기 self-energy
  → lattice Green's function
  → Weiss field / bath 갱신
  → impurity solver
  → 새 self-energy
  → mixing과 convergence 검사
  → 수렴할 때까지 반복
```

IPT는 저렴하지만 half-filling 밖에서 신뢰도가 떨어질 수 있으므로 작은 문제에서는 exact diagonalization, MPS 또는 다른 impurity solver와 비교한다. [MPS 기반 DMFT impurity solver](https://journals.aps.org/prx/abstract/10.1103/PhysRevX.5.041032)는 양자 solver를 평가하기 위한 강한 고전 기준선이다.

[Hybrid quantum-classical correlated-material simulation](https://journals.aps.org/prx/abstract/10.1103/PhysRevX.6.031045)은 고전 self-consistency loop 내부의 작은 impurity solver를 양자컴퓨터에 맡기는 구조를 제시한다. [실재 물질 DFT+DMFT 양자 실험](https://www.nature.com/articles/s41524-025-01772-6)은 최대 14 physical qubit과 제한된 bath 규모의 사례를 다루며, multi-orbital·더 큰 bath·완전한 NISQ 확장은 여전히 과제임을 보여준다.

#### DMFT 통과 기준

- Hubbard parameters, temperature, filling과 lattice DOS를 명시한다.
- bath discretization, Matsubara/time grid와 mixing을 기록한다.
- Green's function, self-energy와 spectral observable의 수렴 기준을 정의한다.
- 전체 self-consistency 반복 횟수와 impurity solver 호출 횟수를 센다.
- quantum impurity solver만의 회로 비용과 전체 hybrid loop 비용을 함께 제시한다.
- 작은 bath에서 ED/MPS와 비교하지 않은 quantum solver 결과는 정확성 검증을 통과한 것으로 보지 않는다.

## 5. 양자 최적화

### 5.1 학습 순서

1. graph problem, SAT, scheduling을 QUBO/Ising Hamiltonian으로 변환한다.
2. exact solver로 작은 instance의 최적해를 확인한다.
3. relaxation, branch-and-bound, local search와 문제 특화 heuristic을 구현하거나 사용한다.
4. [QAOA 원 논문](https://arxiv.org/abs/1411.4028)의 cost/mixer Hamiltonian과 depth \(p\)를 구현한다.
5. optimizer, parameter initialization, warm start, sampling과 noise를 분석한다.
6. 해 품질과 시간을 함께 측정한다.

QAOA의 기대값이 좋아졌다는 사실은 최적해를 빠르게 찾았다는 뜻과 다르다. 최소한 다음 지표를 구분한다.

- approximation ratio
- 최적해 또는 목표 품질 달성 확률
- sample 수를 포함한 time-to-solution
- parameter optimization에 든 총 objective evaluation
- preprocessing과 embedding 비용
- solution feasibility와 constraint violation
- instance와 seed 간 분산

[고전 solver와 QAOA 비교 연구](https://www.nature.com/articles/s41534-023-00718-4)는 제한된 depth에서 Gurobi와 MQLib 같은 강한 고전 방법을 이기지 못한 사례를 보여준다. [Quantum Optimization Benchmarking Library](https://www.nature.com/articles/s43588-026-00991-1)는 여러 문제군, 최신 solver baseline과 표준화된 보고 방식을 제공한다. [noise에 따른 변분 최적화 한계](https://www.nature.com/articles/s41567-021-01356-3)는 장치 오류율과 connectivity가 결론을 어떻게 바꾸는지 평가할 근거다.

### 5.2 필수 benchmark

- 3-regular MaxCut과 구조가 다른 graph family를 사용한다.
- 작은 크기는 brute force 또는 exact integer solver로 검증한다.
- Goemans–Williamson relaxation, local search와 MQLib·OR-Tools·상용 solver 중 가능한 강한 기준선을 포함한다.
- QAOA \(p\), two-qubit depth, shots, optimizer evaluation과 compile 시간을 기록한다.
- 단일 instance의 최고 결과가 아니라 instance family와 여러 seed의 분포를 보고한다.
- 고전 optimizer가 담당한 비용을 양자 실행 비용 밖으로 숨기지 않는다.

## 6. 포트폴리오 구성

### 6.1 필수 미니 프로젝트

#### 프로젝트 A — Poisson에서 HHL/VQLS까지

- FDM과 Chebyshev spectral baseline
- sparse direct/CG solver
- 작은 system의 HHL 또는 VQLS
- 전체 field와 observable 출력 비용 비교
- \(\kappa\), \(\epsilon\), grid 크기 민감도

#### 프로젝트 B — PINN 대 QPINN

- Poisson 또는 Burgers equation
- analytical/reference solution
- 같은 collocation, parameter 또는 계산 budget을 명시한 비교
- noise-free, finite-shot, 선택적으로 실제 hardware 결과
- 정확도·학습 안정성·총 비용 결론

#### 프로젝트 C — LBM 대 QLBM

- D1Q3 또는 D2Q9 고전 구현
- 작은 quantum circuit 또는 statevector 재현
- step 누적 오차와 boundary 검증
- reset/readout/postprocessing을 포함한 end-to-end 자원표

#### 프로젝트 D — 분자 전자구조

- PySCF의 HF·DFT·FCI 또는 고정밀 reference
- OpenFermion qubit mapping
- VQE와 exact diagonalization
- basis/active space/noise/shot ablation
- NISQ 회로표 또는 FT logical resource estimate

#### 프로젝트 E — 강상관계

- Heisenberg/Hubbard 계의 DMRG
- bond dimension과 entanglement 분석
- Bethe-lattice IPT-DMFT
- 작은 impurity에서 ED/MPS와 quantum toy solver 비교

#### 프로젝트 F — QAOA 최적화 benchmark

- 여러 MaxCut graph family
- exact와 강한 classical heuristic
- QAOA depth·noise·optimizer ablation
- approximation ratio와 time-to-solution

### 6.2 전문가 캡스톤 선택지

다음 중 하나를 10~12주 동안 수행한다.

1. **PDE 캡스톤:** variable-coefficient elliptic PDE에 대한 고전 spectral/FEM과 block-encoding 기반 양자 알고리즘의 입력·출력·자원 분석
2. **유체 캡스톤:** obstacle boundary가 있는 LBM에서 QLBM의 비unitary 처리와 측정 비용을 포함한 end-to-end feasibility study
3. **화학 캡스톤:** active-space 분자의 VQE, DMRG와 FT-QPE 자원을 동일 Hamiltonian에서 비교
4. **DMFT 캡스톤:** 고전 outer loop에 ED/MPS/quantum impurity solver를 교체해 정확도와 총 비용을 비교
5. **최적화 캡스톤:** 공개 instance suite에서 QAOA와 최신 고전 solver를 동일 품질·시간 기준으로 평가

### 6.3 제출물

- 연구 질문과 사전 등록한 성공·실패 기준
- 환경 잠금 파일과 한 번에 실행 가능한 명령
- 고전 기준선 코드와 검증 테스트
- 양자 회로 또는 logical algorithm 명세
- 입력 준비부터 출력 추출까지의 데이터 흐름
- raw result, seed와 분석 notebook
- scaling 및 ablation plot
- NISQ와 FT를 분리한 자원표
- 실패 사례, 적용 범위와 재현 한계
- 8~12쪽 연구 보고서와 10분 발표 자료

### 6.4 평가표

| 평가 항목 | 배점 | 우수 기준 |
|---|---:|---|
| 수학·물리 모델 정확성 | 20 | 식, 경계조건, 단위와 가정이 명시되고 독립적으로 검증된다. |
| 고전 기준선의 공정성 | 20 | 문제에 맞는 강한 solver를 사용하고 출력·오차·시간 기준을 일치시킨다. |
| 양자 알고리즘 설계 | 20 | state preparation, oracle/block encoding, 회로와 readout이 끝까지 연결된다. |
| 검증·통계·오차 분석 | 15 | exact/reference 검증, 여러 seed, 신뢰구간과 오차 분해를 제공한다. |
| 복잡도·자원 분석 | 15 | query/gate/shot과 logical/physical 자원을 분리하고 민감도를 분석한다. |
| 재현성·문서화 | 10 | 제3자가 같은 결과를 재실행하고 제한 사항을 확인할 수 있다. |

다음 중 하나라도 해당하면 속도향상 관련 평가를 통과하지 못한다.

- 동일 출력을 내는 고전 기준선이 없다.
- 상태 준비 또는 출력 추출 비용을 제외했다.
- simulator 결과를 실제 NISQ 또는 FT 장치 성능으로 표현했다.
- 작은 한두 instance만으로 점근 scaling을 주장했다.
- DFT/DMRG/DMFT의 수렴 parameter와 오차를 기록하지 않았다.
- 고전 optimizer·preprocessing 시간을 양자 비용에서 숨겼다.

## 7. 속도향상 주장 감사 체크리스트

논문 요약, 프로젝트 README와 발표 자료에서 “advantage”, “speedup”, “exponential”을 쓰기 전에 아래 항목을 모두 답한다.

### 7.1 문제와 출력

- [ ] 입력 domain, 문제 family와 instance distribution을 정의했는가?
- [ ] 고전과 양자 방법이 같은 수학적 문제를 풀고 있는가?
- [ ] 전체 벡터·전체 field, quantum state, 단일 observable 중 요구 출력이 무엇인지 명시했는가?
- [ ] approximation, discretization과 sampling 허용 오차가 같은가?
- [ ] 성공 확률과 실패 시 재실행 비용을 포함했는가?

### 7.2 입력 접근과 전처리

- [ ] classical array, QRAM, sparse oracle, sample-and-query, block encoding 중 입력 모형을 명시했는가?
- [ ] \(|b\rangle\), initial state, molecular state 또는 probability distribution 준비 비용을 포함했는가?
- [ ] matrix·Hamiltonian decomposition과 coefficient 계산 비용을 포함했는가?
- [ ] 고전 방법에도 비교 가능한 데이터 접근 권한을 주었는가?
- [ ] 문제 생성, graph embedding, basis/active-space 선택과 mesh 생성 비용을 포함했는가?

### 7.3 알고리즘 가정

- [ ] dimension 외에 sparsity, rank, locality, smoothness, gap과 condition number를 보고했는가?
- [ ] \(\kappa\), 목표 정밀도 \(\epsilon\), simulation time 의존성을 숨기지 않았는가?
- [ ] state overlap과 amplitude amplification 비용을 포함했는가?
- [ ] variational 방법의 optimizer evaluation과 gradient shot 비용을 포함했는가?
- [ ] nonlinear PDE/QLBM에서 linearization order, reset과 고전 후처리를 포함했는가?

### 7.4 출력과 검증

- [ ] observable을 얻는 shot 수와 confidence interval을 보고했는가?
- [ ] tomography 또는 전체 field 복원이 필요하다면 그 비용을 포함했는가?
- [ ] reference solution과 독립 test set으로 정확성을 검증했는가?
- [ ] 여러 seed와 instance family에서 결과가 유지되는가?
- [ ] approximation ratio뿐 아니라 time-to-solution 또는 동일 품질 도달 시간을 비교했는가?

### 7.5 고전 기준선

- [ ] PDE에는 sparse Krylov, preconditioning, multigrid, FEM 또는 spectral method 중 적절한 최신 기준선이 있는가?
- [ ] 전자구조에는 HF, DFT와 가능한 FCI/CC/DMRG 기준선이 있는가?
- [ ] 강상관 문제에는 DMRG/MPS, ED, 고전 DMFT impurity solver를 비교했는가?
- [ ] 최적화에는 exact solver뿐 아니라 강한 relaxation과 problem-specific heuristic이 있는가?
- [ ] 고전 코드도 최적화된 library와 적절한 hardware를 사용했는가?

### 7.6 NISQ와 FTQC 구분

| 구분 | NISQ 실험에서 보고할 것 | FTQC 분석에서 보고할 것 |
|---|---|---|
| qubit | physical qubit와 connectivity | logical qubit와 physical qubit 환산 |
| 회로 | native two-qubit gate depth, routing, shots | Clifford+T/Toffoli count와 logical depth |
| 오류 | device noise, calibration, mitigation 비용 | code distance, QEC cycle, logical error budget |
| 시간 | queue를 제외한/포함한 wall time을 구분 | logical runtime, decoding, factory throughput |
| 보조자원 | ancilla, reset, measurement | magic-state/T factory 수와 공간·시간 |
| 주장 범위 | 해당 장치·크기에서의 실험 결과 | 명시한 hardware/error model 아래의 추정치 |

- [ ] noise-free simulator 결과를 NISQ 실행 결과와 구분했는가?
- [ ] NISQ error mitigation의 추가 회로·shot 비용을 포함했는가?
- [ ] FT 추정에 code distance와 전체 failure budget이 있는가?
- [ ] T factory 또는 magic-state 생산을 runtime·physical qubit 계산에 포함했는가?
- [ ] 현재 hardware에서 실행했다는 주장과 미래 architecture 추정을 분리했는가?

### 7.7 결론의 강도

- [ ] “표현 가능”, “더 정확함”, “작은 상수 개선”, “scaling evidence”, “다항 속도향상”, “지수 속도향상”, “quantum advantage”를 구분했는가?
- [ ] 이론적 query complexity와 end-to-end wall time을 같은 것으로 표현하지 않았는가?
- [ ] 선택한 parameter·instance만 유리한 결과를 보고하지 않았는가?
- [ ] 유효한 문제 크기 범위와 실패 구간을 함께 공개했는가?
- [ ] 결과가 입증하지 않은 범용 산업 효과를 덧붙이지 않았는가?

최종 통과자는 새로운 양자 회로를 제안하는 데서 멈추지 않고, **어떤 조건에서 왜 유리할 수 있으며 어떤 비용이나 고전 방법 때문에 그 이점이 사라지는지**를 수식, 실행 가능한 코드, 통계와 자원표로 방어할 수 있어야 한다.
