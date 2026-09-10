#!/usr/bin/env python3
"""CCSDS Space Packet primary header 생성·분석 및 CRC-16 검사 도구."""

from __future__ import annotations

import argparse
import json
import struct
from dataclasses import asdict, dataclass


PRIMARY_HEADER_SIZE = 6


@dataclass(frozen=True)
class PrimaryHeader:
    version: int
    packet_type: int
    secondary_header_flag: int
    apid: int
    sequence_flags: int
    sequence_count: int
    packet_data_length_field: int
    packet_data_octets: int
    expected_total_octets: int


def crc16_ccitt_false(data: bytes) -> int:
    """CRC-16/CCITT-FALSE: poly 0x1021, init 0xFFFF, xorout 0x0000."""
    crc = 0xFFFF
    for octet in data:
        crc ^= octet << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


def parse_packet(packet: bytes, crc_present: bool = False) -> dict[str, object]:
    if len(packet) < PRIMARY_HEADER_SIZE:
        raise ValueError("packet은 CCSDS primary header 6 octet보다 짧습니다")
    first, second, length_field = struct.unpack(">HHH", packet[:PRIMARY_HEADER_SIZE])
    header = PrimaryHeader(
        version=(first >> 13) & 0x7,
        packet_type=(first >> 12) & 0x1,
        secondary_header_flag=(first >> 11) & 0x1,
        apid=first & 0x7FF,
        sequence_flags=(second >> 14) & 0x3,
        sequence_count=second & 0x3FFF,
        packet_data_length_field=length_field,
        packet_data_octets=length_field + 1,
        expected_total_octets=PRIMARY_HEADER_SIZE + length_field + 1,
    )
    warnings: list[str] = []
    if header.version != 0:
        warnings.append("CCSDS Space Packet Protocol version 0이 아닙니다")
    if len(packet) != header.expected_total_octets:
        warnings.append(
            f"길이 불일치: header 예상 {header.expected_total_octets}, 실제 {len(packet)} octet"
        )
    payload_end = min(len(packet), header.expected_total_octets)
    data_field = packet[PRIMARY_HEADER_SIZE:payload_end]
    crc_result: dict[str, object] | None = None
    if crc_present:
        if len(data_field) < 2:
            warnings.append("CRC가 있다고 지정했지만 data field가 2 octet보다 짧습니다")
        else:
            received = int.from_bytes(data_field[-2:], "big")
            calculated = crc16_ccitt_false(packet[: payload_end - 2])
            crc_result = {
                "profile": "CRC-16/CCITT-FALSE (example; mission profile 확인 필요)",
                "received_hex": f"0x{received:04X}",
                "calculated_hex": f"0x{calculated:04X}",
                "valid": received == calculated,
            }
    return {
        "primary_header": asdict(header),
        "interpretation": {
            "packet_type": "TC (telecommand)" if header.packet_type else "TM (telemetry)",
            "sequence_flags": {
                0: "continuation segment",
                1: "first segment",
                2: "last segment",
                3: "unsegmented",
            }[header.sequence_flags],
            "data_field_hex": data_field.hex().upper(),
        },
        "crc": crc_result,
        "warnings": warnings,
    }


def build_packet(
    apid: int,
    packet_type: int,
    sequence_count: int,
    payload: bytes,
    secondary_header: bool,
    add_crc: bool,
) -> bytes:
    if not 0 <= apid <= 0x7FF:
        raise ValueError("APID는 0..2047 범위여야 합니다")
    if not 0 <= sequence_count <= 0x3FFF:
        raise ValueError("sequence count는 0..16383 범위여야 합니다")
    data = payload
    data_octets = len(payload) + (2 if add_crc else 0)
    if not 1 <= data_octets <= 65536:
        raise ValueError("packet data field는 1..65536 octet 범위여야 합니다")
    first = ((packet_type & 1) << 12) | (int(secondary_header) << 11) | apid
    second = (0b11 << 14) | sequence_count
    header = struct.pack(">HHH", first, second, data_octets - 1)
    if add_crc:
        data += crc16_ccitt_false(header + payload).to_bytes(2, "big")
    return header + data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    decode = sub.add_parser("decode", help="hex Space Packet을 분석")
    decode.add_argument("hex_packet", help="공백을 포함해도 되는 hexadecimal octet")
    decode.add_argument("--crc", action="store_true", help="끝 2 octet을 CRC-16으로 검사")
    build = sub.add_parser("build", help="unsegmented packet을 생성 후 다시 분석")
    build.add_argument("--apid", type=int, default=100)
    build.add_argument("--type", choices=["tm", "tc"], default="tm")
    build.add_argument("--sequence", type=int, default=1)
    build.add_argument("--payload-hex", default="01020304")
    build.add_argument("--secondary-header", action="store_true")
    build.add_argument("--crc", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        if args.command == "decode":
            packet = bytes.fromhex(args.hex_packet)
            result = parse_packet(packet, args.crc)
        else:
            packet = build_packet(
                args.apid,
                1 if args.type == "tc" else 0,
                args.sequence,
                bytes.fromhex(args.payload_hex),
                args.secondary_header,
                args.crc,
            )
            result = {"packet_hex": packet.hex().upper(), **parse_packet(packet, args.crc)}
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except ValueError as error:
        raise SystemExit(f"입력 오류: {error}") from error


if __name__ == "__main__":
    main()
