# BTTH OOP nâng cao: Rikkei HR Simulator Pro & Rikkei Academy LMS Simulator Pro

Hai bài thực hành tổng hợp về **Abstract Base Class, Kế thừa & `super()`, Đa kế thừa & MRO (kim cương), Đa hình, Duck Typing và Nạp chồng toán tử (`__add__`, `__lt__`)**, kèm `@property`, `@staticmethod`, `@classmethod`.

## Thứ tự bài tập

| STT | Bài tập | Kiến thức trọng tâm |
|---|---|---|
| 1 | [Hệ thống quản lý nhân sự Rikkei Education](bai-1-he-thong-quan-ly-nhan-su-rikkei-education/) | `BaseEmployee(ABC)` → `Lecturer` (phụ cấp ca dạy), `AdmissionStaff` (hoa hồng 5%); `HybridManager(Lecturer, AdmissionStaff)` dùng cooperative `super()`; cổng chi lương Duck Typing |
| 2 | [Hệ thống quản lý nội dung E-Learning Rikkei Education](bai-2-he-thong-quan-ly-noi-dung-e-learning-rikkei-education/) | `BaseLesson(ABC)` → `VideoLesson` (điểm theo thời lượng), `CodingChallenge` (điểm theo testcase); `HybridAssessment(VideoLesson, CodingChallenge)`; lưu trữ đám mây Duck Typing |

Mỗi thư mục bài có `main.py` (sơ đồ thiết kế lớp ở đầu file) và `README.md` riêng (đề bài, Design Document, mã nguồn, kết quả chạy thử, bảng kiểm thử).

## Cách chạy

Yêu cầu Python 3.9+, không cần thư viện ngoài.

```bash
cd bai-1-he-thong-quan-ly-nhan-su-rikkei-education && python main.py
cd ../bai-2-he-thong-quan-ly-noi-dung-e-learning-rikkei-education && python main.py
```
