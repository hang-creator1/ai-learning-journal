"""Text chunking primitives.

Pure functions over `str` — no FastAPI imports. Sentence-friendly: prefers to
break on paragraph (`\\n\\n`) and sentence (`. `, `! `, `? `, `\\n`) boundaries
before falling back to a hard slice. Overlap is character-based and applied
between adjacent chunks so retrieval doesn't lose context across boundaries.
"""

from __future__ import annotations

from app.errors import InvalidParameterError

_CHUNK_SIZE_MIN = 100
_CHUNK_SIZE_MAX = 2000
_CHUNK_OVERLAP_MIN = 0
_CHUNK_OVERLAP_MAX = 500

# Order matters: try the largest semantic unit first.
_BOUNDARIES = ("\n\n", "\n", ". ", "! ", "? ", " ")


def _validate(chunk_size: int, chunk_overlap: int) -> None:
    if not _CHUNK_SIZE_MIN <= chunk_size <= _CHUNK_SIZE_MAX:
        raise InvalidParameterError(
            f"`chunk_size` must be between {_CHUNK_SIZE_MIN} and {_CHUNK_SIZE_MAX}"
        )
    if not _CHUNK_OVERLAP_MIN <= chunk_overlap <= _CHUNK_OVERLAP_MAX:
        raise InvalidParameterError(
            f"`chunk_overlap` must be between {_CHUNK_OVERLAP_MIN} and {_CHUNK_OVERLAP_MAX}"
        )
    if chunk_overlap >= chunk_size:
        raise InvalidParameterError("`chunk_overlap` must be smaller than `chunk_size`")


def _find_break(text: str, target: int) -> int:
    """Return a split index <= target that lands on the nicest boundary we can find.

    Searches a window around `target` for `_BOUNDARIES` in priority order. Falls
    back to the hard target if no boundary is close enough.
    """
    window_lo = max(target - 100, target // 2)
    for sep in _BOUNDARIES:
        idx = text.rfind(sep, window_lo, target)
        if idx != -1:
            return idx + len(sep)
    return target


def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
    """Split `text` into overlapping chunks, biased to semantic boundaries.

    Empty input returns an empty list. A `chunk_size`-or-shorter input returns
    a single-element list. Raises `InvalidParameterError` for out-of-range
    arguments.
    """
    _validate(chunk_size, chunk_overlap)

    text = text.strip()
    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    chunks: list[str] = []
    start = 0
    n = len(text)

    while start < n:
        end_target = start + chunk_size
        if end_target >= n:
            chunk = text[start:].strip()
            if chunk:
                chunks.append(chunk)
            break

        end = _find_break(text, end_target)
        # Guard against pathological no-progress.
        if end <= start:
            end = end_target

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        next_start = end - chunk_overlap
        if next_start <= start:
            next_start = end
        start = next_start

    return chunks
