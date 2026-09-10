# Tomboj VOC Signal-to-Change

An AI-guided system for finding where customers are speaking, establishing a defensible Voice of Customer benchmark, monitoring new feedback, and turning what is learned into action.

## The system

| Step | Question | Outcome | Status |
| --- | --- | --- | --- |
| 1. Establish the benchmark | Where are customers speaking, and what does the current position look like? | Confirmed company profile, validated source register, dated benchmark, coverage gaps, and monitoring-readiness specification | Available |
| 2. Automate monitoring | How will we detect new feedback and changes? | Scheduled collection, deduplication, logging, alerts, and source health checks | Planned |
| 3. Close the loop | What happens after feedback arrives? | Ownership, response and resolution SLAs, escalation, learning, and systemic change | Planned |

## Step 1: VOC Benchmark Builder

The [VOC Benchmark Builder](skills/voc-benchmark-builder/SKILL.md) is a portable set of instructions for an AI assistant with current web-research capability.

It begins with one question:

> What is the company website you want to benchmark?

The assistant then:

1. Researches the company, brands, products, buyers, users, delivery model, locations, countries, and markets.
2. Presents a draft company profile for confirmation.
3. Searches for relevant public feedback across review platforms, app stores, marketplaces, Reddit, forums, complaint sources, and industry-specific directories.
4. Separates verified profiles, plausible candidates, rejected matches, and sources checked but not found.
5. Asks the user to confirm the benchmark scope.
6. Produces a company-specific benchmark and a source-by-source specification for Step 2.

The skill does not treat public reviews as the whole Voice of Customer, combine discussion activity with star ratings, bypass platform restrictions, or generate monitoring automation during Step 1.

## Use the skill

Download or clone this repository and provide the complete `skills/voc-benchmark-builder/` folder to an AI environment that supports skills or project instructions.

- If the environment supports named skills, invoke `$voc-benchmark-builder`.
- Otherwise, ask the assistant to follow `SKILL.md` and make the files in `references/` available when requested.
- Enable current web research. The skill is designed to stop rather than fabricate a researched benchmark when live search is unavailable.

Example starting prompt:

> Use the VOC Benchmark Builder to establish an external customer-feedback benchmark for my company.

## Step 1 outputs

The company-specific package contains:

- Confirmed Company Profile
- Source Register
- Baseline Snapshot
- External VOC Coverage and Gaps
- Benchmark Observations
- Week 2 Monitoring-Readiness Specification
- Evidence and Attribution Log
- Assumptions and Open Questions

When spreadsheet creation is available, the skill also specifies a tailored benchmark workbook and dashboard.

## Repository structure

```text
skills/
└── voc-benchmark-builder/
    ├── SKILL.md
    ├── ATTRIBUTIONS.md
    ├── agents/
    │   └── openai.yaml
    └── references/
        ├── benchmark-output.md
        ├── company-profile.md
        └── source-discovery.md
```

## Attribution and provenance

The project is original instructional work informed by existing Voice of Customer methods, public skill conventions, and prior-art repositories. See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for the repository-level provenance policy and the skill's [detailed attribution record](skills/voc-benchmark-builder/ATTRIBUTIONS.md).

## Licensing

This repository uses two licenses:

| Material | License |
| --- | --- |
| Original written methodology, skill instructions, templates, examples, and documentation | [Creative Commons Attribution 4.0 International](LICENSE-CONTENT.md) |
| Source code, scripts, formulas, and executable utilities | [MIT License](LICENSE-CODE.md) |

Third-party materials retain their original licenses and notices. Tomboj names, logos, and other brand identifiers are not granted for reuse by these licenses unless explicitly stated.

## Author

Created by **Rachel Wilde / Tomboj**.

If you use or adapt this work, please preserve the requested attribution and indicate material changes. Citation metadata is available in [CITATION.cff](CITATION.cff).
