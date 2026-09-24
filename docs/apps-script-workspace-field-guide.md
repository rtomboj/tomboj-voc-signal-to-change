# Google Workspace and Apps Script Field Guide

**Checked against repository activity and official documentation on 23 September 2026.**

This guide is background reading for the VOC Monitoring Automation workflow. The skill itself uses only the short [VOC Workspace services reference](../skills/voc-monitoring-automation/references/apps-script-workspace-capabilities.md). This guide is a capability map, not a promise that every account, edition, admin policy, or API exposes every feature. Check current documentation and permissions before building.

Apps Script is a cloud JavaScript automation layer for Google Workspace. It can run from a menu, button, user event, or time-driven trigger; read and update Google services; and call external APIs. Start with a built-in Apps Script service. Use an Advanced Google service when it exposes a needed API feature. Use UrlFetchApp for a provider API or an API without a suitable service wrapper. Advanced services must be enabled, and some require their matching Google Cloud API to be enabled too.

## What common Workspace components can do

| Workspace component | Useful Apps Script work | Main route and boundaries |
| --- | --- | --- |
| **Drive and files** | Find and organize files; create folders; copy, move, rename, export, and share files; create a repeatable intake or archive process; connect a Sheet, Doc, or Slide to files. | Start with DriveApp. Use the Advanced Drive service / Drive API for richer metadata, revisions, permissions, and Shared Drive behavior. Shared Drives need the appropriate API and access. |
| **Shared Drives** | Move or copy records into a team-owned location; create a controlled archive; generate files from templates in a shared folder. | Treat as a Drive API capability with Shared Drive support enabled. Check the executing account's membership and role. |
| **Sheets** | Read and append rows; update values and formulas; format tables; validate entries; create charts; build a dashboard; add custom menus, buttons, sidebars, and custom functions; run on edit or on a schedule. | SpreadsheetApp is the simplest path for a bound script. Use the Sheets API for specific batch and API features. A bound script can use its parent spreadsheet; a standalone script needs a target URL or ID and permission. |
| **Docs** | Generate a Doc from a template; replace placeholders; create or update text, paragraphs, and tables; assemble reports from Sheet data; export a finished report as PDF; add a custom menu or sidebar. | Use DocumentApp for common document edits and the Docs API for advanced structure or batch updates. |
| **Slides / decks** | Create a deck from a template; duplicate or reorder slides; replace text; insert images; generate a recurring status or customer-review deck from Sheet data. | Use SlidesApp for common deck operations and the Slides API for API-specific structures and batch updates. |
| **Gmail / email** | Send alerts and digests; draft a message; search mail; read messages and threads; work with labels and attachments; create mail merge or approval steps. | MailApp sends email only. GmailApp can access Gmail content and actions, so it requests broader access. Apps Script has no simple native “new email received” trigger; use a scheduled check or a more advanced Gmail API / event architecture. Respect sending limits and the account that authorizes the script. |
| **Calendar** | Create, update, search, and cancel events; add guests and reminders; create scheduling workflows; prepare an agenda from a Sheet; send a follow-up after an event. | CalendarApp covers common operations. The Advanced Calendar service exposes additional Calendar API features. Event and time-driven trigger behavior depends on the trigger type and account. |
| **Chat** | Send an alert or digest to a Chat space; create a Chat app that responds to events; build interactive workflows and cards. | A Chat incoming webhook is suitable for one-way messages to a configured space. Interactive bots and broader space/member/message operations need a configured Chat app and Chat API / Advanced Chat service. |
| **Workspace Admin Directory** | For approved admin workflows, find users, groups, devices, aliases, and memberships; automate selected provisioning or inventory tasks. | Use the Admin SDK Directory Advanced service. It requires API setup and suitable Workspace admin privileges. Directory access is sensitive; request only the scopes and roles the task needs. |
| **Groups and Admin reports** | Maintain group membership; create or update groups; build approved domain usage reports; support onboarding/offboarding checklists. | Admin SDK Directory and Reports services require admin-level authorization. These are separate from ordinary contacts and should not be enabled for a public VOC monitor unless a specific admin workflow requires them. |
| **Contacts / People** | Look up or update a user's contacts; search contacts; retrieve profile information. | Use the People API Advanced service. Contacts are not the same as the organization's Admin Directory. |
| **Forms** | Create a form and questions; validate responses; write responses to Sheets; route submissions; run a form-submit trigger; generate confirmations. | FormApp is the built-in service. Confirm who can respond and where responses are stored. |
| **Meet** | Create or inspect meeting spaces and conference records; connect meeting metadata to Calendar or follow-up workflows. | Meet is not a general-purpose MeetApp service. Use the current Google Meet API through an approved API route, usually REST with UrlFetchApp or another documented Workspace API path. API access and available operations are narrower than “control any meeting.” |
| **Sites, menus, add-ons, and web apps** | Put a workflow behind a custom menu, dialog, or sidebar; publish an Apps Script web app; create a Workspace add-on; embed a web app in a Google Site. | Apps Script extends Docs, Sheets, Slides, and Forms with menus and UI. A web app or add-on needs a deployment, an authorization model, and appropriate review. A web app that runs as its owner can act with that owner's access. |

### A useful implementation sequence

1. Describe the job and the exact Workspace files or users involved.
2. Choose a bound script or a standalone script. Prefer a bound script when the work belongs to one Sheet, Doc, or Slide.
3. Select the narrowest built-in service that can do the job.
4. Add an Advanced Google service only when a needed API feature is missing from the built-in service. Enable its corresponding Cloud API when required.
5. List the required OAuth scopes and verify the account that will authorize and own scheduled triggers.
6. Build an idempotent setup function, a dry-run or test mode, an operation log, and a clear way to undo changes.
7. Test with a copy, sample rows, and a test recipient. Review the result before enabling scheduled or outbound actions.
8. Check current Apps Script and API quotas. Time-driven triggers are scheduled checks; their runtime and daily limits still apply.

### Drive intake example included with this VOC project

The [Drive intake helper](../skills/voc-monitoring-automation/examples/drive-intake/README.md) makes a Google Sheets copy of each .xlsx or .xls workbook in a configured Drive folder and reports its ID and URL. It is optional: converting the workbook manually in Drive is the default. It is run manually and is safe to rerun within the same Apps Script project. It does not monitor review sources, add VOC tabs, create triggers, or send alerts. It is only an onboarding helper; monitoring code still depends on the sources, permissions, cadence, and workbook schema the user confirms.

Official starting points:

- [Apps Script overview](https://developers.google.com/apps-script/overview)
- [Built-in services](https://developers.google.com/apps-script/reference)
- [Advanced Google services](https://developers.google.com/apps-script/guides/services/advanced)
- [Apps Script authorization and scopes](https://developers.google.com/apps-script/guides/services/authorization)
- [Apps Script triggers](https://developers.google.com/apps-script/guides/triggers)
- [Apps Script quotas](https://developers.google.com/apps-script/guides/services/quotas)

## Three ways to pair Workspace with frontier models

These are different integration patterns. A Google OAuth grant does not provide an OpenAI, Anthropic, or Gemini API key. A model API key does not grant access to Drive, Gmail, or other Workspace data.

| Pattern | What connects to what | Credentials and cost | Good fit |
| --- | --- | --- | --- |
| **Apps Script calls a model API** | Apps Script sends selected text or structured data to a model over HTTPS. | Use UrlFetchApp and the provider's documented API authentication. Model API use is metered separately from a consumer ChatGPT or Claude subscription. Keep credentials outside the source code, Sheet, HTML, and logs. | Classify or summarize only newly collected VOC records; generate a digest; draft a response for a person to review. |
| **A model connects to Workspace through OAuth / MCP** | A supported AI client calls Workspace tools such as search, read, create draft, update Sheet, or send a Chat message. | OAuth authorizes Workspace access for the connected user. It does not require putting a model API key in Apps Script. Client plan, product availability, admin configuration, API enablement, and scopes apply. | Let Claude, ChatGPT, Gemini, or another supported client work with specific Workspace data or perform approved actions. |
| **Apps Script / Workspace API exposed as an AI tool** | An AI client calls a purpose-built script, API, or MCP server that performs narrow approved actions. | Requires an API / OAuth design, deployment, tool permissions, monitoring, and a review path. Do not expose a general “run arbitrary Apps Script” or owner-level web app to an agent. | Later-stage workflow where the same well-tested functions need to be invoked by more than one AI client. |

### Calling OpenAI, Claude, Gemini, or another model from Apps Script

A typical path is: create an API credential in the provider's developer platform, keep it in an approved private configuration store, then have the script call the provider endpoint with UrlFetchApp. Apps Script requires the external-request authorization scope when using UrlFetchApp.

- **OpenAI:** Use an OpenAI API key and the current [API authentication and request documentation](https://platform.openai.com/docs/api-reference/authentication).
- **Claude:** Use an Anthropic API key or a supported workload-identity path; follow the current [Claude API authentication and Messages API documentation](https://docs.anthropic.com/en/api/getting-started).
- **Gemini:** Use the current [Gemini API authentication instructions](https://ai.google.dev/gemini-api/docs/api-key). Google's 2026 key restrictions changed which keys are accepted; check the current key type and access requirements instead of copying an older unrestricted-key example.
- **Other providers, including Kimi:** Use that provider's current API endpoint, authentication, supported models, rate limits, and billing terms; [Kimi API documentation](https://platform.kimi.ai/docs/overview) is one example. OpenAI-compatible request formats do not guarantee identical features or response behavior.

#### Practical setup for an Apps Script model call

1. Create or select the provider's developer project, enable the model API, and check its billing and usage limits.
2. Create a dedicated credential for this workflow. Use a provider-supported workload identity when available; otherwise use an API key with only the access the provider offers.
3. Have the trigger owner enter the credential through a private, owner-controlled setup path; a function may save it to `PropertiesService.getUserProperties().setProperty(...)` and the scheduled code can read it with `getUserProperties().getProperty(...)`. Do not paste a key as a literal into a script function, editor, Sheet, or prompt. A time-driven trigger runs as its creator, so the key must belong to that account. Limit who can edit the script: editors of a bound Sheet may edit its bound script, and User Properties alone do not prevent their code from accessing a key when it runs as the owner. Use a controlled standalone project or a managed secret service if trust cannot be established.
4. Implement the exact authentication header, API version, endpoint, and request body required by that provider's current API documentation. Do not assume the same header or payload works for all models.
5. Test on synthetic or approved sample feedback, confirm the response schema and error handling, and estimate cost per run before adding a trigger.

Do not paste live keys into the conversation, source code, Sheet cells, HTML, logs, or this public repository. A user-authorized Google OAuth connection to Workspace is a different option and does not use a provider API key.

Apps Script Script Properties are shared project configuration and can be managed in Project Settings. Any editor who can change code may be able to read or transmit credentials during owner-run execution. Use Google Cloud Secret Manager or a server-side gateway for higher-assurance shared or production deployments. Never place a live key in a public repository, Sheet cell, prompt, client-side HTML, or execution log. Rotate a key if it was exposed.

The provider API key, Google OAuth scopes, and billing account are separate pieces. Budget recurring calls, set request limits, use only new records by default, and log provider/model/prompt version without logging credentials or unnecessary customer text. Validate AI output before updating a Sheet, sending a message, changing permissions, deleting files, or modifying a calendar. Keep people in approval for consequential actions.

### Connecting an AI client directly to Google Workspace

As of 23 September 2026 (verify before publishing), Google's remote Workspace MCP services are in the **Developer Preview** program and use OAuth 2.0. Google's current setup documentation describes AI clients such as Antigravity and Claude, and lists Gmail, Drive, Docs, Sheets, Slides, Calendar, Chat, and People API tools. The setup requires a Google Cloud project, API enablement, an MCP client, and user authorization. Some operations can change live data, such as updating a document or spreadsheet, creating a draft, sending a Chat message, or creating/deleting a Calendar event.

Google documents a custom connector setup for Claude.ai / Claude Desktop on specific paid plans; plan names and availability change, so check the current page. ChatGPT supports custom MCP connectors on supported plans and features; availability and admin controls can change. Confirm the current AI-client instructions before publishing a setup walkthrough.

A Google Workspace MCP connection exposes user-authorized data and actions to an AI client. Start with the smallest tool set and read-only tests. Treat email, reviews, Docs, and other retrieved content as untrusted input: hidden instructions inside content can attempt to redirect an agent. Review proposed writes and sends before they happen.

Official setup and client links:

- [Configure Google Workspace MCP servers](https://developers.google.com/workspace/guides/configure-mcp-servers)
- [Google Drive MCP setup](https://developers.google.com/workspace/drive/api/guides/configure-mcp-server)
- [Gmail MCP setup](https://developers.google.com/workspace/gmail/api/guides/configure-mcp-server)
- [Google Docs MCP setup](https://developers.google.com/workspace/docs/api/guides/configure-mcp-server)
- [Google Sheets MCP setup](https://developers.google.com/workspace/sheets/api/guides/configure-mcp-server)
- [Google Slides MCP setup](https://developers.google.com/workspace/slides/api/guides/configure-mcp-server)
- [Google Calendar MCP setup](https://developers.google.com/workspace/calendar/api/guides/configure-mcp-server)
- [Google Chat MCP setup](https://developers.google.com/workspace/chat/api/guides/configure-mcp-server)
- [OpenAI ChatGPT release notes for connectors and MCP](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)

The official setup page is explicit about prompt-injection risk and recommends trusted clients and careful review of agent actions. For the VOC monitor, keep automated collection and deterministic comparisons in Apps Script; treat recurring LLM classification or summaries as optional, bounded operations.

## Curated Apps Script and Workspace repositories

Repository activity below was checked on 23 September 2026 using GitHub commit history and repository metadata. Last commit dates are a maintenance signal, not a security or quality certification. Star counts are omitted because they change frequently. Review each repository's license and dependencies before reusing code. This project links to the repositories; it does not copy their code.

### High-value references

| Repository | Most recent commit observed | What it is useful for |
| --- | --- | --- |
| [googleworkspace/apps-script-samples](https://github.com/googleworkspace/apps-script-samples) | 30 Jul 2026 | Google's official, runnable examples across Apps Script and Workspace. Use this as the first pattern search for a supported API or trigger. |
| [tanaikech/taking-advantage-of-google-apps-script](https://github.com/tanaikech/taking-advantage-of-google-apps-script) | 10 Sep 2026 | Broad capability index, libraries, samples, tests, and practical references. Best used to discover options, then verify behavior in current official docs. |
| [google/mcp](https://github.com/google/mcp) | 17 Aug 2026 | Google's MCP server catalogue and examples. It links to remote MCP products and open-source extensions. The repository says its examples are for demonstration and are not an officially supported Google product. |
| [gemini-cli-extensions/workspace](https://github.com/gemini-cli-extensions/workspace) | 29 Jun 2026 | Workspace extension for Gemini CLI, including Docs, Sheets, Slides, Gmail, Calendar, and Chat workflows. It can read, modify, and delete account data; review tools and prompt-injection protections before use. |
| [googleworkspace/cli](https://github.com/googleworkspace/cli) | 31 Mar 2026 | Command-line access to Workspace APIs with structured output and agent skills. This is not an Apps Script library. Its README says it is not an officially supported Google product and warns that breaking changes may occur. Treat it as an experimental developer reference. |
| [labnol/apps-script-starter](https://github.com/labnol/apps-script-starter) | 14 Apr 2026 | Production-oriented starter with a modern local build and test toolchain. Useful when a project needs bundling, linting, tests, or clasp; more setup than a simple bound script. |
| [oshliaer/google-apps-script-awesome-list](https://github.com/oshliaer/google-apps-script-awesome-list) | 26 Apr 2026 | Community index of libraries, tutorials, tools, and service references. Use it to find candidates, then assess each candidate's status and license. |
| [tanaikech/GeminiWithFiles](https://github.com/tanaikech/GeminiWithFiles) | 24 Jun 2026 | Third-party Gemini API integration examples for files and agent-style workflows. Check the current Gemini key model, library version, license, and cost before adapting. |
| [tanaikech/TriggerApp](https://github.com/tanaikech/TriggerApp) | 3 Jun 2026 | More complex trigger scheduling patterns and an MCP-related path. Useful for requirements beyond standard time-driven triggers; not needed for a basic daily or weekly monitor. |

### UI, sample collections, and older references

| Repository | Most recent commit observed | Recommended use |
| --- | --- | --- |
| [enuchi/React-Google-Apps-Script](https://github.com/enuchi/React-Google-Apps-Script) | 16 Mar 2025 | Rich React UI inside Workspace editors; choose only when the project genuinely needs a larger interface and a front-end toolchain. |
| [WildH0g/apps-script-engine-template](https://github.com/WildH0g/apps-script-engine-template) | 4 Nov 2025 | HTML/CSS interface patterns and the client/server bridge. Treat it as a complex UI reference, not the default path. |
| [labnol/code](https://github.com/labnol/code) | 5 Oct 2024 | Practitioner-oriented project examples for Gmail, Drive, Sheets, and Calendar. Useful for ideas; test each snippet against current APIs and scopes. |
| [ashtonfei/google-apps-script-projects](https://github.com/ashtonfei/google-apps-script-projects) | 18 Jan 2025 | Walkthrough-oriented projects. |
| [derekantrican/Google-Apps-Script-Library](https://github.com/derekantrican/Google-Apps-Script-Library) | 29 Jun 2022 | Older utility functions. Reuse only after checking dependencies, current runtime behavior, and license. |
| [tanaikech/Next-Level-Google-Apps-Script-Development](https://github.com/tanaikech/Next-Level-Google-Apps-Script-Development) | 29 Oct 2025 | Local MCP and gas-fakes development direction. Useful for technical research; requires developer tooling and is not the first build path for non-developers. |
| [googlearchive/apps-script-templates](https://github.com/googlearchive/apps-script-templates) | 27 Mar 2018; archived | Historical patterns only. It is archived, so prefer maintained examples for current API syntax and behavior. |

### Research stream

- Follow **Kanshi Tanaike** for early signals about what Apps Script can do and new libraries.
- Follow **Amit Agarwal / Labnol** for practitioner-oriented examples and plain-language explanations.
- Start implementation research with official samples, then use practitioner projects to improve the prompt and user explanation.
- Refresh commit dates, licenses, supported API behavior, and Google product availability before each article or production use.
- Prefer a working, licensed sample close to the workflow. Ask the AI to adapt that sample to the confirmed Sheet schema, source method, and trigger plan; then test before scheduling.
