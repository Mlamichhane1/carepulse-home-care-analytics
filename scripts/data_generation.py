import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

# Settings (easy to change)
NUM_CLIENTS = 200
NUM_CAREGIVERS = 40
NUM_VISITS = 1200

# Clients table
clients = pd.DataFrame({
    "client_id": np.arange(1, NUM_CLIENTS + 1),
    "age": np.random.randint(60, 95, size=NUM_CLIENTS),
    "gender": np.random.choice(["Male", "Female"], size=NUM_CLIENTS),
    "enrollment_date": [
        (datetime.today() - timedelta(days=random.randint(30, 900))).date()
        for _ in range(NUM_CLIENTS)
    ],
    "referral_source": np.random.choice(
        ["Hospital", "Physician", "Family", "Insurance"],
        size=NUM_CLIENTS
    )
})

# Simple discharge logic (some clients discharged, some still active)
discharge_days = np.random.choice(
    [-1, 30, 60, 90, 120, 180, 240, 300],
    size=NUM_CLIENTS,
    p=[0.35, 0.10, 0.10, 0.10, 0.10, 0.08, 0.07, 0.10]
)

clients["discharge_date"] = clients.apply(
    lambda row: None if discharge_days[row.name] == -1
    else (pd.to_datetime(row["enrollment_date"]) + pd.Timedelta(days=int(discharge_days[row.name]))).date(),
    axis=1
)

# Caregivers table
caregivers = pd.DataFrame({
    "caregiver_id": np.arange(1, NUM_CAREGIVERS + 1),
    "role": np.random.choice(["RN", "LPN", "HHA"], size=NUM_CAREGIVERS, p=[0.25, 0.35, 0.40]),
    "hire_date": [
        (datetime.today() - timedelta(days=random.randint(100, 1500))).date()
        for _ in range(NUM_CAREGIVERS)
    ],
    "hourly_rate": np.random.randint(18, 45, size=NUM_CAREGIVERS)
})

# Services table
services = pd.DataFrame({
    "service_id": [1, 2, 3, 4],
    "service_type": ["Personal Care", "Skilled Nursing", "Physical Therapy", "Companionship"],
    "default_hours": [2.0, 3.0, 1.5, 2.0],
    "cost_per_visit": [60, 120, 100, 50]
})

# Visits table
visits = pd.DataFrame({
    "visit_id": np.arange(1, NUM_VISITS + 1),
    "client_id": np.random.choice(clients["client_id"], size=NUM_VISITS),
    "caregiver_id": np.random.choice(caregivers["caregiver_id"], size=NUM_VISITS),
    "service_id": np.random.choice(services["service_id"], size=NUM_VISITS),
    "visit_date": [
        (datetime.today() - timedelta(days=random.randint(1, 365))).date()
        for _ in range(NUM_VISITS)
    ],
    "hours": np.random.choice([1.5, 2.0, 2.5, 3.0], size=NUM_VISITS)
})

# Save to CSV (for BI + SQL later)
clients.to_csv("data/raw/clients.csv", index=False)
caregivers.to_csv("data/raw/caregivers.csv", index=False)
services.to_csv("data/raw/services.csv", index=False)
visits.to_csv("data/raw/visits.csv", index=False)

print("Synthetic CarePulse data generated: clients, caregivers, services, visits.")
