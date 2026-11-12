# Kiểm kê từng yêu cầu đề Lab 3 — Cập nhật 12/11/2026

Tài liệu đối chiếu trung thực toàn bộ các mục trong đề `PRM393 - Lab 3` (trang 3–12) với trạng thái code, bằng chứng, kiểm thử và bài nộp hiện tại.

**Quy ước trạng thái:**
- **Đạt:** Đủ code và bằng chứng thực tế trong `evidence/`.
- **Đạt có điều kiện / Một phần:** Có code và bằng chứng chính, nhưng còn giới hạn thực tế được nêu rõ.
- **Chờ hoàn tất:** Mục chưa thu thập xong (chỉ còn 3 ảnh DebugView phụ và quay video demo).

---

## Phần A — Kiến trúc, Design System & Chất lượng UI (Trang 5–6)

| Yêu cầu đề Lab 3 | Trạng thái | Căn cứ & Bằng chứng thực tế |
|---|---|---|
| **MVVM & Riverpod** (`Screens → ViewModels → Contracts → Services`, không logic trong `build()`, có state explicit) | **Đạt** | [architecture.md](architecture.md) khớp 100% cấu trúc `lib/`. `AUD01` (`9bd5bd8`) đã tách `QrCamera` contract & `ScannerViewModel`; các ViewModel dùng `AsyncValue` hoặc state class riêng (`loading/empty/error/data`) và inject service qua provider |
| **Design System in code** (`lib/theme/`, `lib/widgets/`, tokens thay vì hard-code) | **Đạt** | `lib/theme/` khóa `ColorScheme`, `TextTheme`, spacing/radius/shadows/touchTargets; `AUD02` (`c3273ec`) chuẩn hóa `AppTopBar`, `AppButton`, `AppConfirmationDialog`, `AppChoiceChip` across production screens; ánh xạ tại [flutter-handoff.md](flutter-handoff.md) |
| **Accessibility** (contrast ≥ 4.5:1, touch ≥ 48dp, body ≥ 14sp, 360/412dp, large text) | **Đạt** | `AUD02` (`c3273ec`) sửa hint input sang `#5F6B7A` (~5.43:1), body ≥ 14sp, touch ≥ 48dp; kiểm tra tự động trong `73/73` Flutter tests (`accessibility_tokens_test.dart`, `responsive_test.dart` tại 360dp & 412dp) |
| **Design Traceability & Figma sync** | **Một phần** | [design-traceability.md](design-traceability.md) ghi nhận đủ `D01–D15` (không phát sinh `D09`) kèm ảnh trước/sau `D03`, `D08`, `D11` và [figma-app-audit.md](figma-app-audit.md). Baseline Figma Lab 2 giữ nguyên chưa sửa trực tiếp |

---

## Phần B — Sáu dịch vụ Firebase & Cloudinary (Trang 6–7)

| Dịch vụ / Tiêu chí | Trạng thái | Bằng chứng & Lưu ý trung thực |
|---|---|---|
| **Authentication** (Google Sign-In, auth-state routing, hủy có thông báo, sign-out xóa dữ liệu user) | **Đạt** | 4 ảnh [evidence/auth/](../evidence/auth/) (`01-mobile-signed-out.png`, `02-mobile-google-cancelled.png`, `03-mobile-signed-in-home.jpg`, `04-console-auth-users.jpg`); `AUD03` (`53eae7e`) chặn logout race và xóa pending UID trước `signOut`; ARTEMIS `TC01`, `TC02` (3/3), `TC17` (3/3) |
| **Cloud Storage / Cloudinary Free** (tạo PDF, upload có tiến độ/URL, per-user rules) | **Đạt có điều kiện** | 4 ảnh [evidence/export/](../evidence/export/) (`01-pdf-upload-app.png`, `02-pdf-opened-browser.png`, `03-cloudinary-media-library.jpg`, `04-cloudinary-upload-preset.png`); ARTEMIS `TC14` (3/3 = 100%). **Giới hạn trung thực:** Giảng viên cho phép dùng Cloudinary Free thay Firebase Storage; preset unsigned tạo URL `Public` nên không giới hạn đọc theo UID (đã cảnh báo rõ trên UI và lưu `firebase/storage.rules` làm đặc tả Storage rule) |
| **Cloud Messaging (FCM)** (nhận tin ở 3 trạng thái, quyền Android 13+, inbox trong app, chạm tin mở đúng màn) | **Đạt** | 7 ảnh [evidence/instrumentation/fcm/](../evidence/instrumentation/fcm/) cho foreground, background, terminated (`pidof` rỗng trước gửi), inbox và tap mở `/notifications` (`8395203`, `67ddd96`); ARTEMIS `TC16` (3/3 = 100%). Còn mở: deep link theo `eventId` cụ thể từ push Console chung |
| **Analytics** (kế hoạch ≥ 7 event trước code, không PII, `user_id`, DebugView mọi event) | **Một phần (11/14)** | [analytics-plan.md](analytics-plan.md) gồm 14 event không PII; **11/14 event** có ảnh DebugView + tham số + `user_id` (`H8DqKH45nOa27YF1RQ3haCXi2UA3`) tại [evidence/instrumentation/analytics/](../evidence/instrumentation/analytics/), kèm `FA-SVC` Logcat & `TC18`. **Thiếu ảnh DebugView của 3 event:** `view_checkin_result`, `booking_recover`, `notification_open` |
| **Crashlytics** (non-fatal từ nhánh lỗi thực + test crash, kèm `user_id` và custom key) | **Đạt** | 11 ảnh [evidence/instrumentation/crashlytics/](../evidence/instrumentation/crashlytics/) chứng minh lỗi thực `report_upload_failed` khi upload offline và `FirebaseCrashlyticsTestCrash`, đều có `UID` và `app_flow=eventhub` |
| **Remote Config** (≥ 2 tham số đổi UI, defaults, áp dụng không cần rebuild) | **Đạt** | 5 ảnh [evidence/instrumentation/remote-config/](../evidence/instrumentation/remote-config/) (`1/true` → `false` → `10/true` trên Console & App), `firebase/remote-config-defaults.json`, và DebugView `remote_config_fetch` |

---

## Phần C — ARTEMIS E2E Testing (Trang 8–9)

| Yêu cầu đề Lab 3 | Trạng thái | Bằng chứng & Lưu ý trung thực |
|---|---|---|
| **Test plan ≥ 10 ca**, đủ 3 flow, error path, native interaction, 1 ca kiểm Logcat Analytics | **Đạt** | [test-plan.md](test-plan.md) & `e2e_test/`: 25 ca (`TC01–TC25`) dùng `ArtemisClient`, khẳng định structured JSON (`final_screen` + `observed_texts`), không chỉ dựa vào `SUCCESS` |
| **Chạy ≥ 3 lượt / ca**, lưu trace, bảng pass rate, giải trình flaky/skipped | **Đạt** | Flash 3-run regression ngày 11/11/2026: **38/48 = 79.17%** (`9/16` ca active 3/3 = 100%, 0 crash/ANR, 0 HTTP 429). Mọi ca flaky (`TC01, 05, 06, 08, 10, 12, 18` — 100% do format JSON/omitted string của Flash, 0 lỗi app), skipped (`TC19–TC25`) và deselected (`TC13`, `TC15`) đều có giải trình tại [test-plan.md](test-plan.md) và [run-command-and-summary.txt](../evidence/artemis/run-command-and-summary.txt) |
| **Phiên Pro exploratory 15–30 phút** + danh sách issues | **Đạt** | Trace `c8a40964-c1e0-4b14-9867-c1a2eacd4651` ([exploratory-pro-session.md](../evidence/artemis/exploratory-pro-session.md)): `1056.453s` (**17m 36s**), **78 steps**, **229 model calls**, Checker **PASS**, 0 app bugs; ghi nhận trung thực giới hạn `Quét QR` bị vô hiệu khi `checkinSessions` đóng |

---

## Phần D — AI Code Review & Deliverables (Trang 10–12)

| Yêu cầu đề Lab 3 | Trạng thái | Căn cứ & Lưu ý trung thực |
|---|---|---|
| **AI review trên PR**, ≥ 5 findings, ≥ 2 loại, decision + lý do, ≥ 3 fix commits riêng theo ID, AI disclosure | **Đạt (ghi rõ lịch sử gộp PR #3)** | [code-review.md](code-review.md): PR #3 ([pull/3](https://github.com/ThinhCri/PRM393_Lab03_Group4/pull/3)) có `PR01–PR05` (`Bug`, `Security`) với 3 commits (`fe02d20` gộp `PR01+PR02`, `9f92864` gộp `PR03+PR04`, `33fb007` riêng `PR05`), cộng 4 audit fixes chuẩn **1 ID / 1 commit** (`AUD01–AUD04`: `9bd5bd8`, `c3273ec`, `53eae7e`, `599b4c4`) và bảng AI disclosure đầy đủ |
| **Cấu trúc Repo & Secret hygiene** | **Đạt** | Đã dọn sạch phần Web/Core ngoài Lab 3; `android/app/google-services.json` được include; không có email cá nhân (`<TEST_ACCOUNT>`) hay API key lộ trong repo; `flutter analyze` sạch và `73/73` tests pass |
| **Báo cáo PDF (8–12 trang), Slides PDF (12–15 trang), Demo video (5–10 phút)** | **Report/Slides xong; Video chờ quay** | `report/Lab03_Group4.pdf`, `slides/Lab03_Group4_slides.pdf`, kịch bản quay [demo-video-script.md](demo-video-script.md), và placeholder `<LINK_VIDEO_DEMO_5_10_PHUT>` tại [README.md](../README.md) |
