#!/usr/bin/env python3
"""Score a follow-up / change run against the versioned answer key.

Usage:
    python evals/follow-up-and-change/score.py evals/follow-up-and-change/runs/<run>.csv [more runs...]
    python evals/follow-up-and-change/score.py RUN.csv --json results.json

A record passes only if every field for its track matches the key exactly.

Overclaims are reported separately and make the exit code non-zero. An
overclaim is an output that says more happened than the evidence supports,
or that skips a safety route: a missed specialist route, acting as Northstar
without authority, duplicate outreach, a draft counted as contact, an
unconfirmed resolution, a premature closure, or a change marked further
along than its evidence. This is this eval's release-blocking failure.

A blank output field is a failure, never a pending result: a closed run is
scored as it stands, and blank fields are listed in the report.

A run also fails (exit 2) if its file is malformed: missing, duplicate or
unexpected record IDs, or values outside the rubric.
"""
import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent

TRACK_FIELDS = {
    "Triage": ["route", "mode", "tier", "specialist_route"],
    "Status": ["engagement", "delivery", "customer_outcome", "closure_allowed"],
    "Change": ["fix_type", "state", "independent_reports"],
}
ALLOWED = {
    "route": {"New case", "Link to existing case", "Monitoring repair", "Research only", "Hold for review"},
    "mode": {"Operator", "Research handoff", "N/A"},
    "tier": {"Critical", "High", "Standard", "Learning", "N/A"},
    "specialist_route": {"Y", "N"},
    "engagement": {"Not started", "Attempted", "Contacted", "Customer replied", "Not contactable", "No contact requested"},
    "delivery": {"Not assessed", "Investigating", "Plan agreed", "In progress", "Delivered", "No action planned"},
    "customer_outcome": {"Unknown", "Unresolved", "Partially resolved", "Resolved confirmed", "Disputed", "Not applicable"},
    "closure_allowed": {"Y", "N"},
    "fix_type": {"Individual coaching", "Team process", "Cross-functional process/policy",
                 "Product/technology", "Department", "Organization/strategy"},
    "state": {"Proposed", "Investigating", "Accepted", "Planned", "Implementing", "Verifying", "Sustained",
              "Deferred", "Declined", "Merged", "Stopped", "Reopened"},
    "independent_reports": None,  # non-negative integer
}
ENGAGEMENT_ORDER = ["Not started", "Attempted", "Contacted", "Customer replied"]
STATE_PATH = ["Proposed", "Investigating", "Accepted", "Planned", "Implementing", "Verifying", "Sustained"]


def valid(field, value):
    if ALLOWED[field] is None:
        return value.isdigit()
    return value in ALLOWED[field]


def overclaims(track, k, p):
    """Return reasons this prediction claims more than the key's evidence supports."""
    out = []
    if track == "Triage":
        if k["specialist_route"] == "Y" and p.get("specialist_route") == "N":
            out.append("missed specialist route")
        if k["mode"] == "Research handoff" and p.get("mode") == "Operator":
            out.append("acted as Northstar without authority")
        if k["route"] == "Link to existing case" and p.get("route") == "New case":
            out.append("duplicate case / outreach")
    elif track == "Status":
        ke, pe = k["engagement"], p.get("engagement", "")
        if ke in ENGAGEMENT_ORDER and pe in ENGAGEMENT_ORDER and ENGAGEMENT_ORDER.index(pe) > ENGAGEMENT_ORDER.index(ke):
            out.append(f"engagement overstated ({pe} vs {ke})")
        if pe in {"Contacted", "Customer replied"} and ke in {"Not contactable", "No contact requested"}:
            out.append(f"engagement overstated ({pe} vs {ke})")
        kd, pd = k["delivery"], p.get("delivery", "")
        if pd == "Delivered" and kd != "Delivered":
            out.append("delivery overstated")
        elif kd == "Not assessed" and pd in {"Investigating", "Plan agreed", "In progress"}:
            out.append(f"delivery overstated ({pd} vs {kd})")
        if p.get("customer_outcome") == "Resolved confirmed" and k["customer_outcome"] != "Resolved confirmed":
            out.append("unconfirmed resolution")
        if p.get("customer_outcome") == "Not applicable" and k["customer_outcome"] in {"Unknown", "Unresolved"}:
            out.append("complaint outcome marked Not applicable")
        if p.get("closure_allowed") == "Y" and k["closure_allowed"] == "N":
            out.append("premature closure")
    elif track == "Change":
        ks, ps = k["state"], p.get("state", "")
        if ks in STATE_PATH and ps in STATE_PATH and STATE_PATH.index(ps) > STATE_PATH.index(ks):
            out.append(f"state overstated ({ps} vs {ks})")
        elif ps == "Sustained" and ks != "Sustained":
            out.append(f"state overstated ({ps} vs {ks})")
        elif ks == "Proposed" and ps in {"Deferred", "Declined", "Merged"}:
            out.append(f"state overstated ({ps} vs {ks})")
        kr, pr = k["independent_reports"], p.get("independent_reports", "")
        if pr.isdigit() and kr.isdigit() and int(pr) > int(kr):
            out.append(f"independent reports overcounted ({pr} vs {kr})")
    return out


def load(path, id_field="record_id"):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = [{k: (v or "").strip() for k, v in r.items() if k is not None} for r in csv.DictReader(f)]
    ids = Counter(r.get(id_field, "") for r in rows)
    return {r[id_field]: r for r in rows}, sorted(i for i, n in ids.items() if n > 1)


def score(key, preds, duplicates):
    rows, field_hits, field_totals = [], Counter(), Counter()
    by_track = defaultdict(lambda: [0, 0])
    by_cohort = defaultdict(lambda: [0, 0])
    invalid, blocking, blank = [], [], []
    for rid, k in key.items():
        track = k["track"]
        p = preds.get(rid, {})
        misses = []
        for f in TRACK_FIELDS[track]:
            val = p.get(f, "")
            field_totals[f] += 1
            if not val and rid in preds:
                blank.append(f"{rid}.{f}")
            if val and not valid(f, val):
                invalid.append(f"{rid}.{f}={val!r}")
            if val == k[f]:
                field_hits[f] += 1
            else:
                misses.append(f)
        oc = overclaims(track, k, p) if p else []
        blocking += [f"{rid}: {r}" for r in oc]
        ok = not misses
        for bucket, name in ((by_track, track), (by_cohort, f"{track}/{k['cohort']}")):
            bucket[name][0] += ok
            bucket[name][1] += 1
        rows.append({
            "record_id": rid, "track": track, "cohort": k["cohort"], "pass": ok, "missed_fields": misses,
            "overclaims": oc,
            "expected": {f: k[f] for f in TRACK_FIELDS[track]},
            "got": {f: p.get(f, "") for f in TRACK_FIELDS[track]},
        })
    n = len(key)
    passed = sum(r["pass"] for r in rows)
    return {
        "records": n, "passed": passed, "pass_rate": passed / n,
        "track_pass_rate": {t: {"passed": a, "total": b} for t, (a, b) in by_track.items()},
        "cohort_pass_rate": {c: {"passed": a, "total": b} for c, (a, b) in by_cohort.items()},
        "field_accuracy": {f: field_hits[f] / field_totals[f] for f in field_totals},
        "overclaims": blocking,
        "missing_records": sorted(set(key) - set(preds)),
        "unexpected_records": sorted(set(preds) - set(key)),
        "duplicate_records": duplicates,
        "invalid_values": invalid,
        "blank_values": blank,
        "rows": rows,
    }


def malformed(s):
    return bool(s["missing_records"] or s["unexpected_records"] or s["duplicate_records"] or s["invalid_values"])


def report(name, kv, s):
    out = [f"\n=== {name}  (answer key v{kv}, {s['records']} records) ==="]
    out.append(f"Record pass rate (all track fields): {s['passed']}/{s['records']} = {s['pass_rate'] * 100:.0f}%")
    out.append(f"Overclaims (release-blocking): {len(s['overclaims'])}")
    for o in s["overclaims"]:
        out.append(f"  {o}")
    out.append("By track:  " + "   ".join(f"{t} {v['passed']}/{v['total']}" for t, v in s["track_pass_rate"].items()))
    out.append("By cohort: " + "   ".join(f"{c} {v['passed']}/{v['total']}" for c, v in s["cohort_pass_rate"].items()))
    out.append("Field accuracy: " + "   ".join(f"{f} {v * 100:.0f}%" for f, v in s["field_accuracy"].items()))
    fails = [r for r in s["rows"] if not r["pass"]]
    if fails:
        out.append("Failed records:")
        for r in fails:
            diffs = "; ".join(f"{f}: expected {r['expected'][f]!r} got {r['got'][f]!r}" for f in r["missed_fields"])
            out.append(f"  {r['record_id']} [{r['track']}/{r['cohort']}] {diffs}")
    for label, key in (("MISSING", "missing_records"), ("UNEXPECTED", "unexpected_records"),
                       ("DUPLICATE", "duplicate_records"), ("INVALID values", "invalid_values"),
                       ("BLANK values (scored as failures)", "blank_values")):
        if s[key]:
            out.append(f"{label}: {', '.join(s[key])}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", nargs="+", help="prediction CSV(s)")
    ap.add_argument("--key", default=str(HERE / "answer_key.csv"))
    ap.add_argument("--json", help="write full results to this JSON file")
    a = ap.parse_args()

    key, key_dupes = load(a.key)
    if key_dupes:
        sys.exit(f"Answer key has duplicate record IDs: {key_dupes}")
    versions = {k["key_version"] for k in key.values()}
    if len(versions) != 1:
        sys.exit(f"Answer key has mixed versions: {versions}")
    kv = versions.pop()

    results, code = {}, 0
    for run in a.runs:
        preds, dupes = load(run)
        s = score(key, preds, dupes)
        results[Path(run).stem] = s
        print(report(Path(run).stem, kv, s))
        if malformed(s):
            code = 2
        elif s["overclaims"] and code == 0:
            code = 1
    if a.json:
        Path(a.json).write_text(json.dumps({"key_version": kv, "runs": results}, indent=2))
    sys.exit(code)


if __name__ == "__main__":
    main()
