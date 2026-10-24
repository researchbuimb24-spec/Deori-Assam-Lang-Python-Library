"""Script detection and classification for Deori orthographies."""

from __future__ import annotations

import unicodedata

from deori.models import Script

# Unicode ranges for Assamese-Bengali script
ASSAMESE_BENGALI_MIN = 0x0980
ASSAMESE_BENGALI_MAX = 0x09FF

# Characters indicative of Brown (1895) romanization
BROWN_MACRONS = {"ā", "ī", "ū", "ē", "ō", "Ā", "Ī", "Ū", "Ē", "Ō"}

# Characters indicative of IPA phonemic representations
IPA_CHARS = {
    "ə",
    "ɛ",
    "ɔ",
    "ɨ",
    "ɯ",
    "ɲ",
    "ŋ",
    "ʔ",
    "ʃ",
    "ʒ",
    "θ",
    "ð",
    "ɕ",
    "ʑ",
    "ʈ",
    "ɖ",
    "ɸ",
    "β",
    "ɡ",
    "ː",
    "̃",
    "ʰ",
    "ʲ",
}


def is_assamese_char(char: str) -> bool:
    """Return True if character is within the Bengali/Assamese Unicode block."""
    cp = ord(char)
    return ASSAMESE_BENGALI_MIN <= cp <= ASSAMESE_BENGALI_MAX


def detect_script(text: str) -> Script:
    """Detect the script/orthography of input Deori text.

    Distinguishes:
        - Script.ASSAMESE: Assamese/Bengali Indic script characters.
        - Script.ROMAN_BROWN: Latin script with macron diacritics (Brown 1895).
        - Script.ROMAN_COMMUNITY: Latin script used in community publications
          (e.g. digraph 'cch').
        - Script.IPA: International Phonetic Alphabet characters.
        - Script.UNKNOWN: Empty, punctuation-only, or unrecognized scripts.

    Args:
        text: Input string.

    Returns:
        Script enum member.

    Examples:
        >>> detect_script("দেউৰী")
        <Script.ASSAMESE: 'assamese'>
        >>> detect_script("Deori Cchu")
        <Script.ROMAN_COMMUNITY: 'roman_community'>
        >>> detect_script("dāsi")
        <Script.ROMAN_BROWN: 'roman_brown'>
    """
    if not text or not text.strip():
        return Script.UNKNOWN

    norm = unicodedata.normalize("NFC", text)

    assamese_count = 0
    latin_count = 0
    ipa_count = 0
    total_alpha = 0

    has_brown_macron = any(ch in BROWN_MACRONS for ch in norm)
    has_ipa = any(ch in IPA_CHARS for ch in norm)

    for ch in norm:
        if ch.isalpha():
            total_alpha += 1
            if is_assamese_char(ch):
                assamese_count += 1
            elif "LATIN" in unicodedata.name(ch, ""):
                latin_count += 1
            if ch in IPA_CHARS:
                ipa_count += 1

    if total_alpha == 0:
        return Script.UNKNOWN

    if assamese_count / total_alpha > 0.4:
        return Script.ASSAMESE

    if has_ipa or (ipa_count / total_alpha > 0.2):
        return Script.IPA

    if latin_count > 0:
        if has_brown_macron:
            return Script.ROMAN_BROWN
        return Script.ROMAN_COMMUNITY

    return Script.UNKNOWN
