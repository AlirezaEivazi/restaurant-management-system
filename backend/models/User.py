from abc import ABC, abstractmethod


class User(ABC):
    """
    Abstract base class for system users.
    """

    def __init__(self, first_name: str, last_name: str, phone: str, email: str, password: str):
        self._first_name = first_name
        self._last_name = last_name
        self._phone = phone
        self._email = email
        self._password = password

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def phone(self) -> str:
        return self._phone

    @property
    def email(self) -> str:
        return self._email

    @property
    def password(self) -> str:
        return self._password

    @abstractmethod
    def get_role(self) -> str:
        """
        Returns the role of the user (Customer/Admin).
        """
        pass
