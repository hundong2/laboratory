<!-- rumdl-disable MD013 -->

# RFC 9171: 번들 프로토콜 버전 7 — 한국어 번역·해설

[학습 가이드로 돌아가기](README.md)

## 문서 정보와 번역 범위

| 항목 | 내용 |
| --- | --- |
| 원문 제목 | *Bundle Protocol Version 7* |
| 문서 | RFC 9171 |
| 저자 | Scott Burleigh, Kevin Fall, Edward J. Birrane III |
| 발행 주체·상태 | IETF, Standards Track / Proposed Standard |
| 발행일 | 2022년 1월 |
| DOI | `10.17487/RFC9171` |
| 사용자 제공 URL·최종 URL | <https://www.rfc-editor.org/rfc/rfc9171.html> |
| 상태·갱신 정보 | <https://www.rfc-editor.org/info/rfc9171/> |
| 원문 언어 | 영어 |
| 접근·검수일 | 2026-09-11 |
| 접근 결과 | 로그인·paywall 없이 공식 HTML 전체 본문 확인 |
| 후속 갱신 | RFC 9713, RFC 9758 |
| 공식 errata 상태 | Verified 3 / Reported 1 / Held for Document Update 4 / Rejected 1 |

이 문서는 RFC 9171의 초록, 상태·저작권 고지, 1~10절, 부록 A·B,
감사의 글과 저자 정보를 원문 순서대로 따라가는 한국어 번역·해설이다.
프로토콜을 구현하거나 상호운용성을 시험할 때 필요한 데이터 구조, 필드 순서,
비트 위치, 수치 범위와 처리 절차를 보존하되, 원문 전문을 문장별로 복제하지 않고
절별로 재구성한 상세 번역 요약을 제공한다. ABNF와 CDDL도 전체 원문 대신
구조를 이해하는 데 필요한 형태만 설명한다.

RFC Editor 상태 페이지 기준으로 RFC 9171은 다음 문서에 의해 갱신되었다.

- [RFC 9713](https://www.rfc-editor.org/rfc/rfc9713.html)(2025년 1월)은 BPv7 관리 레코드 형식이
  IANA의 `Bundle Administrative Record Types` 레지스트리를 사용하도록 명확히 하고,
  실험·사설 사용 범위를 정한다.
- [RFC 9758](https://www.rfc-editor.org/rfc/rfc9758.html)(2025년 5월)은 `ipn` URI를
  할당자 식별자·노드 번호·서비스 번호의 3요소 구조로 확장하고 텍스트 및 CBOR 표현을 갱신한다.

따라서 아래 4.2.5.1.2절과 6.1절은 RFC 9171의 발행 당시 규칙을 설명하면서,
현재 구현이 따라야 할 갱신 사항을 별도 주석으로 표시한다. 실제 배포에서는 이 문서만으로
규격 적합성을 판단하지 말고 RFC 9171 원문, 위 갱신 RFC, 최신 IANA 레지스트리와
공식 errata를 함께 확인해야 한다.

### 저작권과 재사용 경계

원문은 IETF Trust 및 저자들의 저작권 고지와 BCP 78, 발행 당시의 IETF Trust Legal
Provisions 적용을 받는다. 원문에서 추출하는 Code Components에는 해당 고지가 정한
Revised BSD License 문구가 필요하며 보증 없이 제공된다. 이 자료는 학습을 위한 독자적
한국어 해설이고 원문의 법적·규범적 대체물이 아니다. 긴 직접 인용과 원문 전체 복제를 피했다.

## 읽기 전에: 규범 키워드 번역 원칙

RFC 9171에서 아래 단어가 **모두 대문자**로 쓰였을 때만 BCP 14(RFC 2119 및 RFC 8174)의
규범적 강도를 가진다. 이 자료는 요구 수준을 잃지 않도록 영문 키워드를 병기한다.

| 원문 키워드 | 이 문서의 표현 | 구현 판단 기준 |
| --- | --- | --- |
| `MUST`, `REQUIRED`, `SHALL` | 반드시 해야 한다 / 필수이다 | 적합한 구현이 지켜야 하는 절대 요구사항 |
| `MUST NOT`, `SHALL NOT` | 절대로 해서는 안 된다 / 금지된다 | 적합성 유지를 위한 절대 금지 |
| `SHOULD`, `RECOMMENDED` | 하는 것이 좋다 / 권고한다 | 정당한 사유와 결과를 충분히 이해한 경우에만 이탈 가능 |
| `SHOULD NOT`, `NOT RECOMMENDED` | 하지 않는 것이 좋다 / 권고하지 않는다 | 예외가 가능하지만 영향을 신중히 평가해야 함 |
| `MAY`, `OPTIONAL` | 해도 된다 / 선택 사항이다 | 구현자가 지원 여부를 선택할 수 있음 |

원문의 소문자 `must`, `should`, `may`는 문맥상 일반 서술일 수 있으므로 대문자 키워드와
동일한 적합성 요구로 확대하지 않는다. 이 문서에서 단순 설명을 위해 쓰는 “필요하다”도
바로 옆에 대문자 키워드가 없는 한 새로운 규범 요구를 만드는 표현이 아니다.

## 초록

RFC 9171은 IRTF의 Delay-Tolerant Networking Research Group이 실험 규격 RFC 5050으로
개발한 Bundle Protocol(BP)을 실무 경험에 맞게 다듬어 표준화한 BP 버전 7(BPv7) 규격이다.
연결이 끊기거나 지연이 매우 큰 환경에서도 응용 데이터와 필요한 메타데이터를 하나의
“번들”로 저장·운반·전달하는 방식, 그 바이너리 형식과 노드 처리 절차를 정의한다.

## 이 메모의 상태

이 문서는 IETF 커뮤니티의 합의, 공개 검토와 IESG 승인을 거친 Internet Standards Track
문서다. RFC Editor 정보 페이지는 현재 성숙도를 Proposed Standard로 표시한다. 현 상태,
errata와 피드백 경로는 위의 상태·갱신 정보 링크에서 확인한다.

## 저작권 고지

2022 IETF Trust와 문서 저자에게 저작권이 있다. 적용되는 권리·제한은 BCP 78과 IETF Trust
Legal Provisions가 정하며, 원문에서 떼어 낸 코드 구성요소에는 Revised BSD License 조건이
적용된다. 정확한 법적 문구는 RFC 원문을 따른다.

## 1. 소개(Introduction)

BPv7은 2007년의 실험 규격 RFC 5050을 여러 언어와 플랫폼에서 구현·배포하며 얻은 경험을
반영한다. 목표는 프로토콜을 더 단순하고 유능하며 사용하기 쉽게 만드는 것이다.
RFC 9171 구현은 RFC 5050 구현과 wire-level 상호운용되지 않는다.

DTN(Delay-Tolerant Networking, 지연 허용 네트워킹)은 다음과 같은 “스트레스가 큰”
통신 환경을 대상으로 한다.

- 연결이 간헐적으로만 열림
- 지연이 크거나 변동 폭이 큼
- 비트 오류율이 높음
- 송신자와 수신자가 동시에 네트워크에 존재하지 않을 수 있음

BP는 여러 하위 네트워크 위의 응용 계층에 놓이는 저장-운반-전달(store-carry-forward)
오버레이로 볼 수 있다. 데이터가 저장 매체와 함께 물리적으로 이동하는 경우를 활용하고,
오류 제어 책임을 노드 사이에서 옮길 수 있으며, 연속·예정·예측·기회적 연결과 단방향 연결을
모두 활용한다. 또한 BP EID를 실제 하위 네트워크 주소에 늦게 결합할 수 있다.

각 하위 네트워크의 전송·네트워크 프로토콜과 BP 사이 계층이 convergence layer이며,
구체 프로토콜을 BP에 연결하는 구성요소가 CLA(convergence-layer adapter)다. 이 RFC가
직접 규정하는 것은 노드 사이에 전달되는 PDU인 bundle의 형식과 BPA의 처리 절차다.
다음 항목은 범위 밖이다.

- 특정 하위 네트워크에서 CLA가 데이터를 운반하는 내부 동작. 다만 CLA가 BPA에 제공해야 할
  최소 서비스는 7절에서 정한다.
- 번들 경로 계산 알고리즘과 라우팅·포워딩 정보 기반을 채우는 방식
- 운송 중 번들을 보호하는 구체 보안 메커니즘. 보안 규격은 BPSec이 담당한다.
- 번들 노드 관리 메커니즘

## 2. 문서에서 사용하는 규약(Conventions Used in This Document)

대문자 `MUST`, `MUST NOT`, `REQUIRED`, `SHALL`, `SHALL NOT`, `SHOULD`,
`SHOULD NOT`, `RECOMMENDED`, `NOT RECOMMENDED`, `MAY`, `OPTIONAL`은
BCP 14가 정한 요구 수준으로 해석한다. 앞의 번역 원칙 표는 이 의미를 한국어로 보존하기 위한
기준이다.

## 3. 서비스 설명(Service Description)

### 3.1 정의(Definitions)

| 용어 | 한국어 설명 |
| --- | --- |
| Bundle | BP의 PDU. 응용 데이터와 전달 후 즉시 사용하기 위한 메타데이터를 함께 묶은 것으로, 두 개 이상의 protocol block으로 구성된다. |
| Block | 올바른 형식의 bundle을 함께 이루는 프로토콜 데이터 구조 하나다. |
| ADU (Application Data Unit) | 조각이 아닌 번들이 목적지까지 운반하려는 응용 데이터 단위다. |
| Bundle payload | payload block의 내용. 비조각 번들에서는 ADU 자체다. |
| Partial payload | 길이 `M`인 payload의 처음 또는 마지막 `N`바이트이며 `0 < N < M`이다. 다시 부분 payload로 나눌 수 있다. |
| Fragment | payload block에 partial payload를 담은 번들이다. |
| Bundle node | 번들을 송신하거나 수신할 수 있는 개체다. 개념적으로 BPA, 0개 이상의 CLA, application agent로 구성된다. |
| BPA (Bundle Protocol Agent) | BP 서비스를 제공하고 이 RFC의 절차를 수행하는 노드 구성요소다. |
| CLA | BPA를 대신하여 특정 하위 프로토콜 스택으로 번들을 송수신하는 어댑터다. |
| AA (Application Agent) | 사용자 목적의 통신을 위해 BP 서비스를 쓰는 구성요소다. administrative element와 application-specific element로 나뉜다. |
| Application-specific element | 사용자 ADU를 만들고 전송을 요청하며, 전달받아 처리한다. |
| Administrative element | 상태 보고를 포함한 관리 레코드를 생성·전송 요청하고, 수신·처리한다. |
| Administrative record | 노드의 administrative element끼리 BP 관리 목적으로 교환하는 ADU다. RFC 9171 자체가 정의하는 형식은 bundle status report다. |
| Bundle endpoint | 하나의 공통 EID로 자신을 식별하는 0개 이상 노드의 집합이다. |
| Singleton endpoint | 언제나 정확히 한 노드만 포함하는 endpoint다. |
| Registration | 한 노드의 endpoint 가입 상태를 나타내는 로컬 상태기계다. `Active` 또는 `Passive`이며 delivery failure action을 가진다. BP는 registration 정보를 다른 노드로 배포하지 않는다. |
| Delivery | payload ADU와 관련 메타데이터가 registration 상태에 맞게 application agent에 제시된 순간 성립한다. 응용이 payload를 처리 완료했다는 뜻은 아니다. |
| Deliverability | 목적지 EID가 registration의 endpoint와 같고, 아직 그 registration에 전달되거나 포기되지 않았을 때만 성립한다. |
| Abandonment | 특정 registration 관점에서 그 번들을 더는 전달 가능하지 않다고 선언하는 것이다. |
| Delivery failure action | Passive registration에서 전달 가능한 번들을 받았을 때 취할 동작이다. |
| Destination | 번들이 전달되어야 할 노드 집합인 endpoint다. |
| Transmission | application agent의 요청에 따라 BPA가 목적지 endpoint 구성원에게 번들 복사본을 전달하려는 시도 전체다. |
| Forwarding | 하나 이상의 CLA를 지속적으로 사용해 특정 노드가 번들 복사본을 받게 하려는 동작이다. Transmission과 동일한 개념이 아니다. |
| Discarding | 모든 처리를 중단하고 번들 참조를 기능적으로 지워 저장소를 해제할 수 있게 하는 구현 동작이다. |
| Retention constraint | 존재하는 동안 번들을 discard하지 못하게 하는 상태 요소다. |
| Deletion | 모든 retention constraint를 무조건 제거하여 discard가 가능하게 만드는 프로토콜 절차다. |

번들 노드의 개념적 데이터 흐름은 다음과 같다.

```text
사용자 ADU / 관리 레코드
          ↕
Application Agent (응용 전용 요소 + 관리 요소)
          ↕ BP 서비스·개인 제어 인터페이스
Bundle Protocol Agent
          ↕ 번들
CLA 1 ... CLA n
          ↕ 하위 네트워크 PDU
각 constituent network
```

### 3.2 BP 개념 논의(Discussion of BP Concepts)

- 같은 논리 번들의 여러 복사본이 서로 다른 노드의 저장소와 링크 위에 동시에 있을 수 있고,
  중간 노드가 확장 블록을 바꾸어 복사본의 일부 블록이 달라질 수도 있다.
- 노드·BPA·AA의 구현 형태는 프로세스, 스레드, 객체, 데몬, 공유 라이브러리, 전용 하드웨어
  등 무엇이든 될 수 있다. 이 RFC는 개념적 기능과 외부 동작을 규정한다.
- CLA는 BP와 하위 스택 사이에서 다중화 정도만 제공할 수도 있고 별도 기능을 제공할 수도 있다.
  CLA 및 CL 프로토콜의 구체 정의는 이 RFC 범위 밖이다.
- 원래 번들의 바이트열을 다른 번들의 ADU로 넣는 bundle-in-bundle 터널링이 가능하다.
  수신 측 administrative element가 내부 번들을 다시 BPA에 dispatch하도록 지시한다.
- application-specific element와 BPA 사이는 BP 서비스 인터페이스뿐이다. administrative element는
  그 외에도 BPA와 서로 동작을 지시하는 개념적 private control interface를 가진다.
- 라우터 전용 노드에는 application-specific element가 없을 수 있다. 반대로 한 application agent가
  여러 응용에 복합 DTN 서비스를 제공할 수도 있다.
- endpoint는 0개 이상 노드의 집합이며 한 노드가 여러 endpoint에 가입할 수 있다. 모든 노드는
  관리 레코드를 받는 singleton administrative endpoint에 영구 등록되고, 그 EID는 node ID가 된다.
- 번들 source node ID로 null endpoint를 쓰면 anonymous bundle이다. 이때 번들을 유일하게
  식별할 수 없으므로 조각화와 상태 보고 기능이 제한된다.
- BP 자체는 종단 간 delivery를 보장하지 않는다. 신뢰성 있는 CLA로 홉별 손실을 줄일 수 있으나,
  종단 간 보장은 BP 확장 또는 응용 계층 메커니즘이 필요하다.
- 확장 규격은 블록, 관리 레코드, 제어 플래그, 상태 보고 종류·사유와 특정 처리 시점의 의무를
  추가할 수 있다.

### 3.3 BPA가 제공하는 서비스(Services Offered by Bundle Protocol Agents)

각 BPA는 application agent에 다음 기능을 제공할 것으로 기대된다.

- endpoint registration 시작과 종료
- registration의 Active/Passive 전환
- 지정 endpoint로 bundle transmission 요청
- transmission 취소
- Passive registration polling
- 수신 번들 delivery

registration API의 구체 형태와 내부 구현은 규격 범위 밖이다.

## 4. 번들 형식(Bundle Format)

### 4.1 번들 구조(Bundle Structure)

번들은 CBOR(Concise Binary Object Representation, RFC 8949)를 따라야 한다(`SHALL`).
서명·해시 검증 양쪽이 같은 octet sequence를 보게 하려고 모든 필드의 CBOR 인코딩은
RFC 8949의 core deterministic encoding 요구를 따라야 한다(`MUST`). 단, indefinite-length
item 자체는 금지하지 않는다.

전송 단위의 논리 형태는 다음과 같다.

```text
indefinite-length CBOR array(
  primary block,           # 정확히 1개, 암묵적 block number 0
  zero or more extension blocks,
  payload block,           # 정확히 1개, block number 1, 항상 마지막
  break
)
```

번들은 최소 두 블록이며, primary block 뒤에는 하나 이상의 canonical block이 온다. payload도
canonical block의 한 종류다. 그 밖의 canonical block 번호는 블록 순서와 무관하지만 번들 안에서
유일해야 한다. 구현은 비적합 바이트열을 버려도 되고(`MAY`), 처리 전에 적합 구조로 변환해
수용해도 된다(`MAY`). 변환 절차는 규격 범위 밖이다.

### 4.2 BP 기본 데이터 구조(BP Fundamental Data Structures)

#### 4.2.1 CRC 유형(CRC Type)

CRC type은 CBOR unsigned integer이며 허용값은 다음 세 개뿐이다.

| 값 | 의미 |
| --- | --- |
| `0` | CRC 없음 |
| `1` | 표준 X-25 CRC-16 |
| `2` | CRC32C(Castagnoli) CRC-32 |

CRC보다 강한 무결성 보호가 필요하면 BPSec의 BIB(Block Integrity Block)를 사용한다.

#### 4.2.2 CRC

CRC type이 0일 때 그리고 그때에만 CRC 필드를 생략해야 한다(`SHALL`). type 1은 2바이트,
type 2는 4바이트의 definite-length CBOR byte string이며, 각각 16비트·32비트 unsigned
integer를 network byte order로 담아야 한다(`SHALL`).

#### 4.2.3 번들 처리 제어 플래그(Bundle Processing Control Flags)

primary block의 CBOR unsigned integer bit field가 번들 전체 속성을 나타낸다. 비트 번호는
최하위 비트를 0으로 잡는다.

| 비트 | 16진수 | BPv7 의미 |
| ---: | ---: | --- |
| 0 | `0x000001` | 번들이 fragment임 |
| 1 | `0x000002` | ADU가 administrative record임 |
| 2 | `0x000004` | 번들을 fragment로 나누면 안 됨 |
| 3~4 |  | Reserved |
| 5 | `0x000020` | 사용자 응용의 acknowledgement 요청 |
| 6 | `0x000040` | 모든 status report에 상태 시각 요청 |
| 7~13 |  | Reserved |
| 14 | `0x004000` | bundle reception 보고 요청 |
| 15 |  | Reserved |
| 16 | `0x010000` | bundle forwarding 보고 요청 |
| 17 | `0x020000` | bundle delivery 보고 요청 |
| 18 | `0x040000` | bundle deletion 보고 요청 |
| 19~20 |  | Reserved |
| 21~63 |  | Unassigned |

핵심 조합 제약은 다음과 같다.

- ADU가 administrative record이면 모든 status-report request bit는 0이어야 한다(`MUST`).
- source node ID가 null endpoint인 anonymous bundle이면 bit 2가 1이어야 하고(`MUST`),
  모든 status-report request bit는 0이어야 한다(`MUST`).
- 알 수 없는 bundle processing flag는 미래 확장과의 호환을 위해 무시해야 한다(`MUST`).

#### 4.2.4 블록 처리 제어 플래그(Block Processing Control Flags)

각 canonical block header의 CBOR unsigned integer bit field가 그 블록의 처리 방식을 정한다.

| 비트 | 16진수 | BPv7 의미 |
| ---: | ---: | --- |
| 0 | `0x01` | 모든 fragment에 이 block을 복제 |
| 1 | `0x02` | block을 처리할 수 없으면 status report 전송 |
| 2 | `0x04` | block을 처리할 수 없으면 bundle 삭제 |
| 3 | `0x08` | Reserved |
| 4 | `0x10` | block을 처리할 수 없으면 해당 block 폐기 |
| 5~6 |  | Reserved |
| 7~63 |  | Unassigned |

알 수 없는 block flag는 무시해야 한다(`MUST`). administrative-record bundle과 anonymous
bundle의 모든 canonical block에서는 비트 1이 반드시 0이어야 한다(`MUST`).

#### 4.2.5 식별자(Identifiers)

##### 4.2.5.1 Endpoint ID

EID(Endpoint ID)는 endpoint를 나타내는 URI다. 일반 형태는 `scheme:scheme-specific-part`이며,
허용 scheme은 IANA `Bundle Protocol URI Scheme Types` 레지스트리에 code number와 함께
등록된다. 각 scheme 규격은 SSP의 해석과 BP 전송용 CBOR 인코딩을 정의해야 한다(`MUST`).

모든 EID의 wire representation은 정확히 두 항목인 CBOR array여야 한다(`SHALL`).

```text
[URI scheme code: unsigned integer, scheme별 SSP의 CBOR 표현]
```

###### 4.2.5.1.1 `dtn` URI scheme

`dtn`은 문자 기반 endpoint 식별을 제공한다. 핵심 텍스트 형태는 null endpoint인
`dtn:none` 또는 `dtn://<node-name>/<demux>`다. `demux`의 첫 문자가 `~`가 아니면
singleton endpoint이고, `~`이면 singleton이 아니다. 길이 0인 demux는 해당 node-name의
administrative endpoint를 식별하고 node ID로 쓸 수 있다(`MAY`). 길이가 0이 아닌 demux는
node ID로 쓸 수 없다.

BP EID로 전송할 때 SSP는 CBOR text string이어야 한다(`SHALL`). 단 `none`은 unsigned
integer 0으로 표현한다(`SHALL`). 그 밖의 표현은 US-ASCII다. BP만으로 endpoint 도달 가능성이나
상대 신원을 보장하지 않으므로 primary block을 대상으로 하는 BIB 보호를 검증해야 한다.
악의적 node-name·demux, 위조 source, 트래픽 분석을 고려하고, 필요하면 EID를 노출하지 않는
보안 CLA를 사용한다.

###### 4.2.5.1.2 `ipn` URI scheme

**RFC 9171 발행 당시 규칙:** `ipn:<node-number>.<service-number>` 형태의 두 unsigned
integer로 endpoint를 간결하게 표현한다. 모든 `ipn` endpoint는 singleton이다. service number가
0인 EID는 node number의 administrative endpoint 및 node ID로 쓸 수 있다(`MAY`); 0이 아닌
service number의 EID는 그렇게 쓸 수 없다. wire SSP는 `[node-number, service-number]`의
2항목 CBOR array이며, 텍스트 표현은 US-ASCII다.

도달 가능성과 처리 주체 신원은 BP 자체가 보장하지 않는다. 숫자를 악의적으로 선택한 목적지나
source를 신뢰해서는 안 되고, 수신 노드는 사용 전에 authenticity와 validity를 검증하는 것이 좋다.
EID 노출은 트래픽 분석에 쓰일 수 있다.

**현재 적용할 갱신:** RFC 9758은 `ipn`을
`(allocator identifier, node number, service number)` 3요소로 정의한다. 기존 2항목 SSP
인코딩은 FQNN(allocator와 node를 64비트로 결합)과 service number를 담는 하위 호환 형식으로
남고, 새 3항목 SSP 인코딩도 허용된다. 같은 EID의 두 표현은 디코딩한 의미를 기준으로 같다고
비교해야 한다(`MUST`). 비기본 allocator나 3항목 encoding을 처리하려면 기존 구현 갱신이
필요하므로 새 코드는 RFC 9758의 텍스트·CBOR·상호운용 규칙을 직접 따라야 한다.

##### 4.2.5.2 Node ID

노드와 endpoint는 다르지만 별도 namespace를 만들지 않고 EID로 노드를 식별한다. 모든 노드는
administrative record를 받는 singleton administrative endpoint에 영구 등록된다. 그 EID는
해당 노드를 유일하게 식별해야 한다(`SHALL`). 임의의 singleton endpoint EID도 유일 구성원을
가리키는 node ID로 사용할 수 있다.

#### 4.2.6 DTN 시각(DTN Time)

DTN time은 DTN epoch인 `2000-01-01 00:00:00 UTC` 이후 경과한 밀리초 수를 나타내는
unsigned integer다. 윤초의 영향을 받지 않는다. CBOR unsigned integer로 표현해야 하며
(`SHALL`), 실제 값은 거의 항상 `2^32 - 1`보다 크므로 구현의 정수 폭을 주의한다. 값 0은
시각을 모른다는 뜻이다.

#### 4.2.7 생성 타임스탬프(Creation Timestamp)

각 bundle creation timestamp는 다음 두 항목의 CBOR array여야 한다(`SHALL`).

1. transmission request를 받아 번들을 만든 DTN time
2. source BPA가 관리하는 단조 증가 sequence number

현재 시간이 1밀리초 전진할 때 sequence counter를 0으로 재설정해도 된다(`MAY`). 정확한 시계가
없는 노드는 creation time을 0으로 두고 sequence counter를 절대로 0으로 재설정하지 않는 것이
권고된다. 동일 source node ID와 동일 creation timestamp로 서로 다른 번들을 만들면 식별 충돌과
비정상 네트워크 동작이 발생할 수 있다.

#### 4.2.8 블록 유형별 데이터(Block-Type-Specific Data)

primary block 이외 각 block의 type-specific data는 해당 block-type 규격이 정의하는 내용의
CBOR 표현이어야 한다(`SHALL`).

### 4.3 블록 구조(Block Structures)

#### 4.3.1 Primary Bundle Block

primary block은 목적지까지 forwarding하는 데 필요한 기본 정보를 담고 생성 후 delivery까지
불변이어야 한다. 모든 필드의 CBOR-encoded value가 바뀌어서는 안 된다(`MUST`). array 항목 수는
다음과 같다.

| fragment 여부 | primary CRC 여부 | 항목 수 |
| --- | --- | ---: |
| 아니요 | 없음 | 8 |
| 아니요 | 있음 | 9 |
| 예 | 없음 | 10 |
| 예 | 있음 | 11 |

필드는 아래 순서로 나타나야 한다(`MUST`).

1. **Version**: CBOR unsigned integer `7`.
2. **Bundle Processing Control Flags**: 4.2.3절 bit field.
3. **CRC Type**: primary block을 대상으로 하는 BPSec BIB가 있으면 0이어도 된다(`MAY`).
   그렇지 않으면 0이 아니어야 한다(`MUST`).
4. **Destination EID**: delivery 대상 endpoint.
5. **Source Node ID**: 최초 전송 노드. 익명을 선택하면 null EID가 가능하다.
6. **Report-to EID**: forwarding·delivery status report 수신 endpoint.
7. **Creation Timestamp**: source와 함께 transmission request를 식별한다.
8. **Lifetime**: creation time 이후 payload가 유효한 밀리초 수인 CBOR unsigned integer.
9. **Fragment Offset**: fragment flag가 있을 때만 반드시 존재하며, 원 ADU 시작부터 현재
   payload 시작까지의 byte offset이다.
10. **Total ADU Length**: fragment flag가 있을 때만 반드시 존재하며 원 ADU 전체 byte 길이다.
11. **CRC**: primary를 대상으로 하는 BIB가 없으면 반드시 존재한다(`SHALL`). BIB가 있으면
    있어도 된다(`MAY`).

age가 lifetime을 넘으면 보존·forwarding할 필요가 없으므로 삭제하는 것이 좋다(`SHOULD`). 너무
긴 lifetime이 노드를 압박하거나 DoS로 판단되면 BPA가 더 짧은 임시 effective lifetime을
적용해도 된다(`MAY`). 이 override는 primary의 원 lifetime을 바꾸면 안 되며(`SHALL NOT`),
그 노드에 머무는 동안에만 유효하다. 시계가 부정확하면 Bundle Age block을 사용하도록 권고한다.

Verified Errata 8043에 따라 CRC 계산 시에는 CRC **값 바이트**만 0으로 임시 채우고,
CRC field를 나타내는 CBOR byte-string의 initial/header byte는 바꾸지 않는다. 이 상태에서
CBOR break를 포함한 primary block 전체 바이트에 대해 계산해야 한다(`SHALL`).

#### 4.3.2 Canonical Bundle Block Format

primary 이외 모든 block은 canonical block이다. CRC type이 0이면 5항목, 아니면 6항목 CBOR
array여야 하며(`SHALL`), 필드 순서는 다음과 같다(`MUST`).

1. **Block type code**: payload는 1. `192~255`는 private/experimental 용도다.
2. **Block number**: 번들 안에서 유일한 CBOR unsigned integer. payload는 항상 1이다.
3. **Block processing control flags**
4. **CRC type**
5. **Block-type-specific data**: 하나의 definite-length CBOR byte string. payload block에서는
   ADU 전체 또는 연속된 일부를 담는다.
6. **CRC**: CRC type이 0이 아닐 때만 존재한다. 0으로 채운 CRC 필드와 CBOR break를 포함한
   block 전체 바이트로 계산한다.

### 4.4 확장 블록(Extension Blocks)

primary와 payload를 제외한 모든 block이 extension block이다. BPv7 구현은 이 RFC의 세 확장
유형을 인식·parse·처리하는 절차를 반드시 포함해야 하지만(`MUST`), 생성 기능까지 반드시
제공할 필요는 없다. 알 수 없는 확장 block은 해당 block processing flags가 요구하는 대로
보고·bundle 삭제·block 제거·그대로 유지 중 하나로 처리한다.

다른 BP 및 extension 규격의 의무를 모두 지키는 범위에서 BPA는 extension block을 삽입하거나
제거해도 된다(`MAY`). 다만 제거하면 의도된 처리가 사라질 수 있고, BPSec security block의
target인 block을 제거하면 검증이 불가능해질 수 있다.

#### 4.4.1 Previous Node

block type `6`이며 현재 노드에 번들을 forward한 직전 노드의 node ID를 담는다. 현재 노드가
source이면 이 block이 있어서는 안 된다(`MUST NOT`). 그 밖의 경우 하나를 두는 것이 좋고
(`SHOULD`), 두 개 이상은 금지된다(`MUST NOT`).

#### 4.4.2 Bundle Age

block type `7`이며 생성부터 가장 최근 forwarding까지 알려진 residence time과 propagation
time의 합을 밀리초 CBOR unsigned integer로 담는다. 정확한 계산법은 구현 사항이다.

- creation time이 0이면 정확히 한 개가 반드시 있어야 한다(`MUST`).
- creation time이 0이 아니면 최대 한 개를 둘 수 있다(`MAY`).
- 어떤 경우에도 여러 Bundle Age block을 넣어서는 안 된다(`MUST NOT`).

#### 4.4.3 Hop Count

block type `10`이며 `[hop-limit, hop-count]`의 두 CBOR unsigned integer를 담는다. hop은 한
노드에서 다른 노드로 한 번 forwarding한 사건이다.

- hop limit은 `1~255`여야 한다(`MUST`). 생성 뒤에는 바꾸지 않는 것이 좋다(`SHOULD NOT`).
- hop count는 처음 0이 좋고, hop마다 1씩 늘리는 것이 좋다(`SHOULD`).
- count가 limit을 넘으면 `Hop limit exceeded` 사유로 삭제하는 것이 좋다(`SHOULD`).
- bundle당 한 개는 허용되지만(`MAY`) 두 개 이상은 금지된다(`MUST NOT`).

이 block은 잘못된 routing 때문에 두 노드 사이를 계속 오가는 번들을 제거하는 안전장치다.

## 5. 번들 처리(Bundle Processing)

이 절과 6절의 절차는 BPA 및 application agent의 administrative element가 수행할 기본 동작을
규정하지만 완전하거나 배타적인 목록은 아니다. BPSec을 포함한 후속 DTN 규격이 처리 의무를
추가·재정의·대체할 수 있다.

### 5.1 관리 레코드 생성(Generation of Administrative Records)

모든 bundle transmission은 application agent가 BPA에 제출한 요청에서 시작한다. BPA가 status
report 같은 administrative record를 “생성”해야 할 때는 개념상 administrative element에 레코드
작성과 이를 payload로 하는 새 bundle transmission을 요청하도록 지시한다. 실제 구현 분리는
자유지만 6절의 제약은 지켜야 한다.

status report는 작아도 경로의 노드가 `N`개인 단일 번들에 대해 최악에 가까운 경우
`1 + 2 × (N - 1)`개의 보고 번들을 만들 수 있다. 대량 요청은 네트워크를 증폭시킬 수 있으므로
status report 생성은 기본값으로 반드시 꺼져 있어야 하며(`MUST`), 과도한 트래픽 위험을
수용할 수 있다고 판단한 때만 켠다.

보고 용어는 네 개의 상태 assertion과 대응한다.

- reception status report: reporting node가 bundle을 수신함
- forwarding status report: reporting node가 bundle을 forward함
- delivery status report: reporting node가 application agent에 payload를 전달함
- deletion status report: reporting node가 bundle을 삭제함

### 5.2 번들 전송(Bundle Transmission)

1. transmission request의 매개변수대로 outbound bundle을 만들고 `Dispatch pending` retention
   constraint를 붙여야 한다(`MUST`). source node ID는 anonymous를 뜻하는 null EID 또는 현재
   BPA 노드만 구성원인 singleton endpoint의 EID여야 한다(`MUST`).
2. 5.4절 Bundle Forwarding의 1단계로 진행한다.

공식 errata에서 “5.3절로 가야 한다”는 제안 Errata 8495는 **Rejected** 상태다. 따라서 현행
RFC 9171을 해석할 때 원문대로 5.4절로 진행하며, 거절된 제안을 규범 수정으로 적용하면 안 된다.

### 5.3 번들 디스패치(Bundle Dispatching)

이 절은 5.6절 수신 절차의 4단계를 끝낸 뒤 시작한다.

1. 현재 노드가 destination endpoint의 구성원이면 5.7절 Bundle Delivery를 반드시 수행한다
   (`MUST`). 그 뒤 이 노드에서 남은 처리를 하는 동안에는 목적지 membership을 부인한 것으로
   간주해야 하며(`SHALL`), 자기 자신에게 forward해서는 안 된다(`SHALL NOT`).
2. 5.4절 Bundle Forwarding 1단계로 진행한다.

즉 수신 번들은 로컬 전달 대상이어도 복사본을 다른 목적지 구성원이나 다음 홉으로 계속 보낼 수
있지만, 현재 노드 자신을 forwarding target으로 다시 고르지는 않는다.

### 5.4 번들 포워딩(Bundle Forwarding)

#### 기본 절차

1. `Forward pending` constraint를 추가하고 `Dispatch pending`을 제거해야 한다(`MUST`).
2. BPA는 IANA status-report reason에 해당하는 사유로 forwarding이 부적절한지 판단해야 한다
   (`MUST`). 직접 destination으로 보낼지 중간 노드로 보낼지는 선택할 수 있다(`MAY`). 다음
   노드 또는 적절한 CLA를 고를 수 없으면 forwarding은 contraindicated다. Internet을 통해
   forwarding해야 하는 배포에서는 TCP CLA를 구현해야 하지만(`MUST`), 개별 번들마다 TCP가
   최선이라는 뜻은 아니다.
3. contraindicated라면 5.4.1절을 반드시 수행하고(`MUST`) 현재 forwarding 절차의 나머지를
   건너뛴다.
4. 선택한 각 다음 노드에 대해 선택한 CLA 서비스를 호출해야 한다(`MUST`). 전달 직전에:
   - 기존 Previous Node block이 있으면 제거해야 한다(`MUST`).
   - BPA가 이 block을 붙이도록 구성됐다면 현재 node ID를 담은 새 Previous Node block을
     넣어야 한다(`MUST`).
   - Bundle Age block이 있으면 CLA가 실제 conveyance를 시작하기 직전까지 현재 노드에서
     머문 시간을 age에 더해야 한다(`MUST`).
5. 모든 CLA가 송신 절차 종료를 알리면 결과를 평가한다. 실패 시 BPA가 다시 4단계를 시도해도
   된다(`MAY`). 최소 재시도 횟수는 노드 설정이며 운영 환경상 필요한 범위에서 다른 노드에
   노출되어야 한다. 성공했거나 재시도하지 않기로 했다면, 요청되고 보고 기능이 켜진 경우
   `No additional information` 사유의 forwarding report를 생성하는 것이 좋고(`SHOULD`),
   extension이 요구하는 보고도 생성하는 것이 좋다(`SHOULD`). 마지막으로 `Forward pending`을
   제거해야 한다(`MUST`).

#### 5.4.1 포워딩 금기(Forwarding Contraindicated)

BPA는 contraindication을 즉시 forwarding failure로 선언할지 판단해야 한다(`MUST`). 실패로
선언하면 5.4.2절을 반드시 따른다(`MUST`). 선언하지 않으면 사유가 해소될 때 5.4절 4단계에서
재개한다.

#### 5.4.2 포워딩 실패(Forwarding Failed)

BPA는 Previous Node block이 가리키는 직전 노드로 번들을 되돌려 보내도 된다(`MAY`). 이 경우
그 노드만 대상으로 5.4절 4·5단계를 수행해야 한다(`SHALL`). 현재 노드가 destination endpoint
구성원이면 `Forward pending`만 제거해야 하고(`MUST`), 아니면 contraindication 사유를 붙여
5.10절에 따라 bundle을 삭제해야 한다(`MUST`).

### 5.5 번들 만료(Bundle Expiration)

bundle age가 primary block의 lifetime 또는 BPA의 local override를 초과하면 만료한다. creation
time이 0이 아니고 local clock이 정확할 때는 현재 시각과 creation time의 차로 age를 구해도
된다(`MAY`). 아니면 Bundle Age extension block에서 반드시 얻어야 한다(`MUST`). 만료 검사는
처리 중 어느 시점에나 일어날 수 있다(`MAY`).

- 원 lifetime 만료: `Lifetime expired` 사유로 삭제해야 한다(`MUST`).
- local override 만료: `Traffic pared` 사유로 삭제해야 한다(`MUST`).

### 5.6 번들 수신(Bundle Reception)

1. `Dispatch pending` retention constraint를 추가해야 한다(`MUST`).
2. reception 보고가 요청되고 status reporting이 활성화돼 있으면 `No additional information`
   사유의 reception report를 만드는 것이 좋다(`SHOULD`).
3. CRC가 붙은 모든 block의 CRC를 계산하는 것이 좋다(`SHOULD`). 잘못된 CBOR 등 malformed
   block이 있거나 계산값과 첨부 CRC가 다르면 `Block unintelligible` 사유로 bundle을 반드시
   삭제하고(`MUST`) 남은 수신 단계를 건너뛴다.
4. BPA가 처리할 수 없는 각 extension block에 대해 해당 block flags를 순서대로 적용한다.
   - 보고 bit가 있고 reporting이 켜져 있으면 `Block unsupported` reception report 권고
   - bundle-delete bit가 있으면 같은 사유로 bundle을 삭제하고 남은 단계 중단(`MUST`)
   - delete bit는 없고 block-discard bit가 있으면 그 block을 제거(`MUST`)
   - 어느 bit도 없으면 block을 보존하고 다음 미지원 block 또는 5단계로 진행
5. 5.3절 Bundle Dispatching 1단계로 진행한다.

### 5.7 로컬 번들 전달(Local Bundle Delivery)

1. 수신 bundle이 fragment이면 5.9절 ADU Reassembly를 반드시 수행한다(`MUST`). 전체 ADU가
   모이면 reassembled ADU를 가진 fragment가 2단계로 진행한다. 아직 부족하면 `Reassembly
   pending`을 추가하고(`MUST`) 나머지 delivery 단계를 건너뛴다.
2. destination과 일치하는 registration 상태에 따라 처리한다.
   - 구현별 delivery deferral procedure를 추가로 연결해도 된다(`MAY`).
   - Active면 BPA scheduling policy에서 차례가 되는 즉시 자동 delivery해야 한다(`MUST`).
   - Passive이거나 delivery가 실패하면 registration의 failure action을 수행해야 한다(`MUST`).
     action은 가장 오래 기다린 번들부터 poll/Active 시점까지 defer하거나, 그 registration에
     대한 delivery를 abandon하는 두 가지 중 하나여야 한다(`MUST`).
3. delivery 직후 보고가 요청되고 활성화돼 있으면 delivery status report를 만드는 것이 좋다
   (`SHOULD`). 이 보고는 application agent에 제시됐다는 뜻이며, 응용의 처리 완료 확인이 아니다.

Errata 8377은 reassembly 뒤 원 primary block을 어떻게 복원할지에 관한 기술 문제가 있음을
지적하지만 현재 **Held for Document Update**다. 검증된 규범 수정으로 간주해서는 안 되며,
보안 block 검증과 원 primary 보존이 필요한 구현은 후속 문서와 WG 결정을 추적해야 한다.

### 5.8 번들 조각화(Bundle Fragmentation)

길이 `M`인 payload를 fragment로 나누면 같은 source node ID와 creation timestamp를 가진 두
새 bundle의 payload가 각각 원 payload의 처음 `N`바이트와 마지막 `M-N`바이트가 되어야 한다
(`MUST`, `0 < N < M`). fragment를 다시 fragment할 수 있지만 IP fragmentation처럼 논리적
단계는 한 수준이다.

`must not be fragmented` flag가 설정되지 않은 번들은 BPA 재량으로 언제든 fragment화해도
된다(`MAY`). 다음 제약을 지켜야 한다.

- 모든 fragment payload를 올바른 offset 순서로 결합한 결과가 원 payload와 동일해야 한다
  (`MUST`). 서로 다른 시점에 만든 fragment의 byte 범위는 겹칠 수 있다.
- 각 fragment primary block은 fragment flag, fragment offset, total ADU length를 반영해야
  한다(`MUST`). 원 primary에 CRC가 있었다면 각 새 primary의 CRC를 다시 계산해야 한다(`MUST`).
- RFC 9171 원문은 원 bundle이 fragment가 아니거나 offset 0 fragment이면 모든 extension
  block을 offset 0 fragment에 복제하도록 요구한다(`MUST`).
- `replicate in every fragment` flag가 1인 extension block은 모든 fragment에 복제해야 한다
  (`MUST`).
- 나머지 복제 규칙은 각 extension block 규격이 정의해야 한다.

Errata 8376은 모든 extension block을 “적어도 하나의 fragment”에 넣도록 바꾸자는 기술 문제를
제기했으나 **Held for Document Update**다. 첫 fragment가 MTU보다 커질 수 있고 나중에 추가된
extension을 구분하기 어렵다는 실제 쟁점이 있으나, 아직 RFC 9171의 즉시 적용 가능한 verified
수정은 아니다.

### 5.9 ADU 재조립(Application Data Unit Reassembly)

동일 source node ID와 creation timestamp를 가진 fragment들을 모은다. 새 fragment의
“material extent”는 이전 fragment payload 범위와 겹치지 않는 연속 byte 구간이다. offset과
payload length로 배치한 모든 material extent가 빈틈없는 byte array를 이루고 그 길이가 total
ADU length와 같으면:

- offset 0 범위를 포함한 fragment의 payload를 완성된 ADU로 교체해야 한다(`MUST`).
- 같은 식별자를 가진 다른 모든 fragment에서 `Reassembly pending` constraint를 제거해야 한다
  (`MUST`).

필요한 reassembly는 destination endpoint 구성 노드에서 수행하며, 경로상의 다른 노드도
재조립해도 된다(`MAY`).

### 5.10 번들 삭제(Bundle Deletion)

deletion 보고가 요청되고 reporting이 켜져 있으면 삭제 사유를 담은 report를 만드는 것이 좋다
(`SHOULD`). 이후 bundle의 모든 retention constraint를 반드시 제거한다(`MUST`).

### 5.11 번들 폐기(Discarding a Bundle)

retention constraint가 하나도 남지 않는 즉시 bundle을 discard하여 할당된 persistent storage를
해제해도 된다(`MAY`). deletion은 constraint를 제거하는 프로토콜 상태 전이이고, discarding은
실제 참조·저장소를 없애는 구현 동작이라는 차이를 유지한다.

### 5.12 전송 취소(Canceling a Transmission)

해당 transmission으로 만든 bundle이 아직 discard되지 않은 상태에서 취소 요청을 받으면 BPA는
`Transmission canceled` 사유로 5.10절의 bundle deletion을 수행해야 한다(`MUST`).

## 6. 관리 레코드 처리(Administrative Record Processing)

### 6.1 관리 레코드(Administrative Records)

administrative record는 BP 기능을 제공하는 표준 ADU다. RFC 9171 발행 당시 BPv7에서 정의한
record type은 값 `1`인 Bundle status report뿐이다. 각 레코드는 정확히 두 항목의 CBOR array로
표현해야 한다(`SHALL`).

```text
[record-type-code: unsigned integer, type별 CBOR content]
```

**RFC 9713 갱신:** 현재 BPv7 administrative element는 RFC 9171 본문의 고정 목록이 아니라
IANA `Bundle Administrative Record Types` 레지스트리에서 `Bundle Protocol Version` 열에 `7`이
표시된 code point를 사용해야 한다(`SHALL`). malformed ADU 또는 처리할 수 없는 record type은
무시해야 한다(`SHALL`). 레코드를 무시해도 이를 감싼 bundle의 delivery 사실 및 그 bundle에
대한 status-report 처리에는 영향을 주지 않는다.

RFC 9713이 정한 BPv7 범위는 0 reserved, 1 status report, 16~64383 unassigned,
64384~64511 experimental, 64512~65535 private였다. 레지스트리는 이후에도 바뀔 수 있으므로
[현재 IANA Bundle Protocol 레지스트리](https://www.iana.org/assignments/bundle/)를 조회한다.

#### 6.1.1 번들 상태 보고(Bundle Status Reports)

status report는 요청한 bundle의 reception, forwarding, final delivery, deletion 진행 정보를
report-to EID로 보낸다. 대상이 fragment면 6항목, 아니면 4항목 CBOR array다(`SHALL`).

| 순서 | 필드 | 구조·조건 |
| ---: | --- | --- |
| 1 | Bundle status information | 최소 네 status item의 array. 첫 네 항목은 순서대로 received, forwarded, delivered, deleted다. |
| 2 | Reason code | IANA 등록 CBOR unsigned integer |
| 3 | Subject source node ID | 보고 대상 bundle의 source EID. `dtn`과 `ipn` 모두 가능하다. |
| 4 | Subject creation timestamp | 보고 대상 bundle의 creation timestamp |
| 5 | Fragment offset | 대상이 fragment일 때 그리고 그때에만 존재하는 unsigned integer |
| 6 | Subject payload length | 대상이 fragment일 때 그리고 그때에만 존재하는 unsigned integer |

각 status item은 `[status-indicator]` 또는 `[status-indicator, assertion-time]`이다. 두 번째 항목은
indicator가 true이고 원 bundle의 `status time requested` flag가 1일 때만 존재한다. time은 local
clock으로 측정한 DTN time이다. Verified Errata 8525에 따라 source node ID 표현을 `dtn`으로
제한해서 읽으면 안 되며, 4.2.5.1과 그 하위의 모든 허용 EID scheme을 적용한다.

RFC 9171이 정의한 초기 reason은 다음과 같다.

| 값 | 한국어 의미 |
| ---: | --- |
| 0 | 추가 정보 없음 |
| 1 | lifetime 만료 |
| 2 | 단방향 link를 통해 forwarding함 |
| 3 | transmission 취소 |
| 4 | 저장 공간 고갈 |
| 5 | destination EID 사용 불가 |
| 6 | 여기서 destination으로 가는 알려진 route 없음 |
| 7 | route의 다음 node와 제시간에 contact할 수 없음 |
| 8 | block을 해석할 수 없음 |
| 9 | hop limit 초과 |
| 10 | traffic pared, 즉 트래픽 절감을 위해 제거 |
| 11 | 지원하지 않는 block |
| 17~254 | RFC 9171 발행 시 unassigned |
| 255 | reserved |

값 12~16은 RFC 9172가 BPSec 실패 사유로 등록했으며, 최신 IANA 레지스트리에서 확인해야 한다.
대상 bundle의 lifetime·보안 등 forwarding parameters를 status-report bundle에도 반영할 수
있지만(`MAY`) 이는 구현 사항이며 RFC 9171은 명확한 배포 지침을 정하지 않는다.

### 6.2 관리 레코드 생성(Generation of Administrative Records)

1. BPA의 지시를 받은 administrative element는 레코드를 작성해야 한다. 참조 대상 bundle이
   fragment이면 fragment offset과 length를 반드시 포함해야 한다(`MUST`).
2. 이 record를 payload로 갖는 bundle transmission request를 BPA에 제출해야 한다(`MUST`).

## 7. 수렴 계층에 요구되는 서비스(Services Required of the Convergence Layer)

### 7.1 수렴 계층(The Convergence Layer)

종단 간 BP 동작은 실제 노드 간 통신을 수행하는 하위 convergence-layer protocol에 의존한다.
어떤 프로토콜이든 사용할 수 있지만 그 CLA가 BPA에 정해진 최소 서비스를 제공해야 한다.

### 7.2 수렴 계층 서비스 요약(Summary of Convergence-Layer Services)

CLA는 다음 서비스를 제공할 것으로 기대된다.

- CL protocol로 도달 가능한 bundle node에 bundle 송신
- bundle data-sending procedure 종료 후 그 결과를 BPA에 통지
- 다른 node가 CL protocol로 보낸 bundle을 BPA에 전달

추가 규격은 진행 상황 보고, 손실 데이터 재전송, corrupt/inauthentic unit 폐기, 전달 bundle의
무결성·진위 보고 등 서비스를 더 요구할 수 있다. DTN의 긴 RTT에서는 종단 간 반응형 congestion
control이 적합하지 않으므로 convergence-layer protocol은 rate limiting 또는 congestion control을
반드시 제공해야 한다(`MUST`).

## 8. 보안 고려사항(Security Considerations)

BP 자체의 보안 아키텍처는 [RFC 9172 BPSec](https://www.rfc-editor.org/rfc/rfc9172.html)이
정한다. 응용 또는 하위 CL 보안이 아니라 BP 범위의 보안 서비스가 필요하면 같은 범위의 임의
메커니즘이 아니라 BPSec으로 제공해야 한다(`SHALL`). bundle을 생성하거나 cryptographically
verify하거나 accept하는 BPA는 BPSec 지원을 구현해야 한다(`MUST`). 단 개별 bundle에 실제로
BPSec을 적용하는 것은 선택 사항이다.

- **BIB(Block Integrity Block)**: BPSec extension block을 제외한 각 block에 보안
  context가 정한 authentication/integrity 보호를 개별 적용할 수 있다.
- **BCB(Block Confidentiality Block)**: primary block과 BPSec extension block을 제외한 각
  block을 개별 암호화할 수 있다.
- security block도 bundle 안에 있으므로 보호는 transit뿐 아니라 다음 contact를 기다리며
  저장된 at-rest 상태에도 적용된다.
- 인접 node 간 authenticity를 제공하는 CL protocol을 가능하면 사용하는 것이 좋다(`SHOULD`).
  cleartext primary와 다른 block 노출을 줄이기 위해 confidentiality를 제공하는 CL도 가능하면
  사용하는 것이 좋다(`SHOULD`).
- CL peer name을 BP EID에서 유도한다면 그 mapping의 정확성과 진위가 전체 CL 보안 속성에
  결정적이다.
- routing을 위해 primary block은 cleartext여야 한다. traffic analysis 완화가 필요하면 내부
  bundle을 다른 bundle의 payload로 캡슐화하고 그 payload에 BCB를 적용하는 방법을 고려한다.
- status reporting은 공격자가 큰 traffic amplification을 만들 수 있어 기본적으로 꺼진다.
  lifetime override가 완화책이 될 수 있다.
- lifetime이 매우 긴 fragment를 대량 전송하면 끝나지 않는 reassembly가 저장소를 점유한다.
  이 경우에도 local lifetime override가 완화책이 될 수 있다.
- 절대 timestamp를 쓰므로 부정확한 clock을 정확하다고 오인하는 node는 예기치 않게 동작할 수
  있다. creation time 0과 Bundle Age 규칙을 올바르게 적용해야 한다.
- `dtn`·`ipn` EID는 peer identity 자체를 증명하지 않는다. 위조 source·악성 destination,
  트래픽 분석, 비정상 자원 소비를 데이터 검증 및 배포 정책의 신뢰 경계로 다룬다.

## 9. IANA 고려사항(IANA Considerations)

BP의 여러 integer code와 bit position은 IANA registry로 관리된다. 아래 표는 **RFC 9171 발행
시점의 배정**을 설명한다. 레지스트리는 확장 RFC에 따라 바뀌므로 새 값을 하드코딩하기 전에
[IANA Bundle Protocol registry](https://www.iana.org/assignments/bundle/)를 확인한다.
2026-09-11 확인 시 IANA 페이지의 `Last Updated`는 2026-08-06이었다.

### 9.1 Bundle Block Types

RFC 9171은 registry에 BP version 열을 추가하고 BPv7용 block type을 등록했다.

| BP version | 값 | RFC 9171 발행 시 의미 |
| --- | ---: | --- |
| 없음 | 0 | Reserved |
| 6, 7 | 1 | Bundle Payload Block |
| 6 | 2~5 | BPv6 보안·previous-hop block |
| 7 | 6 | Previous Node |
| 7 | 7 | Bundle Age(milliseconds) |
| 6 | 8~9 | BPv6 metadata·security block |
| 7 | 10 | Hop Count |
| 7 | 11~191 | Unassigned |
| 6, 7 | 192~255 | Private 및/또는 Experimental Use |

현재 레지스트리에는 후속 규격이 BPv7 값 11(BIB), 12(BCB), 13~15의 extension block을 추가했다.
따라서 RFC 9171의 “11~191 unassigned” 표를 현재 할당 현황으로 사용하면 안 된다.

### 9.2 Primary Bundle Protocol Version

IANA는 값 `7`을 RFC 9171에 배정했다. RFC 9171 발행 시 `8~255`는 unassigned로 바뀌었다.

### 9.3 Bundle Processing Control Flags

IANA registry에 BP version 열이 추가됐다. BPv7에 적용되는 bit는 4.2.3절 표와 동일하다.

| 비트 | BPv7 상태 |
| ---: | --- |
| 0, 1, 2, 5, 6, 14, 16, 17, 18 | 지정된 기능 |
| 3, 4, 7~13, 15, 19, 20 | Reserved |
| 21~63 | Unassigned |

BPv6에만 배정된 custody transfer, singleton 표시, class-of-service bit를 BPv7 의미로 재사용해서는
안 된다.

### 9.4 Block Processing Control Flags

BPv7에 유효한 기능 bit는 0(모든 fragment에 복제), 1(처리 불가 보고), 2(처리 불가 시 bundle
삭제), 4(처리 불가 시 block 제거)다. bit 3·5·6은 BPv7 관점에서 reserved이고 7~63은
unassigned다. BPv6에서 쓰던 `last block`, `forwarded without processing`, `EID-reference`
의미를 BPv7에 적용해서는 안 된다.

### 9.5 Bundle Status Report Reason Codes

IANA registry에 BP version 열을 추가하고 6.1.1절의 사유를 BPv7에 연결했다. RFC 9171이 직접
정한 값은 0~11이며, 255는 reserved다. 이후 RFC 9172가 12~16을 BPSec 사유로 추가했다.
처리 로직은 숫자의 과거 표가 아니라 현재 IANA 배정 및 해당 참조 규격을 기준으로 해야 한다.

### 9.6 Bundle Protocol URI Scheme Types

이 registry의 registration policy는 Standards Action이다. 배정은 IESG가 승인한 Standards
Track RFC에 한해 이뤄지는 것이 원칙이다. 각 entry는 scheme 이름·설명, URI scheme 정의 문서,
BP EID 사용 및 CBOR 인코딩 정의 문서를 함께 가리켜야 한다.

| 값 | 의미 |
| ---: | --- |
| 0 | Reserved |
| 1 | `dtn` |
| 2 | `ipn` |
| 3~254 | Unassigned |
| 255~65535 | Reserved |
| 65535 초과 | Private Use |

### 9.7 `dtn` URI Scheme

IANA URI Schemes registry의 `dtn` entry는 Permanent 상태이며 DTN Bundle Protocol이 사용한다.
change controller는 IETF이고 규격 참조는 RFC 9171이다.

### 9.8 `ipn` URI Scheme

RFC 9171은 RFC 6260에 처음 기술된 `ipn` URI scheme entry를 Permanent로 갱신하고 BP가
사용하며 IETF가 변경을 통제한다고 기록했다. 이후 RFC 9758이 allocator hierarchy, 텍스트 표현,
CBOR 2항목·3항목 encoding과 관련 registry를 다시 갱신했으므로 현재 구현은 RFC 9758을 함께
적용한다.

## 10. 참고문헌(References)

참고문헌의 저자·제목·연도는 번역해 새 서지 레코드를 만들지 않고 원문 식별자와 공식 링크를
보존한다. 아래 설명은 이 RFC에서 각 문헌이 하는 역할이다.

### 10.1 규범적 참고문헌(Normative References)

| 식별자 | 공식 자료 | 이 규격에서의 역할 |
| --- | --- | --- |
| BPSEC | [RFC 9172](https://www.rfc-editor.org/info/rfc9172) | BPSec, BIB·BCB와 BP 보안 처리 |
| CRC16 | [ITU-T X.25](https://www.itu.int/rec/T-REC-X.25-199610-I/) | X-25 CRC-16 정의 |
| RFC2119 | [RFC 2119](https://www.rfc-editor.org/info/rfc2119) | 요구 수준 키워드의 기본 의미 |
| RFC4960 | [RFC 4960](https://www.rfc-editor.org/info/rfc4960) | CRC32C 계산 정의 참조 |
| RFC5234 | [RFC 5234](https://www.rfc-editor.org/info/rfc5234) | ABNF 문법 |
| RFC8174 | [RFC 8174](https://www.rfc-editor.org/info/rfc8174) | 대·소문자에 따른 BCP 14 해석 명확화 |
| RFC8949 | [RFC 8949](https://www.rfc-editor.org/info/rfc8949) | CBOR와 deterministic encoding |
| SABR | [CCSDS 734.3-B-1](https://public.ccsds.org/Pubs/734x3b1.pdf) | schedule-aware bundle routing 예시 |
| TCPCL | [RFC 9174](https://www.rfc-editor.org/info/rfc9174) | TCP convergence-layer protocol v4 |
| URI | [RFC 3986](https://www.rfc-editor.org/info/rfc3986) | URI 일반 문법 |
| URIREG | [RFC 7595](https://www.rfc-editor.org/info/rfc7595) | URI scheme 등록 절차 |

### 10.2 정보성 참고문헌(Informative References)

| 식별자 | 공식 자료 | 읽는 목적 |
| --- | --- | --- |
| ARCH | [RFC 4838](https://www.rfc-editor.org/info/rfc4838) | DTN 아키텍처와 설계 근거 |
| BIBE | [draft-ietf-dtn-bibect-03](https://datatracker.ietf.org/doc/html/draft-ietf-dtn-bibect-03) | bundle-in-bundle encapsulation 배경 |
| RFC3987 | [RFC 3987](https://www.rfc-editor.org/info/rfc3987) | IRI와 국제화 표현 |
| RFC5050 | [RFC 5050](https://www.rfc-editor.org/info/rfc5050) | 실험 BPv6 원 규격 및 변경 비교 |
| RFC6255 | [RFC 6255](https://www.rfc-editor.org/info/rfc6255) | 기존 Bundle Protocol IANA registries |
| RFC6257 | [RFC 6257](https://www.rfc-editor.org/info/rfc6257) | 이전 Bundle Security Protocol |
| RFC6258 | [RFC 6258](https://www.rfc-editor.org/info/rfc6258) | BPv6 Metadata Extension Block |
| RFC6259 | [RFC 6259](https://www.rfc-editor.org/info/rfc6259) | BPv6 Previous-Hop Insertion Block |
| RFC6260 | [RFC 6260](https://www.rfc-editor.org/info/rfc6260) | CBHE와 원래 `ipn` scheme |
| RFC7143 | [RFC 7143](https://www.rfc-editor.org/info/rfc7143) | CRC32C 예제 위치 |
| RFC8126 | [RFC 8126](https://www.rfc-editor.org/info/rfc8126) | IANA considerations 작성·배정 정책 |
| SIGC | [SIGCOMM 2003 논문](https://dl.acm.org/doi/10.1145/863955.863960) | challenged Internet을 위한 DTN 배경 |

## 부록 A. RFC 5050에서의 주요 변경(Significant Changes from RFC 5050)

RFC 9171은 BPv6 계열 실험 규격에서 다음을 크게 바꿨다.

1. transmission과 forwarding의 차이를 명확히 했다.
2. custody transfer를 bundle-in-bundle encapsulation 규격으로 이동했다.
3. EID와 문법은 같지만 기능적으로 구별되는 node ID 개념을 도입했다.
4. primary block을 재구성하고 불변으로 만들며 선택적 CRC를 추가했다.
5. non-primary block에도 선택적 CRC를 추가했다.
6. BPSec block 참조를 위해 canonical block에 block number를 추가했다.
7. Bundle Age extension block을 추가했다.
8. Previous Node extension block을 추가했다.
9. Hop Count extension block을 추가했다.
10. Quality of Service 표시를 제거했다.
11. SDNV(Self-Delimiting Numeric Value) 대신 CBOR encoding을 채택했다.
12. node-local lifetime override를 추가했다.
13. time 단위를 초가 아니라 밀리초로 명확히 했다.

## 부록 B. CDDL 표현(CDDL Expression)

부록의 CDDL(Concise Data Definition Language)은 BPv7 구조를 기계적으로 읽기 쉽게 표현한
정보성 자료다. **본문과 CDDL이 충돌하면 본문의 규칙이 우선한다.** 전체 CDDL을 복제하지 않고
핵심 shape만 요약하면 다음과 같다.

```text
bpv7-start := bundle 또는 CBOR tag 55799가 붙은 bundle
bundle := primary-block + extension-block 0개 이상 + payload-block
eid := [uri-code, scheme-specific-part]
creation-timestamp := [dtn-time, sequence]
canonical-block := [type, number, flags, crc-type, data, optional-crc]
admin-record := [record-type, record-content]
status-record := [4개 상태, reason, source EID, creation time,
                  선택적 fragment offset과 payload length]
```

CDDL은 다음 불변조건도 드러낸다.

- version은 7이고 DTN time은 unsigned integer다.
- CRC type은 0·1·2, CRC 값은 각각 2바이트 또는 4바이트다.
- extension block number는 1보다 크고 payload block은 type 1, number 1이다.
- type-specific data는 plain byte string이거나 CBOR tag 24가 붙은 byte string일 수 있다.
- 정의된 extension shape는 Previous Node(type 6), Bundle Age(type 7), Hop Count(type 10)다.

Verified Errata 7337은 RFC 출력 과정에서 Appendix B의 주석 정렬과 줄바꿈 때문에 CDDL parser가
문법 오류를 낼 수 있음을 바로잡는다. 특히 주석 marker 정렬과 길게 갈라진 `payload-block`
production을 한 문법 표현으로 읽어야 한다. 복사해 검증할 때는 RFC Editor의 inline-errata
버전 또는 수정된 원문을 사용한다.

## 감사의 글(Acknowledgments)

이 작업은 DTNRG가 만든 RFC 5050을 자유롭게 각색한 것이다. 원문은 Vinton Cerf, Scott
Burleigh, Adrian Hooke, Leigh Torgerson, Michael Demmer, Robert Durst, Keith Scott,
Susan Symington, Kevin Fall, Stephen Farrell, Howard Weiss, Peter Lovell, Manikantan Ramadas 등
RFC 5050에 기술 자료와 의견을 제공한 참여자에게 감사를 표한다. Scott Burleigh는 Jet
Propulsion Laboratory와 California Institute of Technology의 지속적인 지원에도 감사를 전한다.
부록 B CDDL은 Carsten Bormann과 Brian Sipos가 제공했다.

## 저자 주소(Authors' Addresses)

RFC 9171의 저자는 Scott Burleigh(IPNGROUP), Kevin Fall(Roland Computing Services),
Edward J. Birrane III(Johns Hopkins University Applied Physics Laboratory)다. 최신 연락처는
[RFC 9171 원문 끝부분](https://www.rfc-editor.org/rfc/rfc9171.html#authors-addresses)을 확인한다.

## 2026-09-11 공식 Errata 검토

공식 [RFC Errata 검색 결과](https://errata.rfc-editor.org/search/?rfc_number=9171)를 직접
확인한 상태다. 상태 수는 **Verified 3, Reported 1, Held for Document Update 4, Rejected 1**로
총 9건이다. Verified만 승인된 정정으로 반영하며, Reported·Held는 쟁점을 알리는 자료이지
확정된 규범 변경이 아니다. Rejected 항목은 원문을 바꾸지 않는다.

| Errata ID | 상태·유형 | 영향 절 | 이 자료의 처리 |
| ---: | --- | --- | --- |
| [8043](https://errata.rfc-editor.org/eid8043/) | Verified / Technical | 4.3.1 | primary CRC 계산 때 CRC value bytes만 0으로 하고 CBOR field header는 유지하도록 반영 |
| [8525](https://errata.rfc-editor.org/eid8525/) | Verified / Technical | 6.1.1 | status report의 source node ID는 `dtn` 또는 `ipn` 등 허용 EID scheme을 쓸 수 있음을 반영 |
| [7337](https://errata.rfc-editor.org/eid7337/) | Verified / Editorial | Appendix B | 줄바꿈·주석 정렬로 생긴 CDDL 구문 오류를 설명 |
| [8645](https://errata.rfc-editor.org/eid8645/) | Reported / Technical | 4.2.8 | block-type-specific data가 definite-length CBOR byte string이라는 4.3.2절과의 명확성 쟁점 표시. 미확정이므로 원문 규범을 임의 교체하지 않음 |
| [7272](https://errata.rfc-editor.org/eid7272/) | Held / Technical | 4.2.5.1.1 | `dtn` demux가 query·fragment까지 삼키지 않게 할 ABNF 개선 쟁점. 확정 변경으로 적용하지 않음 |
| [7881](https://errata.rfc-editor.org/eid7881/) | Held / Technical | 6.1.1 | CBOR true/false를 major type 7의 simple value 21/20으로 더 명시하자는 개선 쟁점 |
| [8376](https://errata.rfc-editor.org/eid8376/) | Held / Technical | 5.8 | fragment의 extension-block 배치·크기 문제를 경고하되 원문의 복제 의무를 그대로 설명 |
| [8377](https://errata.rfc-editor.org/eid8377/) | Held / Technical | 5.7 | reassembly 후 원 primary block 복원과 security 검증 쟁점을 경고 |
| [8495](https://errata.rfc-editor.org/eid8495/) | Rejected / Technical | 5.2 | 5.2 단계 2의 목적지를 5.3으로 바꾸지 않고 원문 5.4를 유지 |

## 번역·수치·용어 검수 기록

- 원문 목차의 초록, 상태, 저작권, 1~10절과 모든 번호 하위 절, 부록 A·B, 감사와 저자 순서를
  대조했다.
- CBOR array 항목 수(primary 8/9/10/11, canonical 5/6, status report 4/6), block number
  (primary 0, payload 1), block type(1/6/7/10), CRC type(0/1/2), hop limit(1~255), time 단위
  (milliseconds)와 epoch(2000-01-01 UTC)를 재확인했다.
- bundle 및 block flag의 bit position과 status-report reason code 0~11을 원문 표와 대조했다.
- `transmission`, `forwarding`, `delivery`, `deletion`, `discarding`을 서로 바꾸어 쓰지 않았고,
  `MUST/SHALL`, `SHOULD`, `MAY`의 규범 강도를 분리했다.
- RFC 9713과 RFC 9758의 갱신 관계, 2026-09-11 현재 공식 errata 상태 9건을 별도로 확인했다.
- IANA 값은 RFC 9171 발행 당시 표와 변동 가능한 현재 registry를 구분했다.
