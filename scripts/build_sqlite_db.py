import sqlite3
import pandas as pd
import os

DB_PATH = "database/carepulse.db"

# Make sure database folder exists
os.makedirs("database", exist_ok=True)

# Load CSVs
clients = pd.read_csv("data/raw/clients.csv")
caregivers = pd.read_csv("data/raw/caregivers.csv")
services = pd.read_csv("data/raw/services.csv")
visits = pd.read_csv("data/raw/visits.csv")

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)

# Save tables
clients.to_sql("clients", conn, if_exists="replace", index=False)
caregivers.to_sql("caregivers", conn, if_exists="replace", index=False)
services.to_sql("services", conn, if_exists="replace", index=False)
visits.to_sql("visits", conn, if_exists="replace", index=False)

conn.close()

print("SQLite database created at:", DB_PATH)
print("Tables: clients, caregivers, services, visits")

# Print all the saved
print("visits = pd.read_csv")

