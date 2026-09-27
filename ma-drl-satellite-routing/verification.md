# 출처·번역·실습 검증 기록

확인일: 2026-09-27 · [README](README.md)

## 원문 확인

- arXiv landing/HTML에서 제목·저자·v2(2024-11-28)를 확인했다.
- 공식 학회 PDF를 직접 내려받아 5쪽 모두 텍스트 추출 및 이미지 렌더링으로 확인했다. 웹 도구의 Zenodo 접근은 오류였지만 직접 HTTPS 다운로드에는 성공했다. 접근 실패한 것처럼 처리하거나 검색 초록만으로 전문을 구성하지 않았다.
- PDF SHA-256: `503a4e11f37da2bcc7f93ab0a948030582bd102e4dca92cfd5804090b0f78dae`.
- pp. 420–424와 각 페이지 CC BY 4.0 고지, 그림 1–7을 확인했다. 출판본 원문을 번역 근거로 사용했다. 원본 PDF와 페이지 이미지는 검토용 임시 파일이며 이 폴더에 중복 배포하지 않는다.
- 다단 문장의 이어짐(특히 pp. 420→421, 421→422, 422→423, 423→424), 전송·전파 구분, Fig. 7의 평균 지연 표기를 대조했다.
- 전체 본문·caption·제목은 108쌍 문장 대조 형식이다. 저자 소속·연구비 각주는 요약으로 제공하며 부분 번역으로 표시했다. 참고문헌은 서지 정보 그대로 제공했다.
- 원문 ℓ와 N 표기의 혼용, Kb 단위와 `routed` 오기를 임의 수정·환산하지 않고 별도 주석으로 밝혔다.

## 로컬 실습 검증

환경: Windows, Python 3.13.5. CPU, 표준 라이브러리만 사용. `nbformat`은 파일 형식 검사에만 사용했으며 notebook 실행에 필수는 아니다.

```text
python -X utf8 ma-drl-satellite-routing/verify_notebooks.py
```

- 세 notebook 각각 독립 namespace에서 모든 code cell 실행 및 assert 통과.
- nbformat v4 schema 검사 3/3 통과. Jupyter 브라우저 UI·kernel 통합 검사는 수행하지 않았다. notebook의 execution_count/output은 비워 두었고 실행 결과를 아래에 기록한다.
- 번역 Original/한국어 ID S001–S108의 연속성·짝 순서 검사 통과.
- Markdown 상대 파일 링크·목차 anchor 검사 통과.
- 기존 루트 README 변경과 새 텍스트의 whitespace 검사 완료. 기존 사용자 첨부파일은 변경하지 않았다.

### 교육용 출력 — 논문 결과가 아님

| 검사 | 결과 |
| --- | --- |
| 1,500 byte, 10 Mbit/s, 1,000 km, 큐 없음 | 전송 1.2 ms + 전파 3.335641 ms |
| 합성 그래프 hop / range / rate | A–D / A–C–D / A–B–D |
| 동시 도착 3개, capacity 2 | 수용 2, 드롭 1; 완료 지연 4·5 ms |
| Poisson, λ=1500, seed=42, horizon 1초, drain=False | 생성 1484, 수용 1007, 드롭 477, 완료 996, 미완료 11 |
| 같은 trace, drain=True | 완료 1007, 미완료 0 |
| Q-routing 변화 전 | A–B–D, 4 ms; 5 seed 모두 기준 비용 일치 |
| B–D 제거 후 동결 정책 | 반복 경로, max_hops로 중단·전달 실패 집계 |
| 변화 후 재학습 | A–C–D, 12 ms; 현재 그래프 Dijkstra 비용 일치 |

02는 부하별 5개 seed 출력, 03은 baseline 5 seed를 확인한다. 이 작은 결정론적 그래프에서의 일치를 일반적인 학습 수렴 보장으로 확대하지 않는다.

## 재현하지 않은 범위

원본 SimPy 환경, 군집 궤도역학, RF/FSO/DVB-S2 link budget, 실제 인구 데이터, 원래 reward/state 설계, Keras DNN/DDQN, SFL/CKA, 논문 Fig. 5–7의 수치 재현은 실행하지 않았다. 저자 공식 코드 README는 보조 확인만 했고 저장소를 clone하거나 submodule로 추가하지 않았다. 문헌 인용 목록의 모든 논문을 별도 분석한 작업도 아니다.

본 작업은 논문 학습 자료 생성이다. 코드 실행 시간이나 모델 품질을 원 저자와 동등 조건으로 평가했다고 주장하지 않는다.

후속 기록(2026-09-27): 별도 GitHub 요청에 따라 `MA-DRL_Routing_Simulator` 서브모듈에 코드 분석·경량 실습·Archify 문서를 추가했다. 상기 ‘재현하지 않은 범위’는 이 논문 자료 자체의 검증 범위를 유지한다. 전체 시뮬레이터 학습은 후속 작업에서도 실행하지 않았다.
