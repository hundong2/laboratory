# Large Language Diffusion Models (LLaDA) 학습 노트

작성일: 2026-09-05

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [연구 질문과 기여](#연구-질문과-기여)
- [기초 개념](#기초-개념)
- [방법](#방법)
- [데이터와 평가](#데이터와-평가)
- [주요 결과](#주요-결과)
- [한계와 재현 주의](#한계와-재현-주의)
- [Trillion Labs OCR 접근과의 관계](#trillion-labs-ocr-접근과의-관계)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 원문: [arXiv:2502.09992](https://arxiv.org/abs/2502.09992), DOI `10.48550/arXiv.2502.09992`
- 확인 버전: v3, 2025-10-18 개정본(최초 제출 2025-02-14)
- 저자: Shen Nie, Fengqi Zhu, Zebin You, Xiaolu Zhang, Jingyang Ou, Jun Hu, Jun Zhou, Yankai Lin, Ji-Rong Wen, Chongxuan Li
- 출판 상태: arXiv preprint. 확인한 페이지에는 별도 학회 채택 정보가 없다.
- 라이선스: [arXiv non-exclusive distribution license 1.0](https://arxiv.org/licenses/nonexclusive-distrib/1.0/). 이는 arXiv 배포 허가이지 일반적인 번역·재배포용 오픈 라이선스가 아니다.
- 접근일: 2026-09-05
- 실제 확인 범위: 공식 초록·메타데이터, v3 PDF 33쪽 전체, 본문과 부록 A-C. PDF 전 페이지를 PNG로 렌더링해 다단 편집, 표·그림, 부록 경계를 시각 확인했다.
- 번역·해설: [Large Language Diffusion Models.번역.md](./Large%20Language%20Diffusion%20Models.번역.md). 저작권 경계를 지키기 위해 짧은 원문 대조 1개와 절별 상세 한국어 해설로 구성했다.

## 한눈에 보기

LLaDA(Large Language Diffusion with mAsking)는 다음 토큰을 왼쪽부터 하나씩 생성하는 ARM(autoregressive model) 대신, 문장 곳곳을 마스크한 뒤 Transformer가 모든 마스크를 동시에 복원하도록 학습한 1B/8B 언어 모델이다. 8B 모델을 2.3T 토큰으로 처음부터 사전학습하고 4.5M prompt-response 쌍으로 SFT했다. 논문의 핵심 메시지는 “대규모 언어 능력이 반드시 자기회귀 인수분해에만 의존하지는 않는다”는 실증이다.

다만 LLaDA의 기본 전역 양방향 샘플링은 완료된 응답 prefix의 KV cache를 자연스럽게 재사용하지 못하며, 매 step 여러 위치를 다시 계산한다. 따라서 논문은 비자기회귀 가능성을 입증하는 기반 연구이고, Trillion Labs 블로그의 OCR 가속은 여기에 block diffusion과 AR 검증을 더해 실제 처리량 문제를 푸는 후속 설계로 이해하면 된다.

## 연구 질문과 기여

### 연구 질문

1. in-context learning, instruction following, scaling 같은 핵심 LLM 능력이 자기회귀 구조 없이도 나타나는가?
2. 무작위 마스킹 확산의 학습 목표를 likelihood와 연결된 원리 있는 생성 모델로 만들 수 있는가?
3. 양방향 조건화가 reversal curse처럼 왼쪽-오른쪽 인수분해가 불리한 문제에 도움이 되는가?

### 핵심 기여

- 마스크 비율 `t ~ Uniform(0, 1)`의 masked discrete diffusion을 8B 규모까지 처음부터 확장했다.
- masked-token cross entropy에 `1/t` 가중치를 두어 모델 NLL의 상계와 연결되는 목적식을 사용했다.
- 동일 데이터로 학습한 자체 ARM baseline과 비교해 약 `10^20-10^23` FLOPs 범위에서 downstream scaling 경향이 경쟁적임을 보였다.
- 8B base가 15개 zero/few-shot 과제에서 LLaMA2 7B보다 대체로 우수하고 LLaMA3 8B와 경쟁적이라고 보고했다.
- 496개 중국 고시 문장 쌍의 역방향 완성에서 LLaDA-8B Instruct 45.6, GPT-4o 34.3을 보고해 reversal curse 완화를 보였다.

## 기초 개념

### ARM과 masked diffusion

- ARM은 `p(x)=prod_i p(x_i | x_<i)`로 분해한다. 학습은 병렬화할 수 있지만 생성은 왼쪽에서 오른쪽으로 순차적이다.
- LLaDA는 각 토큰을 독립적으로 확률 `t`로 `[MASK]`로 바꾸고, 남은 토큰 전체를 보며 원래 토큰을 예측한다.
- 생성 시에는 완전 마스크된 길이 `L`의 응답에서 출발해, 여러 위치를 예측하고 저신뢰 토큰을 다시 마스크하며 반복한다.

### 왜 BERT와 다른가

BERT의 고정 15% 마스킹은 표현 학습용이다. LLaDA는 0부터 1까지 모든 마스크 비율을 표본화하고 시간 가중치를 적용해 완전 마스크 상태에서 데이터 상태로 돌아가는 생성 과정을 학습한다. 따라서 “빈칸 채우기 모델”이라는 표면은 비슷하지만, 학습 목표와 샘플링 정의가 다르다.

## 방법

### 목적식

논문의 핵심 목적식을 간략화하면 다음과 같다.

```text
L(theta) = - E[t, x0, xt] [ (1/t) * sum_i 1[xt_i = MASK]
                             * log p_theta(x0_i | xt) ]
```

`t`는 마스크 확률, `x0`는 원문, `xt`는 손상된 문장이다. 마스크 위치에만 손실을 주고 `1/t`로 가중한다. 논문은 이 값이 모델 분포의 negative log-likelihood 상계임을 사용한다. `t`가 매우 작을 때 가중치가 커지므로 분산 관리가 중요하며, 뒤의 Block Diffusion 논문이 이 문제를 더 직접 분석한다.

### 사전학습과 SFT

- 모델: causal mask 없는 Transformer mask predictor, 1B와 8B.
- 사전학습: 2.3T 토큰, 길이 4096, 0.13M H800 GPU-hours. 온라인 일반 문서에 code, math, multilingual 데이터를 섞었다.
- 가변 길이 노출: 사전학습 데이터 1%는 길이를 1-4096에서 무작위 선택했다.
- SFT: 4.5M 쌍, prompt는 깨끗하게 두고 response만 마스킹한다. 3 epochs.
- 생성 길이: 초기 `[MASK]` 수로 지정하고, 생성된 EOS 뒤를 버린다.

### 샘플링

기본 low-confidence remasking은 각 step에서 모든 마스크를 예측한 뒤 낮은 확신의 일부를 다시 마스크한다. 논문은 random, autoregressive, block diffusion 샘플링도 분석하지만 본문 결과에는 순수 diffusion을 기본으로 사용했다. step 수와 품질·비용이 직접 trade-off한다.

## 데이터와 평가

데이터 혼합 비율과 원문 corpus의 완전한 목록은 공개 정보만으로 독립 재구성하기 어렵다. 저자들은 기존 LLM 데이터 프로토콜을 따랐고 품질 필터링과 축소 ARM으로 혼합 비율을 정했다고 설명한다.

평가는 다음 범주를 포함한다.

- 일반·상식: MMLU, BBH, ARC-C, HellaSwag, TruthfulQA, WinoGrande, PIQA
- 수학·과학: GSM8K, MATH, GPQA
- 코드: HumanEval, HumanEval-FIM, MBPP
- 중국어: CMMLU, C-Eval
- 역방향 추론: 496개 중국 고시 문장 쌍의 forward/reversal completion

shot 수와 평가 구현은 과제별로 다르다. 표의 모델 간 사전학습 토큰 수도 LLaDA 2.3T, LLaMA3 8B 15T처럼 크게 달라 단순 우열로 읽으면 안 된다.

## 주요 결과

- base 모델: LLaDA 8B는 MMLU 65.9, GSM8K 70.3, MATH 31.4, HumanEval 35.4, CMMLU 69.9를 보고했다.
- 같은 평가 구현의 LLaMA3 8B base와 비교하면 MMLU는 65.9 대 65.4, HumanEval은 35.4 대 34.8로 비슷하지만 BBH는 49.7 대 62.1, PIQA는 73.6 대 80.6으로 뒤진다. 반대로 GSM8K는 70.3 대 48.7, MATH는 31.4 대 16.0으로 높다.
- SFT 모델: LLaDA-8B Instruct는 ARC-C 88.5, HumanEval 49.4 등을 보고했지만, 비교 모델 다수는 RL alignment까지 사용해 post-training 조건이 동일하지 않다.
- 역방향 고시 완성: LLaDA는 forward 51.8/reversal 45.6으로 격차가 작았다. GPT-4o는 82.7/34.3, Qwen2.5-7B Instruct는 75.9/38.0이었다.

이 결과는 “모든 과제에서 LLaDA가 더 좋다”가 아니라, masked diffusion도 대규모 일반 능력과 일부 독특한 양방향 장점을 획득할 수 있다는 증거다.

## 한계와 재현 주의

- 생성 길이는 초기 하이퍼파라미터이며 EOS로 잘라도 불필요한 계산이 생길 수 있다.
- 전역 양방향 attention은 표준 AR KV caching과 맞지 않아 wall-clock 가속이 자동으로 보장되지 않는다.
- 저자 자체 ARM baseline 외에는 데이터·토큰 수·post-training이 통제되지 않은 비교가 많다.
- 8B 실험과 SFT 실험은 각각 한 번 실행했고 별도 하이퍼파라미터 탐색을 하지 않았다고 명시한다. 오차막대가 없다.
- 전체 데이터 구성과 필터가 완전 공개되지 않아 데이터 오염·혼합 차이를 독립적으로 배제하기 어렵다.
- RL alignment, 적응형 길이, 더 효율적인 sampler, 멀티모달, agent 사용은 미탐색 영역이다.
- 이 폴더의 notebook은 핵심 원리를 작은 어휘로 보여주는 toy reproduction이다. 8B 모델 결과나 논문 벤치마크를 재현하지 않는다.

## Trillion Labs OCR 접근과의 관계

[Trillion Labs 글](https://blog.trillionlabs.co/posts/diffusion-ocr/)은 LLaDA를 masked discrete diffusion의 개념적 출발점으로 인용한다.

| 축 | LLaDA | Trillion Labs OCR |
|---|---|---|
| 문제 | 범용 언어 생성 패러다임 검증 | 문서 OCR의 단건 디코딩 가속 |
| 입력 | 텍스트 prompt | 이미지·prompt·직렬화된 OCR 출력 |
| 범위 | 응답 전체 masked diffusion | 크기 32의 block diffusion |
| 학습 | diffusion 중심, SFT response masking | 같은 backbone에 clean AR loss와 corrupted diffusion loss 동시 적용 |
| 추론 | 반복 denoise/remask | one-shot diffusion draft + 같은 모델의 AR verify |
| 정확성 기준 | diffusion 모델 분포·benchmark | greedy AR 출력과 byte-level 동일한 longest-prefix commit |
| 캐시 | 기본 전역 diffusion은 KV cache 비호환 | 완료 prefix의 AR KV cache 유지 |

OCR은 답의 많은 부분이 이미지에 이미 고정되어 있어 자유 생성보다 draft 일치 길이가 길 수 있다. 블로그는 평균 약 19개 토큰/라운드의 연속 일치, 전체 forward 기준 9.6 tokens/forward를 보고한다. 즉 LLaDA의 병렬 마스크 복원을 그대로 최종 출력으로 쓰지 않고, 빠른 제안기로 사용해 오류를 속도 손실로 바꾼다.

## 용어 정리

- `mask predictor`: 손상된 전체 문맥에서 각 마스크의 원 token을 예측하는 Transformer.
- `remasking`: 한 번 예측한 위치 중 저신뢰 항목을 다시 마스크해 다음 step에서 고치는 절차.
- `sampling step`: 한 번의 병렬 예측·선택·재마스킹 전이. token 수와 동일하지 않다.
- `reversal curse`: 정방향 사실을 배웠어도 역방향 질의에 일반화하지 못하는 현상.
- `likelihood bound`: 직접 NLL과 같다고 보장되는 값이 아니라 NLL을 위에서 제한하는 목적식.

## 실습 학습 가이드

1. [01_foundations.ipynb](./01_foundations.ipynb): 마스크 확률 `t`, 손상 과정, `1/t` 가중 손실을 작은 어휘로 관찰한다.
2. [02_practice.ipynb](./02_practice.ipynb): low-confidence remasking sampler를 확률표로 구현하고 step 수를 비교한다.
3. [03_advanced.ipynb](./03_advanced.ipynb): 마스크율에 따른 Monte Carlo 분산과 AR-style 순차 복원의 차이를 실험한다.

모든 notebook은 Python 표준 라이브러리만 사용하고 고정 seed와 assertion을 포함한다.

## 다음 학습 경로

1. 번역·해설 파일에서 목적식과 결과 해석의 경계를 확인한다.
2. Block Diffusion 아카이브로 이동해 KV cache와 학습 분산 문제의 후속 해법을 본다.
3. Nemotron-Labs-Diffusion과 Fast-dVLM을 읽어 joint AR-diffusion 및 self-speculation으로 이어지는 흐름을 비교한다.
4. 실제 모델 재현 시 공식 code/model card의 tokenizer, checkpoint, sampler 설정을 고정하고 품질뿐 아니라 NFE와 wall-clock을 함께 측정한다.
