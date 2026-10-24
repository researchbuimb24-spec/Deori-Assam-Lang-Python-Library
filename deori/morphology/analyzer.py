"""Morphological analyzer stub for Deori (expanded in M4)."""

from __future__ import annotations

from deori.models import Analysis, Variety


def analyze_word(
    word: str,
    *,
    variety: Variety | str | None = None,
) -> Analysis:
    """Analyze a word into stem and suffixes.

    Returns an Analysis model. If unknown, returns is_known=False and confidence=0.0.
    """
    v = (
        variety
        if isinstance(variety, Variety)
        else (Variety(variety) if variety else Variety.UNSPECIFIED)
    )
    return Analysis(
        surface=word,
        stem=None,
        stem_gloss=None,
        morphemes=[],
        suffixes=[],
        gloss="UNKNOWN",
        variety=v,
        source=None,
        confidence=0.0,
        is_known=False,
    )
