# 2026년 7월 VLM 인기 논문 Top 5 카테고리 분석

작성일: 2026-07-17

## 출처와 작업 범위

확인 기준일: 2026-07-17

이 문서는 사용자가 제공한 "2026년 7월 중순 기준 최신 VLM 인기 논문 Top 5" 목록을 학습용 카테고리로 재구성한 자료입니다. 순위는 사용자가 제공한 순서를 유지하되, 공개 출처에서 확인한 사실과 해석을 분리했습니다.

주의할 점은 다음과 같습니다.

- 다섯 논문은 arXiv 또는 Hugging Face Papers 페이지에서 확인했습니다.
- "글로벌 Top 5"는 단일 공식 랭킹으로 검증한 것이 아니라, 사용자 제공 순위와 Hugging Face 인기도 지표를 학습 목차로 사용한 것입니다.
- "CVPR 2026 등"은 사용자 입력의 연구 맥락 표현으로 보았습니다. 아래 출처에서 직접 확인한 것은 주로 arXiv의 `cs.CV`, Hugging Face Papers, GitHub/프로젝트 페이지 정보입니다.
- Hugging Face upvote, GitHub star, Paper of the day 같은 지표는 시간에 따라 변합니다.

| 순위 | 카테고리 | 논문 | 확인한 공개 출처 |
|---:|---|---|---|
| 1 | 네이티브 문서 비주얼 사전학습 | Scalable Visual Pretraining for Language Intelligence | arXiv: https://arxiv.org/abs/2607.09657, Hugging Face: https://huggingface.co/papers/2607.09657 |
| 2 | 장문 문서 OCR과 상수 KV 캐시 | Unlimited OCR Works | arXiv: https://arxiv.org/abs/2606.23050, Hugging Face: https://huggingface.co/papers/2606.23050, GitHub: https://github.com/baidu/Unlimited-OCR |
| 3 | 통합 멀티모달 생성 | Vision as Unified Multimodal Generation | arXiv: https://arxiv.org/abs/2607.06560, Hugging Face: https://huggingface.co/papers/2607.06560, GitHub: https://github.com/OpenSenseNova/SenseNova-Vision |
| 4 | 조밀 공간 지각과 경계 중심 사전학습 | Vision Pretraining for Dense Spatial Perception | arXiv: https://arxiv.org/abs/2607.05247, Hugging Face: https://huggingface.co/papers/2607.05247, GitHub: https://github.com/robbyant/lingbot-vision |
| 5 | 상호작용형 월드 모델과 에이전트 루프 | Infinite Worlds with Versatile Interactions | arXiv: https://arxiv.org/abs/2607.07534, Hugging Face: https://huggingface.co/papers/2607.07534 |

## 한눈에 보기

2026년 7월 중순의 VLM 관련 흐름은 "이미지를 텍스트로 변환한 뒤 학습하는 방식"에서 "시각 구조를 가능한 한 원형에 가깝게 모델 입력과 출력 공간에 남기는 방식"으로 이동하고 있습니다.

| 축 | 기존 접근 | 새 흐름 | 대표 논문 |
|---|---|---|---|
| 문서 학습 | PDF를 텍스트로 추출한 뒤 언어 모델 학습 | 페이지 레이아웃, 수식, 도표를 시각 입력 그대로 사전학습 | Scalable Visual Pretraining |
| 장문 OCR | 페이지 단위 처리 또는 긴 출력에서 KV 캐시 증가 | 참조 토큰과 최근 출력 토큰만 유지해 메모리를 상수에 가깝게 제어 | Unlimited OCR Works |
| 비전 태스크 | detection, segmentation, depth마다 별도 헤드 | 텍스트, 이미지, 혼합 출력으로 시리얼라이즈해 단일 생성 모델이 처리 | SenseNova-Vision |
| 공간 지각 | 의미 분류 중심 표현학습 | 경계, 깊이 불연속, 서브픽셀 구조를 사전학습 목표로 사용 | LingBot-Vision |
| 상호작용 | 짧은 비디오 생성 또는 수동 제어 | 긴 상호작용 지평, 실시간 변형, 에이전트 기획 루프 | LingBot-World 2.0 |

## 기초 개념

### VLM

VLM은 Vision Language Model의 약자입니다. 이미지를 보고 텍스트로 답하거나, 텍스트 지시에 따라 이미지를 해석하고 조작하는 모델을 넓게 가리킵니다. 최근에는 단순 이미지 캡션이나 VQA를 넘어 문서 파싱, 공간 추론, 로봇/에이전트 행동, 이미지 생성까지 포함하는 방향으로 확장되고 있습니다.

### 비주얼 토큰

이미지를 작은 패치나 잠재 벡터로 나눈 단위입니다. 언어 모델이 단어 토큰을 처리하듯, VLM은 이미지 패치나 이미지 잠재 표현을 토큰처럼 처리합니다. 문서 이미지에서는 글자 모양, 표 경계, 수식 위치, 다이어그램 구조가 비주얼 토큰 안에 남아 있습니다.

### OCR 전처리의 손실

OCR은 이미지 안의 글자를 텍스트로 바꾸는 과정입니다. 문서의 단락, 수식 배치, 표 구조, 그림과 본문의 관계는 단순 텍스트로 바꾸는 순간 약해질 수 있습니다. 그래서 네이티브 비주얼 사전학습은 "텍스트만 남기지 말고 원본 페이지의 시각 구조를 직접 학습하자"는 문제의식에서 출발합니다.

### KV 캐시

트랜스포머 디코더는 이전 토큰의 key와 value를 저장해 다음 토큰 생성을 빠르게 합니다. 이 저장소가 KV 캐시입니다. 출력 토큰이 길어질수록 일반적인 KV 캐시는 계속 커집니다. 장문 OCR처럼 수만 토큰을 생성하는 작업에서는 이것이 GPU 메모리 병목이 됩니다.

### 태스크 헤드

전통적인 비전 모델은 물체 검출용 헤드, 세그멘테이션용 헤드, 깊이 추정용 헤드처럼 태스크별 출력 장치를 따로 둡니다. 통합 멀티모달 생성 접근은 이런 헤드를 줄이고, 여러 종류의 출력을 텍스트나 이미지 생성 문제로 바꿉니다.

### 조밀 공간 지각

이미지 전체의 의미를 맞히는 것을 넘어, 픽셀 수준에서 경계, 깊이, 표면 방향, 좌표, 카메라 포즈 같은 물리적 구조를 파악하는 능력입니다. 로봇, 자율주행, 증강현실, 3D 재구성에서 중요합니다.

## 핵심 요약

| 논문 | 핵심 질문 | 제안된 답 | 읽을 때 봐야 할 포인트 |
|---|---|---|---|
| Scalable Visual Pretraining | 언어 지능은 꼭 텍스트 코퍼스에서만 배워야 하는가? | 시각 문서를 직접 사용한 비지도 비주얼 사전학습 | 같은 원문 자료를 텍스트와 이미지 경로로 학습했을 때의 비교 설계 |
| Unlimited OCR Works | 장문 문서 OCR에서 왜 메모리가 폭증하는가? | Reference Sliding Window Attention으로 디코더 KV 캐시를 고정 크기에 가깝게 유지 | 참조 토큰, 슬라이딩 출력 창, 32K 길이 안의 one-shot parsing |
| Vision as Unified Multimodal Generation | 비전 태스크마다 다른 헤드가 꼭 필요한가? | detection, OCR, depth, segmentation 등을 텍스트/이미지 생성 공간으로 통합 | 출력 포맷 설계와 대규모 instruction-response 코퍼스 |
| Vision Pretraining for Dense Spatial Perception | 의미론 중심 ViT가 공간 구조를 놓치는 이유는 무엇인가? | Masked Boundary Modeling으로 경계와 깊이 단서를 사전학습 | 경계 토큰이 depth completion과 embodied AI에 주는 효과 |
| Infinite Worlds with Versatile Interactions | 월드 모델이 긴 상호작용과 실시간 응답을 동시에 달성할 수 있는가? | LingBot-World 2.0, 실시간 variant, agentic harness | world modeling과 VLM/VLA가 만나는 지점 |

## 상세 정리

### 1. 네이티브 문서 비주얼 사전학습

대상 논문: Scalable Visual Pretraining for Language Intelligence

이 논문은 문서와 웹 페이지를 plain text로 바꾸는 전처리 관습을 의심합니다. 수식의 2차원 배치, 그림 캡션과 본문의 관계, 표의 행과 열, 다이어그램의 위상 구조는 텍스트만으로는 충분히 보존되지 않습니다.

핵심 아이디어는 시각 문서 자체를 사전학습 데이터로 사용하는 것입니다. 모델은 OCR로 추출된 문자열이 아니라 페이지 이미지에서 얻은 시각 표현을 학습합니다. 사용자가 제공한 설명의 "Next-Visual-Latents"는 이런 방향을 쉽게 이해시키는 표현입니다. 중요한 것은 다음 단어 예측만이 아니라, 다음 시각 표현 또는 가려진 시각 구조를 예측하는 학습 목표가 언어 지능에도 도움이 될 수 있다는 점입니다.

학습 관점에서 이 논문은 "텍스트가 지식의 전부가 아니다"라는 질문을 던집니다. 특히 과학 문서, 수학 문서, 기술 보고서처럼 레이아웃과 기호 배치가 의미를 담는 분야에서 중요합니다.

실무적으로는 문서 RAG, 논문 분석, 특허 문서, 재무 보고서, 수학 교재 처리에서 OCR 텍스트만 색인하는 방식의 한계를 다시 검토하게 만듭니다.

### 2. 장문 문서 OCR과 상수 KV 캐시

대상 논문: Unlimited OCR Works

문서 OCR VLM은 입력 이미지 인코더와 텍스트 디코더를 결합합니다. 입력 쪽 이미지는 강하게 압축할 수 있지만, 출력 쪽 디코더는 문서를 길게 전사할수록 KV 캐시가 증가합니다. 수십 페이지를 한 번에 처리하려 할 때 이 증가가 메모리 초과와 속도 저하를 만듭니다.

Unlimited OCR의 핵심은 Reference Sliding Window Attention입니다. 디코더가 모든 과거 출력 토큰을 계속 들고 가는 대신, 고정된 참조 토큰과 최근 출력 창을 중심으로 attention을 계산합니다. 이렇게 하면 출력 길이가 늘어나도 캐시 크기를 통제할 수 있습니다.

이 방식은 "긴 문서 전체를 한 번에 읽는 OCR"이라는 실용적 문제와 직접 연결됩니다. 다만 슬라이딩 윈도우는 멀리 떨어진 출력 토큰 간 의존성을 어떻게 보존할지, 문서 구조 오류가 누적될 때 어떻게 복구할지 같은 평가가 중요합니다.

### 3. 통합 멀티모달 생성

대상 논문: Vision as Unified Multimodal Generation

SenseNova-Vision은 컴퓨터 비전 과제를 통합 멀티모달 생성 문제로 재정의합니다. 물체 검출은 좌표와 레이블을 텍스트로 생성할 수 있고, 세그멘테이션이나 깊이 추정은 이미지 또는 마스크 형태로 생성할 수 있습니다. 복합 태스크는 텍스트와 이미지를 섞은 출력으로 표현할 수 있습니다.

이 접근의 장점은 모델 구조가 단순해진다는 점입니다. 태스크마다 전용 헤드를 붙이는 대신 자연어 지시, 시각 프롬프트, 출력 규약을 통해 한 모델이 다양한 태스크를 수행합니다.

그러나 어려운 점도 분명합니다. 좌표, 마스크, 깊이 맵 같은 출력은 평가 방식이 서로 다르고, 생성 결과가 형식적으로 유효해야 합니다. 통합 모델을 만들려면 데이터셋을 instruction-response 형태로 일관되게 바꾸는 작업이 매우 중요합니다.

### 4. 조밀 공간 지각과 경계 중심 사전학습

대상 논문: Vision Pretraining for Dense Spatial Perception

대형 비전 파운데이션 모델은 객체 분류나 의미 추론에는 강하지만, 물리적 공간 구조에는 약할 수 있습니다. 예를 들어 "컵이 있다"는 것은 알아도, 컵의 경계가 어디이고 배경과 깊이가 어떻게 갈라지는지 정확히 알아야 로봇이 물체를 잡을 수 있습니다.

이 논문은 경계와 형태 불연속이 공간 지각의 핵심 단서라고 봅니다. Masked Boundary Modeling은 이미지의 일부 경계 정보를 가리고 복원하도록 학습합니다. 단순 픽셀 복원보다 "어디에서 물체와 표면이 갈라지는가"에 집중하는 사전학습입니다.

이 카테고리는 VLM이 언어 답변을 잘하는 수준에서 물리 세계를 다루는 수준으로 넘어가는 데 필요합니다.

### 5. 상호작용형 월드 모델과 에이전트 루프

대상 논문: Infinite Worlds with Versatile Interactions

이 논문은 좁은 의미의 문서 VLM이라기보다 월드 모델과 embodied/agentic AI에 가깝습니다. 그래도 최신 멀티모달 연구 흐름에서 중요합니다. 모델이 비디오 세계를 생성하고, 사용자의 행동이나 텍스트 이벤트에 반응하며, 긴 시간 동안 품질을 유지해야 하기 때문입니다.

LingBot-World 2.0은 긴 상호작용 지평, 실시간 720p 60fps 변형, 다양한 행동 이벤트, agentic harness를 강조합니다. 특히 pilot agent와 director agent라는 역할 분리는 "월드를 보는 모델"에서 "월드 안에서 계획하고 변형하는 시스템"으로 이동하는 신호입니다.

VLM 학습 관점에서는 시각 입력을 이해하는 능력, 행동을 조건으로 미래 시각 상태를 예측하는 능력, 사용자와 환경의 닫힌 루프 상호작용을 함께 보아야 합니다.

## 용어 정리

| 용어 | 뜻 | 이 문서에서의 역할 |
|---|---|---|
| VLM | 이미지와 텍스트를 함께 처리하는 모델 | 전체 주제 |
| Visual Pretraining | 시각 데이터를 직접 사용한 사전학습 | 문서 이미지와 레이아웃 학습 |
| Autoregressive | 이전 출력에 조건을 걸어 다음 출력을 순서대로 생성 | 문서 전사, 생성형 비전 태스크 |
| KV Cache | 디코더 attention 계산을 위해 저장하는 key/value 텐서 | 장문 OCR 메모리 병목 |
| R-SWA | Reference Sliding Window Attention | Unlimited OCR의 메모리 절감 핵심 |
| Task-specific Head | 태스크별 전용 출력 모듈 | 통합 생성 모델이 줄이려는 구조 |
| Serialization | 좌표, 마스크, 포즈 같은 출력을 시퀀스나 이미지 포맷으로 바꾸는 것 | SenseNova-Vision의 핵심 데이터 설계 |
| Masked Boundary Modeling | 경계 단서를 가리고 복원하는 자기지도 학습 | 공간 지각용 사전학습 목표 |
| Dense Spatial Perception | 픽셀 또는 패치 수준의 깊이, 경계, 표면, 좌표 인식 | 로봇/자율주행/3D 이해 |
| World Model | 환경의 상태 변화와 미래 장면을 예측하거나 생성하는 모델 | 상호작용형 에이전트 연구 |
| Agentic Harness | 모델을 계획, 실행, 검증 루프로 감싸는 실행 구조 | Infinite Worlds의 상호작용 제어 |

## 실습 학습 가이드

이 폴더의 실습 파일은 외부 대형 모델을 다운로드하지 않고도 핵심 아이디어를 이해하도록 설계했습니다. 모든 예제는 작은 toy data로 동작합니다.

| 파일 | 목적 | 핵심 실습 |
|---|---|---|
| `01_foundations.ipynb` | VLM 트렌드와 논문 카테고리의 기본 구조 이해 | 논문 메타데이터 정리, 카테고리 태그, 비주얼 토큰과 텍스트 토큰 차이 |
| `02_practice.ipynb` | 장문 OCR과 통합 생성 포맷을 직접 모델링 | KV 캐시 메모리 추정, R-SWA 창 크기 실험, detection/depth 출력 시리얼라이즈 |
| `03_advanced.ipynb` | 세 가지 핵심 패러다임을 작은 알고리즘으로 재현 | visual pretraining toy objective, masked boundary modeling, agentic world loop |

## 다음 학습 경로

1. 문서 VLM과 OCR 계열을 먼저 학습합니다.
   - Nougat, Donut, Pix2Struct, DeepSeek-OCR, MinerU, PaddleOCR-VL 같은 문서 이해 모델 흐름을 비교합니다.
   - OCR 텍스트 추출형 RAG와 이미지 기반 문서 RAG의 실패 사례를 모읍니다.

2. 통합 생성형 비전 모델을 학습합니다.
   - detection을 JSON이나 텍스트 시퀀스로 출력하는 방식, segmentation mask를 이미지로 생성하는 방식, depth map을 dense output으로 생성하는 방식을 비교합니다.
   - 출력 검증기와 후처리기를 함께 설계하는 습관이 중요합니다.

3. 공간 지각과 VLA로 확장합니다.
   - depth, surface normal, camera pose, 3D reconstruction을 익힙니다.
   - 이후 로봇 조작 제어와 연결되는 VLA, GUI 조작 에이전트, 실시간 world model을 이어서 보면 좋습니다.

## 확인 필요 사항

- Hugging Face Trending의 순위와 upvote는 시간에 따라 바뀌므로, 후속 업데이트에서는 같은 날짜의 스냅샷이나 별도 로그를 남기는 것이 좋습니다.
- arXiv 논문은 기술 보고서 형태가 많습니다. 정식 학회 채택 여부를 따로 확인해야 합니다.
- 일부 논문은 모델과 코드가 공개되어 있지만, 라이선스, 모델 크기, GPU 요구량은 각 저장소의 최신 README를 다시 확인해야 합니다.
