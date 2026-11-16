class Grade:
    """Lớp quản lý Điểm số, tính điểm trung bình và xếp loại học lực."""

    def __init__(
        self,
        student_id: str,
        course_id: str,
        attendance_score: float,
        midterm_score: float,
        final_score: float,
        student_name: str = "",
        course_name: str = "",
        credits: int = 0,
    ):
        self.student_id = student_id.strip().upper()
        self.course_id = course_id.strip().upper()
        self.attendance_score = attendance_score
        self.midterm_score = midterm_score
        self.final_score = final_score
        self.student_name = student_name
        self.course_name = course_name
        self.credits = credits

    @staticmethod
    def _validate_score(score: float, label: str) -> float:
        try:
            val = float(score)
        except (TypeError, ValueError):
            raise ValueError(f"{label} phải là một số thực.")
        if val < 0.0 or val > 10.0:
            raise ValueError(f"{label} phải nằm trong khoảng từ 0.0 đến 10.0.")
        return round(val, 2)

    @property
    def attendance_score(self) -> float:
        return self._attendance_score

    @attendance_score.setter
    def attendance_score(self, value: float):
        self._attendance_score = self._validate_score(value, "Điểm chuyên cần")

    @property
    def midterm_score(self) -> float:
        return self._midterm_score

    @midterm_score.setter
    def midterm_score(self, value: float):
        self._midterm_score = self._validate_score(value, "Điểm giữa kỳ")

    @property
    def final_score(self) -> float:
        return self._final_score

    @final_score.setter
    def final_score(self, value: float):
        self._final_score = self._validate_score(value, "Điểm cuối kỳ")

    @property
    def average_score(self) -> float:
        """Tính điểm trung bình theo trọng số: 10% CC + 30% GK + 60% CK."""
        avg = (
            self._attendance_score * 0.1
            + self._midterm_score * 0.3
            + self._final_score * 0.6
        )
        return round(avg, 2)

    @property
    def classification(self) -> str:
        """Xếp loại học lực dựa trên điểm trung bình."""
        avg = self.average_score
        if avg >= 9.0:
            return "Xuất sắc"
        elif avg >= 8.0:
            return "Giỏi"
        elif avg >= 7.0:
            return "Khá"
        elif avg >= 5.0:
            return "Trung bình"
        else:
            return "Yếu"