# ovos-utterance-normalizer

`ovos-utterance-normalizer` is an [OVOS](https://github.com/OpenVoiceOS) plugin that
normalizes utterances before intent parsing. It expands contractions, converts spoken
numbers to digits, strips punctuation, and applies other language-specific cleanup so
that intent parsers get a consistent input.

The plugin also fixes text encoding errors with
[python-ftfy](https://github.com/rspeer/python-ftfy).

It is enabled by default in
[mycroft.conf](https://github.com/OpenVoiceOS/ovos-config/blob/8cfb04319516cad38d39203d14f10d6f0f568390/ovos_config/mycroft.conf#L114).

## Install

```bash
pip install ovos-utterance-normalizer
```

## Usage

`ovos-utterance-normalizer` registers as an
[OVOS PHAL](https://github.com/OpenVoiceOS/ovos-plugin-manager) `opm.transformer.text`
plugin, named `ovos-utterance-normalizer`. [ovos-core](https://github.com/OpenVoiceOS/ovos-core)
loads it automatically when it is installed and enabled in the configuration.

For each utterance, the plugin produces up to three variants: the utterance with
contractions expanded, the original utterance, and the normalized utterance. Punctuation
is stripped from each variant, and duplicates are removed while keeping the original order.

Supported configuration options, under the plugin name in `mycroft.conf`:

| Option | Default | Description |
|---|---|---|
| `lang` | `en-us` | Fallback language, used when no language is given in the utterance context |
| `fix_encoding_errors` | `true` | Fix encoding errors with `ftfy` before normalizing |
| `strip_punctuation` | `true` | Strip punctuation from each output variant |

Normalization is language-specific. English, Portuguese, Ukrainian, Catalan, Czech,
Azerbaijani, Russian, and German each have a dedicated normalizer. Other languages fall
back to the generic normalizer.

## Related projects

- [ovos-plugin-manager](https://github.com/OpenVoiceOS/ovos-plugin-manager), which loads
  and runs this plugin as an `opm.transformer.text` transformer.
- [ovos-config](https://github.com/OpenVoiceOS/ovos-config), which ships the default
  `mycroft.conf` that enables this plugin.
- [ovos-core](https://github.com/OpenVoiceOS/ovos-core), the assistant runtime that
  calls transformer plugins before intent parsing.

## License

Apache-2.0
