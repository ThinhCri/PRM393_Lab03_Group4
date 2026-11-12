# EventHub — PRM393 Lab 3 (Group 4)

Ứng dụng **EventHub** (Flutter Android) dành cho sinh viên và khách tham gia sự kiện tại trường: đăng nhập an toàn, khám phá/tìm kiếm sự kiện, đăng ký/hủy theo thời gian thực trên Cloud Firestore, điểm danh bằng QR, xuất lịch tham gia ra PDF và tích hợp đầy đủ 6 nhóm dịch vụ Firebase cùng kiểm thử E2E bằng Google ARTEMIS.

- **Figma chính thức (Lab 2 baseline):** [PRM393 Design File](https://www.figma.com/design/WC21Na9ZDS8jjM2LzPKeXa/PRM393?node-id=0-1&t=vvZ6weDVMtbbxze1-1)
- **Video demo (5–10 phút):** `<LINK_VIDEO_DEMO_5_10_PHUT>` *(kịch bản quay chi tiết tại [docs/demo-video-script.md](docs/demo-video-script.md))*
- **Báo cáo cuối kỳ (PDF):** [report/Lab03_Group4.pdf](report/Lab03_Group4.pdf)
- **Slide thuyết trình (PDF):** [slides/Lab03_Group4_slides.pdf](slides/Lab03_Group4_slides.pdf)

---

## 1. Đề tài, Persona & Dịch vụ Cloud sử dụng

- **Persona (từ Lab 2):**
  - **P01 — Nguyễn Minh Anh:** Sinh viên FPTU, tìm kiếm sự kiện, đăng ký (nhập Khóa K) và quét QR điểm danh.
  - **P02 — Gia Linh:** Khách ngoài trường, đăng ký tham gia sự kiện hợp lệ mà không cần thông tin sinh viên.
  - **P03 — Việt Khoa:** Người xem sự kiện tự do (*Lưu ý D02: bản Lab 3 yêu cầu AuthGate trước khi vào nội dung, vẫn không cần đăng ký sự kiện tự do*).
- **Dịch vụ & API sử dụng (Project Firebase `eventhub-group4`, package `com.eventhub.app`):**
  1. **Firebase Authentication:** Google Sign-In + Email/Password + xác minh email + quên mật khẩu, định tuyến theo phiên (`AuthGate`).
  2. **Cloud Firestore + Security Rules:** Lưu `events`, `registrations`, `checkinSessions`, `qrCredentials` (SHA-256), `users/{uid}/notifications`; đăng ký/hủy nguyên tử qua transaction (`activeCount` được kiểm tra bằng `getAfter()`).
  3. **Cloudinary Free (thay thế Firebase Storage theo chấp thuận của giảng viên):** Tạo file PDF lịch tham gia tiếng Việt từ dữ liệu thật (không chứa email/SĐT) và upload qua unsigned preset (`qcfqv5oj` / `eventhub_lab3_pdf_test`). *Lưu ý: URL kết quả là công khai (`Public`), UI có cảnh báo rõ; [firebase/storage.rules](firebase/storage.rules) được giữ trong repo để minh họa rule chuẩn `reports/{uid}/...`.*
  4. **Firebase Cloud Messaging (FCM):** Nhận thông báo ở cả 3 trạng thái (foreground, background, terminated), xin quyền Android 13+, lưu hộp thư trong app và chạm tin mở đúng tab Thông báo.
  5. **Google Analytics:** Kế hoạch 14 event không PII; đã chụp DebugView kèm tham số và `user_id` cho **11/14 event** (3 event còn chờ chụp: `view_checkin_result`, `booking_recover`, `notification_open`), kèm kiểm tra Logcat tự động `TC18`.
  6. **Firebase Crashlytics & Remote Config:** Crashlytics ghi nhận cả lỗi nghiệp vụ thực (`report_upload_failed` khi upload offline) và native test crash kèm `user_id` + `app_flow=eventhub`. Remote Config dùng 2 tham số (`recommendation_limit`, `show_recommendations`) cập nhật giao diện trực tiếp không cần rebuild.

---

## 2. Phiên bản đã pin (Pinned Versions)

Kiểm chứng trực tiếp tại [pubspec.yaml](pubspec.yaml) và [pubspec.lock](pubspec.lock):

| Thành phần | Phiên bản / Commit pin |
|---|---|
| Flutter / Dart SDK | Flutter **3.47.4** / Dart SDK **^3.13.3** |
| State & Routing | `flutter_riverpod: 3.4.3`, `go_router: 18.1.2` |
| Firebase SDKs | `firebase_core: 5.1.0`, `firebase_auth: 7.0.1`, `google_sign_in: 7.2.0`, `cloud_firestore: 7.1.0`, `firebase_analytics: 13.0.1`, `firebase_crashlytics: 6.0.1`, `firebase_remote_config: 7.0.1`, `firebase_messaging: 17.0.1` |
| Device / Storage / PDF / HTTP | `mobile_scanner: 7.4.3`, `flutter_secure_storage: 11.2.0`, `http: 1.6.0`, `pdf: 3.13.1`, `path_provider: 2.1.6`, `crypto: 3.0.8`, `flutter_svg: 2.3.2`, `cupertino_icons: 1.0.9`, `flutter_lints: 6.0.0` |
| Google ARTEMIS & Python E2E | Upstream `google/artemis` commit **`351ca8422f7b5b54e80a9c1ce03a222e02415b6b`**; Python **3.12.14**, `pytest` **8.4.2** ([e2e_test/pyproject.toml](e2e_test/pyproject.toml)) |

---

## 3. Hướng dẫn chạy ứng dụng & kiểm thử

### 3.1. Chạy ứng dụng Android (`lib/main.dart`)

File cấu hình Android công khai [android/app/google-services.json](android/app/google-services.json) đã có sẵn trong repository. Nếu chạy trên máy mới với Google Sign-In debug keystore khác, thêm SHA-1/SHA-256 của máy đó vào Firebase Console.

```powershell
flutter pub get
flutter devices
flutter run -t lib/main.dart `
  --dart-define=CLOUDINARY_CLOUD_NAME=qcfqv5oj `
  --dart-define=CLOUDINARY_UPLOAD_PRESET=eventhub_lab3_pdf_test
```

### 3.2. Kiểm tra code, Flutter Tests & Firestore Security Rules

```powershell
flutter analyze
flutter test
flutter build apk --debug -t lib/main.dart
```

- Kết quả mới nhất sau dọn dẹp repo: `flutter analyze` sạch (0 issues); `flutter test` đạt **73/73 tests pass**.
- Chạy kiểm thử Firestore Security Rules trên Emulator cục bộ (`demo-direct-booking`, không ảnh hưởng cloud):
  ```powershell
  npm ci --prefix firebase/tests
  npx firebase-tools emulators:exec --only firestore --project demo-direct-booking "npm test --prefix firebase/tests"
  ```

### 3.3. Chạy kiểm thử E2E bằng Google ARTEMIS (`e2e_test/`)

Cài đặt môi trường Python qua `uv` và thiết lập biến môi trường cục bộ (không commit token/tài khoản test):

```powershell
uv sync --project e2e_test
$env:ARTEMIS_BASE_URL = "http://127.0.0.1:8000"
$env:ARTEMIS_TEST_ACCOUNT_EMAIL = "<DEDICATED_TEST_ACCOUNT>"
$env:ARTEMIS_EVENT_TITLE = "Workshop Thiết kế trải nghiệm người dùng"
$env:ARTEMIS_DEVICE = "emulator-5554"

# Chạy bộ Flash regression 3 lượt độc lập (tự động tổng hợp JUnit + summary.csv)
powershell -ExecutionPolicy Bypass -File .\e2e_test\run_regression.ps1 -Selection "not TC13 and not TC15"

# Chạy phiên thăm dò Pro (15-30 phút, opt-in)
$env:ARTEMIS_ALLOW_PRO = "1"
uv run --project e2e_test python e2e_test/explore.py
```

- **Kết quả ARTEMIS đã xác minh (11/11/2026):**
  - **Flash 3-run regression:** **38/48 lượt đạt (79.17%)** trên 16 ca active × 3 lượt (`9/16` ca đạt 100%, 0 crash/ANR, 0 HTTP 429; `TC18` xác nhận `remote_config_fetch` qua Logcat). Chi tiết tại [docs/test-plan.md](docs/test-plan.md) và [evidence/artemis/run-command-and-summary.txt](evidence/artemis/run-command-and-summary.txt).
  - **Pro exploratory session:** Trace `c8a40964-c1e0-4b14-9867-c1a2eacd4651`, **17m 36s** (`1056.453s`), **78 steps**, **229 model calls**, Checker **PASS**, 0 app bugs ([evidence/artemis/exploratory-pro-session.md](evidence/artemis/exploratory-pro-session.md)).

---

## 4. Bản đồ tài liệu & Deliverable (Deliverables Map)

| Hạng mục | Đường dẫn | Nội dung chính |
|---|---|---|
| **Báo cáo cuối kỳ (8–12 trang)** | [report/Lab03_Group4.pdf](report/Lab03_Group4.pdf) | Tổng hợp đầy đủ Lab 2 → Lab 3, kiến trúc, 6 dịch vụ Firebase, ARTEMIS, AI Review, hạn chế |
| **Slide thuyết trình (12–15 trang)** | [slides/Lab03_Group4_slides.pdf](slides/Lab03_Group4_slides.pdf) | Trình bày trực quan kèm ảnh app, Console, bảng kết quả ARTEMIS và đối chiếu Figma |
| **Kịch bản Video Demo** | [docs/demo-video-script.md](docs/demo-video-script.md) | Kịch bản quay 5–10 phút theo đúng thứ tự yêu cầu trang 12 |
| **Design Traceability** | [docs/design-traceability.md](docs/design-traceability.md) | Ma trận màn hình/flow/component, link Figma và sai lệch `D01–D15` |
| **Architecture** | [docs/architecture.md](docs/architecture.md) | Cấu trúc thư mục `lib/`, sơ đồ tầng MVVM, sequence diagram F1, bảng VM ↔ Services |
| **Analytics Plan** | [docs/analytics-plan.md](docs/analytics-plan.md) | Kế hoạch 14 event không PII, liên kết 11/14 ảnh DebugView và 3 event chờ chụp |
| **Test Plan & Results** | [docs/test-plan.md](docs/test-plan.md) | 25 ca ARTEMIS, bảng pass rate Flash 3 lượt (`79.17%`), giải trình flaky/skipped, Pro session |
| **AI Code Review** | [docs/code-review.md](docs/code-review.md) | Appendix C: `PR #3` (`PR01–PR05`), workspace audit fixes (`AUD01–AUD04`), AI disclosure |
| **Bảng kiểm tiến độ** | [docs/lab3-readiness.md](docs/lab3-readiness.md) | Đối chiếu tổng hợp tình trạng từng tiêu chí và điểm còn mở |
| **Bằng chứng Cloud & E2E** | [evidence/instrumentation/status.md](evidence/instrumentation/status.md) | Thư mục ảnh Auth, Export/Cloudinary, FCM, Crashlytics, Remote Config, Analytics, ARTEMIS |

---

## 5. AI Disclosure

| Công cụ AI | Mục đích sử dụng thực tế |
|---|---|
| **OpenAI Codex** (`GPT-6.1`) | Kiến trúc MVVM/Riverpod, refactor (`AUD01–AUD04`), review code cục bộ & diff PR #3 (`PR01–PR05`), viết unit/Rules tests, tài liệu kỹ thuật |
| **Google Antigravity** | Hỗ trợ dựng khung code ban đầu, kiểm tra đối chiếu bằng chứng Console/E2E, đồng nhất tài liệu `docs/`, xuất PDF báo cáo và slides |
| **Google ARTEMIS** | Kiểm thử E2E tự động trên Android Emulator (`Flash` 3-run regression dùng `gemini-3.1-flash-lite`; `Pro` exploratory session `17m 36s`) |
| **Image generation** | Tạo 5 ảnh bìa minh họa cho các sự kiện trong ứng dụng (`assets/event-covers/`) |
| **Stitch** | Tham chiếu/khởi tạo ý tưởng thiết kế UI từ Lab 2 |
