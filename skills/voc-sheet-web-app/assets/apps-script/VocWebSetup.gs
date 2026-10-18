/**
 * VocWebSetup.gs - one-time workbook setup for the Signal-to-Change web app. v0.3.0, generated 2026-10-17.
 * Run from the Apps Script editor (Run menu), never from the website. Works for any company's Steps 1-4 workbook.
 *
 *   1. vocWebSetupTabs()        Adds any MISSING web-app tabs (Steps 3-4 registers + Team + Activity_Log).
 *                               Existing tabs are never renamed, reordered, cleared or overwritten; mismatches are reported.
 *   2. vocWebImportRegisters()  Optional. Copies rows of one data class (default REAL) from separate Step 3/4 files
 *                               listed in VOC_WEB_SETUP.IMPORT into this workbook. Skips rows whose key already exists.
 *                               Adds missing trailing columns from the source (additive only) and logs every import.
 *
 * Editor-only reference: adapt mappings, finish imports before enabling the standalone web writer.
 * Locks do not coordinate different projects or direct Sheet edits.
 * Both functions are idempotent: running them twice changes nothing the second time.
 */
var VOC_WEB_SETUP = {
  HEADER_ROW: 4,   // same layout as the Step 1/2 tabs: title (row 1), note (row 2), blank (row 3), headers (row 4)

  // Register columns = the repository templates (skills/voc-customer-follow-up/assets, skills/voc-systemic-change/assets)
  // + 'Data Class' (REAL / SYNTHETIC separation) + 'Notes'.
  TABS: {
    Follow_Up_Cases: { key: ['Case ID'], note: 'Step 3 · one row per customer case. Edited through the web app; every change is logged in Activity_Log.',
      headers: ['Case ID','Source Record References','Evidence Reference','Evidence Class','Audience','Feedback At','Received At','Trigger','Severity','Contact Route','Contact Reference','Owner','Backup Owner','Assigned At','Accepted At','Acceptance Due At','First Contact Due At','First Contact At','Engagement','Delivery','Plan Agreement Evidence','Customer Outcome','Outcome Evidence','Administrative State','Next Update Due At','Root Cause Confidence','Learning','Closure Reason','Closed At','Data Class','Notes'] },
    Case_Actions: { key: ['Action ID'], note: 'Step 3 · actions per case. Proposed actions are not approved until Status changes.',
      headers: ['Action ID','Case ID','Owner','Action','Intended Outcome','Approval Basis','Due At','Status','Completed At','Completion Evidence','Disposition Reason','Transfer Reference','Transfer Accepted At','Data Class','Notes'] },
    Customer_Updates: { key: ['Update ID'], note: 'Step 3 · updates owed or given to customers. A draft is not contact; the app never sends messages.',
      headers: ['Update ID','Case ID','Change ID','Owner','Audience','Channel','Due At','Status','Occurred At','Content Reference','Delivery Evidence','Disposition Reason','Next Update Due At','Data Class','Notes'] },
    Change_Register: { key: ['Change ID'], note: 'Step 4 · one row per proposed or decided company change.',
      headers: ['Change ID','Title','Fix Type','Evidence Reference','Brief Reference','Root Cause Confidence','Decision','Decision Maker','Decision At','Decision Rationale','Owner','Accepted At','State','Next Milestone','Milestone Due At','Measurement Plan Reference','Delivery Evidence','Result Evidence','Reviewer','Reviewed At','Review Due At','Revisit Condition','Merged Into','Report Back Owner','Next Update Due At','Report Back Disposition','Data Class','Notes'] },
    Change_Case_Links: { key: ['Change ID', 'Case ID'], note: 'Step 4 · many-to-many links between changes and cases. A Proposed link is an unaccepted handoff.',
      headers: ['Change ID','Case ID','Customer Communication Owner','Receiving Change Owner','Accepted At','Acceptance Evidence','Next Update Due At','Obligation Status','Disposition Evidence','Data Class','Notes'] },
    Team: { key: ['Email'], note: 'Who may use the web app and who can be chosen as an owner. Active = Yes grants access in team mode. Edit this tab directly.',
      headers: ['Email','Name','Role','Can Decide Changes','Can Own Cases','Active','Added At','Notes'], yesNo: ['Can Decide Changes','Can Own Cases','Active'] },
    Activity_Log: { key: ['Log ID'], note: 'Append-only record of every change made through the web app or setup. Do not edit.',
      headers: ['Log ID','Timestamp','User','Action','Tab','Record ID','Field','Old Value','New Value','Reason','Source','App Version'] }
  },

  // OPTIONAL: separate Step 3/4 spreadsheets to import from (first sheet of each file). Leave '' to skip a tab.
  // Fill confirmed source IDs privately; never publish instance configuration.
  IMPORT: {
    Follow_Up_Cases:   '',
    Case_Actions:      '',
    Customer_Updates:  '',
    Change_Register:   '',
    Change_Case_Links: ''
  },
  IMPORT_CLASS: 'REAL'   // rows whose 'Data Class' starts with this word are imported; set '' to import every row
};

/* ---------------- 1. Tabs ---------------- */
function vocWebSetupTabs() {
  var ss = SpreadsheetApp.getActiveSpreadsheet(), H = VOC_WEB_SETUP.HEADER_ROW, report = [];
  Object.keys(VOC_WEB_SETUP.TABS).forEach(function (name) {
    var def = VOC_WEB_SETUP.TABS[name], sh = ss.getSheetByName(name);
    if (!sh) {
      sh = ss.insertSheet(name);
      sh.getRange(1, 1).setValue(name).setFontWeight('bold');
      sh.getRange(2, 1).setValue(def.note);
      sh.getRange(H, 1, 1, def.headers.length).setValues([def.headers]).setFontWeight('bold');
      sh.setFrozenRows(H);
      if (def.yesNo) vwSetupYesNo_(sh, def);
      report.push({ tab: name, result: 'CREATED', headers: def.headers.length });
    } else {
      var found = vwSetupHeaders_(sh, def), missing = def.headers.filter(function (h) { return found.headers.indexOf(h) < 0; });
      report.push({ tab: name, result: 'EXISTS (unchanged)', headerRow: found.row, missingHeaders: missing });
    }
  });
  var team = ss.getSheetByName('Team'), me = '';
  try { me = Session.getEffectiveUser().getEmail(); } catch (e) { me = ''; }
  var teamMap = team ? vwSetupHeaders_(team, VOC_WEB_SETUP.TABS.Team) : null;
  if (team && me && team.getLastRow() === teamMap.row && VOC_WEB_SETUP.TABS.Team.headers.every(function (h) { return teamMap.headers.indexOf(h) >= 0; })) {
    var seed = { Email: me, Name: '', Role: 'Program lead', 'Can Decide Changes': 'Yes', 'Can Own Cases': 'Yes', Active: 'Yes', 'Added At': vwSetupNow_(), Notes: 'Added by vocWebSetupTabs (the person who ran setup)' };
    team.getRange(teamMap.row + 1, 1, 1, teamMap.headers.length).setValues([teamMap.headers.map(function (h) { return vwSetupLiteral_(seed[h] || ''); })]);
    report.push({ tab: 'Team', result: 'SEEDED with the account running setup' });
  }
  Logger.log(JSON.stringify(report, null, 1));
  return report;
}

/* ---------------- 2. Import ---------------- */
function vocWebImportRegisters() {
  var ss = SpreadsheetApp.getActiveSpreadsheet(), H = VOC_WEB_SETUP.HEADER_ROW, cls = VOC_WEB_SETUP.IMPORT_CLASS, report = [];
  var lock = LockService.getScriptLock(); if (!lock.tryLock(30000)) throw new Error('Another setup or app write is running. Try again in a minute.');
  try {
    var audit = ss.getSheetByName('Activity_Log');
    if (!audit) throw new Error('Run vocWebSetupTabs and resolve Activity_Log before import.');
    var auditHeaders = vwSetupHeaders_(audit, VOC_WEB_SETUP.TABS.Activity_Log).headers;
    if (JSON.stringify(auditHeaders) !== JSON.stringify(VOC_WEB_SETUP.TABS.Activity_Log.headers)) throw new Error('Map Activity_Log headers before import.');
    Object.keys(VOC_WEB_SETUP.IMPORT).forEach(function (name) {
      var id = VOC_WEB_SETUP.IMPORT[name], def = VOC_WEB_SETUP.TABS[name];
      if (!id) { report.push({ tab: name, result: 'SKIPPED (no source listed)' }); return; }
      var target = ss.getSheetByName(name);
      if (!target) { report.push({ tab: name, result: 'BLOCKED: run vocWebSetupTabs first' }); return; }
      var src, srcName;
      try { var file = SpreadsheetApp.openById(id); src = file.getSheets()[0]; srcName = file.getName(); }
      catch (e) { report.push({ tab: name, result: 'FAILED: source could not be opened (' + String(e.message).slice(0, 80) + ')' }); return; }
      var s = vwSetupHeaders_(src, def), sv = src.getLastRow() > s.row ? src.getRange(s.row + 1, 1, src.getLastRow() - s.row, src.getLastColumn()).getValues() : [];
      var t = vwSetupHeaders_(target, def), added = [];
      if (def.key.some(function (k) { return s.headers.indexOf(k) < 0 || t.headers.indexOf(k) < 0; }) || (cls && s.headers.indexOf('Data Class') < 0)) throw new Error('Missing key or Data Class header in ' + name);
      var required = def.headers.filter(function (h) { return t.headers.indexOf(h) < 0; });
      if (required.length) throw new Error('Resolve target headers before import: ' + name);
      s.headers.forEach(function (h) { if (h && t.headers.indexOf(h) < 0) { t.headers.push(h); added.push(h); } });   // additive trailing columns
      if (added.length) target.getRange(t.row, 1, 1, t.headers.length).setValues([t.headers]).setFontWeight('bold');
      var existing = {}, tv = target.getLastRow() > t.row ? target.getRange(t.row + 1, 1, target.getLastRow() - t.row, t.headers.length).getValues() : [];
      tv.forEach(function (r) { var k = vwSetupKey_(def.key, t.headers, r); if (existing[k]) throw new Error('Duplicate target key in ' + name); existing[k] = true; });
      var rows = [], skippedClass = 0, skippedDup = 0, ids = [];
      sv.forEach(function (r) {
        if (!r.some(function (c) { return c !== '' && c !== null; })) return;
        var o = {}; s.headers.forEach(function (h, i) { if (h) o[h] = r[i]; });
        if (cls && String(o['Data Class'] || '').trim().split(/\s+/)[0].toUpperCase() !== cls.toUpperCase()) { skippedClass++; return; }
        var k = def.key.map(function (kk) { return String(o[kk] || '').trim(); }).join('|');
        if (def.key.some(function (kk) { return !String(o[kk] || '').trim(); }) || existing[k]) { skippedDup++; return; }
        existing[k] = true; ids.push(k);
        rows.push(t.headers.map(function (h) { var v = o[h]; return vwSetupLiteral_(v === undefined ? '' : v); }));
      });
      if (rows.length) target.getRange(target.getLastRow() + 1, 1, rows.length, t.headers.length).setValues(rows);
      if (rows.length) vwSetupLog_(ss, ids.map(function (k) { return ['IMPORT', name, k, '', '', 'row imported', 'from "' + srcName + '" (' + (cls || 'all') + ' rows)']; }));
      report.push({ tab: name, result: 'IMPORTED ' + rows.length, skippedOtherClass: skippedClass, skippedDuplicate: skippedDup, columnsAdded: added });
    });
  } finally { lock.releaseLock(); }
  Logger.log(JSON.stringify(report, null, 1));
  return report;
}

/* ---------------- helpers ---------------- */
function vwSetupNow_() { return Utilities.formatDate(new Date(), SpreadsheetApp.getActiveSpreadsheet().getSpreadsheetTimeZone(), "yyyy-MM-dd'T'HH:mm:ssXXX"); }
function vwSetupHeaders_(sh, def) {
  var rows = Math.min(Math.max(sh.getLastRow(), 1), 20), cols = Math.max(sh.getLastColumn(), 1);
  var v = sh.getRange(1, 1, rows, cols).getValues(), candidates = [];
  v.forEach(function (r, i) {
    var h = r.map(function (c) { return String(c).trim(); });
    if (def.key.every(function (k) { return h.indexOf(k) >= 0; })) candidates.push({ row: i + 1, headers: h });
  });
  if (candidates.length !== 1) throw new Error('Missing or ambiguous header row: ' + sh.getName());
  var found = candidates[0];
  while (found.headers.length && !found.headers[found.headers.length - 1]) found.headers.pop();
  if (found.headers.some(function (h, i, all) { return !h || all.indexOf(h) !== i; })) throw new Error('Blank or duplicate headers: ' + sh.getName());
  return found;
}
function vwSetupKey_(key, headers, r) { return key.map(function (k) { var i = headers.indexOf(k); return i < 0 ? '' : String(r[i] || '').trim(); }).join('|'); }
function vwSetupYesNo_(sh, def) {
  var rule = SpreadsheetApp.newDataValidation().requireValueInList(['Yes', 'No'], true).setAllowInvalid(false).build();
  def.yesNo.forEach(function (h) { sh.getRange(VOC_WEB_SETUP.HEADER_ROW + 1, def.headers.indexOf(h) + 1, 500, 1).setDataValidation(rule); });
}
/** Appends to Activity_Log. entries: [action, tab, recordId, field, old, new, reason] */
function vwSetupLiteral_(v) { return typeof v === 'string' && /^\s*[=+\-@]/.test(v) ? "'" + v : v; }
function vwSetupLog_(ss, entries) {
  var log = ss.getSheetByName('Activity_Log'); if (!log) throw new Error('Activity_Log is required.'); if (!entries.length) return;
  var me = ''; try { me = Session.getEffectiveUser().getEmail(); } catch (e) { me = ''; }
  var now = vwSetupNow_(), ver = (typeof VOC_WEB !== 'undefined' ? VOC_WEB.VERSION : 'setup');
  var rows = entries.map(function (e) { return ['LOG-' + Utilities.getUuid(), now, me, e[0], e[1], e[2], e[3], e[4], e[5], e[6], 'setup', ver].map(vwSetupLiteral_); });
  log.getRange(log.getLastRow() + 1, 1, rows.length, rows[0].length).setValues(rows);
}
