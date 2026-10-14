#!/usr/bin/env python3
"""Read-only validation of the Step 3/4 CSV registers. Python standard library only.

Checks structure and selected evidence gates, not the truth of evidence, SLA calendar
arithmetic, authorization, customer satisfaction, or live delivery. See docs/validation.md.
"""

import argparse
import csv
from datetime import datetime
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TABLES = {
    "Follow_Up_Cases": "voc-customer-follow-up",
    "Case_Actions": "voc-customer-follow-up",
    "Customer_Updates": "voc-customer-follow-up",
    "Change_Register": "voc-systemic-change",
    "Change_Case_Links": "voc-systemic-change",
}
STATES = {
    "Engagement": {"Not started", "Attempted", "Contacted", "Customer replied", "Not contactable", "No contact requested"},
    "Delivery": {"Not assessed", "Investigating", "Plan agreed", "In progress", "Delivered", "No action planned"},
    "Customer Outcome": {"Unknown", "Unresolved", "Partially resolved", "Resolved confirmed", "Disputed", "Not applicable"},
    "Administrative State": {"Open", "Waiting", "Closed", "Reopened"},
    "Root Cause Confidence": {"Unknown", "Hypothesis", "Validated"},
    "State": {"Proposed", "Investigating", "Accepted", "Planned", "Implementing", "Verifying", "Sustained", "Deferred", "Declined", "Merged", "Stopped", "Reopened"},
}


def headers(table):
    path = ROOT / "skills" / TABLES[table] / "assets" / f"{table}.csv"
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return next(csv.reader(stream))


def validate(directory, stage="all"):
    """Return (errors, warnings); never alter input files."""
    errors, warnings, data = [], [], {}
    selected = list(TABLES) if stage == "all" else list(TABLES)[:3] if stage == "follow-up" else list(TABLES)[3:]
    for table in selected:
        path = Path(directory) / f"{table}.csv"
        if not path.is_file():
            errors.append(f"{table}: missing CSV file")
            data[table] = []
            continue
        try:
            with path.open(encoding="utf-8-sig", newline="") as stream:
                reader = csv.DictReader(stream)
                actual = reader.fieldnames or []
                missing = set(headers(table)) - set(actual)
                if missing or len(actual) != len(set(actual)):
                    errors.append(f"{table}: missing headers {sorted(missing)} or duplicate headers")
                rows = []
                for number, raw in enumerate(reader, 2):
                    if None in raw or any(value is None for value in raw.values()):
                        errors.append(f"{table}:{number}: row width does not match headers")
                        continue
                    row = {key: value.strip() for key, value in raw.items()}
                    if not any(row.values()):
                        continue
                    row["_where"] = f"{table}:{number}"
                    rows.append(row)
                data[table] = rows
        except (OSError, UnicodeError, csv.Error) as exc:
            errors.append(f"{table}: cannot read CSV: {exc}")
            data[table] = []

    def fail(row, message):
        errors.append(f"{row['_where']}: {message}")

    def require(row, *fields):
        missing = [field for field in fields if not row.get(field)]
        if missing:
            fail(row, "required: " + ", ".join(missing))

    def choice(row, field, options):
        if row.get(field) not in options:
            fail(row, f"invalid {field}: {row.get(field)!r}")

    def index(table, field):
        result = {}
        for row in data.get(table, []):
            require(row, field)
            key = row.get(field)
            if key and key in result:
                fail(row, f"duplicate {field}: {key}")
            elif key:
                result[key] = row
        return result

    cases = index("Follow_Up_Cases", "Case ID")
    changes = index("Change_Register", "Change ID")
    index("Case_Actions", "Action ID")
    index("Customer_Updates", "Update ID")
    for rows in data.values():
        for row in rows:
            for field, value in row.items():
                if value and field.endswith(" At"):
                    try:
                        date = datetime.fromisoformat(value.replace("Z", "+00:00"))
                        if date.utcoffset() is None:
                            raise ValueError("timezone required")
                    except ValueError:
                        fail(row, f"{field} must be an ISO 8601 timestamp with timezone")

    for row in cases.values():
        require(row, "Source Record References", "Evidence Reference", "Evidence Class", "Audience", "Received At", "Trigger", "Severity", "Contact Route", "Owner", "Backup Owner", "Acceptance Due At")
        for field in ("Engagement", "Delivery", "Customer Outcome", "Administrative State", "Root Cause Confidence"):
            choice(row, field, STATES[field])
        if row.get("Engagement") in {"Contacted", "Customer replied"}:
            require(row, "First Contact At", "Contact Reference")
        if row.get("First Contact At") and row.get("Engagement") in {"Not started", "Attempted"}:
            fail(row, "first contact conflicts with engagement state")
        if row.get("Engagement") not in {"Not contactable", "No contact requested"}:
            require(row, "First Contact Due At")
        if row.get("Accepted At"):
            require(row, "Assigned At")
        if row.get("Customer Outcome") == "Resolved confirmed":
            require(row, "Outcome Evidence")
        if row.get("Delivery") == "Plan agreed":
            require(row, "Plan Agreement Evidence")
        if row.get("Delivery") == "Delivered":
            done = [action for action in data.get("Case_Actions", [])
                    if action.get("Case ID") == row.get("Case ID") and action.get("Status") == "Done"]
            if not done:
                fail(row, "Delivered needs at least one Done action with completion evidence")
        if row.get("Administrative State") == "Closed":
            require(row, "Closure Reason", "Closed At", "Learning")

    for row in data.get("Case_Actions", []):
        require(row, "Case ID", "Owner", "Action", "Intended Outcome", "Due At")
        choice(row, "Status", {"Proposed", "Approved", "In progress", "Done", "Cancelled"})
        case = cases.get(row.get("Case ID"))
        if not case:
            fail(row, "unknown Case ID")
        if row.get("Status") in {"Approved", "In progress", "Done"}:
            require(row, "Approval Basis")
        if row.get("Status") == "Done":
            require(row, "Completed At", "Completion Evidence")
        if row.get("Status") == "Cancelled":
            require(row, "Disposition Reason")
        if case and case.get("Administrative State") == "Closed" and row.get("Status") not in {"Done", "Cancelled"}:
            require(row, "Transfer Reference", "Transfer Accepted At")

    for row in data.get("Customer_Updates", []):
        require(row, "Case ID", "Owner", "Audience", "Channel", "Due At")
        choice(row, "Status", {"Draft", "Scheduled", "Sent", "Attempted", "Failed", "Not possible", "Cancelled"})
        if row.get("Case ID") not in cases:
            fail(row, "unknown Case ID")
        if row.get("Change ID") and stage == "all" and row["Change ID"] not in changes:
            fail(row, "unknown Change ID")
        if row.get("Status") in {"Sent", "Attempted", "Failed"}:
            require(row, "Occurred At", "Delivery Evidence")
        if row.get("Status") == "Sent":
            require(row, "Content Reference")
        if row.get("Status") in {"Draft", "Scheduled"} and row.get("Occurred At"):
            fail(row, "draft/scheduled update cannot have an actual occurrence time")
        if row.get("Status") in {"Not possible", "Cancelled"}:
            require(row, "Disposition Reason")

    delivery_states = {"Planned", "Implementing", "Verifying", "Sustained"}
    for row in changes.values():
        require(row, "Title", "Fix Type", "Evidence Reference", "Brief Reference", "Owner", "Report Back Owner")
        choice(row, "State", STATES["State"])
        choice(row, "Root Cause Confidence", STATES["Root Cause Confidence"])
        state = row.get("State")
        if state != "Proposed":
            require(row, "Decision", "Decision Maker", "Decision At", "Decision Rationale")
            choice(row, "Decision", {"Accept", "Investigate", "Defer", "Decline", "Merge", "Stop", "Reopen"})
        expected = {"Investigating": "Investigate", "Deferred": "Defer", "Declined": "Decline", "Merged": "Merge", "Stopped": "Stop", "Reopened": "Reopen"}
        if state in expected and row.get("Decision") != expected[state]:
            fail(row, f"{state} needs a {expected[state]} decision")
        if state in delivery_states | {"Accepted"}:
            require(row, "Accepted At")
            if row.get("Decision") != "Accept":
                fail(row, "accepted/delivery state needs an Accept decision")
        if state in {"Investigating", "Accepted", "Planned", "Implementing", "Reopened"}:
            require(row, "Next Milestone", "Milestone Due At", "Next Update Due At")
        if state in delivery_states:
            require(row, "Measurement Plan Reference")
        if state in {"Verifying", "Sustained"}:
            require(row, "Delivery Evidence")
        if state == "Verifying":
            require(row, "Review Due At", "Next Update Due At")
        if state == "Sustained":
            require(row, "Result Evidence", "Reviewer", "Reviewed At", "Report Back Disposition")
        if state == "Deferred" and not (row.get("Review Due At") or row.get("Revisit Condition")):
            fail(row, "deferred work needs a review date or revisit condition")
        if state in {"Deferred", "Declined", "Merged", "Stopped"}:
            require(row, "Report Back Disposition")
        if state == "Merged":
            require(row, "Merged Into")
            target = row.get("Merged Into")
            if target not in changes or target == row.get("Change ID"):
                fail(row, "merge target must be a different existing change")
            seen = {row.get("Change ID")}
            while target in changes:
                if target in seen:
                    fail(row, "merge cycle")
                    break
                seen.add(target)
                target = changes[target].get("Merged Into")
        elif row.get("Merged Into"):
            fail(row, "Merged Into is only valid in Merged state")

    pairs = set()
    for row in data.get("Change_Case_Links", []):
        require(row, "Change ID", "Case ID", "Customer Communication Owner", "Receiving Change Owner")
        pair = (row.get("Change ID"), row.get("Case ID"))
        if pair in pairs:
            fail(row, "duplicate change/case link")
        pairs.add(pair)
        if pair[0] not in changes:
            fail(row, "unknown Change ID")
        if stage == "all" and pair[1] not in cases:
            fail(row, "unknown Case ID")
        choice(row, "Obligation Status", {"Proposed", "Active", "Fulfilled", "Ended"})
        if row.get("Obligation Status") == "Active":
            require(row, "Accepted At", "Acceptance Evidence", "Next Update Due At")
        if row.get("Obligation Status") in {"Fulfilled", "Ended"}:
            require(row, "Disposition Evidence")
    if stage != "all":
        warnings.append("Cross-stage references were not checked. Use --stage all with all five tables for local cross-stage checks.")
    warnings.append("Evidence presence is not evidence truth. Manually verify authority, clocks, source quality, transfers, closure, and measured outcomes.")
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="Directory containing exported CSV tables")
    parser.add_argument("--stage", choices=("all", "follow-up", "change"), default="all")
    args = parser.parse_args()
    errors, warnings = validate(args.directory, args.stage)
    for error in errors:
        print("ERROR:", error)
    for warning in warnings:
        print("REVIEW:", warning)
    print(f"{'FAIL' if errors else 'PASS'}: {len(errors)} structural/evidence-gate error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
