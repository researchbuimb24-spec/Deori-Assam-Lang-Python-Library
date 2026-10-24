"""Core typed data models and data integrity schemas for deori.

Every linguistic record in deori must carry:
1. `source`: Provenance tracking author, publication year, page/section.
2. `variety`: Dialect/variety tracking (Dibongiya, Tengapaniya, Borgonya,
   Patorgonya, Historical Brown, etc.).
3. `confidence`: Float indicating attestedness vs rule-derived confidence.

Zero hallucination rule: Forms not attested in a cited source must not be
invented.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Variety(str, Enum):
    """Documented traditional divisions and varieties of Deori."""

    DIBONGIYA = "dibongiya"
    TENGAPANIYA = "tengapaniya"
    BORGONYA = "borgonya"
    PATORGONYA = "patorgonya"
    HISTORICAL_BROWN = "historical_brown"
    COMMUNITY_STANDARD = "community_standard"
    UNSPECIFIED = "unspecified"


class Script(str, Enum):
    """Scripts and orthographic systems used for Deori."""

    ASSAMESE = "assamese"
    ROMAN_COMMUNITY = "roman_community"  # Community orthography using "cch", etc.
    ROMAN_BROWN = "roman_brown"  # Historical Brown (1895) romanization with macrons
    IPA = "ipa"
    UNKNOWN = "unknown"


class SourceCitation(BaseModel):
    """Bibliographic or archival source provenance for a linguistic item."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    author: str = Field(..., description="Author or publishing body")
    year: int | None = Field(default=None, description="Year of publication")
    title: str | None = Field(
        default=None, description="Title of book, paper, or dataset"
    )
    page: str | int | None = Field(default=None, description="Page number or section")
    url: str | None = Field(
        default=None, description="Web/Archive URL if publicly available"
    )
    license: str | None = Field(
        default=None,
        description="License of source data (e.g. Public Domain, CC BY-SA 4.0)",
    )
    notes: str | None = Field(default=None, description="Additional citation details")

    def __str__(self) -> str:
        parts: list[str] = [self.author]
        if self.year:
            parts.append(f"({self.year})")
        if self.page:
            parts.append(f": p. {self.page}")
        return " ".join(parts)


class LexiconEntry(BaseModel):
    """A single lexical entry with strict provenance and dialect tracking."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., description="Unique entry ID e.g. 'brown_1895_cchu_01'")
    deori: str = Field(..., description="Primary surface form in citation script")
    deori_assamese: str | None = Field(
        default=None, description="Assamese-script spelling (দেউৰী লিপিত)"
    )
    deori_roman: str | None = Field(
        default=None, description="Roman orthography representation"
    )
    ipa: str | None = Field(default=None, description="Phonemic IPA transcription")
    pos: str | None = Field(
        default=None,
        description="Part of speech (noun, verb, postposition, etc.)",
    )
    gloss_en: str | None = Field(default=None, description="English definition / gloss")
    gloss_as: str | None = Field(
        default=None, description="Assamese definition / gloss"
    )
    variety: Variety = Field(
        default=Variety.UNSPECIFIED,
        description="Dialect or regional variety",
    )
    source: SourceCitation = Field(
        ..., description="Bibliographical source with page citation"
    )
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Attestation confidence (1.0 for verbatim source attestations)",
    )
    semantic_field: str | None = Field(
        default=None,
        description="Semantic category (kinship, fauna, agriculture, etc.)",
    )
    attested_forms: list[str] = Field(
        default_factory=list, description="Inflected or alternate attested spellings"
    )
    conflicting_entries: list[str] = Field(
        default_factory=list,
        description="IDs of entries with conflicting lexical or phonological claims",
    )
    notes: str | None = Field(
        default=None, description="Linguistic or historical notes"
    )


class TransliterationResult(BaseModel):
    """Result of an orthographic transliteration operation."""

    model_config = ConfigDict(frozen=True)

    source_text: str
    target_text: str
    source_script: Script
    target_script: Script
    confidence: float = Field(
        default=1.0, ge=0.0, le=1.0, description="Transliteration confidence"
    )
    unmapped_chars: list[str] = Field(
        default_factory=list, description="Characters that could not be mapped"
    )
    warnings: list[str] = Field(
        default_factory=list, description="Orthographic notes or ambiguities"
    )


class Analysis(BaseModel):
    """Morphological breakdown of a word adhering to Leipzig Glossing Rules."""

    model_config = ConfigDict(frozen=True)

    surface: str = Field(..., description="Surface input word analyzed")
    stem: str | None = Field(default=None, description="Identified root or stem")
    stem_gloss: str | None = Field(default=None, description="Gloss of the root/stem")
    morphemes: list[str] = Field(
        default_factory=list, description="Segmented morphemes"
    )
    suffixes: list[str] = Field(
        default_factory=list, description="Identified affixal suffixes"
    )
    gloss: str = Field(
        ..., description="Interlinear gloss string (e.g. 'STEM-PAST.PERF')"
    )
    variety: Variety = Field(default=Variety.UNSPECIFIED)
    source: SourceCitation | None = Field(
        default=None,
        description="Citation for the morphological rule or attested paradigm",
    )
    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Confidence score (0.0 for unknown analysis)",
    )
    is_known: bool = Field(
        default=False,
        description="True if stem and all affixes are attested in source data",
    )


class MorphologicalRule(BaseModel):
    """Declarative morphological rule for inflection or derivation."""

    model_config = ConfigDict(extra="forbid")

    rule_id: str
    name: str
    category: str = Field(
        ..., description="noun_case, verb_tense, verb_aspect, pronoun_number, etc."
    )
    affix: str = Field(..., description="Suffix or affix string")
    slot: str = Field(
        ..., description="Position or slot ordering (e.g. 'case', 'tense', 'aspect')"
    )
    gloss: str = Field(..., description="Leipzig gloss label (e.g. 'DAT', 'PST')")
    variety: Variety = Field(default=Variety.UNSPECIFIED)
    source: SourceCitation = Field(
        ..., description="Exact citation (author, year, page) for this rule"
    )
    allomorphs: list[str] = Field(
        default_factory=list, description="Phonologically conditioned variants"
    )
    phonological_condition: str | None = Field(
        default=None,
        description="Condition (e.g. 'after vowel', 'after consonant')",
    )
    notes: str | None = None
    examples: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Attested pairs of (base, inflected, gloss) from source",
    )
