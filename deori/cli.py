"""Command line interface for the deori library."""

from __future__ import annotations

import argparse
import contextlib
import sys
from typing import TYPE_CHECKING

import deori
from deori.models import Script

if TYPE_CHECKING:
    from collections.abc import Sequence


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="deori",
        description="Command line interface for the Deori (Deuri) language library.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {deori.__version__}",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # `deori lookup`
    lookup_parser = subparsers.add_parser(
        "lookup", help="Look up a word in the lexicon"
    )
    lookup_parser.add_argument("query", help="Word to look up")
    lookup_parser.add_argument(
        "--to",
        choices=["en", "as", "der"],
        default="en",
        help="Target language (en=English, as=Assamese, der=Deori)",
    )
    lookup_parser.add_argument(
        "--variety",
        help="Filter by dialect variety (dibongiya, tengapaniya, borgonya, patorgonya)",
    )
    lookup_parser.add_argument(
        "--fuzzy",
        action="store_true",
        help="Enable approximate fuzzy search",
    )

    # `deori translit`
    translit_parser = subparsers.add_parser(
        "translit", help="Transliterate text between Assamese and Roman"
    )
    translit_parser.add_argument("text", help="Text to transliterate")
    translit_parser.add_argument(
        "--src",
        default="roman",
        help="Source script (assamese, roman, roman_community, roman_brown)",
    )
    translit_parser.add_argument(
        "--dst",
        default="assamese",
        help="Target script (assamese, roman, roman_community, roman_brown)",
    )

    # `deori normalize`
    norm_parser = subparsers.add_parser(
        "normalize", help="Normalize Unicode and canonical characters"
    )
    norm_parser.add_argument("text", help="Text to normalize")

    # `deori gloss`
    gloss_parser = subparsers.add_parser(
        "gloss", help="Interlinear glossing for a sentence"
    )
    gloss_parser.add_argument("sentence", help="Sentence in Deori")
    gloss_parser.add_argument("--variety", help="Dialect variety")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
        with contextlib.suppress(Exception):
            sys.stdout.reconfigure(encoding="utf-8")

    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "lookup":
        results = deori.lookup(
            args.query, to=args.to, variety=args.variety, fuzzy=args.fuzzy
        )
        if not results:
            print(f"No entry found for '{args.query}'.")
            return 0
        for entry in results:
            meaning = entry.gloss_en or entry.gloss_as
            print(f"{entry.deori} [{entry.variety.value}]: {meaning}")
            print(f"  Source: {entry.source}")
        return 0

    if args.command == "translit":
        # Resolve script names
        src_script = (
            Script.ASSAMESE if args.src == "assamese" else Script.ROMAN_COMMUNITY
        )
        dst_script = (
            Script.ASSAMESE if args.dst == "assamese" else Script.ROMAN_COMMUNITY
        )
        res = deori.transliterate(args.text, src=src_script, dst=dst_script)
        print(res.target_text)
        return 0

    if args.command == "normalize":
        print(deori.normalize(args.text))
        return 0

    if args.command == "gloss":
        print(deori.gloss(args.sentence, variety=args.variety))
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
