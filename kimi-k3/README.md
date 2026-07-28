# Kimi K3: 개방형 3T급 멀티모달 에이전트 모델

작성일: 2026-07-20
갱신일: 2026-07-28

## 출처와 작업 범위

- 최초 원문: [Kimi K3: Open Frontier Intelligence](https://www.kimi.com/blog/kimi-k3)
- 이번 입력: [Google 공유 링크](https://share.google/RzthWmSD3pWMlObKI)
- 최종 확인 페이지: [moonshotai/Kimi-K3 모델 카드](https://huggingface.co/moonshotai/Kimi-K3)
- 라이선스: [Kimi K3 License](https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE)
- 원문 언어: 영어
- 확인일: 2026-07-20, 재확인 2026-07-28 (Asia/Seoul)
- 확인 기준: 공개 기술 블로그와 Hugging Face 공식 모델 카드
- 확인 revision: Hugging Face `main`의 `9f62e4e` 계열 공개 상태

공유 URL은 안전 리디렉션 제한 때문에 자동으로 열리지 않았으나, 링크
제목과 공식 검색 결과로 최종 대상이 `moonshotai/Kimi-K3`임을 확인했다.
2026-07-28 기준 모델 저장소에는 96개 safetensors shard를 포함한 약
1.56TB의 가중치와 사용자 정의 모델 코드가 공개돼 있다.

이 자료는 Kimi의 소개 글과 공식 모델 카드를 바탕으로 K3의 구조,
에이전트 활용, 평가 조건, 배포 방법과 라이선스를 학습용으로 재구성한다.
제조사가 보고한 수치와 사례는 독립 재현 결과가 아니므로 그대로 성능
보증으로 해석하지 않는다. [한국어 번역 자료](translation.ko.md)에는 두
원문의 구조를 구분해 번역 요약했다.

## 한눈에 보기

Kimi K3는 총 2.8조 파라미터 규모의 희소 Mixture of Experts(MoE)
모델이다. 모델 카드에는 토큰당 896개 전문가 중 16개를 선택하고,
공유 계층까지 포함해 약 1040억 개 파라미터가 활성화된다고 명시돼 있다.
100만 토큰 문맥과 네이티브 비전 입력을 지원하며 장기 코딩, 지식 작업,
시각적 제작과 도구 사용을 하나의 에이전트 모델에서 처리하는 것이
목표다.

핵심 구성은 다음과 같다.

- **Kimi Delta Attention(KDA)**: 긴 시퀀스에서 효율적으로 정보를 다루기 위한 어텐션 기반 구조
- **Attention Residuals(AttnRes)**: 모든 이전 표현을 균일하게 누적하지 않고 깊이 방향으로 필요한 표현을 선택적으로 회수
- **Stable LatentMoE**: 896개 전문가 중 16개를 활성화하는 고희소성 MoE
- **Gated MLA와 SiTU**: 어텐션 선택성과 활성화 제어를 개선하려는 구성
- **양자화 인지 학습**: SFT 단계부터 MXFP4 가중치와 MXFP8 활성화를 고려

## 기초 개념

### 파라미터 수와 활성 파라미터

총 파라미터 수는 모델이 보유한 모든 가중치의 규모다. 희소 MoE는 매 토큰마다 일부 전문가만 실행하므로 총 2.8조 파라미터가 매번 전부 계산되는 것은 아니다. `16 / 896 ≈ 1.79%`는 전문가 개수 기준 라우팅 비율이며, 공유 계층과 전문가별 크기를 모르면 정확한 활성 파라미터 수를 계산할 수 없다.

### 긴 문맥과 기억

100만 토큰 문맥은 긴 저장소나 문서 묶음을 한 요청에 넣을 가능성을 넓힌다. 하지만 최대 길이가 곧 모든 위치의 정보를 동일하게 잘 회수한다는 뜻은 아니다. 검색 정확도, 비용, 지연 시간, 캐시 전략과 에이전트의 문맥 관리가 함께 중요하다.

### 에이전트 하네스

모델을 감싸서 파일, 터미널, 브라우저 같은 도구를 제공하고 대화 이력을 관리하는 실행 환경이다. 원문의 벤치마크도 KimiCode, Claude Code, Codex 등 서로 다른 하네스를 사용한다. 따라서 점수는 모델 자체뿐 아니라 프롬프트, 도구, 반복 정책과 오류 복구 능력의 영향을 받는다.

## 핵심 요약

1. K3는 규모만 키운 밀집 모델이 아니라 희소 MoE, 긴 문맥, 멀티모달 입력과 에이전트 실행을 결합한다.
2. KDA와 AttnRes는 각각 시퀀스 길이와 네트워크 깊이 방향의 정보 흐름을 개선하려는 설계다.
3. 원문은 K2 대비 전체 스케일링 효율이 약 2.5배 개선됐다고 주장하며,
   모델 카드와 전체 기술 보고서가 공개됐지만 독립 재현은 별도 문제다.
4. 코딩 사례는 커널 최적화, GPU 컴파일러, 게임·CAD, 칩 설계, 계산과학까지 장시간 자율 실행을 강조한다.
5. 공개 벤치마크와 내부 평가가 섞여 있고 모델별 하네스 조건도 다르므로 순위표만으로 일반화하면 안 된다.
6. 사고 이력 보존에 민감하고, 모호한 상황에서 과도하게 주도적으로 행동할 수 있다는 한계가 명시됐다.

## 상세 정리

### 아키텍처와 학습

KDA는 긴 문맥에서 어텐션을 확장하기 위한 기반이고, AttnRes는 깊은 층을 통과할 때 필요한 과거 표현을 선택적으로 불러오는 구조로 설명된다. Stable LatentMoE는 매우 많은 전문가를 두되 토큰마다 소수만 사용한다. 이 정도의 희소성에서는 라우터가 특정 전문가에 몰리지 않게 하는 부하 균형이 중요하다.

원문은 라우터 점수의 분위수로 전문가 할당을 정하는 Quantile Balancing과, 어텐션 헤드를 독립적으로 최적화하는 Per-Head Muon을 소개한다. 대규모 전문가 병렬 학습에서는 정적 shape와 중요 경로의 host 동기화 제거로 처리량 저하를 줄였다고 한다.

### 공개 가중치와 모델 구성

모델 카드는 93개 계층, 69개 KDA 계층과 24개 Gated MLA 계층, 7168
attention hidden dimension, 96개 attention head, 16만 vocabulary,
MoonViT-V2 401M 비전 인코더를 명시한다. 가중치는 MXFP4, 활성값은
MXFP8을 사용하며 SFT부터 양자화 인지 학습을 적용했다.

Hugging Face 저장소의 pipeline tag는 `image-text-to-text`이고
`transformers`와 custom code를 사용한다. `trust_remote_code=True`는
다운로드한 저장소 코드를 현재 Python 환경에서 실행한다는 뜻이므로
production에서는 revision을 commit SHA로 고정하고 코드를 검토해야 한다.

### 추론과 배포

제조사는 64개 이상 가속기가 연결된 supernode 구성을 권장한다. 실제
Hugging Face 저장소 크기도 약 1.56TB이므로 공개 가중치가 개인용 GPU에서
쉽게 구동된다는 의미가 아니다. 공식 모델 카드는 vLLM, SGLang,
TokenSpeed를 권장하고 OpenAI 호환 로컬 endpoint 예제를 제공한다.

하드웨어가 없으면 `platform.kimi.ai`의 OpenAI/Anthropic 호환 API에서
`kimi-k3`를 선택하는 방식이 현실적이다. 로컬 deployment 명령은 엔진이
모델을 지원하고 충분한 GPU memory, 고속 interconnect, 저장 공간이
준비됐다는 전제다.

### 사고 이력 보존 API

K3는 thinking이 항상 켜져 있고 `reasoning_content`를 반환한다.
`reasoning_effort`는 `low`, `high`, `max`를 지원하며 기본값은 `max`다.
다중 턴과 tool call에서는 이전 assistant message의 `content`만 보내지
말고 API가 반환한 `reasoning_content`와 `tool_calls`까지 원형 그대로
다음 `messages`에 전달해야 한다. 이 계약을 놓치면 세션 일관성과 품질이
불안정할 수 있다.

### 코딩과 연구 사례

소개 글은 최대 24시간 GPU 커널 최적화, MLIR과 PTX 파이프라인을 갖춘 MiniTriton 개발, 48시간 칩 설계, 천체물리 수치 연구 자동화 사례를 제시한다. 흥미로운 증거지만 과제 정의, 전체 실행 로그, 실패 궤적과 비용이 모두 공개되기 전에는 사례 연구로 보는 편이 안전하다.

### 지식 작업과 멀티모달

Kimi Work에서는 수천 회 웹·터미널 조회를 포함한 산업 조사, 다중 서브에이전트 과학 분석, 대시보드와 위젯, 영상 편집 사례를 보여준다. 네이티브 멀티모달 모델이 텍스트·이미지·비디오를 같은 작업 루프에서 해석하고 수정하는 방향을 강조한다.

### 평가를 읽는 법

원문의 K3 결과는 최대 추론 노력, temperature 1.0, top-p 1.0 조건이다. 벤치마크에 따라 KimiCode, Claude Code, Codex 하네스가 다르며 일부 비교 모델은 fallback이나 다른 GPU 조건을 사용했다. 내부 벤치마크도 포함된다. 공정한 비교를 위해서는 동일 하네스, 동일 도구 예산, 동일 반복 횟수와 독립 재현 결과가 필요하다.

### 명시된 한계

- **사고 이력 민감성**: 보존된 thinking history가 누락되거나 세션 중 다른 모델에서 K3로 전환되면 품질이 불안정할 수 있다.
- **과도한 주도성**: 작은 문제나 모호한 의도에서 사용자 대신 예상 밖 결정을 내릴 수 있다.
- **사용 경험 격차**: 제조사도 최상위 폐쇄형 모델과 비교해 체감 품질 차이가 남아 있다고 밝힌다.

따라서 운영 환경에서는 명시적 권한 경계, 변경 전 확인 조건, 작업 예산, 중단 조건, 로그와 검토 단계를 시스템 프롬프트나 `AGENTS.md`에 넣는 것이 중요하다.

### Kimi K3 License 핵심

가중치와 코드는 표준 Apache/MIT가 아니라 별도의 **Kimi K3 License**로
공개됐다. 다음은 학습용 요약이며 법률 자문이 아니다.

- 저작권·허가 고지를 복사본과 실질적 부분에 포함해야 한다.
- 법률과 규정을 준수해야 한다.
- 제3자가 입력·파라미터·학습 데이터를 의미 있게 제어하는
  Model-as-a-Service 사업을 운영하고 계열사 합산 매출이 연속 12개월
  동안 미화 2천만 달러를 넘으면, 상업적 사용 전에 Moonshot AI와 별도
  계약이 필요하다.
- K3 또는 파생물을 사용하는 상용 제품·서비스가 월간 활성 사용자
  1억 명을 넘거나 월 매출 미화 2천만 달러를 넘으면 UI에 `Kimi K3`를
  눈에 띄게 표시해야 한다.
- 내부 사용과 Moonshot 공식 제품·인증 inference partner를 통한 사용은
  위 두 특별 조건의 예외다.
- 무보증 조건이 적용된다.

상업 배포 전에는 반드시 [라이선스 원문](https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE)과
조직의 법무 검토를 기준으로 판단한다.

## 용어 정리

| 용어 | 설명 |
| --- | --- |
| MoE | 여러 전문가 네트워크 중 일부만 선택해 계산하는 구조 |
| Router | 토큰을 처리할 전문가를 고르는 모듈 |
| KDA | Kimi가 제안한 긴 문맥용 Delta Attention 계열 구조 |
| AttnRes | 깊이 방향에서 이전 표현을 선택적으로 회수하는 잔차 구조 |
| MLA | 잠재 표현을 활용해 KV 관련 비용을 줄이는 어텐션 계열 기법 |
| Active parameters | 전체 가중치 중 한 토큰 처리에 실제 동원되는 파라미터 규모. K3 모델 카드는 104B로 기재 |
| SFT | 지시 데이터로 모델 행동을 조정하는 지도 미세조정 |
| QAT | 낮은 정밀도 추론을 학습 단계부터 고려하는 양자화 인지 학습 |
| Prefix cache | 반복되는 입력 접두부의 계산 결과를 재사용하는 캐시 |
| Agentic harness | 모델에 도구, 상태, 반복 실행과 평가 규칙을 제공하는 실행 틀 |

## 실습 학습 가이드

- [`01_foundations.ipynb`](01_foundations.ipynb): MoE 라우팅·활성
  파라미터와 1.56TB 가중치 저장 비용을 계산한다.
- [`02_practice.ipynb`](02_practice.ipynb): 모델 카드 benchmark를
  비교하고 조건 차이와 독립 검증 여부를 점검한다.
- [`03_advanced.ipynb`](03_advanced.ipynb): 에이전트 권한 정책과
  preserved thinking message 계약을 검증한다.

노트북은 Python 3 표준 라이브러리만으로 실행된다. Jupyter가 없다면 `python -m pip install jupyter` 후 `jupyter lab`을 실행한다.

## 다음 학습 경로

1. K3 전체 기술 보고서에서 학습 토큰, 데이터 구성과 아키텍처
   ablation을 확인한다.
2. KDA, AttnRes, Stable LatentMoE의 논문 또는 공식 구현을 읽고 기존 MLA·MoE와 비교한다.
3. 동일한 공개 과제와 동일 하네스로 여러 모델을 반복 평가해 평균·분산·비용을 기록한다.
4. 100만 토큰 문맥에서 위치별 검색, 장기 세션 압축, prefix cache 효율을 실험한다.
5. vLLM·SGLang deployment에서 64개 이상 가속기 구성의 처리량과
   interconnect 병목을 검증한다.

## 확인이 필요한 사항

- 전체 가중치와 기술 보고서는 공개됐지만 1.56TB 규모 때문에 독립
  재현과 local serving의 진입 비용이 매우 높다.
- 모델 카드 benchmark는 harness·tool·reasoning effort가 다른 결과를
  함께 비교하므로 동일 조건 재평가가 필요하다.
- 가격, API field, 모델 revision, inference engine 지원 상태는 바뀔 수
  있으므로 실제 사용 시 공식 페이지를 다시 확인해야 한다.
- 모델 카드에는 일반적인 dataset 구성, 안전성 평가와 환경 영향에 대한
  상세 정보가 제한적이므로 production risk review를 별도로 수행한다.
