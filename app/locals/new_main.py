import readline
from app.functions import load_data, save_data
from app.visualiser import show_menu
from app.classes.address_book import AddressBook
from app.classes.record import Record
from app.localization import trans  # Імпортуємо функцію trans для перекладу

def get_input(prompt: str) -> str:
    """Отримує ввід користувача для заданого запиту."""
    return input(f"{prompt}: ").strip()

def main():
    book = load_data()
    print(trans("hello"))

    show_menu()
    
    while True:
        command = get_input(trans("Enter a command"))
        
        if command in ["close", "exit"]:
            print(trans("goodbye"))
            break
        elif command in ["help", "menu"]:
            show_menu()
        elif command == "add":
            print(add_contact(book))
        else:
            print(trans("Invalid command"))

    save_data(book)