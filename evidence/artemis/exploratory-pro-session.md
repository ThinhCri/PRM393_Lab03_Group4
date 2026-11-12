# ARTEMIS Pro Exploratory Session Report

- **Trace ID:** `c8a40964-c1e0-4b14-9867-c1a2eacd4651`
- **Raw Trace JSON:** [exploratory-c8a40964-c1e0-4b14-9867-c1a2eacd4651.json](exploratory-c8a40964-c1e0-4b14-9867-c1a2eacd4651.json)
- **Script:** [e2e_test/explore.py](../../e2e_test/explore.py) (`ARTEMIS_ALLOW_PRO=1`, profile `pro`)
- **Device & Build:** `emulator-5554` (AVD `Fitmate_Medium_API35`, Android 15 / API 35), `app-profile.apk` (`--profile` + Cloudinary defines)
- **Test Account:** `<TEST_ACCOUNT>` (redacted dedicated Google test account)
- **Status:** `completed` | **Checker:** `PASS` | **`meets_15_to_30_minutes`:** `true`
- **Duration:** `1056.453s` (**17m 36s**, within the required 15–30 minute window)
- **Execution Metrics:** **78 steps**, **229 model calls**, **0 app crashes / ANRs**, **0 blocking bugs**

---

## 1. Explored Functional Phases (Steps 1–78)

| Phase | Steps | Flow / Feature | Actions & Verifications Observed |
|---|---|---|---|
| 1 | 1–10 | F1 Search (`A02` / `A03`) | Searched `'Workshop'` (returned 5 matching events including *Workshop Thiết kế trải nghiệm người dùng*), then zero-result query `'xyzabc123'` triggering empty state `'Chưa tìm thấy sự kiện'` (`0 sự kiện`) + `'Thử từ khóa khác hoặc đổi bộ lọc'`, and verified clear/reset. |
| 2 | 10–15 | F1 Filters (`A03` Bottom Sheet) | Inspected quick filter chips and `'Lọc sự kiện'` bottom sheet; applied `'Thiết kế'` chip (narrowing list to 1 event), tested `'Xóa lọc'` reset and state persistence. |
| 3 | 19–26 | F1 Discovery & Event Detail (`A02` / `A04`) | Opened ≥ 3 distinct event cards (*Workshop Thiết kế trải nghiệm người dùng*, *Đêm nhạc Acoustic*, etc.), checked status/slot badges (`Cần đăng ký`, `Còn 29 chỗ`), metadata layout, and Back state persistence. |
| 4–5 | 27–37 | F1 Registration Form & State Isolation (`A05` / `A06`) | Opened *Giao hữu cầu lông: Campus Cup*; triggered empty `'Khóa K *'` validation error (`'Vui lòng nhập khóa K.'`); inspected `'Khách ngoài trường'` tab; verified no error-state leakage across events; submitted valid student registration (`Khóa K = 'K18'`) and confirmed slot decrement. |
| 6–7 | 38–49 | F2 Schedule & Cancellation Guard (`A07` / `A08`) | Checked all 3 tabs (`'Sắp tới'`, `'Đã kết thúc'`, `'Đã hủy'`); opened active ticket details; verified guard via `'Hủy đăng ký'` -> `'Giữ đăng ký'`; completed cancellation via `'Hủy đăng ký'` -> `'Xác nhận hủy'` -> `'Về lịch tham gia'` and verified slot restoration + `'Đã hủy'` transition. |
| 8 | 43–49 | F4A QR Scanner Check (`A08` / `A11`) | Verified `'Quét QR'` button on active upcoming registration remained safely disabled when `checkinSessions` was closed by the club; confirmed no crash or unauthorized check-in bypass. |
| 9 | 50–59 | Account & Profile Edit (`A10`) | Verified read-only `'Email tài khoản app'` (`<TEST_ACCOUNT>`) and editable `'Họ tên *'` (`Huy`); tested empty-name validation and unsaved-changes confirmation dialog (`'Bỏ thay đổi chưa lưu?'`) on Back without corrupting profile data. |
| 10 | 60–62 | Notifications (`A09`) | Scrolled through `'Thông báo'` inbox, inspected FCM test items (`'Đã đọc'`), checked item routing and footer note. |
| 11 | 63–67 | Export PDF & Cloudinary (`L3-02`) | Opened `'Xuất lịch tham gia'`, reviewed preview list (`'PDF sẽ chứa...'`) and privacy notice (no email/phone in PDF), tapped `'Tạo PDF và tải lên'`, verified upload completion + `'Sao chép liên kết PDF'` button and Back navigation. |
| 12 | 68–72 | Firebase Tools (`L3-01`) | Opened `'Dịch vụ Firebase'` -> `'Tiện ích Firebase'`, inspected `'Giới hạn gợi ý: 10'` and `'Hiện gợi ý: Bật'`, tapped `'Lấy cấu hình mới'` and observed status `'Đã nhận và kích hoạt cấu hình.'`; strictly avoided `'Test crash (debug)'`. |
| 13 | 73–78 | Timing & Accessibility Gate | Conducted extended exploratory checks (~4m Discovery dwell across Steps 75–77, tab switches, edge scrolling, layout checks) and concluded cleanly at `17m 36s`. |

---

## 2. Consolidated Bug & Issue Table

| Bug ID | Severity | Screen | Summary / Expected vs Actual |
|---|---|---|---|
| — | None (0 bugs) | All explored screens | No app crashes, ANRs, unhandled exceptions, layout overflows, or state-leakage defects occurred during the 17m 36s / 78-step exploratory run. |

---

## 3. Honest Limitations Observed

1. **F4A Live QR Scan (`checkinSessions` closed):** During the exploration window, the `'Quét QR'` button on active registrations was disabled because no club check-in session (`checkinSessions/{eventId}`) was open. The app handled this business guard cleanly without crashing, and live camera QR scanning was not executed inside the Pro emulator session.
2. **External Browser PDF Open:** The Pro session verified PDF generation, Cloudinary upload, and the `'Sao chép liên kết PDF'` UI in-app; opening the resulting Cloudinary URL externally in Chrome was verified separately in [evidence/export/02-pdf-opened-browser.png](../export/02-pdf-opened-browser.png).
3. **Personal Data Redaction:** Dedicated test account credentials were redacted to `<TEST_ACCOUNT>` in the saved JSON and this report. *(Note: minor model character-encoding artifact in the raw trace's Vietnamese status string was normalized cleanly to `'Đã nhận và kích hoạt cấu hình.'` without altering the underlying trace file.)*
