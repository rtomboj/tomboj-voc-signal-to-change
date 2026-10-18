#!/usr/bin/env python3
"""Build eight static, synthetic web reference views from the unchanged Northstar fixtures."""
import csv
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'examples/closed-loop'
OUT = ROOT / 'docs/images/northstar-web-reference.html'
esc = lambda value: html.escape(str(value), quote=True)


def read(name):
    with (BASE / 'registers' / (name + '.csv')).open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def badge(value):
    color = 'good' if value in ('Positive', 'Done', 'SUCCESS', 'Sent') else 'warn' if value in ('FAILED', 'Partially resolved', 'Verifying', 'Proposed', 'Draft') else ''
    return f'<span class="badge {color}">{esc(value)}</span>'


def table(headers, rows):
    return '<div class="table-wrap"><table><thead><tr>' + ''.join(f'<th>{esc(h)}</th>' for h in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>' for row in rows) + '</tbody></table></div>'


def panel(title, note, content):
    return f'<section class="panel"><header><h2>{esc(title)}</h2><p>{esc(note)}</p></header>{content}</section>'


def stats(items):
    return '<div class="stats">' + ''.join(f'<div class="stat"><span>{esc(label)}</span><strong>{esc(value)}</strong><small>{esc(note)}</small></div>' for label, value, note in items) + '</div>'


def main():
    data = json.loads((BASE / 'example.json').read_text(encoding='utf-8'))
    cases, actions, updates, changes = [read(n) for n in ('Follow_Up_Cases', 'Case_Actions', 'Customer_Updates', 'Change_Register')]
    latest = {s['id']: next(r for r in reversed(data['runs']) if r['source'] == s['id']) for s in data['sources']}
    open_cases = sum(r['Administrative State'] != 'Closed' for r in cases)
    drafts = sum(r['Status'] == 'Draft' for r in updates)
    proposed = [r for r in actions if r['Status'] == 'Proposed']
    source_names = {s['id']: s['name'] for s in data['sources']}
    reviews = data['reviews']
    pages = {}
    quotes = '<div class="quotes">' + ''.join(f'<article class="quote"><div class="quote-mark">“</div><blockquote>{esc(r["excerpt"])}</blockquote><p>{esc(source_names[r["source"]])} · {esc(r["source"] + ":" + r["id"])}</p><footer>{badge(r["signal"])}<span class="tag">{esc(r["theme"])}</span></footer></article>' for r in reviews) + '</div>'
    pages['home'] = ('Home', 'Know what needs attention next.',
        panel('WHAT TO DO NEXT', 'Four synthetic records; a small sample, not a customer-wide trend.', '<div class="hero"><h1>Investigate export reliability.<br>Preserve schedule visibility.</h1><p>Three invented export reports and one positive visibility comment connect the benchmark to follow-up and company change.</p><a class="button primary" href="#decisions">Review proposed work →</a> <a class="text-link" href="#benchmark">See the evidence · 4 records →</a></div>') +
        '<div class="section-title"><h2>Voice of the customer</h2><p>Invented excerpts from the repository fixture. No real customer data.</p></div>' + quotes +
        stats([('Source checks needing review', sum(r['result'] == 'FAILED' for r in latest.values()), 'Synthetic failure; volume unknown'), ('Open customer cases', open_cases, 'Partial recovery stays visible'), ('Changes verifying', sum(r['State'] == 'Verifying' for r in changes), 'Delivery is not a confirmed outcome')]))
    themes = list(dict.fromkeys(r['theme'] for r in reviews))
    pages['benchmark'] = ('Benchmark', 'Trace every focus back to the evidence.',
        '<div class="notice">Coverage limitation · four invented records from two fictional sources. Prevalence is unknown.</div>' +
        stats([('Records in fixture',len(reviews),'All invented'),('Negative signals',sum(r['signal']=='Negative' for r in reviews),'Count, not a population share'),('Themes',len(themes),'Separate negative and positive learning')]) +
        panel('Themes', 'Theme counts are derived from the unchanged Northstar fixture.', table(['Theme','Records','Signal','Next step'], [[esc(t),str(sum(r['theme']==t for r in reviews)),badge('Negative' if any(r['theme']==t and r['signal']=='Negative' for r in reviews) else 'Positive'),esc('Investigate' if t==themes[0] else 'Preserve and learn')] for t in themes])) +
        panel('All records in the benchmark', 'Qualified source and record IDs preserve provenance.', table(['Record','Date','Source','Excerpt'],[[esc(r['source']+':'+r['id']),esc(r['date']),esc(source_names[r['source']]),esc(r['excerpt'])] for r in reviews])))
    pages['monitoring'] = ('Monitoring', 'A failed check is unknown feedback, not zero.',
        stats([('Sources',len(data['sources']),'Fictional sources'),('Failed checks',sum(r['result']=='FAILED' for r in latest.values()),'Last state retained'),('New feedback','Unknown','One source failed')]) +
        panel('Source health', 'Illustrative fixture events, not live monitoring executions.', table(['Source','Latest result','New records','Interpretation'], [[esc(s['name']),badge(latest[s['id']]['result']),esc('Unknown' if latest[s['id']]['new'] is None else latest[s['id']]['new']),esc(latest[s['id']]['detail'])] for s in data['sources']])) +
        panel('Run log', 'Synthetic timestamps; no installed schedule is implied.', table(['Run','Source','When','Result'],[[esc(r['id']),esc(r['source']),esc(r['at']),badge(r['result'])] for r in reversed(data['runs'])])))
    pages['follow-up'] = ('Follow-up', 'Keep delivery, customer outcome and closure separate.',
        stats([('Open cases',open_cases,'One communication owner per case'),('Confirmed resolutions',sum(r['Customer Outcome']=='Resolved confirmed' for r in cases),'No inferred satisfaction'),('Draft updates',drafts,'A draft is not contact')]) +
        panel('Customer cases', 'CASE-001 has a workaround and remains partially resolved.', table(['Case / owner','Engagement','Delivery','Outcome','Administration'], [[f'<b>{esc(r["Case ID"])}</b><small>{esc(r["Owner"])}</small>',badge(r['Engagement']),badge(r['Delivery']),badge(r['Customer Outcome']),badge(r['Administrative State'])] for r in cases])) +
        panel('Actions and commitments', 'Proposed work is not accepted ownership.', table(['Action','Owner','Status','Evidence'],[[esc(r['Action']),esc(r['Owner']),badge(r['Status']),esc(r['Completion Evidence'] or 'Not recorded')] for r in actions])) +
        '<div class="notice">The reference form collects Contact Reference, Plan Agreement Evidence and Outcome Evidence. Closure requires a separate commitment/transfer review.</div>')
    change = changes[0]
    pages['changes'] = ('Changes', 'Shipped work stays Verifying until its effect is checked.',
        '<p class="empty-lanes">No changes in: Proposed · Investigating · Accepted · Planned · Implementing · Sustained</p>' +
        '<div class="board"><section class="lane"><h2>Verifying <span>1</span></h2><article class="panel"><p class="mono">'+esc(change['Change ID'])+'</p><h2>'+esc(change['Title'])+'</h2><p>'+esc(change['Owner'])+'</p>'+badge(change['State'])+'<p>Review due '+esc(change['Review Due At'][:10])+'</p><small>Delivery evidence exists; result evidence is pending.</small></article></section></div>' +
        panel('Evidence and report-back', 'One change can retain obligations to more than one case.', table(['Delivery evidence','Result evidence','Report-back'],[[esc(change['Delivery Evidence']),esc(change['Result Evidence'] or 'Not yet verified'),esc(change['Report Back Disposition'])]])))
    pages['decisions'] = ('Decisions', 'Offer only choices the reference form can satisfy.',
        stats([('Proposed actions',len(proposed),'Human decision still needed'),('Changes verifying',len(changes),'No new change approval implied'),('Unavailable choices',2,'Merge and new case closure')]) +
        ''.join(panel(r['Action ID']+' · '+r['Action'], 'Proposed action · '+r['Owner'], '<p>'+esc(r['Intended Outcome'])+'</p><div class="form-note"><b>Approval basis is required for Approved, In progress and Done.</b><p>Done also needs completion evidence. Cancelled needs a reason.</p></div><button disabled title="Static documentation preview">Open action form · illustration only</button>') for r in proposed) +
        panel('Reference decision form', 'A decision needs rationale, confirmation and an audit reason.', table(['Choice','Fields available in the form'],[['Accept','Owner + Owner has accepted'],['Investigate / Reopen','Decision rationale'],['Defer','Report Back Disposition + Review Due At or Revisit Condition'],['Decline / Stop','Report Back Disposition'],['Merge',esc('Disabled: Needs an obligation-transfer workflow (not in this reference)')]])))
    pages['report-back'] = ('Report-back', 'An update owed remains visible until it is fulfilled.',
        stats([('Drafts, not sent',drafts,'No sending from this preview'),('Not possible',sum(r['Status']=='Not possible' for r in updates),'Limitation remains recorded'),('Actual messages sent',0,'No live connection')]) +
        panel('Customer update records', 'Content and delivery evidence are separate fields.', table(['Update / case','Owner','Status','Disposition'],[[f'<b>{esc(r["Update ID"])}</b><small>{esc(r["Case ID"])}</small>',esc(r['Owner']),badge(r['Status']),esc(r['Disposition Reason'] or 'Draft retained; not sent')] for r in updates])) +
        panel('Log an update', 'Record an event that happened outside the app; never send a message.', table(['Outcome','Form evidence'],[['Sent','Content Reference + delivery evidence'],['Attempted / Failed','Attempt evidence + reason or detail'],['Not possible / Cancelled','Reason or detail']])))
    pages['data-qa'] = ('Data & QA', 'Keep fixture checks separate from live evidence.',
        stats([('Synthetic review records',len(reviews),'Unchanged Northstar data'),('Live Google checks','Not run','This is a local documentation preview'),('Operational writes',0,'No live write endpoint')]) +
        panel('Data sources', 'All public preview content comes from repository-owned synthetic records.', table(['Source','Rows','Meaning'],[['Review_Data',str(len(reviews)),'Invented review evidence'],['Follow_Up_Cases',str(len(cases)),'Customer-level records'],['Case_Actions',str(len(actions)),'Commitments and investigations'],['Customer_Updates',str(len(updates)),'Draft and disposition records'],['Change_Register',str(len(changes)),'Improvement under verification']])) +
        panel('Activity_Log', 'No activity-log fixture is supplied; no private run history is copied.', '<div class="form-note"><b>Every changed field needs an audit entry.</b><p>The endpoint tests generate separate synthetic events. A real deployment still needs Google authorization, access checks and user-run verification.</p></div>') +
        '<div class="notice">Not proven here: live deployment permissions, scheduled collection, customer contact, or measured improvement.</div>')
    nav=''.join(f'<a href="#{key}" data-page="{key}"><span>{i:02}</span>{esc(title)}</a>' for i,(key,(title,_,_)) in enumerate(pages.items(),1))
    sections=''.join(f'<article class="view" id="{key}" hidden><div class="page-heading"><div><div class="eyebrow">THE LOOP / {esc(title.upper())}</div><h1>{esc(title)}</h1><p>{esc(sub)}</p></div><span class="badge">SYNTHETIC only</span></div>{body}</article>' for key,(title,sub,body) in pages.items())
    css='''*{box-sizing:border-box}body{margin:0;background:#0b1012;color:#ecf1f3;font:15px/1.5 Arial,sans-serif}a{color:#31bec8;text-decoration:none}aside{position:fixed;inset:0 auto 0 0;width:230px;background:#11191c;border-right:1px solid #29353a;padding:24px 14px;display:flex;flex-direction:column}.brand{display:flex;gap:12px;align-items:center;margin-bottom:34px}.mark{background:#32bcc5;color:#071113;width:34px;height:34px;border-radius:9px;text-align:center;line-height:34px;font-weight:bold}.brand b{display:block;font-size:15px}.brand small{color:#a0b1ba;font-size:12px}.nav-label,.eyebrow{font-size:11px;letter-spacing:.12em;color:#9babb5}nav a{display:flex;gap:14px;color:#b8c6cd;padding:11px 12px;margin:3px 0;border-radius:7px}nav a.active{background:#1c3038;color:#fff}nav span{font:11px/24px monospace;color:#7d969f}aside footer{margin-top:auto;color:#9eb1bb;font-size:12px;border-top:1px solid #29353a;padding:16px 0}.shell{margin-left:230px}.topbar{padding:18px 28px;border-bottom:1px solid #29353a;display:flex;gap:14px;align-items:center;flex-wrap:wrap;color:#b9c6cd;font-size:12px}.company{color:#fff;border:1px solid #45515a;border-radius:6px;padding:7px 12px}.synthetic{color:#49d6df;font-weight:bold}.main{padding:25px 28px 34px;max-width:1600px}.page-heading{display:flex;justify-content:space-between;align-items:center;gap:20px;margin-bottom:23px}.page-heading h1{font-size:28px;letter-spacing:-.6px;margin:4px 0}.page-heading p{margin:0;color:#b7c7cf}.panel{background:#11191d;border:1px solid #29373d;border-radius:11px;margin-bottom:22px;padding:22px}.panel header{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;margin-bottom:18px}.panel h2,.section-title h2{font-size:17px;margin:0}.panel header p{color:#a7bbc5;margin:0;font-size:13px}.hero{max-width:840px}.hero h1{font-size:32px;line-height:1.24;margin:12px 0}.hero p{color:#b9cbd4;max-width:810px}.button,button{display:inline-block;padding:10px 16px;border:1px solid #50616c;border-radius:7px;font:inherit;color:#c3cfd5;background:#152026}.primary{background:#2ebac5;color:#031216;font-weight:bold;border-color:#2ebac5}.text-link{margin-left:16px;font-weight:bold;font-size:14px}.section-title{display:flex;gap:18px;align-items:baseline;margin:26px 0 17px;flex-wrap:wrap}.section-title p{color:#a6b9c4;margin:0;font-size:13px}.quotes{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-bottom:25px}.quote{padding:20px;border:1px solid #2a383e;border-radius:11px;background:#11191d;display:flex;flex-direction:column}.quote-mark{font:bold 42px Georgia;color:#32bbc5;height:45px}blockquote{margin:0 0 22px;font-size:19px;line-height:1.45}.quote p{font-size:12px;color:#9eb5c1}.quote footer{margin-top:auto;border-top:1px solid #2a383e;padding-top:14px}.tag{display:block;font-size:12px;color:#adc2ce;margin-top:9px;overflow-wrap:normal}.stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-bottom:22px}.stat{padding:18px 21px;background:#11191d;border:1px solid #29373d;border-radius:10px}.stat span,.stat small{display:block;color:#abc0ca;font-size:12px}.stat strong{display:block;font-size:29px;margin:7px 0}.badge{display:inline-block;white-space:nowrap;border:1px solid #52616a;border-radius:6px;padding:3px 8px;color:#b9ccd6;font-size:11px}.badge.good{border-color:#226c45;color:#74dfaa;background:#12271e}.badge.warn{border-color:#82601f;color:#f7cd67;background:#2a2211}.notice{border:1px solid #7c611f;background:#211c10;color:#e7ca82;border-radius:8px;padding:14px 18px;margin-bottom:22px;font-size:13px}.table-wrap{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:13px}th{text-align:left;color:#a7bdc9;font-size:11px;padding:9px 12px;border-bottom:1px solid #33424a}td{padding:17px 12px;vertical-align:top;border-bottom:1px solid #28363d;max-width:420px;overflow-wrap:normal}tr:last-child td{border-bottom:0}td small{display:block;color:#91aab8;margin-top:7px}small{color:#a4bac5}.empty-lanes{color:#9db3c0;font-size:13px}.board{display:flex;gap:20px}.lane{width:min(420px,100%);padding:17px;background:#10181c;border:1px solid #29373d;border-radius:10px}.lane>h2{font-size:16px;margin:0 0 18px}.lane>h2 span{float:right;color:#b7cad4}.lane .panel{margin:0}.mono{font-family:monospace;font-size:12px;color:#9fb7c5}.form-note{padding:16px;border:1px dashed #4c626e;border-radius:8px;background:#142128;margin-bottom:16px;color:#c0d2db}.form-note p{margin:8px 0 0}.bottom-note{margin-top:20px;color:#7f9aa8;font-size:11px}[hidden]{display:none!important}button:disabled{opacity:.55;cursor:not-allowed}@media(max-width:850px){aside{position:static;width:100%;padding:15px}.brand{margin:0 0 12px}nav{display:flex;flex-wrap:wrap}nav a{font-size:12px;padding:5px}nav span,.nav-label,aside footer{display:none}.shell{margin-left:0}.topbar{padding:15px}.main{padding:18px}.quotes{grid-template-columns:repeat(2,minmax(0,1fr))}.stats{grid-template-columns:1fr}.page-heading{align-items:flex-start}.hero h1{font-size:26px}.text-link{display:block;margin:12px 0}table{min-width:650px}.panel{padding:16px}}@media(max-width:480px){.quotes{grid-template-columns:1fr}.page-heading{display:block}.page-heading .badge{margin-top:12px}}'''
    script="""function show(){const key=location.hash.slice(1)||'home';document.querySelectorAll('.view').forEach(v=>v.hidden=v.id!==key);document.querySelectorAll('[data-page]').forEach(a=>a.classList.toggle('active',a.dataset.page===key));}window.addEventListener('hashchange',show);show();"""
    output=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Northstar · Synthetic web reference</title><style>{css}</style></head><body><aside><div class="brand"><div class="mark">N</div><div><b>Signal-to-Change</b><small>Voice of Customer</small></div></div><div class="nav-label">THE LOOP</div><nav>{nav}</nav><footer>Static reference · no live writes<br>One workbook · five edit actions<br>Form gates · 2026-10-18</footer></aside><div class="shell"><div class="topbar"><span class="company">Northstar Scheduling · fictional</span><span class="synthetic">SYNTHETIC EXAMPLE · INVENTED DATA</span><span>Fixture as of Oct 14, 2026 · 15:00 UTC</span><span>No Google connection</span></div><main class="main">{sections}<footer class="bottom-note">Local documentation preview · all records, owners and events are invented · no customer messages or operational writes.</footer></main></div><script>{script}</script></body></html>'
    assert not any(token in output for token in ('@gmail.', 'script.google.com', 'fetch(', 'google.script.run'))
    OUT.write_text(output,encoding='utf-8',newline='\n')
    print('Built eight Northstar web reference views from unchanged synthetic fixtures.')


if __name__=='__main__':
    main()
