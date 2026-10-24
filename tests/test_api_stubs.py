"""Tests covering top-level public API stubs and milestone placeholders."""

import deori
import deori.corpus
import deori.morphology
import deori.numerals
import deori.translate
from deori.models import Variety


def test_public_analyze() -> None:
    res = deori.analyze("higaye", variety=Variety.DIBONGIYA)
    assert res.surface == "higaye"
    assert res.is_known is False
    assert res.confidence == 0.0


def test_public_inflect() -> None:
    res = deori.inflect("hi", {"tense": "past"}, variety=Variety.DIBONGIYA)
    assert res is None


def test_public_numerals() -> None:
    assert deori.numerals.to_words(25) is None
    assert deori.numerals.to_int("giba") is None


def test_public_corpus_load() -> None:
    items = deori.corpus.load("brown_1895")
    assert items == []


def test_public_translate() -> None:
    res = deori.translate.translate_gloss("Á mè yó", target="en")
    assert res == "Á mè yó"


def test_tokenize_morpheme_level() -> None:
    tokens = deori.tokenize("দেউৰী চু", level="morpheme")
    assert len(tokens) == 2


def test_transliterate_unsupported_script_pair() -> None:
    res = deori.transliterate("dɛuɾi", src="ipa", dst="assamese")
    assert len(res.warnings) > 0
    assert res.confidence == 0.5


def test_transliterate_auto_detect() -> None:
    res = deori.transliterate("দেউৰী", src="unknown", dst="roman")
    assert "d" in res.target_text
