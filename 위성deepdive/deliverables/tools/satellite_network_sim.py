#!/usr/bin/env python3
"""작은 contact-aware 위성 downlink 성능 시뮬레이터.

외부 패키지 없이 재현 가능한 교육용 discrete-event 모델을 제공한다.
실제 궤도, 링크 적응, 상관된 채널 오류나 인증 결과를 대체하지 않는다.
"""

from __future__ import annotations

import argparse
import heapq
import json
import math
import random
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Contact:
    start_s: float
    end_s: float
    rate_bps: float
    loss_probability: float
    propagation_s: float
    acquisition_s: float = 0.0


@dataclass
class Bundle:
    bundle_id: int
    arrival_s: float
    size_bytes: int
    priority: int
    deadline_s: float
    attempts: int = 0
    first_tx_s: float | None = None


def percentile(values: list[float], probability: float) -> float | None:
    """선형 보간 percentile을 계산한다."""
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def default_contacts() -> list[Contact]:
    return [
        Contact(20, 80, 2_000_000, 0.02, 0.006, 2.0),
        Contact(140, 205, 1_200_000, 0.05, 0.008, 3.0),
        Contact(280, 350, 3_000_000, 0.01, 0.005, 1.0),
    ]


def generate_traffic(
    rng: random.Random,
    duration_s: float,
    arrival_rate_hz: float,
    payload_bytes: int,
) -> list[Bundle]:
    """Poisson arrival과 두 priority class를 생성한다."""
    bundles: list[Bundle] = []
    now = 0.0
    while arrival_rate_hz > 0:
        now += rng.expovariate(arrival_rate_hz)
        if now > duration_s:
            break
        critical = rng.random() < 0.15
        size = max(64, int(payload_bytes * rng.uniform(0.6, 1.4)))
        bundles.append(
            Bundle(
                bundle_id=len(bundles) + 1,
                arrival_s=now,
                size_bytes=size,
                priority=0 if critical else 1,
                deadline_s=now + (60 if critical else 300),
            )
        )
    return bundles


def simulate(
    contacts: list[Contact],
    traffic: list[Bundle],
    rng: random.Random,
    buffer_bytes: int,
    max_retries: int,
    protocol_header_bytes: int,
) -> dict[str, object]:
    queue: list[tuple[int, float, int, Bundle]] = []
    queued_bytes = 0
    max_queue_bytes = 0
    admitted = 0
    delivered: list[dict[str, float | int]] = []
    drops = {"buffer": 0, "deadline": 0, "retry_limit": 0, "unfinished": 0}
    traffic_index = 0
    transmitted_bits = 0
    retransmissions = 0

    for contact in sorted(contacts, key=lambda item: item.start_s):
        now = contact.start_s + contact.acquisition_s
        while traffic_index < len(traffic) and traffic[traffic_index].arrival_s <= now:
            bundle = traffic[traffic_index]
            traffic_index += 1
            if queued_bytes + bundle.size_bytes > buffer_bytes:
                drops["buffer"] += 1
                continue
            heapq.heappush(queue, (bundle.priority, bundle.arrival_s, bundle.bundle_id, bundle))
            queued_bytes += bundle.size_bytes
            admitted += 1
        while now < contact.end_s and (
            queue
            or (
                traffic_index < len(traffic)
                and traffic[traffic_index].arrival_s < contact.end_s
            )
        ):
            if not queue and traffic_index < len(traffic):
                now = max(now, traffic[traffic_index].arrival_s)
            while traffic_index < len(traffic) and traffic[traffic_index].arrival_s <= now:
                bundle = traffic[traffic_index]
                traffic_index += 1
                if queued_bytes + bundle.size_bytes > buffer_bytes:
                    drops["buffer"] += 1
                else:
                    heapq.heappush(queue, (bundle.priority, bundle.arrival_s, bundle.bundle_id, bundle))
                    queued_bytes += bundle.size_bytes
                    admitted += 1

            max_queue_bytes = max(max_queue_bytes, queued_bytes)
            if not queue:
                continue

            _, _, _, bundle = heapq.heappop(queue)
            queued_bytes -= bundle.size_bytes
            if now > bundle.deadline_s:
                drops["deadline"] += 1
                continue
            bits = (bundle.size_bytes + protocol_header_bytes) * 8
            serialization_s = bits / contact.rate_bps
            if now + serialization_s > contact.end_s:
                heapq.heappush(queue, (bundle.priority, bundle.arrival_s, bundle.bundle_id, bundle))
                queued_bytes += bundle.size_bytes
                break
            if bundle.first_tx_s is None:
                bundle.first_tx_s = now
            bundle.attempts += 1
            transmitted_bits += bits
            now += serialization_s
            if rng.random() < contact.loss_probability:
                if bundle.attempts <= max_retries:
                    retransmissions += 1
                    heapq.heappush(queue, (bundle.priority, bundle.arrival_s, bundle.bundle_id, bundle))
                    queued_bytes += bundle.size_bytes
                else:
                    drops["retry_limit"] += 1
                continue
            delivery_s = now + contact.propagation_s
            if delivery_s > bundle.deadline_s:
                drops["deadline"] += 1
            else:
                delivered.append(
                    {
                        "id": bundle.bundle_id,
                        "latency_s": delivery_s - bundle.arrival_s,
                        "queue_wait_s": (bundle.first_tx_s or now) - bundle.arrival_s,
                        "size_bytes": bundle.size_bytes,
                        "priority": bundle.priority,
                        "attempts": bundle.attempts,
                    }
                )
            max_queue_bytes = max(max_queue_bytes, queued_bytes)

    drops["unfinished"] = len(queue) + (len(traffic) - traffic_index)
    latencies = [float(item["latency_s"]) for item in delivered]
    waits = [float(item["queue_wait_s"]) for item in delivered]
    delivered_payload_bytes = sum(int(item["size_bytes"]) for item in delivered)
    duration = max((contact.end_s for contact in contacts), default=0.0)
    generated = len(traffic)
    return {
        "model": "educational contact-aware single-path downlink",
        "generated_bundles": generated,
        "admitted_bundles": admitted,
        "delivered_bundles": len(delivered),
        "delivery_ratio": len(delivered) / generated if generated else 1.0,
        "drops": drops,
        "goodput_bps": delivered_payload_bytes * 8 / duration if duration else 0.0,
        "transmitted_bps": transmitted_bits / duration if duration else 0.0,
        "retransmissions": retransmissions,
        "latency_s": {
            "p50": percentile(latencies, 0.50),
            "p95": percentile(latencies, 0.95),
            "p99": percentile(latencies, 0.99),
            "maximum": max(latencies, default=None),
        },
        "queue_wait_s": {"p95": percentile(waits, 0.95)},
        "max_queue_bytes": max_queue_bytes,
        "contacts": [asdict(contact) for contact in contacts],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--duration", type=float, default=360.0, help="traffic 생성 시간(s)")
    parser.add_argument("--arrival-rate", type=float, default=25.0, help="평균 bundle/s")
    parser.add_argument("--payload", type=int, default=1024, help="평균 payload byte")
    parser.add_argument("--buffer", type=int, default=8_000_000, help="onboard buffer byte")
    parser.add_argument("--max-retries", type=int, default=2)
    parser.add_argument("--header", type=int, default=64, help="전체 protocol overhead byte")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rng = random.Random(args.seed)
    traffic = generate_traffic(rng, args.duration, args.arrival_rate, args.payload)
    result = simulate(
        default_contacts(), traffic, rng, args.buffer, args.max_retries, args.header
    )
    result["parameters"] = vars(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
