# 08. IPsec·MISRA·CWE·OSS·정적 분석

## 1. security engineering 원칙

보안 기능을 protocol 이름으로 시작하지 말고 asset, adversary, trust boundary, failure impact에서 시작한다.

- asset: command authority, key, payload data, orbit/position, firmware
- threat: spoofing, replay, tampering, eavesdropping, jamming, supply-chain compromise, denial of service
- boundary: spacecraft processor, radio, ground modem, provider network, mission cloud
- property: confidentiality, integrity, authenticity, availability, freshness, accountability

RF anti-jam과 cryptographic security는 다르다. encryption은 noise/jamming을 막지 않고 FEC는 malicious modification을 인증하지 않는다.

## 2. IPsec

**IPsec (Internet Protocol Security, 인터넷 프로토콜 보안)**은 IP layer에서 traffic을 보호하는 architecture다.

- **ESP (Encapsulating Security Payload, 캡슐화 보안 페이로드)**: confidentiality, integrity/authentication, anti-replay
- **AH (Authentication Header, 인증 헤더)**: integrity/authentication; NAT(Network Address Translation)과 제약 때문에 ESP가 일반적
- **SA (Security Association, 보안 연관)**: 단방향 cryptographic state, algorithm, key, SPI(Security Parameters Index), lifetime
- **SPD (Security Policy Database, 보안 정책 데이터베이스)**: 어떤 traffic을 protect/bypass/discard할지 결정
- **SAD (Security Association Database, 보안 연관 데이터베이스)**: active SA state
- **IKEv2 (Internet Key Exchange version 2, 인터넷 키 교환 버전 2)**: peer authentication과 CHILD_SA key negotiation

### transport와 tunnel mode

- **transport mode**: original IP header는 남기고 upper-layer payload 보호. host-to-host.
- **tunnel mode**: original IP packet 전체를 새 outer IP packet 안에 넣음. gateway VPN.

IPsec은 IPv6에서 사용할 수 있지만 `IPv6이면 항상 IPsec이 켜진다`는 것은 틀리다. 별도 policy, IKE/authentication, key와 firewall 구성이 필요하다.

## 3. IPv6 IPsec VPN with strongSwan

**VPN (Virtual Private Network, 가상 사설망)**은 shared/untrusted network 위에 authenticated encrypted logical network를 만든다. **strongSwan**은 IKEv1/IKEv2와 IPsec을 구현한 open-source software다. 2026년 현재 6.0 계열 문서를 기준으로 `swanctl.conf`와 VICI(Versatile IKE Configuration Interface) 계열 관리가 일반적이다.

### site-to-site IPv6 예시

다음은 구조 학습용이다. 실제 address, certificate path, algorithm policy와 firewall을 환경에 맞게 바꾼다.

```conf
connections {
  sat-ground-v6 {
    version = 2
    proposals = aes256gcm16-prfsha384-ecp384
    reauth_time = 0s
    rekey_time = 4h
    mobike = yes

    local_addrs = 2001:db8:10::1
    remote_addrs = 2001:db8:20::1

    local {
      auth = pubkey
      certs = ground-cert.pem
      id = ground.example
    }
    remote {
      auth = pubkey
      id = sat-gateway.example
    }

    children {
      mission-v6 {
        local_ts = 2001:db8:100::/48
        remote_ts = 2001:db8:200::/48
        esp_proposals = aes256gcm16-ecp384
        start_action = trap
        dpd_action = restart
      }
    }
  }
}
```

`2001:db8::/32`는 documentation prefix이므로 실제 deployment에 쓰지 않는다.

### packet 흐름

1. outbound packet이 SPD policy/traffic selector와 match
2. IKE_SA가 peer를 certificate로 인증
3. CHILD_SA가 ESP key와 algorithm을 협상
4. kernel XFRM(transform) framework가 packet encrypt/authenticate
5. receiver가 anti-replay 확인, decrypt, inner IPv6 route

### XFRM interface

route-based VPN은 Linux XFRM interface로 route와 IPsec SA를 연결할 수 있다. policy-based tunnel보다 multi-tenant routing, observability, MTU 설정이 쉬울 수 있다. strongSwan 문서상 XFRM interface는 Linux kernel 4.19+, iproute2 5.1.0+에서 지원된다.

```bash
ip link add ipsec0 type xfrm if_id 42
ip link set ipsec0 up
ip -6 route add 2001:db8:200::/48 dev ipsec0
```

configuration의 `if_id_in/out = 42`와 맞춘다. loop route와 IKE/ESP 자체 traffic이 tunnel로 다시 들어가는 것을 막는다.

### IPv6 특유 체크

- ICMPv6(Internet Control Message Protocol for IPv6)를 무조건 차단하면 Neighbor Discovery와 PMTUD(Path MTU Discovery)가 망가진다.
- ESP overhead로 inner MTU가 감소한다. fragmentation 전에 MSS/MTU와 application block size를 조정한다.
- link-local address scope ID, router advertisement, forwarding sysctl을 확인한다.
- NAT가 없어도 firewall state와 UDP 500/4500, ESP protocol 50이 필요하다.
- satellite handover에는 MOBIKE(Mobility and Multihoming extension for IKEv2)가 address/path 변경을 도울 수 있지만 long outage 동안 SA lifetime과 DPD(Dead Peer Detection) timeout을 조정해야 한다.

### algorithm과 key

AEAD(Authenticated Encryption with Associated Data, 연관 데이터 포함 인증 암호)인 AES-GCM을 우선 고려하고 weak/deprecated algorithm을 명시적으로 배제한다. certificate identity는 subjectAltName과 일치시킨다. PSK(Pre-Shared Key)는 fleet scale에서 rotation과 compromise blast radius가 커질 수 있다.

긴 우주 임무에는 cryptographic agility, onboard secure storage, signed time-independent recovery command, key rollover overlap을 설계한다. strongSwan 6.0은 ML-KEM(Module-Lattice-Based Key-Encapsulation Mechanism) 관련 IKEv2 예시를 제공하지만, flight adoption은 interoperability·resource·certification을 별도 검증해야 한다.

## 4. SDLS, BPSec, IPsec을 어디에 쓰나

| 보호 계층 | 장점 | 보호 경계 | 주의점 |
|---|---|---|---|
| SDLS | CCSDS frame과 TC/TM에 직접 결합 | space link | gateway 이후 end-to-end 아님 |
| BPSec | bundle block가 relay storage를 지나도 보호 | BP security endpoints | key와 canonicalization, metadata |
| IPsec | 일반 IP application 투명 보호 | IP hosts/gateways | tunnel overhead, disruption/IKE |
| TLS/DTLS/OSCORE | application/transport 친화 | connection 또는 object endpoint | proxy와 long disruption |

중첩은 trust boundary가 실제로 다를 때만 한다. 각 계층 sequence/replay state가 reboot 후 어떻게 회복되는지 함께 시험한다.

## 5. MISRA

**MISRA (Motor Industry Software Reliability Association)**는 safety/security-related embedded software의 예측 가능성과 analyzability를 높이는 coding guideline을 발행한다. 자동차에서 시작했지만 aerospace embedded C/C++에도 널리 참고된다.

- **MISRA C**: C language guideline. 2023 edition은 C11/C18을 포함하는 최신 세대.
- **MISRA C++**: C++ guideline. 프로젝트의 language version과 edition을 맞춘다.
- **Directive**: process/design 판단과 evidence가 필요한 지침.
- **Rule**: source code에서 더 직접 검증 가능한 규칙.
- **mandatory/required/advisory**: 준수 강도 분류.

MISRA compliance는 warning 0과 같지 않다. 적용 범위, guideline 판본, deviation procedure, tool qualification/confidence, compiler configuration, generated code를 문서화한다.

### deviation

규칙을 어길 정당한 기술 이유가 있으면 무시 주석 하나로 끝내지 않는다.

```text
rule -> exact location -> rationale -> risk analysis
 -> compensating control -> reviewer/approval -> expiry/revisit
```

## 6. CWE

**CWE (Common Weakness Enumeration, 공통 약점 열거)**는 software/hardware weakness 유형의 분류 체계다. CVE(Common Vulnerabilities and Exposures)가 특정 제품의 공개 vulnerability instance라면 CWE는 root cause category다.

위성 embedded C에서 중요한 예:

- CWE-119/787: memory buffer bounds, out-of-bounds write
- CWE-125: out-of-bounds read
- CWE-190: integer overflow/wraparound
- CWE-416: use after free
- CWE-362: race condition
- CWE-400: uncontrolled resource consumption
- CWE-798: hard-coded credential
- CWE-20: improper input validation

2025 CWE Top 25는 39,080 CVE record dataset을 바탕으로 common/impactful weakness를 정리했다. 그러나 flight software risk ranking은 attack surface, command privilege, recoverability를 반영해 mission-specific으로 다시 해야 한다.

## 7. OSS 검증

**OSS (Open-Source Software, 오픈소스 소프트웨어) 검증**은 license scan 하나가 아니다.

### inventory와 provenance

- direct/transitive dependency, version, source URL, commit hash
- SBOM in SPDX(Software Package Data Exchange) 또는 CycloneDX
- source archive와 build toolchain의 immutable digest
- patch와 local modification
- maintainer/release/signature provenance

### license

- license expression과 notice/source obligation
- static/dynamic linking, firmware distribution 해석
- dual-license와 generated artifact
- legal review 기록

### security와 maintenance

- CVE/OSV(Open Source Vulnerabilities) mapping
- EOL, release cadence, maintainer bus factor
- malicious package/typosquat 방어
- reproducible build와 signed artifact
- vulnerability disclosure, patch SLA
- offline mission에서 patch 불가 시 compensating control

### quality

- target compiler/architecture build
- unit/integration/fuzz test
- static/dynamic analysis
- code coverage와 undefined behavior sanitizer
- fault injection, memory/time bound
- requirement traceability와 local change review

SCA(Software Composition Analysis, 소프트웨어 구성 분석)는 dependency 취약점과 license를 찾지만 source-level logic defect를 찾는 SAST(Static Application Security Testing)와 다르다.

## 8. 정적 분석 오픈소스 도구

| 도구 | 초점 | 강점 | 한계/주의 |
|---|---|---|---|
| compiler warnings | type, flow, undefined construct | build에 항상 적용, 빠름 | interprocedural depth 제한 |
| Clang Static Analyzer | C/C++/Obj-C path-sensitive bug | null, leak, lifecycle path | build DB와 모델 품질 필요 |
| clang-tidy | bugprone, CERT, portability, style | compile_commands, fix-it | rule selection/tuning 필요 |
| Cppcheck | C/C++ 독립 분석 | 쉬운 도입, unique checks | compile environment modeling 확인 |
| GCC `-fanalyzer` | C 중심 path analysis | compiler 통합 | version별 diagnostic 변화 |
| CodeQL | code as database/query, data flow | custom query, variant analysis | CLI license/use 조건과 build 비용 확인 |
| Semgrep CE | pattern/dataflow rule | custom secure coding rule 빠름 | deep C/C++ semantic coverage 제한 가능 |
| Frama-C | C abstract interpretation/formal plugin | proof-oriented analysis | annotation/model expertise 필요 |
| Infer | interprocedural separation logic 계열 | memory/concurrency defect | target/build support 확인 |
| CodeChecker | Clang analyzer 결과 관리 | CI, baseline, web review | analyzer 자체가 아니라 orchestration |

`오픈소스`와 `무료 사용 가능`, `규칙 전체가 공개`, `상용 코드 분석 허용`은 같지 않다. 각 version license를 확인한다.

### 최소 pipeline

```text
compile -Wall -Wextra -Wconversion -Werror(profiled)
 -> clang-tidy + Cppcheck
 -> Clang Static Analyzer or GCC -fanalyzer
 -> dependency/SBOM/vulnerability scan
 -> unit + sanitizer + fuzz on host
 -> target HIL and fault injection
 -> triage database and reviewed deviations
```

tool을 여러 개 쓰는 이유는 false negative 영역이 다르기 때문이다. 결과 수보다 confirmed high-impact defect, recurrence prevention, mean time to triage를 metric으로 삼는다.

## 9. 정적 분석 운영

- `compile_commands.json`을 실제 production flags로 생성
- baseline은 legacy debt를 숨기는 영구 면제가 아니라 owner와 deadline 부여
- warning suppression은 exact rule/location/rationale로 제한
- SARIF(Static Analysis Results Interchange Format)로 결과 통합
- CWE, requirement, test, fix commit을 trace
- tool version/ruleset을 pin하고 upgrade delta review
- generated code와 third-party code를 구분하되 security boundary는 scan
- CI gate는 new critical/high와 reviewed MISRA required violation을 차단

## 10. 안전과 보안의 결합

안전은 accidental fault, 보안은 malicious action을 주로 다루지만 같은 memory corruption이 둘 다 위협한다. hazard analysis에서 security-caused hazard를 포함하고, safe mode가 authentication을 우회하는 backdoor가 되지 않게 한다. availability를 위해 fail-open할지 command integrity를 위해 fail-closed할지는 기능별로 결정한다.

[← 이전](07_embedded_platform.md) · [메인](../README.md) · [다음: 미래 로드맵 →](09_future_roadmap.md)
