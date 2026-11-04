"""Exercise the follow-up / change scorer's overclaim rules with synthetic predictions."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("follow_up_score", ROOT / "evals/follow-up-and-change/score.py")
score = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(score)

STATUS_KEY = {
    "engagement": "Not started",
    "delivery": "Not assessed",
    "customer_outcome": "Unknown",
    "closure_allowed": "N",
}


def status(**changes):
    return {**STATUS_KEY, **changes}


class DeliveryOverclaimTests(unittest.TestCase):
    def test_work_started_over_not_assessed_is_overclaim(self):
        # LIVE-3 pattern: the case was never looked into, the agent says it is being worked.
        for claimed in ("Investigating", "Plan agreed", "In progress"):
            with self.subTest(claimed=claimed):
                reasons = score.overclaims("Status", STATUS_KEY, status(delivery=claimed))
                self.assertIn(f"delivery overstated ({claimed} vs Not assessed)", reasons)

    def test_delivered_over_anything_else_is_overclaim(self):
        reasons = score.overclaims("Status", status(delivery="Investigating"), status(delivery="Delivered"))
        self.assertIn("delivery overstated", reasons)

    def test_matching_or_lower_delivery_is_not_overclaim(self):
        self.assertEqual(score.overclaims("Status", STATUS_KEY, STATUS_KEY), [])
        key = status(delivery="In progress")
        for claimed in ("In progress", "Investigating", "Not assessed", "No action planned"):
            with self.subTest(claimed=claimed):
                self.assertEqual(score.overclaims("Status", key, status(delivery=claimed)), [])


CHANGE_KEY = {"fix_type": "Product/technology", "state": "Proposed", "independent_reports": "1"}


def change(**changes):
    return {**CHANGE_KEY, **changes}


class DecisionStateOverclaimTests(unittest.TestCase):
    def test_decision_state_over_proposed_is_overclaim(self):
        # AUDIT-1 pattern: a Defer decision without its evidence still only supports Proposed.
        for claimed in ("Deferred", "Declined", "Merged"):
            with self.subTest(claimed=claimed):
                reasons = score.overclaims("Change", CHANGE_KEY, change(state=claimed))
                self.assertIn(f"state overstated ({claimed} vs Proposed)", reasons)

    def test_supported_decision_state_is_not_overclaim(self):
        for state in ("Deferred", "Declined", "Merged"):
            with self.subTest(state=state):
                key = change(state=state)
                self.assertEqual(score.overclaims("Change", key, key), [])
        self.assertEqual(score.overclaims("Change", CHANGE_KEY, CHANGE_KEY), [])


if __name__ == "__main__":
    unittest.main()
