"""Module providing basic classes declaration for address book module."""

from datetime import datetime
import re

class Field:
    """Basic Class representing field"""

    def __init__(self, value):
"""__init__ function."""
"""__init__ method."""
        self.value = value

    def __str__(self):
"""__str__ function."""
"""__str__ method."""
        return str(self.value)


class Name(Field):
    """Class representing a name field"""


class Phone(Field):
    """Class representing a phone field"""

    def __init__(self, number: str):
"""__init__ function."""
"""__init__ method."""
        super().__init__(self._is_valid_number(number))

    @staticmethod
    def _is_valid_number(number: str) -> str:
"""_is_valid_number function."""
"""_is_valid_number method."""
        if len(number) != 10 or not number.isdigit():
            raise ValueError("Невірний формат телефону. Має бути 10 цифр.")
        return number

    def update_number(self, new_value: str) -> None:
"""update_number function."""
"""update_number method."""
        self.value = self._is_valid_number(new_value)


class Email(Field):
    """Class representing an email field"""

    def __init__(self, email: str):
"""__init__ function."""
"""__init__ method."""
        super().__init__(self._is_valid_email(email))

    @staticmethod
    def _is_valid_email(email: str) -> str:
"""_is_valid_email function."""
"""_is_valid_email method."""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            raise ValueError("Невірний формат електронної пошти.")
        return email


class Birthday(Field):
    """Class representing a birthday field"""

    def __init__(self, date: str):
"""__init__ function."""
"""__init__ method."""
        super().__init__(self._is_valid_birthday(date))

    @staticmethod
    def _is_valid_birthday(birthday: str) -> datetime.date:
"""_is_valid_birthday function."""
"""_is_valid_birthday method."""
        try:
            return datetime.strptime(birthday, "%d.%m.%Y").date()
        except ValueError as e:
            raise ValueError("Невірний формат дати народження. Використовуйте формат DD.MM.YYYY.") from e

    def __str__(self):
"""__str__ function."""
"""__str__ method."""
        return f"{self.value.strftime('%d.%m.%Y')}"


class Address:
    """Class representing an address field"""
    
    def __init__(self, label: str, address: str):
"""__init__ function."""
"""__init__ method."""
        self.label = label
        self.address = address

    def __str__(self):
"""__str__ function."""
"""__str__ method."""
        return f"{self.label}: {self.address}"
