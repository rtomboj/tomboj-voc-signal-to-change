/* Synthetic service/DOM doubles execute the shipped reference code, not a duplicate endpoint.
   They do not establish hosted rendering, cross-origin navigation, or Google permissions. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const crypto = require('node:crypto');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const asset = name => fs.readFileSync(path.join(root, 'skills/voc-sheet-web-app/assets/apps-script', name), 'utf8');
const clone = value => JSON.parse(JSON.stringify(value));

class Sheet {
  constructor(name, rows = []) { this.name = name; this.rows = clone(rows); this.writes = 0; this.formulas = {}; }
  getName() { return this.name; }
  getLastRow() { return this.rows.length; }
  getLastColumn() { return Math.max(0, ...this.rows.filter(Boolean).map(r => r.length)); }
  setFrozenRows() { return this; }
  getRange(row, col, height = 1, width = 1) {
    const sheet = this;
    return {
      getValues() { return Array.from({length: height}, (_, i) => Array.from({length: width}, (_, j) => sheet.rows[row+i-1]?.[col+j-1] ?? '')); },
      setValues(values) {
        values.forEach((r, i) => r.forEach((v, j) => {
          sheet.rows[row+i-1] ||= [];
          // Sheets returns the displayed literal without its leading escape apostrophe.
          sheet.rows[row+i-1][col+j-1] = typeof v === 'string' && v.startsWith("'") ? v.slice(1) : v;
          sheet.writes++;
        })); return this;
      },
      setValue(value) { return this.setValues([[value]]); },
      setFontWeight() { return this; }, setDataValidation() { return this; },
      getFormula() { return sheet.formulas[`${row}:${col}`] || ''; },
    };
  }
}

function environment() {
  const sheets = {}, sources = {};
  const book = {
    getSheetByName: name => sheets[name] || null,
    insertSheet: name => (sheets[name] = new Sheet(name)),
    getSpreadsheetTimeZone: () => 'UTC',
  };
  const state = { locked: false, busy: false, viewer: 'owner@northstar.example', denied: false, calls: [] };
  const sandbox = {
    Date, console: {error() {}}, Logger: {log() {}},
    Utilities: {getUuid: () => crypto.randomUUID(), formatDate: (date, tz, format) => format === 'XXX' ? '+00:00' : date.toISOString().replace('.000Z', '+00:00')},
    Session: {getEffectiveUser: () => ({getEmail: () => 'owner@northstar.example'})},
    SpreadsheetApp: {
      getActiveSpreadsheet: () => book,
      openById: id => { if (id === 'SYNTHETIC-WORKBOOK') return book; if (!sources[id]) throw Error('No source'); return sources[id]; },
      newDataValidation: () => ({requireValueInList() {return this;}, setAllowInvalid() {return this;}, build() {return {};}}),
    },
    LockService: {getScriptLock: () => ({tryLock: () => { if (state.busy) return false; state.locked = true; return true; }, releaseLock: () => {state.locked = false;}})},
  };
  const c = vm.createContext(sandbox);
  vm.runInContext(asset('VocWebSetup.gs'), c);
  vm.runInContext(asset('VocWebWrite.gs'), c);
  c.VOC_WEB = {TZ: 'UTC', VERSION: 'synthetic-test'};
  c.vocWebBenchmarkId_ = () => 'SYNTHETIC-WORKBOOK';
  c.vocWebAuthorize_ = action => {state.calls.push(action); if (state.denied) throw Error('VOC_WEB_DENIED'); return state.viewer;};
  c.vocWebSafeMessage_ = () => 'redacted';
  c.vocWebReadTab_ = name => {
    const sh = sheets[name]; if (!sh) return {state: 'missing', reason: 'Missing tab'};
    const def = c.VOC_WEB_SETUP.TABS[name], map = c.vwSetupHeaders_(sh, def);
    const rows = sh.rows.slice(map.row).filter(r => r.some(v => v !== '')).map((values, i) => {
      const r = Object.fromEntries(map.headers.map((h, j) => [h, values[j] ?? '']));
      r._class = r['Data Class']; r._row = map.row + i + 1;
      r._v = crypto.createHash('sha256').update(JSON.stringify(values)).digest('hex'); return r;
    });
    return {state: 'ok', headers: map.headers, headerRow: map.row, rows};
  };
  c.vocWebBuildViewModel_ = () => ({meta: {}, cases: c.vocWebReadTab_('Follow_Up_Cases').rows});
  const snapshot = () => JSON.stringify(Object.fromEntries(Object.entries(sheets).map(([n, s]) => [n, s.rows])));
  const add = (name, obj) => {const h = c.VOC_WEB_SETUP.TABS[name].headers; sheets[name].rows.push(h.map(k => obj[k] ?? ''));};
  const request = (action, fields, overrides = {}) => {
    const plan = c.VW_ACTIONS_[action], row = c.vocWebReadTab_(plan.tab).rows[0];
    return {action, id: row[plan.key], expect: row._v, fields, note: 'Synthetic operator reason', ...overrides};
  };
  const save = req => JSON.parse(c.vocWebSave(JSON.stringify(req)));
  return {c, state, sheets, sources, snapshot, add, request, save};
}

function fixture() {
  const e = environment(); e.c.vocWebSetupTabs();
  e.add('Follow_Up_Cases', {'Case ID':'CASE-001', Owner:'Intake owner', 'Data Class':'REAL', Engagement:'Not started', Delivery:'Not assessed', 'Customer Outcome':'Unknown', 'Administrative State':'Open'});
  e.add('Case_Actions', {'Action ID':'ACTION-001', 'Case ID':'CASE-001', Owner:'Intake owner', Status:'Proposed', 'Data Class':'REAL', 'Approval Basis':'Synthetic approval'});
  e.add('Customer_Updates', {'Update ID':'UPDATE-001', 'Case ID':'CASE-001', Status:'Draft', 'Content Reference':'Synthetic draft', 'Data Class':'REAL'});
  e.add('Change_Register', {'Change ID':'CHANGE-001', Title:'Synthetic improvement', Decision:'', State:'Proposed', Owner:'Change owner', 'Data Class':'REAL'});
  return e;
}

// Parse controls from the actual reference markup, rather than inventing request fields in the test.
const decode = value => String(value || '').replaceAll('&quot;', '"').replaceAll('&#39;', "'").replaceAll('&lt;', '<').replaceAll('&gt;', '>').replaceAll('&amp;', '&');
function attributes(text) {
  return Object.fromEntries([...text.matchAll(/([\w:-]+)(?:="([^"]*)")?/g)].map(m => [m[1],decode(m[2] || '')]));
}
function parseForm(html) {
  const controls=[];
  for (const match of html.matchAll(/<input\b([^>]*)>|<select\b([^>]*)>([\s\S]*?)<\/select>|<textarea\b([^>]*)>([\s\S]*?)<\/textarea>/g)) {
    const attrs=attributes(match[1] ?? match[2] ?? match[4]);
    if (!attrs.name) continue;
    const options=match[2]===undefined ? [] : [...match[3].matchAll(/<option\b([^>]*)>([\s\S]*?)<\/option>/g)].map(m=>{
      const a=attributes(m[1]); return {value:a.value ?? decode(m[2]),textContent:decode(m[2]),disabled:'disabled' in a,selected:'selected' in a,title:a.title || ''};
    });
    const control={name:attrs.name,type:attrs.type || (match[2]!==undefined?'select':'text'),checked:'checked' in attrs,disabled:'disabled' in attrs,options,
      value:options.length ? (options.find(o=>o.selected) || options.find(o=>!o.disabled) || options[0]).value : match[4]!==undefined ? decode(match[5]) : attrs.value || '',
      hasAttribute:k=>k in attrs,getAttribute:k=>attrs[k],setAttribute:(k,v)=>{attrs[k]=String(v);}};
    controls.push(control);
  }
  const attrs=attributes(/<form\b([^>]*)>/.exec(html)[1]);
  const error={hidden:true,textContent:'',innerHTML:''}, button={disabled:false,lastChild:{textContent:'Save'}};
  const form={controls,html,error,button,dataset:{action:attrs['data-action'],id:attrs['data-id'],expect:attrs['data-expect']},
    querySelectorAll:()=>controls,querySelector:s=>s==='.ef-err'?error:s==='button[type=submit]'?button:controls.find(c=>s===`[name=${c.name}]`)};
  controls.forEach(c=>c.closest=()=>form);
  return form;
}

function setRow(e, tab, fields) {
  const headers=e.c.VOC_WEB_SETUP.TABS[tab].headers;
  for (const [key,value] of Object.entries(fields)) e.sheets[tab].rows[4][headers.indexOf(key)]=value;
}

function formHarness(e, action) {
  const listeners={}, storage={}, captured=[]; let form, loaded;
  const db=Object.fromEntries(['Follow_Up_Cases','Case_Actions','Customer_Updates','Change_Register'].map(n=>[n,e.c.vocWebReadTab_(n).rows]));
  const D={toD:v=>new Date(v),isUnknown:v=>!v,changes:db=>db.Change_Register.map(r=>({id:r['Change ID'],state:r.State,r}))};
  const U={esc:v=>String(v??'').replaceAll('&','&amp;').replaceAll('"','&quot;').replaceAll('<','&lt;'),icon:()=>'',status:()=>'',lifecycle:()=>'',toast:()=>{},drawer:{open:html=>{form=parseForm(html);},close:()=>{}}};
  const google={script:{run:{withSuccessHandler(success){return {withFailureHandler(failure){return {vocWebSave(json){queueMicrotask(()=>{try{captured.push(JSON.parse(json));success(e.c.vocWebSave(json));}catch(error){failure(error);}});}};}};}}}};
  const window={UI:U,APP_CONFIG:{instance:{timezone:'UTC',key:'northstar-synthetic'}},Derive:D,confirm:()=>true,
    Data:{meta:()=>({canEdit:true,viewer:e.state.viewer,vocab:e.c.VW_VOCAB,people:[],caseEditFacts:e.c.vocWebCaseEditFacts_(db.Follow_Up_Cases)}),
      save:req=>new Promise((resolve,reject)=>google.script.run.withSuccessHandler(json=>{const res=JSON.parse(json);resolve({...res,loaded:res.data});}).withFailureHandler(reject).vocWebSave(JSON.stringify(req)))},__s2cSetLoaded:v=>{loaded=v;}};
  const browser=vm.createContext({window,document:{addEventListener:(n,f)=>listeners[n]=f},localStorage:{getItem:k=>storage[k],setItem:(k,v)=>{storage[k]=v;}},Date,Intl});
  vm.runInContext(asset('Edit.html').replace(/^<script>\s*/,'').replace(/<\/script>\s*$/,''),browser);
  const ids={decideChange:'CHANGE-001',setCaseOwner:'CASE-001',setCaseStatus:'CASE-001',setActionStatus:'ACTION-001',logUpdate:'UPDATE-001'};
  window.Edit.open(action,ids[action],null,{db,D});
  return {form,captured,get loaded(){return loaded;},
    fill(values){for (const [name,value] of Object.entries(values)) {const c=form.controls.find(c=>c.name===name);assert.ok(c,`${action} form is missing ${name}`);if(c.type==='checkbox')c.checked=value;else c.value=value;listeners.input?.({target:c});}},
    async submit(){listeners.submit({target:{closest:()=>form},preventDefault:()=>{}});await new Promise(resolve=>setImmediate(resolve));},
  };
}

async function choiceMatrix(action) {
  const probe=formHarness(fixture(),action);
  const selects=probe.form.controls.filter(c=>c.options.length);
  const choices=selects.flatMap(c=>c.options.filter(o=>o.value && !o.disabled).map(o=>[c.name,o.value]));
  if (action==='setCaseOwner') choices.push(['accepted',false],['accepted',true]);
  if (action==='setCaseStatus') choices.push(['delivery','Delivered']); // positive server-evidence variant
  for (const [name,value] of choices) {
    const e=fixture();
    if (action==='decideChange') setRow(e,'Change_Register',{Owner:'','Accepted At':'','Report Back Disposition':'','Review Due At':'','Revisit Condition':''});
    if (action==='setActionStatus') setRow(e,'Case_Actions',{Status:value==='Proposed'?'Cancelled':'Proposed','Approval Basis':'','Completion Evidence':'','Disposition Reason':''});
    if (action==='logUpdate') setRow(e,'Customer_Updates',{'Content Reference':'','Delivery Evidence':'','Disposition Reason':''});
    if (action==='setCaseStatus') {
      const key={engagement:'Engagement',delivery:'Delivery',outcome:'Customer Outcome',admin:'Administrative State'}[name];
      const alternative={engagement:value==='Attempted'?'Not started':'Attempted',delivery:value==='Investigating'?'Not assessed':'Investigating',outcome:value==='Unresolved'?'Unknown':'Unresolved',admin:value==='Waiting'?'Open':'Waiting'}[name];
      setRow(e,'Follow_Up_Cases',{[key]:alternative});
      if (value==='Delivered') setRow(e,'Case_Actions',{Status:'Done','Completion Evidence':'Synthetic done-action proof'});
    }
    const h=formHarness(e,action);
    const common={note:'Synthetic form-only check'};
    const values={
      decideChange:{decision:value,rationale:'Synthetic decision reason',owner:'Synthetic change owner',accepted:true,reportBackDisposition:'Decision retained for internal report-back',reviewDueAt:'2026-11-01T12:00',revisitCondition:''},
      setCaseOwner:{owner:'Synthetic new owner',accepted:value},
      setCaseStatus:{contactReference:'Synthetic contact reference',planAgreementEvidence:'Synthetic agreed plan',outcomeEvidence:'Synthetic customer confirmation',[name]:value},
      setActionStatus:{status:value,approvalBasis:'Synthetic approval',evidence:'Synthetic completion',reason:'Synthetic cancellation'},
      logUpdate:{status:value,contentReference:'Synthetic content',evidence:'Synthetic delivery or attempt',reason:'Synthetic outcome detail'},
    }[action];
    if (name!=='accepted') {const control=h.form.controls.find(c=>c.name===name);assert.ok(control.options.some(o=>o.value===value && !o.disabled),`${name}=${value} must be enabled`);}
    h.fill({...common,...values});const before=e.sheets.Activity_Log.getLastRow();await h.submit();
    assert.ok(h.loaded,`${action} ${name}=${value}: ${h.form.error.textContent || h.form.error.innerHTML}`);
    assert.ok(e.sheets.Activity_Log.getLastRow()>before,`${action} ${value} must log changes`);
    const sent=h.captured[0].fields;
    assert.ok(Object.keys(sent).every(k=>h.form.controls.some(c=>c.name===k)), 'Only actual form fields may be submitted');
    const logs=e.sheets.Activity_Log.rows.slice(before);
    assert.equal(new Set(logs.map(r=>r[0])).size,logs.length);
    if (action==='decideChange' && value==='Accept') assert.ok(logs.some(r=>r[6]==='Owner') && logs.some(r=>r[6]==='Accepted At'));
    if (action==='decideChange' && ['Defer','Decline','Stop'].includes(value)) assert.ok(logs.some(r=>r[6]==='Report Back Disposition'));
    if (action==='logUpdate' && value==='Sent') assert.ok(logs.some(r=>r[6]==='Content Reference'));
  }
  // Defer is also satisfiable with only a revisit condition, without a date.
  if(action==='decideChange') {const e=fixture(),h=formHarness(e,action);h.fill({decision:'Defer',rationale:'Review condition',reportBackDisposition:'Retain report-back owner',revisitCondition:'After the next pilot',note:'Synthetic condition-only test'});await h.submit();assert.ok(h.loaded);}
  console.log(`Exercised ${choices.length} enabled choices for ${action}`);
}

const cases = {
  gates() {
    const e=fixture();
    for(const [action,fields] of [
      ['decideChange',{decision:'Accept',rationale:'Synthetic accept',owner:'New owner',accepted:false}],
      ['decideChange',{decision:'Defer',rationale:'Synthetic defer',reportBackDisposition:'Internal report-back',reviewDueAt:'',revisitCondition:''}],
      ['decideChange',{decision:'Decline',rationale:'Synthetic decline',reportBackDisposition:''}],
      ['decideChange',{decision:'Stop',rationale:'Synthetic stop',reportBackDisposition:''}],
      ['setCaseStatus',{engagement:'Contacted',contactReference:''}],
      ['setCaseStatus',{engagement:'Customer replied',contactReference:''}],
      ['setCaseStatus',{delivery:'Plan agreed',planAgreementEvidence:''}],
      ['setCaseStatus',{outcome:'Resolved confirmed',outcomeEvidence:''}],
      ['setActionStatus',{status:'Approved',approvalBasis:'   '}],
      ['setActionStatus',{status:'In progress',approvalBasis:''}],
      ['setActionStatus',{status:'Done',approvalBasis:'',evidence:'Synthetic proof'}],
      ['logUpdate',{status:'Sent',contentReference:'',evidence:'Synthetic delivery'}],
      ['logUpdate',{status:'Attempted',evidence:'',reason:'Synthetic detail'}],
      ['logUpdate',{status:'Failed',evidence:'',reason:'Synthetic detail'}],
      ['logUpdate',{status:'Cancelled',reason:''}],
    ]) {const before=e.snapshot(),out=e.save(e.request(action,fields));assert.equal(out.ok,false,`${action} must keep its evidence gate`);assert.equal(out.error.kind,'invalid');assert.equal(e.snapshot(),before);}
  },
  choices_decideChange:()=>choiceMatrix('decideChange'),
  choices_setCaseOwner:()=>choiceMatrix('setCaseOwner'),
  choices_setCaseStatus:()=>choiceMatrix('setCaseStatus'),
  choices_setActionStatus:()=>choiceMatrix('setActionStatus'),
  choices_logUpdate:()=>choiceMatrix('logUpdate'),
  async disabled() {
    for (const [action,name,value,reason,fields] of [
      ['decideChange','decision','Merge','Needs an obligation-transfer workflow (not in this reference)',{decision:'Merge',mergeInto:'CHANGE-002',rationale:'Synthetic merge',reportBackDisposition:'Keep obligations'}],
      ['setCaseStatus','admin','Closed','Closure needs a commitment/transfer review (not in this reference)',{admin:'Closed',closureReason:'Synthetic closure'}],
      ['setCaseStatus','delivery','Delivered','Needs a Done action with completion evidence',{delivery:'Delivered'}],
    ]) {
      const e=fixture(),h=formHarness(e,action),o=h.form.controls.find(c=>c.name===name).options.find(o=>o.value===value);
      assert.equal(o.disabled,true);assert.ok(o.textContent.includes(reason));assert.ok(h.form.html.includes(reason));
      const before=e.snapshot(),out=e.save(e.request(action,fields));assert.equal(out.ok,false);assert.equal(out.error.kind,'invalid');assert.equal(e.snapshot(),before);
      assert.ok(!h.form.controls.some(c=>c.name==='mergeInto'||c.name==='closureReason'));
    }
    // Losing evidence after opening still fails on the server even if the UI once allowed Delivered.
    const e=fixture();setRow(e,'Case_Actions',{Status:'Done','Completion Evidence':'Synthetic proof'});
    const h=formHarness(e,'setCaseStatus');h.fill({delivery:'Delivered',note:'Synthetic stale eligibility'});setRow(e,'Case_Actions',{'Completion Evidence':''});await h.submit();assert.ok(!h.loaded);assert.ok(h.form.error.innerHTML.includes('completed action'));
  },
  async prefill() {
    const maps={decideChange:{owner:'Owner',reportBackDisposition:'Report Back Disposition',revisitCondition:'Revisit Condition'},setCaseStatus:{contactReference:'Contact Reference',planAgreementEvidence:'Plan Agreement Evidence',outcomeEvidence:'Outcome Evidence'},setActionStatus:{approvalBasis:'Approval Basis',evidence:'Completion Evidence',reason:'Disposition Reason'},logUpdate:{contentReference:'Content Reference',evidence:'Delivery Evidence',reason:'Disposition Reason'}};
    for (const [action,map] of Object.entries(maps)) {
      const e=fixture(),tab=e.c.VW_ACTIONS_[action].tab,values=Object.fromEntries(Object.values(map).map(k=>[k,`Synthetic existing ${k}`]));setRow(e,tab,values);
      const h=formHarness(e,action);for(const [name,key] of Object.entries(map)){const c=h.form.controls.find(c=>c.name===name);assert.equal(c.value,values[key]);assert.equal(c.getAttribute('data-initial'),values[key]);}
      const changed=action==='decideChange'?{decision:'Investigate',rationale:'Synthetic review'}:action==='setCaseStatus'?{admin:'Waiting'}:{status:action==='logUpdate'?'Failed':'In progress'};
      h.fill({note:'Synthetic unchanged fields test',...changed});await h.submit();assert.ok(h.loaded);
      for(const name of Object.keys(map))assert.ok(!(name in h.captured[0].fields),`Unchanged ${name} should be omitted`);
    }
    const e=fixture();setRow(e,'Change_Register',{'Review Due At':'2026-11-01T12:00:00+00:00','Accepted At':'2026-10-01T12:00:00+00:00'});const h=formHarness(e,'decideChange');
    assert.equal(h.form.controls.find(c=>c.name==='reviewDueAt').value,'2026-11-01T12:00');assert.equal(h.form.controls.find(c=>c.name==='accepted').checked,true);
    h.fill({owner:'Another synthetic owner'});assert.equal(h.form.controls.find(c=>c.name==='accepted').checked,false);
  },
  facts() {
    const e=fixture();let vm=e.c.vocWebViewForSave_(e.state.viewer,'synthetic');assert.equal(vm.meta.caseEditFacts['CASE-001'].canDeliver,false);
    setRow(e,'Case_Actions',{Status:'Done','Completion Evidence':'Synthetic completion'});vm=e.c.vocWebViewForSave_(e.state.viewer,'synthetic');assert.equal(vm.meta.caseEditFacts['CASE-001'].canDeliver,true);
    // Synthetic and unknown-class actions cannot unlock a REAL case.
    setRow(e,'Case_Actions',{'Data Class':'SYNTHETIC'});assert.equal(e.c.vocWebCaseEditFacts_(vm.cases)['CASE-001'].canDeliver,false);
    assert.deepEqual(clone(e.c.vocWebCaseEditFacts_([])),{});
  },
  dates() {
    const e = environment();
    vm.runInContext(fs.readFileSync(path.join(root, 'skills/voc-monitoring-automation/assets/apps-script/MonitorTableDates.gs'), 'utf8'), e.c);
    const now = new Date('2026-10-18T12:00:00Z');
    const old = new Date(now - 30 * 86400000), fresh = new Date(now - 86400000);
    const rows = e.c.vocMonitorTableValues_([[old,'SUCCESS',0,null],[fresh,'SUCCESS'],[new Date(NaN),'FAILED']], 'UTC');
    const stale = value => now - new Date(value) > 7 * 86400000;
    assert.ok(stale(rows[0][0])); assert.ok(!stale(rows[1][0]));
    assert.equal(rows[0][0].slice(0,10), '2026-09-18');
    assert.equal(rows[0][2], 0); assert.equal(rows[0][3], ''); assert.equal(rows[2][0], '');
    assert.equal(e.c.vocMonitorCell_('already text', 'UTC'), 'already text');
    assert.ok(!Number.isFinite(Date.parse(String(old).slice(0,10))) || String(old).slice(0,10) !== rows[0][0].slice(0,10));
  },
  setup() {
    const e = environment(); const {c, sheets, sources} = e;
    assert.ok(Object.values(c.VOC_WEB_SETUP.IMPORT).every(v => v === ''));
    c.vocWebSetupTabs(); const before = e.snapshot(); c.vocWebSetupTabs(); assert.equal(e.snapshot(), before);
    const headers = clone(c.VOC_WEB_SETUP.TABS.Case_Actions.headers);
    const row = (id, cls, value) => headers.map(h => ({'Action ID':id, 'Case ID':'CASE-001', 'Data Class':cls, Action:value})[h] || '');
    const src = new Sheet('Case_Actions', [headers, row('ACTION-001','REAL','=1+1'), row('ACTION-SYN','SYNTHETIC','demo'), row('ACTION-NO','','unknown')]);
    sources['SYNTHETIC-SOURCE'] = {getSheets: () => [src], getName: () => 'Northstar synthetic import'};
    c.VOC_WEB_SETUP.IMPORT.Case_Actions = 'SYNTHETIC-SOURCE';
    c.vocWebImportRegisters(); const tab = c.vocWebReadTab_('Case_Actions');
    assert.equal(tab.rows.length, 1); assert.equal(tab.rows[0].Action, '=1+1');
    assert.equal(sheets.Activity_Log.getLastRow(), 5);
    const imported = e.snapshot(); c.vocWebImportRegisters(); c.vocWebSetupTabs(); assert.equal(e.snapshot(), imported);
    // A header-only Team tab on row 1 must seed row 2, preserving layout.
    sheets.Team = new Sheet('Team', [clone(c.VOC_WEB_SETUP.TABS.Team.headers)]);
    c.vocWebSetupTabs(); assert.equal(sheets.Team.getLastRow(), 2); assert.equal(sheets.Team.rows[1][0], 'owner@northstar.example');
    const frozen = e.snapshot(); sheets.Activity_Log = null;
    assert.throws(() => c.vocWebImportRegisters(), /Activity_Log/); assert.equal(e.state.locked, false);
    assert.ok(frozen.includes('ACTION-001'));
    const malformed = new Sheet('bad', [['Case ID','Case ID']]);
    assert.throws(() => c.vwSetupHeaders_(malformed, c.VOC_WEB_SETUP.TABS.Follow_Up_Cases), /duplicate/);
  },
  edits() {
    const e = fixture(); const {c, sheets, state} = e;
    function rejected(req, kind) {const before=e.snapshot(); const out=e.save(req); assert.equal(out.ok,false); assert.equal(out.error.kind,kind); assert.equal(e.snapshot(),before); assert.equal(state.locked,false);}
    rejected(e.request('setCaseOwner',{owner:'Next owner'},{expect:''}),'stale');
    rejected(e.request('setCaseOwner',{owner:'Next owner'},{expect:'old'}),'stale');
    rejected(e.request('setCaseOwner',{owner:'Next owner'},{note:''}),'invalid');
    rejected({action:'constructor'},'invalid');
    state.denied=true; rejected(e.request('setCaseOwner',{owner:'Next owner'}),'denied'); state.denied=false;
    state.busy=true; rejected(e.request('setCaseOwner',{owner:'Next owner'}),'busy'); state.busy=false;
    rejected(e.request('setCaseStatus',{outcome:'Resolved'}),'invalid');
    rejected(e.request('setCaseStatus',{outcome:'Resolved confirmed'}),'invalid');
    rejected(e.request('setCaseStatus',{delivery:'Plan agreed'}),'invalid');
    rejected(e.request('setActionStatus',{status:'Done'}),'invalid');
    rejected(e.request('logUpdate',{status:'Sent'}),'invalid');
    const audit=sheets.Activity_Log; delete sheets.Activity_Log;
    rejected(e.request('setCaseOwner',{owner:'Next owner'}),'setup'); sheets.Activity_Log=audit;
    const sh=sheets.Follow_Up_Cases, ownerCol=c.VOC_WEB_SETUP.TABS.Follow_Up_Cases.headers.indexOf('Owner')+1;
    sh.formulas[`5:${ownerCol}`]='=SOMEFORMULA()'; rejected(e.request('setCaseOwner',{owner:'Next owner'}),'setup'); sh.formulas={};
    const req=e.request('setCaseOwner',{owner:'Next owner',accepted:true}); const out=e.save(req);
    assert.equal(out.ok,true); assert.equal(out.changed,3); assert.equal(out.data.cases[0].Owner,'Next owner');
    assert.equal(sheets.Activity_Log.getLastRow(),7); assert.ok(state.calls.includes('setCaseOwner'));
    rejected(req,'stale');
    const noChange=e.save(e.request('setCaseOwner',{owner:'Next owner'})); assert.equal(noChange.changed,0); assert.equal(sheets.Activity_Log.getLastRow(),7);
    state.viewer=''; rejected(e.request('setCaseOwner',{owner:'Typed'},{actorName:'   '}),'name');
    const literal=e.save(e.request('setCaseOwner',{owner:' =1+1'},{actorName:'Northstar operator'})); assert.ok(literal.ok);
    assert.equal(c.vocWebReadTab_('Follow_Up_Cases').rows[0].Owner,'=1+1');
    const lastLog=sheets.Activity_Log.rows.at(-1); assert.equal(lastLog[2],'Northstar operator (name entered in app)');
    // All five action paths reach the real server endpoint.
    assert.ok(e.save(e.request('setCaseStatus',{admin:'Waiting'},{actorName:'Northstar operator'})).ok);
    assert.ok(e.save(e.request('setActionStatus',{status:'Done',evidence:'Synthetic proof'},{actorName:'Northstar operator'})).ok);
    assert.ok(e.save(e.request('logUpdate',{status:'Sent',evidence:'Synthetic delivery'},{actorName:'Northstar operator'})).ok);
    assert.ok(e.save(e.request('decideChange',{decision:'Investigate',rationale:'Synthetic review'},{actorName:'Northstar operator'})).ok);
    const logIds=sheets.Activity_Log.rows.slice(4).map(r=>r[0]); assert.equal(new Set(logIds).size,logIds.length);
    const duplicate=clone(sheets.Follow_Up_Cases.rows[4]); sheets.Follow_Up_Cases.rows.push(duplicate);
    rejected(e.request('setCaseOwner',{owner:'Other'},{actorName:'Northstar operator'}),'invalid');
  },
  transport() {
    const value={missing:null, zero:0, empty:'', nested:{unknown:null}, at:'2026-10-18T12:00:00+00:00'};
    // Deliberately lossy mock reproduces the observed transport symptom for objects.
    const lossy = v => typeof v === 'string' ? v : JSON.parse(JSON.stringify(v, (_,x) => x === null ? undefined : x));
    assert.equal(lossy(value).missing,undefined);
    assert.deepEqual(JSON.parse(lossy(JSON.stringify(value))),value);
    const rpc = value => {
      if (value instanceof Date || (value && typeof value === 'object' && Object.values(value).some(v => v instanceof Date))) throw Error('Date is not an RPC value');
      return lossy(value);
    };
    assert.throws(() => rpc({at:new Date()}), /Date/);
    assert.deepEqual(JSON.parse(rpc(JSON.stringify(value))),value);
    const e=fixture(); assert.equal(typeof e.c.vocWebSave(JSON.stringify(e.request('setCaseOwner',{owner:'New owner'}))), 'string');
  },
  async drawer() {
    const e=fixture(); e.state.viewer='';
    const listeners={}, stored={}, drawers=[]; let loaded, confirmed=true;
    const db=Object.fromEntries(['Follow_Up_Cases','Case_Actions','Customer_Updates','Change_Register'].map(n=>[n,e.c.vocWebReadTab_(n).rows]));
    const D={toD:v=>new Date(v),isUnknown:v=>!v,changes: db=>db.Change_Register.map(r=>({id:r['Change ID'],state:r.State,r}))};
    const esc=v=>String(v??'').replaceAll('&','&amp;').replaceAll('"','&quot;').replaceAll('<','&lt;');
    const U={esc,icon:()=>'',status:esc,lifecycle:esc,toast:()=>{},drawer:{open:html=>drawers.push(html),close:()=>{}}};
    // Asynchronous stand-in for the actual google.script.run transport.
    const google={script:{run:{withSuccessHandler(success){return {withFailureHandler(failure){return {vocWebSave(json){queueMicrotask(()=>{try{success(e.c.vocWebSave(json));}catch(error){failure(error);}});}};}};}}}};
    const window={UI:U,APP_CONFIG:{instance:{timezone:'UTC',key:'northstar-synthetic'}},Derive:D,confirm:()=>confirmed,
      Data:{meta:()=>({canEdit:true,viewer:e.state.viewer,vocab:e.c.VW_VOCAB,people:[]}),save:req=>new Promise((resolve,reject)=>google.script.run.withSuccessHandler(json=>{const res=JSON.parse(json);resolve({...res,loaded:res.data});}).withFailureHandler(reject).vocWebSave(JSON.stringify(req)))},__s2cSetLoaded:value=>{loaded=value;}};
    const browser=vm.createContext({window,document:{addEventListener:(n,f)=>listeners[n]=f},localStorage:{getItem:k=>stored[k],setItem:(k,v)=>stored[k]=v},Date,Intl});
    vm.runInContext(asset('Edit.html').replace(/^<script>\s*/,'').replace(/<\/script>\s*$/,''),browser);
    const context={D,db};
    for (const [action,id] of [['decideChange','CHANGE-001'],['setCaseOwner','CASE-001'],['setCaseStatus','CASE-001'],['setActionStatus','ACTION-001'],['logUpdate','UPDATE-001']]) {
      window.Edit.open(action,id,null,context); assert.ok(drawers.at(-1).includes(`data-action="${action}"`)); assert.ok(drawers.at(-1).includes('name="actorName"'));
    }
    const error={hidden:true,textContent:'',innerHTML:''},button={disabled:false,lastChild:{textContent:'Save'}};
    const req=e.request('setCaseOwner',{owner:'Drawer owner'});
    const input=(name,value)=>({name,value,type:'text',hasAttribute:()=>false});
    const inputs=[input('owner','Drawer owner'),input('note','Synthetic drawer reason'),input('actorName','')];
    const form={dataset:{action:req.action,id:req.id,expect:req.expect},querySelectorAll:()=>inputs,querySelector:s=>s==='.ef-err'?error:s==='button[type=submit]'?button:s==='[name=actorName]'?inputs[2]:null};
    const event={target:{closest:()=>form},preventDefault:()=>{}};
    listeners.submit(event); assert.equal(error.textContent,'Please enter your name.');
    inputs[2].value='Northstar operator'; confirmed=false; listeners.submit(event); assert.equal(e.c.vocWebReadTab_('Follow_Up_Cases').rows[0].Owner,'Intake owner');
    confirmed=true; listeners.submit(event); await new Promise(resolve=>setImmediate(resolve));
    assert.equal(loaded.cases[0].Owner,'Drawer owner'); assert.equal(stored['s2c.actorName.northstar-synthetic'],'Northstar operator');
    listeners.submit(event); await new Promise(resolve=>setImmediate(resolve)); assert.ok(error.innerHTML.includes('Refresh now'));
    window.Data.save=async()=>{throw Error('Network');}; listeners.submit(event); await new Promise(resolve=>setImmediate(resolve)); assert.ok(error.textContent.includes('could not be confirmed'));
  },
};
Promise.resolve().then(()=>cases[process.argv[2]]()).then(()=>console.log(`PASS: ${process.argv[2]}`)).catch(error=>{console.error(error);process.exitCode=1;});
