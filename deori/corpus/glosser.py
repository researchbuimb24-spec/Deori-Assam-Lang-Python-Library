"""Interlinear glossing utility for Deori."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from deori.models import Variety


def gloss_sentence(
    sentence: str,
    *,
    variety: Variety | str | None = None,
) -> str:
    """Generate Leipzig-style gloss string for sentence."""
    del variety
    # Will be populated with Leipzig interlinear alignments in M5
    words = sentence.split()
    return " ".join(["UNKNOWN" for _ in words])
