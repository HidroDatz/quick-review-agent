#!/usr/bin/env python3
"""CI guard to validate MR description template."""
import sys
from app.services.template_parser import parse_description


def main() -> int:
    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    try:
        parse_description(text)
    except Exception as exc:  # pragma: no cover - simple script
        print(f"Template invalid: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
