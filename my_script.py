import contextlib
import sys

import deori
from deori.models import LexiconEntry, SourceCitation, Variety

# Tip for Windows consoles to display Assamese Unicode characters properly:
if sys.platform == "win32" and sys.stdout.encoding != "utf-8":
    with contextlib.suppress(Exception):
        sys.stdout.reconfigure(encoding="utf-8")

# 1. Normalize Assamese characters (e.g. cleans erroneous Bengali 'র' -> Assamese 'ৰ')
text = deori.normalize("দেউরী")
print("Normalized:", text)  # -> দেউৰী

# 2. Transliterate Roman community orthography to Assamese script
result = deori.transliterate("cchu", src="roman", dst="assamese")
print("Transliterated:", result.target_text)  # -> চ্চু

# 3. Tokenize words
words = deori.tokenize("দেউৰী চু শিকিবায় নিজিচ্ছা")
print("Words:", words)

# 4. Attach verified source provenance
citation = SourceCitation(
    author="W. B. Brown",
    year=1895,
    title="An Outline Grammar of the Deori Chutiya Language",
    page=65,
    license="Public Domain",
)
entry = LexiconEntry(
    id="der_001",
    deori="cchu",
    deori_assamese="চু",
    deori_roman="cchu",
    pos="noun",
    gloss_en="language, speech",
    variety=Variety.DIBONGIYA,
    source=citation,
    confidence=1.0,
)
print(f"Loaded entry: {entry.deori} -> {entry.gloss_en} (Source: {entry.source})")
