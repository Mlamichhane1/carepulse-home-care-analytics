"""Generate a small KPI pack (CSV + charts) from the CarePulse SQLite database.

Outputs (under reports/):
  - kpi_summary.csv
  - visits_by_service.csv
  - clients_by_referral.csv
  - caregiver_utilization_top10.csv
  - charts/*.png

Run
---
python scripts/kpi_report.py
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def ensure_report_dirs(root: Path) -> tuple[Path, Path]:
    reports = root / "reports"
    charts = reports / "charts"
    charts.mkdir(parents=True, exist_ok=True)
    return reports, charts


def main() -> None:
    root = repo_root()
    db_path = root / "database" / "carepulse.db"
    if not db_path.exists():
        raise FileNotFoundError(
            f"Missing database at {db_path}. Run: python scripts/build_sqlite_db.py"
        )

    reports_dir, charts_dir = ensure_report_dirs(root)

    conn = sqlite3.connect(db_path)
    try:
        # KPI 1: high-level summary
        kpi = pd.read_sql(
            """
            SELECT
              (SELECT COUNT(*) FROM clients) AS total_clients,
              (SELECT COUNT(*) FROM clients WHERE discharge_date IS NULL) AS active_clients,
              (SELECT COUNT(*) FROM caregivers) AS total_caregivers,
              (SELECT COUNT(*) FROM visits) AS total_visits,
              (SELECT ROUND(SUM(hours), 2) FROM visits) AS total_visit_hours,
              (
                SELECT ROUND(SUM(v.hours * s.cost), 2)
                FROM visits v
                JOIN services s ON v.service_id = s.service_id
              ) AS gross_service_charges
            ;
            """,
            conn,
        )
        kpi.to_csv(reports_dir / "kpi_summary.csv", index=False)

        # KPI 2: visits by service type
        visits_by_service = pd.read_sql(
            """
            SELECT s.service_type,
                   COUNT(*) AS visit_count,
                   ROUND(SUM(v.hours), 2) AS total_hours,
                   ROUND(SUM(v.hours * s.cost), 2) AS charges
            FROM visits v
            JOIN services s ON v.service_id = s.service_id
            GROUP BY s.service_type
            ORDER BY visit_count DESC;
            """,
            conn,
        )
        visits_by_service.to_csv(reports_dir / "visits_by_service.csv", index=False)

        # KPI 3: clients by referral source
        clients_by_referral = pd.read_sql(
            """
            SELECT referral_source, COUNT(*) AS client_count
            FROM clients
            GROUP BY referral_source
            ORDER BY client_count DESC;
            """,
            conn,
        )
        clients_by_referral.to_csv(reports_dir / "clients_by_referral.csv", index=False)

        # KPI 4: top 10 caregivers by hours (simple utilization proxy)
        caregiver_top10 = pd.read_sql(
            """
            SELECT c.caregiver_id,
                   c.role,
                   ROUND(SUM(v.hours), 2) AS total_hours,
                   COUNT(*) AS visit_count
            FROM visits v
            JOIN caregivers c ON v.caregiver_id = c.caregiver_id
            GROUP BY c.caregiver_id, c.role
            ORDER BY total_hours DESC
            LIMIT 10;
            """,
            conn,
        )
        caregiver_top10.to_csv(reports_dir / "caregiver_utilization_top10.csv", index=False)

    finally:
        conn.close()

    # Charts (matplotlib default style/colors)
    # Visits by service
    plt.figure()
    plt.bar(visits_by_service["service_type"], visits_by_service["visit_count"])
    plt.title("Visits by Service Type")
    plt.ylabel("Visit count")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(charts_dir / "visits_by_service.png", dpi=180)
    plt.close()

    # Clients by referral
    plt.figure()
    plt.bar(clients_by_referral["referral_source"], clients_by_referral["client_count"])
    plt.title("Clients by Referral Source")
    plt.ylabel("Client count")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(charts_dir / "clients_by_referral.png", dpi=180)
    plt.close()

    # Top caregivers
    plt.figure()
    plt.bar(caregiver_top10["caregiver_id"].astype(str), caregiver_top10["total_hours"])
    plt.title("Top 10 Caregivers by Visit Hours")
    plt.ylabel("Total visit hours")
    plt.xlabel("Caregiver ID")
    plt.tight_layout()
    plt.savefig(charts_dir / "top_caregivers_by_hours.png", dpi=180)
    plt.close()

    print("✅ KPI pack generated under:")
    print(f"  - {reports_dir}")


if __name__ == "__main__":
    main()
