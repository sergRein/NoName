from tabulate import tabulate
from colorama import Fore, Style, init
from app.classes.address_book import AddressBook
from app.classes.record import Record

init(autoreset=True)

def show_menu():
"""show_menu function."""
    menu_data = [
        [f"{Fore.GREEN}help or menu{Style.RESET_ALL}", f"{Fore.GREEN}Show available commands{Style.RESET_ALL}"],
        [f"{Fore.GREEN}hello{Style.RESET_ALL}", f"{Fore.GREEN}Show hello message{Style.RESET_ALL}"],
        [f"{Fore.GREEN}all{Style.RESET_ALL}", f"{Fore.GREEN}Show all phones in address book{Style.RESET_ALL}"],
        [f"{Fore.GREEN}add{Style.RESET_ALL}", f"{Fore.GREEN}Add new record{Style.RESET_ALL}"],
        [f"{Fore.GREEN}change{Style.RESET_ALL}", f"{Fore.GREEN}Change phone number{Style.RESET_ALL}"],
        [f"{Fore.GREEN}phone{Style.RESET_ALL}", f"{Fore.GREEN}Show phone for user with name{Style.RESET_ALL}"],
        [f"{Fore.GREEN}add-birthday{Style.RESET_ALL}", f"{Fore.GREEN}Add birthday for user{Style.RESET_ALL}"],
        [f"{Fore.GREEN}show-birthday{Style.RESET_ALL}", f"{Fore.GREEN}Show birthday for user{Style.RESET_ALL}"],
        [f"{Fore.GREEN}add-email{Style.RESET_ALL}", f"{Fore.GREEN}Add email for user{Style.RESET_ALL}"],
        [f"{Fore.GREEN}add-address{Style.RESET_ALL}", f"{Fore.GREEN}Add or change user address{Style.RESET_ALL}"],
        [f"{Fore.GREEN}remove-address{Style.RESET_ALL}", f"{Fore.GREEN}Remove user address{Style.RESET_ALL}"],
        [f"{Fore.GREEN}birthdays{Style.RESET_ALL}", f"{Fore.GREEN}Show upcoming birthdays{Style.RESET_ALL}"],
        [f"{Fore.GREEN}remove-contact{Style.RESET_ALL}", f"{Fore.GREEN}Remove contact with name{Style.RESET_ALL}"],
        [f"{Fore.GREEN}close or exit{Style.RESET_ALL}", f"{Fore.GREEN}Exit from program{Style.RESET_ALL}"]
    ]
    
    table = tabulate(menu_data, headers=[f"{Fore.GREEN}Command{Style.RESET_ALL}", f"{Fore.GREEN}Description{Style.RESET_ALL}"], tablefmt="grid")
    print(Style.BRIGHT + table)




def error_out(error: str) -> str:
    """Виводить текст помилки червоним кольором."""
    return f"{Fore.RED}{error}{Style.RESET_ALL}"

def green_input(prompt: str) -> str:
    """Виводить текст запиту зеленим кольором і повертає введене користувачем значення."""
    return input(f"{Fore.GREEN}{prompt}{Style.RESET_ALL}")

def blue_input(prompt: str) -> str:
    """Виводить текст запиту зеленим кольором і повертає введене користувачем значення."""
    return input(f"{Fore.BLUE}{prompt}{Style.RESET_ALL}")

def format_record_for_display(record, query=None) -> dict:
    """Форматує запис для виведення у таблиці та виділяє пошуковий запит жовтим кольором, якщо задано."""
    
    def highlight(text):
"""highlight function."""
        return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"

    name = record.name.value
    phones = "; ".join(phone.value for phone in record.phones)
    email = record.email.value if record.email else "Немає"
    addresses = "\n".join(f"{address.label}: {address.address}" for address in record.addresses.values())
    birthday = record.birthday.value.strftime('%d.%m.%Y') if record.birthday else "Немає"

    if query:
        query_lower = query.lower()
        name = name.replace(query, highlight(query)) if query_lower in name.lower() else name
        phones = "; ".join(phone.replace(query, highlight(query)) if query_lower in phone.lower() else phone 
                           for phone in phones.split("; "))
        email = email.replace(query, highlight(query)) if query_lower in email.lower() else email
        addresses = addresses.replace(query, highlight(query)) if query_lower in addresses.lower() else addresses
        birthday = birthday.replace(query, highlight(query)) if query_lower in birthday.lower() else birthday

    return {
        "Ім'я": name,
        "Телефони": phones,
        "Email": email,
        "Адреси": addresses,
        "День народження": birthday,
    }


def show_all_contacts(book: AddressBook) -> str:
    """Виводить всю інформацію по адресній книзі у вигляді таблиці із зеленим кольором."""
    if not book.data:
        return f"{Fore.GREEN}Адресна книга порожня.{Style.RESET_ALL}"
    
    table = [format_record_for_display(record) for record in book.data.values()]
    table_str = tabulate(table, headers="keys", tablefmt="grid", stralign="center")
    
    return f"{Fore.GREEN}{table_str}{Style.RESET_ALL}"


def show_contact_table(record: Record) -> str:
    """Виводить всю інформацію по запису в книзі у вигляді таблиці із зеленим кольором."""
    
    table = [format_record_for_display(record)]
    table_str = tabulate(table, headers="keys", tablefmt="grid", stralign="center")
    
    return f"{Fore.GREEN}{table_str}{Style.RESET_ALL}"


def show_all_notes_table(notes_manager):
    """Відображає всі нотатки у вигляді таблиці."""
    if not notes_manager.notes:
        return f"{Fore.GREEN}Нотаток немає.{Style.RESET_ALL}"
    
    table = [
        {"Заголовок": title, "Вміст": note["content"], "Теги": "\n".join(note["tags"])}
        for title, note in notes_manager.notes.items()
    ]
    table_str = tabulate(table, headers="keys", tablefmt="grid", stralign="center")
    
    return f"{Fore.GREEN}{table_str}{Style.RESET_ALL}"


def show_search_results_table(results, query=None):
    """Відображає результати пошуку у вигляді таблиці, виділяючи пошуковий запит жовтим кольором."""
    if not results:
        return f"{Fore.GREEN}Нічого не знайдено за запитом.{Style.RESET_ALL}"
    
    table = [format_record_for_display(record, query) for record in results]
    table_str = tabulate(table, headers="keys", tablefmt="grid", stralign="center")
    
    return f"{Fore.GREEN}{table_str}{Style.RESET_ALL}"
