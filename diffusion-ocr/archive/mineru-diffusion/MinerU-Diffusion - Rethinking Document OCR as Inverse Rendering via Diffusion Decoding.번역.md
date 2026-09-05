# MinerU-Diffusion: Rethinking Document OCR as Inverse Rendering via Diffusion Decoding - 제한적 대조 번역과 상세 해설

## 논문 metadata

- 원문 제목: **MinerU-Diffusion: Rethinking Document OCR as Inverse Rendering via Diffusion Decoding**
- 저자: Hejun Dong, Junbo Niu, Bin Wang, Weijun Zeng, Wentao Zhang, Conghui He
- 출판처/연도: arXiv preprint (cs.CV), 2026
- 식별자: arXiv:2603.22458, DOI 10.48550/arXiv.2603.22458
- 원문: <https://arxiv.org/abs/2603.22458>
- 사용 버전: v1 (2026-03-23)
- 원문 언어: 영어
- 접근일: 2026-09-05
- 확인 가능한 라이선스: [arXiv non-exclusive license to distribute 1.0](https://arxiv.org/licenses/nonexclusive-distrib/1.0/)
- 저작권·접근 제한: 위 라이선스는 arXiv에 배포권을 주지만 제3자에게 전문 번역·개작권을 허여하지 않는다. 따라서 짧은 원문 한 문장만 대조하고 나머지는 원문을 복제하지 않는 한국어 해설로 작성했다.

[분석 README로 돌아가기](README.md)

## 번역·접근 범위

| 구간 | 상태 | 이 문서의 처리 |
|---|---|---|
| 제목·초록 | 부분 번역 | 짧은 핵심 문장 1개 대조, 나머지 상세 요약 |
| 1 Introduction | 부분 번역 | 한국어 논증 해설 |
| 2 Related Works | 부분 번역 | 연구 계보 요약 |
| 3 Method | 부분 번역 | 수식 보존과 상세 해설 |
| 4 Experiments | 부분 번역 | 설정·표 수치 해설 |
| 5 Conclusion | 부분 번역 | 저자 결론 요약 |
| References | 원문 확인 | 서지 레코드 미복제 |
| Appendix A-D | 부분 번역 | 학습 설정·prompt·ablation·정성 예시 해설 |

PDF 33/33쪽을 텍스트 추출하고 렌더링해 확인했지만, 이 파일은 전문 번역이 아니다. 완전한 문장 대조 번역이 필요하면 저작권자의 허가 또는 재사용 가능한 라이선스가 확인되어야 한다.

## 읽기 전 핵심 배경

렌더링은 구조화된 문서 표현을 이미지로 만드는 과정이다. 역렌더링은 이미지에서 다시 text, layout, table, formula representation을 추론한다. 저자들은 이 관점에서 1차원 직렬화 순서는 저장·출력 편의를 위한 artifact일 뿐, 토큰 간 본질적 관계는 2차원 공간과 포맷 제약에서 온다고 본다.

## 허용 범위의 짧은 문장 대조

### Abstract 핵심 주장

**S001 — Original**

We propose MinerU-Diffusion, a unified diffusion-based parsing framework tailored for document OCR.

**S001 — 한국어**

(저자들은 문서 OCR에 맞춘 통합 확산 기반 파싱 프레임워크 MinerU-Diffusion을 제안한다.)

- **용어·약어 해설**
  - **OCR (Optical Character Recognition, 광학 문자 인식)**: 여기서는 text뿐 아니라 layout, table, formula와 reading order를 구조화해 복원하는 과제를 포함한다.
  - **diffusion-based parsing(확산 기반 파싱)**: 마스킹된 출력 토큰을 이미지 조건 아래 반복·병렬 갱신한다.

## 절별 한국어 해설

### Abstract

저자들은 AR OCR이 긴 구조화 출력에서 순차 지연과 오류 전파를 일으킨다고 본다. MinerU-Diffusion은 visual conditioning 아래 block-wise masked diffusion으로 여러 토큰을 병렬 복원하고, uncertainty 기반 curriculum으로 학습을 안정화한다. 논문은 최대 약 3.2배 decoding 가속과 Semantic Shuffle에서 더 작은 의미 prior 의존을 보고한다.

### 1. Introduction

좋은 OCR은 문맥상 그럴듯한 문장을 쓰기보다 실제 픽셀에 있는 문자를 읽어야 한다. AR factorization은 앞 토큰과 언어 문맥의 영향이 강해, 시각 신호가 약하거나 의미가 깨졌을 때 그럴듯한 내용으로 보완할 위험이 있다. 저자들은 OCR의 조건부 출력이 거의 결정적이므로 마스킹 위치의 조건부 독립 가정이 개방형 텍스트보다 잘 맞는다고 주장한다.

### 2. Related Works

MinerU2.5, PaddleOCR-VL 같은 end-to-end VLM이 pipeline을 단순화했지만 AR의 길이 비례 latency를 남겼다. full-attention dLM은 병렬 갱신이 가능하나 매 step `O(L^2)`이며 긴 출력에서 위치 drift와 반복이 생긴다. block diffusion은 블록 내부 병렬성과 블록 간 anchor를 결합해 이 간극을 줄인다.

### 3.1 Inverse Rendering 수식

출력은 공유 vocabulary `V`의 길이 `L` 토큰열이다.

```text
y = (y^(1), ..., y^(L)) in V^L                                      (3)
```

`V`는 문자만이 아니라 layout marker, table delimiter, math operator까지 포함한다. 1차원 표현이지만 확률적 의존은 주로 공간 배치와 구조 제약에서 나온다는 것이 저자들의 핵심 모델링 가정이다.

### 3.2 Block-wise diffusion

```text
y = (y^(1), ..., y^(B)),  y^(b) in V^(L'),  L = B L'                 (4)
p_theta(y|x) = Π_(b=1..B) p_theta(y^(b)|y^(<b),x)                    (5)
p_theta(y^(b)_(t-1)|y^(b)_t,y^(<b),x)                               (6)
```

블록 `b` 안에서는 마스크 토큰을 양방향으로 함께 복원하고, 이전 블록 `y^(<b)`는 coarse AR prefix다. attention mask는 같은 블록 또는 이전 블록만 허용한다.

```text
M_ij = 1 if b(i)=b(j)
       1 if b(j)<b(i)
       0 otherwise                                                   (7)
```

논문은 full attention의 `O(L^2)`를 block attention의 `O(B L'^2)`로 줄인다고 설명한다. `B=L/L'`라면 고정 block size에서 텍스트 길이에 거의 선형으로 증가하는 직관이다.

### 3.3 Uncertainty-driven curriculum

Stage I은 layout·언어·문서 유형이 다양한 `D_base`로 안정적인 기반을 만든다. Stage II는 같은 입력을 `T`번 stochastic inference해 pairwise task score의 평균 consistency를 계산한다.

```text
C(x) = 2/(T(T-1)) * Σ_(i<j) S(y_hat_i, y_hat_j)                      (10)
D_hard = {x | C(x) < tau}                                            (11)
D_SFT = D_hard_tilde union alpha D_rand                              (13)
w(x) = 1 + beta(1-C(x))                                              (15)
```

불일치가 큰 예는 annotation refinement 후 더 큰 weight로 학습한다. `D_rand` replay는 hard case만 보다가 일반 성능을 잃는 것을 막는다. Stage II만 단독 학습했을 때 성능이 붕괴한 ablation은 curriculum 순서가 단순 데이터 합치기보다 중요함을 보여준다.

### 4.1 Experimental setup

학습 meta data는 약 7.5M이며 중국어·영어 중심이다. decoder는 SDAR-1.7B-Chat-b32, block size 32다. 주 평가에서 dynamic threshold `0.95`, top-k 0, temperature 1.0, top-p 1.0을 사용한다. Overall은 다음처럼 text, formula, table을 동일 비중으로 결합한다.

```text
Overall = ((1 - Text Edit)*100 + Formula CDM + Table TEDS) / 3
```

### 4.2 Full-document parsing

GT layout 없이 Overall `88.94`, GT layout을 주면 `93.37`이다. 후자는 인식기를 더 순수하게 평가하지만 실제 end-to-end layout 오류를 제거하므로 운영 성능처럼 읽으면 안 된다. 저자들은 이 차이를 layout understanding의 남은 병목으로 해석한다.

### 4.3 Table과 formula

Table은 CC-OCR에서 TEDS/TEDS-S `73.77/82.06`, OCRBench v2에서 `81.18/88.66`이다. Formula는 UniMER-Test CPE/HWE/SCE/SPE `91.6/91.6/92.0/96.8`이다. 복잡한 printed expression에서는 MinerU2.5의 `96.6` CPE보다 차이가 있어 symbol-level refinement가 과제로 남는다.

### 4.4 Ablation

- threshold가 0.5에서 0.99로 높아지면 TPF/TPS는 감소한다. `0.95`는 정확도와 효율의 실용 절충점으로 제시된다.
- static 6 step은 `91.56 TPS/88.31 Overall`, static 32 step은 `21.86/93.02`, dynamic `tau=0.97`은 `98.32/93.34`다. 쉬운 토큰은 많이, 어려운 토큰은 적게 확정하는 이점이다.
- full attention은 길이를 과다 할당하면 빈 행을 반복하고 짧게 할당하면 truncation한다. block attention은 block-level EOS와 국소 범위로 이를 완화한다.
- GT layout 없는 curriculum ablation은 Stage 1 `86.13`, Stage 2 only `35.71`, 결합 `88.94`다. hard case만 먼저 주면 안정적 representation 없이 gradient variance가 커진다는 해석이다.

### 4.5 Semantic Shuffle

FOX의 영어 문서 112개에서 일정 비율의 단어를 섞고 같은 형식으로 다시 렌더링한다. 의미가 깨질수록 AR 모델 성능은 크게 감소하지만 diffusion decoder 곡선은 비교적 평탄하다고 보고한다. 이는 visual grounding 가설을 지지하지만, 데이터 규모가 작고 재렌더링 분포에 한정되므로 모든 환각 유형에 대한 증명은 아니다.

### 5. Conclusion

저자들은 2.5B diffusion OCR이 block-level parallel decoding, confidence scheduling, curriculum을 통해 AR의 대안이 될 수 있다고 결론짓는다. 논문이 보여주는 가장 중요한 trade-off는 “완전 병렬”이 아니라 confidence와 block으로 병렬성을 제어해야 정확도를 유지한다는 점이다.

### Appendix A: 학습 recipe

| 단계 | 데이터/규모 | 최대 sequence | 핵심 목적 |
|---|---:|---:|---|
| Stage-0a | LLaVA-Pretrain 550K | 4,096 | MLP adaptor modality alignment |
| Stage-0b | LLaVA-NeXT 739K | 8,192 | 전체 모델 VQA·long visual context |
| Stage-1 | Layout&OCR 6.9M | 12,288 | broad OCR, 9 epoch |
| Stage-2 | Layout&OCR hard 630K | 16,384 | hard-case specialization, 4 epoch |

Vision token budget은 Stage 1/2에서 이미지당 2,048로 제한한다. layout은 full page, recognition은 crop을 써 전역 구조와 국소 전사를 같은 모델에서 다른 입력 형태로 학습한다.

### Appendix B-D

- B: layout, text, formula, table task별 prompt를 공개한다.
- C: full-attention의 짧은/맞는/긴 canvas에서 truncation·반복을 정성·정량 비교한다.
- D: complete parsing과 layout/text/table/formula diffusion step 예시를 제공한다.

## 그림·표를 읽는 법

- Figure 1의 “99.9% relative accuracy”는 절대 점수가 아니라 비교 기준 대비 상대 정확도다.
- Figure 3의 초록 mask 영역은 같은/과거 블록 attention, 빨강은 차단 영역이다. 라벨이 있는 일부 위치만 loss를 계산한다.
- Table 1의 GT Layout 체크 여부를 먼저 보고 점수를 비교해야 한다.
- Figure 7은 추세를 보여주지만 본문 표에 모든 수치가 없으므로 곡선을 눈대중 숫자로 옮기지 않았다.

## 약어 및 기술 용어 사전

| 원어 | 한국어 | 의미 | 최초 등장 |
|---|---|---|---|
| OCR | 광학 문자 인식 | 구조화 문서 역렌더링 과제 | S001 |
| AR | 자기회귀 | 왼쪽에서 오른쪽으로 한 토큰씩 생성 | 배경 |
| dLM | 이산 확산 언어 모델 | 이산 토큰 마스크 복원 모델 | Related Works |
| dVLM | 이산 확산 시각-언어 모델 | 이미지 조건을 결합한 dLM | Method |
| TPF | forward당 토큰 수 | 한 호출에서 확정되는 토큰 수 | Ablation |
| TPS | 초당 토큰 수 | wall-clock 처리량 | Ablation |
| GT Layout | 정답 레이아웃 | oracle region을 제공하는 평가 조건 | Experimental setup |
| TEDS | 트리 편집 유사도 | HTML 표 구조·내용 유사도 | Curriculum |
| CDM | 수식 평가 지표 | formula 일치도를 측정 | Curriculum |
| KV cache | 키-값 캐시 | 확정 prefix attention 상태 재사용 | Block diffusion |

## 번역 검수 기록

- v1 PDF 33/33쪽 렌더링과 본문 1-15쪽, 참고문헌, 부록 A-D의 순서를 확인했다.
- Overall 공식, block mask, consistency와 weighting 수식, threshold별 수치를 원문 표와 대조했다.
- `0.95` main setting과 `0.97` ablation을 분리해 기록했다.
- 비독점 배포 라이선스의 범위를 넘지 않도록 원문 대조는 S001 한 문장으로 제한했다.
