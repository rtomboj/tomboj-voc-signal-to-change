# Connections and manual handoffs

Use this process at entry and when a capability or permission changes. The stack is Google Drive, Google Sheets, and Apps Script; the assistant provider and installed integrations vary. Do not require a new account connection to make useful progress.

## Discover this session's capabilities

Start with supplied links/files and the earlier run's context. Use the host's advertised tool inventory or documented discovery mechanism to identify relevant capabilities. Do not broadly scan unrelated private files. Where a target is already authorized and identifiable, verify access with the smallest useful read, such as its metadata and tab/header inventory.

| Job | What establishes capability | Manual fallback |
| --- | --- | --- |
| Find the working files | Available Drive search/metadata tool plus permission for the intended folder/files | Ask for the existing Sheet/project references, file export, or known filename; do not ask the user to rebuild it |
| Read Sheet structure and data | Targeted tab/header/row reads through an authorized Sheet tool, or a readable export | Workbook export; per-tab CSVs with header-row/type notes; pasted headers and a few redacted rows sufficient for the next mapping step |
| Edit the Sheet | Available write capability and scope authorized for the intended change | Exact owner-run tab/field/config steps only where needed; avoid unnecessary workbook changes |
| Inspect Apps Script source/manifest | A source-reading tool or current exported/pasted code | Ask for current relevant files/manifest; never request secret property values |
| Add/update HTML and GS files | A supported Apps Script editing capability, current source, and authorization | Complete labeled files and precise patches to paste into the existing editor |
| Inspect triggers | An actual trigger inventory from the authorized tool/account, or owner-supplied results | Ask for handler/cadence/timezone/owner evidence without changing the schedule; mark visibility limits |
| Create/version a deployment | Supported deployment capability and authorized account/policy | Owner-run Deploy steps with the exact intended access/identity settings and returned results |
| Test browser/user access | Actual browser/deployment tests under the relevant accounts | Owner supplies results for internal, external, and anonymous tests; keep unrun checks explicit |

Label capability claims as **available and target-verified**, **available but target-unverified**, **unavailable in this session**, **permission denied**, or **not checked**. Label a manual route separately as selected/awaiting input. Drive search does not establish Sheet editing; Sheet editing does not establish Apps Script source/deployment access.

Do not assume all properties or triggers can be observed, or that one account can see every maintainer's triggers. Record user-reported facts as such. An API error does not justify replacing the workbook or changing sharing.

## Offer a route only where needed

When a required job cannot proceed directly, describe that specific gap briefly and offer:

1. **Connect or authorize**, when this host actually exposes a supported integration and the user wants to use it. Follow the host's documented consent flow. Re-check the target capability afterward.
2. **Use files or paste manually**, continuing with exports, snippets, complete generated files, and owner-run steps.

Do not imply a Google Drive connection necessarily adds Apps Script access. Do not invent Kimi, Claude, or ChatGPT settings or ask for passwords, tokens, or browser cookies. If a supported connection route is not exposed, say that and provide the manual route. Treat permission expansion as a separate authorization, never as an automatic dependency.

Offer the choice once for the missing group of jobs, then remember it. The user may choose direct reading for Sheets and manual installation for scripts. Do not repeatedly ask them to connect Apps Script after they have chosen to paste files.

## Use progressive questions

| Checkpoint | Ask only if unresolved |
| --- | --- |
| Locate current work | Which candidate workbook/project is the intended working version? |
| Read/map | Can the user connect a supported read capability or provide the specific missing structure/code? |
| Define behavior | Which requested actions need writes or roles beyond already stated requirements? |
| Prepare installation | Which test target/source version should receive the patch, if not already established? |
| Deploy | Which eligible Workspace domain/audience and execution identity apply, if not inspectable? |
| Verify | What actual editor/test/access result is missing? |

Continue independent work while a particular fact is missing. An unverified domain blocks organization deployment, not HTML generation. Missing current server source can block a collision-safe integrated patch, but the assistant can still prepare the UI and identify exactly what source is needed next. Mark partial deliverables honestly rather than inventing the missing contract.

## Manual installation is part of the workflow

For each batch, provide:

- A file manifest: exact project filename, HTML or Script type, new versus changed, purpose, and paste order.
- Full code for new files; exact replacement blocks or complete inspected-file replacements for changes. Never overwrite unknown source with a generic replacement.
- Private configuration fields and how the owner sets them; never embed credentials or customer-specific values in reusable public examples.
- Editor click path: open the existing Sheet > Extensions > Apps Script > add the specified HTML/Script files. Explain editor filename conventions and preserve existing entry points.
- Any additive manifest changes, with the existing fields preserved; show how to reveal the manifest only if needed.
- The exact setup/read-test function, target test workbook, expected output, and what result to bring back. Avoid test functions that send messages or modify triggers unless expressly in scope.

Then inspect the returned result, reconcile it with the intended mapping, fix the affected files, and repeat the necessary check. Continue to the authorized next checkpoint once evidence supports it. Do not stop permanently at "copy this code"; the returned test result closes that installation step.

## Keep continuity

Record connection route per job, target/source version, mapping, supported actions, generated/pasted files, errors, actual test results, and remaining deployment choices in the build record. Distinguish generated, supplied, installed-reported, installed-verified, tested, and deployed states. Use existing test logs where suitable.

When the user returns later, resume from the next unresolved checkpoint. Do not re-run the entire benchmark, recreate the Sheet, reinstall triggers, or re-ask unchanged decisions merely because a new model or assistant is used.
