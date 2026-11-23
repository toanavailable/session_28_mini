# Bài 2 - Hệ thống quản lý nội dung E-Learning Rikkei Education

## Bối cảnh & vấn đề

Nền tảng học trực tuyến Rikkei Academy LMS quản lý nhiều loại nội dung: **Bài giảng video (Video Lesson)**, **Bài thực hành lập trình (Coding Challenge)** và **Bài đánh giá tích hợp (Hybrid Assessment)** vừa có video hướng dẫn vừa có bài code chấm bằng testcase.

Mỗi loại nội dung có cách tính điểm thưởng (XP) khi học viên hoàn thành và cách cập nhật nội dung khác nhau. Thiết kế rời rạc sẽ khiến logic tính điểm trùng lặp, khó thêm loại bài học mới; thời lượng bài học nếu bị sửa trực tiếp sẽ làm sai lệch thống kê.

Nhiệm vụ: xây dựng module "Rikkei Academy LMS Simulator Pro" áp dụng OOP nâng cao: lớp trừu tượng và đóng gói thời lượng, kế thừa và đa kế thừa (MRO), đa hình khi tính điểm / cập nhật nội dung, đồng bộ bài giảng lên đám mây bằng Duck Typing và nạp chồng toán tử để so sánh / gộp thời lượng.

## Yêu cầu thiết kế lớp

| Hạng mục | Yêu cầu |
|---|---|
| Abstract Base Class `BaseLesson` | Class Attributes `platform_name = "Rikkei Academy LMS"`, `base_completion_points = 10`; private `__duration_minutes` (khởi tạo 0); `@property duration_minutes` không có setter; `@abstractmethod calculate_completion_score(self)`, `update_content(self, new_data)`; `__add__` cộng thời lượng; `__lt__` so sánh thời lượng |
| Subclass 1 `VideoLesson` | Thêm `video_quality`, `view_count`; điểm = `base + duration * 0.5`; `update_content` đổi độ phân giải; `play_video()` tăng lượt xem |
| Subclass 2 `CodingChallenge` | Thêm `number_of_testcases`, `difficulty_multiplier`; điểm = `base * testcases * multiplier`; `update_content` bổ sung testcase |
| Đa kế thừa `HybridAssessment` | Kế thừa `VideoLesson` và `CodingChallenge`, tuân thủ MRO; điểm = điểm video + điểm coding |
| Static & Class Method | `@staticmethod validate_lesson_code(code)`: đúng 10 ký tự, bắt đầu bằng `LMS`; `@classmethod update_base_points(cls, new_points)`: đổi điểm cơ sở toàn hệ thống |

## Yêu cầu nghiệp vụ (Menu)

```
===== RIKKEI ACADEMY LMS SIMULATOR PRO =====
1. Khởi tạo bài học mới (Chọn loại bài học nội dung)
2. Xem thông tin bài học & Kiểm tra thứ tự kế thừa (MRO)
3. Cập nhật thời lượng & Nội dung bài học (Tính đa hình)
4. Xem chi tiết điểm thưởng hoàn thành bài học
5. Kiểm tra gộp thời lượng & So sánh độ dài bài học (Overloading)
6. Đồng bộ bài giảng lên Nền tảng Đám mây (Duck Typing)
7. Thoát chương trình
==================================================
Chọn chức năng (1-7):
```

- **Chức năng 1 - Khởi tạo bài học:** Chọn loại (1: Video, 2: Coding, 3: Hybrid); nhập mã, tiêu đề (tự IN HOA qua setter), thời lượng; Video / Hybrid nhập chất lượng video; Coding / Hybrid nhập số testcase và hệ số độ khó.
- **Chức năng 2 - Thông tin & MRO:** Chưa có bài học thì báo lỗi; có thì in thông tin theo loại và danh sách MRO.
- **Chức năng 3 - Cập nhật (Đa hình):** 3 tác vụ: ghi nhận lượt xem (chỉ Video / Hybrid), cập nhật thông số (cùng gọi `update_content()`: Video đổi độ phân giải, Coding / Hybrid bổ sung testcase), bổ sung thời lượng.
- **Chức năng 4 - Điểm thưởng:** Gọi đa hình `calculate_completion_score()`, in từng thành phần điểm và tổng XP.
- **Chức năng 5 - Gộp & So sánh:** Chọn bài học khác, dùng `<` (`__lt__`) và `+` (`__add__`) trên thời lượng.
- **Chức năng 6 - Đồng bộ đám mây (Duck Typing):** `sync_to_cloud(cloud_service, lesson)` chỉ cần đối tượng có `upload_lesson(lesson)`; có sẵn `AWSS3StorageService`, `GoogleCloudStorageService`.
- **Chức năng 7 - Thoát:** "Cảm ơn bạn đã trải nghiệm hệ thống Quản lý Bài học Rikkei Academy LMS Pro!"

### Edge cases (bẫy dữ liệu nâng cao)

| Bẫy | Xử lý |
|---|---|
| Bẫy 1 - Khởi tạo lớp trừu tượng | `BaseLesson()` → `TypeError` |
| Bẫy 2 - Thông số không hợp lệ | Thời lượng / testcase / hệ số ≤ 0 → "Thời lượng bài học và thông số kỹ thuật không được nhỏ hơn hoặc bằng 0" |
| Bẫy 3 - Sai kiểu khi Overloading | `__add__` / `__lt__` kiểm tra `isinstance(other, BaseLesson)`, sai kiểu trả về `NotImplemented` → `TypeError` |
| Bẫy 4 - Dịch vụ đám mây sai giao diện | Không có `upload_lesson` → bắt `AttributeError`: "Dịch vụ lưu trữ đám mây không hợp lệ hoặc chưa kết nối chứng chỉ API liên thông" |

## (1) Phân tích và thiết kế giải pháp (Design Document)

| Lớp | Kế thừa | Thành phần chính | Vai trò |
|---|---|---|---|
| `BaseLesson` | `ABC` | `platform_name`, `base_completion_points`, `__duration_minutes`, `@property duration_minutes`, `add_duration`, `score_parts`, `__add__`, `__lt__`, static / class method | Khung chuẩn, đóng gói thời lượng |
| `VideoLesson` | `BaseLesson` | `video_quality`, `view_count`, `play_video()`, điểm + base + phút × 0.5 | Bài giảng video |
| `CodingChallenge` | `BaseLesson` | `number_of_testcases`, `difficulty_multiplier`, điểm + base × testcase × hệ số | Bài thực hành code |
| `HybridAssessment` | `VideoLesson`, `CodingChallenge` | không override `calculate_completion_score`; `update_content` dùng nhánh `CodingChallenge` | Bài đánh giá tích hợp |
| `AWSS3StorageService`, `GoogleCloudStorageService` | (không) | `upload_lesson(lesson)` | Lưu trữ đám mây Duck Typing |

**HybridAssessment cộng điểm của hai nhánh như thế nào?**

MRO: `HybridAssessment → VideoLesson → CodingChallenge → BaseLesson → ABC → object`. `VideoLesson.calculate_completion_score` cộng `base + phút × 0.5` rồi gọi `super()`, lời gọi này đi tới `CodingChallenge` (lớp kế tiếp trong MRO của Hybrid, không phải `BaseLesson`), cộng `base × testcase × hệ số`, cuối cùng tới `BaseLesson` trả về 0. VD 30 phút, 8 testcase, hệ số 1.5: (10 + 15) + 120 = **145 XP**. `score_parts()` cũng cooperative nên chức năng 4 in đủ từng thành phần.

**update_content của Hybrid làm gì?**

Theo MRO, `VideoLesson.update_content` (đổi độ phân giải) sẽ được tìm thấy trước. Vì bài đánh giá được cập nhật chủ yếu bằng testcase, `HybridAssessment.update_content` gọi `super(VideoLesson, self).update_content(new_data)` để dùng bản của `CodingChallenge`; prompt nhập (`content_prompt`) cũng lấy theo `CodingChallenge`.

**Vì sao thời lượng không có setter?**

`__duration_minutes` bị name mangling thành `_BaseLesson__duration_minutes`; `@property duration_minutes` chỉ đọc, gán trực tiếp gây `AttributeError`. Thời lượng chỉ tăng qua `add_duration()` có kiểm tra > 0 (Bẫy 2).

**Duck Typing giúp thêm nhà cung cấp đám mây thế nào?**

`sync_to_cloud()` chỉ gọi `cloud_service.upload_lesson(lesson)`. Nhà cung cấp mới (Azure Blob, Cloudflare R2...) chỉ cần một class có phương thức cùng tên; đối tượng sai giao diện bị bắt `AttributeError` (Bẫy 4).

Thuật toán các phương thức chính:

```
VideoLesson.calculate_completion_score():
    TRẢ VỀ super().calculate_completion_score() + base + duration * 0.5

CodingChallenge.calculate_completion_score():
    TRẢ VỀ super().calculate_completion_score() + base * testcases * multiplier

BaseLesson.calculate_completion_score():      # phần lõi (abstract có thân)
    TRẢ VỀ 0

HybridAssessment.update_content(new_data):
    TRẢ VỀ super(VideoLesson, self).update_content(new_data)   # -> CodingChallenge

sync_to_cloud(service, lesson):
    THỬ service.upload_lesson(lesson)          # Duck Typing
    BẮT AttributeError → "Dịch vụ lưu trữ đám mây không hợp lệ ..."
```

## (2) Triển khai code

File: [`main.py`](main.py)

```python
"""
====================================================================
RIKKEI ACADEMY LMS SIMULATOR PRO - THIẾT KẾ LỚP
====================================================================
                        BaseLesson (ABC)
     platform_name, base_completion_points | __duration_minutes (private)
     @property duration_minutes (không setter) | add_duration() | __add__ / __lt__
     @abstractmethod calculate_completion_score (phần lõi = 0) / update_content
     @staticmethod validate_lesson_code | @classmethod update_base_points
                 /                                  \\
          VideoLesson                          CodingChallenge
     + video_quality, view_count          + number_of_testcases, difficulty_multiplier
     điểm += base + duration * 0.5        điểm += base * testcases * multiplier
     update_content: đổi độ phân giải     update_content: bổ sung testcase
     play_video(): +1 lượt xem
                 \\                                  /
          HybridAssessment(VideoLesson, CodingChallenge)

MRO Hybrid: HybridAssessment -> VideoLesson -> CodingChallenge -> BaseLesson -> ABC -> object
calculate_completion_score viết kiểu cooperative (mỗi lớp cộng phần của mình
rồi gọi super()) nên HybridAssessment tự cộng đủ điểm video + điểm coding.
Lưu trữ đám mây (Duck Typing): AWSS3StorageService, GoogleCloudStorageService
chỉ cần có upload_lesson(lesson).
====================================================================
"""

from abc import ABC, abstractmethod

CODE_PREFIX = "LMS"
MINUTE_POINT_RATE = 0.5           # mỗi phút video = 0.5 XP
VIDEO_QUALITIES = ("360p", "480p", "720p", "1080p", "2K", "4K")
POSITIVE_ERROR = "Thời lượng bài học và thông số kỹ thuật không được nhỏ hơn hoặc bằng 0"
MENU_LINE = "=" * 50


def num(value):
    """100.0 -> '100', 2.5 -> '2.5'."""
    return f"{value:,.2f}".rstrip("0").rstrip(".")


class BaseLesson(ABC):
    """Lớp trừu tượng: khung chuẩn cho mọi bài học (không tạo object trực tiếp)."""

    platform_name = "Rikkei Academy LMS"   # Class Attributes dùng chung
    base_completion_points = 10            # điểm XP cơ sở
    content_prompt = "Nhập thông số mới: "

    def __init__(self, lesson_code, title, **kwargs):
        """Kiểm tra mã, chuẩn hóa tiêu đề qua setter, thời lượng ban đầu = 0."""
        super().__init__(**kwargs)         # cooperative theo MRO
        if not BaseLesson.validate_lesson_code(lesson_code):
            raise ValueError("Mã bài học không hợp lệ! Phải gồm đúng 10 ký tự và "
                             "bắt đầu bằng LMS.")
        self.__lesson_code = lesson_code
        self.__title = ""
        self.title = title
        self.__duration_minutes = 0        # private: _BaseLesson__duration_minutes

    # ---------------- @property ----------------
    @property
    def lesson_code(self):
        """Mã bài học (chỉ đọc)."""
        return self.__lesson_code

    @property
    def duration_minutes(self):
        """Thời lượng (phút) - chỉ đọc, KHÔNG setter."""
        return self.__duration_minutes

    @property
    def title(self):
        """Tiêu đề bài học."""
        return self.__title

    @title.setter
    def title(self, new_title):
        """IN HOA, xóa khoảng trắng thừa; rỗng thì ValueError."""
        normalized = " ".join(str(new_title).split()).upper()
        if not normalized:
            raise ValueError("Tiêu đề bài học không được để trống!")
        self.__title = normalized

    @staticmethod
    def _check_positive(value):
        """Bẫy 2: thời lượng / thông số phải > 0."""
        if value <= 0:
            raise ValueError(POSITIVE_ERROR)

    def add_duration(self, minutes):
        """Bổ sung thời lượng (cửa duy nhất thay đổi __duration_minutes)."""
        BaseLesson._check_positive(minutes)
        self.__duration_minutes += minutes

    # ---------------- @abstractmethod ----------------
    @abstractmethod
    def calculate_completion_score(self):
        """Phần lõi = 0. Lớp con override, cộng phần riêng rồi gọi super()."""
        return 0

    @abstractmethod
    def update_content(self, new_data):
        """Cập nhật thông số nội dung - mỗi loại bài học xử lý khác nhau."""

    def score_parts(self):
        """Danh sách (nhãn, điểm) - lớp con bổ sung qua super()."""
        return []

    def lesson_type(self):
        """Tên loại bài học (tên class)."""
        return type(self).__name__

    def info_lines(self):
        """Thông tin chung; lớp con bổ sung qua super()."""
        return [f"Loại bài học: {self.lesson_type()}",
                f"Nền tảng: {BaseLesson.platform_name}",
                f"Mã bài học: {self.lesson_code}",
                f"Tiêu đề: {self.title}",
                f"Thời lượng: {num(self.duration_minutes)} phút"]

    # ---------------- Operator Overloading ----------------
    def __add__(self, other):
        """A + B -> tổng thời lượng (phút); chỉ nhận BaseLesson."""
        if not isinstance(other, BaseLesson):
            return NotImplemented
        return self.duration_minutes + other.duration_minutes

    def __lt__(self, other):
        """A < B -> bài A ngắn hơn bài B."""
        if not isinstance(other, BaseLesson):
            return NotImplemented
        return self.duration_minutes < other.duration_minutes

    # ---------------- Static / Class Method ----------------
    @staticmethod
    def validate_lesson_code(lesson_code):
        """Bắt đầu bằng 'LMS' và đúng 10 ký tự (VD: LMS1234567)."""
        return (isinstance(lesson_code, str) and len(lesson_code) == 10
                and lesson_code.startswith(CODE_PREFIX))

    @classmethod
    def update_base_points(cls, new_points):
        """Đổi điểm XP cơ sở cho TOÀN BỘ bài học."""
        if new_points <= 0:
            raise ValueError("Điểm cơ sở phải lớn hơn 0!")
        BaseLesson.base_completion_points = new_points


class VideoLesson(BaseLesson):
    """Bài giảng video."""

    content_prompt = "Nhập độ phân giải video mới (VD: 720p, 1080p, 4K): "

    def __init__(self, lesson_code, title, video_quality="720p", **kwargs):
        """Thêm chất lượng video và lượt xem; super() cho phần còn lại."""
        super().__init__(lesson_code=lesson_code, title=title, **kwargs)
        self.video_quality = VideoLesson.normalize_quality(video_quality)
        self.view_count = 0

    @staticmethod
    def normalize_quality(quality):
        """'1080P' -> '1080p'; ngoài danh sách thì ValueError."""
        text = str(quality).strip().upper()
        for item in VIDEO_QUALITIES:
            if item.upper() == text:
                return item
        raise ValueError("Độ phân giải không hợp lệ! Hỗ trợ: " + ", ".join(VIDEO_QUALITIES))

    def calculate_completion_score(self):
        """Điểm = base + duration * 0.5 (+ phần của lớp kế tiếp trong MRO)."""
        own = BaseLesson.base_completion_points + self.duration_minutes * MINUTE_POINT_RATE
        return super().calculate_completion_score() + own

    def score_parts(self):
        """Thêm điểm cơ sở hoàn thành video và điểm thời lượng."""
        return [("Điểm cơ sở hoàn thành video", BaseLesson.base_completion_points),
                (f"Điểm thời lượng ({num(self.duration_minutes)} phút x "
                 f"{MINUTE_POINT_RATE})", self.duration_minutes * MINUTE_POINT_RATE)
                ] + super().score_parts()

    def update_content(self, new_data):
        """Nâng / hạ độ phân giải video."""
        self.video_quality = VideoLesson.normalize_quality(new_data)
        return [f"Chất lượng video hiện tại: {self.video_quality}."]

    def play_video(self):
        """Học viên xem video: +1 lượt xem."""
        self.view_count += 1

    def info_lines(self):
        """Bổ sung chất lượng, lượt xem."""
        return super().info_lines() + [f"Chất lượng video: {self.video_quality}",
                                       f"Lượt xem: {self.view_count} lượt"]


class CodingChallenge(BaseLesson):
    """Bài thực hành lập trình."""

    content_prompt = "Nhập số testcase cần bổ sung: "

    def __init__(self, lesson_code, title, number_of_testcases, difficulty_multiplier,
                 **kwargs):
        """Thêm số testcase và hệ số độ khó (đều phải > 0)."""
        super().__init__(lesson_code=lesson_code, title=title, **kwargs)
        BaseLesson._check_positive(number_of_testcases)
        BaseLesson._check_positive(difficulty_multiplier)
        self.number_of_testcases = int(number_of_testcases)
        self.difficulty_multiplier = difficulty_multiplier

    def calculate_completion_score(self):
        """Điểm = base * testcases * multiplier (+ phần của lớp kế tiếp)."""
        own = (BaseLesson.base_completion_points * self.number_of_testcases
               * self.difficulty_multiplier)
        return super().calculate_completion_score() + own

    def score_parts(self):
        """Thêm điểm testcase."""
        own = (BaseLesson.base_completion_points * self.number_of_testcases
               * self.difficulty_multiplier)
        return super().score_parts() + [
            (f"Điểm testcase ({BaseLesson.base_completion_points} x "
             f"{self.number_of_testcases} testcase x {num(self.difficulty_multiplier)})", own)]

    def update_content(self, new_data):
        """Bổ sung testcase (số nguyên > 0)."""
        added = int(new_data)
        BaseLesson._check_positive(added)
        self.number_of_testcases += added
        return [f"Số lượng testcase hiện tại trên hệ thống: "
                f"{self.number_of_testcases} testcases."]

    def info_lines(self):
        """Bổ sung testcase, hệ số."""
        return super().info_lines() + [
            f"Số testcase: {self.number_of_testcases}",
            f"Hệ số độ khó: {num(self.difficulty_multiplier)}"]


class HybridAssessment(VideoLesson, CodingChallenge):
    """Bài đánh giá tích hợp: video hướng dẫn + bài code (đa kế thừa)."""

    content_prompt = CodingChallenge.content_prompt

    def __init__(self, lesson_code, title, video_quality, number_of_testcases,
                 difficulty_multiplier):
        """Một lần super() khởi tạo Video, Coding, BaseLesson theo MRO."""
        super().__init__(lesson_code=lesson_code, title=title, video_quality=video_quality,
                         number_of_testcases=number_of_testcases,
                         difficulty_multiplier=difficulty_multiplier)

    # calculate_completion_score: KHÔNG override - Video -> Coding -> BaseLesson

    def update_content(self, new_data):
        """Cập nhật nội dung của bài đánh giá = bổ sung testcase (bản của Coding)."""
        return super(VideoLesson, self).update_content(new_data)   # -> CodingChallenge


# =====================================================================
# LƯU TRỮ ĐÁM MÂY (DUCK TYPING) - không kế thừa lớp nào
# =====================================================================
class AWSS3StorageService:
    """Amazon S3."""

    def upload_lesson(self, lesson):
        """Tải bài giảng lên S3."""
        print("[Hệ thống AWS S3]: Đang khởi tạo luồng băng thông kết nối tới LMS...")


class GoogleCloudStorageService:
    """Google Cloud Storage."""

    def upload_lesson(self, lesson):
        """Tải bài giảng lên GCS."""
        print(f"[Google Cloud Storage]: Đang mã hóa và tải lên bài giảng "
              f"{lesson.lesson_code}...")


def sync_to_cloud(cloud_service, lesson):
    """Không quan tâm nhà cung cấp nào, chỉ cần có upload_lesson()."""
    try:
        cloud_service.upload_lesson(lesson)
    except AttributeError:
        print("Dịch vụ lưu trữ đám mây không hợp lệ hoặc chưa kết nối chứng chỉ API "
              "liên thông")
        return False
    print("Xác thực đối tác bằng Duck Typing thành công!")
    print(f"Đồng bộ hoàn tất bài giảng {lesson.lesson_code} - {lesson.title} "
          f"({num(lesson.duration_minutes)} phút) lên nền tảng đám mây.")
    return True


# =====================================================================
# HÀM GIAO DIỆN
# =====================================================================
LESSON_TYPES = {"1": ("Video Lesson (Bài giảng Video)", "Video"),
                "2": ("Coding Challenge (Bài thực hành Lập trình)", "Coding Challenge"),
                "3": ("Hybrid Assessment (Bài đánh giá Tích hợp)", "Hybrid Assessment")}


def parse_number(text):
    """'1,5' không hỗ trợ; '1.5' -> 1.5."""
    return float(text.strip().replace(",", ""))


def require_lesson(current_lesson):
    """Chưa có bài học thì báo lỗi."""
    if current_lesson is None:
        print("Hệ thống chưa có bài học nào. "
              "Vui lòng khởi tạo bài học ở Chức năng 1 trước.")
        return False
    return True


def find_lesson(lessons, lesson_code):
    """Tìm bài học theo mã."""
    for lesson in lessons:
        if lesson.lesson_code == lesson_code:
            return lesson
    return None


def friendly(error):
    """Đổi thông báo lỗi ép kiểu của Python sang tiếng Việt."""
    message = str(error)
    if "could not convert" in message or "invalid literal" in message:
        return "Giá trị phải là số hợp lệ!"
    return message


def create_lesson(lessons):
    """Chức năng 1: khởi tạo bài học theo loại."""
    print("--- CHỌN LOẠI BÀI HỌC KHỞI TẠO ---")
    for key, (label, _) in LESSON_TYPES.items():
        print(f"{key}. {label}")
    kind = input("Chọn loại bài học (1-3): ").strip()
    if kind not in LESSON_TYPES:
        print("Loại bài học không hợp lệ!")
        return None
    code = input("Nhập mã bài học 10 ký tự: ").strip()
    if not BaseLesson.validate_lesson_code(code):
        print("Mã bài học không hợp lệ! Phải gồm đúng 10 ký tự và bắt đầu bằng LMS.")
        return None
    if find_lesson(lessons, code) is not None:
        print("Mã bài học đã tồn tại trong hệ thống!")
        return None
    title = input("Nhập tiêu đề bài học: ")
    try:
        duration = parse_number(input("Nhập thời lượng bài học (phút): "))
        BaseLesson._check_positive(duration)
        if kind in ("1", "3"):
            quality = input("Nhập chất lượng video (VD: 720p, 1080p, 4K): ")
        if kind in ("2", "3"):
            testcases = int(input("Nhập số lượng testcase: ").strip())
            multiplier = parse_number(input("Nhập hệ số độ khó (VD: 1.5): "))
        if kind == "1":
            lesson = VideoLesson(code, title, video_quality=quality)
        elif kind == "2":
            lesson = CodingChallenge(code, title, testcases, multiplier)
        else:
            lesson = HybridAssessment(code, title, quality, testcases, multiplier)
        lesson.add_duration(duration)
    except ValueError as error:
        print(friendly(error))
        return None
    lessons.append(lesson)
    print(f"Khởi tạo bài học {LESSON_TYPES[kind][1]} thành công!")
    print(f"Tiêu đề bài học: {lesson.title}")
    return lesson


def show_info(lesson):
    """Chức năng 2: thông tin (đa hình info_lines) + MRO."""
    print("--- THÔNG TIN BÀI HỌC HIỆN TẠI ---")
    print("\n".join(lesson.info_lines()))
    print("Thứ tự kế thừa (MRO): "
          + " -> ".join(cls.__name__ for cls in type(lesson).__mro__))


def update_lesson(lesson):
    """Chức năng 3: xem video / update_content (đa hình) / bổ sung thời lượng."""
    print("--- CẬP NHẬT THỜI LƯỢNG & NỘI DUNG BÀI HỌC ---")
    print("1. Ghi nhận lượt xem video (Chỉ dành cho Video/Hybrid)")
    print("2. Cập nhật thông số nội dung bài học")
    print("3. Bổ sung thời lượng bài học")
    task = input("Chọn tác vụ (1-3): ").strip()
    try:
        if task == "1":
            if not isinstance(lesson, VideoLesson):
                print("Tác vụ xem video chỉ dành cho Video Lesson / Hybrid Assessment.")
                return
            lesson.play_video()
            print("Ghi nhận thành công! Học viên đã xem video bài học.")
            print(f"Tổng lượt xem hiện tại: {lesson.view_count} lượt.")
        elif task == "2":
            lines = lesson.update_content(input(lesson.content_prompt))
            print("\nCập nhật thông số thành công!")
            print("\n".join(lines))
        elif task == "3":
            lesson.add_duration(parse_number(input("Nhập số phút cần bổ sung: ")))
            print(f"Bổ sung thành công! Thời lượng hiện tại: "
                  f"{num(lesson.duration_minutes)} phút.")
        else:
            print("Tác vụ không hợp lệ!")
    except ValueError as error:
        print(friendly(error))


def show_score(lesson):
    """Chức năng 4: gọi đa hình calculate_completion_score()."""
    print("--- CHI TIẾT ĐIỂM THƯỞNG HOÀN THÀNH BÀI HỌC ---")
    print(f"Bài học: {lesson.title} (Loại: {lesson.lesson_type()})")
    print(f"Điểm cơ sở hệ thống: {BaseLesson.base_completion_points} XP")
    for label, value in lesson.score_parts():
        print(f"  + {label}: {num(value)} XP")
    print(f"Tổng điểm thưởng học viên nhận được: "
          f"{num(lesson.calculate_completion_score())} XP")


def compare_lessons(lessons, lesson):
    """Chức năng 5: toán tử < và +."""
    print("--- GỘP & SO SÁNH THỜI LƯỢNG BÀI HỌC (OPERATOR OVERLOADING) ---")
    others = [item for item in lessons if item is not lesson]
    if not others:
        print("Cần ít nhất 2 bài học trong hệ thống để so sánh / gộp!")
        return
    print(f"Bài học hiện tại (A): {lesson.title} "
          f"(Thời lượng: {num(lesson.duration_minutes)} phút)")
    print("Danh sách bài học khác:")
    for item in others:
        print(f"  - {item.lesson_code} ({item.title} - Thời lượng: "
              f"{num(item.duration_minutes)} phút)")
    other = find_lesson(others, input("Chọn bài học đối ứng (B), nhập mã: ").strip())
    if other is None:
        print("Không tìm thấy bài học đối ứng!")
        return
    if lesson < other:
        result = "NGẮN HƠN"
    elif other < lesson:
        result = "DÀI HƠN"
    else:
        result = "BẰNG"
    print(f"[Kết quả So sánh (__lt__)]: Thời lượng bài học A {result} thời lượng "
          "bài học B.")
    print(f"[Kết quả Tổng hợp (__add__)]: Tổng thời lượng của cả 2 bài học là: "
          f"{num(lesson + other)} phút.")


def sync_lesson(lesson):
    """Chức năng 6: đồng bộ qua dịch vụ đám mây (Duck Typing)."""
    print("--- ĐỒNG BỘ BÀI GIẢNG LÊN NỀN TẢNG ĐÁM MÂY ---")
    print("1. Lưu trữ trên Amazon Web Services S3")
    print("2. Lưu trữ trên Google Cloud Storage")
    choice = input("Chọn dịch vụ đám mây (1-2): ").strip()
    service = {"1": AWSS3StorageService(),
               "2": GoogleCloudStorageService()}.get(choice, object())
    sync_to_cloud(service, lesson)


def display_menu():
    """In menu chính."""
    print("\n===== RIKKEI ACADEMY LMS SIMULATOR PRO =====")
    print("1. Khởi tạo bài học mới (Chọn loại bài học nội dung)")
    print("2. Xem thông tin bài học & Kiểm tra thứ tự kế thừa (MRO)")
    print("3. Cập nhật thời lượng & Nội dung bài học (Tính đa hình)")
    print("4. Xem chi tiết điểm thưởng hoàn thành bài học")
    print("5. Kiểm tra gộp thời lượng & So sánh độ dài bài học (Overloading)")
    print("6. Đồng bộ bài giảng lên Nền tảng Đám mây (Duck Typing)")
    print("7. Thoát chương trình")
    print(MENU_LINE)


def main():
    """lessons = [], current_lesson = None; vòng lặp menu."""
    lessons = []
    current_lesson = None
    while True:
        display_menu()
        choice = input("Chọn chức năng (1-7): ").strip()
        if choice == "1":
            current_lesson = create_lesson(lessons) or current_lesson
        elif choice in ("2", "3", "4", "5", "6") and not require_lesson(current_lesson):
            continue
        elif choice == "2":
            show_info(current_lesson)
        elif choice == "3":
            update_lesson(current_lesson)
        elif choice == "4":
            show_score(current_lesson)
        elif choice == "5":
            compare_lessons(lessons, current_lesson)
        elif choice == "6":
            sync_lesson(current_lesson)
        elif choice == "7":
            print("Cảm ơn bạn đã trải nghiệm hệ thống Quản lý Bài học "
                  "Rikkei Academy LMS Pro!")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn từ 1-7!")


if __name__ == "__main__":
    main()
```

## Kết quả chạy thử

Kịch bản: cập nhật khi chưa có bài học → mã LMS12 sai → tạo Video PYTHON CO BAN (45 phút, 1080p), xem 2 lần, đổi 4K, đổi 8K (không hỗ trợ), xem điểm → tạo Coding VONG LAP FOR (60 phút, 5 testcase, hệ số 2), thử xem video (bị chặn), thêm 3 testcase, xem điểm → tạo Hybrid OOP NANG CAO (30 phút, 720p, 5 testcase, hệ số 1.5), thông tin + MRO, thêm 3 testcase, xem video, bổ sung -15 và 0 phút (Bẫy 2), xem điểm (145 XP) → so sánh / gộp với LMS0000002 → đồng bộ AWS S3, Google Cloud, dịch vụ không tồn tại → menu sai → thoát. Khung menu lặp lại được ẩn.

```
Chọn chức năng (1-7): 3
Hệ thống chưa có bài học nào. Vui lòng khởi tạo bài học ở Chức năng 1 trước.

Chọn chức năng (1-7): 1
--- CHỌN LOẠI BÀI HỌC KHỞI TẠO ---
1. Video Lesson (Bài giảng Video)
2. Coding Challenge (Bài thực hành Lập trình)
3. Hybrid Assessment (Bài đánh giá Tích hợp)
Chọn loại bài học (1-3): 1
Nhập mã bài học 10 ký tự: LMS12
Mã bài học không hợp lệ! Phải gồm đúng 10 ký tự và bắt đầu bằng LMS.

Chọn chức năng (1-7): 1
--- CHỌN LOẠI BÀI HỌC KHỞI TẠO ---
1. Video Lesson (Bài giảng Video)
2. Coding Challenge (Bài thực hành Lập trình)
3. Hybrid Assessment (Bài đánh giá Tích hợp)
Chọn loại bài học (1-3): 1
Nhập mã bài học 10 ký tự: LMS0000001
Nhập tiêu đề bài học:   python   co ban  
Nhập thời lượng bài học (phút): 45
Nhập chất lượng video (VD: 720p, 1080p, 4K): 1080p
Khởi tạo bài học Video thành công!
Tiêu đề bài học: PYTHON CO BAN

Chọn chức năng (1-7): 3
--- CẬP NHẬT THỜI LƯỢNG & NỘI DUNG BÀI HỌC ---
1. Ghi nhận lượt xem video (Chỉ dành cho Video/Hybrid)
2. Cập nhật thông số nội dung bài học
3. Bổ sung thời lượng bài học
Chọn tác vụ (1-3): 1
Ghi nhận thành công! Học viên đã xem video bài học.
Tổng lượt xem hiện tại: 1 lượt.

Chọn chức năng (1-7): 3
--- CẬP NHẬT THỜI LƯỢNG & NỘI DUNG BÀI HỌC ---
1. Ghi nhận lượt xem video (Chỉ dành cho Video/Hybrid)
2. Cập nhật thông số nội dung bài học
3. Bổ sung thời lượng bài học
Chọn tác vụ (1-3): 1
Ghi nhận thành công! Học viên đã xem video bài học.
Tổng lượt xem hiện tại: 2 lượt.

Chọn chức năng (1-7): 3
--- CẬP NHẬT THỜI LƯỢNG & NỘI DUNG BÀI HỌC ---
1. Ghi nhận lượt xem video (Chỉ dành cho Video/Hybrid)
2. Cập nhật thông số nội dung bài học
3. Bổ sung thời lượng bài học
Chọn tác vụ (1-3): 2
Nhập độ phân giải video mới (VD: 720p, 1080p, 4K): 4K

Cập nhật thông số thành công!
Chất lượng video hiện tại: 4K.

Chọn chức năng (1-7): 3
--- CẬP NHẬT THỜI LƯỢNG & NỘI DUNG BÀI HỌC ---
1. Ghi nhận lượt xem video (Chỉ dành cho Video/Hybrid)
2. Cập nhật thông số nội dung bài học
3. Bổ sung thời lượng bài học
Chọn tác vụ (1-3): 2
Nhập độ phân giải video mới (VD: 720p, 1080p, 4K): 8K
Độ phân giải không hợp lệ! Hỗ trợ: 360p, 480p, 720p, 1080p, 2K, 4K

Chọn chức năng (1-7): 4
--- CHI TIẾT ĐIỂM THƯỞNG HOÀN THÀNH BÀI HỌC ---
Bài học: PYTHON CO BAN (Loại: VideoLesson)
Điểm cơ sở hệ thống: 10 XP
  + Điểm cơ sở hoàn thành video: 10 XP
  + Điểm thời lượng (45 phút x 0.5): 22.5 XP
Tổng điểm thưởng học viên nhận được: 32.5 XP

Chọn chức năng (1-7): 1
--- CHỌN LOẠI BÀI HỌC KHỞI TẠO ---
1. Video Lesson (Bài giảng Video)
2. Coding Challenge (Bài thực hành Lập trình)
3. Hybrid Assessment (Bài đánh giá Tích hợp)
Chọn loại bài học (1-3): 2
Nhập mã bài học 10 ký tự: LMS0000002
Nhập tiêu đề bài học: vong lap for
Nhập thời lượng bài học (phút): 60
Nhập số lượng testcase: 5
Nhập hệ số độ khó (VD: 1.5): 2
Khởi tạo bài học Coding Challenge thành công!
Tiêu đề bài học: VONG LAP FOR

Chọn chức năng (1-7): 3
--- CẬP NHẬT THỜI LƯỢNG & NỘI DUNG BÀI HỌC ---
1. Ghi nhận lượt xem video (Chỉ dành cho Video/Hybrid)
2. Cập nhật thông số nội dung bài học
3. Bổ sung thời lượng bài học
Chọn tác vụ (1-3): 1
Tác vụ xem video chỉ dành cho Video Lesson / Hybrid Assessment.

Chọn chức năng (1-7): 3
--- CẬP NHẬT THỜI LƯỢNG & NỘI DUNG BÀI HỌC ---
1. Ghi nhận lượt xem video (Chỉ dành cho Video/Hybrid)
2. Cập nhật thông số nội dung bài học
3. Bổ sung thời lượng bài học
Chọn tác vụ (1-3): 2
Nhập số testcase cần bổ sung: 3

Cập nhật thông số thành công!
Số lượng testcase hiện tại trên hệ thống: 8 testcases.

Chọn chức năng (1-7): 4
--- CHI TIẾT ĐIỂM THƯỞNG HOÀN THÀNH BÀI HỌC ---
Bài học: VONG LAP FOR (Loại: CodingChallenge)
Điểm cơ sở hệ thống: 10 XP
  + Điểm testcase (10 x 8 testcase x 2): 160 XP
Tổng điểm thưởng học viên nhận được: 160 XP

Chọn chức năng (1-7): 1
--- CHỌN LOẠI BÀI HỌC KHỞI TẠO ---
1. Video Lesson (Bài giảng Video)
2. Coding Challenge (Bài thực hành Lập trình)
3. Hybrid Assessment (Bài đánh giá Tích hợp)
Chọn loại bài học (1-3): 3
Nhập mã bài học 10 ký tự: LMS0000003
Nhập tiêu đề bài học:  oop nang cao
Nhập thời lượng bài học (phút): 30
Nhập chất lượng video (VD: 720p, 1080p, 4K): 720p
Nhập số lượng testcase: 5
Nhập hệ số độ khó (VD: 1.5): 1.5
Khởi tạo bài học Hybrid Assessment thành công!
Tiêu đề bài học: OOP NANG CAO

Chọn chức năng (1-7): 2
--- THÔNG TIN BÀI HỌC HIỆN TẠI ---
Loại bài học: HybridAssessment
Nền tảng: Rikkei Academy LMS
Mã bài học: LMS0000003
Tiêu đề: OOP NANG CAO
Thời lượng: 30 phút
Số testcase: 5
Hệ số độ khó: 1.5
Chất lượng video: 720p
Lượt xem: 0 lượt
Thứ tự kế thừa (MRO): HybridAssessment -> VideoLesson -> CodingChallenge -> BaseLesson -> ABC -> object

Chọn chức năng (1-7): 3
--- CẬP NHẬT THỜI LƯỢNG & NỘI DUNG BÀI HỌC ---
1. Ghi nhận lượt xem video (Chỉ dành cho Video/Hybrid)
2. Cập nhật thông số nội dung bài học
3. Bổ sung thời lượng bài học
Chọn tác vụ (1-3): 2
Nhập số testcase cần bổ sung: 3

Cập nhật thông số thành công!
Số lượng testcase hiện tại trên hệ thống: 8 testcases.

Chọn chức năng (1-7): 3
--- CẬP NHẬT THỜI LƯỢNG & NỘI DUNG BÀI HỌC ---
1. Ghi nhận lượt xem video (Chỉ dành cho Video/Hybrid)
2. Cập nhật thông số nội dung bài học
3. Bổ sung thời lượng bài học
Chọn tác vụ (1-3): 1
Ghi nhận thành công! Học viên đã xem video bài học.
Tổng lượt xem hiện tại: 1 lượt.

Chọn chức năng (1-7): 3
--- CẬP NHẬT THỜI LƯỢNG & NỘI DUNG BÀI HỌC ---
1. Ghi nhận lượt xem video (Chỉ dành cho Video/Hybrid)
2. Cập nhật thông số nội dung bài học
3. Bổ sung thời lượng bài học
Chọn tác vụ (1-3): 3
Nhập số phút cần bổ sung: -15
Thời lượng bài học và thông số kỹ thuật không được nhỏ hơn hoặc bằng 0

Chọn chức năng (1-7): 3
--- CẬP NHẬT THỜI LƯỢNG & NỘI DUNG BÀI HỌC ---
1. Ghi nhận lượt xem video (Chỉ dành cho Video/Hybrid)
2. Cập nhật thông số nội dung bài học
3. Bổ sung thời lượng bài học
Chọn tác vụ (1-3): 3
Nhập số phút cần bổ sung: 0
Thời lượng bài học và thông số kỹ thuật không được nhỏ hơn hoặc bằng 0

Chọn chức năng (1-7): 4
--- CHI TIẾT ĐIỂM THƯỞNG HOÀN THÀNH BÀI HỌC ---
Bài học: OOP NANG CAO (Loại: HybridAssessment)
Điểm cơ sở hệ thống: 10 XP
  + Điểm cơ sở hoàn thành video: 10 XP
  + Điểm thời lượng (30 phút x 0.5): 15 XP
  + Điểm testcase (10 x 8 testcase x 1.5): 120 XP
Tổng điểm thưởng học viên nhận được: 145 XP

Chọn chức năng (1-7): 5
--- GỘP & SO SÁNH THỜI LƯỢNG BÀI HỌC (OPERATOR OVERLOADING) ---
Bài học hiện tại (A): OOP NANG CAO (Thời lượng: 30 phút)
Danh sách bài học khác:
  - LMS0000001 (PYTHON CO BAN - Thời lượng: 45 phút)
  - LMS0000002 (VONG LAP FOR - Thời lượng: 60 phút)
Chọn bài học đối ứng (B), nhập mã: LMS0000002
[Kết quả So sánh (__lt__)]: Thời lượng bài học A NGẮN HƠN thời lượng bài học B.
[Kết quả Tổng hợp (__add__)]: Tổng thời lượng của cả 2 bài học là: 90 phút.

Chọn chức năng (1-7): 6
--- ĐỒNG BỘ BÀI GIẢNG LÊN NỀN TẢNG ĐÁM MÂY ---
1. Lưu trữ trên Amazon Web Services S3
2. Lưu trữ trên Google Cloud Storage
Chọn dịch vụ đám mây (1-2): 1
[Hệ thống AWS S3]: Đang khởi tạo luồng băng thông kết nối tới LMS...
Xác thực đối tác bằng Duck Typing thành công!
Đồng bộ hoàn tất bài giảng LMS0000003 - OOP NANG CAO (30 phút) lên nền tảng đám mây.

Chọn chức năng (1-7): 6
--- ĐỒNG BỘ BÀI GIẢNG LÊN NỀN TẢNG ĐÁM MÂY ---
1. Lưu trữ trên Amazon Web Services S3
2. Lưu trữ trên Google Cloud Storage
Chọn dịch vụ đám mây (1-2): 2
[Google Cloud Storage]: Đang mã hóa và tải lên bài giảng LMS0000003...
Xác thực đối tác bằng Duck Typing thành công!
Đồng bộ hoàn tất bài giảng LMS0000003 - OOP NANG CAO (30 phút) lên nền tảng đám mây.

Chọn chức năng (1-7): 6
--- ĐỒNG BỘ BÀI GIẢNG LÊN NỀN TẢNG ĐÁM MÂY ---
1. Lưu trữ trên Amazon Web Services S3
2. Lưu trữ trên Google Cloud Storage
Chọn dịch vụ đám mây (1-2): 3
Dịch vụ lưu trữ đám mây không hợp lệ hoặc chưa kết nối chứng chỉ API liên thông

Chọn chức năng (1-7): 9
Lựa chọn không hợp lệ, vui lòng chọn từ 1-7!

Cảm ơn bạn đã trải nghiệm hệ thống Quản lý Bài học Rikkei Academy LMS Pro!
```

Kiểm tra trực tiếp các bẫy, bảo vệ thời lượng, chuỗi MRO và Class Method:

```
1) Khởi tạo trực tiếp lớp trừu tượng BaseLesson:
   TypeError: Can't instantiate abstract class BaseLesson without an implementation for abstract methods 'calculate_completion_score', 'update_content'
2) Tiêu đề / chất lượng sau chuẩn hóa: 'GIOI THIEU PYTHON' 1080p
3) Gán trực tiếp duration_minutes = 999:
   AttributeError: property 'duration_minutes' of 'VideoLesson' object has no setter
4) Toán tử với kiểu sai:
   video + 'abc' -> TypeError: unsupported operand type(s) for +: 'VideoLesson' and 'str'
   video < 100 -> TypeError: '<' not supported between instances of 'VideoLesson' and 'int'
5) Chuỗi calculate_completion_score theo MRO của Hybrid:
   MRO: HybridAssessment -> VideoLesson -> CodingChallenge -> BaseLesson -> ABC -> object
   (10 + 30 * 0.5) + 10 * 5 * 1.5 = 100.0
   update_content('3') của Hybrid đi theo nhánh Coding: ['Số lượng testcase hiện tại trên hệ thống: 8 testcases.']
6) update_base_points(20) áp dụng cho mọi bài học:
   Video: 30.0 | Hybrid: 275.0 | VideoLesson.base_completion_points = 20
7) Thông số <= 0:
   ValueError: Thời lượng bài học và thông số kỹ thuật không được nhỏ hơn hoặc bằng 0
   ValueError: Thời lượng bài học và thông số kỹ thuật không được nhỏ hơn hoặc bằng 0
   ValueError: Thời lượng bài học và thông số kỹ thuật không được nhỏ hơn hoặc bằng 0
8) Duck Typing với object không có upload_lesson:
Dịch vụ lưu trữ đám mây không hợp lệ hoặc chưa kết nối chứng chỉ API liên thông
   Với AWS S3:
[Hệ thống AWS S3]: Đang khởi tạo luồng băng thông kết nối tới LMS...
Xác thực đối tác bằng Duck Typing thành công!
Đồng bộ hoàn tất bài giảng LMS0000002 - OOP (30 phút) lên nền tảng đám mây.
9) validate_lesson_code: [True, False, False, False]
10) sorted() dùng __lt__: ['LMS0000001', 'LMS0000002']
```

### Bảng kiểm thử

| Kịch bản | Dữ liệu | Kết quả |
|---|---|---|
| Chưa có bài học | Chọn 3 | Báo lỗi, yêu cầu khởi tạo |
| Mã sai | LMS12 | Mã bài học không hợp lệ! ... |
| Chuẩn hóa tiêu đề | "  python   co ban  " | PYTHON CO BAN |
| Đổi độ phân giải | 4K / 8K | Thành công / không hỗ trợ |
| Điểm Video | 45 phút | 10 + 22.5 = 32.5 XP |
| Coding xem video | Tác vụ 1 | Chỉ dành cho Video / Hybrid |
| Bổ sung testcase | 5 + 3 | 8 testcases; điểm 10 × 8 × 2 = 160 XP |
| Thời lượng ≤ 0 | -15 / 0 | Bẫy 2: thông báo lỗi |
| Điểm Hybrid | 30 phút, 8 testcase, hệ số 1.5 | 10 + 15 + 120 = 145 XP |
| Gộp / so sánh | 30 vs 60 phút | A NGẮN HƠN B; tổng 90 phút |
| Duck Typing | AWS / Google / dịch vụ 3 | Đồng bộ thành công / thông báo dịch vụ không hợp lệ |
| Bẫy 1, 3 | BaseLesson(), video + 'abc', video < 100 | TypeError |

## Ghi chú

- Thời lượng được nhập khi khởi tạo và ghi vào thuộc tính private qua `add_duration()` (không có setter).
- Độ phân giải hợp lệ: 360p, 480p, 720p, 1080p, 2K, 4K (không phân biệt hoa thường).
- Điểm cơ sở `base_completion_points` được cộng cho phần video, đồng thời là hệ số nhân trong phần coding; `update_base_points()` đổi giá trị ở `BaseLesson` nên áp dụng cho mọi loại bài học.
- Bài Hybrid cập nhật nội dung theo nhánh Coding (bổ sung testcase); muốn đổi độ phân giải có thể gọi `VideoLesson.update_content(lesson, ...)`.

## Cách chạy

```bash
python main.py
```
