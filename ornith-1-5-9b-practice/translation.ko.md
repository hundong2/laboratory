# Ornith-1.5-9B 설치 가이드 한국어 학습용 재구성본

작성일: 2026-08-24

## 원문 정보

- 제목: 🆓 Ornith-1.5-9B 무료 설치 가이드: 9B로 31B급 따라잡은 자가 개선 코딩
  LLM
- 작성자 표시: James AI Explorer
- 게시일 표시: 2026-08-23
- 원문 URL:
  [Tistory 글](https://fornewchallenge.tistory.com/entry/%F0%9F%86%93-Ornith-15-9B-%EB%AC%B4%EB%A3%8C-%EC%84%A4%EC%B9%98-%EA%B0%80%EC%9D%B4%EB%93%9C-9B%EB%A1%9C-31B%EA%B8%89-%EB%94%B0%EB%9D%BC%EC%9E%A1%EC%9D%80-%EC%9E%90%EA%B0%80-%EA%B0%9C%EC%84%A0-%EC%BD%94%EB%94%A9-LLM)
- 최종 확인 URL: 위 URL에서 `#google_vignette` fragment를 제외한 canonical page
- 원문 언어: 한국어
- 접근일: 2026-08-24

원문이 이미 한국어이므로 이 파일은 같은 문장을 복제하지 않는다. 광고와 제휴
영역을 제외하고 원문의 핵심 section 흐름을 따른 교정·재구성본을 제공한다. 수치와
실행 명령은 [공식 모델 카드](https://huggingface.co/ornith-ai/Ornith-1.5-9B)와
[Ornith 공식 기술 설명](https://ornith.ai/ornith_1_5.html)에 대조했다.

## 모델의 정체

Ornith-1.5-9B는 코딩, reasoning, agentic task를 겨냥한 9B급 dense 모델이다.
Ornith-1.0이 scaffold와 rollout을 개선했다면, 1.5는 task generation까지 학습
loop 안에 포함한다. 모델이 새 학습 문제를 제안하고, 문제별 scaffold를 구성하고,
solution rollout을 만든 뒤 보상으로 세 단계를 함께 개선한다.

여기서 “자가 개선”은 설치한 모델이 사용자의 PC에서 임의로 자기 가중치를 바꾼다는
뜻이 아니다. Ornith 팀이 foundation model을 학습한 방법론을 가리킨다.

## 크기와 배포성

공식 모델 카드 본문은 약 9B dense, BF16 가중치 약 19GB라고 설명한다. Hugging
Face UI는 확인일 현재 모델 크기를 10B params로 표시하므로, 정확한 parameter
count가 필요한 용도에서는 설정 파일과 tensor shape를 확인해야 한다.

19GB 가중치가 들어간다고 해서 20GB GPU에서 262K context를 안정적으로 serving할
수 있는 것은 아니다. KV cache와 runtime overhead가 추가되기 때문이다. 공식
serving recipe는 단일 80GB GPU를 기준으로 한다. 소비자 GPU에서는 quantized
model, 짧은 context, CPU offload의 성능·메모리 trade-off를 검증해야 한다.

## 공개 평가 결과

원문이 소개한 주요 coding benchmark는 공식 모델 카드와 일치한다.

| Benchmark                        | Ornith-1.5-9B | Qwen3.5-9B | Qwen3.6-35B-A3B | Gemma-4-31B |
| -------------------------------- | ------------: | ---------: | --------------: | ----------: |
| Terminal-Bench 2.1 (Terminus-2)  |          46.2 |       21.3 |            52.5 |        42.1 |
| Terminal-Bench 2.1 (Claude Code) |          47.0 |       18.9 |            49.2 |           - |
| SWE-bench Verified               |          70.6 |       53.2 |            73.4 |        52.0 |
| SWE-bench Pro                    |          47.5 |       31.3 |            49.5 |        35.7 |
| SWE-bench Multilingual           |          54.4 |       39.7 |            67.2 |        51.7 |
| NL2Repo                          |          32.4 |       16.2 |            29.4 |        15.5 |

Ornith-1.5 결과는 5회 독립 실행 평균이라고 명시돼 있다. 같은 크기 대비 강한
결과이지만 모든 항목에서 35B급 모델을 이긴다는 뜻은 아니다. Qwen3.6-35B-A3B가 더
높은 항목도 있으며 benchmark별 harness와 설정도 다르다.

SWE-bench 평가에서는 local repository의 Git history와 network access를
제거했다고 설명한다. NL2Repo에서도 지정 repository와 pip package 접근을 막아
reward hacking을 줄였다고 한다. 이는 유익한 장치지만 결과는 개발팀 보고값이므로
중요한 도입 판단에는 자체 재현 평가가 필요하다.

## 설치 전 확인

공식 모델 카드 확인일 기준 요구 version은 다음과 같다.

- Transformers 5.8.1 이상
- vLLM 0.19.1 이상
- SGLang 0.5.9 이상

버전은 빠르게 바뀔 수 있으므로 설치 시점의 모델 카드와 각 runtime release note를
다시 확인한다. `--trust-remote-code`는 원격 repository의 code 실행을 허용하므로
revision pinning과 code review 없이 production에서 습관적으로 사용하지 않는다.

## 실행 경로

### Ollama

원문은 가장 쉬운 시작 방법으로 다음 명령을 제시한다.

```bash
ollama run ornith-1.5:9b
```

이는 모델 다운로드를 동반한다. storage, quantization, memory 요구량은 현재
Ollama library에서 확인한다.

### vLLM

공식 recipe는 OpenAI-compatible server, 262,144 token context, prefix caching,
reasoning parser와 tool-call parser를 사용한다. 첫 실습에서는 memory 부족을
피하기 위해 context를 작게 시작하는 것이 좋다. 구체적인 안전한 local binding
예시는 [`README.md`](README.md#경로-b-vllm-서버)에 정리했다.

### SGLang

SGLang도 OpenAI-compatible endpoint를 제공한다. vLLM의 tool parser가
`qwen3_xml`인 반면 공식 SGLang recipe는 `qwen3_coder`를 사용한다. parser를
빼거나 잘못 지정하면 model text 안의 tool block이 표준 `tool_calls`로 변환되지
않을 수 있다.

## 긴 컨텍스트와 YaRN

기본 최대 context는 262,144 token이다. 공식 문서는 scaling factor 4.0의 YaRN으로
유효 길이를 약 1M token까지 늘리는 방법을 제공한다. 하지만 open-source runtime은
같은 scaling factor를 모든 request에 정적으로 적용하므로 평범한 길이의 입력
품질이 약간 나빠질 수 있다고 경고한다.

따라서 “지원 최대 길이”를 기본 운영값으로 삼지 않는다. 실제 request 분포가 512K
이하라면 factor 2.0처럼 필요한 만큼만 늘리고, 품질·latency·KV cache memory를
함께 측정한다.

## 체험 과제의 개선

원문은 빈 list에서 `ZeroDivisionError`가 발생하는 평균 함수 수정을 예제로 든다.
학습 평가에서는 단순히 `if not numbers`를 언급했는지만 보지 말고 다음을 함께
요구한다.

1. 빈 입력의 contract를 예외, `None`, 기본값 중 하나로 명시한다.
2. integer와 float 입력 test를 작성한다.
3. 문자열과 `None` 같은 잘못된 type을 어떻게 처리할지 설명한다.
4. 수정 전 실패 test와 수정 후 통과 test를 보여준다.

이렇게 해야 자연스러운 설명 능력과 실제 code correctness를 구분할 수 있다.

## 활용 시나리오

- 외부 API로 보내기 어려운 private code의 local 분석
- 반복적인 test generation과 작은 refactoring 초안
- terminal coding agent의 읽기 전용 보조 모델
- self-generated curriculum과 reward design 연구용 비교 대상

모델 출력은 신뢰 경계 밖의 입력으로 취급해야 한다. shell command, package
install, secret access, network call, file deletion은 별도 승인과 sandbox를
거친다.

## 한계와 검수 결과

- 영어 중심 공개 평가이므로 한국어 coding 능력은 직접 측정해야 한다.
- BF16 weight size와 전체 serving VRAM을 혼동하면 안 된다.
- 9B급이라는 제품명과 Hugging Face UI의 10B params 표기가 함께 존재한다.
- 큰 context는 곧 더 좋은 결과를 뜻하지 않으며 memory와 latency 비용이 크다.
- benchmark 간 harness가 달라 단일 숫자로 모델 우열을 확정할 수 없다.
- 원문의 주요 section, benchmark 수치, runtime version, serving parser, YaRN
  주의사항을 공식 자료와 대조했다.
