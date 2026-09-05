# Fast-dLLM v2: Efficient Block-Diffusion LLM

작성일: 2026-09-05

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [연구 질문과 기여](#연구-질문과-기여)
- [기초 개념](#기초-개념)
- [방법](#방법)
- [데이터와 평가](#데이터와-평가)
- [핵심 결과](#핵심-결과)
- [한계와 재현 주의점](#한계와-재현-주의점)
- [Trillion Labs 블로그와의 관계](#trillion-labs-블로그와의-관계)
- [실습 학습 가이드](#실습-학습-가이드)
- [용어 정리](#용어-정리)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 원문: [arXiv:2509.26328](https://arxiv.org/abs/2509.26328)
- 사용 버전: v1, 2025-09-30 제출
- 식별자: `arXiv:2509.26328`, DOI `10.48550/arXiv.2509.26328`
- 저자: Chengyue Wu, Hao Zhang, Shuchen Xue, Shizhe Diao, Yonggan Fu, Zhijian Liu, Pavlo Molchanov, Ping Luo, Song Han, Enze Xie
- 출판 상태: arXiv preprint
- 원문 언어: 영어
- 라이선스: [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)
- 접근일: 2026-09-05

공식 PDF 17쪽 전체를 내려받아 90 DPI PNG로 렌더링하고 모든 페이지를 접촉 시트로 시각 확인했다. 모든 페이지에서 본문, 수식, 표, 그림이 렌더링되었고 텍스트 추출도 17/17쪽에서 비어 있지 않았다. 확인한 PDF의 SHA-256은 `9e3dcb349e0269fee8ac8c525131284a6408e506900c69940bb898f41274d49f`다.

라이선스의 NoDerivatives 조건 때문에 원문 전문의 번역 재배포는 하지 않는다. [제한된 문장 대조 번역과 섹션별 상세 해설](Fast-dLLM%20v2-%20Efficient%20Block-Diffusion%20LLM.번역.md)을 제공한다.

## 한눈에 보기

Fast-dLLM v2는 이미 학습된 자기회귀(AR) Qwen2.5-Instruct 모델을 블록 확산 언어 모델로 바꾸는 사후학습 방법이다. 이전 블록은 왼쪽에서 오른쪽으로 확정하되, 현재 블록 안의 여러 `[MASK]` 토큰은 양방향 문맥을 사용해 병렬로 복원한다. 이 구조는 블록 사이에서는 정확한 KV cache를 유지하고 블록 안에서는 병렬성을 확보하려는 절충이다.

핵심은 모델을 처음부터 다시 학습하지 않고 약 10억 토큰의 미세조정으로 변환했다는 점, 상보 마스크로 학습 신호를 빠짐없이 주었다는 점, 블록 캐시와 sub-block DualCache를 계층적으로 결합했다는 점이다.

## 연구 질문과 기여

연구 질문은 세 가지다.

1. 완전 양방향 dLLM보다 AR 모델의 표현을 더 잘 보존하면서 병렬 생성 능력을 넣을 수 있는가?
2. 블록 간 KV cache와 블록 내 병렬 복원을 함께 써 실제 하드웨어 처리량을 높일 수 있는가?
3. 수백억~수천억 토큰 재학습 대신 약 10억 토큰의 사후학습으로 1.5B·7B 모델을 변환할 수 있는가?

논문의 답은 블록 단위 인과 구조, 상보 마스크, 한 칸 이동한 레이블, 계층 캐시를 하나의 학습·추론 레시피로 묶는 것이다. 저자들은 Dream의 약 580B 토큰과 비교해 학습 데이터가 약 500배 적다고 주장하며, 최대 약 2.5배의 AR 대비 가속을 보고한다.

## 기초 개념

### AR과 masked diffusion

AR 모델은 $p(x_i\mid x_{<i})$를 순서대로 계산한다. 품질과 가변 길이 생성은 강하지만 토큰마다 직렬 단계가 필요하다. 마스크 확산 모델은 여러 위치를 가린 뒤 반복적으로 복원한다. 같은 단계에 여러 토큰을 갱신할 수 있지만 전체 양방향 attention 때문에 일반적인 AR KV cache를 그대로 쓰기 어렵다.

### block diffusion

길이 $L$의 시퀀스를 크기 $D$인 $B=L/D$개 블록으로 나눈다. 앞 블록은 확정된 clean prefix이고, 현재 블록만 반복 복원한다. 따라서 블록 사이에는 인과성이, 블록 안에는 양방향 문맥이 적용된다.

### complementary mask

무작위 이진 마스크 $m$과 그 여집합 $\bar m=1-m$을 같은 배치에 둔다. 첫 view에서 보였던 토큰은 둘째 view에서 가려지고 그 반대도 성립하므로 모든 위치가 예측 대상으로 한 번씩 포함된다.

## 방법

### 1. 블록 정렬과 패킹

각 샘플 길이를 블록 크기의 배수가 되도록 `[MASK]`로 오른쪽 padding한다. padding 위치는 loss에서 제외한다. 이 절차가 없으면 패킹 과정에서 한 샘플의 `<EOS>` 뒤에 다음 샘플의 `<BOS>`가 같은 양방향 블록에 들어가 데이터 누수가 생길 수 있다.

### 2. AR 표현을 보존하는 token shift

가려진 위치 $i$의 정답을 같은 위치가 아니라 $i-1$의 hidden state로 예측한다. 이는 기존 next-token prediction의 시간 정렬을 보존하면서 현재 블록의 보이는 토큰도 문맥으로 활용하려는 설계다.

### 3. 블록 손실과 attention

손실은 가려진 토큰에만 적용한다.

$$
\mathcal{L}_{\text{block}}=-\mathbb{E}_{x,m}\sum_{i=1}^{L}
\mathbf{1}[x_i=\texttt{[MASK]}]\log p_\theta(x_i\mid x_{<i},x_{\text{block}(i)}).
$$

앞 블록은 인과적으로, 현재 블록은 양방향으로 보게 하는 구조화 attention mask를 사용한다. 학습에서는 noisy view와 clean view를 이어 붙인 $2L\times2L$ 마스크를 flex-attention으로 구현한다.

### 4. 계층 캐시와 병렬 복원

- block-level cache: 완료된 앞 블록의 KV를 읽기 전용으로 재사용한다.
- sub-block DualCache: 현재 블록에서 이미 확정된 prefix와 아직 마스크인 suffix의 KV를 재사용한다.
- confidence-aware decoding: 예측 확률이 임계값을 넘는 위치를 한 번에 확정하고 불확실한 위치만 다음 반복에 남긴다.
- batch padding: 목표 길이가 다른 요청도 블록 크기의 배수가 되게 맞춰 같은 블록 스케줄로 실행한다.

## 데이터와 평가

- 기반 모델: Qwen2.5-Instruct 1.5B, 7B
- 학습 데이터: LLaMA-Nemotron post-training dataset, 약 10억 토큰
- 1.5B: learning rate $2\times10^{-5}$, 6,000 step, 약 8시간
- 7B: learning rate $1\times10^{-5}$, 2,500 step, 약 12시간
- 공통: batch 256, NVIDIA A100 64장, block size 32, 기본 sub-block size 8
- 품질: HumanEval/MBPP(EvalPlus), GSM8K, MATH, IFEval, MMLU, GPQA(LM-Eval)
- 속도: A100·H100에서 token/s와 batch-size scaling 측정

이는 공개 체크포인트를 작은 환경에서 재현하는 실험이 아니다. 특히 64×A100 학습, custom flex-attention, 캐시 커널과 정확한 평가 harness가 필요하다.

## 핵심 결과

- 1.5B 모델 평균 점수는 45.0으로 같은 데이터·step의 Qwen2.5-1.5B-Nemo-FT 44.3보다 높았다.
- 7B 모델 평균 점수는 60.3으로 Qwen2.5-7B-Nemo-FT 59.6과 Dream 57.6을 상회했다.
- GSM8K 임계값 sweep에서 threshold 0.9는 처리량을 39.1에서 101.7 token/s로 높여 2.6배가 되었고 정확도 저하는 작았다고 보고한다. 초록·결론의 대표 표현은 “최대 2.5배”이므로 서로 다른 측정 맥락과 반올림을 섞지 않아야 한다.
- batch 64에서 AR 기준 처리량 이점은 A100 최대 1.5배, H100 최대 1.8배로 보고되었다.
- `naive token shift → +pad → +pad+CM` 평균은 41.3 → 42.2 → 45.0이었다.
- sub-block size 8이 종합 절충점이었고, 큰 sub-block은 직렬 step을 줄이는 대신 일부 정확도를 낮췄다.

## 한계와 재현 주의점

1. v1 한 편의 기술 보고이며, 논문 자체의 “code and model will be released” 상태를 기준으로 작성되었다. 이후 공개 상태나 구현 차이는 별도 확인이 필요하다.
2. 가속은 하드웨어·batch·메모리 대역폭·커널 구현에 민감하다. 작은 batch에서는 sub-block cache 이득이 거의 없었다.
3. 변환에는 사후학습이 필요하며 speculative decoding처럼 원 target 분포가 수학적으로 동일하다는 보장은 아니다.
4. confidence threshold를 낮추면 더 빠르지만 잘못 확정한 토큰을 되돌리기 어려워 품질과 속도 사이의 직접적인 trade-off가 생긴다.
5. block/sub-block 크기를 학습 설정과 다르게 사용하면 성능이 저하된다.
6. 공개 benchmark 평균은 실제 OCR의 긴 표, 수식, 다국어 layout 품질을 직접 증명하지 않는다. 이 논문은 언어 모델 실험이다.

## Trillion Labs 블로그와의 관계

[Diffusion으로 OCR 디코딩 가속하기](https://blog.trillionlabs.co/posts/diffusion-ocr/)는 AR OCR 모델을 block diffusion/self-speculation 방향으로 전환하는 배경에서 이 논문을 “AR 모델 기반의 효율적 변환 레시피”로 참조한다.

관계는 직접적인 OCR benchmark 재현이 아니라 방법론적이다.

- 공통점: 기존 AR checkpoint 활용, 블록 내부 병렬 예측, 캐시와 병렬 decoding의 결합.
- 차이점: Fast-dLLM v2 실험은 주로 언어·추론 benchmark이고, 블로그는 문서 crop과 OmniDocBench에서 pages/s·tok/s를 측정한다.
- 해석 주의: 블로그의 self-spec 3.85배 decode-only / 1.85배 end-to-end는 vision encode와 prefill 고정비가 포함되느냐에 따라 달라진다. Fast-dLLM v2의 token/s 수치와 직접 비교할 수 없다.

## 실습 학습 가이드

- [01_foundations.ipynb](01_foundations.ipynb): block padding, 무작위 마스크와 상보 마스크가 모든 토큰을 감독하는지 확인한다.
- [02_practice.ipynb](02_practice.ipynb): confidence-aware parallel unmasking을 확률표로 모사하고 임계값에 따른 step 수와 오류 위험을 본다.
- [03_advanced.ipynb](03_advanced.ipynb): block/sub-block/cache의 toy cost model을 sweep해 처리량-품질 절충을 분석한다.

모든 실습은 Python 표준 라이브러리만 사용하며 논문의 모델·속도·정확도를 재현한다고 주장하지 않는다.

## 용어 정리

| 용어 | 의미 |
| --- | --- |
| AR | 토큰을 왼쪽에서 오른쪽으로 하나씩 생성하는 자기회귀 방식 |
| dLLM | 토큰을 마스킹하고 반복 복원하는 확산 언어 모델 |
| block diffusion | 블록 사이는 AR, 블록 안은 diffusion으로 생성하는 혼합 방식 |
| KV cache | 이미 계산한 attention key/value를 재사용하는 캐시 |
| DualCache | 현재 블록의 prefix와 suffix 표현을 함께 재사용하는 근사 캐시 |
| complementary mask | 마스크와 여집합 view를 함께 써 모든 위치를 감독하는 방법 |
| confidence threshold | 토큰을 확정할 최소 예측 신뢰도 |

## 다음 학습 경로

1. AR attention mask와 양방향 attention mask를 행렬로 직접 그린다.
2. [Block Diffusion](https://arxiv.org/abs/2503.09573)에서 블록 확률 모델의 이론을 읽는다.
3. [Fast Inference from Transformers via Speculative Decoding](../speculative-decoding/README.md)과 “분포 보존” 여부를 비교한다.
4. OCR 적용에서는 [OmniDocBench](../omnidocbench/README.md)의 metric과 [MinerU2.5-Pro](../mineru2-5-pro/README.md)의 최신 v1.6 protocol을 구분한다.
