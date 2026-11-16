# ovos-utterance-normalizer

`ovos-utterance-normalizer` is an utterance transformer plugin for [OpenVoiceOS](https://github.com/OpenVoiceOS). It runs after speech-to-text and before the intent engines. It gives the intent pipeline extra candidate utterances, and one of these candidates writes numbers as digits.

```python
from ovos_utterance_normalizer import UtteranceNormalizerPlugin

plugin = UtteranceNormalizerPlugin()
plugin.transform(["i'm sure it's twenty past five"], {"lang": "en-US"})[0]
# ["i'm sure it is twenty past five", "i'm sure it's twenty past five", "i'm sure it is 20 past 5"]
```

## What the plugin does

For each utterance, `transform` returns up to three candidates in this order:

1. the utterance with its contractions expanded;
2. the utterance as received;
3. the normalized utterance, with number words written as digits and the settings of the language applied.

The plugin removes punctuation from the start and the end of each candidate, and it removes duplicates. Before these steps, it repairs text encoding errors with [ftfy](https://github.com/rspeer/python-ftfy). See [docs/candidates.md](docs/candidates.md).

## Numbers

The plugin reads numbers with [numtag](https://github.com/TigreGotico/numtag), in every language that numtag has a lexicon for. A language with no lexicon passes through unchanged. Only a whole-number cardinal said in words becomes digits, at numtag confidence 0.5 or more. Ordinals, fractions, decimals and articles keep their words:

| Language | Input | Normalized candidate |
|---|---|---|
| pt-PT | põe um temporizador de vinte e cinco minutos | põe um temporizador 25 minutos |
| en-US | the twenty first of may | the twenty first of may |
| de-DE | stell einen Timer auf fünfundzwanzig Minuten | stell einen Timer auf 25 Minuten |
| es-ES | a las seis y media | a las seis y media |

See [docs/numbers.md](docs/numbers.md) and [docs/languages.md](docs/languages.md).

Digits can help a template or keyword engine with a number slot. They do not help every pipeline: an engine trained on raw speech-to-text output, or an engine based on a large language model, can gain nothing or do worse. No gain is measured. See [docs/intent-matching.md](docs/intent-matching.md).

No OpenVoiceOS specification defines this normalization. OVOS-INTENT-1 §2 names a separate text-normalization specification that does not exist. See [docs/specification.md](docs/specification.md).

## Install

The package needs Python 3.11 or newer.

```bash
uv pip install --prerelease=allow ovos-utterance-normalizer
```

## Configuration

The default `mycroft.conf` of [ovos-config](https://github.com/OpenVoiceOS/ovos-config) turns the plugin on:

```json
"utterance_transformers": {
   "ovos-utterance-normalizer": {}
}
```

| Key | Default | What it does |
|---|---|---|
| `lang` | `"en-us"` | The language to use when the message context has no `lang` |
| `fix_encoding_errors` | `true` | Repairs encoding errors with ftfy |
| `strip_punctuation` | `true` | Removes punctuation from the start and the end of each candidate |
| `active` | `true` | When it is `false`, the plugin does not load |

See [docs/configuration.md](docs/configuration.md).

## Documentation

The [docs](docs/index.md) directory holds one page for each topic: candidates, the normalized candidate, numbers, languages, contractions, configuration, intent matching and the specification status.

## Related projects

- [ovos-plugin-manager](https://github.com/OpenVoiceOS/ovos-plugin-manager) loads and runs this plugin as an `opm.transformer.text` transformer.
- [ovos-config](https://github.com/OpenVoiceOS/ovos-config) holds the default `mycroft.conf` that turns this plugin on.
- [ovos-core](https://github.com/OpenVoiceOS/ovos-core) calls the utterance transformers before intent matching.
- [numtag](https://github.com/TigreGotico/numtag) finds the numbers and their values.

## License

Apache-2.0
