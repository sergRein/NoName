import readline
from app.functions import add_contact, edit_contact, upcoming_birthdays, remove_contact, show_contact, save_data, load_data, find_contact
from app.visualiser import show_menu, show_all_contacts, green_input, show_all_notes_table
from app.function_notes import NotesManager

def parse_input(user_input: str) -> tuple[str, list[str]]:
    parts = user_input.split()  # split all input args
    cmd = parts[0].strip().lower() if parts else ""
    #args = parts[1:] if len(parts) > 1 else []
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
    "note-add": lambda: notes_manager.add_note(),
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

# autocompleter
def completer(text, state):
    options = [cmd for cmd in (commands_book | commands_note).keys() if cmd.startswith(text)]
    return options[state] if state < len(options) else None

# readline use tab to complete command
readline.parse_and_bind("tab: complete")
readline.set_completer(completer)

def main(book) -> None:
    print("Welcome to the assistant bot!")
    show_menu()
    
    while True:
        user_input = green_input("Enter a command: ")
        command = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "add":  # додано окрему перевірку для add_contact
            result = add_contact(book)
            if result is not None:
                print(result)
        elif command == "edit":  # додано окрему перевірку для add_contact
            result = edit_contact(book)
            if result is not None:
                print(result)
        elif command in commands_book:
            result = commands_book[command](book)
            if result is not None:
                print(result)
        elif command in commands_note:
            result = commands_note[command]()
            if result is not None:
                print(result)
        else:
            print("Invalid command.")

if __name__ == '__main__':
    notes_manager = NotesManager()
    notes_manager.import_notes('notes.json')
    book = load_data()
    main(book)
    #save our data
    save_data(book)
    notes_manager.export_notes('notes.json')
