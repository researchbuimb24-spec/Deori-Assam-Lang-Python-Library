"""Tokenizer implementation for Deori words and morphemes."""

from __future__ import annotations

import regex


def tokenize_text(text: str, level: str = "word") -> list[str]:
    """Tokenize Deori text at word or morpheme level.

    Args:
        text: Input text.
        level: 'word' or 'morpheme'.

    Returns:
        List of string tokens.
    """
    if not text.strip():
        return []
    if level == "word":
        # Unicode word boundary segmentation respecting Indic scripts
        tokens = regex.findall(r"\b\w+\b|[^\w\s]", text, regex.UNICODE)
        return [str(t) for t in tokens if t]
    elif level == "morpheme":
        # Morpheme-level segmentation will hook into the morphological rules in M3/M4
        tokens = regex.findall(r"\b\w+\b|[^\w\s]", text, regex.UNICODE)
        return [str(t) for t in tokens if t]
    else:
        raise ValueError(
            f"Unsupported tokenization level: '{level}'. Use 'word' or 'morpheme'."
        )
