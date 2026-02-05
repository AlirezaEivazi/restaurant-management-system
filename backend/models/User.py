from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, full_name, phone, email, password):
        self._full_name = full_name
        self._phone = phone
        self._email = email
        self._password = password

    @property
    def full_name(self): return self._full_name
    @full_name.setter
    def full_name(self, value): self._full_name = value

    @property
    def phone(self): return self._phone
    @phone.setter
    def phone(self, value): self._phone = value

    @property
    def email(self): return self._email
    @email.setter
    def email(self, value): self._email = value

    @property
    def password(self): return self._password
    @password.setter
    def password(self, value): self._password = value

    @abstractmethod
    def get_role(self): pass