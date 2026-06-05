import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime

# Initialize Faker with an Indian locale to generate region-appropriate names
fake = Faker('en_IN')

# Set seeds for reproducibility (optional, but helpful for consistent testing)
Faker.seed(42)
random.seed(42)
np.random.seed(42)

NUM_RECORDS = 1000

# Common symptoms and diagnoses for a student demographic
symptoms_list = ['Fever', 'Cough', 'Headache', 'Stomach ache', 'Fatigue', 'Nausea', 'Sprained ankle', 'Sore throat']
diagnoses_list = ['Viral Infection', 'Common Cold', 'Migraine', 'Food Poisoning', 'Stress', 'Gastroenteritis', 'Sprain', 'Pharyngitis']

data = []

print("Generating base records...")
for _ in range(NUM_RECORDS):
    record = {
        'student_id': fake.bothify(text='STU-####'),
        'full_name': fake.name(),
        # Inject intentional casing and spacing inconsistencies right from the start
        'gender': random.choice(['Male', 'Female', 'M', 'F', 'male', 'female ', ' M ']), 
        'dob': fake.date_of_birth(minimum_age=17, maximum_age=25).strftime('%Y-%m-%d'),
        'visit_date': fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d'),
        'height_cm': round(random.uniform(150.0, 190.0), 1),
        'weight_kg': round(random.uniform(45.0, 100.0), 1),
        'blood_pressure': f"{random.randint(90, 140)}/{random.randint(60, 90)}",
        'symptoms': random.choice(symptoms_list),
        'diagnosis': random.choice(diagnoses_list),
        'doctor_notes': fake.sentence(nb_words=5) if random.random() > 0.4 else "" # Leave some notes blank
    }
    data.append(record)

df = pd.DataFrame(data)

print("Injecting real-world messiness...")
# --- 1. Missing Values (NaNs) ---
# Randomly drop 5% of height and weight data to simulate missed measurements
df.loc[df.sample(frac=0.05).index, 'height_cm'] = np.nan
df.loc[df.sample(frac=0.05).index, 'weight_kg'] = np.nan

# Randomly drop 10% of blood pressure readings
df.loc[df.sample(frac=0.10).index, 'blood_pressure'] = np.nan


# --- 2. Outliers / Typographical Errors ---
# Make a few heights completely unrealistic (e.g., accidental decimal shift: 16.5 cm instead of 165 cm)
outlier_idx_h = df.sample(5).index
df.loc[outlier_idx_h, 'height_cm'] = df.loc[outlier_idx_h, 'height_cm'] / 10

# Make a few weights unrealistic (e.g., double-tapping a key: 655 kg instead of 65 kg)
outlier_idx_w = df.sample(3).index
df.loc[outlier_idx_w, 'weight_kg'] = df.loc[outlier_idx_w, 'weight_kg'] * 10


# --- 3. Formatting Inconsistencies ---
# Corrupt some date formats in 'visit_date' (simulating someone manually typing DD/MM/YYYY instead of YYYY-MM-DD)
messy_dates = df.sample(15).index
df.loc[messy_dates, 'visit_date'] = df.loc[messy_dates, 'visit_date'].apply(
    lambda x: datetime.strptime(x, '%Y-%m-%d').strftime('%d/%m/%Y') if pd.notnull(x) else x
)

# Corrupt blood pressure formats (e.g., using a hyphen instead of a slash: 120-80)
messy_bp = df.dropna(subset=['blood_pressure']).sample(20).index
df.loc[messy_bp, 'blood_pressure'] = df.loc[messy_bp, 'blood_pressure'].str.replace('/', '-')

# Save the final messy dataset
output_filename = 'messy_student_health_data.csv'
df.to_csv(output_filename, index=False)
print(f"Success! Dataset '{output_filename}' is ready for cleaning.")
