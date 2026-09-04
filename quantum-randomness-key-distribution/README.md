# QRNG·QKD 기반 양자암호통신 기술 가이드

작성일: 2026-08-27

## 목차

- [입력 자료와 조사 범위](#입력-자료와-조사-범위)
- [한눈에 보기](#한눈에-보기)
- [사진에서 확인한 구성](#사진에서-확인한-구성)
- [기초 개념](#기초-개념)
- [전체 시스템 구조](#전체-시스템-구조)
- [QRNG 설계와 검증](#qrng-설계와-검증)
- [QKD 동작과 한계](#qkd-동작과-한계)
- [키 관리와 데이터 암호화](#키-관리와-데이터-암호화)
- [위협 모델과 보안 요구사항](#위협-모델과-보안-요구사항)
- [표준과 참고 자료](#표준과-참고-자료)
- [실습 학습 가이드](#실습-학습-가이드)
- [도입·운영 체크리스트](#도입운영-체크리스트)
- [다음 학습 경로](#다음-학습-경로)

## 입력 자료와 조사 범위

사용자가 제공한 전시 사진 두 장을 2026-08-27에 판독했다.

- Photo 1: `양자암호통신 관련 부품, 장비` 설명과 QRNG-QKD-QKMS-QENC 구성도
- Photo 2: `양자 난수 생성 및 보안 기술 개요`, 광자 기반 QRNG chip과 quantum
  security chip 설명

사진에 표시된 문구와 일반 구조는 분석했지만, 전시 기관, 제조사, 제품명, chip
revision과 성능 수치는 사진만으로 확정하지 않았다. 하단 실물의 번호도 식별표
전체가 보이지 않아 특정 제품에 연결하지 않는다.

조사는 다음 공식 자료를 우선했다.

- [NIST SP 800-90B][nist-90b]: entropy source 설계·평가와 health test
- [NIST SP 800-90C][nist-90c]: entropy source와 DRBG를 결합한 RBG 구성
- [ITU-T Y.3800][itu-y3800]: QKD network의 개념 구조·계층·기본 기능
- [ETSI GS QKD 014 V1.1.1][etsi-qkd-014]: application에 key를 전달하는 REST 기반
  interface

NIST SP 800-90B는 2018년 final이며 NIST 페이지에 향후 수정 대상 errata 두 건이
표시돼 있다. SP 800-90C final은 2025-09-25 발행본을 확인했다. 표준의 현재 상태와
errata는 실제 인증·도입 시점에 다시 확인해야 한다.

## 한눈에 보기

사진의 시스템을 보안 기능 기준으로 나누면 다음과 같다.

| 계층              | 구성          | 역할                                      | 하지 않는 일                          |
| ----------------- | ------------- | ----------------------------------------- | ------------------------------------- |
| Entropy           | QRNG          | 예측하기 어려운 raw sample 생성           | 스스로 key lifecycle을 관리하지 않음  |
| Key establishment | QKD Alice/Bob | 양자·고전 채널로 shared key material 생성 | application data를 직접 전송하지 않음 |
| Key management    | KME/QKMS      | key 식별, 저장, 전달, 폐기와 audit        | 약한 endpoint를 자동 보호하지 않음    |
| Data protection   | QENC          | 받은 key로 plaintext 암호화·인증          | QKD 없이도 동작 가능한 고전 암호 계층 |
| Data network      | 일반 통신망   | ciphertext 전송                           | confidentiality 자체를 제공하지 않음  |

QRNG, QKD와 post-quantum cryptography(PQC)는 서로 대체 관계가 아니다. QRNG는
entropy, QKD는 특정 링크의 key establishment, PQC는 양자 공격을 고려한 공개키
algorithm 문제를 다룬다. 실제 시스템은 요구사항에 따라 이들을 조합할 수 있다.

## 사진에서 확인한 구성

### Photo 1

전시 설명은 QRNG가 암호 재료를 만들고, QKD가 광자 상태를 이용해 송·수신자 사이에
key를 공유하며, QKMS가 key를 보관하고, QENC가 일반 통신망의 데이터를
암호화한다고 설명한다.

도식에는 다음 항목이 보인다.

- `QKD(Alice)`와 `QKD(Bob)`
- key management entity인 `KME`
- `QKMS`와 양자암호 키 관리 시스템
- crypto module을 포함한 `QENC`
- key delivery용 internal secure network
- 공개 채널의 key 동기화·인증과 일반 통신망의 encrypted data

이 그림은 key plane과 data plane을 분리해서 읽어야 한다. 양자 채널에서 사용자
원문 데이터가 이동하는 것이 아니라, data encryption에 사용할 key가
생성·관리된다.

### Photo 2

전시 설명은 chip 내부 LED가 빛을 내고 sensor가 photon의 위치 관련 물리 현상을
sample해 random bit를 만든다는 개념도를 보여준다. `참난수`와 계산식에 의한
`의사난수` 패턴을 대비하고, QRNG chip과 이를 보안 기능과 결합한 quantum security
chip을 제시한다.

사진만으로는 실제 noise model, photon detector 방식, raw bit rate, conditioning
algorithm과 certification 상태를 확인할 수 없다. 개념도에 `photon`이 적혀 있다는
사실만으로 출력 전체가 독립·균등하거나 공격에 안전하다고 결론 내릴 수 없다.

## 기초 개념

### Randomness와 entropy

난수열이 0과 1을 비슷한 비율로 갖는 것만으로 안전하지 않다. 공격자가 다음 bit를
예측하기 어려워야 한다. min-entropy는 가장 가능성이 높은 결과의 확률 `p_max`로
다음처럼 표현한다.

```text
H_min = -log2(p_max)
```

한 bit sample에서 `p_max=0.5`면 이상적인 1 bit의 min-entropy를 갖는다. 하지만
bias, correlation, environmental drift와 sensor manipulation이 있으면 실제
entropy가 낮아질 수 있다.

### TRNG, QRNG와 DRBG

- **TRNG**: thermal noise, jitter 같은 비결정적 물리 현상을 sample한다.
- **QRNG**: quantum measurement의 불확정성을 noise source로 사용한다.
- **DRBG/PRNG**: seed와 deterministic algorithm으로 긴 bit stream을 만든다.

실무 RBG는 raw entropy를 그대로 application에 주기보다 noise source,
digitization, health test, conditioning, DRBG를 조합한다. NIST SP 800-90B는
entropy source를, SP 800-90A는 DRBG를, SP 800-90C는 이들을 조합하는 RBG
construction을 다룬다.

### QKD

QKD는 양자 상태 측정이 상태를 교란하고 unknown quantum state를 완벽히 복제할 수
없다는 성질을 이용해 도청 흔적을 통계적으로 탐지한다. 대표적인 교육용 protocol은
BB84다.

QKD가 성공하려면 quantum channel 외에도 authenticated classical channel이
필요하다. 인증이 없으면 공격자가 Alice와 Bob 각각과 별도 session을 만드는
man-in-the-middle 공격을 막을 수 없다.

### QBER

Alice와 Bob이 같은 basis로 측정한 sifted bit 가운데 다른 bit의 비율이다.

```text
QBER = mismatched sifted bits / total sifted bits
```

QBER가 높으면 eavesdropping뿐 아니라 optical loss, detector noise, alignment
오류나 구현 결함을 의심해야 한다. 허용 threshold는 protocol, security proof와
implementation parameter에 따라 결정하며 단일 고정 숫자로 일반화하지 않는다.

## 전체 시스템 구조

```text
                    key management plane
QRNG -> QKD Alice ===== quantum channel ===== QKD Bob
          |                  +                 |
          +------ authenticated classical ----+
          |                                    |
         KME -------- secure key API -------- KME
          |                                    |
        QKMS                                  QKMS
          |                                    |
         QENC ===== encrypted data network === QENC
                    data protection plane
```

단계별 흐름은 다음과 같다.

1. 양쪽 장비가 local randomness로 basis, bit 또는 protocol nonce를 만든다.
2. quantum signal을 송·수신하고 basis 정보를 authenticated channel에서 비교한다.
3. sifting, parameter estimation, error correction과 privacy amplification을
   한다.
4. 생성한 key를 KME/QKMS가 ID, lifetime, endpoint와 용도에 묶어 저장한다.
5. QENC가 key를 받아 AES-GCM 같은 authenticated encryption이나 요구에 맞는 data
   protection에 사용한다.
6. key 사용량, QBER, key generation rate, alarm과 폐기를 audit한다.

## QRNG 설계와 검증

### 1. Noise source model

측정 대상 quantum effect와 classical noise를 분리해 model을 세운다. LED drive,
temperature, supply noise, detector dark count와 ADC behavior가 output에 미치는
영향을 설명할 수 있어야 한다.

### 2. Digitization과 conditioning

analog measurement를 raw symbol로 바꾸고, 검증된 conditioning function으로
bias와 correlation을 줄인다. Hashing이 관측되지 않은 entropy를 새로 만들지는
않는다. 입력 entropy의 보수적 lower bound가 먼저 필요하다.

### 3. Startup·continuous health test

장비 시작 시 source가 정상 범위에 있는지 확인하고, 운영 중 갑작스러운 고정값,
반복, bias 변화를 탐지한다. 단순 통계 test 통과는 quantum origin이나 적대적
환경에서의 unpredictability를 증명하지 않는다.

### 4. Independent validation

noise source description, raw data access, entropy estimation, conditioning
claim, failure response와 physical attack test를 별도로 검토한다. production
output만 수집하면 conditioner가 raw source failure를 가릴 수 있다.

## QKD 동작과 한계

### BB84 개요

Alice는 random bit와 basis를 고르고 quantum state를 보낸다. Bob은 독립적으로
basis를 골라 측정한다. 두 사람은 인증된 고전 채널에서 basis만 공개해 같은
basis를 쓴 위치를 남긴다. 일부 bit를 비교해 error rate를 추정하고, error
correction과 privacy amplification 뒤에 final key를 얻는다.

### 보안 proof와 구현 보안

protocol의 수학적 security proof는 source와 detector가 model대로 동작한다는
가정에 의존한다. photon-number splitting, detector blinding, timing leakage,
Trojan-horse optical injection과 side channel은 실제 장비의 attack surface다.
decoy-state, measurement-device-independent QKD와 구현 countermeasure가 이
차이를 줄이지만 system validation을 대체하지 않는다.

### 거리와 availability

fiber loss와 detector 성능 때문에 key rate는 거리와 channel 상태에 영향을
받는다. trusted relay를 사용하면 relay가 trust boundary가 된다. 광로 차단이나
noise injection으로 key generation을 중지시키는 denial-of-service도 가능하다.
QKD는 availability를 자동 보장하지 않는다.

## 키 관리와 데이터 암호화

### KME와 QKMS

KME는 QKD endpoint와 application 사이에서 key association과 delivery를 담당하는
기능으로 볼 수 있다. QKMS는 여러 link·application의 key inventory, policy,
lifecycle과 audit를 관리한다. 구현마다 명칭과 경계가 다를 수 있으므로 interface
contract를 기준으로 확인한다.

key record에는 최소한 다음 metadata가 필요하다.

- unique key ID와 peer endpoint
- 생성 시각, expiration과 상태
- 허용된 algorithm·용도·application identity
- 전달 여부와 사용 횟수
- source link와 security parameter
- 삭제·폐기 결과와 audit event

### QENC

QENC는 QKD key material을 실제 data protection algorithm에 연결한다. key를
얻었다고 해서 confidentiality와 integrity가 자동 생기지는 않는다. nonce
uniqueness, authenticated encryption, replay protection, rekey, key exhaustion과
failover가 정확히 구현돼야 한다.

QKD key가 부족할 때 기존 key를 무기한 재사용하거나 조용히 plaintext로 전환하면
안 된다. 명시한 policy에 따라 traffic을 중단하거나 승인된 classical
key-establishment fallback으로 이동하고, downgrade를 audit해야 한다.

## 위협 모델과 보안 요구사항

| 위협                    | 영향                     | 최소 대응                                 |
| ----------------------- | ------------------------ | ----------------------------------------- |
| QRNG source 고정·편향   | 예측 가능한 key          | raw-source health test, fail closed       |
| QRNG conditioner만 감시 | source failure 은폐      | raw·conditioned stream 분리 monitoring    |
| classical channel 위조  | MITM                     | pre-shared 또는 PQC 기반 authentication   |
| detector side channel   | security proof 가정 붕괴 | 구현 test, isolation, countermeasure      |
| key API 탈취            | valid key 유출           | mutual auth, authorization, rate limit    |
| key ID 재사용           | nonce/key misuse         | atomic consume, replay detection          |
| QKMS 침해               | 대량 key compromise      | HSM, segmentation, least privilege        |
| 광로 차단               | key generation 중단      | buffer·alarm·명시적 failover policy       |
| 관리망 침해             | 설정·audit 변조          | signed config, secure boot, immutable log |
| 공급망 변조             | hidden backdoor          | firmware provenance, attestation, SBOM    |

## 표준과 참고 자료

### NIST SP 800-90 series

- SP 800-90A Rev. 1: deterministic random bit generator mechanism
- SP 800-90B: entropy source의 noise model, entropy estimation과 health test
- SP 800-90C: SP 800-90A와 90B를 결합한 RBG1, RBG2, RBG3, RBGC 구성

QRNG라고 부르는 제품도 cryptographic RBG로 사용하려면 source claim과 전체
construction을 구분해 평가해야 한다.

### ITU-T Y.3800

2019년 recommendation은 QKD를 지원하는 network의 design, deployment, operation과
maintenance를 위한 conceptual structure, layered model과 basic function의 개요를
제공한다.

### ETSI GS QKD 014

QKD key를 application에 전달하는 REST 기반 interface를 정의한다. 실제 구축은 key
요청자의 identity, key ID 동기화, status, transport protection, error와 retry의
의미를 명확히 해야 한다.

## 실습 학습 가이드

1. [`01_foundations.ipynb`](01_foundations.ipynb): bias, correlation과
   min-entropy를 계산하고 통계 test의 한계를 확인한다.
2. [`02_practice.ipynb`](02_practice.ipynb): BB84의 basis sifting과
   intercept-resend가 QBER에 미치는 영향을 toy simulation으로 본다.
3. [`03_advanced.ipynb`](03_advanced.ipynb): key ID, TTL, one-time consume,
   exhaustion과 failover를 포함한 작은 QKMS lifecycle을 구현한다.

모든 notebook은 교육용 simulation이며 실제 quantum hardware, certified entropy
assessment, production encryption이나 security proof를 재현하지 않는다.

## 도입·운영 체크리스트

### 요구사항

- [ ] 보호할 data, 보존 기간과 quantum threat horizon을 정의했다.
- [ ] QKD가 필요한 link와 PQC·classical key establishment 대안을 비교했다.
- [ ] confidentiality, integrity, authentication, availability 목표를 분리했다.

### QRNG

- [ ] quantum noise source와 classical noise model 문서가 있다.
- [ ] raw sample에 접근해 entropy를 독립 평가할 수 있다.
- [ ] startup·continuous health test와 failure response가 정의돼 있다.
- [ ] conditioner와 DRBG의 algorithm·revision이 식별된다.

### QKD

- [ ] authenticated classical channel의 trust anchor가 있다.
- [ ] QBER, key rate와 alarm threshold의 근거가 있다.
- [ ] device side-channel과 optical attack test를 수행했다.
- [ ] trusted node와 physical path의 trust boundary를 기록했다.

### QKMS/QENC

- [ ] key ID가 양쪽 endpoint에서 원자적으로 소비된다.
- [ ] expiration, destruction와 exhaustion 정책을 test했다.
- [ ] key API는 mutual authentication과 least privilege를 사용한다.
- [ ] fallback과 downgrade가 명시적이며 audit 가능하다.
- [ ] QENC가 authenticated encryption과 nonce uniqueness를 보장한다.

### 운영

- [ ] firmware update, signing, rollback과 SBOM 절차가 있다.
- [ ] key rate 저하, QBER 상승, source health failure를 monitoring한다.
- [ ] incident 시 key revoke·zeroize·forensic log 보존 절차가 있다.
- [ ] crypto-agility 계획에 QKD, PQC와 classical algorithm 교체를 포함했다.

## 다음 학습 경로

1. 첫 notebook에서 biased·correlated source를 만들고 detector sensitivity를
   비교한다.
2. BB84 simulation에서 Eve 비율과 channel noise를 분리해 QBER를 분석한다.
3. key manager에 concurrent request와 crash recovery test를 추가한다.
4. ETSI key delivery interface를 참고해 OpenAPI schema를 설계한다.
5. 실제 장비 평가에서는 vendor security target, certification report와 raw
   entropy assessment evidence를 요청한다.

[etsi-qkd-014]: https://www.etsi.org/deliver/etsi_gs/QKD/001_099/014/01.01.01_60/gs_QKD014v010101p.pdf
[itu-y3800]: https://www.itu.int/rec/T-REC-Y.3800-201910-I/en
[nist-90b]: https://csrc.nist.gov/pubs/sp/800/90/b/final
[nist-90c]: https://csrc.nist.gov/pubs/sp/800/90/c/final
