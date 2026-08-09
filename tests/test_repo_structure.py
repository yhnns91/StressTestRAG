"""Verify the repository layout matches Section 3.1 of the assignment document."""
import fnmatch
import subprocess
import pytest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED_DIRS = [
    "configs",
    "data/raw_external_metadata", "data/interim", "data/processed", "data/final",
    "corpus/metadata", "corpus/extracted_text", "corpus/chunks",
    "annotations/guideline", "annotations/pilot", "annotations/adjudicated",
    "scripts", "src", "tests", "notebooks",
    "reports/qc", "reports/agreement", "reports/pilot_rag", "reports/weekly",
    "docs", ".github/ISSUE_TEMPLATE", ".github/workflows",
]

REQUIRED_FILES = [
    "README.md", "CONTRIBUTING.md", "CHANGELOG.md", "CITATION.cff",
    ".gitignore", ".gitattributes", "requirements.txt",
    ".github/pull_request_template.md",
    "scripts/validate_metadata.py",
    "docs/schema.md",
]

FORBIDDEN_PATTERNS = ["*.key", "*.pem", ".env", "credentials.json"]


def test_required_directories_exist():
    missing = [d for d in REQUIRED_DIRS if not (REPO / d).is_dir()]
    assert not missing, f"missing directories: {missing}"


def test_required_files_exist():
    missing = [f for f in REQUIRED_FILES if not (REPO / f).is_file()]
    assert not missing, f"missing files: {missing}"


def test_no_secrets_committed():
    """Only files Git actually tracks can leak — ignored paths cannot."""
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO, capture_output=True, text=True,
    )
    if result.returncode != 0:
        pytest.skip("not a git repository")

    tracked = [Path(line) for line in result.stdout.splitlines() if line]
    found = [
        str(p) for p in tracked
        if any(fnmatch.fnmatch(p.name, pattern) for pattern in FORBIDDEN_PATTERNS)
    ]
    assert not found, f"forbidden files tracked by git: {found}"
