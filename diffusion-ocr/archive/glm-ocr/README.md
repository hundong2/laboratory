# GLM-OCR Technical Report

작성일: 2026-09-05

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [연구 질문과 기여](#연구-질문과-기여)
- [방법과 학습](#방법과-학습)
- [데이터와 평가](#데이터와-평가)
- [핵심 결과](#핵심-결과)
- [한계와 재현 주의](#한계와-재현-주의)
- [Diffusion OCR 블로그와의 관계](#diffusion-ocr-블로그와의-관계)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 원문: [arXiv:2603.10910](https://arxiv.org/abs/2603.10910)
- 사용 버전: v2, 2026-03-16 개정본
- 식별자: `arXiv:2603.10910`, DOI `10.48550/arXiv.2603.10910`
- 저자: Shuaiqi Duan, Yadong Xue, Weihan Wang, Zhe Su, Huan Liu, Sheng Yang, Guobing Gan, Guo Wang, Zihan Wang, Shengdong Yan, Dexin Jin, Yuxuan Zhang, Guohong Wen, Yanfeng Wang, Yutao Zhang, Xiaohan Zhang, Wenyi Hong, Yukuo Cen, Da Yin, Bin Chen, Wenmeng Yu, Xiaotao Gu, Jie Tang
- 분류/출판 상태: arXiv preprint, cs.CL, 2026
- 라이선스: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- 공식 코드: <https://github.com/zai-org/GLM-OCR>
- 공식 모델: <https://huggingface.co/zai-org/GLM-OCR>
- 확인일: 2026-09-05
- 확인 범위: v2 PDF 17쪽 전체를 텍스트 추출하고 전 페이지를 PNG로 렌더링해 시각 확인했다. [번역 파일](GLM-OCR%20Technical%20Report.번역.md)은 핵심 문장 대조와 전 절 상세 해설을 포함한 부분 번역이다.

## 한눈에 보기

GLM-OCR은 diffusion decoder가 아니라 **0.9B 경량 AR VLM + Multi-Token Prediction(MTP)** 시스템이다. 0.4B CogViT encoder와 0.5B GLM decoder를 결합하고, document parsing에서는 PP-DocLayout-V3가 페이지를 영역으로 나눈 뒤 영역을 병렬 인식한다. decoder는 한 step에 최대 여러 future token을 제안·검증해 평균 5.2 token/step을 생성한다. 모델 내부 가속과 시스템 수준 region parallelism을 동시에 사용하는 점이 핵심이다.

## 기초 개념

- **문서 파싱**: 텍스트 전사뿐 아니라 reading order, table, formula를 Markdown/JSON 같은 구조로 복원한다.
- **MTP (Multi-Token Prediction)**: main head 외에 미래 offset별 auxiliary head가 여러 다음 토큰을 동시에 예측한다.
- **layout-first pipeline**: 먼저 region을 검출·crop하고 각 crop을 독립 인식한 뒤 reading order에 맞게 합친다.
- **KIE (Key Information Extraction)**: invoice의 금액·날짜처럼 지정 field를 JSON으로 추출한다.
- **MIM/CLIP/SFT/RL**: visual representation, vision-language alignment, task specialization, structured-output reliability를 단계별로 학습한다.

## 연구 질문과 기여

질문은 “대규모 모델을 쓰지 않고도 실서비스 문서의 표·수식·KIE 정확도, 처리량, 배포 편의성을 함께 확보할 수 있는가?”이다.

1. CogViT 0.4B + GLM 0.5B의 총 0.9B compact architecture를 제시한다.
2. parameter-sharing MTP로 10 future token을 학습하고 평균 5.2 token/decoding step을 달성했다고 보고한다.
3. PP-DocLayout-V3 + region crop + parallel recognition + merge의 실용 pipeline을 구축한다.
4. text, formula, table, KIE를 SFT와 task-aware GRPO reward로 한 모델에 통합한다.

## 방법과 학습

Document Parsing 경로는 다음과 같다.

```text
page -> PP-DocLayout-V3 -> text/formula/table crops
     -> GLM-OCR core를 crop별 병렬 실행 -> reading-order merge -> Markdown/JSON
```

KIE는 전체 문서와 schema prompt를 core에 직접 넣어 JSON을 생성하므로 layout crop을 반드시 거치지 않는다.

학습은 네 단계다.

1. Vision encoder: 수백억 규모 image-text pair, grounding/retrieval, MIM·CLIP, larger ViT distillation.
2. Vision-language pretrain: GLM-0.5B를 연결해 image-text, parsing, grounding, VQA; 이후 MTP 추가.
3. SFT: text/formula/table/KIE를 균형 있게 혼합.
4. GRPO RL: NED, CDM, TEDS, field F1과 repetition·tag closure·JSON parse penalty를 task별 reward로 사용.

## 데이터와 평가

- 공개: OmniDocBench v1.5, OCRBench Text, UniMERNet, PubTabNet, TEDS_TEST, Nanonets-KIE, Handwritten-KIE.
- in-house: code document, real-world table, handwriting, 8개 언어 multilingual, seal, receipt KIE.
- 지표: Overall, text/read-order edit(낮을수록 좋음), formula CDM, table TEDS/TEDS-S, KIE score.
- 속도 표: 동일 hardware, single replica·single concurrency라고 설명하지만 PDF 본문 표에는 구체 GPU 모델이 적혀 있지 않다.

## 핵심 결과

- OmniDocBench v1.5 Overall `94.62`, text edit `0.040`, formula CDM `93.90`, table TEDS `93.96`, TEDS-S `96.39`, reading-order edit `0.044`.
- OCRBench Text `94.0`, UniMERNet `96.5`, PubTabNet `85.2`, TEDS_TEST `86.0`.
- KIE: Nanonets-KIE `93.7`, Handwritten-KIE `86.1`.
- in-house: code `84.7`, table `91.5`, handwriting `87.0`, multilingual `69.3`, seal `90.5`, receipt KIE `94.5`.
- single-concurrency throughput: image `0.67/s`, PDF `1.86 pages/s`; 비교 PaddleOCR-VL-1.5는 `0.39/s`, `1.22 pages/s`.
- 논문은 MTP가 평균 `5.2 tokens/step`을 내고 약 `50%` throughput improvement를 가져왔다고 보고한다. 이 값과 end-to-end page/s는 측정 범위가 다르므로 직접 곱하지 않는다.

## 한계와 재현 주의

- layout detector 오류가 downstream recognition과 reading order로 전파된다.
- cross-page dependency나 불규칙 multi-column은 region merge가 틀릴 수 있다.
- low-resolution, 심하게 왜곡된 문서, 복잡한 수식·표, 저자원 언어에서 성능이 저하될 수 있다.
- 생성 모델이므로 whitespace·line break·format이 조금 달라질 수 있고 strict schema를 완전히 보장하지 않는다.
- KIE는 prompt와 schema 명확성에 민감하다.
- in-house dataset 구성과 hardware 세부가 충분히 공개되지 않아 그 수치의 독립 재현은 제한된다.
- notebook은 MTP acceptance, region scheduling, reward metric을 toy로 구현하며 모델 결과 재현이 아니다.

## Diffusion OCR 블로그와의 관계

GLM-OCR은 블로그의 diffusion OCR 계열과 같은 병목, 즉 긴 OCR 출력의 token-by-token latency를 다루지만 해법은 다르다. 본 decoder를 diffusion으로 바꾸지 않고 MTP로 여러 미래 토큰을 제안하며, layout crop을 시스템 수준에서 병렬 처리한다. 따라서 diffusion의 any-order refinement·전역 재검토는 없지만 기존 AR serving stack과 더 직접적으로 결합된다. DODO/MinerU-Diffusion과 비교할 때 “모델 paradigm을 바꾸지 않는 가속 baseline”으로 읽는 것이 적절하다.

## 실습 학습 가이드

1. [01_foundations.ipynb](01_foundations.ipynb): MTP draft와 longest-prefix acceptance를 구현한다.
2. [02_practice.ipynb](02_practice.ipynb): layout region 병렬 scheduling과 reading-order merge를 시뮬레이션한다.
3. [03_advanced.ipynb](03_advanced.ipynb): NED·F1·구조 penalty를 task-aware reward로 결합한다.

## 다음 학습 경로

1. speculative decoding과 MTP의 exactness 조건을 학습한다.
2. PP-DocLayout-V3 오류가 end-to-end metric에 미치는 영향을 sensitivity analysis로 측정한다.
3. [HunyuanOCR-1.5](../hunyuanocr-1-5/README.md)의 diffusion draft-then-verify와 비교한다.
4. [DODO](../dodo/README.md)의 block diffusion decoder와 순차 step 정의를 맞춰 비교한다.
