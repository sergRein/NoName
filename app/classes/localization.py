import yaml
import os

class Localization:
    def __init__(self, locale_dir="./app/locals"):
        self.translations = {}
        self.locale_dir = locale_dir
        self.language = self.choose_language()
        self.file_path = os.path.join(self.locale_dir, f"{self.language}.yaml")
        self.load_language(self.language)

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
        with open(self.file_path, "r", encoding="utf-8") as f:
            self.translations = yaml.safe_load(f) or {}

    def append_missing_translation(self, key: str):
        """Додає відсутній ключ у файл локалізації та оновлює словник у пам'яті."""
        self.translations[key] = key  # Оновлюємо словник перекладів у пам'яті
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(f"\n{key}: {key}")

    def translate(self, key: str) -> str:
        """Повертає перекладений текст для заданого ключа або додає його, якщо він відсутній."""
        if key in self.translations:
            return self.translations[key]
        # If not, add the key and value to both the file and self.translations
        self.append_missing_translation(key)
        return self.translations[key]


# Створюємо єдиний екземпляр Localization, доступний глобально
_localization = Localization()

def trans(key: str) -> str:
    """Глобальна функція для перекладу, що використовує єдиний екземпляр Localization."""
    return _localization.translate(key)
