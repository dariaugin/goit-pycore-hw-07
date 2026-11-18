from functools import wraps
from address_book import AddressBook, Record


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            return str(error)
        except IndexError:
            return "Enter proper arguments for the command."
        except KeyError:
            return "Contact doesn't exist."
    return inner


def parse_input(user_input):
    """Split the input into a lowercase command and a list of arguments."""
    try:
        cmd, *args = user_input.split()
    except ValueError:  # empty input
        return "", []
    return cmd.lower(), args


@input_error
def add_contact(args, book):
    """Add a contact. 
    
    Format: add [name] [phone]
    """
    if len(args) != 2:
        raise IndexError   
    name, phone = args 
    record = book.find(name)
    if record is None:
        record = Record(name, phone)
        book.add_record(record)
        return "Contact added."
    record.add_phone(phone)
    return "Contact updated."


@input_error
def change_contact(args, book):
    """Change the phone of an existing contact.

    Format: change [name] [old phone] [new phone]
    """
    if len(args) != 3:
        raise IndexError 
    name, old_phone, new_phone = args
    book[name].edit_phone(old_phone, new_phone)  # KeyError if no contact
    return "Contact updated."
    

@input_error
def show_phone(args, book):
    """Return the phone of a contact.

    Format: phone [name]
    """
    if len(args) != 1:
        raise IndexError 
    name = args[0]
    return ", ".join(f"{phone.value}" for phone in book[name].phones)


@input_error
def show_all(args,book):
    """Returns all contacts

    Format: all
    """
    if not book:
        return "Empty contact book."
    
    return "\n".join(str(record) for record in book.values())


@input_error
def add_birthday(args, book):
    """Add a birthday to the contact book

    Format: add-birthday [name] [birthday]
    """   
    if len(args) != 2:
        raise IndexError 
    name, birthday= args
    book[name].add_birthday(birthday)
    return f"Birthday {birthday} for {name} was added"


@input_error
def show_birthday(args, book):
    """Show a birthday of a selected contact

    Format: show-birthday [name]
    """ 
    if len(args) != 1:
        raise IndexError 
    name = args[0]
    birthday = book[name].birthday
    if birthday is None:
        return f"{name} has no birthday set."
    return str(birthday)
 

@input_error
def birthdays(args,book):
    """Show birthdays for the next week

    Format: birthdays
    """  
    data = book.get_upcoming_birthdays()
    if not data:
        return "No birthdays in the next 7 days."
    return "Upcoming birthdays:\n"+"\n".join(f"{bd['name']} : {bd['congratulation_date']}" for bd in data)
        
    
def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

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
            print(show_all(args,contacts))
        elif command == "add-birthday":
            print(add_birthday(args,contacts))
        elif command == "show-birthday":
            print(show_birthday(args,contacts))
        elif command == "birthdays":
            print(birthdays(args,contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()