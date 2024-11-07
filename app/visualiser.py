from tabulate import tabulate
from colorama import Fore, Style, init
from app.classes.address_book import AddressBook
from app.functions import get_input, get_contact_from_book

init(autoreset=True)

def show_menu():
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


def green_input(prompt: str) -> str:
    """Виводить текст запиту зеленим кольором і повертає введене користувачем значення."""
    return input(f"{Fore.GREEN}{prompt}{Style.RESET_ALL}")

def format_record_for_display(record) -> dict:
    """Форматує запис для виведення у таблиці."""
    return {
        "Ім'я": record.name.value,
        "Телефони": "; ".join(phone.value for phone in record.phones),
        "Email": record.email.value if record.email else "Немає",
        "Адреси": "; ".join(f"{address.label}: {address.address}" for address in record.addresses.values()),
        "День народження": record.birthday.value.strftime('%d.%m.%Y') if record.birthday else "Немає",
    }

def show_all_contacts(book: AddressBook) -> str:
    """Виводить всю інформацію по адресній книзі у вигляді таблиці із зеленим кольором."""
    if not book.data:
        return f"{Fore.GREEN}Адресна книга порожня.{Style.RESET_ALL}"
    
    table = [format_record_for_display(record) for record in book.data.values()]
    table_str = tabulate(table, headers="keys", tablefmt="grid", stralign="center")
    
    return f"{Fore.GREEN}{table_str}{Style.RESET_ALL}"


def show_contact(book: AddressBook) -> str:
    """Виводить всю інформацію по адресній книзі у вигляді таблиці із зеленим кольором."""
    name = get_input("Enter name of contact")
    record = get_contact_from_book(name, book)
    
    table = [format_record_for_display(record)]
    table_str = tabulate(table, headers="keys", tablefmt="grid", stralign="center")
    
    return f"{Fore.GREEN}{table_str}{Style.RESET_ALL}"