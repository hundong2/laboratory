# 위성 통신 시스템 시험 절차

문서 ID: `TP-SATNET-001`  
Revision: `0.1 Draft`  
작성일: 2026-09-10

## 1. 시험 통제

시험 전에 요구사항·ICD·software/firmware·FPGA(Field-Programmable Gate Array, 현장 프로그래밍 가능 게이트 배열)·시험 장비 calibration revision을 기록한다. 각 시험은 원시 packet capture, console log, 측정 파일, 환경 조건과 UTC timestamp를 보존한다. 재시험은 실패 기록을 삭제하지 않고 새 run ID를 부여한다.

공통 판정:

- `PASS`: 모든 정량 기준 충족, 미해결 severity 1/2 부적합 없음, 증거 checksum 기록.
- `FAIL`: 한 개 이상의 필수 기준 위반 또는 증거 불충분.
- `BLOCKED`: 사전조건·장비·외부 서비스 문제로 실행 불가. PASS로 계산하지 않는다.

## 2. 시험 환경 기록표

| 항목 | 기록 |
|---|---|
| Test run ID / 일시 / 시험자 | TBD |
| 요구사항·ICD revision | TBD |
| HW serial / board revision | TBD |
| SW commit SHA / build flags | TBD |
| RF/optical emulator profile | TBD |
| clock source와 synchronization 오차 | TBD |
| 온도·전압·방사선/진동 조건 | TBD |
| packet capture·log·결과 경로와 SHA-256 | TBD |

## 3. 시험 항목

### TP-RF-001 — Worst-case RF 링크

관련 요구사항: `COM-003`

1. 승인된 링크 버짓의 거리, Doppler, antenna pointing, polarization, noise temperature, implementation loss를 emulator에 설정한다.
2. acquisition 후 최소 30분 또는 통계적으로 충분한 bit 수를 송수신한다.
3. pre-FEC/post-FEC BER(Bit Error Rate, 비트 오류율), PER(Packet Error Rate, 패킷 오류율), RSSI, SNR, Eb/N0를 기록한다.

판정: worst-case link margin `≥ 3.0 dB`, 목표 BER/PER 충족, 허위 lock과 비정상 reset 없음. 정확한 BER/PER 목표는 승인 요구사항으로 `TBD`를 닫는다.

### TP-PERF-001 — 처리율·지연·손실

관련 요구사항: `COM-001`

1. nominal/peak/burst traffic을 각각 30분 이상 주입한다.
2. application payload의 고유 ID와 송수신 timestamp를 비교한다.
3. duplicate를 goodput에서 제거하고 queue·contact wait를 분리한다.

판정: critical telemetry 생성-전달 p99 `≤ 60 s`, 데이터 손실은 승인 목표 이하, buffer overflow 없음. 평균값만으로 판정하지 않는다.

### TP-FO-001 — ISL failover/failback

관련 요구사항: `COM-002`, `COM-012`

1. 정상 primary 경로에서 sequence traffic을 전송한다.
2. RF attenuation 또는 optical loss-of-track를 주입한다.
3. 탐지, 격리, 경로 계산, 첫 성공 packet timestamp를 기록한다.
4. primary 복구 후 hysteresis와 hold-down을 지나 failback한다.

판정: 장애 주입 후 `≤ 10 s` 내 대체 경로 전달, routing loop 없음, command 중복 실행 0회, oscillation 없음. failback이 설정된 안정 시간 전에 발생하면 FAIL.

### TP-BUF-001 — Contact miss와 저장 후 전달

관련 요구사항: `COM-004`

세 개 연속 예정 contact를 차단하고 critical/normal/bulk traffic을 발생시킨 뒤 네 번째 contact를 복구한다. 판정: critical data 영구 손실 0, 보존된 CRC와 길이 일치, priority 순서가 정책과 일치, overflow drop은 사전에 정의된 낮은 class에서만 발생.

### TP-DUP-001 — 분할·중복·순서 wrap

관련 요구사항: `COM-007`

first/continuation/last segment 누락·중복·순서 변경, CCSDS 14-bit sequence count wrap, 같은 command ID 재전송을 주입한다. 판정: 불완전 packet 실행 0회, 중복 command side effect 0회, 기존 결과 반환 또는 명시적 duplicate 응답, bounded reassembly memory.

### TP-SEC-001 — Command 인증과 anti-replay

관련 요구사항: `COM-005`, `COM-011`

정상, 변조, 잘못된 키, 만료, replay, future counter, reset 전 counter 재사용을 시험한다. 판정: 정상 command만 정확히 1회 실행; 나머지는 실행 전 차단; audit event 생성; reset 후 counter rollback 없음. 키 원문은 log에 남기지 않는다.

### TP-SLE-001 — 지상국 상호운용

관련 요구사항: `COM-006`

합의된 SLE RAF(Return All Frames, 모든 반환 프레임), RCF(Return Channel Frames, 반환 채널 프레임), FCLTU(Forward CLTU) service를 bind/start/stop/unbind하고 frame gap, disconnect, reconnect를 시험한다. 판정: version·service instance·credentials 일치, gap indication 보존, 중복 전달 정책 일치.

### TP-RT-001 — HAL/IRQ 실시간성

관련 요구사항: `COM-008`

최대 IRQ rate, 동시 SPI bus 부하, RTOS 최고 우선순위 간섭을 주입한다. logic analyzer와 trace로 ISR entry/exit를 측정한다. 판정: ISR worst-case execution `≤ 50 μs`, ISR 내부 blocking SPI 0회, event queue overflow 0회, timeout 후 radio state가 정의된 상태로 복귀.

### TP-SA-001 / TP-SCA-001 — 정적 분석과 OSS 공급망

관련 요구사항: `COM-009`, `COM-010`

compiler warnings-as-errors, MISRA profile, CWE query, dependency/SBOM scan을 clean build에서 실행한다. 판정: 미승인 required-rule violation 0, severity threshold 이상 CWE finding 0, 알려진 exploitable critical vulnerability 0, 모든 dependency에 version·license·source·digest 기록. suppression에는 owner·근거·만료일이 필요하다.

## 4. 종료 조건

모든 필수 시험이 PASS이고, 실패/편차가 부적합 보고서와 승인된 waiver에 연결되며, [검증 보고서](verification-report.md)와 [추적 매트릭스](../results/requirements-traceability.xlsx)가 동기화되어야 시험 캠페인을 종료한다.

[← 실무 산출물](../README.md)
