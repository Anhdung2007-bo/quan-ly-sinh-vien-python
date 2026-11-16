from abc import ABC, abstractmethod


class Person(ABC):
    """Lớp trừu tượng đại diện cho con người trong hệ thống đào tạo."""

    def __init__(self, full_name: str, dob: str, gender: str, email: str, phone: str):
        self.full_name = full_name
        self.dob = dob
        self.gender = gender
        self.email = email
        self.phone = phone

    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, value: str):
        if not value or not value.strip():
            raise ValueError("Họ tên không được để trống.")
        self._full_name = value.strip()

    @property
    def dob(self) -> str:
        return self._dob

    @dob.setter
    def dob(self, value: str):
        self._dob = value.strip() if value else ""

    @property
    def gender(self) -> str:
        return self._gender

    @gender.setter
    def gender(self, value: str):
        self._gender = value.strip() if value else "Khác"

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if value and "@" not in value:
            raise ValueError("Địa chỉ email không hợp lệ.")
        self._email = value.strip() if value else ""

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str):
        self._phone = value.strip() if value else ""

    @abstractmethod
    def get_role(self) -> str:
        pass

    @abstractmethod
    def display_info(self) -> str:
        pass