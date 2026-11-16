class Course:
    """Lớp quản lý thông tin Môn học."""

    def __init__(
        self,
        course_id: str,
        course_name: str,
        credits: int,
        teacher_id: str = None,
        teacher_name: str = "",
    ):
        if not course_id or not course_id.strip():
            raise ValueError("Mã môn học không được để trống.")
        if not course_name or not course_name.strip():
            raise ValueError("Tên môn học không được để trống.")
        if credits <= 0:
            raise ValueError("Số tín chỉ phải lớn hơn 0.")

        self.course_id = course_id.strip().upper()
        self.course_name = course_name.strip()
        self.credits = int(credits)
        self.teacher_id = teacher_id.strip().upper() if teacher_id else None
        self.teacher_name = teacher_name

    def __str__(self) -> str:
        gv = self.teacher_name if self.teacher_name else (self.teacher_id or "Chưa phân công")
        return (
            f"Mã MH: {self.course_id} | Tên môn: {self.course_name} | "
            f"Số TC: {self.credits} | Giảng viên: {gv}"
        )