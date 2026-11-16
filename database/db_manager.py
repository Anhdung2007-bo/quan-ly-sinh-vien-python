import sqlite3


class DatabaseManager:
    """Quản lý kết nối SQLite, khởi tạo lược đồ bảng và dữ liệu mẫu."""

    def __init__(self, db_name: str = "student_management.db"):
        self.db_name = db_name
        self.init_database()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_database(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS classes (
                    class_id TEXT PRIMARY KEY,
                    class_name TEXT NOT NULL,
                    academic_year TEXT NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS teachers (
                    teacher_id TEXT PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    dob TEXT,
                    gender TEXT,
                    email TEXT,
                    phone TEXT,
                    department TEXT,
                    degree TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id TEXT PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    dob TEXT,
                    gender TEXT,
                    email TEXT,
                    phone TEXT,
                    class_id TEXT,
                    FOREIGN KEY (class_id) REFERENCES classes(class_id)
                        ON UPDATE CASCADE ON DELETE SET NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS courses (
                    course_id TEXT PRIMARY KEY,
                    course_name TEXT NOT NULL,
                    credits INTEGER NOT NULL CHECK(credits > 0),
                    teacher_id TEXT,
                    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
                        ON UPDATE CASCADE ON DELETE SET NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS grades (
                    student_id TEXT NOT NULL,
                    course_id TEXT NOT NULL,
                    attendance_score REAL NOT NULL CHECK(attendance_score BETWEEN 0 AND 10),
                    midterm_score REAL NOT NULL CHECK(midterm_score BETWEEN 0 AND 10),
                    final_score REAL NOT NULL CHECK(final_score BETWEEN 0 AND 10),
                    average_score REAL NOT NULL,
                    classification TEXT NOT NULL,
                    PRIMARY KEY (student_id, course_id),
                    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
                )
            """)
            conn.commit()

    def seed_sample_data_if_empty(self):
        """Tự động nạp dữ liệu mẫu nếu CSDL chưa có dữ liệu để dễ kiểm thử."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM classes")
            if cursor.fetchone()[0] > 0:
                return

            classes = [
                ("CNTT01", "Công nghệ thông tin 01", "2024-2028"),
                ("KTPM02", "Kỹ thuật phần mềm 02", "2024-2028"),
            ]
            cursor.executemany("INSERT INTO classes VALUES (?, ?, ?)", classes)

            teachers = [
                ("GV001", "Nguyễn Văn An", "1982-05-14", "Nam", "an.nv@university.edu.vn", "0901234567", "Công nghệ thông tin", "TS"),
                ("GV002", "Trần Thị Bích", "1987-09-22", "Nữ", "bich.tt@university.edu.vn", "0912345678", "Kỹ thuật phần mềm", "ThS"),
            ]
            cursor.executemany("INSERT INTO teachers VALUES (?, ?, ?, ?, ?, ?, ?, ?)", teachers)

            students = [
                ("SV001", "Lê Hoàng Nam", "2006-03-10", "Nam", "nam.lh@student.edu.vn", "0981112221", "CNTT01"),
                ("SV002", "Phạm Minh Anh", "2006-07-18", "Nữ", "anh.pm@student.edu.vn", "0981112222", "CNTT01"),
                ("SV003", "Đỗ Quốc Bảo", "2006-11-02", "Nam", "bao.dq@student.edu.vn", "0981112223", "CNTT01"),
                ("SV004", "Vũ Thảo Vy", "2006-01-25", "Nữ", "vy.vt@student.edu.vn", "0981112224", "KTPM02"),
                ("SV005", "Ngô Thanh Tùng", "2006-08-30", "Nam", "tung.nt@student.edu.vn", "0981112225", "KTPM02"),
            ]
            cursor.executemany("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?)", students)

            courses = [
                ("PY101", "Lập trình Python hướng đối tượng", 3, "GV001"),
                ("DB202", "Cơ sở dữ liệu", 3, "GV002"),
                ("SE301", "Phân tích và thiết kế hệ thống", 4, "GV002"),
            ]
            cursor.executemany("INSERT INTO courses VALUES (?, ?, ?, ?)", courses)

            sample_grades = [
                ("SV001", "PY101", 9.5, 8.5, 9.0),
                ("SV001", "DB202", 9.0, 8.0, 8.5),
                ("SV002", "PY101", 10.0, 9.5, 9.2),
                ("SV002", "DB202", 9.5, 9.0, 9.0),
                ("SV003", "PY101", 6.0, 4.5, 4.0),
                ("SV003", "DB202", 7.0, 5.5, 5.0),
                ("SV004", "PY101", 8.5, 7.5, 8.0),
                ("SV004", "SE301", 8.0, 7.0, 7.5),
                ("SV005", "PY101", 5.0, 4.0, 3.5),
                ("SV005", "SE301", 7.0, 6.0, 6.5),
            ]
            for sv_id, mh_id, cc, gk, ck in sample_grades:
                avg = round(cc * 0.1 + gk * 0.3 + ck * 0.6, 2)
                if avg >= 9.0:
                    rank = "Xuất sắc"
                elif avg >= 8.0:
                    rank = "Giỏi"
                elif avg >= 7.0:
                    rank = "Khá"
                elif avg >= 5.0:
                    rank = "Trung bình"
                else:
                    rank = "Yếu"
                cursor.execute(
                    "INSERT INTO grades VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (sv_id, mh_id, cc, gk, ck, avg, rank),
                )
            conn.commit()