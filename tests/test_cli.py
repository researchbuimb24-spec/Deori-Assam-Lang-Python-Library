import pytest

from deori.cli import main


def test_cli_help(capsys: pytest.CaptureFixture[str]) -> None:
    code = main([])
    captured = capsys.readouterr()
    assert code == 0
    assert "usage:" in captured.out or "Command line interface" in captured.out


def test_cli_translit(capsys: pytest.CaptureFixture[str]) -> None:
    code = main(["translit", "cchu", "--src", "roman", "--dst", "assamese"])
    captured = capsys.readouterr()
    assert code == 0
    assert "চ্চু" in captured.out


def test_cli_normalize(capsys: pytest.CaptureFixture[str]) -> None:
    # Bengali ro -> Assamese ro
    code = main(["normalize", "দেউরী"])
    captured = capsys.readouterr()
    assert code == 0
    assert "দেউৰী" in captured.out


def test_cli_lookup_not_found(capsys: pytest.CaptureFixture[str]) -> None:
    code = main(["lookup", "nonexistent"])
    captured = capsys.readouterr()
    assert code == 0
    assert "No entry found" in captured.out


def test_cli_gloss(capsys: pytest.CaptureFixture[str]) -> None:
    code = main(["gloss", "Á mè yó"])
    captured = capsys.readouterr()
    assert code == 0
    assert "UNKNOWN" in captured.out
