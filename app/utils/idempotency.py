"""Simple in-memory idempotency helper."""
from __future__ import annotations
from typing import Set, Tuple

_seen: Set[Tuple[str, str]] = set()


def already_commented(head_sha: str, key: str) -> bool:
    pair = (head_sha, key)
    if pair in _seen:
        return True
    _seen.add(pair)
    return False
