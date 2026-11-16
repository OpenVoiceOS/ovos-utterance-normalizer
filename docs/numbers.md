# Numbers

`Normalizer.numbers_to_digits` reads the numbers in the text with `numtag.tag_numbers(utterance, lang)`. numtag gives each number mention its span in the text, its value, its kind (cardinal, ordinal, fraction or decimal), its form (words, digits or mixed) and a confidence.

## The rule

The normalizer writes the value in place of the mention only when all of these are true:

- The kind is cardinal.
- The form is not digits. A mention in words ("vinte e cinco") or in mixed form ("2 milhões") changes. A mention in digits ("2,5") stays as written, so the decimal and group marks of the language stay.
- The confidence is 0.5 or more (`MIN_NUMBER_CONFIDENCE` in `normalizer.py`).

All other mentions keep their words:

- Ordinals: "primeiro", "the twenty first", "der dritte".
- Fractions and decimals: "sete e meia", "two point five", "eins komma fünf". Many of these name a clock time ("a las seis y media"), and a clock reader reads the words better than "6.5".
- Articles. numtag gives an article before a noun the confidence 0.3 ("uma pizza", "ein Bier").
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
| es-ES | tengo treinta y dos años | tengo 32 años |
| es-ES | bajar el brillo a un 20 por ciento | bajar el brillo a un 20 por ciento |
| es-ES | a las seis y media | a las seis y media |
| es-ES | el primer día | el primer día |

## Language of the reading

The normalizer gives numtag the full language tag of the utterance. numtag reads the file of the region when it has one ("pt-BR" reads `pt-BR`), and else the file of the language. A bare "pt" reads `pt-PT`, "fr" reads `fr-FR` and "no" reads `nb`. When numtag has no file for the language, `tag_numbers` raises `ValueError`, and the normalizer returns the text unchanged. See [languages.md](languages.md).

## Known misreads

numtag reads some words as numbers when they are not numbers in the sentence. Some examples:

- an article before a hyphenated noun, as in Portuguese "um guarda-chuva" and German "eine Audio-Erinnerung";
- an article before a word that can also be a number, as in Catalan "un nou enregistrament", where "nou" means "new";
- the English pronoun "one", as in "read the next one";
- Catalan "cent" in "per cent".

The fixes for these misreads belong in numtag.
