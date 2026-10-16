# Start the bonus in Claude, ChatGPT, Kimi, or another assistant

Provide the complete skill folder or current repository. Add existing references or files only if they are not already in the conversation. The assistant discovers the session's actual connections and asks for missing information progressively; no preflight questionnaire is required.

---

Use the VOC Sheet Web App bonus workflow from:
https://github.com/rtomboj/tomboj-voc-signal-to-change

Read skills/voc-sheet-web-app/SKILL.md completely and follow its references.

Continue from the VOC system already created in Google Drive, Google Sheets, and Apps Script. Reuse the earlier outputs and decisions in this conversation. Inspect which stages are complete and which still need work; do not restart them.

Existing working Google Sheet: [link or already available reference]
Existing Apps Script project: [link or access through the Sheet]
Optional visual design: [attached HTML/design]

First determine what this session can actually access: Drive files, Sheet structure/data, Sheet edits, Apps Script source/edits, triggers, and deployments are separate capabilities. Verify the intended targets where possible. Do not assume a capability because I am using a particular AI provider.

Where access is missing, offer a supported connection/authorization route or a manual export/paste route. Remember my choice. Reading my Sheets directly while I copy/paste the generated Apps Script files is a supported route. Do not require me to connect an unsupported tool.

Inspect the current Sheet and available script source. Map the actual tabs, header rows, columns, IDs, statuses, and relationships. Adapt the web app to them. Ask only for information you cannot inspect that changes the next step; derive the remaining setup questions from what you find.

If you cannot edit Apps Script, generate complete HTML and GS files with exact names/types, paste order, precise patches to existing code, configuration steps, and the function I should run. Review the result I return, fix errors, and continue interactively until the relevant tests pass or a specific blocker remains.

Add an Apps Script web interface to this existing workflow. Use the attached design as the visual starting point, replacing embedded sample data, fixed dates, and fake role controls with connections to the current Sheet.

For the first test, support viewing, filtering, details, source health, follow-up and change status, due updates, and copying drafts where the data supports those views. Keep unsupported screens clearly unavailable. Propose any editing actions separately; do not send customer messages or change triggers from the web interface.

The website must be private to my Google Workspace organization. Verify the intended deploying account/domain, execution identity, and organization-only deployment option. Do not publish it for "any Google account" or anonymous access. If my account cannot provide domain-only access, explain the specific blocker and keep testing private.

Prepare and test the patch against a copy first. Preserve the existing monitoring logic, trigger handlers/schedules, source routes, formulas, and operational records. Inspect prior test results and ask for only missing checks. Audit all callable server functions, including pre-existing functions with side effects, so a viewer cannot bypass the UI.

Deliver:
1. An actual capability/route summary and actual-to-web schema map.
2. Complete adapted HTML/GS files and any additive manifest patch.
3. A changed-file list, installation steps, and rollback.
4. Tests covering data reconciliation, unavailable tabs, permissions, direct server calls, and monitoring regression.
5. An evidence-based status for each test: passed, failed, blocked, or not run.

Begin with available context and connections. Keep a build record and continue from each returned result. Resolve missing choices at the relevant checkpoint. Do not claim an edit, deployment, or live test passed without evidence.
