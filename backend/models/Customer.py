from .user import User

class Customer(User):
    def __init__(self, full_name, phone, email, password, national_id, address=""):
        super().__init__(full_name, phone, email, password)
        self._national_id = national_id
        self._address = address
        self._loyalty_points = 0

    @property
    def national_id(self): return self._national_id
    @national_id.setter
    def national_id(self, value): self._national_id = value

    @property
    def address(self): return self._address
    @address.setter
    def address(self, value): self._address = value

    @property
    def loyalty_points(self): return self._loyalty_points
    @loyalty_points.setter
    def loyalty_points(self, value): self._loyalty_points = value

    def get_role(self): return "Customer"