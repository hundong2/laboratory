# 위성 통신·네트워크·임베디드 시스템 Deep Dive

작성일: 2026-09-10  
최신성 확인 기준일: 2026-09-10

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [전문가 학습 지도](#전문가-학습-지도)
- [기초 개념](#기초-개념)
- [핵심 요약](#핵심-요약)
- [상세 정리](#상세-정리)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [실무 산출물](#실무-산출물)
- [현재와 미래의 유망 기술](#현재와-미래의-유망-기술)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

이 자료는 사용자가 지정한 48개 항목과 하위 항목을 하나의 위성 통신 시스템 관점에서 연결한다. 마지막의 빈 `49.`는 별도 기술로 추정하지 않고, 시스템 통합 설계·검증·운영 로드맵으로 보완했다. 특정 임무 요구사항이 없으므로 저궤도(Low Earth Orbit, LEO) 소형 군집위성과 지상국을 주 사례로 삼되, 정지궤도(Geostationary Earth Orbit, GEO)와 심우주에서 달라지는 지연·링크·운영 조건도 구분한다.

주요 근거는 CCSDS(Consultative Committee for Space Data Systems, 우주 데이터 시스템 자문위원회), IETF(Internet Engineering Task Force, 인터넷 기술 표준화 기구), NASA(National Aeronautics and Space Administration, 미국 항공우주국), ESA(European Space Agency, 유럽우주국), ITU(International Telecommunication Union, 국제전기통신연합), 3GPP(3rd Generation Partnership Project, 이동통신 표준화 협력체), OMA(Open Mobile Alliance, 개방형 모바일 연합), OASIS(Organization for the Advancement of Structured Information Standards), LoRa Alliance, Semtech, Arm, FreeRTOS, Wind River, MISRA와 MITRE의 공식 자료다. 링크별 한국어 번역 요약과 접근 범위는 [translation.ko.md](translation.ko.md)에, 전체 참고문헌은 [출처 목록](chapters/10_sources.md)에 정리했다.

이 문서는 표준 원문을 대체하지 않는다. 주파수 허가, 암호 승인, 우주 부품 등급, 안전 인증 및 실제 비행 설계는 관할 규정·최신 표준 판본·부품 데이터시트·임무 요구사항을 다시 확인해야 한다.

## 한눈에 보기

위성 통신 시스템은 하나의 프로토콜이 아니라 다음의 연쇄다.

```text
임무 데이터/명령
  -> MQTT·CoAP·LwM2M 또는 임무 애플리케이션
  -> IP/IPv6·6LoWPAN 또는 DTN Bundle Protocol
  -> CCSDS Space Packet·CFDP
  -> TM/TC/AOS/USLP 데이터 링크 + SDLS/BPSec/IPsec 보안
  -> FEC·변조·RF/FSO 물리 링크
  -> 안테나/광학 단말·SX1262 같은 무선 칩·지상국
```

실제 설계의 핵심은 계층을 많이 쌓는 것이 아니라, 어느 계층이 신뢰성·보안·재전송·분할·중복 제거를 책임지는지 한 번만 명확히 정하는 것이다. 링크가 끊기는 우주 환경에서는 종단 간 TCP(Transmission Control Protocol, 전송 제어 프로토콜)만으로 문제를 해결하기 어렵다. 예측 가능한 접속 시간에는 contact plan(접속 계획), store-and-forward(저장 후 전달), DTN(Delay/Disruption Tolerant Networking, 지연·단절 내성 네트워킹)이 중심이 된다.

## 전문가 학습 지도

| 단계 | 먼저 답할 질문 | 핵심 산출물 |
|---|---|---|
| 1. 임무 | 누가 어떤 데이터를 언제까지 받아야 하는가? | 데이터량, 마감시간, 가용성, 보안 등급 |
| 2. 궤도·접속 | 어느 노드가 언제 보이는가? | topology, contact window, 시간변화 그래프 |
| 3. 링크 | 해당 거리·주파수·날씨에서 비트가 전달되는가? | 링크 버짓, Eb/N0, 링크 마진 |
| 4. 데이터 링크 | 프레임 동기·오류 정정·가상 채널을 어떻게 할 것인가? | CCSDS TM/TC/AOS/USLP 프로파일 |
| 5. 네트워크 | 끊김과 경로 변화를 어떻게 흡수할 것인가? | IP/SDN 또는 DTN/BP 라우팅 정책 |
| 6. 애플리케이션 | 명령, 텔레메트리, 파일을 어떻게 표현할 것인가? | Space Packet, CFDP, MQTT/CoAP/LwM2M |
| 7. 플랫폼 | deadline과 인터럽트를 어떻게 보장할 것인가? | RTOS 태스크·HAL·드라이버 설계 |
| 8. 보안·품질 | 무엇을 신뢰하고 어떻게 증명할 것인가? | 위협 모델, 키 수명주기, MISRA/CWE/OSS 검증 |
| 9. 운용 | 장애를 어떻게 탐지·격리·복구하는가? | FDIR, failover, runbook, 관측성 |

## 기초 개념

### 계층과 캡슐화

물리 계층은 전자기파를 전달하고, 데이터 링크 계층은 한 링크에서 프레임을 전달하며, 네트워크 계층은 여러 노드를 거쳐 경로를 선택한다. 전송·응용 계층은 종단 간 신뢰성과 임무 의미를 다룬다. CCSDS Space Packet은 흔히 네트워크 계층처럼 설명되지만, 실제 임무에서는 패킷 식별·순서·다중화를 제공하는 우주용 패킷 형식으로 보고 IP 또는 BP와의 배치를 명시해야 혼동이 없다.

### 시간과 거리

빛의 속도는 진공에서 약 `299,792,458 m/s`다. 고도 600 km 위성의 직하점 단방향 전파 지연은 이상적으로 약 2 ms지만, 경사 거리·처리·큐잉·다중 홉을 포함하면 커진다. GEO 지상-위성 한 구간은 약 119 ms이고, 지상 단말 간 위성 왕복은 보통 그 몇 배가 된다. 달은 편도 약 1.3초, 화성은 위치에 따라 수 분에서 수십 분이다. 이 차이가 ARQ(Automatic Repeat reQuest, 자동 재전송 요구), TCP window, DTN 필요성을 바꾼다.

### 단위

- `dB`(decibel, 데시벨)는 비율의 로그 표현이고, `dBm`은 1 mW 기준 절대 전력이다.
- `Hz`(hertz, 헤르츠)는 초당 주기 수, `bps`(bits per second)는 초당 비트 수다.
- bandwidth(대역폭)는 문맥에 따라 주파수 폭 Hz 또는 데이터 처리율 bps를 뜻하므로 반드시 단위를 쓴다.
- latency(지연)는 한 방향 시간, RTT(Round-Trip Time, 왕복 시간)는 갔다 돌아오는 시간이다.

## 핵심 요약

1. Optical ISL(Optical Inter-Satellite Link, 광 위성간 링크)은 매우 높은 처리율·좁은 빔·주파수 희소성 완화가 강점이나 PAT(Pointing, Acquisition and Tracking, 지향·획득·추적), 열변형, 진동과 상호운용성이 난제다.
2. RF ISL(Radio-Frequency Inter-Satellite Link, 무선주파수 위성간 링크)은 획득과 운용이 상대적으로 관대하고 성숙했지만 스펙트럼·안테나 크기·간섭·처리율 제약이 크다. 둘은 경쟁재보다 보완재에 가깝다.
3. Space SDN(Software-Defined Networking, 소프트웨어 정의 네트워킹)은 제어와 전달을 논리적으로 분리하지만, 지상 SDN처럼 항상 중앙 제어기에 연결된다는 가정은 버려야 한다. 사전 계산 정책과 위성 자율 복구가 함께 필요하다.
4. CCSDS 계열은 우주 링크·패킷·파일 전달·지상국 상호운용을 위한 기본 어휘다. DTN/BPv7은 단절 구간을 저장 후 전달하며, CFDP는 파일 단위 전달을 맡는다.
5. MQTT(Message Queuing Telemetry Transport)는 broker 기반 publish/subscribe, CoAP(Constrained Application Protocol)는 작은 UDP(User Datagram Protocol, 사용자 데이터그램 프로토콜) 메시지 기반 REST(Representational State Transfer)다. 장시간 단절에서는 둘만으로 부족하며 엣지 broker/proxy 또는 DTN 결합이 필요하다.
6. LwM2M(Lightweight Machine to Machine, 경량 사물 간 통신)은 CoAP 위 장치 관리 객체 모델과 bootstrap을 제공한다. LoRaWAN은 LoRa 물리 변조 위의 저전력 광역망 MAC(Media Access Control, 매체 접근 제어)·네트워크 규약이다.
7. HAL(Hardware Abstraction Layer, 하드웨어 추상화 계층) 드라이버는 SPI(Serial Peripheral Interface), GPIO(General-Purpose Input/Output), reset, DIO(Digital Input/Output), IRQ(Interrupt Request)를 상태기계로 묶어야 한다. ISR(Interrupt Service Routine, 인터럽트 서비스 루틴)에서는 최소 작업만 하고 RTOS 태스크로 넘긴다.
8. MISRA(Motor Industry Software Reliability Association) 규칙 준수, CWE(Common Weakness Enumeration) 기반 약점 분류, OSS(Open-Source Software) 공급망 검증은 서로 대체하지 않는다. compiler warning, 정적 분석, 동적 분석, 구성 분석, SBOM(Software Bill of Materials, 소프트웨어 자재명세서)을 함께 쓴다.

## 상세 정리

아래 순서로 읽으면 개별 용어가 하나의 시스템으로 연결된다.

1. [시스템·궤도·네트워크 기초](chapters/01_system_foundations.md): bandwidth, RTT, topology, contact window, 군집위성, failover
2. [RF·FSO·ISL과 링크 버짓](chapters/02_rf_optical_link_budget.md): Optical/RF ISL, RSSI/SNR, EIRP, FSPL, G/T, Eb/N0, 링크 마진
3. [Space SDN·SD-WAN·동적 라우팅](chapters/03_space_networking.md): link state, handover, controller, 정책, 장애 복구
4. [CCSDS 패킷·데이터 링크·TT&C](chapters/04_ccsds_operations.md): Space Packet, TM, TC, AOS, USLP, SLE, SDLS, Telemetry
5. [DTN·CFDP·전송 신뢰성](chapters/05_dtn_reliability.md): Bundle Protocol, LTP, FEC, ARQ, segmentation, duplicate detection, buffering
6. [위성 IoT 프로토콜](chapters/06_iot_protocols.md): MQTT, CoAP CON/NON/Blockwise, LwM2M bootstrap, 6LoWPAN, LoRaWAN, D2C
7. [HAL·무선칩·RTOS](chapters/07_embedded_platform.md): SPI, GPIO, DIO, IRQ, SX1276/SX1262, VxWorks, FreeRTOS, Mbed OS
8. [IPsec·품질·보안 검증](chapters/08_security_quality.md): IPv6 strongSwan, MISRA, CWE, OSS 검증, 정적 분석
9. [현재 유망 기술과 미래 로드맵](chapters/09_future_roadmap.md): 표준 성숙도, 도입 우선순위, 2026~2035 전망
10. [출처와 판본](chapters/10_sources.md): 공식 자료, 표준 번호, 확인일

## 용어 정리

전체 약어를 영문 전체 이름·한국어·실무 의미와 함께 정리한 [통합 용어집](chapters/00_glossary.md)을 먼저 열어두는 것을 권장한다. 같은 약어도 문맥이 다를 수 있다. 예를 들어 `TC`는 Telecommand(원격명령), `TM`은 Telemetry(원격측정), `BP`는 Bundle Protocol(번들 프로토콜)이다.

## 실습 학습 가이드

[guide/README.md](guide/README.md)에서 실행 순서와 학습 질문을 확인한다.

- [01_foundations.ipynb](guide/01_foundations.ipynb): 단위, RTT, FSPL, Shannon capacity, 링크 버짓
- [02_practice.ipynb](guide/02_practice.ipynb): contact window, 시간변화 topology, failover, buffer 계산
- [03_advanced.ipynb](guide/03_advanced.ipynb): CoAP blockwise, sliding window, CRC, FEC/ARQ trade-off, DTN 우선순위 스케줄링

모든 실습은 외부 데이터나 원격 저장소 없이 Python 표준 라이브러리만으로 실행되며, 결과는 교육용 toy model이다. 실제 궤도·채널·하드웨어 인증 결과를 대체하지 않는다.

## 실무 산출물

[실무 산출물 패키지](deliverables/README.md)는 학습 내용을 설계·시험 업무로 전환한다. 대화형 [네트워크 아키텍처](deliverables/architecture/network-architecture.html), [ICD](deliverables/templates/ICD.md), 수식 기반 [링크 버짓](deliverables/results/link-budget.xlsx), [성능 모델](deliverables/templates/performance-model.md), [시뮬레이터](deliverables/tools/satellite_network_sim.py), [CCSDS 패킷 분석기](deliverables/tools/ccsds_packet_analyzer.py), [시험 절차](deliverables/templates/test-procedure.md), [검증 보고서](deliverables/templates/verification-report.md), [절충 분석](deliverables/templates/trade-off-report.md), [요구사항 추적 매트릭스](deliverables/results/requirements-traceability.xlsx)를 포함한다.

모든 산출물은 공통 ID로 요구사항-설계-인터페이스-시험-결과를 연결한다. 포함된 수치와 판정은 교육용 기준선이므로 실제 임무에서는 승인된 궤도·부품·환경·규제 데이터로 교체해야 한다.

## 현재와 미래의 유망 기술

2026년 현재 특히 주목할 축은 다음과 같다.

- **상호운용 가능한 광 메쉬**: 고속 OISL 자체보다 서로 다른 제조사의 광 단말이 링크를 획득하고 네트워크에 참여하는 표준화가 상용화의 관건이다.
- **시간변화 네트워킹**: 접속 계획을 라우팅 입력으로 쓰는 Schedule-Aware Bundle Routing과 IETF TVR(Time-Variant Routing, 시간변화 라우팅) 계열의 사고방식이 중요하다.
- **5G NTN과 D2D/D2C**: 3GPP Release 17 이후 NB-IoT(Narrowband Internet of Things)·eMTC(enhanced Machine-Type Communication)·NR(New Radio)이 위성 지연과 Doppler를 수용한다. 사업성은 스펙트럼·단말 전력·국가별 허가에 좌우된다.
- **온보드 자율 네트워크**: 링크 상태 예측, 정책 기반 routing, 압축·우선순위·엣지 추론을 위성에서 수행해 지상 왕복 의존성을 줄인다.
- **암호 민첩성과 계층별 보안**: SDLS, BPSec, IPsec의 보호 범위를 구분하고 장기 임무의 키 갱신 및 post-quantum 전환 가능성을 설계한다.
- **안전한 오픈소스 RTOS 생태계**: Mbed OS는 2026년 7월 Arm 지원이 종료되었으므로 신규 설계의 기본 선택으로 두기 어렵다. FreeRTOS, Zephyr, 상용 안전 인증 RTOS를 인증 목표와 공급망 수명에 맞춰 비교해야 한다.

세부 근거와 과장 가능성은 [현재·미래 로드맵](chapters/09_future_roadmap.md)에 기술했다.

## 다음 학습 경로

1. 실습 1에서 링크 버짓과 bandwidth-delay product를 직접 계산한다.
2. CCSDS Space Packet과 TM/TC/AOS/USLP의 경계를 그려 본다.
3. 실습 2에서 contact plan과 failover 정책을 구현한다.
4. SX1262 데이터시트를 보며 HAL 상태기계와 IRQ 처리 코드를 설계한다.
5. 실습 3에서 CRC·ARQ·FEC·blockwise·DTN 우선순위의 상호작용을 비교한다.
6. 가상의 12기 LEO 임무에 대해 요구사항, 링크 버짓, 데이터 흐름, 위협 모델, 검증 계획을 작성한다.

전문가 수준의 기준은 용어 암기가 아니라, 요구사항을 수치로 바꾸고 계층 간 중복·빈틈을 찾아내며, 장애와 보안 사건에서도 왜 설계가 유지되는지 증명할 수 있는가이다.
