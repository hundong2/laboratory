# 주요 외국어 공식 자료 한국어 번역 요약

작성일: 2026-09-10  
원문 언어: 영어  
번역 방식: 저작권이 있는 표준·사이트 전문을 복제하지 않고, 원문 구조와 핵심 의미를 보존한 한국어 번역 요약  
전체 출처: [chapters/10_sources.md](chapters/10_sources.md)

## 접근·번역 범위

| 출처 | 확인 범위 | 상태 |
|---|---|---|
| NASA Small Spacecraft 2026 | index, summary, communications, avionics, ground operation web chapters | 핵심 구조 번역 요약 |
| CCSDS publications | active catalog의 제목·issue·설명, 공개 Blue/Orange/Green Book 일부 | 표준별 목적 번역 요약 |
| IETF RFC | RFC 7252, 7959, 4944, 6282, 4301, 7296, 9171, 9172 공개 전문 | 핵심 section 번역 요약 |
| SDA/ESA/ITU | 공개 web page, fact sheet 및 공개 report | 현황·roadmap 번역 요약 |
| OASIS/OMA/LoRa Alliance | 공개 specification/landing page | protocol 구조 번역 요약 |
| vendor/tool | 공식 product/documentation page | 기능·수명주기 번역 요약 |

## NASA Small Spacecraft Technology 2026

원문: [State-of-the-Art of Small Spacecraft Technology](https://www.nasa.gov/smallsat-institute/sst-soa/)

NASA 보고서는 공개적으로 확인 가능한 소형위성 기술과 성숙도를 임무 설계자·학생에게 제공한다. 2026 edition에서는 avionics가 크게 갱신되었고, communications 장에서는 free-space optical communication과 future communication technology가 보강되었다. 소개된 회사나 성능은 NASA의 보증이 아니며, payload·mission·환경에 따라 TRL(Technology Readiness Level, 기술성숙도)이 달라질 수 있다고 경고한다.

Communications 장은 system을 ground segment와 space segment로 나누고, command uplink, data downlink, satellite crosslink를 핵심 기능으로 설명한다. RF와 FSO를 두 큰 범주로 분류한다. FSO는 near-infrared 주파수와 좁은 beam으로 높은 data rate 잠재력이 있지만 더 정확한 pointing을 요구한다.

## SDA PWSA Optical Mesh

원문: [SDA Resources](https://www.sda.mil/home/work-with-us/resources/), [Transport Layer Fact Sheet](https://www.sda.mil/wp-content/uploads/2024/08/Transport-Layer-Fact-Sheet_V6.9-distro-A.pdf)

PWSA Transport Layer는 다수 LEO satellite가 optical inter-satellite link로 연결되는 mesh network다. Optical Communications Terminal standard는 서로 다른 provider의 terminal이 PWSA와 상호운용되도록 top-level technical specification을 정의한다. NEBULA standard는 constellation과 ground system이 많은 data를 낮은 latency로 운반하기 위한 network requirement를 정의한다.

핵심 의미는 optical hardware 성능만이 아니라 terminal·waveform·network interface의 vendor 간 상호운용이 operational mesh의 전제라는 점이다.

## ESA HydRON

원문: [HydRON: The fibre of the sky](https://www.esa.int/Applications/Connectivity_and_Secure_Communications/ARTES/Hydron_The_fibre_of_the_sky)

HydRON은 high-capacity optical inter-satellite link와 optical ground-space link를 엮어 terrestrial optical transport network를 우주로 확장하려는 계획이다. 공개 계획에서 첫 부분은 2027년 launch 예정인 LEO optical ring이며 ground station과 직접 연결하는 능력을 목표로 한다. 이는 optical link를 point-to-point demonstration에서 network infrastructure로 옮기는 흐름을 보여준다.

## CCSDS 핵심 표준군

원문: [CCSDS Active Publications](https://ccsds.org/publications/allpubs/)

- Space Packet Protocol은 space application data를 packet으로 운반하는 protocol과 service를 정의한다.
- TM/TC/AOS/USLP는 각각 mission link 특성에 맞는 transfer frame과 data-link service를 제공한다.
- CFDP는 file data와 metadata를 transaction으로 전달하며 acknowledged/unacknowledged class를 지원한다.
- LTP는 long-delay link의 point-to-point reliability mechanism을 제공한다.
- Schedule-Aware Bundle Routing은 scheduled contact가 있는 time-varying connectivity에서 bundle route를 계산한다.
- Space Data Link Security는 TM, TC, AOS, USLP frame에 authentication/confidentiality를 적용하는 구조를 제공한다.
- SLE service는 ground station의 return/forward link service를 mission operation system에 표준 interface로 제공한다.

주의할 점은 2015 CCSDS Bundle Protocol Blue Book은 RFC 5050 기반이고, 2025 Orange Book은 RFC 9171 BPv7 기반 experimental specification이라는 것이다.

## IETF CoAP와 Blockwise

원문: [RFC 7252](https://www.rfc-editor.org/info/rfc7252/), [RFC 7959](https://www.rfc-editor.org/info/rfc7959/)

CoAP은 제한된 microcontroller와 lossy low-power network에서 HTTP와 비슷한 RESTful service를 제공하되 implementation complexity와 packet size를 줄이도록 설계되었다. Confirmable request는 ACK와 retransmission을 사용하고 Non-confirmable message는 ACK를 요구하지 않는다. Token은 request-response correlation, Message ID는 message duplicate와 acknowledgement 처리에 사용된다.

Blockwise transfer는 큰 resource representation을 여러 CoAP exchange로 나눈다. 하위 계층 fragmentation 부담과 server conversation state를 줄이는 것이 목적이다. 각 block exchange에도 CoAP congestion control과 security rule이 그대로 적용된다.

## IETF 6LoWPAN

원문: [RFC 4944](https://www.rfc-editor.org/info/rfc4944/), [RFC 6282](https://www.rfc-editor.org/info/rfc6282/)

6LoWPAN은 IPv6 datagram을 작은 IEEE 802.15.4 frame으로 보내기 위한 adaptation format, fragmentation, address 형성을 정의한다. RFC 6282의 LOWPAN_IPHC는 link-local address, common hop limit, inferred payload length 등 공유되는 common case를 이용해 IPv6 header를 줄인다. RFC 4944의 초기 header compression 방식은 새 구현에서 권장되지 않고 RFC 6282 형식이 이를 갱신한다.

## IETF BPv7와 BPSec

원문: [RFC 9171](https://www.rfc-editor.org/rfc/rfc9171.html), [RFC 9172](https://www.rfc-editor.org/rfc/rfc9172.html)

BPv7은 intermittent connectivity, large/variable delay, high error rate 같은 stressed networking environment를 위한 DTN protocol이다. bundle은 node의 storage에 머물다가 route가 생기면 전달될 수 있다. BPSec은 Block Integrity Block과 Block Confidentiality Block을 통해 bundle block별 authentication/integrity와 confidentiality를 제공한다.

## MQTT 5.0

원문: [OASIS MQTT Version 5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html)

MQTT는 lightweight client-server publish/subscribe messaging transport다. machine-to-machine과 IoT constrained environment를 주요 적용처로 든다. Version 5는 large-scale system, better error report, request-response/capability discovery pattern, extensibility와 small-client performance를 개선했다. Specification은 authentication, authorization, secure communication 선택이 implementation 책임임을 강조한다.

## OMA LwM2M 1.2.1

원문: [LwM2M Core Specification](https://openmobilealliance.org/release/LightweightM2M/V1_2_1-20221209-A/OMA-TS-LightweightM2M_Core-V1_2_1-20221209-A.pdf)

LwM2M은 constrained IoT device를 위한 object/resource model, registration, observation, command와 device management를 정의한다. bootstrap-server를 이용하는 mode에서는 client가 Bootstrap-Request를 보내고 server가 operational LwM2M Server 접속에 필요한 Security/Server Object와 credential을 provisioning한다.

## LoRaWAN 1.0.4

원문: [LoRaWAN L2 1.0.4](https://resources.lora-alliance.org/technical-specifications/ts001-1-0-4-lorawan-l2-1-0-4-specification)

LoRaWAN network protocol은 battery-powered fixed/mobile end device에 최적화되어 있다. Class A device는 uplink 뒤 RX1과 RX2 window를 열며, frequency와 data rate 관계는 regional parameter가 결정한다. 따라서 L2 specification만 구현하고 국가별 RP002 parameter와 certification requirement를 무시해서는 안 된다.

## ITU 5G NTN과 D2C/D2D

원문: [ITU-R M.2177-0](https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.2177-0-202602-I%21%21PDF-E.pdf), [The State of Satellite Broadband 2025](https://www.itu.int/hub/publication/s-pol-broadband-31-2025/)

5G-NTN은 3GPP Release 17 이후의 NR-NTN과 IoT-NTN radio interface를 포함하며, satellite motion이 만드는 delay/Doppler 변화, moving cell, switchover, mobility를 다룬다. ITU 보고서는 D2C를 standard smartphone과 satellite의 직접 연결, D2D를 IoT device까지 포함하거나 IoT 중심으로 부르는 용례가 있음을 지적한다. 기술 발전과 함께 spectrum allocation, national licensing, terrestrial coexistence가 상용화 속도를 결정한다.

## Semtech SX1262

원문: [SX1262 공식 product page](https://www.semtech.com/products/wireless-rf/lora-connect/sx1262)

SX1262는 150–960 MHz 범위의 sub-GHz transceiver로 LoRa, LR-FHSS(Long Range Frequency Hopping Spread Spectrum), (G)FSK를 지원한다. 공식 page는 최대 +22 dBm class transmit power, 낮은 receive current, 최대 170 dB link budget 등의 product specification을 제공한다. SPI command, BUSY line, DIO IRQ route, optional DIO2 RF switch와 DIO3 TCXO control은 board/module driver에서 구분해야 한다.

## Mbed OS 수명주기

원문: [Arm Mbed OS EOL](https://www.arm.com/products/development-tools/embedded-and-software/mbed-os), [Arm Mbed GitHub](https://github.com/armmbed)

Arm은 Mbed OS와 Mbed Platform이 2026년 7월 end of life에 도달했다고 공지했다. online build tool은 더 이상 사용할 수 없고 Arm은 Mbed OS를 active maintain/support하지 않는다. source는 open source로 공개되어 있으며 community edition으로 이어지는 경로가 소개되지만, 사용 조직이 security patch와 toolchain 유지 책임을 평가해야 한다.

## strongSwan IPv6/IPsec

원문: [Route-Based VPN](https://docs.strongswan.org/docs/latest/features/routeBasedVpn.html), [MOBIKE](https://docs.strongswan.org/docs/6.0/features/mobike.html)

Linux XFRM interface는 route를 통해 IPsec processing을 제어하고 interface ID로 policy/SA와 연결할 수 있다. IPv4와 IPv6 SA가 같은 XFRM interface를 사용할 수 있으며 interface MTU와 namespace isolation에 장점이 있다. MOBIKE는 IKEv2 initiator의 network attachment/address 변경을 감지해 SA address를 갱신한다.

## MISRA, CWE와 정적 분석

원문: [MISRA](https://misra.org.uk/), [2025 CWE Top 25](https://cwe.mitre.org/top25/index.html), [clang-tidy](https://clang.llvm.org/extra/clang-tidy/)

MISRA guideline은 critical embedded code의 ambiguous, undefined, difficult-to-analyze construct를 제한하고 disciplined deviation process를 요구한다. CWE는 취약점 instance가 아니라 weakness root-cause category를 제공한다. 2025 CWE Top 25는 39,080 CVE record를 분석한 common/impactful weakness 목록이다.

clang-tidy는 Clang LibTooling 기반의 extensible C/C++ linter/static analysis interface로 bug-prone pattern, API misuse, portability, maintainability 등을 검사하고 compile command database 사용을 권장한다. 하나의 analyzer가 모든 weakness를 찾지 못하므로 compiler warning, path-sensitive analyzer, rule checker, dependency scan, dynamic test를 조합한다.

## 번역 검수 기록

- 수치와 표준 issue는 2026-09-10 공식 catalog와 대조했다.
- `may`, `can`, 계획 발표는 확정 deployment로 번역하지 않았다.
- D2C/D2D, CCSDS BP 판본, Mbed EOL처럼 오해하기 쉬운 차이를 별도 표시했다.
- 저작권이 있는 표준의 전문 문장 대조 번역은 하지 않고 학습 목적의 독립적 요약으로 제한했다.

[← 메인 문서](README.md)
