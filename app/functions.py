from functools import wraps
import pickle
from app.classes.address_book import AddressBook
from app.classes.record import Record

class ChangeUserContactError(Exception):
    pass


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError: 
            return("No such user")
        except IndexError: 
            return("Contact not found")
        except ValueError as e:
            return(f"{e}")
        except ChangeUserContactError as e:
            return(f"{e}")
    return inner

def get_input(prompt: str) -> str:
    """Отримує ввід користувача для заданого запиту."""
    value = input(f"{prompt}: ").strip()
    if value == '':
        raise ValueError("Please input something")
    return value



def get_contact_from_book(name, book: AddressBook) -> Record:
    record = book.find(name)
    if not record:
        raise KeyError
    return record


@input_error
def add_contact(book: AddressBook) -> str:
    name = get_input("Enter name for contact")
    phone = get_input("Enter phone for contact")
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(book: AddressBook) -> str:
    name = get_input("Enter name of contact")
    record = get_contact_from_book(name, book)
    
    old_phone = get_input("Enter phone for contact")
    new_phone = get_input("Enter new phone number")
    record.edit_phone(old_phone, new_phone)
    return "Phone changed"
        

@input_error
def show_phone(book: AddressBook) -> str:
    name = get_input("Enter name of contact")
    record = get_contact_from_book(name, book)
    return record.show_phones()

@input_error
def add_birthday(book: AddressBook) -> str:
    name = get_input("Enter name of contact")
    record = get_contact_from_book(name, book)

    birthday = get_input("Enter birthday for contact")
    record.add_birthday(birthday)
    return "Birthday added"


@input_error
def show_birthday(book: AddressBook) -> str:
    name = get_input("Enter name of contact")
    record = get_contact_from_book(name, book)
    if not record.birthday:
        raise ValueError("Birthday for user is not set")
    return record.birthday

@input_error
def upcoming_birthdays(book: AddressBook) -> str:
    period = int(get_input("Enter period in days  to show birthdays"))
    return book.show_upcoming_birthdays(period)

@input_error
def add_email(book: AddressBook) -> str:
    name = get_input("Enter name of contact")
    record = get_contact_from_book(name, book)
    email = get_input("Enter email of contact")
    record.add_email(email)
    return "Email added"

@input_error
def add_address(book: AddressBook) -> str:
    name = get_input("Enter name of contact")
    record = get_contact_from_book(name, book)

    label = get_input("Enter label for address")
    address = get_input("Enter address")
    record.add_address(label, address)
    return "Address updated"

@input_error
def remove_address(book: AddressBook) -> str:
    name = get_input("Enter name of contact")
    record = get_contact_from_book(name, book)

    label = get_input("Enter label of address")
    record.remove_address(label)
    return "Address removed"

@input_error
def remove_contact(book: AddressBook) -> str:
    name = get_input("Enter name of contact")
    book.delete(name)
    return "Contact removed"



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