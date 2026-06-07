import pandas as pd
import numpy as np

print("Loading messy dataset...")
df = pd.read_csv('messy_student_health_data.csv')

df['gender'] = df['gender'].astype(str).str.strip().str.upper().str[0]

print("Standardizing blood pressure formats...")
df['blood_pressure'] = df['blood_pressure'].astype(str).str.replace('-', '/')
df.loc[df['blood_pressure'] == 'nan', 'blood_pressure'] = np.nan 

print("Aligning date formats...")
df['visit_date'] = pd.to_datetime(df['visit_date'], format='mixed', dayfirst=True)

print("Correcting mathematical outliers...")

df.loc[df['height_cm'] < 50, 'height_cm'] = df['height_cm'] * 10 
df.loc[df['weight_kg'] > 300, 'weight_kg'] = df['weight_kg'] / 10

print("Imputing missing values...")
median_height = df['height_cm'].median()
median_weight = df['weight_kg'].median()

df['height_cm'] = df['height_cm'].fillna(median_height)
df['weight_kg'] = df['weight_kg'].fillna(median_weight)

output_filename = 'clean_student_health_data.csv'
df.to_csv(output_filename, index=False)
print(f"Success! Cleaned dataset saved as '{output_filename}'.")
