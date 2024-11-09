# Проєкт "Pip-Boy"

## Огляд
Цей проєкт є персональним асистентом, написаним на Python в рамках курсу "Python Programming: Foundations and Best Practices". Він був створений для ефективного керування контактами та нотатками. "Pip-Boy" працює як інструмент командного рядка, де користувачі можуть зберігати, редагувати, шукати та видаляти інформацію, таку як контакти (імена, номери телефонів, адреси, електронні листи та дні народження) і текстові нотатки. Мета проєкту — допомогти користувачам зберігати особисті дані в організованому та зручному для доступу вигляді.

## Функції
- **Керування контактами**:
  - Додавання нових контактів з такими деталями, як ім'я, номер телефону, електронна пошта, адреса та день народження.
  - Редагування або видалення існуючих контактів.
  - Перевірка правильності номерів телефонів та електронних адрес.
  - Пошук контактів за іменем та перегляд списку контактів з майбутніми днями народження.
- **Керування нотатками**:
  - Створення, редагування та видалення текстових нотаток.
  - Пошук нотаток за ключовими словами.
- **Команди користувача**:
  - Інтерфейс командного рядка для ефективного та інтерактивного керування даними.

## Встановлення
1. **Клонувати репозиторій**:
   ```sh
   git clone [https://github.com/sergRein/NoName.git](https://github.com/sergRein/NoName.git)
   ```

2. **Перейдіть до директорії проєкту**:
   ```sh
   cd Personal-Assistant
   ```

3. **Встановіть залежності**:
   Переконайтеся, що у вас встановлено Python 3.7+. Встановіть необхідні залежності за допомогою:
   ```sh
   pip install -r requirements.txt
   ```

## Використання
Щоб запустити персонального асистента, просто виконайте файл `main.py`:
```sh
python main.py
```

Після запуску ви отримаєте доступ до різних команд для взаємодії з книгою контактів та нотатками. Асистент проведе вас через доступні дії.

### Доступні команди
- **hello**: Вітає користувача та починає взаємодію.
- **add**: Додає новий контакт до книги контактів.
- **edit**: Оновлює існуючий контакт.
- **all**: Показує всі контакти у книзі контактів.
- **birthdays**: Відображає контакти з майбутніми днями народження.
- **close/exit**: Закриває асистента.
- **help/menu**: Показує всі доступні команди.
- **remove-contact**: Видаляє контакт.
- **show-contact**: Відображає деталі конкретного контакту.
- **find**: Знаходить контакт за іменем.
- **note-add**: Додає нову нотатку.
- **note-edit**: Редагує існуючу нотатку.
- **note-delete**: Видаляє нотатку.
- **note-search**: Шукає нотатки за ключовим словом.

## Структура проєкту
- **main.py**: Основна точка входу в додаток.
- **app/functions.py**: Містить основні функції для керування контактами та нотатками.
- **app/visualiser.py**: Відповідає за відображення в командному рядку, наприклад, меню та форматований вивід.
- **app/classes/**:
  - **address_book.py**: Містить клас `AddressBook` для керування контактами.
  - **record.py**: Містить клас `Record`, що представляє окремий контакт.
  - **basic_classes.py**: Визначає базові класи, такі як `Name`, `Phone` та `Birthday`.

## Приклад взаємодії
1. Запустіть програму:
   ```sh
   python main.py
   ```
2. Введіть `hello`, щоб розпочати взаємодію.
3. Використовуйте команди, такі як `add`, `edit` або `all`, для керування контактами.
4. Введіть `help` у будь-який момент, щоб побачити повний список команд.

## Внесок у розвиток
Внесок у розвиток вітається! Якщо у вас є ідеї для нових функцій або покращень, не соромтеся форкнути репозиторій і надіслати pull request. Будь ласка, переконайтеся, що ваш код відповідає найкращим практикам і включає відповідну документацію.

## Ліцензія
Цей проєкт ліцензовано відповідно до ліцензії MIT. Деталі дивіться у файлі `LICENSE`.

