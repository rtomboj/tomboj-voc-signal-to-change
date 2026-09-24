# VOC Workspace services reference

Use this reference before choosing Apps Script services, OAuth scopes, or an optional model API for the VOC monitor. It covers only what this workflow needs. For a wider map of Workspace, AI-client connections, and community repositories, see the optional [Apps Script and Google Workspace field guide](../../../docs/apps-script-workspace-field-guide.md).

## Services the monitor uses

| Job | Default service | Notes |
| --- | --- | --- |
| Read and write the working Sheet | `SpreadsheetApp` in a script bound to the converted Sheet | The bound script reaches its parent Sheet without a copied ID. |
| Check a permitted public review page, API, or feed | `UrlFetchApp` | Needs the external-request scope. Read and validate each site's response; browser-rendered entries may be absent, and public visibility alone does not establish collection permission. |
| Scheduled checks | Installable time-driven trigger (`ScriptApp`) | Runs as the account that created it. Created only after tests pass. |
| Prevent overlapping writes | `LockService.getScriptLock()` | Wrap collection and writes; log a skipped run if the lock is held. |
| Configuration and state | `PropertiesService` | Non-secret settings in Script Properties; credentials in the trigger owner's User Properties. |
| Digest and test notices | `MailApp` | Sends only; narrower than `GmailApp`. Respect daily recipient quotas. |
| Chat notices (optional) | Chat incoming webhook via `UrlFetchApp` | One-way messages to a configured space. Treat the webhook URL as a credential. |
| Manual capture (optional) | A `Manual_Capture` tab, or a Google Form writing to the Sheet | Manual rows enter the same deduplication and baseline pipeline. |
The monitor does not need Drive-wide access, Gmail reading, Admin SDK, Docs, Slides, Meet, or an MCP connection. Do not add them.

## Scopes

- Prefer the narrowest scopes that cover the confirmed design, and list them in `appsscript.json`.
- `@OnlyCurrentDoc` suits a bound script that touches only its own Sheet; check it is compatible with every service the script calls.
- Tell the user which scopes they will approve and why. A script with sensitive scopes may show an "unverified app" screen; explain it before they run setup.
- The optional [Drive intake helper](../examples/drive-intake/README.md) is a separate project with a broad Drive scope. It is not part of the monitor.
## Deterministic automation versus model calls

| | Deterministic Apps Script | Recurring model call |
| --- | --- | --- |
| What it does | Collects, deduplicates, compares, counts, flags | Classifies or summarizes text |
| Cost per run | Google quota only | Provider tokens on every run |
| Credentials | Google authorization only | A provider API key in addition to Google authorization |
| Data leaving Google | None beyond confirmed source requests | Review text sent to the provider |
| Default | On | Off; setup-time help or a one-off summary instead |

If the user opts into recurring model calls, name the provider, the text sent, expected volume and cost, a per-run budget, and how to switch it off. User Properties belong to the trigger owner, but editors of a bound Sheet may edit its script, so those properties do not protect a key against an untrusted editor. Use an owner-controlled private setup and limit script editors, or use a controlled standalone project or Google Cloud Secret Manager for team use. Never put keys in code, cells, logs, alerts, or the setup conversation. Script Properties are shared configuration, not a private key store.

## Official references

- [Container-bound scripts](https://developers.google.com/apps-script/guides/bound)
- [Installable triggers](https://developers.google.com/apps-script/guides/triggers/installable)
- [Properties Service](https://developers.google.com/apps-script/guides/properties)
- [LockService](https://developers.google.com/apps-script/reference/lock/lock-service)
- [Authorization and scopes](https://developers.google.com/apps-script/guides/services/authorization)
- [Quotas](https://developers.google.com/apps-script/guides/services/quotas)
