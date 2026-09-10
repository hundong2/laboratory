# 위성 네트워크 실무 산출물 패키지

작성일: 2026-09-10  
상태: 교육용 기준선(Baseline) — 임무 요구사항·궤도·부품 데이터로 조정 필요

## 사용 순서

1. 요구사항 추적 매트릭스에서 요구사항을 승인한다.
2. 아키텍처와 인터페이스 제어 문서(ICD)를 기준선으로 동결한다.
3. 링크 버짓과 성능 모델의 입력을 실제 값으로 교체한다.
4. 시뮬레이션과 패킷 분석기로 사전 검증한다.
5. 시험 절차를 실행하고 검증 보고서에 원시 증거를 연결한다.
6. 요구사항 상태를 `Verified`로 바꾼다.

## 산출물 인덱스

| 실무 산출물 | 파일 | 현재 포함 내용 |
|---|---|---|
| Network Architecture Document(네트워크 아키텍처 문서) | [대화형 HTML](architecture/network-architecture.html), [원본 JSON](architecture/network-architecture.json), [검증 기록](architecture/README.md) | 위성, RF/광 ISL, 사용자 단말, 지상국, 임무 데이터센터, 제어·데이터·보안 흐름 |
| ICD(Interface Control Document, 인터페이스 제어 문서) | [ICD.md](templates/ICD.md) | RF/HW/SW/지상국/단말 인터페이스, 단위·타이밍·오류·버전 규칙 |
| Link Budget Sheet(링크 버짓 시트) | [link-budget.xlsx](results/link-budget.xlsx) | EIRP, FSPL, G/T, C/N0, Eb/N0, margin 수식과 독립 sanity check |
| Performance Model(성능 모델) | [performance-model.md](templates/performance-model.md) | throughput, latency, hop, queue, contact capacity, buffer 모델 |
| Simulation Script(시뮬레이션 스크립트) | [satellite_network_sim.py](tools/satellite_network_sim.py) | contact-aware 전달, 우선순위 queue, loss, buffer, 지연 통계 |
| Protocol Analysis Tool(프로토콜 분석 도구) | [ccsds_packet_analyzer.py](tools/ccsds_packet_analyzer.py) | CCSDS Space Packet primary header 생성·파싱·길이·CRC 검사 |
| Test Procedure(시험 절차) | [test-procedure.md](templates/test-procedure.md) | 기능·성능·failover·보안·HAL 검증과 pass/fail 기준 |
| Verification Report(검증 보고서) | [verification-report.md](templates/verification-report.md) | throughput, latency, loss, availability 결과·증거·편차 보고 양식 |
| Trade-off Report(절충 분석 보고서) | [trade-off-report.md](templates/trade-off-report.md) | RF 대 Optical, routing, rate, buffer, redundancy 비교 |
| Requirement Traceability(요구사항 추적성) | [requirements-traceability.xlsx](results/requirements-traceability.xlsx) | 요구사항-설계-ICD-시험-결과-상태 연결 |

## 식별자 규칙

- 요구사항: `COM-NNN`
- 인터페이스: `IF-도메인-NN`, 예: `IF-RF-01`
- 시험: `TP-영역-NNN`
- 검증 증거: `VR-영역-NNN`
- 결함·편차: `NCR-NNN`(Non-Conformance Report, 부적합 보고서)

같은 ID를 모든 파일에서 그대로 사용한다. `Verified`는 시험 로그·설정·소프트웨어 revision·결과 파일·승인자가 모두 기록된 경우에만 허용한다.

## 생성·검증 메모

- Excel 워크북은 [build_workbooks.mjs](tools/build_workbooks.mjs)로 다시 생성할 수 있다.
- 미리보기 PNG와 수식 검사 로그는 `results/`에 있다.
- Python 도구는 외부 패키지 없이 실행되며 교육용 deterministic example을 기본 제공한다.
- 수치 기준선은 임무 승인 값이 아니다. 특히 링크 마진은 평균 조건이 아닌 요구 가용도의 worst-case에서 판정해야 한다.

[← 메인 학습 문서](../README.md)
