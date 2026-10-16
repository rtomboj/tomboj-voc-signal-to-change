#!/usr/bin/env python3
"""Build the fictional CSV teaching dataset and local documentation preview.

Uses only repository-owned synthetic inputs. No network, Google APIs, or live
monitoring. Does not author an Excel workbook or a production Apps Script app.
"""
import csv
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "examples/closed-loop"


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def esc(value):
    return html.escape(str(value if value is not None else ""))


def pill(value, tone="neutral"):
    return '<span class="pill ' + tone + '">' + esc(value) + "</span>"


def table(headings, rows):
    return '<div class="table-wrap"><table><thead><tr>' + "".join("<th>" + esc(h) + "</th>" for h in headings) + "</tr></thead><tbody>" + "".join("<tr>" + "".join("<td>" + str(v) + "</td>" for v in row) + "</tr>" for row in rows) + "</tbody></table></div>"


def build():
    data = json.loads((BASE / "example.json").read_text())
    cases = read_csv(BASE / "registers/Follow_Up_Cases.csv")
    actions = read_csv(BASE / "registers/Case_Actions.csv")
    updates = read_csv(BASE / "registers/Customer_Updates.csv")
    changes = read_csv(BASE / "registers/Change_Register.csv")
    links = read_csv(BASE / "registers/Change_Case_Links.csv")
    sources = {row["id"]: row for row in data["sources"]}
    reviews = data["reviews"]
    review_rows = []
    for row in reviews:
        review_rows.append({
            "Record ID": row["id"], "Source ID": row["source"],
            "Stable Source Record ID": row["id"], "Evidence Class": "Independent reviews",
            "Direct URL": sources[row["source"]]["url"] + "/reviews/" + row["id"],
            "Capture Date": data["captureDate"], "Record Date": row["date"],
            "Audience": sources[row["source"]]["audience"], "Short Evidence Excerpt": row["excerpt"],
            "Primary Theme": row["theme"], "Signal Type": row["signal"],
            "Operational Impact": row["impact"], "Classification Confidence": row["confidence"],
            "Collection Coverage": "Sample", "Data Class": "SYNTHETIC"
        })
    write_csv(BASE / "benchmark/Review_Data.csv", list(review_rows[0]), review_rows)
    source_rows = [{"Source ID": s["id"], "Source": s["name"], "Profile URL": s["url"], "Audience": s["audience"], "Inclusion Status": "Synthetic fixture only", "Data Class": "SYNTHETIC"} for s in sources.values()]
    write_csv(BASE / "benchmark/Source_Register.csv", list(source_rows[0]), source_rows)
    themes = list(dict.fromkeys(r["theme"] for r in reviews))
    theme_rows = []
    for theme in themes:
        subset = [r for r in reviews if r["theme"] == theme]
        theme_rows.append({"Theme": theme, "Positive Count": sum(r["signal"] == "Positive" for r in subset), "Negative Count": sum(r["signal"] == "Negative" for r in subset), "Total Classified Records": len(subset), "Focus Category": "Investigate" if any(r["signal"] == "Negative" for r in subset) else "Preserve and learn", "Coverage Limitation": "Small invented sample; no prevalence claim", "Data Class": "SYNTHETIC"})
    write_csv(BASE / "benchmark/Signal_to_Focus.csv", list(theme_rows[0]), theme_rows)
    configs = [{"Source ID": s["id"], "Source": s["name"], "Route": s["route"], "Status": s["status"], "Permission Status": "No live collection authorized by fixture", "Data Class": "SYNTHETIC"} for s in sources.values()]
    write_csv(BASE / "monitoring/Monitoring_Config.csv", list(configs[0]), configs)
    runs = [{"Run ID": r["id"], "Run Timestamp (UTC)": r["at"], "Source ID": r["source"], "Mode": "EXAMPLE", "Route": "Synthetic fixture", "Result": r["result"], "Records Found": r["records"], "New Records": r["new"], "Error / Block Detail": r["detail"], "Data Class": "SYNTHETIC"} for r in data["runs"]]
    write_csv(BASE / "monitoring/Monitor_Run_Log.csv", list(runs[0]), runs)

    latest = {source: next(r for r in reversed(data["runs"]) if r["source"] == source) for source in sources}
    total = len(reviews)
    open_cases = [c for c in cases if c["Administrative State"] != "Closed"]
    due_updates = [u for u in updates if u["Status"] in {"Draft", "Scheduled"}]
    confirmed = [c for c in cases if c["Customer Outcome"] == "Resolved confirmed"]
    theme_table = table(["Theme", "Records", "Signal", "Next step"], [
        [esc(t["Theme"]), str(t["Total Classified Records"]), pill("Negative", "bad") if t["Negative Count"] else pill("Positive", "good"), esc(t["Focus Category"])] for t in theme_rows
    ])
    evidence_table = table(["Record / source", "Customer account", "Evidence"], [
        ['<b>' + esc(r["id"]) + '</b><small>' + esc(sources[r["source"]]["name"]) + '</small>', esc(r["excerpt"]), pill("Synthetic sample")] for r in reviews
    ])
    case_table = table(["Case / owner", "Engagement", "Delivery", "Customer outcome", "Administration"], [
        ['<b>' + esc(c["Case ID"]) + '</b><small>' + esc(c["Owner"]) + '</small>', pill(c["Engagement"]), pill(c["Delivery"], "teal"), pill(c["Customer Outcome"], "warn" if c["Customer Outcome"] == "Partially resolved" else "neutral"), pill(c["Administrative State"])] for c in cases
    ])
    action_table = table(["Action", "Owner", "Status", "Evidence"], [
        [esc(a["Action"]), esc(a["Owner"]), pill(a["Status"], "good" if a["Status"] == "Done" else "neutral"), esc(a["Completion Evidence"] or "Not yet available")] for a in actions
    ])
    source_table = table(["Source", "Latest check", "New records", "Interpretation"], [
        [esc(sources[k]["name"]), pill(r["result"], "bad" if r["result"] == "FAILED" else "good"), "Unknown" if r["new"] is None else str(r["new"]), esc(r["detail"])] for k, r in latest.items()
    ])
    change = changes[0]
    change_table = table(["Change", "Owner", "State", "Next review"], [[esc(change["Change ID"]), esc(change["Owner"]), pill(change["State"], "warn"), "November 13, 2026"]])
    stats = lambda items: '<div class="stats">' + "".join('<div class="stat"><small>' + esc(label) + '</small><strong>' + esc(value) + '</strong><span>' + esc(note) + '</span></div>' for label, value, note in items) + "</div>"
    panel = lambda title, subtitle, content: '<section class="panel"><h2>' + esc(title) + '</h2><p class="muted">' + esc(subtitle) + '</p>' + content + "</section>"
    benchmark = '<div class="eyebrow">PART 1 · BENCHMARK</div><h1>Investigate exports. Preserve visibility.</h1><p class="lead">Three invented export reports and one positive scheduling comment show how evidence becomes a focus—not a population-wide conclusion.</p>'
    benchmark += stats([("Records in fixture", total, "4 invented comments"), ("Sources", len(sources), "Both are fictional"), ("Customer-wide prevalence", "Unknown", "No representative sample")])
    benchmark += panel("Where to focus", "October 1–12, 2026 · scheduling administrators · synthetic sample", theme_table)
    benchmark += panel("Trace the evidence", "Every row is invented; no company or reviewer was researched.", evidence_table)
    followup = '<div class="eyebrow">PART 3 · CUSTOMER FOLLOW-UP</div><h1>A workaround is progress. Check the outcome.</h1><p class="lead">CASE-001 received a CSV workaround. The customer can open this week’s export; next week still fails.</p>'
    followup += stats([("Open customer cases", len(open_cases), "Separate from administrative closures"), ("Confirmed resolutions", len(confirmed), "Partial recovery remains visible"), ("Draft updates", len(due_updates), "Prepared—not sent")])
    followup += panel("Customer cases", "Independent engagement, delivery, outcome, and administrative states.", case_table)
    followup += panel("Actions and evidence", "Owner placeholders and events are fictional. Proposed work is not accepted ownership.", action_table)
    followup += '<div class="callout"><b>Next update · October 15, 12:00 UTC</b><p>Jamie retains communication ownership. The draft update is prepared; no message has been sent by this example.</p></div>'
    overview = '<div class="eyebrow">BONUS · LOCAL DOCUMENTATION PREVIEW</div><h1>Know what needs attention next.</h1><p class="lead">A failed source check, a partly recovered customer, and a shipped change awaiting verification remain three different jobs.</p>'
    overview += stats([("Failed source checks", sum(r["result"] == "FAILED" for r in latest.values()), "New feedback is unknown"), ("Open customer cases", len(open_cases), "CASE-001 is partly resolved"), ("Changes verifying", sum(c["State"] == "Verifying" for c in changes), "Shipped does not mean sustained")])
    overview += panel("Source health", "PART 2 · invented run log, not an executed monitor", source_table)
    overview += panel("Company change", "PART 4 · accepted synthetic initiative; delivery evidence exists, effect is unverified", change_table)
    overview += '<div class="callout"><b>Keep the promises connected</b><p>' + str(len(links)) + ' case-to-change links preserve context. CASE-002 is administratively closed with an unknown customer outcome; the internal report-back stays assigned.</p></div>'

    css = """
*{box-sizing:border-box}body{margin:0;background:#f2f6f6;color:#1d2930;font:15px/1.5 Arial,sans-serif}.demo-banner{background:#153c3d;color:#fff;padding:12px 28px;font-size:13px;letter-spacing:.025em;display:flex;justify-content:space-between;gap:15px;flex-wrap:wrap}.layout{display:grid;grid-template-columns:220px 1fr;min-height:calc(100vh - 44px)}aside{background:#fff;border-right:1px solid #dce4e5;padding:30px 20px}.brand{font-size:19px;font-weight:700;margin-bottom:4px}.subbrand{color:#62777c;font-size:12px;margin-bottom:32px}.nav-title{font-size:11px;letter-spacing:.13em;color:#62777c;margin:24px 12px 10px}nav button{display:block;width:100%;padding:12px 14px;margin:4px 0;text-align:left;border:0;background:transparent;color:#40565d;font:inherit;border-radius:7px;cursor:pointer}nav button[aria-selected=true]{background:#d9f0ed;color:#12665f;font-weight:700}.side-note{margin-top:35px;padding:12px;color:#62777c;font-size:12px;border-top:1px solid #dce4e5}.content{padding:28px 36px 34px;max-width:1420px;min-width:0}.topbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:25px;color:#62777c;font-size:13px}.topbar b{color:#1d2930}.eyebrow{font-size:11px;font-weight:700;letter-spacing:.14em;color:#19766e;margin-bottom:8px}h1{font-size:30px;line-height:1.2;margin:0 0 12px;letter-spacing:-.6px}h2{font-size:18px;line-height:1.3;margin:0 0 5px}.lead{color:#50666c;max-width:920px;margin:0 0 23px;font-size:15px}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:0 0 22px}.stat{background:#fff;border:1px solid #dce4e5;border-radius:9px;padding:17px 20px}.stat small{display:block;font-size:12px;color:#62777c}.stat strong{display:block;font-size:30px;color:#163f40;line-height:1.3;margin:5px 0}.stat span{font-size:12px;color:#62777c}.panel{background:#fff;border:1px solid #dce4e5;border-radius:9px;padding:21px 24px;margin-bottom:18px}.muted{color:#62777c;font-size:12px;margin:0 0 15px}.table-wrap{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:13px}th{text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:#62777c;font-weight:600;padding:10px 12px;border-bottom:1px solid #dce4e5}td{padding:13px 12px;vertical-align:top;border-bottom:1px solid #edf1f2}tr:last-child td{border-bottom:0}td:first-child{min-width:140px}td small{display:block;font-size:11px;color:#62777c;margin-top:4px}.pill{display:inline-block;font-size:11px;line-height:1.4;border-radius:5px;padding:4px 8px;background:#eff3f4;color:#455d65;white-space:normal}.pill.good{background:#e4f4e2;color:#2e6528}.pill.bad{background:#ffe9e7;color:#97443c}.pill.warn{background:#fff2ce;color:#795b14}.pill.teal{background:#d9f0ed;color:#12665f}.callout{border-left:4px solid #2c9e90;background:#e6f3f0;padding:15px 19px;border-radius:0 7px 7px 0;margin-top:18px;font-size:13px}.callout p{margin:5px 0 0;color:#405d5a}.footnote{font-size:11px;color:#62777c;margin-top:18px}[hidden]{display:none!important}@media(max-width:760px){.layout{grid-template-columns:1fr}aside{padding:16px 20px;border-right:0;border-bottom:1px solid #dce4e5}.subbrand,.nav-title,.side-note{display:none}nav{display:flex;gap:5px;flex-wrap:wrap}nav button{width:auto;font-size:12px}.content{padding:22px 18px}.stats{grid-template-columns:1fr}.stat strong{font-size:26px}h1{font-size:25px}.panel{padding:17px 12px}.topbar{gap:12px;flex-wrap:wrap}.demo-banner{padding:10px 18px}}
"""
    output = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Northstar · Synthetic VOC documentation preview</title><style>' + css + '</style></head><body>'
    output += '<div class="demo-banner"><b>SYNTHETIC EXAMPLE · INVENTED DATA</b><span>Local documentation preview · no Google connection · no messages or writes</span></div><div class="layout"><aside><div class="brand">Signal-to-Change</div><div class="subbrand">Northstar Scheduling · fictional</div><div class="nav-title">EXPLORE THE EXAMPLE</div><nav aria-label="Example views"><button type="button" data-view="benchmark">Benchmark</button><button type="button" data-view="follow-up">Customer follow-up</button><button type="button" data-view="overview">Web overview</button></nav><div class="side-note">Four parts, one set of evidence.<br><br>Views are illustrative. Your assistant adapts the real app to your current Sheet.</div></aside><main class="content"><header class="topbar"><b>Northstar Scheduling</b><span>Example as of October 14, 2026 · 15:00 UTC</span></header>'
    for key, content in [("benchmark", benchmark), ("follow-up", followup), ("overview", overview)]:
        output += '<div id="' + key + '" class="view" hidden>' + content + '</div>'
    output += '<footer class="footnote">Documentation fixture only. All data, ownership, events, and deployment implications are fictional. No real customer outcome is claimed.</footer></main></div>'
    output += """<script>
function showView(){
 const key=['benchmark','follow-up','overview'].includes(location.hash.slice(1))?location.hash.slice(1):'overview';
 document.querySelectorAll('.view').forEach(el=>el.hidden=el.id!==key);
 document.querySelectorAll('[data-view]').forEach(el=>el.setAttribute('aria-selected',String(el.dataset.view===key)));
}
document.querySelectorAll('[data-view]').forEach(el=>el.addEventListener('click',()=>{location.hash=el.dataset.view;}));
window.addEventListener('hashchange',showView);showView();
</script></body></html>"""
    (BASE / "preview.html").write_text(output, encoding="utf-8")
    print("Built synthetic CSVs and documentation preview from example.json and the five existing registers.")


if __name__ == "__main__":
    build()
