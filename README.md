# 📊 Smart Expense & Financial Risk Analyzer

An AI/ML-powered personal finance analysis application that analyzes transaction data, detects unusual spending patterns, evaluates financial health, and predicts next-month expenses.

🔗 **Live Demo:** https://financial-risk-analyzer-2026.streamlit.app/

---

## 🚀 Features

### 💰 Financial Analysis

* Calculates total income, expenses, and savings
* Computes expense ratio and savings rate
* Analyzes spending across different categories

### ❤️ Financial Health Assessment

* Generates a financial health score out of 100
* Determines financial risk level
* Evaluates spending and savings behavior

### ⚠️ Anomaly Detection

* Identifies unusual financial transactions
* Helps users detect potentially abnormal spending patterns

### 📈 Spending Analysis

* Category-wise expense analysis
* Monthly spending trend visualization
* Identifies the highest-spending category

### 🔮 Expense Prediction

Predicts the expected expense for the next month using historical spending patterns.

The project evaluates multiple machine learning models:

* Linear Regression
* Random Forest
* Gradient Boosting

The model with the lowest MAE is selected as the best-performing model.

### 💡 Smart Recommendations

Provides personalized recommendations based on:

* Savings rate
* Expense ratio
* Financial health
* Detected anomalies

### 📥 Report Generation

Users can download an analysis report containing the financial insights.

---

## 🧠 Machine Learning

The project compares three regression algorithms:

| Model             | Purpose                      |
| ----------------- | ---------------------------- |
| Linear Regression | Baseline prediction model    |
| Random Forest     | Non-linear ensemble model    |
| Gradient Boosting | Advanced ensemble prediction |

### Best Model

**Gradient Boosting** achieved the best performance based on Mean Absolute Error (MAE) for the current dataset.

The current application predicts:

**Next Month Expense: ₹22,573.34**

---

## 📊 Current Dataset

The application works with a personal finance transaction dataset containing:

* Date
* Transaction Description
* Category
* Amount
* Type

The current dataset contains approximately **1,500 transactions**.

---

## 🏗️ Project Structure

```text
Smart-Expense-Financial-Risk-Analyzer/
│
├── backend/
│   ├── main.py
│   ├── routes/
│   │   └── prediction_routes.py
│   └── services/
│       └── prediction_service.py
│
├── src/
│   ├── anomaly_detection.py
│   ├── data_processing.py
│   ├── financial_analysis.py
│   ├── financial_health.py
│   ├── prediction.py
│   └── test_ml_pipeline.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── data/
│   └── Personal_Finance_Dataset.csv
│
├── notebooks/
│   └── ML_Analysis.ipynb
│
├── app.py
├── requirements.txt
└── .gitignore
```

---

## 🛠️ Technologies Used

**Programming**

* Python

**Data Analysis**

* Pandas
* NumPy

**Machine Learning**

* Scikit-learn
* Linear Regression
* Random Forest
* Gradient Boosting

**Visualization & Dashboard**

* Streamlit

**Backend**

* FastAPI

**Development Tools**

* VS Code
* Jupyter Notebook
* Git
* GitHub

---

## ⚙️ How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/jasvitha2007/smart-expense-financial-risk-analyzer.git
cd smart-expense-financial-risk-analyzer
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Streamlit application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🔄 Application Workflow

```text
Upload CSV
     ↓
Data Processing
     ↓
Financial Analysis
     ↓
Anomaly Detection
     ↓
Financial Health Assessment
     ↓
ML Model Training & Comparison
     ↓
Next-Month Expense Prediction
     ↓
Smart Recommendations
     ↓
Download Report
```

---

## 📌 Example Results

For the current dataset:

* **Total Income:** ₹734,087
* **Total Expenses:** ₹1,227,194.37
* **Total Savings:** -₹493,107.37
* **Financial Health Score:** 15/100
* **Risk Level:** High Risk
* **Expense Ratio:** 167.17%
* **Savings Rate:** -67.17%
* **Detected Anomalies:** 75
* **Best ML Model:** Gradient Boosting
* **Predicted Next-Month Expense:** ₹22,573.34

---

## 🎯 Future Improvements

* User authentication and individual financial profiles
* Database integration for persistent transaction storage
* More advanced time-series forecasting
* Interactive budget planning
* Expense alerts and notifications
* Improved anomaly detection using advanced ML techniques
* Deployment with scalable cloud infrastructure

---

## 👩‍💻 Project

**Smart Expense & Financial Risk Analyzer**

Built as an AI/ML and data analytics portfolio project to demonstrate data processing, machine learning, anomaly detection, financial risk analysis, visualization, and deployment.
