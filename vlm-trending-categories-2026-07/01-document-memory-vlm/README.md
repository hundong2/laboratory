# 문서/메모리 VLM

작성일: 2026-07-17

## 출처와 작업 범위

이 카테고리는 긴 문서, 고해상도 페이지, 문서 이미지 레이아웃, 선택적 읽기 전략을 다룹니다.

포함 논문:

- Unlimited OCR Works: https://arxiv.org/abs/2606.23050
- Scalable Visual Pretraining for Language Intelligence: https://arxiv.org/abs/2607.09657
- SCoPE VLM: https://aclanthology.org/2026.eacl-long.6/

## 한눈에 보기

| 논문 | 병목 | 핵심 아이디어 | 실무 적용 |
|---|---|---|---|
| Unlimited OCR | 긴 출력에서 KV 캐시 증가 | R-SWA로 참조 토큰과 최근 출력 창 유지 | 장문 OCR, PDF 파싱 |
| Scalable Visual Pretraining | OCR 텍스트화로 레이아웃 손실 | 원본 시각 문서 직접 사전학습 | 과학 문서 RAG, 수식 문서 이해 |
| SCoPE VLM | 긴 문서 전체 인코딩 비용 | Chain of Scroll로 관련 구간만 선택 읽기 | GUI, 웹, 슬라이드 QA |

## 기초 개념

### KV 캐시

트랜스포머 디코더가 이전 출력 토큰의 key/value를 저장하는 메모리입니다. 출력이 길수록 일반적인 KV 캐시는 커집니다. OCR은 문서 전체를 Markdown이나 텍스트로 길게 생성하므로 이 병목이 크게 나타납니다.

### 참조 슬라이딩 윈도우

문서 이미지와 프롬프트 같은 참조 토큰은 유지하고, 이미 생성한 출력은 최근 일부만 유지하는 방식입니다. 이렇게 하면 출력 길이가 늘어도 메모리 증가를 제한할 수 있습니다.

### 네이티브 비주얼 사전학습

문서를 텍스트로 변환하지 않고 이미지 상태로 학습하는 접근입니다. 수식, 표, 다이어그램, 레이아웃 같은 2D 구조를 보존하는 데 유리합니다.

### Chain of Scroll

긴 문서에서 필요한 부분만 스크롤하며 찾는 agentic reading 전략입니다. 모든 페이지를 한 번에 인코딩하는 대신, 질문에 필요한 구간을 순차적으로 탐색합니다.

## 상세 정리

Unlimited OCR은 출력 측 메모리 병목을 해결합니다. 입력 이미지를 얼마나 잘 압축하더라도 디코더가 수만 개의 출력 토큰을 만들면 KV 캐시가 커집니다. R-SWA는 이 문제를 attention 구조에서 직접 다룹니다.

Scalable Visual Pretraining은 입력 표현의 손실을 다룹니다. OCR이 만든 plain text는 문서 구조를 단순화합니다. 특히 과학 문서의 수식 배치, 표 구조, 그림-본문 관계는 이미지 상태에서 더 잘 남습니다.

SCoPE VLM은 읽기 정책의 문제를 다룹니다. 긴 문서를 모두 보는 모델보다, 질문에 맞춰 필요한 구간을 찾아 읽는 모델이 메모리와 추론 비용 측면에서 실용적일 수 있습니다.

## 용어 정리

| 용어 | 뜻 |
|---|---|
| OCR | 이미지 속 문자를 텍스트로 변환하는 작업 |
| Document AI | 문서 구조, 텍스트, 표, 이미지 정보를 함께 처리하는 분야 |
| KV cache | 디코더 attention 계산을 위해 저장하는 key/value 텐서 |
| R-SWA | Reference Sliding Window Attention |
| Visual Pretraining | 이미지/문서 시각 표현을 직접 쓰는 사전학습 |
| Chain of Scroll | 문서의 관련 영역을 선택적으로 스크롤하며 탐색하는 방식 |

## 실습 학습 가이드

`01_foundations.ipynb`에서는 세 가지 toy 실험을 합니다.

1. KV 캐시가 출력 길이에 따라 어떻게 커지는지 계산합니다.
2. plain text와 좌표가 있는 문서 토큰의 차이를 비교합니다.
3. 질문에 맞춰 문서 구간을 선택하는 간단한 Chain of Scroll을 구현합니다.

## 다음 학습 경로

- Donut, Nougat, Pix2Struct, DeepSeek-OCR 계열을 먼저 비교합니다.
- vLLM의 KV 캐시 관리와 PagedAttention을 함께 공부합니다.
- 문서 RAG에서는 OCR 텍스트, 레이아웃 OCR, 이미지 embedding을 각각 색인했을 때의 실패 사례를 모아봅니다.
