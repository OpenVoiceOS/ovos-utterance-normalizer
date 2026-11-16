# The normalized candidate

`Normalizer.normalize(utterance)` makes the third candidate. `UtteranceNormalizerPlugin.get_normalizer(lang)` selects the normalizer class for the language (see [languages.md](languages.md)). Each class reads its settings from a JSON file in `ovos_utterance_normalizer/res/<language>/normalize.json`. The generic `Normalizer` class has no file and uses the defaults in the table below.

## Steps

`normalize` does these steps in this order. Each step runs only when its setting is true.

| Step | Setting | Default | What the step does |
|---|---|---|---|
| 1 | `lowercase` | false | Writes all characters in lowercase |
| 2 | `numbers_to_digits` | true | Writes number words as digits (see [numbers.md](numbers.md)) |
| 3 | `expand_contractions` | true | Replaces each word found in the `contractions` table (see [contractions.md](contractions.md)) |
| 4 | none, always runs | | Replaces each word found in the `word_replacements` table |
| 5 | `remove_symbols` | false | Removes each character of the `symbols` list |
| 6 | `remove_accents` | false | Replaces each accented letter of the `accents` table with its plain letter |
| 7 | `remove_articles` | false | Removes each word of the `articles` list |
| 8 | `remove_stopwords` | false | Removes each word of the `stopwords` list |
| 9 | none, always runs | | Joins the words with one space |

Steps 3, 4, 7 and 8 split the text into words with the tokenizer and join the words with spaces. Step 2 runs before step 3 because the tokenizer splits some number words, for example Ukrainian "п’ять" at its apostrophe.

The default `symbols` list holds `;` `_` `!` `?` `<` `>` `|` `(` `)` `=` `[` `]` `{` `}` `»` `«` `*` `~` `^`, the backtick and the double quote. The comma, the period, the colon, the hyphen and the apostrophe are not in the list.

## Settings for each language

| File | `expand_contractions` | `remove_symbols` | `remove_stopwords` | Tables with entries |
|---|---|---|---|---|
| `en` | true | true | false | 166 contractions, 3 articles |
| `de` | true | true | false | 15 contractions, 45 word replacements, 6 articles |
| `pt` | false | true | true | 23 stopwords, 4 articles |
| `ca` | false | true | true | 24 stopwords, 6 articles |
| `az` | true | true | false | 1 word replacement |
| `cs`, `ru`, `uk` | true | true | false | none |

In every file, `lowercase`, `remove_accents` and `remove_articles` are false, and `numbers_to_digits` is true. The article lists are therefore not used by the plugin.

The Portuguese stopword list includes "de", "e", "para" and "que". The Catalan list includes "de", "i", "al" and "que". So "põe um temporizador de vinte e cinco minutos" gives "põe um temporizador 25 minutos".

The German normalizer also splits a hyphenated word into two words before it removes symbols.

## Use from Python

The normalizer classes work without the plugin. Each class has a default language, so a call with no arguments converts numbers:

```python
from ovos_utterance_normalizer.normalizer import Normalizer, PortugueseNormalizer, GermanNormalizer

PortugueseNormalizer().normalize("põe o volume a setenta e cinco")
# 'põe o volume a 75'

PortugueseNormalizer(lang="pt-BR").normalize("dezesseis graus")
# '16 graus'

GermanNormalizer().normalize("starte den Timer zum Kochen, zwanzig Minuten!")
# 'starte den Timer zu dem Kochen , 20 Minuten'
```

A `config` argument replaces the whole settings dictionary of the class. Keys that it does not give take the defaults of the table above, not the values of the language file:

```python
custom = Normalizer(config={"lowercase": True, "remove_symbols": True}, lang="es-ES")
custom.normalize("¡Pon Veinticinco Minutos!")
# 'pon 25 minutos'
```

The plugin does not pass a `config` argument. The settings of the normalized candidate come only from the language files.
