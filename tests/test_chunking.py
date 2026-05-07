import pytest

from app.chunking import chunk_text
from app.errors import InvalidParameterError


def test_chunk_empty_returns_empty():
    assert chunk_text("") == []
    assert chunk_text("   \n\t  ") == []


def test_chunk_short_returns_single():
    assert chunk_text("hello world") == ["hello world"]


def test_chunk_splits_long_text():
    text = ("Sentence number one. " * 100).strip()
    chunks = chunk_text(text, chunk_size=200, chunk_overlap=20)
    assert len(chunks) > 1
    # No chunk should massively exceed the target size.
    for c in chunks:
        assert len(c) <= 220


def test_chunk_overlap_is_applied():
    # Use a text long enough to span multiple chunks at the validated minimum size (100).
    sentence = "The quick brown fox jumps over the lazy dog. "
    text = sentence * 20  # ~900 chars
    chunks = chunk_text(text, chunk_size=200, chunk_overlap=50)
    assert len(chunks) >= 2
    # Pairwise: a tail substring of `a` should appear in the start window of `b`.
    for a, b in zip(chunks, chunks[1:]):
        tail = a[-30:]
        assert any(tail[i:i + 5] in b[:80] for i in range(len(tail) - 4)), (
            f"no overlap between {a!r} and {b!r}"
        )


def test_chunk_rejects_bad_size():
    with pytest.raises(InvalidParameterError):
        chunk_text("hi", chunk_size=10)
    with pytest.raises(InvalidParameterError):
        chunk_text("hi", chunk_size=5000)


def test_chunk_rejects_overlap_ge_size():
    with pytest.raises(InvalidParameterError):
        chunk_text("hi", chunk_size=200, chunk_overlap=200)


def test_chunk_rejects_bad_overlap():
    with pytest.raises(InvalidParameterError):
        chunk_text("hi", chunk_size=200, chunk_overlap=-1)
    with pytest.raises(InvalidParameterError):
        chunk_text("hi", chunk_size=200, chunk_overlap=999)


def test_chunk_prefers_paragraph_breaks():
    a = "First paragraph here. " * 10
    b = "Second paragraph here. " * 10
    text = a.strip() + "\n\n" + b.strip()
    chunks = chunk_text(text, chunk_size=300, chunk_overlap=30)
    # We just want to confirm the boundary-aware splitter doesn't crash and
    # produces multiple chunks.
    assert len(chunks) >= 2
