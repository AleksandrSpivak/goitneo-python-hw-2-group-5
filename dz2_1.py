# one handler for all functions

import re


class WrongCommandError(Exception):
    pass


class ContactAlreadyExistsError(Exception):
    pass


class ContactDoesNotExistError(Exception):
    pass


class NotPhoneNumberError(Exception):
    pass


class ContactListIsEmptyError(Exception):
    pass


def is_phone_number(string):
    number = re.findall(r"\d+", string)
    if len(number[0]) == len(string):
        return True
    else:
        return False


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except WrongCommandError:
            return "Invalid command."
        except ContactAlreadyExistsError:
            return "Such contact already exists"
        except NotPhoneNumberError:
            return "Number should consist of digits"
        except ContactListIsEmptyError:
            return "Empty contact list"
        except (ContactDoesNotExistError, IndexError):
            return "Contact not found"
        except ValueError:
            return "Give me name and phone please."

    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    if cmd == "":
        raise WrongCommandError
    return cmd, *args


@input_error
def add_contact(args, contacts):
    name, phone = args
    if name in contacts:
        raise ContactAlreadyExistsError
    if not is_phone_number(phone):
        raise NotPhoneNumberError
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    name, phone = args
    if name not in contacts:
        raise ContactDoesNotExistError
    if not is_phone_number(phone):
        raise NotPhoneNumberError
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args, contacts):
    name = args[0]
    if name not in contacts:
        raise ContactDoesNotExistError
    return contacts[name]


@input_error
def show_all(contacts):
    if len(contacts) == 0:
        raise ContactListIsEmptyError
    all_contacts = ""
    for contact in contacts:
        all_contacts += f"{contact} {contacts[contact]}\n"
    return all_contacts[:-1]


def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
