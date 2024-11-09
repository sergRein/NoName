from tabulate import tabulate
from colorama import Fore, Style, init
from app.classes.address_book import AddressBook
from app.classes.record import Record

init(autoreset=True)

def show_menu_notes():
    """show help notes data function"""
    menu_data = [
        ['note-add', 'Add note'],
        ['note-edit', 'Edit note'],
        ['note-delete', 'Delete note'],
        ['note-search', 'Search note'],
        ['note-add-tag', 'Add tag to note'],
        ['note-search-by-tag', 'Search note by tag'],
        ['note-encrypt', 'Encrypt note'],
        ['note-decrypt', 'Decrypt note'],
        ['notes-import', 'Import notes from file'],
        ['notes-export', 'Export notes to file'],
        ['note-save', 'Save note'],
        ['notes-backup', 'Backup notes'],
        ['notes-all', 'Show all notes']
    ]
    menu_data = [[green_string(item) for item in row] for row in menu_data]
    table = tabulate(menu_data, headers=[f"{green_string('Command')}", f"{green_string('Description')}"], tablefmt="grid")
    print(Style.BRIGHT + table)

def show_menu():
    """show help data function."""
    menu_data = [
        ['help or menu', 'Show available commands'],
        ['notes-help or notes-menu', 'Show available commands for notes'],
        ['hello', 'Show hello message'],
        ['all', 'Show all phones in address book'],
        ['add', 'Add new record'],
        ['edit', 'Change phone number'],
        ['birthdays', 'Show upcoming birthdays'],
        ['remove-contact', 'Remove contact with name'],
        ['show-contact', 'Show contact by name'],
        ['find', 'Find contacts containing search query'],
        ['close or exit', 'Exit from program']
    ]
    menu_data = [[green_string(item) for item in row] for row in menu_data]
    table = tabulate(menu_data, headers=[f"{green_string('Command')}", f"{green_string('Description')}"], tablefmt="grid")
    print(Style.BRIGHT + table)


def green_string(str: str) -> str:
    """return string in green color"""
    return f"{Fore.GREEN}{str}{Style.RESET_ALL}"

def error_out(error: str) -> str:
    """return red string, used to output errors"""
    return f"{Fore.RED}{error}{Style.RESET_ALL}"

def green_input(prompt: str) -> str:
    """Colorized input to green color"""
    return input(f"{Fore.GREEN}{prompt}{Style.RESET_ALL}")

def blue_input(prompt: str) -> str:
    """Colorized input to blue color"""
    return input(f"{Fore.BLUE}{prompt}{Style.RESET_ALL}")

def format_record_for_display(record, query=None) -> dict:
    """Formating record into table and colorize search query in yellow if serach query presents"""
    
    def highlight(text: str) -> str:
        """highlight in yellow function."""
        return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"

    name = record.name.value
    phones = "\n".join(phone.value for phone in record.phones)
    email = record.email.value if record.email else "Немає"
    addresses = "\n".join(f"{address.label}: {address.address}" for address in record.addresses.values())
    birthday = record.birthday.value.strftime('%d.%m.%Y') if record.birthday else "Немає"

    if query:
        query_lower = query.lower()
        name = name.replace(query, highlight(query)) if query_lower in name.lower() else name
        phones = "\n".join(phone.replace(query, highlight(query)) if query_lower in phone.lower() else phone 
                           for phone in phones.split("\n"))
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
    """show all records in address book as table """
    if not book.data:
        return f"{Fore.GREEN}Адресна книга порожня.{Style.RESET_ALL}"
    
    table = [format_record_for_display(record) for record in book.data.values()]
    table_str = tabulate(table, headers="keys", tablefmt="grid", stralign="center")
    
    return f"{Fore.GREEN}{table_str}{Style.RESET_ALL}"


def show_contact_table(record: Record) -> str:
    """Show one record as table"""
    
    table = [format_record_for_display(record)]
    table_str = tabulate(table, headers="keys", tablefmt="grid", stralign="center")
    
    return f"{Fore.GREEN}{table_str}{Style.RESET_ALL}"


def show_all_notes_table(notes_manager):
    """Show all notes as table"""
    if not notes_manager.notes:
        return f"{Fore.GREEN}Нотаток немає.{Style.RESET_ALL}"
    
    table = [
        {"Заголовок": title, "Вміст": note["content"], "Теги": "\n".join(note["tags"])}
        for title, note in notes_manager.notes.items()
    ]
    table_str = tabulate(table, headers="keys", tablefmt="grid", stralign="center")
    
    return f"{Fore.GREEN}{table_str}{Style.RESET_ALL}"


def show_search_results_table(results, query=None):
    """Show records after search"""
    if not results:
        return f"{Fore.GREEN}Нічого не знайдено за запитом.{Style.RESET_ALL}"
    
    table = [format_record_for_display(record, query) for record in results]
    table_str = tabulate(table, headers="keys", tablefmt="grid", stralign="center")
    
    return f"{Fore.GREEN}{table_str}{Style.RESET_ALL}"
