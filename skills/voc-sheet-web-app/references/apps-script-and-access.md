# Apps Script integration and organization access

Consult current official documentation when implementing. The links in ATTRIBUTIONS.md were checked October 16, 2026. Generate code for the user's actual environment, not a universal server pasted into every Sheet.

## Web execution

Serve the interface through HTML Service and one existing/new doGet entry point. Convert a bundled prototype into maintainable HTML/JS/style partials as needed. Use trusted partial inclusion; do not expose a generic server function that includes arbitrary files requested by the browser.

Use the server-side business-logic default and conversion checklist in [design contract and conversion](design-contract-and-conversion.md). Follow the exact file/paste sequence in [installation and reauthorization](installation-and-reauthorization.md), including font/CDN checks under HTML Service and editor consent for affected trigger owners before relying on unattended execution.

Bound-script active-document methods are not available in web-app execution. Use a fixed, server-configured workbook reference with explicit access and verify it in the deployed context. Store the target ID using the existing server configuration convention or Script Properties. Never accept an arbitrary client workbook ID or a browser-selected cell/range.

The supplied monitor may use spreadsheets.currentonly and @OnlyCurrentDoc. Explicit workbook access may need a different Sheets scope. Confirm the required scope from current documentation and actual test behavior; explain the additive scope change rather than replacing the whole manifest or asserting the old scope is sufficient. Preserve existing dependencies, timezone, runtime, advanced services, and unrelated scopes. Do not request full Drive access merely to read a known Sheet.

Return `JSON.stringify(viewModel)` from read and save endpoints and `JSON.parse` in the client's success handler. Normalize Sheet Date cells to ISO 8601 text with an explicit offset in the configured workbook timezone before serialization; revive only contracted date fields. Test missing, null, zero and empty values explicitly. The live run observed lost/null fields; this JSON envelope is a defensive convention, not a claim that Google prohibits null (see [RPC types](https://developers.google.com/apps-script/guides/html/communication)). Dates are not legal RPC values.

Do not use `<base target="_top">` with in-page routing. Intercept internal route links inside the iframe; use reviewed external links with `target="_blank"` and `rel="noopener noreferrer"`. Put the app version in the footer so screenshots identify the deployed build.

Use selected fields and bounded row counts or pagination for large tables. A refresh should read data, not run monitoring, install triggers, send digests, or change statuses. Keep mutations separate from reads.

## Public callable surface

Inspect every global function, including existing monitor/setup/test/trigger functions. Hiding buttons does not prevent direct google.script.run calls to public server functions. A helper ending with an underscore is not callable through that interface, but do not rename a trigger handler and break its schedule without a tested migration.

For any audience beyond the owner, the default is a standalone web project opening the workbook by ID. Keep bound monitor/setup public functions out of that project; hiding buttons cannot isolate them. Protect register tabs from direct team edits while retaining the deployer's write access. For each callable function, record purpose, role/identity requirement, side effects, and enforcement. Guard both new and existing sensitive entry points. Do not pass a "trusted trigger" flag from the client or trust a forged role/email parameter. Preserve scheduled execution with a design tested under the maintainer account. An owner-only same-project pilot still requires the complete callable-surface audit.

After the read-only gate and setup, integrate the standard five actions through [VocWebWrite.gs](../assets/apps-script/VocWebWrite.gs) and [Edit.html](../assets/apps-script/Edit.html); see their required adapters in [workbook setup and team use](workbook-setup-and-team-use.md). Use one action allowlist and per-action fields, repository status/evidence gates, mandatory key + row fingerprint, a script lock, changed-cells-only writes and one Activity_Log row per changed field. Confirm with a reason; treat formula-like values as literal text in both registers and logs. Return a refreshed, authorized JSON view. Never write Step 1/2 tabs or send customer messages. A log failure or partial write must be reported as needing reconciliation, never as "nothing changed".

Choose `open` or `team` once. In open mode deployment access is the gate, without application roles. In team mode require verified caller email, Active = Yes and the appropriate Team capability for every read/write; a Script Property allowlist override may replace viewer membership but must not invent write permissions. Never trust a browser role or actor name as authorization.

When caller email is unavailable in an explicitly open pilot, ask for a name once and remember it in that browser, scoped to the instance. Log `Name (name entered in app)`; it is an attribution label, not verified identity. Never substitute the deployer's effective-user email. In team mode, blank verified identity denies access.

## Deployment policy

Target webapp access DOMAIN: the deploying Workspace domain. ANYONE allows any signed-in Google user; ANYONE_ANONYMOUS permits anonymous users. Neither meets an organization-only requirement. Domain availability and admin restrictions must be checked in the actual account. Personal accounts default to an Only myself pilot. Any explicitly chosen wider open pilot must be labelled with its actual audience; the application mode `open` does not itself change Google deployment access. Do not equate a custom email address with an eligible Workspace tenant.

Record the execution choice separately:

| Identity | Consequence | Needed check |
| --- | --- | --- |
| USER_ACCESSING | Server runs with each viewer's authority | Each viewer has required Sheet permissions/scopes; unauthorized data remains inaccessible |
| USER_DEPLOYING | Server uses deployer's authority | Data audience is intentionally broader if applicable; server-side caller authorization/redaction works and does not assume deployer identity is the viewer |

Do not use effective-user identity as caller identity in a deployer-executed app. Session identity can be unavailable in some contexts. If a verified identity is necessary to authorize the request and is unavailable, deny that request. Do not fall back to the deployer's identity or a client-provided address.

The organization boundary is a deployment setting, not a label in the UI, a hidden URL, a query-string password, or a client email-suffix check. Additional roles or allowlists belong on the server. For restricted users, omit fields/rows from the response itself; inspect network payloads during tests.

Keep access tokens, credentials, internal property values, and unnecessary personal information out of HTML, browser logs, and error messages. Return useful redacted errors with a trace reference when available.
