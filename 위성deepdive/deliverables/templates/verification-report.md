# 위성 통신 시스템 검증 보고서 양식

문서 ID: `VR-SATNET-001`  
Revision: `0.1 Template`  
작성일: 2026-09-10  
현재 판정: **미실행 — 검증 완료를 주장하지 않음**

## 1. Executive summary(경영진 요약)

| 항목 | 계획 기준 | 측정 결과 | 판정 | 증거 ID |
|---|---:|---:|---|---|
| Critical telemetry p99 latency | ≤ 60 s | 미측정 | NOT RUN | VR-PERF-001 |
| ISL failover time | ≤ 10 s | 미측정 | NOT RUN | VR-FO-001 |
| Worst-case link margin | ≥ 3.0 dB | 예시 시트 10.35 dB | NOT VERIFIED | VR-RF-001 |
| Packet loss ratio | 요구사항 TBD | 미측정 | BLOCKED | VR-PERF-001 |
| Service availability | 요구사항 TBD | 미측정 | BLOCKED | VR-OPS-001 |

예시 링크 마진은 교육용 입력의 계산 결과일 뿐 실제 임무의 검증 결과가 아니다.

## 2. 기준선과 범위

- 요구사항 revision:
- ICD revision:
- architecture revision:
- hardware serial/revision:
- software 40자리 commit SHA와 reproducible build ID:
- 제외 범위와 이유:
- 시험 기간, 장소, 관측 contact:

## 3. 방법과 데이터 무결성

시험 절차 ID, 장비 모델·serial·calibration 만료일, channel/contact profile, traffic generator 설정, random seed를 기록한다. 원시 파일은 변경 불가능한 저장소에 두고 경로·크기·SHA-256 digest를 표에 남긴다. 시간 동기 오차가 latency 정확도보다 충분히 작은지 증명한다.

## 4. 결과

### 4.1 Throughput와 goodput

offered load, PHY throughput, protocol goodput, overhead, retransmission을 분리한다. 평균·peak와 contact별 분포를 함께 보고한다.

### 4.2 Latency

p50/p95/p99/maximum, sample count, dropped sample 처리 방식을 기록한다. propagation, serialization, processing, queue, contact wait로 분해한다.

### 4.3 Packet loss와 duplicate

고유 packet ID 기준으로 생성·전달·만료·buffer drop·retry-limit drop·duplicate를 합계한다. 분모와 측정 구간을 명시한다.

### 4.4 Availability

서비스 조건을 먼저 정의한 뒤 충족 시간/관측 시간을 계산한다. 계획된 maintenance, 지상 날씨, 위성 장애를 임의로 분모에서 제거하지 않고 계약 정의대로 분류한다.

### 4.5 Failover와 recovery

fault injection, detection, isolation, reroute, first successful delivery, stable failback timestamp를 한 timeline으로 정리한다.

## 5. 요구사항별 판정

| 요구사항 | 시험 | 결과 요약 | 증거 | 판정 | 승인자/일자 |
|---|---|---|---|---|---|
| COM-001 | TP-PERF-001 | TBD | VR-PERF-001 | NOT RUN | TBD |
| COM-002 | TP-FO-001 | TBD | VR-FO-001 | NOT RUN | TBD |
| COM-003 | TP-RF-001 | TBD | VR-RF-001 | NOT RUN | TBD |

전체 행은 [요구사항 추적 매트릭스](../results/requirements-traceability.xlsx)와 일치시킨다.

## 6. 부적합·편차·잔여 위험

각 항목에 `NCR ID, severity, 재현 조건, 영향 요구사항, root cause, correction, 재시험, residual risk, 승인자`를 기록한다. 시험 환경 제한으로 관측하지 못한 위험은 PASS가 아니라 잔여 위험이다.

## 7. 결론

`PASS / CONDITIONAL PASS / FAIL / NOT RUN` 중 하나를 명시하고 승인 범위를 정확히 제한한다. 조건부 승인은 만료일과 후속 시험을 포함한다.

[← 실무 산출물](../README.md)
