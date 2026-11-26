"""Regressão do comando de construção do índice documentado no README."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_index.py"


def test_build_index_uses_the_current_checkout_and_writes_artifacts(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [str(SCRIPT), "--output-dir", str(tmp_path)],
    )

    runpy.run_path(str(SCRIPT), run_name="__main__")

    assert (tmp_path / "intent_index.joblib").is_file()
    assert (tmp_path / "intent_index_config.json").is_file()
