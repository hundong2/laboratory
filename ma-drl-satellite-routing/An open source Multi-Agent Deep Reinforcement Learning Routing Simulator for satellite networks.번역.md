# An open source Multi-Agent Deep Reinforcement Learning Routing Simulator for satellite networks — 문장 대조 번역

작성·접근일: 2026-09-27 · [학습 README](README.md)

## 논문 metadata와 이용 조건

- 저자: Federico Lozano-Cuadra, Mathias D. Thorsager, Israel Leyva-Mayorga, Beatriz Soret.
- 출판: *Proceedings of the 1st SPAICE Conference on AI in and for Space*, 2024, pp. 420–424.
- DOI: [10.5281/zenodo.13885645](https://doi.org/10.5281/zenodo.13885645).
- 입력: [arXiv:2407.11047](https://arxiv.org/abs/2407.11047). arXiv v1: 2024-07-08, v2: 2024-11-28.
- 실제 번역 기준: [공식 학회 PDF](https://zenodo.org/records/13885645/files/An%20open%20source%20MultiAgent%20Deep%20Reinforcement%20Learning%20Routing%20Simulator%20for%20satellite%20networks.pdf), 영어, 5쪽. 버전이 지정되지 않아 접근 가능한 출판본을 사용했다. arXiv HTML은 대조 보조 자료다.
- Copyright © 2024, 위 저자들. 출판본 각 페이지의 **CC BY 4.0** 고지를 시각 확인했다. [라이선스](https://creativecommons.org/licenses/by/4.0/). arXiv 페이지의 비독점 배포 허락을 번역 허가로 간주한 것이 아니다.
- 변경 사항: 한국어 번역·용어 설명 추가, 원문 문장 순서에 맞춘 ID 부여, 줄 끝 분철·다단 편집·페이지 header/footer 제거, 수식 Markdown 표기. 번역 및 해설은 CC BY 4.0으로 제공한다. 저자 승인·추천을 의미하지 않는다.

## 번역·접근 범위

| 범위 | 상태 | 비고 |
| --- | --- | --- |
| 제목·초록 | 완료 | S001–S008 |
| §1 Introduction | 완료 | S009–S016 |
| §2 Simulator architecture | 완료 | S019–S053 |
| §3 Routing algorithms | 완료 | S054–S068 |
| §4 Setup and general settings | 완료 | S069–S077 |
| §5 Results and analysis | 완료 | S078–S104 |
| §6 Conclusion and Future work | 완료 | S105–S108 |
| Figure 1–7 caption | 완료 | 본문 사이 해당 구간에 배치 |
| 저자 소속·지원 각주 | 부분 번역 | 아래 요약, 개인 이메일 재기재 생략 |
| 참고문헌 | 완료 | 서지 정보 유지, 문장 번역 대상 아님 |
| 별도 표·알고리즘·부록 | 해당 없음 | 출판본에 별도 항목 없음 |

소속·지원 각주 요약: Lozano-Cuadra와 Soret은 University of Malaga, Thorsager와 Leyva-Mayorga는 Aalborg University 소속이다. 스페인 TATOOINE(PID2022-136269OB-I00) 및 ESA SatNEx V(4000130962/20/NL/NL/FE)의 일부 지원을 명시한다. 저자의 견해가 ESA 공식 견해를 뜻하지 않는다는 고지가 있다.

## 읽기 전 핵심 배경

데이터를 경로로 보내는 결정과 링크가 그 데이터를 실제로 처리하는 속도는 다르다. 짧은 경로라도 큐가 길면 늦을 수 있다. 시뮬레이션 시간, 학습에 소비한 컴퓨터 시간, 실제 위성 탑재 실행 시간을 구분한다. 아래 `Original`은 출판본, `한국어`는 번역, `용어·약어 해설`과 `번역자 주`는 학습을 위해 추가한 내용이다.

## Title / Abstract

**S001 — Original**

An open source Multi-Agent Deep Reinforcement Learning Routing Simulator for satellite networks

**S001 — 한국어**

(위성 네트워크를 위한 오픈소스 다중 에이전트 심층강화학습 라우팅 시뮬레이터)

- **용어·약어 해설**: 다중 에이전트(multi-agent)는 여러 의사결정 주체가 있다는 뜻이다. 이 논문에서는 위성이 라우터이자 학습 주체가 된다. 심층강화학습(deep reinforcement learning)은 신경망으로 값이나 정책을 표현하면서 상호작용의 보상으로 학습하는 방법이다.

**S002 — Original**

This paper introduces an open source simulator for packet routing in Low Earth Orbit Satellite Constellations (LSatCs).

**S002 — 한국어**

(이 논문은 저궤도 위성 군집에서 패킷을 라우팅하기 위한 오픈소스 시뮬레이터를 소개한다.)

- **용어·약어 해설**: LSatCs (Low Earth Orbit Satellite Constellations, 저궤도 위성 군집)는 함께 통신망을 형성하는 저궤도 위성들의 구성이다. 패킷(packet)은 망이 전달하는 데이터 단위다.

**S003 — Original**

The simulator, implemented in Python, supports traditional Dijkstra’s based routing as well as more advanced learning solutions based on Q-Routing and Multi-Agent Deep Reinforcement Learning (MA-DRL) from our previous work.

**S003 — 한국어**

(Python으로 구현한 이 시뮬레이터는 전통적인 Dijkstra 기반 라우팅뿐 아니라 저자들의 이전 연구에서 나온 Q-routing 및 다중 에이전트 심층강화학습 기반의 더 발전된 학습 해법을 지원한다.)

- **용어·약어 해설**: MA-DRL (Multi-Agent Deep Reinforcement Learning, 다중 에이전트 심층강화학습). Q-routing은 다음 홉 선택의 예상 비용 등을 Q 값으로 학습하는 라우팅 방식이다. Dijkstra는 비음수 간선 가중치의 합이 최소인 경로를 찾는 알고리즘이다.

**S004 — Original**

It uses an event-based approach with the SimPy module to accurately simulate packet creation, routing and queuing, providing real-time tracking of queues and latency.

**S004 — 한국어**

(SimPy 모듈의 이벤트 기반 접근으로 패킷 생성·라우팅·큐잉을 정밀하게 시뮬레이션하여 큐와 지연을 실시간으로 추적한다.)

- **용어·약어 해설**: SimPy는 Python 이산사건 시뮬레이션 도구다. 여기의 실시간 추적은 시뮬레이션 중 상태를 추적한다는 문맥이며 hard real-time 실행을 보장한다는 뜻은 아니다.

**S005 — Original**

The simulator is highly configurable, allowing adjustments in routing policies, traffic, ground and space segment topologies, communication parameters, and learning hyperparameters.

**S005 — 한국어**

(시뮬레이터는 라우팅 정책, 트래픽, 지상·우주 구간의 토폴로지, 통신 매개변수, 학습 하이퍼파라미터를 폭넓게 조정할 수 있다.)

- **용어·약어 해설**: 토폴로지(topology)는 노드와 연결의 구조다. 하이퍼파라미터는 학습률처럼 학습 과정의 동작을 정하는 설정이다.

**S006 — Original**

Key features include the ability to visualize system motion and track packet paths while considering the inherent uncertainties of such a dynamic system.

**S006 — 한국어**

(이러한 동적 시스템 고유의 불확실성을 고려하면서 시스템 움직임을 시각화하고 패킷 경로를 추적하는 기능이 핵심에 포함된다.)

**S007 — Original**

Results highlight significant improvements in end-to-end (E2E) latency using Reinforcement Learning (RL)-based routing policies compared to traditional methods.

**S007 — 한국어**

(결과는 전통적인 방법과 비교했을 때 강화학습 기반 라우팅 정책의 종단 간 지연이 크게 개선됨을 보여준다.)

- **용어·약어 해설**: E2E (End-to-End, 종단 간)는 출발지부터 최종 수신지까지다. RL (Reinforcement Learning, 강화학습)은 행동과 환경 피드백으로 정책을 개선한다. 번역자 주: 저자의 결과 요약이며 모든 조건의 우월성이나 통계적 유의성을 별도로 보증하는 표현은 아니다.

**S008 — Original**

The source code, the documentation and a Jupyter notebook with post-processing results and analysis are available on GitHub.

**S008 — 한국어**

(소스 코드, 문서, 후처리 결과와 분석을 담은 Jupyter notebook을 GitHub에서 이용할 수 있다.)

## 1 Introduction

**S009 — Original**

Efficient routing in LSatCs is critical for global connectivity in 6G networks.

**S009 — 한국어**

(저궤도 위성 군집의 효율적 라우팅은 6G 네트워크의 전 지구적 연결성에 중요하다.)

- **용어·약어 해설**: 6G (Sixth Generation, 6세대 이동통신)는 이 연구의 미래 연결성 배경이며 해당 시뮬레이터가 완성된 6G 규격 전체를 구현한다는 뜻은 아니다.

**S010 — Original**

This requires addressing multiple challenges, including the partial knowledge of the network at the satellites and their continuous movement, and the time-varying sources of uncertainty in the system, such as traffic, communication links, or communication buffers [1].

**S010 — 한국어**

(이를 위해 위성이 가진 부분적인 망 정보와 지속적 이동, 그리고 트래픽·통신 링크·통신 버퍼처럼 시간에 따라 달라지는 시스템 불확실성 등 여러 문제를 해결해야 한다 [1].)

**S011 — Original**

Traditional routing algorithms are inadequate to address these problems: They either lack adaptability to network changes or congest the network with feedback messages.

**S011 — 한국어**

(전통적 라우팅 알고리즘은 망 변화에 적응하는 능력이 부족하거나 피드백 메시지로 망을 혼잡하게 하므로 이 문제들을 해결하기에 불충분하다.)

**S012 — Original**

To overcome these challenges, new algorithms must be developed, some of them RL-based, which need to be accompanied by a robust framework.

**S012 — 한국어**

(이 문제를 극복하려면 강화학습 기반 방법 등을 포함한 새로운 알고리즘을 개발해야 하며, 이를 뒷받침하는 견고한 프레임워크가 필요하다.)

**S013 — Original**

Python is the best environment for developing RL-based algorithms due to its extensive libraries for machine learning, such as Keras-TensorFlow, PyTorch, NumPy, and Pandas.

**S013 — 한국어**

(Keras-TensorFlow, PyTorch, NumPy, Pandas 등 풍부한 머신러닝 라이브러리 덕분에 Python은 강화학습 기반 알고리즘 개발에 가장 좋은 환경이다.)

번역자 주: “가장 좋은”은 저자의 평가다. 다른 언어나 환경과의 객관적 순위를 실험한 문장은 아니다.

**S014 — Original**

This paper introduces an open source MA-DRL Routing Simulator for satellite networks built in Python, where these designed algorithms can be implemented and tested.

**S014 — 한국어**

(이 논문은 설계한 알고리즘을 구현하고 시험할 수 있는 Python 기반 위성망 오픈소스 MA-DRL 라우팅 시뮬레이터를 소개한다.)

**S015 — Original**

The simulator supports various routing algorithms, including some Dijkstra’s [2] shortest path-based and those from our recent works: (1) The Q-Routing with Q-tables for distributed routing decisions [3], and (2) the MA-DRL first proposed in [4], which was then further tested and extended to continual learning with Satellite Federated Learning (SFL) in [1].

**S015 — 한국어**

(시뮬레이터는 Dijkstra [2] 최단 경로 기반 알고리즘들과 최근 저자 연구의 방법들, 즉 (1) Q-table로 분산 라우팅을 결정하는 Q-routing [3], (2) [4]에서 처음 제안하고 [1]에서 추가 시험 및 위성 연합학습을 통한 지속학습으로 확장한 MA-DRL을 지원한다.)

- **용어·약어 해설**: SFL (Satellite Federated Learning, 위성 연합학습)은 위성별 학습 결과를 결합하는 접근이다. 지속학습(continual learning)은 변화하는 경험에 맞춰 지식을 계속 갱신하는 문제다.

**S016 — Original**

The source code, a Jupyter notebook with some post-processing results and analysis, and the documentation for the MA-DRL Routing Simulator are available on GitHub [5].

**S016 — 한국어**

(MA-DRL 라우팅 시뮬레이터의 소스 코드, 일부 후처리 결과와 분석이 담긴 Jupyter notebook, 문서를 GitHub [5]에서 이용할 수 있다.)

### Figure 1

**S017 — Original**

Kepler constellation deployed and their corresponding inter-satellite links (ISLs) established following the Greedy matching with 18 active gateways over the population maps [6], where the green tone depends on the population density.

**S017 — 한국어**

(인구 지도 [6] 위에 배치한 Kepler 군집과, 활성 gateway 18개를 두고 탐욕적 매칭으로 설정한 위성 간 링크를 나타낸다. 녹색 농도는 인구 밀도에 따라 달라진다.)

- **용어·약어 해설**: ISL (Inter-Satellite Link, 위성 간 링크)은 위성을 직접 연결한다. Greedy matching(탐욕적 매칭)은 현재 기준에서 유리한 연결을 순차 선택하는 접근이며 전역 최적성을 자동 보장하지 않는다.

**S018 — Original**

Each satellite’s colour is a different orbital plane.

**S018 — 한국어**

(각 위성의 색은 서로 다른 궤도면을 나타낸다.)

## 2 Simulator architecture

**S019 — Original**

The event-based simulation environment was developed in Python using the SimPy module, chosen for its effectiveness in discrete event modeling [7].

**S019 — 한국어**

(이벤트 기반 시뮬레이션 환경은 이산사건 모델링에 효과적인 SimPy 모듈을 선택하여 Python으로 개발했다 [7].)

**S020 — Original**

Time in the simulator progresses by jumping from one scheduled event to the next, rather than continuously.

**S020 — 한국어**

(시뮬레이터의 시간은 연속적으로 흐르는 대신 예약된 사건에서 다음 사건으로 건너뛰며 진행한다.)

**S021 — Original**

Each action, including creating, routing, and queueing of individual data packets, is explicitly simulated as a SimPy event, providing accurate real-time tracking of queues and latency.

**S021 — 한국어**

(개별 패킷의 생성·라우팅·큐잉을 포함한 각 동작을 SimPy 사건으로 명시적으로 시뮬레이션하여 큐와 지연을 정확하게 추적한다.)

**S022 — Original**

Packets are unique entities (objects) existing from creation at a generating gateway until they arrive at the destination gateway.

**S022 — 한국어**

(패킷은 생성 gateway에서 만들어진 때부터 목적지 gateway에 도착할 때까지 존재하는 고유한 개체, 즉 객체다.)

**S023 — Original**

The transmission time is calculated based on the packet size and current link rates, propagation time based on the exact distance between transmitter and receiver at transmission time, and queue time based on the time a packet spends in the queue.

**S023 — 한국어**

(전송 시간은 패킷 크기와 현재 링크 속도, 전파 시간은 전송 시점 송수신기 사이의 정확한 거리, 큐 시간은 패킷이 큐에 머문 시간을 바탕으로 계산한다.)

- **용어·약어 해설**: transmission time(전송 시간)은 비트를 링크에 내보내는 시간이고 propagation time(전파 시간)은 신호가 공간을 이동하는 시간이다. queue time(큐 시간)은 전송 시작 전 대기다.

**S024 — Original**

This detailed level of simulation is essential for representing the states and computing the rewards of the environment in our RL-based routing algorithms.

**S024 — 한국어**

(이 정도로 상세한 시뮬레이션은 저자들의 강화학습 라우팅 알고리즘에서 환경 상태를 표현하고 보상을 계산하는 데 필수적이다.)

**S025 — Original**

The simulator emulates a realistic scenario where ground gateways gather the nearby terrestrial traffic that is assumed to be generated by mobile users and distribute that to each other gateway equally through a LSatC, integrating space and ground segments into the communication network, as shown in Fig. 1.

**S025 — 한국어**

(시뮬레이터는 지상 gateway가 이동 사용자가 생성한다고 가정한 인근 지상 트래픽을 모아 저궤도 위성 군집을 통해 다른 gateway 각각에 균등하게 분배하는 현실적인 시나리오를 모사하며, Fig. 1처럼 지상·우주 구간을 하나의 통신망에 통합한다.)

**S026 — Original**

The environment is built as a time-variant dynamic graph $\mathcal{G}_t(\mathcal{N},\mathcal{E})$ with nodes $\mathcal{N}$, representing satellites and gateways, and edges $\mathcal{E}$, representing the transmission links between them, which can be either ISL or ground-to-satellite link (GSL), implemented as Radio Frequency (RF) or Free Space Optical (FSO).

**S026 — 한국어**

(환경은 위성과 gateway를 나타내는 노드 $\mathcal{N}$, 그 사이의 전송 링크를 나타내는 간선 $\mathcal{E}$로 구성된 시변 동적 그래프 $\mathcal{G}_t(\mathcal{N},\mathcal{E})$로 만든다. 링크는 ISL 또는 지상–위성 링크이며 무선 주파수 또는 자유공간 광통신으로 구현될 수 있다.)

- **용어·약어 해설**: GSL (Ground-to-Satellite Link, 지상–위성 링크), RF (Radio Frequency, 무선 주파수), FSO (Free Space Optical, 자유공간 광통신). 그래프의 t는 시점이며 노드·간선 집합은 신경망 tensor가 아니다.

### Space segment

**S027 — Original**

The satellite constellation consists of $N$ satellites evenly distributed across $O$ orbital planes.

**S027 — 한국어**

(위성 군집은 O개의 궤도면에 고르게 분포한 N개의 위성으로 구성된다.)

번역자 주: 이 문장에서는 N이 전체 수처럼 쓰이지만 §5는 N을 면당 수로 쓴다. 원문 표기 혼용을 그대로 밝히며 임의로 동일 의미로 통일하지 않는다.

**S028 — Original**

Each satellite functions as a router and learning agent for RL-based solutions.

**S028 — 한국어**

(강화학습 기반 해법에서 각 위성은 라우터이자 학습 에이전트로 기능한다.)

**S029 — Original**

Satellites are positioned at specific and configurable altitudes, longitudes, and orbit inclinations, moving according to orbital mechanics and Earth’s rotation [1].

**S029 — 한국어**

(위성은 설정 가능한 특정 고도·경도·궤도 경사각에 배치되며, 궤도역학과 지구 자전에 따라 움직인다 [1].)

**S030 — Original**

Satellites move periodically, at the beginning of each time interval, rather than continuously.

**S030 — 한국어**

(위성은 연속적으로 움직이는 대신 각 시간 구간의 시작에 주기적으로 이동한다.)

**S031 — Original**

After a fixed time interval, each satellite is placed in the exact position that it would reach if it had moved continuously during that period.

**S031 — 한국어**

(고정된 시간 간격이 지나면 각 위성을 그 기간에 연속적으로 이동했을 경우 도달할 정확한 위치에 배치한다.)

**S032 — Original**

This periodic movement impacts latency calculations by updating transmission and propagation times at each position update.

**S032 — 한국어**

(이 주기적 이동은 위치 갱신마다 전송·전파 시간을 갱신하므로 지연 계산에 영향을 준다.)

**S033 — Original**

Each satellite has one antenna for GSL and four for ISL (two for inter-plane and two for intra-plane links).

**S033 — 한국어**

(각 위성은 GSL용 안테나 하나와 ISL용 안테나 네 개, 즉 궤도면 간 링크용 두 개와 궤도면 내 링크용 두 개를 가진다.)

**S034 — Original**

Selecting the best ISL is a dynamic matching problem and consists of establishing the best ISLs among satellites.

**S034 — 한국어**

(최적 ISL 선택은 위성 사이에 가장 적합한 ISL들을 설정하는 동적 매칭 문제다.)

**S035 — Original**

Links are bidirectional, and the network is reconfigured as satellites move, i.e, $\mathcal{G}_t$ is built again maintaining previous queue states.

**S035 — 한국어**

(링크는 양방향이며 위성 이동에 따라 망을 재구성한다. 즉 기존 큐 상태를 유지하면서 $\mathcal{G}_t$를 다시 만든다.)

### Ground segment / Data rate

**S036 — Original**

The ground segment consists of a set of configurable ground gateways, which gather the terrestrial traffic from mobile devices.

**S036 — 한국어**

(지상 구간은 이동 단말의 지상 트래픽을 모으는, 설정 가능한 지상 gateway 집합으로 구성된다.)

**S037 — Original**

Each gateway aggregates this traffic into large packets for transmission to its nearest satellite, with which it maintains a GSL.

**S037 — 한국어**

(각 gateway는 이 트래픽을 큰 패킷으로 묶어 GSL로 연결된 가장 가까운 위성에 전송한다.)

**S038 — Original**

The communication data rate between nodes $i$ and $j$, $R(i,j)$, is determined by the highest modulation and coding scheme that ensures reliable communication based on the current signal-to-noise ratio (SNR), and zero otherwise, using DVB-S2 technology [8] for realistic data rates assuming free-space loss [1].

**S038 — 한국어**

(노드 i와 j 사이 통신 속도 R(i,j)는 현재 신호 대 잡음비에서 신뢰할 수 있는 통신을 보장하는 가장 높은 변조·부호화 방식으로 정하고, 가능하지 않으면 0으로 둔다. 자유공간 손실을 가정하고 [1] DVB-S2 기술 [8]로 현실적인 데이터 속도를 정한다.)

- **용어·약어 해설**: SNR (Signal-to-Noise Ratio, 신호 대 잡음비). DVB-S2 (Digital Video Broadcasting–Satellite–Second Generation, 2세대 위성 디지털 방송 규격)는 이 논문에서 링크 속도 모델에 사용된다. 변조·부호화 조합이 높을수록 무조건 안정적인 것은 아니다.

### Traffic generation / Routing

**S039 — Original**

We consider a scenario with realistic packet generation, queuing, and transmission, where each gateway transmits data equally split among the other gateways through the LSatC, then data is assumed to be distributed to the nearby connected users.

**S039 — 한국어**

(현실적인 패킷 생성·큐잉·전송을 고려하며, 각 gateway가 다른 gateway들에 균등 분할한 데이터를 위성 군집을 통해 전송한 뒤 수신지 인근 연결 사용자들에게 분배한다고 가정한다.)

**S040 — Original**

The total traffic load $\ell$ in the network is determined by the uplink data generation rate at each gateway and the maximum supported traffic load $\ell$, derived from uplink and downlink rates.

**S040 — 한국어**

(망의 전체 트래픽 부하 ℓ는 각 gateway의 상향링크 데이터 생성률과, 상·하향링크 속도로부터 얻은 최대 지원 트래픽 부하 ℓ에 의해 정해진다.)

번역자 주: 출판본은 두 개념에 같은 ℓ를 표기한다. 정규화 부하의 정확한 코드 정의를 이 문장만으로 확정하지 않는다. 실습의 ρ=λL/R은 독립적인 학습용 정의다.

**S041 — Original**

The traffic generation follows a Poisson distribution and $\ell$ is configurable by the user.

**S041 — 한국어**

(트래픽 생성은 Poisson 분포를 따르며 사용자가 ℓ를 설정할 수 있다.)

**S042 — Original**

As each gateway sends traffic to each other, the total number of unidirectional flows $U_f$ can be expressed as: $U_f=n_g\cdot(n_g-1)$, where $n_g$ is the number of active gateways.

**S042 — 한국어**

(각 gateway가 다른 모든 gateway로 트래픽을 보내므로 단방향 흐름의 총수는 $U_f=n_g(n_g-1)$이며, $n_g$는 활성 gateway 수다.)

- **용어·약어 해설**: self-loop를 제외한 순서 있는 쌍의 수다. 예를 들어 gateway 8개이면 56개이며, 왕복을 한 흐름으로 세면 안 된다.

**S043 — Original**

The routing algorithm at each satellite $i$ aims to relay each received packet $p(d)$ towards its destination $d$.

**S043 — 한국어**

(각 위성 i의 라우팅 알고리즘은 수신한 패킷 p(d)를 목적지 d를 향해 중계하는 것을 목표로 한다.)

**S044 — Original**

Each satellite has a transmission buffer with a maximum capacity of $Q^{\max}$, operating under a first-in first-out (FIFO) strategy.

**S044 — 한국어**

(각 위성은 최대 용량 $Q^{\max}$의 전송 버퍼를 가지며 선입선출 방식으로 동작한다.)

- **용어·약어 해설**: FIFO (First-In First-Out, 선입선출)는 먼저 들어온 패킷부터 처리하는 규칙이다. 버퍼에 서비스 중 패킷도 포함하는지는 구체 구현에서 확인해야 한다.

**S045 — Original**

If the buffer is not empty, the satellite takes the Head of Line packet and delivers it to one of its linked nodes following the chosen routing policy.

**S045 — 한국어**

(버퍼가 비어 있지 않으면 위성은 큐 맨 앞 패킷을 꺼내 선택한 라우팅 정책에 따라 연결된 노드 중 하나로 보낸다.)

- **용어·약어 해설**: Head of Line(HoL, 큐의 맨 앞)은 다음에 서비스할 패킷 위치를 뜻한다.

**S046 — Original**

Any packet arriving at a full buffer is dropped.

**S046 — 한국어**

(가득 찬 버퍼에 도착한 패킷은 폐기한다.)

### Latency

**S047 — Original**

The one-hop latency to transmit a packet from $i$ to $j$ depends on three factors: queue time, transmission time, and propagation time [1].

**S047 — 한국어**

(패킷을 i에서 j로 보내는 한 홉의 지연은 큐 시간, 전송 시간, 전파 시간이라는 세 요소에 달려 있다 [1].)

**S048 — Original**

The queue time at the transmission queue is the elapsed time since the packet is ready to be transmitted until the beginning of its transmission.

**S048 — 한국어**

(전송 큐의 큐 시간은 패킷이 전송 준비를 마친 때부터 실제 전송을 시작할 때까지의 경과 시간이다.)

**S049 — Original**

The transmission time is the time taken to transmit the packet based on the transmission rate.

**S049 — 한국어**

(전송 시간은 전송 속도에 따라 패킷을 내보내는 데 걸리는 시간이다.)

**S050 — Original**

The propagation time is the time it takes for the signal to travel the distance between $i$ and $j$, $\lVert ij\rVert$.

**S050 — 한국어**

(전파 시간은 신호가 i와 j 사이 거리 $\lVert ij\rVert$를 이동하는 데 걸리는 시간이다.)

**S051 — Original**

This latency model considers varying traffic loads, where propagation time is significant in low traffic but queue time increases under high traffic conditions [9].

**S051 — 한국어**

(이 지연 모델은 다양한 트래픽 부하를 고려한다. 트래픽이 적으면 전파 시간이 중요하지만 트래픽이 많아지면 큐 시간이 증가한다 [9].)

### Figure 2–3

**S052 — Original**

Input-Output MA-DRL Routing Simulator workflow.

**S052 — 한국어**

(MA-DRL 라우팅 시뮬레이터의 입력·출력 작업 흐름.)

**S053 — Original**

MA-DRL’s exploitation phase congestion test for all routes output with 8 active gateways.

**S053 — 한국어**

(활성 gateway 8개인 MA-DRL 활용 단계에서 모든 경로를 대상으로 한 혼잡 시험 출력.)

## 3 Routing algorithms

**S054 — Original**

Different routing policies are implemented in the simulator.

**S054 — 한국어**

(시뮬레이터에는 여러 라우팅 정책이 구현되어 있다.)

**S055 — Original**

On one hand, we have the deterministic ones, all of them based on shortest path Dijkstra’s algorithm [2], where the edge weights are minimized in centrally with full knowledge of the constellation.

**S055 — 한국어**

(한 부류는 모두 Dijkstra 최단 경로 알고리즘 [2]에 기반한 결정론적 정책으로, 군집 전체 정보를 가진 중앙 방식으로 간선 가중치 합을 최소화한다.)

**S056 — Original**

Each method minimizes a different weight: (1) Data Rate, where the edge weights between two nodes $i$ and $j$ are determined by the inverse of the data rate between nodes, namely $w_{i,j}=1/R(i,j)$.

**S056 — 한국어**

(각 방법은 서로 다른 가중치를 최소화한다. (1) Data Rate는 두 노드 i, j 사이 데이터 속도의 역수, 즉 $w_{i,j}=1/R(i,j)$를 간선 가중치로 사용한다.)

**S057 — Original**

This is a traditional routing approach that leads to choosing routes with high data rate links; (2) Slant Range, where the edge weights between $i$ and $j$ nodes are defined by the distance between them, $\lVert ij\rVert$, in order to minimize propagation times, and the (3) Hop, where all edges have the same weight, 1, where the total number of jumps is minimized.

**S057 — 한국어**

(이는 데이터 속도가 높은 링크로 구성된 경로를 선택하는 전통적 접근이다. (2) Slant Range는 전파 시간을 줄이기 위해 i, j 사이 거리 $\lVert ij\rVert$를 가중치로 사용하며, (3) Hop은 모든 간선의 가중치를 1로 두어 총 홉 수를 최소화한다.)

- **용어·약어 해설**: slant range(사거리)는 노드 사이 실제 직선 거리다. 홉 수는 중간 노드 수와 다르며 연결을 통과한 횟수다.

**S058 — Original**

On the other hand, other two RL-based routing policies are implemented, specifically the ones developed in our previous work.

**S058 — 한국어**

(다른 부류로는 저자들의 이전 연구에서 개발한 두 강화학습 기반 라우팅 정책이 구현되어 있다.)

**S059 — Original**

Firstly, the Q-Routing policy, developed in [3].

**S059 — 한국어**

(첫째는 [3]에서 개발한 Q-routing 정책이다.)

**S060 — Original**

Q-Tables are created automatically with NumPy [10] to increase efficiency.

**S060 — 한국어**

(효율성을 높이기 위해 NumPy [10]로 Q-table을 자동 생성한다.)

**S061 — Original**

They will store the learnt knowledge during the training process.

**S061 — 한국어**

(이 표들은 훈련 과정에서 배운 지식을 저장한다.)

**S062 — Original**

The user can choose if it wants the algorithm to explore and make random routing actions or import pre-trained Q-Tables and exploit its knowledge to use them as routing policy.

**S062 — 한국어**

(사용자는 알고리즘이 탐험하며 임의 라우팅 행동을 하게 할지, 사전 학습한 Q-table을 가져와 그 지식을 라우팅 정책으로 활용하게 할지 선택할 수 있다.)

**S063 — Original**

Secondly, MA-DRL from [1, 4] is implemented.

**S063 — 한국어**

(둘째로 [1, 4]의 MA-DRL을 구현했다.)

**S064 — Original**

The Deep Neural Networks (DNNs) are initialized and trained with Keras [11].

**S064 — 한국어**

(심층신경망은 Keras [11]로 초기화하고 학습한다.)

- **용어·약어 해설**: DNN (Deep Neural Network, 심층신경망)은 여러 계층으로 입력에서 값을 추정한다. 이 논문의 표 기반 Q-routing과 구별되는 표현 수단이다.

**S065 — Original**

Double Deep Q-Learning (DDQN) [12] is implemented and its usage is configurable.

**S065 — 한국어**

(Double Deep Q-Learning [12]이 구현되어 있으며 사용 여부를 설정할 수 있다.)

- **용어·약어 해설**: DDQN (Double Deep Q-Learning, 이중 심층 Q학습)은 다음 행동의 선택과 그 값의 평가를 분리해 과대추정을 줄이려는 방식이다. 원 논문의 전체 학습식을 여기서 새로 정의하지 않는다.

**S066 — Original**

It is also possible either to import pre-trained DNNs or not and choose between the offline and the online phase of the algorithm.

**S066 — 한국어**

(사전 학습된 DNN을 가져올지 여부와 알고리즘의 offline 또는 online 단계를 선택할 수도 있다.)

### Figure 4

**S067 — Original**

Rewards over time of the offline phase of MA-DRL with 8 active gateways.

**S067 — 한국어**

(활성 gateway 8개인 MA-DRL offline 단계에서 시간에 따른 보상.)

**S068 — Original**

The highest rewards are given after a packet has been delivered to the receiving gateway.

**S068 — 한국어**

(패킷이 수신 gateway에 전달된 뒤 가장 높은 보상을 부여한다.)

## 4 Setup and general settings

**S069 — Original**

The simulator, running in Python 3.9, is multi-platform and has been tested on Windows, Linux, and Mac systems.

**S069 — 한국어**

(Python 3.9에서 동작하는 이 시뮬레이터는 여러 플랫폼을 지원하며 Windows, Linux, Mac에서 시험했다.)

**S070 — Original**

The user can install the required packages listed in the requirements.txt file using pip.

**S070 — 한국어**

(사용자는 requirements.txt에 나열된 필수 패키지를 pip로 설치할 수 있다.)

**S071 — Original**

It is advisable to create a virtual environment or an Anaconda environment for better management.

**S071 — 한국어**

(관리를 쉽게 하려면 가상환경 또는 Anaconda 환경을 만드는 것이 좋다.)

**S072 — Original**

The simulator is highly configurable, allowing users to adjust various parameters to suit their specific needs, as illustrated in Fig. 2.

**S072 — 한국어**

(Fig. 2처럼 시뮬레이터는 사용자가 필요에 맞게 다양한 매개변수를 조정할 수 있다.)

**S073 — Original**

Key configurable parameters include: (a) Routing Policy, including the shortest path-based, where the Data Rate, Slant Range or Hop can be set as weights, and the RL-based options; (b) Ground Segment settings, such as the number and locations of active gateways, as well as traffic generation $\ell$; (c) Space Segment parameters, which cover constellation design (configurable elements include the number of orbital planes and its inclination angle, satellites per plane, and the choice between Walker delta and Walker star designs), ISL matching (Greedy or Markovian [13]), and orbital motion (which can be sped up or slowed down); (d) Learning Hyperparameters, including rewards and penalties, exploration $\epsilon$, learning $\alpha$ and gamma $\gamma$ rates, state preprocessing, and training modes (Import pre-trained models for RL-based policies and choosing between online and offline phases for MA-DRL); and (e) Communication Setup, such as physical constants, uplink and downlink parameters, and packet size.

**S073 — 한국어**

(핵심 설정은 (a) Data Rate·Slant Range·Hop을 가중치로 쓰는 최단 경로 및 RL 라우팅 정책, (b) 활성 gateway 수·위치와 트래픽 생성 ℓ 등의 지상 구간, (c) 궤도면 수·경사각·면당 위성 수·Walker delta/star 선택을 포함한 군집 설계, Greedy/Markovian [13] ISL 매칭, 속도 조절 가능한 궤도 이동 등의 우주 구간, (d) 보상·벌점, 탐험 ε, 학습률 α, 감마 γ, 상태 전처리, 사전 학습 모델 가져오기와 MA-DRL online/offline 선택 등의 학습 설정, (e) 물리 상수·상하향링크 매개변수·패킷 크기 등의 통신 설정이다.)

- **용어·약어 해설**: ε는 탐험, α는 갱신 크기, γ는 미래 기여의 할인과 관련된다. Walker delta/star는 군집 배치 설계다. 원문의 “gamma rate”는 그대로 식별하되 일반 RL에서는 discount factor(할인율)라고 부른다.

**S074 — Original**

Additionally, the user can configure the simulator to plot the environment every time the constellation moves to visualize system motion, as in Fig. 1, and to plot the path of each delivered packet over this to track its journey through the network.

**S074 — 한국어**

(또한 사용자는 군집이 이동할 때마다 환경을 그려 Fig. 1처럼 움직임을 시각화하고, 전달된 각 패킷의 경로를 겹쳐 그려 망 안에서의 이동을 추적하도록 설정할 수 있다.)

**S075 — Original**

With all these settings configured, the simulator is now ready to run simulations and generate results.

**S075 — 한국어**

(이 설정들을 마치면 시뮬레이션을 실행하고 결과를 생성할 준비가 된다.)

### Figure 5

**S076 — Original**

E2E latency vs time vs $\epsilon$ connecting one gateway in Malaga, Spain and another one in Los Angeles, USA, through the Starlink constellation during the offline phase of the RL-based methods.

**S076 — 한국어**

(강화학습 방법의 offline 단계에서 Starlink 군집을 통해 스페인 Malaga의 gateway와 미국 Los Angeles의 gateway를 연결할 때 시간·ε에 따른 E2E 지연.)

**S077 — Original**

It can be appreciated how both methods learn to find the optimal path in less than 1 second.

**S077 — 한국어**

(두 방법이 1초 미만에 최적 경로를 찾도록 학습하는 것을 볼 수 있다.)

번역자 주: 특정 실험의 그림 설명이다. 실제 컴퓨터 학습시간이나 모든 조건의 수렴 상한으로 일반화하지 않는다.

## 5 Results and analysis

**S078 — Original**

The default ground segment has up to 18 active (transmitting and receiving) gateways distributed across the Earth, mainly following KSAT’s deployment, but more gateways can be added easily.

**S078 — 한국어**

(기본 지상 구간은 주로 KSAT 배치를 따라 전 지구에 분포한 최대 18개의 송수신 활성 gateway를 가지지만, 더 많은 gateway를 쉽게 추가할 수 있다.)

원문 각주: <https://www.ksat.no/services/ground-station-services/>.

**S079 — Original**

Moreover, four real constellations are implemented: (1) Kepler constellation design, with $O=7$ orbital planes at heights $h=600$ km and $N=20$ satellites per orbital plane, as illustrated in Fig. 1; (2) Iridium Next constellation, with $O=6$, $h=780$ km and $N=11$; (3) the OneWeb constellation, with $O=36$, $h=1200$ km and $N=18$; and (4) Starlink orbital shell at $h=550$ km, with $O=72$ and $N=22$.

**S079 — 한국어**

(또한 네 실제 군집을 구현했다. (1) Fig. 1의 Kepler 설계는 O=7개 궤도면, 고도 h=600 km, 면당 N=20개 위성이고, (2) Iridium Next는 O=6, h=780 km, N=11, (3) OneWeb은 O=36, h=1200 km, N=18, (4) Starlink 궤도 shell은 h=550 km, O=72, N=22다.)

**S080 — Original**

The three first constellations follow a Walker star architecture, while the Starlink shell follows a Walker delta architecture [14].

**S080 — 한국어**

(앞의 세 군집은 Walker star 구조를, Starlink shell은 Walker delta 구조를 따른다 [14].)

**S081 — Original**

Moreover, two additional artificial constellations are implemented for testing.

**S081 — 한국어**

(시험을 위해 두 개의 추가적인 인공 군집도 구현했다.)

**S082 — Original**

Additionally, two ISL matching algorithms are implemented: (1) The Markovian solution proposed in [13] and (2) a Greedy approach, where each satellite connects with immediate neighbors within its plane and closest counterparts in adjacent planes in both East and West directions, optimizing for latency and data rates, as shown in Fig. 1.

**S082 — 한국어**

(추가로 (1) [13]의 Markovian 해법과 (2) 각 위성이 같은 면의 바로 이웃 및 동·서쪽 인접 면의 가장 가까운 상대 위성에 연결하여 지연·데이터 속도를 최적화하는 Fig. 1의 Greedy 접근이라는 두 ISL 매칭 알고리즘을 구현했다.)

**S083 — Original**

When a simulation ends, it automatically outputs a set of results in the form of figures and text files (Fig. 2).

**S083 — 한국어**

(시뮬레이션이 끝나면 그림과 텍스트 파일 형태의 결과를 자동 출력한다(Fig. 2).)

**S084 — Original**

Within the figures, a map like Fig. 1 with the system model information is saved.

**S084 — 한국어**

(그림 중에는 시스템 모델 정보를 담은 Fig. 1과 같은 지도를 저장한다.)

**S085 — Original**

An update of this figure is also saved as the constellation moves if desired.

**S085 — 한국어**

(원하면 군집이 이동할 때 갱신한 그림도 저장한다.)

**S086 — Original**

Then, a congestion test per route and for all routes between gateways is done, in order to see what nodes and edges did the packets went through, as shown in Fig. 3.

**S086 — 한국어**

(이후 Fig. 3처럼 패킷이 통과한 노드와 간선을 확인하려고 경로별 및 gateway 간 전체 경로의 혼잡 시험을 수행한다.)

**S087 — Original**

If one of the RL-based routing policies is chosen, one figure with the exploration rate $\epsilon$ and training stamps and another one with the received rewards (Fig. 4) are also saved.

**S087 — 한국어**

(강화학습 정책을 선택하면 탐험률 ε와 학습 시점의 그림, 수신한 보상의 그림(Fig. 4)도 저장한다.)

**S088 — Original**

Other figures saved are related to the average E2E latency vs time vs $\epsilon$, similar to Fig. 5, but with just one routing policy, and to the queue lengths.

**S088 — 한국어**

(Fig. 5와 비슷하되 하나의 라우팅 정책만을 대상으로 한 시간·ε 대비 평균 E2E 지연 그림과 큐 길이 그림도 저장한다.)

**S089 — Original**

On the other hand, the output files include several .csv with extensive information about each packet’s path and its latency, rewards, exploration rates, training stamps, hyper-parameters and a .txt log-file, that saves everything that happened during the simulation and gives some statistics like like the latency broken down by average queue, transmission and propagation times, packets delivered vs stuck and/or lost, most used links, etc.

**S089 — 한국어**

(출력 파일에는 각 패킷의 경로·지연, 보상, 탐험률, 학습 시점, 하이퍼파라미터의 상세 정보를 담은 여러 .csv와 시뮬레이션 사건 및 통계를 저장하는 .txt 로그가 있다. 통계에는 평균 큐·전송·전파 시간으로 분해한 지연, 전달된 패킷 대비 정체되거나 손실된 패킷, 많이 사용한 링크 등이 포함된다.)

**S090 — Original**

Lastly, if either the MA-DRL or the Q-Routing algorithm was chosen for routing, the trained DNNs (57Kb for the Q-Network and 27 Kb for the Q-Target) or Q-Tables (21Kb for 8 active gateways) are saved, respectively.

**S090 — 한국어**

(마지막으로 MA-DRL 또는 Q-routing을 선택하면 각각 학습한 DNN(Q-Network는 57Kb, Q-Target은 27 Kb) 또는 Q-table(활성 gateway 8개에서 21Kb)을 저장한다.)

번역자 주: 원문의 Kb 표기를 보존했다. bit/byte를 임의 변환하거나 peak RAM 사용량으로 해석하지 않는다.

**S091 — Original**

In the Jupyter notebook, we conduct further post-processing analysis and explore more complex results.

**S091 — 한국어**

(Jupyter notebook에서 추가 후처리 분석과 더 복잡한 결과를 살펴본다.)

**S092 — Original**

A comparison between the Shortest path routing policy, Q-Routing [3] and MA-DRL [1, 4] at their offline phase is shown in Fig. 5.

**S092 — 한국어**

(Fig. 5는 최단 경로 정책, Q-routing [3], MA-DRL [1, 4]의 offline 단계 비교를 보여준다.)

**S093 — Original**

Additionally, a dynamic comparison of these policies at their online phase is shown in Fig. 6, where the constellation has moved to complete one orbital period in 96 minutes, with the satellite positions being updated at intervals of 15 seconds.

**S093 — 한국어**

(Fig. 6은 이 정책들의 online 단계 동적 비교를 보여준다. 군집은 96분 동안 한 궤도 주기를 완료하도록 이동하며 위성 위치는 15초 간격으로 갱신된다.)

**S094 — Original**

Notably, even with only partial knowledge of the constellation, MA-DRL consistently maintains the baseline latency obtained with the Shortest path policy, which has full knowledge of the constellation.

**S094 — 한국어**

(주목할 점은 군집을 부분적으로만 알고도 MA-DRL이 전체 정보를 가진 최단 경로 정책의 기준 지연을 지속적으로 유지한다는 것이다.)

**S095 — Original**

Moreover, we elaborate on the comparison of the four architectures in Fig. 7, where the distribution of the E2E latency is depicted in a box plot when the Shortest path is applied among one orbital period too.

**S095 — 한국어**

(Fig. 7에서는 네 구조를 더 자세히 비교하며, 역시 한 궤도 주기에 최단 경로 정책을 적용한 E2E 지연 분포를 상자그림으로 나타낸다.)

**S096 — Original**

We observe that Kepler and Starlink obtain the smallest average latency, although the latter presents more outliers.

**S096 — 한국어**

(Kepler와 Starlink의 평균 지연이 가장 작지만, 후자인 Starlink에는 이상치가 더 많음을 관찰한다.)

**S097 — Original**

This figure helps to illustrate the behavior of the constellations and highlights the usage of the simulator to test different constellation architectures.

**S097 — 한국어**

(이 그림은 군집들의 동작을 설명하고 서로 다른 군집 구조를 시험하는 시뮬레이터의 활용을 보여준다.)

**S098 — Original**

Additionally, as in MA-DRL, each satellite is an independent agent during the online phase, we conducted a Centered Kernel Alignment (CKA) [15] analysis to compare the differences between each agent’s local model after 1 second with varying traffic patterns around the globe.

**S098 — 한국어**

(MA-DRL의 online 단계에서 각 위성은 독립 에이전트이므로, 전 지구적으로 다른 트래픽 패턴을 적용한 1초 뒤 각 에이전트 로컬 모델의 차이를 비교하려고 중심화 커널 정렬 분석 [15]을 수행했다.)

- **용어·약어 해설**: CKA (Centered Kernel Alignment, 중심화 커널 정렬)는 신경망 표현의 유사성을 비교하는 도구다. 모델이 비슷하다는 것과 라우팅 성능이 좋다는 것은 같은 지표가 아니다.

**S099 — Original**

Each satellite learns and adapts its routing decisions based on these traffic patterns, resulting in distinct updates to their local models.

**S099 — 한국어**

(각 위성은 이 트래픽 패턴에 따라 라우팅 결정을 학습·적응시키므로 로컬 모델에 서로 다른 갱신이 생긴다.)

**S100 — Original**

Consequently, these models exhibit differences.

**S100 — 한국어**

(그 결과 모델들 사이에 차이가 나타난다.)

**S101 — Original**

To homogenize the models, we applied post-processing SFL techniques: Initially among neighboring satellites, Model Anticipation; then, among orbital planes, Orbital Plane Aggregation (SFL); and finally, across the entire constellation, Full Aggregation (SFL) [1].

**S101 — 한국어**

(모델을 균질화하려고 후처리 SFL 기법을 적용했다. 먼저 이웃 위성 사이의 Model Anticipation, 다음으로 궤도면들 사이의 Orbital Plane Aggregation(SFL), 마지막으로 군집 전체의 Full Aggregation(SFL)을 적용했다 [1].)

번역자 주: 구체 집계 알고리즘은 이 짧은 논문이 아니라 참고문헌 [1]에서 확인해야 한다. 이 문장은 online 집계를 이미 구현했다는 뜻이 아니다.

### Figure 6–7

**S102 — Original**

Average E2E latency over an orbital period.

**S102 — 한국어**

(한 궤도 주기 동안의 평균 E2E 지연.)

**S103 — Original**

The fluctuations are given by the movement of the satellites and the resulting changes in the routed followed by the packets.

**S103 — 한국어**

(변동은 위성의 이동과 그에 따라 패킷이 따라가는 경로가 바뀌기 때문에 나타난다.)

번역자 주: 원문의 `routed`는 문맥상 `routes`로 해석했다.

**S104 — Original**

Box plot of the E2E latency of the four constellation topologies with the Shortest Path policy after one orbital period is completed.

**S104 — 한국어**

(한 궤도 주기를 마친 뒤 최단 경로 정책을 적용한 네 군집 토폴로지의 E2E 지연 상자그림.)

## 6 Conclusion and Future work

**S105 — Original**

The development of an open source MA-DRL simulator for satellite network routing provides a robust platform for testing and implementing various routing algorithms in Python, where different machine learning libraries can be leveraged.

**S105 — 한국어**

(위성망 라우팅용 오픈소스 MA-DRL 시뮬레이터 개발은 여러 머신러닝 라이브러리를 활용해 Python에서 다양한 라우팅 알고리즘을 구현·시험할 수 있는 견고한 플랫폼을 제공한다.)

**S106 — Original**

The simulator’s high configurability and realism allows for comprehensive evaluation of different constellation designs and communication setups.

**S106 — 한국어**

(시뮬레이터의 높은 설정 자유도와 현실성은 서로 다른 군집 설계와 통신 설정을 포괄적으로 평가할 수 있게 한다.)

**S107 — Original**

The results highlight the effectiveness of RL-based routing policies compared to traditional methods, demonstrating significant improvements in E2E latency and overall network performance.

**S107 — 한국어**

(결과는 전통적 방법 대비 강화학습 라우팅의 효과를 보여주며, E2E 지연과 전체 네트워크 성능의 상당한 개선을 나타낸다.)

**S108 — Original**

Future directions include: (1) Developing an SFL framework to enable aggregation during the online phase of MA-DRL rather than implementing it as a post-processing analysis; (2) implementing a two-tier mesh network for UE-satellite-UE communications, enabling ground moving users to connect directly to satellites without the need for gateways; (3) increase the complexity of satellites with regenerative capabilities; and (4) implementing different types of traffic with splittable flows.

**S108 — 한국어**

(향후 방향은 (1) 후처리 분석이 아니라 MA-DRL online 단계에 집계할 수 있는 SFL 체계, (2) gateway 없이 지상의 이동 사용자가 위성에 직접 연결하는 UE–satellite–UE용 2계층 메시망, (3) 재생 기능을 가진 위성의 복잡성 확대, (4) 분할 가능한 흐름을 포함한 다양한 트래픽 유형 구현이다.)

- **용어·약어 해설**: UE (User Equipment, 사용자 단말)는 여기서 지상 사용자 측 장비다. 재생 기능(regenerative capabilities)은 단순 신호 전달을 넘어 위성에서 통신 신호를 처리·재생하는 기능을 뜻한다. splittable flow는 한 트래픽 흐름을 여러 경로 등으로 나눌 수 있는 경우다.

## 수식·그림 해설 — 번역자 추가

원문 수식은 본문 안에 있는 $\mathcal{G}_t(\mathcal{N},\mathcal{E})$, $U_f=n_g(n_g-1)$, $w_{i,j}=1/R(i,j)$, 거리 $\lVert ij\rVert$, 버퍼 $Q^{\max}$ 등이다. 별도 번호 식·tensor shape·pseudocode는 없다. 1/R은 R>0에서 정의되며 연결 불가인 R=0은 최단 경로 계산에서 제외해야 한다. 논문에 없는 Bellman 식을 원문 식처럼 붙이지 않았다.

| 그림 | 확인한 내용 | 읽는 방법 |
| --- | --- | --- |
| 1 | 지상 지도·gateway·위성·ISL | 녹색은 인구, 위성 색은 궤도면으로 서로 다른 범례 |
| 2 | a–e 설정→f simulator→g 결과 | 입력을 바꾸면 결과 조건도 달라지므로 설정을 함께 저장 |
| 3 | 사용된 링크의 상대 트래픽 부하 | 선 색이 경로 성능 전체나 전달 성공률은 아님 |
| 4 | 평균·상위·하위 보상 추이, ms 축 | 높은 보상과 낮은 지연의 관계는 reward 설계에 의존 |
| 5 | E2E ms, simulation time ms, ε 보조축 | 탐험 감소와 지연 변화를 함께 읽되 인과관계를 과장하지 않음 |
| 6 | 96분 궤도에서 동적 지연 변화 | 평균 하나만으로 큐 tail/실패를 숨기지 않음 |
| 7 | 네 군집의 상자·수염·이상치 | 평균 표기 46.5 / 50.5 / 51.7 / 45.7 ms와 분포를 함께 읽음 |

그림 원본은 출판 PDF를 참조한다. 수치가 인쇄되지 않은 곡선 전체를 digitize하거나 임의의 표로 복원하지 않았다. Fig. 5의 “최적 경로”는 해당 실험 문맥이며 모든 정책·부하에 대한 수학적 보장이 아니다.

## 약어 및 기술 용어 사전

| 원어 | 한국어·의미 | 최초 ID |
| --- | --- | --- |
| Multi-agent / deep reinforcement learning | 여러 의사결정 주체 / 신경망 기반 강화학습 | S001 |
| LSatCs, Low Earth Orbit Satellite Constellations | 저궤도 위성 군집; 동적 망의 위성 구성 | S002 |
| Packet | 패킷; 추적하는 데이터 객체 | S002 |
| MA-DRL, Multi-Agent Deep Reinforcement Learning | 위성별 심층강화학습 | S003 |
| Q-routing / Q-table | 다음 홉의 값을 학습 / 이를 저장한 표 | S003 |
| Dijkstra | 비음수 가중치 최단 경로 알고리즘 | S003 |
| SimPy / discrete event | 사건 시간으로 진행하는 시뮬레이션 | S004 |
| Topology / hyperparameter | 망 연결 구조 / 학습 과정 설정 | S005 |
| E2E, End-to-End | 종단 간 지연 범위 | S007 |
| RL, Reinforcement Learning | 환경 피드백을 통한 정책 학습 | S007 |
| 6G, Sixth Generation | 미래 전 지구 연결성의 이동통신 배경 | S009 |
| SFL, Satellite Federated Learning | 위성 모델 집계; 본 논문은 후처리 분석 | S015 |
| Continual learning | 변화에 따라 지식을 계속 갱신 | S015 |
| ISL, Inter-Satellite Link | 위성 간 링크 | S017 |
| Greedy matching | 현재 기준에 유리한 링크를 선택하는 매칭 | S017 |
| Transmission / propagation / queue time | 전송 / 전파 / 대기 시간 | S023 |
| GSL, Ground-to-Satellite Link | 지상–위성 링크 | S026 |
| RF, Radio Frequency | 무선 주파수 통신 | S026 |
| FSO, Free Space Optical | 자유공간 광통신 | S026 |
| SNR, Signal-to-Noise Ratio | 신호 대 잡음비; 링크 속도 선택 근거 | S038 |
| DVB-S2 | 2세대 위성 디지털 방송 규격; 속도 모델 | S038 |
| FIFO, First-In First-Out | 선입선출 버퍼 | S044 |
| HoL, Head of Line | 큐에서 다음에 처리할 맨 앞 패킷 | S045 |
| Slant range / hop | 노드 간 거리 / 링크 통과 횟수 | S057 |
| DNN, Deep Neural Network | Q 값을 표현하는 심층신경망 | S064 |
| DDQN, Double Deep Q-Learning | 행동 선택·평가를 분리하는 Q학습 | S065 |
| ε / α / γ | 탐험 / 학습률 / 할인율 | S073 |
| Walker delta / star | 위성 군집 배치 구조 | S073 |
| CKA, Centered Kernel Alignment | 로컬 모델 표현의 유사성 비교 | S098 |
| Model Anticipation / Orbital Plane Aggregation / Full Aggregation | 이웃 / 궤도면 / 전체 군집의 후처리 집계 기법 | S101 |
| UE, User Equipment | 사용자 단말 | S108 |
| Regenerative / splittable flow | 신호 처리·재생 / 분할 가능한 흐름 | S108 |

## References — 원문 서지 정보

1. Lozano-Cuadra, F., Soret, B., Leyva-Mayorga, I. & Popovski, P. *Continual Deep Reinforcement Learning for Decentralized Satellite Routing*. arXiv preprint [arXiv:2405.12308](https://arxiv.org/abs/2405.12308) (2024).
2. Dijkstra, E. W. *A note on two problems in connexion with graphs*. Numerische mathematik 1, 269–271 (1959).
3. Soret, B., Leyva-Mayorga, I., Lozano-Cuadra, F. & Thorsager, M. D. *Q-learning for distributed routing in LEO satellite constellations* in Proc. IEEE ICMLCN 2024, arXiv preprint [arXiv:2306.01346](https://arxiv.org/abs/2306.01346) (2023).
4. Lozano-Cuadra, F. & Soret, B. *Multi-Agent Deep Reinforcement Learning for Distributed Satellite Routing* in Proc. IEEE ICMLCN 2024, arXiv preprint [arXiv:2402.17666](https://arxiv.org/abs/2402.17666) (2024).
5. Lozano-Cuadra, F., Thorsager, M. D., Leyva-Mayorga, I. & Soret, B. *MA-DRL Routing Simulator*. [GitHub](https://github.com/SatCom-TELMA/MA-DRL_Routing_Simulator). 2024.
6. Center for International Earth Science Information Network - CIESIN - Columbia U. *Gridded Population of the World, Version 4 (GPWv4)*. [Source](https://sedac.ciesin.columbia.edu/data/collection/gpw-v4/sets/browse).
7. Zinoviev, D. *Discrete Event Simulation: It’s Easy with SimPy!* arXiv preprint [arXiv:2405.01562](https://arxiv.org/abs/2405.01562) (2024).
8. *Digital Video Broadcasting (DVB); Second generation framing structure, channel coding and modulation systems for broadcasting, interactive services, news gathering and other broadband satellite applications (DVB-S2)*. Standard (ETSI, France, Oct. 2014).
9. Rabjerg, J. W., Leyva-Mayorga, I., Soret, B. & Popovski, P. *Exploiting topology awareness for routing in LEO satellite constellations* in Proc. IEEE GLOBECOM (2021).
10. Van Der Walt, S., Colbert, S. C. & Varoquaux, G. *The NumPy array: a structure for efficient numerical computation*. Computing in science & engineering 13, 22–30 (2011).
11. Ketkar, N. & Ketkar, N. *Introduction to keras*. Deep learning with python: a hands-on introduction, 97–111 (2017).
12. Van Hasselt, H., Guez, A. & Silver, D. *Deep reinforcement learning with double q-learning* in Proceedings of the AAAI conference on artificial intelligence 30 (2016).
13. Leyva-Mayorga, I., Soret, B. & Popovski, P. *Inter-Plane Inter-Satellite Connectivity in Dense LEO Constellations*. IEEE Trans. on Wireless Comms. 20, 3430–3443. ISSN: 1536-1276 (6 June 2021).
14. Leyva-Mayorga, I. et al. *NGSO constellation design for global connectivity*. arXiv preprint [arXiv:2203.16597](https://arxiv.org/abs/2203.16597) (2022).
15. Kornblith, S., Norouzi, M., Lee, H. & Hinton, G. *Similarity of neural network representations revisited* in International conference on machine learning (2019), 3519–3529.

## 번역 검수 기록

- PDF 5쪽을 렌더링해 단 순서, 페이지 경계, Fig. 1–7, CC BY 고지를 확인했다. 분철만 합쳤고 반복 header/footer는 본문에서 제거했다.
- 108개 Original/한국어 쌍의 ID 연속성·대응 여부를 자동 검사한다. 제목·caption·문장 조각도 각각 하나의 ID로 관리한다.
- N과 ℓ 표기의 모호함, Kb 단위, Fig. 6 `routed` 오기, 과도하게 일반화하기 쉬운 성능 주장을 번역자 주로 분리했다.
- 수식의 인용 번호는 원문 그대로 유지했다. 원문에 없는 학습 알고리즘의 상세 상태·보상·네트워크 구조를 추측해 번역하지 않았다.
- 저자 소속·지원 각주는 요약한 부분 번역이며 본문 전체 번역과 구분한다. 저자 검수 번역은 아니다.
