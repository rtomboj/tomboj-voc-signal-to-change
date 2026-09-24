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

If not, point the user to the [VOC Benchmark Builder](https://github.com/rtomboj/tomboj-voc-signal-to-change/blob/main/skills/voc-benchmark-builder/SKILL.md). Give them this starting instruction: “Use the VOC Benchmark Builder to establish an external customer-feedback benchmark for my company.” Ask them to return when they have both outputs. Do not start monitoring from an incomplete benchmark.

If they have both files:

1. Ask them to place them in a Google Drive folder named VOC_Automation.
2. Keep both Part 1 files as the originals in that folder. Create a Google Sheets copy of the Excel workbook. By default, point the user to the [Drive intake helper](examples/drive-intake/README.md), which converts .xlsx/.xls files in VOC_Automation and outputs the Sheet ID and URL. It must be run and authorized in the user's Apps Script project. If they prefer not to grant its Drive access, use Drive's manual “Open with Google Sheets” and “Save as Google Sheets” flow. Never overwrite the original Excel file.
3. Ask for the Drive URLs of the Markdown file and Google Sheet. Parse the file IDs from the links when needed.
4. Check whether an authorized Google Drive or Sheets connection can read the files. Ask before making changes to the user's Sheet. If access is unavailable or not authorized, ask the user to upload both files for assessment. Generate setup code and manual instructions when the Sheet itself cannot be edited directly.

Do not publish customer-specific sheet links, IDs, review text, credentials, or generated code to this public repository.

## Assess the workbook before designing automation

Read the Markdown benchmark and inspect the workbook tabs, headers, formulas, records, taxonomy, source map, and readiness notes. Confirm that both files refer to the same company and benchmark.

Use the [Part 1 workbook contract](../voc-benchmark-builder/references/benchmark-output.md) and [workbook validator](../voc-benchmark-builder/scripts/validate_workbook.py) when available, then report what the validator found. Treat the workbook contract as a reference, not proof that an individual file conforms. In the reviewed examples, Harri is a legacy workbook that fails the current contract, Nory is closer but still has validator errors, and Toast is missing monitoring-critical tabs. These examples show why every workbook must be inspected before code is generated.

Preserve existing data, formulas, tab names, and headers. Map field aliases by header name; do not rename or reorder existing columns. Look for headers in the first 20 rows, since some example tabs have title and notes rows above the table. Show the user a short schema map with matches, aliases, missing fields, and unresolved values before creating code.

Use `Week2_Readiness` as the source plan only when it contains a row per source and the source decisions and fields are clear. If it is an internal readiness checklist or otherwise not source-shaped, build a separate `Monitoring_Config` from `Source_Register`, preserving the Part 1 workbook. Never infer permission to automate from inclusion, public visibility, or a readiness label.

Read [monitoring-design.md](references/monitoring-design.md) before defining monitoring fields, measures, categories, or alert rules.

## Confirm what to monitor

Prefill a compact source table from Part 1: source, audience/evidence class, inclusion or treatment, known route, Part 1 access/readiness note, and the question that remains. Ask the user to confirm exceptions and unresolved entries rather than repeating eight questions for every source.

Confirm these global choices once, then ask only source-specific exceptions:

- **Account and response path:** does the user own or manage each profile? For each source, choose owned-profile access, public viewing only, or no response route. Part 2 may surface an item for investigation or handoff; customer response and resolution belong to Part 3.
- **Collection route:** approved API/feed/export/notification, manual check, watchlist, deferred, or excluded. Capture permission evidence, the date checked, and who confirmed it. A publicly visible page is not automatically permitted for automated collection.
- **Cadence:** one global default (daily, weekly, biweekly, or manual), with explicit source exceptions. Confirm timezone and a digest recipient if email/chat alerts are selected.
- **First-run behavior:** use Part 1 rows as history and start new monitoring from an agreed date, or capture the current page as the start point.
- **Analysis and alerts:** collection only, deterministic measures/rules, and/or optional AI. Confirm separately whether a single serious item warrants an investigation notice and what evidence is required for possible-trend alerts. If no possible-pattern rule is confirmed, keep trend alerts off and show counts only.

Offer manual capture with a reminder when no permitted and reliable automated route is confirmed. Do not imply that a website can be monitored just because it is reachable in a browser. Do not bypass sign-in, CAPTCHAs, paywalls, rate limits, or platform restrictions.

The default should be deterministic collection, source health, and a quiet digest. A single record may merit a private investigation prompt under a user-approved rule, but it must remain an individual signal. Do not call one record a trend.

Automate measures such as record counts, source-specific rating movement, last-check age, new/changed records, and source errors when the inputs support them. Do not average unlike rating scales, audiences, or source populations. Say “measure” or “change measure”; never frame a measure as an employee score or ranking.

AI may help during setup or run an on-demand summary. Recurring AI classification or summaries are opt-in only. Before generating recurring model calls, name the provider, where review text is sent, the key/secret storage approach, expected token use/cost, and a per-run budget; get the user's explicit choice.

## Prepare the Google Sheet

After the user confirms the source plan and permits changes, create a dated backup of the Part 1 workbook and work in its Google Sheets conversion. Keep the .xlsx and Markdown benchmark unchanged. Excel conversion can alter formatting, charts, validation, or formulas, so treat the converted Sheet as a working copy and compare important sections after conversion.

Add only missing tabs and fields. Prefer existing compatible Step 1 tabs. For an incompatible legacy workbook, map into its existing schema and create a clearly documented monitor-specific config; do not force the Part 1 workbook into the current validator contract.

A standard setup can include:

- **Monitoring_Config:** one row per source if `Week2_Readiness` is not a clear row-per-source source of truth. Include method, permission status/evidence, cadence, ID approach, baseline rule, fields, alert choice, and process-owner role.
- **Manual_Capture:** source, observed date, review date, canonical URL/ID, audience/evidence class, rating/scale, excerpt, capture person/role, theme suggestion, and human-review status. A Google Form is optional.
- **Monitor_Run_Log:** timestamp, source, success/partial/failure status, fetched/new/updated/duplicate counts, and concise error.
- **Review_Data:** append to the existing table where compatible; otherwise create a mapped monitor data tab and document the field map.
- **Monitor_Dashboard:** separate monitoring view. Preserve the Part 1 `Executive_Dashboard`, which may use fixed ranges or represent a historical benchmark.
- **Review_Change_Log:** optional; use when the source edits prior reviews and the user wants field-level history.

Use `Week2_Readiness` as config only if it is already a clear row-per-source plan. Otherwise derive the monitoring plan from `Source_Register` once and show the mapping; avoid two conflicting editable source lists.

Define the jobs separately:

- **Collection** checks a chosen source using its confirmed route, or records a human-captured observation.
- **Monitoring** compares successful observations with the agreed baseline and prior run, deduplicates, appends new records, records permitted edits, and logs source health.
- **Classification** applies confirmed labels or measures to the stored records. Suggestions remain marked as suggestions until approved.

Record evidence class and audience separately, so customer reviews, vendor-selected stories, press, and other context do not get mixed into one count. Count syndicated copies once using an agreed canonical source while retaining other URLs as provenance. Add permission evidence URL, confirmation date, and confirmer role to the source plan.

For identifiers, add an **ID Origin** field where it is missing: platform ID, canonical URL, fingerprint, synthetic, or unknown. Join on Source ID plus record ID and origin; never deduplicate on URL alone when URLs are unstable. For synthetic/unknown IDs, compare the source's current visible state, establish a fresh dated baseline, and begin alerts from that point. Do not replay historical Part 1 rows as new alerts.

If direct Sheet editing is unavailable, deliver an idempotent setup function and a manual tab/header checklist. The function must create missing structures without clearing existing rows.

## Generate and test the monitoring code

Read [apps-script-delivery.md](references/apps-script-delivery.md) and [apps-script-workspace-capabilities.md](references/apps-script-workspace-capabilities.md) before selecting Google APIs, OAuth scopes, or an optional LLM connection. Generate complete source-specific Apps Script files from the confirmed schema and permitted collection methods. Do not return pseudocode where runnable code is expected.

Deliver all required .gs files and setup instructions. Generate an .html file only if the user chooses a custom sidebar or web interface; a native Sheet dashboard does not require HTML.

Keep collection adapters, record mapping, deduplication, measures, notifications, and trigger setup independently testable. Do not hardcode secrets, Sheet IDs, customer-specific URLs, or review data in public files. In a bound script, use the parent Sheet where possible.

Ship a `TEST_MODE` and `runAllTests()` that uses fixtures and a separate test copy or test tabs; tests must not send alerts to operational recipients or append fixtures to production data. Until the user runs it in their Google account and shares results, report live Workspace tests as **not run**. Do not say a Google authorization, trigger, live fetch, email, or Chat delivery passed unless the user has supplied the result.

Give the user a clear click path: open the converted Google Sheet → **Extensions → Apps Script** → add the provided files → save → run the documented setup function on the backup/test copy → review and approve the requested scopes → run the manual checks. Explain account-owner/admin restrictions where relevant. Only after the manual tests pass should they run the separate trigger-setup function. The trigger runs under the account that created it; that person should be the maintainer.

Test at least:
- baseline-date and Part 1 suppression, including text/ambiguous dates and synthetic-ID sources;
- new ID appended once, duplicate skipped, edited record handled by the agreed policy;
- source ID and ID Origin disambiguation; syndicated copies counted once;
- positive and negative single-item signals, possible-pattern rules, low-volume display, and audience/evidence-class separation;
- wrong-entity and out-of-scope records flagged or excluded;
- manual capture and overdue reminders;
- failed source, stale source, and partial run are visible and are never shown as “no feedback”;
- test notifications go only to test recipients;
- concurrent runs cannot write the same records twice;
- repeated trigger setup by the same maintainer does not create duplicates;
- quota/time-limit handling leaves a clear resumable or failed state.

Report each test as passed, failed, partially tested, blocked, or not run. Pause for user-run test results before generating the dashboard builder.

## Build and test the dashboard after collection passes

After the user confirms the monitoring tests passed, generate or run the separate `Monitor_Dashboard` builder. Keep the Part 1 dashboard unchanged. Default to a native Google Sheet tab; ask before adding HTML.

Show last successful check and source health, new/changed records, positive and negative signals, themes and their evidence window, source and audience coverage, possible incidents/patterns, and items needing human review. Keep an individual incident separate from a recurring pattern. Keep evidence class, audience, evidence strength, frequency, confidence, and operational impact separate. A process owner is a role responsible for follow-up, not the person being evaluated.

Below the agreed minimum volume, show counts and records without percentages or “trend” labels. Use an explicitly confirmed threshold for possible patterns. A quiet theme should read “no new reports in this window,” not “fixed,” unless a later resolution check supports that conclusion.

Test that dashboard counts reconcile to the monitoring data, filters preserve source/audience/evidence distinctions, failed checks stay visible, and one individual review is never drawn as a trend. Do not infer prevalence or causality beyond the evidence.

## Finish

Provide the updated Sheet link only if the user authorized direct editing, or provide exact manual steps otherwise. Include generated Apps Script files, scope explanation, chosen source routes and cadences, confirmed alert rules, limits, test status, and dashboard validation status. State any user-run tests as not run until results are returned.

Keep internal company sources out of this public-source version. Offer them as a later phase once the public-source workflow is working.
