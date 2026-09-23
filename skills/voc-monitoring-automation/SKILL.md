---
name: voc-monitoring-automation
description: Guide users from a completed public VOC benchmark to a tested Google Workspace monitoring workflow. Use when they have the Part 1 Markdown report and workbook, want permitted public-source checks, Google Sheets updates, Apps Script generation, change detection, alerts, or a later dashboard.
---

# VOC Monitoring Automation

Guide the user through Step 2 of Tomboj VOC Signal-to-Change: convert a completed public-source benchmark into a tested monitoring workflow in Google Workspace.

Step 1 establishes the benchmark. Step 2 collects permitted updates, compares them with the saved baseline, and surfaces changes. Step 3 closes the loop through ownership, customer response, resolution, and organizational learning.

Use VOC to help organizations, teams, and people see opportunities to improve. Never frame it as a way to punish people or rank individual employees. Surface both positive and negative change. One comment is not a trend, though one serious customer signal may justify an individual follow-up. Distinguish a temporary incident from a sustained shift.

For this version, monitor public external feedback through Google Workspace. Internal support, product, CRM, survey, and account data are out of scope until a later phase.

## Begin with the two Part 1 files

Ask first:

> Do you have both Part 1 files for the company you want to monitor: the Markdown benchmark and the Excel workbook?

If not, point the user to the [VOC Benchmark Builder](https://github.com/rtomboj/tomboj-voc-signal-to-change/tree/main/skills/voc-benchmark-builder/SKILL.md). Give them this starting instruction: “Use the VOC Benchmark Builder to establish an external customer-feedback benchmark for my company.” Ask them to return when they have both outputs. Do not start monitoring from an incomplete benchmark.

If they have both files:

1. Ask them to place them in a Google Drive folder named VOC_Automation.
2. Have them save the Excel workbook as a Google Sheets file. Keep the original Excel workbook and Markdown report as the benchmark record.
3. Ask for the Drive URLs of the Markdown file and Google Sheet. Parse the file IDs from the links when needed.
4. Check whether an authorized Google Drive or Sheets connection can read the files. Ask before making changes to the user's Sheet. If access is unavailable or not authorized, ask the user to upload both files for assessment. Generate setup code and manual instructions when the Sheet itself cannot be edited directly.

Do not publish customer-specific sheet links, IDs, review text, credentials, or generated code to this public repository.

## Assess the workbook before designing automation

Read the Markdown benchmark and inspect the workbook tabs, headers, formulas, current records, taxonomy, source map, and monitoring-readiness notes. Confirm that the two files refer to the same company and benchmark.

Do not assume that every Part 1 workbook has the same additions or status meanings. Preserve existing data and headers. Map equivalent fields when names differ; do not rename or reorder existing columns. Identify missing or ambiguous fields and show the user a short schema map before generating code.

Prefer existing Step 1 tabs when present, including Review_Data, Source_Register, Baseline_Snapshot, Theme_Taxonomy, Signal_to_Focus, and Executive_Dashboard. In the Harri example, Review_Data already has record IDs, source IDs, review dates, audience, ratings, excerpts, themes, signal type, operational impact, classification confidence, and a human-review field. Its Week2_Readiness tab inventories internal data readiness; it does not authorize public-site automation. Use the Source_Register to select public sources and add a source-monitoring configuration for this phase.

Read [monitoring-design.md](references/monitoring-design.md) before defining workbook fields, classifications, scores, or alert rules.

## Confirm what to monitor

Review every row in Source_Register with the user. For each source, confirm:

- whether to include, defer, monitor manually, or exclude it;
- whether the identity and audience are appropriate;
- the permitted collection method and available fields;
- the review cadence: daily, weekly, biweekly, or manual;
- the stable record identifier and deduplication method;
- first-run baseline behavior;
- source failure handling;
- alert conditions and recipients.

Do not treat a source as automatable simply because it is publicly visible. Use a permitted API, feed, export, notification, or manual review. Do not bypass sign-in, CAPTCHAs, paywalls, rate limits, or platform restrictions. If a source has no permitted automated method, offer manual capture or a watchlist status.

Ask the user which analysis to automate:

1. **Collection only:** detect and record new or changed source data.
2. **Rules and formulas:** calculate source-specific rating or volume movement and propose categories using the existing taxonomy or approved keyword rules.
3. **Optional AI classification:** classify and summarize new records with confidence labels. Estimate token use for the expected volume. Process new records only by default; do not resummarize the entire history on every run.

If the user chooses AI classification or summaries, confirm the provider, connection path, data handling, and per-run budget before generating model calls. Keep AI optional and do not expose or use an API key without authorization.

Keep source ratings separate. Do not combine unlike platforms into a company score. Use any operational-impact or trend category to direct investigation, not to evaluate or punish a person.

## Prepare the Google Sheet

After the user confirms the source plan and permits changes, make a working copy or edit only the designated Google Sheets copy. Preserve the original Part 1 files.

Add only missing tabs and fields. The standard setup is:

- **Monitoring_Config:** one row per selected public source with collection method, cadence, permission status, stable ID field, first-run rule, fields collected, alert rule, and owner.
- **Monitor_Run_Log:** timestamp, source, run status, records fetched, new records, updated records, duplicates skipped, alerts sent, and error summary.
- **Review_Data:** continue the existing Step 1 record table. Append new records and map them into its existing schema.
- **Review_Change_Log:** add only when the source can revise an existing review and the user wants field-level change history.
- **Baseline_Snapshot, Theme_Taxonomy, Signal_to_Focus, and Executive_Dashboard:** preserve and reuse existing tabs. Do not build or refresh the dashboard until collection and monitoring tests pass.

If direct Sheet editing is unavailable, generate an idempotent setup function that creates missing tabs and headers without overwriting existing rows, plus a manual setup table. Clearly tell the user which setup path they must run.

Define collection, monitoring, and classification separately:

- **Collection** checks the selected source and retrieves accessible aggregate measures or review records.
- **Monitoring** compares that result with the saved baseline and prior run, identifies new or changed items, prevents duplicates, updates the record store, and records source health.
- **Classification and scoring** interpret the stored records using the confirmed taxonomy or optional AI. They are analysis applied to the records, not collection itself.

On first run, treat existing Step 1 records and current source state as a baseline. Do not alert on historical items unless the user asks to backfill them. A failed or blocked source check is an error state, never a zero-feedback result.

## Generate and test the monitoring code

Read [apps-script-delivery.md](references/apps-script-delivery.md) and [apps-script-workspace-capabilities.md](references/apps-script-workspace-capabilities.md) before selecting Google APIs, OAuth scopes, or an optional LLM connection. Generate complete, source-specific Apps Script project files from the confirmed workbook schema and permitted collection methods. Do not return pseudocode where runnable code is expected.

Deliver all required .gs files and setup instructions. Generate an .html file only if the user chooses a custom Apps Script sidebar or web interface; a native Sheets dashboard does not require HTML.

Keep the source-checking, record mapping, deduplication, classification, alerts, and trigger setup readable and independently testable. Do not hardcode secrets into code, cells, or public files. Do not put the user's Spreadsheet ID or generated code in this repository. A bound script opened from the Google Sheet can target its parent spreadsheet; use a copied Sheet ID only when the selected design requires a standalone script or another target.

Include a setup operation for the user to create the scheduled trigger, but leave it inactive until manual tests pass. Explain the requested Google authorization scopes. The user must run the setup operation and approve the permissions from the account that will own and maintain the trigger.

Run tests before building the dashboard. Test at least:

- first-run baseline does not send historical alerts;
- a new record is appended once;
- the same stable ID is skipped on the next check;
- an edited record follows the agreed update and change-log policy;
- positive and negative signals follow their respective rules;
- one serious signal can prompt investigation without being labeled a trend;
- wrong-entity or out-of-scope records are excluded or flagged for human review;
- source failure is logged and never presented as “no new feedback”;
- test alerts go only to test recipients;
- duplicate trigger setup does not create duplicate schedules.

Report each test as passed, failed, partially tested, or blocked. Give the user the code files, installation and authorization steps, and the test results. Pause for the user to run the tests in Google Workspace and return the results.

## Build and test the dashboard after collection passes

After the user confirms the monitoring tests passed, generate or run the dashboard builder. Default to a native Executive_Dashboard sheet. Ask before adding a custom HTML interface.

Show source health and last successful check, new and changed feedback, positive and negative signals, theme changes, the evidence window and coverage, and items that need human review. Keep incident signals distinct from recurring patterns. Keep classification confidence, evidence strength, prevalence confidence, and operational impact separate. Do not create a hidden composite score or an employee ranking.

Test that dashboard totals reconcile to Review_Data, filters preserve source and audience distinctions, failed checks remain visible, and one individual review is not displayed as a trend. Do not claim an unsupported prevalence or causal conclusion.

## Finish

Provide the updated Google Sheet link if the user authorized direct editing, or setup code and precise manual instructions otherwise. Include the generated Apps Script files, test instructions and results, chosen source methods and cadences, alert rules, known limits, and dashboard validation status.

Do not add internal company data sources in this version. Offer them as a later phase only after the public-source monitor is working.
