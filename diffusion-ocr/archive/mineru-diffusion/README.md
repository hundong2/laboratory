# MinerU-Diffusion: 문서 OCR을 역렌더링으로 보기

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

- 원문: [arXiv:2603.22458](https://arxiv.org/abs/2603.22458)
- 공식 제목: *MinerU-Diffusion: Rethinking Document OCR as Inverse Rendering via Diffusion Decoding*
- 사용 버전: v1, 2026-03-23 제출본
- 식별자: `arXiv:2603.22458`, DOI `10.48550/arXiv.2603.22458`
- 저자: Hejun Dong, Junbo Niu, Bin Wang, Weijun Zeng, Wentao Zhang, Conghui He
- 분류/출판 상태: arXiv preprint, cs.CV, 2026
- 라이선스: [arXiv non-exclusive license to distribute 1.0](https://arxiv.org/licenses/nonexclusive-distrib/1.0/). 이는 arXiv의 배포 권한이며 제3자의 전문 번역·개작 허락으로 보지 않았다.
- 공식 코드: <https://github.com/opendatalab/MinerU-Diffusion>
- 공식 모델: <https://huggingface.co/opendatalab/MinerU-Diffusion-V1-0320-2.5B>
- 확인일: 2026-09-05
- 확인 범위: v1 PDF 33쪽 전체(본문 15쪽, 참고문헌, 부록)를 텍스트 추출하고 전 페이지 PNG 렌더를 시각 확인했다. 저작권 경계 때문에 [번역 파일](MinerU-Diffusion%20-%20Rethinking%20Document%20OCR%20as%20Inverse%20Rendering%20via%20Diffusion%20Decoding.번역.md)은 짧은 원문 한 문장만 대조하고 나머지를 한국어 절별 해설로 제공한다.

## 한눈에 보기

MinerU-Diffusion은 OCR을 언어의 왼쪽-오른쪽 생성이 아니라 **2차원 문서를 구조화 토큰으로 되돌리는 역렌더링(inverse rendering)**으로 본다. 2.5B 모델은 블록 사이에는 거친 순서를 유지하고 블록 내부에서는 마스킹 토큰을 병렬 갱신한다. confidence threshold가 한 forward에서 확정할 토큰 수를 조절하며, broad data로 기초를 잡은 뒤 stochastic consistency가 낮은 hard case를 재학습하는 2단계 curriculum이 최적화를 안정화한다.

## 기초 개념

- **역렌더링**: 텍스트·표·수식을 배치해 만든 이미지에서 그 원래 구조화 표현을 추론하는 관점이다.
- **dLM/dVLM**: discrete diffusion Language/Vision-Language Model. `[MASK]`로 오염된 이산 토큰을 이미지 조건과 함께 복원한다.
- **block attention**: 같은 블록은 양방향, 이전 블록은 인과적으로 볼 수 있게 제한한다.
- **TPF/TPS**: Tokens Per Forward는 한 모델 호출당 확정 토큰 수, Tokens Per Second는 실제 시간 처리량이다. TPF가 커져도 한 forward가 비싸지면 TPS가 비례하지 않는다.
- **uncertainty curriculum**: 같은 입력을 여러 번 추론했을 때 결과 일치도가 낮은 샘플을 hard case로 간주한다.
- **GT Layout**: 정답 layout crop을 주는 oracle 조건이다. 실제 end-to-end 성능과 구분해야 한다.

## 연구 질문과 기여

질문은 “문서 토큰의 1차원 직렬화 순서를 생성의 본질로 보지 않고, 시각 증거 아래 병렬 복원하면 정확도·환각·지연을 함께 개선할 수 있는가?”이다.

1. 문서 OCR을 공간적으로 결합된 discrete random field의 역렌더링으로 재정의한다.
2. `O(L^2)` full attention 대신 block-wise diffusion과 KV cache를 결합한다.
3. 다양한 base data 다음 uncertainty 기반 hard sample을 학습하는 2단계 curriculum을 제안한다.
4. 의미를 깨뜨린 Semantic Shuffle로 언어 prior 의존도를 진단한다.

## 방법

출력 `y`를 text symbol, layout marker, table delimiter, math operator를 공유 vocabulary로 표현하고 `B`개 길이 `L'` 블록으로 나눈다.

```text
p_theta(y | x) = Π_b p_theta(y^(b) | y^(<b), x)
M_ij = 1  if b(i)=b(j) or b(j)<b(i), otherwise 0
```

현재 블록은 양방향 diffusion, 이전 블록은 고정 문맥이다. 따라서 long-range drift를 블록 안에 제한하고 prefix KV cache를 재사용한다. 기본 실험은 SDAR-1.7B-Chat-b32 decoder, block size 32, Qwen2-VL-7B에서 초기화한 vision encoder, 무작위 초기화 abstractor를 사용한다.

동적 decoding은 각 step에서 확신도 `τ`를 넘은 토큰을 함께 확정한다. 낮은 `τ`는 빠르지만 조기 오류가 늘고, 높은 `τ`는 보수적이지만 AR에 가까워진다.

학습은 다음 순서다.

1. Stage-0a/0b: LLaVA 계열 550K+739K로 modality alignment와 VQA 초기화.
2. Stage-1: Layout&OCR 6.9M, sequence 12,288, 9 epoch로 broad OCR 적응.
3. Stage-2: consistency가 낮아 전문가/AI-assisted로 다듬은 hard 630K, sequence 16,384, 4 epoch로 경계 사례를 보강한다.

hard sample의 consistency는 task metric `S`의 모든 추론 쌍 평균이며 `C(x)<τ`를 선택한다. layout은 PageIoU, formula는 CDM, table은 TEDS를 사용한다.

## 데이터와 평가

- 전체 meta training data: MinerU2.5 계열 약 7.5M, 주로 중국어·영어.
- OmniDocBench v1.5: 1,355쪽 hybrid matching, text edit·formula CDM·table TEDS/TEDS-S·reading order.
- table: CC-OCR, OCRBench v2.
- formula: UniMER-Test의 CPE/HWE/SCE/SPE.
- Semantic Shuffle: FOX 영어 문서 112개를 바탕으로 단어 순서를 비율별로 섞어 재렌더링.
- 속도: NVIDIA H200, batch 1 조건의 TPF/TPS. 서로 다른 하드웨어나 pipeline 전체 지연으로 일반화할 때 주의해야 한다.

OmniDocBench Overall은 다음과 같다.

```text
Overall = ((1 - TextEdit)*100 + FormulaCDM + TableTEDS) / 3
```

Reading Order와 TEDS-S는 Overall에 포함되지 않는다.

## 핵심 결과

- OmniDocBench에서 GT layout 없이 Overall `88.94`, text edit `0.061`, formula CDM `86.41`, table TEDS `86.50`, reading-order edit `0.059`다.
- GT layout에서는 Overall `93.37`, text edit `0.028`, formula `91.92`, table TEDS `91.00`이다. 두 조건의 큰 차이는 layout이 병목임을 보여준다.
- table은 CC-OCR `73.77/82.06` TEDS/TEDS-S, OCRBench v2 `81.18/88.66`이다.
- formula UniMER-Test는 CPE/HWE/SCE/SPE `91.6/91.6/92.0/96.8`이다.
- threshold `0.95`에서 93%+ 정확도와 `108.9 TPS`, MinerU2.5 기준 약 `52 TPS` 대비 약 `2.1×`; threshold `0.6`에서는 90% 초과 정확도와 `164.8 TPS`, 약 `3.2×`를 보고한다.
- 별도 decoding 표에서 dynamic `τ=0.97`은 `98.32 TPS`, Overall `93.34`로 static 6-step의 `91.56 TPS`, `88.31`보다 정확도와 처리량이 모두 높았다. static 32-step은 `21.86 TPS`, `93.02`였다.
- curriculum ablation의 GT layout Overall은 Stage 1 `92.89`, Stage 2 only `89.33`, Stage 1+2 `93.37`; GT layout이 없는 조건은 각각 `86.13`, `35.71`, `88.94`였다.

`τ=0.95` 주 실험과 `τ=0.97` decoding ablation은 서로 다른 표 조건이므로 하나의 설정으로 합치지 않았다.

## 한계와 재현 주의

- 저자도 GT layout 유무 격차를 layout prediction 병목으로 해석한다.
- 데이터가 중국어·영어 중심이며 저자들은 low-resource language 전용 평가를 하지 않았다.
- 논문은 Semantic Shuffle 곡선의 강한 robustness 차이를 보여주지만 본문에 모든 점의 숫자를 표로 제공하지 않는다. 정성적 추세를 임의 수치화하면 안 된다.
- `O(BL'^2)` 표기는 블록 수와 블록 길이에 대한 논문의 단순화다. 실제 vision token, batching, cache, kernel 비용을 포함한 wall-clock complexity와 같지 않다.
- 공식 코드·모델이 있어도 7.5M 데이터와 multi-stage 대규모 학습을 그대로 재현하려면 상당한 계산·데이터 권한이 필요하다.
- 본 notebook은 마스킹, attention mask, confidence scheduler, hard-case mining을 작은 문자열로 재현할 뿐 논문 성능을 재현하지 않는다.

## Diffusion OCR 블로그와의 관계

블로그의 “OCR은 언어 생성보다 역렌더링에 가깝다”는 관점을 제목과 문제정의 수준에서 직접 확장한 논문이다. DODO와 같은 block diffusion 계열이지만, MinerU-Diffusion은 confidence threshold를 연속적인 속도-정확도 조절기로 강조하고 uncertainty-driven curriculum 및 Semantic Shuffle 평가를 추가한다. DODO가 구조적 동기화 실패와 exact cache를 깊게 파고든다면, 이 논문은 학습 데이터 curriculum과 시각 증거 충실성까지 시스템 범위를 넓힌다.

## 실습 학습 가이드

1. [01_foundations.ipynb](01_foundations.ipynb): block attention mask와 이산 masking을 구현한다.
2. [02_practice.ipynb](02_practice.ipynb): confidence threshold에 따른 TPF·step·오류 trade-off를 실험한다.
3. [03_advanced.ipynb](03_advanced.ipynb): stochastic consistency로 hard case를 고르고 Overall metric을 검산한다.

## 다음 학습 경로

1. [DODO 분석](../dodo/README.md)과 block-causal exact cache ablation을 비교한다.
2. SDAR/Block Diffusion에서 block 간 factorization을 확인한다.
3. TEDS, CDM, PageIoU가 각각 어떤 구조 오류에 민감한지 실습한다.
4. Semantic Shuffle와 CHAOS-Bench를 함께 보고 언어 prior 의존도 평가의 차이를 비교한다.
