# Installation and configuration

## Installation

The package needs Python 3.11 or newer.

```bash
uv pip install --prerelease=allow ovos-utterance-normalizer
```

The package registers the entry point `ovos-utterance-normalizer` in the group `opm.transformer.text`. The plugin priority is 1. OVOS-TRANSFORM-1 §4 runs a lower priority number first, so this plugin runs before utterance transformers with a higher number. An `order` list in the `utterance_transformers` section sets a different order.

## Turn the plugin on

The plugin loads only when it is installed and the `utterance_transformers` section of `mycroft.conf` names it, as a key or in the `order` list. The default `mycroft.conf` of ovos-config holds this entry:

```json
"utterance_transformers": {
   "ovos-utterance-normalizer": {}
}
```

## Plugin keys

The plugin reads its section, `utterance_transformers` → `ovos-utterance-normalizer`, from the OVOS configuration. It reads these keys:

| Key | Default | What it does |
|---|---|---|
| `lang` | `"en-us"` | The language to use when the message context has no `lang` |
| `fix_encoding_errors` | `true` | Repairs encoding errors with ftfy before the other steps |
| `strip_punctuation` | `true` | Removes punctuation from the start and the end of each candidate |
| `active` | `true` | Read by the plugin loader of ovos-plugin-manager. When it is `false`, the plugin does not load |

This example sets all the plugin keys:

```json
{
  "utterance_transformers": {
    "ovos-utterance-normalizer": {
      "lang": "pt-PT",
      "fix_encoding_errors": true,
      "strip_punctuation": false
    }
  }
}
```

With this configuration, `transform(["vinte e cinco por cento!"])` with no language in the context returns `['vinte e cinco por cento!', '25 por cento']`. The original keeps its "!", and the normalized candidate has no "!" because the Portuguese normalizer removes symbols.

## Turn the plugin off

Set `active` to `false`:

```json
{
  "utterance_transformers": {
    "ovos-utterance-normalizer": {
      "active": false
    }
  }
}
```

With this configuration, the `UtteranceTransformersService` of ovos-plugin-manager loads no `ovos-utterance-normalizer`. A section without the `ovos-utterance-normalizer` key also turns the plugin off, unless the `order` list of the section names the plugin. A name in the `order` list turns the plugin on without its own key.

## Normalizer settings

The settings of the normalized candidate (`lowercase`, `numbers_to_digits`, `expand_contractions`, `remove_symbols`, `remove_accents`, `remove_articles`, `remove_stopwords`, and the tables) are not `mycroft.conf` keys. They come from the language files in the package. See [normalized-utterance.md](normalized-utterance.md).
