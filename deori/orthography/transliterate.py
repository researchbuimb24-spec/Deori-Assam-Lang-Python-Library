"""Transliteration engine for Deori orthographies.

Supports bidirectional transliteration between:
    - Assamese Indic script (দেউৰী চু)
    - Community Roman orthography (with 'cch', etc.)
    - Brown (1895) historical Roman orthography (with macrons)
"""

from __future__ import annotations

import json
from importlib import resources
from pathlib import Path
from typing import Any

from deori.models import Script, TransliterationResult
from deori.orthography.normalize import normalize_text
from deori.orthography.scripts import detect_script

# Inherent vowel in Assamese script for Deori
DEFAULT_INHERENT_VOWEL = "o"


def _load_orthography_data() -> dict[str, Any]:
    """Load the bundled JSON orthography tables."""
    try:
        # Python 3.9+ importlib.resources.files
        res_path = resources.files("deori.data.orthography").joinpath(
            "assamese_roman.json"
        )
        return json.loads(res_path.read_text(encoding="utf-8"))  # type: ignore[no-any-return]
    except Exception:
        # Fallback to direct path
        p = (
            Path(__file__).parent.parent
            / "data"
            / "orthography"
            / "assamese_roman.json"
        )
        with open(p, encoding="utf-8") as f:
            return json.load(f)  # type: ignore[no-any-return]


_DATA = _load_orthography_data()
INDEPENDENT_VOWELS: dict[str, str] = _DATA["vowels"]["independent"]
DEPENDENT_VOWELS: dict[str, str] = _DATA["vowels"]["dependent"]
CONSONANTS: dict[str, str] = _DATA["consonants"]
SIGNS: dict[str, str] = _DATA.get("signs", {})
ROMAN_TO_ASSAMESE: dict[str, str] = _DATA.get("roman_to_assamese", {})

# Reverse mappings
ROMAN_TO_INDEP_VOWELS = {
    "a": "আ",
    "aa": "আ",
    "i": "ই",
    "ee": "ঈ",
    "u": "উ",
    "oo": "ঊ",
    "e": "এ",
    "ai": "ঐ",
    "oi": "ঐ",
    "o": "অ",
    "ou": "ঔ",
    "au": "ঔ",
}

ROMAN_TO_DEP_VOWELS = {
    "a": "া",
    "aa": "া",
    "i": "ি",
    "ee": "ী",
    "u": "ু",
    "oo": "ূ",
    "e": "ে",
    "ai": "ৈ",
    "oi": "ৈ",
    "o": "ো",
    "ou": "ৌ",
    "au": "ৌ",
}

# Brown macron mappings
BROWN_TO_COMMUNITY = {
    "ā": "a",
    "ī": "i",
    "ū": "u",
    "ē": "e",
    "ō": "o",
    "Ā": "A",
    "Ī": "I",
    "Ū": "U",
    "Ē": "E",
    "Ō": "O",
}

COMMUNITY_TO_BROWN = {
    "aa": "ā",
    "ee": "ī",
    "oo": "ū",
}


def _resolve_script(val: Script | str) -> Script:
    """Normalize script argument to a Script enum."""
    if isinstance(val, Script):
        return val
    s = val.lower().strip()
    if s in ("assamese", "as", "indic"):
        return Script.ASSAMESE
    if s in ("roman", "roman_community", "community"):
        return Script.ROMAN_COMMUNITY
    if s in ("roman_brown", "brown"):
        return Script.ROMAN_BROWN
    if s == "ipa":
        return Script.IPA
    return Script.UNKNOWN


def assamese_to_roman_community(text: str) -> tuple[str, list[str]]:
    """Convert Assamese script text to Community Roman orthography."""
    norm = normalize_text(text)
    out: list[str] = []
    unmapped: list[str] = []
    i = 0
    n = len(norm)

    while i < n:
        # Check 2-character conjuncts first
        two_char = norm[i : i + 2]
        if two_char in CONSONANTS:
            # Check following character for matra or virama
            cons_rom = CONSONANTS[two_char]
            i += 2
            if i < n and norm[i] == "\u09cd":  # Virama
                out.append(cons_rom)
                i += 1
            elif i < n and norm[i] in DEPENDENT_VOWELS:
                out.append(cons_rom + DEPENDENT_VOWELS[norm[i]])
                i += 1
            else:
                out.append(cons_rom + DEFAULT_INHERENT_VOWEL)
            continue

        ch = norm[i]

        # 1. Independent vowels
        if ch in INDEPENDENT_VOWELS:
            out.append(INDEPENDENT_VOWELS[ch])
            i += 1
            continue

        # 2. Consonants
        if ch in CONSONANTS:
            cons_rom = CONSONANTS[ch]
            i += 1
            if i < n and norm[i] == "\u09cd":  # Virama / hasanta
                out.append(cons_rom)
                i += 1
            elif i < n and norm[i] in DEPENDENT_VOWELS:
                out.append(cons_rom + DEPENDENT_VOWELS[norm[i]])
                i += 1
            else:
                # If followed by another consonant or whitespace or sign.
                # In Indic Deori, word-final consonant without matra
                # sometimes drops inherent vowel; standard translit preserves it.
                if i < n and (
                    norm[i].isspace() or norm[i] in SIGNS or norm[i] in ".,!?-"
                ):
                    out.append(cons_rom)
                else:
                    out.append(cons_rom + DEFAULT_INHERENT_VOWEL)
            continue

        # 3. Dependent vowels (unattached or stray)
        if ch in DEPENDENT_VOWELS:
            out.append(DEPENDENT_VOWELS[ch])
            i += 1
            continue

        # 4. Signs
        if ch in SIGNS:
            out.append(SIGNS[ch])
            i += 1
            continue

        # 5. Non-Assamese characters (punctuation, numbers, spaces)
        out.append(ch)
        if ch.isalpha() and ord(ch) >= 0x0980 and ord(ch) <= 0x09FF:
            unmapped.append(ch)
        i += 1

    return "".join(out), unmapped


def roman_community_to_assamese(text: str) -> tuple[str, list[str]]:
    """Convert Community Roman orthography to Assamese script."""
    norm = normalize_text(text)
    out: list[str] = []
    unmapped: list[str] = []
    i = 0
    n = len(norm)

    # Sort multi-character roman clusters by length descending
    sorted_rom_cons = sorted(ROMAN_TO_ASSAMESE.keys(), key=len, reverse=True)
    sorted_rom_vowels = sorted(ROMAN_TO_DEP_VOWELS.keys(), key=len, reverse=True)

    while i < n:
        ch = norm[i]

        # If whitespace or punctuation, preserve as is
        if not ch.isalpha():
            out.append(ch)
            i += 1
            continue

        # Check for consonant match
        matched_cons: str | None = None
        lower_sub = norm[i:].lower()
        for r_cons in sorted_rom_cons:
            if lower_sub.startswith(r_cons):
                matched_cons = r_cons
                break

        if matched_cons is not None:
            as_cons = ROMAN_TO_ASSAMESE[matched_cons]
            i += len(matched_cons)

            # Check if followed by vowel
            matched_vow: str | None = None
            lower_vow_sub = norm[i:].lower()
            for r_vow in sorted_rom_vowels:
                if lower_vow_sub.startswith(r_vow):
                    matched_vow = r_vow
                    break

            if matched_vow is not None:
                i += len(matched_vow)
                if matched_vow == "o":
                    # Inherent vowel, so no matra needed
                    out.append(as_cons)
                else:
                    out.append(as_cons + ROMAN_TO_DEP_VOWELS[matched_vow])
            else:
                # Consonant with no following vowel: add virama
                # Check if followed by another letter
                if i < n and norm[i].isalpha():
                    out.append(as_cons + "\u09cd")
                else:
                    out.append(as_cons + "\u09cd")
            continue

        # Check for independent vowel match
        matched_indep_vow: str | None = None
        for r_vow in sorted_rom_vowels:
            if lower_sub.startswith(r_vow):
                matched_indep_vow = r_vow
                break

        if matched_indep_vow is not None:
            out.append(ROMAN_TO_INDEP_VOWELS[matched_indep_vow])
            i += len(matched_indep_vow)
            continue

        # Unmatched alpha char
        out.append(ch)
        unmapped.append(ch)
        i += 1

    return "".join(out), unmapped


def transliterate_text(
    text: str,
    src: Script | str = Script.ROMAN_COMMUNITY,
    dst: Script | str = Script.ASSAMESE,
) -> TransliterationResult:
    """Transliterate Deori text between scripts with diagnostics."""
    if not text:
        s = _resolve_script(src)
        d = _resolve_script(dst)
        return TransliterationResult(
            source_text="",
            target_text="",
            source_script=s,
            target_script=d,
            confidence=1.0,
            unmapped_chars=[],
            warnings=[],
        )

    resolved_src = _resolve_script(src)
    resolved_dst = _resolve_script(dst)

    # Auto-detect if src is UNKNOWN
    if resolved_src == Script.UNKNOWN:
        resolved_src = detect_script(text)
        if resolved_src == Script.UNKNOWN:
            resolved_src = Script.ROMAN_COMMUNITY

    warnings: list[str] = []
    unmapped: list[str] = []
    intermediate = normalize_text(text)

    # 1. From Brown Roman -> Community Roman
    if resolved_src == Script.ROMAN_BROWN:
        for b_ch, c_ch in BROWN_TO_COMMUNITY.items():
            intermediate = intermediate.replace(b_ch, c_ch)
        if resolved_dst == Script.ROMAN_COMMUNITY:
            return TransliterationResult(
                source_text=text,
                target_text=intermediate,
                source_script=resolved_src,
                target_script=resolved_dst,
                confidence=1.0,
            )
        resolved_src = Script.ROMAN_COMMUNITY

    # 2. Assamese -> Roman Community
    if resolved_src == Script.ASSAMESE and resolved_dst in (
        Script.ROMAN_COMMUNITY,
        Script.ROMAN_BROWN,
    ):
        target, unmapped = assamese_to_roman_community(intermediate)
        if resolved_dst == Script.ROMAN_BROWN:
            for c_str, b_str in COMMUNITY_TO_BROWN.items():
                target = target.replace(c_str, b_str)
        conf = 1.0 if not unmapped else max(0.0, 1.0 - (len(unmapped) / len(text)))
        return TransliterationResult(
            source_text=text,
            target_text=target,
            source_script=resolved_src,
            target_script=resolved_dst,
            confidence=conf,
            unmapped_chars=unmapped,
            warnings=warnings,
        )

    # 3. Roman Community -> Assamese
    if resolved_src == Script.ROMAN_COMMUNITY and resolved_dst == Script.ASSAMESE:
        target, unmapped = roman_community_to_assamese(intermediate)
        conf = 1.0 if not unmapped else max(0.0, 1.0 - (len(unmapped) / len(text)))
        return TransliterationResult(
            source_text=text,
            target_text=target,
            source_script=resolved_src,
            target_script=resolved_dst,
            confidence=conf,
            unmapped_chars=unmapped,
            warnings=warnings,
        )

    # 4. Identity or unsupported
    if resolved_src == resolved_dst:
        return TransliterationResult(
            source_text=text,
            target_text=intermediate,
            source_script=resolved_src,
            target_script=resolved_dst,
            confidence=1.0,
        )

    warnings.append(
        f"Transliteration directly from {resolved_src.value} to "
        f"{resolved_dst.value} is not fully implemented."
    )
    return TransliterationResult(
        source_text=text,
        target_text=intermediate,
        source_script=resolved_src,
        target_script=resolved_dst,
        confidence=0.5,
        warnings=warnings,
    )
