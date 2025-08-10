"""Dedupe utilities for findings."""
from __future__ import annotations
import hashlib
import re
from typing import Iterable, List, Dict, TypedDict

STOPWORDS = {"the", "a", "an", "and", "or", "to", "of"}


def normalize_title(title: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9 ]", "", title).lower()
    return " ".join(w for w in cleaned.split() if w not in STOPWORDS)


def line_bucket(line: int) -> int:
    return line // 5


def dedupe_key(file: str, rule_id: str, title: str, line: int) -> str:
    title_norm = normalize_title(title)
    bucket = line_bucket(line)
    key = f"{file}|{rule_id}|{title_norm}|{bucket}"
    return hashlib.sha1(key.encode()).hexdigest()


def user_issue_key(rule_id: str, title: str) -> str:
    title_norm = normalize_title(title)
    key = f"{rule_id}|{title_norm}"
    return hashlib.sha1(key.encode()).hexdigest()


class FindingDict(TypedDict):
    file: str
    rule_id: str
    title: str
    start_line: int


def map_findings(old: List[FindingDict], new: List[FindingDict]) -> Dict[str, str]:
    """Map old findings to new by dedupe_key. Return statuses."""
    new_keys = {dedupe_key(f["file"], f["rule_id"], f["title"], f["start_line"]): f for f in new}
    result = {}
    for f in old:
        key = dedupe_key(f["file"], f["rule_id"], f["title"], f["start_line"])
        result[key] = "resolved" if key not in new_keys else "open"
    return result
