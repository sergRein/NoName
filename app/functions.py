from functools import wraps
import pickle
from app.classes.address_book import AddressBook
from app.classes.record import Record
from app.visualiser import show_contact_table, error_out, show_search_results_table, blue_input



def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError: 
            print(f"{error_out('No such user')}")
        except IndexError: 
            print("Contact not found")
        except ValueError as e:
            print(f"{error_out(e)}")
    return inner

def get_input(prompt: str, required = True) -> str:
    """Отримує ввід користувача для заданого запиту."""
    value = blue_input(f"{prompt}: ").strip()
    if value == '' and required:
        print(f"{error_out('Please input something')}")
    return value

def get_contact_from_book(name, book: AddressBook) -> Record:
    record = book.find(name)
    if not record:
        raise KeyError
    return record


@input_error
def add_contact(book: AddressBook) -> str:
    name = get_input("Enter name for contact")
    record = get_contact_from_book(name, book)
    if record:
        raise ValueError('Contat exists, you can edit it with edit command')
    # Перевірка та додавання телефону
    phone_added = False
    while not phone_added:
        phone = get_input("Enter phone for contact")
        if not phone:
            continue
        try:
            record = book.find(name) or Record(name)
            record.add_phone(phone)
            if name not in book.data:
                book.add_record(record)
            phone_added = True
        except ValueError as e:
            print(f"Error: {e}")
    
    email_added = False
    while not email_added:
        email = get_input("Enter email for contact (press Enter to skip)", False)
        if not email:
            email_added = True
        else:
            try:
                record.add_email(email)
                email_added = True
            except ValueError as e:
                print(f"Error: {e}")

    # Додавання дня народження з можливістю пропустити крок
    birthday_added = False
    while not birthday_added:
        birthday = get_input("Enter birthday for contact (press Enter to skip)", False)
        if not birthday:
            birthday_added = True
        else:
            try:
                record.add_birthday(birthday)
                birthday_added = True
            except ValueError as e:
                print(f"Error: {e}")

    # Додавання адрес з можливістю закінчити цикл натисканням Enter на
    addresses_finished = False
    while not addresses_finished:
        address_label = get_input("Enter address label (press Enter to finish adding addresses)", False)
        if not address_label:
            addresses_finished = True
        else:
            address = get_input("Enter address")
            record.add_address(address_label, address)

    print("Contact added successfully:")

    return show_contact_table(record)


@input_error
def edit_contact(book: AddressBook) -> str:
    name = get_input("Enter name of contact")
    record = get_contact_from_book(name, book)
    
    # Відображення поточного контакту
    print("Current contact information:")
    print(show_contact_table(record))

    print("\nAvailable options for updating contact:")
    print("Use commands in the format 'add field', 'change field', or 'delete field'.")
    print("Fields can be: phone, email, birthday, address.")
    print("Type 'done' to finish updating the contact.")
    print("Type 'show' to show current contact.")

    # Словник дій для кожного поля
    change_actions = {
        "phone": modify_phone,
        "email": modify_email,
        "birthday": modify_birthday,
        "address": modify_address
    }

    # Основний цикл для додавання, зміни чи видалення даних
    while True:
        action = get_input("Choose an action (e.g., 'add phone', 'change address', 'done' to finish)").strip().lower()
        
        if action == 'done':
            print("Finished updating contact")
            break

        if action == 'show':
            print(show_contact_table(record))
            continue

        # Розділення команди на дії та поле
        command_parts = action.split(maxsplit=1)
        if len(command_parts) < 2:
            print("Invalid format. Use 'add field', 'change field', or 'delete field'.")
            continue
        
        command, field = command_parts
        if command in ["add", "change", "delete"] and field in change_actions:
            # Виклик відповідної функції для обробки дій
            change_actions[field](record, command)
        else:
            print("Invalid option. Please choose a valid action in the format 'add field', 'change field', or 'delete field'.")

    # Показ оновленого контакту
    print("\nUpdated contact information:")
    return show_contact_table(record)


def modify_phone(record, action):
    if action == "add":
        new_phone = get_input("Enter new phone number: ")
        if record.find_phone(new_phone):
            print(f"The phone number '{new_phone}' already exists.")
        else:
            record.add_phone(new_phone)
            print("Phone added successfully.")
    
    elif action == "change":
        old_phone = get_input("Enter the phone number to update")
        if not record.find_phone(old_phone):
            print(f"The phone number '{old_phone}' does not exist.")
        else:
            new_phone = get_input("Enter the new phone number")
            if record.find_phone(new_phone):
                print(f"The phone number '{new_phone}' already exists.")
            else:
                record.edit_phone(old_phone, new_phone)
                print("Phone updated successfully.")
    
    elif action == "delete":
        phone_to_delete = get_input("Enter the phone number to delete")
        if not record.find_phone(phone_to_delete):
            print(f"The phone number '{phone_to_delete}' does not exist.")
        else:
            record.remove_phone(phone_to_delete)
            print("Phone deleted successfully.")


def modify_email(record, action):
    if action == "add":
        if record.email:
            print(f"The email '{record.email.value}' already exists.")
        else:
            new_email = get_input("Enter new email")
            record.add_email(new_email)
            print("Email added successfully.")
    
    elif action == "change":
        if not record.email:
            print("No email to update. Use 'add' to add a new email.")
        else:
            new_email = get_input("Enter the new email")
            record.add_email(new_email)
            print("Email updated successfully.")
    
    elif action == "delete":
        if not record.email:
            print("No email to delete.")
        else:
            record.email = None
            print("Email deleted successfully.")


def modify_birthday(record, action):
    if action == "add":
        if record.birthday:
            print(f"The birthday '{record.birthday.value.strftime('%d.%m.%Y')}' already exists.")
        else:
            new_birthday = get_input("Enter new birthday (DD.MM.YYYY)")
            record.add_birthday(new_birthday)
            print("Birthday added successfully.")
    
    elif action == "change":
        if not record.birthday:
            print("No birthday to update. Use 'add' to add a new birthday.")
        else:
            new_birthday = get_input("Enter the new birthday (DD.MM.YYYY)")
            record.add_birthday(new_birthday)
            print("Birthday updated successfully.")
    
    elif action == "delete":
        if not record.birthday:
            print("No birthday to delete.")
        else:
            record.birthday = None
            print("Birthday deleted successfully.")


def modify_address(record, action):
    if action == "add":
        label = get_input("Enter address label (e.g., 'Home', 'Work')")
        if label in record.addresses:
            print(f"Address with label '{label}' already exists.")
        else:
            address = get_input("Enter new address: ")
            record.add_address(label, address)
            print("Address added successfully.")
    
    elif action == "change":
        label = get_input("Enter the address label to update")
        if label not in record.addresses:
            print(f"No address with label '{label}' exists.")
        else:
            new_address = get_input("Enter the new address")
            record.edit_address(label, new_address)
            print("Address updated successfully.")
    
    elif action == "delete":
        label = get_input("Enter the address label to delete")
        if label not in record.addresses:
            print(f"No address with label '{label}' exists.")
        else:
            record.remove_address(label)
            print("Address deleted successfully.")

  
@input_error
def upcoming_birthdays(book: AddressBook) -> str:
    period = int(get_input("Enter period in days  to show birthdays"))
    return book.show_upcoming_birthdays(period)


@input_error
def remove_contact(book: AddressBook) -> str:
    name = get_input("Enter name of contact")
    book.delete(name)
    return "Contact removed"

@input_error
def show_contact(book: AddressBook) -> str:
    name = get_input("Enter name of contact")
    record = get_contact_from_book(name, book)
    return show_contact_table(record) 

@input_error
def find_contact(address_book: AddressBook) -> None:
    query = input("Enter search query: ")
    results = address_book.find_by_query(query)
    print(show_search_results_table(results, query))


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            data = pickle.load(f)
            if isinstance(data, AddressBook): #if saved data from our class
                return data
            else:
                print("Помилка читання збережених даних, створюмо нову книгу")
                return AddressBook()
    except Exception: 
        return AddressBook()
    
