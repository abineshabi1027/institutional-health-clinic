import pandas as pd
import numpy as np

# 1. Load the messy data
print("Loading messy dataset...")
df = pd.read_csv('messy_student_health_data.csv')

# 2. Standardize Categorical Data (Gender)
# Issue: 'Male', 'Female', 'M', 'F', 'male', 'female ', ' M '
# Fix: Strip whitespaces, uppercase everything, and just take the first letter ('M' or 'F')
print("Standardizing gender column...")
df['gender'] = df['gender'].astype(str).str.strip().str.upper().str[0]

# 3. Fix Formatting Inconsistencies
# Issue A: 'blood_pressure' has slashes (120/80) and hyphens (120-80)
# Fix A: Replace hyphens with slashes
print("Standardizing blood pressure formats...")
df['blood_pressure'] = df['blood_pressure'].astype(str).str.replace('-', '/')
df.loc[df['blood_pressure'] == 'nan', 'blood_pressure'] = np.nan # Restore actual NaNs

# Issue B: Dates are a mix of YYYY-MM-DD and DD/MM/YYYY
# Fix B: Use pandas to aggressively parse the mixed formats into a standard datetime object
print("Aligning date formats...")
df['visit_date'] = pd.to_datetime(df['visit_date'], format='mixed', dayfirst=True)

# 4. Handle Extreme Outliers (Math Errors)
# Issue: Heights accidentally divided by 10 (e.g., 16.5 cm) and Weights multiplied by 10 (e.g., 650 kg)
print("Correcting mathematical outliers...")
# If height is ridiculously low (under 50cm for a college student), multiply by 10
df.loc[df['height_cm'] < 50, 'height_cm'] = df['height_cm'] * 10 

# If weight is ridiculously high (over 300kg), divide by 10
df.loc[df['weight_kg'] > 300, 'weight_kg'] = df['weight_kg'] / 10

# 5. Handle Missing Data (NaNs)
# Issue: Missing heights and weights.
# Fix: Impute (fill in) the missing values using the median of the dataset. 
print("Imputing missing values...")
median_height = df['height_cm'].median()
median_weight = df['weight_kg'].median()

df['height_cm'] = df['height_cm'].fillna(median_height)
df['weight_kg'] = df['weight_kg'].fillna(median_weight)

# Note: We will leave missing blood pressure and doctor notes as NaN, 
# as imputing medical diagnoses/readings is usually unsafe practice.

# 6. Save the Cleaned Data
output_filename = 'clean_student_health_data.csv'
df.to_csv(output_filename, index=False)
print(f"Success! Cleaned dataset saved as '{output_filename}'.")
