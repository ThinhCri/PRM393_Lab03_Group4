"""Explicit opt-in only: uses the host's Pro profile and may incur model charges."""
import asyncio
import json
import os
import re
import time
import urllib.request
from pathlib import Path


def _redact_pii(text: str) -> str:
    account = os.getenv("ARTEMIS_TEST_ACCOUNT_EMAIL")
    if account:
        text = text.replace(account, "<TEST_ACCOUNT>")
    return re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "<REDACTED_EMAIL>", text)


def _fetch_session_output(base_url: str, trace_id: str) -> str | dict | None:
    req = urllib.request.Request(f"{base_url.rstrip('/')}/api/sessions/{trace_id}/notes")
    token = os.getenv("ARTEMIS_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
    except Exception:
        return None
    notes = data.get("notes") if isinstance(data, dict) else None
    if not isinstance(notes, dict):
        return None
    for preferred in ("output.md", "output", "bug_report_eventhub.md", "eventhub_bug_report.md"):
        val = notes.get(preferred)
        if isinstance(val, str) and val.strip():
            return val
    non_plan = {
        k: v
        for k, v in notes.items()
        if isinstance(v, str) and v.strip() and k not in {"task_plan.md", "subgoal_hash_chain.json"}
    }
    return non_plan or None


def main():
    if os.getenv("ARTEMIS_ALLOW_PRO") != "1":
        raise SystemExit("Set ARTEMIS_ALLOW_PRO=1 only after configuring the team's model/host and budget")
    from artemis_client import ArtemisClient

    base_url = os.environ["ARTEMIS_BASE_URL"]
    client = ArtemisClient(base_url, token=os.getenv("ARTEMIS_TOKEN"))
    goal = (
        "Explore ONLY EventHub (com.eventhub.app) on the dedicated test device thoroughly for 18-21 minutes "
        "using ONLY the already signed-in Google test account. Do NOT sign out permanently, alter Firebase Console data, "
        "expose credentials, use personal accounts, or tap 'Test crash (debug)' / 'Tạo test crash'. "
        "CRITICAL TASK_PLAN RULE: Keep EVERY top-level milestone starting at column 0 (`- [ ] ...` with ZERO leading spaces). "
        "Whenever calling `update_note` on `task_plan`, NEVER add leading spaces to top-level milestones or overwrite the whole plan with indentation. "
        "CRITICAL LOGGING RULE: Before marking `[x]` on ANY phase (1)-(12), FIRST call `append_note(key='eventhub_exploration_log')` "
        "with concrete screens/texts/behaviors observed in that phase; whenever ANY bug, error banner, blocked UI, layout issue, or limitation is seen, "
        "immediately call `append_note(key='bug_report_eventhub')` with Bug ID, Severity, Screen, Reproduction Steps, Expected vs Actual, and Step Ref. "
        "Plan 13 concrete column-0 exploratory phases (~3-5 UI actions each): "
        "(1) F1 Search: test keyword query ('Workshop'), case/diacritic search, zero-result query ('xyzabc123') empty state, and clear/reset; "
        "(2) F1 Filters: inspect quick filter chips and 'Lọc sự kiện' bottom sheet apply vs 'Xóa lọc' and Back/scroll persistence; "
        "(3) F1 Discovery & Event Detail: open at least 3 distinct event cards, verify badges/slots/schedule/layout alignment and Back persistence; "
        "(4) F1 Registration Form ('Đăng ký sự kiện'): check Student 'Khóa K *' empty validation error ('Vui lòng nhập khóa K.'), form scroll/IME overlap, and 'Khách ngoài trường' tab fields; "
        "(5) F1 State Isolation & Booking Check: if any event returns a registration error banner, switch to a second event's detail/form to verify whether the error state leaks across events; then submit a valid Student registration (Khóa K = 'K18') on a resettable test event and check slot decrement; "
        "(6) F2 Schedule ('Lịch' -> 'Lịch tham gia'): inspect all 3 chips ('Sắp tới', 'Đã kết thúc', 'Đã hủy'), card metadata, truncation, and empty states; "
        "(7) F2 Registration Detail & Cancellation Guard: open active ticket ('Xem chi tiết đăng ký'), inspect QR/session info card, tap 'Hủy đăng ký' -> 'Giữ đăng ký' to verify safe guard, then tap 'Hủy đăng ký' -> 'Xác nhận hủy' -> 'Về lịch tham gia' and verify 'Đã hủy' + 'Khám phá' slot restore; "
        "(8) F4A QR Scanner Check: with an active upcoming registration on 'Chi tiết đăng ký', inspect 'Quét QR' button state (disabled until CLB opens checkinSessions vs enabled); if enabled, open scanner and verify permission/viewfinder/Back recovery cleanly; if disabled due to closed session, verify tapping it stays blocked safely and log that limitation honestly (then cancel the temporary test registration if keeping schedule clean); "
        "(9) Account & Profile Edit ('Tài khoản'): inspect read-only 'Email tài khoản app' and editable fields ('Họ tên *'), test validation/edit-and-Back unsaved guard (do NOT permanently corrupt display name); "
        "(10) Notifications ('Thông báo'): scroll notification center, inspect items, tap unread/read item to verify status/detail routing and Back; "
        "(11) Export ('Xuất lịch tham gia'): open Export screen, verify registration preview list ('PDF sẽ chứa ...') and privacy notice, trigger 'Tạo PDF và tải lên', inspect upload progress / URL output ('Sao chép liên kết PDF') and Back navigation; "
        "(12) Firebase Tools ('Dịch vụ Firebase' -> 'Tiện ích Firebase'): inspect Remote Config values ('Giới hạn gợi ý', 'Hiện gợi ý'), tap 'Lấy cấu hình mới', verify scroll and status messages (NEVER tap 'Test crash (debug)'); "
        "(13) Final Accessibility & Timing Gate: Keep this final top-level milestone `[ ]` until session elapsed timer `T+mm:ss` reaches AT LEAST `T+16:30` (do NOT sleep/idle — spend remaining time performing deeper exploratory checks like rapid tab switches, edge scrolling, search/filter resets, and layout checks; wrap up cleanly BEFORE `T+22:30` so Outputter completes inside 15-30 min). "
        "Report every anomaly honestly with step references; never claim unverified actions or fabricate outcomes."
    )
    expected_output = (
        "Markdown exploratory test & bug report containing: "
        "(1) Summary of all EventHub areas explored across F1, F2, F4A, Profile, Notifications, Export, and Firebase Tools with observed screens and step references; "
        "(2) Consolidated Bug Table & Reproduction Details (ID, Severity, Screen, Steps, Expected vs Actual, Step Ref); "
        "(3) Honest fixture/emulator limitations (e.g., virtual camera for F4A QR) with NO raw personal emails, passwords, or fabricated claims."
    )
    start = time.monotonic()
    result = asyncio.run(
        client.run(
            goal,
            profile="pro",
            device_serial=os.getenv("ARTEMIS_DEVICE", "emulator-5554"),
            expected_output=expected_output,
            timeout=1800,
        )
    )
    elapsed = time.monotonic() - start
    output = result.output
    if output is None and result.trace_id:
        output = _fetch_session_output(base_url, result.trace_id)
    if output is not None:
        raw_out = json.dumps(output, ensure_ascii=False) if not isinstance(output, str) else output
        redacted = _redact_pii(raw_out)
        output = redacted if isinstance(output, str) else json.loads(redacted)
    evidence = Path(__file__).resolve().parents[1] / "evidence" / "artemis"
    evidence.mkdir(parents=True, exist_ok=True)
    payload = {
        "trace_id": result.trace_id,
        "status": result.status,
        "elapsed_seconds": elapsed,
        "meets_15_to_30_minutes": 900 <= elapsed <= 1800,
        "output": output,
    }
    serialized = _redact_pii(json.dumps(payload, ensure_ascii=False, indent=2))
    (evidence / f"exploratory-{result.trace_id}.json").write_text(serialized, encoding="utf-8")
    if not result.succeeded or not payload["meets_15_to_30_minutes"]:
        raise SystemExit("Exploration does not meet completion/duration requirement; inspect actual evidence")


if __name__ == "__main__":
    main()

