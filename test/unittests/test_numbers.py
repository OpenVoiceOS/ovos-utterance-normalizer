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
        # 20 + 5
        self.assertEqual(normalize("vint-i-cinc", "ca-ES"), "25")
        # "a les nou": nine o'clock
        self.assertEqual(normalize("posa una alarma a les nou", "ca-ES"), "posa una alarma a les 9")
        # the percent word "cent" is no number without a number before it
        self.assertEqual(normalize("posa el volum al quinze per cent", "ca-ES"), "posa el volum 15 per cent")
        self.assertEqual(normalize("atenua la llum al per cent", "ca-ES"), "atenua la llum per cent")
        self.assertEqual(normalize("un cafè", "ca-ES"), "un cafè")

    def test_russian(self):
        # 10
        self.assertEqual(normalize("поставь таймер на десять минут", "ru-RU"), "поставь таймер на 10 минут")
        # "не ... ни одного" and "одно и то же" name no number
        self.assertEqual(normalize("я не пропустил ни одного таймера", "ru-RU"),
                         "я не пропустил ни одного таймера")
        self.assertEqual(normalize("обнови календарь чтобы было одно и то же", "ru-RU"),
                         "обнови календарь чтобы было одно и то же")

    def test_czech_homograph_stays_word(self):
        # "jednou" is "once", not the number 1: numtag marks it as a homograph
        self.assertEqual(normalize("nastav časovač jednou", "cs-CZ"), "nastav časovač jednou")

    def test_catalan_homograph_stays_word(self):
        # "nou" is "new" in "un nou enregistrament", not 9
        self.assertEqual(normalize("un nou enregistrament", "ca-ES"), "un nou enregistrament")

    def test_galician(self):
        # "dez" is 10; the article "unha" stays a word
        self.assertEqual(normalize("pon un temporizador de dez minutos", "gl-ES"),
                         "pon un temporizador de 10 minutos")
        self.assertEqual(normalize("pon unha alarma", "gl-ES"), "pon unha alarma")
        self.assertEqual(normalize("unha", "gl-ES"), "unha")

    def test_romanian(self):
        # "zece" is 10; "o" is the article or the pronoun "her", never the number 1
        self.assertEqual(normalize("setează un cronometru de zece minute", "ro-RO"),
                         "setează un cronometru de 10 minute")
        self.assertEqual(normalize("pune o alarmă", "ro-RO"), "pune o alarmă")
        self.assertEqual(normalize("o", "ro-RO"), "o")

    def test_several_numbers_in_one_utterance(self):
        # 30 and 5: each span keeps its place while the text changes
        self.assertEqual(normalize("set a timer for thirty seconds and five minutes", "en-US"),
                         "set a timer for 30 seconds and 5 minutes")
        self.assertEqual(normalize("pon un temporizador de veinte minutos y treinta segundos", "es-ES"),
                         "pon un temporizador de 20 minutos y 30 segundos")

    def test_czech(self):
        # 20 + 5
        self.assertEqual(normalize("nastav časovač na dvacet pět minut", "cs-CZ"), "nastav časovač na 25 minut")

    def test_ukrainian_typographic_apostrophe(self):
        # двадцять п’ять: 20 + 5, written with U+2019
        self.assertEqual(normalize("постав таймер на двадцять п’ять хвилин", "uk-UA"), "постав таймер на 25 хвилин")

    def test_azerbaijani_keeps_words(self):
        # no shipped skill locale measures az, so it is outside NUMBER_LANGUAGES
        self.assertEqual(normalize("iyirmi beş", "az-AZ"), "iyirmi beş")

    def test_language_outside_set_keeps_words(self):
        # fr and it are outside NUMBER_LANGUAGES: no value check covers them
        self.assertEqual(normalize("mets le volume à cinquante pour cent", "fr-FR"),
                         "mets le volume à cinquante pour cent")
        self.assertEqual(normalize("un'altra volta", "it-IT"), "un'altra volta")

    def test_idiom_keeps_number_value(self):
        # numtag does no idiom detection: "mil" is 1000 in "mil gracias" too
        self.assertEqual(normalize("mil gracias", "es-ES"), "1000 gracias")
        self.assertEqual(normalize("desde cero", "es-ES"), "desde 0")
        # da is outside NUMBER_LANGUAGES: no value check covers it
        self.assertEqual(normalize("tusind tak", "da-DK"), "tusind tak")
        # hu is outside NUMBER_LANGUAGES: "ötkor" is 5 with the suffix "-kor", which a bare digit loses
        self.assertEqual(normalize("hozz létre egy emlékeztetőt hogy ötkor vegyek kenyeret", "hu-HU"),
                         "hozz létre egy emlékeztetőt hogy ötkor vegyek kenyeret")

    def test_language_in_set_without_own_normalizer(self):
        # Finnish kymmeneksi: translative case of kymmenen, 10
        self.assertEqual(normalize("laita ajastin kymmeneksi minuutiksi", "fi-FI"),
                         "laita ajastin 10 minuutiksi")
        # Turkish üç: 3
        self.assertEqual(normalize("önümüzdeki üç gün", "tr-TR"), "önümüzdeki 3 gün")

    def test_digits_keep_their_form(self):
        # numtag reads "05" as 5 and "1.000" as 1000; the user wrote digits, so they stay
        self.assertEqual(normalize("set a timer for 05 minutes", "en-US"), "set a timer for 05 minutes")
        self.assertEqual(normalize("custa 1.000 euros", "pt-PT"), "custa 1.000 euros")

    def test_plugin_variants(self):
        variants, _ = UtteranceNormalizerPlugin().transform(["vinte e cinco por cento"], {"lang": "pt-PT"})
        self.assertIn("25 por cento", variants)
        self.assertIn("vinte e cinco por cento", variants)


if __name__ == "__main__":
    unittest.main()
