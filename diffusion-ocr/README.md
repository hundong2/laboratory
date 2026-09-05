<!-- rumdl-disable MD013 -->

# Diffusion OCR와 Self-Speculative Decoding

작성일: 2026-09-05
원문 확인일: 2026-09-05

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [학습 방법](#학습-방법)
- [추론 알고리즘](#추론-알고리즘)
- [결과 읽기](#결과-읽기)
- [한계와 재현 주의점](#한계와-재현-주의점)
- [Reference 논문 아카이브](#reference-논문-아카이브)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 원문: [Diffusion으로 OCR 디코딩 가속하기](https://blog.trillionlabs.co/posts/diffusion-ocr/)
- 저자·게시일: 김형국, 2026-08-28
- 원문 언어: 한국어
- 확인 범위: 본문 전체, 표 2개, 그림 설명 6개, Reference와 연결 논문
- 학습용 재구성본: [translation.ko.md](translation.ko.md)
- Reference 분석: [archive/README.md](archive/README.md)

원문이 이미 한국어이므로 `translation.ko.md`는 문장을 복제한 번역이 아니라 원문 구조를 따라 개념과 실험을 교정·재구성한 한국어 학습본이다. 블로그가 예고한 technical report, model weight와 code는 확인 시점에도 `TBD`다. 아래 수치와 동일 출력 주장은 블로그의 저자 보고이며 공개 코드로 독립 재현한 값이 아니다.

## 한눈에 보기

OCR 생성은 이미지가 정답의 강한 조건이므로 일반 자유 생성보다 여러 토큰을 동시에 예측하기 쉽다. 하지만 같은 diffusion step에서 선택한 토큰들은 서로의 새 값을 보지 못해 누락·중복이 생길 수 있다. 블로그의 해법은 **같은 모델의 block-diffusion 경로가 초안을 만들고 autoregressive(AR) 경로가 가장 긴 일치 prefix만 승인하는 self-speculative decoding**이다.

```text
확정 prefix + MASK 32개
        │
        ├─ bidirectional draft forward ─ 후보 d1...d32
        │
        └─ causal verify forward ─────── 기준 a1...a32
                         │
              최장 일치 prefix + 첫 AR 불일치 토큰 확정
                         │
                    다음 round 반복
```

초안이 틀리면 품질을 낮추는 대신 해당 round의 수락 길이가 짧아진다. Greedy decoding에서 승인 토큰이 항상 같은 checkpoint의 AR 경로와 일치하므로 최종 byte sequence를 보존한다는 것이 핵심 주장이다.

## 기초 개념

### AR decoding

왼쪽에서 오른쪽으로 한 토큰씩 생성한다. 출력 길이가 `N`이면 보통 `N`회의 decode forward가 필요하지만 이미 확정한 prefix의 key-value(KV) cache를 재사용할 수 있다.

### Masked discrete diffusion

가우시안 노이즈 대신 `[MASK]`를 사용한다. 모델이 여러 빈칸의 분포를 동시에 예측하고 confidence가 높은 위치부터 확정한다. 병렬성은 높지만 미확정 위치가 서로를 보는 문맥이 매 step 변해 cache 재사용이 어렵고, 동시에 고른 토큰 사이의 의존성을 놓칠 수 있다.

### Block diffusion

전체 출력을 일정한 블록으로 나눈다. 이전 블록에는 causal 관계와 KV cache를 유지하고 현재 블록 안에서만 bidirectional attention을 허용한다. AR의 cache 효율과 diffusion의 블록 내 병렬성을 절충한다.

### Speculative decoding

빠른 drafter가 여러 토큰을 제안하고 target/verifier 모델이 한 번에 검사한다. 원래 방식은 작은 별도 drafter를 사용하지만, self-speculation은 한 checkpoint의 다른 계산 경로나 일부 계층을 drafter로 사용한다.

## 학습 방법

GLM-OCR 0.9B를 하나의 backbone과 LM head로 AR과 block diffusion 양쪽에서 동작하도록 fine-tune한다. 같은 정답 sequence에서 다음 view를 함께 만든다.

| View | Attention | Loss | 목적 |
| --- | --- | --- | --- |
| Clean | token-level causal | 모든 응답 위치의 AR loss | 기존 AR 분포 보존 |
| Corrupted A | 현재 블록 bidirectional, 이전 clean block 참조 | mask 위치의 diffusion loss | 블록 병렬 복원 |
| Corrupted B | A와 보완적인 mask ratio | A에서 남긴 위치의 diffusion loss | 응답 토큰을 한 번씩 감독 |

두 corrupted stream은 `t`와 `1-t`의 보완 마스킹을 사용한다. 현재·미래 clean answer를 보지 못하게 막아 정답 누출을 피한다. 이미지와 prompt는 항상 clean이며 별도 drafter parameter 대신 필요할 경우 `[MASK]` embedding만 추가한다.

블로그는 AR auxiliary loss가 AR 능력을 보존할 뿐 아니라 diffusion 품질에도 도움이 되었고, 블록 전체를 항상 가리는 것보다 여러 mask ratio를 섞는 학습이 더 좋았다고 보고한다.

## 추론 알고리즘

블로그의 기본 block size는 `B=32`다.

1. **Draft**: 확정 prefix 뒤에 MASK `B`개를 붙이고 블록 내부 bidirectional forward로 후보 `d_1...d_B`를 만든다.
2. **Verify**: 같은 prefix에 causal forward를 수행해 AR 예측 `a_1...a_B`를 얻는다.
3. `d_i = a_i`가 연속으로 성립하는 최장 prefix를 확정한다.
4. 첫 불일치 위치가 있으면 그 위치의 AR token도 함께 확정해 round가 항상 전진하게 한다.
5. EOS 또는 길이 한도까지 반복한다.

수락한 token은 causal path의 token이므로 해당 prefix의 KV cache를 유지할 수 있다. Bidirectional draft의 cache는 버린다. Sampling에서는 단순 동일성 비교가 아니라 speculative rejection rule이 필요하다.

## 결과 읽기

### 모델 간 페이지 처리 비교

블로그는 OmniDocBench v1.6 1,651페이지의 공식 품질 protocol과 영어 페이지의 H100 1장·single-stream 측정을 사용했다고 설명한다.

| Model | Decode | Overall ↑ | pages/s ↑ |
| --- | --- | ---: | ---: |
| MinerU2.5-Pro 1.2B | AR | 95.57 | 0.399 |
| HunyuanOCR-1.5 | AR | 95.52 | 0.313 |
| HunyuanOCR-1.5 + DFlash | speculative | 미보고 | 0.579 |
| GLM-OCR base 0.9B | AR | 95.48 | 0.571 |
| GLM-OCR base 0.9B | MTP | 미보고 | 0.472 |
| PaddleOCR-VL | AR | 94.86 | 0.389 |
| MinerU-Diffusion | diffusion | 89.87 | 0.059 |
| 블로그 제안 모델 0.9B | self-spec | 95.16 | **0.781** |

파이프라인 경계가 다른 모델을 pages/s 하나로만 순위화하면 안 된다. 특히 HunyuanOCR은 full-page 경로라 레이아웃 처리 조건이 다르다는 주의가 원문에도 있다.

### 같은 checkpoint의 decode 구간

| Decode | decode-only tok/s | end-to-end tok/s | speedup |
| --- | ---: | ---: | ---: |
| AR | 739 | 442 | 기준 |
| self-spec | 2,846 | 816 | 3.85× / 1.85× |

페이지 전체 pipeline에서는 0.581→0.781 pages/s로 1.34×다. Vision encode와 prefill 같은 고정 비용은 speculation으로 줄지 않기 때문에 decode-only, crop end-to-end, page pipeline의 배율이 서로 다르다.

평균 draft 연속 일치는 약 19 token이고 두 forward당 평균 확정량은 9.6 tokens/forward다. 긴 구조 출력일수록 효과가 컸으며 블로그 보고 수락 길이는 table 25.4, formula 20.7, 자유 text 16.9였다. Batch가 커져 GPU가 포화되면 이점은 batch 1의 1.85×에서 최대 처리량 비교 1.08×로 줄었다.

### 정확도-병렬성 비교

같은 diffusion checkpoint를 검증 없이 사용할 때 threshold 0.7은 Overall 86.17과 9.59 tokens/forward, threshold 0.99는 93.23과 5.40이었다. Self-speculation은 95.16과 9.60을 보고해, confidence threshold만 높이는 대신 AR 검증에 forward를 쓰는 편이 이 실험에서 우세했다. 변환 전 GLM-OCR 95.48과 비교하면 최종 품질은 약 0.32점 낮으며 차이 대부분이 표 TEDS에서 나타났다.

## 한계와 재현 주의점

- technical report, weight, code가 아직 공개되지 않아 training data, optimizer, 정확한 SGLang kernel과 모든 측정 protocol을 재현할 수 없다.
- 동일 AR 결과 주장은 greedy byte equality의 저자 검증이다. 공개 artifact가 나오기 전 독립 검증이 필요하다.
- Cross-model pages/s는 tokenizer 차이를 줄이지만 preprocessing, layout, crop, maximum output, kernel 성숙도 차이를 모두 제거하지 못한다.
- H100 single-stream 결과는 latency 중심이다. 큰 batch와 지속 처리 환경에서는 이득이 크게 줄 수 있다.
- one-shot draft가 최선이라는 결과는 OCR·해당 checkpoint·block size에 조건부다.
- 표와 수식의 긴 구조 출력은 수락률이 높지만 최종 품질 저하도 표에서 컸다. 속도와 domain별 품질을 함께 봐야 한다.
- Sampling 분포 보존은 rejection sampling을 올바르게 구현할 때만 성립한다.

## Reference 논문 아카이브

블로그가 직접 또는 보조로 연결한 실제 논문 12편을 [archive/README.md](archive/README.md)에 정리했다. 각 폴더에는 논문별 한국어 분석, 라이선스 범위에 맞춘 번역·해설, 3단계 toy reproduction이 있다.

## 용어 정리

| 용어 | 설명 |
| --- | --- |
| AR | 이전 token만 조건으로 다음 token을 순차 생성하는 autoregressive 방식 |
| dLLM | 여러 masked token을 반복 복원하는 diffusion language model |
| MTP | 여러 미래 위치를 추가 head로 동시에 예측하는 multi-token prediction |
| Draft | 검증 전 한 번에 제안한 token block |
| Verify | target AR 분포로 draft를 검사하는 단계 |
| Acceptance length | 한 round에서 연속으로 승인된 draft token 수 |
| Tokens/forward | forward 호출당 최종 확정한 token 수 |
| KV cache | 이미 확정한 causal prefix의 attention key/value를 재사용하는 cache |
| TEDS | 표의 tree 구조 유사성을 평가하는 metric |
| OmniDocBench | 문서 parsing의 layout·text·table·formula 등을 평가하는 benchmark |

## 실습 학습 가이드

1. [01_foundations.ipynb](01_foundations.ipynb): AR, full diffusion, block diffusion attention mask를 직접 만든다.
2. [02_practice.ipynb](02_practice.ipynb): deterministic draft-verify-commit loop와 AR 동일성을 검증한다.
3. [03_advanced.ipynb](03_advanced.ipynb): acceptance, 고정 비용, batch 포화가 실제 speedup을 어떻게 제한하는지 모의 실험한다.

모든 실습은 Python 표준 라이브러리만 사용하며 원 모델 결과를 재현하는 것이 아니라 알고리즘의 불변조건과 비용 구조를 확인한다.

## 다음 학습 경로

1. Attention mask 실습으로 정보 누출 조건을 확인한다.
2. Draft 오류 위치를 바꾸며 수락 길이와 AR 동일성이 어떻게 달라지는지 실험한다.
3. Vision/prefill 고정 비용을 바꾸고 어느 출력 길이부터 speculation이 유리한지 계산한다.
4. [archive](archive/README.md)에서 speculative decoding → block diffusion → Fast-dVLM → OCR 전용 모델 순으로 읽는다.
5. 기술 보고서와 코드가 공개되면 checkpoint hash, SGLang version, dataset split과 측정 script를 고정해 독립 재현한다.
