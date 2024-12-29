import json

class Translator:
    def __init__(self, locale="en"):
        self.locale = locale
        self.translations = self.load_translations()

    def load_translations(self):
        try:
            with open(f"locales/{self.locale}.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def translate(self, key, **kwargs):
        text = self.translations.get(key, key)
        return text.format(**kwargs)

    def set_locale(self, locale):
        self.locale = locale
        self.translations = self.load_translations()
