# Installation and configuration

## Installation

The package needs Python 3.11 or newer.

```bash
uv pip install --prerelease=allow ovos-utterance-normalizer
```

The package registers the entry point `ovos-utterance-normalizer` in the group `opm.transformer.text`. The plugin priority is 1. The order of the utterance transformers depends on the loader:

- ovos-core 2.1.1 sorts the transformers by priority with `reverse=True` (`ovos_core/transformers.py`). A higher number runs first, so this plugin runs after the transformers with a higher number. ovos-core 2.1.1 reads no `order` key.
- The loader of ovos-plugin-manager 3.1 runs a lower number first, as OVOS-TRANSFORM-1 §4 says. So this plugin runs before the transformers with a higher number. An `order` list in the `utterance_transformers` section sets a different order.

## Turn the plugin on

The plugin loads only when it is installed and the `utterance_transformers` section of `mycroft.conf` names it as a key. The loader of ovos-plugin-manager 3.1 also loads it when the `order` list of the section names it. The default `mycroft.conf` of ovos-config holds this entry:

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

With this configuration, the `UtteranceTransformersService` of ovos-core 2.1.1 and the one of ovos-plugin-manager 3.1 load no `ovos-utterance-normalizer`. A section without the `ovos-utterance-normalizer` key also turns the plugin off. For ovos-plugin-manager 3.1, a name in the `order` list turns the plugin on without its own key.

## Normalizer settings

The settings of the normalized candidate (`lowercase`, `numbers_to_digits`, `expand_contractions`, `remove_symbols`, `remove_accents`, `remove_articles`, `remove_stopwords`, and the tables) are not `mycroft.conf` keys. They come from the language files in the package. See [normalized-utterance.md](normalized-utterance.md).
