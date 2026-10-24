"""Tests for Deori orthography: script detection, normalization, and transliteration."""

from hypothesis import given
from hypothesis import strategies as st

import deori
from deori.models import Script
from deori.orthography.normalize import clean_invisible_chars, normalize_text
from deori.orthography.scripts import detect_script, is_assamese_char
from deori.orthography.transliterate import (
    assamese_to_roman_community,
    roman_community_to_assamese,
    transliterate_text,
)

# --- 1. Script Detection Tests ---


def test_detect_script_assamese() -> None:
    assert detect_script("দেউৰী") == Script.ASSAMESE
    assert detect_script("চু") == Script.ASSAMESE
    assert detect_script("দিবঙীয়া ভাষা") == Script.ASSAMESE


def test_detect_script_roman_community() -> None:
    assert detect_script("cchu") == Script.ROMAN_COMMUNITY
    assert detect_script("Deori Cchu") == Script.ROMAN_COMMUNITY
    assert detect_script("dibongiya") == Script.ROMAN_COMMUNITY


def test_detect_script_roman_brown() -> None:
    assert detect_script("dāsi") == Script.ROMAN_BROWN
    assert detect_script("mīchī") == Script.ROMAN_BROWN
    assert detect_script("ān") == Script.ROMAN_BROWN


def test_detect_script_ipa() -> None:
    assert detect_script("dɛuɾi") == Script.IPA
    assert detect_script("cɕu") == Script.IPA


def test_detect_script_unknown() -> None:
    assert detect_script("") == Script.UNKNOWN
    assert detect_script("   ") == Script.UNKNOWN
    assert detect_script("12345!@#$") == Script.UNKNOWN


def test_is_assamese_char() -> None:
    assert is_assamese_char("ৰ") is True
    assert is_assamese_char("ৱ") is True
    assert is_assamese_char("ক") is True
    assert is_assamese_char("A") is False
    assert is_assamese_char("5") is False


# --- 2. Normalization Tests ---


def test_normalize_bengali_ro_to_assamese() -> None:
    # Bengali ro (U+09B0) -> Assamese ro (U+09F0)
    bengali_str = "\u09a6\u09c7\u0989\u09b0\u09c0"  # দেউরী with Bengali ro
    normalized = normalize_text(bengali_str)
    assert "\u09b0" not in normalized
    assert "\u09f0" in normalized
    assert normalized == "দেউৰী"


def test_normalize_nukta_composition() -> None:
    # ড + nukta -> ড়
    decomposed = "\u09a1\u09bc"
    normalized = normalize_text(decomposed)
    assert normalized == "ড়"


def test_normalize_quotes() -> None:
    curly = "‘Deori’ “Cchu”"
    normalized = normalize_text(curly)
    assert normalized == "'Deori' \"Cchu\""


def test_clean_invisible_chars() -> None:
    with_nbsp = "দেউৰী\u00a0চু\u200b"
    cleaned = clean_invisible_chars(with_nbsp)
    assert cleaned == "দেউৰী চু"

    # Virama + ZWNJ preserved for explicit halant display
    virama_zwnj = "ক্\u200c"
    assert clean_invisible_chars(virama_zwnj, keep_virama_zwnj=True) == "ক্\u200c"
    assert clean_invisible_chars(virama_zwnj, keep_virama_zwnj=False) == "ক্"


# --- 3. Transliteration Tests ---


def test_assamese_to_roman_basic() -> None:
    text = "দেউৰী"
    rom, unmapped = assamese_to_roman_community(text)
    assert "d" in rom
    assert "r" in rom
    assert len(unmapped) == 0


def test_roman_cch_to_assamese() -> None:
    # 'cch' should map to 'চ্চ'
    text = "cchu"
    as_text, unmapped = roman_community_to_assamese(text)
    assert "চ্চু" in as_text
    assert len(unmapped) == 0


def test_transliterate_public_api() -> None:
    res = deori.transliterate("cchu", src="roman", dst="assamese")
    assert res.target_script == Script.ASSAMESE
    assert "চ্চু" in res.target_text
    assert res.confidence == 1.0


def test_transliterate_brown_to_community() -> None:
    res = deori.transliterate("dāsi", src="roman_brown", dst="roman_community")
    assert res.target_text == "dasi"
    assert res.confidence == 1.0


def test_transliterate_identity() -> None:
    res = deori.transliterate("দেউৰী", src="assamese", dst="assamese")
    assert res.target_text == "দেউৰী"
    assert res.confidence == 1.0


def test_transliterate_empty() -> None:
    res = deori.transliterate("", src="roman", dst="assamese")
    assert res.target_text == ""
    assert res.confidence == 1.0


# --- 4. Property-Based Testing (Hypothesis) ---


@given(st.text(min_size=0, max_size=100))
def test_normalize_idempotency(text: str) -> None:
    """Normalization should be idempotent: f(f(x)) == f(x)."""
    norm1 = normalize_text(text)
    norm2 = normalize_text(norm1)
    assert norm1 == norm2


@given(
    st.text(
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ",
        min_size=1,
        max_size=40,
    )
)
def test_roman_translit_does_not_crash(text: str) -> None:
    """Arbitrary ASCII Latin strings should transliterate to Assamese without error."""
    res = transliterate_text(text, src=Script.ROMAN_COMMUNITY, dst=Script.ASSAMESE)
    assert isinstance(res.target_text, str)
    assert 0.0 <= res.confidence <= 1.0


@given(
    st.text(
        alphabet="অআইঈউঊঋএঐওঔকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযৰলৱশষসহড়ঢ়য়ৎংঃািীুূৃেৈোৌ্ ",
        min_size=1,
        max_size=40,
    )
)
def test_assamese_translit_does_not_crash(text: str) -> None:
    """Assamese character strings should transliterate to Roman without error."""
    res = transliterate_text(text, src=Script.ASSAMESE, dst=Script.ROMAN_COMMUNITY)
    assert isinstance(res.target_text, str)
    assert 0.0 <= res.confidence <= 1.0
