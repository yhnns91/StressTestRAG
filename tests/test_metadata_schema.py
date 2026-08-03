"""Reproducibility tests for the corpus metadata schema."""

import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

REPO = Path(__file__).resolve().parents[1]
METADATA_DIR = REPO / "corpus" / "metadata"
VALIDATOR = REPO / "scripts" / "validate_metadata.py"

REQUIRED_COLUMNS = [
    "document_id", "domain", "source_type", "document_title",
    "publication_year", "source_url", "publisher", "license_status",
    "safety_level", "document_length", "chunk_count", "download_date",
    "checksum", "notes",
]

METADATA_FILES = sorted(METADATA_DIR.glob("*.csv"))


def test_metadata_directory_exists():
    assert METADATA_DIR.is_dir(), "corpus/metadata/ is missing"


def test_validator_script_exists():
    assert VALIDATOR.is_file(), "scripts/validate_metadata.py is missing"


@pytest.mark.parametrize("path", METADATA_FILES, ids=lambda p: p.name)
def test_required_columns_present(path):
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    assert not missing, f"{path.name} is missing columns: {missing}"


@pytest.mark.parametrize("path", METADATA_FILES, ids=lambda p: p.name)
def test_validator_passes(path):
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    if df.empty:
        pytest.skip(f"{path.name} has no data rows yet")

    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(path)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, f"validation failed:\n{result.stdout}"


def test_document_ids_unique_across_files():
    seen = {}
    for path in METADATA_FILES:
        df = pd.read_csv(path, dtype=str, keep_default_na=False)
        if df.empty or "document_id" not in df.columns:
            continue
        for doc_id in df["document_id"]:
            assert doc_id not in seen, (
                f"document_id '{doc_id}' appears in both {seen[doc_id]} and {path.name}"
            )
            seen[doc_id] = path.name
