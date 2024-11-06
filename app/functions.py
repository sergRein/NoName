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

def get_contact_from_book(name, book: AddressBook) -> Record:
    record = book.find(name)
    if not record:
        raise KeyError
    return record

@input_error
def add_contact(args, book: AddressBook) -> str:
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args
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
def change_contact(args, book: AddressBook) -> str:
    if len(args) != 3:
        raise ChangeUserContactError("Wrong number of arguments provide user old phone and new phone")
    
    name, old_phone, new_phone = args
    record = get_contact_from_book(name, book)
    record.edit_phone(old_phone, new_phone)
    return "Phone changed"
        

@input_error
def show_phone(args, book: AddressBook) -> str:
    if len(args) != 1:
        raise ValueError("Please priovide user name")
    
    name = args[0]
    record = get_contact_from_book(name, book)
    return record.show_phones()

@input_error
def add_birthday(args, book: AddressBook) -> str:
    if len(args) != 2:
        raise ValueError("Please priovide user name and birthday")
    
    name, birthday = args
    record = get_contact_from_book(name, book)
    record.add_birthday(birthday)
    return "Birthday added"


@input_error
def show_birthday(args, book: AddressBook) -> str:
    if len(args) != 1:
        raise ValueError("Please priovide user name")
    
    name = args[0]
    record = get_contact_from_book(name, book)
    if not record.birthday:
        raise ValueError("Birthday for user is not set")
    return record.birthday

@input_error
def upcoming_birthdays(args, book: AddressBook) -> str:
    if len(args) == 0:
        period = 'upcoming'
    elif len(args) == 1:
        period = args[0]
        if period not in ('next-week', 'next-month'):
            raise ValueError("Available arguments for time period is 'next-week' or 'next-month'")
    else:
        raise ValueError("Provide 0 or 1 arguments for upcoming birthdays: 0 arguments for next 7 days, 1 argument for desire time period")
    
    return book.show_upcoming_birthdays(period)


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