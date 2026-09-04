# Ornith-1.5-9B 로컬 코딩 LLM 실습

작성일: 2026-08-24

## 목차

- [출처와 작업 범위](#출처와-작업-범위)
- [한눈에 보기](#한눈에-보기)
- [기초 개념](#기초-개념)
- [핵심 요약](#핵심-요약)
- [상세 정리](#상세-정리)
- [설치와 실행 경로](#설치와-실행-경로)
- [용어 정리](#용어-정리)
- [실습 학습 가이드](#실습-학습-가이드)
- [다음 학습 경로](#다음-학습-경로)

## 출처와 작업 범위

- 주 원문:
  [🆓 Ornith-1.5-9B 무료 설치 가이드](https://fornewchallenge.tistory.com/entry/%F0%9F%86%93-Ornith-15-9B-%EB%AC%B4%EB%A3%8C-%EC%84%A4%EC%B9%98-%EA%B0%80%EC%9D%B4%EB%93%9C-9B%EB%A1%9C-31B%EA%B8%89-%EB%94%B0%EB%9D%BC%EC%9E%A1%EC%9D%80-%EC%9E%90%EA%B0%80-%EA%B0%9C%EC%84%A0-%EC%BD%94%EB%94%A9-LLM)
- 공식 모델 카드:
  [ornith-ai/Ornith-1.5-9B](https://huggingface.co/ornith-ai/Ornith-1.5-9B)
- 공식 기술 설명:
  [Ornith-1.5: From Self-Scaffolding to Self-Improvement](https://ornith.ai/ornith_1_5.html)
- 확인일: 2026-08-24
- 원문 언어: 한국어. [`translation.ko.md`](translation.ko.md)는 전문 복제가
  아니라 원문 흐름을 보존한 교정·재구성본이다.

이 자료는 모델 자체를 내려받지 않아도 실행할 수 있는 오프라인 실습부터 시작한다.
실제 모델 서빙은 별도의 GPU 메모리와 수십 GB 다운로드가 필요하므로 자동으로
설치하거나 다운로드하지 않는다.

## 한눈에 보기

Ornith-1.5-9B는 Ornith 팀이 공개한 코딩·추론·에이전트 작업용 dense 모델이다.
공식 설명에 따르면 고정된 사람이 만든 과제만 사용하는 대신 다음 세 요소를 함께
개선한다.

1. 현재 모델에 유익한 새 과제를 생성한다.
2. 과제를 풀고 평가할 scaffold/harness를 만든다.
3. solution rollout을 생성하고 보상으로 정책을 갱신한다.

모델 카드가 보고한 SWE-bench Verified 점수는 70.6이며 5회 실행 평균이다. 이는
개발팀 공개 평가값이지 모든 로컬 코딩 작업에서 70.6% 성공한다는 보장은 아니다.
비교 모델, harness, 채팅 템플릿, 샘플링 설정과 오염·보상 해킹 방지 조건까지 함께
봐야 한다.

> 모델 카드 본문은 약 9B dense 모델이라고 설명하지만 Hugging Face UI는 확인일
> 현재 `10B params`로 표시한다. 이 문서에서는 제품명에 따라 9B급으로 부르되,
> 정확한 파라미터 수가 중요한 계산에는 체크포인트 설정을 직접 확인하도록 한다.

## 기초 개념

### Dense 모델

모든 토큰 처리에 전체 파라미터가 참여하는 모델이다. 일부 expert만 활성화하는
MoE와 달리 총 파라미터와 토큰당 활성 파라미터의 차이가 작다.

### Self-improvement loop

단순히 자기 답변을 다시 읽는 것이 아니다. 공식 설계는
`task → scaffold/harness → rollout → reward → GRPO update`의 학습 루프를 뜻한다.
실서비스에서 모델이 사용자 코드를 보며 자동으로 계속 학습한다는 의미도 아니다.

### Harness와 rollout

- **Harness**: 도구, 지시, 분해 전략, 실행 환경과 채점기를 묶은 과제 수행
  틀이다.
- **Rollout**: 주어진 과제와 harness 안에서 모델이 만든 한 번의 해결 궤적이다.
- **Reward hacking**: 실제 과제를 풀지 않고 채점기의 허점을 이용해 높은 보상을
  얻는 현상이다.

### 컨텍스트와 메모리

공식 기본 최대 컨텍스트는 262,144 토큰이다. 하지만 긴 컨텍스트를 설정할 수
있다는 사실과 해당 길이를 현재 GPU에서 감당할 수 있다는 사실은 다르다. 가중치
외에도 KV cache, 활성값, 런타임 여유 메모리가 필요하다. YaRN으로 약 1M 토큰까지
확장할 수 있지만 일반 길이 입력 품질이 조금 저하될 수 있다는 공식 주의사항도
있다.

## 핵심 요약

| 항목          | 확인 내용                              | 실무 해석                                                       |
| ------------- | -------------------------------------- | --------------------------------------------------------------- |
| 라이선스      | 모델 카드상 MIT                        | 배포 전 모델 파일과 파생 체크포인트의 라이선스를 다시 확인한다. |
| 모델 형태     | 약 9B dense, BF16 약 19GB              | 19GB는 대략적인 가중치 크기이며 전체 서빙 VRAM이 아니다.        |
| 기본 컨텍스트 | 최대 262,144 토큰                      | 첫 실행은 8K~32K로 낮춰 성공 경로를 먼저 만든다.                |
| API           | vLLM/SGLang의 OpenAI 호환 endpoint     | 기존 OpenAI SDK 기반 도구를 `base_url` 변경으로 연결할 수 있다. |
| reasoning     | `reasoning_content` 분리 지원          | 내부 추론을 로그·UI에 무조건 노출하거나 저장하지 않는다.        |
| tool calling  | 서버 parser로 표준 `tool_calls` 변환   | 도구 실행 전 schema 검증, allowlist, 권한 승인 계층이 필요하다. |
| 평가          | SWE-bench Verified 70.6 등 개발팀 보고 | 자체 저장소의 회귀 테스트로 독립 검증한다.                      |

## 상세 정리

### 자가 개선 보상 설계

공식 기술 설명은 과제 보상을 다음 세 신호의 곱으로 설명한다.

```text
R_task = validity × frontier_difficulty × novelty
```

- 유효성은 과제와 채점 환경이 실행 가능하고 검증 가능한지 본다.
- frontier difficulty는 현재 정책의 성공률이 목표 성공률(공식 예시는 0.2)에
  가까운지를 본다.
- novelty는 과거 과제와 지나치게 비슷한 문제의 반복을 억제한다.

곱셈 구조라서 한 요소가 0이면 전체 보상도 0이다. 따라서 어렵기만 하고 채점
불가능한 과제나, 새롭지만 무의미한 과제가 보상을 독점하기 어렵다. 세 번째
노트북에서 이 성질을 작은 시뮬레이션으로 확인한다.

### 벤치마크를 읽는 법

원문과 공식 모델 카드의 주요 코딩 점수는 일치한다. Ornith-1.5-9B는 SWE-bench
Verified 70.6, SWE-bench Pro 47.5, Multilingual 54.4, NL2Repo 32.4를 보고한다.
모든 Ornith-1.5 결과는 5회 평균이라고 명시되어 있다.

다만 서로 다른 benchmark 점수를 하나의 순위로 합치면 안 된다. 예를 들어
SWE-bench는 실제 저장소 이슈 해결, Terminal-Bench는 terminal task, NL2Repo는
자연어 명세에서 저장소를 만드는 능력을 측정한다. 공개 평가는 영어 중심이며
한국어 프롬프트 품질은 별도 검증 대상이다.

### 보안 경계

코딩 모델이 만든 shell command를 즉시 실행하지 않는다. 최소한 다음 경계를 둔다.

- 읽기 전용 분석과 파일 변경 권한을 분리한다.
- 허용된 작업 디렉터리 밖의 접근을 차단한다.
- 네트워크, secret, package installation은 별도 승인 대상으로 둔다.
- patch 적용 전에 diff를 표시하고, 이후 테스트를 실행한다.
- tool call argument를 JSON Schema로 검증하고 알 수 없는 도구는 거부한다.

## 설치와 실행 경로

### 경로 A: Ollama로 기능 확인

가장 작은 진입점이다. Ollama 설치는 사용자가 직접 완료한 뒤 다음 명령을
실행한다.

```bash
ollama run ornith-1.5:9b
```

양자화 종류와 실제 다운로드 크기는 실행 시점의 Ollama library를 확인한다. 모델
실행 후 빈 배열, 잘못된 타입, timeout 같은 edge case를 포함한 코딩 문제로
평가한다.

### 경로 B: vLLM 서버

공식 모델 카드 확인일 기준 최소 버전은 Transformers 5.8.1, vLLM 0.19.1이다. 첫
실행은 컨텍스트를 줄이는 편이 안전하다.

```bash
vllm serve ornith-ai/Ornith-1.5-9B \
  --served-model-name Ornith-1.5-9B \
  --host 127.0.0.1 --port 8000 \
  --max-model-len 16384 \
  --gpu-memory-utilization 0.90 \
  --enable-prefix-caching \
  --enable-auto-tool-choice \
  --tool-call-parser qwen3_xml \
  --reasoning-parser qwen3 \
  --trust-remote-code
```

학습용 기본값은 외부 노출을 피하려고 `127.0.0.1`을 사용했다. 외부 접속이
필요하면 인증·방화벽·TLS를 먼저 설계한 후 명시적으로 binding을 변경한다.

### 경로 C: SGLang 서버

공식 모델 카드 확인일 기준 최소 버전은 SGLang 0.5.9다.

```bash
python -m sglang.launch_server \
  --model-path ornith-ai/Ornith-1.5-9B \
  --served-model-name Ornith-1.5-9B \
  --host 127.0.0.1 --port 8000 \
  --context-length 16384 \
  --mem-fraction-static 0.85 \
  --tool-call-parser qwen3_coder \
  --reasoning-parser qwen3
```

### API 연결 확인

서버가 준비된 뒤 두 번째 노트북의 `DRY_RUN = False`로 바꾸면
`/v1/chat/completions` 요청을 보낼 수 있다. 처음에는 짧은 context와 제한된
`max_tokens`로 연결·응답 schema·timeout부터 확인한다.

## 용어 정리

| 용어                  | 뜻                                                                               |
| --------------------- | -------------------------------------------------------------------------------- |
| BF16                  | 16비트 부동소수점 형식. 가중치 약 19GB라는 설명의 기준이다.                      |
| KV cache              | attention에서 이전 token의 key/value를 저장하는 메모리. context가 길수록 커진다. |
| YaRN                  | RoPE를 scaling해 학습 길이보다 긴 context를 다루는 방법이다.                     |
| GRPO                  | 여러 rollout의 상대 보상을 이용하는 policy optimization 계열 방법이다.           |
| Prefix caching        | 공통 prompt prefix의 계산 결과를 재사용하는 serving 최적화다.                    |
| OpenAI-compatible API | OpenAI SDK와 유사한 endpoint·request schema를 제공하는 인터페이스다.             |

## 실습 학습 가이드

1. [`01_foundations.ipynb`](01_foundations.ipynb): 파라미터 정밀도별 가중치
   메모리와 context 예산을 계산한다.
2. [`02_practice.ipynb`](02_practice.ipynb): 안전한 코딩 prompt와 OpenAI 호환
   request를 만들고 응답을 검사한다.
3. [`03_advanced.ipynb`](03_advanced.ipynb): 공식 self-improvement 보상 구조와
   benchmark 비교의 함정을 시뮬레이션한다.

모든 노트북의 기본 경로는 모델·GPU 없이 실행된다. 실제 서버 요청은 명시적인
flag를 켜야만 수행된다.

## 다음 학습 경로

1. Ollama 또는 축소 context vLLM으로 10개짜리 개인 평가 세트를 실행한다.
2. pass/fail뿐 아니라 수정 정확성, test 통과율, latency, peak memory를 기록한다.
3. 한국어와 영어 prompt를 같은 과제로 비교한다.
4. tool calling은 읽기 전용 도구부터 연결하고 승인·sandbox·audit log를 추가한다.
5. 262K 또는 YaRN은 짧은 context baseline을 확보한 뒤 품질과 비용을 함께
   비교한다.
