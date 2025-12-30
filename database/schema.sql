-- CarePulse Home Care Database Schema

CREATE TABLE clients (
    client_id INTEGER PRIMARY KEY,
    age INTEGER,
    gender TEXT,
    enrollment_date DATE,
    discharge_date DATE,
    referral_source TEXT
);

CREATE TABLE caregivers (
    caregiver_id INTEGER PRIMARY KEY,
    role TEXT,
    hire_date DATE,
    hourly_rate REAL
);

CREATE TABLE services (
    service_id INTEGER PRIMARY KEY,
    service_type TEXT,
    duration_hours REAL,
    cost REAL
);

CREATE TABLE visits (
    visit_id INTEGER PRIMARY KEY,
    client_id INTEGER,
    caregiver_id INTEGER,
    service_id INTEGER,
    visit_date DATE,
    hours REAL,
    FOREIGN KEY (client_id) REFERENCES clients(client_id),
    FOREIGN KEY (caregiver_id) REFERENCES caregivers(caregiver_id),
    FOREIGN KEY (service_id) REFERENCES services(service_id)
);
