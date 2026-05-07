"""Embedding engine — sentence-transformers wrapper.

Lazy-loaded singleton: the model (~90MB for MiniLM) is only loaded on first
call. Tests bypass this entirely by monkey-patching `embed`.
"""

from __future__ import annotations

import os
import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer  # pragma: no cover

DEFAULT_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
DEFAULT_DIM = 384  # MiniLM-L6-v2

_lock = threading.Lock()
_model: "SentenceTransformer | None" = None


def _load_model() -> "SentenceTransformer":
    global _model
    if _model is None:
        with _lock:
            if _model is None:
                from sentence_transformers import SentenceTransformer  # noqa: WPS433

                _model = SentenceTransformer(DEFAULT_MODEL)
    return _model


def embedding_dim() -> int:
    """Return embedding dimensionality without forcing a model load when possible.

    Returns the known dimension of the default model (`DEFAULT_DIM`) for fast
    startup. If `EMBEDDING_MODEL` was overridden, loads the model lazily and
    asks it directly.
    """
    if DEFAULT_MODEL == "sentence-transformers/all-MiniLM-L6-v2":
        return DEFAULT_DIM
    return int(_load_model().get_sentence_embedding_dimension() or DEFAULT_DIM)


def embed(texts: list[str]) -> list[list[float]]:
    """Encode a batch of strings into dense vectors.

    Returns a plain `list[list[float]]` so callers don't need to depend on numpy.
    """
    if not texts:
        return []
    model = _load_model()
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return [list(map(float, v)) for v in vectors]
