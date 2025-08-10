"""Parse merge request descriptions adhering to the project template."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List
import re
import yaml


SECTION_HEADERS = [
    "Summary",
    "Motivation & Context",
    "Implementation Details",
    "Affected Areas",
    "Testing Plan",
    "Security & Performance",
    "Rollback Plan",
    "Reviewer Hints",
    "Screenshots / Logs",
]


@dataclass
class MRContext:
    meta: Dict[str, str]
    summary: str
    implementation: str
    testing: str
    secperf: str
    hints: str
    languages: List[str]


def translate_vi(text: str) -> str:
    """Stub translation function removing the [VI] prefix."""
    return re.sub(r"^\[VI\]\s*", "", text.strip())


def parse_description(description: str) -> MRContext:
    """Parse the MR description and return structured context."""
    fm_match = re.match(r"---\n(.*?)\n---", description, re.DOTALL)
    if not fm_match:
        raise ValueError("Missing YAML front matter")
    meta = yaml.safe_load(fm_match.group(1)) or {}
    body = description[fm_match.end():]
    sections: Dict[str, List[str]] = {}
    current = None
    lines = body.splitlines()
    for line in lines:
        header = next((h for h in SECTION_HEADERS if line.strip() == f"# {h}"), None)
        if header:
            current = header
            sections[current] = []
            continue
        if current:
            sections[current].append(line)
    def section_text(name: str) -> str:
        raw = "\n".join(sections.get(name, [])).strip()
        paragraphs = [translate_vi(p) for p in re.split(r"\n{2,}", raw) if p]
        return "\n\n".join(paragraphs)
    required = ["Summary", "Implementation Details", "Testing Plan", "Security & Performance", "Reviewer Hints"]
    for req in required:
        if req not in sections:
            raise ValueError(f"Missing section: {req}")
    return MRContext(
        meta=meta,
        summary=section_text("Summary"),
        implementation=section_text("Implementation Details"),
        testing=section_text("Testing Plan"),
        secperf=section_text("Security & Performance"),
        hints=section_text("Reviewer Hints"),
        languages=meta.get("languages", []),
    )
