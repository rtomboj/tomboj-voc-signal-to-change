#!/usr/bin/env python3
"""Score a classification run against the versioned answer key.

Usage:
    python3 evals/classification/score.py evals/classification/runs/<run>.csv [more runs...]
    python3 evals/classification/score.py RUN.csv --json results.json

A record passes only if all four graded fields match the key exactly.
Escalation is reported separately because a missed escalation is the
costliest error: money, privacy, or churn risk reaches no human.
"""
import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIELDS = ["primary_theme", "signal_type", "operational_impact", "escalate"]
ALLOWED = {
    "primary_theme": {
        "Large-booking export reliability", "Schedule visibility",
        "Billing and invoicing accuracy", "Onboarding and setup",
        "Support responsiveness", "Mobile app performance",
        "Data privacy and security", "Other", "Out of scope",
    },
    "signal_type": {"Positive", "Negative", "Mixed", "Request", "Question", "N/A"},
    "operational_impact": {"Blocker", "High", "Medium", "Low", "Unknown"},
    "escalate": {"Y", "N"},
}


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return {r["record_id"].strip(): {k: (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)}


def score(key, preds):
    rows, field_hits = [], Counter()
    cohort = defaultdict(lambda: [0, 0])
    failure_types = Counter()
    esc = Counter()  # tp, fn (missed), fp (over-escalated), tn
    invalid = []
    for rid, k in key.items():
        p = preds.get(rid, {})
        misses = []
        for f in FIELDS:
            val = p.get(f, "")
            if val and val not in ALLOWED[f]:
                invalid.append(f"{rid}.{f}={val!r}")
            if val == k[f]:
                field_hits[f] += 1
            else:
                misses.append(f)
                failure_types[f] += 1
        ok = not misses
        cohort[k["cohort"]][0] += ok
        cohort[k["cohort"]][1] += 1
        ke, pe = k["escalate"], p.get("escalate", "")
        esc["tp" if ke == "Y" and pe == "Y" else "fn" if ke == "Y" else "fp" if pe == "Y" else "tn"] += 1
        rows.append({
            "record_id": rid, "cohort": k["cohort"], "pass": ok,
            "missed_fields": misses,
            "expected": {f: k[f] for f in FIELDS},
            "got": {f: p.get(f, "") for f in FIELDS},
            "confidence": p.get("confidence", ""),
        })
    n = len(key)
    passed = sum(r["pass"] for r in rows)
    pos = esc["tp"] + esc["fn"]
    return {
        "records": n,
        "passed": passed,
        "pass_rate": passed / n,
        "field_accuracy": {f: field_hits[f] / n for f in FIELDS},
        "cohort_pass_rate": {c: {"passed": a, "total": t, "rate": a / t} for c, (a, t) in cohort.items()},
        "escalation": {
            "should_escalate": pos,
            "caught": esc["tp"],
            "missed": esc["fn"],
            "over_escalated": esc["fp"],
            "recall": esc["tp"] / pos if pos else None,
        },
        "failure_types": dict(failure_types.most_common()),
        "missing_records": sorted(set(key) - set(preds)),
        "invalid_values": invalid,
        "rows": rows,
    }


def pct(x):
    return "n/a" if x is None else f"{x * 100:.0f}%"


def report(name, key_version, s):
    out = [f"\n=== {name}  (answer key v{key_version}, {s['records']} records) ==="]
    out.append(f"Record pass rate (all 4 fields): {s['passed']}/{s['records']} = {pct(s['pass_rate'])}")
    e = s["escalation"]
    out.append(f"Escalation recall: caught {e['caught']}/{e['should_escalate']} = {pct(e['recall'])}"
               f"   missed: {e['missed']}   over-escalated: {e['over_escalated']}")
    out.append("Field accuracy:   " + "   ".join(f"{f} {pct(v)}" for f, v in s["field_accuracy"].items()))
    out.append("By cohort:")
    for c, v in s["cohort_pass_rate"].items():
        out.append(f"  {c:<12} {v['passed']}/{v['total']}  {pct(v['rate'])}")
    if s["failure_types"]:
        out.append("Failure types:    " + ", ".join(f"{k} x{v}" for k, v in s["failure_types"].items()))
    fails = [r for r in s["rows"] if not r["pass"]]
    if fails:
        out.append("Failed records:")
        for r in fails:
            diffs = "; ".join(f"{f}: expected {r['expected'][f]!r} got {r['got'][f]!r}" for f in r["missed_fields"])
            out.append(f"  {r['record_id']} [{r['cohort']}] {diffs}")
    if s["missing_records"]:
        out.append(f"MISSING records: {', '.join(s['missing_records'])}")
    if s["invalid_values"]:
        out.append(f"INVALID values: {', '.join(s['invalid_values'])}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("runs", nargs="+", help="prediction CSV(s)")
    ap.add_argument("--key", default=str(HERE / "answer_key.csv"))
    ap.add_argument("--json", help="write full results to this JSON file")
    a = ap.parse_args()

    key = load(a.key)
    versions = {k["key_version"] for k in key.values()}
    if len(versions) != 1:
        sys.exit(f"Answer key has mixed versions: {versions}")
    kv = versions.pop()

    results = {}
    for run in a.runs:
        s = score(key, load(run))
        results[Path(run).stem] = s
        print(report(Path(run).stem, kv, s))
    if a.json:
        Path(a.json).write_text(json.dumps({"key_version": kv, "runs": results}, indent=2))
    # Non-zero exit if any run misses an escalation: that is the release-blocking failure.
    sys.exit(1 if any(r["escalation"]["missed"] for r in results.values()) else 0)


if __name__ == "__main__":
    main()
