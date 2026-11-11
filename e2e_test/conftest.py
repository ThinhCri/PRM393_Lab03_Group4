import asyncio
import json
import os
import re
import time
import urllib.request
import uuid
from pathlib import Path

import pytest

@pytest.fixture
def run_case():
    base = os.getenv("ARTEMIS_BASE_URL")
    account = os.getenv("ARTEMIS_TEST_ACCOUNT_EMAIL")
    if not base or not account:
        pytest.skip("Set ARTEMIS_BASE_URL and ARTEMIS_TEST_ACCOUNT_EMAIL; no device/model calls made")
    sdk = pytest.importorskip("artemis_client")
    client = sdk.ArtemisClient(base, token=os.getenv("ARTEMIS_TOKEN"))
    event = os.getenv("ARTEMIS_EVENT_TITLE")
    evidence = Path(__file__).resolve().parents[1] / "evidence" / "artemis"
    evidence.mkdir(parents=True, exist_ok=True)

    def run(case_id, goal, expected_screen, expected_text, needs_event=False):
        if needs_event and not event:
            pytest.skip("ARTEMIS_EVENT_TITLE must name an approved test event with resettable registration")
        goal = goal.replace("{account}", account).replace("{event}", event or "")
        instruction = (
            "Test ONLY EventHub (com.eventhub.app) on the assigned dedicated test device. "
            "Each case is independent: return to login through Account > Logout if necessary. "
            "Use only the explicitly named Google test account already added to Android; never use personal accounts, "
            "type passwords, change security settings, edit Firebase console, or invent observations. "
            + goal + " Complete every requested action before reporting completion. "
            "Return ONLY a JSON object with this exact structure: "
            '{"observed_values":{"final_screen":"<observed screen code>"},'
            '"observed_texts":["<verbatim visible UI text>"],"precondition_failed":null}. '
            "final_screen MUST be nested inside observed_values, never at the root. "
            "Copy Vietnamese text exactly from the latest screen; do not translate, paraphrase, "
            "invent explanatory text, or infer text from the task goal. If text cannot be read, "
            "report that limitation rather than making it up. "
            "Screen-code mapping for this case: " + expected_screen +
            ". Report that code only if the corresponding final screen is actually observed. "
            "Put the JSON in report_task_status explanation. If setup is missing, "
            "set precondition_failed to the reason; do not fake success."

        )
        started = time.monotonic()
        def save(payload):
            serialized = json.dumps(payload, ensure_ascii=False, indent=2).replace(account, "<TEST_ACCOUNT>")
            serialized = re.sub(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', '<REDACTED_EMAIL>', serialized)
            run_id = re.sub(r'[^\w-]', '_', os.getenv('ARTEMIS_RUN', '1'))
            trace_id = re.sub(r'[^\w-]', '_', str(payload.get('trace_id') or uuid.uuid4()))
            (evidence / f'{case_id}-run-{run_id}-{trace_id}.json').write_text(serialized, encoding='utf-8')
        try:
            result = asyncio.run(client.run(instruction, profile="flash", device_serial=os.getenv("ARTEMIS_DEVICE", "emulator-5554"), timeout=int(os.getenv("ARTEMIS_CASE_TIMEOUT_SECONDS", "1800"))))
        except Exception as exc:
            save({'case_id': case_id, 'status': 'client_error', 'acceptance_status': 'not_passed',
                  'elapsed_seconds': time.monotonic() - started, 'error_type': type(exc).__name__})
            pytest.fail(f'ARTEMIS request failed ({type(exc).__name__}); check the local host log', pytrace=False)
        duration = time.monotonic() - started
        output = result.output
        # Pinned host omits Flash final reports from TaskResult. Read the
        # report actually recorded in that exact session, never invent output.
        if output is None:
            for attempt in range(10):
                steps = []
                request = urllib.request.Request(f"{base.rstrip('/')}/api/sessions/{result.trace_id}/steps")
                if os.getenv('ARTEMIS_TOKEN'):
                    request.add_header('Authorization', 'Bearer ' + os.environ['ARTEMIS_TOKEN'])
                try:
                    with urllib.request.urlopen(request, timeout=15) as response:
                        steps = json.load(response)
                except Exception:
                    steps = []  # Missing evidence must fail assertions, never imply success.
                for step in reversed(steps if isinstance(steps, list) else []):
                    action = step.get("action_taken") or {}
                    if isinstance(action, str):
                        try:
                            action = json.loads(action)
                        except json.JSONDecodeError:
                            continue
                    if action.get("action") == "report_task_status":
                        output = (action.get("args") or {}).get("explanation")
                        break
                if output is not None:
                    break
                if attempt < 9:
                    time.sleep(0.5)
        if isinstance(output, str):
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", output.strip())
            try:
                output = json.loads(cleaned)
            except json.JSONDecodeError:
                parsed = None
                decoder = json.JSONDecoder()
                for idx, ch in enumerate(cleaned):
                    if ch == "{":
                        try:
                            candidate, _ = decoder.raw_decode(cleaned, idx)
                        except json.JSONDecodeError:
                            continue
                        if isinstance(candidate, dict) and "observed_values" in candidate:
                            parsed = candidate
                            break
                output = parsed if parsed is not None else {"unparsed": cleaned}
        payload = {"case_id": case_id, "trace_id": result.trace_id, "status": result.status,
                   "elapsed_seconds": duration, "output": output, "error": result.error,
                   "run": os.getenv("ARTEMIS_RUN", "1")}
        # Only pytest's full test outcome (including additional assertions such as
        # TC18's Logcat check) may establish acceptance. Raw model status cannot.
        payload['acceptance_status'] = 'pending_pytest_assertions'
        save(payload)
        if isinstance(output, dict) and output.get("precondition_failed"):
            pytest.skip(f"Setup missing (trace {result.trace_id}): {output['precondition_failed']}")
        assert result.succeeded, f"Task status={result.status}; trace={result.trace_id}"
        assert isinstance(output, dict), "Agent must report structured observations, not just SUCCESS"
        assert output.get("observed_values", {}).get("final_screen") == expected_screen
        observed = output.get("observed_texts", [])
        assert isinstance(observed, list)
        assert any(expected_text in text for text in observed if isinstance(text, str)), f"Missing observed text: {expected_text}"
        return result, output
    return run
