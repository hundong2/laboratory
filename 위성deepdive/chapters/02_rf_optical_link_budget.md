# 02. RF·FSO·ISL과 링크 버짓

## 1. 왜 RF와 optical ISL이 탄생했는가

단일 위성이 지상국 위를 지나갈 때만 데이터를 내리면 관측에서 전달까지 수십 분 이상 걸릴 수 있다. ISL(Inter-Satellite Link, 위성간 링크)은 다른 위성을 relay로 사용해 가시권 밖에서도 데이터를 전달하고, 지상국 수요를 줄이며, 군집을 하나의 네트워크로 만든다.

RF(Radio Frequency, 무선주파수) ISL은 성숙한 변조·안테나·추적 기술과 넓은 beam을 활용한다. Optical ISL 또는 OISL(Optical Inter-Satellite Link)은 데이터 폭증과 RF spectrum 희소성에 대응하기 위해 짧은 파장의 매우 좁은 laser beam을 사용한다. NASA의 2026 Small Spacecraft 보고서는 RF와 FSO(Free-Space Optical, 자유공간 광통신)를 소형위성 통신의 두 축으로 다룬다.

## 2. RF ISL

### 송수신 사슬

```text
bits -> FEC -> framing -> modulation -> up-conversion -> PA -> antenna
     free-space path
antenna -> LNA -> down-conversion -> synchronization -> demodulation -> FEC -> bits
```

- **PA (Power Amplifier, 전력 증폭기)**: 송신 신호 전력을 높인다.
- **LNA (Low-Noise Amplifier, 저잡음 증폭기)**: 수신기의 첫 증폭기로 noise figure가 중요하다.
- **modulation(변조)**: bit를 phase, frequency, amplitude 변화로 표현한다.
- **FEC (Forward Error Correction, 전방 오류 정정)**: 추가 parity를 보내 수신측이 재전송 없이 일부 오류를 고친다.

### 장단점

장점은 넓은 beam에 따른 획득 용이성, cloud 영향이 거의 없음, 성숙한 부품·시험법이다. 단점은 spectrum coordination, 상대적으로 큰 안테나 또는 낮은 data rate, 간섭·재밍 노출, 동일 aperture에서 optical보다 넓은 beam이다.

위성간은 대기가 없어 rain fade가 없지만, Doppler, antenna pointing, polarization mismatch, oscillator stability, 다른 위성 간섭은 남는다.

## 3. FSO와 Optical ISL

**FSO (Free-Space Optical communication, 자유공간 광통신)** 또는 lasercom은 광섬유가 아니라 자유공간을 통해 laser를 보낸다. 1064 nm와 1550 nm 부근이 대표적이다.

### PAT: 가장 중요한 제어 고리

1. **pointing(지향)**: 궤도·자세 정보로 상대 방향을 예측한다.
2. **acquisition(획득)**: 상대 terminal beacon을 탐색해 최초 lock을 건다.
3. **tracking(추적)**: fine steering mirror와 sensor로 좁은 beam을 계속 맞춘다.

beam divergence가 작을수록 receiver에 집중되는 전력은 늘지만 pointing error 허용치는 작아진다. spacecraft jitter, thermoelastic distortion(열탄성 변형), orbit ephemeris error, terminal alignment가 link outage로 직결된다.

### optical link의 손실

- diffraction/geometric loss: beam 확산과 aperture 크기
- pointing loss: 중심에서 벗어난 정도
- optical train loss: lens, mirror, filter, coupling
- detector sensitivity와 background light
- space-ground link일 때 cloud, turbulence, scintillation, atmospheric absorption

OISL은 대기 손실이 없지만 PAT와 terminal thermal control이 어렵다. OGSL(Optical Ground-to-Space Link)은 cloud diversity를 위해 여러 광 지상국과 weather-aware scheduling이 필요하다.

### 왜 유망한가

광주파수의 거대한 가용 대역, 작은 beam에 따른 공간 재사용과 낮은 탐지·간섭 가능성, 작은 aperture로 높은 gain을 얻는 점이 장점이다. 다만 `optical = secure`는 과장이다. 좁은 beam은 도청·재밍 난도를 높일 뿐, endpoint compromise, key theft, malicious routing을 막지 않으므로 암호와 인증은 별도다.

## 4. RF 대 FSO 선택

| 기준 | RF | FSO/laser |
|---|---|---|
| 획득·추적 | 상대적으로 관대 | 정밀 PAT 필수 |
| 처리율 잠재력 | 중~고 | 매우 높음 |
| 규제 spectrum | 허가·조정 필요 | 현행 RF와 다른 규제 환경, 안전·정책 확인 필요 |
| 기상(지상 링크) | 주파수별 rain 영향 | cloud에 매우 취약 |
| 간섭·재밍 | 비교적 넓은 노출 | 좁은 beam으로 난도 상승 |
| SWaP | 주파수·성능에 따라 | terminal·PAT가 지배 가능 |
| 성숙도 | 높음 | 빠르게 성숙, 상호운용이 핵심 |

**SWaP (Size, Weight and Power, 크기·무게·전력)** 또는 SWaP-C(+Cost)는 탑재 선택의 핵심 지표다. 실무적으로는 RF를 command/safe-mode 저속 생존 링크로, optical을 payload·backhaul 고속 링크로 두는 hybrid가 강하다.

## 5. 링크 버짓

링크 버짓은 송신 전력에서 모든 gain을 더하고 loss를 빼 수신 전력 또는 `Eb/N0`를 계산하는 회계표다.

### EIRP

**EIRP (Effective Isotropic Radiated Power, 등가 등방 복사 전력)**:

```text
EIRP[dBW] = transmitter power[dBW] - transmitter losses[dB] + transmit antenna gain[dBi]
```

`dBi`는 isotropic antenna 대비 gain이다. EIRP는 실제 PA 전력과 같지 않다.

### FSPL

**FSPL (Free-Space Path Loss, 자유공간 경로 손실)**:

```text
FSPL[dB] = 20 log10(4πd/λ)
         = 92.45 + 20 log10(d_km) + 20 log10(f_GHz)
```

거리 두 배면 6.02 dB 증가, 주파수 두 배면 같은 aperture gain을 고려하지 않은 등방 기준 FSPL은 6.02 dB 증가한다. `주파수가 높아 항상 불리하다`는 결론은 antenna aperture gain을 함께 보지 않으면 불완전하다.

### G/T

**G/T (Gain-to-Noise-Temperature ratio, 이득 대 잡음온도비)**는 수신 시스템 품질이다.

```text
G/T[dB/K] = receive antenna gain[dBi] - 10 log10(system noise temperature[K])
```

antenna gain만 높아도 LNA와 sky/background가 뜨거우면 수신 품질은 나쁘다.

### C/N0와 Eb/N0

**C/N0 (Carrier-to-Noise-Density ratio, 반송파 대 잡음전력밀도비)**:

```text
C/N0[dB-Hz] = EIRP - path losses + G/T - k
```

여기서 Boltzmann constant의 dB 표현 `k ≈ -228.6 dBW/K/Hz`이므로 식에서는 보통 `+228.6`이 된다.

**Eb/N0 (Energy per bit to Noise power spectral density ratio, 비트 에너지 대 잡음전력밀도비)**:

```text
Eb/N0[dB] = C/N0[dB-Hz] - 10 log10(bit_rate[bps])
```

수신기·변조·FEC가 요구하는 `required Eb/N0`와 비교한다.

```text
link margin[dB] = available Eb/N0 - required Eb/N0 - implementation margin
```

양의 margin이 있다고 가용성이 자동 보장되지는 않는다. pointing, polarization, aging, temperature, Doppler residual, rain/cloud, interference, model uncertainty의 worst case를 포함해야 한다.

## 6. RSSI, SNR, BER, PER

- **RSSI (Received Signal Strength Indicator, 수신 신호 강도 지시값)**: 수신 대역 내 총 전력의 장치 추정치. 보정 오차와 간섭을 포함한다.
- **SNR (Signal-to-Noise Ratio, 신호 대 잡음비)**: 원하는 신호 전력과 noise 전력 비.
- **SINR (Signal-to-Interference-plus-Noise Ratio, 신호 대 간섭·잡음비)**: 간섭을 명시적으로 포함한다.
- **BER (Bit Error Rate, 비트 오류율)**: 전체 bit 중 틀린 비율.
- **PER (Packet Error Rate, 패킷 오류율)**: 전체 packet 중 실패 비율.

LoRa 같은 spread-spectrum 수신기는 음수 SNR에서도 동작할 수 있다. 이는 신호 전력이 잡음 대역 전력보다 작아도 processing gain으로 복원할 수 있다는 뜻이지, noise가 없다는 뜻이 아니다.

RSSI 기반 handover는 간섭에 속을 수 있다. filtered SNR, PER, Doppler, queue, predicted contact duration, acquisition cost를 함께 metric으로 쓴다.

## 7. 링크 adaptation

ACM(Adaptive Coding and Modulation, 적응 부호화·변조)은 channel 상태에 따라 modulation order와 FEC code rate를 바꾼다. 높은 SNR에서는 효율을 높이고 낮을 때 강한 FEC로 생존한다. feedback RTT가 길거나 상태가 빨리 변하면 보고가 도착할 때 이미 channel이 달라지므로 prediction과 conservative margin이 필요하다.

## 8. NASA Small Spacecraft 통신 관점

NASA의 2026 Small Spacecraft State-of-the-Art Communications 장은 small spacecraft communication을 `RF`와 `FSO` 두 범주로 나누고, ground/space segment, frequency band, antenna, radio, encryption, licensing, mission example을 함께 검토한다. 특정 vendor table의 최고 성능을 바로 설계값으로 쓰지 말고 mission configuration에서 성능과 TRL(Technology Readiness Level, 기술성숙도)을 다시 확인하라고 명시한다.

소형위성에서 반복되는 engineering lesson은 다음과 같다.

- communication subsystem은 payload data volume에서 거꾸로 sizing한다.
- ground station latitude와 network 분포가 contact와 latency를 결정한다.
- antenna deployment와 spacecraft attitude mode가 nominal gain을 제한한다.
- licensing은 launch 직전 행정 작업이 아니라 concept of operations와 초기 설계 입력이다.
- high-rate optical/RF payload와 별도로 low-rate command·safe-mode path를 확보한다.
- advertised throughput가 아니라 pass 전체의 acquisition·overhead·weather를 뺀 delivered volume을 계산한다.

NASA가 FSO를 future/high-rate 축으로 강조하지만, 공개 조사 보고서에 제품이 실렸다는 것은 NASA endorsement나 특정 mission의 flight qualification을 뜻하지 않는다.[NASA Communications chapter](https://www.nasa.gov/smallsat-institute/sst-soa/soa-communications/)

## 9. 실무 체크리스트

- range와 상대 각속도의 min/nominal/max를 분리했는가?
- antenna/optical terminal gain이 전체 scan range에서 유효한가?
- polarization, feeder, radome, pointing, aging loss를 포함했는가?
- noise temperature와 bandwidth 기준이 일치하는가?
- required Eb/N0가 uncoded가 아니라 실제 code rate·BER 요구와 맞는가?
- acquisition과 protocol overhead를 contact capacity에서 뺐는가?
- link margin을 평균이 아니라 요구 availability percentile에서 평가했는가?
- optical ground link는 cloud diversity와 site correlation을 모델링했는가?

[← 이전](01_system_foundations.md) · [메인](../README.md) · [다음: Space SDN →](03_space_networking.md)
