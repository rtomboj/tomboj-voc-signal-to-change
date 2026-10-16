# Detailed user guide

An AI-guided system for finding where customers are speaking, establishing a defensible Voice of Customer benchmark, monitoring new feedback, and turning what is learned into action.

## The system

| Step | Question | Outcome | Status |
| --- | --- | --- | --- |
| 1. Establish the benchmark | Where are customers speaking, what do they appear to value, and where should attention go? | Confirmed profile and source map, dated platform baseline, review-level insight window, starter taxonomy, visual dashboard, Signal-to-Focus Map, coverage gaps, and monitoring specification | Available |
| 2. Automate monitoring | How will we detect new feedback and changes? | Manual or permitted scheduled public-source checks, deduplication, classification options, alerts, source health, and a separate tested monitoring dashboard | Available |
| 3. Follow up with customers | Who responds, what happens next, and is the customer's outcome resolved? | Owned cases, response clocks, coaching, action plans, customer updates, and honest closure | Available |
| 4. Make company changes | What should change across product, policy, process, teams, or the organization? | Evidence-based decisions, accountable delivery, verification, and report-back | Available |

The four steps are portable AI-guided workflows, with templates and validation utilities. “Available” means the skill is included; customer-specific automation, live access, and business outcomes still require implementation and verification. See [the full workflow and handoff contract](../docs/four-part-workflow.md).

**Optional bonus:** [Turn the existing VOC Sheet into a private web app](../skills/voc-sheet-web-app/SKILL.md). Continue from the Sheet, Apps Script, and triggers already produced; inspect and adapt their actual structure rather than rebuilding to a template.

## Connections and manual routes

Use the same workflow in Claude, ChatGPT, Kimi, or another capable assistant. The Google stack is assumed for monitoring and the web bonus; a particular provider's connections are not. At each stage, inspect the current session's tools and the existing outputs, use authorized connections where available, and ask only for the missing information needed next.

Drive file access, Sheet reads/edits, Apps Script source/edits, trigger inventory, and deployment are distinct capabilities. Offer a supported connection/authorization route or a manual file/export/copy-paste route for missing jobs. A common setup reads the Google Sheet directly while the user pastes generated HTML and GS files into Apps Script. Return test output to the assistant so it can correct errors and continue from that checkpoint.

Step 1 remains public-source and file-based; it does not require a Google connection. See the bonus's [connection and manual-handoff protocol](../skills/voc-sheet-web-app/references/connections-and-manual-handoffs.md) for the detailed capability map.

## Step 1: VOC Benchmark Builder

The [VOC Benchmark Builder](../skills/voc-benchmark-builder/SKILL.md) is a portable set of instructions for an AI assistant with current web-research capability.

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

These are starting recommendations for dependable output, not hard minimums or guarantees. Less expensive models may be suitable for batch classification after the company profile, sources, sample, and taxonomy have been confirmed. Audit low-confidence records and a sample of all classifications with the baseline model or a person. Model names, capabilities, and pricing change; see [Model evaluation and background testing](../docs/model-evaluation.md) for the current testing method.

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

When spreadsheet creation is available, the skill requires a tailored, downloadable `.xlsx` workbook with validated tabs, fields, formulas, charts, and traceable evidence. Workbook outputs follow a shared [visual standard](../skills/voc-benchmark-builder/references/visual-style.md): Calibri, Tomboj charcoal and teal, labeled status colors, wrapped text, and vertically centered cell content.

Before delivery, the assistant runs the dependency-free [workbook validator](../skills/voc-benchmark-builder/scripts/validate_workbook.py). The validator does not edit or upload the workbook. It fails when required tabs, fields, dashboard sections, evidence-class labels, freeze panes, core styling, or chart rules are missing, and it supplies a short manual-review checklist for judgments that cannot be verified reliably from workbook XML.

## Step 2: VOC Monitoring Automation

The [VOC Monitoring Automation](../skills/voc-monitoring-automation/SKILL.md) is the companion workflow for a completed Part 1 benchmark. Its first version uses Google Drive, Google Sheets, and Apps Script to monitor permitted public feedback. It assesses both Part 1 files, confirms source routes and cadence, prepares a preserved Google Sheets working copy, generates source-specific code, and tests collection before building a separate Monitor_Dashboard. Sources without a confirmed automated route remain manual, watchlist, deferred, or excluded. Internal company sources remain out of scope for this version.

The skill starts with a source-specific Apps Script public-page check when permitted and usable, prefers official APIs/feeds/exports/notifications when more reliable, and supports manual review for exceptions. A blocked or changed page is a failed/partial check, not zero feedback. The user-specific monitoring code and dashboard are generated and tested during the guided workflow.

For the Workspace service map, frontier-model connection patterns, and refreshed Apps Script repository references, see the optional [Apps Script and Google Workspace field guide](../docs/apps-script-workspace-field-guide.md). The skill itself uses a short [VOC Workspace services reference](../skills/voc-monitoring-automation/references/apps-script-workspace-capabilities.md). The repo also includes an optional [Drive intake Apps Script example](../skills/voc-monitoring-automation/examples/drive-intake/README.md) for converting several Part 1 Excel workbooks at once; for a single workbook, Drive's manual “Save as Google Sheets” flow is the default.

## Step 3: VOC Customer Follow-Up

The [VOC Customer Follow-Up skill](../skills/voc-customer-follow-up/SKILL.md) handles the immediate customer loop: triage, assignment and acceptance, response timing, conversation preparation, training/coaching, action plans, updates, and closure. It supports both authorized company operators and researchers preparing a handoff. Supplied feedback can be handled without waiting for a complete benchmark.

It delivers a follow-up operating plan and three reusable registers: cases, actions, and customer updates. Engagement, delivery, customer outcome, and administrative closure remain separate. Unknown reviewer identities, unaccepted handoffs, unanswered contact attempts, and draft messages never become invented customer resolutions.

> Use $voc-customer-follow-up with my VOC signals to prepare owned follow-up cases, a response and coaching plan, and customer update drafts.

Provide the complete `skills/voc-customer-follow-up/` folder, including its references and assets. Existing approved policy takes precedence over suggested pilot timings. The skill prepares drafts by default; sending requires authorization.

## Step 4: VOC Systemic Change

The [VOC Systemic Change skill](../skills/voc-systemic-change/SKILL.md) handles product, process/policy, team, department, and organizational opportunities. It turns evidence into an explicit decision, assigns accountable ownership, plans delivery and adoption, verifies outcomes, and reports back. It also supports positive practices worth expanding and clear deferred or declined decisions.

It delivers a change register, case-to-change links, decision briefs, measurement plans, and report-back drafts. A shipped fix stays under verification until the agreed evidence supports improvement; customer cases retain their own status and update obligations.

> Use $voc-systemic-change with these VOC cases to prioritize company improvements, draft decision briefs, and define how we will verify and report the results.

Provide the complete `skills/voc-systemic-change/` folder. No CRM, product-tool, or employee-system connection is required to prepare a reviewable proposal. Execution requires the relevant authority and environment.

## Bonus: turn the existing Sheet into a private web app

The [VOC Sheet Web App skill](../skills/voc-sheet-web-app/SKILL.md) adds an Apps Script web interface to the system the user already has. It inspects current tabs, header rows, aliases, IDs, status values, script files, and trigger/deployment state; then generates adapted HTML and GS files with a documented schema map and additive patches. An optional design export supplies the visual starting point.

The Sheet remains the source of truth. Existing monitoring, formulas, records, and triggers stay in place. Begin with viewing, filters, details, and draft copying; add editing only when its actions are specified and authorized. Require a verified organization-only Workspace deployment, server-side access controls, and live permission tests. If direct Apps Script tools are unavailable, deliver complete files and precise owner-run installation steps.

Use [this provider-neutral starting prompt](../skills/voc-sheet-web-app/assets/web-app-test-prompt.md) in Claude, ChatGPT, Kimi, or another capable assistant. Provide the complete bonus skill folder; reuse existing conversation context and references. The assistant determines the available connections, offers supported connection or manual routes, generates complete files, and continues interactively from returned installation/test results. Keep private instance code, IDs, and operational records outside this public repository.

> Use $voc-sheet-web-app to inspect my existing VOC Sheet and Apps Script project, adapt this design to the actual structure, and prepare a private organization-only web app.

## Try the complete customer-to-company loop

Read the [synthetic walkthrough](../examples/closed-loop/walkthrough.md) and its five linked CSV registers. Everything in that example is fictional. Run the local checks from a clone with Python 3.10 or later:

```bash
python scripts/check_repository.py
python scripts/validate_loop_registers.py examples/closed-loop/registers
python -m unittest discover -s tests -v
```

The [validation guide](../docs/validation.md) explains checks, limits, private CSV exports, and live pilot requirements. The repository validator is optional tooling for a full clone; each portable skill includes its own manual acceptance checks. It does not contact customers or change operational systems.

## Test models and measure cost

Use [Model evaluation and background testing](../docs/model-evaluation.md) to compare OpenAI, Claude, and Kimi using the same inputs. The guide separates interactive research from batch classification and records tokens, cost, elapsed time, source quality, schema compliance, and human corrections.

## Repository structure

```text
docs/                                  # Workflow, validation, Workspace, model evaluation
skills/voc-benchmark-builder/           # Step 1; includes workbook validator
skills/voc-monitoring-automation/       # Step 2; includes Drive intake example
skills/voc-customer-follow-up/          # Step 3; references, plan, three CSV templates
skills/voc-systemic-change/             # Step 4; references, brief, two CSV templates
skills/voc-sheet-web-app/               # Bonus; adapt current Sheet/script to a private web UI
examples/closed-loop/                  # Fictional connected walkthrough and registers
scripts/check_repository.py            # Local links, metadata, template structure
scripts/validate_loop_registers.py     # CSV relationships and selected evidence gates
tests/                                # Invalid closure, delivery, and handoff checks
.github/workflows/validate.yml         # Automated repository checks
```

## Attribution and provenance

The project is original instructional work informed by existing Voice of Customer methods, public skill conventions, and prior-art repositories. See [ATTRIBUTIONS.md](../ATTRIBUTIONS.md) for repository-level provenance and the [Benchmark Builder](../skills/voc-benchmark-builder/ATTRIBUTIONS.md), [Monitoring Automation](../skills/voc-monitoring-automation/ATTRIBUTIONS.md), [Customer Follow-Up](../skills/voc-customer-follow-up/ATTRIBUTIONS.md), and [Systemic Change](../skills/voc-systemic-change/ATTRIBUTIONS.md) attribution records. Proposed timings, schemas, and lifecycle gates are operating-design choices, not universal standards or guaranteed financial results.

## Licensing

| Material | License |
| --- | --- |
| Original written methodology, skill instructions, templates, examples, and documentation | [Creative Commons Attribution 4.0 International](../LICENSE-CONTENT.md) |
| Source code, scripts, formulas, and executable utilities | [MIT License](../LICENSE-CODE.md) |

Third-party materials retain their original licenses and notices. Tomboj names, logos, and other brand identifiers are not granted for reuse unless explicitly stated.

## Author

Created by **Rachel Wilde / Tomboj**.

If you use or adapt this work, preserve the requested attribution and indicate material changes. Citation metadata is available in [CITATION.cff](../CITATION.cff).
