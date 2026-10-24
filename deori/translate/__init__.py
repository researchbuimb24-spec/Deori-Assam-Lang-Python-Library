"""Dictionary- and rule-based gloss translation module for Deori."""

from __future__ import annotations


def translate_gloss(text: str, target: str = "en") -> str:
    """Provide rule-based/dictionary-based gloss translation."""
    del target
    return text


__all__ = ["translate_gloss"]
