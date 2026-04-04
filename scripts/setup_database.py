# Create DB+ dummy data
import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "data/clinic.db"


def create_connection():
    return sqlite3.connect(DB_PATH)


def create_tables(conn):
    cursor = conn.cursor()

    cursor.executescript("""
    DROP TABLE IF EXISTS invoices;
    DROP TABLE IF EXISTS treatments;
    DROP TABLE IF EXISTS appointments;
    DROP TABLE IF EXISTS doctors;
    DROP TABLE IF EXISTS patients;

    CREATE TABLE patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        date_of_birth DATE,
        gender TEXT,
        city TEXT,
        registered_date DATE
    );

    CREATE TABLE doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT,
        department TEXT,
        phone TEXT
    );

    CREATE TABLE appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        appointment_date DATETIME,
        status TEXT,
        notes TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id),
        FOREIGN KEY(doctor_id) REFERENCES doctors(id)
    );

    CREATE TABLE treatments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER,
        treatment_name TEXT,
        cost REAL,
        duration_minutes INTEGER,
        FOREIGN KEY(appointment_id) REFERENCES appointments(id)
    );

    CREATE TABLE invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        invoice_date DATE,
        total_amount REAL,
        paid_amount REAL,
        status TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(id)
    );
    """)

    conn.commit()


# ---------- Dummy Data Helpers ----------

FIRST_NAMES = [
    "Amit", "Rahul", "Sneha", "Priya", "Karan", "Neha",
    "Rohit", "Anjali", "Vikram", "Pooja", "Arjun", "Meera"
]

LAST_NAMES = [
    "Sharma", "Patil", "Verma", "Gupta", "Singh",
    "Joshi", "Deshmukh", "Kulkarni"
]

CITIES = [
    "Mumbai", "Pune", "Delhi", "Bangalore", "Hyderabad",
    "Chennai", "Nagpur", "Nashik", "Jaipur"
]

SPECIALIZATIONS = [
    "Dermatology", "Cardiology", "Orthopedics",
    "General", "Pediatrics"
]

TREATMENTS = [
    "Consultation", "X-Ray", "Blood Test", "MRI Scan",
    "Physiotherapy", "Skin Treatment"
]

STATUSES = ["Scheduled", "Completed", "Cancelled", "No-Show"]
INVOICE_STATUSES = ["Paid", "Pending", "Overdue"]


def random_date_within_last_year():
    days_ago = random.randint(0, 365)
    return datetime.now() - timedelta(days=days_ago)


def maybe_null(value, probability=0.2):
    return value if random.random() > probability else None


# ---------- Insert Data ----------

def insert_doctors(conn):
    cursor = conn.cursor()

    doctors = []
    for i in range(15):
        name = f"Dr. {random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        specialization = random.choice(SPECIALIZATIONS)
        department = specialization
        phone = f"9{random.randint(100000000, 999999999)}"

        doctors.append((name, specialization, department, phone))

    cursor.executemany("""
        INSERT INTO doctors (name, specialization, department, phone)
        VALUES (?, ?, ?, ?)
    """, doctors)

    conn.commit()
    return len(doctors)


def insert_patients(conn):
    cursor = conn.cursor()

    patients = []
    for _ in range(200):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)

        email = maybe_null(f"{first.lower()}.{last.lower()}@mail.com")
        phone = maybe_null(f"9{random.randint(100000000, 999999999)}")

        dob = datetime.now() - timedelta(days=random.randint(18*365, 70*365))
        gender = random.choice(["M", "F"])
        city = random.choice(CITIES)
        registered = random_date_within_last_year()

        patients.append((
            first, last, email, phone,
            dob.date(), gender, city,
            registered.date()
        ))

    cursor.executemany("""
        INSERT INTO patients
        (first_name, last_name, email, phone, date_of_birth, gender, city, registered_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, patients)

    conn.commit()
    return len(patients)


def insert_appointments(conn):
    cursor = conn.cursor()

    appointments = []
    for _ in range(500):
        patient_id = random.randint(1, 200)
        doctor_id = random.randint(1, 15)

        date = random_date_within_last_year()
        status = random.choices(
            STATUSES,
            weights=[0.3, 0.5, 0.1, 0.1]
        )[0]

        notes = maybe_null("Follow-up required", 0.5)

        appointments.append((
            patient_id, doctor_id,
            date, status, notes
        ))

    cursor.executemany("""
        INSERT INTO appointments
        (patient_id, doctor_id, appointment_date, status, notes)
        VALUES (?, ?, ?, ?, ?)
    """, appointments)

    conn.commit()
    return len(appointments)


def insert_treatments(conn):
    cursor = conn.cursor()

    treatments = []
    for _ in range(350):
        appointment_id = random.randint(1, 500)
        name = random.choice(TREATMENTS)
        cost = round(random.uniform(50, 5000), 2)
        duration = random.randint(10, 120)

        treatments.append((
            appointment_id, name, cost, duration
        ))

    cursor.executemany("""
        INSERT INTO treatments
        (appointment_id, treatment_name, cost, duration_minutes)
        VALUES (?, ?, ?, ?)
    """, treatments)

    conn.commit()
    return len(treatments)


def insert_invoices(conn):
    cursor = conn.cursor()

    invoices = []
    for _ in range(300):
        patient_id = random.randint(1, 200)
        invoice_date = random_date_within_last_year()

        total = round(random.uniform(100, 8000), 2)

        status = random.choice(INVOICE_STATUSES)

        if status == "Paid":
            paid = total
        elif status == "Pending":
            paid = round(total * random.uniform(0.2, 0.8), 2)
        else:
            paid = 0

        invoices.append((
            patient_id, invoice_date.date(),
            total, paid, status
        ))

    cursor.executemany("""
        INSERT INTO invoices
        (patient_id, invoice_date, total_amount, paid_amount, status)
        VALUES (?, ?, ?, ?, ?)
    """, invoices)

    conn.commit()
    return len(invoices)


# ---------- Main ----------

def main():
    conn = create_connection()

    create_tables(conn)

    doctor_count = insert_doctors(conn)
    patient_count = insert_patients(conn)
    appointment_count = insert_appointments(conn)
    treatment_count = insert_treatments(conn)
    invoice_count = insert_invoices(conn)

    conn.close()

    print(f"Created {patient_count} patients, "
          f"{doctor_count} doctors, "
          f"{appointment_count} appointments, "
          f"{treatment_count} treatments, "
          f"{invoice_count} invoices.")


if __name__ == "__main__":
    main()