"""Tests for tokenization."""

import pytest

import deori
from deori.tokenizer.tokenize import tokenize_text


def test_tokenize_words() -> None:
    tokens = deori.tokenize("দেউৰী চু শিকিবায় নিজিচ্ছা")
    assert len(tokens) == 4
    assert tokens[0] == "দেউৰী"


def test_tokenize_empty() -> None:
    assert deori.tokenize("") == []
    assert deori.tokenize("   ") == []


def test_tokenize_invalid_level() -> None:
    with pytest.raises(ValueError, match="Unsupported tokenization level"):
        tokenize_text("hello", level="invalid")
