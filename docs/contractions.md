# Contractions

`Normalizer.expand_contractions(utterance)` splits the text into words with the tokenizer. It replaces each word that is a key of the `contractions` table with the value of that key. Then it joins the words with spaces.

## Tables

| Language | Entries | Examples |
|---|---|---|
| English (`res/en/normalize.json`) | 166 | "can't" → "can not", "it's" → "it is", "won't" → "will not", "gonna" → "going to", "I'm" → "I am" |
| German (`res/de/normalize.json`) | 15 | "zum" → "zu dem", "beim" → "bei dem", "ins" → "in das", "vom" → "von dem", "fürs" → "für das" |
| All other languages | 0 | none |

The German table holds the contractions of a preposition and an article: am, ans, aufs, beim, durchs, fürs, hinterm, ins, übers, unters, unterm, vom, vors, vorm, zum.

## Case

A key matches only a word with the same case. The plugin does not lowercase the text first. The English table has lowercase keys, and 9 keys that start with "I" ("I'm", "I'd", "I'll", "I've", "I'm'a", "I'm'o", "I'll've", "I'd've", "Whatcha"):

```python
from ovos_utterance_normalizer import UtteranceNormalizerPlugin

en = UtteranceNormalizerPlugin.get_normalizer("en-US")
en.expand_contractions("i can't go, we're late")
# 'i can not go , we are late'
en.expand_contractions("I'm sure it's fine")
# 'I am sure it is fine'
en.expand_contractions("i'm sure")
# "i'm sure"

de = UtteranceNormalizerPlugin.get_normalizer("de-DE")
de.expand_contractions("ich gehe zum Bahnhof")
# 'ich gehe zu dem Bahnhof'
```

## Where the expansion is used

The plugin calls `expand_contractions` for the first candidate of each utterance, in every language (see [candidates.md](candidates.md)). For the normalized candidate, `normalize` expands contractions only when the `expand_contractions` setting of the language is true. It is false for Portuguese and Catalan, and their tables are empty.
