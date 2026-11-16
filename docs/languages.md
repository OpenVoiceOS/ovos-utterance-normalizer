# Languages

Two separate things depend on the language: the number reading and the other settings of the normalized candidate.

## Number reading

The normalizer converts numbers only in the languages of `NUMBER_LANGUAGES` in `normalizer.py`:

an, ar, bg, cs, de, en, et, fi, he, hr, id, nb, pt, sk, sl, tr, uk

Every other language passes through unchanged: the normalizer keeps every number word. For example, Japanese "五分" stays "五分", and French "cinquante minutes" stays "cinquante minutes". A language enters the set when a value check over the shipped skill locales finds no new wrong digit for it. See [numbers.md](numbers.md#languages-with-number-reading).

numtag 0.8.2a1 has lexicons for these tags, a larger list than the set:

an, ar, ast, az, bg, ca, cs, da, de, el, en, es, et, eu, fa, fi, fr-BE, fr-CH, fr-FR, fy, gl, he, hr, hu, id, it, kab, mwl, nb, nl, nn, oc, pl, pt-BR, pt-PT, ro, ru, sk, sl, sv, tr, uk

## Normalizer classes

`UtteranceNormalizerPlugin.get_normalizer(lang)` selects a class by the start of the language tag:

| Tag starts with | Class | Settings file |
|---|---|---|
| `en` | `EnglishNormalizer` | `res/en/normalize.json` |
| `pt` | `PortugueseNormalizer` | `res/pt/normalize.json` |
| `uk` | `UkrainianNormalizer` | `res/uk/normalize.json` |
| `ca` | `CatalanNormalizer` | `res/ca/normalize.json` |
| `cs` | `CzechNormalizer` | `res/cs/normalize.json` |
| `az` | `AzerbaijaniNormalizer` | `res/az/normalize.json` |
| `ru` | `RussianNormalizer` | `res/ru/normalize.json` |
| `de` | `GermanNormalizer` | `res/de/normalize.json` |
| any other | `Normalizer` | none, the defaults of [normalized-utterance.md](normalized-utterance.md) |

Each class receives the full tag, and gives it to numtag. So "pt-BR" uses the Portuguese settings and the Brazilian number lexicon. The classes for ca, az and ru do not convert numbers, because these languages are not in `NUMBER_LANGUAGES`.

The Portuguese and Catalan classes use their own tokenizer. The Portuguese tokenizer splits hyphenated words ("acorda-me" gives "acorda - me"). The Catalan tokenizer keeps them whole. The German class splits a hyphenated word into two words when it removes symbols.

The package also holds settings files for es, fr, it, nl, no, sl and sv. No class reads them. These languages use the generic `Normalizer`, which does not remove symbols. Of these languages, only sl is in `NUMBER_LANGUAGES`.
