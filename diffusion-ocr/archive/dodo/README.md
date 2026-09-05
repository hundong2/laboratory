# DODO: Discrete OCR Diffusion Models

작성일: 2026-09-05

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [연구 질문과 기여](#연구-질문과-기여)
- [방법](#방법)
- [데이터와 평가](#데이터와-평가)
- [핵심 결과](#핵심-결과)
- [한계와 재현 주의](#한계와-재현-주의)
- [Diffusion OCR 블로그와의 관계](#diffusion-ocr-블로그와의-관계)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 원문: [arXiv:2602.16872](https://arxiv.org/abs/2602.16872)
- 사용 버전: v2, 2026-05-27 개정본
- 식별자: `arXiv:2602.16872`, DOI `10.48550/arXiv.2602.16872`
- 저자: Sean Man, Gilad Deutch, Roy Ganz, Roi Ronen, Shahar Tsiper, Shai Mazor, Niv Nayman
- 분류/출판 상태: arXiv preprint, cs.CV, 2026
- 라이선스: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- 확인일: 2026-09-05
- 확인 범위: v2 PDF 15쪽 전체를 추출하고 전 페이지를 PNG로 렌더링해 시각 대조했다. 참고문헌과 정성 예시 부록까지 확인했으나, 번역 파일은 초록·핵심 문장 대조와 전 절 한국어 해설을 제공하는 **부분 번역**이다.
- 코드 공개: 논문 첫 페이지와 arXiv 레코드에서 공식 코드 저장소 링크를 확인하지 못했다.

전체 분석은 [문장 대조 번역과 절별 해설](<DODO - Discrete OCR Diffusion Models.번역.md>)에서 이어진다.

## 한눈에 보기

DODO는 OCR을 “정답이 거의 하나로 정해지는 저엔트로피 조건부 생성”으로 보고, 한 토큰씩 생성하는 자기회귀(AR) 대신 **블록 이산 확산**을 적용한다. 전체 문서를 한 번에 마스킹 복원하면 길이 추정과 절대 위치가 어긋나므로, 문장을 여러 블록으로 나누고 이전 블록을 확정된 접두사로 삼는다. 블록 내부 토큰은 병렬 복원하고 블록 사이는 왼쪽에서 오른쪽으로 진행해 안정성과 속도를 절충한다.

## 기초 개념

- **마스킹 확산 모델(MDM)**: 원문 토큰을 `[MASK]`로 오염시킨 뒤, 조건부 분포로 깨끗한 토큰을 반복 복원한다.
- **조건부 독립 가정**: 이미지와 부분 복원 결과가 주어졌을 때 여러 마스킹 위치를 동시에 예측해도 충돌이 작다고 본다. OCR은 캡셔닝보다 가능한 정답 표현이 훨씬 적어 이 가정이 상대적으로 잘 맞는다.
- **carry-over unmasking**: 한 번 공개한 토큰을 다시 마스킹하거나 수정하지 않는다. 빠르지만 잘못 확정한 위치 오류가 남는다.
- **블록 인과 어텐션**: 현재 블록 안에서는 양방향으로 보고, 이전 블록은 읽되 이전 블록이 현재 블록을 보지 못하게 한다. 이 불변 접두사 덕분에 정확한 KV cache를 쓸 수 있다.
- **NED (Normalized Edit Distance)**: 예측과 정답의 편집 거리를 길이로 정규화한 오류 지표다. 이 논문 표에서는 낮을수록 좋다.

## 연구 질문과 기여

연구 질문은 “OCR의 결정성을 이용해 여러 토큰을 병렬 생성하면서, 전역 확산의 길이·위치 동기화 실패를 어떻게 막을 것인가?”이다.

핵심 기여는 세 가지다.

1. 캡셔닝에서는 견딜 수 있는 전역 마스킹 확산의 길이 불일치와 위치 고정 오류가 exact transcription에서는 치명적임을 분석한다.
2. 블록 단위 확산, 블록 인과 어텐션, 정확한 KV cache를 결합한 DODO를 제안한다.
3. 같은 OCR 데이터로 학습한 전역 확산과 블록 확산을 비교해 성능 차이가 데이터만이 아니라 구조에서 온다는 ablation을 제공한다.

## 방법

문서 이미지 `I`를 직렬화된 토큰 `x_1:L`로 바꾼다. 전체 확산 대신 길이 `L'`의 `B`개 블록으로 나눠 다음처럼 모델링한다.

```text
p(x_1:L | I, c) = Π_b p(x^(b) | x^(<b), I, c)
```

각 블록은 `[MASK]`에서 시작하고 확신도가 높은 위치부터 공개한다. 이전 블록은 고정 접두사이므로 길이와 위치를 블록 경계마다 다시 고정할 수 있다. 기본 빠른 변형은 block-causal mask와 exact KV cache를 쓰며, 정확도 분석용 양방향 변형은 이전 블록 표현까지 다시 계산해 더 큰 블록을 안정적으로 사용한다.

구현은 Qwen2.5-VL-3B를 기반으로 하며 최대 길이 8,192, 200,000 step, global batch 8, 8×A100 40GB, AdamW, peak LR `5e-6`, weight decay `0.01`, bfloat16을 사용한다. 기본 샘플러는 confidence threshold `p=0.99`다.

## 데이터와 평가

- 학습: `olmOCR-mix-1025` 약 270K 문서-텍스트 쌍.
- OmniDocBench 영어 subset: 290개 문서, 9개 문서 유형, 텍스트·표·수식 구조 포함.
- Fox-Page-EN: 순수 텍스트 중심 112쪽.
- 정확도: NED(낮을수록 좋음).
- 효율: TPS(tokens per second), 모델 forward 수/토큰.
- 비교군: 전문 OCR, Qwen2.5-VL AR 계열, Dimple·LaViDa·LLaDA-V 확산 VLM.

## 핵심 결과

- DODO-3B NED는 OmniDocBench `0.069`, Fox-Page-EN `0.038`이다. 같은 표의 확산 비교군은 OmniDocBench에서 Dimple `0.856`, LaViDa-L `0.994`, LLaDA-V `0.524`였다.
- 처리량은 exact KV cache 기준 `103.69 TPS`로, Qwen2.5-VL-3B AR의 `21.00 TPS`보다 약 5배 빠르다.
- cache를 모두 끈 통제 비교에서도 DODO 양방향 변형 `42.80 TPS`, AR `2.18 TPS`로 병렬 복원 자체의 이점을 보였다.
- 전역 확산은 oracle length를 줘도 NED `0.100`이었고, 블록 학습+32 토큰 블록은 `0.067`이었다. 전역 학습 모델에 추론 시에만 블록을 적용하면 `0.951`로 악화돼 학습-추론 구조 일치가 중요하다.
- 양방향·no-cache 변형은 블록 256에서 NED `0.057`, `42.8 TPS`로 가장 정확했다. exact-cache 변형은 블록 32에서 NED `0.069`, `103.7 TPS`이며 블록 256에서는 `0.177`로 나빠졌다.
- 4,096 토큰 이상 문서에서 DODO NED `0.079`, Qwen2.5-VL-7B `0.185`로 긴 출력에서 강점이 커졌다.

수치는 서로 다른 cache·attention·block 조건을 섞어 비교하면 안 된다. 특히 “5×”는 논문의 지정 하드웨어/구현과 exact-cache 기본형에 대한 값이다.

## 한계와 재현 주의

- exact KV cache는 과거 표현을 고정하므로 큰 블록에서 양방향 변형보다 정확도가 떨어진다.
- 학습 비용이 8×A100 40GB, 200K step으로 toy notebook과 실제 재현 사이의 격차가 크다.
- 전역 확산, 양방향 블록, block-causal exact-cache의 계산량과 품질을 동일 조건으로 분리해야 한다.
- NED는 구조 태그의 의미적 정확성이나 reading order를 완전히 설명하지 않는다.
- 공개 코드 링크를 확인하지 못했으므로 세부 tokenizer, 전처리, sampler 구현을 PDF만으로 완전히 복원할 수 없다.
- 본 폴더의 notebook은 알고리즘 직관과 지표를 작은 문자열로 검증하는 toy reproduction이며 논문 성능 재현이 아니다.

## Diffusion OCR 블로그와의 관계

Trillion Labs 블로그가 설명하는 핵심 논지, 즉 OCR은 개방형 언어 생성보다 시각 입력에 의해 답이 강하게 고정되므로 병렬 확산에 적합하다는 주장을 DODO가 가장 직접적으로 정식화한다. 동시에 “전체 시퀀스를 병렬 복원하면 충분하다”는 단순한 결론을 반박하고, 블록 경계라는 구조적 안전장치와 KV cache까지 포함해야 실제 처리량이 나온다는 근거를 제공한다.

## 실습 학습 가이드

1. [01_foundations.ipynb](01_foundations.ipynb): 마스킹·확신도 기반 병렬 공개를 직접 구현한다.
2. [02_practice.ipynb](02_practice.ipynb): 블록 접두사 고정, 동적 종료, 편집 거리를 toy OCR로 확인한다.
3. [03_advanced.ipynb](03_advanced.ipynb): 논문 ablation 표에서 정확도-처리량 Pareto frontier를 계산한다.

모든 notebook은 Python 표준 라이브러리만 사용한다.

## 다음 학습 경로

1. MDLM의 이산 ELBO와 complementary masking을 학습한다.
2. Block Diffusion/BD3-LM에서 block factorization과 KV cache 조건을 확인한다.
3. [MinerU-Diffusion 분석](../mineru-diffusion/README.md)과 confidence scheduling·curriculum 차이를 비교한다.
4. [HunyuanOCR-1.5 분석](../hunyuanocr-1-5/README.md)에서 확산 모델을 본 decoder가 아니라 draft model로 쓰는 방식을 비교한다.
