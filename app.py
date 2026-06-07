from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import pandas as pd

app = Flask(__name__)
CORS(app)

DB_PATH = r'C:\Users\user\OneDrive\New folder\OneDrive\Desktop\analytic project\student_health.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/dashboard-data', methods=['GET'])
def get_dashboard_data():
    conn = get_db_connection()
    
    kpi_query = '''
        SELECT 
            COUNT(visit_id) as total_visits,
            COUNT(DISTINCT student_id) as unique_patients
        FROM Visits
    '''
    kpis = dict(conn.execute(kpi_query).fetchone())

    symp_query = 'SELECT symptoms, COUNT(*) as count FROM Visits GROUP BY symptoms ORDER BY count DESC LIMIT 5'
    symptoms = {row['symptoms']: row['count'] for row in conn.execute(symp_query).fetchall()}

    diag_query = 'SELECT diagnosis, COUNT(*) as count FROM Visits GROUP BY diagnosis ORDER BY count DESC LIMIT 5'
    diagnoses = {row['diagnosis']: row['count'] for row in conn.execute(diag_query).fetchall()}
 
    df = pd.read_sql_query('SELECT visit_date FROM Visits', conn)
    df['visit_date'] = pd.to_datetime(df['visit_date'])
    df['month'] = df['visit_date'].dt.strftime('%Y-%m') 
    trend_counts = df.groupby('month').size().tail(6).to_dict() 
    
    conn.close()
    
    return jsonify({
        'status': 'success',
        'data': {
            'kpis': kpis,
            'symptoms': symptoms,
            'diagnoses': diagnoses,
            'trends': trend_counts
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
