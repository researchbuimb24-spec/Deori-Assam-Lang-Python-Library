"""Numerals and numeral classifier module for Deori."""

from __future__ import annotations


def to_words(n: int) -> str | None:
    """Convert an integer to its attested Deori numeral representation."""
    del n
    return None


def to_int(word: str) -> int | None:
    """Convert a Deori numeral string to an integer."""
    del word
    return None


__all__ = ["to_int", "to_words"]
