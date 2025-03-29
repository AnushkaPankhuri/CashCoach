# CashCoach - Real-Time Personal Finance Tracker

CashCoach is a **persona-driven**, **real-time personal finance tracker** that not only visualizes your spending but also acts as a **personal finance coach**, empowering you to make informed financial decisions instantly.

---

## Features

- **Interactive AI Coach**  
  Powered by Fetch AI agents, get personalized financial insights and recommendations.

- **Real-Time Spending Visualizations**  
  Dynamic graphs with daily, weekly, and monthly breakdowns.

- **Smart Alert System**  
  Detects spending anomalies and sends proactive alerts.

- **CSV Upload Support**  
  Simulate bank transactions easily by uploading CSV files.

- **Natural Language Querying**  
  Example: _"Can I afford a ₹1000 dinner?"_

- **Interactive Graphs**  
  Hover for tooltips and category breakdowns.

---

## Modules Overview

| Module | Description |
|--------|-------------|
| Data Ingestion | Upload CSV files; processed by Pathway Vector Store for real-time indexing. |
| Analysis Engine | Fetch AI agents analyze patterns, answer queries, and generate insights. |
| AI Coach | Personalized advice based on your spending behavior. |
| Alert System | Detects anomalies and notifies you instantly. |

---

## Tech Stack

### Frontend
![React](https://img.shields.io/badge/React.js-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-0EA5E9?style=for-the-badge&logo=tailwindcss&logoColor=white)

### Backend
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/DRF-FF1709?style=for-the-badge&logo=django&logoColor=white)

### Real-Time Data
![Pathway Vector Store](https://img.shields.io/badge/Pathway_Vector_Store-F59E0B?style=for-the-badge)

### AI Agent
![Fetch AI uAgents](https://img.shields.io/badge/Fetch_AI_uAgents-5A23D5?style=for-the-badge)

### Visualization
![Chart.js](https://img.shields.io/badge/Chart.js-F5788D?style=for-the-badge&logo=chartdotjs&logoColor=white)

### Database
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

### Data Source
![CSV](https://img.shields.io/badge/User--uploaded_CSV_Files-999999?style=for-the-badge)

---

## Installation (Development Setup)

### Step 1 - Clone the Repository

```powershell
git clone https://github.com/Suhani-T/CashCoach.git
cd cashcoach\finance-tracker
```

### Step 2 - Create Virtual Environment

```powershell
python -m venv env
\env\Scripts\activate
```

### Step 3 - Install Backend Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4 - Apply Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

### Step 5 - Run Development Server

```powershell
python manage.py runserver
```

---

## Future Scope

- Integration with Real Bank APIs (Plaid, Open Banking)
- Spending Goal Tracking
- Voice-based Queries
- Multi-user Support
- Mobile App Extension

---

## Built For

FrostHack 2025 by Team SUAN
