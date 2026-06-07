import pandas as pd
import sqlite3

print("Loading cleaned dataset...")
df = pd.read_csv('clean_student_health_data.csv')

print("Connecting to database...")
conn = sqlite3.connect('student_health.db')
cursor = conn.cursor()

print("Building SQL schema...")

cursor.execute('''
CREATE TABLE IF NOT EXISTS Students (
    student_id TEXT PRIMARY KEY,
    full_name TEXT,
    gender TEXT,
    dob DATE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Visits (
    visit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT,
    visit_date DATE,
    height_cm REAL,
    weight_kg REAL,
    blood_pressure TEXT,
    symptoms TEXT,
    diagnosis TEXT,
    doctor_notes TEXT,
    FOREIGN KEY (student_id) REFERENCES Students (student_id)
)
''')

students_df = df[['student_id', 'full_name', 'gender', 'dob']].drop_duplicates(subset=['student_id'])

visits_df = df[['student_id', 'visit_date', 'height_cm', 'weight_kg', 'blood_pressure', 'symptoms', 'diagnosis', 'doctor_notes']]

print("Inserting data into tables...")
students_df.to_sql('Students', conn, if_exists='append', index=False)
visits_df.to_sql('Visits', conn, if_exists='append', index=False)

conn.commit()
conn.close()

print("Success! Database 'student_health.db' created and populated.")
