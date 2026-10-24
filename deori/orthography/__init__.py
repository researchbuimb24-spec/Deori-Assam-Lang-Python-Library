"""Orthography module for Deori:
normalization, script detection, and transliteration.
"""

from deori.orthography.normalize import normalize_text
from deori.orthography.scripts import detect_script, is_assamese_char
from deori.orthography.transliterate import (
    assamese_to_roman_community,
    roman_community_to_assamese,
    transliterate_text,
)

__all__ = [
    "assamese_to_roman_community",
    "detect_script",
    "is_assamese_char",
    "normalize_text",
    "roman_community_to_assamese",
    "transliterate_text",
]
