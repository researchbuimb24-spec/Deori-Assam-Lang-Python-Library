"""Corpus loading and interlinear glossing for Deori."""

from __future__ import annotations

from typing import Any

from deori.corpus.glosser import gloss_sentence


def load(corpus_id: str) -> list[dict[str, Any]]:
    """Load a documented Deori corpus (e.g. 'brown_1895')."""
    del corpus_id
    return []


__all__ = ["gloss_sentence", "load"]
