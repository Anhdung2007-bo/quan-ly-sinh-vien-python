# Phần mềm Quản lý Sinh viên và Kết quả Học tập

Đồ án môn học áp dụng **Lập trình hướng đối tượng (Python OOP)** kết hợp cơ sở dữ liệu **SQLite** và giao diện Web **Flask**.

## Tính năng chính
- **Quản lý danh mục:** Thêm, sửa, xóa, tìm kiếm Sinh viên, Lớp học, Giảng viên và Môn học.
- **Quản lý điểm & Xếp loại:** Nhập điểm thành phần (Chuyên cần 10%, Giữa kỳ 30%, Cuối kỳ 60%), tự động tính điểm trung bình và xếp loại học lực.
- **Bảng điểm cá nhân:** Tính điểm trung bình tích lũy (GPA) có trọng số tín chỉ cho từng sinh viên.
- **Thống kê học tập:** Thống kê tỷ lệ đạt/không đạt, phân bố xếp loại, danh sách khen thưởng và cảnh báo học vụ.

## Cấu trúc dự án (Kiến trúc 3 lớp)
- `models/`: Các lớp đối tượng OOP (`Person`, `Student`, `Teacher`, `Classroom`, `Course`, `Grade`).
- `database/`: Khởi tạo và quản lý kết nối SQLite (`db_manager.py`).
- `services/`: Xử lý nghiệp vụ, tính GPA và thống kê (`academic_service.py`).
- `templates/` & `app.py`: Giao diện Web và điều khiển máy chủ bằng Flask.

## Hướng dẫn cài đặt và chạy
1. Cài đặt thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
