# Tomboj VOC Signal-to-Change

Turn customer feedback into a benchmark, a monitoring routine, owned customer follow-up, and company improvements whose results can be checked.

For Customer Success, Support, CX, and operations leaders. Use these AI-guided instructions in Claude, ChatGPT, Kimi, or another capable assistant. The assistant adapts the workflow to your company, available tools, and existing files.

**[Start here](docs/start-here.md)** · [See the fictional example](examples/closed-loop/walkthrough.md) · [View example images](docs/example-gallery.md)

## Choose where to begin

| You want to… | Start with |
| --- | --- |
| Understand public feedback about a company | [Step 1: Benchmark](docs/start-here.md#starting-fresh) — supply the company website |
| Continue a benchmark, monitoring setup, or action plan already built | [Continue existing work](docs/start-here.md#continuing-existing-work) — reuse the files and last test results |
| Turn your existing Google Sheet and Apps Script into a private web interface | [Web app bonus](docs/start-here.md#adding-the-private-web-interface) — inspect and adapt the current system |

No coding setup or Google connection is required to start the public-source benchmark. Later stages use Google Drive, Google Sheets, and Apps Script. The assistant checks what it can access and offers supported connections or manual files/copy-paste for anything missing.

## The four parts and optional bonus

| Part | Question | What you get |
| --- | --- | --- |
| [1. Benchmark](skills/voc-benchmark-builder/SKILL.md) | Where are customers speaking, and what deserves attention? | Source map, dated evidence, themes, report, workbook, and monitoring handoff |
| [2. Monitor](skills/voc-monitoring-automation/SKILL.md) | What changed, and are our checks working? | Permitted source checks, deduplication, adapted Apps Script, alerts, and source health |
| [3. Follow up](skills/voc-customer-follow-up/SKILL.md) | Who responds, what happens next, and did it help? | Cases, actions, customer update drafts, coaching, and closure evidence |
| [4. Improve the company](skills/voc-systemic-change/SKILL.md) | What should change, and did the change work? | Explicit decisions, accountable delivery, verification, and report-back |
| [Bonus: Web interface](skills/voc-sheet-web-app/SKILL.md) | How do people use the workflow through a browser? | HTML/GS files adapted to the existing Sheet, private deployment instructions, and tests |

All five skills are included. They are portable instructions and supporting templates; user-specific code and live deployment are created and tested during your run. Recommendations, generated files, installed code, completed tests, and measured customer outcomes remain separate.

## What the output can look like

These are **rendered documentation previews** of the included Northstar example. All companies, comments, owners, actions, and results are synthetic. The images illustrate the information each view can show; they are not browser screenshots of a live Google Sheet or a deployed private app. Your assistant should adapt the actual output to your data and structure.

### Benchmark: evidence before conclusions

![Synthetic Northstar benchmark preview showing themes, sample counts, and evidence limits](docs/images/northstar-benchmark.jpg)

See what feedback says, how much evidence supports it, and what would confirm or challenge the interpretation. A small accessible sample does not establish customer-wide prevalence.

### Follow-up: delivery and customer outcome stay separate

![Synthetic Northstar follow-up preview showing a delivered workaround with only partial customer resolution](docs/images/northstar-follow-up.jpg)

A delivered workaround can coexist with an unresolved customer outcome. Ownership, next updates, and longer-running change obligations remain visible.

### Web interface: one view of the loop

![Synthetic Northstar web overview connecting source health, customer follow-up, and a change awaiting verification](docs/images/northstar-overview.jpg)

The optional web layer reads the existing system. A failed source check is visible, a shipped change remains under verification, and drafts are not counted as sent messages.

[Explore the connected example and its CSV files](examples/closed-loop/walkthrough.md) · [Open the example gallery](docs/example-gallery.md)

## How to run it

1. Open the [start-here guide](docs/start-here.md) and copy the prompt for your route.
2. Run it in an assistant with the required research/file tools, supplying existing context where available.
3. Answer the questions the assistant cannot resolve from inspection.
4. Keep generated files and return actual test output so the assistant can correct errors and continue.

A normal mixed route is direct Google Sheet reading with manual Apps Script installation. A missing integration does not require restarting the workflow or connecting an unsupported service.

If your assistant cannot open GitHub references, download this repository and supply the relevant complete skill folder, including its references and assets. Named-skill installation is optional when the assistant can follow the files as project instructions.

## Expectations and validation

- Step 1 starts with public sources and a company website; internal system access is not a prerequisite.
- Monitoring depends on permitted, usable collection routes; some sources will remain manual.
- The web bonus requires verified organization-only Workspace deployment for organization-only access.
- Automated checks cover repository structure and selected record/evidence gates. They do not prove authorization, live delivery, or improved customer outcomes.
- The workflow is designed to be portable across assistants. Completed cross-provider production testing is not claimed.

See the [validation and pilot guide](docs/validation.md). The fictional example can be checked from a clone with Python 3.10+:

```bash
python scripts/check_repository.py
python scripts/validate_loop_registers.py examples/closed-loop/registers
python scripts/check_example.py
python -m unittest discover -s tests -v
```

These are maintainer/example checks; users can begin with the prompts without installing Python.

## Documentation and source files

| Need | Read |
| --- | --- |
| Starting prompts, expected questions, and manual routes | [Start here](docs/start-here.md) |
| Detailed skill usage and capabilities | [User guide](docs/user-guide.md) |
| Stage inputs, outputs, and handoffs | [Four-part workflow](docs/four-part-workflow.md) |
| Connected fictional data and rendered previews | [Northstar example](examples/closed-loop/walkthrough.md) and [gallery](docs/example-gallery.md) |
| Checks, limitations, and live pilot requirements | [Validation guide](docs/validation.md) |
| Google Workspace services and Apps Script | [Workspace field guide](docs/apps-script-workspace-field-guide.md) |
| Provider/model evaluation method | [Model evaluation](docs/model-evaluation.md) |

Core instructions live in `skills/`; human guides in `docs/`; the fictional example in `examples/closed-loop/`; read-only validation utilities in `scripts/`.

## Attribution and licensing

Created by **Rachel Wilde / Tomboj**. Original methodology and written content are available under [CC BY 4.0](LICENSE-CONTENT.md); code is available under the [MIT License](LICENSE-CODE.md). Third-party material retains its own terms. Tomboj brand identifiers are not granted for reuse.

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for provenance and [CITATION.cff](CITATION.cff) for citation metadata. Proposed timing, schemas, and gates are operating-design choices, not universal standards or guaranteed financial results.
