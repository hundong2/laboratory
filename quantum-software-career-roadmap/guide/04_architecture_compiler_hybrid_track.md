# 양자 소프트웨어 아키텍처·컴파일러·FTQC·Quantum-HPC 트랙

작성일: 2026-09-13

권장 학습량: 주 10~12시간

선행 과정: [공통 기반 40주](01_common_foundations.md)

## 목차

- [과정의 목표와 권장 순서](#과정의-목표와-권장-순서)
- [표준과 도구의 현재 경계](#표준과-도구의-현재-경계)
- [공통 선수지식과 진입 시험](#공통-선수지식과-진입-시험)
- [트랙 D: 양자 소프트웨어 아키텍처](#트랙-d-양자-소프트웨어-아키텍처)
- [트랙 E: MLIR·OpenQASM·QIR 양자 회로 컴파일러](#트랙-e-mliropenqasmqir-양자-회로-컴파일러)
- [트랙 E 심화: 하드웨어 이해·오류정정·FTQC 자원 추정](#트랙-e-심화-하드웨어-이해오류정정ftqc-자원-추정)
- [트랙 F: Quantum-HPC·클라우드·API 통합](#트랙-f-quantum-hpc클라우드api-통합)
- [언어별 역할과 인터페이스 전략](#언어별-역할과-인터페이스-전략)
- [통합 포트폴리오와 평가 기준](#통합-포트폴리오와-평가-기준)
- [공식 학습 자료](#공식-학습-자료)

## 과정의 목표와 권장 순서

이 문서는 양자 알고리즘을 직접 발명하는 과정보다, 알고리즘을 **표현하고 변환하고 실행하며 운영하는 소프트웨어 계층**을 설계하는 세 직무를 위한 네 가지 전문 과정을 제공한다. 하드웨어·FTQC 과정은 별도 직무가 아니라 회로 컴파일러의 심화 과정이다.

| 트랙 | 핵심 질문 | 권장 기간 | 대표 결과물 |
| --- | --- | ---: | --- |
| D. 소프트웨어 아키텍처 | 서로 다른 SDK·backend·job을 어떻게 안정된 계약으로 묶는가? | 8주 | `portable-qpu-gateway` |
| E. 회로 컴파일러 | source circuit를 target에 적법한 프로그램으로 어떻게 낮추고 검증하는가? | 16주 | `target-aware-quantum-compiler` |
| E 심화. 하드웨어·FTQC | logical algorithm을 어떤 오류정정 가정과 물리 자원으로 평가하는가? | 12주 | `fault-tolerant-resource-study` |
| F. Quantum-HPC 통합 | CPU·GPU·QPU 작업을 scheduler·cloud API와 어떻게 결합하는가? | 12주 | `quantum-hpc-workflow` |

처음부터 네 트랙을 병렬로 시작하지 않는다. 다음 순서가 가장 안전하다.

```text
공통 기반
  → 아키텍처 1~4주: program·target·job·result 계약
    → 컴파일러 1~12주: parser·IR·rewrite·lowering·target mapping
      ├─ 하드웨어·FTQC: logical ISA·QEC·resource estimation
      └─ Quantum-HPC: scheduler·runtime·cloud·API·운영
```

- **아키텍처 직무**는 D 전 과정을 이수한 뒤 F의 1~2주, 7~10주를 보조 과정으로 듣는다.
- **컴파일러 직무**는 E를 주력으로 하고 [회로 검증 과정](03_circuit_and_qml_track.md)의 1~7주를 먼저 통과한다.
- **fault-tolerant compiler 직무**는 E의 1~12주와 E 심화 전 과정을 모두 이수한다.
- **Quantum-HPC 통합 직무**는 D의 1~7주와 F 전 과정을 이수하고 E의 8~10주를 통해 artifact 경계를 이해한다.
- ML 기반 compiler 최적화는 E의 마지막 선택 과목이다. 의미 보존·legality·고전 heuristic 기준선을 만들기 전에 시작하지 않는다.

각 주차는 달력이 아니라 exit gate다. 통과 증거가 없으면 다음 주차로 넘어가지 않는다.

## 표준과 도구의 현재 경계

> 아래 내용은 **2026-09-13 확인 스냅샷**이다. 표준의 개발 branch, 클라우드 target, SDK API와 제공 plan은 바뀔 수 있다. 실습 당일 공식 문서와 release를 다시 확인하고 사용한 commit·version·target capability snapshot을 결과에 기록한다.

### 반드시 구분해야 할 표현 계층

| 계층 | 대표 표현·도구 | 표현하는 것 | 단독으로 보장하지 않는 것 |
| --- | --- | --- | --- |
| 알고리즘·source | Python/C++ DSL, Q#, Qiskit circuit, PennyLane tape | 사용자의 양자·고전 계산 의도 | 특정 QPU에서의 실행 가능성 |
| 교환용 assembly | **OpenQASM 3.1** | gate, timing, classical control을 포함한 프로그램 문법·의미 | vendor calibration과 job/runtime API |
| 다단계 compiler IR | **MLIR** dialect | 높은 수준 연산에서 target 수준으로 단계적 lowering | 양자 instruction 의미 자체 |
| LLVM 기반 양자 IR | **QIR 2.0** | LLVM IR 위의 quantum runtime 호출과 entry-point 계약 | 모든 backend가 모든 QIR을 받는다는 보장 |
| backend capability | Qiskit `Target`, provider target metadata | qubit, instruction, connectivity, duration, error와 제약 | snapshot 이후의 calibration 상태 |
| runtime·job | provider API, QIR runtime, Qiskit Runtime, Braket Hybrid Jobs | 제출, queue, 실행, 결과, 취소와 오류 계약 | 회로 의미 보존 또는 성능 우위 |
| FT 자원 모델 | Qualtran, Microsoft Resource Estimator | 논리 자원과 QEC·하드웨어 가정 아래의 물리 자원 추정 | 실제 장비 납기나 실측 runtime |

### 2026-09-13 기준 호환성 경계

1. **OpenQASM 3.1이 확인 기준 안정판이다.** [3.1 사양](https://openqasm.com/versions/3.1/index.html)을 학습 기준으로 고정한다. [OpenQASM 저장소](https://github.com/openqasm/openqasm)의 개발 중 문서와 안정판을 섞지 않는다. 공개 grammar는 parse tree를 만드는 참고 구현이며 완전한 semantic validation을 보장하지 않는다. 따라서 “parse 성공”을 “올바른 양자 프로그램”으로 판정하지 않는다.
2. **QIR 2.0은 LLVM 16 이상을 요구한다.** LLVM의 opaque pointer 전환 때문이다. QIR version과 LLVM version은 1:1 번호 체계가 아니므로 `QIR 2.0 == LLVM 2.0`처럼 해석하지 않는다. producer·transformer·runner가 사용하는 LLVM major를 함께 고정한다.
3. **backend 지원 단위는 ‘QIR’ 한 단어가 아니다.** [QIR specification](https://github.com/qir-alliance/qir-spec/blob/main/specification/README.md)의 **profile**과 [QIS (Quantum Instruction Set)](https://github.com/qir-alliance/qir-spec/blob/main/specification/Instruction_Set.md) 조합, runtime convention과 target 제약을 함께 확인한다. 어떤 backend가 Base Profile만 받는다면 dynamic allocation이나 결과 기반 control이 포함된 unrestricted module을 그대로 실행할 수 있다고 가정하지 않는다.
4. [QIR Alliance QAT](https://github.com/qir-alliance/qat)는 변환·적응 도구로 학습할 수 있지만, README의 `qat --validate` 예시는 확인 기준 **“not implemented yet”**로 표시되어 있다. 문서화된 validation 목표와 실제 CLI 구현을 구분하고, 선택한 revision에서 명령이 존재함을 직접 확인하기 전에는 이를 CI 통과 gate로 쓰지 않는다.
5. [Azure Quantum target profile 문서](https://learn.microsoft.com/en-us/azure/quantum/quantum-computing-target-profiles)의 확인 기준으로 hardware 지원 범위가 profile마다 다르다. **Base**는 문서에 열거된 IonQ·Rigetti simulator/QPU가, **Adaptive RI**는 열거된 Quantinuum H2 simulator/QPU가 지원한다. 반면 **Adaptive RIF**와 **Adaptive**를 지원하는 Azure Quantum target은 현재 없으며 로컬 QDK simulator에서만 시험할 수 있다. **Unrestricted**도 현재 지원 quantum target이 없고 QDK simulator용이다. 따라서 로컬에서 성공했다는 사실이 hardware-ready를 뜻하지 않으며, 제출 시점에 정확한 provider target과 capability를 다시 확인한다.
6. Qiskit transpilation은 `init → layout → routing → translation → optimization → scheduling` 단계로 이해한다. [공식 transpiler stage 문서](https://quantum.cloud.ibm.com/docs/en/guides/transpiler-stages)에서 scheduling은 자동으로 항상 수행되는 단계가 아니며 명시적 요청과 target timing 정보가 필요하다.
7. MLIR은 quantum language가 아니라 compiler infrastructure다. dialect, verifier, rewrite, conversion target과 lowering을 직접 설계해야 한다. [MLIR 문서](https://mlir.llvm.org/docs/)와 [LLVM IR lowering 문서](https://mlir.llvm.org/docs/TargetLLVMIR/)를 기준으로 한다.

### 모든 결과물에 붙일 capability manifest

다음 항목을 machine-readable YAML 또는 JSON으로 남긴다.

```yaml
source_language: openqasm
source_version: "3.1"
compiler_revision: "<40-char commit SHA>"
llvm_major: 16
qir_version: "2.0"
qir_profile: "<backend-advertised exact profile identifier>"
qis: ["<supported instruction set names>"]
target_snapshot_id: "<provider/target/calibration timestamp>"
dynamic_qubit_management: false
result_dependent_control: false
shots: 1000
seed: 1234
```

값을 알 수 없으면 추측한 기본값을 넣지 말고 `unknown`과 확인 실패 이유를 기록한다.

## 공통 선수지식과 진입 시험

### 최소 선수지식

| 영역 | 필요한 수준 | 먼저 복습할 내용 |
| --- | --- | --- |
| 양자 정보 | 1·2-qubit 회로, 측정, density matrix, noise를 설명 | [IBM Basics of Quantum Information](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information) |
| 회로 | logical circuit와 ISA circuit, basis, connectivity, layout을 구분 | [회로 검증 과정](03_circuit_and_qml_track.md) |
| compiler | lexer/parser, AST, SSA, CFG, dominance, pass, data-flow 기초 | [LLVM Kaleidoscope](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/) |
| 시스템 | process/thread, async I/O, queue, retry, timeout, idempotency | 작은 비동기 job service 구현 |
| 분산/HPC | distributed memory, collective, scheduler, container 기초 | MPI hello world와 Slurm batch job |
| 수학 | 선형대수, graph, 확률, 복잡도와 benchmark 통계 | [공통 기반](01_common_foundations.md) |
| 개발 도구 | Git, CMake, Python packaging, unit/integration test, profiler | 깨끗한 환경의 one-command build |

### 언어별 최소 과제

- **Python**: `Protocol` 또는 abstract base class로 `Backend`, `Job`, `Result`를 정의하고 fake backend 두 개를 붙인다.
- **C++**: CMake로 library와 CLI를 분리하고, ownership·RAII·error type을 명시한다. compiler 트랙은 C++17 이상, CUDA-Q 실습은 공식 요구에 맞춰 C++20을 사용한다.
- **Rust**: `enum`으로 job state와 error를 모델링하고, `Result`를 통해 parse·validation 실패를 호출자에게 보존한다.
- 세 언어를 모두 전문가 수준으로 시작할 필요는 없다. Python을 orchestration 기준으로 삼고, E 트랙은 C++, parser/runtime 안전성에 관심이 있으면 Rust를 보조 언어로 선택한다.

### 진입 시험

다음을 모두 통과해야 전문 트랙을 시작한다.

1. Bell circuit를 logical gate 목록으로 표현하고 두 개의 서로 다른 basis로 변환한 뒤 global phase를 허용해 의미를 비교한다.
2. 5-qubit coupling graph에서 허용되지 않는 CX를 찾아 SWAP을 삽입하고 최종 logical-to-physical mapping을 계산한다.
3. `CREATED → VALIDATING → QUEUED → RUNNING → SUCCEEDED|FAILED|CANCELLED|TIMED_OUT` 상태기계를 구현하고 금지된 전이를 테스트한다.
4. 같은 idempotency key로 두 번 제출해 계산이 하나만 생성되는지 검증한다.
5. parser가 성공하지만 선언되지 않은 identifier를 포함한 입력을 만들어 syntactic parse와 semantic validation의 차이를 설명한다.
6. 1·2·4 worker에서 독립 circuit batch의 wall time, throughput, serialization 비용을 분리해 측정한다.

통과 증거는 코드, 자동 테스트, 환경 lock, 실행 로그와 2쪽 이내 설계 기록이다.

## 트랙 D: 양자 소프트웨어 아키텍처

### 역할과 선수지식

이 트랙은 여러 SDK와 provider를 하나의 얇은 추상화로 감추는 것이 목표가 아니다. 서로 다른 능력을 공통 최소분모로 지워 버리지 않고, **capability를 명시적으로 협상하는 확장 가능한 시스템**을 설계하는 것이 목표다.

진입 전에 다음을 할 수 있어야 한다.

- circuit/program, compile artifact, target snapshot, job과 result를 서로 다른 객체로 설명한다.
- 동기 함수 호출과 장시간 비동기 job의 오류 모델 차이를 설명한다.
- credential, 사용자 입력, compiler service, provider, artifact store의 신뢰 경계를 그린다.
- Python type hint와 test double을 사용할 수 있다.

### 1주차: 도메인 모델과 경계

**학습**

- bounded context: authoring, compilation, execution, result analysis
- logical program과 target-specific artifact의 분리
- `Program`, `TargetSnapshot`, `CompilationRequest`, `Artifact`, `Job`, `Result`의 식별자와 불변조건
- control plane과 data plane, online metadata와 immutable artifact의 차이

**실습**

1. 위 여섯 객체의 JSON Schema를 만든다.
2. compiler version, source hash, target snapshot과 option으로 artifact digest를 계산한다.
3. result가 source·artifact·backend·calibration·shots·seed로 역추적되는 provenance graph를 만든다.

**통과 기준**

- program ID와 execution ID를 혼동하지 않는다.
- mutable 최신 calibration 대신 제출 당시 snapshot 또는 그 식별자를 보존한다.
- 결과 파일만 받아도 사용한 code·config·target을 찾을 수 있다.

### 2주차: Ports and Adapters

**학습**

- dependency inversion, provider adapter와 anti-corruption layer
- capability query와 feature negotiation
- Qiskit `BackendV2`·`Target` 같은 구체 API와 내부 domain contract의 분리
- vendor-specific extension을 보존하는 방법

**실습**

Python `Protocol`로 다음 최소 계약을 만든다.

```python
class CompilerPort(Protocol):
    def compile(self, request: CompilationRequest) -> Artifact: ...

class ExecutionPort(Protocol):
    async def submit(self, artifact: Artifact, *, idempotency_key: str) -> Job: ...
    async def get(self, job_id: str) -> Job: ...
    async def cancel(self, job_id: str) -> Job: ...
```

fake simulator와 제한된 fake QPU adapter를 구현한다. 후자는 mid-circuit measurement나 dynamic allocation을 지원하지 않게 만들고 사전 검증에서 거부한다.

**통과 기준**

- 지원하지 않는 기능이 provider 내부 오류가 아니라 제출 전 구조화된 capability 오류로 나온다.
- vendor extension을 버리지 않으면서 공통 코드가 vendor module을 import하지 않는다.
- contract test 한 벌이 두 adapter에 동일하게 실행된다.

### 3주차: Target registry와 compiler service

**학습**

- target discovery, versioned capability, calibration TTL
- compile cache key와 재현성
- immutable artifact store와 content-addressed storage
- compile timeout, resource limit와 untrusted input

**실습**

1. `TargetRegistry`와 `CompilerService`를 분리한다.
2. 같은 source라도 target snapshot이나 compiler option이 다르면 다른 artifact가 되는지 테스트한다.
3. OpenQASM input 크기, include depth와 compile 시간을 제한한다.

**통과 기준**

- cache key에 source, compiler, target, option이 모두 포함된다.
- expired target 정보로 hardware artifact를 조용히 재사용하지 않는다.
- compiler worker가 실패해도 원본과 마지막 성공 artifact는 손상되지 않는다.

### 4주차: 비동기 job과 상태기계

**학습**

- at-least-once delivery, idempotency, deduplication
- polling, webhook, backoff와 jitter
- timeout, cancellation, provider terminal state 정규화
- saga와 compensating action의 적용 한계

**실습**

job state machine을 만들고 다음 fault를 주입한다.

- submit 응답 손실 후 retry
- provider가 job을 받았지만 gateway가 timeout
- 동일 webhook의 중복·역순 도착
- cancel과 success의 경쟁
- worker 재시작 후 checkpoint 복구

**통과 기준**

- duplicate submit이 duplicate QPU 비용으로 이어지지 않는다.
- terminal state가 다른 terminal state로 되돌아가지 않는다.
- 취소 요청과 실제 취소 성공을 구분한다.
- client timeout을 provider job 실패로 기록하지 않는다.

### 5주차: API와 데이터 계약

**학습**

- REST/OpenAPI와 gRPC의 선택 기준
- long-running operation, pagination, problem detail, versioning
- 대용량 circuit/result의 object-store handoff
- schema compatibility와 consumer-driven contract test

**실습**

`POST /compilations`, `POST /jobs`, `GET /jobs/{id}`, `POST /jobs/{id}:cancel`과 artifact download 계약을 작성한다. 외부 도구 호환성이 중요하면 널리 지원되는 OpenAPI 3.1을 우선하고, 3.2 기능은 client generator가 지원하는지 먼저 확인한다.

**통과 기준**

- retry 가능한 오류와 영구 오류를 구분한다.
- credential과 대형 binary를 job metadata에 직렬화하지 않는다.
- old client가 모르는 optional field를 받아도 깨지지 않는다.

### 6주차: 보안과 multi-tenant 운영

**학습**

- least privilege, secret rotation, tenant isolation
- input validation, artifact integrity, dependency provenance
- quota, cost budget와 denial-of-wallet
- audit log와 민감 정보 redaction
- [OWASP API Security Top 10](https://api-security.owasp.org/editions/2023/en/0x03-introduction/)

**실습**

1. tenant가 다른 사용자의 job ID를 추측해 조회하는 공격을 차단한다.
2. provider token은 secret store에서 adapter 실행 시점에만 주입한다.
3. shots, circuit size, concurrent jobs와 금액에 quota를 둔다.

**통과 기준**

- source, log, trace, exception과 artifact에 token이 없다.
- authorization은 UI가 아니라 resource별 server-side 검사다.
- 사용량 초과가 submit 이후가 아니라 가능한 한 사전에 거부된다.

### 7주차: 관측 가능성과 신뢰성 시험

**학습**

- log, metric, distributed trace의 역할
- queue, compile, transfer, provider, QPU, post-process 시간 분해
- SLI/SLO, retry storm, circuit breaker와 backpressure
- [OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/)

**실습**

한 job의 trace에 `validate`, `compile`, `upload`, `queue`, `execute`, `download`, `postprocess` span을 연결한다. provider mock에 latency, 429, 500, malformed result와 partial outage를 주입한다.

**통과 기준**

- end-to-end latency만 보고 QPU 실행이 느리다고 결론내리지 않는다.
- retry budget과 최대 동시 요청 수가 있다.
- trace에는 circuit 본문이나 credential 대신 hash와 안전한 metadata만 남는다.

### 8주차: Architecture capstone

**실습**

`portable-qpu-gateway`를 완성한다.

```text
client
  → API/auth/quota
    → capability validation
      → compiler port → immutable artifact store
        → execution port → provider
          → event normalizer → result/provenance store
```

두 fake provider와 선택 가능한 실제 cloud provider 하나를 adapter로 붙인다. 실제 계정이 없으면 cloud 호출은 contract fixture로 대체하고 hardware 실행을 주장하지 않는다.

**최종 통과 기준**

- architecture decision record 5개 이상이 trade-off와 기각안을 포함한다.
- provider별 capability 차이가 manifest와 test에 드러난다.
- timeout·중복·취소·부분 실패·복구를 자동 시험한다.
- 위협 모델, secret 경계, quota와 관측 dashboard가 있다.
- clean environment에서 한 명령으로 local demo가 실행된다.

### 포트폴리오: `portable-qpu-gateway`

필수 제출물:

- C4 context/container diagram과 trust-boundary diagram
- JSON Schema 또는 protobuf와 API specification
- 두 provider adapter의 contract test
- job state transition table과 failure-injection report
- target snapshot·artifact·result provenance 예시
- OpenTelemetry trace와 latency breakdown
- 보안·비용 한도·운영 runbook
- “공통 추상화로 표현하지 못한 provider 기능” 목록

좋은 포트폴리오는 provider 수가 많기보다, 지원 범위와 실패 의미가 정확하다.

## 트랙 E: MLIR·OpenQASM·QIR 양자 회로 컴파일러

### 역할과 선수지식

이 트랙의 목표는 syntax converter가 아니라 **의미 보존과 target legality를 증명 가능한 방식으로 관리하는 compiler pipeline**을 만드는 것이다.

진입 전에 다음을 통과한다.

- C++의 value/reference, RAII, template 기초와 CMake build
- parser, AST, symbol table, type checking, SSA와 basic block 설명
- graph traversal, shortest path, matching 또는 heuristic 기초
- unitary circuit의 equivalence와 measurement circuit의 통계적 검증 차이
- basis gate, coupling graph와 timing constraint 설명

### 1~2주차: LLVM compiler 기초

**학습**

- lexer → parser → AST → semantic analysis → IR → optimization → code generation
- LLVM IR의 function, basic block, instruction, SSA, dominance
- verifier와 pass manager
- [LLVM Kaleidoscope tutorial](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/)

**실습**

작은 수식 언어에 type error, undefined symbol, function call과 custom optimization 하나를 추가한다. IR 생성 전 semantic error와 IR verifier error를 분리한다.

**통과 기준**

- parse 성공과 type-correct를 구분한다.
- invalid IR을 backend까지 보내지 않는다.
- optimization 전후 결과를 reference interpreter와 differential test한다.

### 3~4주차: MLIR operation·dialect·SSA

**학습**

- operation, region, block, value, type, attribute와 trait
- declarative operation definition과 custom verifier
- textual IR round trip
- [MLIR Language Reference](https://mlir.llvm.org/docs/LangRef/)와 [Toy tutorial](https://mlir.llvm.org/docs/Tutorials/Toy/)

**실습**

`qtoy` dialect를 만들고 `alloc`, `h`, `cx`, `measure`, `return` operation을 정의한다. qubit ownership, operand/result type와 measurement result type의 불변조건을 verifier에 넣는다.

**통과 기준**

- parse/print round trip 뒤 구조가 보존된다.
- 잘못된 operand type, 중복 소비, 누락된 terminator가 verifier에서 실패한다.
- verifier 오류가 source location과 원인을 제공한다.

### 5~6주차: Rewrite·pass·dialect conversion

**학습**

- canonicalization, pattern rewrite, greedy rewrite의 종료성
- analysis와 transformation pass 분리
- partial/full conversion, legal·illegal operation
- type converter, conversion target와 [Dialect Conversion](https://mlir.llvm.org/docs/DialectConversion/)
- [Pass Management](https://mlir.llvm.org/docs/PassManagement/)

**실습**

1. inverse gate cancellation과 adjacent rotation folding을 구현한다.
2. high-level `bell` operation을 gate dialect로 낮춘다.
3. target basis 밖의 gate를 illegal로 표시하고 conversion이 남기면 실패시킨다.

**통과 기준**

- rewrite 전후 small statevector 또는 unitary가 global phase까지 일치한다.
- rewrite가 무한 반복되지 않고 deterministic하다.
- `full conversion succeeded`가 정말 모든 illegal operation 제거를 의미한다.

### 7주차: OpenQASM 3.1 front end

**학습**

- [OpenQASM 3.1](https://openqasm.com/versions/3.1/index.html)의 declaration, gate, measurement, classical expression, control flow와 timing 표현
- concrete syntax, AST와 semantic model의 차이
- include resolution, source span, diagnostic recovery
- [reference grammar](https://openqasm.com/versions/3.1/grammar/index.html)의 parse-only 경계

**실습**

지원할 3.1 subset을 명세한 뒤 parser 출력을 내부 AST로 옮긴다. duplicate declaration, type/width mismatch, unresolved gate, unsupported control flow와 include cycle을 semantic validator에서 거부한다.

**통과 기준**

- 지원 subset과 미지원 syntax를 표로 공개한다.
- parse 성공 입력의 semantic error를 별도 test corpus로 보유한다.
- 원본 source span이 MLIR diagnostic까지 이어진다.
- 개발 HEAD 문법을 3.1 안정판 기능으로 잘못 표시하지 않는다.

### 8주차: QIR 2.0과 LLVM lowering

**학습**

- QIR module, entry point, quantum runtime 호출과 QIS intrinsic
- Base·adaptive·unrestricted profile이 제약하는 resource와 control
- static/dynamic qubit·result management
- LLVM opaque pointer와 QIR 2.0의 LLVM 16+ 요구
- [QIR specification](https://github.com/qir-alliance/qir-spec/blob/main/specification/README.md), [Base Profile](https://github.com/qir-alliance/qir-spec/blob/main/specification/profiles/Base_Profile.md), [QIS](https://github.com/qir-alliance/qir-spec/blob/main/specification/Instruction_Set.md)

**실습**

같은 Bell program을 두 가지로 내보낸다.

1. static resource와 제한된 control을 쓰는 Base Profile 후보
2. 로컬 simulator에서만 시험할 unrestricted 후보

각 module에 required qubits/results, profile·QIS와 entry-point metadata를 기록한다.

**통과 기준**

- LLVM 16+ toolchain으로 생성·parse·verify한다.
- opaque pointer를 typed pointer 예제와 섞지 않는다.
- profile 위반 feature를 code generation 전에 거부한다.
- “QIR output 생성”과 “특정 backend 실행 가능”을 구분한다.

### 9주차: PyQIR·QIR Runner·QAT 실습

**학습**

- [PyQIR](https://github.com/qir-alliance/pyqir)의 Python builder와 Rust `qirlib` 경계
- [QIR Runner](https://github.com/qir-alliance/qir-runner)의 runner API/CLI와 sparse simulation
- [QAT](https://github.com/qir-alliance/qat)의 adaptation 목표와 실제 구현 상태

**실습**

1. PyQIR로 작은 module을 만들고 LLVM verifier와 QIR Runner에서 실행한다.
2. QAT을 선택한 고정 commit으로 build하고 `--help`·test suite로 실제 명령을 조사한다.
3. profile/QIS manifest와 module 검사 결과를 함께 저장한다.

**통과 기준**

- PyQIR, LLVM, QIR Runner revision을 모두 고정한다.
- QIR Runner simulation 성공을 실제 QPU 호환성으로 확대 해석하지 않는다.
- QAT README에서 미구현으로 표시된 `qat --validate`를 실행했다고 꾸미지 않는다. 필요한 validation은 독립 verifier·정적 검사·backend dry run으로 구성하고 그 한계를 기록한다.

### 10주차: Qiskit target과 transpiler pipeline

**학습**

- [Qiskit transpiler stages](https://quantum.cloud.ibm.com/docs/en/guides/transpiler-stages)
- `init`, `layout`, `routing`, `translation`, `optimization`, `scheduling`
- [custom backend](https://quantum.cloud.ibm.com/docs/guides/custom-backend)와 `Target`
- basis instruction, coupling, instruction property, duration와 error snapshot

**실습**

선형, ring, heavy-hex-like toy topology의 fake target을 만들고 동일 circuit corpus를 transpile한다. initial layout와 optimization level을 고정·변경해 효과를 분리한다.

**통과 기준**

- transpiled circuit의 모든 2-qubit gate가 target edge에 적법하다.
- final layout을 observable·measurement 해석에 반영한다.
- target snapshot이 바뀐 결과를 같은 benchmark sample로 합치지 않는다.

### 11주차: Layout와 routing

**학습**

- subgraph/isomorphism 관점의 placement
- shortest path, SWAP insertion와 token swapping
- routing 최적화의 계산 난도와 heuristic
- SABRE baseline, direction correction와 ancilla trade-off

**실습**

작은 topology는 exhaustive search로 oracle을 만들고, greedy·random·SABRE와 비교한다. [MQT Bench](https://github.com/munich-quantum-toolkit/bench) 또는 라이선스를 확인한 작은 공개 corpus를 사용한다.

측정 항목:

- 2-qubit gate와 SWAP 수
- depth와 2-qubit depth
- compiler wall time와 peak memory
- 성공률과 최악 회귀

**통과 기준**

- heuristic이 항상 optimal이라고 주장하지 않는다.
- 작은 oracle과 held-out topology에서 baseline을 비교한다.
- mapping 오류 0건, 지원하지 않는 circuit은 명시적 실패다.

### 12주차: Translation·optimization·scheduling

**학습**

- basis decomposition과 gate synthesis
- commutation, cancellation, resynthesis와 cost model
- ASAP/ALAP scheduling, alignment, granularity와 instruction duration
- logical depth와 시간 단위 schedule의 차이

**실습**

optimization 전후 의미를 검사하고, duration이 있는 target에서 ASAP와 ALAP를 비교한다. duration이 없는 target에는 임의 시간을 생성하지 않고 scheduling을 건너뛴다.

**통과 기준**

- scheduling을 수행했는지 metadata로 명확히 기록한다.
- pulse/timing constraint 위반이 0건이다.
- gate count 감소가 duration 또는 estimated error 감소와 같다고 단정하지 않는다.

### 13주차: 의미 보존과 compiler 검증

**학습**

- IR verifier, property-based test, differential test
- global-phase-aware unitary equivalence
- measurement mapping과 distribution test
- symbolic/decision-diagram equivalence와 scalability 한계
- [MQT QCEC](https://github.com/munich-quantum-toolkit/qcec)

**실습**

- 각 pass를 단독·조합으로 random small circuit에 적용한다.
- unitary circuit는 exact/equivalence checker로 검사한다.
- measurement·dynamic circuit는 지원 범위에 맞는 reference execution과 classical mapping을 검사한다.
- 잘못된 rewrite를 mutation으로 주입해 test가 실제로 실패하는지 확인한다.

**통과 기준**

- 지원 범위 안에서 semantic mismatch가 0건이다.
- timeout을 equivalent로 간주하지 않는다.
- equivalence tool이 지원하지 않는 dynamic behavior를 문서화한다.

### 14주차: Benchmark와 regression 관리

**학습**

- corpus stratification, train/tune/test 분리
- target·seed·compiler revision pinning
- quality/runtime Pareto와 tail regression
- bootstrap confidence interval, multiple comparison과 cherry-picking 방지

**실습**

크기·구조·gate family별 corpus manifest를 만든다. baseline과 후보 pass manager를 여러 seed로 실행하고 raw result, 실패 목록, summary를 분리한다.

**통과 기준**

- compiler tuning에 쓴 circuit와 최종 test circuit가 분리된다.
- 평균 개선만이 아니라 median, p95, 최악 회귀와 compile overhead를 보고한다.
- 실패·timeout·unsupported sample을 분모에서 몰래 제거하지 않는다.

### 15주차: ML 기반 compiler 최적화 — 선택

**학습**

- [MLGO](https://llvm.org/docs/MLGO.html)의 model-guided decision 구조
- correctness decision과 profitability/choice decision 분리
- imitation, ranking 또는 reinforcement learning의 데이터 누수
- safe fallback, uncertainty와 inference overhead

**실습**

legality와 의미 보존은 rule/verifier가 담당하게 하고, 모델은 적법한 initial layout 또는 rewrite 후보의 순위만 선택하게 한다. 작은 exact oracle과 SABRE/hand-written heuristic을 baseline으로 둔다.

**통과 기준**

- 학습 모델이 illegal transformation을 허가할 권한이 없다.
- unseen circuit와 unseen topology를 분리해 평가한다.
- training 비용, inference latency, model artifact와 fallback을 포함한다.
- baseline 대비 우위가 없으면 그 결과를 그대로 보고한다.

### 16주차: Compiler capstone

**실습**

`target-aware-quantum-compiler`를 완성한다.

```text
OpenQASM 3.1 subset
  → parser + semantic validation
    → qtoy/high-level MLIR
      → canonicalization
        → target mapping + basis lowering + scheduling
          → QIR 2.0 or target circuit artifact
            → verifier + runner/backend adapter
```

**최종 통과 기준**

- 3.1 subset과 extension 정책이 문서화되어 있다.
- 모든 stage 전후에 verifier 또는 명시적 invariant가 있다.
- 지원 subset에서 parse·semantic·legality·equivalence test를 모두 통과한다.
- QIR 2.0/LLVM 16+와 profile+QIS manifest를 정확히 기록한다.
- Azure 제출 후보는 target profile 제한에 맞는지 사전 검사한다. Adaptive RI의 문서상 지원 target과 Adaptive RIF·Adaptive·Unrestricted의 local-only/unsupported 범위를 구분한다.
- benchmark가 raw data부터 report까지 한 명령으로 재생성된다.

### 포트폴리오: `target-aware-quantum-compiler`

필수 제출물:

- language subset 명세와 diagnostic catalog
- MLIR dialect·verifier·pass pipeline 문서
- OpenQASM source span에서 최종 diagnostic까지의 추적 예시
- QIR profile·QIS·LLVM version manifest
- target topology별 layout/routing/scheduling report
- equivalence·property·mutation test report
- MQT Bench 계열 corpus의 재현 가능한 benchmark
- 정확성 판단과 최적화 선택을 구분한 설계 기록
- QAT `validate` 미구현 등 사용 도구의 실제 제한 목록

## 트랙 E 심화: 하드웨어 이해·오류정정·FTQC 자원 추정

### 역할과 선수지식

이 트랙은 device physics 전공 전체를 대신하지 않는다. compiler·architecture 개발자가 logical program을 physical execution으로 연결할 때 필요한 **오류 모델, logical instruction와 resource-estimation 계약**을 다룬다.

진입 전 요구 사항:

- Pauli operator, density matrix, quantum channel과 stabilizer 기초
- 확률, graph, maximum-likelihood 또는 matching 개념
- logical circuit의 gate count·depth·ancilla·measurement를 계산
- physical noise simulation과 logical FT estimate를 구분

### 1~2주차: Stabilizer와 오류정정 기초

**학습**

- repetition code, stabilizer, syndrome와 decoder
- bit/phase error, CSS construction와 code distance
- detectable, correctable error와 logical failure
- [IBM Foundations of Quantum Error Correction](https://quantum.cloud.ibm.com/learning/en/courses/foundations-of-quantum-error-correction/index)

**실습**

3·5-bit repetition code를 구현하고 physical error rate, rounds와 shots를 변화시킨다. syndrome 생성, decoder 결정과 logical outcome을 별도 데이터로 저장한다.

**통과 기준**

- detection event와 physical error를 같은 것으로 부르지 않는다.
- decoder가 관측하지 못한 실제 error를 사용하는 data leakage가 없다.
- uncertainty와 실패 수를 함께 보고한다.

### 3~4주차: Surface-code memory와 noise model

**학습**

- surface code의 data/measurement qubit, stabilizer cycle와 boundary
- phenomenological, circuit-level, correlated·leakage noise의 차이
- code capacity와 repeated syndrome measurement
- threshold를 보편 상수가 아닌 code·decoder·noise·operation 조합의 결과로 이해

**실습**

[Stim](https://github.com/quantumlib/Stim)으로 작은 repetition/surface-code memory experiment와 detector error model을 만든다. distance, rounds와 Pauli error를 sweep한다.

**통과 기준**

- Stim의 빠른 stabilizer simulation이 **Clifford operation과 Pauli noise 중심**이라는 범위를 명시한다.
- non-Clifford algorithm 전체를 Stim으로 정확히 simulation했다고 주장하지 않는다.
- noise model, decoder와 shot 수를 결과에 고정한다.

### 5~6주차: Decoder와 logical error 분석

**학습**

- lookup, matching, union-find 계열 decoder의 역할
- detector graph, observables와 boundary
- logical error rate, confidence interval와 rare-event 문제
- decoder latency와 streaming 요구

**실습**

적어도 두 decoder 또는 하나의 decoder와 trivial baseline을 비교한다. 동일 detector sample을 사용해 정확도와 decode latency를 함께 측정한다.

**통과 기준**

- decoder가 다른 noise prior를 썼다면 공정 비교로 표시하지 않는다.
- zero observed failure를 zero logical error probability라고 쓰지 않는다.
- real-time decoder 주장에는 latency distribution과 syndrome cycle budget이 있다.

### 7~8주차: Fault-tolerant logical operation

**학습**

- transversal gate, lattice surgery, code deformation의 개념
- error propagation, fault-tolerant gadget와 malignant fault
- Clifford+T, non-Clifford resource, magic-state distillation/factory
- logical ISA, scheduling과 space-time trade-off
- [IBM Fault-tolerant quantum computing introduction](https://quantum.cloud.ibm.com/learning/en/courses/foundations-of-quantum-error-correction/fault-tolerant-quantum-computing/introduction)

**실습**

작은 algorithm의 Clifford/T decomposition에서 logical qubit, T count, T depth, measurement와 feed-forward 의존성을 추출한다. factory 수를 늘릴 때 qubit와 runtime이 어떻게 바뀌는지 toy scheduler로 비교한다.

**통과 기준**

- T count와 물리 qubit 수를 직접 동일시하지 않는다.
- feed-forward latency와 factory throughput 가정을 공개한다.
- logical circuit, FT gadget와 physical schedule을 다른 artifact로 보존한다.

### 9주차: Logical resource counting

**학습**

- algorithm call graph와 bloq/component decomposition
- logical gate count, width, depth, ancilla와 uncomputation
- error budget을 subroutine에 배분하는 법
- [Qualtran](https://quantumai.google/qualtran)

**실습**

phase estimation, amplitude estimation 또는 chemistry subroutine 하나를 작은 parameter로 구성하고 hand count와 Qualtran 계열 count를 대조한다.

**통과 기준**

- asymptotic 식, symbolic count와 구체 parameter count를 구분한다.
- state preparation과 oracle 비용을 누락하지 않는다.
- uncompute, synthesis precision과 실패 확률 가정을 기록한다.

### 10~11주차: 물리 자원 추정과 민감도

**학습**

- application, hardware, QEC scheme, distillation factory와 error-budget model
- physical qubits, runtime, code distance/cycles, factory와 failure probability
- Pareto frontier와 가정 민감도
- [Microsoft Quantum Resource Estimator](https://learn.microsoft.com/en-us/azure/quantum/intro-to-resource-estimation)

**실습**

같은 logical workload에 대해 다음을 각각 바꾼 batch estimate를 실행한다.

- gate time·physical error rate를 포함한 hardware model
- QEC scheme 또는 code parameter
- total error budget와 synthesis error 배분
- factory 또는 runtime 최적화 목표

결과의 physical qubits, runtime, logical cycles, code distance, factory 수와 Pareto 점을 비교한다.

**통과 기준**

- 입력 logical resource와 estimator가 추가한 overhead를 분리한다.
- 숫자마다 hardware/QEC/error-budget 가정을 연결한다.
- estimator 결과를 실제 장비의 보장 성능·구매 견적·실측치로 표현하지 않는다.
- 단일 optimistic point 대신 민감도와 Pareto trade-off를 보고한다.

### 12주차: FTQC capstone

**실습**

`fault-tolerant-resource-study`를 완성한다. 하나의 공개 algorithm을 선택해 source → logical operations → FT decomposition → physical resource estimate로 이어지는 manifest를 만든다.

**최종 통과 기준**

- 모든 수치가 입력 가정과 tool version으로 역추적된다.
- 작은 instance는 직접 count 또는 독립 구현으로 교차 검증한다.
- physical noise simulation, logical error experiment와 analytical/resource estimate를 구분한다.
- Stim이 다루지 못하는 non-Clifford 범위를 별도 counting/modeling으로 처리한다.
- compilation choice가 T count/depth, factory와 space-time volume에 주는 영향을 설명한다.

### 포트폴리오: `fault-tolerant-resource-study`

필수 제출물:

- algorithm·oracle·state-preparation resource breakdown
- stabilizer memory experiment와 decoder 결과
- noise/QEC/hardware/error-budget assumption cards
- logical gate/T resource와 physical estimate 연결표
- 여러 scenario의 Pareto chart와 sensitivity analysis
- estimator·simulator·실제 hardware 결과의 경계 설명
- 실패한 scenario와 가장 민감한 가정 세 가지

## 트랙 F: Quantum-HPC·클라우드·API 통합

### 역할과 선수지식

이 트랙은 QPU를 CPU/GPU와 같은 로컬 accelerator로 단순 취급하지 않는다. queue와 provider scheduler가 있는 원격 자원, co-located runtime, simulator와 실제 QPU의 latency·failure model을 구분해 hybrid workflow를 설계한다.

진입 전 요구 사항:

- Linux shell, process/thread, network와 container 기초
- Python async·multiprocessing 또는 C++ concurrency
- MPI point-to-point·collective 기초와 batch scheduler 개념
- timeout, retry, idempotency, checkpoint와 provenance

### 먼저 구분할 세 실행 시간대

| 시간대 | 예 | 설계 원칙 |
| --- | --- | --- |
| 실시간 제어 | pulse/control electronics, QEC feedback | 일반 cloud REST 왕복으로 구현하지 않는다 |
| 근실시간·co-located | runtime 내부 iterative loop, decoder·classical coprocessor | provider가 보장한 execution model과 latency 범위 안에서 설계 |
| 비동기·batch | parameter sweep, VQE iteration batch, resource estimate | queue, checkpoint, retry, cost와 throughput을 최적화 |

### 1~2주차: 로컬 hybrid workflow와 DAG

**학습**

- preprocess → circuit generate → compile → submit → monitor → retrieve → postprocess
- DAG dependency, artifact boundary와 checkpoint
- embarrassingly parallel task와 tightly coupled task
- [IBM Quantum-HPC programming models](https://quantum.cloud.ibm.com/learning/en/courses/integrating-quantum-and-high-performance-computing/programming-models)

**실습**

local simulator로 workflow engine을 만든다. 각 stage가 immutable input/output manifest를 갖게 하고 stage 단위 재시작, cache와 실패 주입을 구현한다.

**통과 기준**

- process 재시작 후 완료 stage를 반복하지 않는다.
- source, artifact, result와 analysis output을 같은 파일로 덮어쓰지 않는다.
- workflow 전체 seed가 아니라 task별 deterministic seed derivation이 있다.

### 3주차: Slurm scheduler

**학습**

- job, step, partition, allocation, dependency와 array
- CPU/GPU/memory/time request와 over-allocation
- [Slurm job arrays](https://slurm.schedmd.com/job_array.html)
- scheduler log, exit code와 preemption handling

**실습**

parameter sweep를 Slurm array로 제출하고 aggregation job을 dependency로 연결한다. 실제 Slurm이 없으면 container 또는 generated script를 검증하고 실행은 local executor로 대체한다.

**통과 기준**

- array index가 input manifest와 안정적으로 매핑된다.
- failed index만 재실행할 수 있다.
- wall time, requested/used CPU·memory와 queue time을 분리한다.

### 4주차: MPI와 분산 메모리

**학습**

- rank, communicator, collective, nonblocking communication
- serialization, load balance와 straggler
- [MPI 표준 문서](https://www.mpi-forum.org/docs/)
- cluster 구현이 최신 표준 전체를 즉시 제공하지 않을 수 있다는 경계

**실습**

Hamiltonian term 또는 circuit batch를 rank에 분배하고 expectation partial sum을 reduction한다. 1·2·4 rank에서 compute, communication, serialization과 idle time을 나눈다.

**통과 기준**

- single-rank 결과와 tolerance 안에서 일치한다.
- rank 수가 늘어 느려지는 구간과 이유를 보고한다.
- MPI implementation/version과 실제 사용 subset을 기록한다.

### 5주차: CUDA-Q multi-QPU·multi-node

**학습**

- CUDA-Q C++·Python hybrid model
- [multi-QPU/MPI simulation](https://nvidia.github.io/cuda-quantum/latest/using/backends/sims/mqpusims.html)
- `mqpu`: 독립 QPU task나 expectation term의 병렬 분산
- `mgpu`: 하나의 큰 state simulation을 여러 GPU memory/compute로 분산
- thread 기반 단일 node와 MPI 기반 multi-node의 차이

**실습**

동일 workload를 single simulator, `mqpu`-style independent tasks, 가능하면 MPI simulator로 비교한다. GPU/MPI 환경이 없으면 공식 example의 control flow를 CPU mock으로 재현하고 성능 결과는 내지 않는다.

**통과 기준**

- `mqpu`와 `mgpu`를 같은 기능으로 설명하지 않는다.
- QPU 수 표기와 실제 physical hardware 사용 수를 구분한다.
- Windows는 [CUDA-Q 설치 문서](https://nvidia.github.io/cuda-quantum/latest/using/install/local_installation.html)에 따라 WSL2 등 공식 지원 경계를 확인한다.

### 6주차: Qiskit Runtime 실행 mode

**학습**

- [job, session, batch mode](https://quantum.cloud.ibm.com/docs/en/guides/execution-modes)
- 독립 workload와 iterative workload
- queue, fair-share, session inactivity와 maximum time
- first session job의 queue 특성

**실습**

독립 circuit batch와 iterative optimizer loop를 fake/runtime local testing으로 비교한다. 실제 계정이 있으면 작은 budget 안에서 job·batch·session 중 의미가 맞는 mode 하나만 사용한다.

**통과 기준**

- session이 첫 job의 queue를 제거한다고 주장하지 않는다.
- 독립 task를 불필요하게 session으로 직렬화하지 않는다.
- mode별 timeout·cost·queue 가정을 기록한다.

### 7주차: Cloud hybrid service 비교

**학습**

- [Amazon Braket Hybrid Jobs](https://docs.aws.amazon.com/braket/latest/developerguide/braket-jobs.html)의 managed container, classical instance, quantum task와 checkpoint
- [Azure Quantum job 제출](https://learn.microsoft.com/en-us/azure/quantum/how-to-submit-jobs)과 target profile
- [IBM Qiskit Serverless](https://quantum.cloud.ibm.com/docs/en/guides/serverless)의 확인 기준 experimental·plan 제한
- region, data, IAM, container registry, queue와 비용 경계

**실습**

세 provider를 직접 모두 실행하지 않는다. 공통 `HybridJobSpec`을 설계하고 한 provider는 실제 또는 공식 local mode, 나머지는 문서 기반 adapter fixture로 구현한다.

**통과 기준**

- provider별 container, artifact, credential와 cancellation 의미 차이를 표로 보존한다.
- experimental 기능을 production SLA가 있는 기능처럼 표현하지 않는다.
- Azure의 Adaptive RIF·Adaptive·Unrestricted local 실행을 hardware target 지원으로 기록하지 않는다. Adaptive RI도 문서에 열거된 지원 target에만 적용한다.
- cloud 계정이 없으면 실행하지 않았음을 명시한다.

### 8주차: REST·gRPC와 long-running operation

**학습**

- [gRPC core concepts](https://grpc.io/docs/what-is-grpc/core-concepts/)
- unary, server streaming, deadline와 cancellation
- REST resource와 long-running job
- schema/version compatibility, signed artifact URL와 pagination
- OpenAPI 3.2.1이 확인 기준 최신 사양이지만, generator·gateway가 늦을 수 있으므로 지원성을 확인해 3.1을 고정하는 실무 선택

**실습**

같은 job service를 REST schema와 protobuf service로 각각 표현한다. 클라이언트 retry, deadline propagation, idempotency와 result streaming을 시험한다.

**통과 기준**

- network timeout 뒤 서버 작업 존재 여부를 조회한 후 retry한다.
- client cancellation과 backend cancellation 가능 여부를 구분한다.
- schema breaking change를 compatibility test가 잡는다.

### 9주차: 관측 가능성·보안·비용

**학습**

- trace context를 scheduler·worker·provider 요청까지 전달
- queue·compile·transfer·QPU·postprocess latency와 비용 분해
- workload identity, secret rotation와 egress control
- quota, budget alert, runaway optimizer와 denial-of-wallet
- OpenTelemetry와 OWASP API Security

**실습**

각 task에 trace, cost tag와 provenance ID를 연결한다. credential redaction test와 per-user concurrency·shots·budget limit를 추가한다.

**통과 기준**

- 원격 provider 호출 수와 예상/실제 비용을 집계한다.
- trace에 circuit 원문이나 token이 없다.
- queue time을 quantum compute speed로 잘못 해석하지 않는다.

### 10주차: 복구·재시도·정확히 한 번의 환상

**학습**

- at-least-once queue, idempotent consumer와 transactional outbox
- checkpoint, partial result와 eventual consistency
- retry classification, exponential backoff와 circuit breaker
- preemption, provider outage와 poison task

**실습**

worker kill, scheduler preemption, lost response, duplicate event, provider 429/500을 순차적으로 주입한다. 각 장애 뒤 추가 QPU 비용과 artifact 일관성을 검사한다.

**통과 기준**

- end-to-end exactly-once를 근거 없이 주장하지 않는다.
- 재시도 가능한 stage와 금지된 stage를 명시한다.
- 동일 idempotency key의 비용 중복이 없다.

### 11주차: 성능·확장성 평가

**학습**

- strong/weak scaling, throughput, utilization과 efficiency
- queueing, batching, granularity와 Amdahl의 법칙
- cost per valid result와 실패 비용
- simulator scaling과 QPU workflow scaling의 차이

**실습**

worker/rank 1·2·4, batch 크기와 circuit 크기를 바꾼다. 다음을 별도로 기록한다.

- queue wait
- source validation과 compile
- upload/download와 serialization
- simulator/QPU execution
- post-processing
- retry·failed work와 비용

**통과 기준**

- speedup에 setup, communication과 failed work가 포함된다.
- simulator multi-node 결과를 여러 실제 QPU의 성능으로 표현하지 않는다.
- raw event log에서 표와 그래프를 재생성할 수 있다.

### 12주차: Quantum-HPC capstone

**실습**

`quantum-hpc-workflow`를 완성한다.

```text
manifest
  → Slurm/MPI local-classical preprocessing
    → target-aware compilation
      → async provider submission
        → checkpoint/poll/event normalization
          → result reduction and provenance report
```

**최종 통과 기준**

- local simulator만으로 전체 workflow를 재현할 수 있다.
- 실제 cloud 실행은 별도 credential·budget gate 뒤에 있다.
- worker 수와 provider failure를 바꿔도 결과 일관성을 유지한다.
- latency, throughput, utilization, 비용과 정확도를 함께 보고한다.
- runbook에 queue 지연, provider outage, credential expiry와 partial failure 대응이 있다.

### 포트폴리오: `quantum-hpc-workflow`

필수 제출물:

- DAG와 artifact/provenance schema
- Slurm array·dependency와 MPI reduction 예제
- CUDA-Q `mqpu`/`mgpu` 경계 설명 및 가능한 환경의 실행 기록
- cloud adapter 하나와 두 개의 contract fixture
- retry·checkpoint·idempotency failure-injection report
- OpenTelemetry trace와 stage별 latency/cost dashboard
- 1·2·4 worker/rank scaling report
- real-time, near-time와 asynchronous boundary 결정 기록

## 언어별 역할과 인터페이스 전략

### 권장 역할 분담

| 언어 | 우선 사용 영역 | 학습 목표 | 주의점 |
| --- | --- | --- | --- |
| Python | SDK 통합, orchestration, benchmark, notebook | 빠른 adapter·실험·test 작성 | GIL, packaging, native ABI와 대형 object serialization |
| C++17/20 | MLIR/LLVM pass, 고성능 runtime, CUDA-Q | ownership, build/link, pass plugin, low-level profiling | LLVM major·C++ ABI·compiler toolchain을 함께 고정 |
| Rust | parser, 안전한 job/runtime service, QIR tooling | enum 기반 상태·오류, async, FFI 경계 | LLVM binding과 native library version 결합 확인 |

### 인터페이스 선택 순서

1. 먼저 **versioned file artifact**를 고려한다. OpenQASM, MLIR bytecode/text, QIR bitcode와 JSON manifest는 재현·디버깅에 유리하다.
2. 프로세스 경계가 필요하면 stable CLI와 exit/error schema를 만든다.
3. 원격 서비스는 OpenAPI/gRPC로 deadline, idempotency와 compatibility를 명시한다.
4. 성능이 입증된 병목에만 Python binding 또는 C ABI를 추가한다.
5. C++ 객체 ABI를 Python·Rust에 직접 노출하지 않는다. C ABI, opaque handle 또는 serialization boundary를 선호한다.

### 필수 상호운용 시험

- OpenQASM `parse → print → parse` 구조 보존
- MLIR `parse → verify → bytecode/text → parse` 보존
- QIR producer output을 독립 LLVM tool과 runner로 확인
- Python client와 Rust/C++ service 사이 schema golden test
- old/new client-server pair의 backward compatibility matrix
- artifact hash, compiler revision과 target snapshot의 end-to-end provenance

## 통합 포트폴리오와 평가 기준

### 권장 저장소 구조

```text
quantum-platform-capstone/
  README.md
  docs/
    architecture.md
    threat-model.md
    decisions/
    support-matrix.md
  schemas/
  compiler/
  gateway/
  runtime/
  workflows/
  qec-resource-study/
  tests/
    conformance/
    equivalence/
    integration/
    failure-injection/
  benchmarks/
    manifest/
    raw/
    reports/
  env/
  Makefile
```

### 12주 통합 capstone 순서

| 주차 | 산출물 | 통과 기준 |
| ---: | --- | --- |
| 1 | problem statement, 지원·비지원 범위 | 사용 scenario와 non-goal이 분명하다 |
| 2 | domain model, architecture와 trust boundary | program/artifact/job/result가 분리된다 |
| 3 | OpenQASM subset·AST·diagnostic | parse와 semantic error가 구분된다 |
| 4 | MLIR dialect·verifier | malformed IR이 모두 거부된다 |
| 5 | rewrite·lowering pipeline | pass별 의미 보존 test가 있다 |
| 6 | QIR 2.0 또는 target artifact | LLVM 16+, profile+QIS가 기록된다 |
| 7 | target routing·scheduling | legality 위반 0건이다 |
| 8 | async execution adapter | idempotency·timeout·cancel test를 통과한다 |
| 9 | Slurm/MPI 또는 cloud workflow | checkpoint에서 재시작 가능하다 |
| 10 | QEC/resource-estimation study | 가정·민감도·Pareto를 공개한다 |
| 11 | benchmark·failure injection·security | raw data, secret scan, tail regression이 있다 |
| 12 | clean-room reproduction와 보고서 | 제3자가 one-command local demo를 재현한다 |

### 100점 평가표

| 영역 | 점수 | 증거 |
| --- | ---: | --- |
| 의미·정확성 | 25 | oracle, equivalence, verifier, semantic test |
| target 적법성·표준 경계 | 15 | OpenQASM/QIR/LLVM/profile/QIS/Target manifest |
| architecture·API | 15 | 명시적 계약, capability negotiation, ADR |
| 신뢰성·운영 | 15 | 상태기계, retry, idempotency, recovery, trace |
| benchmark·재현성 | 15 | lock, seed, raw data, 여러 workload와 CI |
| hardware·FTQC 해석 | 10 | QEC/physical assumptions와 sensitivity |
| 문서·보안 | 5 | runbook, threat model, secret·license 검사 |

80점 이상을 권장 합격선으로 삼되, 다음 critical gate는 총점과 무관하게 모두 통과해야 한다.

- 지원 범위 안 semantic mismatch **0건**
- target legality 또는 QIR profile 위반 **0건**
- credential·개인정보·비공개 circuit의 log/artifact 유출 **0건**
- duplicate submit으로 인한 확인된 중복 비용 **0건**
- environment lock, seed, compiler/backend revision와 raw result 보존
- unsupported, timeout, inconclusive을 성공으로 계산하지 않음

### 면접에서 설명할 수 있어야 하는 질문

1. OpenQASM, MLIR과 QIR은 왜 서로 대체재가 아닌가?
2. QIR backend 호환성을 profile과 QIS 조합으로 써야 하는 이유는 무엇인가?
3. parse success, IR verification, target legality와 semantic equivalence는 어떻게 다른가?
4. layout/routing/scheduling 중 어느 단계가 final measurement mapping을 바꾸는가?
5. cloud QPU를 Slurm이 직접 제어하는 로컬 accelerator처럼 모델링하면 어디서 깨지는가?
6. `mqpu`와 `mgpu`는 어떤 병렬성을 각각 표현하는가?
7. physical error simulation과 FT resource estimation은 왜 같은 검증이 아닌가?
8. QAT의 문서화된 목표와 현재 구현 상태가 다를 때 CI gate를 어떻게 설계하는가?
9. Azure의 Adaptive RI, Adaptive RIF, Adaptive와 Unrestricted profile은 hardware 지원 범위가 어떻게 다른가?
10. ML optimizer가 compiler correctness를 결정하지 못하게 어떤 안전 경계를 두었는가?

## 공식 학습 자료

### Compiler·표준

- [LLVM Kaleidoscope tutorial](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/)
- [MLIR documentation](https://mlir.llvm.org/docs/)
- [MLIR Language Reference](https://mlir.llvm.org/docs/LangRef/)
- [MLIR Toy tutorial](https://mlir.llvm.org/docs/Tutorials/Toy/)
- [MLIR Dialect Conversion](https://mlir.llvm.org/docs/DialectConversion/)
- [MLIR Pass Management](https://mlir.llvm.org/docs/PassManagement/)
- [Lowering to LLVM IR](https://mlir.llvm.org/docs/TargetLLVMIR/)
- [LLVM MLGO](https://llvm.org/docs/MLGO.html)
- [OpenQASM 3.1 specification](https://openqasm.com/versions/3.1/index.html)
- [OpenQASM reference grammar](https://openqasm.com/versions/3.1/grammar/index.html)
- [OpenQASM specification repository](https://github.com/openqasm/openqasm)
- [QIR specification](https://github.com/qir-alliance/qir-spec/blob/main/specification/README.md)
- [QIR Base Profile](https://github.com/qir-alliance/qir-spec/blob/main/specification/profiles/Base_Profile.md)
- [QIR instruction set](https://github.com/qir-alliance/qir-spec/blob/main/specification/Instruction_Set.md)
- [PyQIR](https://github.com/qir-alliance/pyqir)
- [QIR Runner](https://github.com/qir-alliance/qir-runner)
- [QAT](https://github.com/qir-alliance/qat)
- [QAT goals and assumptions](https://www.qir-alliance.org/qat/UsingQAT/GoalsAndAssumptions/)
- [Qiskit transpiler stages](https://quantum.cloud.ibm.com/docs/en/guides/transpiler-stages)
- [Qiskit custom backend](https://quantum.cloud.ibm.com/docs/guides/custom-backend)
- [MQT Bench](https://github.com/munich-quantum-toolkit/bench)
- [MQT QCEC](https://github.com/munich-quantum-toolkit/qcec)
- [CUDA-Q compiler development](https://nvidia.github.io/cuda-quantum/latest/using/extending/compiler/index.html)
- [CUDA-Q IR dialects](https://nvidia.github.io/cuda-quantum/latest/using/extending/compiler/cudaq_ir.html)
- [CUDA-Q backend plugin](https://nvidia.github.io/cuda-quantum/latest/using/extending/backend.html)
- [Catalyst architecture](https://docs.pennylane.ai/projects/catalyst/en/latest/dev/architecture.html)

### 오류정정·FTQC·자원 추정

- [IBM Foundations of Quantum Error Correction](https://quantum.cloud.ibm.com/learning/en/courses/foundations-of-quantum-error-correction/index)
- [IBM Fault-tolerant quantum computing introduction](https://quantum.cloud.ibm.com/learning/en/courses/foundations-of-quantum-error-correction/fault-tolerant-quantum-computing/introduction)
- [Stim](https://github.com/quantumlib/Stim)
- [Qualtran](https://quantumai.google/qualtran)
- [Microsoft Quantum Resource Estimator](https://learn.microsoft.com/en-us/azure/quantum/intro-to-resource-estimation)
- [Azure Quantum target profiles](https://learn.microsoft.com/en-us/azure/quantum/quantum-computing-target-profiles)

### Quantum-HPC·cloud·API

- [IBM Integrating Quantum and High-Performance Computing](https://quantum.cloud.ibm.com/learning/en/courses/integrating-quantum-and-high-performance-computing)
- [IBM Quantum-HPC compute resources](https://quantum.cloud.ibm.com/learning/en/courses/integrating-quantum-and-high-performance-computing/compute-resources)
- [IBM Quantum-HPC programming models](https://quantum.cloud.ibm.com/learning/en/courses/integrating-quantum-and-high-performance-computing/programming-models)
- [IBM Qiskit execution modes](https://quantum.cloud.ibm.com/docs/en/guides/execution-modes)
- [IBM Qiskit Serverless](https://quantum.cloud.ibm.com/docs/en/guides/serverless)
- [Amazon Braket Hybrid Jobs](https://docs.aws.amazon.com/braket/latest/developerguide/braket-jobs.html)
- [Azure Quantum job submission](https://learn.microsoft.com/en-us/azure/quantum/how-to-submit-jobs)
- [CUDA-Q multi-QPU and multi-node simulation](https://nvidia.github.io/cuda-quantum/latest/using/backends/sims/mqpusims.html)
- [CUDA-Q local installation](https://nvidia.github.io/cuda-quantum/latest/using/install/local_installation.html)
- [MPI standards](https://www.mpi-forum.org/docs/)
- [Slurm job arrays](https://slurm.schedmd.com/job_array.html)
- [OpenAPI Specification 3.2.1](https://spec.openapis.org/oas/v3.2.1.html)
- [gRPC core concepts](https://grpc.io/docs/what-is-grpc/core-concepts/)
- [OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/)
- [OWASP API Security Top 10 2023](https://api-security.owasp.org/editions/2023/en/0x03-introduction/)
- [Open Container Initiative](https://opencontainers.org/)

이 과정의 핵심은 많은 framework 이름을 나열하는 것이 아니다. source 의미, IR invariant, target capability, runtime failure와 물리 자원 가정을 서로 다른 계약으로 보존하고, 각 경계를 자동 검사와 재현 가능한 증거로 연결하는 것이다.
