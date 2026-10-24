"""Tests for core data models, validation, and serialization."""

import pytest
from pydantic import ValidationError

from deori.models import (
    Analysis,
    LexiconEntry,
    MorphologicalRule,
    SourceCitation,
    Variety,
)


def test_source_citation_creation(brown_source: SourceCitation) -> None:
    assert brown_source.author == "W. B. Brown"
    assert brown_source.year == 1895
    assert "Brown" in str(brown_source)


def test_source_citation_frozen(brown_source: SourceCitation) -> None:
    with pytest.raises(ValidationError):
        # Source citations are immutable;
        # setattr avoids static analyzer errors on frozen models
        setattr(brown_source, "author", "New Author")  # noqa: B010


def test_lexicon_entry_valid(brown_source: SourceCitation) -> None:
    entry = LexiconEntry(
        id="der_001",
        deori="cchu",
        deori_assamese="চু",
        deori_roman="cchu",
        pos="noun",
        gloss_en="language, speech",
        variety=Variety.DIBONGIYA,
        source=brown_source,
        confidence=1.0,
    )
    assert entry.id == "der_001"
    assert entry.variety == Variety.DIBONGIYA
    assert entry.confidence == 1.0


def test_lexicon_entry_confidence_bounds(brown_source: SourceCitation) -> None:
    with pytest.raises(ValidationError):
        LexiconEntry(
            id="bad_001",
            deori="test",
            source=brown_source,
            confidence=1.5,  # Must be <= 1.0
        )
    with pytest.raises(ValidationError):
        LexiconEntry(
            id="bad_002",
            deori="test",
            source=brown_source,
            confidence=-0.1,  # Must be >= 0.0
        )


def test_analysis_model() -> None:
    analysis = Analysis(
        surface="higaye",
        stem="hi",
        stem_gloss="go",
        morphemes=["hi", "gaye"],
        suffixes=["gaye"],
        gloss="go-PAST",
        variety=Variety.DIBONGIYA,
        confidence=0.9,
        is_known=True,
    )
    assert analysis.surface == "higaye"
    assert analysis.stem == "hi"
    assert analysis.is_known is True


def test_morphological_rule_model(brown_source: SourceCitation) -> None:
    rule = MorphologicalRule(
        rule_id="case_loc_01",
        name="Locative Case -yo",
        category="noun_case",
        affix="yo",
        slot="case",
        gloss="LOC",
        variety=Variety.DIBONGIYA,
        source=brown_source,
        examples=[{"base": "me", "inflected": "meyo", "gloss": "in the house"}],
    )
    assert rule.rule_id == "case_loc_01"
    assert rule.affix == "yo"


def test_json_schemas_exportable() -> None:
    schema1 = LexiconEntry.model_json_schema()
    schema2 = MorphologicalRule.model_json_schema()
    schema3 = SourceCitation.model_json_schema()
    assert "properties" in schema1
    assert "properties" in schema2
    assert "properties" in schema3
