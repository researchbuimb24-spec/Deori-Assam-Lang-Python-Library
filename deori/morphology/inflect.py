"""Morphological inflection stub for Deori (expanded in M4)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from deori.models import Variety


def inflect_stem(
    stem: str,
    features: dict[str, Any],
    *,
    variety: Variety | str | None = None,
) -> str | None:
    """Inflect a stem given features. Returns None if unknown."""
    del stem, features, variety
    return None
