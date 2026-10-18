/**
 * VocWebWrite.gs - Signal-to-Change web app edits, v0.4.0, generated 2026-10-17.
 * Reference implementation: requires the adapters documented in workbook-setup-and-team-use.md.
 * Implement the complete mapped lifecycle/closure/merge gates before enabling the relevant controls.
 * One public endpoint, vocWebSave(requestJson). Five allowed actions, each with a fixed set of writable fields and
 * allowed values (repository vocabulary). Every save: authorise -> lock -> re-read the row -> reject if it changed since
 * the page loaded -> write only changed cells -> append one Activity_Log row per changed field -> return the refreshed view.
 * Edits touch only the five Step 3/4 tabs, only REAL rows, and never send anything to a customer.
 */
var VW_VOCAB = {
  engagement: ['Not started', 'Attempted', 'Contacted', 'Customer replied', 'Not contactable', 'No contact requested'],
  delivery:   ['Not assessed', 'Investigating', 'Plan agreed', 'In progress', 'Delivered', 'No action planned'],
  outcome:    ['Unknown', 'Unresolved', 'Partially resolved', 'Resolved confirmed', 'Disputed', 'Not applicable'],
  admin:      ['Open', 'Waiting', 'Closed', 'Reopened'],
  action:     ['Proposed', 'Approved', 'In progress', 'Done', 'Cancelled'],
  update:     ['Sent', 'Attempted', 'Failed', 'Not possible', 'Cancelled'],
  decision:   ['Accept', 'Investigate', 'Defer', 'Decline', 'Merge', 'Stop', 'Reopen']
};
var VW_DECISION_STATE = { Accept: 'Accepted', Investigate: 'Investigating', Defer: 'Deferred', Decline: 'Declined', Merge: 'Merged', Stop: 'Stopped', Reopen: 'Reopened' };

/** req: {action, id, expect, fields:{...}, note, actorName} -> JSON string {ok, changed, data} or {ok:false, error}. */
function vocWebSave(requestJson) {
  var trace = 'VW-' + Date.now().toString(36);
  try {
    var req = JSON.parse(String(requestJson || '{}'));
    if (!req || typeof req !== 'object' || !Object.prototype.hasOwnProperty.call(VW_ACTIONS_, req.action)) return vwSaveErr_('invalid', 'Unknown action.', trace);
    var viewer = vocWebAuthorize_(req.action);
    if (!String(req.note || '').trim()) return vwSaveErr_('invalid', 'Add a reason for this change.', trace);
    var name = String(req.actorName || '').trim().slice(0, 80);
    var actor = viewer || (name ? name + ' (name entered in app)' : '');
    if (!actor) return vwSaveErr_('name', 'Please enter your name so the change can be recorded.', trace);
    var plan = VW_ACTIONS_[req.action];
    if (!plan) return vwSaveErr_('invalid', 'Unknown action.', trace);

    var lock = LockService.getScriptLock();
    if (!lock.tryLock(20000)) return vwSaveErr_('busy', 'Someone else is saving right now. Try again in a moment.', trace);
    try {
      var tab = vocWebReadTab_(plan.tab, {});
      if (tab.state === 'missing') return vwSaveErr_('setup', tab.reason, trace);
      if (tab.state === 'error') return vwSaveErr_('failed', tab.reason, trace);
      var matches = tab.rows.filter(function (r) { return r._class === 'REAL' && String(r[plan.key]).trim() === String(req.id || '').trim(); });
      if (matches.length > 1) return vwSaveErr_('invalid', 'Duplicate record key; reconcile the register first.', trace);
      var row = matches[0];
      if (!row) return vwSaveErr_('invalid', 'Record ' + req.id + ' was not found.', trace);
      if (!req.expect || !row._v || req.expect !== row._v) return vwSaveErr_('stale', 'This record was changed by someone else after you opened it. Refresh to see the latest, then try again.', trace);

      var now = Utilities.formatDate(new Date(), VOC_WEB.TZ, "yyyy-MM-dd'T'HH:mm:ssXXX");
      var out = plan.build(req.fields || {}, row, { actor: actor, now: now, tab: tab });
      if (out.error) return vwSaveErr_('invalid', out.error, trace);

      var missing = Object.keys(out.set).filter(function (h) { return tab.headers.indexOf(h) < 0; });
      if (missing.length) return vwSaveErr_('setup', 'Column(s) missing in ' + plan.tab + ': ' + missing.join(', ') + '.', trace);
      var ss = SpreadsheetApp.openById(vocWebBenchmarkId_()), sh = ss.getSheetByName(plan.tab), hdrRow = vwHeaderRowValues_(sh, tab.headerRow);
      var audit = ss.getSheetByName('Activity_Log');
      if (!audit || !vwAuditReady_(audit)) return vwSaveErr_('setup', 'Map the Activity_Log schema before enabling edits.', trace);
      var changes = [];
      if (Object.keys(out.set).some(function (h) { return hdrRow.indexOf(h) < 0 || sh.getRange(row._row, hdrRow.indexOf(h) + 1).getFormula(); })) return vwSaveErr_('setup', 'A writable field is missing or contains a formula.', trace);
      Object.keys(out.set).forEach(function (h) {
        var raw = out.set[h], nv = vwLiteral_(raw), ov = row[h] === undefined ? '' : row[h];
        if (String(ov) === String(raw)) return;
        var cell = sh.getRange(row._row, hdrRow.indexOf(h) + 1);
        if (cell.getFormula()) throw new Error('Formula cell is not writable.');
        cell.setValue(nv);
        changes.push([h, ov, raw]);
      });
      if (!changes.length) return JSON.stringify({ ok: true, changed: 0, message: 'Nothing changed.', data: vocWebViewForSave_(viewer, trace) });
      var reason = String(req.note || out.reason || '').slice(0, 500);
      vwAppendLog_(ss, changes.map(function (c) { return [actor, plan.label, plan.tab, req.id, c[0], c[1], c[2], reason]; }), now);
    } finally { lock.releaseLock(); }
    return JSON.stringify({ ok: true, changed: changes.length, message: plan.label + ' · ' + changes.length + ' field' + (changes.length === 1 ? '' : 's') + ' logged', data: vocWebViewForSave_(viewer, trace) });
  } catch (e) {
    console.error(trace + ' save failed: ' + vocWebSafeMessage_(e));
    var denied = /VOC_WEB_DENIED/.test(String(e && e.message));
    return vwSaveErr_(denied ? 'denied' : 'failed', denied ? 'You do not have access to this view.' : 'Save failed and may have partially changed the Sheet. Refresh and reconcile Activity_Log before retrying.', trace);
  }
}

var VW_ACTIONS_ = {
  decideChange: { tab: 'Change_Register', key: 'Change ID', label: 'Decision recorded', build: function (f, row, x) {
    if (VW_VOCAB.decision.indexOf(f.decision) < 0) return { error: 'Choose a decision.' };
    var why = String(f.rationale || '').trim(); if (!why) return { error: 'Add the reason for the decision.' };
    var set = { 'Decision': f.decision, 'Decision Maker': x.actor, 'Decision At': x.now, 'Decision Rationale': why, 'State': VW_DECISION_STATE[f.decision] };
    if (f.decision === 'Merge') {
      var into = String(f.mergeInto || '').trim(); if (!into || into === row['Change ID']) return { error: 'Choose the change to merge into.' };
      set['Merged Into'] = into;
    }
    if (f.decision !== 'Merge' && row['Merged Into']) set['Merged Into'] = '';
    if (f.decision === 'Accept' && (!row.Owner || !row['Accepted At'])) return { error: 'Acceptance needs an owner and recorded owner acceptance.' };
    if (f.decision === 'Defer' && !(row['Review Due At'] || row['Revisit Condition'])) return { error: 'Deferring needs a review date or revisit condition.' };
    if (['Defer','Decline','Merge','Stop'].indexOf(f.decision) >= 0 && !row['Report Back Disposition']) return { error: 'Record the report-back disposition first.' };
    if (f.decision === 'Merge') return { error: 'Merge requires a mapped obligation-transfer workflow; this reference keeps it disabled.' };
    return { set: set, reason: why };
  } },
  setCaseOwner: { tab: 'Follow_Up_Cases', key: 'Case ID', label: 'Owner updated', build: function (f, row, x) {
    var owner = String(f.owner || '').trim().slice(0, 120); if (!owner) return { error: 'Enter or choose an owner.' };
    var set = { 'Owner': owner };
    if (owner !== row.Owner) { set['Assigned At'] = x.now; set['Accepted At'] = ''; }
    if (f.accepted) set['Accepted At'] = row['Accepted At'] && owner === row.Owner ? row['Accepted At'] : x.now;
    return { set: set };
  } },
  setCaseStatus: { tab: 'Follow_Up_Cases', key: 'Case ID', label: 'Case status updated', build: function (f, row, x) {
    var set = {}, map = { engagement: ['Engagement', VW_VOCAB.engagement], delivery: ['Delivery', VW_VOCAB.delivery], outcome: ['Customer Outcome', VW_VOCAB.outcome], admin: ['Administrative State', VW_VOCAB.admin] };
    for (var k in map) { if (f[k] === undefined || f[k] === '') continue; if (map[k][1].indexOf(f[k]) < 0) return { error: 'Invalid ' + map[k][0] + '.' }; set[map[k][0]] = f[k]; }
    if (f.nextUpdateDueAt !== undefined) { var d = vwLocalToIso_(f.nextUpdateDueAt); if (f.nextUpdateDueAt && !d) return { error: 'Next update time is not valid.' }; set['Next Update Due At'] = d; }
    if (set['Administrative State'] === 'Closed' && row['Administrative State'] !== 'Closed') {
      var cr = String(f.closureReason || '').trim(); if (!cr) return { error: 'Closing a case needs a closure reason.' };
      set['Closure Reason'] = cr; set['Closed At'] = x.now;
    }
    if (set['Customer Outcome'] === 'Resolved confirmed' && !row['Outcome Evidence']) return { error: 'Confirmed resolution needs outcome evidence.' };
    if (set.Delivery === 'Plan agreed' && !row['Plan Agreement Evidence']) return { error: 'Plan agreed needs agreement evidence.' };
    if (set.Delivery === 'Delivered') {
      var actions = vocWebReadTab_('Case_Actions', {});
      if (actions.state !== 'ok' || !actions.rows.some(function (a) { return a._class === 'REAL' && a['Case ID'] === row['Case ID'] && a.Status === 'Done' && a['Completion Evidence']; })) return { error: 'Delivered needs a completed action with evidence.' };
    }
    if (set['Administrative State'] === 'Closed' && row['Administrative State'] !== 'Closed') return { error: 'Closure requires a mapped commitment/transfer review; this reference keeps it disabled.' };
    if (['Contacted','Customer replied'].indexOf(set.Engagement) >= 0 && !row['Contact Reference']) return { error: 'Contact needs an evidence reference.' };
    if (set['Engagement'] === 'Contacted' && !row['First Contact At']) set['First Contact At'] = x.now;
    return { set: set };
  } },
  setActionStatus: { tab: 'Case_Actions', key: 'Action ID', label: 'Action updated', build: function (f, row, x) {
    if (VW_VOCAB.action.indexOf(f.status) < 0) return { error: 'Choose a status.' };
    var set = { 'Status': f.status };
    if (f.owner !== undefined && String(f.owner).trim()) set['Owner'] = String(f.owner).trim().slice(0, 120);
    if (['Approved','In progress','Done'].indexOf(f.status) >= 0 && !(f.approvalBasis || row['Approval Basis'])) return { error: 'Record the approval basis first.' };
    if (f.status === 'Done') { var ev = String(f.evidence || '').trim(); if (!ev) return { error: 'Done needs completion evidence (what shows it was done).' }; set['Completion Evidence'] = ev; set['Completed At'] = x.now; }
    if (f.status === 'Cancelled') { var dr = String(f.reason || '').trim(); if (!dr) return { error: 'Cancelling needs a reason.' }; set['Disposition Reason'] = dr; }
    if (f.approvalBasis) set['Approval Basis'] = String(f.approvalBasis).trim().slice(0, 300);
    return { set: set };
  } },
  logUpdate: { tab: 'Customer_Updates', key: 'Update ID', label: 'Update logged', build: function (f, row, x) {
    if (VW_VOCAB.update.indexOf(f.status) < 0) return { error: 'Choose what happened.' };
    var set = { 'Status': f.status, 'Occurred At': vwLocalToIso_(f.occurredAt) || x.now };
    if (['Sent','Attempted','Failed'].indexOf(f.status) >= 0 && !String(f.evidence || '').trim()) return { error: 'Record delivery/attempt evidence.' };
    if (f.status === 'Sent' && !row['Content Reference']) return { error: 'Sent needs a content reference.' };
    if (['Attempted','Failed'].indexOf(f.status) >= 0) set['Delivery Evidence'] = String(f.evidence).trim();
    if (f.occurredAt && !vwLocalToIso_(f.occurredAt)) return { error: 'Occurrence time is not valid.' };
    if (f.status === 'Sent') { var ev = String(f.evidence || '').trim(); if (!ev) return { error: 'Sent needs delivery evidence (where it was sent, message link or reference).' }; set['Delivery Evidence'] = ev; }
    else { var dr = String(f.reason || '').trim(); if (!dr) return { error: 'Add a short reason or detail.' }; set['Disposition Reason'] = dr; }
    return { set: set };
  } }
};

/* ---------- helpers ---------- */
function vwSaveErr_(kind, message, trace) { return JSON.stringify({ ok: false, error: { kind: kind, message: message, trace: trace } }); }
function vwLiteral_(v) { return (typeof v === 'string' && /^\s*[=+\-@]/.test(v)) ? "'" + v : v; }
function vwHeaderRowValues_(sh, headerRow) { return sh.getRange(headerRow, 1, 1, sh.getLastColumn()).getValues()[0].map(function (c) { return String(c).trim(); }); }
function vwAuditReady_(sh) {
  var expected = ['Log ID','Timestamp','User','Action','Tab','Record ID','Field','Old Value','New Value','Reason','Source','App Version'];
  var rows = sh.getRange(1, 1, Math.min(20, sh.getLastRow()), sh.getLastColumn()).getValues();
  return rows.filter(function (r) { return JSON.stringify(r.map(function (c) { return String(c).trim(); })) === JSON.stringify(expected); }).length === 1;
}
/** Browser local time is interpreted in configured VOC_WEB.TZ. Verify DST transitions in the adapted app. */
function vwLocalToIso_(v) {
  var m = /^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})$/.exec(String(v || '').trim()); if (!m) return '';
  var probe = new Date(m[1] + 'T12:00:00Z'), off = Utilities.formatDate(probe, VOC_WEB.TZ, 'XXX');
  var d = new Date(m[1] + 'T' + m[2] + ':00' + off); return isNaN(d.getTime()) ? '' : Utilities.formatDate(d, VOC_WEB.TZ, "yyyy-MM-dd'T'HH:mm:ssXXX");
}
function vwAppendLog_(ss, entries, now) {
  var log = ss.getSheetByName('Activity_Log'); if (!log) throw new Error('Activity_Log is required.');
  var rows = entries.map(function (e) { return ['LOG-' + Utilities.getUuid(), now, e[0], e[1], e[2], e[3], e[4], String(e[5]), String(e[6]), e[7], 'web app', VOC_WEB.VERSION].map(function (v) { return vwLiteral_(v); }); });
  log.getRange(log.getLastRow() + 1, 1, rows.length, 12).setValues(rows);
}
function vocWebViewForSave_(viewer, trace) {
  var vm = vocWebBuildViewModel_(new Date()); vm.meta.viewer = viewer; vm.meta.trace = trace; return vm;
}
