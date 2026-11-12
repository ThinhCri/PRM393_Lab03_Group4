# ARTEMIS Setup & Execution Status

## Current Verified Status (2026-11-11 / 2026-11-12)

- **Upstream Pin:** `D:/Ky8/artemis` at commit `351ca8422f7b5b54e80a9c1ce03a222e02415b6b`.
- **Active Runtime Configuration:** Switched from Groq free-tier TPM (see historical notes below) to **Gemini Developer API** via `D:/Ky8/artemis/config/artemis.jsonc` (Flash profile: `gemini-3.1-flash-lite` / fallback `gemini-3.5-flash-lite`, `step_summarizer.enabled=false`, `object_detector=gemini-robotics-er-2-preview`; Pro profile for exploratory run). No runner logic modified.
- **Flash 3-Run Regression (PASS — Verified):**
  - Command: `powershell -ExecutionPolicy Bypass -File .\e2e_test\run_regression.ps1 -Selection "not TC13 and not TC15"`
  - Result: **38/48 passed (79.17%)** across 16 active cases × 3 independent runs (`9/16` cases passed 3/3 = 100%, all 16 cases passed ≥ 1/3 runs, `0` crashes/ANRs, `0` HTTP 429 quota failures).
  - Analytics Logcat (`TC18`): Passed `FA`/`FA-SVC` `remote_config_fetch` logcat assertion in Run 1 & Run 2.
  - Exclusions/Skips: `TC19–TC25` skipped (`7/run`) because dedicated fixture env vars were unset; `TC13` (F4A checked-in A12) and `TC15` (Remote Config live toggle) deselected to avoid mutating shared Console state / requiring physical live QR scan.
  - Summary & JUnit files: [run-command-and-summary.txt](run-command-and-summary.txt), [flash-regression-20261111/summary.csv](flash-regression-20261111/summary.csv).
- **Pro Exploratory Session (PASS — Verified):**
  - Trace `c8a40964-c1e0-4b14-9867-c1a2eacd4651`, status `completed`, Checker **PASS**, elapsed `1056.453s` (`17m 36s`), **78 steps**, **229 model calls**, **0 app bugs/crashes**.
  - Covered all 12 functional phases + ~4m Discovery dwell (`Steps 75–77`); noted `'Quét QR'` safely disabled when `checkinSessions` is closed.
  - Full report: [exploratory-pro-session.md](exploratory-pro-session.md).

---

## Historical Setup Log (2026-11-06 — 2026-11-07, Groq Free-Tier Troubleshooting)

- **2026-11-06:** Installed upstream runtime at `D:/Ky8/artemis` (`351ca8422f7b5b54e80a9c1ce03a222e02415b6b`) and pinned pytest client (`uv` + Python 3.12.14 + pytest 8.4.2). Pytest collected 25 cases (`TC01`–`TC25`).
- Initial Flash smoke (`e290ba38-f9ab-46f1-8fec-352c9373cd1f`) hit cold-boot Android `systemui` ANR and HTTP 409 lock state before app execution.
- Subsequent Groq (`qwen/qwen3.8-27b`) attempts (`fc739a62`, `4f928a29`, `70e56591`) hit Groq 8000 TPM rate limits (HTTP 429) even with `groq-compact.patch` and 62s/90s HTTP pacing. These early aborted/blocked attempts were never counted as passing runs and motivated switching the local host config to Gemini Developer API for the clean 2026-11-11 regression and Pro runs above.
