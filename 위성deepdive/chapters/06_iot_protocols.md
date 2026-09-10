# 06. 위성 IoT 프로토콜

## 1. IoT protocol stack을 고르는 기준

IoT(Internet of Things, 사물인터넷)는 sensor와 actuator를 network로 연결한다. 위성 IoT에서는 작은 battery, 낮은 data rate, 긴/가변 RTT, intermittent coverage, 국가별 spectrum 규제가 terrestrial IoT보다 강하다. `가볍다`는 말은 최소한 header byte, code/RAM, handshake, keepalive, retransmission, security overhead로 나눠 평가한다.

## 2. MQTT

**MQTT (Message Queuing Telemetry Transport, 메시지 큐잉 원격측정 전송)**는 client가 broker를 통해 topic에 message를 publish하고 subscriber가 받는 client-server publish/subscribe protocol이다. OASIS MQTT 5.0은 scalability, error reporting, request/response pattern, user property 등을 강화했다.

### 구성요소

- **publisher**: message 발행
- **subscriber**: topic filter를 등록하고 message 수신
- **broker**: connection, subscription, retained message, session과 routing 관리
- **topic**: 계층형 UTF-8 이름, 예: `sat/42/eps/battery`
- **QoS (Quality of Service)**: 전달 handshake 수준

### QoS

- **QoS 0, at most once**: 한 번 전송, 확인 없음. 손실 가능.
- **QoS 1, at least once**: PUBACK 확인까지 재전송. duplicate 가능.
- **QoS 2, exactly once protocol flow**: 4단계 handshake로 application message 중복 전달을 억제. session state와 비용이 큼.

QoS 2도 physical actuator action의 exactly-once를 자동 보장하지 않는다. application command ID와 execution journal이 필요하다.

### 위성에서의 주의점

MQTT는 보통 TCP 위에서 동작해 long RTT, loss, contact break에 민감하다. persistent session, message expiry, Receive Maximum, Session Expiry Interval을 조정하고, spacecraft/ground edge에 broker 또는 bridge를 둔다. MQTT-SN(MQTT for Sensor Networks)은 UDP 등 비-TCP network를 위한 별도 protocol이지만 MQTT 5.0과 동일 wire protocol이 아니다.

TLS(Transport Layer Security)는 connection 구간을 보호한다. 여러 broker bridge를 거치며 decrypt/re-encrypt하면 true end-to-end confidentiality가 아니므로 payload-level protection을 검토한다.

## 3. CoAP

**CoAP (Constrained Application Protocol, 제약 환경 응용 프로토콜)**은 constrained node와 low-power lossy network를 위한 RESTful application protocol이다. 기본 CoAP은 UDP 위에서 작은 binary header, method `GET/POST/PUT/DELETE`, response code, URI option, content format을 제공한다.

### Message ID와 Token

- **Message ID**: confirmable 전송의 duplicate와 ACK/RST를 연결하는 hop endpoint 수준 식별자
- **Token**: request와 response를 연결하는 client-local 식별자

둘을 혼동하면 separate response나 retransmission에서 잘못 매칭한다.

### CON

**CON (Confirmable, 확인형)** message는 ACK(Acknowledgement)를 받을 때까지 exponential backoff로 재전송한다. receiver가 즉시 response를 만들면 ACK에 piggyback할 수 있고, 늦으면 empty ACK 후 separate response를 보낸다.

장점은 loss recovery, 단점은 RTT마다 state와 traffic이 증가하는 것이다. contact가 ACK timeout보다 짧거나 one-way path면 적합하지 않다.

### NON

**NON (Non-confirmable, 비확인형)** message는 ACK를 요구하지 않는다. frequent non-critical telemetry처럼 일부 loss가 허용될 때 적합하다. duplicate detection은 여전히 가능하지만 delivery 보장은 없다. 중요한 명령을 단지 overhead가 작다는 이유로 NON으로 보내면 안 된다.

### Blockwise transfer

큰 representation을 작은 block으로 나눈다.

- **Block1**: request payload를 분할해 upload
- **Block2**: response payload를 분할해 download
- option의 `NUM`: block number, `M`: more flag, `SZX`: block size exponent

Block size는 `2^(SZX+4)` bytes 범위로 표현되며 base RFC에서 16~1024 bytes다. RFC 7959의 목표는 lower-layer fragmentation과 server state를 줄이는 것이다. loss가 있을 때 작은 block만 재전송하지만 request/response 왕복이 늘어난다. 긴 RTT에서는 BERT(Block-Wise Transfer over Reliable Transport) 또는 application/DTN file protocol이 더 나을 수 있다.

RFC 7959는 RFC 9177의 Q-Block1/Q-Block2 option으로 일부 갱신되었다. 새 구현은 최신 update와 congestion control을 확인한다.

### Observe와 security

Observe option은 resource 변경 notification을 subscription처럼 받게 한다. security는 DTLS(Datagram Transport Layer Security) 또는 OSCORE(Object Security for Constrained RESTful Environments)를 사용할 수 있다. DTLS는 hop/transport connection 보호, OSCORE는 CoAP message field를 object security로 보호해 proxy 통과 시 유리하다.

## 4. MQTT와 CoAP 선택

| 질문 | MQTT | CoAP |
|---|---|---|
| 상호작용 | broker pub/sub | resource request/response, observe |
| 기본 transport | TCP | UDP |
| 중개 | broker 필수 | proxy 선택 |
| device management | 별도 model 필요 | LwM2M이 표준 model 제공 |
| 단절 | persistent session/edge bridge 필요 | retry/observe만으로 장기 단절 해결 못함 |
| large file | 권장 핵심 기능 아님 | blockwise, 그러나 CFDP/DTN과 비교 |

## 5. LwM2M

**LwM2M (Lightweight Machine to Machine, 경량 사물 간 통신)**은 OMA SpecWorks가 정의한 device management와 service enablement protocol이다. CoAP, object/resource model, registration, observation, firmware update, security와 bootstrap을 묶는다.

### Object model

URI는 `/Object ID/Instance ID/Resource ID` 형식이다. 예:

- Security Object `0`
- Server Object `1`
- Device Object `3`
- Firmware Update Object `5`

Read, Write, Execute, Create, Delete, Observe operation을 resource permission에 따라 쓴다. vendor extension은 ID 등록·schema version·compatibility를 관리한다.

### bootstrap

**bootstrap(부트스트랩)**은 새 device가 어느 LwM2M Server를 어떤 credential로 신뢰할지 provisioning하는 절차다.

1. factory bootstrap 또는 bootstrap-server 정보로 최초 신뢰 anchor 준비
2. client가 Bootstrap-Request 전송
3. Bootstrap Server가 Security/Server Object를 write/delete
4. Bootstrap-Finish
5. client가 operational LwM2M Server에 Register

bootstrap credential과 operational credential을 분리하고, key material이 log/telemetry에 노출되지 않도록 secure element 또는 protected storage를 쓴다. 실패 중 power loss가 나도 최소 한 개의 복구 가능한 bootstrap path가 남아야 한다.

## 6. 6LoWPAN

**6LoWPAN (IPv6 over Low-Power Wireless Personal Area Networks, 저전력 무선 개인영역망에서의 IPv6)**은 작은 IEEE 802.15.4 frame에서 IPv6를 쓰기 위한 adaptation layer다. IPv6 minimum MTU 1280 bytes와 802.15.4의 작은 frame 간 격차 때문에 탄생했다.

기능:

- LOWPAN_IPHC를 통한 IPv6 header compression
- UDP next-header compression
- fragmentation/reassembly
- mesh addressing 관련 dispatch

RFC 6282의 common case에서 IPv6 header를 매우 작게 줄일 수 있지만 context synchronization이 틀리면 packet이 해석되지 않는다. link-layer fragment 하나만 잃어도 전체 IPv6 datagram을 재조립하지 못하므로 application payload를 작게 유지하는 편이 좋다.

6LoWPAN은 LoRaWAN과 동일하지 않다. 전자는 IPv6 adaptation 기술, 후자는 LoRa 기반 LPWAN network protocol이다. SCHC(Static Context Header Compression, 정적 문맥 헤더 압축)는 LPWAN 같은 더 작은 MTU를 위한 후속 접근으로 유망하다.

## 7. LoRa와 LoRaWAN

**LoRa (Long Range, 장거리)**는 Semtech의 chirp spread spectrum 계열 physical modulation 기술이다. **LoRaWAN (Long Range Wide Area Network, 장거리 광역망)**은 LoRa Alliance가 정의한 MAC/network protocol이다.

### LoRa physical parameters

- **SF (Spreading Factor, 확산 계수)**: symbol당 chirp 수를 좌우. 높으면 sensitivity와 airtime이 증가하고 data rate가 감소.
- **BW (Bandwidth, 대역폭)**: 대표적으로 125/250/500 kHz 등 region/chip profile에 따라 선택.
- **CR (Coding Rate, 부호율)**: redundancy 수준.
- airtime이 길면 energy, collision, duty-cycle 사용량이 증가.

### LoRaWAN architecture

```text
end device -> one or more gateways -> network server -> application server
                                      -> join server
```

gateway는 packet forwarder에 가깝고 network server가 duplicate 제거, MIC(Message Integrity Code), frame counter, ADR(Adaptive Data Rate), downlink scheduling을 담당한다.

### device class

- **Class A**: uplink 후 RX1/RX2 receive window. 모든 device 필수, 최저 전력.
- **Class B**: periodic beacon과 scheduled ping slot 추가.
- **Class C**: 송신 때를 제외하고 거의 계속 수신, 전력 소모 큼.

ABP(Activation by Personalization)보다 OTAA(Over-the-Air Activation)가 session key 갱신과 lifecycle에 유리하다. frame counter rollback은 replay 취약점을 만들 수 있다.

LoRaWAN L2 1.0.4와 Regional Parameters RP002는 별도 문서다. KR920 등 지역별 channel, duty-cycle, EIRP 제한과 인증을 실제 배포 전에 확인한다.

## 8. SX1276, SX1262와 RF module

SX1276과 SX1262는 Semtech sub-GHz transceiver IC다. module은 chip에 crystal/TCXO, matching network, RF switch, PA, antenna connector, shielding을 결합한 제품이다. 같은 SX1262 module이라도 pinout, RF switch control, TCXO voltage, frequency matching, regulatory certification이 다르다.

| 특성 | SX1276 계열 | SX1262 계열 |
|---|---|---|
| 제어 모델 | register 중심 | opcode command + BUSY 중심 |
| IRQ | 여러 DIO mapping register | IRQ mask를 DIO1/2/3로 route |
| TX power | variant/board에 따라 | SX1262 최대 +22 dBm class |
| 신규 설계 | 오래된 성숙 생태계 | 저전력·새 기능으로 일반적 우선 후보 |

chip maximum과 module/country legal EIRP는 다르다. antenna gain과 feed loss까지 포함해 규제를 지킨다.

### 관련 radio IC·module 계열을 읽는 법

- **SX1261/SX1262**: sub-GHz LoRa/(G)FSK/LR-FHSS transceiver. SX1262는 +22 dBm class PA가 특징이다.
- **SX1276/77/78/79**: 성숙한 이전 세대 sub-GHz LoRa/FSK register 기반 계열. 기존 board와 software 유지에 많이 보인다.
- **SX1280/1281**: 2.4 GHz LoRa/FLRC(Fast Long Range Communication) 계열. sub-GHz SX1262와 RF front-end·range·regulation이 다르다.
- **LR1110/LR1120/LR1121 계열**: multi-band 또는 geolocation/long-range 기능을 통합한 후속 제품군. 정확한 band와 기능은 part number별 최신 datasheet로 확인한다.
- **SX1302/SX1303**: multi-channel LoRa gateway baseband 계열로 end-device transceiver가 아니다.
- **STM32WL 계열**: MCU와 sub-GHz radio를 한 package에 통합한 SoC(System on Chip, 단일칩 시스템) 선택지다.
- **module 예시**: Murata Type 1SJ, Seeed Wio-E5/STM32WLE5, RAK3172, Ebyte E22 계열처럼 chip에 crystal, matching, shielding을 묶은 제품이 있다. 이름이 비슷해도 band, power, firmware interface, certification이 다르므로 정확한 ordering code를 확인한다.

우주 탑재에서는 commercial module 이름보다 radiation tolerance, temperature range, vacuum/outgassing, oscillator Doppler stability, latch-up protection, lot traceability와 qualification evidence가 우선이다. 지상 prototype에서 통신되었다는 사실은 flight qualification이 아니다.

## 9. D2C와 위성 IoT

용어가 혼용되므로 구분한다.

- **D2C (Direct-to-Cell, 위성-일반 휴대전화 직접 연결)**: 수정하지 않은 또는 표준 cellular handset을 satellite와 연결.
- **D2D (Direct-to-Device, 위성-단말 직접 연결)**: broader term이며 IoT device를 포함. ITU 자료는 D2C를 smartphone, D2D를 IoT 중심으로 구분하는 용례도 소개한다.
- **NTN (Non-Terrestrial Network, 비지상 네트워크)**: satellite, high-altitude platform 등을 포함하는 3GPP network segment.

3GPP Release 17은 NR-NTN과 NB-IoT/eMTC 기반 IoT-NTN을 위한 latency, Doppler, timing, mobility enhancement를 표준화했다. 위성 IoT의 유망 use case는 maritime asset, agriculture, environment sensor, pipeline, disaster backup이다.

### 기술 난제

- 단말의 작은 antenna와 낮은 EIRP
- fast Doppler와 timing advance
- moving beam과 feeder-link switchover
- 긴 RTT와 HARQ/resource scheduling
- sparse message에 비해 큰 attach/authentication overhead
- spectrum coordination, country border beam shaping, roaming
- battery 수명과 satellite pass prediction

현재는 저속 message·emergency·asset telemetry가 broadband보다 경제적·기술적으로 먼저 성숙한다. 미래에는 terrestrial/NTN seamless roaming, direct-to-standard-chipset, regenerative payload가 중요하다.

## 10. 권장 결합 패턴

- local sensor: CoAP/LwM2M over UDP/IPv6/6LoWPAN
- LPWAN sensor: compact binary payload over LoRaWAN, gateway에서 LwM2M/MQTT bridge
- satellite pass가 드문 sensor: message expiry와 local persistent queue
- constellation backbone: IP 또는 BPv7/DTN; application MQTT bridge는 edge에 위치
- large software/image: MQTT message로 억지 전송하지 말고 CFDP 또는 검증된 block/file transfer 사용

[← 이전](05_dtn_reliability.md) · [메인](../README.md) · [다음: HAL·RTOS →](07_embedded_platform.md)
