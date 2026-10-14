"""Exercise false closure, delivery, and cross-stage linkage failures with synthetic data."""
import csv
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("registers", ROOT / "scripts/validate_loop_registers.py")
registers = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(registers)


class RegisterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)
        for source in (ROOT / "examples/closed-loop/registers").glob("*.csv"):
            shutil.copyfile(source, self.path / source.name)

    def edit(self, table, **values):
        path = self.path / f"{table}.csv"
        with path.open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            fields, rows = reader.fieldnames, list(reader)
        rows[0].update(values)
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fields)
            writer.writeheader()
            writer.writerows(rows)

    def assert_invalid(self, fragment):
        errors, _ = registers.validate(self.path)
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_valid_partial_resolution_and_unreachable_closure(self):
        self.assertEqual(registers.validate(self.path)[0], [])

    def test_resolution_requires_evidence(self):
        self.edit("Follow_Up_Cases", **{"Customer Outcome": "Resolved confirmed", "Outcome Evidence": ""})
        self.assert_invalid("Outcome Evidence")

    def test_plan_agreement_cannot_be_invented(self):
        self.edit("Follow_Up_Cases", **{"Delivery": "Plan agreed"})
        self.assert_invalid("Plan Agreement Evidence")

    def test_delivery_needs_completed_action(self):
        self.edit("Case_Actions", **{"Status": "In progress"})
        self.assert_invalid("Delivered needs at least one Done action")

    def test_decision_must_match_disposition(self):
        self.edit("Change_Register", **{"State": "Declined"})
        self.assert_invalid("Declined needs a Decline decision")

    def test_closed_case_cannot_abandon_open_actions(self):
        self.edit("Follow_Up_Cases", **{"Administrative State": "Closed", "Closure Reason": "Workaround delivered", "Closed At": "2026-10-14T13:00:00Z"})
        self.assert_invalid("Transfer Accepted At")

    def test_draft_is_not_sent(self):
        self.edit("Customer_Updates", **{"Occurred At": "2026-10-14T13:00:00Z"})
        self.assert_invalid("draft/scheduled")

    def test_sent_requires_delivery_evidence(self):
        self.edit("Customer_Updates", **{"Status": "Sent"})
        self.assert_invalid("Delivery Evidence")

    def test_sustained_needs_outcome_review(self):
        self.edit("Change_Register", **{"State": "Sustained"})
        self.assert_invalid("Result Evidence")

    def test_unaccepted_handoff_cannot_be_active(self):
        self.edit("Change_Case_Links", **{"Accepted At": ""})
        self.assert_invalid("Accepted At")

    def test_active_update_survives_case_closure(self):
        self.edit("Follow_Up_Cases", **{"Administrative State": "Closed", "Closure Reason": "Accepted transfer", "Closed At": "2026-10-14T13:00:00Z"})
        # Transfer every remaining open action with recorded acceptance.
        path = self.path / "Case_Actions.csv"
        with path.open(newline="") as stream:
            reader = csv.DictReader(stream); fields, rows = reader.fieldnames, list(reader)
        rows[1].update({"Transfer Reference": "CHANGE-001 / accepted investigation", "Transfer Accepted At": "2026-10-14T12:00:00Z"})
        with path.open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fields); writer.writeheader(); writer.writerows(rows)
        self.assertEqual(registers.validate(self.path)[0], [])

    def test_orphan_case_link(self):
        self.edit("Change_Case_Links", **{"Case ID": "MISSING"})
        self.assert_invalid("unknown Case ID")

    def test_unknown_change_on_customer_update(self):
        self.edit("Customer_Updates", **{"Change ID": "MISSING"})
        self.assert_invalid("unknown Change ID")

    def test_self_merge_rejected(self):
        self.edit("Change_Register", **{"State": "Merged", "Decision": "Merge", "Merged Into": "CHANGE-001"})
        self.assert_invalid("merge target")

    def test_deferred_needs_revisit(self):
        self.edit("Change_Register", **{"State": "Deferred", "Decision": "Defer", "Review Due At": "", "Revisit Condition": ""})
        self.assert_invalid("review date or revisit condition")

    def test_ambiguous_timezone_rejected(self):
        self.edit("Follow_Up_Cases", **{"Received At": "2026-10-12T09:00:00"})
        self.assert_invalid("timestamp with timezone")

    def test_missing_file_fails_cleanly(self):
        (self.path / "Case_Actions.csv").unlink()
        self.assert_invalid("missing CSV")

    def test_partial_stage_discloses_unchecked_links(self):
        errors, warnings = registers.validate(self.path, "change")
        self.assertEqual(errors, [])
        self.assertTrue(any("Cross-stage references were not checked" in value for value in warnings))

    def test_duplicate_id_rejected(self):
        path = self.path / "Case_Actions.csv"
        lines = path.read_text().splitlines()
        path.write_text("\n".join(lines + [lines[1]]) + "\n")
        self.assert_invalid("duplicate Action ID")

    def test_malformed_csv_row_rejected(self):
        with (self.path / "Case_Actions.csv").open("a") as stream:
            stream.write("too,few,fields\n")
        self.assert_invalid("row width")


if __name__ == "__main__":
    unittest.main()
