"""Module providing record clas declaration for address book module."""

from app.classes.basic_classes import Name, Phone, Birthday, Email, Address

class Record:
    """Record Class responding for phone, birthday, email and address"""
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

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
        pass

    def add_address(self, address_name: str, address: str) -> None:
        pass

    def remove_address(self, address_name: str) -> None:
        pass

    def edit_address(self, address_name: str, address: str) -> None:
        pass

    def __str__(self):
        to_return = f"Контакт: {self.name.value}, телефони: {'; '.join(p.value for p in self.phones)}"
        if self.birthday:
            to_return += f", День народження: {self.birthday}"
        return to_return
    
