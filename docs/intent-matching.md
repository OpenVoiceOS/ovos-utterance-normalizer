# Intent matching with digits

The plugin gives the intent pipeline more candidates. The intent engines decide which candidate they use. This page explains when the digit candidate can help and when it cannot. No measurement of the gain exists. The text below is a design reason, not a measured result.

## When digits can help

Speech-to-text engines can write numbers in different forms. One engine can write "25" where another writes "twenty five", and one engine can write both forms in different sentences. An intent matcher that compares text with a template or a keyword list sees two different strings for one number.

The normalized candidate writes the number words as digits. Some matchers can gain from this form:

- A template engine with a number slot, for example `set a timer for {number} minutes`, gets the same slot text for "twenty five" and for "25".
- A keyword engine with a vocabulary of digits matches the spoken form too.
- A component that reads numbers from the text later gets digits that it can read without a number parser.

## When digits do not help

The gain depends on the pipeline that the deployment configures:

- An engine trained or tuned on raw speech-to-text output learned the forms that the speech-to-text engine writes. A candidate in another form can match less well.
- An engine based on a large language model reads number words without help. A digit candidate can give it no gain, or a different reading.
- A template that writes a number as a word, for example `bajo cero`, does not match the digit candidate. The original candidate stays in the list, so that template still matches the original.
- A misread changes the text. numtag reads some words as numbers when they are no number in the sentence (see [numbers.md](numbers.md)). A matcher that uses only the normalized candidate sees the wrong text.

The plugin keeps the original utterance in the list, so an engine can always use the transcription as received. If the normalized candidate does not help a pipeline, a deployment can turn the plugin off (see [configuration.md](configuration.md)).
