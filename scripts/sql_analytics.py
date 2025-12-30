import sqlite3
import pandas as pd

DB_PATH = "database/carepulse.db"
conn = sqlite3.connect(DB_PATH)

# 1) Total visits
q1 = "SELECT COUNT(*) AS total_visits FROM visits;"
print("\n1) Total visits:")
print(pd.read_sql(q1, conn))

# 2) Most common services
q2 = """
SELECT s.service_type, COUNT(*) AS visit_count
FROM visits v
JOIN services s ON v.service_id = s.service_id
GROUP BY s.service_type
ORDER BY visit_count DESC;
"""
print("\n2) Visits by service type:")
print(pd.read_sql(q2, conn))

# 3) Top 10 caregivers by hours
q3 = """
SELECT caregiver_id, SUM(hours) AS total_hours
FROM visits
GROUP BY caregiver_id
ORDER BY total_hours DESC
LIMIT 10;
"""
print("\n3) Top 10 caregivers by total hours:")
print(pd.read_sql(q3, conn))

# 4) Enrollment by referral source
q4 = """
SELECT referral_source, COUNT(*) AS client_count
FROM clients
GROUP BY referral_source
ORDER BY client_count DESC;
"""
print("\n4) Clients by referral source:")
print(pd.read_sql(q4, conn))

conn.close()
