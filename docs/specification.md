# Specification status

The OpenVoiceOS architecture repository does not specify a text normalization between speech-to-text and the intent engines. This plugin follows no normalization contract, because none exists.

## OVOS-INTENT-1 §2

OVOS-INTENT-1 §2 (OpenVoiceOS/architecture, commit f137b15, `intent-1.md` lines 85 to 89) says:

> Normalization (lowercasing, punctuation and apostrophe stripping, whitespace
> collapsing, locale-specific transliteration) is performed **upstream** of the
> intent engine and is **out of scope** for this grammar; it belongs to a
> separate text-normalization specification. An engine MAY assume its input
> already satisfies the contract.

The "separate text-normalization specification" does not exist. The architecture repository holds no such document. Number conversion is not in the list of that clause.

The plugin output does not satisfy the input contract of OVOS-INTENT-1 §2 in all cases. With the default settings, the plugin does not write lowercase, and the normalized candidate can keep commas, periods and hyphens.

## OVOS-TRANSFORM-1 §3.2

OVOS-TRANSFORM-1 §3.2 defines the utterance transformer type: the input is a list of candidate utterances, and the output is a possibly modified list. It permits a transformer to add candidates: "plugins that produce alternatives extend the list. Downstream matchers MAY try any candidate." This plugin is an utterance transformer of that kind. §3.2 defines the plugin type. It does not define what a normalization does.
