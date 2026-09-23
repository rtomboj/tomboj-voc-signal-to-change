# Apps Script delivery and test sequence

Use this reference after the user confirms a source plan and permits a Google Sheets setup.

Before choosing services, scopes, or an optional model connection, consult [apps-script-workspace-capabilities.md](apps-script-workspace-capabilities.md). Prefer a built-in service for straightforward operations, use an Advanced Google service when its API adds a required capability, and use UrlFetchApp for an external model API or unsupported endpoint. Treat Google OAuth authorization and provider API keys as separate credentials.

The [Drive intake example](../examples/drive-intake/README.md) handles only the initial Excel-to-Sheets copy. It does not collect reviews or replace the source-specific monitoring files generated later in this workflow.

## Choose the script design

Prefer a container-bound Apps Script opened from the user's Google Sheet. It can address its parent spreadsheet without a copied ID. If using a standalone script or one script that writes to a different workbook, ask for the target Sheet URL and use its ID privately in the user's generated code. Do not place a user's Sheet URL, ID, credentials, or review data in the public repository.

Use official source APIs, feeds, exports, notifications, or manual input. A generic HTTP request service does not grant permission to collect from a website or guarantee that the source is stable. Do not bypass authentication, CAPTCHAs, paywalls, or platform restrictions. Document one source adapter per automated source. Leave unsupported sources as manual, deferred, or watchlist.

## Prepare the spreadsheet

If connected and the user authorizes edits, add missing tabs and headers to the designated Google Sheets working copy. Preserve Part 1 data and formulas. Make setup operations idempotent so rerunning them does not duplicate tabs, clear records, or overwrite user content.

If not connected, provide:

- the generated setup function for missing tabs and headers;
- a manual tab-and-header table as a fallback;
- instructions for making a backup copy before running it.

Do not create or activate time-driven triggers during workbook preparation.

## Generate the code package

Return complete, user-specific files, not fragments that require the user to invent missing logic. Split files when that improves readability. A typical project may include:

- Config.gs for selected sources, cadence, fields, and alert rules;
- SourceAdapters.gs for permitted retrieval and source-specific parsing;
- ReviewStore.gs for schema mapping, stable IDs, deduplication, inserts, and updates;
- Classification.gs for selected deterministic or optional AI classification;
- Alerts.gs for test and production email or configured chat notices;
- TriggerSetup.gs for an idempotent setup function to create the chosen trigger;
- TestRunner.gs for fixtures and checks;
- DashboardBuilder.gs only after the monitoring test gate passes;
- Dashboard.html only if the user chooses a custom Apps Script sidebar or web interface.

The file names may be simpler for a one-source pilot. Include a manifest or README listing each file, the function to run, requested permissions, configuration values, and expected result.

Do not include secrets in generated code or sheet cells. Put source credentials only in an approved private configuration location and explain who can access them. Use a test recipient and test mode before sending alerts to operational recipients.

## Authorization and triggers

Installable Apps Script triggers can run on a time-driven schedule and use the authorization of the account that created them. Explain that the person who will own the ongoing monitor must run the setup operation and approve the requested Google permissions. Do not create a trigger silently or promise that another user's trigger will run under the document owner's identity.

Provide a setup function that:

- checks whether the matching trigger already exists;
- creates only one trigger for the confirmed cadence;
- reports the trigger owner and next-run expectation;
- can remove or reset that trigger without changing source data.

Use the Google Apps Script trigger documentation and service quotas as current implementation references:

- https://developers.google.com/apps-script/guides/triggers/installable
- https://developers.google.com/apps-script/guides/services/external
- https://developers.google.com/apps-script/guides/services/quotas
- https://developers.google.com/apps-script/guides/services/authorization

Have the user run one manual check before enabling a schedule. If the project needs an external API credential, explain the required source-specific authorization and do not store the credential in a public code file.

## Test the monitor before building a dashboard

Use fixtures first, then a permitted live-source check where practical. Test each source separately. Do not send tests to live recipients.

Required cases:

1. Existing Part 1 rows remain unchanged and are not re-alerted on the baseline run.
2. A new stable ID creates exactly one Review_Data row.
3. A repeated ID is skipped as a duplicate.
4. An edited existing record follows the approved update and change-log behavior.
5. Positive, negative, mixed, and uncertain content keep the source evidence and receive only the selected analysis.
6. One serious individual signal can alert for investigation without incrementing an unsupported trend claim.
7. Wrong-entity and out-of-scope records do not enter the in-scope analysis.
8. A source failure writes Failed or Partial to Monitor_Run_Log and preserves the last successful state.
9. An empty result is labeled No New Records only after a successful source check.
10. Alert routing in test mode reaches only the test recipient.
11. Running trigger setup twice leaves one matching trigger.
12. The run respects the confirmed cadence and source limits.

Report passed, failed, partially tested, or blocked for every case. Give exact manual steps for tests that must run under the user's Google account. Pause for results before writing dashboard code.

## Dashboard build and validation

After the user returns successful monitoring test results, build a native Executive_Dashboard tab by default. Add an HTML interface only if selected. The dashboard should read from the validated workbook rather than duplicate or reinterpret raw source data.

Check that:

- record counts reconcile to Review_Data by source and period;
- source-specific ratings retain their own scales and audiences;
- new, changed, and duplicate records are distinguishable;
- positive and negative signals are both visible;
- individual signals and possible trends have different labels;
- source failures and stale checks cannot appear as zero customer feedback;
- coverage gaps and classification confidence remain visible;
- no score ranks employees or teams.

Keep Apps Script quotas and source limits in the setup notes. Recheck Google's quota documentation before publication because service limits can change.
