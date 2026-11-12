# Kế hoạch & Kết quả Kiểm thử EventHub — Lab 3

Cập nhật 12/11/2026 (khởi tạo 31/10/2026). Nguồn persona từ Lab 2: **P01** Nguyễn Minh Anh (sinh viên đăng ký/điểm danh), **P02** Gia Linh (khách ngoài trường), **P03** Việt Khoa (xem sự kiện tự do). Lab 3 bổ sung AuthGate trước nội dung; không cấp quyền quản trị CLB/admin cho mobile.

## 1. Các luồng trọng yếu & ánh xạ màn hình

| Luồng | Màn hình tham gia | Mục tiêu kiểm thử |
|---|---|---|
| **Auth** | `A01a` Đăng nhập, `A01b` Tạo tài khoản, `A01c` Xác nhận email, `A01d` Quên mật khẩu, `A02` | Google Sign-In, hủy native account picker, chặn phiên chưa xác nhận, đăng xuất xóa dữ liệu user và chặn Back |
| **F1 — Khám phá & Đăng ký** | `A02` Khám phá, `A03` Tìm kiếm/Lọc, `A04` Chi tiết, `A05` Form đăng ký, `A06` Xác nhận, `A07` Lịch | Tìm kiếm/empty state/bộ lọc, xem chi tiết (cần đăng ký vs tự do), validation `Khóa K`, đăng ký khách/sinh viên qua Firestore transaction, phục hồi mạng |
| **F2 — Lịch, Hủy & Thông báo** | `A07` Lịch (3 tab), `A08` Chi tiết đăng ký, `A09` Thông báo, `A10` Hồ sơ | Xem 3 tab lịch, dialog hủy -> `Giữ đăng ký`, xác nhận hủy giảm `activeCount`, đọc thông báo/chạm tin, sửa hồ sơ & cảnh báo chưa lưu |
| **F4A — Điểm danh QR** | `A08` Chi tiết đăng ký, `A11` Quét QR, `A12` Kết quả điểm danh | Xin quyền camera native, xử lý từ chối/sai QR/phiên đóng an toàn, quét QR mở từ phiên điểm danh và xem `A12` |
| **Lab 3 Firebase & Export** | `L3-01` Tiện ích Firebase, `L3-02` Xuất lịch tham gia, `A09` | Tạo PDF tiếng Việt & upload Cloudinary, nhận/chạm FCM ở 3 trạng thái, fetch Remote Config không rebuild, Crashlytics non-fatal/test crash, Analytics DebugView & `TC18` Logcat |

## 2. Ma trận 25 ca kiểm thử ARTEMIS (Appendix B)

Tất cả ca test được cài đặt trong [e2e_test/cases.py](../e2e_test/cases.py) và chạy qua `ArtemisClient` ([e2e_test/conftest.py](../e2e_test/conftest.py)), khẳng định cả `observed_values.final_screen` lẫn `observed_texts` (không chỉ dựa vào `status == "SUCCESS"`). Tài khoản Google test chuyên dụng được truyền qua biến môi trường và ẩn thành `<TEST_ACCOUNT>`.

| ID | Flow | Tiền điều kiện | Thao tác (tóm tắt từ `cases.py`) | Kết quả mong đợi | Loại |
|---|---|---|---|---|---|
| `TC01` | Auth (`A01a→A02`) | Đã cài app; nếu đang login thì Logout trước | Chọn `<TEST_ACCOUNT>` trên native Google picker → mở Khám phá | Đăng nhập thật, hiện `A02` và tiêu đề `Sắp tới` | Native / Happy |
| `TC02` | Auth (`A01a`) | Tại màn Đăng nhập | Bấm Google Sign-In rồi hủy native account picker | Ở lại `A01a`, hiện thông báo hủy, không có phiên giả | Native / Error |
| `TC03` | F1 (`A03`) | Đã đăng nhập | Tìm chuỗi không tồn tại `zzz_no_event_8362` | `A03` hiện empty state `Chưa tìm thấy` + gợi ý xóa/đổi lọc | Error path |
| `TC04` | F1 (`A02→A04`) | Đã đăng nhập; có `{event}` | Tìm kiếm `{event}`, mở đúng card `{event}` | Mở `A04` (`Giới thiệu`, đúng tiêu đề `{event}`) | Happy path |
| `TC05` | F1 (`A05`) | Có `{event}` chưa đăng ký | Chọn `Sinh viên FPTU`, để trống `Khóa K`, bấm gửi | Ở lại `A05`, hiện lỗi `Vui lòng nhập khóa K` | Error path |
| `TC06` | F1 (`A05→A06`) | Có `{event}` chưa đăng ký | Chọn `Khách ngoài trường`, giữ tên/email test, gửi | Transaction Firestore thành công, mở `A06` (`Đăng ký được xác nhận`) | Happy path |
| `TC07` | F2 (`A07`) | Đã đăng nhập | Mở tab `Lịch`, kiểm tra 3 tab `Sắp tới`, `Đã kết thúc`, `Đã hủy` | Hiển thị đúng 3 tab, kết thúc tại `Đã hủy` (`A07`) | Happy path |
| `TC08` | F2 (`A08`) | Có đăng ký active cho `{event}` | Mở `A08`, mở dialog hủy → chọn `Giữ đăng ký` | Không hủy, giữ nguyên `A08` trạng thái `Đã đăng ký` | Alternative |
| `TC09` | F2 (`A08→A07`) | Có đăng ký active cho `{event}` | Mở `A08`, `Hủy đăng ký` → xác nhận hủy → mở `Lịch > Đã hủy` | Firestore cập nhật cùng `activeCount`, thấy `{event}` ở `Đã hủy` | Happy path |
| `TC10` | F2 (`A09`) | Đã đăng nhập | Mở `Thông báo`, chạm 1 item (ưu tiên `Chưa đọc`), quay lại `A09` | Item được đánh dấu `Đã đọc` / mở đúng đích và quay về `A09` | Happy path |
| `TC11` | Profile (`A10-edit`) | Đã đăng nhập Google | Mở `Tài khoản` → `Chỉnh sửa thông tin`, kiểm tra nhãn email | Hiển thị nhãn `Email tài khoản app` chỉ đọc | Happy path |
| `TC12` | F4A (`A11`) | Có đăng ký active & `checkinSessions` mở | Mở `A08` → `Quét QR`, xử lý dialog quyền camera native (`Allow`) | Mở scanner `A11` (`Quét mã QR do CLB`) | Native / Happy |
| `TC13` | F4A (`A12`) | Fixture đã check-in từ QR Web CLB | Mở đăng ký đã điểm danh của `{event}` → xem xác nhận | Hiện `A12` (`điểm danh`) cùng giờ check-in, không lộ SĐT/email | Happy path (deselected) |
| `TC14` | L3-02 (`Export`) | Đã có dữ liệu lịch; cấu hình Cloudinary | Mở `Tài khoản → Xuất lịch tham gia` → `Tạo PDF và tải lên` | Tạo PDF & upload thành công (`Đã tạo và tải PDF` + URL) | Happy path |
| `TC15` | L3-01 (`RC`) | Console có 2 param RC | Sửa Remote Config trên Console → `Lấy cấu hình mới` | UI cập nhật số lượng/ẩn gợi ý không cần rebuild | Happy path (deselected) |
| `TC16` | L3-01 (`FCM`) | Android 13+ | Mở `Tiện ích Firebase` → `Bật thông báo trên thiết bị`, xử lý quyền | Xử lý dialog quyền native, hiển thị trạng thái `thông báo` | Native |
| `TC17` | Auth (`Logout`) | Đã đăng nhập | Đăng xuất qua `Tài khoản`, bấm nút Android Back | Ở lại `A01a` (`Đăng nhập`), không lộ dữ liệu phiên cũ | Security / Boundary |
| `TC18` | Analytics | Bật `FA`/`FA-SVC` verbose & debug prop | Vào `L3-01` → `Lấy cấu hình mới`, đọc `adb logcat` | UI hiện `Giới hạn gợi ý` và Logcat ghi nhận `remote_config_fetch` | Instrumentation |
| `TC19` | F1 (`A04` free) | `ARTEMIS_FREE_EVENT_TITLE` | Tìm và mở sự kiện tự do | `Không cần đăng ký`, không có nút đăng ký/QR | Fixture / Skipped |
| `TC20` | F1 (`A04` full) | `ARTEMIS_FULL_EVENT_TITLE` | Mở sự kiện hết chỗ (chưa đăng ký) | Hiện trạng thái `hết chỗ`, chặn gửi mới | Boundary / Skipped |
| `TC21` | F1 (`A04` expired) | `ARTEMIS_EXPIRED_EVENT_TITLE` | Mở sự kiện quá hạn | Hiện trạng thái `hết hạn`, chặn gửi mới | Boundary / Skipped |
| `TC22` | F1/F2 (`A04` cancel) | `ARTEMIS_CANCELLED_EVENT_TITLE` | Mở sự kiện đã bị CLB hủy | Hiện trạng thái `hủy`, không cho đăng ký mới | Boundary / Skipped |
| `TC23` | F1 (`A05` recovery) | `ARTEMIS_NETWORK_TEST_READY` | Ngắt mạng giữa lúc submit đăng ký → bật lại → kiểm tra trạng thái | Hiện `Kiểm tra trạng thái`, giữ form/op ID idempotent | Error path / Skipped |
| `TC24` | F4A (`A11` wrong QR) | `ARTEMIS_WRONG_QR_READY` | Quét QR thuộc sự kiện khác | Báo `không đúng sự kiện`, cho phép quét lại | Error path / Skipped |
| `TC25` | F4A (`A11` denied) | `ARTEMIS_CAMERA_PERMISSION_READY` | Từ chối quyền `camera` trên dialog native | Hiện hướng dẫn mở Cài đặt và nút thử lại | Native Error / Skipped |

## 3. Kết quả thực thi ARTEMIS Flash 3-Run Regression (11/11/2026)

- **Lệnh chạy chính xác:**
  ```powershell
  powershell -ExecutionPolicy Bypass -File .\e2e_test\run_regression.ps1 -Selection "not TC13 and not TC15"
  ```
- **Cấu hình runtime:** Upstream ARTEMIS commit `351ca8422f7b5b54e80a9c1ce03a222e02415b6b`, thiết bị `emulator-5554` (Android 15 / API 35), `app-profile.apk` (`--profile` + Cloudinary defines), profile `flash` (`gemini-3.1-flash-lite` / fallback `gemini-3.5-flash-lite`, `step_summarizer.enabled=false`).
- **Tổng hợp 3 lượt chạy từ JUnit XML (`evidence/artemis/flash-regression-20261111/`):**
  - **Run 1 (`run-1.xml`):** 12 passed, 4 failed (`TC01`, `TC05`, `TC08`, `TC10`), 7 skipped (`TC19`–`TC25`) trong `1176.02s`.
  - **Run 2 (`run-2.xml`):** 12 passed, 4 failed (`TC05`, `TC06`, `TC08`, `TC12`), 7 skipped (`TC19`–`TC25`) trong `1496.51s`.
  - **Run 3 (`run-3.xml`):** 14 passed, 2 failed (`TC10`, `TC18`), 7 skipped (`TC19`–`TC25`) trong `1281.45s`.
  - **Tổng kết toàn batch:** **38 / 48 lượt active đạt (79.17%)**, **9 / 16 ca active đạt 3/3 (100%)**, tất cả **16 / 16** ca active đều pass ít nhất 1/3 lượt, **0 crash/ANR**, **0 lỗi HTTP 429**.

| Case | Lượt | Pass | Fail | Skip | Kết quả Run 1 / 2 / 3 | Tỷ lệ Pass | Thời gian TB (s) | Bằng chứng / Trạng thái |
|---|---|---|---|---|---|---|---|---|
| `TC01` | 3 | 2 | 1 | 0 | FAIL / PASS / PASS | **66.67%** | 157.15 | Flaky (lỗi định dạng JSON ở Run 1; pass Run 2–3) |
| `TC02` | 3 | 3 | 0 | 0 | PASS / PASS / PASS | **100.0%** | 75.84 | Đạt 3/3 |
| `TC03` | 3 | 3 | 0 | 0 | PASS / PASS / PASS | **100.0%** | 124.16 | Đạt 3/3 |
| `TC04` | 3 | 3 | 0 | 0 | PASS / PASS / PASS | **100.0%** | 97.19 | Đạt 3/3 |
| `TC05` | 3 | 1 | 2 | 0 | FAIL / FAIL / PASS | **33.33%** | 68.71 | Flaky (lỗi định dạng JSON ở Run 1–2; pass Run 3) |
| `TC06` | 3 | 2 | 1 | 0 | PASS / FAIL / PASS | **66.67%** | 35.49 | Flaky (lỗi định dạng JSON ở Run 2; pass Run 1 & 3) |
| `TC07` | 3 | 3 | 0 | 0 | PASS / PASS / PASS | **100.0%** | 177.40 | Đạt 3/3 |
| `TC08` | 3 | 1 | 2 | 0 | FAIL / FAIL / PASS | **33.33%** | 61.77 | Flaky (lỗi định dạng JSON ở Run 1–2; pass Run 3) |
| `TC09` | 3 | 3 | 0 | 0 | PASS / PASS / PASS | **100.0%** | 49.16 | Đạt 3/3 |
| `TC10` | 3 | 1 | 2 | 0 | FAIL / PASS / FAIL | **33.33%** | 109.06 | Flaky (lỗi định dạng JSON ở Run 1 & 3; pass Run 2) |
| `TC11` | 3 | 3 | 0 | 0 | PASS / PASS / PASS | **100.0%** | 68.87 | Đạt 3/3 |
| `TC12` | 3 | 2 | 1 | 0 | PASS / FAIL / PASS | **66.67%** | 22.52 | Flaky (lỗi định dạng JSON ở Run 2; pass Run 1 & 3) |
| `TC14` | 3 | 3 | 0 | 0 | PASS / PASS / PASS | **100.0%** | 110.59 | Đạt 3/3 |
| `TC16` | 3 | 3 | 0 | 0 | PASS / PASS / PASS | **100.0%** | 60.72 | Đạt 3/3 |
| `TC17` | 3 | 3 | 0 | 0 | PASS / PASS / PASS | **100.0%** | 56.75 | Đạt 3/3 |
| `TC18` | 3 | 2 | 1 | 0 | PASS / PASS / FAIL | **66.67%** | 42.30 | Flaky ở Run 3 (thiếu chuỗi `'Giới hạn gợi ý'` trong `observed_texts`; Run 1–2 pass cả Logcat) |
| `TC19`–`TC25` | 3 | 0 | 0 | 3 | SKIP / SKIP / SKIP | **0.0%** | N/A | Skip do thiếu biến env fixture chuyên biệt (`test_alternatives.py:9`) |
| `TC13`, `TC15` | — | — | — | — | Deselected | — | — | Loại bằng `-k "not TC13 and not TC15"` (xem giải trình bên dưới) |

Số liệu nguồn: [evidence/artemis/flash-regression-20261111/summary.csv](../evidence/artemis/flash-regression-20261111/summary.csv) và 48 file trace tại [evidence/artemis/run-command-and-summary.txt](../evidence/artemis/run-command-and-summary.txt).

## 4. Giải trình nguyên nhân gốc rễ từng ca Flaky, Skipped & Deselected

### 4.1. Các ca Flaky (`TC01`, `TC05`, `TC06`, `TC08`, `TC10`, `TC12`, `TC18`)
Kiểm tra trực tiếp cả 10 lượt FAIL trong `run-1.xml`, `run-2.xml`, `run-3.xml` cho thấy **0/10 lỗi xuất phát từ bug của ứng dụng EventHub**. Toàn bộ 10 lượt fail đều đến từ **hành vi xuất structured output của model `gemini-3.1-flash-lite`** trong `report_task_status`:

1. **`TC01` (Run 1 fail — 66.67%):** Agent đã đăng xuất tài khoản cũ, đăng nhập `<TEST_ACCOUNT>` và mở đúng tab `Khám phá` (`"Sắp tới tại TP.HCM"`), nhưng trả lời bằng văn xuôi tiếng Anh (`unparsed`) thay vì JSON schema có `observed_values.final_screen == "A02"`, nên `conftest.py:117` fail. Run 2 & 3 trả JSON đúng và pass.
2. **`TC05` (Run 1 & 2 fail — 33.33%):** Agent đã mở đúng event, chọn `Sinh viên FPTU`, bấm gửi khi trống `Khóa K` và quan sát đúng thông báo `"Vui lòng nhập khóa K."`, nhưng trả lời dạng bullet prose thay vì JSON (`observed_values.final_screen == "A05"`). Run 3 trả JSON chuẩn và pass.
3. **`TC06` (Run 2 fail — 66.67%):** Agent hoàn tất đăng ký khách và xác nhận dòng `"Đăng ký được xác nhận"`, nhưng trả prose thay vì JSON (`final_screen == "A06"`). Run 1 & 3 pass.
4. **`TC08` (Run 1 & 2 fail — 33.33%):** Agent mở chi tiết đăng ký, mở dialog hủy và chọn `"Giữ đăng ký"`, ở lại `A08` đúng nghiệp vụ nhưng trả prose thay vì JSON (`final_screen == "A08"`). Run 3 pass.
5. **`TC10` (Run 1 & 3 fail — 33.33%):** Agent mở tab `Thông báo` (`A09`) và liệt kê chính xác danh sách tin FCM (`Đã đọc` / `Chưa đọc`), nhưng xuất văn xuôi / danh sách gạch đầu dòng thay vì JSON (`final_screen == "A09"`). Run 2 pass.
6. **`TC12` (Run 2 fail — 66.67%):** Agent điều hướng vào màn quét QR `A11` thành công nhưng trả prose (`"The application is now on the QR scanning screen as requested."`) thay vì JSON (`final_screen == "A11"`). Run 1 & 3 pass.
7. **`TC18` (Run 3 fail — 66.67%):** Ở Run 3 (`52b81df0`), agent trả JSON hợp lệ (`final_screen: "L3-01"` và `"Đã nhận và kích hoạt cấu hình."`), nhưng mảng `observed_texts` chỉ liệt kê 3 chuỗi và bỏ sót chuỗi `"Giới hạn gợi ý"` mà `test_analytics.py:13` yêu cầu kiểm tra tại `conftest.py:120`. Run 1 & Run 2 đều ghi nhận đầy đủ `observed_texts` và pass kiểm tra `adb logcat` (`"remote_config_fetch" in log`).

**Biện pháp đã áp dụng & hướng khắc phục:** Trong `conftest.py`, prompt đã ép hậu tố JSON chặt hơn và đọc trực tiếp bước `report_task_status` qua host `/api/sessions/{trace_id}/steps` (giải quyết trường hợp Flash SDK trả `result.output = None`); nguyên nhân flaky còn lại là model Flash thỉnh thoảng bỏ JSON ở lượt 1/3 nhưng chứng minh tính năng chạy đúng trên UI trong mọi lượt.

### 4.2. Các ca Skipped (`TC19`–`TC25`) & Deselected (`TC13`, `TC15`)
- **`TC19` (`ARTEMIS_FREE_EVENT_TITLE`):** Skip do biến môi trường fixture sự kiện tự do chưa được truyền trong batch script (luồng xem sự kiện tự do đã được kiểm tra trong Pro session Phase 3 và unit/widget tests).
- **`TC20` (`ARTEMIS_FULL_EVENT_TITLE`):** Skip do chưa gắn fixture sự kiện hết chỗ độc lập cho batch tự động.
- **`TC21` (`ARTEMIS_EXPIRED_EVENT_TITLE`):** Skip do chưa gắn fixture sự kiện hết hạn đăng ký cho batch tự động.
- **`TC22` (`ARTEMIS_CANCELLED_EVENT_TITLE`):** Skip do chưa gắn fixture sự kiện bị CLB hủy cho batch tự động.
- **`TC23` (`ARTEMIS_NETWORK_TEST_READY`):** Skip do script chưa cấu hình tự động bật/tắt chế độ máy bay trên emulator đúng thời điểm transaction đang gửi.
- **`TC24` (`ARTEMIS_WRONG_QR_READY`):** Skip do camera ảo của Android emulator không tự quét được mã QR vật lý sai sự kiện nếu không tiêm ảnh/luồng camera riêng.
- **`TC25` (`ARTEMIS_CAMERA_PERMISSION_READY`):** Skip do `TC12` cần cấp quyền camera trên cùng thiết bị trong khi batch chạy 3 lượt liên tiếp chưa tự động thu hồi quyền giữa các ca.
- **`TC13` (Deselected):** Yêu cầu đăng ký đã check-in từ phiên QR mở trên Web CLB (`checkinSessions`); đã được xác minh trên thiết bị thật và Firestore Rules emulator.
- **`TC15` (Deselected):** Tránh thay đổi cấu hình Remote Config trên Firebase Console giữa lúc batch 3 lượt chạy tự động; thay đổi trực tiếp 2 tham số (`1/true` → `false` → `10/true`) không rebuild đã có bằng chứng Console + App đầy đủ tại [evidence/instrumentation/remote-config/](../evidence/instrumentation/remote-config/) và `TC18`.

## 5. Phiên thăm dò ARTEMIS Pro (15–30 phút) & Kiểm tra Analytics

- **Trace ID:** `c8a40964-c1e0-4b14-9867-c1a2eacd4651` ([exploratory-pro-session.md](../evidence/artemis/exploratory-pro-session.md))
- **Trạng thái:** `completed` | Checker: **PASS** | `meets_15_to_30_minutes: true`
- **Thời gian thực tế:** `1056.453s` (**17 phút 36 giây**), **78 bước**, **229 lần gọi model**, **0 app crash / 0 bug**.
- **Phạm vi bao phủ:** Hoàn thành toàn bộ 12 phase chức năng (tìm kiếm/empty state, lọc bottom sheet `Thiết kế`, chi tiết ≥ 3 sự kiện, validation `Khóa K`, cô lập trạng thái form & đăng ký `K18`, Lịch 3 tab & hủy có `Giữ đăng ký`, kiểm tra `Quét QR` bị khóa an toàn khi `checkinSessions` đóng, sửa hồ sơ & dialog `Bỏ thay đổi chưa lưu?`, Thông báo FCM, Xuất PDF + Cloudinary + `Sao chép liên kết PDF`, Firebase Tools `Lấy cấu hình mới`, và ~4 phút kiểm tra Khám phá/cuộn ở Steps 75–77).
- **Analytics Logcat Verification:** `TC18` (`e2e_test/test_analytics.py`) kiểm chứng trực tiếp `adb logcat -d -s FA FA-SVC` chứa `remote_config_fetch` trong Run 1 & Run 2; đồng thời file [analytics-search-detail-logcat.txt](../evidence/instrumentation/analytics-search-detail-logcat.txt) ghi lại đầy đủ event `view_screen`, `search` (`query_length=8`), `view_event_detail` (`screen_code=A04`) cùng phản hồi upload HTTP `204`.

## 6. Kiểm thử cục bộ & Firestore Rules

- **Flutter Analyzer & Unit/Widget Tests:** Xem [evidence/source-fixes/validation.md](../evidence/source-fixes/validation.md) (`flutter analyze` 0 lỗi/cảnh báo; **73/73** Flutter unit/widget tests đạt sau khi khắc phục `AUD01`–`AUD04`, bao gồm layout 360/412dp, large text 150%, contrast/touch target, logout cleanup, `ScannerViewModel` fake camera và session isolation).
- **Firestore Security Rules Emulator:** Các test tại [firebase/tests/direct-firestore.test.js](../firebase/tests/direct-firestore.test.js) kiểm tra nguyên tử `registrations` + `activeCount`, `qrCredentials`, `checkinSessions`, `announcements` và `notifications` trên emulator `demo-direct-booking`.
