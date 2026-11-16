from typing import List, Dict, Optional
from database.db_manager import DatabaseManager
from models.classroom import Classroom
from models.teacher import Teacher
from models.student import Student
from models.course import Course
from models.grade import Grade


class AcademicService:
    """Lớp xử lý toàn bộ nghiệp vụ quản lý đào tạo, điểm số và thống kê."""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    # ==================== QUẢN LÝ LỚP HỌC ====================
    def add_classroom(self, classroom: Classroom):
        with self.db.get_connection() as conn:
            conn.execute(
                "INSERT INTO classes (class_id, class_name, academic_year) VALUES (?, ?, ?)",
                (classroom.class_id, classroom.class_name, classroom.academic_year),
            )
            conn.commit()

    def get_all_classrooms(self) -> List[Classroom]:
        with self.db.get_connection() as conn:
            rows = conn.execute("SELECT * FROM classes ORDER BY class_id").fetchall()
            return [Classroom(r["class_id"], r["class_name"], r["academic_year"]) for r in rows]

    def update_classroom(self, classroom: Classroom) -> bool:
        with self.db.get_connection() as conn:
            cur = conn.execute(
                "UPDATE classes SET class_name = ?, academic_year = ? WHERE class_id = ?",
                (classroom.class_name, classroom.academic_year, classroom.class_id),
            )
            conn.commit()
            return cur.rowcount > 0

    def delete_classroom(self, class_id: str) -> bool:
        with self.db.get_connection() as conn:
            cur = conn.execute("DELETE FROM classes WHERE class_id = ?", (class_id.upper(),))
            conn.commit()
            return cur.rowcount > 0

    # ==================== QUẢN LÝ GIẢNG VIÊN ====================
    def add_teacher(self, teacher: Teacher):
        with self.db.get_connection() as conn:
            conn.execute(
                """INSERT INTO teachers 
                   (teacher_id, full_name, dob, gender, email, phone, department, degree)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    teacher.teacher_id,
                    teacher.full_name,
                    teacher.dob,
                    teacher.gender,
                    teacher.email,
                    teacher.phone,
                    teacher.department,
                    teacher.degree,
                ),
            )
            conn.commit()

    def get_all_teachers(self) -> List[Teacher]:
        with self.db.get_connection() as conn:
            rows = conn.execute("SELECT * FROM teachers ORDER BY teacher_id").fetchall()
            return [
                Teacher(
                    r["teacher_id"],
                    r["full_name"],
                    r["dob"],
                    r["gender"],
                    r["email"],
                    r["phone"],
                    r["department"],
                    r["degree"],
                )
                for r in rows
            ]

    def delete_teacher(self, teacher_id: str) -> bool:
        with self.db.get_connection() as conn:
            cur = conn.execute("DELETE FROM teachers WHERE teacher_id = ?", (teacher_id.upper(),))
            conn.commit()
            return cur.rowcount > 0

    # ==================== QUẢN LÝ SINH VIÊN ====================
    def add_student(self, student: Student):
        with self.db.get_connection() as conn:
            conn.execute(
                """INSERT INTO students 
                   (student_id, full_name, dob, gender, email, phone, class_id)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    student.student_id,
                    student.full_name,
                    student.dob,
                    student.gender,
                    student.email,
                    student.phone,
                    student.class_id if student.class_id else None,
                ),
            )
            conn.commit()

    def get_all_students(self, keyword: str = "") -> List[Student]:
        with self.db.get_connection() as conn:
            if keyword:
                kw = f"%{keyword.strip()}%"
                rows = conn.execute(
                    """SELECT s.*, c.class_name FROM students s
                       LEFT JOIN classes c ON s.class_id = c.class_id
                       WHERE s.student_id LIKE ? OR s.full_name LIKE ? OR s.class_id LIKE ?
                       ORDER BY s.student_id""",
                    (kw, kw, kw),
                ).fetchall()
            else:
                rows = conn.execute(
                    """SELECT s.*, c.class_name FROM students s
                       LEFT JOIN classes c ON s.class_id = c.class_id
                       ORDER BY s.student_id"""
                ).fetchall()
            return [
                Student(
                    r["student_id"],
                    r["full_name"],
                    r["dob"],
                    r["gender"],
                    r["email"],
                    r["phone"],
                    r["class_id"] or "Chưa phân lớp",
                    r["class_name"] or "",
                )
                for r in rows
            ]

    def update_student(self, student: Student) -> bool:
        with self.db.get_connection() as conn:
            cur = conn.execute(
                """UPDATE students
                   SET full_name = ?, dob = ?, gender = ?, email = ?, phone = ?, class_id = ?
                   WHERE student_id = ?""",
                (
                    student.full_name,
                    student.dob,
                    student.gender,
                    student.email,
                    student.phone,
                    student.class_id if student.class_id else None,
                    student.student_id,
                ),
            )
            conn.commit()
            return cur.rowcount > 0

    def delete_student(self, student_id: str) -> bool:
        with self.db.get_connection() as conn:
            cur = conn.execute("DELETE FROM students WHERE student_id = ?", (student_id.upper(),))
            conn.commit()
            return cur.rowcount > 0

    # ==================== QUẢN LÝ MÔN HỌC ====================
    def add_course(self, course: Course):
        with self.db.get_connection() as conn:
            conn.execute(
                """INSERT INTO courses (course_id, course_name, credits, teacher_id)
                   VALUES (?, ?, ?, ?)""",
                (course.course_id, course.course_name, course.credits, course.teacher_id),
            )
            conn.commit()

    def get_all_courses(self) -> List[Course]:
        with self.db.get_connection() as conn:
            rows = conn.execute(
                """SELECT c.*, t.full_name AS teacher_name FROM courses c
                   LEFT JOIN teachers t ON c.teacher_id = t.teacher_id
                   ORDER BY c.course_id"""
            ).fetchall()
            return [
                Course(
                    r["course_id"],
                    r["course_name"],
                    r["credits"],
                    r["teacher_id"],
                    r["teacher_name"] or "",
                )
                for r in rows
            ]

    def update_course(self, course: Course) -> bool:
        with self.db.get_connection() as conn:
            cur = conn.execute(
                """UPDATE courses SET course_name = ?, credits = ?, teacher_id = ?
                   WHERE course_id = ?""",
                (course.course_name, course.credits, course.teacher_id, course.course_id),
            )
            conn.commit()
            return cur.rowcount > 0

    def delete_course(self, course_id: str) -> bool:
        with self.db.get_connection() as conn:
            cur = conn.execute("DELETE FROM courses WHERE course_id = ?", (course_id.upper(),))
            conn.commit()
            return cur.rowcount > 0

    # ==================== QUẢN LÝ ĐIỂM & XẾP LOẠI ====================
    def save_grade(self, grade: Grade):
        """Thêm mới hoặc cập nhật điểm môn học cho sinh viên."""
        with self.db.get_connection() as conn:
            conn.execute(
                """INSERT INTO grades 
                   (student_id, course_id, attendance_score, midterm_score, final_score, average_score, classification)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(student_id, course_id) DO UPDATE SET
                       attendance_score = excluded.attendance_score,
                       midterm_score = excluded.midterm_score,
                       final_score = excluded.final_score,
                       average_score = excluded.average_score,
                       classification = excluded.classification""",
                (
                    grade.student_id,
                    grade.course_id,
                    grade.attendance_score,
                    grade.midterm_score,
                    grade.final_score,
                    grade.average_score,
                    grade.classification,
                ),
            )
            conn.commit()

    def get_grades(self, student_id: str = "", course_id: str = "") -> List[Grade]:
        query = """
            SELECT g.*, s.full_name AS student_name, c.course_name, c.credits
            FROM grades g
            JOIN students s ON g.student_id = s.student_id
            JOIN courses c ON g.course_id = c.course_id
            WHERE 1=1
        """
        params = []
        if student_id:
            query += " AND g.student_id = ?"
            params.append(student_id.upper())
        if course_id:
            query += " AND g.course_id = ?"
            params.append(course_id.upper())
        query += " ORDER BY g.student_id, g.course_id"

        with self.db.get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            return [
                Grade(
                    r["student_id"],
                    r["course_id"],
                    r["attendance_score"],
                    r["midterm_score"],
                    r["final_score"],
                    r["student_name"],
                    r["course_name"],
                    r["credits"],
                )
                for r in rows
            ]

    def calculate_student_gpa(self, student_id: str) -> Optional[Dict]:
        """Tính điểm trung bình tích lũy có trọng số tín chỉ cho 1 sinh viên."""
        grades = self.get_grades(student_id=student_id)
        if not grades:
            return None
        total_credits = sum(g.credits for g in grades)
        weighted_sum = sum(g.average_score * g.credits for g in grades)
        gpa = round(weighted_sum / total_credits, 2) if total_credits > 0 else 0.0

        if gpa >= 9.0:
            rank = "Xuất sắc"
        elif gpa >= 8.0:
            rank = "Giỏi"
        elif gpa >= 7.0:
            rank = "Khá"
        elif gpa >= 5.0:
            rank = "Trung bình"
        else:
            rank = "Yếu (Cảnh báo học vụ)"

        return {
            "student_id": student_id.upper(),
            "student_name": grades[0].student_name,
            "total_courses": len(grades),
            "total_credits": total_credits,
            "gpa": gpa,
            "classification": rank,
            "grades": grades,
        }

    # ==================== THỐNG KÊ KẾT QUẢ HỌC TẬP ====================
    def get_statistics(self, course_id: str = "") -> Dict:
        grades = self.get_grades(course_id=course_id)
        total = len(grades)
        if total == 0:
            return {"total": 0}

        ranks = {"Xuất sắc": 0, "Giỏi": 0, "Khá": 0, "Trung bình": 0, "Yếu": 0}
        passed = 0
        for g in grades:
            ranks[g.classification] += 1
            if g.average_score >= 5.0:
                passed += 1

        failed = total - passed
        avg_all = round(sum(g.average_score for g in grades) / total, 2)
        highest = max(grades, key=lambda g: g.average_score)
        lowest = min(grades, key=lambda g: g.average_score)
        commendations = [g for g in grades if g.average_score >= 8.0]
        warnings = [g for g in grades if g.average_score < 5.0]

        return {
            "total": total,
            "avg_all": avg_all,
            "passed": passed,
            "pass_rate": round(passed * 100 / total, 2),
            "failed": failed,
            "fail_rate": round(failed * 100 / total, 2),
            "ranks": ranks,
            "highest": highest,
            "lowest": lowest,
            "commendations": commendations,
            "warnings": warnings,
        }