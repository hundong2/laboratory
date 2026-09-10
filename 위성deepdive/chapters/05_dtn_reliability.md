# 05. DTN·CFDP·전송 신뢰성

## 1. DTN이 왜 생겼는가

인터넷 transport는 대체로 end-to-end path가 존재하고 RTT가 timeout보다 짧다는 전제를 암묵적으로 가진다. 우주망은 행성 차폐, 궤도, 지상국 일정, 긴 light time 때문에 path가 수 분·수 시간 끊길 수 있다. TCP는 이를 congestion으로 오인하고 반복 backoff한다.

**DTN (Delay/Disruption Tolerant Networking, 지연·단절 내성 네트워킹)**은 application message를 bundle로 만들고 각 node의 persistent storage에 보관한 뒤 다음 contact에서 전달하는 overlay architecture다. 핵심은 `end-to-end 연결을 기다리지 않고 hop마다 책임 있게 보관`하는 것이다.

## 2. store-and-forward

**store-and-forward(저장 후 전달)**에서는 수신 node가 완전한 data unit을 non-volatile storage에 저장하고 적절한 outbound contact를 기다린다.

장점:

- 예정된 단절을 오류로 취급하지 않는다.
- 서로 다른 link와 rate를 연결한다.
- 여러 future route 중 선택할 수 있다.

비용:

- storage 용량·wear·radiation upset 관리
- custody와 삭제 시점의 정확성
- stale/expired data 정리
- compromise node에 평문이 오래 머무는 보안 위험

## 3. Bundle Protocol Version 7

**BPv7 (Bundle Protocol Version 7, 번들 프로토콜 버전 7)**은 RFC 9171 표준이다. bundle은 primary block과 payload 및 extension block들로 구성된다.

- **Endpoint ID**: `dtn:` 또는 `ipn:` scheme 등 logical endpoint
- **creation timestamp/sequence**: 식별과 lifetime 계산
- **lifetime**: 만료 후 전달 가치가 없는 bundle 폐기 기준
- **fragment**: 필요 시 bundle 단위 fragmentation
- **CRC**: block 손상 탐지 선택
- **extension blocks**: previous node, hop count, bundle age, security 등

`delivery`는 application이 수신했음을 뜻할 수 있지만, hop storage 수락과 혼동하면 안 된다. status report는 유용하지만 report storm과 reverse-path resource를 고려한다.

### BPSec

**BPSec (Bundle Protocol Security, 번들 프로토콜 보안)**은 RFC 9172다.

- **BIB (Block Integrity Block, 블록 무결성 블록)**: 대상 block의 integrity와 source authentication
- **BCB (Block Confidentiality Block, 블록 기밀성 블록)**: 대상 block encryption

BPSec은 bundle이 여러 untrusted relay에 저장될 때 end-to-end 또는 security-source-to-security-destination 보호를 제공한다. metadata traffic analysis, key distribution, replay/expiry policy는 별도 설계가 필요하다.

## 4. contact plan과 SABR

**contact plan**은 `(from, to, start, end, rate, range/confidence)` records다. **SABR (Schedule-Aware Bundle Routing, 일정 인지 번들 라우팅)**은 CCSDS 734.3-B-1로, 안정적인 node topology와 시간변화 scheduled connectivity에서 route를 계산한다.

Contact Graph Routing 계열은 현재 node에서 destination까지의 earliest-arrival path를 contact graph에서 찾는다. contact capacity는 이미 예약된 traffic을 빼야 한다. 오래된 plan, execution drift, unplanned outage에는 local rerouting과 plan versioning이 필요하다.

## 5. LTP

**LTP (Licklider Transmission Protocol, 릭라이더 전송 프로토콜)**는 긴 RTT와 link interruption을 고려한 point-to-point convergence-layer protocol이다. TCP처럼 continuous full-duplex connection을 요구하지 않는다.

- **red data**: reliable delivery가 필요한 부분, checkpoint와 report/retransmission 사용
- **green data**: reliability를 요구하지 않는 부분
- **session**: block 전송 단위

BP는 여러 hop의 bundle forwarding, LTP는 한 scheduled hop에서 reliable convergence를 맡는다. 따라서 경쟁 관계가 아니라 `BP over LTP`로 결합할 수 있다. LTP timer는 one-way light time과 contact interruption을 인지해야 한다.

## 6. CFDP

**CFDP (CCSDS File Delivery Protocol, CCSDS 파일 전달 프로토콜)**는 file과 metadata를 전달하는 표준이다. file 생성·삭제·rename 같은 filestore request도 profile에 따라 다룬다.

- **Class 1**: unacknowledged, receiver의 재전송 feedback 없이 전송
- **Class 2**: acknowledged, missing data와 metadata를 NAK(Negative Acknowledgment)로 복구
- **PDU**: metadata, file data, EOF(End of File), Finished, ACK, NAK 등
- **transaction ID**: source entity ID와 sequence number로 transaction 식별
- **checksum**: 완전성 확인; cryptographic integrity와 같지 않음

큰 file을 Space Packet 하나에 넣지 않고 CFDP가 segment하여 file data PDU로 보낸다. CFDP over BP 또는 store-and-forward overlay는 mission profile과 구현 판본을 확인해야 한다.

### fault handler

inactivity, checksum failure, file size error, cancel, suspend에 대한 action을 `ignore`, `notice`, `cancel`, `suspend` 등으로 profile화한다. Class 2가 언제나 낫지는 않다. return link가 매우 비싸거나 contact가 단방향이면 strong FEC와 재전송 없는 Class 1이 합리적일 수 있다.

## 7. FEC와 ARQ

### FEC

송신 시 redundancy를 추가해 receiver가 error를 자체 복구한다. 추가 bandwidth/compute를 쓰지만 RTT를 기다리지 않는다. deep-space와 broadcast에 유리하다.

### ARQ

receiver가 loss/corruption을 알리고 sender가 다시 보낸다. channel이 좋을 때 효율적이나 long RTT에서 latency와 buffer가 커진다.

### Hybrid ARQ

**HARQ (Hybrid Automatic Repeat reQuest, 혼합 자동 재전송 요구)**는 FEC와 retransmission을 결합하고 soft information을 누적할 수 있다. terrestrial cellular에 강력하지만 매우 긴 RTT와 짧은 contact에서는 process count·memory·timer가 부담이다.

선택은 평균 BER이 아니라 burst error, feedback availability, deadline, energy, contact capacity로 한다.

## 8. packet segmentation과 reassembly

**segmentation(분할)**은 큰 service data unit을 MTU 이하 unit으로 나눈다. 계층마다 fragmentation을 중복하면 header와 loss amplification이 커진다.

예: payload 4,096 bytes를 256-byte fragment 16개로 나눌 때 fragment 성공률이 0.99라면 재전송 없이 전체가 성공할 확률은 `0.99^16 ≈ 0.851`이다. 작은 fragment는 error cost를 낮추지만 header·ACK 수를 늘린다.

receiver는 transaction ID, offset, total length, bitmap, timeout을 관리한다. offset+length overflow, overlapping segment, duplicate, inconsistent total length를 방어해야 한다.

## 9. duplicate detection

재전송과 route replication은 duplicate를 만든다. `exactly once`는 저장·실행 결과까지 포함하면 어렵고 비용이 크다. 보통 at-least-once delivery와 idempotent operation을 결합한다.

- sequence number + source/epoch
- sliding receive window와 bitmap
- transaction ID cache + expiry
- reboot 후 monotonic counter 보존
- command는 semantic idempotency key와 execution journal

Bloom filter는 memory를 줄이지만 false positive로 정상 data를 버릴 수 있어 critical command에는 부적절할 수 있다.

## 10. onboard buffering, compression, prioritization

### buffer sizing

```text
required storage >= production_rate × maximum_expected_outage
                 + retransmission reserve
                 + filesystem/journal overhead
                 + uncertainty margin
```

평균 생성률만 쓰지 말고 burst, contact miss correlation, compression worst-case를 본다. lossless compression은 data에 따라 원본보다 커질 수도 있으므로 expansion bound를 둔다.

### compression

- lossless: science raw, command log, audit에 필요
- lossy: image/video에서 mission value와 downstream algorithm 영향 검증
- delta/dictionary: housekeeping처럼 천천히 변하는 signal에 효율적
- compress-then-encrypt: 일반적으로 암호화 후에는 압축이 거의 안 됨; secret과 attacker-controlled data를 함께 압축하면 side channel 주의

### prioritization

priority만으로 부족하다. deadline, size, destination, custody, expiry, retransmission cost를 함께 scheduling한다.

```text
score = criticality_weight + urgency(deadline)
      + age_bonus - size_penalty - route_risk
```

critical queue에 reserved capacity를 두고, 낮은 priority에는 aging을 적용한다. `drop-tail`은 큰 file 조각이 buffer를 선점할 수 있어 per-class quota와 admission control이 필요하다.

## 11. network window size와 max payload size

**window size**는 ACK 없이 보낼 수 있는 data 또는 sequence 범위다. 필요한 최소 window는 대략 BDP를 segment size로 나눈 값이다.

```text
window_segments >= ceil(bitrate × RTT / segment_payload_bits)
```

memory 제한, sequence number 공간, receiver reordering, contact remaining capacity가 상한을 만든다. max payload는 physical frame maximum이 아니라 모든 header, security tag, FEC/link encapsulation, MTU와 fragmentation policy를 빼 계산한다.

```text
app_payload_max = path_MTU
                - network/transport headers
                - security overhead
                - adaptation/fragment headers
```

IPsec tunnel, IPv6, UDP, CoAP, block option을 쌓으면 작은 RF frame에서 overhead 비율이 매우 커질 수 있다.

## 12. CRC

**CRC (Cyclic Redundancy Check, 순환 중복 검사)**는 bit string을 생성다항식(generator polynomial)으로 나눈 나머지를 frame/block 뒤에 붙이는 오류 탐지 code다. receiver가 같은 나눗셈을 수행해 나머지를 검사한다. CRC-n은 보통 n-bit 나머지를 만든다.

### 직관

송신 data polynomial을 `M(x)`, generator를 `G(x)`라 하면 `M(x)` 뒤에 `degree(G)`개의 0을 붙이고 modulo-2 division, 즉 carry 없는 XOR division을 수행한다. 나머지 `R(x)`를 붙인 codeword는 `G(x)`로 나누어떨어진다.

```text
T(x) = M(x) · x^n + R(x)
T(x) mod G(x) = 0
```

CRC parameter는 polynomial만이 아니다. width, initial value, input/output reflection, final XOR와 byte order가 모두 같아야 한다. `CRC-16`이라는 이름만으로 interoperability가 보장되지 않으므로 정확한 profile과 known-answer vector를 ICD에 기록한다.

CRC는 random/burst error 탐지에는 강하지만 cryptographic authentication이 아니다. 공격자는 내용을 바꾸고 CRC를 다시 계산할 수 있다. malicious tampering에는 MAC(Message Authentication Code, 메시지 인증 코드), AEAD 또는 digital signature가 필요하다.

### 어느 계층의 CRC인가

physical/data-link frame CRC, Space Packet/Bundle block CRC, file checksum이 중첩될 수 있다. 각 검사는 서로 다른 fault boundary를 탐지한다. 이미 authenticated encryption tag가 있는 구간에서는 CRC가 빠른 corruption rejection 또는 legacy framing을 위해 남을 수 있으나, overhead와 error reporting 의미를 문서화한다.

## 13. 검증 시나리오

- contact가 PDU 중간에 종료된 뒤 다음 contact에서 재개
- custody 수락 직후 sender/receiver reboot
- bundle/CFDP transaction ID wrap 또는 persistent counter 손상
- duplicate command가 서로 다른 route로 도착
- buffer 95%, 100%, filesystem read-only
- contact plan version mismatch와 clock jump
- FEC가 고치지 못한 error를 CRC/checksum/security tag가 탐지
- 높은 priority flood 중 low priority aging과 critical admission 보장

[← 이전](04_ccsds_operations.md) · [메인](../README.md) · [다음: 위성 IoT →](06_iot_protocols.md)
