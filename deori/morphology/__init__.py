"""Morphology module for Deori inflection, stemming, and rule analysis."""

from deori.morphology.analyzer import analyze_word
from deori.morphology.inflect import inflect_stem

__all__ = ["analyze_word", "inflect_stem"]
