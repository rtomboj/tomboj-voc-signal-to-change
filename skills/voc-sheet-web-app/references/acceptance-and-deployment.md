# Acceptance, deployment, and rollback

Use a test workbook/project before applying a patch to the installed project. Record original script source/version, manifest, target workbook references, relevant configuration names, deployment versions, and observed trigger handler/cadence/owner state. Do not export credentials into the test report. State trigger visibility limits.

Do not create installable triggers on the test copy automatically. Keep its web adapter pointed to the test workbook. Use synthetic records for write tests; never send test notifications to operational recipients.

## Acceptance checks

| Scenario | Required evidence |
| --- | --- |
| No design source, or inaccessible/render-only design link | Request source/export or help create/select a minimal design; no backend generated before Step 0 is ready |
| Design expects headers/formulas that differ from Sheet | Field/derivation contract table resolves exact mappings, timezone, nulls and joins before backend generation |
| Business rules embedded in prototype JS | Port authoritative logic to GS; browser presentation does not duplicate formulas; counts reconcile with actual rows |
| Packed design bundle and external assets | Conversion checklist records removal/replacement decisions; hosted visual parity and font/CDN failure behavior checked |
| Fixed now, fake role controls or demo fallback | Live clock/as-of works, selections persist and failures never substitute demo data |
| Manual file installation | One collision-resolved filename/type/paste-order list, complete code and exact read-only test function; returned output closes the checkpoint |
| New explicit or inferred scopes in a triggered project | Before-paste scope report; safe editor consent by affected creators in the actual target project; schedules preserved and scheduled results checked when available |
| No Google integrations exposed | Offer manual inputs and generate a file/paste workflow; do not invent a connector or stop all work |
| Drive works; Sheets/source editing is absent | Reuse Drive for available files and choose manual routes only for missing jobs |
| Sheet reads work; Apps Script edits do not | Map the live Sheet, generate full files/patches, guide owner installation, and review returned test output |
| A supported connector needs consent | Offer connection or manual input; use only documented host consent and verify access afterward |
| Manual route already chosen | Continue it without repeatedly requiring a connection |
| Owner returns an editor error or changed headers | Diagnose the result, refresh affected facts, patch affected files, and resume the relevant test |
| New session/model resumes the workflow | Use the build record; retain completed stages and previously made choices |
| Different tab names, aliases, or header rows | Actual mapping reads the current tables without migration |
| Missing, empty, and inaccessible tables | Distinct UI states; no invented zeros or demo substitution |
| Real and synthetic rows | Separate views and totals; unknown classifications visible |
| Actual run-log statuses | SUCCESS/PARTIAL/FAILED/etc. correctly mapped; failed checks visible |
| Web request with no active Sheet | Adapter opens only the configured test workbook |
| Date cells and long tables | Serializable timestamps, correct timezone, bounded reads/pagination |
| Untrusted feedback and links | Text escaped, links validated, no injected executable markup |
| Internal permitted viewer | Intended data loads through the actual web deployment |
| External signed-in account | Access denied by the deployment boundary |
| Anonymous/incognito browser | Access denied; sign-in alone is not the full external-account test |
| Restricted role, if used | Unauthorized fields absent from server payloads, not merely hidden |
| Forged role/tab/workbook and direct RPC calls | Server rejects unauthorized reads/mutations, including legacy functions |
| Open/refresh website | No emails, monitoring runs, trigger installation, or data changes |
| Existing automation | Original handler names, cadence, configuration, and behavior retained |
| Editing, if authorized | Stable-ID write, transition validation, stale-edit rejection, lock, audit, no unintended formula execution |
| Setup and import idempotency | Second setup/import produces no new tabs, cells, rows, or audit entries; existing row-1 and row-4 layouts stay intact; only selected data class imports |
| Internal navigation regression | First reproduce the reported blank-page failure on the shipped old build; then click every internal link on the fix in a cross-origin sandboxed iframe. A file:// page or already-fixed fixture is insufficient |
| RPC transport regression | Run a null-dropping object mock and a Date-rejecting transport; JSON envelope preserves null, zero, empty and missing-field handling without undefined labels |
| Long operational text | Privately inspect actual rows at 390 px and 1440 px; no mid-word breaks/overflow, short status chips stay whole, free-text chips wrap at spaces and tables scroll inside cards; public fixtures stay synthetic |
| Edit flow end to end | Real server code behind a google.script.run stand-in exercises all five forms, confirmation/reason, save/refresh, cancel, stale conflict, transport error and blank-email name prompt; no customer messages |
| Edit invariants | Missing/forged fingerprint, duplicate key, invalid vocabulary, missing evidence, unauthorized Team capability, lock contention and missing audit tab reject without writes; changed fields only, literal formula text and one audit row per field |
| Team and open access choices | Open admits only the chosen deployment audience; team denies blank/inactive/unknown identities and forged roles; entered names never grant access; directory failure still allows typed owners |
| Product shipped / case closed with owed update | Verification and update obligations remain accurate |

Classify each check passed, failed, blocked, or not run. Provide actual evidence and environment/version, not a bare "all passed." Local mocks cannot establish live access, script permissions, trigger behavior, email delivery, or data freshness.

## Deployment sequence

1. Finish design-source intake, the design data-contract check, inspect/map/build, the conversion checklist and the ordered installation/reauthorization path. Missing deployment choices do not block these stages.
2. Test files locally where feasible and in the Apps Script editor/test environment. A /dev test URL is editor-only and does not prove an organization's viewer access.
3. Verify the chosen account, intended domain/audience, open/team mode, execution identity, scope changes, and complete callable-function audit. Use a standalone project beyond the owner.
4. When deployment is authorized, use Deploy > New deployment > Web app (or a new version of an existing intended deployment). Select the agreed access: organization/domain-only for team use, Only myself for a personal owner pilot, or the explicitly authorized wider open-pilot audience. Never broaden an organization-only requirement as a workaround.
5. Record the deployed version and settings. Test the /exec URL with the internal, external, and anonymous cases above. Report unavailable account tests as not run, keeping the claimed access boundary unverified. For an explicitly wider open pilot, record expected allowed/denied outcomes for that audience rather than falsely asserting external users are denied.
6. Compare monitoring behavior and trigger inventory to the pre-change state without sending unnecessary digests or recreating working triggers.
7. Hand over the URL, changed files, configuration/mapping, test results, unresolved limitations, and rollback.

If direct project editing/deployment is unavailable, deliver exact file contents and click paths for the owner. Do not claim that source files uploaded to Drive have been installed in Apps Script. Do not claim deployment from a saved manifest alone.

In the manual route, return to the build after each owner-run checkpoint. A pasted file is not a test result; compare the actual returned output with the expected output, address errors, and continue toward the next authorized step. Deployment details should be requested when needed for deployment, not as a prerequisite to reading a Sheet or preparing HTML.

## Rollback

Retain the pre-change code and deployment version. Restore the intended deployment to the prior version or disable the new deployment; restore only changed web files/manifest/configuration if needed. Do not delete/recreate existing triggers as a rollback shortcut. Any authorized data writes need their own reconciliation plan; code rollback does not undo them.

Keep the public reusable skill separate from private instance code and records. A sanitized example must replace company identifiers, contact details, source records, workbook/script IDs, properties, recipients, and embedded payloads as appropriate; a renamed company label alone is insufficient.
