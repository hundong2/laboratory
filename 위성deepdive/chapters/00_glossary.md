# 통합 약어 및 용어 사전

이 표는 문서에서 사용하는 대표 뜻을 고정한다. 영문 약어를 처음 볼 때 `영문 전체 이름 → 한국어 → 이 시스템에서의 역할` 순서로 읽는다.

| 약어/용어 | 영문 전체 이름 | 한국어 | 실무 의미 |
|---|---|---|---|
| ACK | Acknowledgement | 확인응답 | data unit 수신 또는 protocol 단계 확인 |
| AEAD | Authenticated Encryption with Associated Data | 연관 데이터 포함 인증 암호 | 암호화와 무결성 인증을 함께 제공 |
| AOS | Advanced Orbiting Systems | 고급 궤도 시스템 | CCSDS 고속·다중 virtual channel data link |
| APID | Application Process Identifier | 응용 프로세스 식별자 | CCSDS Space Packet stream 식별 |
| API | Application Programming Interface | 응용 프로그램 인터페이스 | software component 사이 호출 계약 |
| ARQ | Automatic Repeat reQuest | 자동 재전송 요구 | ACK/NAK에 따라 손실 data 재전송 |
| BER | Bit Error Rate | 비트 오류율 | 전체 bit 중 잘못 수신된 비율 |
| BIB | Block Integrity Block | 블록 무결성 블록 | BPSec integrity/authentication block |
| BP/BPv7 | Bundle Protocol / Version 7 | 번들 프로토콜 / 버전 7 | DTN의 store-and-forward network protocol |
| BCB | Block Confidentiality Block | 블록 기밀성 블록 | BPSec encryption block |
| BDP | Bandwidth-Delay Product | 대역폭-지연 곱 | link를 채우는 비행 중 data 양 |
| BSP | Board Support Package | 보드 지원 패키지 | 특정 board pin·clock·power 설정 |
| BPSec | Bundle Protocol Security | 번들 프로토콜 보안 | BPv7 block integrity/confidentiality |
| BW | Bandwidth | 대역폭 | Hz 주파수 폭 또는 bps 처리 용량; 단위 필수 |
| CAD | Channel Activity Detection | 채널 활동 탐지 | LoRa preamble/activity 탐지 |
| CCSDS | Consultative Committee for Space Data Systems | 우주 데이터 시스템 자문위원회 | 우주 data interoperability 표준 조직 |
| CFDP | CCSDS File Delivery Protocol | CCSDS 파일 전달 프로토콜 | 우주 link에서 file/metadata 전송 |
| CLCW | Communications Link Control Word | 통신 링크 제어어 | TC delivery control feedback |
| CLTU | Communications Link Transmission Unit | 통신 링크 전송 단위 | coded telecommand 전송 단위 |
| CoAP | Constrained Application Protocol | 제약 환경 응용 프로토콜 | 작은 RESTful IoT protocol |
| CON | Confirmable | 확인형 | CoAP ACK/retransmission 대상 message |
| COP-1 | Communications Operation Procedure-1 | 통신 운용 절차 1 | CCSDS TC sequence/retransmission procedure |
| CRC | Cyclic Redundancy Check | 순환 중복 검사 | polynomial division 기반 오류 탐지 code |
| CR | Coding Rate | 부호율 | 전체 encoded bit 중 정보 bit의 비율 |
| CWE | Common Weakness Enumeration | 공통 약점 열거 | software/hardware weakness 분류 |
| D2C | Direct-to-Cell | 위성-휴대전화 직접 연결 | 일반 cellular handset의 satellite access |
| D2D | Direct-to-Device | 위성-단말 직접 연결 | IoT/handset 등 device 직접 satellite access |
| DIO | Digital Input/Output | 디지털 입출력 | radio event 또는 RF switch/TCXO control pin |
| DMA | Direct Memory Access | 직접 메모리 접근 | CPU 개입을 줄인 peripheral-memory transfer |
| DPD | Dead Peer Detection | 상대 노드 생존 탐지 | IKEv2 peer failure 확인 |
| DTLS | Datagram Transport Layer Security | 데이터그램 전송 계층 보안 | UDP application transport security |
| DTN | Delay/Disruption Tolerant Networking | 지연·단절 내성 네트워킹 | intermittent/long-delay network architecture |
| Eb/N0 | Energy per bit to noise density ratio | 비트 에너지 대 잡음밀도비 | modulation/coding 성능 판단 기준 |
| EIRP | Effective Isotropic Radiated Power | 등가 등방 복사 전력 | transmitter loss와 antenna gain 포함 방사 능력 |
| EOF | End of File | 파일 끝 | CFDP file data 종료 PDU |
| ESP | Encapsulating Security Payload | 캡슐화 보안 페이로드 | IPsec encryption/integrity protocol |
| FCLTU | Forward CLTU | 순방향 통신 링크 전송 단위 서비스 | SLE telecommand uplink service |
| FDIR | Fault Detection, Isolation and Recovery | 결함 탐지·격리·복구 | fault를 찾아 영향 범위를 제한하고 회복 |
| FEC | Forward Error Correction | 전방 오류 정정 | 재전송 없이 일부 bit error 복구 |
| FSO | Free-Space Optical communication | 자유공간 광통신 | 자유공간 laser communication |
| FSPL | Free-Space Path Loss | 자유공간 경로 손실 | 거리와 파장에 따른 ideal propagation loss |
| GEO | Geostationary Earth Orbit | 정지궤도 | 지상에서 정지해 보이는 적도 궤도 |
| GPIO | General-Purpose Input/Output | 범용 입출력 | MCU digital pin |
| G/T | Gain-to-Noise-Temperature ratio | 이득 대 잡음온도비 | receiver sensitivity system figure |
| HAL | Hardware Abstraction Layer | 하드웨어 추상화 계층 | device driver와 MCU/BSP 분리 interface |
| HARQ | Hybrid Automatic Repeat reQuest | 혼합 자동 재전송 요구 | FEC와 retransmission 결합 |
| HIL | Hardware in the Loop | 하드웨어 포함 폐루프 시험 | 실제 hardware를 simulation loop에 연결 |
| IKEv2 | Internet Key Exchange version 2 | 인터넷 키 교환 버전 2 | IPsec authentication/key negotiation |
| IoT | Internet of Things | 사물인터넷 | networked sensor/actuator system |
| IPsec | Internet Protocol Security | 인터넷 프로토콜 보안 | IP layer protection architecture |
| IRQ | Interrupt Request | 인터럽트 요청 | peripheral이 CPU service를 요구하는 signal |
| ISR | Interrupt Service Routine | 인터럽트 서비스 루틴 | IRQ에 즉시 실행되는 짧은 handler |
| ISL/OISL | Inter-Satellite Link / Optical ISL | 위성간 링크 / 광 위성간 링크 | constellation node 간 direct link |
| LEO | Low Earth Orbit | 저궤도 | 대략 수백~2,000 km Earth orbit |
| LDPC | Low-Density Parity-Check | 저밀도 패리티 검사 | 강력한 block error-correcting code |
| LNA | Low-Noise Amplifier | 저잡음 증폭기 | receiver front-end 첫 amplifier |
| LoRa | Long Range | 장거리 | chirp spread spectrum 기반 radio modulation |
| LoRaWAN | Long Range Wide Area Network | 장거리 광역망 | LoRa 기반 LPWAN MAC/network protocol |
| LPI/LPD | Low Probability of Intercept/Detection | 낮은 도청/탐지 가능성 | adversary가 signal을 찾거나 가로채기 어려움 |
| LTP | Licklider Transmission Protocol | 릭라이더 전송 프로토콜 | long-delay point-to-point DTN convergence protocol |
| LwM2M | Lightweight Machine to Machine | 경량 사물 간 통신 | CoAP 기반 device management protocol |
| MAC | Media Access Control | 매체 접근 제어 | shared link access와 frame addressing sublayer |
| MEO | Medium Earth Orbit | 중궤도 | LEO와 GEO 사이 Earth orbit |
| MISRA | Motor Industry Software Reliability Association | 자동차 산업 소프트웨어 신뢰성 협회 | embedded coding guideline 발행 조직 |
| MQTT | Message Queuing Telemetry Transport | 메시지 큐잉 원격측정 전송 | broker 기반 publish/subscribe protocol |
| MTU | Maximum Transmission Unit | 최대 전송 단위 | fragmentation 없이 link/path가 운반하는 최대 packet |
| NAK | Negative Acknowledgement | 부정 확인응답 | 누락/오류 data 재전송 요청 |
| NB-IoT | Narrowband Internet of Things | 협대역 사물인터넷 | 3GPP 저전력 cellular IoT radio technology |
| NON | Non-confirmable | 비확인형 | CoAP ACK를 요구하지 않는 message |
| NR | New Radio | 뉴 라디오 | 5G radio access technology |
| NTN | Non-Terrestrial Network | 비지상 네트워크 | satellite/airborne platform 기반 network |
| OGSL | Optical Ground-to-Space Link | 지상-우주 광 링크 | optical terminal과 ground station link |
| OSCORE | Object Security for Constrained RESTful Environments | 제약 REST 환경 객체 보안 | CoAP message object-level protection |
| OSS | Open-Source Software | 오픈소스 소프트웨어 | source license와 공개 개발 model의 software |
| PA | Power Amplifier | 전력 증폭기 | radio transmitter output amplifier |
| PAT | Pointing, Acquisition and Tracking | 지향·획득·추적 | optical terminal beam lock control loop |
| PER | Packet Error Rate | 패킷 오류율 | packet 단위 실패 비율 |
| PDU | Protocol Data Unit | 프로토콜 데이터 단위 | protocol layer가 처리하는 구조화 data |
| PMTUD | Path MTU Discovery | 경로 최대 전송 단위 발견 | path에서 fragmentation 없는 packet 크기 탐색 |
| QoS | Quality of Service | 서비스 품질 | latency/loss/priority 등 traffic service property |
| RAF | Return All Frames | 귀환 전체 프레임 | SLE return frame stream service |
| RCF | Return Channel Frames | 귀환 채널 프레임 | SLE selected channel return service |
| RF | Radio Frequency | 무선주파수 | radio electromagnetic spectrum/technology |
| RSSI | Received Signal Strength Indicator | 수신 신호 강도 지시값 | receiver가 추정한 in-band power |
| RTT | Round-Trip Time | 왕복 시간 | signal/request가 돌아오는 전체 시간 |
| RTOS | Real-Time Operating System | 실시간 운영체제 | deadline과 deterministic scheduling을 지원하는 OS |
| SABR | Schedule-Aware Bundle Routing | 일정 인지 번들 라우팅 | scheduled contact를 이용한 CCSDS DTN routing |
| SA | Security Association | 보안 연관 | IPsec의 단방향 key/algorithm/security state |
| SAST | Static Application Security Testing | 정적 응용 보안 시험 | 실행 없이 source/build artifact 분석 |
| SBOM | Software Bill of Materials | 소프트웨어 자재명세서 | component/dependency inventory |
| SCA | Software Composition Analysis | 소프트웨어 구성 분석 | dependency license/vulnerability 분석 |
| SDLS | Space Data Link Security | 우주 데이터 링크 보안 | CCSDS link-layer authentication/encryption |
| SDN | Software-Defined Networking | 소프트웨어 정의 네트워킹 | control과 forwarding의 논리 분리·programmability |
| SD-WAN | Software-Defined Wide Area Network | 소프트웨어 정의 광역망 | multiple underlay 위 policy-based WAN overlay |
| SF | Spreading Factor | 확산 계수 | LoRa symbol duration/sensitivity/data rate parameter |
| SLE | Space Link Extension | 우주 링크 확장 | ground cross-support service interface |
| SNR/SINR | Signal-to-Noise(/Interference-plus-Noise) Ratio | 신호 대 잡음(/간섭+잡음)비 | desired signal quality ratio |
| SPI | Serial Peripheral Interface | 직렬 주변장치 인터페이스 | synchronous MCU-peripheral bus |
| SWaP-C | Size, Weight, Power and Cost | 크기·무게·전력·비용 | spacecraft component trade metric |
| TC | Telecommand | 원격명령 | ground-to-space command data |
| TCP | Transmission Control Protocol | 전송 제어 프로토콜 | reliable ordered byte-stream transport |
| Telemetry/TM | Telemetry | 원격측정 | spacecraft-to-ground status/data |
| TLS | Transport Layer Security | 전송 계층 보안 | connection confidentiality/integrity/authentication |
| TT&C | Telemetry, Tracking and Command | 원격측정·추적·명령 | spacecraft operation communication functions |
| UDP | User Datagram Protocol | 사용자 데이터그램 프로토콜 | connectionless datagram transport |
| USLP | Unified Space Data Link Protocol | 통합 우주 데이터 링크 프로토콜 | CCSDS flexible unified data-link protocol |
| VPN | Virtual Private Network | 가상 사설망 | untrusted transport 위 secure logical network |
| WCET | Worst-Case Execution Time | 최악 실행시간 | task/code의 분석된 최대 실행 시간 |
| XFRM | Linux IP transform framework | 리눅스 IP 변환 프레임워크 | kernel IPsec SA/policy processing |

[← 메인](../README.md)
