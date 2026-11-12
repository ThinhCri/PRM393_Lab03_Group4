# AI-Assisted Code Review Record — EventHub Lab 3

Cập nhật 12/11/2026. Tài liệu trình bày trung thực toàn bộ quá trình review code có hỗ trợ AI theo đúng mẫu **Appendix C** của đề Lab 3 (trang 10 & 17–18): **PR #3** trên GitHub ([pull/3](https://github.com/ThinhCri/PRM393_Lab03_Group4/pull/3)), các **fix khắc phục sau audit trong workspace (`AUD01`–`AUD04`)** có mỗi finding một commit riêng, lịch sử review cục bộ trước PR (`L01`–`L06`), và bảng **AI Disclosure** đầy đủ.

---

## 1. Bảng ghi nhận Findings & Quyết định (Appendix C)

### 1.1. Findings từ Review PR #3 (Codex assistant trên diff GitHub PR #3)

- **PR được review:** [ThinhCri/PRM393_Lab03_Group4#3](https://github.com/ThinhCri/PRM393_Lab03_Group4/pull/3) (source tại revision `fb2d2ee`)
- **Output & metadata phạm vi lưu trong repo:** [docs/review-pr-findings.md](review-pr-findings.md) và [evidence/code-review/pr-3-scope.json](../evidence/code-review/pr-3-scope.json)
- **Validation sau sửa PR #3:** [evidence/code-review/validation.md](../evidence/code-review/validation.md) (`flutter analyze` 0 issue; `65/65` Flutter test đạt tại thời điểm merge PR #3).

| ID | Tool | File:line (rev `fb2d2ee`) | Kind | Finding (summary) | Decision | Reason (theo §3/§5/§6 & ràng buộc thực tế) | Fix commit |
|---|---|---|---|---|---|---|---|
| `PR01` | Codex assistant (`GPT-6.1`) | `lib/screens/events/scanner_screen.dart:83` | `Bug` | `didChangeAppLifecycleState` dừng camera khi app vào nền nhưng không khởi động lại khi app `resumed` | `Accepted` | Ảnh hưởng khôi phục luồng F4A (§3) khi người dùng chuyển sang Cài đặt/ứng dụng khác rồi quay lại màn quét QR | `fe02d20` *(gộp với `PR02`)* |
| `PR02` | Codex assistant (`GPT-6.1`) | `lib/screens/events/scanner_screen.dart:37` | `Bug` | Truy cập `ref` sau `await restore` trong `initState` mà chưa kiểm tra `mounted` | `Accepted` | Đảm bảo độ ổn định state (§5); nếu widget đã `dispose` trong lúc chờ `await`, truy cập `ref` gây ngoại lệ runtime | `fe02d20` *(gộp với `PR01`)* |
| `PR03` | Codex assistant (`GPT-6.1`) | `lib/viewmodels/cloud_tools_viewmodel.dart:34` | `Security` | `refresh()` phát Analytics event sau `await` bằng `ref` của phiên hiện tại, dễ gán nhầm thao tác tài khoản cũ sang UID mới nếu đổi phiên giữa chừng | `Accepted` | Bảo toàn tính đúng đắn `user_id` & cô lập phiên (§6 Analytics); gắn kiểm tra `UID + epoch` trước khi ghi log | `9f92864` *(gộp với `PR04`)* |
| `PR04` | Codex assistant (`GPT-6.1`) | `lib/viewmodels/cloud_tools_viewmodel.dart:81` | `Bug` | `nonFatal()` chỉ kiểm tra `mounted`, kết quả hoàn tất muộn có thể ghi đè feedback lỗi lên phiên tài khoản mới | `Accepted` | Đảm bảo cô lập state và phản hồi lỗi theo đúng phiên đăng nhập (§5/§6) | `9f92864` *(gộp với `PR03`)* |
| `PR05` | Codex assistant (`GPT-6.1`) | `lib/services/firebase/firebase_cloud_services.dart:135` | `Bug` | `onRegistered.first.timeout(...)` khởi tạo trước khi gọi `register()`; nếu `register()` ném lỗi trước, Future timeout không được quan sát sẽ gây lỗi async thứ hai | `Accepted` | Xử lý lỗi dịch vụ sạch sẽ không tạo crash thứ cấp (§6). *(Ghi chú lịch sử: sau đó adapter FCM đổi sang `getToken()` ở commit `67ddd96`, `PR05` vẫn là lịch sử thật tại `33fb007`)* | `33fb007` *(riêng `PR05`)* |

> **Ghi nhận trung thực về PR #3:** PR #3 có **5 findings thuộc 2 nhóm (`Bug`, `Security`)** và **3 fix commits** (`fe02d20`, `9f92864`, `33fb007`). Tuy nhiên, 2 commit đầu gộp cặp (`fe02d20` gộp `PR01+PR02`; `9f92864` gộp `PR03+PR04`), chưa khớp chặt quy tắc mỗi finding một commit riêng. Nhóm giữ nguyên lịch sử Git đã push (không rewrite history) và áp dụng đúng chuẩn **1 finding ID / 1 commit riêng** cho toàn bộ các fix audit tiếp theo bên dưới.

### 1.2. Findings khắc phục sau Audit trang 5–10 (Mỗi ID một commit riêng)

Các findings dưới đây được phát hiện trong đợt đối chiếu source theo yêu cầu trang 5–10 của đề Lab 3 (không phải review bot ngoài trên PR mới) và đã được khắc phục hoàn toàn với **mỗi finding ID gắn một commit riêng**:

| ID | Tool | File:line | Kind | Finding (summary) | Decision | Reason (theo §5/§6 & Accessibility) | Fix commit |
|---|---|---|---|---|---|---|---|
| `AUD01` | Codex assistant (Workspace Audit) | `lib/screens/events/scanner_screen.dart` & `lib/services/device/qr_camera_service.dart` | `Architecture` | Màn hình UI trực tiếp tạo `MobileScannerController`, gọi `start()`/`stop()`/`openSettings()` và giữ state camera | `Accepted` | Vi phạm quy tắc tách lớp MVVM (§5); chuyển toàn bộ điều phối sang `ScannerViewModel` + contract `QrCamera` (`services/qr_camera_provider.dart`), giữ `QrCameraPreview` chỉ render | `9bd5bd8` |
| `AUD02` | Codex assistant (Workspace Audit) | `lib/theme/app_theme.dart` & `lib/screens/*` | `Maintainability` | Hint input dùng `#A0ABBA` (độ tương phản ~2.33:1 < 4.5:1), `bodySmall=12sp`, còn dùng raw `AppBar`/`AlertDialog`/`ChoiceChip` ở một số màn | `Accepted` | Đạt checklist accessibility Lab 2/§6 (hint `#5F6B7A` ~5.43:1, chữ nội dung ≥ 14sp, vùng chạm ≥ 48dp) và 1 reusable widget mỗi component (`AppTopBar`, `AppButton`, `AppConfirmationDialog`, `AppChoiceChip`) | `c3273ec` |
| `AUD03` | Codex assistant (Workspace Audit) | `lib/viewmodels/auth_viewmodel.dart` | `Security` | Dữ liệu pending booking theo UID trong secure storage chưa bị xóa khi logout và có thể race với thao tác booking đang chạy | `Accepted` | Đáp ứng §6 Auth (`sign-out clears local user data`); chặn logout khi đang busy, xóa pending của UID hiện tại trước `signOut` và báo lỗi nếu xóa thất bại | `53eae7e` |
| `AUD04` | Codex assistant (Workspace Audit) | `lib/viewmodels/notifications_viewmodel.dart` & `lib/services/firebase/firebase_cloud_services.dart` | `Bug` | Mở thông báo từ push chưa phát `notification_open(source=push)`, và lỗi lưu lịch sử inbox bị `catchError` nuốt lặng | `Accepted` | Đáp ứng §6 Analytics completeness và failure handling; phát `notification_open(source=push)` cho UID hợp lệ và báo lỗi + ghi non-fatal `notification_history_save_failed` | `599b4c4` |

Validation sau `AUD01`–`AUD04` ([evidence/source-fixes/validation.md](../evidence/source-fixes/validation.md)): `flutter analyze --no-pub` 0 issue; **73/73 Flutter unit/widget tests pass**.

---

## 2. Lịch sử review cục bộ trước khi mở PR (31/10/2026)

Nhật ký review tự động trong lúc triển khai ban đầu (trước khi mở PR #3, lưu làm lịch sử phát triển; không tính thay cho PR review):

| ID | File:line tham chiếu | Kind | Vấn đề và quyết định | Kiểm tra |
|---|---|---|---|---|
| `L01` | `lib/viewmodels/booking_viewmodel.dart:34`; `lib/viewmodels/export_viewmodel.dart:57` | `Security` / Concurrency | Accepted: kiểm tra `UID + epoch + mounted` trước khi nhận kết quả async để tránh rò rỉ kết quả giữa hai tài khoản | Đổi UID khi đang chờ không hiện dữ liệu cũ |
| `L02` | `lib/viewmodels/profile_viewmodel.dart:6` | `Bug` / State | Accepted: tách trạng thái `saved` riêng, không suy ra thành công từ `errors.isEmpty` | `profile_viewmodel_test` |
| `L03` | `lib/utils/push_destination.dart:3` | `Bug` / Navigation | Accepted: lọc ID rỗng và từ chối đường dẫn push không hợp lệ | Push fallback / cross-UID tests |
| `L04` | `lib/viewmodels/booking_viewmodel.dart:109` | `Bug` / Concurrency | Accepted: khóa thao tác trước mọi `await`; tracking Analytics không làm gián đoạn nghiệp vụ | Double-tap & unknown/recovery tests |
| `L05` | `lib/app/bootstrap.dart:10`; `lib/services/firebase/firebase_bootstrap.dart:13` | `Bug` / Startup | Accepted: giữ future `initializeCore()` không khởi tạo chồng, có UI retry khi timeout | `bootstrap_test` |
| `L06` | `lib/viewmodels/auth_viewmodel.dart` | `Bug` / Auth | Accepted: không để lỗi mạng khi gỡ push token làm kẹt luồng đăng xuất | Unit tests đăng xuất |

---

## 3. AI Disclosure (Danh sách công cụ AI sử dụng)

| Công cụ AI | Mục đích sử dụng thực tế trong Lab 3 |
|---|---|
| **OpenAI Codex** (`GPT-6.1`) | Hỗ trợ thiết kế kiến trúc MVVM/Riverpod, triển khai & refactor (`AUD01`–`AUD04`), đối chiếu yêu cầu đề Lab 3, thực hiện review code cục bộ (`L01`–`L06`) & review diff GitHub PR #3 (`PR01`–`PR05`), viết unit/Firestore Rules tests và tài liệu kỹ thuật |
| **Google Antigravity** | Hỗ trợ dựng khung code ban đầu, kiểm tra đối chiếu bằng chứng/ảnh chụp Console & logcat, rà soát đồng nhất tài liệu `docs/` & `README.md`, biên soạn báo cáo PDF và slide thuyết trình |
| **Google ARTEMIS** | Công cụ AI E2E testing tự động điều khiển Android Emulator (`Flash` profile dùng `gemini-3.1-flash-lite` cho 3-run regression `38/48 = 79.17%`; `Pro` profile cho phiên exploratory `17m 36s` / 78 bước / Checker PASS) |
| **Image generation** | Tạo 5 ảnh bìa minh họa cho các sự kiện trong ứng dụng (`assets/event-covers/`); không dùng ảnh tạo sinh làm bằng chứng test hay ảnh Console |
| **Stitch** | Hỗ trợ khởi tạo/tham chiếu ý tưởng thiết kế UI từ giai đoạn Lab 2 |

Mọi bằng chứng chạy thật trên Firebase Console, Cloudinary, Android Emulator và ARTEMIS traces đều được thành viên nhóm trực tiếp vận hành và kiểm chứng; không công bố API key, mật khẩu hay email cá nhân trong repository.
