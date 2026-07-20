# NVIDIA Nemotron 3 Nano Omni

작성일: 2026-07-20

## 출처와 작업 범위

- 입력 URL: [DebuggerCafe - Introduction to NVIDIA Nemotron 3 Nano Omni](https://debuggercafe.com/introduction-to-nvidia-nemotron-3-nano-omni/)
- 원문 작성자: Sovit Ranjan Rath
- 원문 게시일: 2026-07-13
- 확인 기준일: 2026-07-20
- 주요 공식 자료:
  - [NVIDIA 연구 보고서 PDF - Nemotron 3 Nano Omni: Efficient and Open Multimodal Intelligence](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Omni-report.pdf)
  - [arXiv:2604.24954](https://arxiv.org/abs/2604.24954)
  - [Hugging Face model card - Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16](https://huggingface.co/nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16)
  - [NVIDIA Build model page](https://build.nvidia.com/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning)
- 작업 범위: DebuggerCafe 글의 모델 소개와 NVIDIA API/Gradio 앱 구현 흐름을 바탕으로, Nemotron 3 Nano Omni의 아키텍처, 학습 레시피, API payload 구성, 추론 옵션, 한계, 실습 코드를 한국어 학습 자료로 정리한다.

원문과 주요 공식 자료가 영어이므로 `translation.ko.md`에 핵심 번역/해설을 별도로 작성했다. 이 폴더의 노트북은 API 키 없이도 실행 가능한 교육용 축소 구현이며, 실제 NVIDIA API 호출 코드는 payload 구조와 운영 주의점을 이해하는 목적으로 다룬다.

## 한눈에 보기

Nemotron 3 Nano Omni는 NVIDIA의 옴니모달 언어 모델이다. 텍스트만 다루는 LLM과 달리 텍스트, 이미지, 비디오, 오디오, 문서형 입력을 하나의 흐름에서 처리하도록 설계되었다. DebuggerCafe 글은 이 모델을 소개하면서 NVIDIA API를 이용해 간단한 Gradio 챗 애플리케이션을 만드는 흐름을 보여준다.

공식 모델 카드 기준으로 모델은 약 31B 전체 파라미터를 갖는 Mamba2-Transformer hybrid MoE 구조이며, token당 활성 파라미터는 약 3B다. 글에서는 이를 30B 파라미터, 3B active parameter로 설명한다. 두 표기는 같은 모델 계열을 서로 다른 정밀도와 반올림 관점에서 부르는 것으로 보면 된다.

핵심 장점은 멀티모달 입력을 여러 모델 파이프라인으로 쪼개지 않고, modality-specific encoder와 shared decoder로 통합 처리한다는 점이다. 이 접근은 이미지 OCR, 문서 이해, 비디오+음성 이해, GUI/agentic workflow 같은 enterprise multimodal task에 적합하다.

## 기초 개념

### 옴니모달 모델

멀티모달 모델은 여러 입력 형식을 다루는 모델이다. 옴니모달 모델은 여기서 더 나아가 텍스트, 이미지, 비디오, 오디오처럼 서로 다른 modality를 하나의 통합 추론 흐름으로 처리하려는 모델을 뜻한다. Nemotron 3 Nano Omni는 입력으로 비디오, 오디오, 이미지, 텍스트를 받고 출력은 텍스트로 낸다.

### Encoder-Projector-Decoder 구조

텍스트는 tokenizer를 거쳐 언어 모델로 들어간다. 이미지, 비디오, 오디오는 원래 숫자 배열의 형태와 시간/공간 구조가 다르므로 modality-specific encoder가 먼저 처리한다. encoder 출력은 projector를 거쳐 LLM decoder가 이해할 수 있는 token-like representation으로 바뀐다.

Nemotron 3 Nano Omni의 대표 구성은 다음과 같다.

- Vision encoder: C-RADIOv4-H
- Audio encoder: Parakeet-TDT-0.6B-v2 FastConformer
- Backbone LLM: Nemotron 3 Nano 30B-A3B, Mamba2-Transformer hybrid MoE
- Projector/adaptor: modality encoder 출력을 shared decoder 입력 공간으로 맞추는 MLP 계열 모듈

### MoE와 active parameter

Mixture of Experts, 즉 MoE는 전체 파라미터 중 일부 expert만 token별로 활성화하는 구조다. 전체 모델은 크지만 매 token 처리에 쓰이는 활성 파라미터 수는 작게 유지할 수 있다. 그래서 모델 카드의 "31B total parameters"와 "~3B active parameters per token"을 함께 읽어야 한다.

### Token reduction

비디오와 고해상도 이미지는 token 수가 급격히 커져 VRAM, latency, throughput에 직접 영향을 준다. Nemotron 3 Nano Omni는 dynamic image resolution, pixel shuffle downsampling, Conv3D video patch embedding 같은 방법으로 visual token을 줄인다. 오디오도 초당 약 12.5 token 수준으로 압축해 긴 오디오 입력을 다루기 쉽게 만든다.

### Reasoning mode

모델 카드와 DebuggerCafe 예제는 `enable_thinking` 옵션을 통해 reasoning mode를 다룬다. reasoning mode는 더 긴 추론 예산을 쓰는 대신 latency와 출력 길이가 늘 수 있다. API 예제에서는 `reasoning_budget`을 별도로 지정한다.

## 핵심 요약

- Nemotron 3 Nano Omni는 텍스트, 이미지, 비디오, 오디오 입력을 지원하는 NVIDIA 옴니모달 모델이다.
- 모델 카드 기준 전체 파라미터는 31B, token당 활성 파라미터는 약 3B다.
- 최대 context 길이는 256K token이다.
- 입력 modality는 video, audio, image, text이고 출력은 text다.
- 아키텍처는 modality-specific encoder, projector/adaptor, shared decoder 구조다.
- 이미지는 dynamic resolution으로 native aspect ratio를 보존하고, 16x16 patch 기반 token으로 바꾼다.
- 비디오는 Conv3D patch embedder로 두 frame을 하나로 압축해 temporal token을 줄인다.
- 오디오는 16 kHz mono, log-mel spectrogram, FastConformer encoder를 거쳐 초당 약 12.5 token으로 표현된다.
- SFT는 vision, audio, omni, long-context를 단계적으로 확장하는 7개 stage로 구성된다.
- NVIDIA API는 OpenAI-compatible client 형태로 호출할 수 있으며 base URL은 `https://integrate.api.nvidia.com/v1`이다.
- DebuggerCafe 예제는 `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` 모델 ID, Gradio UI, session-local history, media file payload builder를 사용한다.
- 실제 운영에서는 rate limit, 파일 크기, base64 payload 비용, reasoning mode 안정성, 개인정보와 저작권, 모델 라이선스를 별도로 점검해야 한다.

## 상세 정리

### 1. 왜 옴니모달인가

현실 업무 문서는 텍스트만으로 구성되지 않는다. 회의 녹화에는 영상과 음성이 있고, 계약서에는 표와 도장이 있으며, 고객 지원에는 사진, 동영상, 음성 설명이 섞인다. 전통적인 방식은 OCR 모델, ASR 모델, 이미지 captioning 모델, 텍스트 LLM을 따로 이어 붙인다. 이 방식은 구현이 복잡하고, 각 단계에서 context 손실이 생기며, latency와 비용이 누적된다.

Nemotron 3 Nano Omni의 방향은 여러 modality를 하나의 decoder context로 정렬해 공동 추론하는 것이다. 특히 video with audio에서 시각 token과 audio token을 시간 순서로 interleave하면 "무엇이 보이는가"와 "그 순간 무엇이 들리는가"를 함께 추론할 수 있다.

### 2. 아키텍처

모델은 encoder-projector-decoder 설계를 따른다. 텍스트는 tokenizer를 거쳐 LLM backbone으로 들어간다. 이미지와 비디오는 C-RADIOv4-H vision encoder가 처리하고, 오디오는 Parakeet-TDT-0.6B-v2 FastConformer encoder가 처리한다. 각 encoder 출력은 projector/adaptor를 거쳐 shared LLM decoder 입력으로 연결된다.

이미지 처리에서 기존 tiling 방식 대신 dynamic resolution을 사용한다. 이 방식은 원본 aspect ratio를 보존하면서 이미지 token 수를 입력 해상도에 따라 조절한다. 공식 보고서는 이미지당 visual token 수가 1,024에서 13,312 범위에 놓인다고 설명한다. projection 전에 pixel shuffle로 4배 downsampling을 적용해 decoder가 받아야 하는 token 수를 더 줄인다.

비디오에서는 Conv3D patch embedder를 사용해 두 개의 연속 frame을 하나의 temporal unit으로 압축한다. 이는 비디오 token을 약 2배 줄이는 효과가 있다. 비디오는 context 비용이 매우 크기 때문에 이 구조는 throughput과 latency에 직접적인 영향을 준다.

오디오는 16 kHz mono로 resampling한 뒤 log-mel spectrogram으로 변환된다. 세 개의 stride-2 convolutional subsampling layer를 거치며 초당 약 12.5 token, 즉 token당 약 80 ms 수준으로 압축된다. 보고서는 학습 시 0.5초에서 20분까지의 오디오를 다루었고, context 길이 관점에서는 5시간 이상의 오디오도 수용 가능하다고 설명한다.

### 3. 학습 레시피

공식 보고서는 SFT를 7개 stage로 나눈다.

| Stage | 목적 | context | 대략적 규모 |
| --- | --- | --- | --- |
| 0 | vision projector warmup | 16K | 9.35M samples, 15.5B tokens |
| 1 | vision encoder + LLM SFT | 16K | 86.3M samples, 214.8B tokens |
| 2 | audio projector warmup | 16K | 59.2M samples, 11.4B tokens |
| 3 | audio encoder/projector training | 16K | 242.0M samples, 100.5B tokens |
| 4 | joint omni SFT | 16K | 30.5M samples, 57.3B tokens |
| 5 | joint omni SFT | 48K | 6.08M samples, 33.5B tokens |
| 6 | long-context omni/text/vision SFT | 256K | 623K samples, 34.0B tokens |

이 staged curriculum의 목적은 한 번에 모든 modality와 긴 context를 밀어 넣지 않고, projector 정렬, modality 확장, long-context 확장을 순차적으로 안정화하는 것이다. 이후에는 text, vision, omni 영역에 대한 RL 단계가 이어진다.

### 4. NVIDIA API 호출 구조

DebuggerCafe 예제는 OpenAI Python SDK를 NVIDIA endpoint에 연결하는 방식이다.

- API base URL: `https://integrate.api.nvidia.com/v1`
- model: `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning`
- media payload: local file을 base64 data URI로 바꾸거나, URL이 있으면 그대로 전달
- content type: `image_url`, `video_url`, `audio_url`, `text`
- reasoning toggle: `extra_body.chat_template_kwargs.enable_thinking`
- reasoning budget: `extra_body.reasoning_budget`
- video audio toggle: `extra_body.mm_processor_kwargs.use_audio_in_video`

이 구조는 OpenAI-compatible API 형식에 익숙한 개발자가 빠르게 실험하기 좋다. 다만 base64 data URI는 파일 크기만큼 request payload가 커지므로 실제 서비스에서는 파일 크기 제한, timeout, retry, rate limit, 개인정보 처리를 함께 설계해야 한다.

### 5. Gradio 앱 구조

원문 앱은 크게 두 파일로 나뉜다.

- `api.py`: MIME type 판별, local file to data URI 변환, user message 생성, streaming API 호출
- `app.py`: Gradio UI, 업로드 파일 정규화, session-local chat history, streaming 응답 표시

중요한 점은 history가 영구 저장되지 않는다는 것이다. Gradio 세션 안에서만 대화 맥락을 유지하고, 페이지 새로고침이나 서버 재시작 시 사라진다. 실서비스에서는 user/session ID, 저장소, 삭제 정책, 민감정보 마스킹을 별도로 설계해야 한다.

### 6. 배포 옵션

모델 카드는 BF16, FP8, NVFP4 precision을 제공한다. BF16은 H100 80GB급 단일 GPU를 최소로 제시하고, FP8은 L40S 48GB, NVFP4는 RTX 5090 32GB까지 내려가는 구성을 안내한다. vLLM, TensorRT-LLM, SGLang, NeMo, Megatron 계열 통합도 언급된다.

DebuggerCafe 글은 API 실험 다음 단계로 Modal serverless 배포를 예고한다. 이는 rate limit이 있는 hosted API에서 벗어나 GPU serving, latency, context, 비용을 직접 통제하려는 방향이다.

### 7. 한계와 주의점

- DebuggerCafe 예제는 입문용 앱이며, production-grade 파일 검증과 보안 처리가 제한적이다.
- reasoning mode는 출력이 길고 비용이 커지며, 원문은 일부 상황에서 불안정한 출력 가능성을 언급한다.
- 무료 API rate limit은 실험에는 충분해도 평가 자동화나 대량 처리에는 부족할 수 있다.
- 모델 카드 기준 언어 지원은 English only로 표시된다. 한국어 입력/출력 품질은 별도 검증이 필요하다.
- media data URI는 편하지만 payload가 커지고 로그에 민감정보가 남을 위험이 있다.
- NVIDIA Open Model Agreement와 API 약관을 실제 사용 전에 확인해야 한다.

## 용어 정리

| 용어 | 뜻 |
| --- | --- |
| Omni-modal | 텍스트, 이미지, 비디오, 오디오 등 여러 modality를 통합 처리하는 방식 |
| Modality | 입력 정보의 종류. 예: text, image, video, audio |
| Encoder | modality별 원시 입력을 feature/token 표현으로 바꾸는 모델 |
| Projector/Adaptor | encoder 출력을 LLM decoder가 받을 수 있는 공간으로 맞추는 모듈 |
| Decoder | 통합 token context를 바탕으로 텍스트 출력을 생성하는 LLM 부분 |
| MoE | Mixture of Experts, token별로 일부 expert만 활성화하는 모델 구조 |
| Active parameters | 특정 token 처리에 실제로 사용되는 파라미터 수 |
| Dynamic resolution | 이미지 원본 비율을 보존하며 token 수를 조절하는 처리 |
| Pixel shuffle | 공간 정보를 재배치해 token 또는 feature 해상도를 줄이는 기법 |
| Conv3D patch embedder | 비디오의 공간과 시간 축을 함께 처리하는 3D convolution 기반 patch embedding |
| Log-mel spectrogram | 오디오를 시간-주파수 특징으로 표현한 입력 |
| Reasoning mode | 더 긴 추론 예산을 쓰는 모델 동작 모드 |
| `enable_thinking` | NVIDIA API 예제에서 reasoning mode를 켜는 옵션 |
| `use_audio_in_video` | 비디오 입력 안의 오디오까지 함께 처리하도록 요청하는 옵션 |
| Data URI | 파일 내용을 base64로 인코딩해 URL 문자열처럼 넣는 표현 |
| Session-local history | 서버 재시작이나 새로고침 후 사라지는 임시 대화 기록 |

## 실습 학습 가이드

선택적으로 원문 스타일의 API/Gradio 앱을 직접 확장하려면 다음 패키지를 설치한다.

```bash
pip install -r nvidia-nemotron-3-nano-omni/requirements.txt
```

- `01_foundations.ipynb`: 이미지, 비디오, 오디오 입력이 token budget에 어떤 영향을 주는지 계산하며 옴니모달 아키텍처를 익힌다.
- `02_practice.ipynb`: NVIDIA OpenAI-compatible API payload를 직접 조립한다. 실제 네트워크 호출은 하지 않고 `messages`, media part, `extra_body` 구조를 검증한다.
- `03_advanced.ipynb`: session-local chat history, streaming 응답, reasoning mode, rate limit 방어, multimodal request validation을 모의 구현한다.

노트북은 Python 표준 라이브러리만 사용한다. 실제 API 호출에는 `NVIDIA_API_KEY`와 NVIDIA API 사용 권한이 필요하다.

## 다음 학습 경로

1. 멀티모달 LLM 기본: CLIP, Flamingo, LLaVA, Qwen-VL 계열의 encoder-projector-decoder 구조를 비교한다.
2. 오디오/비디오 tokenization: log-mel spectrogram, video patch embedding, frame sampling, temporal compression을 실습한다.
3. API 앱 확장: 파일 크기 제한, MIME sniffing, request timeout, retry/backoff, streaming UI를 추가한다.
4. 평가 설계: text-only, image QA, OCR, video QA, audio transcription, video+audio reasoning을 분리 평가한다.
5. 배포 학습: NVIDIA API, vLLM, TensorRT-LLM, SGLang 배포 경로의 latency와 비용을 비교한다.
6. 책임 있는 사용: 민감한 오디오/문서 입력, 보안 로그, 저작권 자료 처리, hallucination 검증 정책을 설계한다.
