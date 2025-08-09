from datetime import datetime, timedelta
from app.services.metrics import counts_by, compute_mr_metrics, avg_time_to_resolve


def test_counts_by():
    items = [{"severity": "low"}, {"severity": "high"}, {"severity": "low"}]
    assert counts_by(items, "severity") == {"low": 2, "high": 1}


def test_compute_mr_metrics():
    f = [{"severity": "low", "category": "style"}]
    metrics = compute_mr_metrics(f)
    assert metrics["counts_by_severity"]["low"] == 1
    assert metrics["counts_by_category"]["style"] == 1


def test_avg_time_to_resolve():
    now = datetime.utcnow()
    f = [{"first_seen_at": now - timedelta(hours=2), "resolved_at": now}]
    assert avg_time_to_resolve(f) == 2.0
