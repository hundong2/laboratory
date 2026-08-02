# 「Ten advances in mathematics and theoretical computer science」 한국어 번역 요약

작성일: 2026-08-03

- 원문: [OpenAI 공식 발표](https://openai.com/index/ten-advances-in-mathematics/)
- 게시일: 2026-08-01
- 원문 언어: 영어
- 접근일: 2026-08-03 (Asia/Seoul)
- 관련 자료: [논문](https://cdn.openai.com/pdf/ten-proofs-oai.pdf), [추론 해설](https://cdn.openai.com/pdf/reasoning-walkthroughs.pdf), [Lean 인증](https://github.com/openai/ten-proofs)

> 저작권을 존중해 원문 전문을 복제하지 않고, 원문의 섹션 구조와 핵심 주장·수치를 유지한 한국어 번역 요약을 제공한다. 신규 수학 결과는 OpenAI의 발표 내용이며 독립 검증 완료를 뜻하지 않는다.

## 수학과 이론 컴퓨터과학의 10가지 진전

OpenAI는 과학자와 수학자의 발견을 가속하는 도구를 만들고자 한다. 최근에는 10만 명의 과학자와 수학자에게 최고 성능의 ChatGPT 모델을 무료 제공하는 ChatGPT for Academic Researchers 계획을 발표했으며, 개발 과정에서 공개 연구 문제로 모델을 계속 평가하고 있다고 설명한다.

2026년 5월에는 당시 미공개 모델을 평가하다 발견한 Erdős unit-distance conjecture의 AI 생성 반례를 공유했다. OpenAI는 이 결과가 수학과 이론 컴퓨터과학의 후속 연구를 촉발했다고 말한다. 이번에는 핵심 결과에서 최소 10년, 대부분은 그보다 오래 진전이 없었던 공개 문제 10개에 대한 결과를 제시한다.

문제들은 고차원 기하, 부호 이론, 산술 회로 복잡도, 군론, 작용소 대수, 양자 복잡도, 격자 암호와 극값 조합론을 아우른다.

## 결과

결과는 OpenAI의 차기 주요 모델인 Astra 내부 버전이 만들었다. OpenAI는 해법을 찾는 데 필요한 전체 token을 Sol API 요금으로 환산하면 약 2,000달러라고 설명한다. 이후 인간이 같은 모델을 사용해 논증을 원고로 정리했고, 모델은 각 논증을 Lean 인증서로 형식화했다. 각 해법에 대해서는 모델이 발견 과정을 설명하는 별도 서술도 공개했다.

1. **고차원 sphere packing**: 구 채우기 밀도의 새 상한을 Cohn–Elkies threshold까지 낮췄다.
2. **이진·구면 code**: 주어진 모든 최소 거리에서 최대 이진 code 크기의 상한을 지수적으로 개선하고, 고차원 구면 code에도 대응 결과를 얻었다.
3. **비소픽 군**: 비소픽 군을 구성해 모든 가산 군이 소픽인지에 대한 군론의 중심 질문에 답한다.
4. **Connes 강성 추측**: 특정 군이 von Neumann algebra로 유일하게 결정된다는 오랜 추측을 반증한다.
5. **산술 회로 복잡도**: permanent 계산의 새 하한을 제시하며, 산술 formula에는 `n⁴/log n` 차수의 하한을 얻는다.
6. **양자 parallel repetition**: 일반적인 2인 양자 game에 대한 지수적 병렬 반복 정리를 증명해 고전 복잡도 이론의 기본 원리를 확장한다.
7. **Closest Vector Problem**: post-quantum cryptography와 관련된 기본 격자 문제에서 다항 인자 근사의 hardness를 보인다.
8. **Ehrhart 부피 추측**: 무게중심이 유일한 내부 격자점인 convex body의 최대 가능 부피를 모든 차원에서 결정한다.
9. **다색 Ramsey 수**: 다색 삼각형 Ramsey 수의 초지수 하한을 얻어 Erdős problem 183을 해결한다.
10. **극값 수 추측**: 극값 graph theory의 compactness와 degeneracy 추측에 답해 Erdős problem 146과 180을 해결한다.

## 수학 공동체에 대한 책임

수학 연구에 기여할 수 있는 시스템의 등장은 기술 기업 혼자 답할 수 없는 질문을 만든다. 수학에서 AI가 맡을 역할에 다양한 견해가 있으며, OpenAI는 Leiden Declaration on AI and Mathematics 서명자들을 포함해 영향에 우려를 표하는 사람들의 입장을 존중한다고 밝힌다.

OpenAI는 저자 표시가 결과의 생산 방식을 정직하게 반영해야 한다고 주장한다. AI 시스템이 전적으로 생성한 증명을 인간이 만든 것으로 표시하면 시스템의 기여와 인간의 실제 지적 작업을 모두 잘못 나타낸다는 것이다. 인간은 원고 준비와 Lean 형식화를 도왔고 OpenAI는 정확성에 책임을 지지만, 수학적 논증 자체는 시스템이 생성했다고 구분한다.

OpenAI는 수학 공동체가 결과를 깊이 검토하고 맥락 속에 놓으며, 그 아이디어를 새로운 연구와 발견으로 발전시키기를 기대한다. AI가 더 정교한 연구 협력자로 발전할수록 과학자와 수학자가 미래의 규범을 함께 정할 수 있도록 넓은 접근성을 보장하는 것이 중요하다고 말한다.

## 각주와 후속 연구

발표는 앞서 공개한 Erdős unit-distance conjecture 반례에서 이어진 후속 연구로 sum-product conjecture, Elekes–Rónyai 문제, 고차원 furthest-pair 복잡도, 실수 위 점-직선 incidence의 communication complexity와 Minkowski grid의 반복 거리 관련 논문을 열거한다. 정확한 서지정보와 링크는 원문의 각주를 따른다.

## 번역 검수 기록

- 원문의 `The results`, `Responsibility to the mathematical community`, 각주 흐름을 유지했다.
- 10개 결과의 문제명, 차수와 Erdős problem 번호를 원문 및 논문 abstract와 대조했다.
- `proof`, `formalization`, `certificate`를 같은 뜻으로 합치지 않고 역할을 구분했다.
- 신규 주장을 확정된 정설로 강화하지 않고 OpenAI가 발표한 결과임을 표시했다.
