"""Module providing basic classes declaration for address book module."""

from datetime import datetime
import re

class Field:
    """Basic Class representing field"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Class representing a name field"""


class Phone(Field):
    """Class representing a phone field"""

    def __init__(self, number: str):
        super().__init__(self.__is_valid_number(number))

    def __is_valid_number(self, number: str) -> str:
        if len(number) != 10 or not number.isdigit():
            raise ValueError("Wrong phone number format. Must be 10 digits")
        return number

    def update_number(self, new_number: str) -> None:
        """Update phone number if correct"""
        self.value = self.__is_valid_number(new_number)


class Birthday(Field):
    """Class representing a birthday field"""

    def __init__(self, date: str):
        super().__init__(self.__is_valid_birthday(date))

    def __is_valid_birthday(self, birthday: str) -> datetime.date:
        """Validate and return a birthday date."""
        try:
            return datetime.strptime(birthday, "%d.%m.%Y").date()
        except ValueError as e:
            raise ValueError("Invalid date format for birthday. Use DD.MM.YYYY") from e

    def __str__(self):
        return f"{self.value.strftime('%d.%m.%Y')}"
    

class Email():
    """Class representing a email field"""
    def __init__(self, email: str):
        super().__init__(self.__is_valid_email(email))

    def __is_valid_email(self, email: str) -> str:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            raise ValueError("Wrong email format.")
        return email


class Address():
    """Class representing an address field with a name and address details."""
    
    def __init__(self, address: str, label: str = "дім"):
        self.label = label or "Дім"
        self.address = address

    def __str__(self):
        return f"{self.label}: {self.address}"


class Note():
    pass

class NoteTag():
    pass
