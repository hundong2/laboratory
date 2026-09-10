# 09. 현재 유망 기술과 미래 로드맵

## 1. 평가 방법

`유망`은 성능이 높은 것과 같지 않다. 다음 다섯 축으로 평가한다.

1. **mission value**: latency, coverage, autonomy, data volume을 얼마나 개선하는가
2. **technical readiness**: lab demo, on-orbit demo, interoperable operation 중 어디까지 왔는가
3. **ecosystem**: multi-vendor component, standard, ground support, toolchain이 있는가
4. **integration cost/risk**: SWaP-C, thermal, pointing, certification, regulation
5. **option value**: 지금 interface를 준비하면 future component로 교체하기 쉬운가

## 2. 2026년 현재 우선순위

| 등급 | 기술 | 판단 | 지금 할 일 |
|---|---|---|---|
| A | RF + optical hybrid ISL | 고속 optical과 resilient RF의 상호 보완 | terminal abstraction, path policy, dual-link test |
| A | DTN BPv7 + contact-aware routing | 단절·달 네트워크의 핵심 | BPv7/BPSec profile, persistent store 시험 |
| A | onboard buffering·priority·compression | 모든 제한 link에서 즉시 가치 | deadline-aware scheduler와 storage fault test |
| A | CCSDS interoperability + SLE | ground cross-support의 기반 | active issue 고정, golden frame, provider test |
| A | 5G NTN IoT | 표준 chipset 생태계가 형성 | Doppler/timing/power/regulation field trial |
| A | secure update + SBOM + static analysis | 긴 수명 software risk의 전제 | signed build, provenance, multi-analyzer CI |
| B | Space SDN hierarchical control | constellation 자동화에 중요 | local autonomy와 policy version부터 구현 |
| B | SD-WAN over satellite | hybrid underlay enterprise에 유효 | application SLA와 MTU/long RTT profile |
| B | LwM2M over constrained satellite IoT | device fleet management에 유효 | bootstrap recovery와 block/file update 검증 |
| C | end-to-end post-quantum transition | 장기 confidentiality에 중요하나 통합 성숙도 관찰 | crypto agility, memory/handshake benchmark |

등급은 범용 우선순위이며 특정 임무에서는 바뀐다.

## 3. Optical ISL의 현재와 미래

SDA의 PWSA(Proliferated Warfighter Space Architecture)는 optical inter-satellite mesh를 transport backbone으로 설계하고 OCT(Optical Communications Terminal) 상호운용 표준을 공개한다. ESA HydRON은 terrestrial optical network와 연결되는 all-optical space network를 추진하며 2027년 첫 LEO optical segment 계획을 제시한다.

현재 병목은 peak Gbit/s 수치보다 다음이다.

- vendor 간 acquisition/waveform/network interoperability
- PAT acquisition time과 terminal handover
- optical terminal 수 대비 simultaneous link scheduling
- thermal/jitter calibration과 on-orbit alignment
- optical ground station의 cloud diversity
- encryption, keying, management-plane interoperability

2026~2030에는 optical crosslink가 high-capacity constellation의 표준 선택으로 확대될 가능성이 높다. 2030 이후에는 multi-orbit optical relay, terabit-class aggregation, space-ground optical transport integration이 유망하지만 schedule은 launch, terminal yield, ground weather diversity에 민감하다.

## 4. RF의 미래

RF는 사라지지 않는다. electronically scanned array, digital beamforming, RFSoC(Radio-Frequency System-on-Chip), regenerative payload, flexible channelization, higher-frequency Ka/Q/V band가 capacity를 늘린다. safe-mode, mobile/D2D access, cloud-obstructed ground link에서 optical의 backup이 된다.

유망 포인트:

- multi-band software-defined payload
- spectrum sensing과 interference geolocation
- beam hopping과 demand-aware allocation
- onboard RF Doppler/timing correction
- optical backbone + RF access 통합

위험은 spectrum coordination, power amplifier efficiency, thermal dissipation, supply-chain/export control이다.

## 5. 5G NTN과 D2C/D2D

3GPP Release 17의 NR-NTN과 IoT-NTN은 satellite delay, Doppler, moving cell, timing을 cellular ecosystem에 끌어들였다. ITU-R M.2177-0(2026)은 5G-NTN satellite radio interface를 IMT-2020 구성으로 정리한다.

### 현재 유망 순서

1. emergency text/SOS와 sparse messaging
2. NB-IoT/eMTC 기반 asset telemetry
3. voice와 low-rate data
4. broader smartphone data service

일반 handset direct connection은 거대한 space antenna, terrestrial spectrum coexistence, national authorization, handset power, beam capacity가 모두 맞아야 한다. 기술 demo와 nationwide profitable service를 구분해야 한다.

2027 WRC(World Radiocommunication Conference) agenda와 국가별 supplemental coverage rule이 시장 속도를 좌우한다. 6G에서는 terrestrial과 NTN을 별도 network가 아닌 통합 access로 설계하는 방향이 강하다.

## 6. DTN과 lunar internet

NASA LunaNet은 lunar communication/navigation framework의 핵심 network technology로 DTN을 제시한다. 달 남극 relay가 늘면 scheduled contact, multi-provider interoperability, onboard routing과 time service가 필요하다.

가까운 미래 과제:

- RFC 9171 BPv7과 CCSDS experimental profile의 정합
- BPSec interoperable security context와 key management
- schedule-aware routing의 plan exchange format
- custody transfer와 compressed status reporting
- application streaming과 deadline traffic의 DTN coexistence
- Earth-independent time/navigation과 network management

DTN은 `느린 인터넷`이 아니라 다른 availability model이다. interactive traffic은 가능한 continuous IP path를 사용하고, delivery-critical asynchronous data는 BP로 보내는 dual stack이 현실적이다.

## 7. Space SDN과 autonomous operations

군집 수백 기를 사람의 command sequence만으로 운영하기 어렵다. 앞으로 controller는 orbit/contact, energy, thermal, queue, threat를 함께 최적화한다. 그러나 autonomy level을 단계적으로 올린다.

- L1: ground plan을 onboard에서 실행
- L2: threshold 기반 local failover
- L3: constraint 안에서 local route/resource 재계산
- L4: constellation cooperative optimization
- L5: mission goal 기반 자율 planning, 아직 높은 assurance 과제

유망 기술은 digital twin에서 policy를 검증하고, signed intent와 bounded optimizer를 배포하며, onboard telemetry로 drift를 감지하는 closed loop다. ML(Machine Learning, 기계학습)은 anomaly score와 traffic prediction에 유용하지만 deterministic guard와 rule-based safe fallback을 둔다.

## 8. embedded platform의 변화

Mbed OS Arm 지원 종료는 `feature-rich IoT platform`보다 maintainable component architecture와 open governance가 중요함을 보여준다. FreeRTOS는 작은 kernel과 넓은 MCU ecosystem, Zephyr는 device tree·driver·network·governance, VxWorks 등 commercial RTOS는 certification evidence와 support가 강점이다.

향후 핵심:

- Rust 등 memory-safe language를 non-critical component부터 도입
- time/space partition과 mixed-criticality
- RISC-V ecosystem과 radiation-tolerant implementation
- hardware root of trust, measured boot, remote attestation
- deterministic Ethernet/TSN(Time-Sensitive Networking) onboard network
- container보다 더 작은 partition/sandbox for onboard applications

새 language가 MISRA, WCET, qualified toolchain, FFI(Foreign Function Interface), radiation behavior를 자동 해결하지는 않는다.

## 9. security의 변화

- **crypto agility**: algorithm ID만 바꾸는 것이 아니라 key size, message size, hardware acceleration, update path를 수용
- **zero trust**: network location보다 workload/device identity와 least privilege
- **supply-chain security**: SBOM, signed provenance, reproducible build, dependency pinning
- **post-quantum preparation**: harvest-now-decrypt-later 가치가 큰 장기 secret부터 hybrid trial
- **cross-layer incident response**: RF anomaly, auth failure, route change, firmware measurement를 함께 분석

post-quantum algorithm을 즉시 모든 low-power link에 넣기보다 mission lifetime과 data secrecy horizon을 기준으로 우선순위를 정한다.

## 10. 2026~2035 학습·구축 로드맵

### 0~6개월: 기반

- link budget와 contact simulation 자동화
- CCSDS packet/frame golden vector
- SX1262 HAL driver state machine + fault injection
- FreeRTOS queue/notification/priority analysis
- OSS inventory, SBOM, clang-tidy/Cppcheck baseline

### 6~18개월: 통합

- RF/optical path abstraction과 failover lab
- BPv7 store-forward와 BPSec key lifecycle
- CFDP Class 1/2 contact interruption test
- CoAP/LwM2M bootstrap over constrained link
- IPv6 strongSwan XFRM tunnel과 MTU/roaming test

### 18~36개월: constellation

- time-expanded contact graph routing
- hierarchical Space SDN controller
- network digital twin과 hardware-in-the-loop
- multi-ground SLE interoperability
- 5G IoT-NTN field terminal comparison

### 3~9년: advanced

- multi-vendor optical mesh
- multi-orbit route/resource orchestration
- bounded onboard autonomy
- post-quantum/hybrid key establishment where justified
- lunar/space internetwork cross-provider service

## 11. 최종 시스템 설계 checklist

### Mission

- data class별 volume, deadline, loss tolerance, security class가 수치인가?
- safe mode에서 필요한 최소 link와 command set은 무엇인가?

### Link

- worst-case link budget와 measurement uncertainty가 있는가?
- RF/optical acquisition, Doppler, weather, pointing failure를 시험했는가?

### Network

- contact plan version, time sync, stale state behavior가 정의됐는가?
- controller 없이 유지 가능한 local policy와 복구 경로가 있는가?

### Data

- segmentation, FEC, ARQ, duplicate detection 책임이 계층별 한 번씩인가?
- buffer overflow 시 무엇을 어떤 근거로 버리는가?

### Security

- SDLS/BPSec/IPsec/application security의 trust boundary가 그려졌는가?
- reset, key rollover, clock rollback, replay를 함께 시험했는가?

### Software

- ISR deadline, stack, heap, priority inversion의 bound가 있는가?
- MISRA deviation과 CWE mapping, OSS provenance가 review 가능한가?

### Operations

- failover를 실제로 정기 실행하고 failback까지 검증하는가?
- telemetry가 탐지뿐 아니라 원인 격리와 책임 추적에 충분한가?

[← 이전](08_security_quality.md) · [메인](../README.md) · [출처 →](10_sources.md)
