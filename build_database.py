import pandas as pd
import sqlite3

# 1. Load the cleaned data
print("Loading cleaned dataset...")
df = pd.read_csv('clean_student_health_data.csv')

# 2. Connect to SQLite database (this creates a new file called student_health.db)
print("Connecting to database...")
conn = sqlite3.connect('student_health.db')
cursor = conn.cursor()

# 3. Define the SQL Schema (Tables and Relationships)
print("Building SQL schema...")

# Create the Students table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Students (
    student_id TEXT PRIMARY KEY,
    full_name TEXT,
    gender TEXT,
    dob DATE
)
''')

# Create the Visits table with a Foreign Key linking back to Students
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

# 4. Split the Pandas DataFrame to match our Relational Schema

# Extract unique students for the Students table
students_df = df[['student_id', 'full_name', 'gender', 'dob']].drop_duplicates(subset=['student_id'])

# Extract visit details for the Visits table
visits_df = df[['student_id', 'visit_date', 'height_cm', 'weight_kg', 'blood_pressure', 'symptoms', 'diagnosis', 'doctor_notes']]

# 5. Insert the data into the database
print("Inserting data into tables...")
students_df.to_sql('Students', conn, if_exists='append', index=False)
visits_df.to_sql('Visits', conn, if_exists='append', index=False)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Success! Database 'student_health.db' created and populated.")
