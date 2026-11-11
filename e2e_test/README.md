# ARTEMIS E2E — cần host thật trước khi chạy

SDK được pin commit `351ca8422f7b5b54e80a9c1ce03a222e02415b6b` từ google/artemis. Đã đối chiếu API `ArtemisClient.run`, TaskResult.output/trace_id/succeeded trên source của commit này. Client hiện là remote SDK; daemon/model/device nằm trên host, không tự khởi chạy agent chỉ vì cài client.

Cần: Python ≥3.12, uv, Android/ADB, Artemis daemon đã cấu hình model, app thật và cloud/fixtures đã sẵn sàng. Host local/Groq và tài khoản test đã cấu hình. Đã có các lần thử lỗi; **chưa có regression được xác nhận đạt hoặc phiên Pro hoàn chỉnh**.

Thiết lập biến môi trường (không commit giá trị thật): ARTEMIS_BASE_URL, ARTEMIS_TOKEN nếu host có proxy, ARTEMIS_TEST_ACCOUNT_EMAIL, ARTEMIS_EVENT_TITLE, ARTEMIS_DEVICE. Chỉ dùng tài khoản test được chỉ rõ, đã thêm vào Android; không đưa mật khẩu vào prompt. Không expose daemon chưa có xác thực ra Internet.

```powershell
uv sync --project e2e_test
uv run --project e2e_test pytest e2e_test --collect-only
1..3 | ForEach-Object {
  $env:ARTEMIS_RUN = "$_"
  uv run --project e2e_test pytest e2e_test
}
```

Mỗi test xác minh screen code + chữ agent thực sự quan sát, không chỉ trạng thái SUCCESS. SDK result được lưu với trace ID/thời gian ở evidence/artemis; email test được thay bằng placeholder trong JSON. Screenshot/replay của host vẫn cần kiểm tra dữ liệu riêng tư trước khi chia sẻ. Fixtures thiếu được ghi skipped với lý do, không tính pass.

TC19–TC25 bao phủ free/full/expired/cancelled, mạng và QR/quyền camera; cần fixture riêng, không thay backend thật để ép lỗi. TC18 kiểm tra analytics emission bằng ADB debug log sau thao tác mới; vẫn cần ảnh console DebugView theo đề. Bật verbose log FA/FA-SVC trên thiết bị test nếu SDK không ghi event trong log mặc định. Reset debug flag sau test. Không chạy các ca thay đổi đăng ký trên tài khoản người dùng thật. Tài khoản/event test cần cho phép reset trước mỗi lần; fixture đã điểm danh phải được chuẩn bị từ web CLB/backend để TC13 có ý nghĩa.

Sau regression: một session profile Pro 15–30 phút trên host thật, lưu trace/replay và vấn đề tìm thấy. Người chạy chủ động kiểm tra quota/model trước khi bắt đầu phiên này. Không thay bằng test Flutter/emulator rồi gọi là ARTEMIS.

Exploratory: sau khi host/model/budget sẵn sàng, đặt `ARTEMIS_ALLOW_PRO=1` và chạy `uv run --project e2e_test python e2e_test/explore.py`. Script ghi thời gian thật và không tính đạt nếu dưới 15 phút; chưa thực thi phiên Pro này.

## Groq local compatibility setup (2026-11-06)

Upstream pin remains unchanged; local modifications are disclosed in `groq-compact.patch`. Apply only to a clean checkout of the pinned commit with `git apply`. Copy `groq-config.example.json` to the runtime's `config/artemis.jsonc`; set OPENAI_API_KEY locally to the Groq credential and OPENAI_BASE_URL to https://api.groq.com/openai/v1. No keys are in these files.

Changes shorten Flash instructions/tool descriptions and cap the accessibility list at 1000 characters while retaining the screenshot. Background Gemini summarization is disabled. Tool names, argument schemas and test assertions are preserved. Full traces remain local. This is an experimental compatibility configuration, not a passing test suite.

Actual TC01 retry: 86.19 seconds, failed structured-output assertion (`output=None`). Runtime marked its trace PASS but the recorded final report did not satisfy the requested schema/actions; pytest correctly rejected it. Do not count the runtime PASS label as evidence. Groq also returned quota errors during the run. The regression suite and Pro exploration are still incomplete.

## Chạy và tổng hợp để bàn giao

Các file `test_auth.py`, `test_events.py`, `test_registrations.py`, `test_profile.py`, `test_export.py`, `test_analytics.py`, `test_alternatives.py` dùng chung fixture trong `conftest.py` và kịch bản trong `cases.py`.

Sau khi cấu hình các biến ở trên, thử `pytest e2e_test -k TC01 -v`. Khi ca thử hoạt động đúng mới chạy:

```powershell
.\e2e_test\run_regression.ps1
```

Có thể dùng `-Selection 'TC01 or TC03'` để chẩn đoán một nhóm; không dùng kết quả nhóm nhỏ thay cho yêu cầu bao phủ toàn bộ flow. Script chạy 3 lượt, lưu JUnit và `summary.csv` tại một thư mục có timestamp trong `evidence/artemis/local-runs/` (gitignore vì log có thể chứa dữ liệu tài khoản). Bảng tính theo kết quả pytest cuối cùng, kể cả assertion bổ sung của TC18, không theo status tự báo của model. Skipped không tính là pass; thiếu 3 lượt phải review. Đây là thời gian pytest đo cho từng ca.

Trước nộp: kiểm tra/ẩn dữ liệu riêng tư trong XML và trace, sao chép bằng chứng đã duyệt sang thư mục evidence được theo dõi Git, bổ sung lý do từng lỗi/skipped và liên kết replay. Script không tự reset dữ liệu cloud; chuẩn bị fixture độc lập theo test-plan trước mỗi ca.

## Groq slow mode

Local runtime `ARTEMIS_MIN_MODEL_INTERVAL_SECONDS=90` giãn nhịp mỗi model call; `ARTEMIS_MODEL_MAX_TOKENS=1024` giới hạn output. Pytest `ARTEMIS_CASE_TIMEOUT_SECONDS` mặc định 1800 giây để không timeout chỉ vì nhịp chậm. Chạy tuần tự; không chạy nhiều model task song song. Đây là cấu hình tương thích, không bỏ assertion hoặc thay thế yêu cầu 3 lượt/ca. Phiên Pro vẫn phải 15–30 phút thật.

Transport pacing: `ARTEMIS_GROQ_HTTP_INTERVAL_SECONDS=90` applies to all OpenAI-compatible model HTTP requests from the runtime, including auxiliary observations and SDK retries. With this set, use `ARTEMIS_MIN_MODEL_INTERVAL_SECONDS=0` to avoid double delays. Test timeout can be set via `ARTEMIS_CASE_TIMEOUT_SECONDS` (seconds). This local runtime patch is disclosed; do not claim it is unmodified upstream.

## TC03 structured-output retry — 07/11/2026

Trace 501cad31-7650-4659-bbef-140b6bd22edd completed without recent 429 responses, but pytest failed: final_screen was at the JSON root rather than observed_values.final_screen. Reported Vietnamese empty-state text also did not match current UI source (Chưa tìm thấy sự kiện). Clarified exact JSON structure and verbatim observations in the prompt; assertions were not relaxed and the old attempt remains failed. A fresh native run is required.
