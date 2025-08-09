from app.services.dedupe import dedupe_key, user_issue_key, map_findings


def test_dedupe_key_stable():
    k1 = dedupe_key("a.py", "R1", "Title", 10)
    k2 = dedupe_key("a.py", "R1", "Title", 12)
    assert k1 == k2


def test_user_issue_key():
    assert user_issue_key("R1", "Some Title") == user_issue_key("R1", "Some title!")


def test_map_findings():
    old = [{"file": "a.py", "rule_id": "R1", "title": "t", "start_line": 1}]
    new = []
    result = map_findings(old, new)
    assert list(result.values()) == ["resolved"]
