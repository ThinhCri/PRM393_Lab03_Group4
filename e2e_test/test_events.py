import os
import pytest
from cases import CASES

CASES = [case for case in CASES if case[0] in ['TC03', 'TC04', 'TC05', 'TC06']]
@pytest.mark.parametrize("case_id,goal,screen,text,needs_event", CASES, ids=[c[0] for c in CASES])
def test_flow(run_case, case_id, goal, screen, text, needs_event):
    _, output = run_case(case_id, goal, screen, text, needs_event)
    if needs_event:
        event = os.environ["ARTEMIS_EVENT_TITLE"]
        observed = output.get("observed_texts", [])
        assert any(event in item for item in observed if isinstance(item, str)), (
            f"Observed texts did not verify target event {event!r}"
        )
