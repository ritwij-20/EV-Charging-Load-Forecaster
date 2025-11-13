EV Charging Load Forecaster (with Gen-AI Chatbot)
⚡ EV Charging Load Forecaster & Gen-AI Operator Chatbot

A complete EV Charging Station Load Forecasting System that combines Machine Learning, Time-Series Pattern Analysis, and a ChatGPT-style Gen-AI Chatbot to assist EV charging station operators.

This project predicts hourly/daily load, identifies peak hours, analyzes charging session patterns, and provides an intelligent chatbot interface for operator queries.

🚀 Project Highlights
🔥 Machine Learning Models (Week 1)

Trained Prophet model for time-series load forecasting

Trained XGBoost Regressor on engineered features

Compared ML performance (MAE, RMSE)

Generated synthetic forecasts (now optional)

🤖 Gen-AI Chatbot (Week 2)

Understands natural language:

“Load tomorrow?”

“Load on 15-11-2025?”

“Day after tomorrow?”

“Show detailed forecast.”

ChatGPT-style chat UI

Remembers last date for follow-ups

Always returns valid predictions using pattern-based forecasting

Hour-by-hour breakdown on request

Charging station insights, peak hours, weekly summary

📊 Interactive Dashboard

Built with Streamlit featuring:

Chatbot interface

Hourly EV load graphs

Weekly trend graph

Energy consumption by charger type

Peak hours visualization

Charging sessions data view

🧠 How Forecasting Works (Pattern-Only Strategy)

Since historical data timestamps did not match current dates, a robust pattern-only method is used:

Detect the weekday of the requested date

Compute the average hourly load pattern for that weekday

Generate:

Total daily load

Peak hour

24-hour predicted curve

If weekday data missing → fallback to global hourly pattern

This ensures:
✔ No Prophet errors
✔ No XGBoost date mismatches
✔ 100% stability
✔ Accurate pattern-based behavior

🧩 Project Structure
EV_Load_Forecaster/
│── app.py                      # Streamlit UI (ChatGPT style + dashboard tabs)
│── chatbot.py                  # Pattern-based Gen-AI chatbot logic
│── data_utils.py               # Data loaders + preprocessing utilities
│── hourly_ev_load.csv          # Hourly load data
│── ev_charging_patterns.csv    # Charging session data
│── prophet_forecast.csv        # (Optional) Prophet output
│── xgb_predictions.csv         # (Optional) XGBoost output
│── train_prepared.csv          # ML training data
│── test_prepared.csv           # ML test data
│── model_comparison_results.csv# ML metrics
│── README.md                   # Project documentation
└── ...

⚙️ Installation & Setup
1️⃣ Create/Activate Environment
conda activate your-env

2️⃣ Install Dependencies
pip install streamlit python-dateutil pandas altair


Optional ML packages:

pip install prophet xgboost scikit-learn

▶️ Run the Application
streamlit run app.py


Open your browser at:
👉 http://localhost:8501

💬 Using the Chatbot
🔹 Example Questions:

“Hi”

“What will be the load tomorrow?”

“What will be the load on 15-11-2025?”

“Show detailed forecast for that day”

“What are the peak hours this week?”

“Which charger type is used the most?”

“Weekly load summary”

🔹 Chatbot Features:

ChatGPT-style UI

Input fixed at bottom

Auto-clear text

Auto-scroll

Hourly chart rendering

Memory of previous date

📈 Dashboard Features
📊 Raw Hourly Data

Data table

Line chart (energy_kwh over time)

🚗 Charging Sessions

Data table

Charger-type energy bar chart

📈 Weekly Summary

Last 7-day load chart

🔥 Peak Hours

Bar chart of top peak hours

🛠️ Tech Stack

Python

Streamlit

Pandas

Altair

Dateutil

(Optional) Prophet, XGBoost

Custom Gen-AI Chatbot logic

🧪 ML Model Performance

From model comparison:

Model	MAE	RMSE
Prophet	18.52	24.87
XGBoost	12.43	16.71

XGBoost performed better, but pattern-based forecasting is used in the chatbot for maximum stability.

🎯 Why Pattern-Based Forecasting?

Because your dataset timestamps (2024) didn’t match system dates (2025), Prophet/XGB future predictions caused:

❌ Missing forecast dates
❌ “Forecast unavailable” errors
❌ Wrong horizons

Pattern-based forecasting:

✔ Requires no future timestamps
✔ Works with ANY date
✔ Never errors
✔ Ideal for Gen-AI chatbot
✔ Perfect for academic project demonstration

🚀 Future Improvements

Add real Prophet/XGBoost live forecast switching

Add PDF report generation

Add EV demand simulation (+10%, +20% load scenario)

Add Google Maps charger visualization

Add user login & saved chat sessions

Add cloud deployment (Streamlit Cloud)

🙌 Acknowledgements

This project was developed as part of the EV Charging Station Load Forecaster module with:

ML modeling (Week 1)

Gen-AI integration (Week 2)


Interactive dashboard using Streamlit
