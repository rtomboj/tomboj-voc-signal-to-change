#!/usr/bin/env python3
"""Check cross-stage joins and key teaching invariants in the synthetic example."""
import csv
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "examples/closed-loop"


def read(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def main():
    errors = []
    def check(condition, message):
        if not condition:
            errors.append(message)
    data = json.loads((BASE / "example.json").read_text())
    check(data["dataClass"] == "SYNTHETIC", "Example data must be labeled SYNTHETIC")
    reviews = read(BASE / "benchmark/Review_Data.csv")
    sources = read(BASE / "benchmark/Source_Register.csv")
    themes = read(BASE / "benchmark/Signal_to_Focus.csv")
    config = read(BASE / "monitoring/Monitoring_Config.csv")
    runs = read(BASE / "monitoring/Monitor_Run_Log.csv")
    cases = read(BASE / "registers/Follow_Up_Cases.csv")
    actions = read(BASE / "registers/Case_Actions.csv")
    updates = read(BASE / "registers/Customer_Updates.csv")
    changes = read(BASE / "registers/Change_Register.csv")
    check(len(reviews) == len(data["reviews"]), "Generated review count differs from authored fixture")
    source_ids = {s["Source ID"] for s in sources}
    review_keys = {(r["Source ID"], r["Record ID"]) for r in reviews}
    check(len(review_keys) == len(reviews), "Duplicate qualified source/record IDs")
    for table in [reviews, sources, themes, config, runs]:
        check(all(r["Data Class"] == "SYNTHETIC" for r in table), "A teaching row lost its synthetic label")
    for row in sources:
        check((urlsplit(row["Profile URL"]).hostname or "").endswith(".example"), "Source profile must use a reserved .example domain")
    for row in reviews:
        check(row["Source ID"] in source_ids, "Unknown review source")
        check((urlsplit(row["Direct URL"]).hostname or "").endswith(".example"), "Review link must remain fictional")
    for row in themes:
        selected = [r for r in reviews if r["Primary Theme"] == row["Theme"]]
        check(int(row["Total Classified Records"]) == len(selected), "Theme total differs from review rows")
        check(int(row["Negative Count"]) == sum(r["Signal Type"] == "Negative" for r in selected), "Negative theme count mismatch")
        check(int(row["Positive Count"]) == sum(r["Signal Type"] == "Positive" for r in selected), "Positive theme count mismatch")
    for row in cases:
        for reference in row["Source Record References"].split(";"):
            source, record = reference.strip().split(":", 1)
            check((source, record) in review_keys, "Case references missing benchmark evidence: " + reference)
    for row in runs:
        check(row["Source ID"] in source_ids, "Run log references an unknown source")
        if row["Result"] == "FAILED":
            check(row["Records Found"] == "" and row["New Records"] == "", "Failed check must not become a zero-new-record success")
    check(any(r["Result"] == "FAILED" for r in runs), "Fixture must retain the failed-source teaching case")
    check(any(r["Result"] == "SUCCESS" and r["New Records"] == "0" for r in runs), "Fixture must distinguish successful zero-new-record checks")
    partial = [c for c in cases if c["Delivery"] == "Delivered" and c["Customer Outcome"] == "Partially resolved" and c["Administrative State"] == "Open"]
    check(bool(partial), "Fixture lost delivery versus customer-outcome distinction")
    check(any(a["Status"] == "Proposed" for a in actions), "Fixture lost the unaccepted action")
    check(any(u["Status"] == "Draft" and not u["Occurred At"] for u in updates), "Fixture lost the unsent draft")
    check(any(c["State"] == "Verifying" and not c["Result Evidence"] for c in changes), "Fixture lost delivery versus verified-effect distinction")
    preview = (BASE / "preview.html").read_text(encoding="utf-8")
    check("SYNTHETIC EXAMPLE" in preview and "no Google connection" in preview, "Preview needs explicit synthetic/no-live labels")
    check(not any(term in preview for term in ["fetch(", "XMLHttpRequest", "google.script.run"]), "Documentation preview must not call live services")
    for name in ["northstar-benchmark", "northstar-follow-up", "northstar-overview"]:
        image = ROOT / "docs/images" / (name + ".jpg")
        check(image.exists() and image.stat().st_size > 1000, "Missing rendered preview: " + name)
    for error in errors:
        print("ERROR:", error)
    print(f"{'FAIL' if errors else 'PASS'}: connected synthetic example ({len(errors)} errors)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
