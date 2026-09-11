# Workbook visual standard

Use this standard for the Step 1 `.xlsx` workbook. The goal is to make the evidence easy to scan and the interpretation easy to understand while keeping every chart and conclusion traceable.

## Brand structure

- Use **Calibri** throughout the workbook, including chart titles, axes, legends, tables, and notes.
- Use Tomboj charcoal `#1D1D1D` for primary text and dark section or column headers.
- Use Tomboj teal `#2C9E90` for major section bands, primary chart series, and restrained accents.
- Use light teal `#D9F0ED` for supporting fills and white `#FFFFFF` for the main canvas.
- Use muted gray `#667085` for secondary text, light gray `#F2F4F7` for neutral fills, and `#D0D5DD` for borders.
- Keep the layout clean and spacious. Do not reproduce the Tomboj website as an interface.

Tomboj names, logos, and brand identifiers are not licensed for third-party reuse unless explicitly stated. The colors above define the visual direction for Tomboj-produced workbook outputs.

## Evidence and status colors

Use the following five-color sequence only when color communicates a labeled evidence state:

| Meaning | Hex |
| --- | --- |
| Positive | `#8CD47E` |
| Strong or confirmed positive | `#7ABD7E` |
| Mixed or uncertain | `#F8D66D` |
| Needs attention or watch | `#FFB54C` |
| Negative or friction | `#FF6961` |

Rules:

- Include a compact legend when two or more status colors appear.
- Never use color as the only signal; include a text label such as `Positive`, `Mixed`, `Watch`, or `Negative`.
- Use dark text on these fills unless contrast testing requires otherwise.
- Use neutral gray—not red—for unknown, unavailable, or not-yet-classified data.
- Do not use status colors as decoration or to imply evidence strength that the data does not support.

Palette source: [SchemeColor — Soft Green, Orange & Red](https://www.schemecolor.com/soft-green-orange-red.php).

## Cell alignment and readability

- Turn on text wrapping for every populated cell.
- Vertically center text in cells.
- Horizontally center headers, short labels, statuses, and compact metric cells.
- Left-align narrative text, excerpts, evidence, rationales, URLs, and open questions.
- Right-align numeric measures when that improves comparison.
- Increase row height and column width enough to prevent clipped text.
- Freeze the title and header rows on long data tabs and enable filters where useful.
- On `Review_Data`, freeze the top four rows and the first four identifying columns so source and record identity remain visible while scrolling.
- On `Signal_to_Focus`, freeze the top four rows and the first three identifying columns.
- On other wide tables, freeze the identifying columns needed to retain context, not only the header row.

## Dashboard and charts

Arrange the executive view in this order:

1. What this means
2. Timeframe, sources, audiences, geographies, and record coverage
3. What looks good, where friction appears, what may be emerging, and where to focus next
4. Charts supported by the available data
5. Signal-to-Focus view with evidence pattern, confidence, and what would confirm or challenge the recommendation
6. Visible limitations and unanswered questions

Use native editable spreadsheet charts linked to workbook data. Use Tomboj teal for general metric series and the status palette only where it encodes a labeled meaning. Do not average unlike rating scales or combine ratings, complaint counts, and discussion volume into a composite score. If the data does not support a chart, use a labeled table and explain what is missing.

Keep evidence classes visually distinct:

- chart independent reviews and complaints separately from vendor-selected customer stories;
- label vendor-selected evidence as `Reported customer outcomes`, not independent sentiment;
- show official operational evidence as corroboration in a separate table, marker, or panel;
- never let vendor-selected positive stories visually or numerically offset independent negative feedback.

Include a compact evidence-class coverage table on the dashboard. Show the number of records collected for independent reviews, vendor-selected customer stories, official operational evidence, public discussions, complaints, and other evidence. Use `0` or `Not available` when applicable rather than silently omitting a class.

Use a horizontal bar chart whenever any displayed theme or category label exceeds 24 characters. Do not abbreviate a meaningful label to avoid this rule. Every chart must identify its evidence class, date range, denominator or population basis, audience, and geography where relevant.

## Visual quality assurance

Before delivery:

1. Confirm Calibri is applied to every sheet and chart.
2. Confirm populated cells wrap and are vertically centered.
3. Confirm narrative text is not clipped and headers remain readable.
4. Confirm charts are editable, labeled, and connected to non-empty data ranges.
5. Confirm status colors have labels and a legend where needed.
6. Confirm formulas show no errors and dashboard statements trace to evidence.
7. Confirm independent feedback, vendor-selected outcomes, and corroborating operational evidence are not blended in one sentiment chart.
8. Confirm long labels are readable and wide sheets preserve identifying columns while scrolling.
9. Confirm the dashboard shows record counts by evidence class, including collected classes that do not appear in sentiment charts.
10. Confirm charts with a theme or category label longer than 24 characters use horizontal bars.
