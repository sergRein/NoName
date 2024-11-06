"""Module providing basic classes declaration for address book module."""

from datetime import datetime


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
    pass


class Address():
    """Provide address with its name (Ex. Home -> address 1, Work -> address 2)"""
    pass 


class Note():
    pass

class NoteTag():
    pass
