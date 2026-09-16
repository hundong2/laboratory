# 포트폴리오와 역량 평가

포트폴리오의 목적은 튜토리얼을 실행했다는 사실이 아니라, 문제를 정의하고 구현·검증하며 결과의 한계를 방어할 수 있음을 보여 주는 것이다.

## 1. 모든 프로젝트의 필수 구조

```text
project/
  README.md                 # 문제, 범위, 실행법, 결과와 한계
  pyproject.toml 또는 lock  # 재현 환경
  src/                      # 구현
  tests/                    # unit, property, integration test
  configs/                  # backend, seed, shots, tolerance
  experiments/              # 실행 entrypoint
  results/raw/              # 변경하지 않은 원시 결과
  results/processed/        # 표와 그림을 만드는 파생 결과
  docs/decisions/           # 중요한 설계 결정
  report.md                 # 주장·근거·반례·자원 분석
```

README에는 최소한 다음 질문에 답한다.

- 문제의 입력, 출력, 정확도와 실패 조건은 무엇인가?
- 어떤 고전 baseline과 exact oracle을 사용했는가?
- 어떤 가정에서 양자 표현이 가능한가?
- data/state preparation과 readout 비용은 무엇인가?
- simulator, noise model, QPU 또는 FT estimate 중 어느 단계인가?
- 결과를 재현하는 한 명령과 환경 정보는 무엇인가?

## 2. 트랙별 대표 capstone

### A. 양자 알고리즘 설계자

`pde-or-materials-quantum-feasibility-study`

- PDE 경로: Poisson/heat 문제의 FDM·spectral·iterative baseline과 QLSA/QPINN 후보 비교
- 물성 경로: PySCF HF/DFT → active space → qubit Hamiltonian → exact/VQE/SQD 비교
- 최적화 경로: exact·강한 heuristic → QUBO/Ising → QAOA의 품질·시간·shot 비교
- 필수 증거: condition number, precision, state preparation, output extraction, scaling과 FT resource sensitivity

### B. 양자 회로 검증·개발자

`cross-sdk-circuit-conformance`

- 같은 Bell/GHZ/QFT/parameterized circuit를 두 SDK로 구현
- bit order와 measurement mapping을 하나의 canonical form으로 변환
- unitary, state, distribution, noisy 결과의 검증 사다리 작성
- transpiler seed·target별 depth, SWAP, 2-qubit gate regression

### C. 양자 기계학습 전문가

`fair-qml-benchmark-card`

- 고정된 data split과 preprocessing
- logistic/RBF-SVM/작은 MLP와 quantum kernel/QNN 비교
- 동일한 tuning budget, 여러 seed와 신뢰구간
- PSR gradient audit, no-entanglement·fixed-layer·shot/noise ablation
- accuracy뿐 아니라 AUROC/AUPRC 또는 적절한 regression metric, calibration, 회로 실행 횟수와 총 wall time 보고

### D. 양자 소프트웨어 architecture 설계자

`provider-neutral-quantum-control-plane`

- backend capability, compile request, job, result, artifact와 credential의 contract
- simulator와 두 mock provider adapter
- async queue, cancel, timeout, retry, idempotency와 cost quota
- provenance/telemetry와 tenant 신뢰 경계
- provider 변경 시 domain logic가 변하지 않는 contract test

### E. 양자 회로 compiler 개발자

`verified-multi-level-quantum-compiler`

- 작은 source language parser와 typed AST
- high-level circuit IR → canonical IR → target gate set lowering
- cancellation, rotation folding, decomposition, placement/routing pass
- pass별 legality, equivalence와 resource regression test
- OpenQASM export 또는 QIR profile/QIS를 명시한 제한적 lowering

### F. Quantum-HPC 통합 개발자

`resilient-hybrid-workflow`

- parameter sweep·Hamiltonian group을 classical worker와 mock QPU에 배치
- queue, checkpoint, retry budget, cancellation, partial result
- local/MPI 또는 containerized 실행과 artifact store
- end-to-end trace, utilization, queue·compute 분해와 비용 한도
- 실패 주입과 재개 시 중복 실행 방지 테스트

## 3. 12주 capstone 일정

| 주차 | 활동 | review gate |
| --- | --- | --- |
| 1 | 연구 질문, 사용자와 output contract 정의 | 성공·실패 기준이 수치화됨 |
| 2 | 관련 연구·공식 API 확인, 위험 목록 | 출처와 현재 버전 기록 |
| 3 | exact 또는 강한 고전 baseline | 작은 instance에서 검증 통과 |
| 4 | architecture와 실험 계획 | 비용·신뢰 경계·data flow 명시 |
| 5~6 | 최소 quantum/hybrid 구현 | deterministic ideal test 통과 |
| 7 | noise·compiler·distributed 조건 추가 | 한 요인씩 분리된 실험 |
| 8 | 통계·자원 instrumentation | seed·shots·depth·시간 자동 기록 |
| 9 | scaling과 failure injection | 최소 3개 크기와 실패 복구 |
| 10 | ablation과 반례 | 유리한 설정만 고르지 않음 |
| 11 | 독립 재현·코드 review | 새 환경에서 실행 가능 |
| 12 | 최종 보고·구두 방어 | 주장마다 근거와 제한 연결 |

## 4. 공통 평가표

| 항목 | 배점 | 우수 기준 |
| --- | ---: | --- |
| 문제·수학·도메인 정확성 | 15 | 가정, 단위, boundary와 output이 명확 |
| 고전 baseline과 비교 공정성 | 15 | 같은 입력·출력·오차·예산에서 비교 |
| 양자/시스템 구현 정확성 | 15 | 작은 exact case와 자동 테스트 통과 |
| 검증·통계 | 15 | 여러 seed, 신뢰구간, error decomposition |
| 자원·성능 분석 | 15 | 준비·compile·shot·queue·후처리를 포함 |
| architecture·운영 품질 | 10 | failure, security, provenance가 설계됨 |
| 재현성 | 10 | lock, config, one-command run과 raw result |
| 설명과 한계 | 5 | 성공·실패·적용 범위를 정직하게 구분 |

- 80점 이상: 해당 트랙의 실무형 입문 프로젝트로 인정
- 90점 이상: 독립 설계와 기술 면접·코드 방어가 가능한 전문가 준비 수준
- 점수와 무관한 재작업: data leakage, exact baseline 누락, 허위 quantum advantage, version/seed/shots 미기록, simulator를 QPU로 표현, secret 노출

## 5. 트랙별 추가 배점 질문

### 알고리즘

- `N`, sparsity, rank, condition number `κ`, precision `ε`를 보고했는가?
- 전체 vector와 단일 observable 중 무엇을 출력하는가?
- 최신 sparse/Krylov/tensor-network/optimization solver와 비교했는가?

### 회로·QML

- logical circuit와 transpiled ISA circuit를 모두 검증했는가?
- bit order, layout-mapped observable과 finite-shot 불확실성을 처리했는가?
- QML에 classical surrogate와 동일 tuning budget이 있는가?

### architecture·compiler·hybrid

- backend capability/version negotiation이 있는가?
- rewrite legality와 equivalence가 별개로 검증되는가?
- timeout, duplicate submit, worker crash, partial result와 cancellation을 시험했는가?

## 6. 연구 주장 감사표

최종 보고서에 아래 표를 복사해 채운다.

| 질문 | 답 | 증거 |
| --- | --- | --- |
| 고전 baseline과 입력이 같은가? |  |  |
| 출력 계약이 같은가? |  |  |
| state preparation 비용을 포함했는가? |  |  |
| shots·tomography·postselection을 포함했는가? |  |  |
| classical optimization·후처리를 포함했는가? |  |  |
| compiler·routing overhead를 포함했는가? |  |  |
| NISQ와 fault-tolerant 수치를 분리했는가? |  |  |
| 여러 seed와 instance family에서 유지되는가? |  |  |
| 최소 3개 문제 크기의 scaling evidence가 있는가? |  |  |
| 반례·실패 조건을 공개했는가? |  |  |

## 7. 제출 전 최종 점검

- 새 가상환경에서 README의 명령만으로 실행했다.
- 모든 자동 테스트와 notebook cell이 순서대로 통과한다.
- raw result를 손으로 편집하지 않았고 파생 과정이 코드에 있다.
- 표와 그림의 단위, sample 수와 error bar가 표시된다.
- 외부 API·SDK는 확인 날짜와 버전을 기록한다.
- 논문 주장을 자신의 실험 결과처럼 쓰지 않는다.
- 가장 중요한 실패 한 가지와 다음 실험을 결론에 포함한다.
