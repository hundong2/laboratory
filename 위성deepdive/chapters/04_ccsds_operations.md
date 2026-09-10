# 04. CCSDS 패킷·데이터 링크·TT&C

## 1. CCSDS가 왜 생겼는가

서로 다른 우주기관의 spacecraft와 ground station이 agency별 형식만 사용하면 cross support가 어렵다. CCSDS(Consultative Committee for Space Data Systems, 우주 데이터 시스템 자문위원회)는 packet, data link, coding, file delivery, ground service, security의 상호운용 표준을 제공한다.

CCSDS 문서 색은 성숙도와 성격을 뜻한다.

- **Blue Book**: 구현 가능한 Recommended Standard(권고 표준)
- **Magenta Book**: Recommended Practice(권고 실무)
- **Green Book**: 개념과 근거를 설명하는 Informational Report
- **Orange Book**: Experimental Specification(실험 규격)
- **Yellow Book**: record, procedure 등
- **Silver Book**: historical(과거 판본)

표준 번호와 issue를 고정하지 않으면 이미 대체된 판본을 구현할 수 있다. 2026-09-10 기준 active publication을 [출처 목록](10_sources.md)에서 확인한다.

## 2. TT&C

**TT&C (Telemetry, Tracking and Command, 원격측정·추적·명령)**는 위성을 운영하는 세 기능이다.

- **Telemetry(TM, 원격측정)**: health/status, event, payload data를 우주에서 지상으로 전달
- **Tracking(추적)**: range, range-rate/Doppler, angle 등으로 orbit와 위치를 추정
- **Command/Telecommand(TC, 명령/원격명령)**: 지상에서 configuration, mode change, action을 전달

TC는 낮은 data rate라도 integrity, authentication, replay protection, execution verification이 매우 중요하다. TM은 loss 허용도에 따라 realtime housekeeping, alarm, stored telemetry, science payload로 분리한다.

### command lifecycle

```text
authorize -> encode -> uplink -> receive/authenticate
 -> accept/reject -> schedule/execute -> verify -> report completion
```

`link ACK`와 `command executed successfully`는 다르다. acceptance, start, progress, completion, failure를 별도 event로 모델링한다.

## 3. Space Packet Protocol

**CCSDS Space Packet Protocol**은 application data를 space packet으로 캡슐화해 식별, sequencing, multiplexing한다. 주요 개념은 다음과 같다.

- **APID (Application Process Identifier, 응용 프로세스 식별자)**: packet stream 구분
- **sequence flags/count**: standalone 또는 segment 관계와 순서 탐지
- **packet length**: primary header 뒤 data field 길이에서 정의되는 규칙을 정확히 따라야 함
- **secondary header**: time, service type 같은 mission profile 정보

Space Packet은 암호화나 delivery guarantee를 자동 제공하지 않는다. APID 할당, secondary header, timeout, duplicate 처리, endian, time code를 mission ICD(Interface Control Document, 인터페이스 통제 문서)에 고정한다.

## 4. TM, TC, AOS, USLP 데이터 링크

### TM Space Data Link Protocol

**TM (Telemetry) Space Data Link Protocol**은 주로 space-to-ground telemetry frame과 virtual channel을 제공한다. 지속적인 downlink와 고정 길이 frame 운용에 적합하다.

### TC Space Data Link Protocol

**TC (Telecommand) Space Data Link Protocol**은 ground-to-space command frame과 reliable delivery procedure를 지원한다. CLCW(Communications Link Control Word, 통신 링크 제어어)와 COP-1(Communications Operation Procedure-1)이 sequence와 재전송을 제어할 수 있다.

### AOS Space Data Link Protocol

**AOS (Advanced Orbiting Systems, 고급 궤도 시스템) Space Data Link Protocol**은 높은 data rate, 여러 virtual channel, 다양한 service를 위한 frame protocol이다. 2025년 10월 Issue 5가 active Blue Book으로 게시되었다.

### USLP

**USLP (Unified Space Data Link Protocol, 통합 우주 데이터 링크 프로토콜)**는 space-to-ground, ground-to-space, space-to-space를 하나의 유연한 protocol로 지원하고 future mission과 긴 frame length 요구를 수용한다. `최신이므로 무조건 USLP`가 아니라 ground compatibility, legacy equipment, mission profile과 implementation maturity를 비교한다.

### virtual channel

하나의 physical/master channel 안에 여러 logical stream을 다중화한다. critical TC, realtime TM, playback, payload를 virtual channel로 분리하면 독립 sequence, QoS(Quality of Service), buffer 정책을 둘 수 있다. priority만 두고 admission control을 하지 않으면 high-rate payload가 control channel memory를 고갈시킬 수 있다.

## 5. synchronization과 channel coding

data link frame 아래에는 다음이 배치된다.

- randomization: 긴 동일 bit pattern을 줄여 동기·spectrum 특성 개선
- attached sync marker: frame 경계 탐지
- FEC: convolutional, Reed-Solomon, turbo, LDPC(Low-Density Parity-Check) 등 profile에 맞는 오류 정정
- CLTU(Communications Link Transmission Unit): TC 전송 단위

어떤 순서로 randomize, encode, interleave, authenticate하는지 송수신 양쪽이 정확히 같아야 한다. security와 coding의 순서는 표준 profile을 따른다.

## 6. Telemetry engineering

Telemetry point는 이름만 나열하지 말고 다음 metadata를 갖는다.

| 필드 | 예 |
|---|---|
| source | EPS battery sensor 2 |
| type/unit | signed 16-bit, mV |
| calibration | raw × scale + offset |
| valid range | 18,000~25,200 mV |
| sample/report rate | 10 Hz / 1 Hz |
| quality | valid, stale, substituted |
| timestamp | onboard time + correlation quality |
| alarm | persistence, hysteresis, severity |

**housekeeping telemetry**는 상태 감시, **event report**는 의미 있는 전이, **payload telemetry**는 임무 데이터다. time correlation이 없으면 여러 subsystem event의 causal order를 잘못 해석할 수 있다.

## 7. SLE

**SLE (Space Link Extension, 우주 링크 확장)**는 ground station 또는 network가 mission control에 표준화된 space link service를 제공하도록 한다. 즉 spacecraft radio protocol이 아니라 ground-space service interface다.

- **RAF (Return All Frames, 귀환 전체 프레임)**: 수신한 frame stream 제공
- **RCF (Return Channel Frames, 귀환 채널 프레임)**: 선택된 channel frame 제공
- **FCLTU (Forward Communications Link Transmission Unit)**: TC용 CLTU를 ground station에 전달
- 서비스 instance configuration, bind/start/stop, status report, schedule과 credential이 필요하다.

`return`은 space-to-ground, `forward`는 ground-to-space 방향이다. SLE가 RF modem을 대체하지 않고, 여러 agency ground asset을 mission system에 일관된 방식으로 연결한다.

## 8. Space Data Link Security

**SDLS (Space Data Link Security, 우주 데이터 링크 보안)**는 TM, TC, AOS, USLP frame에 authentication과/or confidentiality를 적용한다. security header/trailer, security association, anti-replay sequence와 operational procedure가 핵심이다.

SDLS는 한 space link를 보호하지만 application-to-application end-to-end 보안을 항상 보장하지 않는다. trusted gateway에서 복호화되면 이후 구간은 별도 보호가 필요하다. 반대로 IPsec과 BPSec을 무조건 중첩하면 overhead와 key operation이 커진다. threat boundary를 기준으로 선택한다.

### TC 보안 필수 질문

- command origin authentication은 어디서 검증하는가?
- sequence number와 replay window는 reset 후에도 안전한가?
- key rotation이 contact loss 중 중간 상태가 되면 rollback 가능한가?
- safe-mode receiver도 secure command를 처리할 수 있는가?
- crypto failure와 link noise를 구분해 telemetry로 보고하는가?

## 9. protocol stack 예시

### 전통 telemetry

```text
Application telemetry
 -> CCSDS Space Packet
 -> TM or AOS transfer frame + SDLS
 -> synchronization/channel coding
 -> RF physical link
 -> ground modem
 -> SLE RAF/RCF
 -> mission control
```

### 파일 전달

```text
File -> CFDP PDU -> Space Packet or Encapsulation Packet
 -> AOS/USLP + SDLS -> RF/optical link
```

### DTN relay

```text
Application Data Unit -> BPv7 bundle + BPSec
 -> convergence layer/LTP -> CCSDS data link -> hop
 -> persistent store -> next scheduled hop
```

PDU는 Protocol Data Unit(프로토콜 데이터 단위)다.

## 10. 구현 검증

- golden packet/frame binary와 bit-level field map
- malformed length, unknown APID, duplicate sequence, counter wrap test
- loss, bit flip, reordering, reset, clock jump fault injection
- transmitter/receiver independent implementation interoperability test
- security association rollover와 replay test
- ground SLE provider와 bind/start/stop/error test
- long-duration virtual channel fairness와 buffer exhaustion test

[← 이전](03_space_networking.md) · [메인](../README.md) · [다음: DTN·CFDP →](05_dtn_reliability.md)
