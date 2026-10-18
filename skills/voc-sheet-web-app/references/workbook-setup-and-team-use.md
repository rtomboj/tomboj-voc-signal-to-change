# One workbook, setup, and team use

Use the workbook Step 2's monitor is bound to as the default record. Keep Step 1/2 tabs, formulas, IDs and triggers intact. Step 3/4 registers become tabs in that workbook: `Follow_Up_Cases`, `Case_Actions`, `Customer_Updates`, `Change_Register`, and `Change_Case_Links`. Keep `Data Class` on each register; the default import selects REAL rows only. Separate source files remain preserved originals, not competing editable registers after cutover.

## Setup and import order

1. Inspect all source files/tabs and header rows (often 1 or 4); resolve missing/duplicate keys and ambiguous headers. Back up the workbook and source first. Confirm the one-workbook target and import class.
2. Adapt [VocWebSetup.gs](../assets/apps-script/VocWebSetup.gs) in the bound project's editor. Its `IMPORT` map is intentionally blank; privately fill only confirmed source IDs. The reference reads the first sheet in each source file: if the register is elsewhere, adapt that selection explicitly before importing. Do not publish IDs. New tabs use header row 4; existing tabs are preserved and mismatches reported.
3. Save and run **`vocWebSetupTabs`** once from the editor. It creates missing register, Team and Activity_Log tabs, and seeds the setup account only when a compatible Team tab is empty. Inspect the structured CREATED/EXISTS/missing-header report. It does not migrate existing schemas or create triggers. Resolve mismatches before continuing.
4. If separate registers exist, pause app writes/direct register edits, set the private import map and run **`vocWebImportRegisters`**. It imports the chosen class, appends source-only trailing fields, skips existing stable keys (composite Change ID + Case ID for links), and logs imports. Conflicting duplicate keys require reconciliation; skipping is not proof of equality. Unknown/missing Data Class rows are excluded from a REAL import and need review.
5. Run setup and import again on the test copy. Expect unchanged cell contents, row/tab counts, and audit rows; report counts as INFO. Reconcile source/destination IDs and class counts. Choose the destination as authoritative before resuming writes. Clear the private import map after cutover.
6. Complete web configuration, public authorized **`vocWebSelfTest()`**, read/permission checks, then edit checks in the [installation path](installation-and-reauthorization.md). These references are patterns to adapt, not an installable finished site.

Setup runs in the bound project; web writes run in the standalone web project for a team. Locks are scoped to their project and do **not** coordinate these two projects or direct human Sheet edits. Finish imports before enabling writes; thereafter use one web writer project and protect operational register tabs. A future importer must use that same writer/lock or a deliberate maintenance pause. Never claim a document lock and script lock provide cross-project exclusion.

## Team and activity tables

| Tab | Headers and meaning |
| --- | --- |
| Team | `Email`, `Name`, `Role`, `Can Decide Changes`, `Can Own Cases`, `Active`, `Added At`, `Notes`. Active = Yes admits a verified member in team mode. Capabilities use Yes/No. Keep this owner-maintained; a role label alone grants nothing. |
| Activity_Log | `Log ID`, `Timestamp`, `User`, `Action`, `Tab`, `Record ID`, `Field`, `Old Value`, `New Value`, `Reason`, `Source`, `App Version`. Append-only: one row per changed field, and one per imported record. Use ISO timestamps with an offset in the workbook timezone. Map older timestamp headers rather than renaming existing columns. |

Choose application `ACCESS_MODE = 'open'` or `'team'` once and keep the choice server-side. Open is the simple model when the user chooses it: everyone admitted by the deployment may use all five edit actions. Google deployment access remains the gate; open does not mean anonymous publication. Team requires verified caller identity, a unique active Team row and action capability checks (`Can Decide Changes` for decisions, `Can Own Cases` for the remaining edits). Fail closed on blank/duplicate identity. A private Script Property such as `VOC_WEB_VIEWER_EMAILS` may explicitly override the viewer allowlist; it never bypasses verified identity or assigns edit permissions. Do not return this property to the browser. Document and test the exact override semantics in the generated authorization helper.

The owner picker tries the Workspace directory (optional People advanced service and reviewed scopes), then active Team members with Can Own Cases = Yes, then owners already used in the authorized registers, then typed names. Directory failure is nonfatal; manual entry always works. Suggestions are not permission or proof of owner acceptance. Filter suggestions to the approved audience and deduplicate them; do not expose an entire directory unnecessarily.

## Phased use and access

Start read-only, then enable owner writes after setup and the read gate, then team use on Workspace with a standalone web project opening the same workbook by server-configured ID. The monitor stays bound; never copy its public setup/trigger/notification functions into the web project. Protect register, Team and Activity_Log tabs against direct team edits while retaining deployer authority. If executing as the accessing user, their Sheet permissions must support the chosen design; do not promise protected writes without verifying it.

A personal Google account defaults to **Only myself**. It lacks a Workspace organization boundary and may not disclose other callers' emails in a deployer-executed app. An explicitly chosen wider open pilot uses entered names as unverified attribution: ask once, remember only that label in instance-scoped browser storage, and log `Name (name entered in app)`. Never substitute the deployer as caller. Blank identity blocks team mode. Record the actual audience and test it; an open personal pilot is not a verified team deployment.

## Write rules and reference integration

Adapt [VocWebWrite.gs](../assets/apps-script/VocWebWrite.gs) and [Edit.html](../assets/apps-script/Edit.html) after the actual design contract. They preserve the supplied five-action pattern: `decideChange`, `setCaseOwner`, `setCaseStatus`, `setActionStatus`, `logUpdate`. Step 1/2 tabs and customer sending are outside that allowlist. Changes to records are human assertions with evidence, never automatic business decisions.

Each save needs an explicit confirmation and reason, server authorization, per-action writable fields, repository vocabulary/evidence validation, a stable unique key and mandatory row fingerprint of current values. Under `LockService.getScriptLock()`, re-read by key, reject duplicate keys/stale values, preflight writable headers and the audit table, write only changed cells, append Activity_Log per field, and return the refreshed authorized JSON view. Escape formula-like text in registers **and every log field**. Protect formula cells; direct register edits must be paused or routed through the same writer. Sheet writes and audit appends are not transactional: retain a backup, report possible partial writes with a trace, and reconcile after failure rather than retrying blindly.

Use the [Step 3 evidence gates](../../voc-customer-follow-up/references/registers-and-closure.md) and [Step 4 lifecycle gates](../../voc-systemic-change/references/registers-and-verification.md). Evidence presence does not establish truth or authority. The pattern blocks common missing-evidence cases; the generated adapter must implement the full approved transition/closure/merge rules for the mapped system before enabling those controls. Reject/disable an action whose required evidence cannot be established. A merge must preserve case/update obligations, not just set a state.

The supplied references intentionally depend on the adapted app; generate these dependencies in full before owner installation:

| Reference dependency | Required contract |
| --- | --- |
| `VOC_WEB` | Server-only VERSION and TZ from the configured workbook; no hard-coded company, email, or ID. |
| `vocWebAuthorize_(action)` | Returns verified caller email, or blank only for deliberately open access. Enforces open/team policy, Team/override membership and per-action capability on every call; never trusts actorName. |
| `vocWebBenchmarkId_()` | Fixed private workbook ID; never obtained from client input. |
| `vocWebReadTab_(name, options)` | Allowlisted mapped tabs; `{state, reason, headers, headerRow, rows}`. Each row carries `_class`, physical `_row`, and `_v`: a deterministic fingerprint of stable key plus **all mapped values**, including blank fields and formula content where relevant. Dates normalized before hashing; duplicate keys rejected. No filtering that hides dependencies needed for evidence validation. |
| `vocWebBuildViewModel_(now)` | Authorized/redacted fresh view with `meta`, `meta.vocab`, `meta.people`, `meta.viewer`, `meta.canEdit`, `meta.editBlockedReason`; REAL-only policy enforced before row payloads. Return current row fingerprints; do not compute them in the browser. |
| `vocWebSafeMessage_(error)` | Redacts private IDs, values, contacts and property contents in server diagnostics. |
| `window.APP_CONFIG`, `window.Data` | Config provides `instance.timezone` and a nonsecret `instance.key` for local name storage. `Data.meta()` and `Data.save(request)` adapt the server view; save wraps google.script.run with success/failure handlers, JSON.stringify request/JSON.parse response, and returns `{ok, error, message, loaded}`. `loaded` is the refreshed adapter state from `response.data`. |
| `window.UI`, `window.Derive`, context `c` | UI supplies escaping, toast, icon/status/lifecycle helpers and drawer open/close; Derive supplies date parsing and mapped selectors (`c.D`, `c.db`). `window.__s2cSetLoaded(loaded)` refreshes the render. Provide edit button handlers calling `Edit.open(kind, id, preset, c)` and matching drawer styles. Load Edit after these dependencies. |

Keep [acceptance evidence](acceptance-and-deployment.md) separate for local stubs, browser tests, Google editor, deployed permissions and actual team use. A synthetic harness can verify the real endpoint's behavior; it cannot establish Google identity or deployment settings.
