from abc import ABC, abstractmethod


class INotifierService(ABC):
    """
    Interface for notification services (email/SMS).
    """

    @abstractmethod
    def send_password_reset(self, email: str, new_password: str) -> None:
        pass
