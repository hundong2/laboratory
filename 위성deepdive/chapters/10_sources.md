# 10. 출처와 판본

확인일: 2026-09-10

가능한 한 표준 본문과 기관·제조사 공식 자료를 우선했다. CCSDS와 IETF 문서는 개정·대체될 수 있으므로 실제 구현 시작 시 active/superseded 상태를 다시 확인한다.

## 우주 통신과 최신 동향

1. NASA Small Spacecraft Systems Virtual Institute. [State-of-the-Art of Small Spacecraft Technology, 2026](https://www.nasa.gov/smallsat-institute/sst-soa/). 공개된 소형위성 기술의 2026년 현황과 성숙도.
2. NASA. [9.0 Communications, 2026](https://www.nasa.gov/smallsat-institute/sst-soa/soa-communications/). RF/FSO 구조, 설계 고려사항, 미래 기술.
3. NASA. [LunaNet](https://www.nasa.gov/communicating-with-missions/lunanet/). lunar network에서 DTN과 shared navigation/service framework의 역할.
4. NASA. [LunaNet Interoperability Specification](https://www.nasa.gov/directorates/somd/space-communications-navigation-program/lunanet-interoperability-specification/). 2025년 공개된 LNIS v5 및 관련 표준 문서 진입점.
5. Space Development Agency. [Resources: OCT Standard and NEBULA Standard](https://www.sda.mil/home/work-with-us/resources/). PWSA 광 단말과 네트워크 상호운용 요구.
6. Space Development Agency. [PWSA Transport Layer Fact Sheet](https://www.sda.mil/wp-content/uploads/2024/08/Transport-Layer-Fact-Sheet_V6.9-distro-A.pdf). optical ISL mesh와 multi-band transport 구조.
7. ESA. [HydRON: The fibre of the sky](https://www.esa.int/Applications/Connectivity_and_Secure_Communications/ARTES/Hydron_The_fibre_of_the_sky). all-optical multi-orbit network와 2027 LEO segment 계획.
8. ITU. [Recommendation ITU-R M.2177-0: satellite radio interfaces of IMT-2020](https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.2177-0-202602-I%21%21PDF-E.pdf), 2026-02. 5G NR-NTN/IoT-NTN radio interface 정리.
9. ITU. [The State of Satellite Broadband 2025](https://www.itu.int/hub/publication/s-pol-broadband-31-2025/). D2D/D2C, regulation, satellite-terrestrial integration.

## CCSDS

10. CCSDS. [All Active Publications](https://ccsds.org/publications/allpubs/). 문서 active 판본 확인용 catalog.
11. CCSDS 133.0-B-2. [Space Packet Protocol](https://ccsds.org/Pubs/133x0b2e2.pdf), Issue 2, June 2020 with corrigenda. Space Packet header/service.
12. CCSDS 132.0-B-3. TM Space Data Link Protocol, Issue 3, September 2021. CCSDS active publication catalog에서 확인.
13. CCSDS 232.0-B-4. TC Space Data Link Protocol, Issue 4, October 2021 with corrigendum. CCSDS active publication catalog에서 확인.
14. CCSDS 732.0-B-5. AOS Space Data Link Protocol, Issue 5, October 2025. CCSDS active publication catalog에서 확인.
15. CCSDS 732.1-B-3. [Unified Space Data Link Protocol](https://ccsds.org/view/bluebooks/entry/3287/), Issue 3, June 2024.
16. CCSDS 727.0-B-5. CCSDS File Delivery Protocol, Issue 5, July 2020. CCSDS active publication catalog에서 current issue 확인.
17. CCSDS 734.1-B-1. Licklider Transmission Protocol for CCSDS, Issue 1, May 2015; Technical Corrigendum 1, February 2026.
18. CCSDS 734.3-B-1. Schedule-Aware Bundle Routing, Issue 1, July 2019.
19. CCSDS 734.20-O-1. CCSDS Bundle Protocol Specification, Orange Book, April 2025. RFC 9171 기반 experimental specification.
20. CCSDS 355.0-B-2. [Space Data Link Security Protocol](https://ccsds.org/view/bluebooks/entry/3258/), Issue 2, August 2022.
21. CCSDS 355.1-B-1. [Space Data Link Security Protocol—Extended Procedures](https://ccsds.org/publications/allpubs/entry/3259/), February 2020.
22. CCSDS Cross Support Services Area. SLE RAF, RCF, FCLTU service Blue Books. [CCSDS Publications](https://ccsds.org/publications/bluebooks/); mission provider가 지원하는 service version을 별도 확인.

## IETF, IoT와 security

23. IETF RFC 7252. [The Constrained Application Protocol (CoAP)](https://www.rfc-editor.org/info/rfc7252/), June 2014.
24. IETF RFC 7959. [Block-Wise Transfers in CoAP](https://www.rfc-editor.org/info/rfc7959/), August 2016; RFC 9177 update도 함께 확인.
25. IETF RFC 4944. [Transmission of IPv6 Packets over IEEE 802.15.4 Networks](https://www.rfc-editor.org/info/rfc4944/), September 2007.
26. IETF RFC 6282. [Compression Format for IPv6 Datagrams over IEEE 802.15.4-Based Networks](https://www.rfc-editor.org/info/rfc6282/), September 2011.
27. IETF RFC 4301. [Security Architecture for the Internet Protocol](https://www.rfc-editor.org/info/rfc4301/), December 2005.
28. IETF RFC 7296. [Internet Key Exchange Protocol Version 2](https://www.rfc-editor.org/info/rfc7296/), October 2014.
29. IETF RFC 9171. [Bundle Protocol Version 7](https://www.rfc-editor.org/rfc/rfc9171.html), January 2022.
30. IETF RFC 9172. [Bundle Protocol Security](https://www.rfc-editor.org/rfc/rfc9172.html), January 2022.
31. OASIS. [MQTT Version 5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html), OASIS Standard, March 2019.
32. OMA SpecWorks. [LwM2M Core v1.2.1](https://openmobilealliance.org/release/LightweightM2M/V1_2_1-20221209-A/OMA-TS-LightweightM2M_Core-V1_2_1-20221209-A.pdf), December 2022.
33. LoRa Alliance. [LoRaWAN L2 1.0.4 Specification](https://resources.lora-alliance.org/technical-specifications/ts001-1-0-4-lorawan-l2-1-0-4-specification), September 2023.
34. LoRa Alliance. [Regional Parameters RP002-1.0.5](https://resources.lora-alliance.org/technical-specifications), current catalog entry visible as of access date. Deployment region별 parameter는 항상 최신 document 확인.
35. MEF. [SD-WAN Standards](https://www.mef.net/service-standards/overlay-services/sd-wan/). MEF 70, 70.1, 70.2와 secure SD-WAN 자료.

## 하드웨어와 운영체제

36. Semtech. [SX1262 product page and current datasheet](https://www.semtech.com/products/wireless-rf/lora-connect/sx1262). 150–960 MHz, LoRa/LR-FHSS/(G)FSK, DIO/IRQ/SPI 공식 자료 진입점.
37. Semtech. SX1276/77/78/79 Datasheet, Rev. 7, May 2020. DIO mapping, register, reset, SPI timing; 제조사 archive 또는 module vendor가 보존한 revision과 silicon errata 확인.
38. FreeRTOS. [Kernel documentation](https://www.freertos.org/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-About-the-FreeRTOS-Kernel). task, queue, ISR-safe API, scheduler.
39. Wind River. [VxWorks RTOS](https://www.windriver.com/products/embedded/vxworks). commercial real-time/safety platform 개요.
40. Arm. [Mbed OS End-of-Life Announcement](https://www.arm.com/products/development-tools/embedded-and-software/mbed-os). July 2026 EOL.
41. Arm Mbed GitHub organization. [Mbed sunset status and Community Edition notice](https://github.com/armmbed). Arm maintenance 종료 이후 source/community path.
42. strongSwan. [Route-Based VPN](https://docs.strongswan.org/docs/latest/features/routeBasedVpn.html). XFRM interface와 policy/route 처리.
43. strongSwan. [IPv6 Configuration Examples](https://docs.strongswan.org/docs/latest/config/IPv6.html). IPv6 site-to-site, host, remote access scenario.
44. strongSwan. [MOBIKE](https://docs.strongswan.org/docs/6.0/features/mobike.html). IKEv2 mobility/multihoming behavior.

## 안전성·보안 품질

45. MISRA. [MISRA C:2023 Addendum 4](https://misra.org.uk/app/uploads/2024/10/MISRA-C-2023-ADD4.pdf) 및 [MISRA 공식 사이트](https://misra.org.uk/). 세부 guideline 본문은 정식 문서를 구매/허가 범위에서 사용.
46. MITRE CWE. [2025 CWE Top 25 Most Dangerous Software Weaknesses](https://cwe.mitre.org/top25/index.html), page updated 2026-01-29.
47. LLVM. [clang-tidy documentation](https://clang.llvm.org/extra/clang-tidy/).
48. LLVM. [Clang Static Analyzer](https://clang.llvm.org/docs/ClangStaticAnalyzer.html).
49. Cppcheck. [Official repository](https://github.com/danmar/cppcheck).
50. GCC. [Static Analyzer Options](https://gcc.gnu.org/onlinedocs/gcc/Static-Analyzer-Options.html).
51. GitHub. [CodeQL documentation](https://codeql.github.com/docs/contents/) 및 사용 조건.
52. Semgrep. [Community Edition repository](https://github.com/semgrep/semgrep).
53. Frama-C. [Official site](https://frama-c.com/).
54. OpenSSF. [OpenSSF Scorecard](https://securityscorecards.dev/) 및 [SLSA](https://slsa.dev/). Open-source project risk signal과 build provenance framework.

## 판본 관련 중요 주의

- NASA web page는 2026 edition을 제공하지만 일부 검색 결과와 PDF URL은 2024 edition이다. 이 문서는 최신 방향에는 2026 page를, 자세한 수치 예시에는 해당 판본임을 구분해 사용했다.
- CCSDS Bundle Protocol은 2015 Blue Book이 RFC 5050 기반이고 2025 Orange Book이 RFC 9171 BPv7 기반이다. `CCSDS BP`라고만 쓰지 말고 판본/profile을 명시한다.
- AOS Issue 5(2025)는 이전 Issue 4를 대체했다. ground provider 지원 판본과 mission ICD를 맞춘다.
- Mbed OS는 source가 사라진 것이 아니라 Arm의 active maintenance/support가 2026년 7월 종료된 것이다.
- D2C/D2D는 업계에서 혼용된다. ITU 보고서의 구분과 프로젝트 정의를 함께 표기한다.

[← 미래 로드맵](09_future_roadmap.md) · [메인](../README.md)
