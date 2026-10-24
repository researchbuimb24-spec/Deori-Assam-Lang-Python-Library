"""Pytest test configuration and fixtures for deori."""

import pytest

from deori.models import SourceCitation, Variety


@pytest.fixture
def brown_source() -> SourceCitation:
    return SourceCitation(
        author="W. B. Brown",
        year=1895,
        title="An Outline Grammar of the Deori Chutiya Language Spoken in Upper Assam",
        page=42,
        license="Public Domain",
    )


@pytest.fixture
def default_variety() -> Variety:
    return Variety.DIBONGIYA
