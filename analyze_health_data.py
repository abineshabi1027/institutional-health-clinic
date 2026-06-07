import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


sns.set_theme(style="whitegrid")

conn = sqlite3.connect('student_health.db')

query = '''
    SELECT 
        s.gender, 
        s.dob, 
        v.visit_date, 
        v.symptoms, 
        v.diagnosis,
        v.height_cm,
        v.weight_kg
    FROM Visits v
    JOIN Students s ON v.student_id = s.student_id
'''
df = pd.read_sql_query(query, conn)
conn.close()

df['visit_date'] = pd.to_datetime(df['visit_date'])
df['visit_month'] = df['visit_date'].dt.month_name()

print("Data loaded successfully. Generating insights...\n")

plt.figure(figsize=(10, 6))
sns.countplot(data=df, y='symptoms', order=df['symptoms'].value_counts().index, palette='viridis')
plt.title('Most Common Student Clinic Symptoms')
plt.xlabel('Number of Visits')
plt.ylabel('Reported Symptom')
plt.tight_layout()
plt.savefig('symptom_distribution.png')
print("Generated: symptom_distribution.png")

correlation = df['height_cm'].corr(df['weight_kg'])
print(f"Karl Pearson's Correlation Coefficient (Height vs. Weight): {correlation:.3f}")

plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x='height_cm', y='weight_kg', hue='gender', alpha=0.6)
plt.title(f'Height vs. Weight \n(Correlation: {correlation:.2f})')
plt.xlabel('Height (cm)')
plt.ylabel('Weight (kg)')
plt.tight_layout()
plt.savefig('height_weight_correlation.png')
print("Generated: height_weight_correlation.png")

monthly_visits = df.groupby('visit_month').size().reset_index(name='visit_count')

months = ["January", "February", "March", "April", "May", "June", 
          "July", "August", "September", "October", "November", "December"]
monthly_visits['visit_month'] = pd.Categorical(monthly_visits['visit_month'], categories=months, ordered=True)
monthly_visits = monthly_visits.sort_values('visit_month')

plt.figure(figsize=(12, 5))
sns.lineplot(data=monthly_visits, x='visit_month', y='visit_count', marker='o', linewidth=2, color='coral')
plt.title('Clinic Visit Volume by Month')
plt.xlabel('Month')
plt.ylabel('Total Visits')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('monthly_visit_trends.png')
print("Generated: monthly_visit_trends.png")

print("\nEDA Complete! Check your folder for the generated PNG files.")
