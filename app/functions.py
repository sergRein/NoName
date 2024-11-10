from functools import wraps
import pickle
from app.classes.address_book import AddressBook
from app.classes.record import Record
from app.visualiser import (
    show_contact_table, error_out, show_search_results_table, 
    blue_input, blue_string
)
from app.classes.localization import trans


def input_error(func):
    """Function to wrap user input handle errors."""
    @wraps(func)
    def inner(*args, **kwargs):
        """Inner function."""
        try:
            return func(*args, **kwargs)
        except KeyError: 
            print(f"""{error_out('No such user in address book')}""")
        except IndexError: 
            print(f"""{error_out('Contact not found')}""")
        except ValueError as e:
            print(f"""{error_out(str(e))}""")
    return inner


def get_input(prompt: str, required=True) -> str:
    """Get user input for selected request."""
    value = blue_input(f"{prompt}").strip()
    if value == '' and required:
        print(f"""{error_out('Please input something')}""")
    return value


def get_contact_from_book(name, book: AddressBook) -> Record:
    """Function to find contact by name."""
    record = book.find(name)
    if not record:
        raise KeyError
    return record


@input_error
def add_contact(book: AddressBook) -> str:
    """Process adding contact functionality (saving info step by step)."""
    while True:
        name = get_input("Enter name for contact")
        if len(name) <= 3:
            print(f"""{error_out("Name must be more than 3 chars")}""")
            continue
        else:
            break
        
    record = book.find(name)
    if record:
        raise ValueError("Contact exists, you can edit it with edit command")

    # Ask for phone
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
            print(f"""{error_out(e)}""")
    
    # Ask for email
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
                print(f"""{error_out(e)}""")

    # Ask for birthday
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
                print(f"""{error_out(e)}""")

    # Ask for address
    addresses_finished = False
    while not addresses_finished:
        address_label = get_input("Enter address label (press Enter to finish adding addresses)", False)
        if not address_label:
            addresses_finished = True
        else:
            address = get_input("Enter address")
            record.add_address(address_label, address)

    print("Contact added successfully")
    return show_contact_table(record)


@input_error
def edit_contact(book: AddressBook, exit_edit_mode) -> str:
    """Contact edit functionality."""
    name = get_input("Enter name of contact")
    record = get_contact_from_book(name, book)
    
    print(f"""\n{blue_string('Current contact information')}""")
    print(show_contact_table(record))

    print(f"""{blue_string('Available options for updating contact')}""")
    print(f"""{blue_string("Use commands in the format 'add-field', 'change-field', or 'delete-field'.")}""")
    print(f"""{blue_string('Fields can be phone, email, birthday, address.')}""")
    print(f"""{blue_string('Type "done" to finish updating the contact.')}""")
    print(f"""{blue_string('Type "show" to show current contact.')}""")

    # Functions to use inside record to manipulate data
    change_actions = {
        "phone": modify_phone,
        "email": modify_email,
        "birthday": modify_birthday,
        "address": modify_address
    }

    # Loop to ask fields input
    while True:
        action = get_input("Choose an action (e.g., 'add-phone', 'change-address', 'done' to finish)").strip().lower()
        
        if action == 'done':
            print(f"""{blue_string("Finished updating contact")}""")
            exit_edit_mode()
            break

        if action == 'show':
            print(show_contact_table(record))
            continue

        # Split command for action and field to manipulate
        command_parts = action.split('-', maxsplit=1)
        if len(command_parts) != 2:
            print(f"""{error_out("Invalid format. Use 'add-field', 'change-field', or 'delete-field'.")}""")
            continue
        
        command, field = command_parts
        if command in ["add", "change", "delete"] and field in change_actions:
            # Call needed function
            change_actions[field](record, command)
        else:
            print(f"""{error_out("Invalid option. Please choose a valid action in the format 'add-field', 'change-field', or 'delete-field'.")}""")

    # Show updated contact
    print("\nUpdated contact information:")
    return show_contact_table(record)

def modify_phone(record, action):
    if action == "add":
        while True:
            try:
                new_phone = get_input("Enter new phone number")
                if not new_phone:
                    print(f"""{error_out("Phone number cannot be empty. Please enter a valid phone number.")}""")
                    continue
                record.add_phone(new_phone)
                print(f"""{blue_string("Phone added successfully.")}""")
                break
            except ValueError as e:
                print(f"""{error_out(str(e))}""")

    elif action == "change":
        while True:
            try:
                old_phone = get_input("Enter the phone number to update")
                if not old_phone:
                    print(f"""{error_out("Phone number cannot be empty. Please enter a valid phone number.")}""")
                    continue
                if not record.find_phone(old_phone):
                    print(f"""{error_out("The phone number '{old_phone}' does not exist.").replace('{old_phone}', old_phone)}""")
                    continue

                new_phone = get_input("Enter the new phone number")
                if not new_phone:
                    print(f"""{error_out("Phone number cannot be empty. Please enter a valid phone number.")}""")
                    continue
                record.edit_phone(old_phone, new_phone)
                print(f"""{blue_string("Phone updated successfully.")}""")
                break
            except ValueError as e:
                print(f"""{error_out(str(e))}""")

    elif action == "delete":
        while True:
            try:
                phone_to_delete = get_input("Enter the phone number to delete")
                if not phone_to_delete:
                    print(f"""{error_out("Phone number cannot be empty. Please enter a valid phone number.")}""")
                    continue
                record.remove_phone(phone_to_delete)
                print(f"""{blue_string("Phone deleted successfully.")}""")
                break
            except ValueError as e:
                print(f"""{error_out(str(e))}""")



def modify_email(record, action):
    if action == "add":
        if record.email:
            print(f"""{error_out("The email '{email}' already exists.").replace('{email}', record.email.value)}""")
        else:
            while True:
                try:
                    new_email = get_input("Enter new email")
                    if not new_email:
                        print(f"""{error_out("Email cannot be empty. Please enter a valid email.")}""")
                        continue
                    record.add_email(new_email)
                    print(f"""{blue_string("Email added successfully.")}""")
                    break
                except ValueError as e:
                    print(f"""{error_out(str(e))}""")

    elif action == "change":
        if not record.email:
            print(error_out("No email to update. Use 'add' to add a new email."))
        else:
            while True:
                try:
                    new_email = get_input("Enter the new email")
                    if not new_email:
                        print(f"""{error_out("Email cannot be empty. Please enter a valid email.")}""")
                        continue
                    record.add_email(new_email)
                    print(f"""{blue_string("Email updated successfully.")}""")
                    break
                except ValueError as e:
                    print(f"""{error_out(str(e))}""")

    elif action == "delete":
        if not record.email:
            print(error_out("No email to delete."))
        else:
            record.email = None
            print(f"""{blue_string("Email deleted successfully.")}""")


def modify_birthday(record, action):
    if action == "add":
        if record.birthday:
            print(f"""{error_out("The birthday '{birthday}' already exists.").replace('{birthday}', record.birthday.value.strftime('%d.%m.%Y'))}""")
        else:
            while True:
                try:
                    new_birthday = get_input("Enter new birthday (DD.MM.YYYY)")
                    if not new_birthday:
                        print(f"""{error_out("Birthday cannot be empty. Please enter a valid date.")}""")
                        continue
                    record.add_birthday(new_birthday)
                    print(f"""{blue_string("Birthday added successfully.")}""")
                    break
                except ValueError as e:
                    print(f"""{error_out(str(e))}""")

    elif action == "change":
        if not record.birthday:
            print(error_out("No birthday to update. Use 'add' to add a new birthday."))
        else:
            while True:
                try:
                    new_birthday = get_input("Enter the new birthday (DD.MM.YYYY)")
                    if not new_birthday:
                        print(f"""{error_out("Birthday cannot be empty. Please enter a valid date.")}""")
                        continue
                    record.add_birthday(new_birthday)
                    print(f"""{blue_string("Birthday updated successfully.")}""")
                    break
                except ValueError as e:
                    print(f"""{error_out(str(e))}""")

    elif action == "delete":
        if not record.birthday:
            print(error_out("No birthday to delete."))
        else:
            record.birthday = None
            print(f"""{blue_string("Birthday deleted successfully.")}""")


def modify_address(record, action):
    if action == "add":
        while True:
            try:
                label = get_input("Enter address label (e.g., 'Home', 'Work')")
                if not label:
                    print(f"""{error_out("Address label cannot be empty. Please enter a valid label.")}""")
                    continue
                if label in record.addresses:
                    print(f"""{error_out("Address with label '{label}' already exists.").replace('{label}', label)}""")
                else:
                    address = get_input("Enter new address")
                    if not address:
                        print(f"""{error_out("Address cannot be empty. Please enter a valid address.")}""")
                        continue
                    record.add_address(label, address)
                    print(f"""{blue_string("Address added successfully.")}""")
                break
            except ValueError as e:
                print(f"""{error_out(str(e))}""")

    elif action == "change":
        while True:
            try:
                label = get_input("Enter the address label to update")
                if not label:
                    print(f"""{error_out("Address label cannot be empty. Please enter a valid label.")}""")
                    continue
                if label not in record.addresses:
                    print(f"""{error_out("No address with label '{label}' exists.").replace('{label}', label)}""")
                else:
                    break

            except ValueError as e:
                print(f"""{error_out(str(e))}""")

        while True:
            try:
                new_address = get_input("Enter the new address")
                if not new_address:
                    print(f"""{error_out("Address cannot be empty. Please enter a valid address.")}""")
                    continue
                record.edit_address(label, new_address)
                print(f"""{blue_string("Address updated successfully.")}""")
                break
            except ValueError as e:
                print(f"""{error_out(str(e))}""")

    elif action == "delete":
        while True:
            try:
                label = get_input("Enter the address label to delete")
                if not label:
                    print(f"""{error_out("Address label cannot be empty. Please enter a valid label.")}""")
                    continue
                if label not in record.addresses:
                    print(f"""{error_out("No address with label '{label}' exists.").replace('{label}', label)}""")
                else:
                    record.remove_address(label)
                    print(f"""{blue_string("Address deleted successfully.")}""")
                break
            except ValueError as e:
                print(f"""{error_out(str(e))}""")




@input_error
def upcoming_birthdays(book: AddressBook) -> str:
    """Upcoming birthdays function."""
    period = int(get_input("Enter period in days to show birthdays"))
    return book.show_upcoming_birthdays(period)


@input_error
def remove_contact(book: AddressBook) -> str:
    """Remove contact function."""
    name = get_input("Enter name of contact")
    book.delete(name)
    return trans("Contact removed")


@input_error
def show_contact(book: AddressBook) -> str:
    """Show contact function."""
    name = get_input("Enter name of contact")
    record = get_contact_from_book(name, book)
    return show_contact_table(record)


@input_error
def find_contact(address_book: AddressBook) -> None:
    """Function to find data in record data."""
    query = input("Enter search query: ")
    results = address_book.find_by_query(query)
    print(show_search_results_table(results, query))


def save_data(book, filename="addressbook.pkl"):
    """Save address book to file."""
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    """Load address book from file."""
    try:
        with open(filename, "rb") as f:
            data = pickle.load(f)
            if isinstance(data, AddressBook):  # Check if loaded data is from AddressBook
                return data
            else:
                print(f"""{error_out("Error reading saved data")}""")
                return AddressBook()
    except Exception: 
        return AddressBook()
