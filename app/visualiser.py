from tabulate import tabulate
from colorama import Fore, Style, init
from app.classes.address_book import AddressBook
from app.classes.record import Record
from app.classes.localization import trans

init(autoreset=True)

def show_menu_notes():
    """show help notes data function"""
    menu_data = [
        ['note-add', trans('Add note')],
        ['note-show', trans('Show note')],
        ['note-edit', trans('Edit note')],
        ['note-delete', trans('Delete note')],
        ['note-search', trans('Search note')],
        ['note-add-tag', trans('Add tag to note')],
        ['note-search-by-tag', trans('Search note by tag')],
        ['note-encrypt', trans('Encrypt note')],
        ['note-decrypt', trans('Decrypt note')],
        ['notes-import', trans('Import notes from file')],
        ['notes-export', trans('Export notes to file')],
        ['note-save', trans('Save note')],
        ['notes-backup', trans('Backup notes')],
        ['notes-all', trans('Show all notes')]
    ]
    menu_data = [[green_string(item) for item in row] for row in menu_data]
    table = tabulate(menu_data, headers=[f"{green_string('Command')}", f"{green_string('Description')}"], tablefmt="grid")
    print(Style.BRIGHT + table)

def show_menu():
    """show help data function."""
    menu_data = [
        ['help or menu', trans('Show available commands')],
        ['notes-help or notes-menu', trans('Show available commands for notes')],
        ['hello', trans('Show hello message')],
        ['all', trans('Show all phones in address book')],
        ['add', trans('Add new record')],
        ['edit', trans('Change phone number')],
        ['birthdays', trans('Show upcoming birthdays')],
        ['remove-contact', trans('Remove contact with name')],
        ['show-contact', trans('Show contact by name')],
        ['find', trans('Find contacts containing search query')],
        ['close or exit', trans('Exit from program')]
    ]
    menu_data = [[green_string(item) for item in row] for row in menu_data]
    table = tabulate(menu_data, headers=[f"{green_string('Command')}", f"{green_string('Description')}"], tablefmt="grid")
    print(Style.BRIGHT + table)


def green_string(text: str) -> str:
    """return string in green color"""
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}"

def blue_string(text: str) -> str:
    """return string in green color"""
    return f"{Fore.BLUE}{trans(text)}{Style.RESET_ALL}"

def error_out(error: str) -> str:
    """return red string, used to output errors"""
    return f"{Fore.RED}{trans(str(error))}{Style.RESET_ALL}"

def green_input(prompt: str) -> str:
    """Colorized input to green color"""
    return input(f"{Fore.GREEN}{trans(prompt)+':'}{Style.RESET_ALL}")

def blue_input(prompt: str) -> str:
    """Colorized input to blue color"""
    return input(f"{Fore.BLUE}{trans(prompt)+':'}{Style.RESET_ALL}")

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
        trans("Name_short"): name,
        trans("Phones_short"): phones,
        trans("Email_short"): email,
        trans("Adresses_short"): addresses,
        trans("Birthday_short"): birthday,
    }


def show_all_contacts(book: AddressBook) -> str:
    """show all records in address book as table """
    if not book.data:
        return f"{green_string(trans('Address book is empty'))}"
    
    table = [format_record_for_display(record) for record in book.data.values()]
    table_str = tabulate(table, headers="keys", tablefmt="grid", stralign="center")
    
    return f"{green_string(table_str)}"


def show_contact_table(record: Record) -> str:
    """Show one record as table"""
    
    table = [format_record_for_display(record)]
    table_str = tabulate(table, headers="keys", tablefmt="grid", stralign="center")
    
    return f"{green_string(table_str)}"

def show_note_table(title, content, tags):
    """Draw a single note as a table."""
    # Prepare the table data
    table = [
        {trans("Header"): title, trans("Text"): content, trans("Tags"): "\n".join(tags) if tags else trans("No tags")}
    ]
    # Format the table using tabulate
    table_str = tabulate(table, headers="keys", tablefmt="grid", stralign="center")
    return green_string(table_str)

def show_all_notes_table(notes_manager):
    """Show all notes as table"""
    if not notes_manager.notes:
        return f"{green_string(trans('Notes are empty'))}"
    
    table = [
        {trans("Header"): title, trans("Text"): note["content"], trans("Tags"): "\n".join(note["tags"])}
        for title, note in notes_manager.notes.items()
    ]
    table_str = tabulate(table, headers="keys", tablefmt="grid", stralign="center")
    
    return f"{green_string(table_str)}"


def show_search_results_table(results, query=None):
    """Show records after search"""
    if not results:
        return f"{green_string(trans('Nothing was found by query: ') + query)}"
    
    table = [format_record_for_display(record, query) for record in results]
    table_str = tabulate(table, headers="keys", tablefmt="grid", stralign="center")
    
    return f"{green_string(table_str)}"
