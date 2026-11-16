# Numbers

`Normalizer.numbers_to_digits` reads the numbers in the text with `numtag.tag_numbers(utterance, lang)`. numtag gives each number mention its span in the text, its value, its kind (cardinal, ordinal, fraction or decimal), its form (words, digits or mixed) and a confidence.

## The rule

The normalizer writes the value in place of the mention only when all of these are true:

- The language is in `NUMBER_LANGUAGES` (see [Languages with number reading](#languages-with-number-reading)).
- The kind is cardinal.
- The form is not digits. A mention in words ("vinte e cinco") or in mixed form ("2 milhões") changes. A mention in digits ("2,5") stays as written, so the decimal and group marks of the language stay.
- The confidence is 0.5 or more (`MIN_NUMBER_CONFIDENCE` in `normalizer.py`).

All other mentions keep their words:

- Ordinals: "primeiro", "the twenty first", "der dritte".
- Fractions and decimals: "sete e meia", "two point five", "eins komma fünf". Many of these name a clock time ("a las seis y media"), and a clock reader reads the words better than "6.5".
- Most articles. numtag gives an article before a noun the confidence 0.3 ("uma pizza", "ein Bier"). Some articles get a higher confidence and become digits. See [Known misreads](#known-misreads).
- Words whose usual meaning is no number. numtag gives these the confidence 0.4 ("half past seven").

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

an, ar, bg, cs, de, en, es, et, fi, he, hr, id, nb, pt, sk, sl, tr, uk

The normalizer compares the first subtag of the language tag with the set, so "pt-BR" and "pt_PT" are in the set. Every other language keeps all its number words, also when numtag has a lexicon for it.

A language enters the set when a value check finds no new wrong digit for it. The value check runs the normalizer before and after the change on every `.intent`, `.voc` and `.entity` line and every test utterance of the OpenVoiceOS skills, in every locale that the skills ship. A reader then examines each digit that the change writes. A wrong digit is new when the normalizer before the change did not write it. A change that adds a language to the set also gives its value check.

numtag has a lexicon for more languages. These languages are not in the set:

- ca, da, el, eu, fa, fr, gl, hu, it, kab, nl, oc, pl, ro, ru and sv: the value check found new wrong digits. See [Known misreads](#known-misreads).
- ast, az, fy, mwl and nn: no shipped skill locale has a number for the value check to examine.

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

In the languages of the set, the normalizer writes these digits. The normalizer before numtag wrote the same digits:

- an article before a hyphenated noun, as in Portuguese "uma quinta-feira" and German "eine Audio-Erinnerung";
- the English pronoun "one", as in "read the next one".

These misreads keep a language out of the set:

- the percent word read as 100: Catalan "per cent", French "pour cent", Italian "per cento", Greek "τοις εκατό" and Occitan "per cent". French "cinquante pour cent" gives "50 pour 100".
- the Italian elided article "un'": "un'altra volta" gives "1'altra volta".
- an article before a hyphenated noun in Danish, Dutch, French, Kabyle and Swedish: French "un rendez-vous" gives "1 rendez-vous", and Dutch "een audio-opname" gives "1 audio-opname".
- the Basque article "bat" after a noun: "pantaila-argazki bat" gives "pantaila-argazki 1".
- Persian weekday names written with a space: "سه شنبه" (Tuesday) gives "3 شنبه".
- "not a single one" and "the same": Russian "ни одного" gives "ни 1", "одно и то же" gives "1 и то же", and Polish "ani jedna" gives "ani 1".
- an article or a pronoun alone in a vocabulary file: Galician "un" and "unha" and Hungarian "egy" (the article "a"), and Romanian "o" (the pronoun "her"), give "1".
