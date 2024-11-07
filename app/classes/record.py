"""Module providing record clas declaration for address book module."""

from app.classes.basic_classes import Name, Phone, Birthday, Email, Address

class Record:
    """Record Class responding for phone, birthday, email and address"""
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.addresses = {}

    def show_phones(self) -> str:
        """Show user phones"""
        return f"{self.name} телефони: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone: str) -> None:
        """Add phone to record"""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """Remove phone from record"""
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Edit phone in record"""
        phone = self.find_phone(old_phone)
        if phone:
            phone.update_number(new_phone)
            return
        raise ValueError("Не існує телефона який ви бажаєте змінити")

    def find_phone(self, phone: str) -> str:
        """Find phone in record"""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday: str) -> None:
        """Add birthday to record"""
        self.birthday = Birthday(birthday)

    def add_email(self, email: str) -> None:
        """Add email to record"""
        self.email = Email(email)

    def add_address(self, label: str, address: str) -> None:
        """Add an address to the record."""
        self.addresses[label] = Address(address, label)

    def remove_address(self, label: str) -> None:
        """Remove an address from the record by its label."""
        if label in self.addresses:
            del self.addresses[label]
        else:
            print(f"No address found with label '{label}'")

    def show_addresses(self) -> str:
        """Return a string representation of all addresses."""
        if not self.addresses:
            return "No addresses"
        return "\n".join(str(address) for address in self.addresses.values())

    def __str__(self):
        to_return = f"Контакт: {self.name.value}, телефони: {'; '.join(p.value for p in self.phones)}"
        if self.birthday:
            to_return += f", День народження: {self.birthday}"
        if self.email:
            to_return += f", Email: {self.email}"
        if self.addresses:
            to_return += f", Адреси: {self.show_addresses()}"
        return to_return
    
