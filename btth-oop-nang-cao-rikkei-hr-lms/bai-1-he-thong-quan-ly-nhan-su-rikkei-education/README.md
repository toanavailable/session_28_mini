# Bài 1 - Hệ thống quản lý nhân sự Rikkei Education

## Bối cảnh & vấn đề

Rikkei Education đang mở rộng quy mô đào tạo với nhiều vị trí nhân sự khác nhau: **Giảng viên chuyên trách (Lecturer)**, **Nhân viên tuyển sinh (Admission Staff)** và vị trí đặc thù **Giảng viên kiêm Quản lý tuyển sinh (Hybrid Manager)**. Mỗi vị trí có cách tính lương, phụ cấp và chỉ số KPI riêng.

Nếu quản lý bằng các hàm rời rạc và chuỗi if-else theo loại nhân sự, mã nguồn tính lương sẽ trùng lặp, khó mở rộng khi có vị trí mới và dễ sai lệch quỹ lương; giờ công nếu bị chỉnh sửa tùy tiện sẽ gây thất thoát ngân sách.

Nhiệm vụ: xây dựng module "Rikkei HR Simulator Pro" áp dụng OOP nâng cao: lớp trừu tượng (ABC) và đóng gói giờ công, kế thừa và đa kế thừa (MRO), đa hình khi tính lương / cập nhật KPI, chi lương qua cổng ngân hàng bằng Duck Typing và nạp chồng toán tử để so sánh / gộp giờ công.

## Yêu cầu thiết kế lớp

| Hạng mục | Yêu cầu |
|---|---|
| Abstract Base Class `BaseEmployee` | Class Attributes `company_name = "Rikkei Education"`, `base_salary_rate = 3,000,000`; private `__working_hours` (khởi tạo 0); `@property working_hours` không có setter; `@abstractmethod calculate_salary(self)`, `update_kpi(self, progress)`; `__add__` cộng giờ công 2 nhân sự; `__lt__` so sánh giờ công |
| Subclass 1 `Lecturer` | Thêm `teaching_slots`; lương = lương giờ + `teaching_slots * 500,000`; `update_kpi` ghi nhận tỷ lệ hoàn thành KPI giảng dạy (%); đứng thêm 1 ca → +1 ca, +2 giờ làm việc |
| Subclass 2 `AdmissionStaff` | Thêm `revenue_generated`, `kpi_target`; lương = lương giờ + hoa hồng **5% doanh số**; `update_kpi` cộng dồn doanh số hợp đồng mới |
| Đa kế thừa `HybridManager` | Kế thừa `Lecturer` và `AdmissionStaff`, tuân thủ MRO; lương gồm cả phụ cấp ca dạy lẫn hoa hồng tuyển sinh |
| Static & Class Method | `@staticmethod validate_employee_code(code)`: đúng 10 ký tự, bắt đầu bằng `RKE`; `@classmethod update_base_salary_rate(cls, new_rate)`: đổi mức lương cơ sở toàn hệ thống |

## Yêu cầu nghiệp vụ (Menu)

```
===== RIKKEI EDUCATION HR SIMULATOR PRO =====
1. Tuyển dụng nhân sự mới (Chọn loại hợp đồng nhân sự)
2. Xem thông tin & Kiểm tra thứ tự kế thừa (MRO)
3. Ghi nhận công nhật & Cập nhật KPI (Tính đa hình)
4. Tổng hợp quỹ lương và ngân sách chi trả
5. Kiểm tra gộp giờ làm việc & So sánh hiệu suất (Overloading)
6. Giải ngân lương qua Cổng thanh toán đối tác (Duck Typing)
7. Thoát chương trình
==================================================
Chọn chức năng (1-7):
```

- **Chức năng 1 - Tuyển dụng:** Chọn loại (1: Lecturer, 2: Admission Staff, 3: Hybrid Manager); nhập mã, họ tên (tự IN HOA, xóa khoảng trắng thừa qua setter); Admission / Hybrid nhập thêm chỉ tiêu doanh số.
- **Chức năng 2 - Thông tin & MRO:** Chưa có nhân sự thì báo lỗi; có thì in thông tin theo loại và danh sách MRO.
- **Chức năng 3 - Công nhật & KPI (Đa hình):** 3 tác vụ: ghi nhận đứng lớp (chỉ Lecturer / Hybrid), cập nhật KPI (cùng gọi `update_kpi()` nhưng Lecturer nhận %, Admission / Hybrid cộng doanh số), chấm công giờ làm việc.
- **Chức năng 4 - Quỹ lương:** Gọi đa hình `calculate_salary()`, in lương cứng theo giờ, phần phụ cấp / hoa hồng và tổng lương.
- **Chức năng 5 - Gộp & So sánh:** Chọn nhân sự khác, dùng `<` (`__lt__`) và `+` (`__add__`) trên giờ công.
- **Chức năng 6 - Chi lương (Duck Typing):** `execute_payroll(payment_service, employee, amount)` chỉ cần đối tượng có `transfer_salary(employee, amount)`; có sẵn `VietcombankCorporateService`, `TechcombankCorporateService`.
- **Chức năng 7 - Thoát:** "Cảm ơn đã sử dụng hệ thống Quản lý Nhân sự Rikkei Education Pro!"

### Edge cases (bẫy dữ liệu nâng cao)

| Bẫy | Xử lý |
|---|---|
| Bẫy 1 - Khởi tạo lớp trừu tượng | `BaseEmployee()` → `TypeError` |
| Bẫy 2 - Số liệu hiệu suất không hợp lệ | Giờ công / KPI / doanh số ≤ 0 → "Số liệu cập nhật hiệu suất không được nhỏ hơn hoặc bằng 0" |
| Bẫy 3 - Sai kiểu khi Overloading | `__add__` / `__lt__` kiểm tra `isinstance(other, BaseEmployee)`, sai kiểu trả về `NotImplemented` → `TypeError` |
| Bẫy 4 - Cổng ngân hàng sai giao diện | Không có `transfer_salary` → bắt `AttributeError`: "Cổng dịch vụ ngân hàng doanh nghiệp không hợp lệ hoặc chưa được liên kết liên thông kỹ thuật" |

## (1) Phân tích và thiết kế giải pháp (Design Document)

| Lớp | Kế thừa | Thành phần chính | Vai trò |
|---|---|---|---|
| `BaseEmployee` | `ABC` | `company_name`, `base_salary_rate`, `__working_hours`, `@property working_hours`, `log_working_hours`, `base_pay`, `__add__`, `__lt__`, static / class method | Khung chuẩn, đóng gói giờ công |
| `Lecturer` | `BaseEmployee` | `teaching_slots`, `kpi_percent`, `conduct_class()`, lương + 500,000 / ca | Giảng viên |
| `AdmissionStaff` | `BaseEmployee` | `revenue_generated`, `kpi_target`, lương + 5% doanh số | Tuyển sinh |
| `HybridManager` | `Lecturer`, `AdmissionStaff` | không override `calculate_salary`; `update_kpi` dùng nhánh `AdmissionStaff` | Quản lý kiêm giảng dạy |
| `VietcombankCorporateService`, `TechcombankCorporateService` | (không) | `transfer_salary(employee, amount)` | Cổng chi lương Duck Typing |

**Vì sao HybridManager không cần viết lại calculate_salary?**

Mỗi lớp con viết `calculate_salary` theo kiểu **cooperative**: cộng phần của mình rồi gọi `super().calculate_salary()`. Với MRO `HybridManager → Lecturer → AdmissionStaff → BaseEmployee → ABC → object`, lời gọi đi qua `Lecturer` (+ phụ cấp ca dạy) → `AdmissionStaff` (+ 5% doanh số) → `BaseEmployee` (lương giờ). Nhờ vậy Hybrid tự có đủ ba phần mà không lặp code. `__init__` cũng dùng `super().__init__(**kwargs)` nên một lần khởi tạo đi qua đủ các lớp, `BaseEmployee.__init__` chỉ chạy đúng một lần (bài toán kim cương).

**KPI của Hybrid Manager đi theo nhánh nào?**

Theo MRO, `update_kpi` của `Lecturer` sẽ được tìm thấy trước. Vì vai trò quản lý tuyển sinh được đánh giá theo doanh số, `HybridManager.update_kpi` gọi `super(Lecturer, self).update_kpi(progress)` để bỏ qua `Lecturer` và dùng bản của lớp kế tiếp trong MRO (`AdmissionStaff`). Phần giảng dạy của Hybrid vẫn được ghi nhận qua `conduct_class()`.

**Vì sao giờ công không có setter?**

`__working_hours` bị name mangling thành `_BaseEmployee__working_hours`; `@property working_hours` chỉ đọc nên `emp.working_hours = 9999` gây `AttributeError`. Giờ công chỉ tăng qua `log_working_hours()` (có kiểm tra > 0) hoặc `conduct_class()` → chống chỉnh sửa công tùy tiện.

**Duck Typing giúp tích hợp ngân hàng mới thế nào?**

`execute_payroll()` chỉ gọi `payment_service.transfer_salary(employee, amount)`, không kiểm tra class. Ngân hàng mới (BIDV, MB...) chỉ cần một class có phương thức cùng tên là dùng được; đối tượng sai giao diện bị bắt `AttributeError` (Bẫy 4).

Thuật toán các phương thức chính:

```
Lecturer.calculate_salary():
    TRẢ VỀ super().calculate_salary() + teaching_slots * 500,000

AdmissionStaff.calculate_salary():
    TRẢ VỀ super().calculate_salary() + revenue_generated * 5%

BaseEmployee.calculate_salary():            # phần lõi (abstract có thân)
    TRẢ VỀ working_hours * base_salary_rate

HybridManager.update_kpi(progress):
    TRẢ VỀ super(Lecturer, self).update_kpi(progress)   # -> AdmissionStaff: cộng dồn doanh số

execute_payroll(service, employee, amount):
    THỬ service.transfer_salary(employee, amount)        # Duck Typing
    BẮT AttributeError → "Cổng dịch vụ ngân hàng doanh nghiệp không hợp lệ ..."
```

## (2) Triển khai code

File: [`main.py`](main.py)

```python
"""
====================================================================
RIKKEI HR SIMULATOR PRO - THIẾT KẾ LỚP
====================================================================
                      BaseEmployee (ABC)
     company_name, base_salary_rate | __working_hours (private)
     @property working_hours (không setter) | __add__ / __lt__
     @abstractmethod calculate_salary (phần lõi: lương giờ) / update_kpi
     @staticmethod validate_employee_code | @classmethod update_base_salary_rate
                 /                               \\
          Lecturer                          AdmissionStaff
     + teaching_slots, kpi_percent         + revenue_generated, kpi_target
     lương += slots * 500,000              lương += revenue * 5%
     conduct_class(): +1 ca, +2 giờ        update_kpi: cộng dồn doanh số
                 \\                               /
               HybridManager(Lecturer, AdmissionStaff)

MRO Hybrid: HybridManager -> Lecturer -> AdmissionStaff -> BaseEmployee -> ABC -> object
calculate_salary viết kiểu cooperative (mỗi lớp cộng phần của mình rồi gọi
super()) nên HybridManager tự có: lương giờ + phụ cấp ca dạy + hoa hồng 5%.
Cổng chi lương (Duck Typing): VietcombankCorporateService,
TechcombankCorporateService chỉ cần có transfer_salary(employee, amount).
====================================================================
"""

from abc import ABC, abstractmethod

SLOT_ALLOWANCE = 500_000          # phụ cấp mỗi ca dạy
HOURS_PER_CLASS = 2               # mỗi ca dạy cộng 2 giờ làm việc
COMMISSION_RATE = 0.05            # hoa hồng 5% doanh số
CODE_PREFIX = "RKE"
POSITIVE_ERROR = "Số liệu cập nhật hiệu suất không được nhỏ hơn hoặc bằng 0"
MENU_LINE = "=" * 50


def vnd(amount):
    """Định dạng tiền."""
    return f"{amount:,.0f} VND"


def num(value):
    """100.0 -> '100', 2.5 -> '2.5'."""
    return f"{value:,.2f}".rstrip("0").rstrip(".")


class BaseEmployee(ABC):
    """Lớp trừu tượng: khung chuẩn cho mọi nhân sự (không tạo object trực tiếp)."""

    company_name = "Rikkei Education"     # Class Attributes dùng chung
    base_salary_rate = 3_000_000          # mức lương cơ sở / giờ (theo đề)
    bonus_label = "Phụ cấp"
    kpi_prompt = "Nhập giá trị KPI: "

    def __init__(self, employee_code, full_name, **kwargs):
        """Kiểm tra mã, chuẩn hóa họ tên qua setter, giờ làm việc ban đầu = 0."""
        super().__init__(**kwargs)        # cooperative theo MRO
        if not BaseEmployee.validate_employee_code(employee_code):
            raise ValueError("Mã nhân sự không hợp lệ! Phải gồm đúng 10 ký tự và "
                             "bắt đầu bằng RKE.")
        self.__employee_code = employee_code
        self.__full_name = ""
        self.full_name = full_name
        self.__working_hours = 0          # private: _BaseEmployee__working_hours

    # ---------------- @property ----------------
    @property
    def employee_code(self):
        """Mã nhân sự (chỉ đọc)."""
        return self.__employee_code

    @property
    def working_hours(self):
        """Số giờ làm việc - chỉ đọc, KHÔNG setter (chống chỉnh sửa công)."""
        return self.__working_hours

    @property
    def full_name(self):
        """Họ tên."""
        return self.__full_name

    @full_name.setter
    def full_name(self, new_name):
        """IN HOA, xóa khoảng trắng thừa; rỗng thì ValueError."""
        normalized = " ".join(str(new_name).split()).upper()
        if not normalized:
            raise ValueError("Họ và tên không được để trống!")
        self.__full_name = normalized

    @staticmethod
    def _check_positive(value):
        """Bẫy 2: số liệu cập nhật phải > 0."""
        if value <= 0:
            raise ValueError(POSITIVE_ERROR)

    def log_working_hours(self, hours):
        """Chấm công: cộng giờ làm việc (cửa duy nhất thay đổi __working_hours)."""
        BaseEmployee._check_positive(hours)
        self.__working_hours += hours

    def base_pay(self):
        """Lương cứng theo giờ = working_hours * base_salary_rate."""
        return self.__working_hours * BaseEmployee.base_salary_rate

    # ---------------- @abstractmethod ----------------
    @abstractmethod
    def calculate_salary(self):
        """Phần lõi: lương giờ. Lớp con override, cộng phần riêng và gọi super()."""
        return self.base_pay()

    @abstractmethod
    def update_kpi(self, progress):
        """Cập nhật KPI - mỗi loại nhân sự xử lý khác nhau."""

    def employee_type(self):
        """Tên loại nhân sự (tên class)."""
        return type(self).__name__

    def info_lines(self):
        """Thông tin chung; lớp con bổ sung qua super()."""
        return [f"Loại nhân sự: {self.employee_type()}",
                f"Tổ chức: {BaseEmployee.company_name}",
                f"Mã nhân sự: {self.employee_code}",
                f"Họ và tên: {self.full_name}",
                f"Số giờ làm việc: {num(self.working_hours)} giờ"]

    # ---------------- Operator Overloading ----------------
    def __add__(self, other):
        """A + B -> tổng giờ làm việc (số); chỉ nhận BaseEmployee."""
        if not isinstance(other, BaseEmployee):
            return NotImplemented
        return self.working_hours + other.working_hours

    def __lt__(self, other):
        """A < B -> giờ công A ít hơn B."""
        if not isinstance(other, BaseEmployee):
            return NotImplemented
        return self.working_hours < other.working_hours

    # ---------------- Static / Class Method ----------------
    @staticmethod
    def validate_employee_code(employee_code):
        """Bắt đầu bằng 'RKE' và đúng 10 ký tự (VD: RKE1234567)."""
        return (isinstance(employee_code, str) and len(employee_code) == 10
                and employee_code.startswith(CODE_PREFIX))

    @classmethod
    def update_base_salary_rate(cls, new_rate):
        """Đổi mức lương cơ sở cho TOÀN BỘ nhân sự."""
        if new_rate <= 0:
            raise ValueError("Mức lương cơ sở phải lớn hơn 0!")
        BaseEmployee.base_salary_rate = new_rate


class Lecturer(BaseEmployee):
    """Giảng viên chuyên trách."""

    bonus_label = "Phụ cấp ca dạy"
    kpi_prompt = "Nhập tỷ lệ hoàn thành KPI (%): "

    def __init__(self, employee_code, full_name, teaching_slots=0, **kwargs):
        """Thêm số ca đã đứng lớp; super() cho phần còn lại."""
        super().__init__(employee_code=employee_code, full_name=full_name, **kwargs)
        self.teaching_slots = teaching_slots
        self.kpi_percent = 0

    def calculate_salary(self):
        """Lương = lương giờ + teaching_slots * 500,000."""
        return super().calculate_salary() + self.teaching_slots * SLOT_ALLOWANCE

    def update_kpi(self, progress):
        """Tỷ lệ hoàn thành khung chương trình / đánh giá học viên (0-100%)."""
        BaseEmployee._check_positive(progress)
        if progress > 100:
            raise ValueError("Tỷ lệ KPI không được vượt quá 100%")
        self.kpi_percent = progress
        return [f"Tỷ lệ hoàn thành KPI: Đạt {num(progress)}% KPI."]

    def conduct_class(self):
        """Đứng thêm 1 ca: +1 ca dạy, +2 giờ làm việc."""
        self.teaching_slots += 1
        self.log_working_hours(HOURS_PER_CLASS)

    def info_lines(self):
        """Bổ sung số ca, KPI."""
        return super().info_lines() + [f"Số ca đã dạy: {self.teaching_slots} ca",
                                       f"Tỷ lệ KPI giảng dạy: {num(self.kpi_percent)}%"]


class AdmissionStaff(BaseEmployee):
    """Nhân viên tuyển sinh."""

    bonus_label = "Hoa hồng tuyển sinh (5%)"
    kpi_prompt = "Nhập giá trị doanh số hợp đồng mới mang về: "

    def __init__(self, employee_code, full_name, kpi_target, **kwargs):
        """Thêm doanh số và chỉ tiêu doanh số bắt buộc."""
        super().__init__(employee_code=employee_code, full_name=full_name, **kwargs)
        BaseEmployee._check_positive(kpi_target)
        self.revenue_generated = 0
        self.kpi_target = kpi_target

    def calculate_salary(self):
        """Lương = lương giờ + revenue_generated * 5%."""
        return super().calculate_salary() + self.revenue_generated * COMMISSION_RATE

    def update_kpi(self, progress):
        """Cộng dồn doanh số mới mang về."""
        BaseEmployee._check_positive(progress)
        self.revenue_generated += progress
        rate = self.revenue_generated / self.kpi_target * 100
        return [f"Doanh số tích lũy mới: {vnd(self.revenue_generated)}.",
                f"Tiến độ chỉ tiêu: {num(round(rate, 1))}% / {vnd(self.kpi_target)}"]

    def info_lines(self):
        """Bổ sung doanh số."""
        return super().info_lines() + [f"Doanh số mang về: {vnd(self.revenue_generated)}",
                                       f"Chỉ tiêu doanh số: {vnd(self.kpi_target)}"]


class HybridManager(Lecturer, AdmissionStaff):
    """Giảng viên kiêm quản lý tuyển sinh (đa kế thừa)."""

    bonus_label = "Phụ cấp ca dạy + Hoa hồng tuyển sinh tích hợp"
    kpi_prompt = AdmissionStaff.kpi_prompt

    def __init__(self, employee_code, full_name, kpi_target):
        """Một lần super() khởi tạo Lecturer, AdmissionStaff, BaseEmployee theo MRO."""
        super().__init__(employee_code=employee_code, full_name=full_name,
                         kpi_target=kpi_target)

    # calculate_salary: KHÔNG override - Lecturer -> AdmissionStaff -> BaseEmployee

    def update_kpi(self, progress):
        """KPI của quản lý tuyển sinh: cộng dồn doanh số (bỏ qua bản của Lecturer)."""
        return super(Lecturer, self).update_kpi(progress)   # -> AdmissionStaff


# =====================================================================
# CỔNG CHI LƯƠNG (DUCK TYPING) - không kế thừa lớp nào
# =====================================================================
class VietcombankCorporateService:
    """Tài khoản doanh nghiệp Vietcombank."""

    def transfer_salary(self, employee, amount):
        """Giải ngân lương."""
        print("[Hệ thống VCB Corporate]: Đang kết nối tới cổng chi trả Rikkei...")


class TechcombankCorporateService:
    """Tài khoản doanh nghiệp Techcombank."""

    def transfer_salary(self, employee, amount):
        """Giải ngân lương."""
        print(f"[Techcombank Business]: Xác thực lệnh chi cho nhân sự "
              f"{employee.employee_code}...")


def execute_payroll(payment_service, employee, amount):
    """Không quan tâm ngân hàng nào, chỉ cần có transfer_salary()."""
    try:
        BaseEmployee._check_positive(amount)
        payment_service.transfer_salary(employee, amount)
    except AttributeError:
        print("Cổng dịch vụ ngân hàng doanh nghiệp không hợp lệ hoặc chưa được "
              "liên kết liên thông kỹ thuật")
        return False
    except ValueError as error:
        print(f"Giải ngân thất bại: {error}")
        return False
    print("Xác thực đối tác bằng Duck Typing thành công!")
    print(f"Ngân hàng đối tác đã giải ngân thành công số tiền: {vnd(amount)} tới "
          f"nhân sự {employee.employee_code}.")
    return True


# =====================================================================
# HÀM GIAO DIỆN
# =====================================================================
EMPLOYEE_TYPES = {"1": ("Lecturer (Giảng viên chuyên trách)", "Giảng viên"),
                  "2": ("Admission Staff (Nhân viên Tuyển sinh)", "Nhân viên Tuyển sinh"),
                  "3": ("Hybrid Manager (Quản lý kiêm Giảng dạy)", "Quản lý Hybrid")}


def parse_number(text):
    """'15,000,000' -> 15000000.0."""
    return float(text.strip().replace(",", ""))


def require_employee(current_employee):
    """Chưa có nhân sự thì báo lỗi."""
    if current_employee is None:
        print("Hệ thống chưa có thông tin nhân sự. "
              "Vui lòng tuyển dụng nhân sự ở Chức năng 1 trước.")
        return False
    return True


def find_employee(employees, employee_code):
    """Tìm nhân sự theo mã."""
    for employee in employees:
        if employee.employee_code == employee_code:
            return employee
    return None


def recruit(employees):
    """Chức năng 1: tuyển dụng theo loại hợp đồng."""
    print("--- CHỌN LOẠI NHÂN SỰ KHỞI TẠO ---")
    for key, (label, _) in EMPLOYEE_TYPES.items():
        print(f"{key}. {label}")
    kind = input("Chọn loại nhân sự (1-3): ").strip()
    if kind not in EMPLOYEE_TYPES:
        print("Loại nhân sự không hợp lệ!")
        return None
    code = input("Nhập mã nhân sự 10 ký tự: ").strip()
    if not BaseEmployee.validate_employee_code(code):
        print("Mã nhân sự không hợp lệ! Phải gồm đúng 10 ký tự và bắt đầu bằng RKE.")
        return None
    if find_employee(employees, code) is not None:
        print("Mã nhân sự đã tồn tại trong hệ thống!")
        return None
    name = input("Nhập họ và tên: ")
    try:
        if kind == "1":
            employee = Lecturer(code, name)
        else:
            target = parse_number(input("Nhập chỉ tiêu doanh số (VND): "))
            employee_class = AdmissionStaff if kind == "2" else HybridManager
            employee = employee_class(code, name, kpi_target=target)
    except ValueError as error:
        message = str(error)
        print(message if "could not convert" not in message else "Dữ liệu nhập không hợp lệ!")
        return None
    employees.append(employee)
    print(f"Tuyển dụng {EMPLOYEE_TYPES[kind][1]} thành công!")
    print(f"Tên nhân sự: {employee.full_name}")
    return employee


def show_info(employee):
    """Chức năng 2: thông tin (đa hình info_lines) + MRO."""
    print("--- THÔNG TIN NHÂN SỰ HIỆN TẠI ---")
    print("\n".join(employee.info_lines()))
    print("Thứ tự kế thừa (MRO): "
          + " -> ".join(cls.__name__ for cls in type(employee).__mro__))


def record_performance(employee):
    """Chức năng 3: đứng lớp / KPI (đa hình update_kpi) / chấm công."""
    print("--- GHI NHẬN CÔNG NHẬT & HIỆU SUẤT ---")
    print("1. Ghi nhận tham gia đứng lớp (Chỉ dành cho Giảng viên/Hybrid)")
    print("2. Cập nhật tiến độ KPI / Doanh số")
    print("3. Chấm công giờ làm việc")
    task = input("Chọn tác vụ (1-3): ").strip()
    try:
        if task == "1":
            if not isinstance(employee, Lecturer):
                print("Tác vụ đứng lớp chỉ dành cho Giảng viên / Hybrid Manager.")
                return
            employee.conduct_class()
            print("Ghi nhận thành công! Thầy/Cô đã hoàn thành thêm 1 ca dạy.")
            print(f"Số ca dạy hiện tại: {employee.teaching_slots} ca.")
            print(f"Số giờ làm việc tích lũy: +{HOURS_PER_CLASS} giờ "
                  f"(tổng {num(employee.working_hours)} giờ).")
        elif task == "2":
            lines = employee.update_kpi(parse_number(input(employee.kpi_prompt)))
            print("\nCập nhật KPI thành công!")
            print("\n".join(lines))
        elif task == "3":
            employee.log_working_hours(parse_number(input("Nhập số giờ công cần ghi nhận: ")))
            print(f"Chấm công thành công! Tổng giờ làm việc: "
                  f"{num(employee.working_hours)} giờ.")
        else:
            print("Tác vụ không hợp lệ!")
    except ValueError as error:
        message = str(error)
        print(message if "could not convert" not in message else "Giá trị phải là số!")


def show_payroll(employee):
    """Chức năng 4: gọi đa hình calculate_salary()."""
    print("--- CHI TIẾT QUỸ LƯƠNG NHÂN SỰ ---")
    total = employee.calculate_salary()
    base = employee.base_pay()
    print(f"Nhân sự: {employee.full_name} (Loại: {employee.employee_type()})")
    print(f"Mức lương cơ sở hệ thống: {vnd(BaseEmployee.base_salary_rate)}")
    print(f"Số giờ làm việc tích lũy: {num(employee.working_hours)} giờ")
    print(f"Lương cứng tính theo giờ: {vnd(base)}")
    print(f"{employee.bonus_label}: {vnd(total - base)}")
    print(f"Tổng lương thực nhận tháng này: {vnd(total)}")


def compare_employees(employees, employee):
    """Chức năng 5: toán tử < và +."""
    print("--- ĐỒNG BỘ & SO SÁNH GIỜ CÔNG (OPERATOR OVERLOADING) ---")
    others = [item for item in employees if item is not employee]
    if not others:
        print("Cần ít nhất 2 nhân sự trong hệ thống để so sánh / gộp!")
        return
    print(f"Nhân sự hiện tại (A): {employee.full_name} "
          f"(Giờ công: {num(employee.working_hours)} giờ)")
    print("Danh sách nhân sự khác:")
    for item in others:
        print(f"  - {item.employee_code} ({item.full_name} - Giờ công: "
              f"{num(item.working_hours)} giờ)")
    other = find_employee(others, input("Chọn nhân sự đối ứng (B), nhập mã: ").strip())
    if other is None:
        print("Không tìm thấy nhân sự đối ứng!")
        return
    if employee < other:
        result = "ÍT HƠN"
    elif other < employee:
        result = "NHIỀU HƠN"
    else:
        result = "BẰNG"
    print(f"[Kết quả So sánh (__lt__)]: Giờ công cống hiến của nhân sự A {result} "
          "nhân sự B.")
    print(f"[Kết quả Tổng hợp (__add__)]: Tổng số giờ làm việc của cả 2 nhân sự là: "
          f"{num(employee + other)} giờ.")


def pay_salary(employee):
    """Chức năng 6: giải ngân qua cổng đối tác (Duck Typing)."""
    print("--- CHI TRẢ LƯƠNG QUA CỔNG ĐỐI TÁC TRUNG GIAN ---")
    print("1. Chi trả qua tài khoản Doanh nghiệp Vietcombank")
    print("2. Chi trả qua tài khoản Doanh nghiệp Techcombank")
    choice = input("Chọn cổng ngân hàng (1-2): ").strip()
    service = {"1": VietcombankCorporateService(),
               "2": TechcombankCorporateService()}.get(choice, object())
    text = input("Nhập số tiền giải ngân (Enter = lương tháng này): ").strip()
    try:
        amount = parse_number(text) if text else employee.calculate_salary()
    except ValueError:
        print("Số tiền phải là số!")
        return
    execute_payroll(service, employee, amount)


def display_menu():
    """In menu chính."""
    print("\n===== RIKKEI EDUCATION HR SIMULATOR PRO =====")
    print("1. Tuyển dụng nhân sự mới (Chọn loại hợp đồng nhân sự)")
    print("2. Xem thông tin & Kiểm tra thứ tự kế thừa (MRO)")
    print("3. Ghi nhận công nhật & Cập nhật KPI (Tính đa hình)")
    print("4. Tổng hợp quỹ lương và ngân sách chi trả")
    print("5. Kiểm tra gộp giờ làm việc & So sánh hiệu suất (Overloading)")
    print("6. Giải ngân lương qua Cổng thanh toán đối tác (Duck Typing)")
    print("7. Thoát chương trình")
    print(MENU_LINE)


def main():
    """employees = [], current_employee = None; vòng lặp menu."""
    employees = []
    current_employee = None
    while True:
        display_menu()
        choice = input("Chọn chức năng (1-7): ").strip()
        if choice == "1":
            current_employee = recruit(employees) or current_employee
        elif choice in ("2", "3", "4", "5", "6") and not require_employee(current_employee):
            continue
        elif choice == "2":
            show_info(current_employee)
        elif choice == "3":
            record_performance(current_employee)
        elif choice == "4":
            show_payroll(current_employee)
        elif choice == "5":
            compare_employees(employees, current_employee)
        elif choice == "6":
            pay_salary(current_employee)
        elif choice == "7":
            print("Cảm ơn đã sử dụng hệ thống Quản lý Nhân sự Rikkei Education Pro!")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn từ 1-7!")


if __name__ == "__main__":
    main()
```

## Kết quả chạy thử

Kịch bản: xem thông tin khi chưa có nhân sự → mã RKE99 sai → tuyển Admission NGUYEN VAN AN (chỉ tiêu 100 triệu), chấm 180 giờ, doanh số 40 triệu, thử đứng lớp (bị chặn), xem lương → tuyển Lecturer TRAN THI LAN, chấm 40 giờ, đứng 1 ca, KPI 90%, KPI 150% (bị chặn), xem lương → tuyển Hybrid LE HOANG NAM, chấm 160 giờ, đứng 1 ca, doanh số 15 triệu, -500 (Bẫy 2), 50 triệu → thông tin + MRO → lương → so sánh / gộp với RKE0099999 → chi lương Vietcombank (Enter = lương tháng), Techcombank 12 triệu, cổng không tồn tại → menu sai → thoát. Khung menu lặp lại được ẩn.

```
Chọn chức năng (1-7): 2
Hệ thống chưa có thông tin nhân sự. Vui lòng tuyển dụng nhân sự ở Chức năng 1 trước.

Chọn chức năng (1-7): 1
--- CHỌN LOẠI NHÂN SỰ KHỞI TẠO ---
1. Lecturer (Giảng viên chuyên trách)
2. Admission Staff (Nhân viên Tuyển sinh)
3. Hybrid Manager (Quản lý kiêm Giảng dạy)
Chọn loại nhân sự (1-3): 3
Nhập mã nhân sự 10 ký tự: RKE99
Mã nhân sự không hợp lệ! Phải gồm đúng 10 ký tự và bắt đầu bằng RKE.

Chọn chức năng (1-7): 1
--- CHỌN LOẠI NHÂN SỰ KHỞI TẠO ---
1. Lecturer (Giảng viên chuyên trách)
2. Admission Staff (Nhân viên Tuyển sinh)
3. Hybrid Manager (Quản lý kiêm Giảng dạy)
Chọn loại nhân sự (1-3): 2
Nhập mã nhân sự 10 ký tự: RKE0099999
Nhập họ và tên: nguyen van an
Nhập chỉ tiêu doanh số (VND): 100,000,000
Tuyển dụng Nhân viên Tuyển sinh thành công!
Tên nhân sự: NGUYEN VAN AN

Chọn chức năng (1-7): 3
--- GHI NHẬN CÔNG NHẬT & HIỆU SUẤT ---
1. Ghi nhận tham gia đứng lớp (Chỉ dành cho Giảng viên/Hybrid)
2. Cập nhật tiến độ KPI / Doanh số
3. Chấm công giờ làm việc
Chọn tác vụ (1-3): 3
Nhập số giờ công cần ghi nhận: 180
Chấm công thành công! Tổng giờ làm việc: 180 giờ.

Chọn chức năng (1-7): 3
--- GHI NHẬN CÔNG NHẬT & HIỆU SUẤT ---
1. Ghi nhận tham gia đứng lớp (Chỉ dành cho Giảng viên/Hybrid)
2. Cập nhật tiến độ KPI / Doanh số
3. Chấm công giờ làm việc
Chọn tác vụ (1-3): 2
Nhập giá trị doanh số hợp đồng mới mang về: 40,000,000

Cập nhật KPI thành công!
Doanh số tích lũy mới: 40,000,000 VND.
Tiến độ chỉ tiêu: 40% / 100,000,000 VND

Chọn chức năng (1-7): 3
--- GHI NHẬN CÔNG NHẬT & HIỆU SUẤT ---
1. Ghi nhận tham gia đứng lớp (Chỉ dành cho Giảng viên/Hybrid)
2. Cập nhật tiến độ KPI / Doanh số
3. Chấm công giờ làm việc
Chọn tác vụ (1-3): 1
Tác vụ đứng lớp chỉ dành cho Giảng viên / Hybrid Manager.

Chọn chức năng (1-7): 4
--- CHI TIẾT QUỸ LƯƠNG NHÂN SỰ ---
Nhân sự: NGUYEN VAN AN (Loại: AdmissionStaff)
Mức lương cơ sở hệ thống: 3,000,000 VND
Số giờ làm việc tích lũy: 180 giờ
Lương cứng tính theo giờ: 540,000,000 VND
Hoa hồng tuyển sinh (5%): 2,000,000 VND
Tổng lương thực nhận tháng này: 542,000,000 VND

Chọn chức năng (1-7): 1
--- CHỌN LOẠI NHÂN SỰ KHỞI TẠO ---
1. Lecturer (Giảng viên chuyên trách)
2. Admission Staff (Nhân viên Tuyển sinh)
3. Hybrid Manager (Quản lý kiêm Giảng dạy)
Chọn loại nhân sự (1-3): 1
Nhập mã nhân sự 10 ký tự: RKE0055555
Nhập họ và tên: tran   thi lan
Tuyển dụng Giảng viên thành công!
Tên nhân sự: TRAN THI LAN

Chọn chức năng (1-7): 3
--- GHI NHẬN CÔNG NHẬT & HIỆU SUẤT ---
1. Ghi nhận tham gia đứng lớp (Chỉ dành cho Giảng viên/Hybrid)
2. Cập nhật tiến độ KPI / Doanh số
3. Chấm công giờ làm việc
Chọn tác vụ (1-3): 3
Nhập số giờ công cần ghi nhận: 40
Chấm công thành công! Tổng giờ làm việc: 40 giờ.

Chọn chức năng (1-7): 3
--- GHI NHẬN CÔNG NHẬT & HIỆU SUẤT ---
1. Ghi nhận tham gia đứng lớp (Chỉ dành cho Giảng viên/Hybrid)
2. Cập nhật tiến độ KPI / Doanh số
3. Chấm công giờ làm việc
Chọn tác vụ (1-3): 1
Ghi nhận thành công! Thầy/Cô đã hoàn thành thêm 1 ca dạy.
Số ca dạy hiện tại: 1 ca.
Số giờ làm việc tích lũy: +2 giờ (tổng 42 giờ).

Chọn chức năng (1-7): 3
--- GHI NHẬN CÔNG NHẬT & HIỆU SUẤT ---
1. Ghi nhận tham gia đứng lớp (Chỉ dành cho Giảng viên/Hybrid)
2. Cập nhật tiến độ KPI / Doanh số
3. Chấm công giờ làm việc
Chọn tác vụ (1-3): 2
Nhập tỷ lệ hoàn thành KPI (%): 90

Cập nhật KPI thành công!
Tỷ lệ hoàn thành KPI: Đạt 90% KPI.

Chọn chức năng (1-7): 3
--- GHI NHẬN CÔNG NHẬT & HIỆU SUẤT ---
1. Ghi nhận tham gia đứng lớp (Chỉ dành cho Giảng viên/Hybrid)
2. Cập nhật tiến độ KPI / Doanh số
3. Chấm công giờ làm việc
Chọn tác vụ (1-3): 2
Nhập tỷ lệ hoàn thành KPI (%): 150
Tỷ lệ KPI không được vượt quá 100%

Chọn chức năng (1-7): 4
--- CHI TIẾT QUỸ LƯƠNG NHÂN SỰ ---
Nhân sự: TRAN THI LAN (Loại: Lecturer)
Mức lương cơ sở hệ thống: 3,000,000 VND
Số giờ làm việc tích lũy: 42 giờ
Lương cứng tính theo giờ: 126,000,000 VND
Phụ cấp ca dạy: 500,000 VND
Tổng lương thực nhận tháng này: 126,500,000 VND

Chọn chức năng (1-7): 1
--- CHỌN LOẠI NHÂN SỰ KHỞI TẠO ---
1. Lecturer (Giảng viên chuyên trách)
2. Admission Staff (Nhân viên Tuyển sinh)
3. Hybrid Manager (Quản lý kiêm Giảng dạy)
Chọn loại nhân sự (1-3): 3
Nhập mã nhân sự 10 ký tự: RKE0012345
Nhập họ và tên:  le hoang nam
Nhập chỉ tiêu doanh số (VND): 100,000,000
Tuyển dụng Quản lý Hybrid thành công!
Tên nhân sự: LE HOANG NAM

Chọn chức năng (1-7): 3
--- GHI NHẬN CÔNG NHẬT & HIỆU SUẤT ---
1. Ghi nhận tham gia đứng lớp (Chỉ dành cho Giảng viên/Hybrid)
2. Cập nhật tiến độ KPI / Doanh số
3. Chấm công giờ làm việc
Chọn tác vụ (1-3): 3
Nhập số giờ công cần ghi nhận: 160
Chấm công thành công! Tổng giờ làm việc: 160 giờ.

Chọn chức năng (1-7): 3
--- GHI NHẬN CÔNG NHẬT & HIỆU SUẤT ---
1. Ghi nhận tham gia đứng lớp (Chỉ dành cho Giảng viên/Hybrid)
2. Cập nhật tiến độ KPI / Doanh số
3. Chấm công giờ làm việc
Chọn tác vụ (1-3): 1
Ghi nhận thành công! Thầy/Cô đã hoàn thành thêm 1 ca dạy.
Số ca dạy hiện tại: 1 ca.
Số giờ làm việc tích lũy: +2 giờ (tổng 162 giờ).

Chọn chức năng (1-7): 3
--- GHI NHẬN CÔNG NHẬT & HIỆU SUẤT ---
1. Ghi nhận tham gia đứng lớp (Chỉ dành cho Giảng viên/Hybrid)
2. Cập nhật tiến độ KPI / Doanh số
3. Chấm công giờ làm việc
Chọn tác vụ (1-3): 2
Nhập giá trị doanh số hợp đồng mới mang về: 15,000,000

Cập nhật KPI thành công!
Doanh số tích lũy mới: 15,000,000 VND.
Tiến độ chỉ tiêu: 15% / 100,000,000 VND

Chọn chức năng (1-7): 3
--- GHI NHẬN CÔNG NHẬT & HIỆU SUẤT ---
1. Ghi nhận tham gia đứng lớp (Chỉ dành cho Giảng viên/Hybrid)
2. Cập nhật tiến độ KPI / Doanh số
3. Chấm công giờ làm việc
Chọn tác vụ (1-3): 2
Nhập giá trị doanh số hợp đồng mới mang về: -500
Số liệu cập nhật hiệu suất không được nhỏ hơn hoặc bằng 0

Chọn chức năng (1-7): 3
--- GHI NHẬN CÔNG NHẬT & HIỆU SUẤT ---
1. Ghi nhận tham gia đứng lớp (Chỉ dành cho Giảng viên/Hybrid)
2. Cập nhật tiến độ KPI / Doanh số
3. Chấm công giờ làm việc
Chọn tác vụ (1-3): 2
Nhập giá trị doanh số hợp đồng mới mang về: 50,000,000

Cập nhật KPI thành công!
Doanh số tích lũy mới: 65,000,000 VND.
Tiến độ chỉ tiêu: 65% / 100,000,000 VND

Chọn chức năng (1-7): 2
--- THÔNG TIN NHÂN SỰ HIỆN TẠI ---
Loại nhân sự: HybridManager
Tổ chức: Rikkei Education
Mã nhân sự: RKE0012345
Họ và tên: LE HOANG NAM
Số giờ làm việc: 162 giờ
Doanh số mang về: 65,000,000 VND
Chỉ tiêu doanh số: 100,000,000 VND
Số ca đã dạy: 1 ca
Tỷ lệ KPI giảng dạy: 0%
Thứ tự kế thừa (MRO): HybridManager -> Lecturer -> AdmissionStaff -> BaseEmployee -> ABC -> object

Chọn chức năng (1-7): 4
--- CHI TIẾT QUỸ LƯƠNG NHÂN SỰ ---
Nhân sự: LE HOANG NAM (Loại: HybridManager)
Mức lương cơ sở hệ thống: 3,000,000 VND
Số giờ làm việc tích lũy: 162 giờ
Lương cứng tính theo giờ: 486,000,000 VND
Phụ cấp ca dạy + Hoa hồng tuyển sinh tích hợp: 3,750,000 VND
Tổng lương thực nhận tháng này: 489,750,000 VND

Chọn chức năng (1-7): 5
--- ĐỒNG BỘ & SO SÁNH GIỜ CÔNG (OPERATOR OVERLOADING) ---
Nhân sự hiện tại (A): LE HOANG NAM (Giờ công: 162 giờ)
Danh sách nhân sự khác:
  - RKE0099999 (NGUYEN VAN AN - Giờ công: 180 giờ)
  - RKE0055555 (TRAN THI LAN - Giờ công: 42 giờ)
Chọn nhân sự đối ứng (B), nhập mã: RKE0099999
[Kết quả So sánh (__lt__)]: Giờ công cống hiến của nhân sự A ÍT HƠN nhân sự B.
[Kết quả Tổng hợp (__add__)]: Tổng số giờ làm việc của cả 2 nhân sự là: 342 giờ.

Chọn chức năng (1-7): 6
--- CHI TRẢ LƯƠNG QUA CỔNG ĐỐI TÁC TRUNG GIAN ---
1. Chi trả qua tài khoản Doanh nghiệp Vietcombank
2. Chi trả qua tài khoản Doanh nghiệp Techcombank
Chọn cổng ngân hàng (1-2): 1
Nhập số tiền giải ngân (Enter = lương tháng này): 
[Hệ thống VCB Corporate]: Đang kết nối tới cổng chi trả Rikkei...
Xác thực đối tác bằng Duck Typing thành công!
Ngân hàng đối tác đã giải ngân thành công số tiền: 489,750,000 VND tới nhân sự RKE0012345.

Chọn chức năng (1-7): 6
--- CHI TRẢ LƯƠNG QUA CỔNG ĐỐI TÁC TRUNG GIAN ---
1. Chi trả qua tài khoản Doanh nghiệp Vietcombank
2. Chi trả qua tài khoản Doanh nghiệp Techcombank
Chọn cổng ngân hàng (1-2): 2
Nhập số tiền giải ngân (Enter = lương tháng này): 12,000,000
[Techcombank Business]: Xác thực lệnh chi cho nhân sự RKE0012345...
Xác thực đối tác bằng Duck Typing thành công!
Ngân hàng đối tác đã giải ngân thành công số tiền: 12,000,000 VND tới nhân sự RKE0012345.

Chọn chức năng (1-7): 6
--- CHI TRẢ LƯƠNG QUA CỔNG ĐỐI TÁC TRUNG GIAN ---
1. Chi trả qua tài khoản Doanh nghiệp Vietcombank
2. Chi trả qua tài khoản Doanh nghiệp Techcombank
Chọn cổng ngân hàng (1-2): 3
Nhập số tiền giải ngân (Enter = lương tháng này): 1000
Cổng dịch vụ ngân hàng doanh nghiệp không hợp lệ hoặc chưa được liên kết liên thông kỹ thuật

Chọn chức năng (1-7): 9
Lựa chọn không hợp lệ, vui lòng chọn từ 1-7!

Cảm ơn đã sử dụng hệ thống Quản lý Nhân sự Rikkei Education Pro!
```

Kiểm tra trực tiếp các bẫy, bảo vệ giờ công, chuỗi MRO và Class Method:

```
1) Khởi tạo trực tiếp lớp trừu tượng BaseEmployee:
   TypeError: Can't instantiate abstract class BaseEmployee without an implementation for abstract methods 'calculate_salary', 'update_kpi'
2) Họ tên sau setter: 'PHAM MINH'
3) Gán trực tiếp working_hours = 9999:
   AttributeError: property 'working_hours' of 'Lecturer' object has no setter
   __working_hours bên ngoài: False
4) Toán tử với kiểu sai:
   lec + 'abc' -> TypeError: unsupported operand type(s) for +: 'Lecturer' and 'str'
   lec < 100 -> TypeError: '<' not supported between instances of 'Lecturer' and 'int'
5) Chuỗi calculate_salary theo MRO của Hybrid:
   MRO: HybridManager -> Lecturer -> AdmissionStaff -> BaseEmployee -> ABC -> object
   3 giờ * 3,000,000 + 1 ca * 500,000 + 20,000,000 * 5% = 10,500,000
6) update_base_salary_rate(100_000) áp dụng cho mọi nhân sự:
   Lecturer (10h): 1,000,000 | Hybrid (3h): 1,800,000 | Lecturer.base_salary_rate = 100,000
7) update_kpi(0) / log_working_hours(-5):
   ValueError: Số liệu cập nhật hiệu suất không được nhỏ hơn hoặc bằng 0
   ValueError: Số liệu cập nhật hiệu suất không được nhỏ hơn hoặc bằng 0
8) Duck Typing với object không có transfer_salary:
Cổng dịch vụ ngân hàng doanh nghiệp không hợp lệ hoặc chưa được liên kết liên thông kỹ thuật
   Với Vietcombank:
[Hệ thống VCB Corporate]: Đang kết nối tới cổng chi trả Rikkei...
Xác thực đối tác bằng Duck Typing thành công!
Ngân hàng đối tác đã giải ngân thành công số tiền: 1,000,000 VND tới nhân sự RKE0000002.
9) validate_employee_code: [True, False, False, False]
10) AdmissionStaff chỉ tiêu 0:
   ValueError: Số liệu cập nhật hiệu suất không được nhỏ hơn hoặc bằng 0
```

### Bảng kiểm thử

| Kịch bản | Dữ liệu | Kết quả |
|---|---|---|
| Chưa có nhân sự | Chọn 2 | Báo lỗi, yêu cầu tuyển dụng |
| Mã sai | RKE99 | Mã nhân sự không hợp lệ! ... |
| Chuẩn hóa tên | "tran   thi lan" | TRAN THI LAN |
| Admission đứng lớp | Tác vụ 1 | Chỉ dành cho Giảng viên / Hybrid |
| Lương Admission | 180 giờ, 40 triệu | 540,000,000 + 2,000,000 = 542,000,000 |
| Lương Lecturer | 42 giờ, 1 ca | 126,000,000 + 500,000 = 126,500,000 |
| KPI vượt 100% | 150 | Tỷ lệ KPI không được vượt quá 100% |
| Doanh số âm | -500 | Bẫy 2: thông báo lỗi |
| Lương Hybrid | 162 giờ, 1 ca, 65 triệu | 486,000,000 + 3,750,000 = 489,750,000 |
| Gộp / so sánh | 162 vs 180 giờ | A ÍT HƠN B; tổng 342 giờ |
| Duck Typing | Vietcombank / Techcombank / cổng 3 | Giải ngân thành công / thông báo cổng không hợp lệ |
| Bẫy 1, 3 | BaseEmployee(), emp + 'abc', emp < 100 | TypeError |

## Ghi chú

- `base_salary_rate = 3,000,000` được dùng đúng như đề làm **mức lương theo giờ**, nên tổng lương trong kịch bản chạy thử rất lớn; có thể đổi bằng `BaseEmployee.update_base_salary_rate()`.
- Ví dụ hoa hồng mẫu trong đề không khớp với công thức 5% doanh số; chương trình làm đúng công thức đề nêu (VD 65,000,000 × 5% = 3,250,000).
- Vì giờ công không có setter, chức năng 3 bổ sung tác vụ "Chấm công giờ làm việc" để tăng giờ công qua `log_working_hours()`.
- KPI của Lecturer là tỷ lệ % (0 < KPI ≤ 100); KPI của Admission / Hybrid là doanh số cộng dồn.
- Chức năng 6: nhấn Enter khi nhập số tiền thì hệ thống giải ngân đúng bằng lương tháng đã tính.

## Cách chạy

```bash
python main.py
```
