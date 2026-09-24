# Attribution and Provenance

This file records the provenance of material in the Tomboj VOC Signal-to-Change repository. It distinguishes original work from third-party material that was copied, adapted, or consulted as prior art.

## Original work

Unless otherwise identified, the repository's original methodology, skill instructions, schemas, examples, and future source code were created by Rachel Wilde / Tomboj.

The VOC Benchmark Builder and its VOC Monitoring Automation companion are original instructional work. No third-party code or prose was copied into either skill.

## Prior art consulted

| Project or source | Relevance | Treatment |
| --- | --- | --- |
| [GainTrace Customer Success Skills](https://github.com/gaintrace/customer-success-skills) | Broader Customer Success skill collection that includes Voice of Customer methods | Consulted only; no code or text copied |
| [Andrew Luxem — Voice of the Customer](https://github.com/andrewluxem/voice-of-the-customer) | Standalone skill for turning supplied feedback into themes and actions | Consulted only; no code or text copied |
| [Google Business Profile Reviews Monitor](https://github.com/abhi-ai-marketing/google-business-profile-reviews-monitor-workflow) | Example of review monitoring with Google Apps Script | Prior-art awareness only; not used as a code source because no license was identified during review |
| [OpenAI Skills](https://github.com/openai/skills) | Public examples of skill packaging and structure | General format reference only |
| [Anthropic Skills](https://github.com/anthropics/skills) | Public examples of portable agent skills | General format reference only |
| [SPDX License List Data](https://github.com/spdx/license-list-data) | Standard license texts | MIT and CC BY 4.0 legal texts used for the repository license files |
| [OpenAI API documentation](https://developers.openai.com/api/docs/) | Background execution, Batch API, model selection, usage, and pricing guidance | Consulted for `docs/model-evaluation.md`; no code or prose copied |
| [Claude Platform documentation](https://platform.claude.com/docs/) | Current models, batch processing, usage, caching, and pricing guidance | Consulted for `docs/model-evaluation.md`; no code or prose copied |
| [Kimi API Platform documentation](https://platform.kimi.ai/docs/overview) | Current models, Batch API, usage fields, tools, and pricing guidance | Consulted for `docs/model-evaluation.md`; no code or prose copied |
| [Google Apps Script and Workspace API documentation](https://developers.google.com/apps-script/) | Apps Script services, Drive conversion, OAuth, triggers, quotas, and Workspace APIs | Consulted for the VOC Monitoring Automation guide and Drive intake example; no code or prose copied |
| [Google Workspace MCP documentation](https://developers.google.com/workspace/guides/configure-mcp-servers) | OAuth-based AI-client connections to Workspace | Consulted for current connection options and access boundaries; no code or prose copied |
| [OpenAI API documentation](https://platform.openai.com/docs/api-reference/authentication), [Anthropic API documentation](https://docs.anthropic.com/en/api/getting-started), and [Gemini API documentation](https://ai.google.dev/gemini-api/docs/api-key) | Frontier-model API authentication and key handling | Consulted for the Step 2 integration guide; no credentials, code, or prose copied |
| Apps Script and Workspace repositories listed in the [field guide](docs/apps-script-workspace-field-guide.md) | Examples, ecosystem status, and new Workspace/MCP tooling | Descriptions and commit dates checked; linked as prior art only; no code or repository prose copied; licenses must be checked before reuse |

The [Benchmark Builder attribution record](skills/voc-benchmark-builder/ATTRIBUTIONS.md) and [Monitoring Automation attribution record](skills/voc-monitoring-automation/ATTRIBUTIONS.md) document the sources consulted for each skill.

## Required attribution for this project

For reuse of the original written material under CC BY 4.0, use a reasonable attribution such as:

> “Tomboj VOC Signal-to-Change” by Rachel Wilde / Tomboj, https://github.com/rtomboj/tomboj-voc-signal-to-change

For adaptations, also indicate that changes were made. Code distributed under the MIT License must retain its copyright and permission notice.

## Contributor provenance rule

When third-party material is added:

1. Record the project, author, source URL, license, version or commit, and affected files.
2. Classify the use as **Copied**, **Adapted**, or **Consulted only**.
3. Preserve all required copyright, license, and attribution notices.
4. Do not copy or adapt material from a repository without an explicit license or direct permission.
5. Prefer official platform documentation when implementing future connectors.
6. Keep Tomboj brand assets outside the reusable content and code licenses unless explicitly stated.

This file documents provenance and does not replace any applicable third-party license.

