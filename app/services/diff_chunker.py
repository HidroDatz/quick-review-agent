"""Split unified diffs into hunks capped at 250 lines."""
from __future__ import annotations
from typing import List


def chunk_diff(diff: str, max_lines: int = 250) -> List[str]:
    hunks: List[str] = []
    lines = diff.splitlines()
    current: List[str] = []
    for line in lines:
        if line.startswith('@@'):
            if current:
                hunks.append('\n'.join(current))
                current = []
            current.append(line)
        else:
            if not current:
                continue
            current.append(line)
            if len(current) - 1 >= max_lines:
                hunks.append('\n'.join(current))
                current = [current[0]]
    if current and len(current) > 1:
        hunks.append('\n'.join(current))
    return hunks
