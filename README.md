# Laboratory

작성일: 2026-07-16

## TODO

- [ ] [TripoSplat 한국어 학습 가이드](TripoSplat/guide/README.md) - 2026-07-23
- [ ] [Thinking to Recall: 추론과 파라메트릭 지식 회상](thinking-to-recall-parametric-knowledge/README.md) - 2026-07-23
- [ ] [NeuralLog: 로그 파싱 없는 로그 이상 탐지](neurallog-log-anomaly-detection/README.md) - 2026-07-23
- [ ] [On-Policy Delta Distillation](on-policy-delta-distillation/README.md) - 2026-07-23
- [ ] [Inkling 오픈 웨이트 모델](inkling-open-weights-model/README.md) - 2026-07-23
- [ ] [사전학습에서 포스트 트레이닝까지의 추론 이해](pretraining-post-training-reasoning/README.md) - 2026-07-23
- [ ] [언어 모델 하네스와 조합적 일반화](language-model-harnesses/README.md) - 2026-07-23
- [ ] [SEED: Self-Evolving On-Policy Distillation](seed-self-evolving-opd/README.md) - 2026-07-23
- [ ] [Transformer Explainer 한국어 학습 가이드](transformer-explainer/guide/README.md) - 2026-07-23
- [ ] [확산 언어 모델: LLaDA에서 DiffusionGemma까지](diffusion-llm-llada-diffusiongemma/README.md) - 2026-07-22
- [ ] [LLM 비용 64% 절감과 캐시 히트율 98% 달성 사례](llm-prompt-caching-cost-optimization/README.md) - 2026-07-22
- [ ] [추론 흔적에서 재사용 가능한 모듈로](reasoning-traces-reusable-modules/README.md) - 2026-07-21
- [ ] [Shepherd 한국어 학습 가이드](shepherd/guide/README.md) - 2026-07-21
- [ ] [Unlimited-OCR 한국어 학습 가이드](Unlimited-OCR/guide/README.md) - 2026-07-21
- [ ] [D-FINE-seg: 실시간 객체 검출·분할과 멀티 백엔드 배포](d-fine-seg/README.md) - 2026-07-21
- [ ] [TabFM 한국어 학습 가이드](tabfm/guide/README.md) - 2026-07-21
- [ ] [TabFM: 표 데이터용 Zero-shot Foundation Model](tabfm-tabular-foundation-model/README.md) - 2026-07-21
- [ ] [에이전트형 세계 모델](agentic-world-models/README.md) - 2026-07-20
- [ ] [Hands-On AI Engineering 한국어 학습 가이드](Hands-On-AI-Engineering/guide/README.md) - 2026-07-20
- [ ] [Kimi K3: 개방형 3T급 멀티모달 에이전트 모델](kimi-k3/README.md) - 2026-07-20
- [ ] [Orca 한국어 사용 가이드](orca/guide.md) - 2026-07-20
- [ ] [NVIDIA Nemotron 3 Nano Omni](nvidia-nemotron-3-nano-omni/README.md) - 2026-07-20
- [ ] [S2Vec: 자기지도 지리공간 임베딩](s2vec-geospatial-embeddings/README.md) - 2026-07-18
- [ ] [pdf-inspector 오픈소스 정리](Opensource/README.md) - 2026-07-17
- [ ] [2026년 7월 중순 VLM 트렌드 카테고리별 학습 자료](vlm-trending-categories-2026-07/README.md) - 2026-07-17
- [ ] [2026년 7월 VLM 인기 논문 Top 5 카테고리 분석](vlm-trending-papers-2026-07/README.md) - 2026-07-17
- [ ] [Chrome Built-in AI Embedding API](chrome-built-in-embedding-api/README.md) - 2026-07-17
- [ ] [Nexus: 에이전트형 시계열 예측](nexus-agentic-time-series-forecasting/README.md) - 2026-07-16

## 목적

이 레포는 사용자가 전달한 링크, 문서, 기술 주제, 코드 예제, 설명 자료를 에이전트가 분석하고 학습 가능한 형태로 정리하기 위한 실험실입니다.

핵심 목표는 단순 요약이 아니라, 기초 개념부터 실습 중심 학습 자료까지 한 폴더 안에 체계적으로 쌓는 것입니다. 어떤 에이전트가 작업하더라도 같은 방식으로 결과물이 나오도록 루트의 [AGENTS.md](AGENTS.md)를 표준 작업 하네스로 사용합니다.

## 에이전트 작업 결과물

사용자가 링크나 내용을 주고 분석을 요청하면 에이전트는 다음 구조를 만듭니다.

```text
topic-folder/
  README.md
  translation.ko.md        # 원문이 한국어가 아닐 때 필수
  01_foundations.ipynb     # 기본은 Python 실습
  02_practice.ipynb
  03_advanced.ipynb
```

주제가 C++ 또는 C# 중심이면 실습 파일은 문서 내용에 맞춰 `01_foundations.cpp`, `01_foundations.csx`처럼 작성할 수 있습니다.

## 필수 규칙

- 하나의 요청은 적절한 이름의 하나의 폴더로 정리합니다.
- 새 폴더의 `README.md` 상단에는 작성 일자 `YYYY-MM-DD`를 표시합니다.
- 원문이나 사이트가 한국어가 아니면 한국어 번역본 `translation.ko.md`를 만듭니다.
- 새 폴더의 `README.md` 경로를 이 파일 상단 `TODO`에 체크박스 링크로 추가합니다.
- 학습 코드는 새 폴더의 `README.md` 안에 몰아넣지 않고, 번호가 붙은 별도 파일로 제공합니다.
- 실습 코드는 기초 문법, 작성 이유, 중요한 설계 선택을 주석으로 충분히 설명합니다.
- 자료는 기초 지식 베이스부터 전문적인 수준까지 올라갈 수 있도록 단계별로 구성합니다.

## 사용법

에이전트에게 작업을 요청할 때는 다음처럼 말하면 됩니다.

```text
이 레포의 AGENTS.md 규칙에 따라 아래 링크를 분석해서 학습 폴더를 만들어줘.
<분석할 링크 또는 내용>
```

또는 주제만 전달할 수도 있습니다.

```text
이 레포의 AGENTS.md 규칙에 따라 React Server Components를 기초부터 실습할 수 있게 정리해줘.
```

에이전트는 [AGENTS.md](AGENTS.md)의 Content Learning Harness를 읽고 다음 순서로 작업합니다.

1. 요청한 링크나 내용을 수집하고 분석합니다.
2. 주제에 맞는 폴더명을 정합니다.
3. 새 폴더에 한국어 요약 및 상세 정리 `README.md`를 작성합니다.
4. 원문이 한국어가 아니면 `translation.ko.md`를 작성합니다.
5. 번호가 붙은 실습 파일을 만듭니다.
6. 이 README 상단 `TODO`에 새 `README.md` 경로를 추가합니다.
7. 누락된 산출물이 없는지 하네스 체크리스트로 검증합니다.

## 추천 폴더명 규칙

- 영문 기술명은 소문자 kebab-case를 사용합니다. 예: `react-server-components`
- 한글 주제는 의미를 살린 짧은 영문 slug를 우선 사용합니다. 예: `llm-agent-harness`
- 같은 이름이 이미 있으면 `topic-name-2`처럼 뒤에 숫자를 붙입니다.

## 현재 포함된 실험

- [hairstyle-app](hairstyle-app/README.md)
