# Start here

Use an AI assistant to build a Voice of Customer workflow around your company and the files you already have. Start with public feedback, then progress to monitoring, customer follow-up, company improvements, and an optional private web interface.

You do not need to be a developer or clone this repository to begin. Use an assistant that can open the instructions and their references. If it cannot read GitHub links, download the repository and provide the relevant complete skill folder, including its references and assets.

## Choose your route

| Your starting point | Start here | Have ready |
| --- | --- | --- |
| I am starting fresh | Step 1: Benchmark | Company website |
| I have already built some of the workflow | Continue existing work | Earlier conversation, reports/files or working links, and last test results |
| My Sheet and Apps Script exist; I want a website | Web app bonus | Existing Sheet/project references or exports; optional design |

### Starting fresh

Paste this into Claude, ChatGPT, Kimi, or another capable assistant with web research and file creation:

```text
Follow the VOC Benchmark Builder instructions at:
https://raw.githubusercontent.com/rtomboj/tomboj-voc-signal-to-change/main/skills/voc-benchmark-builder/SKILL.md

Read the skill completely and follow its references.
My company website is: [website]
Begin with Step 1. Guide me through the questions and validation.
```

Step 1 uses public sources and does not require Google access. The expected outputs are a written benchmark and an Excel workbook that can later be converted to Google Sheets. If the assistant cannot create a workbook, it should explain the limitation and provide the allowed table/CSV fallback. Microsoft software is not required to use files in Google Sheets.

### Continuing existing work

Use the same conversation where practical, or supply the previous outputs and build record in a new conversation:

```text
Continue my VOC Signal-to-Change workflow:
https://github.com/rtomboj/tomboj-voc-signal-to-change

Review the existing work and last test results I have supplied.
Identify the next incomplete step and read its SKILL.md and references.
Inspect what you can access, reuse my decisions, and ask only for
missing information needed next. Preserve completed work.
```

Step 2 needs the Step 1 report and workbook. Steps 3 and 4 can also begin with directly supplied feedback or improvement evidence. See the [handoff guide](four-part-workflow.md) for the inputs to each stage.

### Adding the private web interface

Paste this in the conversation with your current Google Drive/Sheet context:

```text
Follow the VOC Sheet Web App bonus instructions:
https://raw.githubusercontent.com/rtomboj/tomboj-voc-signal-to-change/main/skills/voc-sheet-web-app/SKILL.md
Read it completely and follow its references.

I have completed Steps 1–4 for my company. Continue from my existing Google Sheet and Apps Script; do not restart earlier steps.

Before building, ask me (once):
1. Do I have a design (file, link, or a Claude Design project — I can export it as a zip)? If not, help me pick a minimal one.
2. Which Google account will run this: Google Workspace (needed for team use) or a personal account ("Only myself" pilot)?
3. REAL data only, or a REAL/SYNTHETIC toggle?

Keep it as simple as possible: one workbook (the one my Step 2 script is attached to). If my Step 3–4 registers are in
separate files, find them and use the setup script to add the tabs and import REAL rows. Add Team and Activity_Log tabs.

Map my actual tabs and the design's fields before writing server code. Give me complete files, the exact paste order,
the one function to run, and what I should see. Keep a build record and a learning log as we go,
and continue from the results, screenshots or PDFs I send back.

Choose application access mode open or team with me once. Start read-only; after setup and read tests, add the standard five edit actions with confirmation, reasons, stale checks and Activity_Log. Never send customer messages. For anyone beyond the owner, use a standalone web project and keep the monitor in the bound project.
```

The [full bonus prompt](../skills/voc-sheet-web-app/assets/web-app-test-prompt.md) includes the required design-source intake, conversion checklist, exact file/paste order and testing details. Supply a design source file/link; if none exists, the assistant helps establish one before backend work. Team deployment needs an eligible Workspace account/domain and verified settings. A personal account starts with an Only myself pilot; a wider open pilot is a separate explicit audience choice with unverified entered names. The app uses one workbook, adds Team and Activity_Log through setup, and keeps non-owner web access in a standalone project.

## What the interaction looks like

The assistant will research or inspect, propose a mapping or plan, ask a targeted question where needed, create files/code, and check the result. Research and file generation can take time between questions. There is no fixed completion-time promise; source accessibility, volume, and your environment affect the run.

| Stage | What you should receive | Your typical part |
| --- | --- | --- |
| Benchmark | Source map, evidence, themes, focus, report/workbook | Confirm company, scope, sources, and insight window |
| Monitor | Source plan, adapted Apps Script, tests, monitoring view | Confirm collection choices; install/run code if direct editing is unavailable |
| Follow-up | Cases, actions, update drafts, coaching and closure plan | Confirm authority, owners, commitments, and actual customer outcomes |
| Company change | Decisions, change records, delivery/verification plans | Make the business decisions and supply delivery/result evidence |
| Web bonus | Design-to-Sheet contract, adapted HTML/GS files, ordered installation and tests | Supply/reuse design source; paste files or authorize supported edits; return actual results |

Connection and business questions should arise when relevant. You do not need to answer a long setup questionnaire before the assistant inspects work already supplied.

## Connected, manual, or both

The Google stack is used for monitoring and the web bonus. A particular AI provider's connections are not assumed. Your assistant may be able to read Sheets while being unable to edit Apps Script; in that case, it should produce complete files and tell you where to paste them.

Return the exact error or test output, with secrets and unnecessary personal data removed. The assistant should fix the affected step and continue. Files generated, code installed, tests passed, and an app deployed are distinct checkpoints.

## See an example first

Explore the [Northstar fictional example](../examples/closed-loop/walkthrough.md), its [rendered example images](example-gallery.md), and its downloadable CSV tables. The illustration uses synthetic data throughout. Its web preview is a local documentation demo, not a live private deployment.

For more detail, use the [user guide](user-guide.md), [workflow contract](four-part-workflow.md), and [validation guide](validation.md). Users can ask their assistant to run the repository validators; Python is not a prerequisite for the starting prompts.
