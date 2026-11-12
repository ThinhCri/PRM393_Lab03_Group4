# Đối chiếu thiết kế Lab 2 → triển khai Lab 3

Cập nhật 12/11/2026 (lập 30/10/2026). Tài liệu ánh xạ toàn bộ màn hình, luồng và component từ bản thiết kế Lab 2 sang code Flutter Android Lab 3, kèm nhật ký đầy đủ các sai lệch thiết kế (`D01`–`D15`) và lý do. Trạng thái tổng thể xem thêm tại [lab3-readiness.md](lab3-readiness.md).

## Liên kết Figma chính thức

- **Figma chính thức Lab 2/Lab 3:** [PRM393 Design File](https://www.figma.com/design/WC21Na9ZDS8jjM2LzPKeXa/PRM393?node-id=0-1&t=vvZ6weDVMtbbxze1-1)
- Các trang thành phần trong cùng file: [Final UI (`153:2`)](https://www.figma.com/design/WC21Na9ZDS8jjM2LzPKeXa/PRM393?node-id=153-2), [Components (`23:2`)](https://www.figma.com/design/WC21Na9ZDS8jjM2LzPKeXa/PRM393?node-id=23-2), [Prototype (`199:1681`)](https://www.figma.com/design/WC21Na9ZDS8jjM2LzPKeXa/PRM393?node-id=199-1681).
- **Ghi chú đồng bộ Figma:** Theo quyết định giữ nguyên baseline đã chốt của Lab 2, các sai lệch `D01`–`D15` được ghi nhận minh bạch bằng đối chiếu trước/sau tại `evidence/design-changes/` và [figma-app-audit.md](figma-app-audit.md) chứ chưa chỉnh sửa trực tiếp trên file Figma gốc.

## Tóm tắt theo dõi sai lệch thiết kế (D01–D15)

*(Ghi chú: mã `D09` không phát sinh trong quá trình đánh số; tổng cộng có 14 mục sai lệch thực tế `D01`–`D08`, `D10`–`D15`.)*

| ID | Phạm vi | Thay đổi (Lab 2 → Lab 3) & Lý do | Bằng chứng / Trạng thái |
|---|---|---|---|
| `D01` | `A01` Auth | Bổ sung nút Google Sign-In cạnh email/password để đáp ứng §6 Auth mà không mất bộ màn `A01a–d` | Code & ảnh auth (`evidence/auth/01..03`); Figma giữ baseline |
| `D02` | `AuthGate` / `P03` | Chặn người dùng chưa đăng nhập vào nội dung (`signed-out -> A01a`); giữ deep link mở lại đích sau login (ảnh hưởng persona P03) | Đã triển khai & test `TC01`, `TC17` |
| `D03` | `A10` → `L3-01/02` | Thêm khu demo Firebase (`Tiện ích Firebase`) và `Xuất lịch tham gia` dưới Tài khoản | [D03 before/after](../evidence/design-changes/D03-firebase-tools/README.md) |
| `D04` | `A06` / `A11` / `A12` | Làm rõ `A06` chỉ là xác nhận đăng ký (không phải vé QR cá nhân), `A11` quét QR của CLB, `A12` che email/SĐT | Đã triển khai theo `screen-spec.md` |
| `D05` | Điều hướng & `A10`/`A12` | Giữ pending route sau login, hỗ trợ sửa hồ sơ tại `A10`, `A12` trả về kết quả đã check-in hợp lệ | Đã triển khai |
| `D06` | Responsive & Touch | Chuẩn hóa vùng chạm tối thiểu `48dp` (thay 44dp), kiểm layout tại `360dp` và `412dp` | Đã kiểm chứng bằng widget tests |
| `D07` | `A10` Email Google | Email tài khoản Google ở `A10` là chỉ đọc theo provider; không tự gộp provider trùng email | Code & `TC11` đạt 3/3 (100%) |
| `D08` | `A05` / `A08` / `A11` | Thêm nhãn sự kiện đang chờ và nút `Thử lại cùng thao tác` dùng `operationId` idempotent khi mất mạng | [D08 before/after](../evidence/design-changes/D08-network-recovery/README.md) |
| `D10` | Khởi tạo Firebase | Thêm màn loading/retry khi khởi tạo Firebase timeout (45s) để phân biệt lỗi mạng với thiếu config | Đã triển khai & unit test (`bootstrap_test`) |
| `D11` | `A02` / `A03` | Tách nhãn CLB khỏi viền card, tăng khoảng cách chip/empty state để tránh chữ đè viền | [D11 before/after](../evidence/design-changes/D11-discover-filters/README.md) |
| `D12` | `A02` vs `A03` | Phân tách vai trò: `A02` giữ tối đa 3 gợi ý (theo Remote Config) và bỏ nút `Xem tất cả`; tìm kiếm/lọc đầy đủ chuyển vào `A03` | Đã triển khai & kiểm chứng E2E |
| `D13` | `A10` & `A01c` | Tinh gọn `A10`, giữ lối vào `Dịch vụ Firebase` theo §3, căn giữa email trên `A01c`, điều hướng đăng nhập từ Account về `A02` | Đã triển khai |
| `D14` | `A02` / `A04` | Dùng 5 ảnh bìa AI đóng gói trong `assets/event-covers/` qua `coverKey` (fallback `coverUrl` HTTPS) thay màu cam đơn sắc | Đã triển khai trên app & Firestore |
| `D15` | Toàn bộ màn production | Chuẩn hóa `AppTopBar`, `AppButton`, `AppConfirmationDialog`, `AppChoiceChip`, contrast hint `#5F6B7A` (5.43:1), `body ≥ 14sp`, tách `ScannerViewModel` (`AUD01–AUD02`) | Đã sửa tại `9bd5bd8`, `c3273ec`; 73/73 Flutter tests pass |

## Quyết định triển khai mới 04/11/2026

| Màn/phạm vi | Thay đổi so với bản thiết kế trước | Vì sao |
|---|---|---|
| A05/A08/A11 | App ghi Firestore qua transaction, Rules bảo vệ số chỗ và QR; không gọi Cloud Functions | Hướng phát triển lên Final không dùng Functions. UI vẫn giữ cùng luồng; cần test cloud và cập nhật Figma nếu thông báo lỗi thay đổi |
| L3-02 Xuất lịch | Upload PDF qua Cloudinary Free, không qua Firebase Storage; thêm cảnh báo liên kết có thể chia sẻ | Nhóm chọn phương án miễn phí thay Storage theo trao đổi với giảng viên. Chỉ upload PDF không có email/số điện thoại; cần ảnh trước/sau và bằng chứng giảng viên chấp nhận thay thế |
| A09 Thông báo | FCM test bằng Console; không có push tự động theo đăng ký/hủy khi chưa có web/admin phát tin | Không có server hoặc Functions. Inbox Firestore do vai trò web/admin tạo, mobile chỉ đọc |

## 1. Nguồn và thứ tự đối chiếu

- Đề Lab 3: `C:/Users/ThinhCri/Downloads/PRM393 - Lab 3 Cloud-Enabled Mobile App (Firebase, Patrol, AI Code Review).pdf`, mục 3–6: mọi màn Final UI, mọi flow, MVVM, sáu dịch vụ Firebase, dữ liệu thật, xuất/upload file.
- [Figma Final UI](https://www.figma.com/design/WC21Na9ZDS8jjM2LzPKeXa/PRM393?node-id=153-2), [Components](https://www.figma.com/design/WC21Na9ZDS8jjM2LzPKeXa/PRM393?node-id=23-2), [Prototype](https://www.figma.com/design/WC21Na9ZDS8jjM2LzPKeXa/PRM393?node-id=199-1681).
- Đã đọc trực tiếp danh sách node page 03/05 ngày 30/10/2026. Page 03 còn cả bản 156/157 cũ và các màn redesign; ưu tiên các node được chỉ rõ trong bảng dưới. Đây là kiểm kê cấu trúc, không phải kết quả chạy Present hay kiểm tra pixel.
- Tài liệu local đã đọc: `D:/Ky8/prm323-lab2-group2/ux/persona.md`, `ux/user-flow.md`, `design/screen-spec.md`, `handoff/flutter-handoff.md`, `project/design/design-system.md` (các đường dẫn sau cùng thuộc cùng repo Lab 2).
- Khi Markdown cũ mâu thuẫn: áp dụng đề Lab 3 cho yêu cầu mới; giữ quy tắc sản phẩm và flow đã chốt cho nghiệp vụ. Ghi quyết định tại mục 6, không âm thầm triển khai theo dòng lỗi.

Các route/widget/ViewModel dưới đây đã được đối chiếu với source mobile ngày 07/11/2026. Đây là ánh xạ triển khai, không thay thế bằng chứng E2E hoặc khẳng định pixel 1:1. ID Figma là node thật đã đọc; mở bằng URL file với `?node-id=ID` (đổi dấu `:` thành `-`).

## 2. Ma trận màn hình và dữ liệu

| Màn / node Final UI tham chiếu | Route triển khai | Screen / ViewModel | Nguồn dữ liệu | Trạng thái và hành vi cần giữ |
|---|---|---|---|---|
| A01a Đăng nhập `275:2894`, `177:231` | `/auth/login` | AuthScreen(mode: login) / AuthViewModel | Firebase Auth qua AuthService | Email/password + thêm Google; nhập sai, đang xác thực, hủy Google, lỗi mạng; giữ đích quay lại |
| A01b Tạo tài khoản `177:409`, đổi email `177:476` | `/auth/register` | AuthScreen(mode: register/change-email) / AuthViewModel | AuthService (FirebaseAuthService) | Form trống; lỗi trường/mạng; biến thể đổi email giữ họ tên; không hỏi khóa K |
| A01c Kiểm tra email `177:610` | `/auth/verify-email` | AuthScreen(mode: verify) / AuthViewModel | AuthService | Đã gửi, chưa xác nhận, đang kiểm tra, lỗi gửi lại; backend xác nhận mới tiếp tục |
| A01d Quên mật khẩu `177:721` | `/auth/forgot-password` | AuthScreen(mode: reset) / AuthViewModel | AuthService | Nhập, sai email, đang gửi, kiểm tra hộp thư, lỗi; reset bằng liên kết email ngoài app |
| A02 Khám phá `164:241` | `/discover` | EventListScreen / EventFilterViewModel + recommendationFeedProvider | EventService: Firestore events/clubs | Loading/data/empty/error; tìm/lọc; giữ vị trí cuộn; thông tin thời gian/địa điểm |
| A03 Kết quả `179:599`, lọc `179:670`, sheet `179:908` | `/discover/search` | EventListScreen(search: true) / EventFilterViewModel + eventFeedProvider | EventService; SearchFilter trong VM | Có/không kết quả, loading `179:800`, error `179:852`; đổi/xóa lọc; Back giữ trạng thái |
| A04 Chi tiết `164:336`; tự do `214:1681` | `/events/:eventId` | EventDetailScreen / eventProvider + eventAvailabilityProvider | EventService (FirestoreEventService) | Còn chỗ/hết chỗ/hết hạn/hủy/đã đăng ký/tự do; loading/error/not-found; thông tin sâu, diễn giả khi có |
| A05 Sinh viên `179:965`, khách `179:1046` | `/events/:eventId/register` | RegistrationFormScreen / BookingViewModel | AuthService; EventService (FirestoreEventService) | Lỗi K `179:1125`, gửi `179:1206`, chưa rõ `179:1287`, kiểm tra `179:1370`, được gửi lại `179:1455`; giữ form |
| A06 Xác nhận `179:1538`, khách `255:2802` | `/registrations/:registrationId/success` | RegistrationDetailScreen(success: true) / registrationProvider | EventService: registrations snapshot từ Firestore | Chỉ hiện sau xác nhận; không QR/vé cá nhân; về A07 hoặc A08; không gửi lại khi Back |
| A07 Lịch `179:1581`, khách `255:3204` | `/schedule` | LiveScheduleScreen / scheduleEntriesProvider + ScheduleTabViewModel | EventService: Firestore events/registrations | Trống `179:1637`, sau tự hủy `179:1686`, lịch sử `179:1739`, kết thúc `179:1795`, loading/error `179:1851/1896`, CLB hủy `194:1699` |
| A08 Chi tiết đăng ký `181:1345`, khách `255:2832` | `/registrations/:registrationId` | RegistrationDetailScreen / registrationProvider + BookingViewModel | EventService + checkinSessionProvider | Dialog `181:1388`, đang hủy `181:1443`, chưa rõ `181:1488`, kiểm tra `181:1529`, phiên mở `181:1572`, đã điểm danh `181:1611`, tự hủy/CLB hủy/không thể hủy |
| A09 Thông báo `181:1767` | `/notifications` | NotificationsTabScreen / NotificationsViewModel | NotificationService: Firestore inbox; FCM là tín hiệu giao tin | Đổi lịch/địa điểm `181:1816`, hủy `181:1862`, empty/error `181:1902/1942`; đọc/chưa đọc; mở dữ liệu mới nhất |
| A10 Hồ sơ `181:1982`, sửa `181:2030` | `/account`, `/account/edit` | AccountTabScreen, ProfileEditScreen / ProfileViewModel + SessionViewModel | AuthService (FirebaseAuthService) | Đang lưu `181:2073`, email chờ `181:2118`, lỗi `181:2161`, chưa lưu `181:2208`, hợp lệ `194:1722`; đăng xuất |
| A11 Quét `182:1804` | `/registrations/:registrationId/scan` | ScannerScreen / BookingViewModel + QrCameraService | QrCameraService + EventService | Chưa quyền `182:1822`, xử lý `182:1843`, sai sự kiện `182:1866`, phiên đóng `182:1887`, không đăng ký `182:1908`, chưa rõ `182:1930`, tra trạng thái `182:1951`, hủy `182:1974`; QR không hợp lệ |
| A12 Kết quả `182:1995` | `/registrations/:registrationId/check-in` | RegistrationDetailScreen(checkInResult: true) / registrationProvider | EventService | Mới, đã ghi nhận `182:2036`, xem lại khi phiên đóng, CLB hủy `182:2074`, lỗi tải; giữ giờ gốc; không email/điện thoại |
| L3-01 Khu demo Firebase — mới, chưa có node | `/account/firebase-demo` | CloudToolsScreen / CloudToolsViewModel | CloudServices + NotificationService | Xem config, refresh, lỗi; mở A09/export, test crash có xác nhận rõ |
| L3-02 Xuất và upload — mới, chưa có node | `/account/export` | ExportScreen / ExportViewModel | EventService + ReportService + ReportStorageService | Tạo PDF từ lịch, upload Cloudinary, URL, empty/error/retry; cảnh báo URL chia sẻ được |

Các state dùng cùng route và model, không tạo route riêng cho mọi spinner hoặc dialog. A01a–d vẫn được triển khai, không bị xóa vì bổ sung Google. Lỗi tải A06/A12 là lỗi lấy lại dữ liệu, không đảo ngược kết quả nghiệp vụ đã ghi nhận.

## 3. Flow → route → persona → kết quả

| Flow | Đường chính Lab 3 | Nhánh và phục hồi | Nguồn dữ liệu / widget chính |
|---|---|---|---|
| F1 — P01 và P02 | Login nếu chưa có phiên → Discover → Search → EventDetail → RegistrationForm → Success → Schedule | Empty tìm kiếm; đã có đăng ký mở A08 trước khi xét chỗ/hạn; form khách ẩn K; lỗi form; hết điều kiện; chưa rõ kết quả thì tra thao tác, không gửi trùng | Auth/Event/Registration/ProfileService; EventCard, FilterSheet, ParticipantForm, EventPanel + BookingFeedback/AppErrorState |
| F1 tự do — P03 | Login theo yêu cầu Lab 3 → Discover/Search hoặc deep link → EventDetail tự do → Back | Không tạo đăng ký, không thêm lịch, không QR. Hạn chế mới về đăng nhập ghi tại D02 | EventService; EventCardFree, EventPanel + Text |
| F2 — P01/P02 | Schedule → RegistrationDetail → ConfirmCancelDialog → đang xử lý → Schedule cập nhật | Giữ đăng ký; quá giờ/đã điểm danh không hủy; CLB hủy khác tự hủy; mạng lỗi tra kết quả; nhánh Notifications → A04/A08; Account → Schedule | Registration/Event/Notification/ProfileService; Tabs, Summary, Dialog, Banner |
| F4A — P01/P02 | RegistrationDetail → Scanner → server xác nhận → CheckInResult → Schedule | Camera bị từ chối; sai QR/event; chưa đăng ký về A04; phiên đóng/hủy; đã điểm danh xem giờ cũ; chưa rõ thì tra trạng thái | Camera/CheckIn/EventService; CameraViewport, ErrorState, EventPanel trong RegistrationDetailScreen |
| Bổ sung Lab 3 | Account → export/upload; Account → FirebaseDemo; push → A04/A08 | Quyền notification bị từ chối; file rỗng, mất mạng; config dùng mặc định; auth hết hạn | Report/Cloudinary/Config/Diagnostics/NotificationService |

P01: giữ mục tiêu đo từ A02 đến đăng ký ≤90 giây, QR ≤30 giây với mạng ổn định. P02: không yêu cầu email FPTU/khóa K. P03: đo đọc giờ/địa điểm ≤60 giây sau khi vào màn nội dung; yêu cầu không tạo tài khoản của persona gốc bị ảnh hưởng bởi D02, phải nêu trong báo cáo. Các mốc là mục tiêu, chưa phải kết quả test.

## 4. Component → widget

Bảng ánh xạ đã có; code đã triển khai nhưng cần kiểm tra ảnh Figma/Android trước khi chốt tương đương. Variant triển khai phải đối chiếu instance thực khi dựng widget; danh sách dưới ghi trạng thái cần hỗ trợ, không khẳng định đã đọc toàn bộ property của từng variant.

| Component page 05 (node) | Widget dùng lại | State/thuộc tính |
|---|---|---|
| Button `24:341` | AppButton | primary/secondary/text, pressed/disabled/loading |
| Icon Button `24:431` | AppIconButton | icon, tooltip, enabled/loading, vùng chạm 48 |
| Text Field `24:711` | AppTextField | default/focus/filled/error/disabled, password visibility |
| Search Field `24:764` | AppSearchField | query, clear, focus, submit; icon/text căn trái |
| Filter Button `24:777`, Filter Chip `24:794` | AppButton + FilterChip (Material) | selected, count, removable |
| Choice Chip `24:801` | ChoiceChip (Material) | selected/enabled; student/guest |
| Status Badge `24:886` | AppStatusBadge | chữ + icon + semantic status color |
| Top App Bar `24:945` | AppTopBar | title căn trái, back/action, Semantics |
| Bottom Navigation Item `24:954`, Navigation `24:955` | AppNavigationBar | bốn tab, selected; giữ stack/tab |
| Tab `24:986` | ChoiceChip + ScheduleTabViewModel | selected, nhãn và nội dung tương ứng |
| Event Card Required `24:1438`, Free `29:358` | EventCard | registrationMode, pressed, current status; free ẩn chỗ/hạn |
| Event Summary `24:1455` | EventSummary | dữ liệu thật, không bịa mã/vé |
| Metadata Row `24:1494` | EventPanel + Text | icon, label, value, wrap |
| Information Card `24:1495` | EventPanel | title/body/tone |
| Participant Card `24:1521` | EventPanel trong RegistrationDetailScreen | student/guest, che contact trên A12 |
| Registration Details Group `24:1535` | RegistrationDetailScreen + EventPanel | snapshot thông tin lúc đăng ký |
| Inline Message `24:1655` | EventPanel + BookingFeedback/AppErrorState | info/error/warning/success, retry |
| Empty State `24:1704` | AppEmptyState | thông báo + hành động |
| Loading State `24:1723` | AppLoadingState | skeleton/spinner, loading semantics |
| Toast or Banner `24:1764` | ScaffoldMessenger/SnackBar | thông báo và dismiss nếu phù hợp |
| Bottom Sheet `24:1769` | showModalBottomSheet + _EventFilterSheet | mở/đóng, draft filter/apply/reset |
| Confirmation Dialog `24:1797` | AppConfirmationDialog | confirm/cancel/pending, tránh bấm lặp |
| Icon/* `23:7`…`23:61`, __Event Image `24:994` | EventAssetIcon + ảnh bìa trong EventSummary | icon nhất quán, ảnh loading/error/placeholder |

ErrorState được compose từ EventPanel + BookingFeedback/AppErrorState + nút Thử lại; các phần mới GoogleSignInButton, CameraViewport, UploadProgress và ConfigValueTile dùng theme, bổ sung vào thiết kế Lab 3.

## 5. Điều hướng và quy tắc nhất quán

- AuthGate chờ Firebase xác định phiên; signed-out → A01a; email/password chưa verify → A01c; phiên hợp lệ → đích nội bộ đang chờ hoặc A02. Không dùng màn đang tải như signed-out.
- Bốn tab: A02/A07/A09/A10. Detail/form nằm trên stack; Back app và hệ thống cùng kết quả. Giữ filter/tab/scroll; dialog không tự gửi khi đóng.
- Deep link/push chỉ chứa loại đích và ID, kiểm tra đăng nhập + quyền trước khi đọc. Không dùng route tùy ý từ payload. Lỗi/not-found có Back hoặc về tab nguồn.
- Không tự lưu mật khẩu; chỉ giữ form trong bộ nhớ khi lỗi. Đăng xuất hủy subscription, xóa state/draft/cache riêng theo user, gỡ token push khỏi UID trước khi sign-out nếu có mạng.
- Nhóm/K tự khai không cấp quyền. CLB/admin luôn dùng web riêng, không thêm nút quản trị vào mobile.

## 6. Nhật ký thay đổi và xử lý mâu thuẫn

| ID | Nguồn/khác biệt | Quyết định Lab 3 và lý do | Trạng thái |
|---|---|---|---|
| D01 | A01 chỉ email/password; Lab 3 mục 6 yêu cầu Google | Thêm Google Sign-In, giữ A01a–d để không mất màn Lab 2; backend xác định provider và verified state | Code auth đã thêm; Figma còn chờ đồng bộ |
| D02 | Lab 2 cho khách xem A02–A04; rubric Lab 3 yêu cầu signed-out → login | Bản nộp Lab 3 có AuthGate trước nội dung; giữ deep link để vào đúng sự kiện sau login. P03 vẫn không phải đăng ký sự kiện nhưng phải đăng nhập app | Đặc tả xong; Figma chưa cập nhật; nêu ảnh hưởng persona khi trình bày |
| D03 | Lab 2 chưa có export/config/crash demo | Thêm L3-01/L3-02 dưới A10, không đổi bốn tab. PDF từ lịch thật, không xuất dữ liệu người khác | Code đã có; Figma và ảnh đối chiếu chưa hoàn tất |
| D04 | screen-spec mục 3 gọi A06 là vé QR; mục 1–2 và flow phủ nhận vé cá nhân | A06 chỉ xác nhận đăng ký; A11 quét QR web CLB; A12 không hiện email/phone | Giải quyết cho triển khai; không sửa repo Lab 2 |
| D05 | handoff cũ A01 luôn → A02; A10 chỉ logout; A12 coi đã check-in là lỗi trong bảng cũ | Giữ pending destination; A10 có edit profile như Figma `181:2030`; đã check-in trả kết quả cũ hợp lệ, không tạo mới | Giải quyết cho triển khai |
| D06 | token cũ vùng chạm 44, frame 390; đề yêu cầu ≥48 và 360/412 | Token touchMin=48, layout adaptive 360/412, body ≥14; không kéo giãn theo một ảnh cố định | Đặc tả xong; đo lại khi có app |
| D07 | Google account và thay email ở A10 | Giữ email đăng nhập do Google quản lý; A10 sửa email liên hệ với xác nhận riêng. Tài khoản password dùng cập nhật email có xác minh/reauth. Không tự liên kết hai provider chỉ vì cùng email | Đặc tả xong; cần thể hiện rõ nhãn trên Figma |

## 7. Điểm hoàn thành bước 1

Cập nhật triển khai 31/10/2026: A01a–d đã có Flutter screen và Firebase Auth adapter; Google button đã thêm. Tham chiếu [firebase-setup.md](firebase-setup.md) cho khác biệt UI: summary chỉ hiển thị khi có dữ liệu thật ở bước F1, đổi email dùng xác thực lại/link mới thay vì tạo account lần hai. Chưa đồng bộ Figma. Đã cấu hình project `eventhub-group4`; chủ dự án xác nhận Google Sign-In thành công, chưa kiểm thử toàn bộ cloud. Không thay trạng thái toàn bộ ma trận thành hoàn thành chỉ dựa trên việc viết auth.

Đã có ánh xạ A01a–d/A02–A12, state/flow, component và thay đổi Lab 3; đã có route/widget và bằng chứng local được ghi ở phần trạng thái code. **Còn thao tác đồng bộ Figma cho D01/D02/D03/D07 trước khi coi bước 1 hoàn tất toàn bộ theo kế hoạch.** Lần này người dùng yêu cầu tài liệu bước 1–2; chưa chỉnh file Figma đã chốt của Lab 2. Tiếp tục bằng bản thiết kế Lab 3 có truy vết các thay đổi này, sau đó bước 3.


## Quy trình ghi nhận thay đổi UI khi triển khai

Nguồn: đề Lab 3 trang 3 (Changes to the design), trang 11 (báo cáo và slide). Mọi thay đổi so với Final UI Lab 2 phải có lý do ở tài liệu này và đồng bộ Figma. Ảnh trước/sau lưu theo [quy ước bằng chứng](../evidence/design-changes/README.md). Không xem mọi khác biệt UI là thay đổi đã được chấp nhận; lỗi triển khai cần sửa về đúng thiết kế.

| ID | Màn / flow | Trước → sau | Lý do | Bằng chứng trước/sau | Figma / commit | Trạng thái |
|---|---|---|---|---|---|---|

Chưa tạo bản ghi mới chỉ từ mẫu: cần ảnh thực, thay đổi cụ thể và kiểm tra trước khi ghi hoàn tất. Các quyết định tại mục 6 vẫn cần được bổ sung bằng chứng và trạng thái thực tế tương ứng.

Ưu tiên hiện tại: dùng bộ UI prototype làm nền để phát triển app thật trên Firebase project chung của nhóm; lần lượt thay dữ liệu mô phỏng bằng service/ViewModel thật theo F1, F2, F4A. Không coi bản mô phỏng là đầu ra cloud hoàn chỉnh. Sửa UI phát sinh phải đi qua quy trình trên.

## Trạng thái code thực tế 04/11/2026 — không thay thế ma trận yêu cầu

| Màn | Code thực tế | Nguồn | Trạng thái |
|---|---|---|---|
| A01a–d | AuthScreen / AuthViewModel | Firebase Auth | Google sign-in chủ dự án xác nhận; các nhánh còn cần test cloud |
| A02/A03 | EventListScreen / EventFilterViewModel + eventFeedProvider | Firestore EventService | Đã code/test local, chưa test nguồn CLB thật |
| A04 | EventDetailScreen / eventAvailabilityProvider | EventService, registrationsProvider | Đã code; ưu tiên active registration trước điều kiện chỗ/hạn |
| A05 | RegistrationFormScreen / BookingViewModel | Firestore transaction + secure pending store | Đã code/test form, Rules/index deploy; chưa test cloud Android |
| A06/A08 | RegistrationDetailScreen / registrationProvider + BookingViewModel | server-owned registration | Đã code; snapshot/confirmed, dialog hủy/recovery; chưa cloud |
| A07 | LiveScheduleScreen / scheduleEntriesProvider | owner registrations + event streams | Đã code; tách tự hủy/CLB hủy và ended; chưa cloud |
| A09 | NotificationsTabScreen / NotificationsViewModel | owner Firestore notifications | Đã nối in-app feed/read/navigation; FCM tự động theo event chưa có, chưa test ba trạng thái |
| A11 | ScannerScreen / BookingViewModel + QrCameraService | native camera + Firestore Rules | Đã code; QR hợp lệ/sai test emulator, chưa test camera với QR web CLB thật |
| A12 | RegistrationDetailScreen(checkInResult) | confirmed server checkInAt | Đã code/test privacy; chưa cloud |
| A10/edit, L3-01/02 | ProfileEditScreen, CloudToolsScreen, ExportScreen và ViewModel | Firebase Auth, CloudServices, ReportStorage | Đã code/test local; cloud/Figma còn cần xác minh |

Artwork Lab 2 dùng lại từ prototype đã dựng và SVG đã tải; dữ liệu nội dung sự kiện đọc từ Firestore, cover fallback cho nội dung khác cần review và ghi bằng chứng nếu khác thiết kế đã chốt. Chưa tuyên bố Figma đã đồng bộ hoặc mọi màn pixel-perfect.

### D08 — Phục hồi thao tác mạng và nội dung cover từ dữ liệu

A05/A08/A11 bổ sung nhãn sự kiện của thao tác đang chờ và nút “Thử lại cùng thao tác”. Nút gửi lại payload + operation ID cũ, không tạo đăng ký mới; lý do: backend có thể đã ghi nhận dù client mất phản hồi, cần retry idempotent. Cần review UI và đồng bộ Figma trước khi chốt; đã có ảnh đối chiếu A05 trong thư mục D08 bên dưới; các màn A08/A11 còn cần đối chiếu riêng, không coi là đã duyệt. Cover UX workshop và Acoustic dùng lại artwork đã có; fallback cho event ngoài hai artwork cần được đối chiếu riêng, không gọi là bản Final UI đã duyệt.


### Bằng chứng thay đổi Lab 3

- [D03 — Tài khoản và công cụ Firebase](../evidence/design-changes/D03-firebase-tools/README.md): baseline Figma A10 và ảnh Flutter sau thay đổi.
- [D08 — Phục hồi A05](../evidence/design-changes/D08-network-recovery/README.md): baseline Figma A05 và trạng thái pending/retry Flutter.
- D07: Google email chỉ đọc vì thuộc provider; không triển khai contact-email độc lập. Cần đồng bộ quyết định và màn Profile lên Figma.
- D10: thêm màn khởi tạo Firebase đang tải/thử lại để timeout không bị hiểu nhầm là thiếu cấu hình. Có test retry; cần bổ sung state này lên Figma.

Ảnh Flutter UI fixture chỉ chứng minh bố cục; không dùng làm bằng chứng nghiệp vụ cloud hoặc xác nhận thầy đã duyệt.


### D11 — Khám phá: bộ lọc và dữ liệu mẫu

Tách nhãn CLB, sửa khoảng cách và empty state, chỉ hiện reset khi cần. Thêm hai event demo có nhãn rõ để xem giao diện theo yêu cầu chủ dự án; không dùng chúng làm bằng chứng sự kiện CLB thật. Xem [ảnh trước/sau và lý do](../evidence/design-changes/D11-discover-filters/README.md). Chưa cập nhật Figma.


### D12 — Phân biệt Khám phá và danh sách đầy đủ

01/11/2026: Khám phá chỉ có ô tìm kiếm và tối đa 3 gợi ý (vẫn tuân theo giới hạn Remote Config nếu nhỏ hơn 3), không lặp bộ lọc nâng cao/số kết quả. Xem tất cả mở danh sách đầy đủ, reset điều kiện cũ, tiêu đề “Tất cả sự kiện”; có từ khóa mới dùng “Kết quả tìm kiếm”. Bộ lọc CLB/chủ đề/ngày và số kết quả thuộc màn danh sách. Gợi ý Khám phá độc lập bộ lọc ở màn tìm kiếm khi Back. Lý do: giảm trùng vai trò hai màn theo yêu cầu người dùng; chưa cập nhật Figma.

04/11/2026: bỏ nút “Xem tất cả” trên Khám phá theo yêu cầu người dùng. Thanh tìm kiếm mở A03 để xem kết quả và dùng bộ lọc; các thẻ gợi ý vẫn tuân theo Remote Config. Lý do: tránh lặp hai cách vào danh sách từ cùng màn. Cần đồng bộ Figma.


### D13 — Tài khoản và đích sau đăng nhập

04/11/2026: bỏ nhãn “Email đã xác nhận”, đoạn giải thích FPTU và nút xem thử component khỏi A10 theo yêu cầu người dùng. Auth verification vẫn được giữ trong nghiệp vụ. Khi đăng nhập từ đích Account chuyển về Khám phá, tránh quay lại Account sau logout/login; đích đăng ký sự kiện vẫn được giữ. Chưa cập nhật Figma.

04/11/2026: bỏ nút “Tiện ích Firebase” khỏi A10 theo yêu cầu người dùng. 05/11/2026: thêm lại lối vào **Dịch vụ Firebase** vì mục 3 của đề Lab 3 yêu cầu khu demo truy cập được trên Profile; màn gồm thông báo, xuất/upload, giá trị Remote Config và Crashlytics test. Không đưa nút xem thử component trở lại. Cần cập nhật Figma và lưu ảnh trước/sau của thay đổi này.

04/11/2026: căn giữa địa chỉ email trên A01c “Kiểm tra email” để khớp trục của tiêu đề và các thao tác; trước đó email bị lệch trái. Cần đồng bộ Figma nếu bản thiết kế hiện dùng căn trái.

### D14 — Ảnh bìa theo sự kiện

07/11/2026: thay cover cam trên 5 sự kiện bằng ảnh minh họa AI riêng (thiết kế, acoustic, cầu lông, trồng cây, nghề nghiệp). Firestore chọn ảnh qua coverKey; hỗ trợ coverUrl HTTPS cho nội dung sau này. Ảnh bundled để không thay đổi preset Cloudinary PDF. Lý do: phân biệt sự kiện theo yêu cầu chủ dự án; cần đồng bộ Figma. Danh sách sự kiện vẫn lấy từ Firestore, không có seed tự chạy trong app.

## Bàn giao mục 3 — 07/11/2026

Chủ dự án báo đã test toàn bộ chức năng; chưa có tập ảnh/video đầy đủ của lượt test đó trong repo nên ghi nhận là user-reported. Danh mục bằng chứng mục 3 ở `evidence/task3/README.md`. Không tự đánh dấu ảnh tồn tại hoặc cloud pass.

Figma giữ nguyên theo quyết định của chủ dự án; đây chưa phải miễn trừ từ giảng viên. PDF mục 3 yêu cầu cập nhật Figma. Giải pháp báo cáo/slides đối chiếu chỉ thay thế được khi giảng viên chấp thuận. Không tự sửa Figma hoặc ghi đã được chấp thuận.

### D15 — Chuẩn hóa component và accessibility sau audit Lab3

07/11/2026: màn production dùng AppTopBar, AppButton text variant, AppConfirmationDialog/AppInfoDialog và AppChoiceChip dùng lại. Placeholder input đổi về #5F6B7A theo token Lab2 (contrast trên trắng khoảng5.43:1), input border về #CBD2DC; bodySmall nâng14sp, subtitle appbar dùng bodyMedium. Không đổi route/tab hay nghiệp vụ; glyph Back được thống nhất theo AppTopBar. Camera UI chỉ render, lifecycle và error state chuyển sang ScannerViewModel. Bằng chứng trước sửa trong evidence/instrumentation; chưa có ảnh mọi màn sau sửa, chưa đồng bộ Figma. Không coi ghi log là thay thế cập nhật Figma theo đề.
