# AI 텍스트 워터마킹: 원리, 검출, 편집 내성

작성일: 2026-08-17

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [핵심 요약](#핵심-요약)
- [상세 정리](#상세-정리)
- [주장을 읽을 때의 주의점](#주장을-읽을-때의-주의점)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 주 원문: [How AI text watermarking works: a visual guide](https://declaude.org/watermarking/)
- 최종 URL: `https://declaude.org/watermarking/`
- 저자 표기: James Padolsey, NOPE / DeClaude
- 원문 언어: 영어
- 접근일: 2026-08-17
- 원문 게시일: 페이지에 별도 표시되지 않음
- 확인 범위: 5개 본문 단계, interactive figure의 설명과 수식 메모, 출처 목록

원문은 interactive animation으로 후보 token의 확률, secret-key green/red partition, detector count, 편집 깊이에 따른 window 생존을 보여준다. 이 저장소는 화면을 복제하지 않고 저작권 범위 내에서 [한국어 번역·재구성본](translation.ko.md)과 독립적인 toy simulation을 제공한다.

교차 확인한 1차 출처:

- Kirchenbauer et al., [A Watermark for Large Language Models](https://arxiv.org/abs/2301.10226), 2023
- Kirchenbauer et al., [On the Reliability of Watermarks for Large Language Models](https://arxiv.org/abs/2306.04634), 2023
- Dathathri et al., [Scalable watermarking for identifying large language model outputs](https://www.nature.com/articles/s41586-024-08025-4), Nature 2024
- Google DeepMind, [Watermarking AI-generated text and video with SynthID](https://deepmind.google/blog/watermarking-ai-generated-text-and-video-with-synthid/)
- Sadasivan et al., [Can AI-Generated Text be Reliably Detected?](https://arxiv.org/abs/2303.11156), 2023
- Anthropic, [How Claude marks AI-generated content](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content), 2026-08-17 확인

## 한눈에 보기

텍스트 워터마크는 character나 metadata에 숨는 표식이 아니다. 생성 model이 다음 token을 고르는 수많은 작은 선택에서 secret key가 선호하는 후보를 조금 더 자주 선택하도록 만드는 통계적 신호다.

```text
prefix + secret key
       ↓
후보 token을 green/red로 재현 가능하게 분할
       ↓
생성 시 green token의 logit을 약하게 높임
       ↓
긴 문서에서 green 비율이 우연 수준보다 높아짐
       ↓
key-holder가 같은 분할을 재생하고 z-score/p-value 계산
```

핵심은 문장 하나를 보고 맞히는 style classifier가 아니라, key를 가진 주체가 충분히 긴 text에서 작은 편향이 누적됐는지 검정하는 통계 절차라는 점이다.

## 기초 개념

### 다음 token 확률

LLM은 매 위치에서 vocabulary의 logit을 확률로 바꾸고 token을 선택한다. 의미가 자연스러운 후보가 여러 개라면 품질을 크게 바꾸지 않고 선택 확률에 작은 신호를 넣을 여지가 생긴다.

### keyed partition

대표적인 green-list 방식은 secret key와 직전 token window를 hash해 현재 위치의 vocabulary를 green set과 red set으로 나눈다. 같은 key와 prefix를 가진 detector는 이 분할을 그대로 재현할 수 있다. 같은 단어도 prefix가 바뀌면 다른 색이 될 수 있다.

### logit bias

green 후보의 logit에 `δ`를 더하면 green 선택 확률이 조금 오른다. `δ`가 크면 검출은 쉬워지지만 품질·분포 왜곡 위험이 커진다. `δ`가 작으면 자연스럽지만 긴 text가 필요하다.

### 통계 검정

검사한 token 수를 `T`, green 수를 `G`, 기대 green 비율을 `γ`라 하면 단순 근사는 다음과 같다.

```text
z = (G - γT) / sqrt(T γ (1 - γ))
```

null hypothesis는 “이 key 기준으로 green 선택이 우연 수준이다”이다. 큰 양의 `z`는 watermark 증거지만 저자 신원이나 생성 과정 전체를 증명하지 않는다.

## 핵심 요약

1. **워터마크는 선택 분포에 있다.** copy-and-paste로 없어지는 metadata가 아니라 token 선택의 누적 편향이다.
2. **secret key가 필요하다.** 진짜 keyed detector와 style 기반 “AI detector”는 다른 도구다.
3. **길이가 검출력을 만든다.** 작은 편향은 `√T` 규모로 증거가 커지므로 짧은 text는 본질적으로 어렵다.
4. **편집은 신호를 희석한다.** context-dependent scheme에서는 표현을 바꾼 위치 주변 window가 깨져 해당 evidence가 사라진다.
5. **발견은 processing evidence다.** proofreading·translation처럼 human text를 model이 처리해도 mark가 생길 수 있다.
6. **미검출은 AI가 아님을 뜻하지 않는다.** 구형 model, 짧은 output, unsupported surface, heavy edit가 false negative를 만든다.
7. **scheme마다 공격 표면이 다르다.** context-free token mark, context-dependent mark, semantic watermark는 같은 rewrite에 다르게 반응한다.

## 상세 정리

### 1. 생성은 작은 선택의 연속이다

원문 첫 단계는 한 문장의 마지막 후보들이 서로 다른 확률을 갖되 모두 자연스러울 수 있음을 보여준다. 한 번의 선택은 정보가 거의 없지만 문서 전체에는 이런 fork가 수백 번 존재한다. 이 redundancy가 watermark signal의 carrier가 된다.

제약이 강한 factual answer, code, quotation은 가능한 continuation이 적다. 품질을 보존하면서 bias를 넣을 자유도가 줄어들어 signal이 약해진다.

### 2. key가 선택을 약하게 기울인다

KGW 계열 teaching model에서는 key와 context가 후보를 green/red로 나누고 green logit을 올린다. red token도 여전히 선택될 수 있어 개별 단어만으로는 mark를 알 수 없다.

SynthID-Text는 같은 목적을 더 정교한 tournament sampling으로 달성한다. Google의 설명에 따르면 여러 후보 sample을 secret scoring function으로 비교하면서 model의 원래 품질을 유지하도록 설계한다. 특정 provider의 production parameter와 key는 공개되지 않는다.

Aaronson 계열은 pseudo-random sampling 자체를 key와 prefix에서 유도한다. 구현 수학은 달라도 “key-holder만 재현 가능한 token choice pattern”이라는 공통 원리를 갖는다.

### 3. detector는 key로 다시 세고 검정한다

detector는 문체나 의미를 판정하지 않는다. tokenization 후 각 위치의 prefix와 key로 green 여부를 다시 계산하고 count statistic을 만든다. wrong key에서는 색 분할이 signal과 독립이므로 chance 부근이어야 한다.

임계값은 false-positive tolerance와 text length에 따라 정해야 한다. 여러 key, 여러 span, 여러 detector를 동시에 시험하면 multiple testing correction도 필요하다. 실무 verdict는 단순 `detected/not detected`뿐 아니라 text 길이, score, calibration version, 적용 model surface를 함께 제공해야 한다.

### 4. 편집은 context window를 끊는다

context-dependent mark에서 한 token의 색은 앞선 몇 token에 의존한다. 단어 하나를 바꾸면 그 위치뿐 아니라 이후 context window도 원래 detector sequence와 달라진다. typo correction이나 light edit는 많은 run을 보존하고, 의미부터 다시 구성하는 rewrite는 lexical run을 크게 줄인다.

원문은 공개 KGW/EXP implementation에 대한 자체 실험으로 full rewrite 뒤 window 생존율 약 0.5%, AUC가 약 0.5로 하락했다고 보고한다. 이는 DeClaude 저자의 실험이며 Anthropic production watermark 결과가 아니다. Anthropic scheme은 공개되지 않아 외부에서 동일 test를 수행할 수 없다는 제한도 원문이 명시한다.

원문의 교육용 잔여 증거 근사는 다음과 같다.

```text
z_residual ≈ f × sqrt(N) × z₁
```

- `f`: 살아남은 keyed window 비율
- `N`: 문서 token 수
- `z₁`: token당 signal strength

이는 직관 model이지 모든 detector의 정확한 공식이 아니다. 실제 detector는 provider tokenizer, repeated n-gram 처리, score aggregation과 calibration을 사용할 수 있다.

### 5. 실제 verdict의 의미

- provider key 또는 provider가 운영하는 검출 service가 없으면 같은 test를 할 수 없다.
- mark 검출은 해당 system이 content를 처리했을 가능성의 evidence다.
- proofreading, translation, summary에도 mark가 붙을 수 있어 original authorship을 단정할 수 없다.
- short passage, heavy edit, translation, mixed text, unsupported model·surface에서는 mark가 검출되지 않을 수 있다.
- provider documentation과 적용 범위는 변할 수 있으므로 verdict 시점의 version을 기록한다.

## 주장을 읽을 때의 주의점

### 공급자 적용 범위는 시간에 따라 변한다

DeClaude 페이지는 2026년 8월 기준 Claude 새 model이 model-level text marking을 사용한다고 설명한다. 2026-08-17에 확인한 Anthropic Help Center는 EU에서 2026-08-02 이후 출시되는 model의 machine-readable marking, supported Claude surfaces의 text watermark와 detection tooling 지원 계획을 설명한다. 동시에 platform·feature별 예외와 heavy editing·translation·짧은 passage의 미검출 가능성을 명시한다.

Google DeepMind는 Gemini web/app output에 SynthID를 사용한다고 설명하며, API 적용 여부는 product·시점별 공식 문서를 확인해야 한다. DeClaude가 연결한 forum 답변만으로 모든 Gemini API model을 일반화하지 않는다.

### 원문 animation은 production detector가 아니다

원문도 후보 확률, green 비율, threshold와 edit simulation이 illustrative parameter라고 밝힌다. animation에서 보이는 강한 bias와 짧은 passage의 verdict를 실제 서비스 성능으로 읽으면 안 된다.

### robustness와 impossibility result를 함께 읽는다

워터마크 논문은 충분한 길이에서 paraphrase·insertion·deletion을 견디는 설계를 보인다. 반면 detection 한계 연구는 품질을 유지하는 transformation, distribution access, human text와 AI text의 overlap 때문에 완벽한 detector가 불가능함을 지적한다. 검출 결과는 다른 provenance evidence와 결합해야 한다.

## 용어 정리

| 용어 | 설명 |
|---|---|
| watermark | 생성 과정에 의도적으로 넣은 machine-readable statistical signal |
| token | model tokenizer가 text를 나눈 기본 단위. word와 일치하지 않을 수 있음 |
| logit | softmax 전의 비정규화 점수 |
| green list | key와 context가 해당 위치에서 선호하도록 정한 후보 집합 |
| `γ` | null hypothesis에서 기대하는 green 비율 |
| `δ` | green token logit에 더하는 bias strength |
| z-score | 관측 green 수가 우연 기대에서 표준편차 몇 배 떨어졌는지 나타내는 값 |
| false positive | unmarked text를 marked로 판정 |
| false negative | marked text를 검출하지 못함 |
| AUC | threshold 전체에서 ranking 성능을 요약한 ROC 면적 |
| context window | 현재 색/score 계산에 쓰는 직전 token 범위 |
| paraphrase attack | 의미를 유지하며 wording을 바꿔 signal을 희석하는 변환 |
| provenance | content가 어디서 어떤 처리를 거쳤는지에 관한 이력 evidence |

## 실습 학습 가이드

- [01_foundations.ipynb](01_foundations.ipynb): keyed green-list 생성, logit bias, z-score
- [02_practice.ipynb](02_practice.ipynb): right/wrong key와 편집 깊이별 검출력 비교
- [03_advanced.ipynb](03_advanced.ipynb): Monte Carlo false-positive calibration, ROC AUC, mixture·rewrite simulation

모든 notebook은 Python 표준 library만 사용하며 실제 provider watermark를 구현하거나 우회하는 도구가 아니다. 공개된 교육용 toy scheme으로 통계 직관과 평가 함정을 학습한다.

## 다음 학습 경로

1. KGW 논문에서 generation algorithm과 detector의 hypothesis test를 읽는다.
2. reliability 논문에서 insertion, deletion, paraphrase와 repeated n-gram 처리를 비교한다.
3. SynthID-Text 논문에서 tournament sampling과 detector training을 공부한다.
4. Sadasivan et al.의 detection 한계와 watermark assumption을 비교한다.
5. 실제 system에서는 C2PA·signed metadata, access log, human disclosure와 watermark를 함께 설계한다.

## 책임 있는 사용

이 자료는 watermark 원리와 평가를 이해하기 위한 것이다. 교육기관·고용·법적 제재처럼 중대한 결정에서 단일 detector score를 유일한 근거로 사용하지 않는다. key 탈취, provider detector 회피, 타인 content의 provenance 위조를 목적으로 사용해서는 안 된다.
