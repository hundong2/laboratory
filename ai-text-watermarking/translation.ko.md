# 「How AI text watermarking works」 한국어 번역·재구성

작성일: 2026-08-17

- 원문: [How AI text watermarking works: a visual guide](https://declaude.org/watermarking/)
- 최종 URL: `https://declaude.org/watermarking/`
- 저자: James Padolsey, NOPE / DeClaude
- 원문 언어: 영어
- 접근일: 2026-08-17
- 번역 범위: 본문 5단계와 한계·출처 설명
- 저작권 경계: interactive page의 전문과 JavaScript를 복제하지 않고 구조와 핵심 의미를 보존한 한국어 번역 요약을 제공한다.

## 이 글이 던지는 질문

plain text에는 pixel도 숨은 metadata도 없다. copy-and-paste하면 보이지 않는 file 정보도 사라진다. 그런데 어떻게 눈에 보이지 않는 표식을 text에 남길 수 있을까?

답은 character 안이 아니라 단어와 token 사이의 **선택**에 있다. model은 매 순간 하나의 정답 단어를 알고 쓰는 것이 아니라, 문맥상 가능한 후보에 서로 다른 확률을 부여하고 그중 하나를 고른다. watermark는 이 선택을 secret key에 따라 아주 조금 기울여 긴 text에 통계 pattern을 축적한다.

원문은 Google SynthID와 2026년 Claude marking을 사례로 들지만 product별 적용 범위는 변동될 수 있다. 실제 판정에는 각 provider의 최신 공식 문서가 필요하다.

## 1. 글쓰기는 작은 선택의 연속이다

model이 문장을 거의 완성한 순간에도 다음 token 후보는 하나가 아니다. “important”, “significant”, “substantial”, “notable”처럼 모두 문법적이고 의미상 허용되지만 확률은 서로 다를 수 있다.

원문의 첫 animation은 weighted dice를 여러 번 굴려 높은 확률 후보가 더 자주 선택되되 낮은 확률 후보도 가끔 나온다는 점을 보여준다. 어느 후보가 나와도 문장은 자연스럽다.

한 문서에는 이런 fork가 수백 번 있다. 그때마다 의미를 유지하는 여유가 있다면, dice가 어느 쪽으로 조금 더 자주 기우는지에 pattern을 숨길 수 있다.

## 2. secret key가 선택을 기울인다

고전적인 green-list 방식에서는 secret key와 직전 문맥을 이용해 후보 token을 임의의 green/red 집합으로 나눈다. 이 색은 단어의 고정 속성이 아니다. 같은 단어도 앞선 token이 달라지면 green이 되거나 red가 된다.

generator는 green 후보의 확률을 조금 높인다. 편향은 약하기 때문에 red도 여전히 선택되고 text 품질과 의미가 유지된다. 한 token만 보아서는 어떤 mark도 알 수 없지만 많은 위치에서 green이 예상보다 자주 나오면 pattern이 생긴다.

원문은 같은 원리를 구현하는 여러 계열을 구분한다.

- KGW 계열: context와 key로 green list를 만들고 logit을 nudging한다.
- SynthID-Text: model 확률에서 뽑은 후보를 secret tournament score로 비교하는 더 정교한 방식이다.
- Aaronson 계열: key로 pseudo-random sampling choice 자체를 유도한다.

세부 수학은 다르지만 secret key를 가진 쪽만 재현 가능한 선택 pattern에 mark가 있다는 원리는 같다.

## 3. key-holder는 pattern을 다시 셀 수 있다

검출기는 글의 style이나 주장을 읽지 않는다. 같은 key로 각 위치의 색을 다시 계산하고 green이 몇 번 나왔는지 센다.

mark가 없거나 wrong key를 사용하면 green 비율은 chance 수준에 가까워야 한다. right key를 사용한 marked text에서는 green이 더 자주 나온다. 작은 차이는 짧은 text에서 우연과 구분하기 어렵지만 문서가 길어질수록 evidence가 누적된다.

원문의 animation은 이를 눈에 잘 보이도록 실제 production보다 훨씬 강한 편향으로 그린다. 예를 들어 50:50 null에서 1,500 word가 약 55% green인 작은 차이도 길이 덕분에 설득력 있는 통계가 될 수 있다는 직관을 준다. 실제 detector는 word가 아니라 provider tokenizer의 token과 자체 calibration을 사용한다.

## 4. 편집은 mark에 어떤 영향을 주는가

context-dependent scheme에서는 현재 token의 색이 직전 몇 token에 의존한다. 한 단어를 고치면 그 단어와 주변 window가 원본과 달라져 해당 위치의 evidence가 사라진다. 반면 손대지 않은 긴 run의 evidence는 남는다.

원문의 slider는 typo correction, light edit, sentence tightening, heavy edit, full rewrite로 갈수록 원문과 동일한 짧은 window가 줄어드는 모습을 보여준다.

- 가벼운 편집은 mark를 즉시 삭제하기보다 희석한다.
- 충분히 긴 text라면 일부 wording이 바뀌어도 detector가 신호를 회복할 수 있다.
- 표현 run을 거의 공유하지 않는 re-composition은 context-dependent signal을 크게 줄인다.
- context-free unigram 또는 meaning-space watermark는 같은 rewrite에 다르게 반응할 수 있다.

DeClaude 저자는 공개 KGW/EXP 구현을 자체 full-rewrite route로 변환했을 때 window가 약 0.5%만 생존하고 detection AUC가 약 0.99에서 chance 수준으로 떨어졌다고 적는다. 이 수치는 공개 implementation에 대한 저자 실험이지 Claude production scheme 측정이 아니다. Anthropic scheme은 비공개라 외부 검증이 불가능하다는 경계도 함께 제시한다.

## 5. 실무에서 뜻하는 것

### key-holder만 진짜 검사를 할 수 있다

secret key 또는 provider가 운영하는 detection service가 없으면 같은 keyed statistical test를 수행할 수 없다. 일반 “AI detector” website의 style classifier와 혼동하면 안 된다.

### 검출은 저작자가 아니라 처리 이력을 시사한다

mark가 발견돼도 model이 original author였다는 뜻은 아니다. 사람이 쓴 글을 proofreading, translation, summarization한 output에도 marking이 생길 수 있다. 즉 verdict는 “해당 system으로 처리됐을 가능성”에 가깝다.

### 미검출은 더 약한 주장이다

old model, 짧은 text, heavy edit, translation, 다른 text와의 mixture, metadata가 제거된 file, 지원하지 않는 surface에서는 AI content라도 mark가 없거나 검출되지 않을 수 있다.

### 짧고 선택지가 적은 text는 signal이 약하다

code, exact quotation, fact list처럼 continuation 자유도가 낮은 text는 품질을 해치지 않고 probability를 움직일 여지가 적다. 길이가 짧으면 통계 검정의 표본 수도 부족하다.

### 모든 watermark가 rewrite에 똑같이 반응하지 않는다

직전 context에 keying한 scheme은 lexical window가 깨지면 약해진다. 단어 자체에 고정 color를 주는 scheme은 같은 의미 rewrite에서도 같은 단어가 남아 더 버틸 수 있지만 많은 output으로 color mapping을 역추론할 위험이 있다. meaning-level scheme은 표현보다 의미 보존에 강할 수 있다.

## 검출 결과를 안전하게 해석하는 규칙

1. detector provider, model family, 적용 surface, key/calibration version을 기록한다.
2. text token 수, score, threshold와 false-positive target을 함께 제시한다.
3. mark 발견을 human misconduct나 AI authorship의 단독 증거로 사용하지 않는다.
4. 미검출을 human-written의 증명으로 사용하지 않는다.
5. signed provenance, generation log, user disclosure와 문서 history를 함께 검토한다.
6. 중대한 결정에는 human review와 appeal 절차를 둔다.

## 원문 출처와 추가 읽기

원문은 KGW(ICML 2023), reliability 연구(ICLR 2024), SynthID-Text(Nature 2024), Aaronson/Kirchner 방식, AI text detection 한계 연구와 2026년 paraphrase attack 연구를 안내한다. [학습 README](README.md)의 1차 출처 링크와 세 개 notebook에서 개념을 단계별로 확인할 수 있다.

## 번역 검수 기록

- 2026-08-17: 원문 최종 URL, title, 5개 section, author note와 source note 확인
- 수식·수치: 원문 교육용 `1,500 words`, `~55% green`, window `~0.5%`, AUC `0.99→≈0.5`, `z ≈ f√N z₁` 표기를 주장 주체와 함께 보존
- provider 주장: DeClaude 설명과 Anthropic·Google 공식 문서 확인 내용을 분리
- 누락 범위: interactive animation의 JavaScript와 원문 전문은 저작권 및 재사용 필요성 때문에 포함하지 않음
