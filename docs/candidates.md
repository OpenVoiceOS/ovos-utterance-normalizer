# The candidate list

`UtteranceNormalizerPlugin.transform(utterances, context)` receives a list of utterances and returns a new list of candidate utterances and the context. The intent pipeline can try each candidate.

## Steps

The plugin does these steps for each input utterance, in the input order:

1. It finds the language. It reads `context["lang"]`. If the context has no language, it reads the `lang` key of its own configuration. The default is `en-us`.
2. It repairs text encoding errors with [ftfy](https://github.com/rspeer/python-ftfy), when `fix_encoding_errors` is true. For example, "Ã©lan" becomes "élan".
3. It adds three candidates to the list, in this order:
   1. the utterance with its contractions expanded (see [contractions.md](contractions.md));
   2. the utterance as received;
   3. the normalized utterance (see [normalized-utterance.md](normalized-utterance.md)).

After the loop, the plugin removes punctuation from the start and the end of each candidate, when `strip_punctuation` is true. It uses Python's `string.punctuation` for this step. Punctuation inside a candidate stays.

Then it removes duplicate candidates and keeps the first copy of each. So the list can have one, two or three candidates for each input utterance.

## Examples

These outputs come from the default configuration:

```python
from ovos_utterance_normalizer import UtteranceNormalizerPlugin

plugin = UtteranceNormalizerPlugin()
plugin.transform(["what's the weather like?"], {"lang": "en-US"})[0]
# ['what is the weather like', "what's the weather like"]

plugin.transform(["turn the volume to fifty"], {"lang": "en-US"})[0]
# ['turn the volume to fifty', 'turn the volume to 50']

plugin.transform(["acorda-me às sete"], {"lang": "pt-PT"})[0]
# ['acorda - me às sete', 'acorda-me às sete', 'acorda - às 7']

plugin.transform(["what's up", "set ten timers"], {"lang": "en-US"})[0]
# ['what is up', "what's up", 'set ten timers', 'set 10 timers']
```

In the first example, the normalized candidate is the same as the first candidate, so it is removed. In the second example, the first candidate is the same as the original, so the original is removed and the first candidate holds its place.

The first candidate is a tokenized form. The tokenizer puts spaces around some punctuation, so "hello, what's the time?" gives "hello , what is the time". In Portuguese, the tokenizer splits hyphenated words: "acorda-me" gives "acorda - me".

## The first candidate in the list

OVOS-TRANSFORM-1 §3.2 says: "By convention `utterances[0]` is the **primary candidate** — the canonical STT transcription". This plugin puts the contraction-expanded candidate first. When the utterance has no contraction to expand, that candidate is the tokenized transcription, or the same as the original and removed. A component that reads only `utterances[0]` therefore reads the contraction-expanded or tokenized text, not always the text that speech-to-text gave.
