# Analytics event plan — EventHub Lab 3

Lập trước khi thêm tracking (31/10/2026), cập nhật trạng thái bằng chứng DebugView ngày 12/11/2026.

Nguyên tắc thiết kế:
- Analytics không được làm thất bại nghiệp vụ; mọi lời gọi đều đi qua `AnalyticsService` contract và được inject qua Riverpod.
- **Không gửi PII:** tuyệt đối không gửi email, họ tên, số điện thoại, QR token, URL download, nội dung chuỗi tìm kiếm hay registration ID.
- Firebase `user_id` được gán bằng UID giả danh sau khi đăng nhập thành công (`setUserId`) và xóa về `null` khi đăng xuất.
- `result` / `action` / `screen_code` sử dụng enum kiểm soát; các tham số đếm (`query_length`, `row_count`, `byte_count`) là kiểu `int`.

## Bảng kế hoạch 14 event & trạng thái DebugView

| Event | Flow Lab 2 / Trigger | Tham số và kiểu | Câu hỏi sản phẩm trả lời | Bằng chứng DebugView hiện tại |
|---|---|---|---|---|
| `login` | Auth: xác nhận đăng nhập thành công | `method: string` (`google` / `password`) | Người dùng chọn phương thức đăng nhập nào và tỷ lệ quay lại? | **Đã chụp** ([login.jpg](../evidence/instrumentation/analytics/login.jpg): `method=google`, có `user_id`) |
| `logout` | Auth: người dùng đăng xuất chủ động | `method: string` (`manual`) | Phiên sử dụng kết thúc qua đăng xuất thủ công ra sao? | **Đã chụp** ([logout.png](../evidence/instrumentation/analytics/logout.png): `method=manual`) |
| `search` | F1 (`A02`/`A03`): gửi truy vấn tìm kiếm | `query_length: int` | Người dùng có sử dụng tìm kiếm và độ dài từ khóa trung bình là bao nhiêu? | **Đã chụp** ([search-query-length-8.png](../evidence/instrumentation/analytics/search-query-length-8.png): `query_length=8`) |
| `view_event_detail` | F1 (`A04`): mở chi tiết sự kiện | `screen_code: string` (`A04`) | Có bao nhiêu lượt xem chi tiết sự kiện so với lượt tìm kiếm? | **Đã chụp** ([view-event-detail-A04.png](../evidence/instrumentation/analytics/view-event-detail-A04.png): `screen_code=A04`) |
| `view_registration_detail` | F2 (`A08`): mở chi tiết đăng ký | `screen_code: string` (`A08`) | Người dùng truy cập chi tiết đăng ký để theo dõi/hủy/quét QR nhiều không? | **Đã chụp** ([view-registration-detail-A08.png](../evidence/instrumentation/analytics/view-registration-detail-A08.png): `screen_code=A08`) |
| `view_checkin_result` | F4A (`A12`): mở màn kết quả điểm danh | `screen_code: string` (`A12`) | Có bao nhiêu lượt mở lại hoặc hoàn tất màn kết quả điểm danh? | **Chờ chụp DebugView** (cần ca check-in QR thực với `checkinSessions` mở) |
| `booking_submit` | F1/F2/F4A: gửi lệnh đăng ký, hủy hoặc check-in | `action: string` (`register` / `cancel` / `checkin`) | Tần suất bắt đầu từng hành động nghiệp vụ là bao nhiêu? | **Đã chụp** ([booking-submit-register.png](../evidence/instrumentation/analytics/booking-submit-register.png): `action=register`) |
| `booking_result` | F1/F2/F4A: nhận kết quả từ Firestore | `action: string`, `result: string` (`confirmed` / `rejected` / `unknown`) | Tỷ lệ thành công, bị từ chối theo rule hay rơi vào trạng thái chưa rõ? | **Đã chụp** ([booking-result-register.png](../evidence/instrumentation/analytics/booking-result-register.png), [booking-result-confirmed.png](../evidence/instrumentation/analytics/booking-result-confirmed.png): `action=register`, `result=confirmed`) |
| `booking_recover` | F1/F2/F4A: người dùng bấm kiểm tra lại kết quả chưa rõ | `action: string` (`register` / `cancel` / `checkin`) | Mức độ người dùng phải dùng cơ chế phục hồi mạng (retry idempotent)? | **Chờ chụp DebugView** (cần ca ngắt mạng giữa lúc submit) |
| `export_generate` | L3-02: tạo file PDF lịch tham gia thành công | `row_count: int` | Tính năng xuất PDF lịch có được dùng và trung bình xuất bao nhiêu dòng? | **Đã chụp** ([export-generate-row-count-2.png](../evidence/instrumentation/analytics/export-generate-row-count-2.png): `row_count=2`) |
| `export_upload` | L3-02: upload PDF lên Cloudinary hoàn tất | `byte_count: int` | Dung lượng và tần suất upload báo cáo thành công là bao nhiêu? | **Đã chụp** ([export-upload-byte-count-13803.png](../evidence/instrumentation/analytics/export-upload-byte-count-13803.png): `byte_count=13803`) |
| `notification_open` | F2 (`A09` / FCM): chạm thông báo | `source: string` (`in_app` / `push`) | Thông báo trong inbox hay push ngoài hệ thống dẫn người dùng quay lại tốt hơn? | **Chờ chụp DebugView** (đã sửa code phát `source=push` ở `599b4c4`, cần chụp DebugView sau cài bản mới) |
| `remote_config_fetch` | L3-01: fetch & activate Remote Config | `result: string` (`success` / `error`) | Ứng dụng có nhận và kích hoạt cấu hình mới từ xa thành công không? | **Đã chụp** ([remote-config-fetch.png](../evidence/instrumentation/analytics/remote-config-fetch.png): `result=success`; kèm `TC18` Logcat) |
| `view_screen` | Điều hướng giữa các màn hình chính | `screen_code: string` (`A01a`–`d`, `A02`–`A12`, `LAB3_*`) | Hành trình chuyển màn của người dùng và điểm rời bỏ trong từng flow? | **Đã chụp** ([view-screen-A01a.png](../evidence/instrumentation/analytics/view-screen-A01a.png): `screen_code=A01a`; [user-id-and-view-screen.jpg](../evidence/instrumentation/analytics/user-id-and-view-screen.jpg): `user_id=H8DqKH45nOa27YF1RQ3haCXi2UA3`) |

> **Tổng kết bằng chứng Analytics (12/11/2026):** **11/14 event** đã có ảnh chụp Google Analytics DebugView trên property `eventhub-group4` kèm đầy đủ tham số và `user_id`. **3 event** còn thiếu ảnh DebugView (`view_checkin_result`, `booking_recover`, `notification_open`) được ghi nhận trung thực là đang chờ chụp trong lần test thiết bị thực có fixture QR / ngắt mạng / push bản build mới.

## Quy trình DebugView & Logcat verification

1. Bật DebugView trên thiết bị/emulator Android:
   ```powershell
   adb shell setprop debug.firebase.analytics.app com.eventhub.app
   adb shell setprop log.tag.FA VERBOSE
   adb shell setprop log.tag.FA-SVC VERBOSE
   ```
2. Chạy thao tác hoặc chạy test tự động `TC18` (`e2e_test/test_analytics.py`). Kiểm tra log `FA-SVC` xác nhận upload HTTP `204` ([analytics-search-detail-logcat.txt](../evidence/instrumentation/analytics-search-detail-logcat.txt)) và chụp DebugView tại Firebase/GA4 Console.
3. Tắt debug mode sau khi kiểm thử:
   ```powershell
   adb shell setprop debug.firebase.analytics.app .none.
   ```

## Quy ước Screen Identity & Privacy sau audit

- Screen identity được quản lý tập trung tại `lib/utils/screen_identity.dart`: `A01a`–`A01d` riêng biệt; `A11` quét QR; `LAB3_EXPORT` và `LAB3_FIREBASE` dành cho khu demo Lab 3. Route khởi tạo/không hợp lệ không phát `view_screen`. Không đưa ID thực thể hoặc chuỗi tìm kiếm vào `screen_code`.
- `notification_open` (cập nhật commit `599b4c4`, `AUD04`) phát `source=push` khi `onMessageOpenedApp` / `getInitialMessage` được xử lý với UID hợp lệ, và phát `source=in_app` khi chạm một mục trong inbox. Foreground receipt không tự phát `notification_open`.
- Xem chi tiết bảng tổng hợp bằng chứng tại [evidence/instrumentation/status.md](../evidence/instrumentation/status.md).
