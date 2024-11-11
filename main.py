"""Main module for address book"""

import readline
from app.functions import (
    add_contact, edit_contact, upcoming_birthdays, remove_contact,
    show_contact, save_data, load_data, find_contact
)
from app.visualiser import (
    show_menu, show_all_contacts, green_input, show_all_notes_table,
    show_menu_notes
)
from app.function_notes import NotesManager
from app.classes.localization import trans

# init main classes
notes_manager = NotesManager()
book = load_data()


def parse_input(user_input: str) -> tuple[str, list[str]]:
    """Parse user input into command and arguments."""
    parts = user_input.split()  # Split all input args
    cmd = parts[0].strip().lower() if parts else ""
    return cmd


# Dictionary of commands and their functions
commands_book = {
    "hello": lambda book: "How can I help you?",
    "add": add_contact,
    "edit": edit_contact,
    "all": show_all_contacts,
    "birthdays": upcoming_birthdays,
    "close": lambda book: "Good bye!",
    "exit": lambda book: "Good bye!",
    "help": lambda book: show_menu(),
    "menu": lambda book: show_menu(),
    "remove-contact": remove_contact,
    "show-contact": show_contact,
    "find": find_contact
}

commands_note = {
    "notes-help": show_menu_notes,
    "notes-menu": show_menu_notes,
    "note-add": lambda: notes_manager.add_note(),
    "note-show": lambda: notes_manager.show_note(),
    "note-edit": lambda: notes_manager.edit_note(),
    "note-delete": lambda: notes_manager.delete_note(),
    "note-search": lambda: notes_manager.search_notes_by_keyword(),
    "note-add-tag": lambda: notes_manager.add_tag(),
    "note-search-by-tag": lambda: notes_manager.search_notes_by_tag(),
    "note-encrypt": lambda: notes_manager.encrypt_note(),
    "note-decrypt": lambda: notes_manager.decrypt_note(),
    "notes-import": lambda: notes_manager.import_notes(),
    "notes-export": lambda: notes_manager.export_notes(),
    "note-save": lambda: notes_manager.save_notes(),
    "notes-backup": lambda: notes_manager.backup_notes(),
    "notes-all": lambda: show_all_notes_table(notes_manager),
}

# Commands and elements for edit
actions = ["add", "change", "delete"]
elements = ["phone", "address", "email", "birthday"]

# Dict for all edit commands
record_edit_commands = {
    f"{action}-{element}": None for action in actions for element in elements
}
record_edit_commands["done"] = None
record_edit_commands["show"] = None

current_commands = commands_book | commands_note


def enter_edit_mode():
    """Switch autocompleter to edit user commands."""
    global current_commands
    current_commands = record_edit_commands
    init_completer()


def exit_edit_mode():
    """Switch autocompleter to main commands."""
    global current_commands
    current_commands = commands_book | commands_note
    init_completer()


def completer(text, state):
    """Completer function. Use tab for available commands."""
    options = [
        cmd for cmd in current_commands.keys() if cmd.startswith(text)
    ]
    return options[state] if state < len(options) else None


# Initialize readline for tab completion
def init_completer():
    """autocompliter setup"""
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)


init_completer()


def main():
    """Main function to handle user input and commands."""
    notes_manager.import_notes('notes.json')  # load notes
    book = load_data()  # load address book data
    
    print(trans("Welcome to the assistant bot!"))
    show_menu()

    while True:
        user_input = green_input("Enter a command")
        command = parse_input(user_input)

        if command in ["close", "exit"]:
            print(trans("Good bye!"))
            break

        if command == "add":
            result = add_contact(book)
            if result:
                print(result)
        elif command == "edit":
            enter_edit_mode()
            result = edit_contact(book, exit_edit_mode)
            if result:
                print(result)
        elif command in commands_book:
            result = commands_book[command](book)
            if result:
                print(result)
        elif command in commands_note:
            result = commands_note[command]()
            if result:
                print(result)
        else:
            print(trans("Invalid command."))

    # Save our data
    save_data(book)
    notes_manager.export_notes('notes.json')



if __name__ == '__main__':
    #notes_manager = NotesManager()
    #notes_manager.import_notes('notes.json')
    #book = load_data()
    #main(book)
    ## Save our data
    #save_data(book)
    #notes_manager.export_notes('notes.json')
    main()
