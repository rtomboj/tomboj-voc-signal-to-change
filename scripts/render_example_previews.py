#!/usr/bin/env python3
"""Render three labeled synthetic documentation previews from the example data.

Requires PyMuPDF (fitz) only for SVG-to-JPEG rendering. Not a browser screenshot
tool and not a production app. Source SVGs remain editable in docs/images.
"""
import csv
import html
import json
from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "examples/closed-loop"
OUT = ROOT / "docs/images"
INK, TEAL, MUTED = "#1D2930", "#15766E", "#5E747A"
WIDTH, HEIGHT = 1360, 930


def rows(name):
    with (BASE / "registers" / (name + ".csv")).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


class View:
    def __init__(self, active):
        self.parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1360" height="930" viewBox="0 0 1360 930">']
        self.rect(0, 0, WIDTH, HEIGHT, "#F2F6F6")
        self.rect(0, 0, WIDTH, 42, "#153C3D")
        self.text(24, 27, "SYNTHETIC EXAMPLE · INVENTED DATA", 12, "#FFFFFF", True)
        self.text(720, 27, "Rendered documentation preview · no Google connection or deployment", 12, "#FFFFFF")
        self.rect(0, 42, 210, HEIGHT - 42, "#FFFFFF")
        self.text(23, 91, "Signal-to-Change", 18, INK, True)
        self.text(23, 115, "Northstar Scheduling", 12, MUTED)
        self.text(23, 133, "Fictional company", 12, MUTED)
        self.text(23, 189, "EXPLORE THE EXAMPLE", 10, MUTED, True)
        for i, (key, title) in enumerate([("benchmark", "Benchmark"), ("follow-up", "Customer follow-up"), ("overview", "Web overview")]):
            y = 215 + i * 53
            if active == key:
                self.rect(14, y - 24, 182, 42, "#D9F0ED", 6)
            self.text(26, y + 2, title, 14, TEAL if active == key else MUTED, active == key)
        self.text(24, 827, "Four parts. One evidence chain.", 11, MUTED)
        self.text(24, 848, "Illustrative views; adapt to", 11, MUTED)
        self.text(24, 866, "the user's actual Sheet.", 11, MUTED)
        self.text(245, 79, "Northstar Scheduling", 14, INK, True)
        self.text(971, 79, "Example as of October 14, 2026", 12, MUTED)

    def rect(self, x, y, w, h, fill, radius=0, stroke=None):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}"' + (f' stroke="{stroke}"' if stroke else "") + "/>")

    def text(self, x, y, value, size=14, color=INK, bold=False):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" fill="{color}" font-weight="{700 if bold else 400}">' + html.escape(str(value)) + "</text>")

    def wrap(self, x, y, value, chars=80, size=14, color=INK, line=22):
        for i, value in enumerate(textwrap.wrap(value, width=chars)):
            self.text(x, y + i * line, value, size, color)

    def heading(self, eyebrow, title, subtitle):
        self.text(245, 120, eyebrow, 11, TEAL, True)
        self.text(245, 163, title, 29, INK, True)
        self.wrap(245, 195, subtitle, 119, 14, MUTED)

    def stats(self, items):
        for i, (label, value, note) in enumerate(items):
            x = 245 + i * 353
            self.rect(x, 246, 335, 111, "#FFFFFF", 9, "#DCE4E5")
            self.text(x + 19, 273, label, 12, MUTED)
            self.text(x + 19, 313, value, 30, "#163F40", True)
            self.text(x + 19, 339, note, 11, MUTED)

    def panel(self, y, height, title, note):
        self.rect(245, y, 1041, height, "#FFFFFF", 9, "#DCE4E5")
        self.text(267, y + 32, title, 18, INK, True)
        self.text(267, y + 55, note, 12, MUTED)

    def pill(self, x, y, value, color="#EFF3F4", text_color=MUTED, width=None):
        w = width or max(62, len(value) * 6.3 + 18)
        self.rect(x, y - 17, w, 27, color, 4)
        self.text(x + 9, y + 1, value, 11, text_color)

    def foot(self):
        self.text(245, 904, "All records, ownership, events, and results are invented. No live customer outcome or private deployment is claimed.", 11, MUTED)

    def save(self, name):
        import fitz
        self.foot()
        source = "".join(self.parts) + "</svg>"
        (OUT / (name + ".svg")).write_text(source, encoding="utf-8")
        with fitz.open(stream=source.encode(), filetype="svg") as document:
            (OUT / (name + ".jpg")).write_bytes(document[0].get_pixmap().tobytes("jpeg"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    data = json.loads((BASE / "example.json").read_text())
    reviews, cases, updates, changes = data["reviews"], rows("Follow_Up_Cases"), rows("Customer_Updates"), rows("Change_Register")
    latest = {s["id"]: next(r for r in reversed(data["runs"]) if r["source"] == s["id"]) for s in data["sources"]}
    open_count = sum(c["Administrative State"] != "Closed" for c in cases)
    resolved = sum(c["Customer Outcome"] == "Resolved confirmed" for c in cases)
    draft_count = sum(u["Status"] == "Draft" for u in updates)
    v = View("benchmark")
    v.heading("PART 1 · BENCHMARK", "Investigate exports. Preserve visibility.", "Three invented export reports and one positive comment show how evidence becomes a focus. The small sample does not establish customer-wide prevalence.")
    v.stats([("Records in fixture", str(len(reviews)), "All comments are invented"), ("Sources", str(len(data["sources"])), "Both sources are fictional"), ("Customer-wide prevalence", "Unknown", "No representative sample")])
    v.panel(380, 194, "Where to focus", "October 1–12, 2026 · scheduling administrators · synthetic sample")
    for x, name in [(267, "THEME"), (761, "RECORDS"), (901, "SIGNAL"), (1071, "NEXT STEP")]:
        v.text(x, 471, name, 10, MUTED, True)
    for y, theme in [(507, "Large-booking export reliability"), (548, "Schedule visibility")]:
        subset = [r for r in reviews if r["theme"] == theme]
        bad = any(r["signal"] == "Negative" for r in subset)
        v.text(267, y, theme, 14)
        v.text(783, y, len(subset), 14)
        v.pill(901, y, "Negative" if bad else "Positive", "#FFE9E7" if bad else "#E4F4E2", "#97443C" if bad else "#2E6528")
        v.text(1071, y, "Investigate" if bad else "Preserve and learn", 13)
    v.panel(595, 262, "Trace the evidence", "Source references join the benchmark to cases and company changes.")
    for i, review in enumerate(reviews):
        y = 688 + 44 * i
        v.text(267, y, review["source"] + ":" + review["id"], 12, TEAL, True)
        v.text(390, y, review["excerpt"], 13)
    v.save("northstar-benchmark")

    v = View("follow-up")
    v.heading("PART 3 · CUSTOMER FOLLOW-UP", "A workaround is progress. Check the outcome.", "CASE-001 received a CSV workaround. The customer can open this week's export; next week's schedule still fails.")
    v.stats([("Open customer cases", str(open_count), "Administration and outcome differ"), ("Confirmed resolutions", str(resolved), "Partial recovery stays visible"), ("Draft updates", str(draft_count), "Prepared; no message sent")])
    v.panel(380, 236, "Customer cases", "Keep engagement, delivery, customer outcome, and administration separate.")
    for x, title in [(267, "CASE / OWNER"), (548, "ENGAGEMENT"), (761, "DELIVERY"), (929, "OUTCOME"), (1123, "ADMIN")]:
        v.text(x, 472, title, 10, MUTED, True)
    for y, case in zip([514, 577], cases):
        v.text(267, y, case["Case ID"], 13, INK, True)
        v.text(267, y + 20, case["Owner"], 11, MUTED)
        v.pill(548, y, case["Engagement"])
        v.pill(761, y, case["Delivery"], "#D9F0ED", TEAL, 141)
        v.pill(929, y, case["Customer Outcome"], "#FFF2CE" if case["Customer Outcome"] == "Partially resolved" else "#EFF3F4")
        v.pill(1123, y, case["Administrative State"])
    v.panel(637, 139, "Next action", "Owner and dates are synthetic example facts, not an approved policy for another company.")
    v.text(267, 729, "Reproduce the next-week export failure", 15, INK, True)
    v.pill(986, 729, "Proposed—not accepted")
    v.rect(245, 797, 1041, 66, "#E6F3F0", 6)
    v.text(265, 823, "Next update · October 15, 12:00 UTC", 14, TEAL, True)
    v.text(265, 846, "Jamie retains communication ownership. The update is a draft; no contact is claimed.", 13, MUTED)
    v.save("northstar-follow-up")

    v = View("overview")
    v.heading("BONUS · LOCAL DOCUMENTATION PREVIEW", "Know what needs attention next.", "Source health, customer recovery, and company improvement remain connected—without treating one as proof of another.")
    v.stats([("Failed source checks", str(sum(r["result"] == "FAILED" for r in latest.values())), "New feedback is unknown"), ("Open customer cases", str(open_count), "CASE-001 is partly resolved"), ("Changes verifying", str(sum(c["State"] == "Verifying" for c in changes)), "Shipped does not mean sustained")])
    v.panel(380, 223, "Source health", "PART 2 · invented run log, not an executed monitor")
    for x, title in [(267, "SOURCE"), (600, "LATEST CHECK"), (824, "NEW RECORDS"), (1030, "WHAT IT MEANS")]:
        v.text(x, 472, title, 10, MUTED, True)
    for y, source in zip([516, 568], data["sources"]):
        run = latest[source["id"]]
        v.text(267, y, source["name"], 14)
        v.pill(600, y, run["result"], "#FFE9E7" if run["result"] == "FAILED" else "#E4F4E2", "#97443C" if run["result"] == "FAILED" else "#2E6528")
        v.text(824, y, "Unknown" if run["new"] is None else run["new"], 14)
        v.text(1030, y, "Investigate the check" if run["result"] == "FAILED" else "No additional records", 12, MUTED)
    v.panel(624, 139, "Company change", "PART 4 · delivery evidence exists; the customer effect remains unverified")
    v.text(267, 717, changes[0]["Change ID"] + " · Reliable large-booking exports", 14, INK, True)
    v.pill(930, 717, changes[0]["State"], "#FFF2CE", "#795B14")
    v.text(1065, 717, "Review: Nov 13", 12, MUTED)
    v.rect(245, 784, 1041, 80, "#E6F3F0", 6)
    v.text(265, 813, "Keep the promises connected", 14, TEAL, True)
    v.text(265, 840, "The customer case stays open while the larger fix is verified. Report-back remains assigned.", 13, MUTED)
    v.save("northstar-overview")
    print("Rendered three synthetic SVG/JPEG documentation previews.")


if __name__ == "__main__":
    main()
