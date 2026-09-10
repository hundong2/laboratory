# 위성 네트워크 성능 모델

문서 ID: `PM-SATNET-001`  
Revision: `0.1`  
작성일: 2026-09-10

## 1. 목적

처리율, 종단 간 지연, hop 수, queue delay, contact time과 onboard buffer를 같은 시간축에서 계산한다. 평균만 보지 않고 percentile, deadline miss, drop 원인과 자원 포화를 보고한다.

## 2. 입력

| 분류 | 변수 | 단위 | 설명 |
|---|---|---:|---|
| topology | `N`, `E(t)` | node, edge | 노드 수와 시간에 따라 활성화되는 링크 |
| contact | `start`, `end`, `rate` | s, s, bit/s | contact window와 usable data rate |
| traffic | `arrival`, `size`, `priority`, `deadline` | s, byte, class, s | bundle/packet 생성 과정 |
| link | `propagation`, `processing`, `loss` | s, s, probability | 홉별 지연과 독립 loss 가정 |
| queue | discipline, capacity | —, byte | strict priority/WFQ/FIFO와 buffer 제한 |
| protocol | header, block, retry, FEC rate | byte, byte, count, ratio | goodput을 줄이는 overhead |

`E(t)`는 정적 adjacency matrix가 아니라 contact interval 목록으로 표현한다. Optical contact는 acquisition time을 window에서 빼고, RF/광 availability가 상관되어 있으면 독립 확률을 곱하지 않는다.

## 3. 핵심 식

유효 contact 용량:

```text
C_contact = max(0, t_end - t_start - t_acquisition - t_guard) × R_goodput
```

프로토콜 goodput:

```text
R_goodput = R_phy × code_rate × payload/(payload + headers) × (1 - residual_loss)
```

종단 간 지연:

```text
D_e2e = Σ(D_queue + D_serialization + D_propagation + D_processing + D_acquisition)
        + D_wait_for_contact + D_retransmission
```

직렬화 지연은 `packet_bits / link_rate`, 전파 지연은 `distance / c`다. BDP(Bandwidth-Delay Product, 대역폭-지연 곱)는 `rate × RTT`이며, in-flight window가 이보다 작으면 링크를 채우지 못한다.

큐 안정성의 필요조건은 장기 평균 도착률 `λ`가 장기 서비스율 `μ`보다 작다는 것이다. 단, 주기적으로 끊기는 링크는 평균만으로 부족하므로 각 outage 동안 누적되는 backlog가 buffer보다 작은지 검사한다.

## 4. 모델링 절차

1. 동일한 mission epoch와 clock 기준으로 contact plan을 정렬한다.
2. contact마다 acquisition/guard 후 usable interval을 계산한다.
3. traffic을 생성하고 deadline·priority·destination을 부여한다.
4. 활성 링크와 queue policy로 다음 hop을 선택한다.
5. serialization 후 확률적 loss 또는 trace 기반 error를 적용한다.
6. 실패 시 재시도 정책, 다음 contact 대기 또는 drop reason을 결정한다.
7. delivered bytes, offered load, p50/p95/p99 latency, loss, deadline miss, max queue를 집계한다.

## 5. 성능 지표 정의

- Throughput(처리율): 측정 구간에 물리적으로 전송된 bit/s.
- Goodput(유효 처리율): 최종 목적지에서 중복을 제거한 application payload bit/s.
- Packet loss ratio(패킷 손실률): 고유 생성 개수 대비 영구 미전달 개수. 아직 deadline 전 queue에 남은 항목은 별도 표시한다.
- Availability(가용성): 합의한 서비스 조건을 만족한 시간 비율. 단순 link-up 비율이 아니다.
- Latency percentile(지연 백분위수): delivered sample에 대한 p50/p95/p99. drop을 제외했다는 사실을 함께 표시한다.
- Hop count(홉 수): 성공 데이터의 평균·최대. retransmission은 hop과 별도 계수한다.
- Queue delay(큐 대기 지연): 전송 시작에서 생성/도착 시간을 뺀 값 중 contact wait와 local scheduling을 구분한다.

## 6. 실험 설계

| Case | 변화 | 고정 | 확인할 주장 |
|---|---|---|---|
| P-BASE | 기준 contact/traffic | seed, packet size | 기준 p95와 loss |
| P-RATE | link rate 0.5×/1×/2× | contact/traffic | rate와 goodput의 비선형성 |
| P-LOSS | loss 0/1/5/10% | retry/FEC | 재시도와 deadline trade-off |
| P-HOP | 1/2/4 hop | per-hop rate | serialization·queue 누적 |
| P-CONTACT | window ±20%, miss 1회 | traffic | buffer와 delivery deadline |
| P-FAILOVER | primary 단절 | alternate capacity | 전환 시간과 packet duplication |

동일 seed를 쓰는 paired comparison과 여러 seed의 confidence interval을 함께 사용한다. 최적값을 고른 뒤 같은 trace로만 평가하는 data leakage를 피한다.

## 7. 구현과 한계

[satellite_network_sim.py](../tools/satellite_network_sim.py)는 단일 공유 downlink contact와 priority queue를 이용한 최소 참조 구현이다. 실제 constellation 분석에는 궤도 전파, 시간변화 routing, contention, antenna scheduling, correlated weather, link adaptation, protocol state를 추가해야 한다. 결과를 비행 인증 증거로 사용하지 않는다.

[← 실무 산출물](../README.md)
