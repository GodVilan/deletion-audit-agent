"""Integration: the sample scorer on the real dataset.

Skipped when dataset/ is absent (it isn't redistributed), and when the screenshots and PDFs can't be read:
no ANTHROPIC_API_KEY (environment or root .env) and no media cache in code/cache/media/. Without media,
sample case_07 (PDF-only evidence) can't be scored correctly, so the 32/32 gate wouldn't be meaningful.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
HAS_DATASET = (ROOT / "dataset" / "sample_output.csv").exists()
CAN_READ_MEDIA = bool(os.environ.get("ANTHROPIC_API_KEY")) or (ROOT / ".env").exists() or \
    any((ROOT / "code" / "cache" / "media").glob("*.json"))

pytestmark = [
    pytest.mark.skipif(not HAS_DATASET, reason="dataset/ not present"),
    pytest.mark.skipif(not CAN_READ_MEDIA, reason="no API key and no media cache: media evidence can't be read"),
]


def test_sample_status_and_precision():
    """Gate (SPEC_CARD §12): status 32/32 and 6-field step precision 1.0 on the public samples."""
    sys.path.insert(0, str(ROOT / "code" / "evaluation"))
    import score_sample
    _, summary = score_sample.score(write_report=False, quiet=True)
    assert summary["status_accuracy"] == "32/32"
    assert summary["step_P(6-field, no step_no)"] == 1.0
