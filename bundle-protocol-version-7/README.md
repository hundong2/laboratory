<!-- rumdl-disable MD013 -->

# Bundle Protocol Version 7(RFC 9171) 한국어 학습 가이드

작성일: 2026-09-11
원문 확인일: 2026-09-11

> 이 문서는 RFC 9171을 처음 읽는 개발자부터 실제 구현을 검토하는 엔지니어까지를 위한
> 학습 자료입니다. 규범적 요구사항의 최종 근거는 반드시 RFC 원문, 후속 업데이트 RFC,
> RFC Editor 정오표를 함께 확인해야 합니다.

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [핵심 요약](#핵심-요약)
- [Bundle 노드와 계층 구조](#bundle-노드와-계층-구조)
- [Bundle의 전송 형식](#bundle의-전송-형식)
- [처리 수명주기](#처리-수명주기)
- [신뢰성·보안·운영 주의점](#신뢰성보안운영-주의점)
- [후속 업데이트와 정오표](#후속-업데이트와-정오표)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [구현 점검표](#구현-점검표)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

### 주 출처

| 항목 | 확인 내용 |
| --- | --- |
| 원문 | [RFC 9171: Bundle Protocol Version 7](https://www.rfc-editor.org/rfc/rfc9171.html) |
| 최종 URL | `https://www.rfc-editor.org/rfc/rfc9171.html` |
| 문서 상태 | IETF Standards Track의 Proposed Standard, 2022년 1월 발행 |
| 저자 | Scott Burleigh, Kevin Fall, Edward Birrane III |
| DOI | [10.17487/RFC9171](https://doi.org/10.17487/RFC9171) |
| 원문 언어 | 영어 |
| 현재 상태 | [RFC 9171 정보 페이지](https://www.rfc-editor.org/info/rfc9171/) |
| 정오표 | [RFC 9171 Errata](https://errata.rfc-editor.org/search/?rfc_number=9171) |
| 접근일 | 2026-09-11 |

### 함께 확인한 공식 문서

- [RFC 9713](https://www.rfc-editor.org/rfc/rfc9713.html): BPv7 관리 레코드 유형을
  IANA 레지스트리로 판별하도록 RFC 9171을 갱신합니다.
- [RFC 9758](https://www.rfc-editor.org/rfc/rfc9758.html): `ipn` URI 구조와 BPv7에서의
  CBOR 인코딩·디코딩 규칙을 갱신합니다.
- [RFC 9172](https://www.rfc-editor.org/rfc/rfc9172.html): Bundle Protocol Security(BPSec)를
  정의합니다.
- [RFC 9174](https://www.rfc-editor.org/rfc/rfc9174.html): 인터넷에서 사용할 수 있는
  TCP Convergence-Layer Protocol v4(TCPCLv4)를 정의합니다.
- [RFC 8949](https://www.rfc-editor.org/rfc/rfc8949.html): BPv7 블록의 기반 표현인 CBOR를
  정의합니다.
- [RFC 4838](https://www.rfc-editor.org/rfc/rfc4838.html): 지연 내성 네트워킹(DTN)의
  아키텍처와 설계 배경을 설명합니다.

### 이 폴더의 산출물

- [한국어 번역·해설](translation.ko.md): 원문의 섹션 흐름을 보존한 구조적 번역 요약
- [기초 실습](01_foundations.ipynb): DTN과 BPv7의 시간·수명·기본 CBOR 표현
- [응용 실습](02_practice.ipynb): 블록 모델, CRC, 단편화와 재조립 검증
- [심화 실습](03_advanced.ipynb): BPA 처리 상태 머신과 방어적 검증

### 번역 및 재현 범위

RFC 9171은 IETF Trust 저작권과 관련 법적 조건의 적용을 받습니다. 따라서
[translation.ko.md](translation.ko.md)는 원문 전체를 그대로 복제한 전문 번역이 아니라,
원문의 장·절 구조와 규범적 의미를 따라가며 학습에 필요한 내용을 한국어로 재구성한
번역 해설입니다. 코드 구성요소를 실제 제품에 재사용할 때는 RFC의 라이선스 고지도 별도로
확인해야 합니다.

노트북은 표준 라이브러리만으로 개념을 확인하는 **교육용 축소 모델**입니다. 별도 표시가
없는 한 RFC 9171의 완전한 CBOR 직렬화기, 네트워크 상호운용 구현 또는 보안 구현이 아닙니다.

## 한눈에 보기

BPv7는 연결이 항상 유지된다는 전제를 버리고, 데이터를 `bundle`이라는 자립적인 단위로
저장·운반·전달하는 DTN용 오버레이 프로토콜입니다. 지상국과 우주선, 간헐적인 무선망,
재난 통신처럼 왕복 지연이 길거나 다음 링크가 언제 열릴지 미리 정해져 있는 환경에
적합합니다.

```text
Application Agent
      │ ADU·관리 레코드
      ▼
Bundle Protocol Agent (BPA)
      │ bundle 저장·수명·전달·중계 판단
      ▼
Convergence-Layer Adapter (CLA)
      │ TCPCLv4, LTP 등 환경별 전송 방식
      ▼
다음 Bundle 노드 ── store → carry → forward ── 목적지 노드
```

핵심은 다음 세 가지입니다.

1. **오버레이와 지연 허용**: 하위 네트워크가 서로 달라도 CLA로 연결하고, 접촉이 없을 때는
   bundle을 영속 저장합니다.
2. **자립적인 전달 단위**: payload뿐 아니라 목적지, 출처, 생성 시각, 수명, 처리 지시를
   함께 운반합니다.
3. **확장 가능한 블록 구조**: 기본 블록과 payload 외에 이전 노드, bundle 나이, hop 수,
   BPSec 보안 블록 등을 붙일 수 있습니다.

## 기초 개념

### 일반 인터넷 전송과 무엇이 다른가

일반적인 TCP 통신은 비교적 짧은 왕복 시간과 지속적인 종단 간 경로를 기대합니다. DTN은
그 기대가 성립하지 않는 환경을 대상으로 합니다.

| 환경 특성 | 전통적인 실시간 세션의 어려움 | BPv7의 대응 |
| --- | --- | --- |
| 간헐적 연결 | 송신자와 수신자가 동시에 온라인이 아닐 수 있음 | 중간 노드가 bundle을 저장 후 전달 |
| 매우 긴 지연 | 종단 간 재전송과 혼잡 제어의 피드백이 너무 늦음 | hop별 CLA와 예약·예측 접촉 활용 |
| 이종 네트워크 | 링크마다 주소·MTU·신뢰성 특성이 다름 | CLA가 하부 프로토콜 차이를 흡수 |
| 높은 오류율 | 한 번의 장거리 전송 실패 비용이 큼 | 인접 구간 신뢰성, CRC, 선택적 BPSec 조합 |
| 제한된 접촉 시간 | 전체 데이터를 한 번에 보낼 수 없음 | 필요 시 payload 단편화와 이후 재조립 |

### Store-Carry-Forward

- **Store**: 다음 전달 기회가 없을 때 bundle을 영속 저장합니다.
- **Carry**: 노드 또는 물리 매체가 이동하는 동안 데이터를 유지할 수도 있습니다.
- **Forward**: 적합한 접촉과 CLA가 준비되면 다음 노드로 보냅니다.

따라서 큐, 영속 저장소, 수명 만료, 중복, 재시도, 저장 공간 고갈이 모두 프로토콜 구현의
중요한 운영 문제입니다.

### 규범 키워드 읽기

RFC 9171의 대문자 키워드는 BCP 14의 의미를 갖습니다.

| 원문 | 이 자료의 표현 | 의미 |
| --- | --- | --- |
| `MUST`, `SHALL`, `REQUIRED` | 반드시 | 준수 구현에 필수 |
| `MUST NOT`, `SHALL NOT` | 절대로 해서는 안 됨 | 명시적 금지 |
| `SHOULD`, `RECOMMENDED` | 권고 | 타당한 예외가 있을 수 있으나 영향을 이해해야 함 |
| `SHOULD NOT` | 비권고 | 예외가 있을 수 있으나 보통 피해야 함 |
| `MAY`, `OPTIONAL` | 선택 가능 | 구현 또는 운영 정책에 따라 선택 |

한국어 설명에서 문장을 쉽게 풀어도 규범 강도는 바꾸지 않습니다. 모호할 때는 원문 문장과
정오표를 최종 기준으로 삼습니다.

## 핵심 요약

- 하나의 bundle은 CBOR의 **indefinite-length array**로 표현하며 최소 두 블록을 가집니다.
- 첫 블록은 하나뿐인 **Primary Block**이고, 그 뒤의 모든 블록은 **Canonical Block**입니다.
- 마지막 canonical block은 반드시 **Payload Block**이고 bundle당 정확히 하나만 존재합니다.
- Primary Block의 암시적 block number는 `0`, Payload Block의 block number는 항상 `1`입니다.
- Primary Block은 생성부터 전달까지 불변입니다. 중계 중 바뀌는 정보는 확장 블록으로
  표현합니다.
- Endpoint ID(EID)는 URI이며 RFC 9171은 `dtn`과 `ipn` scheme을 정의합니다. 다만 현재
  `ipn` 규칙은 RFC 9758의 갱신 내용까지 적용해야 합니다.
- CRC는 전송 오류 검출용이지 인증·무결성 공격 방어 수단이 아닙니다. 보안에는 RFC 9172의
  BPSec과 적절한 하위 계층 보안을 사용합니다.
- BP 자체는 종단 간 전달을 보장하지 않습니다. 신뢰성 있는 CLA 또는 응용/확장 계층의
  확인 메커니즘이 필요합니다.
- BPv7는 RFC 5050의 BPv6 구현과 상호운용되지 않습니다.
- 라우팅 계산, 라우팅 정보 배포, 노드 관리, 개별 CLA의 내부 프로토콜은 RFC 9171의 범위
  밖입니다.

## Bundle 노드와 계층 구조

### Application Agent(AA)

사용자 목적을 수행하는 부분입니다. 두 개의 논리 요소로 나뉩니다.

- **Application-specific element**: 사용자 ADU를 만들고 전송을 요청하며, 전달된 ADU를
  처리합니다.
- **Administrative element**: 상태 보고서 같은 관리 레코드를 생성·수신·처리합니다.

### Bundle Protocol Agent(BPA)

BP 서비스를 제공하고 RFC의 처리 절차를 수행합니다. 구현 형태는 프로세스, 데몬, 공유
라이브러리, 객체 또는 전용 하드웨어일 수 있습니다. 다음을 책임집니다.

- endpoint 등록과 활성/수동 상태 관리
- bundle 생성, 수신, dispatch, forwarding, local delivery
- retention constraint와 영속 저장 관리
- 수명 만료, 삭제, 폐기, 취소
- 단편화와 재조립
- 선택적인 상태 보고서 생성

### Convergence-Layer Adapter(CLA)

BPA 대신 실제 하위 네트워크를 통해 bundle을 송수신합니다. RFC 9171은 구체적인 CLA
프로토콜을 정의하지 않고 BPA에 제공해야 할 서비스만 설명합니다. 인터넷 환경에서는
TCPCLv4(RFC 9174)가 대표적인 선택이지만, 특정 bundle과 환경에 항상 적합하다는 뜻은
아닙니다.

### Endpoint, EID와 Node ID

- **Endpoint**는 같은 Endpoint ID를 공유하는 0개 이상의 bundle node 집합입니다.
- **Singleton endpoint**는 정확히 한 노드만 포함합니다.
- **EID**는 `<scheme>:<scheme-specific part>` 형태의 URI입니다.
- **Node ID**는 노드의 영구적인 administrative endpoint ID를 사용합니다. 문법은 EID와
  같지만 목적지 집합을 가리키는 EID와 개념적 역할이 다릅니다.
- 익명 source는 null EID를 사용할 수 있으나 관련 상태 보고 제약을 함께 지켜야 합니다.

익명 source를 쓰는 bundle은 `must not fragment` flag를 설정해야 하고 모든 상태 보고 요청
flag를 0으로 둬야 합니다. 비익명 source는 송신 BPA 노드 하나만 구성원인 singleton EID여야
합니다.

`ipn` EID를 새로 구현할 때는 RFC 9171의 2-요소 설명만 고립해서 사용하지 말고 RFC 9758이
정의한 allocator identifier, node number, service number의 3요소 개념과 호환 인코딩을
반드시 확인해야 합니다.

## Bundle의 전송 형식

### 전체 구조

```text
indefinite-length CBOR array
├─ Primary Block                    # 정확히 1개, 암시적 block number 0
├─ Canonical Extension Block ...    # 0개 이상
└─ Payload Block                    # 정확히 1개, 마지막, block number 1
CBOR break
```

모든 필드는 RFC 8949의 core deterministic encoding 요구사항을 따라야 합니다. 단, BPv7는
상위 bundle 배열에 indefinite-length 표현을 허용합니다. 보안 해시와 CRC는 의미상 같은
데이터가 아니라 **실제 직렬화 octet 열**에 적용되므로 결정적 인코딩이 중요합니다.

### Primary Block

목적지까지 전달하는 데 필요한 핵심 정보를 담으며 중계 중 바꿀 수 없습니다.

| 순서 | 필드 | 핵심 의미 |
| ---: | --- | --- |
| 1 | Version | BPv7에서는 `7` |
| 2 | Bundle Processing Control Flags | bundle 전체의 단편·관리 레코드·상태 보고 요청 등 |
| 3 | CRC Type | `0` 없음, `1` X-25 CRC-16, `2` CRC32C |
| 4 | Destination EID | 최종 전달 endpoint |
| 5 | Source Node ID | 최초 송신 노드 또는 null EID |
| 6 | Report-to EID | 상태 보고서를 받을 endpoint |
| 7 | Creation Timestamp | DTN time과 sequence number |
| 8 | Lifetime | 생성 시점 이후 유효한 밀리초 |
| 9 | Fragment Offset | fragment일 때만 존재 |
| 10 | Total ADU Length | fragment일 때만 존재 |
| 마지막 | CRC | CRC type이 0이 아니면 존재 |

배열 원소 수는 fragment 여부와 CRC 여부에 따라 8, 9, 10, 11 중 하나입니다. Primary
Block을 대상으로 하는 BPSec Block Integrity Block(BIB)이 없다면 primary CRC type은 0이
아니어야 합니다.

### Canonical Block

Primary Block 이외의 모든 블록이 공통으로 따르는 외피입니다.

| 순서 | 필드 | 핵심 의미 |
| ---: | --- | --- |
| 1 | Block Type Code | payload는 `1`; 확장 유형을 식별 |
| 2 | Block Number | bundle 내부에서 유일한 참조 번호 |
| 3 | Block Processing Control Flags | 처리 불가 시 복제·보고·삭제·폐기 정책 |
| 4 | CRC Type | 없음, CRC-16 또는 CRC32C |
| 5 | Block-Type-Specific Data | definite-length CBOR byte string |
| 6 | CRC | CRC type이 0이 아니면 존재 |

CRC가 없으면 5개, 있으면 6개 원소입니다. block number는 배열 순서와 같다는 보장이
없습니다. BPSec 블록이 다른 블록을 모호함 없이 가리킬 수 있도록 유일성을 검사해야 합니다.

### RFC 9171 기본 확장 블록

| Type | 이름 | 역할 | 중계 시 주의점 |
| ---: | --- | --- | --- |
| 6 | Previous Node | 직전에 forwarding한 노드의 Node ID | 기존 값을 제거하고 정책에 따라 현재 노드 값 삽입 |
| 7 | Bundle Age | 생성 이후 경과 밀리초 | CLA가 보내기 직전 체류 시간을 반영 |
| 10 | Hop Count | 현재 hop 수와 hop limit | forwarding마다 증가, limit 초과 검사 |

모든 준수 구현은 이 세 블록을 생성할 필요까지는 없지만 인식·파싱·요구된 동작을 지원해야
합니다. 알 수 없는 확장 블록을 만났을 때의 동작은 해당 블록의 processing control flag가
결정합니다.

Creation Timestamp의 DTN time이 `0`으로 시각 미상임을 나타내면 Bundle Age Block이 정확히
하나 있어야 합니다. 시각을 알고 있으면 Bundle Age Block은 최대 하나입니다. Hop limit은
1부터 255까지입니다. hop count의 hop별 증가는 `SHOULD`, limit 초과 시 삭제도 `SHOULD`인
권고 요구사항이며 그 강도를 구현 문서와 시험에 그대로 남겨야 합니다.

### CRC를 정확히 이해하기

- `CRC type 1`: 표준 X-25 CRC-16
- `CRC type 2`: Castagnoli CRC-32C
- CRC 값은 각각 2-byte 또는 4-byte CBOR byte string이며 network byte order입니다.
- CRC가 있는 블록은 CRC **값 octet**을 0으로 둔 상태의 블록 직렬화 전체를 계산 대상으로
  삼습니다.
- Verified Errata 8043에 따라 CRC byte string을 나타내는 CBOR initial byte까지 0으로
  바꾸면 안 됩니다.
- CRC 성공은 우연한 손상 가능성을 낮출 뿐, 공격자가 다시 계산한 위조 데이터를 막지
  못합니다.

## 처리 수명주기

### 대표 흐름

```text
AA 전송 요청
  → bundle 생성 + Dispatch pending
  → forwarding 판단 + Forward pending
  → 다음 노드와 CLA 선택
  → 확장 블록 갱신
  → CLA 송신
  → 수신 노드의 형식·수명·확장 블록 검사
  → dispatch
      ├─ 로컬 목적지: 전달 또는 fragment 재조립 대기
      └─ 원격 목적지: 다음 hop으로 forwarding
  → retention constraint가 모두 사라지면 저장소에서 폐기 가능
```

### Retention Constraint

Retention constraint는 bundle을 버릴 수 없게 하는 상태 조건입니다. `Dispatch pending`,
`Forward pending`, `Reassembly pending` 등이 대표적입니다. **삭제(delete)**는 모든 constraint를
제거하는 절차이고, **폐기(discard)**는 constraint가 하나도 없을 때 실제 참조와 저장 공간을
해제하는 동작입니다. 두 단어를 같은 의미로 구현하면 상태 보고와 저장소 정리가 어긋날 수
있습니다.

### Lifetime과 Bundle Age

- Lifetime은 생성 시점 이후 payload가 유용한 기간을 밀리초로 나타냅니다.
- 정확한 시계가 있으면 현재 DTN time과 creation timestamp의 차이로 age를 판단할 수
  있습니다.
- 정확한 시계가 없으면 Bundle Age Block을 사용하고 각 노드의 체류 시간을 누적합니다.
- age가 lifetime을 넘으면 삭제가 권고됩니다.
- 비정상적으로 긴 lifetime이 저장소를 위협하면 노드는 원래 값을 바꾸지 않고 로컬에서만
  더 짧은 effective lifetime을 적용할 수 있습니다.

### 단편화와 재조립

payload가 `M` bytes일 때 `0 < N < M`을 만족하는 앞 `N` bytes와 뒤 `M-N` bytes의 두
fragment로 나눌 수 있습니다. fragment는 다시 쪼갤 수 있지만 논리적 offset은 항상 원본
ADU를 기준으로 하는 한 단계 모델입니다.

재조립 키에는 source node ID와 creation timestamp가 필요하며, fragment offset과 payload
길이로 다음을 검증해야 합니다.

- 모든 구간이 전체 ADU 길이 안에 있는가
- 중복 구간의 byte가 서로 모순되지 않는가
- offset 0부터 total ADU length까지 빈틈없이 이어지는가
- 자원 제한을 넘는 fragment 수나 총 크기를 거부하는가

현재 정오표에는 확장 블록을 fragment에 배치하는 규칙과 원본 primary block을 복원하는
문제에 대해 문서 차원의 추가 갱신이 필요하다는 항목이 있습니다. 실전 구현은 이 부분을
RFC 본문만으로 단순화하지 말아야 합니다.

### 상태 보고서

상태 보고서는 수신, forwarding, 전달, 삭제 여부와 사유를 report-to EID로 알리는 관리
레코드입니다. 그러나 경로의 노드 수를 `N`이라 할 때 요청 하나가
`1 + 2(N - 1)`개 정도의 추가 bundle을 쉽게 유발할 수 있습니다. 그래서 생성 기능은 기본적으로
꺼져 있어야 하며 트래픽 증가 위험을 수용할 때만 켜야 합니다. 전달 보고는 payload가 AA에
전달됐다는 뜻이지 응용 프로그램이 성공적으로 처리했다는 확인이 아닙니다.

## 신뢰성·보안·운영 주의점

### BP는 전달 보장 프로토콜이 아니다

BPv7의 저장·운반·전달 모델이 데이터 손실을 자동으로 없애지는 않습니다. hop 사이에서는
신뢰성 있는 CLA를 선택할 수 있고, 종단 간 확인은 응용 계층 또는 별도 확장으로 설계해야
합니다. 중복 전달에 안전한 idempotent 처리와 중복 제거 키도 응용 설계에 포함하는 편이
좋습니다.

### CRC와 BPSec의 역할은 다르다

| 수단 | 주 목적 | 방어하지 못하는 것 |
| --- | --- | --- |
| CRC-16/CRC32C | 우발적인 전송·저장 오류 탐지 | 의도적으로 재계산한 위조, 기밀성 침해 |
| BIB | 대상 블록의 무결성·인증 | payload 기밀성 자체 |
| BCB | primary 이외 대상 블록의 기밀성 | 노출된 primary metadata 전부 |
| 보안 CLA | 인접 노드 간 인증·기밀성 | store-carry-forward 전체 경로의 종단 간 보호 |

RFC 9171은 bundle을 생성하거나 암호학적으로 검증하거나 받아들이는 BPA에 BPSec 지원을
요구하지만, 개별 bundle에 BPSec을 실제 적용하는 것은 선택 사항입니다. 배포의 위협 모델과
보안 정책이 그 선택을 결정해야 합니다.

### 자원 고갈과 메타데이터 노출

- bundle 크기, block 수, extension data 크기, fragment 수, 재조립 대기 시간에 명시적인
  상한을 둡니다.
- 수명 만료와 저장소 quota를 원자적으로 관리하고 우선순위 정책을 기록합니다.
- status report는 증폭 트래픽이 될 수 있으므로 기본 비활성화와 rate limit을 적용합니다.
- convergence layer는 긴 RTT에서 종단 간 반응형 제어에만 의존하지 말고 자체 rate limit
  또는 congestion control을 제공해야 합니다.
- BCB가 있어도 목적지와 시간 같은 primary metadata는 보일 수 있으므로 traffic analysis
  위험을 별도로 평가합니다.
- parsing 전에 전체 데이터를 메모리에 복제하지 말고 길이·중첩 깊이·정수 범위를 제한합니다.

## 후속 업데이트와 정오표

2026-09-11 기준 RFC Editor 정보 페이지는 RFC 9171이 RFC 9713과 RFC 9758에 의해
갱신됐음을 표시합니다. 구현 준수성을 평가할 때 세 문서를 하나의 규칙 집합으로 읽어야
합니다.

### 후속 RFC

| 문서 | 현재 구현에 미치는 영향 |
| --- | --- |
| RFC 9713 | BPv7 administrative record type은 IANA의 `Bundle Administrative Record Types`에서 version `7`로 표시된 값을 사용 |
| RFC 9758 | `ipn` URI를 allocator ID, node number, service number로 명확화하고 새 CBOR 표현과 호환 규칙 추가 |

### RFC Editor 정오표 상태

확인 당시 목록은 Verified 3건, Reported 1건, Held for Document Update 4건, Rejected 1건입니다.
상태는 바뀔 수 있으므로 배포 전 [정오표 원문](https://errata.rfc-editor.org/search/?rfc_number=9171)을
다시 확인합니다.

| ID·상태 | 영향 요약 | 적용 판단 |
| --- | --- | --- |
| 8043 · Verified | CRC 계산 시 CRC 값 bytes만 0으로 두고 CBOR byte-string header는 유지 | 구현과 테스트 벡터에 반영 |
| 8525 · Verified | 상태 보고서의 source node ID는 `dtn`뿐 아니라 `ipn`도 가능 | EID decoder를 scheme 하나로 제한하지 않음 |
| 7337 · Verified | Appendix B CDDL의 줄바꿈으로 생긴 문법 오류 | 기계 검증 시 교정된 CDDL 사용 |
| 8645 · Reported | block-type-specific data가 definite-length byte string임을 더 명확히 하자는 제안 | 미확정임을 표시하되 4.3.2와 CDDL을 함께 따름 |
| 7272 · Held | `dtn` URI의 demux/query 문법 정리 필요 | 향후 문서 갱신 추적 |
| 7881 · Held | 상태 Boolean의 CBOR simple value 표현 명료화 | RFC 8949의 true/false 인코딩 확인 |
| 8376 · Held | 단편화 시 확장 블록 배치 규칙이 MTU와 충돌할 수 있음 | 실전 단편화 설계에서 별도 위험 분석 |
| 8377 · Held | 재조립 후 원본 primary block과 보안 블록 검증 문제 | 보안 적용 단편화는 상호운용 시험 필수 |

Rejected 항목은 정정 규칙으로 적용하지 않습니다. 특히 Section 5.2의 전송 흐름을 5.4가 아닌
5.3으로 바꾸자는 Errata 8495는 rejected 상태이므로 원문을 임의로 변경하면 안 됩니다.

## 용어 정리

| 용어 | 한국어 설명 |
| --- | --- |
| ADU | Application Data Unit. 응용이 BP에 전달하거나 BP로부터 받는 데이터 단위 |
| AA | Application Agent. 응용별 기능과 관리 기능을 가진 노드 구성요소 |
| BP/BPv7 | Bundle Protocol/Version 7. RFC 9171의 지연 내성 전송 프로토콜 |
| BPA | Bundle Protocol Agent. BP 서비스와 처리 절차를 실행하는 구성요소 |
| BPSec | Bundle Protocol Security. BIB·BCB 보안 블록을 정의하는 RFC 9172 체계 |
| BIB | Block Integrity Block. 다른 블록의 무결성과 인증을 보호 |
| BCB | Block Confidentiality Block. primary를 제외한 대상 블록을 암호화 |
| Bundle | BP의 PDU. payload와 전달에 필요한 metadata를 묶은 단위 |
| Canonical Block | Primary Block 이외 모든 블록이 따르는 공통 외피 |
| CBOR | Concise Binary Object Representation. BPv7의 이진 데이터 표현 |
| CLA | Convergence-Layer Adapter. 특정 하위 전송/네트워크와 BPA를 연결 |
| DTN | Delay/Disruption-Tolerant Networking. 긴 지연과 연결 단절을 견디는 네트워크 |
| DTN time | 2000-01-01 00:00:00 UTC 이후 경과 밀리초. leap second는 세지 않음 |
| EID | Endpoint ID. bundle 목적지 등을 식별하는 URI |
| Fragment | 원본 ADU의 연속된 일부를 payload로 담은 bundle |
| Payload Block | block type 1, block number 1인 마지막 canonical block |
| Primary Block | version, EID, timestamp, lifetime 등 전달 핵심 정보를 담은 불변 블록 |
| Retention Constraint | bundle이 아직 폐기되지 못하도록 유지하는 처리 상태 |
| TCPCLv4 | TCP 위에서 bundle을 교환하는 RFC 9174 convergence-layer protocol |

## 실습 학습 가이드

노트북은 위에서 아래로 실행하면 됩니다. Python 표준 라이브러리만 사용하며, 각 단계가
이전 단계의 개념을 확장합니다.

### 환경

노트북은 Python 3.10 이상이 필요하며 Python 3.12.13으로 검증했습니다. 실행에는 Jupyter와
`nbconvert`가 필요하지만 노트북 코드 자체는 Python 표준 라이브러리만 사용합니다.

```powershell
python --version
jupyter notebook
```

`nbconvert`가 설치된 환경에서는 다음처럼 비대화형 실행 검증을 할 수 있습니다.

```powershell
python -m jupyter nbconvert --to notebook --execute --inplace `
  bundle-protocol-version-7/01_foundations.ipynb
```

### 1단계 — [기초 실습](01_foundations.ipynb)

학습 목표:

- 연결 시간표가 있는 작은 DTN에서 store-carry-forward를 추적합니다.
- DTN time, creation timestamp, lifetime과 bundle age의 관계를 계산합니다.
- 교육용 CBOR encoder로 정수, byte string, array의 바이트 구조를 확인합니다.

완료 기준: 각 bundle이 `보관`, `전달 가능`, `만료` 중 어떤 상태인지 근거와 함께 설명할 수
있습니다.

### 2단계 — [응용 실습](02_practice.ipynb)

학습 목표:

- Primary/Canonical Block 데이터 모델과 구조 제약을 검증합니다.
- X-25 CRC-16과 CRC32C를 계산하고 CRC 필드 처리 규칙을 확인합니다.
- payload를 fragment로 나누고 순서가 뒤섞인 입력을 방어적으로 재조립합니다.

완료 기준: 잘못된 block number, payload 위치, CRC 또는 fragment 범위를 테스트가 거부하게
만들 수 있습니다.

### 3단계 — [심화 실습](03_advanced.ipynb)

학습 목표:

- BPA의 수신·dispatch·forward·deliver·expire 흐름을 상태 머신으로 모델링합니다.
- Previous Node, Bundle Age, Hop Count가 forwarding에서 어떻게 바뀌는지 추적합니다.
- 알 수 없는 extension block, 저장소 quota, hop limit, lifetime과 malformed input을
  실패 주입으로 시험합니다.

완료 기준: 각 거부·삭제 결정이 형식 오류, 정책, 자원 제한, 수명 또는 hop limit 중 어느
근거에 의한 것인지 event log에서 구분할 수 있습니다.

### 실습의 경계

노트북의 객체와 encoder는 wire-compatible 라이브러리를 대체하지 않습니다. 실제 구현을
만들려면 다음이 추가로 필요합니다.

- RFC 8949 deterministic CBOR 전체 구현 또는 검증된 라이브러리
- RFC 9171 Appendix B CDDL과 공식/상호운용 테스트 벡터
- RFC 9172 BPSec 및 위협 모델에 맞는 키 관리
- RFC 9174 같은 실제 CLA와 영속 저장소
- RFC 9713·9758 및 최신 IANA registry 반영
- fuzzing, resource limit, crash recovery, 중복 억제, 시계 불확실성 시험

## 구현 점검표

- [ ] outer bundle array, Primary Block 1개, 마지막 Payload Block 1개를 검증한다.
- [ ] canonical block number의 유일성과 payload number `1`을 검증한다.
- [ ] Primary Block이 중계 중 바뀌지 않도록 한다.
- [ ] deterministic CBOR와 definite-length block data 규칙을 검증한다.
- [ ] CRC 값 bytes만 0으로 두는 Verified Errata 8043을 반영한다.
- [ ] lifetime과 Bundle Age를 밀리초로 처리하고 integer overflow를 검사한다.
- [ ] `dtn` 및 RFC 9758이 갱신한 `ipn` EID를 처리한다.
- [ ] unknown extension block의 processing flags를 정확히 적용한다.
- [ ] fragment 범위·중복·충돌·총 크기와 reassembly 자원을 제한한다.
- [ ] status report를 기본 비활성화하고 rate limit을 둔다.
- [ ] CRC를 보안 기능으로 취급하지 않고 BPSec 정책을 정의한다.
- [ ] CLA가 rate limiting 또는 congestion control을 제공하는지 확인한다.
- [ ] 최신 RFC Editor 정오표와 IANA registry를 배포 시점에 다시 확인한다.
- [ ] BPv6와 BPv7의 wire interoperability를 가정하지 않는다.

## 다음 학습 경로

1. 이 폴더의 세 노트북으로 시간, 형식, 처리 상태를 순서대로 익힙니다.
2. RFC 9171 Appendix B의 CDDL을 RFC 8949·RFC 8610과 함께 읽고 실제 CBOR diagnostic
   notation과 비교합니다. Appendix B는 참고용이며 본문과 충돌하면 본문이 우선입니다.
3. RFC 9172의 BIB/BCB 대상 지정과 canonicalization을 학습합니다.
4. [RFC 9173](https://www.rfc-editor.org/rfc/rfc9173.html)의 기본 BPSec context와
   상호운용 테스트 구성을 확인합니다.
5. RFC 9174 TCPCLv4의 session negotiation, transfer, message framing을 연결합니다.
6. RFC 9713의 administrative record registry와 RFC 9758의 최신 `ipn` 규칙을 구현에
   합칩니다.
7. [RFC 9675](https://www.rfc-editor.org/rfc/rfc9675.html)의 DTN Management Architecture로
   상태·구성·운영 관측 범위를 확장합니다.
8. IETF DTN의 공개 구현과 테스트 벡터를 이용해 상호운용 시험을 수행합니다.
9. 저장소 고갈, 중복 bundle, clock drift, contact 중단, 프로세스 재시작, 악성 CBOR를
   포함한 장애 주입 시험으로 운영 준비도를 확인합니다.

가장 중요한 원칙은 **RFC 번호 하나를 고정된 문서로만 보지 않는 것**입니다. Standards
Track 본문, 이를 갱신하는 RFC, IANA registry, Verified Errata를 함께 추적해야 실제
상호운용 가능한 BPv7 구현에 가까워집니다.
