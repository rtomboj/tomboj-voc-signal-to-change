# Apps Script delivery and test sequence

Use this reference after the source plan is confirmed and before generating a Google Sheets setup.

Before selecting services, OAuth scopes, or an optional model API, consult [apps-script-workspace-capabilities.md](apps-script-workspace-capabilities.md). Prefer built-in services for straightforward operations, an Advanced Google service when its API adds a needed capability, and `UrlFetchApp` for an external endpoint. Google authorization and provider API keys are separate credentials.

The [Drive intake example](../examples/drive-intake/README.md) handles only the initial Excel-to-Sheets copy. It does not collect reviews or replace the source-specific monitor.

## Choose the script design

Prefer a container-bound Apps Script opened from the user's working Google Sheet. It can address the parent spreadsheet without storing a copied Sheet ID. For a standalone script or a different workbook, use the ID privately in the user's generated code. Never publish customer-specific Sheet URLs, IDs, review text, or generated code in this repository.

Use official source APIs, feeds, exports, notifications, or manual capture. A generic HTTP request does not create permission to collect from a website or make its layout stable. Use one source adapter per approved automated source. Leave unsupported sources manual, on a watchlist, deferred, or excluded.

## Prepare the workbook safely

Create a dated backup of the converted Google Sheet before setup. The .xlsx and Markdown Part 1 outputs remain the frozen benchmark. Check important formulas, validation, charts, and formatting because Excel conversion may change them.

If editing is authorized, add missing tabs and headers only. Setup must be idempotent: rerunning it cannot clear existing rows, duplicate tabs, alter Part 1 headers, or overwrite the benchmark dashboard.

If no authorized Sheets connection is available, provide:
- an idempotent setup function;
- a manual tab/header checklist;
- instructions to use a backup or test copy first.

Do not create a time-driven trigger while preparing the workbook.

## Generate the code package

Deliver complete user-specific files, not fragments. A small pilot may use one or two files; a larger project may separate:

- `Config.gs`: confirmed source plan, cadence, fields, and alert choices;
- `SourceAdapters.gs`: approved retrieval/parsing per source;
- `ReviewStore.gs`: schema mapping, ID origin, deduplication, append/update;
- `Classification.gs`: confirmed deterministic rules or optional AI;
- `Alerts.gs`: test and operational email/Chat notices;
- `ManualCapture.gs`: manual capture, due checks, and reminders;
- `TriggerSetup.gs`: explicit trigger creation/removal;
- `TestRunner.gs`: fixtures and a `runAllTests()` entry point;
- `MonitorDashboard.gs`: only after the monitoring test gate passes;
- `Dashboard.html`: only if the user selects a custom interface.

Include a README or manifest listing files, function names, scopes, configuration values, and expected outputs. Do not place secrets in code or Sheet cells.

### Optional frontier model connection

Deterministic collection, deduplication, measures, and notification do not need an LLM key. AI is optional and has a recurring token/API cost if scheduled. Default to no recurring AI; allow setup-time assistance or a user-requested one-off summary.

If the user opts in, state what text/data will leave Google, the provider, expected per-run volume and cost, retention/data-use assumptions, and the budget/disable path. Keep the provider key out of source control, cells, logs, and alerts. Apps Script `UserProperties` are per user; `ScriptProperties` are available to users of the script and should not be presented as a private secret store. For shared/team credentials, a controlled service such as Google Cloud Secret Manager is an option but adds Cloud project, IAM, and API setup. Use the [Properties Service](https://developers.google.com/apps-script/guides/properties) and appropriate provider documentation to select storage. The scheduled trigger runs as its creator, so user-scoped credentials must belong to the trigger owner.

## Test before scheduling

Provide a `TEST_MODE` and `runAllTests()` using fixture records and an isolated test copy/tab, with results written to `Test_Results`. Test runs must not change production rows or alert real recipients. Until the user runs tests in their Google account and returns results, report live Google authorization, collection, trigger execution, email, and Chat delivery as **not run**.

Use fixtures first. Use a permitted live-source check only after the route and access are confirmed. Test each source separately. Required cases:

1. Part 1 rows and records at/before baseline date do not trigger historical alerts.
2. Synthetic/unknown IDs are captured in a fresh baseline before monitoring begins.
3. One new ID appends once; the same ID is skipped on recheck.
4. Source ID plus ID Origin distinguish records; canonical syndicated copies count once.
5. Edited records follow the agreed update/change-log rule.
6. Positive and negative individual signals remain separate from trend counts.
7. An individual high-impact signal can prompt review without being labeled representative or a trend.
8. Evidence class and audience filters/counts remain distinct.
9. Wrong-entity/out-of-scope data is held for review or excluded.
10. Manual capture enters the same pipeline; overdue manual checks are visible.
11. Failed, partial, and stale checks are visible, preserve the last success, and never look like no feedback.
12. Test notifications route only to test recipients and expose minimal necessary text.
13. Simultaneous executions cannot write duplicate rows (use a script-level lock).
14. Repeated trigger setup by the same user does not duplicate that user's trigger.
15. A missing/ambiguous trigger owner is handled as setup-needed, not reported as a healthy schedule.
16. Quota/time-limit errors are logged and do not erase the last successful state.

Report each case as passed, failed, partially tested, blocked, or not run. The assistant cannot run a user's live Google Apps Script environment; wait for their test output before claiming the gate passed or writing the dashboard builder.

## Authorization and trigger setup

Show a clear click path: open the converted Sheet → **Extensions → Apps Script** → add the provided files → save → run the documented initialization on the backup/test copy → review and approve the requested scopes → run manual tests.

Explain which account will run the continuing monitor. Installable time-driven triggers execute using the authorization of the account that created them. Have that maintainer run trigger setup after tests pass. Keep the maintainer role and account recorded in the monitor notes/config so ownership can be transferred deliberately.

Make trigger setup explicit and reversible. It should check for duplicates visible to the current user, create a single trigger for the confirmed cadence, and provide a remove/reset function that does not touch source data. Apps Script only returns project triggers associated with the current user; setup cannot inspect or remove a trigger created by another collaborator. Do not report another account's trigger owner or promise to detect cross-account duplicates. Before changing maintainership, have each current maintainer inspect their own triggers and remove their own obsolete one. Time-driven triggers run within a time window, not necessarily at an exact minute.

Use a script lock around collection and write operations. If another run holds the lock, skip or defer cleanly and log the result; never run two overlapping writes.

Add self-health to the monitor data and dashboard: last successful check, next due/overdue status, last error, and last alert attempt. Use formulas/conditional formatting or a separate monitoring view so failure is visible even if a trigger stops. Provide a periodic human check as a backup. Do not claim the script can alert after the script itself is unable to execute.

Use least-privilege OAuth scopes. Use `@OnlyCurrentDoc` only when the design truly needs only the bound file and the annotation is compatible with every requested service. Explain that the Drive intake example uses a broader Drive scope because it searches/converts Drive files. Quotas and account limits can change; check Google's [quota page](https://developers.google.com/apps-script/guides/services/quotas) for the selected account and APIs before rollout. Do not promise a cadence a source or quota cannot sustain.

## Build and validate the dashboard

Only after the user returns successful monitoring test results, generate a separate `Monitor_Dashboard` builder. Preserve Part 1's `Executive_Dashboard`. Use a native Sheet by default; add HTML only if chosen.

Validate that:
- totals reconcile with monitoring data by source and time window;
- rating scales, audiences, and evidence classes are not combined;
- positive and negative movement are visible;
- individual signals, possible patterns, and reviewed sustained changes have separate labels;
- failure, overdue, and stale status cannot appear as zero feedback;
- evidence window, denominator, volume floor, and coverage gaps are clear;
- no measure ranks individuals or claims causality without evidence.

## Official implementation references

- [Installable triggers](https://developers.google.com/apps-script/guides/triggers/installable)
- [Apps Script Script service](https://developers.google.com/apps-script/reference/script/script-app)
- [LockService](https://developers.google.com/apps-script/reference/lock/lock-service)
- [Properties Service](https://developers.google.com/apps-script/guides/properties)
- [OAuth authorization](https://developers.google.com/apps-script/guides/services/authorization)
- [Apps Script quotas](https://developers.google.com/apps-script/guides/services/quotas)
