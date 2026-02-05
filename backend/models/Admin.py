from .User import User

class Admin(User):
    def __init__(self, personnel_id, address):
        super().__init__("admin", "021-12345678", "admin@restaurant.com", "admin123")
        self._personnel_id = personnel_id
        self._address = address

    @property
    def personnel_id(self): return self._personnel_id
    @personnel_id.setter
    def personnel_id(self, value): self._personnel_id = value

    @property
    def address(self): return self._address
    @address.setter
    def address(self, value): self._address = value
    
    def get_role(self): return "Admin"