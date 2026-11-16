# Numbers

`Normalizer.numbers_to_digits` reads the numbers in the text with `numtag.tag_numbers(utterance, lang)`. numtag gives each number mention its span in the text, its value, its kind (cardinal, ordinal, fraction or decimal), its form (words, digits or mixed) and a confidence.

## The rule

The normalizer writes the value in place of the mention only when all of these are true:

- The language is in `NUMBER_LANGUAGES` (see [Languages with number reading](#languages-with-number-reading)).
- The kind is cardinal.
- The form is not digits. A mention in words ("vinte e cinco") or in mixed form ("2 milhões") changes. A mention in digits ("2,5") stays as written, so the decimal and group marks of the language stay.
- The mention has no reason: numtag marks an article with `Reason.ARTICLE` and a word with another meaning with `Reason.HOMOGRAPH` (`WORD_REASONS` in `normalizer.py`).

All other mentions keep their words:

- Ordinals: "primeiro", "the twenty first", "der dritte".
- Fractions and decimals: "sete e meia", "two point five", "eins komma fünf". Many of these name a clock time ("a las seis y media"), and a clock reader reads the words better than "6.5".
- Articles. numtag marks an article with `Reason.ARTICLE` ("uma pizza", "ein Bier"). See [Known misreads](#known-misreads).
- Words whose usual meaning is no number. numtag marks these with `Reason.HOMOGRAPH` (Czech "jednou", "once").

The normalizer replaces the mentions from the last to the first, so each span stays correct while the text changes.

## Examples

Each row shows the output of `numbers_to_digits`:

| Language | Input | Output |
|---|---|---|
| pt-PT | quero uma pizza | quero uma pizza |
| pt-PT | o primeiro filme | o primeiro filme |
| pt-PT | dois milhões de pessoas | 2000000 de pessoas |
| pt-PT | 2 milhões de euros | 2000000 de euros |
| pt-PT | 2,5 litros | 2,5 litros |
| pt-PT | acorda-me às sete e meia | acorda-me às sete e meia |
| en-US | one hundred and two | 102 |
| en-US | minus four degrees | -4 degrees |
| en-US | the twenty first of may | the twenty first of may |
| en-US | half past seven | half past 7 |
| en-US | two point five | two point five |
| en-US | a third of the cake | a third of the cake |
| de-DE | zweiundzwanzig Grad | 22 Grad |
| de-DE | ein Bier bitte | ein Bier bitte |
| de-DE | der dritte Platz | der dritte Platz |
| de-DE | eins komma fünf | eins komma fünf |
| fi-FI | laita ajastin kymmeneksi minuutiksi | laita ajastin 10 minuutiksi |
| cs-CZ | nastav časovač na dvacet pět minut | nastav časovač na 25 minut |
| es-ES | tengo treinta y dos años | tengo 32 años |
| fr-FR | mets le volume à cinquante pour cent | mets le volume à cinquante pour cent |

fr is not in `NUMBER_LANGUAGES`, so its number words stay.

## Languages with number reading

The normalizer reads numbers only in the languages of `NUMBER_LANGUAGES` in `normalizer.py`:

an, ar, bg, ca, cs, de, en, es, et, fi, gl, he, hr, hu, id, nb, pt, ro, ru, sk, sl, tr, uk

The normalizer compares the first subtag of the language tag with the set, so "pt-BR" and "pt_PT" are in the set. Every other language keeps all its number words, also when numtag has a lexicon for it.

A language enters the set when a value check finds no new wrong digit for it. The value check runs the normalizer before and after the change on every `.intent`, `.voc` and `.entity` line and every test utterance of the OpenVoiceOS skills, in every locale that the skills ship. A reader then examines each digit that the change writes. A wrong digit is new when the normalizer before the change did not write it. A change that adds a language to the set also gives its value check.

numtag has a lexicon for more languages. These languages are not in the set:

- da, el, eu, fa, fr, it, kab, nl, oc, pl and sv: no value check has run on the current numtag, so they stay out.
- ast, az, fy, mwl and nn: no shipped skill locale has a number for the value check to examine.

## Hungarian suffixes

numtag reads "ötkor" (at five) as 5 and reports the whole word, suffix included. Hungarian writes a digit with its suffix after a hyphen (AkH 11, section 265 d): "5-kor". The normalizer finds the stem as the longest prefix that numtag reads as the same number. It keeps the suffix of the word, so the form fits the spoken numeral:

| Input | Output |
|---|---|
| ötkor | 5-kor |
| öttől | 5-től |
| hattól | 6-tól |
| hattal | 6-tal |
| hárommal | 3-mal |

A word stays unchanged when its suffix is not one of the listed case suffixes ("hatnak"), when the stem changes ("hármat", "hatot") or when numtag marks it as another word ("egykor", "hétkor"). "háromszor" is no number for numtag and stays.

## Idioms, titles and names

numtag does not find idioms, titles or names. A number word keeps its number value in these too, and the normalizer writes the digit. The value check counts these digits as right:

| Language | Input | Output |
|---|---|---|
| es-ES | mil gracias | 1000 gracias |
| es-ES | empezar desde cero | empezar desde 0 |
| es-ES | temperaturas bajo cero | temperaturas bajo 0 |
| fi-FI | kuka kirjoitti Seitsemän veljestä | kuka kirjoitti 7 veljestä |
| de-DE | type null | type 0 |

## Language of the reading

The normalizer gives numtag the full language tag of the utterance. numtag reads the file of the region when it has one ("pt-BR" reads `pt-BR`), and else the file of the language. A bare "pt" reads `pt-PT`. When numtag has no file for the language, `tag_numbers` raises `ValueError`, and the normalizer returns the text unchanged. See [languages.md](languages.md).

## Known misreads

numtag reads some words as numbers when they are not numbers in the sentence. The fixes for these misreads belong in numtag.

In the languages of the set, the normalizer writes this digit. The normalizer before numtag wrote the same digit:

- the English pronoun "one", as in "read the next one".

