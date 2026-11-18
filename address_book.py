from collections import UserDict
from datetime import datetime, timedelta


class Field:
    """Base class for record fields. Stores a value"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    

class Birthday(Field):
    def __init__(self, value):
        try:
            bd_date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(bd_date)
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Name(Field):
    """Required contact name"""
    pass


class Phone(Field):
    """Required phone number that must consist of 10 digits"""
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Record:
    """Class for the records (contacts)
    
    A record can have one name and multiple phone numbers"""
    def __init__(self, name, phone = None):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        if phone is not None:
            self.add_phone(phone)


    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        result = f"Contact name: {self.name.value}, phones: {phones}"
        if self.birthday:
            result += f", birthday: {self.birthday}"
        return result
    

    def add_phone(self, phone):
        """Add a phone unless the record already has it"""
        if not self.find_phone(phone):
            new_phone = Phone(phone)
            self.phones.append(new_phone)
        else:
            raise ValueError(f"Phone {phone} already exists.")
  

    def edit_phone(self, phone, new_phone):
        """Replace an existing phone with a new one"""
        phone_to_edit = self.find_phone(phone)
        if phone_to_edit:
            new = Phone(new_phone)
            self.phones[self.phones.index(phone_to_edit)] = new
        else:
            raise ValueError(f"Phone {phone} not found.")
            
  
    def remove_phone(self, phone):
        """Remove a phone from the record"""
        phone_to_delete = self.find_phone(phone)
        if phone_to_delete:
            self.phones.remove(phone_to_delete)
        else:
            raise ValueError(f"Phone {phone} not found.")


    def find_phone(self, phone):
        """Return the Phone object with the given phone number or None"""
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    

    def add_birthday(self, birthday):
        """Add a birthday to the record"""
        self.birthday = Birthday(birthday)


class AddressBook(UserDict):
    """Class that stores the records, key is a contact name"""
    @staticmethod
    def _change_birthday_year(date, year):
        """Return date moved to year (29 Feb becomes 28 Feb in non-leap years)"""
        try:
            return date.replace(year=year)
        except ValueError:
            return date.replace(year=year, day=28)


    def add_record(self, record):
        """Add a record to the book"""
        if record.name.value not in self.data:
            self.data[record.name.value] = record
        else:
            raise ValueError(f"Name {record.name.value} already exists.")
   

    def find(self, name):
        """Return the record with the given name or None"""
        return self.get(name) 

   
    def delete(self, name):
        """Delete the record with the given name

        If it doesn't exist, a message is printed"""
        del self.data[name] #KeyError if it doesn't exist


    def get_upcoming_birthdays(self):
        """Return the users whose birthday falls within the next 7 days (today included).

        Returns:
            A list of dicts with the keys - name and congratulation_date - ("DD.MM.YYYY").
            If a birthday falls on a weekend the congratulation date is moved
            to the following Monday. Contacts without a birthday are skipped
        """
        next_week_bd = []
        today = datetime.today().date()
        records = self.data.values()
        for record in records:
            if record.birthday is None:
                continue
            user_bd = record.birthday.value
            user_bd_thisyear = self._change_birthday_year(user_bd, today.year)
            if user_bd_thisyear < today:
                user_bd_thisyear = self._change_birthday_year(user_bd, today.year + 1)

            dif = (user_bd_thisyear - today).days
            if 0 <= dif <= 6:
                congratulation_date = user_bd_thisyear
                if congratulation_date.weekday() >= 5 :
                    congratulation_date +=  timedelta(days=(7 - congratulation_date.weekday()))


                next_week_bd.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                    })

        return next_week_bd
   

if __name__ == "__main__":
    pass