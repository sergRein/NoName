import yaml
import os

class Localization:
    def __init__(self, locale_dir="locales"):
        self.translations = {}
        self.locale_dir = locale_dir
        self.load_language(self.choose_language())

    def choose_language(self) -> str:
        """Запитує у користувача бажану мову з доступних файлів у папці."""
        files = [f for f in os.listdir(self.locale_dir) if f.endswith('.yaml')]
        languages = [os.path.splitext(f)[0] for f in files]
        
        print("Виберіть мову:", ", ".join(languages))
        lang = input("Language: ").strip().lower()

        while lang not in languages:
            print("Невірний вибір. Доступні мови:", ", ".join(languages))
            lang = input("Language: ").strip().lower()

        return lang

    def load_language(self, lang: str):
        """Завантажує файл локалізації для вибраної мови."""
        path = os.path.join(self.locale_dir, f"{lang}.yaml")
        with open(path, "r", encoding="utf-8") as f:
            self.translations = yaml.safe_load(f)

    def translate(self, key: str) -> str:
        """Повертає перекладений текст для заданого ключа, або сам ключ, якщо переклад відсутній."""
        return self.translations.get(key, key)

# Ініціалізуємо об'єкт локалізації
localization = Localization()

# Функція для спрощення перекладу
def trans(key: str) -> str:
    return localization.translate(key)