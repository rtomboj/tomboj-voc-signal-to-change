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

Continue from my existing VOC Google Sheet and Apps Script.
Determine the capabilities available in this session. Offer a supported
connection or manual route for anything missing. Adapt the HTML/GS
files to the actual Sheet and script. Give me installation steps,
review the results I return, and continue through testing.
The intended deployment is private to my Workspace organization.
```

The [full bonus prompt](../skills/voc-sheet-web-app/assets/web-app-test-prompt.md) adds optional design and testing details. Organization-only deployment needs an eligible Workspace account/domain and verified deployment settings; if unavailable, the assistant can still prepare files and explain the deployment blocker.

## What the interaction looks like

The assistant will research or inspect, propose a mapping or plan, ask a targeted question where needed, create files/code, and check the result. Research and file generation can take time between questions. There is no fixed completion-time promise; source accessibility, volume, and your environment affect the run.

| Stage | What you should receive | Your typical part |
| --- | --- | --- |
| Benchmark | Source map, evidence, themes, focus, report/workbook | Confirm company, scope, sources, and insight window |
| Monitor | Source plan, adapted Apps Script, tests, monitoring view | Confirm collection choices; install/run code if direct editing is unavailable |
| Follow-up | Cases, actions, update drafts, coaching and closure plan | Confirm authority, owners, commitments, and actual customer outcomes |
| Company change | Decisions, change records, delivery/verification plans | Make the business decisions and supply delivery/result evidence |
| Web bonus | Adapted HTML/GS files, access/deployment steps, tests | Paste files or authorize supported edits; return actual installation/access results |

Connection and business questions should arise when relevant. You do not need to answer a long setup questionnaire before the assistant inspects work already supplied.

## Connected, manual, or both

The Google stack is used for monitoring and the web bonus. A particular AI provider's connections are not assumed. Your assistant may be able to read Sheets while being unable to edit Apps Script; in that case, it should produce complete files and tell you where to paste them.

Return the exact error or test output, with secrets and unnecessary personal data removed. The assistant should fix the affected step and continue. Files generated, code installed, tests passed, and an app deployed are distinct checkpoints.

## See an example first

Explore the [Northstar fictional example](../examples/closed-loop/walkthrough.md), its [rendered example images](example-gallery.md), and its downloadable CSV tables. The illustration uses synthetic data throughout. Its web preview is a local documentation demo, not a live private deployment.

For more detail, use the [user guide](user-guide.md), [workflow contract](four-part-workflow.md), and [validation guide](validation.md). Users can ask their assistant to run the repository validators; Python is not a prerequisite for the starting prompts.
