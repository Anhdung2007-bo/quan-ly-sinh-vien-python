from models.person import Person


class Teacher(Person):
    """Lớp Giảng viên kế thừa từ lớp Person."""

    def __init__(
        self,
        teacher_id: str,
        full_name: str,
        dob: str,
        gender: str,
        email: str,
        phone: str,
        department: str,
        degree: str,
    ):
        super().__init__(full_name, dob, gender, email, phone)
        self.teacher_id = teacher_id
        self.department = department
        self.degree = degree

    @property
    def teacher_id(self) -> str:
        return self._teacher_id

    @teacher_id.setter
    def teacher_id(self, value: str):
        if not value or not value.strip():
            raise ValueError("Mã giảng viên không được để trống.")
        self._teacher_id = value.strip().upper()

    def get_role(self) -> str:
        return "Giảng viên"

    def display_info(self) -> str:
        return (
            f"[{self.get_role()}] Mã GV: {self.teacher_id} | {self.degree}. {self.full_name} | "
            f"Khoa: {self.department} | Email: {self.email} | SĐT: {self.phone}"
        )