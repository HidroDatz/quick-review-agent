import json
import pytest
from app.utils.json_validator import validate_json


def test_validate_json_success():
    data = {
        "findings": [
            {
                "file": "a.py",
                "start_line": 1,
                "end_line": 1,
                "severity": "low",
                "category": "style",
                "rule_id": "PY.STYLE.DUMMY",
                "rule_version": "1.0.0",
                "title": "x",
                "rationale": "r",
                "recommendation": "fix",
                "patch": "",
            }
        ],
        "confidence": 0.5,
    }
    validate_json(json.dumps(data))


def test_validate_json_failure():
    with pytest.raises(Exception):
        validate_json("{bad json}")
