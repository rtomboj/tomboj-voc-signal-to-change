"""Run reference Apps Script code with synthetic in-memory Google service doubles."""
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which('node'), 'Node.js is required for Apps Script reference tests')
class AppsScriptReferenceTests(unittest.TestCase):
    def run_case(self, case):
        result = subprocess.run(
            ['node', str(ROOT / 'tests/apps_script_references.cjs'), case],
            cwd=ROOT, text=True, capture_output=True, encoding='utf-8',
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_native_date_freshness_regression(self):
        self.run_case('dates')

    def test_setup_import_and_idempotency(self):
        self.run_case('setup')

    def test_edit_endpoint_guards_and_audit(self):
        self.run_case('edits')

    def test_drawer_submit_against_real_endpoint(self):
        self.run_case('drawer')

    def test_json_transport_preserves_null_zero_and_dates(self):
        self.run_case('transport')

    def test_every_enabled_decision_saves_from_its_form(self):
        self.run_case('choices_decideChange')

    def test_owner_form_acceptance_choices_save(self):
        self.run_case('choices_setCaseOwner')

    def test_every_enabled_case_status_saves_from_its_form(self):
        self.run_case('choices_setCaseStatus')

    def test_every_action_status_saves_from_its_form(self):
        self.run_case('choices_setActionStatus')

    def test_every_update_outcome_saves_from_its_form(self):
        self.run_case('choices_logUpdate')

    def test_disabled_choices_explain_and_server_refuses(self):
        self.run_case('disabled')

    def test_prefill_and_only_changed_fields(self):
        self.run_case('prefill')

    def test_delivery_eligibility_is_server_view_data(self):
        self.run_case('facts')

    def test_new_fields_do_not_bypass_evidence_gates(self):
        self.run_case('gates')


if __name__ == '__main__':
    unittest.main()
