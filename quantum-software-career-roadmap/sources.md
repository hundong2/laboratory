# 출처와 버전 확인 기록

확인일: 2026-09-13

이 문서는 학습 로드맵을 만들 때 확인한 공식 문서와 대표 원 논문을 주제별로 묶은 것이다. SDK·클라우드·컴파일러는 빠르게 바뀌므로 아래 버전은 **확인일 당시의 스냅샷**이며, 설치 직전 공식 설치 문서와 migration guide를 다시 확인한다. 논문 링크는 학습 순서를 설계하기 위한 근거이며, 특정 방법의 양자 우위를 보증하지 않는다.

## 공통 교육과 수학·물리 기반

- [IBM Quantum Learning 과정 목록](https://quantum.cloud.ibm.com/learning/en/courses): 양자 정보, 알고리즘, 오류정정, QML, 양자화학, Quantum-HPC 과정을 확인했다.
- [IBM Basics of Quantum Information](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information): 상태, 회로, 얽힘의 공통 입문 과정이다.
- [IBM Fundamentals of Quantum Algorithms](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/index): query model, search, phase estimation 등 알고리즘 기반 과정이다.
- [MIT 18.06 Linear Algebra](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/): 선형계, 고유값, positive-definite matrix의 선수 자료다.
- [MIT 18.085 Computational Science and Engineering I](https://ocw.mit.edu/courses/18-085-computational-science-and-engineering-i-summer-2020/resources/lecture-notes/): 선형대수, 미분방정식과 수치 방법을 연결한다.
- [MIT 8.04 Quantum Physics I](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2013/): 파동역학과 Schrödinger 방정식의 물리 기반이다.
- [Trefethen의 Spectral Methods 자료](https://people.maths.ox.ac.uk/trefethen/spectral.html): Fourier·Chebyshev spectral method와 공개 예제를 제공한다.

## SDK·회로·시뮬레이션

- [Qiskit 최신 API](https://quantum.cloud.ibm.com/docs/en/api/qiskit/index), [Primitives](https://quantum.cloud.ibm.com/docs/en/guides/primitives), [transpilation](https://quantum.cloud.ibm.com/docs/en/guides/transpile): 회로, V2 primitive, target 기반 변환의 현재 공식 표면이다.
- [Qiskit bit ordering](https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering): SDK 간 결과 비교 때 반드시 정규화해야 하는 표기 규칙이다.
- [Qiskit Aer](https://qiskit.github.io/qiskit-aer/): statevector, density matrix와 noise simulation용 별도 패키지다.
- [PennyLane circuits](https://docs.pennylane.ai/en/stable/introduction/circuits.html), [gradients](https://docs.pennylane.ai/en/stable/introduction/interfaces.html), [`param_shift`](https://docs.pennylane.ai/en/stable/code/api/pennylane.gradients.param_shift.html): QNode와 미분 방법의 공식 문서다.
- [Cirq basics](https://quantumai.google/cirq/start/basics), [simulation](https://quantumai.google/cirq/simulate/simulation): circuit/moment와 ideal·sampling simulation의 공식 자료다.

확인일 당시 공식 문서 표면에서 Qiskit 2.5 계열, PennyLane 0.45 계열, Cirq 1.7 계열이 관찰되었다. 이를 영구 고정 버전으로 해석하지 않으며, 프로젝트별 lock file을 만든다. Qiskit Nature, Optimization, Machine Learning과 SQD add-on은 릴리스 주기와 의존성 경계가 서로 다르므로 하나의 범용 버전 조합을 가정하지 않는다.

## 변분 알고리즘·QSCI·SQD

- [VQE 원 논문](https://doi.org/10.1038/ncomms5213): 짧은 coherent circuit와 고전 optimizer를 결합한 초기 실험이다.
- [QAOA 원 논문](https://arxiv.org/abs/1411.4028): cost/mixer Hamiltonian을 교대로 적용하는 조합 최적화 방법이다.
- [QSCI 원 논문](https://arxiv.org/abs/2302.11320): 측정으로 중요한 configuration을 선택하고 고전 부분공간에서 대각화한다.
- [Qiskit SQD 공식 개요](https://quantum.cloud.ibm.com/docs/en/addons/qiskit-addon-sqd)와 [SQD quickstart](https://qiskit.github.io/qiskit-addon-sqd/guides/quickstart.html): configuration recovery와 projected diagonalization을 포함하는 현재 hybrid workflow다.
- [Qiskit Nature](https://qiskit-community.github.io/qiskit-nature/): electronic structure, lattice model, fermion-to-qubit mapping 학습에 사용한다.

QSCI와 SQD는 관련 있지만 동의어로 취급하지 않는다. 둘 모두 quantum sampling뿐 아니라 선택한 부분공간의 고전 diagonalization 비용과 memory를 함께 측정한다.

## 선형계·PDE·유체

- [HHL 원 논문](https://arxiv.org/abs/0811.3171): sparse linear system의 해에 비례하는 **양자 상태**를 준비한다. 전체 고전 벡터 출력과 같은 계약이 아니다.
- [Childs–Kothari–Somma QLSA](https://arxiv.org/abs/1511.02306): LCU와 Fourier/Chebyshev 기법으로 정밀도 의존성을 개선한다.
- [Quantum Singular Value Transformation](https://arxiv.org/abs/1806.01838): block-encoded matrix의 singular value 변환을 통합적으로 다룬다.
- [High-precision quantum algorithms for PDE](https://quantum-journal.org/papers/q-2021-11-10-574/): finite-difference Poisson과 spectral elliptic PDE의 복잡도를 분석한다.
- [Variational quantum simulation of nonlinear PDE](https://arxiv.org/abs/1907.09032): nonlinear PDE용 변분 접근의 소규모 proof of concept다.
- [QLBM 연구 프레임워크](https://github.com/QCFD-Lab/qlbm)와 [framework 논문](https://arxiv.org/abs/2411.19439): 현재 연구용 구현의 범위와 backend 구성을 확인하는 자료다.

PDE 프로젝트에서는 discretization error, boundary encoding, condition number, state preparation, observable extraction과 전체 field 복원 비용을 나누어 기록한다.

## 물성·양자화학과 강한 고전 기준선

- [PySCF DFT 공식 문서](https://pyscf.org/user/dft.html): Kohn–Sham DFT 계산과 functional 설정의 기준 자료다.
- [OpenFermion 전자구조 워크숍](https://quantumai.google/openfermion/tutorials/intro_workshop_exercises): PySCF, second quantization, Jordan–Wigner/Bravyi–Kitaev와 sparse eigensolver를 연결한다.
- [ITensorMPS DMRG 튜토리얼](https://docs.itensor.org/ITensorMPS/stable/tutorials/DMRG.html): MPS/MPO, sweep, bond dimension과 truncation 설정을 다룬다.
- [Schollwöck MPS·DMRG 리뷰](https://arxiv.org/abs/1008.3477): 1차원 저얽힘 계에서 tensor network가 강한 이유를 설명한다.
- [TRIQS model-DMFT 튜토리얼](https://triqs.github.io/triqs/latest/userguide/python/tutorials/ModelDMFT/solutions/01s-IPT_and_DMFT.html): impurity solver와 self-consistency loop의 고전 기준 구현이다.
- [TRIQS DFTTools 튜토리얼](https://triqs.github.io/dft_tools/latest/tutorials.html): DFT+DMFT workflow용 도구이며 자동으로 정답을 보장하는 black box가 아님을 문서에서 경고한다.

DFT, DMRG, DMFT는 그 자체가 양자컴퓨터 알고리즘이 아니다. 양자 후보 해법이 실제로 보탬이 되는 범위를 판정하는 문제 정의·초기화·embedding·검증 기준선으로 학습한다.

## 양자 기계학습

- [IBM Quantum Machine Learning](https://quantum.cloud.ibm.com/learning/en/courses/quantum-machine-learning): data encoding, variational classifier와 quantum kernel의 공식 입문 과정이다.
- [Parameter-shift rule](https://doi.org/10.1103/PhysRevA.99.032331): 특정 generator spectrum을 가진 gate의 analytic gradient 근거다.
- [PennyLane quantum kernel demo](https://pennylane.ai/qml/demos/tutorial_kernels_module)와 [kernel training demo](https://pennylane.ai/qml/demos/tutorial_kernel_based_training): kernel matrix와 trainable kernel 실습이다.
- [Barren plateaus 원 연구](https://doi.org/10.1038/s41467-018-07090-4), [local/global cost 연구](https://doi.org/10.1038/s41467-021-21728-w): gradient variance scaling과 cost locality의 영향을 다룬다.
- [Power of data in QML](https://www.nature.com/articles/s41467-021-22539-9): 고전 모델과 classical surrogate를 포함한 공정한 비교가 필요한 근거다.

## 언어·IR·컴파일러

- [OpenQASM 3.1 specification](https://openqasm.com/versions/3.1/index.html): 확인일 당시 안정판 사양이다. 기본 페이지의 개발 HEAD와 버전을 혼동하지 않는다.
- [QIR specification](https://github.com/qir-alliance/qir-spec/blob/main/specification/README.md)과 [QIS](https://github.com/qir-alliance/qir-spec/blob/main/specification/Instruction_Set.md): LLVM 기반 IR, profile과 quantum instruction set의 계약을 정의한다.
- [MLIR documentation](https://mlir.llvm.org/docs/), [Toy tutorial](https://mlir.llvm.org/docs/Tutorials/Toy/), [Dialect Conversion](https://mlir.llvm.org/docs/DialectConversion/): dialect, rewrite, legality와 lowering을 배우는 공식 자료다.
- [LLVM Kaleidoscope tutorial](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/): lexer/parser에서 LLVM IR generation까지의 compiler 기초다.

QIR 2.0은 LLVM 16 이상의 opaque pointer model을 전제로 한다. 어떤 backend가 QIR을 지원한다고 할 때는 단순히 “QIR 지원”이라고 쓰지 않고, 지원하는 **profile과 QIS 조합**을 기록한다.

## Fault tolerance·자원 추정·Quantum-HPC

- [IBM Fault-tolerant quantum computing 과정](https://quantum.cloud.ibm.com/learning/en/courses/foundations-of-quantum-error-correction/fault-tolerant-quantum-computing/introduction): logical operation과 오류정정 기반을 다룬다.
- [Microsoft Quantum Resource Estimator](https://learn.microsoft.com/en-us/azure/quantum/intro-to-resource-estimation): logical algorithm에서 physical qubit과 runtime overhead를 추정하는 공식 도구다.
- [CUDA-Q documentation](https://nvidia.github.io/cuda-quantum/latest/index.html)과 [multi-QPU/MPI simulation](https://nvidia.github.io/cuda-quantum/latest/using/backends/sims/mqpusims.html): C++·Python hybrid programming과 분산 simulation의 현재 경계를 확인한다.
- [Amazon Braket Hybrid Jobs](https://docs.aws.amazon.com/braket/latest/developerguide/braket-jobs.html): classical container와 QPU task를 묶는 managed asynchronous workflow다.
- [IBM Qiskit Serverless](https://quantum.cloud.ibm.com/docs/en/guides/serverless): 확인일 현재 실험적 기능이며 이용 plan·배포 방식 제약을 확인해야 한다.

클라우드 실행은 API 호출 한 번으로 끝나는 동기 함수가 아니다. queue, cancellation, timeout, idempotency, checkpoint, artifact provenance, credential, 비용과 data residency를 architecture contract에 포함한다.

## 사용 원칙

1. 튜토리얼 코드를 복사하기 전에 해당 페이지의 현재 버전과 Python 지원 범위를 확인한다.
2. SDK별 가상환경과 lock file을 분리하고 Python, package, backend, seed, shots를 결과와 함께 저장한다.
3. simulator 결과를 QPU 또는 fault-tolerant 성능으로 표현하지 않는다.
4. 논문의 asymptotic claim과 현재 구현의 wall time을 같은 숫자처럼 비교하지 않는다.
5. 새로운 양자 우위를 주장하기 전 같은 입력·출력·오차 계약의 최신 고전 기준선을 먼저 실행한다.
