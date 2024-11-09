
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
    "notes-help": lambda: show_menu_notes(),
    "notes-menu": lambda: show_menu_notes(),
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


record_edit_commands = {
    "add phone": None,
    "edit phone": None,
    "delete phone": None,
    "add address": None,
    "edit address": None,
}

current_commands = commands_book | commands_note

def enter_edit_mode():
    """Входить в режим редагування і переключає команди на редагування."""
    global current_commands
    current_commands = record_edit_commands

def exit_edit_mode():
    """Виходить з режиму редагування і повертає основні команди."""
    global current_commands
    current_commands = commands_book | commands_note



def completer(text, state):
    """completer function. use tab for available commands"""
    options = [cmd for cmd in (current_commands).keys() if cmd.startswith(text)]
    return options[state] if state < len(options) else None
