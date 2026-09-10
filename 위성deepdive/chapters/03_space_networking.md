# 03. Space SDN·SD-WAN·동적 라우팅

## 1. SDN이 왜 탄생했는가

전통 network device는 forwarding(패킷 전달)과 control(경로 계산)을 한 장비 안에서 수행하고 vendor별 설정 인터페이스를 사용했다. 대규모망에서 이를 장비마다 수동 설정하면 정책 일관성과 자동화가 어려웠다. SDN(Software-Defined Networking, 소프트웨어 정의 네트워킹)은 control plane과 data plane을 논리적으로 분리하고, 추상화된 API(Application Programming Interface, 응용 프로그램 인터페이스)를 통해 network를 프로그램할 수 있게 했다.

- **data plane(데이터 평면)**: 실제 packet/frame lookup과 forwarding
- **control plane(제어 평면)**: topology, route, policy 계산
- **management plane(관리 평면)**: configuration, telemetry, lifecycle, operator intent
- **orchestrator(오케스트레이터)**: 여러 controller와 service를 조정해 목표 상태를 배포

분리는 물리적 분리와 같지 않다. 위성 안에 controller agent와 forwarding process가 함께 있어도 인터페이스와 책임이 분리되면 SDN적 구조다.

## 2. Space SDN

**Space SDN**은 시간에 따라 바뀌는 RF/optical link, 제한된 onboard compute, 긴/가변 지연, 지상 연결 단절을 고려해 SDN 원리를 적용한다. 지상 controller가 모든 packet 결정을 실시간으로 내려주는 구조는 단절 시 실패하므로 세 계층이 현실적이다.

1. **offline planner**: orbit와 contact plan으로 장기 정책·후보 경로를 계산한다.
2. **ground controller**: 임무 정책, key, software, flow rule을 contact 때 동기화한다.
3. **onboard autonomous agent**: local link state와 pre-authorized policy 안에서 빠르게 failover한다.

이를 `hierarchical/hybrid control`이라 한다. 중앙 최적화와 지역 생존성을 함께 얻지만, policy version과 stale state 충돌을 해결해야 한다.

## 3. forwarding pipeline

```text
ingress -> classify -> authenticate/decrypt -> meter/police
        -> queue/priority -> route/next-hop -> encapsulate/encrypt -> egress
```

flow key는 source/destination, virtual channel, DSCP(Differentiated Services Code Point), application ID, security label, deadline, bundle priority가 될 수 있다. 우주망에서 deadline과 expiry time은 단순 IP 5-tuple보다 중요한 경우가 많다.

rule에는 version, validity interval, fallback action, signature를 둔다. controller reachability가 끊기면 `fail-secure`(확실하지 않은 traffic 차단)와 `fail-operational`(제한된 기존 service 지속) 중 임무별 선택이 필요하다.

## 4. link-state monitoring

**link state monitoring(링크 상태 감시)**는 단순 up/down이 아니다.

- received power, RSSI, SNR/SINR
- frame/packet error와 FEC correction count
- Doppler estimate, timing lock, optical pointing error
- queue depth, age of information, drop count
- predicted remaining contact time
- energy, thermal limit, terminal availability
- neighbor heartbeat와 route version

Raw sample은 jitter가 크므로 exponential moving average, median, hysteresis를 사용하되 fault를 늦게 발견하지 않도록 fast-path hard alarm도 둔다. metric마다 timestamp, measurement window, confidence를 포함해야 오래된 정보가 새 정보처럼 쓰이지 않는다.

## 5. dynamic routing

지상 link-state protocol은 현재 topology를 flood한다. 위성망은 orbit 때문에 미래 topology가 상당 부분 예측되므로 다음을 결합한다.

- **reactive routing(반응형)**: 지금 관측한 link failure에 대응
- **predictive routing(예측형)**: ephemeris와 contact plan으로 미래 경로 계산
- **schedule-aware routing(일정 인지 라우팅)**: contact start/end, capacity, latency를 시간 확장 그래프에 반영
- **opportunistic routing(기회형)**: 계획에 없던 contact를 활용

최단 거리만 쓰면 큰 queue 또는 곧 끝날 contact로 traffic이 몰린다. cost 예시는 다음과 같다.

```text
cost = α·arrival_time + β·loss_risk + γ·energy
     + δ·queue_delay + ε·contact_switch_penalty
```

priority traffic에는 separate queue와 resource reservation을 두되 starvation(낮은 우선순위가 영원히 서비스받지 못함)을 막는 aging이 필요하다.

## 6. handover logic

**handover(핸드오버)**는 user 또는 route가 한 beam/satellite/gateway/link에서 다른 것으로 전환되는 과정이다.

### make-before-break와 break-before-make

- **make-before-break**: 새 link를 먼저 만들고 old link를 끊는다. 손실은 적지만 terminal·spectrum·power가 이중 필요하다.
- **break-before-make**: old link를 끊은 후 새 link를 획득한다. 자원은 적지만 outage가 생긴다.

trigger는 단일 RSSI threshold가 아니라 predicted time-to-link-loss, target link margin, acquisition time, queue, policy를 결합한다.

```text
if current_remaining < acquire_time + guard_time
   and target_score > current_score + hysteresis
   and target_dwell >= minimum_dwell:
       prepare_target()
       switch_when_verified()
```

세션 연속성을 위해 IP mobility, locator/identifier separation, transport multipath, application reconnect, BP store-forward 중 어느 계층이 책임지는지 정한다.

## 7. SD-WAN

**SD-WAN (Software-Defined Wide Area Network, 소프트웨어 정의 광역망)**은 여러 underlay(인터넷, MPLS, cellular, satellite 등) 위에 application-aware policy overlay를 만든다. MEF 70.2는 externally visible service behavior와 attribute를 표준화한다.

### 핵심 구성

- **SD-WAN edge**: site에서 application flow를 분류하고 tunnel/underlay를 선택
- **controller/orchestrator**: policy와 topology 배포
- **underlay connectivity service**: 실제 IP/MPLS/5G/satellite 회선
- **overlay tunnel**: IPsec 등의 암호화된 논리 경로

위성 backhaul에서는 application SLA(Service-Level Agreement, 서비스 수준 협약)에 따라 low-latency LEO, 고가용 GEO, terrestrial link를 선택할 수 있다. 그러나 SD-WAN은 physical link capacity나 propagation delay를 없애지 않는다. tunnel overhead, MTU(Maximum Transmission Unit), asymmetric route, intermittent link를 profile에 포함해야 한다.

## 8. Space SDN과 SD-WAN 비교

| 항목 | Space SDN | SD-WAN |
|---|---|---|
| 주 대상 | satellite/ground network 내부 control | site 간 WAN service overlay |
| 주요 입력 | contact plan, ISL, orbit, terminal resource | application class, SLA, underlay metric |
| 제어 범위 | link부터 network slice까지 | overlay path와 security policy 중심 |
| 공통점 | policy-based forwarding, controller, telemetry, automation |
| 결합 | Space SDN이 satellite underlay를 운영하고 SD-WAN이 end-user overlay를 선택 가능 |

## 9. failover 설계 패턴

- **fast local repair**: onboard agent가 미리 승인된 next-hop으로 수 초 내 전환
- **global reoptimization**: ground/controller가 새 contact plan과 flow allocation 계산
- **graceful degradation**: video를 낮은 rate로, critical command를 우선
- **circuit breaker**: 반복 실패 link를 일정 시간 격리
- **configuration rollback**: signed last-known-good policy로 복귀

controller 이중화는 leader election만으로 끝나지 않는다. 우주 partition 중 양쪽 controller가 서로 다른 명령을 내릴 수 있는 split-brain에 대비해 epoch, lease, monotonic policy version, authority scope가 필요하다.

## 10. 현재 기술과 연구 과제

광 메쉬 constellation과 LunaNet 같은 달 네트워크가 network-aware payload processing과 DTN을 실제 요구사항으로 끌어올렸다. 유망 분야는 time-variant routing, intent-based resource scheduling, digital twin 기반 사전 검증, onboard anomaly detection, multi-domain interoperability다. AI가 routing을 제안할 수는 있지만 hard constraint, explainable fallback, offline verification 없이 flight-critical control을 단독 맡겨서는 안 된다.

[← 이전](02_rf_optical_link_budget.md) · [메인](../README.md) · [다음: CCSDS·TT&C →](04_ccsds_operations.md)
