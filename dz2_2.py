from collections import UserDict
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        self.value = value


class Phone(Field):
    def __init__(self, value):
        self.value = value

    def is_phone_number(self, value):
        self.value = value
        digits = re.findall(r"\d+", self.value)
        number = ""
        for digit in digits:
            number += digit
        if len(number) == len(self.value) and len(number) == 10:
            return True
        else:
            return False


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, number):
        self.phone = Phone(number)
        if self.phone.is_phone_number:
            self.phones.append(self.phone)

    def remove_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                self.phones.remove(phone)

    def edit_phone(self, old_number, new_number):
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = new_number

    def find_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                return number

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def __init__(self):
        self.data = UserDict()

    def add_record(self, record):
        self.data[record.name] = record

    def find(self, name):
        for key, val in self.data.items():
            if key.value == name:
                return val

    def delete(self, name):
        for key in self.data:
            if key.value == name:
                store = key
        self.data.pop(store)

    def __str__(self):
        s = ""
        for key in self.data:
            name = key
            value = self.data[key]
            phones = value.phones
            s += f"Contact name: {name.value}, phones: {'; '.join(p.value for p in phones)}\n"
        return s


# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі - два варіанти
print(book)
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")
print(book)
