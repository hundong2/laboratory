# HunyuanOCR-1.5: Making Lightweight OCR VLMs Faster and Better

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

- 원문: [arXiv:2607.04884](https://arxiv.org/abs/2607.04884)
- 사용 버전: v2, 2026-08-06 개정본
- 식별자: `arXiv:2607.04884`, DOI `10.48550/arXiv.2607.04884`
- 저자: Gengluo Li, Xingyu Wan, Shangpin Peng, Weinong Wang, Hao Feng, Yongkun Du, Binghong Wu, Zheng Ruan, Zhiqiong Lu, Liang Wu, Pengyuan Lyu, Huawen Shen, Zibin Lin, Shijing Hu, Jieneng Yang, Hongbing Wen, Guanghua Yu, Hong Liu, Bochao Wang, Can Ma, Han Hu, Chengquan Zhang, Yu Zhou
- 분류/출판 상태: arXiv preprint, cs.CV, 2026
- 라이선스: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). 번역·개작 문서도 동일 라이선스로 제공한다.
- 공식 코드: <https://github.com/Tencent-Hunyuan/HunyuanOCR>
- 공식 모델: <https://huggingface.co/tencent/HunyuanOCR>
- 확인일: 2026-09-05
- 확인 범위: v2 PDF 41쪽(본문, 참고문헌, supplementary) 전체를 추출하고 모든 페이지를 PNG 렌더링해 시각 확인했다. [번역 파일](<HunyuanOCR-1.5 - Making Lightweight OCR VLMs Faster and Better.번역.md>)은 핵심 문장 대조와 전 절 상세 해설을 제공하는 부분 번역이다.

## 한눈에 보기

HunyuanOCR-1.5는 약 1B급 end-to-end OCR VLM의 backbone을 크게 바꾸지 않고 두 축을 개선한다. **DFlash**는 90.7M block-diffusion draft model이 16개 candidate token을 병렬 제안하고 기존 AR target이 한 번에 검증해 원래 target distribution을 보존하는 speculative decoding이다. **Agentic Data Flow**는 model failure를 실행 가능한 데이터 요구로 바꾸고 material search·검증·pipeline 개발을 반복한다. 4K image, 128K context, long-tail data와 post-training 개선도 결합한다.

## 기초 개념

- **speculative decoding**: 작은 draft가 여러 token을 제안하고 target model이 한 번에 검증해 longest valid prefix만 받아들인다.
- **DFlash**: target hidden state를 조건으로 block-diffusion draft가 candidate block을 한 parallel pass에 만든다.
- **effective acceptance length**: verification step 한 번에 전진한 평균 token 수(보너스 token 포함).
- **FlexAttention block-diagonal mask**: 한 batch 안 여러 anchor의 draft block이 서로 보지 않게 격리한다.
- **Agentic Data Flow**: 약점을 requirement로 바꾸고 자료 탐색, 품질 검증, pipeline 구현, 평가 feedback을 agent가 보조하는 data engineering loop다.
- **seen-text faithfulness**: 언어적으로 말이 안 되더라도 이미지에 보이는 문자열을 그대로 보존하는 능력이다.

## 연구 질문과 기여

질문은 “검증된 lightweight end-to-end OCR backbone을 유지하면서 long structured output을 더 빠르게 만들고, 수작업 중심 데이터 구축의 long-tail 병목을 어떻게 체계적으로 줄일 것인가?”이다.

1. block-diffusion draft와 AR target verification을 결합한 DFlash를 OCR에 적용한다.
2. 4K native-resolution vision, 128K context, multi-image를 지원하도록 training recipe를 확장한다.
3. Agentic Data Flow로 ancient scripts, low-resource language, table/chart, multi-image QA hard case를 만든다.
4. CHAOS-Bench를 추가해 visual evidence와 language prior가 충돌할 때 seen-text recall을 측정한다.

## 방법과 학습

Backbone은 native-resolution Hunyuan-ViT, adaptive MLP connector, Hunyuan-0.5B language model(XD-RoPE)이다. 2K였던 최대 image resolution을 4K로 늘렸고 task-specific post-processing 없이 Markdown, HTML, LaTeX, chart description 등을 생성한다.

DFlash training에서 target model은 freeze한다. target hidden state를 한 번 계산·cache하고 sequence에서 `K=16` anchor를 뽑는다. 각 anchor의 mask block(`B=16`)을 한 batch로 연결하되 block-diagonal attention으로 격리한다. 5-layer, 약 90.7M draft를 target decoder 마지막 5 layer에서 초기화한다. 먼 future position의 loss를 `gamma=7.0` exponential decay로 낮춘다.

추론에서는 draft block을 target이 parallel verification하고 longest accepted prefix만 확정하므로 target의 output distribution을 유지한다. 낮은 concurrency에서 남는 compute를 draft에 사용해 memory-bandwidth-bound AR step 수를 줄이는 설계다.

## 데이터와 평가

평가는 capability tree로 구성한다.

- 기본: OmniDocBench v1.6, OCRBench, in-house Spotting.
- long-tail: MORE 149개 언어, Chronicles-OCR 7개 역사 문자 유형.
- 구조 요소: TableVerse-5K, ChartArena.
- cross-page/cross-lingual: DUDE, DoTA, MMTIT.
- 실용·신뢰성: in-house IE/VSE, 공개 CHAOS-Bench.
- 속도: OmniDocBench, batch 1, Transformers와 vLLM; 별도 concurrency 1-32 sweep.

Spotting·IE·Video Subtitle Extraction만 in-house이고 나머지는 공개 benchmark라고 논문은 구분한다.

## 핵심 결과

- Transformers: AR `34.850s`, `40.9 TPS`에서 DFlash `5.474s`, `245.7 TPS`, `6.37×`; effective acceptance `8.89`.
- vLLM: AR `3.032s`, `466.9 TPS`에서 `1.408s`, `1002.3 TPS`, `2.14×`; effective acceptance `8.36`.
- vLLM output 0-256 token은 `1.31×`, 2048+는 `2.30×`; table은 `2.39×`, formula `2.06×`, text `1.81×`다.
- concurrency 1-32에서 `2.14×`에서 `1.80×`로 줄어든다. GPU 포화 시 draft가 활용할 idle compute가 줄기 때문이다.
- OmniDocBench v1.6 Overall `94.74`, text edit `0.039`, formula CDM `94.50`, table TEDS/TEDS-S `93.67/94.71`, order edit `0.129`.
- Chronicles-OCR archaic/mature average `0.54/0.79`; MORE Overall `91.90`; TableVerse-5K TEDS/TEDS-S `79.37/86.05`; ChartArena 평균 EN/ZH `48.9/64.1`.
- CHAOS-Bench page-average recall `14.15`로 비교군 중 높지만 절대값이 매우 낮다. 저자들도 seen-text faithfulness가 여전히 어렵다고 명시한다.
- text-free image 1,000장 no-text accuracy `99.8%`(1.0은 `78.1%`).

## 한계와 재현 주의

- DFlash의 큰 speedup은 target output distribution을 보존하지만 전체 system output correctness를 새로 보장하는 것은 아니다.
- Transformers `6.37×`와 vLLM `2.14×` 차이는 baseline 최적화 정도가 다름을 보여준다. serving framework를 빼고 숫자만 비교하면 안 된다.
- 긴·규칙적 output일수록 acceptance가 길다. 짧은 출력은 prefill/fixed overhead가 지배한다.
- concurrency가 높아지면 speedup이 감소한다.
- 4K/128K와 multi-task recipe는 데이터·hardware 요구가 크고 공개 예정 표현과 실제 공개 상태를 시점별로 확인해야 한다.
- CHAOS `14.15`는 best-in-table이어도 낮은 recall이라 hallucination 문제가 해결됐다고 말할 수 없다.
- 일부 benchmark는 in-house여서 외부 재현 범위가 제한된다.
- notebook은 draft acceptance, weighted loss, 속도 표 산술을 toy로 재현하며 실제 model 성능 재현이 아니다.

## Diffusion OCR 블로그와의 관계

이 논문은 diffusion을 OCR decoder 전체에 쓰지 않고 **draft accelerator**로 사용한다. DODO/MinerU-Diffusion은 block diffusion이 최종 토큰을 직접 생성하지만, HunyuanOCR-1.5는 AR target이 candidate를 검증하므로 target distribution 보존이 강점이다. 블로그의 “결정적 OCR은 병렬 예측에 유리하다”는 직관을 활용하면서도, production-serving 호환성과 exact speculative verification을 우선한 hybrid 경로다.

## 실습 학습 가이드

1. [01_foundations.ipynb](01_foundations.ipynb): draft-then-verify와 longest-prefix acceptance를 구현한다.
2. [02_practice.ipynb](02_practice.ipynb): position-weighted DFlash loss와 block-diagonal visibility를 계산한다.
3. [03_advanced.ipynb](03_advanced.ipynb): 실제 보고 속도 표를 재계산하고 output length·concurrency 효과를 분석한다.

## 다음 학습 경로

1. speculative decoding의 rejection sampling/bonus token과 distribution-preserving 조건을 학습한다.
2. DFlash 원 논문에서 hidden-state-conditioned draft 학습을 확인한다.
3. [GLM-OCR](../glm-ocr/README.md)의 shared-head MTP와 별도 draft model의 차이를 비교한다.
4. [DODO](../dodo/README.md)·[MinerU-Diffusion](../mineru-diffusion/README.md)의 direct diffusion decoder와 품질·속도 측정 단위를 맞춘다.
