#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read-only structural audit for monthly keirin CSV files.

This script never edits source CSVs. It reports malformed row widths, missing
keys, duplicate rider rows, and whether race-result fields are populated.
Run: python scripts/audit_data.py
"""
import csv
import json
from collections import Counter
from pathlib import Path

DATA_DIR = Path("keirin_data")
OUT = DATA_DIR / "audit_report.json"
REQUIRED = ("race_id", "date", "race_no", "banum", "player_name", "pref")
RESULT_FIELDS = ("rank", "san_ren_tan")


def audit_file(path: Path) -> dict:
    report = {
        "file": path.name,
        "bytes": path.stat().st_size,
        "header_columns": 0,
        "rows": 0,
        "malformed_width_rows": 0,
        "malformed_examples": [],
        "missing_required": Counter(),
        "duplicate_race_rider_rows": 0,
        "unique_races": 0,
        "rank_populated_rows": 0,
        "trifecta_populated_rows": 0,
        "suspicious_pref_rows": 0,
        "suspicious_pref_examples": [],
        "parse_errors": 0,
    }
    race_ids = set()
    seen_pairs = set()

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            report["parse_errors"] += 1
            return report

        report["header_columns"] = len(header)
        idx = {name.strip(): i for i, name in enumerate(header)}

        for line_no, row in enumerate(reader, start=2):
            if not row:
                continue
            report["rows"] += 1
            if len(row) != len(header):
                report["malformed_width_rows"] += 1
                if len(report["malformed_examples"]) < 8:
                    report["malformed_examples"].append({
                        "line": line_no,
                        "expected_columns": len(header),
                        "actual_columns": len(row),
                        "sample": row[: min(8, len(row))],
                    })
                continue

            for field in REQUIRED:
                i = idx.get(field)
                if i is None or not row[i].strip():
                    report["missing_required"][field] += 1

            race_id = row[idx["race_id"]].strip() if "race_id" in idx else ""
            banum = row[idx["banum"]].strip() if "banum" in idx else ""
            if race_id:
                race_ids.add(race_id)
            if race_id and banum:
                pair = (race_id, banum)
                if pair in seen_pairs:
                    report["duplicate_race_rider_rows"] += 1
                else:
                    seen_pairs.add(pair)

            if "pref" in idx:
                pref = row[idx["pref"]].strip()
                if pref and not (2 <= len(pref) <= 4):
                    report["suspicious_pref_rows"] += 1
                    if len(report["suspicious_pref_examples"]) < 8:
                        report["suspicious_pref_examples"].append({
                            "line": line_no,
                            "banum": banum,
                            "player_name": row[idx["player_name"]].strip() if "player_name" in idx else "",
                            "pref": pref,
                        })

            if "rank" in idx and row[idx["rank"]].strip():
                report["rank_populated_rows"] += 1
            if "san_ren_tan" in idx and row[idx["san_ren_tan"]].strip():
                report["trifecta_populated_rows"] += 1

    report["unique_races"] = len(race_ids)
    report["missing_required"] = dict(report["missing_required"])
    report["result_fields_present"] = {
        field: field in idx for field in RESULT_FIELDS
    }
    report["structurally_clean"] = (
        report["malformed_width_rows"] == 0
        and all(field in idx for field in REQUIRED)
    )
    return report


def main() -> None:
    files = sorted(
        p for p in DATA_DIR.glob("*_keirin.csv")
        if p.is_file()
    )
    results = [audit_file(p) for p in files]
    summary = {
        "files_found": len(files),
        "files_structurally_clean": sum(
            1 for r in results if r.get("structurally_clean")
        ),
        "files_with_malformed_rows": sum(
            1 for r in results if r.get("malformed_width_rows", 0) > 0
        ),
        "total_rows": sum(r.get("rows", 0) for r in results),
        "total_malformed_width_rows": sum(
            r.get("malformed_width_rows", 0) for r in results
        ),
        "total_suspicious_pref_rows": sum(
            r.get("suspicious_pref_rows", 0) for r in results
        ),
        "total_unique_races_per_file_sum": sum(
            r.get("unique_races", 0) for r in results
        ),
        "files": results,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({k: v for k, v in summary.items() if k != "files"},
                     ensure_ascii=False, indent=2))
    print(f"Detailed report: {OUT}")


if __name__ == "__main__":
    main()
