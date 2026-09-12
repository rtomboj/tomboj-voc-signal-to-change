#!/usr/bin/env python3
"""Validate a VOC Benchmark Builder .xlsx workbook before delivery.

This script uses only the Python standard library. It inspects the workbook's
OOXML package without opening, editing, or recalculating the workbook.
"""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple
from xml.etree import ElementTree as ET


MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CHART_NS = "http://schemas.openxmlformats.org/drawingml/2006/chart"
DRAWING_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"

NS = {"m": MAIN_NS, "r": REL_NS, "pr": PKG_REL_NS, "c": CHART_NS, "a": DRAWING_NS}

FORMULA_ERRORS = {"#NULL!", "#DIV/0!", "#VALUE!", "#REF!", "#NAME?", "#NUM!", "#N/A", "#GETTING_DATA"}

REQUIRED_COLUMNS: Dict[str, List[str]] = {
    "Company_Profile": [
        "Entity ID", "Company", "Parent", "Brand/Product", "Official URL",
        "Business Model", "Buyer Type", "User/Customer Type", "Delivery Model",
        "Country/Market", "Location Model", "In Scope", "Evidence URL",
        "Evidence Type", "User Confirmed", "Last Validated",
    ],
    "Source_Register": [
        "Source ID", "Source", "Profile URL", "Source Type", "Company/Brand/Product",
        "Requested Country/Market", "Source Aggregate Geography", "Geography Filterable",
        "Location", "Audience", "Identity Status", "Verification Evidence",
        "Identity Confidence", "Audience Fit", "Benchmark Role", "Accessible History",
        "Sample Method", "Inclusion Status", "Week 2 Collection Method",
        "Access or Permission Notes", "Last Validated",
    ],
    "Baseline_Snapshot": [
        "Snapshot Date", "Source ID", "Company/Brand/Product", "Country/Market Claimed",
        "Source Aggregate Geography", "Location", "Rating Value", "Rating Scale",
        "Review Count", "Latest Review Date", "Reviews Last 30 Days", "Reviews Last 90 Days",
        "Reviews Last 365 Days", "Company Responses Visible", "Response Rate",
        "Measure Status", "Evidence URL", "Notes",
    ],
    "Review_Data": [
        "Record ID", "Source ID", "Stable Source Record ID", "Source Type", "Evidence Class",
        "Direct URL", "Capture Date", "Record Date", "Company/Brand/Product",
        "Requested Country/Market", "Source-Reported Geography", "Geography Confidence",
        "Location", "Rating Value", "Rating Scale", "Audience", "Audience Fit",
        "Short Evidence Excerpt", "Company Response Visible", "Collection Coverage",
        "Journey Stage", "Primary Theme", "Secondary Theme", "Signal Type",
        "Operational Impact", "Classification Confidence", "Human Review Needed", "Notes",
    ],
    "Theme_Taxonomy": [
        "Theme ID", "Theme", "Parent Theme", "Definition", "Include When", "Exclude When",
        "Relevant Journey Stages", "Relevant Audiences", "Example Terms", "User Confirmed",
        "Last Updated",
    ],
    "Discussion_Snapshot": [
        "Snapshot Date", "Source ID", "Community/Forum", "Search Scope",
        "Relevant Threads Found", "Most Recent Relevant Date", "Representative Thread URLs",
        "Participant Identity Caveat", "Geography Caveat", "Evidence Status", "Notes",
    ],
    "Signal_to_Focus": [
        "Theme", "Audience", "Journey Stage", "Positive Count", "Negative Count",
        "Mixed/Request Count", "Total Classified Records", "Most Recent Signal", "Impact",
        "Evidence Class(es)", "Independent Cross-Source Support", "Corroboration Status",
        "Classification Confidence", "Evidence Strength", "Prevalence Confidence",
        "Coverage Limitation", "Focus Category", "Evidence Pattern", "Rationale",
        "What Would Confirm or Challenge It", "Internal Evidence Needed",
    ],
    "Coverage_Gaps": [
        "Channel or Audience", "Expected/Relevant", "Covered", "Geography Covered",
        "Period Covered", "Gap Description", "Impact on Interpretation",
        "Recommended Next Step", "Step",
    ],
    "Week2_Readiness": [
        "Source ID", "Source", "Access Method", "Authentication/Ownership Requirement",
        "Proposed Schedule", "Stable Identifier/Deduplication Key", "First-Run Baseline Rule",
        "Accessible Fields", "Known Limitations", "Automation Permission Status",
        "Failure Signal", "Readiness Status",
    ],
    "Evidence_Log": [
        "Evidence ID", "Claim or Measure", "Source Name", "Direct URL", "Accessed Date",
        "Evidence Type", "Observed/Calculated/Inferred/User-provided", "Geography Supported",
        "Audience Supported", "Notes",
    ],
}

REQUIRED_TABS = ["Executive_Dashboard", *REQUIRED_COLUMNS.keys()]

DASHBOARD_SECTIONS = [
    "What this means",
    "What looks good",
    "Where friction appears",
    "What may be emerging",
    "Where to focus next",
]

EVIDENCE_CLASSES = [
    "Independent reviews",
    "Vendor-selected customer stories",
    "Official operational evidence",
    "Public discussions",
    "Complaints",
    "Other",
]

FREEZE_RULES = {
    "Review_Data": (4, 4),
    "Signal_to_Focus": (3, 4),
}


def qname(namespace: str, name: str) -> str:
    return f"{{{namespace}}}{name}"


def normalize(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip()).casefold()


def column_number(cell_ref: str) -> int:
    letters = re.match(r"[A-Z]+", cell_ref.upper())
    if not letters:
        return 0
    value = 0
    for char in letters.group(0):
        value = value * 26 + ord(char) - 64
    return value


def resolve_part(source_part: str, target: str) -> str:
    if target.startswith("/"):
        return target.lstrip("/")
    return posixpath.normpath(posixpath.join(posixpath.dirname(source_part), target))


@dataclass
class Result:
    workbook: str
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    passes: List[str] = field(default_factory=list)
    manual_review: List[str] = field(default_factory=lambda: [
        "Confirm dashboard statements trace to Review_Data or Evidence_Log.",
        "Confirm observed facts, AI classifications, calculations, and recommendations are visibly distinct.",
        "Confirm status colors have text labels and legends and do not imply unsupported strength.",
        "Confirm evidence classes are not blended in sentiment totals or charts.",
        "Confirm every chart states its evidence class, timeframe, audience, geography, and denominator where relevant.",
        "Confirm narrative text is readable and no content is visually clipped.",
    ])

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def passed(self, message: str) -> None:
        self.passes.append(message)


class WorkbookInspector:
    def __init__(self, path: Path, result: Result):
        self.path = path
        self.result = result
        self.archive = zipfile.ZipFile(path)
        self.shared_strings = self._load_shared_strings()
        self.sheets = self._load_sheet_paths()
        self.cells: Dict[str, Dict[str, str]] = {}
        self.cell_styles: Dict[str, Dict[str, Optional[int]]] = {}
        self.style_xfs, self.fonts = self._load_styles()
        for sheet_name, sheet_path in self.sheets.items():
            self.cells[sheet_name], self.cell_styles[sheet_name] = self._load_cells(sheet_path)

    def close(self) -> None:
        self.archive.close()

    def _xml(self, path: str) -> ET.Element:
        return ET.fromstring(self.archive.read(path))

    def _load_shared_strings(self) -> List[str]:
        if "xl/sharedStrings.xml" not in self.archive.namelist():
            return []
        root = self._xml("xl/sharedStrings.xml")
        values = []
        for item in root.findall("m:si", NS):
            values.append("".join(node.text or "" for node in item.iter(qname(MAIN_NS, "t"))))
        return values

    def _load_sheet_paths(self) -> Dict[str, str]:
        workbook_path = "xl/workbook.xml"
        workbook = self._xml(workbook_path)
        rels = self._xml("xl/_rels/workbook.xml.rels")
        targets = {
            rel.attrib["Id"]: resolve_part(workbook_path, rel.attrib["Target"])
            for rel in rels.findall("pr:Relationship", NS)
        }
        output = {}
        for sheet in workbook.findall("m:sheets/m:sheet", NS):
            rel_id = sheet.attrib.get(qname(REL_NS, "id"))
            if rel_id in targets:
                output[sheet.attrib["name"]] = targets[rel_id]
        return output

    def _load_styles(self) -> Tuple[List[Tuple[int, bool, str]], List[str]]:
        if "xl/styles.xml" not in self.archive.namelist():
            return [], []
        root = self._xml("xl/styles.xml")
        fonts = []
        for font in root.findall("m:fonts/m:font", NS):
            name = font.find("m:name", NS)
            fonts.append(name.attrib.get("val", "") if name is not None else "")
        xfs = []
        for xf in root.findall("m:cellXfs/m:xf", NS):
            alignment = xf.find("m:alignment", NS)
            wrap = alignment is not None and alignment.attrib.get("wrapText") in {"1", "true"}
            vertical = alignment.attrib.get("vertical", "") if alignment is not None else ""
            xfs.append((int(xf.attrib.get("fontId", "0")), wrap, vertical))
        return xfs, fonts

    def _cell_value(self, cell: ET.Element) -> str:
        kind = cell.attrib.get("t")
        if kind == "inlineStr":
            inline = cell.find("m:is", NS)
            return "" if inline is None else "".join(n.text or "" for n in inline.iter(qname(MAIN_NS, "t")))
        value = cell.findtext("m:v", default="", namespaces=NS)
        if kind == "s" and value:
            try:
                return self.shared_strings[int(value)]
            except (ValueError, IndexError):
                return value
        if kind == "b":
            return "TRUE" if value == "1" else "FALSE"
        return value

    def _load_cells(self, sheet_path: str) -> Tuple[Dict[str, str], Dict[str, Optional[int]]]:
        root = self._xml(sheet_path)
        values: Dict[str, str] = {}
        styles: Dict[str, Optional[int]] = {}
        for cell in root.findall(".//m:sheetData/m:row/m:c", NS):
            ref = cell.attrib.get("r", "")
            value = self._cell_value(cell)
            if ref and value != "":
                values[ref] = value
                try:
                    styles[ref] = int(cell.attrib.get("s", "0"))
                except ValueError:
                    styles[ref] = None
        return values, styles

    def row_values(self, sheet_name: str, row_number: int) -> List[str]:
        row = [
            (column_number(ref), value)
            for ref, value in self.cells.get(sheet_name, {}).items()
            if re.search(r"\d+$", ref) and int(re.search(r"\d+$", ref).group(0)) == row_number
        ]
        if not row:
            return []
        max_col = max(column for column, _ in row)
        values = [""] * max_col
        for column, value in row:
            values[column - 1] = value
        while values and values[-1] == "":
            values.pop()
        return values

    def all_text(self, sheet_name: str) -> List[str]:
        return list(self.cells.get(sheet_name, {}).values())

    def validate_tabs(self) -> None:
        missing = [name for name in REQUIRED_TABS if name not in self.sheets]
        if missing:
            self.result.fail("Missing required tab(s): " + ", ".join(missing))
        else:
            self.result.passed("All 11 required tabs are present with exact names.")

    def validate_headers(self) -> None:
        failed = 0
        for sheet_name, required in REQUIRED_COLUMNS.items():
            if sheet_name not in self.sheets:
                continue
            match_row = None
            closest: Tuple[int, List[str]] = (0, [])
            for row_number in range(1, 21):
                values = self.row_values(sheet_name, row_number)
                matched = sum(
                    1 for index, header in enumerate(required)
                    if index < len(values) and normalize(values[index]) == normalize(header)
                )
                if matched > closest[0]:
                    closest = (matched, values)
                if len(values) >= len(required) and all(
                    normalize(values[index]) == normalize(header)
                    for index, header in enumerate(required)
                ):
                    match_row = row_number
                    break
            if match_row is None:
                failed += 1
                found = closest[1]
                missing = [header for header in required if normalize(header) not in {normalize(v) for v in found}]
                details = f"; missing/renamed: {', '.join(missing[:6])}"
                if len(missing) > 6:
                    details += f" (+{len(missing) - 6} more)"
                self.result.fail(
                    f"{sheet_name}: exact required header sequence was not found in rows 1-20{details}. "
                    "Do not rename, remove, combine, transpose, or reorder required fields."
                )
        if failed == 0:
            self.result.passed("All structured tabs contain the exact required headers in order.")

    def validate_dashboard(self) -> None:
        if "Executive_Dashboard" not in self.sheets:
            return
        normalized_cells = [normalize(value) for value in self.all_text("Executive_Dashboard")]

        missing_sections = [
            label for label in DASHBOARD_SECTIONS
            if not any(normalize(label) in value for value in normalized_cells)
        ]
        if missing_sections:
            self.result.fail("Executive_Dashboard is missing required section label(s): " + ", ".join(missing_sections))
        else:
            self.result.passed("Executive_Dashboard contains all required interpretation sections.")

        missing_classes = [
            label for label in EVIDENCE_CLASSES
            if not any(normalize(label) in value for value in normalized_cells)
        ]
        if missing_classes:
            self.result.fail(
                "Executive_Dashboard evidence-class coverage table is incomplete; missing label(s): "
                + ", ".join(missing_classes)
            )
        else:
            self.result.passed("Executive_Dashboard includes all required evidence-class coverage labels.")

    def validate_formula_errors(self) -> None:
        errors = []
        for sheet_name, sheet_path in self.sheets.items():
            root = self._xml(sheet_path)
            for cell in root.findall(".//m:c", NS):
                value = self._cell_value(cell).strip().upper()
                if cell.attrib.get("t") == "e" or value in FORMULA_ERRORS:
                    errors.append(f"{sheet_name}!{cell.attrib.get('r', '?')}={value or 'formula error'}")
        if errors:
            self.result.fail("Formula error value(s) found: " + ", ".join(errors[:10]))
        else:
            self.result.passed("No cached Excel formula errors were found.")

    def _freeze_splits(self, sheet_name: str) -> Tuple[int, int]:
        root = self._xml(self.sheets[sheet_name])
        pane = root.find("m:sheetViews/m:sheetView/m:pane", NS)
        if pane is None or pane.attrib.get("state") not in {"frozen", "frozenSplit"}:
            return 0, 0
        return int(float(pane.attrib.get("xSplit", "0"))), int(float(pane.attrib.get("ySplit", "0")))

    def validate_freeze_panes(self) -> None:
        for sheet_name, expected in FREEZE_RULES.items():
            if sheet_name not in self.sheets:
                continue
            actual = self._freeze_splits(sheet_name)
            if actual != expected:
                self.result.fail(
                    f"{sheet_name}: freeze panes are x={actual[0]}, y={actual[1]}; "
                    f"required x={expected[0]}, y={expected[1]}."
                )
            else:
                self.result.passed(f"{sheet_name} has the required freeze panes.")

    def validate_cell_styles(self) -> None:
        if not self.style_xfs or not self.fonts:
            self.result.fail("Workbook styles could not be inspected; styles.xml is missing or incomplete.")
            return
        wrong_font: List[str] = []
        no_wrap: List[str] = []
        wrong_vertical: List[str] = []
        for sheet_name, refs in self.cell_styles.items():
            for ref, style_id in refs.items():
                if style_id is None or style_id >= len(self.style_xfs):
                    self.result.warn(f"{sheet_name}!{ref}: invalid or missing cell style reference.")
                    continue
                font_id, wrap, vertical = self.style_xfs[style_id]
                font_name = self.fonts[font_id] if font_id < len(self.fonts) else ""
                if normalize(font_name) != "calibri":
                    wrong_font.append(f"{sheet_name}!{ref} ({font_name or 'unspecified'})")
                if not wrap:
                    no_wrap.append(f"{sheet_name}!{ref}")
                if normalize(vertical) != "center":
                    wrong_vertical.append(f"{sheet_name}!{ref}")
        for label, items in [
            ("Non-Calibri populated cells", wrong_font),
            ("Populated cells without text wrapping", no_wrap),
            ("Populated cells not vertically centered", wrong_vertical),
        ]:
            if items:
                preview = ", ".join(items[:8])
                suffix = f" (+{len(items) - 8} more)" if len(items) > 8 else ""
                self.result.fail(f"{label}: {preview}{suffix}.")
        if not (wrong_font or no_wrap or wrong_vertical):
            self.result.passed("All populated cells use Calibri, text wrapping, and vertical centering.")

    def _range_values(self, formula: str) -> Optional[List[str]]:
        match = re.fullmatch(
            r"'?((?:[^']|'')+)'?!\$?([A-Z]+)\$?(\d+)(?::\$?([A-Z]+)\$?(\d+))?",
            formula.strip(),
        )
        if not match:
            return None
        sheet_name = match.group(1).replace("''", "'")
        if sheet_name not in self.cells:
            return []
        start_col, start_row = column_number(match.group(2)), int(match.group(3))
        end_col = column_number(match.group(4) or match.group(2))
        end_row = int(match.group(5) or match.group(3))
        output = []
        for row in range(start_row, end_row + 1):
            for column in range(start_col, end_col + 1):
                letters = ""
                value = column
                while value:
                    value, remainder = divmod(value - 1, 26)
                    letters = chr(65 + remainder) + letters
                output.append(self.cells[sheet_name].get(f"{letters}{row}", ""))
        return output

    def validate_charts(self) -> None:
        chart_paths = sorted(
            name for name in self.archive.namelist()
            if name.startswith("xl/") and "/charts/chart" in name and name.endswith(".xml")
        )
        if not chart_paths:
            self.result.fail("No native editable Excel charts were found.")
            return

        bad_ranges: List[str] = []
        long_label_violations: List[str] = []
        unresolved: List[str] = []
        for chart_path in chart_paths:
            root = self._xml(chart_path)
            bar_chart = root.find(".//c:barChart", NS)
            horizontal = False
            if bar_chart is not None:
                direction = bar_chart.find("c:barDir", NS)
                horizontal = direction is not None and direction.attrib.get("val") == "bar"
            for formula_node in root.findall(".//c:ser//c:f", NS):
                formula = formula_node.text or ""
                values = self._range_values(formula)
                if values is None:
                    unresolved.append(f"{chart_path}: {formula}")
                elif not any(str(value).strip() for value in values):
                    bad_ranges.append(f"{chart_path}: {formula}")
            for category_formula in root.findall(".//c:ser/c:cat//c:f", NS):
                values = self._range_values(category_formula.text or "")
                if values and any(len(str(value).strip()) > 24 for value in values) and not horizontal:
                    long_label_violations.append(chart_path)

        if bad_ranges:
            self.result.fail("Chart source range(s) are empty or broken: " + ", ".join(bad_ranges[:8]))
        else:
            self.result.passed(f"Found {len(chart_paths)} native chart(s) with non-empty resolvable source ranges.")
        if long_label_violations:
            self.result.fail(
                "Chart(s) with category labels longer than 24 characters are not horizontal: "
                + ", ".join(sorted(set(long_label_violations)))
            )
        else:
            self.result.passed("Charts with resolvable category labels longer than 24 characters use horizontal bars.")
        if unresolved:
            self.result.warn(
                f"Could not automatically resolve {len(unresolved)} chart formula range(s); review them manually."
            )

    def run(self) -> None:
        self.validate_tabs()
        self.validate_headers()
        self.validate_dashboard()
        self.validate_formula_errors()
        self.validate_freeze_panes()
        self.validate_cell_styles()
        self.validate_charts()


def format_text(result: Result) -> str:
    status = "PASS" if not result.errors else "FAIL"
    lines = [f"VOC workbook validation: {status}", f"Workbook: {result.workbook}"]
    if result.passes:
        lines.extend(["", f"Passed ({len(result.passes)}):"] + [f"  + {item}" for item in result.passes])
    if result.errors:
        lines.extend(["", f"Errors ({len(result.errors)}):"] + [f"  - {item}" for item in result.errors])
    if result.warnings:
        lines.extend(["", f"Warnings ({len(result.warnings)}):"] + [f"  ! {item}" for item in result.warnings])
    lines.extend(["", "Manual review still required:"] + [f"  * {item}" for item in result.manual_review])
    return "\n".join(lines)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a VOC Benchmark Builder Excel workbook.")
    parser.add_argument("workbook", type=Path, help="Path to the .xlsx workbook")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    result = Result(workbook=str(args.workbook))
    if not args.workbook.is_file():
        result.fail("Workbook file does not exist.")
    elif args.workbook.suffix.casefold() != ".xlsx":
        result.fail("Workbook must be an .xlsx file.")
    else:
        try:
            inspector = WorkbookInspector(args.workbook, result)
            try:
                inspector.run()
            finally:
                inspector.close()
        except (zipfile.BadZipFile, KeyError, ET.ParseError, OSError, ValueError) as exc:
            result.fail(f"Workbook could not be inspected: {exc}")

    if args.json:
        print(json.dumps({
            "status": "pass" if not result.errors else "fail",
            "workbook": result.workbook,
            "passes": result.passes,
            "errors": result.errors,
            "warnings": result.warnings,
            "manual_review": result.manual_review,
        }, indent=2))
    else:
        print(format_text(result))
    return 0 if not result.errors else 1


if __name__ == "__main__":
    sys.exit(main())
