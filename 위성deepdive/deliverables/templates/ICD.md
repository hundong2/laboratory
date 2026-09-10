# ICD — 위성 통신 시스템 인터페이스 제어 문서

문서 ID: `ICD-SATNET-001`  
Revision: `0.1 Draft`  
작성일: 2026-09-10

## 1. 목적과 변경 통제

ICD(Interface Control Document, 인터페이스 제어 문서)는 두 구성요소 사이에서 송신자가 무엇을 보장하고 수신자가 무엇을 가정할 수 있는지 고정한다. 설계 설명서가 아니라 계약서다. 표의 `TBD`(To Be Determined, 추후 결정)는 시험 전 모두 닫아야 하며, 주파수·전압·pin·byte order·시간 기준은 추측하지 않는다.

변경 요청에는 영향받는 요구사항, 호환성, 시험, 운용 절차와 rollback을 기록한다. wire format을 바꾸면 major version, 해석을 보존한 확장은 minor version을 증가시킨다.

## 2. 시스템 경계와 공통 규칙

| 항목 | 기준선 |
|---|---|
| 시간 | TAI(International Atomic Time, 국제원자시) 또는 UTC(Coordinated Universal Time, 협정세계시) 중 하나를 mission epoch와 함께 고정. leap second 처리 명시 |
| byte order | network byte order인 big-endian을 기본값으로 사용하되 각 필드에 명시 |
| bit numbering | CCSDS 관례에 맞춰 most-significant bit를 bit 0으로 정의 |
| 식별 | spacecraft ID, virtual channel ID, APID(Application Process Identifier, 응용 프로세스 식별자), command ID의 할당표를 형상관리 |
| 단위 | SI(International System of Units, 국제단위계) 우선, dB/dBW/dBi처럼 로그 단위는 기준을 표기 |
| 오류 | drop, retry, reset, quarantine, operator alarm 가운데 동작과 최대 시간을 인터페이스마다 명시 |
| 보안 | 인증 주체, 키 ID, algorithm suite, anti-replay window, 실패 시 동작을 명시 |

## 3. 인터페이스 요약

| ID | A ↔ B | 계층 | 주요 계약 | 관련 요구사항 |
|---|---|---|---|---|
| IF-RF-01 | 위성 RF 송수신기 ↔ 안테나 | RF/동축 | 주파수, 전력, 손실, impedance, inhibit | COM-003 |
| IF-OPT-01 | 위성 광 단말 ↔ 광학계 | 광학 | 파장, divergence, aperture, PAT, eye safety | COM-002 |
| IF-HW-01 | 비행 컴퓨터 ↔ RF 모듈 | SPI/GPIO | mode, clock, chip select, reset, IRQ | COM-008 |
| IF-SW-01 | radio HAL ↔ network service | 함수/queue | buffer ownership, timeout, error code | COM-007, COM-008 |
| IF-NET-01 | 위성 ↔ 위성 | data link/network | framing, MTU, routing metric, handover | COM-002, COM-007 |
| IF-GS-01 | 위성 ↔ 지상국 | RF/data link | modulation, coding, CCSDS frame profile | COM-003 |
| IF-GS-02 | 지상국 ↔ 임무센터 | SLE/IP | RAF/RCF/FCLTU profile, TLS/IPsec, timing | COM-006 |
| IF-UT-01 | 사용자 단말 ↔ 위성 | access/IoT | attach, payload, duty cycle, retry, security | COM-001 |
| IF-SEC-01 | command source ↔ executor | security | authentication, freshness, authorization | COM-005, COM-011 |

## 4. RF 인터페이스 — IF-RF-01 / IF-GS-01

| 파라미터 | 단위 | 허용값/범위 | 검증 방법 | 상태 |
|---|---:|---|---|---|
| center frequency / channel plan | Hz | TBD, 관할 허가와 일치 | spectrum analyzer | TBD |
| occupied bandwidth | Hz | TBD | 99% occupied bandwidth 측정 | TBD |
| conducted output power | dBW | min/nominal/max TBD | calibrated power meter | TBD |
| EIRP(Equivalent Isotropically Radiated Power, 등가 등방성 복사전력) | dBW | link budget와 규제 mask 충족 | chamber/range + 계산 | TBD |
| antenna gain pattern | dBi | azimuth/elevation별 파일 | antenna range | TBD |
| polarization | — | RHCP/LHCP/linear 중 명시 | axial ratio 포함 | TBD |
| modulation/coding | — | waveform ID와 FEC profile | vector signal analyzer | TBD |
| Doppler range/rate | Hz, Hz/s | acquisition/track 범위 TBD | channel emulator | TBD |
| receiver sensitivity | dBm | 목표 PER에서 TBD | conducted test | TBD |
| impedance/connector | Ω / part no. | 50 Ω, 실제 part TBD | inspection/TDR | TBD |

RSSI(Received Signal Strength Indicator, 수신 신호 세기 지표)는 vendor-specific raw code인지 dBm calibration 값인지 구분한다. SNR(Signal-to-Noise Ratio, 신호대잡음비)은 측정 bandwidth, integration time, pre/post-FEC 위치를 함께 기록한다.

## 5. 광 인터페이스 — IF-OPT-01

파장, 송신 광전력, aperture, beam divergence, receiver field of view, detector sensitivity, acquisition beacon, PAT(Pointing, Acquisition and Tracking, 지향·획득·추적) state와 transition timeout을 고정한다. `SEARCH → ACQUIRE → TRACK → DATA → HOLD/REACQUIRE` 상태와 실패 코드를 열거한다. cloud/turbulence는 지상 광 링크에, jitter/thermal distortion은 ISL에 별도 budget으로 포함한다.

## 6. 하드웨어 인터페이스 — IF-HW-01

### 6.1 SPI

| 항목 | 계약 |
|---|---|
| mode | CPOL(Clock Polarity, 클록 극성)/CPHA(Clock Phase, 클록 위상) 조합 TBD |
| maximum clock | 데이터시트와 board signal-integrity 시험 중 작은 값 |
| word/byte order | 8-bit word, multi-byte register order 명시 |
| chip select | active-low 여부, setup/hold 시간, transaction 동안 유지 여부 |
| ownership | 단일 driver task가 bus mutex와 DMA lifetime 소유 |
| 오류 | timeout, bus fault, invalid status를 서로 다른 error code로 반환 |

### 6.2 GPIO, reset, DIO, IRQ

- reset GPIO는 active level, minimum pulse, power-on 안정 시간과 post-reset ready 조건을 정의한다.
- DIO(Digital Input/Output, 디지털 입출력) mapping은 `DIO1=RxDone|TxDone|Timeout`처럼 event-to-pin 표와 register configuration을 함께 version 관리한다.
- IRQ(Interrupt Request, 인터럽트 요청)는 edge/level, polarity, deglitch, 공유 여부, maximum interrupt rate를 기록한다.
- ISR(Interrupt Service Routine, 인터럽트 서비스 루틴)은 timestamp와 event flag만 확보하고 SPI read/write와 callback은 RTOS task로 미룬다.

## 7. 소프트웨어 인터페이스 — IF-SW-01

```c
typedef enum {
    RADIO_OK = 0,
    RADIO_E_TIMEOUT,
    RADIO_E_BUSY,
    RADIO_E_CRC,
    RADIO_E_IO,
    RADIO_E_STATE
} radio_status_t;

radio_status_t radio_send(const uint8_t *data, size_t length,
                          uint32_t deadline_ms, uint32_t transaction_id);
```

계약에는 maximum payload, zero-length 허용 여부, 호출 문맥(task/ISR), 동기·비동기, buffer 복사/대여, timeout 이후 하드웨어 상태, callback 순서, 재진입성과 thread safety를 명시한다. transaction ID는 중복 요청과 지연 callback을 구분한다.

## 8. 네트워크·패킷 인터페이스 — IF-NET-01

| 항목 | 기준선 결정 |
|---|---|
| encapsulation | CCSDS Space Packet / IPv6 / Bundle Protocol 조합과 순서 |
| maximum packet | 각 계층 header 포함/제외 여부를 명시한 octet 수 |
| segmentation | 수행 계층 하나를 지정하고 재조립 timeout·memory cap 설정 |
| sequence | CCSDS 14-bit sequence count wrap 처리, 중복 cache 범위 |
| CRC | polynomial, initial value, reflected input/output, final XOR, coverage |
| routing | metric, contact-plan version, stale-state 처리, loop prevention |
| handover | trigger, hysteresis, time-to-trigger, make-before-break 가능 여부 |
| QoS | traffic class, deadline, drop precedence, reserved capacity |

CCSDS Space Packet의 packet length 필드는 전체 길이가 아니라 `packet data field octets - 1`이다. 길이 검사는 allocation 전에 수행하며, APID와 command service를 authorization policy에 연결한다.

## 9. 지상 인터페이스 — IF-GS-02

SLE(Space Link Extension, 우주 링크 확장) service instance별 RAF(Return All Frames), RCF(Return Channel Frames), FCLTU(Forward Communications Link Transmission Unit) 사용 여부, version, bind identity, latency, delivery mode, gap indication을 지정한다. 전송 보호는 TLS(Transport Layer Security, 전송 계층 보안) 또는 IPsec profile과 인증서/키 rotation 절차를 포함한다.

## 10. 보안 인터페이스 — IF-SEC-01

command는 `source identity + role + spacecraft ID + command ID + sequence/freshness + validity window + authentication tag`를 검증한 후에만 실행한다. reset 이후 anti-replay counter rollback을 막는 persistent monotonic state와 emergency-key 절차를 정의한다. 인증 실패와 권한 실패는 audit에는 구분하되 외부 응답으로 과도한 정보를 노출하지 않는다.

## 11. 수락 기준과 미결정 항목

- 모든 `TBD`가 승인된 요구사항·부품 데이터·시험 결과 중 하나로 닫혀야 한다.
- 양측 독립 구현으로 정상·경계·오류 vector를 교환한다.
- major/minor version 호환표와 unsupported-version 동작을 시험한다.
- timing, payload length, endian, CRC, reset, duplicate, timeout fault를 주입한다.
- 각 결과는 [시험 절차](test-procedure.md)와 [요구사항 추적 매트릭스](../results/requirements-traceability.xlsx)에 연결한다.

[← 실무 산출물](../README.md)
