CASES = [
 ("TC01", "If already signed in, use Account > Logout. Then sign in with Google account {account}, navigate to Discover and verify its heading Sắp tới. Stop only on Discover.", "A02", "Sắp tới", False),
 ("TC02", "At login tap Google then cancel Android account picker. Stop at login and read cancellation feedback.", "A01a", "Đăng nhập", False),
 ("TC03", "Sign in with {account}. Focus the search field and enter zzz_no_event_8362; if the text stays on the keyboard clipboard chip instead of inside the field, tap the clipboard chip so zzz_no_event_8362 appears inside the search field, then submit search.", "A03", "Chưa tìm thấy", False),
 ("TC04", "Sign in with {account}. Search {event}, select its card and read event details.", "A04", "Giới thiệu", True),
 ("TC05", "Sign in with {account}. Open {event}, choose Register. If an active registration exists and the app permits cancellation, cancel it first; otherwise report setup missing. Choose student, clear cohort and submit. Stop at field error.", "A05", "Vui lòng nhập khóa K", True),
 ("TC06", "Sign in with {account}. For {event}, ensure no active registration (cancel only if app allows). Register as guest using the test name/email. Do not enter cohort. Stop at confirmed result; report setup missing if event is full/expired.", "A06", "Đăng ký được xác nhận", True),
 ("TC07", "Sign in with {account}. Open Schedule; inspect Upcoming, Ended and Cancelled tabs. Stop on Cancelled.", "A07", "Đã hủy", False),
 ("TC08", "Sign in with {account}. Ensure an active, cancellable registration for {event}; register if allowed. Open its detail and cancellation dialog, choose Keep registration. Stop on active registration detail.", "A08", "Đã đăng ký", True),
 ("TC09", "Sign in with {account}. Ensure an active cancellable registration for {event}; cancel and confirm. Open Schedule > Cancelled and observe that entry.", "A07", "Đã hủy", True),
 ("TC10", "Sign in with {account}. Open Notifications. If a notification exists, open it and verify the current destination, then return to Notifications.", "A09", "Thông báo", False),
 ("TC11", "Sign in with {account}. Open Account > Edit information. Do not change Google email. Stop on edit screen and inspect the email label.", "A10-edit", "Email tài khoản app", False),
 ("TC12", "Sign in with {account}. Ensure active registration for {event}. Open its detail > Scan QR (if Scan QR is disabled because the check-in session is closed, set precondition_failed to 'Check-in session is closed' and stop without reporting A11). Handle native camera permission dialog by Allow if shown. Do not scan unknown QR. Stop on scan screen.", "A11", "Quét mã QR do CLB", True),
 ("TC13", "Sign in with {account}. Open the known already checked-in test registration for {event} and View confirmation. If no such fixture exists, report setup missing. Verify time displayed; do not create a fake check-in.", "A12", "điểm danh", True),
 ("TC14", "Sign in with {account}. Open Account > Export participation schedule, inspect current preview and Create PDF and upload. Wait for an actual completed URL; report setup missing if Cloudinary upload is not configured. Stop at export result.", "L3-02", "Đã tạo và tải PDF", False),
 ("TC15", "Sign in with {account}. Open Account > Firebase tools > Fetch new config. Read the visible recommendation limit and flag; do not modify the console.", "L3-01", "Giới hạn gợi ý", False),
 ("TC16", "Sign in with {account}. Open Firebase tools > Enable device notifications. Handle the native permission dialog. Stop on Firebase tools and report actual permission feedback.", "L3-01", "thông báo", False),
 ("TC17", "Sign in with {account}. Logout through Account. Try Android Back. Confirm private schedule/details do not appear and login remains.", "A01a", "Đăng nhập", False),
]

FIXTURES = [
 ("TC19", "ARTEMIS_FREE_EVENT_TITLE", "A04", "Không cần đăng ký", "Sign in with {account}. Search and open {fixture}. Read time/location and verify no registration or QR button. Report observed_values.has_registration_button=false only if actually absent."),
 ("TC20", "ARTEMIS_FULL_EVENT_TITLE", "A04", "hết chỗ", "Sign in with {account}. Ensure no active registration for {fixture}; open it and observe full-event state. Do not edit backend."),
 ("TC21", "ARTEMIS_EXPIRED_EVENT_TITLE", "A04", "hết hạn", "Sign in with {account}. Open {fixture}, with no active registration, and observe expired registration state."),
 ("TC22", "ARTEMIS_CANCELLED_EVENT_TITLE", "A04", "hủy", "Sign in with {account}. Open {fixture} and observe that the CLB has cancelled the event."),
 ("TC23", "ARTEMIS_NETWORK_TEST_READY", "A05", "Kiểm tra trạng thái", "Sign in with {account}. Use a resettable registration for {event}. During submit, toggle network off using native Android controls, return to app and observe unknown-result recovery. Never treat a timeout as success. Restore network after observation. Report setup missing if request completed too quickly; do not fabricate an unknown state."),
 ("TC24", "ARTEMIS_WRONG_QR_READY", "A11", "không đúng sự kiện", "Sign in with {account}. For active registration {event}, open scanner. Scan the explicitly prepared QR for a different event visible to the camera. If camera/QR fixture is not ready, report setup missing."),
 ("TC25", "ARTEMIS_CAMERA_PERMISSION_READY", "A11", "camera", "Sign in with {account}. For active registration {event}, open QR scanner and deny the native camera permission dialog. Verify retry/settings guidance. Do not change account security settings; if permission was already permanently granted, report setup missing."),
]
