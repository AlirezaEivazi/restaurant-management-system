import re
import random
import string
from backend.models.customer import Customer
from backend.models.admin import Admin
from backend.interfaces.repository_interfaces import IUserRepository
from backend.interfaces.notifier_interface import INotifierService


class AuthUseCase:
    """
    Handles authentication logic (register/login/password reset).
    """

    def __init__(self, user_repo: IUserRepository, notifier: INotifierService):
        self.user_repo = user_repo
        self.notifier = notifier

    def _validate_name(self, name: str) -> bool:
        return bool(re.fullmatch(r"[A-Za-zآ-ی\s]+", name))

    def _validate_email(self, email: str) -> bool:
        return bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email))

    def _validate_phone(self, phone: str) -> bool:
        return bool(re.fullmatch(r"(\+98|0)?9\d{9}", phone))

    def _validate_national_id(self, national_id: str) -> bool:
        return bool(re.fullmatch(r"\d{10}", national_id))

    def _validate_password(self, password: str) -> bool:
        """
        Password rules:
        - min 8 chars
        - at least 1 uppercase
        - at least 1 digit
        - at least 1 special char
        - must contain english letters
        """
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password):
            return False
        if not re.search(r"[a-zA-Z]", password):
            return False
        return True

    def register_customer(
        self,
        first_name: str,
        last_name: str,
        phone: str,
        email: str,
        national_id: str,
        password: str,
        password_repeat: str
    ) -> Customer:
        """
        Registers a new customer with full validation.
        """

        if not self._validate_name(first_name) or not self._validate_name(last_name):
            raise ValueError("نام و نام خانوادگی فقط باید شامل حروف باشد.")

        if not self._validate_phone(phone):
            raise ValueError("شماره تماس معتبر نیست.")

        if not self._validate_email(email):
            raise ValueError("ایمیل معتبر نیست.")

        if not self._validate_national_id(national_id):
            raise ValueError("کد ملی باید 10 رقم باشد.")

        if password != password_repeat:
            raise ValueError("رمز عبور و تکرار رمز عبور یکسان نیستند.")

        if not self._validate_password(password):
            raise ValueError("رمز عبور امن نیست (حداقل 8 کاراکتر، یک حرف بزرگ، یک عدد و یک کاراکتر خاص).")

        if self.user_repo.get_customer_by_email(email) is not None:
            raise ValueError("این ایمیل قبلاً ثبت شده است.")

        if self.user_repo.get_customer_by_national_id(national_id) is not None:
            raise ValueError("این کد ملی قبلاً ثبت شده است.")

        customer = Customer(first_name, last_name, phone, email, national_id, password)
        self.user_repo.add_customer(customer)
        return customer

    def login_customer(self, email: str, password: str) -> Customer:
        """
        Login customer with lockout after 3 failed attempts.
        """

        customer = self.user_repo.get_customer_by_email(email)
        if customer is None:
            raise ValueError("کاربری با این ایمیل وجود ندارد.")

        if customer.password != password:
            count = self.user_repo.increase_failed_login(email)
            if count >= 3:
                new_password = self._generate_random_password()
                self.user_repo.reset_failed_login(email)

                # reset password in db
                customer = self.user_repo.get_customer_by_email(email)
                customer._password = new_password  # internal update
                self.user_repo.update_customer(customer)

                self.notifier.send_password_reset(email, new_password)
                raise ValueError("ورود قفل شد! رمز جدید به ایمیل ارسال شد.")

            raise ValueError(f"رمز اشتباه است. تلاش {count}/3")

        self.user_repo.reset_failed_login(email)
        return customer

    def login_admin(self, personnel_id: str, password: str) -> Admin:
        """
        Admin login using personnel_id and password.
        """

        admin = self.user_repo.get_admin_by_personnel_id(personnel_id)
        if admin is None:
            raise ValueError("مدیری با این شماره پرسنلی وجود ندارد.")

        if admin.password != password:
            raise ValueError("رمز عبور مدیر اشتباه است.")

        return admin

    def _generate_random_password(self, length: int = 10) -> str:
        """
        Generates secure random password.
        """
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return "".join(random.choice(chars) for _ in range(length))
