# Tomboj VOC Signal-to-Change

An AI-guided system for finding where customers are speaking, establishing a defensible Voice of Customer benchmark, monitoring new feedback, and turning what is learned into action.

## The system

| Step | Question | Outcome | Status |
| --- | --- | --- | --- |
| 1. Establish the benchmark | Where are customers speaking, what do they appear to value, and where should attention go? | Confirmed profile and source map, dated platform baseline, review-level insight window, starter taxonomy, visual dashboard, Signal-to-Focus Map, coverage gaps, and monitoring specification | Available |
| 2. Automate monitoring | How will we detect new feedback and changes? | Manual or permitted scheduled public-source checks, deduplication, classification options, alerts, source health, and a separate tested monitoring dashboard | Available |
| 3. Close the loop | What happens after feedback arrives? | Ownership, response and resolution SLAs, escalation, learning, and systemic change | Planned |

## Step 1: VOC Benchmark Builder

The [VOC Benchmark Builder](skills/voc-benchmark-builder/SKILL.md) is a portable set of instructions for an AI assistant with current web-research capability.

It begins with one question:

> What is the company website you want to benchmark?

The assistant researches the company, proposes and verifies public feedback sources, recommends a review-level insight window, and asks the user to confirm the scope. It then preserves current platform measures, classifies accessible recent feedback with a traceable company-specific taxonomy, creates visual analysis, and shows what customers appear to value, where they struggle, what may be emerging, and where attention should go first.

The skill keeps company identity, audience fit, geography, and analytic role separate. It does not label unfiltered global metrics as country-specific, combine discussion activity with ratings, bypass platform restrictions, or generate monitoring automation during Step 1.

## Recommended model level

For the complete Step 1 benchmark, use a model capable of sustained web research, source validation, structured data extraction, and spreadsheet creation. The current recommended quality baselines are:

| AI environment | Recommended baseline |
| --- | --- |
| OpenAI | GPT-5.6 Sol |
| Claude | Claude Sonnet 5 |
| Kimi | Kimi K3 |

These are starting recommendations for dependable output, not hard minimums or guarantees. Less expensive models may be suitable for batch classification after the company profile, sources, sample, and taxonomy have been confirmed. Audit low-confidence records and a sample of all classifications with the baseline model or a person. Model names, capabilities, and pricing change; see [Model evaluation and background testing](docs/model-evaluation.md) for the current testing method.

## Required capabilities and default setup

Before starting, allow the AI environment to:

- search the current public web and open source URLs;
- create downloadable files;
- create and export an Excel `.xlsx` workbook with formulas and charts.

The standard Step 1 path is **public-source and file-based**. The assistant creates the workbook in its working environment and provides it as a downloadable `.xlsx` file. Readers do not need to connect Google Drive, authorize Google Sheets, or configure another integration to complete this exercise.

If the reader already has trusted, authorized connections in their AI environment, they may use those capabilities or choose an existing storage destination. The skill should not stop the benchmark to make them configure a new connection. Google Drive, Google Sheets, Gmail, CRM, support, product, company-system, review-platform login, API, and credential access are not prerequisites for Step 1. If `.xlsx` creation is unavailable, the assistant should provide Markdown or CSV tables and clearly explain the limitation.

## Use the skill

Download or clone this repository and provide the complete `skills/voc-benchmark-builder/` folder to an AI environment that supports skills or project instructions.

- If the environment supports named skills, invoke `$voc-benchmark-builder`.
- Otherwise, ask the assistant to follow `SKILL.md` and make the files in `references/` available when requested.
- Enable current web research. The skill stops rather than fabricating a researched benchmark when live search is unavailable.

Example starting prompt:

> Use the VOC Benchmark Builder to establish an external customer-feedback benchmark for my company.

## Step 1 outputs

- Executive “What this means” summary
- Confirmed Company Profile and Source Register
- Platform Baseline and Review-Level Insight Dataset
- Starter Theme Taxonomy
- Visual Insight Dashboard
- Signal-to-Focus Map
- External VOC Coverage and Gaps
- Week 2 Monitoring-Readiness Specification
- Evidence, Attribution, Assumptions, and Open Questions

When spreadsheet creation is available, the skill requires a tailored, downloadable `.xlsx` workbook with validated tabs, fields, formulas, charts, and traceable evidence. Workbook outputs follow a shared [visual standard](skills/voc-benchmark-builder/references/visual-style.md): Calibri, Tomboj charcoal and teal, labeled status colors, wrapped text, and vertically centered cell content.

Before delivery, the assistant runs the dependency-free [workbook validator](skills/voc-benchmark-builder/scripts/validate_workbook.py). The validator does not edit or upload the workbook. It fails when required tabs, fields, dashboard sections, evidence-class labels, freeze panes, core styling, or chart rules are missing, and it supplies a short manual-review checklist for judgments that cannot be verified reliably from workbook XML.

## Step 2: VOC Monitoring Automation

The [VOC Monitoring Automation](skills/voc-monitoring-automation/SKILL.md) is the companion workflow for a completed Part 1 benchmark. Its first version uses Google Drive, Google Sheets, and Apps Script to monitor permitted public feedback. It assesses both Part 1 files, confirms source routes and cadence, prepares a preserved Google Sheets working copy, generates source-specific code, and tests collection before building a separate Monitor_Dashboard. Sources without a confirmed automated route remain manual, watchlist, deferred, or excluded. Internal company sources remain out of scope for this version.

The skill requires a permitted collection method for each public source, such as an approved API/feed, export, notification, or manual review. The user-specific monitoring code and dashboard are generated and tested during the guided workflow.

For the Workspace service map, frontier-model connection patterns, and refreshed Apps Script repository references, see the optional [Apps Script and Google Workspace field guide](docs/apps-script-workspace-field-guide.md). The skill itself uses a short [VOC Workspace services reference](skills/voc-monitoring-automation/references/apps-script-workspace-capabilities.md). The repo also includes an optional [Drive intake Apps Script example](skills/voc-monitoring-automation/examples/drive-intake/README.md) for converting several Part 1 Excel workbooks at once; for a single workbook, Drive's manual “Save as Google Sheets” flow is the default.

## Test models and measure cost

Use [Model evaluation and background testing](docs/model-evaluation.md) to compare OpenAI, Claude, and Kimi using the same inputs. The guide separates interactive research from batch classification and records tokens, cost, elapsed time, source quality, schema compliance, and human corrections.

## Repository structure

```text
docs/
├── apps-script-workspace-field-guide.md
└── model-evaluation.md
skills/
├── voc-benchmark-builder/
│   ├── SKILL.md
│   ├── ATTRIBUTIONS.md
│   ├── agents/
│   │   └── openai.yaml
│   ├── scripts/
│   │   └── validate_workbook.py
│   └── references/
│       ├── benchmark-output.md
│       ├── company-profile.md
│       ├── insight-analysis.md
│       ├── source-discovery.md
│       └── visual-style.md
└── voc-monitoring-automation/
    ├── SKILL.md
    ├── ATTRIBUTIONS.md
    ├── agents/
    │   └── openai.yaml
    ├── examples/
    │   └── drive-intake/
    │       ├── DriveIntake.gs
    │       ├── README.md
    │       └── appsscript.json
    └── references/
        ├── apps-script-delivery.md
        ├── apps-script-workspace-capabilities.md
        └── monitoring-design.md
```

## Attribution and provenance

The project is original instructional work informed by existing Voice of Customer methods, public skill conventions, and prior-art repositories. See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for repository-level provenance and the [Benchmark Builder](skills/voc-benchmark-builder/ATTRIBUTIONS.md) and [Monitoring Automation](skills/voc-monitoring-automation/ATTRIBUTIONS.md) attribution records.

## Licensing

| Material | License |
| --- | --- |
| Original written methodology, skill instructions, templates, examples, and documentation | [Creative Commons Attribution 4.0 International](LICENSE-CONTENT.md) |
| Source code, scripts, formulas, and executable utilities | [MIT License](LICENSE-CODE.md) |

Third-party materials retain their original licenses and notices. Tomboj names, logos, and other brand identifiers are not granted for reuse unless explicitly stated.

## Author

Created by **Rachel Wilde / Tomboj**.

If you use or adapt this work, preserve the requested attribution and indicate material changes. Citation metadata is available in [CITATION.cff](CITATION.cff).
