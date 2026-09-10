# 위성 통신·네트워크 절충 분석 보고서

문서 ID: `TO-SATNET-001`  
Revision: `0.1`  
작성일: 2026-09-10

## 1. 평가 원칙

후보를 고르기 전에 임무 deadline, data volume, coverage, 가용성, SWaP-C(Size, Weight, Power and Cost; 크기·무게·전력·비용), 규제, 상호운용, 개발 일정과 위험 허용도를 수치화한다. 점수는 사실이 아니라 가정의 함수이므로 weight와 evidence를 함께 남기고 ±20% sensitivity analysis를 수행한다.

## 2. RF ISL 대 Optical ISL

| 기준 | RF ISL | Optical ISL(FSO/laser) | 설계 함의 |
|---|---|---|---|
| 처리율/주파수 자원 | 보통 낮고 spectrum 조정 필요 | 높은 잠재 처리율, 좁은 beam | 대용량 backbone은 optical 우세 |
| 획득·추적 | beamwidth가 넓어 상대적으로 관대 | 정밀 PAT와 ephemeris 필요 | commissioning 위험은 RF가 낮음 |
| 간섭/탐지 | sidelobe·간섭·규제 고려 | 좁은 beam으로 공간 재사용·low probability of intercept에 유리 | 보안은 별도 암호가 여전히 필요 |
| 날씨 | ISL은 대기 영향 없음, 지상 RF는 band별 rain fade | ISL은 대기 없음, optical ground는 cloud에 취약 | optical gateway diversity 필요 |
| terminal SWaP | 안테나·PA와 band에 좌우 | aperture, fast steering, thermal stability | 실제 vendor data로 비교 |
| 성숙도 | 높은 편 | 빠르게 성장하나 interoperability/PAT가 핵심 | 혼합망이 현실적 기준선 |

권장 기준선: mission-critical 저율 제어·초기 획득·복구에는 RF, 대용량 정상 데이터에는 optical을 배치하는 dual-plane 또는 hybrid mesh를 우선 검토한다. 두 링크의 공통 원인 고장과 실제 redundancy를 따로 검증한다.

## 3. Routing 방식

| 후보 | 장점 | 약점 | 적합 조건 |
|---|---|---|---|
| reactive distributed | 예상 밖 장애에 자율 대응 | convergence, loop, control overhead | 연결성이 충분하고 상태 전파가 빠름 |
| precomputed contact routing | 궤도 예측 활용, deterministic | plan drift와 unplanned outage | 예측 가능한 scheduled contacts |
| Space SDN policy | 중앙 최적화·slice/QoS | controller 단절과 stale rule | 지상 계산 + onboard fallback |
| DTN store-and-forward | 단절과 긴 RTT 수용 | storage custody·security·expiry 운영 | intermittent/deep-space path |

권장 기준선: contact plan 기반 route + onboard local repair + DTN persistence를 조합하고, SDN controller는 정책/최적화에 사용하되 단일 실시간 의존점으로 만들지 않는다.

## 4. 데이터율·패킷·window

높은 PHY rate가 자동으로 높은 goodput을 뜻하지 않는다. acquisition overhead, FEC code rate, header, retransmission, short contact의 ramp-up을 포함한다. packet이 크면 header 비율은 줄지만 한 번의 오류로 잃는 payload와 재조립 memory가 증가한다. 전송 window는 적어도 BDP를 수용하되 flight memory, maximum outstanding command, replay window와 함께 제한한다.

## 5. Buffering 정책

| 정책 | 장점 | 위험 |
|---|---|---|
| FIFO(First In, First Out, 선입선출) | 단순·예측 가능 | bulk가 critical deadline을 막음 |
| strict priority | critical 보호 | 낮은 class starvation |
| WFQ(Weighted Fair Queuing, 가중 공정 큐잉) | class 간 최소 몫 | 구현·검증 복잡도 |
| deadline-aware | 임무 가치 반영 | clock/metadata 오류에 민감 |

권장 기준선: critical reserved capacity + class별 quota + deadline/expiry + persistent journal. buffer 크기는 `최대 생성률 × 최대 무접속 시간 × 안전계수`에서 시작하고 압축 실패·재전송·metadata·wear leveling을 더한다.

## 6. Redundancy(중복성)

- cold standby는 전력은 작지만 전환과 잠복 결함 위험이 크다.
- hot standby는 빠르지만 전력·열·공통 원인 고장 가능성이 커진다.
- packet replication은 지연 tail을 줄일 수 있으나 capacity를 소비하고 duplicate suppression이 필수다.
- path diversity는 같은 안테나, clock, power rail, routing database를 공유하면 독립 redundancy가 아니다.

## 7. 가중 평가표 양식

| 기준 | Weight | RF-only | Optical-only | Hybrid | 근거/불확실성 |
|---|---:|---:|---:|---:|---|
| 임무 처리율 | TBD | TBD | TBD | TBD | traffic model |
| 99.9% service availability | TBD | TBD | TBD | TBD | weather/contact simulation |
| SWaP-C | TBD | TBD | TBD | TBD | vendor quote/test |
| 일정·성숙도 | TBD | TBD | TBD | TBD | TRL와 qualification evidence |
| 상호운용·규제 | TBD | TBD | TBD | TBD | standards/licensing |

점수 합계만으로 결론내리지 않는다. mandatory threshold를 먼저 적용하고, 통과 후보에만 가중 합계를 사용한다. 최종 선택에는 바뀌면 결론이 뒤집히는 핵심 가정을 명시한다.

[← 실무 산출물](../README.md)
