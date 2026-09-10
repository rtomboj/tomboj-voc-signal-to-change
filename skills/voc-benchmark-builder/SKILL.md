---
name: voc-benchmark-builder
description: Research a company, confirm its business and market profile, discover and validate relevant public customer-feedback sources, and establish a cited external Voice of Customer benchmark with a defined insight window, starter taxonomy, visual analysis, and focus recommendations. Use when starting a company-specific VOC baseline before monitoring or closed-loop automation. Do not use this skill to automate ongoing collection, scrape restricted sites, or treat public reviews as the complete Voice of Customer.
---

# VOC Benchmark Builder

Build a company-specific external Voice of Customer benchmark through progressive research and confirmation. Start with the smallest useful input, research what can be established reliably, and ask the user to confirm decisions that materially change the benchmark.

This is Step 1 of a broader progression:

1. **Benchmark:** identify where customers speak, establish the current position, and show what the available evidence suggests.
2. **Monitor:** automate permitted ongoing collection and change detection.
3. **Close the loop:** route, resolve, communicate, and learn from feedback.

Complete only Step 1 unless the user explicitly asks to continue.

## Human-facing interaction

Make the process feel like a guided conversation, not a technical audit or intake form.

- Ask one focused confirmation question at a time when possible. Batch only closely related corrections.
- Explain what you are checking and why in plain language.
- Do not mention that the skill directed you to read a reference file, internal instruction, schema, or tool.
- Keep progress updates short and useful. Example: “I’m checking the company’s products, customers, markets, and public presence. Then I’ll show you a short profile to confirm.”
- Do not require the user to re-enter facts already supported by reliable sources.
- At each confirmation point, show a compact recommendation and the decision the user is confirming.
- Lead the final deliverable with a concise “what this means” summary before the detailed evidence.

## Interaction model

1. Ask only for the company website. If it is unavailable or ambiguous, also ask for the company name and primary market.
2. Research the company and present a compact draft profile for confirmation.
3. Discover likely public feedback sources and present a proposed source map.
4. Separate source identity, audience alignment, and analytic role; do not use one label to represent all three.
5. Recommend an insight window and sampling approach based on available source history.
6. Ask the user to confirm the source scope, geography, audiences, insight window, and whether competitor comparison is included.
7. Capture the platform baseline and accessible review-level evidence.
8. Draft a company-specific theme taxonomy, classify the evidence, and show the user what appears to be working, what needs attention, and what remains uncertain.
9. Create the benchmark package and monitoring-readiness specification.

## Stage 1: Draft and confirm the company profile

Read [company-profile.md](references/company-profile.md) and follow it to identify:

- company and website identity;
- parent company, brands, products, and material aliases;
- B2B, B2C, B2B2C, marketplace, nonprofit, or mixed model;
- customer and user types;
- physical-location, web, mobile-app, marketplace, or hybrid delivery;
- countries, markets, regions, languages, and location footprint;
- material distinctions between buyers, users, consumers, partners, and locations.

Use current web research. Cite the official company sources used. Treat the profile as a draft until the user confirms it. Ask “Is this the right company, and is this profile accurate?” rather than asking whether it is a “good” company.

Do not judge reputation at this stage. Use identity confidence, profile completeness, and evidence quality.

## Stage 2: Discover and validate public VOC sources

After the company profile is confirmed, read [source-discovery.md](references/source-discovery.md).

Let the confirmed company profile determine the search. Search general and industry-specific review platforms, app stores, marketplaces, public discussions, complaint sources, directories, and relevant physical-location profiles.

For every candidate, verify that it belongs to the correct company, brand, product, market, location, or app. Never invent a profile because the source seems likely. If identity remains ambiguous, label it **Needs confirmation** and ask the user.

For each source, record three separate decisions:

1. **Identity status:** Verified, Probable, Needs confirmation, or Rejected.
2. **Audience fit:** Primary, Mixed, Secondary, or Unknown.
3. **Benchmark role:** Quantitative baseline, Contextual signal, Watchlist, or Excluded.

Keep rated reviews, complaints, and public discussion analytically separate. Do not combine Reddit threads, forum activity, complaint counts, and star ratings into one score.

## Stage 3: Confirm scope and insight window

Present the proposed source register before capturing the benchmark. For each source show:

- verified profile URL and entity covered;
- source type and why it matters;
- identity status and confidence;
- audience fit;
- geography visible in the source and whether the requested market can be filtered;
- benchmark role;
- accessible history and proposed sampling method;
- likely Week 2 collection method.

Recommend a default **12-month insight window** for review-level analysis. If the full period cannot be accessed through permitted means, propose a transparent recent sample and disclose the number of items and dates covered. Preserve all-time platform totals as a separate point-in-time baseline.

Ask the user to confirm:

- brands, products, countries, markets, and physical locations in scope;
- primary, mixed, and secondary audiences to include;
- the insight window and any sampling limits;
- whether competitor comparison is wanted now or later.

Default to benchmarking the company against itself. Do not choose competitors without user confirmation.

## Stage 4: Capture the baseline and review-level evidence

After scope confirmation, read [benchmark-output.md](references/benchmark-output.md) and create a dated platform snapshot. Then read [insight-analysis.md](references/insight-analysis.md) and capture the accessible review-level evidence needed for classification and visual analysis.

Record unavailable metrics as `Not publicly available`; do not estimate them. Distinguish Observed, Calculated, User-provided, and Inferred information.

Enforce the confirmed geography. If a platform aggregate or review sample cannot be filtered to the requested market, label its geography **Global/unknown** and use it only at that scope. Never present an unfiltered global measurement as a country-specific benchmark.

Do not bypass authentication, pagination controls, CAPTCHAs, robots controls, paywalls, or platform restrictions. When permitted history is limited, disclose the limitation instead of implying complete coverage.

## Stage 5: Classify, visualize, and connect the dots

Use [insight-analysis.md](references/insight-analysis.md) to:

- draft a company-specific theme and journey-stage taxonomy;
- classify the accessible feedback while preserving audience and source distinctions;
- quantify themes using explicit numerators and denominators;
- identify positive strengths, friction, emerging signals, and unanswered questions;
- create the required dashboard visuals;
- produce a directional Signal-to-Focus Map with evidence and confidence.

AI classifications are analytical labels, not source facts. Mark classification confidence and keep a short excerpt plus direct source URL so a person can trace each material conclusion. Do not infer prevalence beyond the collected sample.

## Required output

Create a custom company benchmark package containing:

1. Executive “What this means” summary
2. Confirmed Company Profile
3. Source Register
4. Platform Baseline Snapshot
5. Review-Level Insight Dataset and Coverage Statement
6. Starter Theme Taxonomy
7. Visual Insight Dashboard
8. Signal-to-Focus Map
9. External VOC Coverage and Gaps
10. Week 2 Monitoring-Readiness Specification
11. Evidence and Attribution Log
12. Assumptions and Open Questions

If spreadsheet creation is available, create a tailored workbook using the exact core tab and field definitions in [benchmark-output.md](references/benchmark-output.md). Validate every required tab and column before delivery. Otherwise provide copy-ready Markdown or CSV tables. Do not create automation code during Step 1.

Create a written brief named `[company-slug]-voc-benchmark.md` plus the workbook when available. The final brief must state the platform-baseline date, review-level insight window, number of items analyzed by source and audience, and any geography or access limitations.

## Evidence and safety rules

- Use live web research; cite every profile and material company fact with a direct URL.
- If current web search is unavailable, say so and ask the user to enable it or provide source URLs.
- Prefer official company pages and the platform’s own profile over aggregators or search snippets.
- State when a site was checked but no verified profile was found.
- Do not recommend scraping when an official API, notification, export, or manual method is the permitted route.
- Do not reproduce full reviews. Capture only necessary fields and short excerpts, respecting source terms and applicable rights.
- Do not infer company-wide sentiment, market representativeness, or company quality from public ratings or a review sample.
- Do not expose personal reviewer information beyond what is necessary and already public.
- Public reviews are an external VOC channel, not the complete Voice of Customer. Inventory missing internal channels.

## Stop condition

End Step 1 when the user has a confirmed company profile and source scope, a dated platform baseline, a disclosed review-level insight window, traceable classifications, visual findings, a directional focus map, a coverage-gap statement, and source-by-source readiness notes for Week 2. Offer monitoring automation as the next step, but do not implement it unless requested.
