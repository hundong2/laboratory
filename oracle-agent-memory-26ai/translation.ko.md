# 사이트 한국어 번역·재구성본

원문: [How I Taught an AI to Sound Like Me: Agent Memory with Oracle AI Database](https://blogs.oracle.com/developers/how-i-taught-an-ai-to-sound-like-me-agent-memory-with-oracle-database-26ai)
저자: Wojtek Pluta · 게시일: 2026-07-22 · 접근일: 2026-08-11 · 원문 언어: 영어

> 이 문서는 저작권이 있는 Oracle 블로그 전문을 복제하지 않고, 원문의 section 흐름·수치·코드 의미를 보존한 한국어 번역 요약이다. 전체 코드는 원문과 [공식 companion repository](https://github.com/oracle-devrel/oracle-ai-developer-hub/tree/main/apps/oracle-agent-memory)에서 확인할 수 있다.

## 핵심 요점

- AI가 글을 못 쓰는 것이 아니라 매번 아무 기억 없이 시작하는 것이 문제다.
- 좋은 글쓰기 보조에는 과거 사례인 episodic, 구조화된 문체 profile인 semantic, 시간에 따른 변화를 반영하는 reflective memory가 필요하다.
- Oracle AI Database는 post, vector, JSON profile과 reflection log를 한 DB에 둔다.
- 학습처럼 느끼게 만드는 부분은 최근 글과 profile을 비교해 보수적인 diff를 적용하는 reflection loop다.
- 최종 `generatePost`는 profile, 유사 예제 몇 개와 LLM 호출 한 번으로 작다. 어려운 부분은 prompt보다 올바른 memory다.

## 문제와 목표

stateless model은 과거 글, 성공·실패, 자연스러운 말투를 모른 채 인터넷 평균 문체로 돌아간다. 목표는 topic과 platform을 입력받아 사용자처럼 들리는 초안을 만들고, prompt 자체를 바꾸지 않은 채 편집·게시 이력으로 점차 개선되는 agent다. 예제 stack은 Node.js, React+Vite, TypeScript, 공식 `oracledb` driver와 OCI Generative AI다. Python에서는 `langchain-oracledb`가 대응 선택지로 소개된다.

## 만들 시스템

episodic memory는 모든 게시물을 embedding과 함께 저장하고 비슷한 과거 글 K개를 예제로 가져온다. semantic memory는 tone, 평균 문장 길이, 구조 습관, signature phrase, 하지 않는 표현, 관심 주제와 platform별 특징을 JSON으로 저장한다. reflective memory는 최근 글에서 확인된 변화와 적용 후 profile을 기록한다.

## 설정과 세 테이블

companion repository에는 Always Free Autonomous AI Database 26ai용 Terraform 구성이 있으며 `terraform init`, `terraform apply`, `terraform output`으로 `.env`를 만들도록 안내한다. OCI Generative AI는 Always Free가 아니며 원문은 신규 계정 trial credit과 소액 call 비용을 언급한다. 가격·혜택은 변동 가능하므로 현재 정책을 확인해야 한다.

`posts`는 `VECTOR(1024, FLOAT32)`와 HNSW cosine index를 사용한다. `style_profile`은 사용자별 JSON과 version을, `reflections`는 post window·diff·적용 후 profile을 저장한다. vector 차원 1024는 `cohere.embed-english-v3.0`에 맞춘 것이므로 model 변경 시 schema도 변경해야 한다.

## LLM wrapper

OCI SDK를 `embed(texts)`와 `chat({system,user})` 두 함수로 감싼다. 원문은 config의 DEFAULT profile을 읽는 authentication provider와 on-demand serving을 사용한다. 이 wrapper 덕분에 이후 memory 코드는 provider 세부사항에 의존하지 않는다.

## Episodic memory

게시 시 content embedding을 만들고 `posts`에 저장한다. 새 topic의 embedding으로 cosine distance를 계산하면서 `user_id`, 같은 `platform`, 미삭제 조건을 한 SQL query에 적용한다. `FETCH APPROX FIRST :k ROWS ONLY`를 써야 Oracle이 HNSW approximate nearest-neighbor index를 활용하며, `APPROX`가 없으면 exact scan으로 돌아간다는 점을 강조한다.

## Semantic memory

사람은 자기 문체를 정확히 설명하기 어려우므로 초기 N개 글을 voice analyst prompt에 넣고 JSON profile을 생성한다. “친근하다” 같은 추상 표현보다 “직설적이고 때때로 자기비하적이며 과장에 약간 회의적”처럼 관찰 가능한 특징을 요구한다. `MERGE`로 insert/update를 한 round trip에 처리하고 Oracle JSON type으로 형식을 검증한다. 실제 구현에서는 LLM 출력에 별도 application schema validation도 필요하다.

## Reflective memory

취향과 문체는 변하므로 최근 K개 글마다 reflection을 실행한다. 원문 예시는 K=5다. 최근 글만으로 profile 전체를 덮어쓰면 profile thrashing이 생기므로, model에 구체적 증거가 있는 additions와 removals만 반환하라고 지시한다. diff를 적용한 뒤 입력 post ID, diff, `profile_after`를 기록한다. 잘못 학습하면 이전 snapshot에서 재구성해 사실상 “unlearn”할 수 있다.

## 실제 생성

`generatePost`는 style profile을 읽고 같은 사용자의 같은 platform에서 유사 글 5개를 가져온다. system prompt에 profile과 예제를 넣되 예제 문구를 복사하거나 AI임을 언급하지 말라고 하고, platform과 topic을 user message로 전달한다. 사용자가 초안을 편집해 게시하고 그 결과를 다시 저장하면 실제 목소리에 가까운 사례가 축적된다.

## FAQ 요약

- “내 목소리로 써라”만으로 부족한 이유는 model이 목소리를 입증할 과거 증거가 없기 때문이다.
- episodic memory는 embedding된 과거 글에서 유사 사례를 찾는다.
- style profile은 글의 tone·문장·구조·금기·관심사를 담는 semantic memory다.
- reflection diff는 최근 다섯 글에 과민 반응하는 것을 막는다.
- 잘못된 style update는 reflection history의 이전 `profile_after`로 rollback한다.

## 마무리

agent memory는 단순 사실 기억이 아니라 유사 사례, 요약된 정체성과 장기 audit을 포함한다. 원문은 production-ready system에 세 계층이 모두 필요하며, Oracle AI Database의 vector·JSON·filter 통합이 DB 계층을 작게 유지한다고 결론짓는다.
