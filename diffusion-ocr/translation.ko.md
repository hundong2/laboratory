<!-- rumdl-disable MD013 -->

# Diffusion으로 OCR 디코딩 가속하기 - 한국어 학습용 재구성본

작성일: 2026-09-05

## 원문 정보

- 원문: [Trillion Labs Research 블로그](https://blog.trillionlabs.co/posts/diffusion-ocr/)
- 제목: Diffusion으로 OCR 디코딩 가속하기
- 저자·게시일: 김형국, 2026-08-28
- 원문 언어: 한국어
- 접근일: 2026-09-05

[종합 분석으로 돌아가기](README.md) · [Reference 논문 아카이브](archive/README.md)

## 재구성 범위

원문이 한국어이므로 중복 복사 대신 원문의 문제 제기, 기초 설명, 방법, 실험과 결론 순서를 유지한 교정·학습용 재구성본을 제공한다. 표의 수치와 모델명은 보존하되 본문 표현과 비유는 그대로 재현하지 않았다. 원문에서 예고한 technical report·모델 weight·code는 확인 시점에 링크가 아직 `TBD`다.

## 1. 문제: 생성 OCR의 병목은 긴 출력이다

문서 OCR 모델은 이미지에서 본문, HTML table, LaTeX formula를 하나의 긴 token sequence로 만든다. AR decoder는 token마다 forward를 요구하므로 인식 정확도가 충분히 높아진 뒤에는 decode latency와 serving cost가 새로운 병목이 된다.

최근 가속 방식은 크게 세 갈래다.

- GLM-OCR처럼 본 모델에 MTP head를 추가한다.
- HunyuanOCR-1.5의 DFlash처럼 작은 외부 diffusion drafter를 둔다.
- DODO와 MinerU-Diffusion처럼 본 생성을 discrete diffusion으로 수행한다.

블로그의 접근은 GLM-OCR 0.9B 하나를 AR과 block diffusion 양쪽으로 사용한다. Diffusion path가 block 초안을 만들고 같은 weight의 AR path가 검사한다.

## 2. Diffusion language model의 직관

Masked discrete diffusion은 모든 빈칸을 동시에 예측하고 confidence가 높은 일부를 채운 다음, 남은 mask를 반복해서 복원한다. AR은 왼쪽 token만 볼 수 있어 순차적이지만 prefix KV cache가 가능하다. Full diffusion은 block 전체를 서로 보게 해 병렬적이지만 문맥 변화 때문에 cache가 어렵다.

Block diffusion은 이전 block을 causal prefix로 고정하고 현재 block만 bidirectional하게 연다. 완료한 block의 KV cache는 유지하면서 현재 `B`개 위치를 병렬로 제안할 수 있다.

## 3. OCR이 병렬 초안에 유리한 이유

자유 text의 다음 token은 앞 문장에 크게 의존하지만 OCR의 출력은 이미지에 이미 보이는 문자와 구조에 강하게 결정된다. 따라서 앞 token이 아직 미확정이어도 여러 위치를 올바르게 맞힐 가능성이 높다. 블로그는 변환 모델의 draft가 AR decoder와 round당 평균 약 19 token 연속 일치했다고 보고한다.

하지만 같은 diffusion step에서 고른 token은 서로의 새 값을 조건으로 보지 못한다. 이 때문에 중간 단어가 빠지거나 관사가 반복되는 등 국소적인 상호의존 오류가 생긴다. Confidence threshold를 높이면 오류는 줄지만 병렬 확정량도 감소한다.

## 4. 한 모델에서 AR과 diffusion을 함께 학습

정답 sequence로 clean stream 하나와 corrupted stream 두 개를 만든다.

- Clean stream은 causal attention과 AR loss를 유지한다.
- Corrupted stream은 현재 block의 일부를 mask하고 block 안에서 bidirectional attention을 쓴다.
- Corrupted block은 이전 clean block만 참조하며 현재와 미래의 정답 token은 볼 수 없다.
- 두 corrupted stream의 mask ratio를 `t`, `1-t`로 만들어 모든 응답 token이 한 번씩 diffusion loss를 받게 한다.

Image와 prompt는 항상 clean하다. 세 stream이 같은 decoder와 LM head를 지나므로 별도 draft model이 필요하지 않으며 기존 vocabulary에 없을 때 mask embedding만 추가한다.

## 5. Draft와 AR verification

한 round는 두 forward로 구성된다.

1. 확정 prefix 뒤에 `B=32`개의 mask를 붙여 bidirectional draft를 만든다.
2. 같은 prefix의 causal path가 다음 `B`개 AR token을 예측한다.
3. 두 sequence가 앞에서부터 같은 구간을 승인한다.
4. 첫 불일치에서는 AR token을 하나 승인한다.

Draft가 정확하면 두 forward로 여러 token을 확정한다. 틀리면 승인량이 짧아질 뿐 AR 결과와 다른 draft token이 출력에 들어가지 않는다. Greedy에서는 byte-level AR 결과를 보존할 수 있고 sampling에서는 정식 speculative rejection rule이 필요하다.

## 6. 다른 가속 방식과의 차이

| 방식 | Drafter | Verifier | 추가 parameter |
| --- | --- | --- | --- |
| 외부 draft model | 별도 소형 model | 본 model | 별도 model 필요 |
| MTP | 여러 future head | 없거나 main head | MTP head |
| Self-speculation | 같은 model의 diffusion path | 같은 model의 AR path | mask embedding 정도 |

Self-speculation은 별도 model의 배포·동기화 비용을 없애지만 한 model이 두 decoding mode를 안정적으로 수행하도록 추가 학습해야 한다.

## 7. 성능 결과

블로그의 H100 batch 1 결과에서 같은 checkpoint의 self-spec decode-only 처리량은 739에서 2,846 tok/s로 3.85배, vision encode와 prefill을 포함한 crop end-to-end는 442에서 816 tok/s로 1.85배다. Page pipeline은 0.581에서 0.781 pages/s로 1.34배다.

OmniDocBench Overall은 self-spec 모델 95.16, 변환 전 GLM-OCR 95.48로 약 0.32점 차이다. Text edit와 reading order는 같았고 표 TEDS가 0.934에서 0.928로 내려가 차이의 대부분을 차지했다.

Table처럼 길고 구조가 강한 출력은 draft 수락 길이와 속도 향상이 컸다. 반면 batch를 크게 해 AR도 GPU를 충분히 사용하면 최대 처리량 차이는 1.08배까지 줄었다. 따라서 이 방식은 긴 출력과 low-batch latency가 중요한 환경에 특히 적합하다.

## 8. 추가 관찰

한 block을 여러 denoising step으로 다듬으면 acceptance length는 늘지만 extra forward가 더 빨리 증가했다. 이 OCR 설정에서는 one-shot draft의 tokens/forward가 가장 높았다. 또한 AR auxiliary loss를 함께 둔 것이 diffusion 품질에도 도움이 됐고, 고정된 full-block mask보다 다양한 mask ratio 학습이 더 좋았다고 보고한다.

## 9. 검증이 필요한 지점

- 공개 예정 technical report와 code가 없어 세부 학습 recipe를 확인할 수 없다.
- 모델별 전체 pipeline 조건이 달라 cross-model pages/s는 제한적으로 비교해야 한다.
- Byte equality와 sampling 분포 보존을 공개 구현으로 독립 검증해야 한다.
- Batch, output length, document domain, kernel에 따라 이득이 달라진다.
- 표 영역의 작은 품질 하락이 실제 업무 비용에 미치는 영향을 별도로 평가해야 한다.

## 10. 참고문헌 읽기 순서

개념 기반은 [speculative decoding](archive/speculative-decoding/README.md), [LLaDA](archive/llada/README.md), [Block Diffusion](archive/block-diffusion/README.md)이다. 변환·hybrid 계열은 [Fast-dLLM v2](archive/fast-dllm-v2/README.md), [Fast-dVLM](archive/fast-dvlm/README.md), [Nemotron-Labs-Diffusion](archive/nemotron-labs-diffusion/README.md)을 읽는다. OCR 적용은 [GLM-OCR](archive/glm-ocr/README.md), [HunyuanOCR-1.5](archive/hunyuanocr-1-5/README.md), [DODO](archive/dodo/README.md), [MinerU-Diffusion](archive/mineru-diffusion/README.md)이며 평가는 [OmniDocBench](archive/omnidocbench/README.md)와 [MinerU2.5-Pro](archive/mineru2-5-pro/README.md)로 연결된다.
