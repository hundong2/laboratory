# Kimi K3 원문 한국어 번역 요약

작성일: 2026-07-20
갱신일: 2026-07-28

원문:

- [Kimi K3: Open Frontier Intelligence](https://www.kimi.com/blog/kimi-k3)
- [moonshotai/Kimi-K3 Hugging Face 모델 카드](https://huggingface.co/moonshotai/Kimi-K3)
- [Kimi K3 License](https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE)

사용자 입력: [Google 공유 링크](https://share.google/RzthWmSD3pWMlObKI)

확인일: 2026-07-20, 재확인 2026-07-28

원문 언어: 영어

> 저작권을 존중하기 위해 원문 전체를 복제하지 않고, 각 원문의 제목
> 흐름과 핵심 주장·수치·주의사항을 보존한 한국어 번역 요약을 제공한다.
> 라이선스 설명은 법률 자문이 아니며 반드시 원문을 확인해야 한다.

## Hugging Face 모델 카드 한국어 번역 요약

### 1. 모델 소개

Kimi K3는 공개 가중치를 제공하는 네이티브 멀티모달 에이전트 모델이며
Moonshot AI가 현재까지 공개한 모델 중 가장 강력한 모델로 소개된다.
Kimi Delta Attention(KDA)과 Attention Residuals(AttnRes)를 기반으로 한
2.8조 파라미터 모델이고, 네이티브 비전과 100만 토큰 문맥 창을 갖는다.
장시간 코딩, 지식 작업과 추론에서 frontier 수준의 지능을 목표로 한다.

주요 특징:

- **새 아키텍처**: KDA, AttnRes, Stable LatentMoE를 결합한다. 896개
  전문가 중 16개를 활성화하며 K2 대비 전체 scaling efficiency가 약
  2.5배 개선됐다고 제작사는 설명한다.
- **장시간 코딩**: 사람의 개입을 줄인 긴 엔지니어링 세션, 대규모
  저장소 탐색, terminal tool orchestration을 목표로 한다.
- **에이전트형 지식 작업**: 심층 조사, interactive visualization,
  widget·dashboard, motion design과 video editing을 수행한다.
- **네이티브 멀티모달과 긴 문맥**: 텍스트·이미지를 같은 모델에서
  이해하고 1,048,576 token context를 지원한다.
- **전체 가중치 공개**: Kimi K3 License 아래 연구·배포·후속 개발용
  전체 가중치를 공개한다.

### 2. 모델 요약

| 항목 | 모델 카드 값 |
| --- | --- |
| 아키텍처 | Mixture-of-Experts |
| 전체/활성 파라미터 | 2.8T / 104B |
| 계층 | 93개, 이 중 dense layer 1개 |
| attention 구성 | 69 KDA + 24 Gated MLA |
| attention hidden dimension/head | 7168 / 96 |
| latent MoE dimension | 3584 |
| 전문가 | 896개 중 token당 16개 선택, shared expert 2개 |
| vocabulary | 160K |
| 최대 문맥 | 1,048,576 token |
| 비전 인코더 | MoonViT-V2, 401M parameters |
| 양자화 | MXFP4 weights / MXFP8 activations |
| modality | Text, Image |

Hugging Face 저장소는 2026-07-28 확인 시 약 1.56TB이며 96개
safetensors shard와 모델·processor custom code를 제공한다.

### 3. 평가 결과

모델 카드는 reasoning·knowledge, coding, agentic, vision benchmark를
비교한다. 대표적으로 Kimi K3(max)는 GPQA Diamond 93.5,
Terminal-Bench 2.1 88.3, BrowseComp 91.2, MCPMark-Verified 94.5,
OmniDocBench 91.1을 보고한다. 이 수치는 제작사 모델 카드의 보고값이며
성능 보증이나 동일 조건 독립 재현 결과가 아니다.

모든 K3 결과는 `reasoning_effort=max`, temperature 1.0을 사용한다.
GPQA·HLE와 도구 없는 vision benchmark는 top-p 0.95, agentic task는
top-p 1.0이다. benchmark에 따라 Kimi Code, Codex, Claude Code 등
harness가 다르고 일부 표는 tool augmentation 전후 점수를 함께 쓴다.
따라서 단순 순위보다 각주, harness, tool budget, 반복 횟수를 함께
읽어야 한다.

### 4. 네이티브 MXFP4 양자화

K3는 SFT 단계부터 quantization-aware training을 적용한다. 가중치에는
MXFP4, 활성값에는 MXFP8을 사용해 여러 하드웨어에서 낮은 정밀도로
추론할 수 있도록 설계했다.

### 5. 배포

Moonshot 공식 API에서는 `platform.kimi.ai`에서 `kimi-k3`를 선택할 수
있고 OpenAI/Anthropic 호환 API를 제공한다. 자체 호스팅용 권장 추론
엔진은 vLLM, SGLang, TokenSpeed다.

Hugging Face가 제시하는 최소 형태:

```bash
pip install vllm
vllm serve "moonshotai/Kimi-K3"
```

```bash
pip install sglang
python -m sglang.launch_server \
  --model-path "moonshotai/Kimi-K3" \
  --host 0.0.0.0 \
  --port 30000
```

이 명령이 consumer GPU 한 대에서 실행 가능하다는 뜻은 아니다. 저장소가
약 1.56TB이고 제작사는 64개 이상 가속기의 supernode를 권장한다.
`trust_remote_code=True`로 Transformers custom code를 실행할 때는
revision을 SHA로 고정하고 내려받은 코드를 먼저 검토해야 한다.

### 6. 모델 사용

K3는 thinking이 항상 활성화되고 `reasoning_content`를 반환한다.
top-level `reasoning_effort`는 `low`, `high`, `max`를 지원하며 기본값은
`max`다.

K3는 preserved thinking history mode로 학습됐다. 다중 턴 대화와 tool
call에서는 API가 반환한 assistant message를 그대로 다음 `messages`에
넣어야 한다. `content`뿐 아니라 `reasoning_content`, `tool_calls`까지
보존해야 한다. 일부 field만 재구성하면 이전 사고 상태와의 연결이
깨져 품질이 불안정해질 수 있다.

### 7. 라이선스

코드와 모델 가중치는 Kimi K3 License로 공개된다. 핵심 조건의 한국어
요약은 다음과 같다.

1. 저작권과 허가 고지를 복사본 또는 실질적 부분에 포함하고 관련 법률을
   준수해야 한다.
2. 제3자가 입력·파라미터·학습 데이터를 의미 있게 제어하는
   Model-as-a-Service 사업을 운영하면서 사용자와 계열사의 합산 매출이
   연속 12개월 동안 미화 2천만 달러를 넘으면, K3나 파생물을 상업적으로
   사용하기 전에 Moonshot AI와 별도 계약을 체결해야 한다.
3. K3 또는 파생물을 사용하는 상용 제품·서비스가 월간 활성 사용자
   1억 명을 넘거나 월 매출 미화 2천만 달러를 넘으면 제품 UI에
   `Kimi K3`를 눈에 띄게 표시해야 한다.
4. 내부 사용과 Moonshot 공식 제품 또는 인증 inference partner를 통한
   사용에는 2·3항의 특별 조건이 적용되지 않는다.
5. 소프트웨어와 출력은 무보증으로 제공되고 손해 책임이 제한된다.

정확한 의무와 용어 정의는
[영문 라이선스 원문](https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE)을
기준으로 확인해야 한다.

---

## 기술 블로그 한국어 번역 요약

## Kimi K3: 개방형 프런티어 지능

Kimi는 자사에서 가장 강력한 모델인 Kimi K3를 소개한다. K3는 Kimi Delta Attention과 Attention Residuals를 기반으로 한 2.8조 파라미터 모델이며, 네이티브 비전과 100만 토큰 문맥 창을 갖춘 최초의 개방형 3T급 모델이라고 설명한다. 장시간 코딩, 지식 작업, 추론을 목표로 한다.

회사는 K3가 가장 강력한 폐쇄형 모델보다는 전반적으로 뒤처지지만, 자사의
평가군에서는 다른 시험 모델을 지속적으로 앞서는 프런티어급 성능을
보였다고 주장한다. K3는 Kimi 웹, Kimi Work, Kimi Code와 API에서
제공되며 출시 시점에는 최대 사고 노력을 기본으로 사용한다. 기술 블로그
당시 2026년 7월 27일까지 공개하겠다고 예고한 전체 가중치는
2026-07-28 재확인 시 Hugging Face에 실제 공개됐다.

## 개방형 3T급 모델

K3는 2.8조 파라미터에 도달한 첫 개방형 모델로 소개된다. KDA와 AttnRes는 각각 시퀀스 길이와 모델 깊이 전반의 정보 흐름을 개선하려는 구조다. Stable LatentMoE와 결합해 896개 전문가 중 16개를 활성화한다. 개선된 학습·데이터 방법과 함께 K2보다 전체 스케일링 효율이 약 2.5배 좋아졌다고 설명한다.

## 코딩

K3는 적은 사람의 감독으로 긴 엔지니어링 세션을 지속하고, 대규모 저장소와 터미널 도구를 다루는 능력을 강조한다. 시각 추론을 함께 사용해 게임 개발, 프런트엔드와 CAD 결과를 스크린샷으로 보면서 반복 개선할 수 있다고 한다.

### 커널 최적화

동일한 샌드박스에서 모델별로 최대 24시간 동안 NVIDIA H200과 다른 공급사의 범용 GPU를 대상으로 네 가지 커널을 최적화했다. 회사는 K3가 강한 경쟁력을 보였다고 보고한다. 일부 모델 실행은 fallback을 포함하고, 허용 오차 안의 정밀도 단축도 있으므로 조건을 함께 읽어야 한다.

### GPU 컴파일러 개발

K3는 MLIR 위의 타일 수준 IR, 최적화 패스, PTX 코드 생성 파이프라인을 갖춘 작은 Triton 유사 컴파일러 MiniTriton을 처음부터 개발했다고 한다. 지원하는 roofline 벤치마크와 nanoGPT 학습에서 경쟁력 있는 성능과 안정적 수렴을 보고했다.

### 게임, 칩, 과학 연구

K3는 코드와 실제 스크린샷 사이를 반복하는 방식으로 3D 콘텐츠와 게임을 만들었다. 또 공개 EDA 도구와 Nangate 45nm 라이브러리를 사용한 48시간 자율 실행에서 소형 모델용 칩을 설계·검증했다고 소개한다. 계산천체물리 사례에서는 20편 이상의 논문 검토, 300개 이상의 상태방정식 평가, 3천 줄 이상의 Python과 대화형 대시보드 생성을 수행했다고 한다.

## 지식 작업

내부 평가에서는 실제 에이전트 작업에서 반복되는 문제를 바탕으로 지식 작업 능력이 향상됐다고 보고한다. 사례로 42년간의 AI ASIC 산업 조사, 핵융합 산업 보고서, 20개 이상의 동시 서브에이전트를 사용한 391개 중력파 사건 분석을 제시한다.

Kimi Work의 Widget은 채팅 안에서 로컬 데이터나 외부 플러그인과 연결되는 대화형 구성 요소를 만들고, Dashboard는 이를 주제·프로젝트·목표별 지속 화면으로 모은다. 네이티브 멀티모달 구조를 활용한 모션 그래픽과 영상 편집 사례도 소개한다.

## 아키텍처와 인프라

KDA와 AttnRes가 모델의 핵심 뼈대다. 16/896 전문가를 활성화하는 Stable LatentMoE에서는 라우팅과 최적화가 특히 중요하다. Quantile Balancing은 라우터 점수의 분위수로 전문가 할당을 정하고, Per-Head Muon은 어텐션 헤드를 독립적으로 최적화한다. SiTU와 Gated MLA는 각각 활성화 제어와 어텐션 선택성을 개선한다.

SFT부터 MXFP4 가중치와 MXFP8 활성화를 사용하는 양자화 인지 학습을
적용했다. 대규모 전문가 병렬 학습의 처리량을 위해 정적 shape와 중요
경로에서 host 동기화가 없는 완전 균형 방식을 도입했다고 한다. 추론에는
64개 이상 가속기의 supernode 구성을 권장하며, 모델 공개 후 vLLM
recipe도 연결했다.

## 이용 방법

- Kimi 앱 또는 kimi.com에서 K3 에이전트 사용
- Windows와 Apple silicon Mac용 Kimi Work 3.1.0 이상 사용
- Kimi Code에서 `/model` 명령으로 K3 선택
- Kimi API에서 `kimi-k3` 선택

원문 확인 당시 API 가격은 백만 토큰당 cache-hit 입력 0.30달러, cache-miss 입력 3달러, 출력 15달러로 제시됐다. 가격은 변동될 수 있다.

## 평가 주석

K3 결과는 최대 추론 노력, temperature 1.0, top-p 1.0으로 얻었다. 벤치마크별로 KimiCode, Claude Code 또는 Codex 하네스를 사용하며 비교 모델의 조건도 항상 같지는 않다. 일부 점수는 외부 리더보드, 일부는 회사 내부 평가에서 왔다. 따라서 결과는 각주와 실행 조건을 포함해 해석해야 한다.

## 한계

1. K3는 보존된 사고 이력을 사용하는 방식으로 학습됐다. 하네스가 필요한 사고 이력을 다시 전달하지 않거나 진행 중 다른 모델에서 K3로 바꾸면 생성 품질이 크게 불안정해질 수 있다.
2. 장시간 어려운 과제를 중시한 학습 때문에 작은 문제나 모호한 의도에서 사용자 대신 예상하지 못한 결정을 내릴 수 있다. 시스템 프롬프트나 `AGENTS.md`에 행동 경계를 더 명확하게 설정할 것을 권한다.
3. 전반적으로 경쟁력은 높지만 가장 강력한 폐쇄형 모델과 비교해 사용자 경험 차이가 남아 있다고 회사도 밝힌다.
