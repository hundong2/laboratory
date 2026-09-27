# 위성망 MA-DRL 라우팅 시뮬레이터 논문 학습

작성일·확인일: 2026-09-27

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [핵심 요약](#핵심-요약)
- [상세 정리](#상세-정리)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)
- [검증 기록](verification.md)

## 출처와 작업 범위

입력은 논문 URL이며 저장소 규칙에 따라 논문 해설·번역·교육용 실습 요청으로 해석했다. GitHub submodule 작업이 아니다.

- 입력: [arXiv:2407.11047](https://arxiv.org/abs/2407.11047), 최신 표시 버전 v2(2024-11-28).
- 제목: *An open source Multi-Agent Deep Reinforcement Learning Routing Simulator for satellite networks*.
- 저자: Federico Lozano-Cuadra, Mathias D. Thorsager, Israel Leyva-Mayorga, Beatriz Soret.
- 사용 원문: [SPAICE2024 학회 출판본](https://doi.org/10.5281/zenodo.13885645), pp. 420–424, 2024. [공식 PDF](https://zenodo.org/records/13885645/files/An%20open%20source%20MultiAgent%20Deep%20Reinforcement%20Learning%20Routing%20Simulator%20for%20satellite%20networks.pdf).
- arXiv의 비독점 배포권과 별개로 **출판본 각 페이지에 CC BY 4.0**이 명시되어 있다. 접근 가능한 최종 출판본을 우선하여 5쪽 전체 본문·그림 7개를 확인했다. arXiv v2 HTML과 제목·저자·핵심 내용을 대조했지만 두 버전의 바이트 단위 동일성을 주장하지 않는다.
- [문장 대조 번역](<An open source Multi-Agent Deep Reinforcement Learning Routing Simulator for satellite networks.번역.md>): 출판본을 바탕으로 원문→한국어→용어 해설 순서로 읽는다. 번역은 저자의 검수를 받지 않은 2차 저작물이다.
- [저자 공식 코드](https://github.com/SatCom-TELMA/MA-DRL_Routing_Simulator)는 README에서 실행 경로만 보조 확인했다. clone·submodule 추가·학습 실행·코드 전체 감사를 하지 않았다.

## 한눈에 보기

후속 GitHub 요청으로 [코드 저장소 한국어 가이드·실습·아키텍처](https://github.com/hundong2/MA-DRL_Routing_Simulator/blob/d6b05a0c16d7ad5bd1a2b38f5a400d4e793bcb87/guide/README.md)를 별도로 추가했다. 위 출처 항목은 논문 자료 작성 당시의 범위다. 후속 코드 분석에서는 현재 `DDQNAgent.train`과 표준 DDQN 식의 차이를 확인했으므로 논문 서술과 최신 구현이 동일하다고 전제하지 않는다. 아래 노트북은 계속 독립 toy 실습이다.

**연구 질문:** 위성이 움직이고 트래픽이 변하며 각 위성이 전체 망을 알지 못할 때, 라우팅 정책을 어떻게 패킷 단위로 비교할 것인가?

이 논문의 주된 기여는 새로운 학습 규칙 자체보다 **비교·학습·분석을 위한 공개 시뮬레이터**다. SimPy 기반 패킷 이벤트에 궤도·링크 갱신과 학습 정책을 연결한다. Dijkstra 계열과 기존 Q-routing·MA-DRL을 같은 환경에서 평가한다. 초록의 성능 개선 주장을 모든 환경에서 Dijkstra보다 우수하다는 정리로 읽지 않는다. 본문의 동적 실험은 MA-DRL이 전역 정보를 가진 최단 경로 기준 지연을 유지한다는 설명이다. [출판본, §§1–6](https://doi.org/10.5281/zenodo.13885645)

## 기초 개념

### 거리가 짧아도 늦을 수 있다

패킷 하나의 링크 통과 지연을 교육용으로 다음처럼 나눌 수 있다.

$$d_{ij}=q_{ij}+\frac{L}{R_{ij}}+\frac{r_{ij}}{c}.$$

q는 큐에서 기다린 초, L은 bit, R은 bit/s, r은 m, c는 m/s다. L/R은 패킷의 모든 bit를 링크에 밀어 넣는 **전송 지연**, r/c는 신호가 이동하는 **전파 지연**이다. 논문의 서술을 수식으로 정리한 것으로 논문에 번호가 붙은 원식은 아니다.

예컨대 1,500 byte, 10 Mbit/s, 1,000 km라면 큐가 없어도 약 4.536 ms다. 같은 거리를 가더라도 큐에서 20 ms 기다리면 이 값보다 훨씬 커진다. 이 수치는 논문 실험 설정이 아니라 학습용이다.

### 이벤트 시간과 실제 실행 시간

이산사건 시뮬레이터는 매 1 ns마다 망 전체를 갱신하지 않는다. 패킷 생성, 전송 완료, 도착 같은 다음 사건으로 시간을 건너뛴다. 따라서 그림의 “1초 안에 학습”은 시뮬레이션 축의 시간이며 일반 PC에서 wall-clock 1초 만에 모델 학습이 끝난다는 뜻이 아니다.

### Q 값의 부호

비용 형태 Q-routing은 앞으로 걸릴 지연을 추정하므로 **작을수록 좋다**. 보상 형태 DQN은 누적 보상을 최대화하므로 보통 **클수록 좋다**. 둘의 `min`과 `max`를 섞으면 잘못된 정책을 학습한다. 아래 실습은 비용 형태의 표 기반 Q-routing이며 논문의 DDQN 신경망을 대체하지 않는다.

## 핵심 요약

| 비교 대상 | 목적·정보 | 읽을 때 주의점 |
| --- | --- | --- |
| Dijkstra, 가중치 1/R | 고속 링크를 선호하는 전역 경로 | 동일 패킷 길이라면 L/R 합 최소화와 연결되지만 큐는 무시 |
| Dijkstra, 거리 | 전파 거리 합 최소화 | 거리와 전체 지연은 다름 |
| Dijkstra, hop | 링크 수 최소화 | 느리거나 혼잡한 링크도 선택 가능 |
| Q-routing | Q-table로 다음 홉 평가 | 탐험 비용·반복 경로·정보 지연 고려 |
| MA-DRL | 위성별 학습 정책, DNN·선택적 DDQN | 학습·통신 비용과 부분 관측 조건을 함께 평가 |

위 표의 알고리즘 분류는 출판본 §3, 부가 해석은 학습용 설명이다. 선행 [3] Q-routing, [4] MA-DRL, [1] continual learning을 통합·평가하는 것이 이 시뮬레이터 논문의 위치다.

## 상세 정리

### 환경·데이터·실험

공개 벤치마크 데이터셋의 accuracy 경쟁이 아니다. 지상 gateway, 인구 지도, 위성 배치, 생성 트래픽으로 패킷 경로·지연을 생성하는 시뮬레이션이다. 입력과 학습 seed, 초기 큐 상태, simulation horizon을 함께 보존해야 결과를 비교할 수 있다.

논문은 gateway 18개까지의 기본 구성, FIFO 유한 버퍼, Poisson 생성, 링크 갱신 시 기존 큐 유지, 4개의 모델링된 군집을 설명한다. 아래 값은 **2024 논문 시나리오**이며 현재 운용 중인 전체 상용 위성망의 상태가 아니다. [출판본, §§2·5](https://doi.org/10.5281/zenodo.13885645)

| 모델 | 궤도면 O | 면당 위성 N (§5 표기) | 고도 km | 논문 설계 |
| --- | ---: | ---: | ---: | --- |
| Kepler | 7 | 20 | 600 | Walker star |
| Iridium Next | 6 | 11 | 780 | Walker star |
| OneWeb | 36 | 18 | 1200 | Walker star |
| Starlink shell | 72 | 22 | 550 | Walker delta |

§2는 N을 전체 위성 수처럼 정의하고 §5는 면당 위성 수로 사용한다. 번역에서 이를 숨기지 않았다. 모델을 구현할 때 `planes`, `satellites_per_plane`, `total_satellites`를 별도 이름으로 두는 편이 안전하다.

### 결과를 과장하지 않고 읽기

- Fig. 5: 특정 Malaga–Los Angeles/Starlink offline 시나리오에서 지연이 감소한다. 일반적인 수렴 보장은 아니다.
- Fig. 6: 96분 한 궤도, 위치 갱신 15초의 동적 평가. 전역 최단 경로와 부분 정보 MA-DRL의 지연을 비교한다.
- Fig. 7의 평균 표기: Kepler **46.5 ms**, Iridium Next **50.5 ms**, OneWeb **51.7 ms**, Starlink **45.7 ms**. PDF 그림에서 읽은 수치다. 모든 트래픽·gateway 배치의 보편적 순위가 아니다.
- CKA는 각 로컬 모델의 표현 유사성 분석이지 패킷 전달률 자체가 아니다. 논문에서 SFL은 후처리 분석이며 온라인 집계 체계는 향후 과제로 명시된다.

### 한계와 재현 체크리스트

**저자 명시 향후 과제:** online SFL, gateway 없는 UE–satellite–UE, 재생 중계 기능 복잡화, 분할 가능한 트래픽. **학습자 관점의 추가 점검:** 학습 seed 반복, confidence interval, 드롭·미완료 패킷, max-hop 방어, 링크 전환 중 패킷 처리, 지상 구간/연산 지연 모델 포함 여부다. 이 점검 목록은 논문의 실험 결과가 아니다.

도착한 패킷만 평균내면 느린 패킷이 simulation 끝에 남아 점수가 좋아 보일 수 있다. 평균·p95와 함께 **생성/수용/드롭/완료/미완료 수**를 기록한다. 제어 정책 비교에는 같은 arrival trace를 재사용하되, 다른 부하 실험을 합쳐 독립 반복처럼 취급하지 않는다.

공식 README는 `Simulation.py`와 `SimulationRL.py`, `input.csv`/`inputRL.csv`, Python 3.9.12 권장과 별도 requirements를 안내한다. 논문 시대 의존성을 현재 환경에 무작정 설치하지 말고 별도 가상환경·commit 고정·데이터 준비부터 확인한다. 이 작업은 upstream 시뮬레이터를 실행하지 않았다. [공식 실행 안내](https://github.com/SatCom-TELMA/MA-DRL_Routing_Simulator#usage)

## 용어 정리

| 용어 | 쉬운 뜻 |
| --- | --- |
| LSatC / LEO | 저궤도 위성 군집 / 저궤도 |
| ISL / GSL | 위성 간 링크 / 지상–위성 링크 |
| FIFO / HoL | 먼저 온 패킷을 먼저 처리 / 큐 맨 앞 패킷 |
| E2E | 출발지부터 목적지까지의 전체 경로 |
| ε / α / γ | 탐험 확률 / 학습률 / 할인율 |
| DDQN | 행동 선택과 값 평가를 분리하는 Deep Q-learning 변형 |
| CKA / SFL | 표현 유사성 분석 / 위성 연합학습 |

전체 문맥별 정의와 최초 등장 ID는 [번역 파일](<An open source Multi-Agent Deep Reinforcement Learning Routing Simulator for satellite networks.번역.md>) 끝에 있다.

## 실습 학습 가이드

세 notebook은 외부 저장소·데이터·GPU 없이 **Python 표준 라이브러리만** 사용한다. Python 3.10 이상 권장. Jupyter를 이용한다면 별도 가상환경에서 `python -m pip install notebook` 후 열고 위에서부터 실행한다. 패키지 없는 검증은 `python verify_notebooks.py`로 가능하다.

| 실습 | 목표 | 원 논문과의 차이 |
| --- | --- | --- |
| [01_foundations.ipynb](01_foundations.ipynb) | 단위·3가지 가중치·Dijkstra | 고정된 4-node 합성 그래프 |
| [02_practice.ipynb](02_practice.ipynb) | Poisson 도착·유한 FIFO·지연 분해 | 단일 링크, heapq 이벤트 엔진; SimPy/위성 궤도 미사용 |
| [03_advanced.ipynb](03_advanced.ipynb) | 비용 Q-routing·학습/평가 분리·토폴로지 변화 | 표 기반, 신경망/DDQN/SFL 미구현 |

**원 논문 성능 재현이 아니라 핵심 원리를 검증하는 toy reproduction**이다. 모든 notebook에 목표·가정·assert·확장 과제가 있다. 난수 seed는 고정하며 자동 검증은 각 notebook을 독립 namespace에서 실행한다. 출력은 논문 수치와 분리한다.

## 다음 학습 경로

1. 그래프 최단 경로와 단위 분석 → 01에서 세 정책의 경로가 달라지는 이유를 설명한다.
2. 대기행렬과 이산사건 모델 → 02에서 offered load를 높이고 drop 및 tail latency를 관찰한다.
3. Bellman update와 탐험 → 03에서 stale Q 값과 새 링크의 학습을 분리한다.
4. 논문의 참고문헌 [3] → [4] → [1] 순서로 Q-routing, MA-DRL, continual learning을 읽는다. 참고 URL은 번역 파일에 보존했다.
5. 공식 구현의 특정 revision·환경·데이터를 고정한 뒤 original benchmark를 별도 재현한다. 이후에야 신경망 크기·학습 비용·SFL 통신량을 포함한 공정 비교를 설계한다.
