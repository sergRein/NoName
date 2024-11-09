"""Module providing AddressBook class declaration."""

from collections import UserDict, defaultdict 
from datetime import datetime, timedelta
from app.classes.record import Record
   

class AddressBook(UserDict):
    """AddressBook class for all address book data"""

    def __init__(self):
"""__init__ function."""
"""__init__ method."""
        super().__init__()

    def __str__(self):
"""__str__ function."""
"""__str__ method."""
        if len(self.data) == 0:
            return "Записи відсутні"
        to_return = "Записи"
        for record in self.data.values():
            to_return += f"\n{record}"
        return to_return
    

    def add_record(self, record: Record) -> None:
"""add_record function."""
"""add_record method."""
        self.data[record.name.value] = record


    def find(self, name: str) -> str:
"""find function."""
"""find method."""
        if name in self.data:
            return self.data[name]
        
        return None

    def delete(self, name: str) -> None:
"""delete function."""
"""delete method."""
        if name not in self.data:
            raise KeyError(f"Record for name '{name}' not found")
        del self.data[name]

    def show_upcoming_birthdays(self, period = 7) -> str:
"""show_upcoming_birthdays function."""
"""show_upcoming_birthdays method."""
        today = datetime.today().date()
        congratulation_dict = defaultdict(list)
        date_start = today 
        date_end = date_start + timedelta(days=period-1)
    
        for username, user in self.data.items():
            if user.birthday:
                user_birthday = user.birthday.value.replace(year=today.year)
                user_birthday = user_birthday.replace(year=today.year + 1) if today > user_birthday else user_birthday
                
                if date_start <= user_birthday <= date_end:
                    day_label = f"{user_birthday.strftime('%A')} ({user_birthday.strftime('%d.%m.%Y')})"
                    congratulation_dict[day_label].append(username)


        output = ''
        for day, names in sorted(congratulation_dict.items()):
            output += f"{day}: {', '.join(names)}\n"
        
        output = "No birthdays for this period" if output == '' else output
        return output
    
    def find_by_query(self, query: str) -> str:
        """Search query data in any field"""
        query = query.lower()
        results = []

        for record in self.data.values():
            if query in record.name.value.lower():
                results.append(record)
                continue

            if record.email and query in record.email.value.lower():
                results.append(record)
                continue

            if any(query in phone.value for phone in record.phones):
                results.append(record)
                continue

            if any(query in address.address.lower() for address in record.addresses.values()):
                results.append(record)
                continue

            if record.birthday and query in record.birthday.__str__().lower():
                results.append(record)
                continue

        return results
