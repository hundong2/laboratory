# 네트워크 아키텍처 문서 검증 기록

작성일: 2026-09-10  
분석 revision: 학습 자료 기준선 1.0

## 범위와 설계 관점

대상은 다수의 저궤도 위성, RF(Radio Frequency, 무선주파수)와 Optical ISL(Optical Inter-Satellite Link, 광 위성간 링크), 사용자 단말, 지상국, 임무 데이터센터다. 대표 실행 경로는 `사용자/탑재체 데이터 → 위성 edge → ISL mesh → gateway → ground processing`이며, 반대 방향 telecommand와 별도 control-plane 정책 배포도 표시한다.

구체적인 궤도·사업자·주파수·벤더가 지정되지 않았으므로 일반화된 논리 아키텍처다. 실제 연결성, 처리율, 신뢰 경계와 암호 경계는 임무 ICD와 요구사항으로 다시 확정해야 한다.

## 산출물

- [network-architecture.html](network-architecture.html): self-contained 대화형 뷰어
- [network-architecture.json](network-architecture.json): 원본 architecture schema
- [visual-check 결과](network-architecture.visual-check.html): 브라우저 기반 다중 해상도 검사
- [1440×900 light](network-architecture.visual-check.1440x900.light.png) / [dark](network-architecture.visual-check.1440x900.dark.png)
- [2048×1320 light](network-architecture.visual-check.2048x1320.light.png) / [dark](network-architecture.visual-check.2048x1320.dark.png)

## 코드·문서 근거

이 주제는 구현 저장소가 아니라 학습·설계 문서이므로, component의 `sources`는 이 폴더의 상세 장과 실무 문서를 가리킨다. 근거는 `chapters/01_system_foundations.md`, `02_rf_optical_link_budget.md`, `03_space_networking.md`, `04_ccsds_operations.md`, `05_dtn_reliability.md`, `08_security_quality.md`다. 실행 코드가 없는 부분을 특정 제품 구현처럼 표현하지 않았다.

## 신뢰 경계

- 사용자 단말과 위성 접속 경계
- 위성 RF/광 링크와 온보드 라우팅 경계
- 지상국 RF front-end와 mission network 경계
- 임무 데이터센터의 운영자·키 관리·외부 연계 경계
- SDLS(Space Data Link Security, 우주 데이터 링크 보안), BPSec(Bundle Protocol Security, 번들 프로토콜 보안), IPsec(Internet Protocol Security, 인터넷 프로토콜 보안)은 보호 계층과 종단점이 다르므로 중복 적용 시 책임을 명시해야 한다.

## 검증 receipt

- Archify schema: `architecture`
- quality profile: `showcase`
- artifact checks: `9/9`
- composition: 오류 `0`, 경고 `0`
- spec SHA-256: `fb9b582ccad90078c6327ed08873d34b168b5b2921ea229e8ca5cc2109896a2d`
- HTML SHA-256: `f56adaed66dad0d21cca81a941454509fae5f8ee3f6657fc0444f6db1ef53a2f`
- 브라우저 검사: 1440×900, 1600×1000, 1920×1080, 2048×1320에서 overflow와 readability 검사 통과
- 지각적 시각 검토: light/dark 이미지를 직접 확인했으며 node·edge 겹침, 잘림, 읽을 수 없는 label이 없음을 확인

뷰어 고정 사용자 인터페이스는 Archify가 한국어 locale을 제공하지 않아 영어 fallback을 사용하지만, 아키텍처 제목·설명·노드 내용은 한국어다.

[← 실무 산출물 인덱스](../README.md)
