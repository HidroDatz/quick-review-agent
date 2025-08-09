from app.services.diff_chunker import chunk_diff

def test_chunk_diff_splits():
    diff = "@@\n" + "\n".join([f"+line{i}" for i in range(300)])
    hunks = chunk_diff(diff, max_lines=100)
    assert len(hunks) == 3
    assert all(h.startswith('@@') for h in hunks)
