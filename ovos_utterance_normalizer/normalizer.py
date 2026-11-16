import json
import re
from os.path import dirname
from typing import List, Dict

from numtag import Form, Kind, Reason, tag_numbers

from ovos_utterance_normalizer.tokenization import word_tokenize

# numtag marks a lone article ("uma pizza", "ein Bier") and a word whose
# common meaning is no number ("jednou", "half past"): both stay words
WORD_REASONS = frozenset({Reason.ARTICLE, Reason.HOMOGRAPH})

# A language enters this set when a value check over every shipped skill locale finds no new wrong digit
NUMBER_LANGUAGES = frozenset({"an", "ar", "bg", "ca", "cs", "de", "en", "es", "et", "fi", "gl", "he", "hr",
                              "hu", "id", "nb", "pt", "ro", "ru", "sk", "sl", "tr", "uk"})


class Normalizer:
    # taken from lingua_franca
    """
    individual languages may subclass this if needed

    normalize_XX should pass a valid config read from json
    """
    _default_config = {}
    lang = None

    def __init__(self, config=None, lang=None):
        self.config = config or self._default_config
        self.lang = lang or self.lang

    @staticmethod
    def tokenize(utterance) -> List[str]:
        return word_tokenize(utterance)

    @property
    def should_lowercase(self) -> bool:
        return self.config.get("lowercase", False)

    @property
    def should_numbers_to_digits(self) -> bool:
        return self.config.get("numbers_to_digits", True)

    @property
    def should_expand_contractions(self) -> bool:
        return self.config.get("expand_contractions", True)

    @property
    def should_remove_symbols(self) -> bool:
        return self.config.get("remove_symbols", False)

    @property
    def should_remove_accents(self) -> bool:
        return self.config.get("remove_accents", False)

    @property
    def should_remove_articles(self) -> bool:
        return self.config.get("remove_articles", False)

    @property
    def should_remove_stopwords(self) -> bool:
        return self.config.get("remove_stopwords", False)

    @property
    def contractions(self) -> Dict[str, str]:
        return self.config.get("contractions", {})

    @property
    def word_replacements(self) -> Dict[str, str]:
        return self.config.get("word_replacements", {})

    @property
    def accents(self) -> Dict[str, str]:
        return self.config.get("accents",
                               {"á": "a", "à": "a", "ã": "a", "â": "a",
                                "é": "e", "è": "e", "ê": "e", "ẽ": "e",
                                "í": "i", "ì": "i", "î": "i", "ĩ": "i",
                                "ò": "o", "ó": "o", "ô": "o", "õ": "o",
                                "ú": "u", "ù": "u", "û": "u", "ũ": "u",
                                "Á": "A", "À": "A", "Ã": "A", "Â": "A",
                                "É": "E", "È": "E", "Ê": "E", "Ẽ": "E",
                                "Í": "I", "Ì": "I", "Î": "I", "Ĩ": "I",
                                "Ò": "O", "Ó": "O", "Ô": "O", "Õ": "O",
                                "Ú": "U", "Ù": "U", "Û": "U", "Ũ": "U"
                                })

    @property
    def stopwords(self) -> List[str]:
        return self.config.get("stopwords", [])

    @property
    def articles(self) -> List[str]:
        return self.config.get("articles", [])

    @property
    def symbols(self) -> List[str]:
        return self.config.get("symbols",
                               [";", "_", "!", "?", "<", ">", "|",
                                "(", ")", "=", "[", "]", "{", "}",
                                "»", "«", "*", "~", "^", "`", "\""])

    def expand_contractions(self, utterance: str) -> str:
        """ Expand common contractions, e.g. "isn't" -> "is not" """
        words = self.tokenize(utterance)
        for idx, w in enumerate(words):
            if w in self.contractions:
                words[idx] = self.contractions[w]
        utterance = " ".join(words)
        return utterance

    def numbers_to_digits(self, utterance: str) -> str:
        """Write each whole number said in words as digits: "vinte e cinco" becomes "25".

        Only cardinals change. Ordinals ("primeiro"), fractions and decimals
        ("sete e meia", often a clock time) stay words, and so do the mentions
        numtag marks as an article or as a word with another meaning. A language outside
        NUMBER_LANGUAGES keeps all its words.
        """
        if not self.lang or self.lang.replace("_", "-").split("-")[0].lower() not in NUMBER_LANGUAGES:
            return utterance
        try:
            mentions = tag_numbers(utterance, self.lang)
        except ValueError:  # numtag has no lexicon for this language
            return utterance
        for mention in reversed(mentions):
            if mention.kind is not Kind.CARDINAL or mention.form is Form.DIGITS \
                    or mention.reasons & WORD_REASONS:
                continue
            start, end = mention.char_span
            utterance = utterance[:start] + mention.value + utterance[end:]
        return utterance

    def remove_articles(self, utterance: str) -> str:
        words = self.tokenize(utterance)
        for idx, w in enumerate(words):
            if w in self.articles:
                words[idx] = ""
        utterance = " ".join(words)
        return utterance

    def remove_stopwords(self, utterance: str) -> str:
        words = self.tokenize(utterance)
        for idx, w in enumerate(words):
            if w in self.stopwords:
                words[idx] = ""
        # if words[-1] == '-':
        #    words = words[:-1]
        utterance = " ".join(words)
        # Remove trailing whitespaces from utterance along with orphaned
        # hyphens, more characters may be added later
        utterance = re.sub(r'- *$', '', utterance)
        return utterance

    def remove_symbols(self, utterance: str) -> str:
        mapping = str.maketrans('', '', "".join(self.symbols))
        return utterance.translate(mapping)

    def remove_accents(self, utterance : str) -> str:
        for s in self.accents:
            utterance = utterance.replace(s, self.accents[s])
        return utterance

    def replace_words(self, utterance: str) -> str:
        words = self.tokenize(utterance)
        for idx, w in enumerate(words):
            if w in self.word_replacements:
                words[idx] = self.word_replacements[w]
        utterance = " ".join(words)
        return utterance

    def normalize(self, utterance: str = ""):
        # mutations
        if self.should_lowercase:
            utterance = utterance.lower()
        # numbers first: the tokenizer splits words such as "п’ять"
        if self.should_numbers_to_digits:
            utterance = self.numbers_to_digits(utterance)
        if self.should_expand_contractions:
            utterance = self.expand_contractions(utterance)
        utterance = self.replace_words(utterance)

        # removals
        if self.should_remove_symbols:
            utterance = self.remove_symbols(utterance)
        if self.should_remove_accents:
            utterance = self.remove_accents(utterance)
        if self.should_remove_articles:
            utterance = self.remove_articles(utterance)
        if self.should_remove_stopwords:
            utterance = self.remove_stopwords(utterance)
        # remove extra spaces
        utterance = " ".join([w for w in utterance.split(" ") if w])
        return utterance


class CatalanNormalizer(Normalizer):
    lang = "ca"
    with open(f"{dirname(__file__)}/res/ca/normalize.json") as f:
        _default_config = json.load(f)

    @staticmethod
    def tokenize(utterance : str) -> List[str]:
        return word_tokenize(utterance, lang="ca")


class CzechNormalizer(Normalizer):
    lang = "cs"
    with open(f"{dirname(__file__)}/res/cs/normalize.json", encoding='utf8') as f:
        _default_config = json.load(f)


class PortugueseNormalizer(Normalizer):
    lang = "pt"
    with open(f"{dirname(__file__)}/res/pt/normalize.json") as f:
        _default_config = json.load(f)

    @staticmethod
    def tokenize(utterance: str) -> List[str]:
        return word_tokenize(utterance, lang="pt")


class RussianNormalizer(Normalizer):
    lang = "ru"
    with open(f"{dirname(__file__)}/res/ru/normalize.json", encoding='utf8') as f:
        _default_config = json.load(f)


class UkrainianNormalizer(Normalizer):
    lang = "uk"
    with open(f"{dirname(__file__)}/res/uk/normalize.json", encoding='utf8') as f:
        _default_config = json.load(f)


class EnglishNormalizer(Normalizer):
    lang = "en"
    with open(f"{dirname(__file__)}/res/en/normalize.json") as f:
        _default_config = json.load(f)


class AzerbaijaniNormalizer(Normalizer):
    lang = "az"
    with open(f"{dirname(__file__)}/res/az/normalize.json") as f:
        _default_config = json.load(f)


class GermanNormalizer(Normalizer):
    lang = "de"
    with open(f"{dirname(__file__)}/res/de/normalize.json") as f:
        _default_config = json.load(f)
    
    def remove_symbols(self, utterance: str) -> str:
        # special rule for hyphanated words in german as some STT engines falsely
        # return them pretty regularly
        utterance = re.sub(r'\b(\w*)-(\w*)\b', r'\1 \2', utterance)
        return super().remove_symbols(utterance)
