<!-- rumdl-disable MD013 -->

# Diffusion OCR Reference 논문 아카이브

작성일: 2026-09-05

[상위 학습 가이드로 돌아가기](../README.md)

## 범위

블로그 Reference의 실제 논문 12편을 직접 연결한다. 블로그 번호 [1]–[9]의 논문, [8]이 추가로 안내한 Fast-dLLM v2, [10]의 평가 benchmark 원 논문과 최신 protocol을 제시한 MinerU2.5-Pro를 포함한다. Version은 사용자가 별도 지정하지 않아 2026-09-05 기준 arXiv에서 확인 가능한 최신 revision을 사용한다.

## 권장 학습 순서

### 1. 생성과 검증의 기초

1. [Fast Inference from Transformers via Speculative Decoding](speculative-decoding/README.md) - drafter와 target이 분포를 보존하며 가속하는 원리
2. [Large Language Diffusion Models](llada/README.md) - masked discrete diffusion 언어 모델
3. [Block Diffusion](block-diffusion/README.md) - AR과 diffusion 사이의 block factorization

### 2. AR 모델의 diffusion 변환과 hybrid decoding

4. [Fast-dLLM v2](fast-dllm-v2/README.md) - AR checkpoint를 효율적인 block-diffusion LLM으로 변환
5. [Fast-dVLM](fast-dvlm/README.md) - 변환 방식을 vision-language model로 확장
6. [Nemotron-Labs-Diffusion](nemotron-labs-diffusion/README.md) - AR, diffusion, self-speculation의 tri-mode 모델

### 3. OCR 모델

7. [GLM-OCR](glm-ocr/README.md) - 블로그의 0.9B 기반 모델과 MTP baseline
8. [HunyuanOCR-1.5](hunyuanocr-1-5/README.md) - 외부 DFlash diffusion drafter
9. [DODO](dodo/README.md) - discrete OCR diffusion
10. [MinerU-Diffusion](mineru-diffusion/README.md) - inverse rendering 관점의 diffusion OCR

### 4. 평가와 강한 AR baseline

11. [OmniDocBench](omnidocbench/README.md) - 문서 parsing 데이터와 종합 평가 protocol
12. [MinerU2.5-Pro](mineru2-5-pro/README.md) - 블로그가 사용한 최신 protocol과 강한 AR 비교 모델

## Reference 매핑

| 블로그 표기 | arXiv | 최신 확인 version | 역할 |
| --- | --- | --- | --- |
| [1] | [2603.10910](https://arxiv.org/abs/2603.10910) | v2 | GLM-OCR와 MTP |
| [2] | [2607.04884](https://arxiv.org/abs/2607.04884) | v2 | HunyuanOCR와 DFlash |
| [3] | [2602.16872](https://arxiv.org/abs/2602.16872) | v2 | OCR discrete diffusion |
| [4] | [2603.22458](https://arxiv.org/abs/2603.22458) | v1 | OCR diffusion inverse rendering |
| [5] | [2502.09992](https://arxiv.org/abs/2502.09992) | v3 | LLaDA |
| [6] | [2607.05722](https://arxiv.org/abs/2607.05722) | v1 | Tri-mode self-speculation |
| [7] | [2604.06832](https://arxiv.org/abs/2604.06832) | v2 | AR VLM→block diffusion |
| [8] | [2503.09573](https://arxiv.org/abs/2503.09573) | v3 | Block diffusion 이론·모델 |
| [8] 보조 | [2509.26328](https://arxiv.org/abs/2509.26328) | v1 | Fast-dLLM v2 변환 recipe |
| [9] | [2211.17192](https://arxiv.org/abs/2211.17192) | v2 | Speculative decoding |
| [10] benchmark | [2412.07626](https://arxiv.org/abs/2412.07626) | v2 | OmniDocBench 원 논문 |
| [10] protocol | [2604.04771](https://arxiv.org/abs/2604.04771) | v2 | MinerU2.5-Pro |
