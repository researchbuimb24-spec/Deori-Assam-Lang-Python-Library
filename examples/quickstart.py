import contextlib
import sys

import deori
from deori.models import LexiconEntry, Script, SourceCitation, Variety
from deori.orthography import detect_script

# Ensure Windows PowerShell/CMD terminal supports UTF-8 stdout
if sys.platform == "win32" and sys.stdout.encoding != "utf-8":
    with contextlib.suppress(Exception):
        sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    print("=== 1. Text Normalization ===")
    # Fixes Bengali ro 'র' to Assamese ro 'ৰ' and normalizes Unicode NFC
    raw_text = "দেউরী"
    clean_text = deori.normalize(raw_text)
    print(f"Original  : {raw_text}")
    print(f"Normalized: {clean_text}\n")

    print("=== 2. Script Detection ===")
    samples = ["দেউৰী চু", "Deori Cchu", "dāsi"]
    for s in samples:
        script = detect_script(s)
        print(f"'{s}' -> Script: {script.value}")
    print()

    print("=== 3. Transliteration ===")
    # Community Roman -> Assamese Script
    res1 = deori.transliterate("cchu", src=Script.ROMAN_COMMUNITY, dst=Script.ASSAMESE)
    print(f"Roman 'cchu' -> Assamese: {res1.target_text}")

    # Assamese Script -> Roman
    res2 = deori.transliterate(
        "দেউৰী চু", src=Script.ASSAMESE, dst=Script.ROMAN_COMMUNITY
    )
    print(f"Assamese 'দেউৰী চু' -> Roman: {res2.target_text}\n")

    print("=== 4. Tokenization ===")
    sentence = "দেউৰী চু শিকিবায় নিজিচ্ছা"
    tokens = deori.tokenize(sentence)
    print(f"Sentence: {sentence}")
    print(f"Tokens  : {tokens}\n")

    print("=== 5. Working with Linguistic Data Models & Provenance ===")
    # Create an immutable citation (author, year, title, page)
    brown_citation = SourceCitation(
        author="W. B. Brown",
        year=1895,
        title="An Outline Grammar of the Deori Chutiya Language",
        page=65,
        license="Public Domain",
    )

    # Create a lexicon record with verified provenance and dialect variety
    word_entry = LexiconEntry(
        id="brown_1895_cchu_01",
        deori="cchu",
        deori_assamese="চু",
        deori_roman="cchu",
        pos="noun",
        gloss_en="language, speech",
        gloss_as="ভাষা",
        variety=Variety.DIBONGIYA,
        source=brown_citation,
        confidence=1.0,
    )

    print(
        f"Word       : {word_entry.deori} "
        f"(Roman: {word_entry.deori_roman}, Assamese: {word_entry.deori_assamese})"
    )
    print(f"Meaning    : {word_entry.gloss_en} / {word_entry.gloss_as}")
    print(f"Variety    : {word_entry.variety.value}")
    print(f"Provenance : {word_entry.source}")


if __name__ == "__main__":
    main()
