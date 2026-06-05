🏥 Student Health Operations Dashboard

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)

An end-to-end data analytics and full-stack web project that simulates a student health clinic's operational dashboard. This project handles the entire data lifecycle: generating realistic mock data, cleaning inconsistencies with Pandas, structuring a relational SQLite database, building a RESTful API with Flask, and visualizing metrics via an interactive JavaScript/Chart.js frontend.

*Note: All data used in this project is 100% synthetically generated using the Python Faker library. No real medical records are used.*

## ✨ Key Features
* **ETL Pipeline:** Automated scripts to generate, clean (impute missing values, standardize formats), and load data.
* **Relational Database Design:** Normalized schema separating demographic data (`Students`) from transactional records (`Visits`).
* **REST API Backend:** Flask server that processes data queries and serves lightweight JSON payloads.
* **Interactive Frontend:** Responsive UI with real-time KPI tracking and dynamic charts (Line, Bar, Doughnut).

## 🛠️ Tech Stack
* **Data Generation & Cleaning:** Python, Pandas, NumPy, Faker
* **Database:** SQLite3
* **Backend:** Flask, Flask-CORS
* **Frontend:** HTML5, CSS3, Vanilla JavaScript, Chart.js
