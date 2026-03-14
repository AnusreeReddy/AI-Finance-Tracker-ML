# 💰 AI-Based Personal Finance Tracker

A web-based finance tracking system that records, categorizes, and analyzes user transactions using machine learning.

The application helps users understand their spending patterns and manage finances through automated expense categorization and visual dashboards.

---

# 🚀 Features

- Add and manage personal financial transactions
- Machine learning based **automatic expense categorization**
- Visual dashboards for **expense distribution and savings trends**
- User authentication system (login / registration)
- Interactive transaction history

---

# 🧠 Machine Learning

The system uses a **Scikit-learn classification model** to automatically categorize transactions based on textual descriptions.

### ML Pipeline

1. Data preprocessing and cleaning  
2. Feature extraction from transaction descriptions  
3. Model training using Scikit-learn  
4. Predicting expense categories for new transactions  

---

# 🛠 Technologies Used

## Backend
- Python
- Flask
- Scikit-learn
- Pandas

## Frontend
- HTML
- CSS
- JavaScript

## Data Visualization
- Matplotlib

---

---
# Project Structure

backend/     → Flask backend and ML logic  
frontend/    → HTML, CSS, JavaScript interface  
models/      → Trained machine learning models  
dataset/     → Training dataset for expense classification 

---

# ⚙️ How to Run the Project

Clone the repository:

    git clone <repo-link>
    cd finance-tracker

Install dependencies:

    pip install -r requirements.txt

Run the application:

    python app.py

The application will start locally and open in your browser.

---

# 📊 Future Improvements

- Budget prediction using time-series models
- Smart financial alerts
- Personalized spending recommendations
- Mobile responsive interface improvements

---

