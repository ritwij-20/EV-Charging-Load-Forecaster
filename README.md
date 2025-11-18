
# ⚡ EV Charging Load Forecaster (with Gen-AI Chatbot + Dashboard)

An intelligent EV Charging Station Load Forecasting System powered by  
**Machine Learning**, **Pattern Analysis**, and a **Gen-AI Chatbot**  
with a fully interactive **Streamlit Dashboard**.



---

## 🚀 Live Demo

Experience the full web application here:

👉 **https://ev-charging-load-forecaster.streamlit.app/**  

You can interact with the Gen‑AI chatbot, explore load forecasts, view charging data, and use all dashboard features live.

---

## 📌 Table of Contents
- Overview  
- Week 1 — Machine Learning Models  
- Week 2 — Gen-AI Chatbot  
- Week 3 — Streamlit Dashboard  
- Screenshots  
- Project Structure  
- Installation  
- Run the App  
- Future Enhancements  

---

# 🚀 Overview
This project predicts **daily and hourly EV charging load**, identifies **peak usage hours**, analyzes **charging session trends**, and provides an **AI-powered assistant** for natural-language forecasting queries.

---

# 🧠 Week 1 — Machine Learning Models

### ✔ Data Preprocessing  
- train_prepared.csv  
- test_prepared.csv  

### ✔ Models Implemented  
- Prophet (Time-series forecasting)  
- XGBoost Regressor  

### ✔ Model Comparison  

| Model      | MAE    | RMSE   |
|------------|--------|--------|
| Prophet    | 18.52  | 24.87  |
| XGBoost    | 12.43  | 16.71  |

---

# 🤖 Week 2 — Gen-AI Chatbot

### ✔ Natural Language Understanding  
Handles:
- “Load tomorrow?”  
- “Load on 15‑11‑2025?”  
- “Show detailed forecast”  
- “Peak hours this week?”  
- “Who are you?”  
- “How do you work?”  

### ✔ Features  
- Predict load for **any date**  
- Hour‑by‑hour detailed forecast  
- Peak hour detection  
- Weekly summary  
- Charging session insights  
- Rejects unrelated/gibberish queries  
- Remembers last forecast date  

---

# 🎨 Week 3 — Streamlit Dashboard

Includes:
- Chatbot UI  
- Raw hourly EV load viewer  
- Charging session table  
- Weekly summary visualization  
- Peak hour visualization  

---

# 🖼️ Screenshots  

### 💬 Chatbot  
![Chatbot UI](screenshots/chatbot_ui.png)

### 📊 Raw Hourly Data  
![Raw Hourly Data](screenshots/raw_hourly_data.png)

### 🚗 Charging Sessions  
![Charging Sessions](screenshots/charging_sessions.png)

### 📈 Weekly Summary  
![Weekly Summary](screenshots/weekly_summary.png)

### 🔥 Peak Hours  
![Peak Hours](screenshots/peak_hours.png)

---

# 📂 Project Structure
```
EV_Load_Forecaster/
│── app.py
│── chatbot.py
│── data_utils.py
│── hourly_ev_load.csv
│── ev_charging_patterns.csv
│── train_prepared.csv
│── test_prepared.csv
│── model_comparison_results.csv
│── prophet_forecast.csv
│── xgb_predictions.csv
│── README.md
│── requirements.txt
└── screenshots/
```

---

# ⚙️ Installation
```bash
pip install -r requirements.txt
```

---

# ▶️ Run the App
```bash
streamlit run app.py
```

---

# 🚀 Future Enhancements
- PDF report generator  
- What‑if EV demand simulation  
- Geo‑map visualization  
- Theme toggle (Light/Dark)  
- Live cloud deployment autosync  

---

# 🙌 Credits  
Developed as a 3‑week project:  
- **Week 1:** Machine Learning  
- **Week 2:** Gen‑AI Chatbot  
- **Week 3:** Streamlit Dashboard  





