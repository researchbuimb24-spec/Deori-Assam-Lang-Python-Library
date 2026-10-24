"""deori: A Python library for the Deori (Deuri) language (ISO 639-3: der).

This library provides computational and linguistic tools for Deori (Deori Cchu),
an endangered Tibeto-Burman language of Upper Assam and Arunachal Pradesh.

Core API functions:
    - deori.lookup(word, to='en')
    - deori.transliterate(text, src='roman', dst='assamese')
    - deori.normalize(text)
    - deori.tokenize(text, level='word')
    - deori.analyze(word)
    - deori.inflect(stem, features={...})
    - deori.gloss(sentence)
"""

from __future__ import annotations

from typing import Any

from deori.models import (
    Analysis,
    LexiconEntry,
    MorphologicalRule,
    Script,
    SourceCitation,
    TransliterationResult,
    Variety,
)

__version__ = "0.1.0.dev1"
__author__ = "Sagar Joshi and contributors"

__all__ = [
    "Analysis",
    "LexiconEntry",
    "MorphologicalRule",
    "Script",
    "SourceCitation",
    "TransliterationResult",
    "Variety",
    "analyze",
    "gloss",
    "inflect",
    "lookup",
    "normalize",
    "tokenize",
    "transliterate",
]


def normalize(text: str) -> str:
    """Normalize Deori text to Unicode NFC and canonical character mappings.

    Handles Assamese-specific characters (ৰ vs র, ৱ vs ব), virama sequences,
    and strips spurious zero-width non-joiners.

    Args:
        text: Input string in Assamese script or Roman transliteration.

    Returns:
        Unicode NFC normalized string with standard glyph representations.
    """
    from deori.orthography.normalize import normalize_text

    return normalize_text(text)


def transliterate(
    text: str,
    src: Script | str = Script.ROMAN_COMMUNITY,
    dst: Script | str = Script.ASSAMESE,
) -> TransliterationResult:
    """Transliterate Deori text between supported scripts.

    Supported scripts include:
        - `assamese` (or Script.ASSAMESE)
        - `roman_community` (or Script.ROMAN_COMMUNITY, with digraphs like 'cch')
        - `roman_brown` (or Script.ROMAN_BROWN, historical Brown 1895 with macrons)

    Args:
        text: Input text to transliterate.
        src: Source script identifier or Script enum.
        dst: Target script identifier or Script enum.

    Returns:
        TransliterationResult containing mapped text, confidence, and diagnostics.
    """
    from deori.orthography.transliterate import transliterate_text

    return transliterate_text(text, src=src, dst=dst)


def lookup(
    query: str,
    to: str = "en",
    *,
    variety: Variety | str | None = None,
    fuzzy: bool = False,
    limit: int = 10,
) -> list[LexiconEntry]:
    """Look up a word across Deori, Assamese, and English.

    Args:
        query: Search term in Deori (Assamese script or Roman) or translation.
        to: Target gloss language ('en', 'as', or 'der').
        variety: Optional filter for dialect variety (e.g. 'dibongiya').
        fuzzy: If True, performs fuzzy matching with rapidfuzz.
        limit: Maximum number of matches to return.

    Returns:
        List of matching LexiconEntry objects with source citations.
        Returns an empty list for unknown queries (no hallucinated entries).
    """
    from deori.lexicon.lookup import lookup_word

    return lookup_word(query, to=to, variety=variety, fuzzy=fuzzy, limit=limit)


def analyze(word: str, *, variety: Variety | str | None = None) -> Analysis:
    """Analyze the morphological structure of a Deori word.

    Breaks down a surface word into its stem and inflectional/derivational
    suffixes according to declarative morphological rules with page citations.

    Args:
        word: Surface word string.
        variety: Dialect variety to assume. Defaults to UNSPECIFIED.

    Returns:
        Analysis dataclass with stem, suffixes, Leipzig gloss, and source.
        Returns Analysis with is_known=False and confidence=0.0 if not analyzed.
    """
    from deori.morphology.analyzer import analyze_word

    return analyze_word(word, variety=variety)


def inflect(
    stem: str,
    features: dict[str, Any],
    *,
    variety: Variety | str | None = None,
) -> str | None:
    """Inflect a Deori stem given a feature bundle.

    Args:
        stem: Base stem or root.
        features: Grammatical features e.g. {'case': 'locative'} or {'tense': 'past'}.
        variety: Dialect variety.

    Returns:
        Inflected surface form, or None if rules cannot satisfy features.
    """
    from deori.morphology.inflect import inflect_stem

    return inflect_stem(stem, features, variety=variety)


def tokenize(text: str, level: str = "word") -> list[str]:
    """Tokenize Deori text at word or morpheme level.

    Args:
        text: Input sentence or discourse.
        level: 'word' or 'morpheme'.

    Returns:
        List of string tokens.
    """
    from deori.tokenizer.tokenize import tokenize_text

    return tokenize_text(text, level=level)


def gloss(sentence: str, *, variety: Variety | str | None = None) -> str:
    """Generate Leipzig-style interlinear gloss for a Deori sentence.

    Args:
        sentence: Input sentence in Deori.
        variety: Variety to condition analysis on.

    Returns:
        Interlinear gloss string.
    """
    from deori.corpus.glosser import gloss_sentence

    return gloss_sentence(sentence, variety=variety)
