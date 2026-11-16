"""Hungarian digits with a case suffix.

AkH 11 (helyesiras.mta.hu) section 265 d): "A számjegyekhez, írásjelekhez, rövidítésekhez, betűszókhoz stb.
kötőjellel kapcsoljuk a toldalékokat, például: 4-et, 12-t, 19-szer, 32-en (= harmincketten), de: 32-n
(= harminckettőn)". Section 82 f), for -val/-vel: "a v hasonult alakját mindig feltüntetjük, például: 4-gyel, 15%-kal".
So "ötkor" is "5-kor" and "hattal" is "6-tal": the suffix keeps the form of the spoken numeral.

numtag reports the whole word as one number, so the stem is found by asking numtag for a prefix that reads
as the same number. A word whose suffix is not in SUFFIXES stays a word.
"""
import re
from typing import Optional

from numtag import Form, Kind, tag_numbers

# Case suffixes that numtag reads after a numeral. numtag accepts only the form that fits the vowels of the
# numeral, so the suffix of the word is the suffix of the digits. The -val/-vel family shows the assimilated form.
SUFFIXES = frozenset({"kor", "ig", "ért", "tól", "től", "ra", "re", "ba", "be", "ban", "ben", "ról", "ről",
                      "hoz", "hez", "höz", "val", "vel", "tal", "tel", "mal", "mel", "nal", "nel", "cal", "cel",
                      "zal", "zel", "ral", "rel", "dal", "del"})

# the numeral words and combining forms: a word made only of these has no suffix
NUMERAL_ATOMS = ("nulla", "egy", "két", "kettő", "három", "négy", "öt", "hat", "hét", "nyolc", "kilenc", "tíz",
                 "tizen", "húsz", "huszon", "harminc", "negyven", "ötven", "hatvan", "hetven", "nyolcvan",
                 "kilencven", "száz", "ezer", "millió", "milliárd", "billió", "billiárd")


def _is_bare_numeral(word: str) -> bool:
    """True when the word is made only of numeral words ("ötszáz"), so it carries no suffix."""
    word = word.lower()
    reachable = [True] + [False] * len(word)
    for i in range(len(word)):
        if reachable[i]:
            for atom in NUMERAL_ATOMS:
                if word.startswith(atom, i):
                    reachable[i + len(atom)] = True
    return reachable[-1]


def _reads_as(stem: str, value: str) -> bool:
    mentions = tag_numbers(stem, "hu")
    return len(mentions) == 1 and mentions[0].char_span == (0, len(stem)) and mentions[0].value == value \
        and mentions[0].kind is Kind.CARDINAL and mentions[0].form is Form.WORDS


def digits_with_suffix(word: str, value: str) -> Optional[str]:
    """Return "5-kor" for "ötkor" and "5" for "öt" (value "5"), or None when the suffix is not certain."""
    suffixed = False
    for end in range(len(word) - 1, 1, -1):
        stem, suffix = word[:end], word[end:]
        if not _reads_as(stem, value):
            continue
        suffixed = True
        if suffix.lower() in SUFFIXES:
            return f"{value}-{suffix}"
    if suffixed:
        return None
    return value if all(_is_bare_numeral(part) for part in re.split(r"[\s-]+", word)) else None
