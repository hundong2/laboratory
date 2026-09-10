# 위성 통신 실습 가이드

작성일: 2026-09-10

## 목표

문서의 공식을 직접 계산하고, 시간에 따라 바뀌는 위성망의 routing·buffer·protocol 선택을 작은 simulation으로 검증한다. 세 notebook은 Python 표준 라이브러리만 사용하며 앞에서부터 순서대로 실행한다.

## 실행

```bash
jupyter lab
```

Jupyter에서 이 폴더를 열고 `Kernel > Restart Kernel and Run All Cells`를 실행한다. Python 3.10 이상을 권장한다. notebook은 외부 network, 실제 spacecraft data, third-party package에 의존하지 않는다.

## 학습 순서

### 1. [기초: 링크와 지연](01_foundations.ipynb)

- dB/dBm을 선형 전력과 변환
- LEO/GEO/Moon의 propagation delay와 RTT 비교
- FSPL, C/N0, Eb/N0, link margin 계산
- Shannon capacity와 BDP 계산
- 질문: bit rate를 2배로 하면 link margin과 window는 어떻게 바뀌는가?

### 2. [응용: contact·routing·failover](02_practice.ipynb)

- contact window usable capacity 계산
- time-aware earliest-arrival route 구현
- primary link degradation에서 hysteresis failover
- onboard buffer backlog simulation
- 질문: 가장 빠른 route와 가장 안전한 route가 왜 다른가?

### 3. [심화: reliability와 protocol](03_advanced.ipynb)

- CRC 생성·검증과 bit flip 탐지
- segmentation 크기에 따른 전체 성공률·overhead
- BDP 기반 sliding window 크기
- CoAP Blockwise transfer 분할
- FEC/ARQ 기대 전송량 toy model
- DTN deadline/priority scheduler
- 질문: 큰 block이 언제 유리하고 언제 loss amplification을 만드는가?

## 실험 확장

1. 실제 TLE(Two-Line Element, 2행 궤도요소)와 orbit library를 사용해 contact를 만든다.
2. elevation-dependent range와 atmospheric loss를 link budget에 넣는다.
3. optical link에 cloud probability와 PAT acquisition distribution을 추가한다.
4. contact plan version mismatch와 clock drift fault를 주입한다.
5. CFDP/BPv7 구현과 packet capture를 notebook model과 비교한다.

학습을 마친 뒤 [실무 산출물 패키지](../deliverables/README.md)에서 같은 계산을 ICD, 링크 버짓, 성능 모델, 시험 절차와 요구사항 추적성으로 확장한다.

## 한계

모든 계산은 교육용 모델이다. antenna pattern, polarization, implementation loss, regulatory mask, hardware nonlinearity, accurate orbit propagation을 생략했다. 수치 결과가 비행 적합성이나 인증을 증명하지 않는다.

[← 메인 문서](../README.md)
