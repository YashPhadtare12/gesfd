# database.py
import sqlite3
from werkzeug.security import generate_password_hash

def init_db():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()

    # Drop all tables if they exist
    cursor.execute('DROP TABLE IF EXISTS staff')
    cursor.execute('DROP TABLE IF EXISTS doctors')
    cursor.execute('DROP TABLE IF EXISTS patients')
    cursor.execute('DROP TABLE IF EXISTS appointments')
    cursor.execute('DROP TABLE IF EXISTS prescriptions')
    cursor.execute('DROP TABLE IF EXISTS doctor_slots')

    # Admin/Staff table
    cursor.execute('''
    CREATE TABLE staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        hospital_name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Doctors table
    cursor.execute('''
    CREATE TABLE doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT NOT NULL,
        experience INTEGER,
        consultation_fee REAL,
        contact TEXT,
        bio TEXT,
        image_path TEXT,
        username TEXT UNIQUE,
        password TEXT,
        created_by INTEGER,
        hospital_id INTEGER NOT NULL,
        FOREIGN KEY (created_by) REFERENCES staff(id),
        FOREIGN KEY (hospital_id) REFERENCES staff(id)
    )
    ''')

    # Patients table
    cursor.execute('''
    CREATE TABLE patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT,
        contact TEXT,
        address TEXT,
        medical_history TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_by INTEGER,
        hospital_id INTEGER NOT NULL,
        FOREIGN KEY (created_by) REFERENCES staff(id),
        FOREIGN KEY (hospital_id) REFERENCES staff(id)
    )
    ''')

    # Appointments table
    cursor.execute('''
    CREATE TABLE appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        time_slot TEXT NOT NULL,
        status TEXT DEFAULT 'Scheduled',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        hospital_id INTEGER NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES patients(id),
        FOREIGN KEY (doctor_id) REFERENCES doctors(id),
        FOREIGN KEY (hospital_id) REFERENCES staff(id)
    )
    ''')

    # Prescriptions table
    cursor.execute('''
    CREATE TABLE prescriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER NOT NULL,
        diagnosis TEXT,
        medicines TEXT,
        instructions TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        hospital_id INTEGER NOT NULL,
        FOREIGN KEY (appointment_id) REFERENCES appointments(id),
        FOREIGN KEY (hospital_id) REFERENCES staff(id)
    )
    ''')

    cursor.execute('''
CREATE TABLE IF NOT EXISTS prescriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER NOT NULL UNIQUE,
    diagnosis TEXT NOT NULL,
    medicines TEXT NOT NULL,
    instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    hospital_id INTEGER NOT NULL,
    FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE CASCADE,
    FOREIGN KEY (hospital_id) REFERENCES staff(id)
)
''')

    # Doctor availability slots
    cursor.execute('''
    CREATE TABLE doctor_slots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_id INTEGER NOT NULL,
        day TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        break_start TEXT,
        break_end TEXT,
        hospital_id INTEGER NOT NULL,
        FOREIGN KEY (doctor_id) REFERENCES doctors(id),
        FOREIGN KEY (hospital_id) REFERENCES staff(id)
    )
    ''')

    # Add default admin
    cursor.execute(
        'INSERT INTO staff (name, email, password, hospital_name) VALUES (?, ?, ?, ?)',
        ('Admin', 'admin@hospital.com', generate_password_hash('admin123'), 'City General Hospital')
    )

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()