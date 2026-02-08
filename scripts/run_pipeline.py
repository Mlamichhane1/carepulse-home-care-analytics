"""End-to-end runner for the CarePulse mini analytics pipeline.

Steps
-----
1) Generate synthetic data (data/raw)
2) Build SQLite DB (database/carepulse.db)
3) Produce KPI outputs (reports/)

Run
---
python scripts/run_pipeline.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    print("\n$", " ".join(cmd))
    subprocess.check_call(cmd)


def main() -> None:
    root = repo_root()
    py = sys.executable

    run([py, str(root / "scripts" / "data_generation.py")])
    run([py, str(root / "scripts" / "build_sqlite_db.py")])
    run([py, str(root / "scripts" / "kpi_report.py")])

    print("\n✅ Done. Open the outputs in:")
    print(f"  - {root / 'reports'}")


if __name__ == "__main__":
    main()
