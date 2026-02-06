from backend.models.user import User


class Admin(User):
    """
    Admin user entity.
    Admin logs in with personnel_id + password.
    """

    def __init__(self, first_name: str, last_name: str, phone: str, email: str,
                 personnel_id: str, password: str):
        super().__init__(first_name, last_name, phone, email, password)
        self._personnel_id = personnel_id

    @property
    def personnel_id(self) -> str:
        return self._personnel_id

    def get_role(self) -> str:
        return "Admin"
