from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Invalid phone number format.")
        super().__init__(value)

    @staticmethod
    def validate(value):
        return isinstance(value, str) and value.isdigit() and len(value) in [10, 12]  # Example for phone validation


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Record(name={self.name.value}, phones={self.phones}, birthday={self.birthday.value if self.birthday else None})"


class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_record(self, record):
        self.contacts.append(record)

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.contacts:
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)

                # If the birthday has already passed this year, move to next year
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                # Check if the birthday is within the next 7 days
                if today <= birthday_this_year <= today + timedelta(days=7):
                    # Check if the birthday falls on a weekend
                    if birthday_this_year.weekday() in [5, 6]:  # 5 = Saturday, 6 = Sunday
                        # Move to the next Monday
                        birthday_this_year += timedelta(days=(7 - birthday_this_year.weekday()))

                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": birthday_this_year.strftime("%Y.%m.%d")
                    })

        return upcoming_birthdays


# Приклад використання
book = AddressBook()
record1 = Record("John Doe")
record1.add_phone("1234567890")
record1.add_birthday("13.11.1985")
book.add_record(record1)

record2 = Record("Jane Smith")
record2.add_phone("0987654321")
record2.add_birthday("07.11.1990")
book.add_record(record2)

record3 = Record("Alice Johnson")
record3.add_phone("5555555555")
record3.add_birthday("18.11.1992")
book.add_record(record3)

record4 = Record("Bob Brown")
record4.add_phone("1112223333")
record4.add_birthday("12.11.1988")
book.add_record(record4)

# Отримуємо список привітань на найближчий тиждень
upcoming_birthdays = book.get_upcoming_birthdays()
print("Список привітань на цьому тижні:", upcoming_birthdays)