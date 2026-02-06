from backend.interfaces.notifier_interface import INotifierService


class EmailMockService(INotifierService):
    """
    Mock service for sending emails (prints in console).
    """

    def send_password_reset(self, email: str, new_password: str) -> None:
        print("===================================")
        print("MOCK EMAIL SERVICE")
        print(f"To: {email}")
        print("Subject: Password Reset")
        print(f"Your new password is: {new_password}")
        print("===================================")
