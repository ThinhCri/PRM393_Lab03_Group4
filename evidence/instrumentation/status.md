# Instrumentation & Cloud Evidence — Cập nhật 12/11/2026

Tổng hợp bằng chứng đã kiểm tra trực tiếp trên ảnh chụp Console, ảnh app Android, ADB Logcat và ARTEMIS traces trong repository. Không tạo kết quả Console giả; mọi ảnh gốc đều được lưu tại `evidence/` và đã rà soát để không đưa API key hay email cá nhân dạng text vào tài liệu.

| Hạng mục | Đã xác minh | Còn thiếu / Ghi chú trung thực |
|---|---|---|
| Auth | 4 ảnh tại [auth/](../auth/): signed-out (A01a), hủy Google picker (hiển thị thông báo hủy), signed-in (A02), và Firebase Console `Authentication -> Users` (`eventhub-group4`) | Đã đủ bộ bằng chứng signed-out, cancel, signed-in và Users Console |
| Export / Cloudinary | 4 ảnh tại [export/](../export/): app L3-02 tạo & upload PDF (2 mục), mở PDF tiếng Việt trên trình duyệt (không chứa email/SĐT), Cloudinary Media Library (`qcfqv5oj`), và unsigned preset `eventhub_lab3_pdf_test` | Giảng viên cho phép dùng Cloudinary Free thay Firebase Storage; tuy nhiên URL public chưa giới hạn đọc theo UID (đã ghi cảnh báo trên UI; `firebase/storage.rules` giữ lại trong repo để đặc tả rule `reports/{uid}/...`) |
| Remote Config | 5 ảnh tại [remote-config/](remote-config/): baseline (`10`/`true`), limit `1`/`true` (1 thẻ), `false` (ẩn danh sách gợi ý), và khôi phục `10`/`true` trên app đang chạy không cần rebuild; kèm DebugView `remote_config_fetch` (`result=success`) | Đã đủ before/after Console + App |
| Analytics | **11/14 event** trong [analytics-plan.md](../../docs/analytics-plan.md) đã có ảnh DebugView kèm tham số riêng và `user_id` (`H8DqKH45nOa27YF1RQ3haCXi2UA3`) tại [analytics/](analytics/); kèm log `FA-SVC` HTTP 204 | Còn **3 event chưa có ảnh DebugView**: `view_checkin_result`, `booking_recover`, `notification_open` |
| Crashlytics | 11 ảnh tại [crashlytics/](crashlytics/): Native test crash (`FirebaseCrashlyticsTestCrash`), manual non-fatal, và lỗi upload thực `report_upload_failed` khi offline; đều có `user_id` và custom key `app_flow=eventhub` | Lỗi `unhandled_platform_error` cũ ở ảnh đầu tiên được tách riêng, không dùng làm bằng chứng test crash |
| FCM | 7 ảnh tại [fcm/](fcm/): nhận tin ở đủ 3 trạng thái (foreground, background, terminated với `pidof` rỗng trước gửi), lưu inbox, và chạm thông báo mở đúng tab Thông báo (`router.go('/notifications')`) | Tin Console chung chưa xác minh deep link tới `eventId` cụ thể hoặc hộp thoại cấp quyền lần đầu sau cài mới |
| ARTEMIS E2E | Flash 3-run regression đạt **38/48 = 79.17%** (9/16 ca 100%, 0 crash/ANR) + Pro exploratory `c8a40964` **PASS** (`17m 36s`, 78 steps, 0 app bugs) + `TC18` Logcat `remote_config_fetch` pass 2/3 lượt | `TC19–TC25` skip do thiếu env fixture; `TC13` (F4A check-in) & `TC15` (RC live toggle) deselect; `Quét QR` bị vô hiệu an toàn khi `checkinSessions` đóng |

## 1. Auth (`evidence/auth/`)

- `01-mobile-signed-out.png`: Màn A01a Đăng nhập khi chưa có phiên (email/mật khẩu + Google + Tạo tài khoản).
- `02-mobile-google-cancelled.png`: Phản hồi rõ ràng `"Bạn đã hủy đăng nhập Google."` trên A01a khi người dùng hủy native picker, không tạo phiên giả.
- `03-mobile-signed-in-home.jpg`: Sau đăng nhập Google thành công, điều hướng vào A02 Khám phá với dữ liệu sự kiện thật từ Firestore.
- `04-console-auth-users.jpg`: Firebase Console project `eventhub-group4` -> `Authentication -> Users` hiển thị các tài khoản Google và Email/Password cùng UID thật.

## 2. Export PDF & Cloudinary (`evidence/export/`)

- `01-pdf-upload-app.png`: Màn L3-02 `Xuất lịch tham gia` hiển thị danh sách 2 đăng ký thực tế, cảnh báo URL công khai (`Ai có liên kết đều có thể xem`), URL kết quả, nút `Sao chép liên kết PDF` và `Tạo PDF và tải lên`.
- `02-pdf-opened-browser.png`: Mở trực tiếp URL PDF trên trình duyệt, nội dung tiếng Việt hiển thị chuẩn (`EventHub – Lịch tham gia`, 2 sự kiện), không lộ email hay số điện thoại.
- `03-cloudinary-media-library.jpg`: Cloudinary Media Library (`qcfqv5oj (Test)`) hiển thị file PDF `13.48 KB` trong thư mục `lab3-test`, định dạng `PDF`, Access control `Public`.
- `04-cloudinary-upload-preset.png`: Cấu hình unsigned preset `eventhub_lab3_pdf_test` (`Allowed formats: pdf`, `Asset folder: eventhub/lab3-test`, `Access control: Public`).
- **Lưu ý trung thực:** URL Cloudinary hiện là `Public` nên chưa đạt kiểm soát đọc riêng theo UID như `firebase/storage.rules` mô tả cho Firebase Storage; đây là giới hạn đã biết của phương án Cloudinary unsigned preset được giảng viên chấp thuận. Dữ liệu export trong ảnh còn 1 sự kiện lịch sử mang hậu tố `(Mẫu)` từ dữ liệu test trước đó.

## 3. Remote Config (`evidence/instrumentation/remote-config/`)

- `baseline-console.png`: Console giá trị mặc định `recommendation_limit = 10`, `show_recommendations = true`.
- `limit-1-console-and-app.png`: Console Version 2 (`1` / `true`) và app Khám phá chỉ còn 1 thẻ gợi ý sau khi bấm `Lấy cấu hình mới` (không rebuild).
- `recommendations-false-console.png` & `recommendations-hidden-app.png`: Console Version 3 (`show_recommendations = false`) và app ẩn toàn bộ danh sách thẻ gợi ý, giữ tiêu đề và lời giải thích.
- `restored-10-true-console-and-app.png`: Khôi phục Version 5 (`10` / `true`) trên Console và app hiển thị lại nhiều thẻ gợi ý.

## 4. Analytics DebugView (`evidence/instrumentation/analytics/`)

Property `eventhub-group4` trên Google Analytics DebugView đã xác nhận **11/14 event** trong kế hoạch kèm tham số cụ thể và `user_id` (`H8DqKH45nOa27YF1RQ3haCXi2UA3`):

| Event | Ảnh bằng chứng | Tham số / User ID nhìn thấy trong ảnh | Trạng thái |
|---|---|---|---|
| `login` | [login.jpg](analytics/login.jpg) | `method = google`; `user_id = H8DqKH...i2UA3` ở bảng thuộc tính hoạt động | Đã xác minh |
| `logout` | [logout.png](analytics/logout.png) | `method = manual` | Đã xác minh |
| `search` | [search-query-length-8.png](analytics/search-query-length-8.png) | `query_length = 8` | Đã xác minh |
| `view_event_detail` | [view-event-detail-A04.png](analytics/view-event-detail-A04.png) | `screen_code = A04` | Đã xác minh |
| `view_registration_detail` | [view-registration-detail-A08.png](analytics/view-registration-detail-A08.png) | `screen_code = A08` | Đã xác minh |
| `booking_submit` | [booking-submit-register.png](analytics/booking-submit-register.png) | `action = register` | Đã xác minh |
| `booking_result` | [booking-result-register.png](analytics/booking-result-register.png), [booking-result-confirmed.png](analytics/booking-result-confirmed.png) | `action = register`, `result = confirmed` | Đã xác minh |
| `export_generate` | [export-generate-row-count-2.png](analytics/export-generate-row-count-2.png) | `row_count = 2` | Đã xác minh |
| `export_upload` | [export-upload-byte-count-13803.png](analytics/export-upload-byte-count-13803.png) | `byte_count = 13803` | Đã xác minh |
| `remote_config_fetch` | [remote-config-fetch.png](analytics/remote-config-fetch.png) | `result = success` | Đã xác minh |
| `view_screen` | [view-screen-A01a.png](analytics/view-screen-A01a.png), [user-id-and-view-screen.jpg](analytics/user-id-and-view-screen.jpg) | `screen_code = A01a`; tab `Thuộc tính người dùng` hiện `user_id = H8DqKH45nOa27YF1RQ3haCXi2UA3` | Đã xác minh |
| `view_checkin_result` | — | Cần chụp khi mở A12 sau quét QR thực | **Chờ chụp DebugView** |
| `booking_recover` | — | Cần chụp khi kích hoạt tra cứu trạng thái chưa rõ sau lỗi mạng | **Chờ chụp DebugView** |
| `notification_open` | — | Cần chụp khi chạm tin từ inbox (`in_app`) hoặc từ push (`push`) | **Chờ chụp DebugView** |

- Ảnh tổng quan timeline kết hợp emulator: [debugview-search-detail-overview.png](analytics/debugview-search-detail-overview.png).
- Logcat `FA-SVC` đã lọc (hiển thị `view_screen`, `search`, `view_event_detail` và `Successful upload. Got network response. code, size: 204, 0`): [analytics-search-detail-logcat.txt](analytics-search-detail-logcat.txt).
- Ngoài ra, kiểm thử tự động ARTEMIS `TC18` (`test_analytics.py`) đã xác nhận event `remote_config_fetch` xuất hiện trong `adb logcat` (`FA`/`FA-SVC`) ở Run 1 & Run 2.

## 5. Crashlytics (`evidence/instrumentation/crashlytics/`)

- `native-test-crash-dashboard.png`, `test-crash-user-and-time.png`, `test-crash-custom-keys.png`: `FirebaseCrashlyticsTestCrash` lúc `06:28:18`, có `UID` và `app_flow=eventhub`.
- `nonfatal-dashboard.png`, `nonfatal-custom-keys.png`, `nonfatal-user-and-time.png`: `manual_non_fatal_test` lúc `06:28:00`, có `UID` và `app_flow=eventhub`.
- `real-upload-error-app.png`, `real-upload-error-dashboard.png`, `real-upload-error-custom-keys.png`, `real-upload-error-user-and-time.png`: lỗi nghiệp vụ thực `report_upload_failed` khi upload PDF lúc offline (app xử lý mượt, hiển thị thông báo, không crash; Console ghi nhận lúc `06:38:45` kèm `UID` và `app_flow=eventhub`).
- `crashes-dashboard.png`: ảnh ghi nhận `unhandled_platform_error` cũ; giữ lại làm lịch sử đối chiếu, không tính là test crash.

## 6. FCM (`evidence/instrumentation/fcm/`)

- `foreground-console-and-receipt.png`, `foreground-inbox.png`: nhận tin khi app đang mở, hiện thông báo và lưu vào inbox Firestore.
- `background-system-notifications.png`, `background-open-inbox-before-tab-fix.png`, `background-open-inbox-tab-fixed.png`: nhận tin khi app chạy nền; sau khi sửa `router.go('/notifications')` (commit `8395203`), chạm tin mở đúng tab Thông báo.
- `terminated-system-notification.png`, `terminated-open-inbox.png`: trước khi gửi đã kiểm tra `pidof com.eventhub.app` rỗng (`am kill`, không `force-stop`); tin hiển thị trên notification shade và chạm vào mở đúng lịch sử thông báo trong app.
- Bản sửa tương thích token Console (`getToken`/`onTokenRefresh`/`deleteToken`, commit `67ddd96`) đã được kiểm tra bằng unit test và chạy thật trên emulator API 35.

## 7. ARTEMIS E2E (`evidence/artemis/`)

- **Flash 3-run regression (11/11/2026):** `38/48 = 79.17%` trên 16 ca active × 3 lượt (9/16 ca đạt 3/3 = 100%, tất cả 16 ca pass ít nhất 1/3 lượt, 0 app crash/ANR, 0 HTTP 429). Chi tiết tại [run-command-and-summary.txt](../artemis/run-command-and-summary.txt) và [docs/test-plan.md](../../docs/test-plan.md).
- **Pro Exploratory Session (11/11/2026):** Trace `c8a40964-c1e0-4b14-9867-c1a2eacd4651`, `1056.453s` (`17m 36s`), 78 bước, 229 model calls, Checker **PASS**, 0 app crash/bug. Chi tiết tại [exploratory-pro-session.md](../artemis/exploratory-pro-session.md).
