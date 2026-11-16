class Classroom:
    """Lớp quản lý thông tin Lớp học."""

    def __init__(self, class_id: str, class_name: str, academic_year: str):
        if not class_id or not class_id.strip():
            raise ValueError("Mã lớp không được để trống.")
        if not class_name or not class_name.strip():
            raise ValueError("Tên lớp không được để trống.")
        self.class_id = class_id.strip().upper()
        self.class_name = class_name.strip()
        self.academic_year = academic_year.strip()

    def __str__(self) -> str:
        return f"Mã lớp: {self.class_id} | Tên lớp: {self.class_name} | Niên khóa: {self.academic_year}"