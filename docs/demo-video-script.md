# Kịch bản Video Demo EventHub — Lab 3 (5–10 phút)

Thời lượng mục tiêu: **~8 phút 30 giây** (nằm trọn trong khung 5–10 phút theo yêu cầu trang 12 đề Lab 3).  
Thứ tự các cảnh bám sát chính xác trình tự test plan và checklist trang 12 của đề bài, kết hợp quay trực tiếp màn hình thiết bị Android + Firebase/Cloudinary Console.

## Chuẩn bị trước khi quay

1. Dùng tài khoản Google test chuyên dụng (`<TEST_ACCOUNT>`), tránh lộ email/mật khẩu cá nhân khi chọn picker nếu có thể (hoặc dùng tài khoản test đã đăng nhập sẵn cho phần sau nếu cần, nhưng cảnh 1 phải quay thao tác sign-in).
2. Chuẩn bị sẵn sự kiện còn hạn/còn chỗ (ví dụ *Workshop Thiết kế trải nghiệm người dùng*), đảm bảo tài khoản chưa đăng ký trước đó.
3. Bật Analytics DebugView trước khi quay nếu muốn hiện log real-time:
   ```powershell
   adb shell setprop debug.firebase.analytics.app com.eventhub.app
   ```
4. Mở sẵn các tab trình duyệt: Firebase Console (`eventhub-group4`: Authentication Users, Remote Config, Messaging, Crashlytics, GA4 DebugView), Cloudinary Media Library (`qcfqv5oj`), và GitHub PR #3 + commits.

---

## Trình tự cảnh quay (8 phút 30 giây)

| Thời gian | Cảnh / Mục tiêu (theo PDF p.12) | Thao tác trên thiết bị & Console | Điểm cần thuyết minh |
|---|---|---|---|
| **0:00 – 0:45** | **1. Sign-in & Auth Gate** | Mở app ở trạng thái signed-out (`A01a`). Nhấn *Tiếp tục với Google* → **Hủy picker** để hiện thông báo `"Bạn đã hủy đăng nhập Google."`. Nhấn lại và chọn tài khoản test → vào `A02 Khám phá`. Chuyển nhanh sang tab **Firebase Console → Authentication → Users**. | AuthGate chặn người chưa đăng nhập; hủy picker xử lý gọn không tạo phiên giả; UID thật khớp Console `eventhub-group4`. |
| **0:45 – 2:15** | **2. Flow F1 + Error Path** | Trên `A02` gõ tìm `"zzz_no_event_8362"` → `A03` hiện **empty state** (`Chưa tìm thấy sự kiện`). Xóa từ khóa, tìm `"Workshop"` (hoặc lọc bằng bottom sheet `Lọc sự kiện`) → mở `A04 Chi tiết` → nhấn *Đăng ký sự kiện* (`A05`). Chọn *Sinh viên FPTU*, để trống *Khóa K* và nhấn gửi → **Error path:** hiện `"Vui lòng nhập khóa K."`. Nhập `K18` (hoặc chuyển tab *Khách ngoài trường*) → gửi → `A06 Xác nhận đăng ký`. | Dữ liệu đọc từ Firestore thật; validation form nằm ở `BookingViewModel`; transaction cập nhật nguyên tử `registrations` + `activeCount`. |
| **2:15 – 3:15** | **3. Flow F2 + Guard Path** | Vào tab `Lịch` (`A07`), lướt qua 3 tab *Sắp tới / Đã kết thúc / Đã hủy*. Mở đăng ký vừa tạo (`A08`) → nhấn *Hủy đăng ký* → trong dialog chọn **Giữ đăng ký** (guard path giữ nguyên trạng thái). Sau đó nhấn *Hủy đăng ký* → *Xác nhận hủy* → *Về lịch tham gia*, kiểm tra mục chuyển sang tab *Đã hủy*. | Hủy qua dialog xác nhận tránh thao tác nhầm; transaction giảm `activeCount` đồng bộ theo Security Rules. |
| **3:15 – 4:10** | **4. Flow F4A (QR & Error/Guard Path)** | Mở một đăng ký *Sắp tới* khác trên `A08`: chỉ rõ trạng thái nút `Quét QR` khi phiên điểm danh CLB đóng (`checkinSessions` closed — không cho quét bừa) và/hoặc mở `A11` xin quyền camera native (nếu phiên mở trên thiết bị test, quét QR hợp lệ → `A12 Kết quả điểm danh`; minh họa thêm nhánh sai QR / từ chối quyền). | Mobile chỉ băm SHA-256 token khi quét, không tự mở phiên; quyền camera và trạng thái lỗi điều phối qua `ScannerViewModel` (`AUD01`). |
| **4:10 – 4:55** | **5. Export PDF & Cloudinary Upload** | Vào `Tài khoản` → *Xuất lịch tham gia* (`L3-02`). Kiểm tra danh sách preview (không email/SĐT) → nhấn *Tạo PDF và tải lên*. Copy URL trả về, mở thử trên trình duyệt điện thoại/PC và chiếu tab **Cloudinary Media Library (`qcfqv5oj`)**. | Tạo PDF tiếng Việt từ dữ liệu thật của user; hiển thị tiến độ/URL; nêu trung thực Cloudinary là phương án được giảng viên chấp thuận thay Storage (URL public có cảnh báo rõ). |
| **4:55 – 5:45** | **6. Push Notification (FCM)** | Mở tab **Firebase Console → Messaging** gửi 1 test notification. Quay về app đang mở (foreground) thấy thông báo & tin vào inbox; hoặc thu app về nền/đóng app → nhận notification trên thanh trạng thái → chạm vào để app mở thẳng tab `Thông báo` (`A09`). | Đã kiểm chứng đủ 3 trạng thái foreground/background/terminated; chạm push dùng `router.go('/notifications')` mở đúng inbox và lưu lịch sử theo UID. |
| **5:45 – 6:35** | **7. Remote Config Live Change (No Rebuild)** | Tại `A02` hiện đang có nhiều thẻ gợi ý (`recommendation_limit = 10`). Mở **Firebase Console → Remote Config**, đổi `recommendation_limit = 1` (hoặc `show_recommendations = false`) và Publish. Quay lại app vào *Tài khoản → Dịch vụ Firebase* (`L3-01`), nhấn *Lấy cấu hình mới* → quay về `A02` thấy số thẻ giảm còn 1 (hoặc ẩn) **không cần rebuild**. Khôi phục `10 / true`. | Chứng minh ≥ 2 tham số Remote Config hoạt động live và an toàn với fallback defaults. |
| **6:35 – 7:20** | **8. Crashlytics & Analytics DebugView** | Trên `L3-01` nhấn *Ghi lỗi non-fatal thử nghiệm* (hoặc minh họa lỗi thực `report_upload_failed` khi mất mạng) và giải thích nút *Test crash*. Chuyển sang **Firebase Console → Crashlytics** (chỉ rõ cả 2 issue kèm `User ID` và custom key `app_flow=eventhub`) và **GA4 DebugView** (chỉ rõ `login`, `search`, `export_upload`, `remote_config_fetch`, `user_id`). | Crashlytics gắn đủ UID + key; Analytics tuân thủ plan 14 event không PII (11/14 đã có ảnh DebugView, 3 event còn lại đang chờ chụp). |
| **7:20 – 8:05** | **9. ARTEMIS E2E Run on Device** | Mở terminal PowerShell, chạy 1 ca ARTEMIS Flash trực tiếp (ví dụ `uv run --project e2e_test pytest e2e_test -k TC02 -v` hoặc `TC04`), quay cảnh emulator tự động thao tác theo agent cho tới khi pytest báo `PASSED`. Chiếu nhanh `summary.csv` (**38/48 = 79.17%**) và báo cáo Pro exploratory (**17m 36s, 78 steps, Checker PASS**). | Kiểm thử độc lập bằng `ArtemisClient`, assert JSON `final_screen` + `observed_texts`, không chỉ `SUCCESS`. |
| **8:05 – 8:30** | **10. AI Code Review Finding + Fix** | Mở `docs/code-review.md` và GitHub **PR #3** / commit `AUD01` (`9bd5bd8`) hoặc `AUD03` (`53eae7e`). Trình bày nhanh 1 finding cụ thể (ví dụ `PR03` rò rỉ Analytics cross-account hoặc `AUD01` tách `ScannerViewModel` khỏi UI), quyết định `Accepted` theo §5/§6 và diff commit đã sửa + kết luận kết thúc. | Thể hiện quy trình *AI finds; developer decides*, minh bạch mọi công cụ AI sử dụng. |

---

## Checklist sau khi quay

- [ ] Kiểm tra lại toàn bộ video để chắc chắn không lộ API key hay email cá nhân không mong muốn.
- [ ] Tải video lên Google Drive / YouTube (Unlisted), mở kiểm tra bằng **trình duyệt ẩn danh (Incognito)** để đảm bảo giảng viên xem được.
- [ ] Dán link video thay thế `<LINK_VIDEO_DEMO_5_10_PHUT>` tại [README.md](../README.md).
