import fs from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const outDir = fileURLToPath(new URL("../results/", import.meta.url));
await fs.mkdir(outDir, { recursive: true });

const font = "Arial";
const dark = "#243447";
const header = "#36566F";
const light = "#E8EEF3";
const input = "#FFF2CC";
const green = "#E2F0D9";
const red = "#FCE4D6";

function baseSheet(sheet) {
  sheet.showGridLines = false;
  sheet.getRange("A1:Z100").format.font = { name: font, size: 10, color: "#1F2933" };
  sheet.getRange("A2:H2").format.font = { name: font, size: 15, bold: true, color: dark };
  sheet.getRange("A3:H3").format.borders = { bottom: { style: "thin", color: "#7F8C8D" } };
}

function tableHeader(range) {
  range.format = {
    fill: header,
    font: { name: font, size: 10, bold: true, color: "#FFFFFF" },
    horizontalAlignment: "center",
    verticalAlignment: "center",
    borders: { preset: "inside", style: "thin", color: "#FFFFFF" },
  };
}

async function buildLinkBudget() {
  const wb = Workbook.create();
  const summary = wb.worksheets.add("Summary");
  const budget = wb.worksheets.add("Link Budget");
  const sources = wb.worksheets.add("Sources");
  summary.tabColor = dark;
  budget.tabColor = "#7FA6C9";
  sources.tabColor = "#A6A6A6";
  [summary, budget, sources].forEach(baseSheet);

  budget.getRange("A2").values = [["RF 링크 버짓 계산"]];
  budget.getRange("A3").values = [["노란색 셀은 임무·부품 데이터로 교체해야 하는 입력값입니다."]];
  budget.getRange("A3").format.font = { name: font, size: 10, italic: true, color: "#5B6573" };
  budget.getRange("A4:C4").values = [["입력", "값", "단위"]];
  tableHeader(budget.getRange("A4:C4"));
  budget.getRange("A5:C15").values = [
    ["송신기 출력", 10, "dBW"],
    ["송신 계통 손실", 1, "dB"],
    ["송신 안테나 이득", 20, "dBi"],
    ["경로 거리", 1500, "km"],
    ["반송파 주파수", 8.2, "GHz"],
    ["수신 안테나 이득", 25, "dBi"],
    ["시스템 잡음 온도", 500, "K"],
    ["기타 경로 손실", 3, "dB"],
    ["정보 비트율", 2000000, "bit/s"],
    ["요구 Eb/N0", 3, "dB"],
    ["구현 여유", 2, "dB"],
  ];
  budget.getRange("B5:B15").format.fill = input;
  budget.getRange("B5:B15").format.numberFormat = "#,##0.00";
  budget.getRange("A17:C17").values = [["계산 결과", "값", "단위"]];
  tableHeader(budget.getRange("A17:C17"));
  budget.getRange("A18:A25").values = [
    ["EIRP"], ["FSPL"], ["G/T"], ["C/N0"], ["Eb/N0"], ["링크 마진"], ["수신 전력"], ["판정"],
  ];
  budget.getRange("C18:C25").values = [["dBW"], ["dB"], ["dB/K"], ["dB-Hz"], ["dB"], ["dB"], ["dBW"], [""]];
  budget.getRange("B18:B25").formulas = [
    ["=B5-B6+B7"],
    ["=92.45+20*LOG10(B8)+20*LOG10(B9)"],
    ["=B10-10*LOG10(B11)"],
    ["=B18-B19-B12+B20+228.6"],
    ["=B21-10*LOG10(B13)"],
    ["=B22-B14-B15"],
    ["=B18-B19-B12+B10"],
    ["=IF(B23>=3,\"PASS\",\"REVIEW\")"],
  ];
  budget.getRange("B18:B24").format.numberFormat = "0.00";
  budget.getRange("A23:C25").format.font = { name: font, size: 10, bold: true, color: dark };
  budget.getRange("B23").conditionalFormats.add("cellIs", { operator: "greaterThanOrEqual", formula: 3, format: { fill: green, font: { bold: true, color: "#375623" } } });
  budget.getRange("B23").conditionalFormats.add("cellIs", { operator: "lessThan", formula: 3, format: { fill: red, font: { bold: true, color: "#9C0006" } } });
  budget.getRange("B25").conditionalFormats.add("containsText", { text: "REVIEW", format: { fill: red, font: { bold: true, color: "#9C0006" } } });
  budget.getRange("B25").conditionalFormats.add("containsText", { text: "PASS", format: { fill: green, font: { bold: true, color: "#375623" } } });
  budget.getRange("E4:F4").values = [["독립 확인", "값"]];
  tableHeader(budget.getRange("E4:F4"));
  budget.getRange("E5:E7").values = [["거리 2배 FSPL 증가"], ["주파수 2배 FSPL 증가"], ["비트율 2배 Eb/N0 변화"]];
  budget.getRange("F5:F7").formulas = [
    ["=(92.45+20*LOG10(B8*2)+20*LOG10(B9))-B19"],
    ["=(92.45+20*LOG10(B8)+20*LOG10(B9*2))-B19"],
    ["=(B21-10*LOG10(B13*2))-B22"],
  ];
  budget.getRange("F5:F7").format.numberFormat = "0.00";
  budget.getRange("E9:F9").values = [["검토 항목", "확인"]];
  tableHeader(budget.getRange("E9:F9"));
  budget.getRange("E10:F16").values = [
    ["거리 min/nominal/max", "미입력"],
    ["pointing/polarization loss", "미입력"],
    ["온도·aging·제조 편차", "미입력"],
    ["요구 BER/PER와 code rate", "미입력"],
    ["Doppler와 acquisition", "미입력"],
    ["규제 EIRP/대역", "미입력"],
    ["가용성 percentile", "미입력"],
  ];
  budget.getRange("F10:F16").format.fill = input;
  budget.getRange("F10:F16").dataValidation = { rule: { type: "list", values: ["미입력", "확인", "해당 없음"] } };

  summary.getRange("A2").values = [["링크 버짓 요약"]];
  summary.getRange("A4:B4").values = [["핵심 지표", "결과"]];
  tableHeader(summary.getRange("A4:B4"));
  summary.getRange("A5:A9").values = [["EIRP (dBW)"], ["FSPL (dB)"], ["C/N0 (dB-Hz)"], ["Eb/N0 (dB)"], ["링크 마진 (dB)"]];
  summary.getRange("B5:B9").formulas = [["='Link Budget'!B18"], ["='Link Budget'!B19"], ["='Link Budget'!B21"], ["='Link Budget'!B22"], ["='Link Budget'!B23"]];
  summary.getRange("B5:B9").format.numberFormat = "0.00";
  summary.getRange("D4:E4").values = [["상태", "값"]];
  tableHeader(summary.getRange("D4:E4"));
  summary.getRange("D5:D7").values = [["판정"], ["검토 완료 항목"], ["남은 검토 항목"]];
  summary.getRange("E5:E7").formulas = [["='Link Budget'!B25"], ["=COUNTIF('Link Budget'!F10:F16,\"확인\")"], ["=COUNTIF('Link Budget'!F10:F16,\"미입력\")"]];
  summary.getRange("A12:E15").values = [
    ["해석", "", "", "", ""],
    ["링크 마진은 평균값이 아니라 worst-case와 요구 가용성에서 판정해야 합니다.", "", "", "", ""],
    ["광 링크에는 FSPL 식 외에 aperture, pointing, optical train, detector와 cloud/turbulence 모델이 필요합니다.", "", "", "", ""],
    ["입력값은 교육용 예시이며 실제 부품·궤도·규제 데이터로 교체해야 합니다.", "", "", "", ""],
  ];
  summary.getRange("A12:E12").format = { fill: light, font: { name: font, bold: true, color: dark } };

  sources.getRange("A2").values = [["출처와 식"]];
  sources.getRange("A4:C4").values = [["항목", "근거", "URL"]];
  tableHeader(sources.getRange("A4:C4"));
  sources.getRange("A5:C8").values = [
    ["RF/FSO 설계 고려", "NASA Small Spacecraft Communications 2026", "https://www.nasa.gov/smallsat-institute/sst-soa/soa-communications/"],
    ["FSPL", "Friis 자유공간 식의 dB 표현", "https://www.itu.int/rec/R-REC-P.525"],
    ["C/N0와 Eb/N0", "표준 link-budget 관계식", "https://www.nasa.gov/directorates/somd/space-communications-navigation-program/"],
    ["주의", "모든 입력은 예시이며 mission ICD와 부품 시험값으로 교체", ""],
  ];

  budget.freezePanes.freezeRows(4);
  sources.freezePanes.freezeRows(4);
  budget.getRange("A1:F30").format.verticalAlignment = "center";
  summary.getRange("A1:E20").format.verticalAlignment = "center";
  sources.getRange("A1:C12").format.verticalAlignment = "center";
  budget.getRange("A:A").format.columnWidth = 30;
  budget.getRange("B:B").format.columnWidth = 15;
  budget.getRange("C:C").format.columnWidth = 12;
  budget.getRange("D:D").format.columnWidth = 3;
  budget.getRange("E:E").format.columnWidth = 29;
  budget.getRange("F:F").format.columnWidth = 16;
  summary.getRange("A:A").format.columnWidth = 30;
  summary.getRange("B:B").format.columnWidth = 16;
  summary.getRange("C:C").format.columnWidth = 4;
  summary.getRange("D:D").format.columnWidth = 24;
  summary.getRange("E:E").format.columnWidth = 16;
  sources.getRange("A:A").format.columnWidth = 24;
  sources.getRange("B:B").format.columnWidth = 48;
  sources.getRange("C:C").format.columnWidth = 70;
  sources.getRange("A5:C8").format.wrapText = true;
  sources.getRange("A5:C8").format.rowHeight = 38;
  summary.getRange("A13:E15").format.wrapText = true;
  summary.getRange("A13:E15").format.rowHeight = 30;

  wb.recalculate();
  const inspect = await wb.inspect({ kind: "table", range: "Link Budget!A4:F25", include: "values,formulas", tableMaxRows: 30, tableMaxCols: 8 });
  console.log(inspect.ndjson);
  const errors = await wb.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!", options: { useRegex: true, maxResults: 100 }, summary: "link budget formula errors" });
  console.log(errors.ndjson);
  for (const [sheetName, fileName] of [["Summary", "link-budget-summary.png"], ["Link Budget", "link-budget.png"], ["Sources", "link-budget-sources.png"]]) {
    const preview = await wb.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
    await fs.writeFile(`${outDir}/${fileName}`, new Uint8Array(await preview.arrayBuffer()));
  }
  const out = await SpreadsheetFile.exportXlsx(wb);
  await out.save(`${outDir}/link-budget.xlsx`);
}

async function buildTraceability() {
  const wb = Workbook.create();
  const summary = wb.worksheets.add("Summary");
  const trace = wb.worksheets.add("Traceability");
  summary.tabColor = dark;
  trace.tabColor = "#7FA6C9";
  [summary, trace].forEach(baseSheet);

  trace.getRange("A2").values = [["요구사항 추적 매트릭스"]];
  trace.getRange("A3").values = [["상태와 실제 증거 링크를 프로젝트 진행에 맞춰 갱신합니다."]];
  trace.getRange("A5:J5").values = [["요구사항 ID", "분류", "요구사항", "근거", "설계 요소", "ICD", "시험 ID", "결과 증거", "상태", "담당"]];
  tableHeader(trace.getRange("A5:J5"));
  trace.getRange("A6:J17").values = [
    ["COM-001", "성능", "Critical telemetry를 생성 후 60초 안에 전달한다.", "운영 경보 지연", "우선순위 queue, DTN route", "ICD-NET-04", "TP-PERF-001", "VR-PERF-001", "Draft", "Network"],
    ["COM-002", "가용성", "단일 ISL 상실 시 10초 안에 대체 경로로 전환한다.", "단일 결함 허용", "RF/Optical failover", "ICD-NET-03", "TP-FO-001", "VR-FO-001", "Draft", "Network"],
    ["COM-003", "링크", "Worst-case 링크 마진은 3 dB 이상이어야 한다.", "환경·구현 불확실성", "RF link budget", "ICD-RF-01", "TP-RF-001", "VR-RF-001", "Draft", "RF"],
    ["COM-004", "데이터", "세 번의 연속 contact miss 동안 critical data를 보존한다.", "지상국/날씨 장애", "Persistent DTN store", "ICD-SW-05", "TP-BUF-001", "VR-BUF-001", "Draft", "Flight SW"],
    ["COM-005", "보안", "모든 telecommand는 실행 전에 출처와 freshness를 검증한다.", "spoof/replay 방지", "SDLS anti-replay", "ICD-SEC-01", "TP-SEC-001", "VR-SEC-001", "Draft", "Security"],
    ["COM-006", "상호운용", "Ground return frame은 합의한 SLE RAF version으로 제공한다.", "다중 지상국 지원", "SLE provider/user", "ICD-GS-02", "TP-SLE-001", "VR-SLE-001", "Draft", "Ground"],
    ["COM-007", "프로토콜", "중복 command ID는 재실행하지 않고 기존 결과를 반환한다.", "at-least-once 경로", "Execution journal", "ICD-SW-07", "TP-DUP-001", "VR-DUP-001", "Draft", "Flight SW"],
    ["COM-008", "실시간", "Radio IRQ ISR 실행시간은 50 microseconds 이하이다.", "RTOS deadline", "ISR defer-to-task", "ICD-HW-03", "TP-RT-001", "VR-RT-001", "Draft", "Embedded"],
    ["COM-009", "품질", "Flight C code의 required MISRA deviation은 승인 기록을 가진다.", "안전성", "Static analysis pipeline", "ICD-SW-09", "TP-SA-001", "VR-SA-001", "Draft", "Quality"],
    ["COM-010", "공급망", "Release마다 SBOM과 dependency digest를 생성한다.", "OSS provenance", "CI release pipeline", "ICD-SW-10", "TP-SCA-001", "VR-SCA-001", "Draft", "Security"],
    ["COM-011", "복구", "Reset 후 replay counter가 rollback되지 않는다.", "command freshness", "Protected monotonic state", "ICD-SEC-03", "TP-RST-001", "VR-RST-001", "Draft", "Security"],
    ["COM-012", "운영", "Failover와 failback을 분기마다 실제 경로로 시험한다.", "잠복 장애 방지", "Operations runbook", "ICD-OPS-01", "TP-OPS-001", "VR-OPS-001", "Draft", "Operations"],
  ];
  trace.getRange("I6:I100").dataValidation = { rule: { type: "list", values: ["Draft", "Approved", "Implemented", "Verified", "Blocked"] } };
  trace.getRange("I6:I17").format.fill = input;
  trace.getRange("A5:J17").format.verticalAlignment = "center";
  trace.getRange("C6:H17").format.wrapText = true;
  trace.getRange("A6:J17").format.rowHeight = 42;
  trace.freezePanes.freezeRows(5);
  trace.freezePanes.freezeColumns(2);
  const widths = [16, 13, 48, 30, 30, 16, 16, 18, 14, 16];
  "ABCDEFGHIJ".split("").forEach((col, index) => { trace.getRange(`${col}:${col}`).format.columnWidth = widths[index]; });
  trace.getRange("I6:I17").conditionalFormats.add("containsText", { text: "Blocked", format: { fill: red, font: { bold: true, color: "#9C0006" } } });
  trace.getRange("I6:I17").conditionalFormats.add("containsText", { text: "Verified", format: { fill: green, font: { bold: true, color: "#375623" } } });

  summary.getRange("A2").values = [["요구사항 추적 현황"]];
  summary.getRange("A4:B4").values = [["지표", "값"]];
  tableHeader(summary.getRange("A4:B4"));
  summary.getRange("A5:A10").values = [["전체 요구사항"], ["Verified"], ["Implemented"], ["Approved"], ["Draft"], ["Blocked"]];
  summary.getRange("B5:B10").formulas = [
    ["=COUNTA(Traceability!A6:A100)"],
    ["=COUNTIF(Traceability!I6:I100,\"Verified\")"],
    ["=COUNTIF(Traceability!I6:I100,\"Implemented\")"],
    ["=COUNTIF(Traceability!I6:I100,\"Approved\")"],
    ["=COUNTIF(Traceability!I6:I100,\"Draft\")"],
    ["=COUNTIF(Traceability!I6:I100,\"Blocked\")"],
  ];
  summary.getRange("D4:E4").values = [["완전성", "값"]];
  tableHeader(summary.getRange("D4:E4"));
  summary.getRange("D5:D8").values = [["설계 연결"], ["ICD 연결"], ["시험 연결"], ["결과 증거 연결"]];
  summary.getRange("E5:E8").formulas = [
    ["=COUNTA(Traceability!E6:E100)/B5"],
    ["=COUNTA(Traceability!F6:F100)/B5"],
    ["=COUNTA(Traceability!G6:G100)/B5"],
    ["=COUNTA(Traceability!H6:H100)/B5"],
  ];
  summary.getRange("E5:E8").format.numberFormat = "0.0%";
  summary.getRange("A:A").format.columnWidth = 26;
  summary.getRange("B:B").format.columnWidth = 15;
  summary.getRange("C:C").format.columnWidth = 4;
  summary.getRange("D:D").format.columnWidth = 28;
  summary.getRange("E:E").format.columnWidth = 16;
  summary.getRange("A13:E15").values = [
    ["사용 규칙", "", "", "", ""],
    ["요구사항은 하나의 검증 가능한 shall 문장으로 유지하고 수치·조건·대상을 포함합니다.", "", "", "", ""],
    ["Verified는 실제 시험 결과와 승인된 증거 경로가 있을 때만 선택합니다.", "", "", "", ""],
  ];
  summary.getRange("A13:E13").format = { fill: light, font: { name: font, bold: true, color: dark } };
  summary.getRange("A14:E15").format.wrapText = true;
  summary.getRange("A14:E15").format.rowHeight = 28;

  wb.recalculate();
  const inspect = await wb.inspect({ kind: "table", range: "Summary!A4:E10", include: "values,formulas", tableMaxRows: 15, tableMaxCols: 8 });
  console.log(inspect.ndjson);
  const errors = await wb.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!", options: { useRegex: true, maxResults: 100 }, summary: "traceability formula errors" });
  console.log(errors.ndjson);
  for (const [sheetName, fileName] of [["Summary", "traceability-summary.png"], ["Traceability", "traceability.png"]]) {
    const preview = await wb.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
    await fs.writeFile(`${outDir}/${fileName}`, new Uint8Array(await preview.arrayBuffer()));
  }
  const out = await SpreadsheetFile.exportXlsx(wb);
  await out.save(`${outDir}/requirements-traceability.xlsx`);
}

await buildLinkBudget();
await buildTraceability();
