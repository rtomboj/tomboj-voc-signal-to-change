# Model evaluation and background testing

This guide defines a repeatable way to compare the VOC Benchmark Builder across providers. Model names and prices change; verify the linked official pages before each evaluation.

Last reviewed: 2026-09-10.

## Separate the workload

The workflow contains two materially different jobs:

1. **Interactive research and judgment:** company identification, source discovery, identity checks, geography decisions, scope confirmation, and final interpretation.
2. **Repeatable classification:** applying a confirmed taxonomy to review records and returning structured fields.

Use a capable tool-using model for the first job. Use asynchronous batch processing on a lower-cost model for the second job, then audit a sample with the stronger model or a human reviewer. Build spreadsheet formulas and charts deterministically after the model returns structured data.

## What can run in the background

A real user run must pause for company, source, and scope confirmation. After those decisions are confirmed, evidence classification, workbook generation, and quality checks can run as a background job.

For an unattended model comparison, use a test fixture with the company profile, source scope, insight window, and source records already confirmed. This tests analysis and artifact creation without simulating human decisions.

Provider options:

- **OpenAI:** Responses API background mode runs a response asynchronously and supports status polling. Batch API is suited to review-by-review classification and offers a 50% discount with completion within 24 hours. See [background mode](https://developers.openai.com/api/docs/guides/background), [Batch API](https://developers.openai.com/api/docs/guides/batch), and [pricing](https://developers.openai.com/api/docs/pricing).
- **Anthropic:** Message Batches process classification requests asynchronously with a 50% input/output discount. See [batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing), [models](https://platform.claude.com/docs/en/models/overview), and [pricing](https://platform.claude.com/docs/en/about-claude/pricing).
- **Kimi:** Kimi Batch accepts JSONL jobs, exposes polling and per-request usage, and currently saves 40% versus real-time calls. It supports Kimi K2.6 and K2.7 Code; Kimi K3 is not currently supported in Batch. See [Batch API](https://platform.kimi.ai/docs/guide/use-batch-api), [quickstart](https://platform.kimi.ai/docs/overview), and [pricing](https://platform.kimi.ai/).

## Current starting models

These are candidates for evaluation, not a claim that one provider is universally best.

| Provider | Accurate interactive research | Efficient full run | Batch classification |
| --- | --- | --- | --- |
| OpenAI | GPT-6 Astra | GPT-5.6 Sol | GPT-5.6 Luna or Terra, audited by Sol/Astra |
| Anthropic | Claude Opus 5; use Fable 5.1 only when Opus evals fall short | Claude Sonnet 5 | Claude Haiku 4.5, audited by Sonnet/Opus |
| Kimi | Kimi K3 | Kimi K2.6 | Kimi K2.6 Batch, audited by K3 |

For the first controlled comparison, use **GPT-5.6 Sol, Claude Sonnet 5, and Kimi K3** for the complete workflow. Then compare their low-cost classification options on the same frozen review set.

## Record usage and cost

Store one run record with:

- run ID and test-fixture version;
- provider, requested model, and served model;
- reasoning or thinking setting;
- start time, completion time, and elapsed seconds;
- input, cached-input, output, and reasoning/thinking tokens when reported;
- tool calls, web searches, pages retrieved, and failed calls;
- number of review records classified;
- provider-reported cost or a dated price calculation;
- generated files and validation result;
- human-review minutes and corrections.

Token totals are not directly comparable across providers because tokenizers and billing treatments differ. Compare **total cost per accepted benchmark**, elapsed time, and quality as the primary measures.

## Quality score

Score each completed run out of 100:

| Area | Points |
| --- | ---: |
| Company and product identity | 10 |
| Source identity verification | 15 |
| Audience and geography integrity | 20 |
| Evidence traceability | 15 |
| Review classification quality | 15 |
| Workbook schema and technical validity | 10 |
| Visual usefulness and focus recommendations | 15 |

A run fails regardless of total score if it fabricates a source, labels an unfiltered global metric as country-specific, omits citations for material claims, or produces an invalid workbook.

## Two evaluation modes

### Live-agent test

Give each model only the same company website. Record its questions, searches, sources, token usage, time, and artifacts. This measures the complete user experience but is affected by changing web results.

### Frozen-evidence test

Give each model the same confirmed profile, source register, and set of review records. Require the same JSON schema and workbook contract. This is the better comparison for classification quality, token consumption, and reproducibility.

Run each model at least three times before drawing a conclusion. Preserve the exact prompt, model ID, reasoning setting, date, source fixture, and price table used.
