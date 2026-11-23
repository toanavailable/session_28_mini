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
