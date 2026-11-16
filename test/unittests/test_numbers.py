import unittest

from ovos_utterance_normalizer import UtteranceNormalizerPlugin


def normalize(utterance: str, lang: str) -> str:
    return UtteranceNormalizerPlugin.get_normalizer(lang).normalize(utterance)


class TestNumbersToDigits(unittest.TestCase):
    def test_english(self):
        # 100 + 2
        self.assertEqual(normalize("one hundred and two", "en-US"), "102")
        # "half" here names no number: the time is 7:30
        self.assertEqual(normalize("half past seven", "en-US"), "half past 7")

    def test_fraction_stays_words(self):
        # a fraction read from words keeps its words: it is often a clock time
        self.assertEqual(normalize("set a timer for two and a half hours", "en-US"),
                         "set a timer for two and a half hours")
        # the Portuguese stopword step removes "e"
        self.assertEqual(normalize("sete e meia", "pt-PT"), "sete meia")

    def test_portuguese_compound(self):
        # 20 + 5; "por cento" is the percent word, no number
        self.assertEqual(normalize("vinte e cinco por cento", "pt-PT"), "25 por cento")
        # 70 + 5
        self.assertEqual(normalize("põe o volume a setenta e cinco", "pt-PT"), "põe o volume a 75")

    def test_portuguese_article_stays_word(self):
        self.assertEqual(normalize("quero uma pizza", "pt-PT"), "quero uma pizza")

    def test_portuguese_ordinal_stays_word(self):
        self.assertEqual(normalize("o primeiro filme", "pt-PT"), "o primeiro filme")

    def test_german(self):
        # fünf-und-zwanzig: 5 + 20
        self.assertEqual(normalize("fünfundzwanzig", "de-DE"), "25")
        # "einen" is the article of "timer"
        self.assertEqual(normalize("stelle einen timer für fünf minuten", "de-DE"),
                         "stelle einen timer für 5 minuten")

    def test_spanish(self):
        # 30 + 2
        self.assertEqual(normalize("tengo treinta y dos años", "es-ES"), "tengo 32 años")
        self.assertEqual(normalize("pon una alarma a las siete", "es-ES"), "pon una alarma a las 7")
        # "un" is the article of "20 por ciento"
        self.assertEqual(normalize("bajar el brillo a un 20 por ciento", "es-ES"),
                         "bajar el brillo a un 20 por ciento")

    def test_catalan(self):
        # vint-i-cinc: 20 + 5
        self.assertEqual(normalize("vint-i-cinc", "ca-ES"), "25")
        self.assertEqual(normalize("un cafè", "ca-ES"), "un cafè")
        # "nou" is "new" here
        self.assertEqual(normalize("crea un esdeveniment nou", "ca-ES"), "crea un esdeveniment nou")

    def test_czech(self):
        # 20 + 5
        self.assertEqual(normalize("nastav časovač na dvacet pět minut", "cs-CZ"), "nastav časovač na 25 minut")

    def test_ukrainian_typographic_apostrophe(self):
        # двадцять п’ять: 20 + 5, written with U+2019
        self.assertEqual(normalize("постав таймер на двадцять п’ять хвилин", "uk-UA"), "постав таймер на 25 хвилин")

    def test_azerbaijani(self):
        # iyirmi beş: 20 + 5
        self.assertEqual(normalize("iyirmi beş", "az-AZ"), "25")

    def test_plugin_variants(self):
        variants, _ = UtteranceNormalizerPlugin().transform(["vinte e cinco por cento"], {"lang": "pt-PT"})
        self.assertIn("25 por cento", variants)
        self.assertIn("vinte e cinco por cento", variants)


if __name__ == "__main__":
    unittest.main()
