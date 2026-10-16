# Bonus test prompt: use the system already built

Provide the complete skill folder or the current repository plus the existing Sheet/project references and any design export. Replace bracketed references with actual links/files. The prompt intentionally leaves business-specific schema decisions to inspection.

---

Use the VOC Sheet Web App bonus workflow from:
https://github.com/rtomboj/tomboj-voc-signal-to-change

Read skills/voc-sheet-web-app/SKILL.md completely and follow its references.

I have already completed the earlier VOC stages. My Google Sheet, Apps Script, and scheduled triggers already exist and work. Continue from this state.

Existing working Google Sheet: [link or already available reference]
Existing Apps Script project: [link or access through the Sheet]
Optional visual design: [attached HTML/design]

Inspect the current Sheet and installed script through your authorized tools where supported. Map the actual tabs, header rows, columns, IDs, statuses, and relationships. Adapt the web app to them; do not rebuild my workbook to match a template. Reuse any already supplied links or exports and ask only for information you cannot inspect.

Check whether your tools can actually read/edit Apps Script source and deployments; Drive access alone may not support this. If direct changes are unavailable, produce complete HTML and GS files, precise patches, and editor instructions for me to install.

Add an Apps Script web interface to this existing workflow. Use the attached design as the visual starting point, replacing embedded sample data, fixed dates, and fake role controls with connections to the current Sheet.

For the first test, support viewing, filtering, details, source health, follow-up and change status, due updates, and copying drafts where the data supports those views. Keep unsupported screens clearly unavailable. Propose any editing actions separately; do not send customer messages or change triggers from the web interface.

The website must be private to my Google Workspace organization. Verify the intended deploying account/domain, execution identity, and organization-only deployment option. Do not publish it for "any Google account" or anonymous access. If my account cannot provide domain-only access, explain the specific blocker and keep testing private.

Prepare and test the patch against a copy first. Keep the existing monitoring logic, trigger handlers/schedules, source routes, formulas, and operational records intact. Audit all callable server functions, including pre-existing functions with side effects, so a viewer cannot bypass the UI.

Deliver:
1. An inspection summary and actual-to-web schema map.
2. Complete adapted HTML/GS files and any additive manifest patch.
3. A changed-file list, installation steps, and rollback.
4. Tests covering data reconciliation, unavailable tabs, permissions, direct server calls, and monitoring regression.
5. An evidence-based status for each test: passed, failed, blocked, or not run.

Begin by inspecting what is already available and showing the proposed mapping and file changes. Continue building the parts you can complete. Resolve only missing choices that affect live installation or deployment before applying them. Do not claim a deployment or live test passed without evidence.
