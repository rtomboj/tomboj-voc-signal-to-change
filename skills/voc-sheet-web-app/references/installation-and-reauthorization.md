# One installation path and trigger-safe reauthorization

Use this path for connected edits and manual pasting. Choose and record the exact target/version and file manifest once. Do not present several competing layouts or tell a user to install a generic starter before the adapted files.

## Before touching the project

1. Finish design intake and the design data-contract check. Preserve a private snapshot of current source, manifest, properties' names, deployment version and visible trigger inventory. Inspect existing globals and entry points; identify owners whose triggers may not be visible.
2. Bind the generated configuration to the test workbook. A copied Sheet is not proof that script properties, deployments or triggers have been copied; inspect each separately. Do not install production schedules or send notifications in the test copy.
3. Produce one exact filename/type/add-or-patch/paste-order table. Use the layout below by default. Resolve filename, global-function and property-name collisions first; freeze the substituted names and update every include/call consistently. Existing doGet requires a precise inspected router patch, not another global doGet.
4. Show a before/after scope report **before pasting code**. Cover explicit oauthScopes, automatic scope inference and `@OnlyCurrentDoc`. New code can change inferred scopes without a manifest edit. Explain every added scope; preserve unrelated scopes, timezone, services and runtime. Check current Google documentation for the actual APIs used. Do not broaden Drive access just to read a known Sheet.
5. If scope requirements change, flag that existing unattended trigger executions cannot present consent dialogs. Arrange editor reauthorization by each relevant trigger creator before relying on that automation again. Mark unidentified/unavailable owners as a verification blocker. Never fix this by deleting/recreating triggers or by treating the deployer's consent as consent for all owners.

## Exact paste order

For owner-only setup, open the **intended test Sheet > Extensions > Apps Script**. For a non-owner audience, create the separate standalone web project and install only web files there; keep setup and monitoring in the bound project. Record both targets. In the editor, use **+ > Script** for GS and **+ > HTML** for HTML files. Enter the basename (for example `VocWebConfig` or `Styles`); the editor supplies `.gs` or `.html`. Do not create `Styles.html.html`. Reuse inspected existing files only through the listed patches. Do not delete existing Code.gs.

| Order | Exact default project filename | Type | Contents and constraints |
| --- | --- | --- | --- |
| 1 | `VocWebSetup.gs` | Script, bound project only | Adapt the [setup reference](../assets/apps-script/VocWebSetup.gs); blank IMPORT map by default. Run `vocWebSetupTabs` once on the test copy before web configuration. Optional import is a separate explicit editor action. |
| 2 | `VocWebConfig.gs` | Script, web project | Private config/access helpers and authorized public `vocWebSelfTest()` wrapper around private `vocWebSelfTest_()`. No setup at file load. |
| 3 | `VocWebData.gs` | Script | Authorized JSON reads, mapped schema and private view-model helpers; no side effects on read. |
| 4 | `VocWebWrite.gs` | Script | Adapted five-action endpoint plus fingerprint/evidence/audit integration; writes stay disabled until read checks pass. |
| 5 | `Styles.html` | HTML | Complete styles, including edit drawer styles and font fallbacks. |
| 6 | `App.html` | HTML | Asynchronous reads/saves, JSON parsing, rendering and drawer/data adapters. |
| 7 | `Edit.html` | HTML | Adapted drawer forms; load after App initializes its helpers. |
| 8 | `Index.html` | HTML | Shell with trusted Styles/App/Edit includes and loading/error states. |
| 9 | `VocWeb.gs` | Script | One entry point and private allowlisted includes; patch an existing router precisely. |
| 10, only if needed | `appsscript.json` | Existing manifest patch | Reviewed additive changes only; preserve existing fields/services. |

Supply every new file in full, plus exact inspected-source patches. Do not leave omitted helpers or placeholders in an installable batch. State file version and exact input/config values the owner must set privately. If a collision changes `vocWebSelfTest` or `vocWebSelfTest_` or any filename, state the resolved exact name everywhere; never ask the owner to guess. Complete all files and save before running anything. Paste order organizes the handoff; Apps Script shares GS globals, so it does not solve duplicate function definitions.

## Authorize and verify interactively

1. Provide a public, authorized, read-only **`vocWebSelfTest()`** wrapper that calls private `vocWebSelfTest_()`; select `vocWebSelfTest` in the editor Run menu. Underscore helpers are not editor Run-menu entry points. The public wrapper must enforce owner/test authority before calling the helper. It must inspect/read only the configured test workbook, serialize results, check required mappings/joins and selected derived values, and log a redacted structured report: target-match boolean, source/version, tabs/header rows, contract checks, unavailable features, as-of/timezone and failures. Do not log customer rows, credentials or private property values. Structural/contract checks are PASS or FAIL. Counts are run-specific INFO, never universal pass criteria: for example, 8 / 5 / 2 / 7 / 5 belongs only to a documented example run. Specify this run's expected reconciliation, not a generic "success" message.
2. Run it from the editor. If Google requests additional consent, have the relevant maintainer review the reported scope change and authorize. Compare actual granted/required scopes to the planned change. If consent is denied or blocked, preserve the checkpoint and diagnose; do not expand access as a workaround. Each accessing user may also need consent for a user-executed deployment.
3. Ask for the returned report/error. Label pasting as **installed-reported**, not tested. Check the actual output, fix affected files and repeat. Keep **generated**, **installed-reported**, **tested** and **deployed** distinct; supplied and installed-verified may add evidence without replacing those labels. Record tests as passed, failed, blocked or not run separately.
4. Where scopes affect an existing operational project, each relevant trigger creator must authorize from the editor in that project using an inspected, safe read-only function exercising the required services. A test-copy read does not authorize the production project. Do not run a digest/setup/monitor merely to get a consent prompt. If a required service cannot be exercised safely, state the block and agree a controlled check. Never request OAuth tokens or secret exports.
5. Continue with HTML Service/editor preview and web-context tests, then the existing private deployment/access tests. A local mock or editor read cannot establish hosted font/CDN loading, viewer permissions, or organization access. Compare server counts/queues to actual rows and check navigation preserves the selected data class.
6. Check trigger inventory remains unchanged and examine the next scheduled execution's result where available. A user can return sanitized execution status/time/error. Do not call it passed until evidence exists, and do not send test notifications to operational recipients. Record owner visibility limits and checks pending for other creators.

Return to the last failed checkpoint on errors rather than restarting the benchmark or re-pasting every unchanged file. For production promotion, refresh source/schema/version, repeat the scope/owner checks in the target project, then version the intended deployment. Preserve rollback to the prior source/manifest/deployment without changing trigger schedules. See [acceptance and deployment](acceptance-and-deployment.md) for the full permission matrix.
