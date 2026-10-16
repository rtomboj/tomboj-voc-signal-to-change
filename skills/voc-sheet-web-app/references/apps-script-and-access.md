# Apps Script integration and organization access

Consult current official documentation when implementing. The links in ATTRIBUTIONS.md were checked October 16, 2026. Generate code for the user's actual environment, not a universal server pasted into every Sheet.

## Web execution

Serve the interface through HTML Service and one existing/new doGet entry point. Convert a bundled prototype into maintainable HTML/JS/style partials as needed. Use trusted partial inclusion; do not expose a generic server function that includes arbitrary files requested by the browser.

Bound-script active-document methods are not available in web-app execution. Use a fixed, server-configured workbook reference with explicit access and verify it in the deployed context. Store the target ID using the existing server configuration convention or Script Properties. Never accept an arbitrary client workbook ID or a browser-selected cell/range.

The supplied monitor may use spreadsheets.currentonly and @OnlyCurrentDoc. Explicit workbook access may need a different Sheets scope. Confirm the required scope from current documentation and actual test behavior; explain the additive scope change rather than replacing the whole manifest or asserting the old scope is sufficient. Preserve existing dependencies, timezone, runtime, advanced services, and unrelated scopes. Do not request full Drive access merely to read a known Sheet.

Return JSON-compatible objects, arrays, strings, numbers, booleans, and null. Serialize Date values explicitly before returning getValues results through google.script.run. Normalize dates consistently to the workbook's timezone and preserve timestamp offsets where needed.

Use selected fields and bounded row counts or pagination for large tables. A refresh should read data, not run monitoring, install triggers, send digests, or change statuses. Keep mutations separate from reads.

## Public callable surface

Inspect every global function, including existing monitor/setup/test/trigger functions. Hiding buttons does not prevent direct google.script.run calls to public server functions. A helper ending with an underscore is not callable through that interface, but do not rename a trigger handler and break its schedule without a tested migration.

For each callable function, record purpose, role/identity requirement, side effects, and enforcement. Guard both new and existing sensitive entry points. Do not pass a "trusted trigger" flag from the client or trust a forged role/email parameter. Preserve scheduled execution with a design tested under the maintainer account. If same-project exposure cannot be contained without disrupting working automation, explain that blocker and propose an isolated web project reading the same Sheet.

If editing is requested, validate writable fields/status transitions server-side, use stable IDs rather than row numbers, check current state/version to detect stale edits, lock shared writes, and log actor, timestamp, previous/new state, and reason in the existing audit system or a specifically approved additive log. Treat spreadsheet input beginning with formula syntax as literal data unless a formula is explicitly intended. Authorization to view is not authorization to send customer messages or change triggers.

## Deployment policy

Target webapp access DOMAIN: the deploying Workspace domain. ANYONE allows any signed-in Google user; ANYONE_ANONYMOUS permits anonymous users. Neither meets an organization-only requirement. Domain availability and admin restrictions must be checked in the actual account. Do not equate a custom email address with an eligible Workspace tenant.

Record the execution choice separately:

| Identity | Consequence | Needed check |
| --- | --- | --- |
| USER_ACCESSING | Server runs with each viewer's authority | Each viewer has required Sheet permissions/scopes; unauthorized data remains inaccessible |
| USER_DEPLOYING | Server uses deployer's authority | Data audience is intentionally broader if applicable; server-side caller authorization/redaction works and does not assume deployer identity is the viewer |

Do not use effective-user identity as caller identity in a deployer-executed app. Session identity can be unavailable in some contexts. If a verified identity is necessary to authorize the request and is unavailable, deny that request. Do not fall back to the deployer's identity or a client-provided address.

The organization boundary is a deployment setting, not a label in the UI, a hidden URL, a query-string password, or a client email-suffix check. Additional roles or allowlists belong on the server. For restricted users, omit fields/rows from the response itself; inspect network payloads during tests.

Keep access tokens, credentials, internal property values, and unnecessary personal information out of HTML, browser logs, and error messages. Return useful redacted errors with a trace reference when available.
