import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from database.db_manager import DatabaseManager
from services.academic_service import AcademicService
from models.classroom import Classroom
from models.teacher import Teacher
from models.student import Student
from models.course import Course
from models.grade import Grade

app = Flask(__name__)
app.secret_key = "student_management_oop_secret_key"

# Khởi tạo CSDL và tầng nghiệp vụ OOP
db_manager = DatabaseManager("student_management.db")
db_manager.seed_sample_data_if_empty()
service = AcademicService(db_manager)


@app.route("/")
def index():
    active_tab = request.args.get("tab", "stats")
    keyword = request.args.get("keyword", "").strip()
    stat_course = request.args.get("stat_course", "").strip()
    transcript_sid = request.args.get("transcript_sid", "").strip()

    classrooms = service.get_all_classrooms()
    teachers = service.get_all_teachers()
    students = service.get_all_students(keyword)
    all_students = service.get_all_students()
    courses = service.get_all_courses()
    grades = service.get_grades()
    stats = service.get_statistics(stat_course)

    # Mặc định chọn sinh viên đầu tiên nếu chưa chọn khi xem bảng điểm cá nhân
    if not transcript_sid and all_students:
        transcript_sid = all_students[0].student_id
    transcript = service.calculate_student_gpa(transcript_sid) if transcript_sid else None

    return render_template(
        "index.html",
        active_tab=active_tab,
        keyword=keyword,
        stat_course=stat_course,
        transcript_sid=transcript_sid,
        classrooms=classrooms,
        teachers=teachers,
        students=students,
        all_students=all_students,
        courses=courses,
        grades=grades,
        stats=stats,
        transcript=transcript,
    )


# ==================== ROUTES: SINH VIÊN ====================
@app.route("/students/add", methods=["POST"])
def add_student():
    try:
        student = Student(
            student_id=request.form["student_id"],
            full_name=request.form["full_name"],
            dob=request.form.get("dob", ""),
            gender=request.form.get("gender", "Nam"),
            email=request.form.get("email", ""),
            phone=request.form.get("phone", ""),
            class_id=request.form.get("class_id", ""),
        )
        service.add_student(student)
        flash(f"Đã thêm sinh viên {student.full_name} ({student.student_id})!", "success")
    except ValueError as e:
        flash(f"Lỗi dữ liệu: {e}", "danger")
    except sqlite3.IntegrityError:
        flash("Lỗi: Mã sinh viên đã tồn tại hoặc mã lớp không hợp lệ!", "danger")
    return redirect(url_for("index", tab="students"))


@app.route("/students/update", methods=["POST"])
def update_student():
    try:
        student = Student(
            student_id=request.form["student_id"],
            full_name=request.form["full_name"],
            dob=request.form.get("dob", ""),
            gender=request.form.get("gender", "Nam"),
            email=request.form.get("email", ""),
            phone=request.form.get("phone", ""),
            class_id=request.form.get("class_id", ""),
        )
        service.update_student(student)
        flash(f"Đã cập nhật thông tin sinh viên {student.student_id}!", "success")
    except ValueError as e:
        flash(f"Lỗi dữ liệu: {e}", "danger")
    return redirect(url_for("index", tab="students"))


@app.route("/students/delete/<student_id>", methods=["POST"])
def delete_student(student_id):
    service.delete_student(student_id)
    flash(f"Đã xóa sinh viên {student_id}!", "warning")
    return redirect(url_for("index", tab="students"))


# ==================== ROUTES: ĐIỂM & XẾP LOẠI ====================
@app.route("/grades/save", methods=["POST"])
def save_grade():
    try:
        grade = Grade(
            student_id=request.form["student_id"],
            course_id=request.form["course_id"],
            attendance_score=float(request.form["attendance_score"]),
            midterm_score=float(request.form["midterm_score"]),
            final_score=float(request.form["final_score"]),
        )
        service.save_grade(grade)
        flash(
            f"Đã lưu điểm ({grade.student_id} - {grade.course_id}): "
            f"ĐTB = {grade.average_score} | Xếp loại: {grade.classification}",
            "success",
        )
    except ValueError as e:
        flash(f"Lỗi nhập điểm: {e}", "danger")
    except sqlite3.IntegrityError:
        flash("Lỗi: Sinh viên hoặc môn học không tồn tại!", "danger")
    return redirect(url_for("index", tab="grades"))


@app.route("/grades/delete/<student_id>/<course_id>", methods=["POST"])
def delete_grade(student_id, course_id):
    with db_manager.get_connection() as conn:
        conn.execute(
            "DELETE FROM grades WHERE student_id = ? AND course_id = ?",
            (student_id.upper(), course_id.upper()),
        )
        conn.commit()
    flash(f"Đã xóa điểm môn {course_id} của sinh viên {student_id}!", "warning")
    return redirect(url_for("index", tab="grades"))


# ==================== ROUTES: LỚP HỌC, GIẢNG VIÊN, MÔN HỌC ====================
@app.route("/classes/add", methods=["POST"])
def add_classroom():
    try:
        classroom = Classroom(
            class_id=request.form["class_id"],
            class_name=request.form["class_name"],
            academic_year=request.form["academic_year"],
        )
        service.add_classroom(classroom)
        flash(f"Đã thêm lớp {classroom.class_name}!", "success")
    except ValueError as e:
        flash(f"Lỗi dữ liệu: {e}", "danger")
    except sqlite3.IntegrityError:
        flash("Lỗi: Mã lớp đã tồn tại!", "danger")
    return redirect(url_for("index", tab="academic"))


@app.route("/classes/delete/<class_id>", methods=["POST"])
def delete_classroom(class_id):
    service.delete_classroom(class_id)
    flash(f"Đã xóa lớp {class_id}!", "warning")
    return redirect(url_for("index", tab="academic"))


@app.route("/teachers/add", methods=["POST"])
def add_teacher():
    try:
        teacher = Teacher(
            teacher_id=request.form["teacher_id"],
            full_name=request.form["full_name"],
            dob=request.form.get("dob", ""),
            gender=request.form.get("gender", "Nam"),
            email=request.form.get("email", ""),
            phone=request.form.get("phone", ""),
            department=request.form.get("department", ""),
            degree=request.form.get("degree", "ThS"),
        )
        service.add_teacher(teacher)
        flash(f"Đã thêm giảng viên {teacher.full_name}!", "success")
    except ValueError as e:
        flash(f"Lỗi dữ liệu: {e}", "danger")
    except sqlite3.IntegrityError:
        flash("Lỗi: Mã giảng viên đã tồn tại!", "danger")
    return redirect(url_for("index", tab="academic"))


@app.route("/teachers/delete/<teacher_id>", methods=["POST"])
def delete_teacher(teacher_id):
    service.delete_teacher(teacher_id)
    flash(f"Đã xóa giảng viên {teacher_id}!", "warning")
    return redirect(url_for("index", tab="academic"))


@app.route("/courses/add", methods=["POST"])
def add_course():
    try:
        tid = request.form.get("teacher_id", "").strip() or None
        course = Course(
            course_id=request.form["course_id"],
            course_name=request.form["course_name"],
            credits=int(request.form["credits"]),
            teacher_id=tid,
        )
        service.add_course(course)
        flash(f"Đã thêm môn học {course.course_name}!", "success")
    except ValueError as e:
        flash(f"Lỗi dữ liệu: {e}", "danger")
    except sqlite3.IntegrityError:
        flash("Lỗi: Mã môn học đã tồn tại!", "danger")
    return redirect(url_for("index", tab="academic"))


@app.route("/courses/delete/<course_id>", methods=["POST"])
def delete_course(course_id):
    service.delete_course(course_id)
    flash(f"Đã xóa môn học {course_id}!", "warning")
    return redirect(url_for("index", tab="academic"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)