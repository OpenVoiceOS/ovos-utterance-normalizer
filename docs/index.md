# ovos-utterance-normalizer documentation

`ovos-utterance-normalizer` is an utterance transformer plugin for OpenVoiceOS. It runs after speech-to-text and before the intent engines. It does not replace the transcription. It adds candidate utterances to the list that the intent pipeline receives, and one of these candidates writes numbers as digits.

## Pages

| Page | Topic |
|---|---|
| [candidates.md](candidates.md) | The candidate list that `transform` returns, its order and the deduplication |
| [normalized-utterance.md](normalized-utterance.md) | The steps that make the normalized candidate |
| [numbers.md](numbers.md) | Which number words become digits, and which stay words |
| [languages.md](languages.md) | The languages that convert numbers (`NUMBER_LANGUAGES`), and the languages with their own settings |
| [contractions.md](contractions.md) | The contraction tables for each language |
| [configuration.md](configuration.md) | Installation, `mycroft.conf` keys, how to turn the plugin on and off |
| [intent-matching.md](intent-matching.md) | When digits can help an intent engine, and when they cannot |
| [specification.md](specification.md) | What the OpenVoiceOS architecture specifications say about this step |

## Requirements

The package needs Python 3.11 or newer (`requires-python = ">=3.11"` in `pyproject.toml`). It reads numbers with [numtag](https://github.com/TigreGotico/numtag) (`numtag>=0.12.0a1`).
