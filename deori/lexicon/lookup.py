"""Lexicon lookup implementations for Deori."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from deori.models import LexiconEntry, Variety


def lookup_word(
    query: str,
    to: str = "en",
    *,
    variety: Variety | str | None = None,
    fuzzy: bool = False,
    limit: int = 10,
) -> list[LexiconEntry]:
    """Look up a word across Deori, Assamese, and English.

    Args:
        query: Search term in Deori or gloss language.
        to: Target translation language.
        variety: Optional variety filter.
        fuzzy: If True, uses fuzzy matching.
        limit: Max entries to return.

    Returns:
        List of matching LexiconEntry objects. Returns empty list if not found.
    """
    del query, to, variety, fuzzy, limit
    # Full loader and indexing will be loaded in Milestone 2
    return []
