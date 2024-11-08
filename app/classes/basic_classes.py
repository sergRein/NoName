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
        super().__init__(self._is_valid_number(number))

    @staticmethod
    def _is_valid_number(number: str) -> str:
        if len(number) != 10 or not number.isdigit():
            raise ValueError("Невірний формат телефону. Має бути 10 цифр.")
        return number

    def update_number(self, new_value: str) -> None:
        self.value = self._is_valid_number(new_value)


class Email(Field):
    """Class representing an email field"""

    def __init__(self, email: str):
        super().__init__(self._is_valid_email(email))

    @staticmethod
    def _is_valid_email(email: str) -> str:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            raise ValueError("Невірний формат електронної пошти.")
        return email


class Birthday(Field):
    """Class representing a birthday field"""

    def __init__(self, date: str):
        super().__init__(self._is_valid_birthday(date))

    @staticmethod
    def _is_valid_birthday(birthday: str) -> datetime.date:
        try:
            return datetime.strptime(birthday, "%d.%m.%Y").date()
        except ValueError as e:
            raise ValueError("Невірний формат дати народження. Використовуйте формат DD.MM.YYYY.") from e

    def __str__(self):
        return f"{self.value.strftime('%d.%m.%Y')}"


class Address:
    """Class representing an address field"""
    
    def __init__(self, label: str, address: str):
        self.label = label
        self.address = address

    def __str__(self):
        return f"{self.label}: {self.address}"
