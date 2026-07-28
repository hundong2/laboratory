# AGENTS.md - Content Learning Harness

이 파일은 이 레포에서 작업하는 모든 에이전트가 따라야 하는 표준 작업 하네스입니다. 상위 시스템/개발자 지시가 우선하지만, 이 레포 안의 분석 및 학습 자료 생성 작업은 아래 계약을 기본값으로 삼습니다.

## Mission

사용자가 전달한 링크, 텍스트, 문서, 기술 주제, 코드 자료를 하나의 학습 폴더로 만들고, 한국어 사용자에게 바로 학습 가능한 분석 문서와 실습 자료를 제공합니다.

결과물은 요약에서 끝나지 않아야 합니다. 기초 개념, 핵심 원리, 상세 정리, 용어, 실습 코드, 다음 학습 경로를 포함해 초보자가 출발하고 숙련자가 깊게 들어갈 수 있어야 합니다.

## Harness Contract

모든 작업은 다음 입출력 계약을 지킵니다.

### Input

- 사용자가 제공한 URL, 문서 내용, 코드, 기술명, 질문을 작업 입력으로 본다.
- URL이나 최신 정보가 포함된 요청은 원문 출처와 확인 기준일을 기록한다.
- 입력이 불명확해도 합리적으로 주제를 추론할 수 있으면 진행하고, 추론한 내용을 새 폴더 `README.md`에 명시한다.

### Output

하나의 사용자 요청은 하나의 주제 폴더를 생성하거나 갱신한다.

```text
topic-folder/
  README.md
  translation.ko.md        # 논문이 아닌 외국어 원문일 때 필수
  <논문 제목>.번역.md       # 논문 입력일 때 translation.ko.md 대신 사용하는 문장 대조 번역
  01_foundations.ipynb     # 기본 학습 실습
  02_practice.ipynb        # 응용 실습
  03_advanced.ipynb        # 심화 실습
  guide/                   # 다중 URL 묶음 또는 실습 중심 요청의 단계별 가이드와 코드
    README.md
    01_foundations.ipynb
    02_practice.ipynb
    03_advanced.ipynb
```

위 트리는 입력 유형에 따라 달라진다. 사용자가 한 요청에 여러 URL을 주고 그 안에 GitHub 저장소와 일반 웹사이트·논문·블로그·문서 URL이 섞여 있으면 `Mixed URL Bundle Workflow`가 `GitHub Repository Workflow`보다 우선한다. 논문 URL, 논문 PDF 또는 논문 원문이 입력이면 아래 `Paper Translation Workflow`가 일반 `Website URL Workflow`와 `Translation Gate`보다 우선한다. 이 경우 `<논문 제목>.번역.md`가 필수 번역 산출물이며 같은 내용을 `translation.ko.md`로 중복 생성하지 않는다.

문서 주제가 C++ 또는 C# 중심이면 실습 파일은 `*.cpp` 또는 `*.csx`를 사용한다. Python이 자연스러운 주제는 `*.ipynb`를 기본으로 한다.

## Mixed URL Bundle Workflow

사용자가 한 번의 요청에 GitHub 저장소 주소와 일반 웹사이트, 논문, 블로그, 공식 문서 URL을 함께 제공하면 이 절을 우선 적용한다. 이 경우 GitHub 저장소는 분석 대상 출처이지 편집 대상 저장소가 아니다.

- 하나의 공통 주제 폴더를 만들고 모든 출처를 `README.md`의 `출처와 작업 범위`에 URL별로 기록한다.
- GitHub 저장소는 submodule, clone, subtree로 추가하지 않는다. 원격 페이지, README, 문서, 공개 코드 파일을 직접 확인해 일반 사이트처럼 분석한다.
- GitHub 저장소를 확인할 때는 저장소명, 기본 브랜치, 확인 가능한 최신 commit 또는 release, license, 주요 언어, 핵심 디렉터리와 실행 진입점을 기록한다.
- 저장소 코드에 대해서는 `README.md` 또는 `guide/README.md`에 한국어 코드 리뷰를 추가한다. 리뷰는 아키텍처, 주요 모듈, 실행 흐름, 의존성, 확장 지점, 테스트·디버깅 포인트, 주의할 위험을 포함한다.
- 저장소 README나 문서가 외국어이면 `translation.ko.md`에 사이트 번역 작업으로 포함한다. 여러 출처가 있으면 URL별 section을 나누고 원문 구조와 링크를 보존한다.
- 함께 제공된 논문 URL이 실제 논문이면 같은 주제 폴더 안에 `Paper Translation Workflow`를 적용해 `<논문 제목>.번역.md`를 만든다. 논문 번역 내용을 `translation.ko.md`에 중복하지 않는다.
- 실습 자료는 주제 폴더의 `guide/` 안에 둔다. `guide/README.md`를 시작점으로 만들고 단계별 학습 코드는 `guide/01_foundations.*`, `guide/02_practice.*`, `guide/03_advanced.*`처럼 번호를 붙인다.
- 실습 코드는 원격 저장소를 로컬 submodule로 가져왔다는 전제 없이 동작해야 한다. 필요한 경우 작은 toy implementation, API 사용 예제, 설정 템플릿, 의사 코드, 공개 raw 파일 다운로드 예제를 사용한다.
- `README.md`에는 목차를 두고, 번역 파일, 논문 번역 파일, `guide/README.md`, 핵심 실습 파일로 이동하는 링크를 포함한다.
- 루트 `README.md`의 `TODO`에는 submodule 경로가 아니라 생성한 주제 폴더의 `README.md` 링크를 추가한다.

## Website URL Workflow

사용자가 GitHub 저장소가 아닌 일반 웹사이트 주소를 입력으로 제공하면 사이트 내용 확인과 한국어 번역을 필수 작업으로 처리한다.

한 요청에 GitHub 저장소와 일반 웹사이트·논문 URL이 함께 있으면 이 절만 단독 적용하지 말고 `Mixed URL Bundle Workflow`를 우선 적용한다.

논문 사이트, DOI와 논문 PDF는 이 절의 일반 규칙 대신 아래 `Paper Translation Workflow`를 우선 적용한다.

- 원문 페이지를 직접 확인하고 최종 URL, 페이지 제목, 원문 언어와 접근 일자를 기록한다.
- 로그인, JavaScript 렌더링 또는 지역 제한으로 일부 내용만 확인할 수 있으면 확인 가능한 범위와 누락 가능성을 명시한다.
- 사이트의 주제를 대표하는 `topic-folder/`를 만들고, 분석·학습 문서인 `README.md`와 사이트 번역 자료인 `translation.ko.md`를 항상 함께 생성한다.
- 원문이 외국어이면 `translation.ko.md`에 제목과 핵심 섹션 흐름을 유지한 자연스러운 한국어 번역을 제공한다.
- 원문이 이미 한국어여도 `translation.ko.md` 생성을 생략하지 않는다. 이때 파일 상단에 원문이 한국어임을 밝히고, 원문의 구조를 따른 교정·재구성본 또는 학습용 한국어 정리본을 제공한다.
- 여러 페이지로 구성된 사이트는 사용자가 제공한 페이지를 우선 번역하고, 이해에 필수적인 연결 페이지가 있으면 출처 URL을 구분해 필요한 범위만 추가한다.
- 표, 목록, 수치, 경고와 코드 예제는 의미가 달라지지 않도록 보존한다. 변동 가능한 가격, 버전, 일정과 제공 상태에는 확인 기준일을 붙인다.
- 저작권이 있는 사이트의 전문을 그대로 복제하지 않는다. 원문의 구조와 의미를 보존한 번역 요약을 작성하고, 직접 인용은 꼭 필요한 짧은 범위로 제한한다.
- 접근할 수 없거나 번역할 실질적 본문이 없는 사이트는 임의로 내용을 만들지 않는다. 접근 실패 사유, 확인한 메타데이터와 추가 확인이 필요한 사항을 `translation.ko.md`에 기록한다.
- 번역 자료에서 원문 사이트로 이동할 수 있게 링크하고, 주제 `README.md`에서 `translation.ko.md`를 명확히 연결한다.
- 번역 후에는 원문의 주요 섹션이 빠지지 않았는지, 고유명사·수치·코드·링크가 왜곡되지 않았는지 대조한다.

## Paper Translation Workflow

사용자가 학술 논문 URL, DOI, 논문 PDF, 학회·저널 페이지, preprint 페이지 또는 논문 본문을 입력하면 일반 웹 문서가 아니라 논문 전용 학습·번역 작업으로 처리한다.

### 1. Paper Detection and Source Verification

- arXiv, OpenReview, ACL Anthology, IEEE Xplore, ACM Digital Library, SpringerLink, ScienceDirect, Nature, PubMed, 학회 proceedings, 대학 repository와 DOI landing page는 논문 사이트 후보로 본다.
- domain 이름만으로 판정하지 않는다. 제목, 저자, 초록, 출판처, DOI·arXiv ID, PDF 또는 full-text 링크가 있는지도 함께 확인한다.
- landing page, HTML full text, 공식 PDF가 함께 있으면 논문 제목·저자·버전이 일치하는지 확인하고 읽기 가장 완전한 원문을 사용한다.
- preprint와 최종 출판본이 모두 있으면 사용자가 지정한 버전을 우선한다. 지정이 없으면 접근 가능한 최종 출판본을 우선하되, 사용한 버전과 차이 가능성을 기록한다.
- 번역 파일 상단에 원문 제목, 저자, 학회·저널, 연도, DOI 또는 식별자, 원문 URL, 사용한 버전, 원문 언어, 접근일과 확인 가능한 license를 기록한다.
- abstract만 확인했으면 논문 전체를 읽은 것처럼 작성하지 않는다. 확인 가능한 섹션과 누락된 섹션을 명확히 구분한다.
- PDF가 scan image이거나 수식·다단 편집 때문에 추출이 깨지면 OCR 또는 시각 확인을 사용하고, 확신할 수 없는 문장은 `[판독 불확실]`로 표시한다. 임의로 복원하지 않는다.
- PDF의 반복 header·footer·page number는 본문에서 제거하고, column 순서와 page 경계에서 이어지는 문장을 시각적으로 대조한다. 줄 끝 하이픈은 실제 복합어인지 편집상 단어 분리인지 확인한 뒤 합친다.

### 2. Translation File Naming

- 번역 파일명은 반드시 `<논문 제목>.번역.md` 형식으로 만든다.
- `<논문 제목>`에는 원문에 표시된 공식 논문 제목을 사용한다. 예: `Attention Is All You Need.번역.md`
- Windows와 Linux에서 모두 쓸 수 있도록 파일명에서 `\ / : * ? " < > |`를 제거하거나 의미를 보존하는 하이픈으로 바꾸고, 연속 공백은 하나로 줄이며 끝의 공백과 마침표는 제거한다.
- 제목이 파일시스템 한계에 가까울 정도로 길면 의미를 보존한 공식 short title 또는 앞부분을 사용하고, 전체 원문 제목은 파일 상단 metadata에 빠짐없이 기록한다.
- 같은 제목의 다른 버전이 이미 있으면 덮어쓰지 말고 `-2`, `-3` 또는 식별 가능한 연도·venue를 붙인다.
- 논문 입력에서는 이 파일이 `translation.ko.md`를 대체한다. `README.md`에서 실제 번역 파일명을 명확히 링크한다.

### 3. Sentence-Aligned Korean Translation

논문 번역은 요약만 제공하지 않는다. 저작권과 이용 조건이 허용하고 실제 원문을 확인할 수 있는 범위에서, 원문 문장 하나를 제시한 직후 대응하는 한국어 문장을 제공한다.

필수 형식:

```md
### Abstract

**S001 — Original**

We propose a lightweight model for real-time robot perception.

**S001 — 한국어**

(우리는 실시간 로봇 인지를 위한 경량 모델을 제안한다.)

- **용어·약어 해설**
  - **lightweight model(경량 모델)**: 계산량과 메모리 사용량을 줄여 제한된 장치에서도 실행하기 쉽게 만든 모델이다.
  - **real-time(실시간)**: 단순히 빠르다는 뜻이 아니라 정해진 deadline 안에 결과를 내야 한다는 시스템 요구사항이다.
```

- 원문 문장과 번역 문장에 같은 순번 `S001`, `S002`를 붙여 즉시 대조할 수 있게 한다.
- sentence ID는 파일 전체에서 중복 없이 단조 증가시키고 section이 바뀌어도 `S001`로 다시 시작하지 않는다.
- 원문 한 문장을 여러 문단 뒤의 번역과 연결하지 않는다. 반드시 원문 바로 다음에 대응 번역을 둔다.
- 원칙적으로 한 원문 문장과 한 번역 문장을 하나의 block으로 유지한다. 한국어 어순상 두 문장으로 나눠야 정확해지는 경우에도 같은 sentence ID 아래에 둔다.
- `e.g.`, `i.e.`, `et al.`, `Fig.`, `Eq.`, 소수점, 인용 표기와 수식 내부의 마침표를 문장 경계로 잘못 나누지 않는다.
- 제목, 초록, 서론, 관련 연구, 방법, 실험, 결과, 한계, 결론 등 원문의 section 순서를 유지한다.
- 부정 표현, 조건, 가능성 표현(`may`, `might`, `can`), 비교 기준과 인과 관계를 강하게 바꾸지 않는다. 저자가 가능성만 말한 내용을 확정 사실로 번역하지 않는다.
- 인용 번호, 식 번호, 변수명, 단위, 수치, dataset·model 이름은 원문과 대조해 보존한다.
- 직역이 오히려 의미를 흐리면 자연스럽게 번역하되, 중요한 의역에는 `번역자 주:`를 짧게 붙여 원래 의미를 설명한다.
- 해석이 둘 이상 가능한 문장은 임의로 하나를 확정하지 말고 가장 타당한 번역과 대안 해석 또는 확인 필요 사항을 함께 적는다.
- 원문이 이미 한국어이면 같은 문장을 복제하지 말고 `한국어` label을 `쉬운 한국어`로 바꿔 초보자가 이해하기 쉬운 풀이를 제공한다. 원문의 기술적 강도와 의미는 그대로 유지한다.

### 4. Acronyms and Technical Terms

- 약어가 처음 등장하면 `약어 (영문 전체 이름, 한국어 번역)` 순서로 풀어쓴다.
- 예: `SLAM (Simultaneous Localization and Mapping, 동시적 위치추정 및 지도작성): 로봇이 자신의 위치를 추정하면서 동시에 주변 지도를 만드는 기술`
- 기술 용어가 처음 등장하면 한국어 번역 뒤에 원어를 함께 둔다. 예: `자기지도학습(self-supervised learning)`
- 단순 사전 뜻만 적지 말고 해당 논문에서 그 용어가 어떤 역할을 하는지 1~3문장으로 설명한다.
- 같은 용어는 문서 전체에서 같은 번역어를 사용한다. 분야 관용 번역이 여러 개면 대표 번역 하나를 정하고 처음에 대체 번역을 병기한다.
- 논문 저자가 새로 정의한 용어는 일반 용어와 구분해 `이 논문에서의 정의`를 적는다.
- 약어·기술 용어가 없는 문장에는 빈 해설 section을 반복하지 않는다. 새롭거나 이해에 중요한 항목이 있을 때만 문장 바로 아래에 추가한다.
- 번역 파일 끝에는 전체 문서에서 사용한 용어를 모은 `## 약어 및 기술 용어 사전`을 만들고, 원어·한국어·의미·최초 등장 sentence ID를 표로 정리한다.

### 5. Equations, Figures, Tables, and References

- 수식은 원문 표기를 보존하고, 바로 아래에서 각 기호, tensor shape, 입력·출력과 수식의 직관을 한국어로 설명한다.
- figure와 table caption도 sentence ID를 부여해 원문과 한국어를 대조한다. 본문을 이해하는 데 중요한 그림과 표는 “무엇을 비교하고 어떻게 읽는지”를 추가 설명한다.
- 표의 수치와 단위는 번역 과정에서 재계산하거나 반올림하지 않는다. 본문 주장과 표 수치가 맞는지도 확인한다.
- algorithm, pseudocode와 source code는 식별자와 동작을 보존한다. 필요한 한국어 설명은 code block 밖에 둔다.
- 참고문헌의 저자, 제목, venue, 연도와 링크는 bibliographic record이므로 임의 번역하거나 변경하지 않는다. 본문 이해에 핵심적인 참고문헌만 별도 학습 메모로 설명할 수 있다.

### 6. Copyright and Access Boundary

- open license, public domain, 저작자가 번역·재사용을 명시적으로 허용한 원문, 사용자가 직접 제공한 문서 등 번역 가능한 범위를 먼저 확인한다.
- 저작권과 사이트 이용 조건이 전문의 문장별 재현을 허용하지 않으면 원문 전체를 복제하지 않는다. 이 경우 확인 가능한 짧은 구간만 문장 대조 형식으로 제공하고, 나머지는 section별 한국어 해설·요약으로 전환하며 제한 사유를 파일 상단에 기록한다.
- paywall, login, robot 차단 또는 손상된 PDF 때문에 본문을 확인할 수 없으면 초록이나 metadata만으로 전체 번역을 만들지 않는다. 확인한 범위, 접근 실패 원인과 사용자가 원문 파일을 제공하면 이어서 처리할 수 있다는 점을 기록한다.
- 번역만 읽어도 원문의 저자 주장과 에이전트의 설명을 구분할 수 있게 `원문`, `한국어`, `용어·약어 해설`, `번역자 주` label을 일관되게 사용한다.

### 7. Required Paper Deliverables

논문 작업의 최소 결과물:

```text
paper-topic/
  README.md
  <논문 제목>.번역.md
  01_foundations.ipynb
  02_practice.ipynb
  03_advanced.ipynb
```

- `README.md`에는 논문의 연구 질문, 핵심 기여, 선행 연구와의 차이, 방법, dataset과 평가 지표, 결과, 한계, 재현 시 주의점과 다음 학습 경로를 설명한다.
- 번역 파일 첫 부분에는 section별 상태를 `완료`, `부분 번역`, `원문 미확인`, `해당 없음`으로 표시한 범위 표를 둔다. 긴 논문을 여러 차례에 걸쳐 작업해도 완료 여부를 과장하지 않는다.
- 번역 파일의 권장 순서는 `논문 metadata → 번역·접근 범위 → 읽기 전 핵심 배경 → section별 문장 대조 번역 → 수식·그림 해설 → 약어 및 기술 용어 사전 → 번역 검수 기록`이다.
- notebook은 논문과 관계없는 일반 예제가 아니라 핵심 수식, algorithm, evaluation 또는 ablation을 작은 규모로 재현하는 방향으로 구성한다.
- 코드나 데이터가 공개되지 않아 정확한 재현이 불가능하면 toy reproduction임을 명시하고 원 논문 결과를 재현했다고 주장하지 않는다.
- `README.md`와 번역 파일은 서로 링크하며, 번역 파일에서 원문 URL로 이동할 수 있어야 한다.

## GitHub Repository Workflow

사용자가 단일 GitHub 저장소 주소를 주요 입력으로 제공하면 일반 웹 문서 처리 대신 다음 절차를 우선 적용한다.

예외: 한 요청에 GitHub 저장소와 일반 웹사이트·논문·블로그·문서 URL이 함께 제공되었거나, 사용자가 clone/submodule 없이 분석하라고 명시하면 이 절을 적용하지 않는다. 이 경우 `Mixed URL Bundle Workflow`에 따라 GitHub 저장소를 일반 사이트처럼 분석하고, 결과물은 상위 작업 주제 폴더 안에 만든다.

### 1. Submodule Registration

- GitHub 저장소를 프로젝트 최상단의 Git submodule로 추가한다.
- 기본 경로는 GitHub 저장소 이름을 사용한다. 같은 경로가 이미 있으면 기존 파일을 덮어쓰지 말고 현재 submodule 등록 여부와 충돌 원인을 먼저 확인한다.
- submodule을 추가한 뒤 초기화와 업데이트를 수행한다. 중첩 submodule도 가져올 수 있도록 재귀 옵션을 사용한다.

```bash
git submodule add <github-url> <repository-name>
git submodule update --init --recursive <repository-name>
```

- 이미 등록된 submodule이면 다시 추가하지 않고 해당 경로를 대상으로 `git submodule update --init --recursive`를 수행한다.
- 추가 및 업데이트가 끝나면 `.gitmodules`, submodule URL, 체크아웃된 커밋과 상태를 확인한다.
- 이후 번역, 가이드, 예제와 실습 자료 작업은 해당 submodule 저장소 내부에서 수행한다.
- submodule 내부에 `AGENTS.md`나 그에 준하는 작업 지침이 있으면 먼저 읽고 함께 준수한다.

### 2. Korean README Translation

- submodule 루트의 원본 `README.md`를 한국어로 번역한 Markdown 파일을 만든다.
- 기본 파일명은 `README_kor.md`로 한다.
- 저장소에 `README.ko.md`, `README-ko.md`, `docs/readme/README.<locale>.md`처럼 다른 언어 번역의 파일명·경로 규칙이 이미 있으면 그 규칙에 맞춰 한국어 locale 파일을 만든다. 이 경우 `README_kor.md`를 중복 생성하지 않는다.
- 기존 한국어 번역본이 있으면 원본 README와 비교해 누락되거나 오래된 부분을 갱신한다.
- 원문의 제목 구조, 링크, 표, 이미지와 코드 의미를 최대한 보존하되 설명 문장은 자연스러운 한국어로 작성한다.
- 원본 `README.md`의 언어 선택 영역이나 소개부 등 사용자가 쉽게 찾을 수 있는 위치에 생성한 한국어 번역 파일 링크를 추가한다.
- 원본 저장소가 이미 한국어 번역 링크를 제공하면 링크가 올바른지 확인하고 불필요하게 중복 추가하지 않는다.

### 3. Guide Directory

- submodule 안에 `guide/` 폴더를 생성하고, 시작 문서로 `guide/README.md`를 작성한다.
- 가이드는 한국어로 작성하며 초보자가 설치부터 시작해 숙련자가 내부 구조와 고급 활용까지 학습할 수 있도록 단계적으로 구성한다.
- 최소한 다음 내용을 포함한다.
  - 프로젝트의 목적과 해결하는 문제
  - 필수 개념과 주요 용어
  - 설치, 환경 설정과 최소 실행 방법
  - 핵심 기능과 일반적인 사용 흐름
  - 저장소 구조와 주요 모듈 설명
  - 기본 예제에서 응용 예제로 이어지는 실습
  - 테스트, 디버깅과 자주 발생하는 문제 해결
  - 성능, 보안, 배포 또는 확장 등 프로젝트에 해당하는 고급 주제
  - 기여 방법과 다음 학습 경로
- 내용이 길면 `01_getting_started.md`, `02_core_concepts.md`, `03_advanced.md`처럼 번호가 붙은 여러 문서로 나누고 `guide/README.md`에서 학습 순서대로 연결한다.
- 원본 `README.md`와 한국어 번역 README 양쪽에서 `guide/README.md`를 찾을 수 있도록 적절한 링크를 추가한다.

### 4. Examples and Practice Files

- 실행 가능한 예제나 실습을 만들 수 있으면 `guide/examples/` 또는 저장소가 이미 사용하는 예제 디렉터리에 추가한다.
- 예제의 주 언어와 도구는 해당 저장소의 기반 언어, 패키지 매니저, 빌드 시스템과 기존 코딩 규칙을 따른다. 예를 들어 TypeScript 저장소에 임의로 Python 노트북을 기본 실습으로 추가하지 않는다.
- 저장소가 여러 언어를 사용하면 핵심 구현과 공식 예제가 가장 많이 사용하는 언어를 우선한다.
- 각 예제에는 학습 목표, 실행 전 요구 사항, 실행 명령, 예상 결과와 코드 작성 이유를 설명한다.
- 기초 문법 확인에서 끝내지 않고 최소 실행, 핵심 기능 활용, 오류 처리 또는 고급 패턴으로 난이도가 이어지게 구성한다.
- 새 예제가 실제 제품 코드나 빌드에 영향을 주지 않도록 격리하고, 가능한 범위에서 저장소의 공식 테스트·lint·format 명령으로 검증한다.

### 5. Commit and Push to Main

- GitHub 저장소 내부 작업은 기본 브랜치인 `main`에서 수행한다. 별도 작업 브랜치나 pull request를 만들지 않는다.
- 작업을 시작하기 전에 `main`을 checkout하고 원격을 fetch한 뒤 로컬 `main`이 `origin/main`에서 안전하게 fast-forward 가능한 상태인지 확인한다.
- 원격 `main`에 새 변경이 있으면 이를 먼저 fast-forward로 반영한다. 로컬과 원격이 diverge한 경우 force push하거나 임의로 이력을 덮어쓰지 말고 충돌 원인을 확인한다.
- 작업 파일만 명시적으로 stage하고, 사용자나 다른 작업의 관련 없는 변경을 함께 커밋하지 않는다.
- 커밋 전 관련 테스트와 `git diff --check`를 실행하고 staged diff의 파일 목록과 변경 범위를 확인한다.
- 검증을 통과하면 변경 사항을 반드시 간결하고 의미 있는 메시지로 commit한다.
- commit 후 `git push origin main`으로 원격 `main`에 직접 push한다.
- push가 끝나면 로컬 `HEAD`와 원격 `main`의 commit SHA가 같은지 확인하고 작업 트리가 깨끗한지 검사한다.
- pull request는 생성하지 않는다. 사용자가 특정 작업에서 명시적으로 PR을 요청한 경우에만 그 요청을 우선한다.
- 인증 실패, push 권한 부족, branch protection 또는 원격 오류가 발생하면 force push로 우회하지 말고 정확한 오류와 사용자가 해야 할 조치를 보고한다.
- submodule과 상위 저장소를 모두 변경했다면 submodule 변경을 먼저 해당 저장소의 `main`에 commit·push하고, 그 commit을 가리키는 상위 저장소의 gitlink와 `.gitmodules` 변경도 상위 `main`에 commit·push한다.

### 6. Submodule Completion Check

- [ ] GitHub 저장소가 submodule로 등록되었는가?
- [ ] `init`과 재귀 `update`를 완료했는가?
- [ ] 작업 기준 submodule 커밋을 기록했는가?
- [ ] 저장소의 번역 파일명 규칙을 확인했는가?
- [ ] 한국어 README 번역본이 생성 또는 갱신되었는가?
- [ ] 원본 README에 한국어 번역 링크가 있는가?
- [ ] `guide/README.md`와 단계별 학습 자료가 있는가?
- [ ] 가능한 경우 저장소 기반 언어로 실행 가능한 예제·실습을 만들었는가?
- [ ] 원본 README와 한국어 번역 README에서 가이드로 이동할 수 있는가?
- [ ] submodule 내부 지침과 검증 명령을 준수했는가?
- [ ] 최상단 `README.md`의 `TODO`에 submodule 학습 가이드 링크를 추가했는가?
- [ ] 변경 사항을 해당 저장소의 `main`에 커밋했는가?
- [ ] `origin/main`에 직접 push하고 로컬·원격 commit SHA가 일치하는지 확인했는가?
- [ ] 불필요한 작업 브랜치나 pull request를 생성하지 않았는가?

submodule 내부 변경은 상위 저장소의 gitlink만으로 저장되지 않는다. 작업 결과를 커밋하도록 요청받은 경우 submodule 저장소에서 번역·가이드 변경을 먼저 커밋한 뒤, 상위 저장소에서 갱신된 submodule 포인터와 `.gitmodules`를 커밋한다.

## Execution Loop

### 1. Intake

- 입력의 주제, 원문 언어, 난이도, 주요 기술 키워드를 파악한다.
- 링크를 받은 경우 원문 URL, 제목, 접근 또는 확인 일자를 기록한다.
- 한 요청에 여러 URL이 있고 GitHub 저장소와 일반 웹사이트·논문 URL이 섞였는지 먼저 확인한다. 섞여 있으면 `Mixed URL Bundle Workflow`를 작업 계획에 명시한다.
- 논문 URL, DOI, PDF 또는 논문 본문인지 먼저 판별한다. 논문이면 `Paper Translation Workflow`를 작업 계획에 명시한다.
- 논문이면 원문 전체, abstract만, supplementary 포함 여부 중 실제 확인 가능한 범위를 기록하고 번역 범위를 과장하지 않는다.
- 원문이 한국어가 아니면 번역 산출물 생성을 필수 작업으로 표시한다.

### 2. Folder Naming

- 주제를 대표하는 짧고 명확한 폴더명을 만든다.
- 영문 기술명은 소문자 kebab-case를 사용한다. 예: `react-server-components`
- 한글 주제는 의미를 살린 영문 slug를 우선 사용한다. 예: `agent-harness-engineering`
- 기존 폴더와 충돌하면 `topic-name-2`, `topic-name-3`처럼 숫자를 붙인다.

### 3. Topic README

새 폴더의 `README.md`는 반드시 한국어로 작성하고, 파일 상단에 작성 일자와 목차를 표시한다.

기본 구조:

```md
# <주제명>

작성일: YYYY-MM-DD

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [핵심 요약](#핵심-요약)
- [상세 정리](#상세-정리)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

## 한눈에 보기

## 기초 개념

## 핵심 요약

## 상세 정리

## 용어 정리

## 실습 학습 가이드

## 다음 학습 경로
```

`실습 학습 가이드`에는 별도 실습 파일의 목차와 목적을 설명한다. 다중 URL 묶음 작업에서는 `guide/README.md`와 `guide/01_foundations.*` 같은 단계별 실습 파일 링크를 포함한다. 긴 코드를 `README.md` 안에 몰아넣지 않는다.

### 4. Translation Gate

논문이 아닌 원문 또는 주요 참고 자료가 한국어가 아니면 `translation.ko.md`를 만든다.

일반 웹사이트 URL이 입력이면 원문 언어와 관계없이 위 `Website URL Workflow`에 따라 `translation.ko.md`를 반드시 만든다.

논문 입력이면 위 두 규칙 대신 `Paper Translation Workflow`를 적용하여 `<논문 제목>.번역.md`를 만든다. 논문 번역 파일이 있으면 같은 내용을 담은 `translation.ko.md`를 중복 생성하지 않는다.

- 원문의 핵심 구조와 제목 흐름을 유지한다.
- 코드는 원문의 의미를 보존한다.
- 코드 주석을 새로 작성하거나 보강할 때는 한국어 학습자에게 도움이 되도록 설명한다.
- 저작권이 있는 웹 문서는 전문을 무단 복제하지 말고, 필요한 범위에서 번역 요약과 핵심 설명을 제공한다.
- 논문 문장 대조 번역은 원문과 번역을 같은 sentence ID로 연결하고, 약어·기술 용어의 원어·한국어·논문 내 역할을 설명한다.

### 5. Learning Guides

학습 파일은 번호 라벨을 붙여 순서를 고정한다.

단일 웹사이트나 논문 중심 작업은 주제 폴더 루트에 둘 수 있다. 다중 URL 묶음, GitHub 코드 분석이 포함된 작업, 사용자가 실습 중심 구성을 요구한 작업은 주제 폴더 안의 `guide/` 폴더에 둔다.

루트 배치 예시:

```text
01_foundations.ipynb
02_core_concepts.ipynb
03_build_something.ipynb
04_advanced_patterns.ipynb
```

`guide/` 배치 예시:

```text
guide/
  README.md
  01_foundations.ipynb
  02_practice.ipynb
  03_advanced.ipynb
  examples/
```

코드 작성 규칙:

- 기본은 Python과 Jupyter Notebook이다.
- 문서의 핵심 예제가 C++이면 `*.cpp`, C#이면 `*.csx`를 사용한다.
- 모든 실습 파일은 초보자가 바로 실행 목적을 이해할 수 있게 시작 부분에 목표와 실행 방법을 적는다.
- 코드 주석에는 문법 설명과 "왜 이렇게 작성했는지"를 함께 적는다.
- 단순 예제에서 끝내지 말고, 기초 예제에서 응용 예제로 이어지게 구성한다.
- 외부 패키지가 필요하면 설치 방법과 최소 실행 예제를 적는다.
- GitHub 저장소를 submodule로 두지 않는 다중 URL 작업에서는 실습 코드가 외부 저장소의 로컬 경로에 의존하지 않도록 작성한다.

### 6. Root README Index Update

작업이 끝나면 프로젝트 최상단 `README.md`의 `## TODO` 바로 아래에 새 폴더 `README.md` 경로를 체크박스 링크로 추가한다.

형식:

```md
- [ ] [<주제명>](<topic-folder>/README.md) - YYYY-MM-DD
```

새 항목은 최신순으로 위에 둔다. 최초 안내용 placeholder 항목이 실제 작업 목록을 방해하면 제거한다.

### 7. Self-Check

작업 완료 전에 아래 항목을 스스로 확인한다.

- [ ] 요청 하나가 하나의 주제 폴더로 정리되었는가?
- [ ] 새 폴더 `README.md` 상단에 작성일이 있는가?
- [ ] 새 폴더 `README.md`에 목차가 있고 주요 산출물 링크가 포함되었는가?
- [ ] 분석, 요약, 기초 개념, 상세 정리, 용어, 학습 경로가 포함되었는가?
- [ ] 여러 URL에 GitHub 저장소와 일반 사이트·논문이 섞인 경우 submodule/clone 없이 일반 사이트처럼 분석했는가?
- [ ] GitHub 코드 분석이 포함된 경우 코드 리뷰, 사용 방법, 실행 흐름, 주의점이 작업 주제 폴더 안에 정리되었는가?
- [ ] 논문이 아닌 외국어 원문이면 `translation.ko.md`가 있는가?
- [ ] 논문이 아닌 일반 웹사이트 URL이면 원문 언어와 관계없이 `translation.ko.md`가 있는가?
- [ ] 논문 입력이면 일반 번역 파일 대신 `<논문 제목>.번역.md`가 생성되었는가?
- [ ] 논문 제목, 저자, venue, 연도, DOI·식별자, 원문 URL, 버전, 접근일과 확인 범위가 기록되었는가?
- [ ] 논문 원문 문장과 한국어 번역이 동일한 sentence ID로 바로 이어지는가?
- [ ] sentence ID가 중복 없이 순서대로 이어지고 모든 `Original` block에 대응하는 `한국어` block이 있는가?
- [ ] 약어와 기술 용어가 최초 등장 문장 아래에서 설명되고 문서 끝 용어 사전에 정리되었는가?
- [ ] 수식·인용·수치·단위·표·그림 caption과 가능성·부정 표현이 왜곡되지 않았는가?
- [ ] 접근 제한, OCR 불확실성, 저작권·license와 번역 범위가 정직하게 표시되었는가?
- [ ] 번호가 붙은 실습 파일이 있는가?
- [ ] 다중 URL 묶음 또는 실습 중심 작업의 단계별 학습 코드를 `guide/` 폴더에 배치했는가?
- [ ] 실습 파일에 기초 문법과 작성 이유를 설명하는 주석이 충분한가?
- [ ] 최상단 `README.md`의 `TODO`에 새 `README.md` 링크가 추가되었는가?
- [ ] 출처와 확인 기준일이 기록되었는가?

## Agent Prompt Pattern

다른 에이전트에게 이 레포의 작업을 맡길 때는 다음 패턴을 사용한다.

```text
이 레포의 AGENTS.md Content Learning Harness를 반드시 따른다.
아래 입력을 하나의 주제 폴더로 분석, 요약, 번역, 실습화한다.
완료 후 루트 README.md의 TODO에 새 폴더 README.md 링크를 추가한다.

입력:
<URL 또는 내용>
```

입력이 논문이면 다음 요구를 prompt에 추가한다.

```text
입력을 논문으로 판별하면 AGENTS.md의 Paper Translation Workflow를 우선 적용한다.
원문·버전·license와 실제 접근 범위를 확인하고 `<논문 제목>.번역.md`를 만든다.
각 원문 문장 직후 같은 sentence ID의 한국어 번역을 배치한다.
처음 등장하는 약어와 기술 용어는 원어, 한국어 번역과 논문 내 역할을 설명한다.
수식, 인용, 수치, 단위와 가능성·부정 표현을 원문과 대조해 검수한다.
```

## Quality Bar

- 한국어 학습자가 원문을 보지 않아도 핵심을 이해할 수 있어야 한다.
- 논문 번역은 원문과 번역을 오가며 읽을 수 있어야 하고, 문장별 의미와 분야 용어를 동시에 학습할 수 있어야 한다.
- 기초 설명을 생략하지 않는다.
- 실습 자료는 복사해서 실행하는 수준이 아니라, 읽으면서 배우는 코드여야 한다.
- 불확실한 내용은 단정하지 않고 가정, 추론, 확인 필요 사항으로 분리한다.
- 결과물의 목적은 "아카이브"가 아니라 "학습 가능한 실험실"이다.
