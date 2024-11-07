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

    @staticmethod
    def __is_valid_number(number: str) -> str:
        pattern = r"^\+?\d{10,15}$"
        if re.match(pattern, number):
            return number
        raise ValueError(f"Invalid phone number: {number}. Phone number must include the country code and be between 10 and 15 digits.")


class Email(Field):
    """Class representing an email field"""

    def __init__(self, email: str):
        super().__init__(self.__is_valid_email(email))

    @staticmethod
    def __is_valid_email(email: str) -> str:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.match(pattern, email):
            return email
        raise ValueError(f"Invalid email address: {email}. Please provide a valid email format, e.g., example@domain.com.")


class Birthday(Field):
    """Class representing a birthday field"""

    def __init__(self, birthday: str):
        super().__init__(self.__is_valid_birthday(birthday))

    @staticmethod
    def __is_valid_birthday(birthday: str) -> str:
        try:
            date = datetime.strptime(birthday, "%Y-%m-%d")
            if date > datetime.now():
                raise ValueError(f"Birthday cannot be in the future: {birthday}")
            return birthday
        except ValueError:
            raise ValueError(f"Invalid birthday format: {birthday}. Expected format: YYYY-MM-DD")


class Address(Field):
    """Class representing an address field"""

    def __init__(self, address: str):
        super().__init__(self.__is_valid_address(address))

    @staticmethod
    def __is_valid_address(address: str) -> str:
        if len(address) > 5:
            return address
        raise ValueError(f"Invalid address: {address}. Address must be longer than 5 characters.")
