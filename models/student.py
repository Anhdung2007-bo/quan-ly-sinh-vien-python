from models.person import Person


class Student(Person):
    """Lớp Sinh viên kế thừa từ lớp Person."""

    def __init__(
        self,
        student_id: str,
        full_name: str,
        dob: str,
        gender: str,
        email: str,
        phone: str,
        class_id: str,
        class_name: str = "",
    ):
        super().__init__(full_name, dob, gender, email, phone)
        self.student_id = student_id
        self.class_id = class_id
        self.class_name = class_name

    @property
    def student_id(self) -> str:
        return self._student_id

    @student_id.setter
    def student_id(self, value: str):
        if not value or not value.strip():
            raise ValueError("Mã sinh viên không được để trống.")
        self._student_id = value.strip().upper()

    def get_role(self) -> str:
        return "Sinh viên"

    def display_info(self) -> str:
        lop = self.class_name if self.class_name else self.class_id
        return (
            f"[{self.get_role()}] Mã SV: {self.student_id} | Họ tên: {self.full_name} | "
            f"Ngày sinh: {self.dob} | Giới tính: {self.gender} | Lớp: {lop} | Email: {self.email}"
        )