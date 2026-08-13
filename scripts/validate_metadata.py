#!/usr/bin/env python3
"""
Validate corpus metadata CSV files against the StressTestRAG schema.

Usage:
    python scripts/validate_metadata.py corpus/metadata/INF_pilot_sources.csv
    python scripts/validate_metadata.py corpus/metadata/*.csv

Exits with code 1 if any error is found, so it can gate CI.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

import pandas as pd

# --- Schema definition (Section 6.3 of the assignment document) ---

REQUIRED_COLUMNS = [
    "document_id",
    "domain",
    "source_type",
    "document_title",
    "publication_year",
    "source_url",
    "publisher",
    "license_status",
    "safety_level",
    "document_length",
    "chunk_count",
    "download_date",
    "checksum",
    "notes",
]

VALID_DOMAINS = {
    "natural_disaster",
    "infrastructure_disruption",
    "cyber_incident_response",
}

DOMAIN_PREFIX = {
    "DIS": "natural_disaster",
    "INF": "infrastructure_disruption",
    "CYB": "cyber_incident_response",
}

VALID_SAFETY_LEVELS = {"low", "medium", "high"}

VALID_LICENSE_STATUS = {
    "public_domain",
    "open_license_redistributable",
    "metadata_only_until_verified",
    "metadata_only_restricted",
    "excluded",
}

DOCUMENT_ID_PATTERN = re.compile(r"^(DIS|INF|CYB)-\d{3}$")

MIN_PUBLICATION_YEAR = 1990


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, row: int | None, message: str) -> None:
        prefix = f"row {row}: " if row is not None else ""
        self.errors.append(prefix + message)

    def warn(self, row: int | None, message: str) -> None:
        prefix = f"row {row}: " if row is not None else ""
        self.warnings.append(prefix + message)


def check_columns(df: pd.DataFrame, rep: Report) -> bool:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        rep.error(None, f"missing required column(s): {', '.join(missing)}")
        return False

    extra = [c for c in df.columns if c not in REQUIRED_COLUMNS]
    if extra:
        rep.warn(None, f"unexpected column(s) present: {', '.join(extra)}")
    return True


def check_rows(df: pd.DataFrame, rep: Report) -> None:
    today = date.today()
    seen_ids: dict[str, int] = {}
    seen_urls: dict[str, int] = {}

    for idx, row in df.iterrows():
        n = idx + 2  # +1 for zero-index, +1 for header line

        # --- document_id ---
        doc_id = str(row["document_id"]).strip()
        if not DOCUMENT_ID_PATTERN.match(doc_id):
            rep.error(n, f"document_id '{doc_id}' does not match [DIS|INF|CYB]-NNN")
        elif doc_id in seen_ids:
            rep.error(n, f"duplicate document_id '{doc_id}' (first seen at row {seen_ids[doc_id]})")
        else:
            seen_ids[doc_id] = n

        # --- domain, and consistency with the ID prefix ---
        domain = str(row["domain"]).strip()
        if domain not in VALID_DOMAINS:
            rep.error(n, f"domain '{domain}' not in {sorted(VALID_DOMAINS)}")
        elif DOCUMENT_ID_PATTERN.match(doc_id):
            expected = DOMAIN_PREFIX[doc_id[:3]]
            if domain != expected:
                rep.error(n, f"document_id prefix '{doc_id[:3]}' implies domain '{expected}', found '{domain}'")

        # --- free-text fields that must not be blank ---
        for field in ("document_title", "publisher", "source_type"):
            value = str(row[field]).strip()
            if not value or value.lower() in {"nan", "none", "-"}:
                rep.error(n, f"{field} is empty")

        # --- publication_year ---
        try:
            year = int(row["publication_year"])
            if year < MIN_PUBLICATION_YEAR or year > today.year:
                rep.error(n, f"publication_year {year} outside {MIN_PUBLICATION_YEAR}–{today.year}")
        except (ValueError, TypeError):
            rep.error(n, f"publication_year '{row['publication_year']}' is not an integer")

        # --- source_url ---
        url = str(row["source_url"]).strip()
        if not url.startswith(("http://", "https://")):
            rep.error(n, f"source_url must start with http:// or https:// (found '{url[:40]}')")
        elif url in seen_urls:
            rep.error(n, f"duplicate source_url (first seen at row {seen_urls[url]})")
        else:
            seen_urls[url] = n

        # --- license_status ---
        lic = str(row["license_status"]).strip()
        if lic not in VALID_LICENSE_STATUS:
            rep.error(n, f"license_status '{lic}' not in {sorted(VALID_LICENSE_STATUS)}")
        if lic == "metadata_only_until_verified":
            rep.warn(n, f"{doc_id}: license still unverified — open a needs-review issue before storing full text")
        if lic == "excluded":
            notes = str(row["notes"]).strip()
            if not notes or notes.lower() in {"nan", "none", "-"}:
                rep.error(n, "license_status is 'excluded' but notes does not record the reason")

        # --- safety_level ---
        safety = str(row["safety_level"]).strip()
        if safety not in VALID_SAFETY_LEVELS:
            rep.error(n, f"safety_level '{safety}' not in {sorted(VALID_SAFETY_LEVELS)}")
        if safety == "high":
            rep.warn(n, f"{doc_id}: safety_level is 'high' — confirm the document contains no excluded content")

        # --- download_date ---
        raw_date = str(row["download_date"]).strip()
        try:
            dl = datetime.strptime(raw_date, "%Y-%m-%d").date()
            if dl > today:
                rep.error(n, f"download_date {raw_date} is in the future")
        except ValueError:
            rep.error(n, f"download_date '{raw_date}' is not in YYYY-MM-DD format")

        # --- checksum ---
        checksum = str(row["checksum"]).strip()
        if not re.fullmatch(r"[a-f0-9]{64}", checksum.lower()):
            rep.error(n, "checksum must be a 64-character SHA-256 hex digest")

        # --- numeric counts ---
        for field in ("document_length", "chunk_count"):
            value = str(row[field]).strip()
            if value.lower() in {"", "nan", "none"}:
                rep.warn(n, f"{field} is empty (acceptable before Phase 2)")
                continue
            try:
                if int(value) < 0:
                    rep.error(n, f"{field} must not be negative")
            except ValueError:
                rep.error(n, f"{field} '{value}' is not an integer")


def validate(path: Path) -> Report:
    rep = Report()

    try:
        df = pd.read_csv(path, dtype=str, keep_default_na=False)
    except Exception as exc:  # noqa: BLE001
        rep.error(None, f"could not read file: {exc}")
        return rep

    if df.empty:
        rep.warn(None, "file has headers but no data rows yet (template state)")
        check_columns(df, rep)
        return rep

    if check_columns(df, rep):
        check_rows(df, rep)

    return rep


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate StressTestRAG corpus metadata.")
    parser.add_argument("files", nargs="+", type=Path, help="CSV file(s) to validate")
    args = parser.parse_args()

    exit_code = 0

    for path in args.files:
        print(f"\n=== {path} ===")
        if not path.exists():
            print("  ERROR: file not found")
            exit_code = 1
            continue

        rep = validate(path)

        for w in rep.warnings:
            print(f"  WARN   {w}")
        for e in rep.errors:
            print(f"  ERROR  {e}")

        if rep.errors:
            print(f"  -> FAILED ({len(rep.errors)} error, {len(rep.warnings)} warning)")
            exit_code = 1
        else:
            print(f"  -> PASSED ({len(rep.warnings)} warning)")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
