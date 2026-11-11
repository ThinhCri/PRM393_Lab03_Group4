import os
import pytest
from cases import CASES

CASES_BY_ID = {case[0]: case for case in CASES}
CASES = [CASES_BY_ID[cid] for cid in ('TC07', 'TC08', 'TC12', 'TC09', 'TC13')]
@pytest.mark.parametrize("case_id,goal,screen,text,needs_event", CASES, ids=[c[0] for c in CASES])
def test_flow(run_case, case_id, goal, screen, text, needs_event):
    _, output = run_case(case_id, goal, screen, text, needs_event)
    if case_id in ('TC08', 'TC09'):
        event = os.environ["ARTEMIS_EVENT_TITLE"]
        observed = output.get("observed_texts", [])
        assert any(
            line.strip() == event
            for item in observed
            if isinstance(item, str)
            for line in item.splitlines()
        ), f"Observed texts did not verify exact event {event!r}"
