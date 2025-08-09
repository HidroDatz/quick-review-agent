"""Metrics calculation utilities."""
from __future__ import annotations
from datetime import datetime
from typing import List, Dict


def counts_by(items: List[dict], key: str) -> Dict[str, int]:
    result: Dict[str, int] = {}
    for item in items:
        result[item[key]] = result.get(item[key], 0) + 1
    return result


def compute_mr_metrics(findings: List[dict]) -> Dict[str, Dict[str, int]]:
    return {
        "counts_by_severity": counts_by(findings, "severity"),
        "counts_by_category": counts_by(findings, "category"),
    }


def avg_time_to_resolve(findings: List[dict]) -> float:
    durations = []
    for f in findings:
        if f.get("resolved_at") and f.get("first_seen_at"):
            durations.append((f["resolved_at"] - f["first_seen_at"]).total_seconds() / 3600)
    return sum(durations) / len(durations) if durations else 0.0
