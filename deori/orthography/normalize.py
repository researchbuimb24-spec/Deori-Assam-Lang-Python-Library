"""Unicode and orthographic normalization for Deori text."""

from __future__ import annotations

import unicodedata

# Mapping Bengali-specific code points to standard Assamese script code points
BENGALI_TO_ASSAMESE = {
    "\u09b0": "\u09f0",  # Bengali ro 'র' -> Assamese ro 'ৰ'
}

# Decomposed to precomposed Indic letters with nukta
NUKTA_COMPOSITIONS = {
    "\u09a1\u09bc": "\u09dc",  # ড + nukta -> ড়
    "\u09a2\u09bc": "\u09dd",  # ঢ + nukta -> ঢ়
    "\u09af\u09bc": "\u09df",  # য + nukta -> য়
}

# Quote & apostrophe normalization
APOSTROPHE_MAP = {
    "\u2018": "'",  # Left single quote
    "\u2019": "'",  # Right single quote
    "\u02bc": "'",  # Modifier letter apostrophe
    "\u201c": '"',  # Left double quote
    "\u201d": '"',  # Right double quote
}


def normalize_assamese_chars(text: str) -> str:
    """Normalize Assamese-specific characters and handle Bengali confusions."""
    out = text
    for bengali_ch, assamese_ch in BENGALI_TO_ASSAMESE.items():
        out = out.replace(bengali_ch, assamese_ch)
    for decomposed, precomposed in NUKTA_COMPOSITIONS.items():
        out = out.replace(decomposed, precomposed)
    return out


def clean_invisible_chars(text: str, keep_virama_zwnj: bool = True) -> str:
    """Strip or normalize invisible and non-breaking Unicode characters.

    Args:
        text: Input text.
        keep_virama_zwnj: If True, preserves Virama + ZWNJ sequences which are
            grammatically used in Indic scripts to display explicit halant.
    """
    # Replace non-breaking spaces and zero-width spaces
    out = text.replace("\u00a0", " ").replace("\u200b", "")

    if not keep_virama_zwnj:
        out = out.replace("\u200c", "").replace("\u200d", "")
    else:
        # Only keep ZWNJ if immediately preceded by virama '\u09CD'
        clean_chars: list[str] = []
        for i, ch in enumerate(out):
            if ch == "\u200c" or ch == "\u200d":
                if i > 0 and out[i - 1] == "\u09cd":
                    clean_chars.append(ch)
            else:
                clean_chars.append(ch)
        out = "".join(clean_chars)

    return out


def normalize_text(text: str) -> str:
    """Perform full Unicode and orthographic normalization on Deori text.

    Steps applied:
        1. Unicode Normalization Form C (NFC).
        2. Replace curly quotes and glottal markers with ASCII equivalents.
        3. Convert Bengali-specific confusable characters to Assamese (e.g. র -> ৰ).
        4. Compose nukta combinations (ড + nukta -> ড়, etc.).
        5. Clean non-breaking and spurious zero-width spaces.
        6. Re-apply NFC to ensure composition stability.

    Args:
        text: Input string.

    Returns:
        Normalized string.

    Examples:
        >>> normalize_text("দেউরী")
        'দেউৰী'
        >>> normalize_text("a\\u0304")
        'ā'
    """
    if not text:
        return ""

    # 1. Unicode NFC decomposition to precomposed
    norm = unicodedata.normalize("NFC", text)

    # 2. Quotes and apostrophes
    for k, v in APOSTROPHE_MAP.items():
        norm = norm.replace(k, v)

    # 3. Assamese characters and nukta
    norm = normalize_assamese_chars(norm)

    # 4. Invisible chars
    norm = clean_invisible_chars(norm)

    # 5. Final NFC round
    return unicodedata.normalize("NFC", norm)
