# 01. 시스템·궤도·네트워크 기초

## 1. 왜 우주 네트워크는 지상망과 다른가

지상 유선망은 대체로 링크가 지속되고 지연이 짧으며, 장비에 전력·냉각·정비 접근성이 있다. 위성망은 노드가 빠르게 이동하고 가시성이 시간에 따라 바뀌며, 방사선·전력·열·질량 제약 속에서 원격 복구해야 한다. 따라서 `현재 연결되어 있는가`만이 아니라 `언제, 얼마나 오래, 어느 용량으로 연결될 것인가`가 topology의 일부다.

위성 시스템은 다음 세 구간으로 나눈다.

- **space segment(우주 구간)**: 위성 버스, 탑재체, 위성간 링크
- **ground segment(지상 구간)**: 지상국, 안테나, 모뎀, 임무운영센터, 데이터 처리
- **user segment(사용자 구간)**: 센서, 휴대전화, IoT 단말, 전술 단말 등 실제 서비스를 쓰는 장치

## 2. 궤도와 지연

### LEO, MEO, GEO

- **LEO (Low Earth Orbit, 저궤도)**: 대략 수백~2,000 km. 지연이 낮고 단말 링크 버짓에 유리하지만 위성이 빠르게 지나가므로 handover와 다수 위성이 필요하다.
- **MEO (Medium Earth Orbit, 중궤도)**: LEO와 GEO 사이. 항법위성 및 일부 통신망이 사용한다. 커버리지와 지연의 절충이다.
- **GEO (Geostationary Earth Orbit, 정지궤도)**: 적도 상공 약 35,786 km에서 지상에 정지해 보인다. 넓은 커버리지와 단순한 추적이 장점이나 지연과 경로 손실이 크다.

진공 전파 지연의 하한은 `거리 / 빛의 속도`다. 실제 지연은 다음 합이다.

```text
총 지연 = 전파 + 변복조/부호화 + 프레임 처리 + 라우팅 + 큐잉 + 재전송 + 애플리케이션 처리
```

RTT가 커지면 확인응답을 기다리는 stop-and-wait ARQ의 이용률이 급락한다. 전송률 `R`, RTT `T`일 때 파이프를 채우기 위한 최소 미확인 데이터량은 BDP(Bandwidth-Delay Product, 대역폭-지연 곱) `R × T`다. 예를 들어 100 Mbit/s 링크와 80 ms RTT는 1 MB의 비행 중 데이터를 필요로 한다.

## 3. bandwidth의 세 의미

1. **occupied bandwidth(점유 대역폭)**: 변조 신호가 차지하는 주파수 폭, Hz.
2. **channel capacity(채널 용량)**: 주어진 잡음·대역폭에서 이론적으로 가능한 정보율. Shannon 식은 `C = B log2(1 + S/N)`이다.
3. **throughput/goodput(처리율/유효 처리율)**: 실제 전달 비트율과 실제 애플리케이션 데이터 비트율. FEC·헤더·재전송·idle frame은 goodput을 낮춘다.

`1 MHz 대역폭 = 1 Mbit/s`는 일반적으로 거짓이다. spectral efficiency(주파수 효율, bit/s/Hz), 변조 차수, 부호율, guard band, SNR과 구현 손실이 필요하다.

## 4. topology와 contact window

**topology(토폴로지)**는 노드와 링크의 연결 구조다. 위성군에서는 그래프 `G(t)=(V,E(t))`처럼 시간 함수로 표현해야 한다. 링크 존재만으로 충분하지 않고 다음 속성을 둔다.

- 시작·종료 시간
- 단방향 또는 양방향
- data rate와 one-way light time
- 예상 오류율·가용성·비용
- 안테나/광 단말 자원 충돌
- 허용 보안 등급과 트래픽 클래스

**contact window(접속 창)**는 두 노드가 통신 가능한 시간 구간이다. 기하학적 가시성만이 아니라 최소 elevation angle(앙각), 링크 마진, 지상국 예약, 규제, 자세 제어, 전력, 날씨를 모두 통과한 운영 가능 구간이다.

접속 창의 전송 가능량은 단순하게 `rate × duration`이지만 acquisition time, ramp-up, protocol overhead, link adaptation을 빼야 한다.

```text
usable_bytes ≈ rate_bps × (window_s - acquisition_s) × efficiency / 8
```

## 5. 군집위성

**군집위성(satellite constellation)**은 공동 임무를 수행하도록 궤도·링크·운영이 설계된 다수 위성이다. 수를 늘리면 coverage와 경로 다양성이 커지지만 자동화 없이는 지상 운영 비용과 충돌 가능성이 폭증한다.

구조 예:

- **ring**: 각 위성이 앞·뒤 위성과 연결. 단순하지만 절단에 민감하다.
- **mesh**: 여러 이웃과 연결. 복원력과 경로 선택성이 높지만 단말 수, PAT, 라우팅 복잡도가 증가한다.
- **hub-and-spoke**: relay가 중심. 제어는 단순하지만 hub가 병목·단일 장애점이 된다.
- **multi-layer**: LEO sensing, MEO relay, GEO gateway처럼 궤도별 역할을 나눈다.

### 군집 설계 핵심

위성 수보다 `서비스 지속성`, `동시에 유지 가능한 ISL 수`, `경로 직경`, `지상 게이트웨이 분포`, `위성별 buffer`가 성능을 결정한다. optical terminal이 4개 있어도 attitude 또는 전력 제약으로 동시에 모두 사용할 수 없다면 명목 degree와 실제 degree가 다르다.

## 6. failover

**failover(장애 전환)**는 주 구성요소 또는 경로가 실패했을 때 예비 구성요소로 서비스를 넘기는 과정이다. `redundancy(중복)`는 자원을 복제하는 구조, `fault tolerance(결함 허용)`는 결함 중에도 기능을 유지하는 성질, `resilience(복원력)`는 저하·복구를 포함한 전체 능력이다.

### 계층별 failover

| 계층 | 감지 신호 | 전환 예 | 위험 |
|---|---|---|---|
| 하드웨어 | watchdog, 전류, self-test | cold/warm spare radio | 공통 원인 결함 |
| 링크 | loss of lock, SNR, frame error | RF ↔ optical, 다른 beam | flap, 재획득 시간 |
| 네트워크 | adjacency timeout, path metric | 다른 ISL/gateway | 오래된 topology |
| 서비스 | health probe, SLA 위반 | broker/controller replica | split brain |
| 운영 | telemetry trend, anomaly | safe mode, 지상 절차 | 자동화와 통제 균형 |

**FDIR (Fault Detection, Isolation and Recovery, 결함 탐지·격리·복구)**는 탐지 후 원인을 좁히고 안전한 상태 또는 대체 경로로 옮긴다. 단순 timeout만 쓰면 긴 RTT·일시적 차폐·혼잡을 고장으로 오인한다. hysteresis(이력 임계), hold-down timer, 다중 지표, 전환 횟수 제한이 필요하다.

### 상태기계

```text
PRIMARY -> DEGRADED -> SWITCH_PENDING -> BACKUP
   ^           |             |             |
   |           +-> RECOVER <-+-------------+
   +---------------- validated failback ----+
```

failback은 자동으로 원 경로에 즉시 복귀시키지 않는다. 검증 시간과 최소 유지 시간을 두어 ping-pong 전환을 막는다.

## 7. 요구사항을 수치로 바꾸기

`고가용성`, `저지연`, `대용량`은 검증 불가능하다. 다음처럼 바꾼다.

- 95번째 백분위 command delivery latency ≤ 3 s, 계획된 접속 중 99.9%
- critical telemetry는 생성 후 60 s 이내 지상 도달 확률 ≥ 0.999
- 단일 위성 또는 단일 지상국 상실 시 10분 이내 서비스 회복
- 하루 20 GB payload data 중 priority 1은 손실 0, priority 3은 만료 시 폐기 가능
- buffer는 최악의 3회 연속 contact miss와 20% 압축 실패 여유를 수용

이 요구사항에서 link rate, storage, contact plan, routing, FEC/ARQ, redundancy가 역산된다.

## 8. 흔한 오해

- **RSSI가 좋으면 링크가 좋다**: 간섭도 RSSI를 높인다. SNR, BER, PER을 함께 본다.
- **대역폭을 늘리면 항상 유리하다**: 수신 잡음 전력도 대역폭에 비례해 증가하고 규제·전력이 따른다.
- **위성 수가 많으면 가용성이 높다**: 공통 소프트웨어 버그, 동일 공급망, 지상국 집중은 전체를 동시에 실패시킬 수 있다.
- **backup이 있으면 failover가 된다**: 탐지, 상태 동기화, 전환, 복귀, 정기 시험까지 있어야 한다.

[← 메인](../README.md) · [다음: RF·FSO 링크 →](02_rf_optical_link_budget.md)
