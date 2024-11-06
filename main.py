import readline
from app.functions import load_data, save_data, add_contact, change_contact, show_phone, add_birthday, show_birthday, upcoming_birthdays
from app.visualiser import show_menu

def parse_input(user_input: str) -> tuple[str, list[str]]:
    parts = user_input.split()  # split all input args
    cmd = parts[0].strip().lower() if parts else ""
    args = parts[1:] if len(parts) > 1 else []
    return cmd, args

# Словник команд та їх функцій
commands = { 
    "hello": lambda args, book: "How can I help you?",
    "add": add_contact,
    "change": change_contact,
    "phone": show_phone,
    "all": lambda args, book: str(book),
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": upcoming_birthdays,
    "close": lambda args, book: "Good bye!",
    "exit": lambda args, book: "Good bye!",
    "help": lambda args, book: show_menu(),
    "menu": lambda args, book: show_menu()
}

# autocompeter
def completer(text, state):
    options = [cmd for cmd in commands.keys() if cmd.startswith(text)]
    return options[state] if state < len(options) else None

# readline use tab to complete command
readline.parse_and_bind("tab: complete")
readline.set_completer(completer)

def main(book) -> None:
    print("Welcome to the assistant bot!")
    show_menu()
    
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command in commands:
            result = commands[command](args, book)
            if result is not None:
                print(result)
        else:
            print("Invalid command.")

if __name__ == '__main__':
    book = load_data()
    main(book)
    save_data(book)
