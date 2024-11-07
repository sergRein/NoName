import readline
from app.functions import *
from app.visualiser import show_menu, show_all_contacts, green_input, show_contact
from app.classes.function_notes import NotesManager

def parse_input(user_input: str) -> tuple[str, list[str]]:
    parts = user_input.split()  # split all input args
    cmd = parts[0].strip().lower() if parts else ""
    args = parts[1:] if len(parts) > 1 else []
    return cmd, args

# Dictionary of commands and their functions
commands = { 
    "hello": lambda book: "How can I help you?",
    "add": add_contact,
    "change": change_contact,
    "phone": show_phone,
    "all": show_all_contacts,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": upcoming_birthdays,
    "close": lambda book: "Good bye!",
    "exit": lambda book: "Good bye!",
    "help": lambda book: show_menu(),
    "menu": lambda book: show_menu(),
    "add-email": add_email,
    "add-address": add_address,
    "remove-address": remove_address,
    "remove-contact": remove_contact,
    "show-contact": show_contact,
    "add-note": lambda: notes_manager.add_note(),
    "edit-note": lambda: notes_manager.edit_note(),
    "delete-note": lambda: notes_manager.delete_note(),
    "search-note": lambda: notes_manager.search_notes_by_keyword(),
    "add-tag": lambda: notes_manager.add_tag(),
    "search-note-by-tag": lambda: notes_manager.search_notes_by_tag(),
    "encrypt-note": lambda: notes_manager.encrypt_note(),
    "decrypt-note": lambda: notes_manager.decrypt_note(),
    "import-notes": lambda: notes_manager.import_notes(),
    "export-notes": lambda: notes_manager.export_notes(),
    "save-note": lambda: notes_manager.save_notes(),
    "backup-notes": lambda: notes_manager.backup_notes(),
}

# autocompleter
def completer(text, state):
    options = [cmd for cmd in commands.keys() if cmd.startswith(text)]
    return options[state] if state < len(options) else None

# readline use tab to complete command
readline.parse_and_bind("tab: complete")
readline.set_completer(completer)

def main(book) -> None:
    notes_manager = NotesManager()
    print("Welcome to the assistant bot!")
    show_menu()
    
    while True:
        user_input = green_input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command in commands:
            # Use notes_manager instance for notes-related commands
            if command in ["add-note", "edit-note", "delete-note", "search-note", "add-tag", "search-note-by-tag", "encrypt-note", "decrypt-note", "import-notes", "export-notes", "save-note", "backup-notes"]:
                result = commands[command]()
            else:
                result = commands[command](book)
            if result is not None:
                print(result)
        else:
            print("Invalid command.")

if __name__ == '__main__':
    book = load_data()
    main(book)
    save_data(book)
