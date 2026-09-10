# 누리호 성능을 고려한 Walker-Delta 군집위성 궤도설계

작성일: 2026-09-10  
원문 확인일: 2026-09-10

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [연구 질문과 설계 논리](#연구-질문과-설계-논리)
- [Walker-Delta 수학](#walker-delta-수학)
- [시뮬레이션 조건](#시뮬레이션-조건)
- [결과 해석](#결과-해석)
- [비판적 검토와 재현 시 주의점](#비판적-검토와-재현-시-주의점)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 논문 페이지: [우주기술과 응용](https://www.jstna.org/archive/view_article?pid=jsta-5-2-73)
- 공식 PDF: [PDF Download](https://www.jstna.org/download/download_pdf?pid=jsta-5-2-73)
- DOI(Digital Object Identifier, 디지털 객체 식별자): [`10.52912/jsta.2025.5.2.73`](https://doi.org/10.52912/jsta.2025.5.2.73)
- 제목: 누리호 성능을 고려한 Walker-Delta 군집위성 궤도설계
- 영문 제목: Walker-Delta Constellation Orbit Design Considering Korea Space Launch Vehicle-II (KSLV-II) Performance
- 저자: 서성원, 최수진
- 학술지: Journal of Space Technology and Applications, 2025, 5(2), 73-85
- 투고·수정·게재승인: 2025-03-06 / 2025-03-20 / 2025-03-22
- 온라인 출판: 2025-05-31
- 이용 조건: Creative Commons Attribution-NonCommercial 4.0 International(CC BY-NC 4.0)

공식 PDF는 13쪽이며 6개 figure, 3개 table, 6개 식과 참고문헌을 포함한다. 전 페이지를 렌더링해 2단 편집 순서, 수식, histogram(히스토그램), contour map(등고선 지도)과 결론을 시각적으로 확인했다.

원문이 한국어이므로 [논문 대조 파일](누리호%20성능을%20고려한%20Walker-Delta%20군집위성%20궤도설계.번역.md)은 동일 문장을 번역하는 대신 `원문 → 쉬운 한국어` 형식으로 기술 강도를 유지하며 풀이한다.

## 한눈에 보기

이 논문의 출발점은 `재방문 주기만 가장 짧은 경사각`과 `국내 발사체로 많은 질량을 직접 투입할 수 있는 경사각`이 다를 수 있다는 점이다. 기존 연구가 약 35°~45° 경사각을 최적해로 제안하더라도, 나로우주센터에서 누리호로 그 궤도에 직접 투입하려면 큰 yaw maneuver(요기동) 또는 별도 발사가 필요하다.

```text
누리호 직접 투입에 유리한 경사각 80°
  + 고도 500 km
  + 위성 총 30기
  + 센서 FOV 30°
  + Walker-Delta 80°:30/5/f 또는 80°:30/6/f
  + 가능한 모든 phase parameter f
  -> 북한 전체 및 0.1° grid의 최소·평균·최대 revisit time
```

두 배치의 총 탑재 질량은 다음과 같다.

- 5개 궤도면 × 면당 6기 × 400 kg = 2,400 kg
- 6개 궤도면 × 면당 5기 × 500 kg = 2,500 kg

전체 지역 평균 재방문 주기는 phase에 따라 약 43.2~46.3분이다. 평균은 5면과 6면이 비슷하지만 최대 공백은 5면의 180~200분에서 6면의 140~160분으로 줄어든다. 즉 평균만 보면 놓치는 tail risk(꼬리 위험)가 있다.

## 기초 개념

### 궤도 경사각과 발사 방위각

inclination(궤도 경사각) `i`는 궤도면과 지구 적도면 사이의 각도다. launch azimuth(발사 방위각)는 발사 지점에서 로켓이 수평으로 향하는 방향이다. 발사장 위도, 방위각, 지구 자전과 ascent guidance를 함께 고려해야 실제 투입 경사각과 payload가 결정된다.

누리호는 1·2단 낙하구역과 안전거리 때문에 발사 방향이 제한된다. 논문은 약 172° 방위각에서 yaw maneuver 없이 투입하기 유리한 경사각을 80°로 보고, 45° 부근 궤도보다 높은 payload delivery를 활용하려 한다.

### 재방문 주기

RT(Revisit Time, 재방문 주기)는 관측이 끝난 뒤 같은 관심 지역 또는 지점을 다시 관측할 때까지의 시간 간격이다.

- area revisit: 관심 영역 어디에도 coverage가 없는 구간부터 coverage가 다시 시작할 때까지
- grid revisit: 관심 영역을 작은 격자로 나눠 각 격자에서 관측 사이의 gap을 계산
- minimum RT: 우연히 가장 빠른 재방문
- average RT: 모든 관측 gap의 산술평균
- maximum RT: 가장 긴 감시 공백, 보장 성능에 가까운 지표

```math
ART = (1/N) Σ_(n=1)^N RT_n
```

`N`은 관측 간격 표본 수다. 관측 event가 한 번뿐이면 gap이 없으므로 ART를 정의할 수 없다는 경계 조건을 구현해야 한다.

### FOV와 지상 coverage

FOV(Field of View, 시야)는 센서가 볼 수 있는 각도 범위다. `30°`가 full cone angle인지 half-angle인지, 센서가 항상 nadir(천저점)를 보는지 agile pointing을 허용하는지에 따라 coverage가 크게 달라진다. 재현 코드는 반드시 정의를 고정해야 한다.

### 궤도면, RAAN, AoL

- RAAN(Right Ascension of the Ascending Node, 승교점 적경) `Ω`: 궤도면이 적도와 교차해 북쪽으로 올라가는 점의 방향
- AoL(Argument of Latitude, 위도인수) `u` 또는 논문의 `μ`: 승교점부터 궤도면 안에서 잰 위성 위치
- phase difference(위상차): 인접 궤도면 위성들의 진행 방향 상대 배치

## 연구 질문과 설계 논리

1. 누리호 직접 투입 성능을 우선하면 어떤 경사각·고도·위성 질량 조합이 가능한가?
2. 30기를 5개 또는 6개 궤도면에 나눌 때 북한 지역 재방문 주기는 어떻게 달라지는가?
3. Walker phase parameter `f`가 짧은·긴 revisit interval 분포에 영향을 주는가?
4. 전체 평균과 0.1° grid별 최소·평균·최대 결과가 어떤 공간적 불균형을 보이는가?

핵심 의의는 orbit-only optimum이 아니라 launch-constrained system optimum을 보려는 것이다. 다만 비용·발사 횟수·배치기동·고장·운영을 하나의 목적함수로 최적화하지 않고, 두 실현 가능 설계안을 정해 revisit 결과를 비교한다.

## Walker-Delta 수학

```math
i : t / p / f,  0 ≤ f ≤ p-1
```

- `i`: 모든 위성의 공통 경사각
- `t`: 전체 위성 수
- `p`: 등간격 궤도면 수
- `f`: 인접 궤도면의 위상 parameter
- `s=t/p`: 한 궤도면의 위성 수

`j`번째 궤도면의 RAAN과 `k`번째 위성 AoL:

```math
Ω_j = (2π/p)j,  0 ≤ j ≤ p-1
μ_jk = (2π/s)k + (2πf/(sp))j,  0 ≤ k ≤ s-1
```

`80°:30/5/0`은 경사각 80°, 총 30기, 5면, phase 0이며 면당 6기다. `80°:30/6/5`는 6면, 면당 5기, phase 5다. 실제 배치에서는 동일 epoch, 궤도요소·좌표계·각도 단위를 ICD(Interface Control Document, 인터페이스 제어 문서)에서 고정해야 한다.

## 시뮬레이션 조건

| 변수 | 논문 기준선 |
|---|---:|
| 고도 | 500 km |
| 경사각 | 80° |
| 전체 위성 | 30기 |
| 궤도면 | 5 또는 6 |
| phase `f` | `0..p-1` 전부 |
| sensor FOV | 30° |
| 기간 | 1일, 1주, 1개월 |
| 관심 지역 | 북한 전체 및 0.1° grid |
| 동역학 | 외란 없는 2체 문제 |

```math
r¨ = -(μ/|r|^3) r
```

`μ`는 지구 중력상수, `r`은 지구중심에서 위성까지의 위치벡터다. 원궤도라면 평균 운동 `n=sqrt(μ/a^3)`, 주기 `T=2π/n`을 쓸 수 있다.

## 결과 해석

| phase `f` | 5 planes 평균(min) | 6 planes 평균(min) |
|---:|---:|---:|
| 0 | 45.7 | 45.4 |
| 1 | 43.7 | 43.5 |
| 2 | 45.3 | 46.3 |
| 3 | 43.9 | 43.2 |
| 4 | 43.7 | 45.2 |
| 5 | 해당 없음 | 44.6 |

- 5면에서는 60분 미만 interval이 약 85%, 180~200분 interval이 약 15%다.
- 6면에서는 phase 1·3·5일 때 40분 미만 비율이 약 80%, phase 0·2·4일 때 약 65%다.
- 6면의 긴 interval은 약 120~160분이며 5면의 180~200분보다 짧다.
- 긴 gap은 지구 자전으로 coverage 담당 궤도면이 다음 면으로 넘어갈 때 생긴다고 해석한다.

평균값 차이는 작지만 maximum gap과 histogram shape는 다르다. 최대 무관측 시간을 제한하는 임무라면 6면이 더 유리할 수 있다. 반대로 발사당 위성 수, 분리장치, plane deployment 비용까지 포함하면 결론이 달라질 수 있다.

격자 결과는 minimum이 서쪽 일부에 편향되고, average는 북부가 상대적으로 짧고 남부가 길며, 4.4.3 본문상의 maximum은 북부 대부분이 12,500초 이상이고 남부 일부가 11,700초 이하라고 기술한다.

## 비판적 검토와 재현 시 주의점

### 1. 논문 내부의 방향 불일치

4.4.3 본문은 `북부의 maximum revisit time이 길고 남부 일부가 짧다`고 설명한다. 그러나 결론은 `maximum revisit time이 남부에서 더 길다`고 적는다. 두 진술은 반대다. contour 원본 수치와 aggregation 코드를 확인하기 전에는 어느 쪽도 사실로 확정하면 안 된다.

### 2. 발사체 성능 입력

서론의 향상된 누리호 성능 수치는 일부 인터넷 기사 인용과 `예상된다`는 표현에 기반한다. 실제 mission design에는 KARI(Korea Aerospace Research Institute, 한국항공우주연구원)의 승인된 payload performance curve, fairing, injection error, reserve, adapter 질량을 사용해야 한다.

### 3. 이상적인 2체 모델

J2(지구 편평도 2차 중력항), 대기항력, 태양·달 섭동, station-keeping, 발사 분산을 생략한다. 80° 궤도의 RAAN drift와 장기간 형상 유지는 1개월 이상 분석에서 중요하다.

### 4. 센서·운용 제약

FOV 30°만으로 coverage를 판정하면 cloud, solar illumination, imaging mode, slew/settling, duty cycle, storage, downlink와 task priority가 빠진다. `볼 수 있음`과 `유효 영상을 제때 전달함`은 다르다.

### 5. 통계와 최적성

평균 차이는 수 분이지만 uncertainty, timestep resolution, boundary treatment가 보고되지 않는다. 시작·종료 censored gap, 연속 visibility의 event 병합, grid weighting을 명시해야 한다. 또한 선택한 후보를 분석했을 뿐 launch cost·deployment ΔV·fault tolerance까지 포함한 전역 최적화는 아니다.

## 용어 정리

| 약어·용어 | 영문 전체 이름 | 한국어·역할 |
|---|---|---|
| KSLV-II | Korea Space Launch Vehicle-II | 한국형발사체 누리호 |
| Walker-Delta | Walker Delta Pattern | 동일 고도·경사각 원형 궤도의 균등 군집 배치 |
| RT / ART | Revisit Time / Average Revisit Time | 재방문 주기 / 평균 재방문 주기 |
| FOV | Field of View | 센서 시야각 |
| RAAN | Right Ascension of the Ascending Node | 승교점 적경, 궤도면 방향 |
| AoL | Argument of Latitude | 위도인수, 궤도면 내 위성 위치 |
| SSO | Sun-Synchronous Orbit | 태양동기궤도 |
| LEO | Low Earth Orbit | 저궤도 |
| SAR | Synthetic Aperture Radar | 합성개구레이더 |
| AOI | Area of Interest | 관심 지역 |
| epoch | 기준시각 | 궤도요소가 정의되는 공통 시각 |
| ΔV | Delta-V | 속도 변화량, 궤도기동 비용 |
| J2 | Second Zonal Harmonic | 지구 편평도에 의한 대표적 궤도 섭동 |

## 실습 학습 가이드

- [01_foundations.ipynb](01_foundations.ipynb): 원궤도 주기, Walker `i:t/p/f`, RAAN·AoL 생성
- [02_practice.ipynb](02_practice.ipynb): visibility event에서 최소·평균·최대 RT 집계
- [03_advanced.ipynb](03_advanced.ipynb): 2체 원궤도·지구 자전·nadir FOV를 포함한 30기 toy simulation

세 notebook은 논문 원시 코드·데이터가 공개되지 않은 상태에서 만든 독립 toy reproduction이다. 논문의 43~47분 결과를 재현했다고 주장하지 않는다. 실제 재현에는 정확한 북한 polygon/grid, epoch, Earth orientation, FOV 정의와 event detector 설정이 필요하다.

## 다음 학습 경로

1. `80°:30/5/f`와 `80°:30/6/f`의 RAAN·AoL 배치를 생성한다.
2. visibility sample을 pass event로 병합하고 censored gap을 구분한다.
3. time step과 FOV 정의를 바꿔 결과 민감도를 확인한다.
4. SGP4(Simplified General Perturbations 4, 단순 일반 섭동 모델 4) 또는 고정밀 propagator로 J2·drag를 추가한다.
5. 발사체 성능, 분리·배치 ΔV, downlink와 cloud를 포함한 end-to-end trade study로 확장한다.

[쉬운 한국어 문장 대조 읽기 →](누리호%20성능을%20고려한%20Walker-Delta%20군집위성%20궤도설계.번역.md)
