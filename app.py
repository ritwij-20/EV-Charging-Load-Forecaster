import streamlit as st
import pandas as pd
from chatbot import operator_chatbot
from data_utils import load_hourly, load_sessions
import altair as alt

st.set_page_config(page_title="EV Load Forecaster", layout="wide")

# ---------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["💬 Chatbot", "📊 Raw Hourly Data", "🚗 Charging Sessions", "📈 Weekly Summary", "🔥 Peak Hours"],
)


# ---------------------------------------------------
# 1️⃣ CHATBOT PAGE (ChatGPT-Style)
# ---------------------------------------------------
if page == "💬 Chatbot":
    st.title("⚡ EV-Charging Load Forecaster Chatbot")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Clear Chat
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.clear()
        st.rerun()

    # Chat History
    chat_container = st.container()
    with chat_container:
        st.markdown("### 💬 Conversation")

        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(
                    f"""
                    <div style="text-align:right; margin:8px;">
                        <div style="
                            display:inline-block;
                            background:#0059ff;
                            color:white;
                            padding:10px 14px;
                            border-radius:12px;
                            max-width:70%;
                            font-size:16px;">
                            {msg['text']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div style="text-align:left; margin:8px;">
                        <div style="
                            display:inline-block;
                            background:#1e1e1e;
                            color:white;
                            padding:10px 14px;
                            border-radius:12px;
                            max-width:70%;
                            font-size:16px;">
                            {msg['text']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # ⭐ If message is hourly forecast, render graph
            if msg["role"] == "bot" and "Hour-by-hour" in msg["text"]:
                # Load last forecast from chatbot memory
                from chatbot import _last_forecast_df
                if _last_forecast_df is not None:
                    chart = alt.Chart(_last_forecast_df.reset_index()).mark_line().encode(
                        x="index:T",
                        y="pred:Q"
                    ).properties(
                        width=700,
                        height=300,
                        title="24-Hour Forecast Chart"
                    )
                    st.altair_chart(chart, use_container_width=True)

    st.markdown("---")

    # Input at bottom
    input_key = f"chat_input_{len(st.session_state.chat_history)}"
    user_input = st.text_input("You:", key=input_key, label_visibility="collapsed")
    send = st.button("Send", key=f"send_{input_key}")

    if send:
        if user_input.strip():
            st.session_state.chat_history.append({"role": "user", "text": user_input})
            with st.spinner("Thinking..."):
                reply = operator_chatbot(user_input)
            st.session_state.chat_history.append({"role": "bot", "text": reply})
            st.rerun()


# ---------------------------------------------------
# 2️⃣ RAW HOURLY DATA
# ---------------------------------------------------
elif page == "📊 Raw Hourly Data":
    st.title("📊 Raw Hourly Load Data")
    df = load_hourly()

    if df is None:
        st.error("hourly_ev_load.csv not found.")
    else:
        st.dataframe(df, use_container_width=True)

        st.markdown("### 🔥 Hourly Load Line Chart")
        st.line_chart(df.set_index("timestamp")["energy_kwh"])


# ---------------------------------------------------
# 3️⃣ CHARGING SESSIONS
# ---------------------------------------------------
elif page == "🚗 Charging Sessions":
    st.title("🚗 Charging Sessions Data")
    df = load_sessions()

    if df is None:
        st.error("ev_charging_patterns.csv missing.")
    else:
        st.dataframe(df, use_container_width=True)

        if "Charger Type" in df.columns:
            st.markdown("### ⚡ Energy Consumption by Charger Type")
            chart = alt.Chart(
                df.groupby("Charger Type")["Energy Consumed (kWh)"]
                .sum()
                .reset_index()
            ).mark_bar().encode(
                x="Charger Type:N",
                y="Energy Consumed (kWh):Q",
            )
            st.altair_chart(chart, use_container_width=True)


# ---------------------------------------------------
# 4️⃣ WEEKLY SUMMARY
# ---------------------------------------------------
elif page == "📈 Weekly Summary":
    st.title("📈 Weekly Summary")

    df = load_hourly()
    if df is None:
        st.error("hourly_ev_load.csv missing.")
    else:
        df["date"] = df["timestamp"].dt.date
        daily = df.groupby("date")["energy_kwh"].sum().tail(7)

        st.markdown("### 🔷 Last 7 Days Load Trend")
        st.line_chart(daily)


# ---------------------------------------------------
# 5️⃣ PEAK HOURS
# ---------------------------------------------------
elif page == "🔥 Peak Hours":
    st.title("🔥 Peak Hours (Last 7 Days)")

    df = load_hourly()
    if df is None:
        st.error("hourly_ev_load.csv missing.")
    else:
        recent = df[df["timestamp"] >= (df["timestamp"].max() - pd.Timedelta(days=7))]
        recent["hour"] = recent["timestamp"].dt.hour

        peaks = recent.groupby("hour")["energy_kwh"].mean().sort_values(ascending=False).head(5)

        st.markdown("### ⏰ Top Peak Hours (Avg kWh)")
        st.bar_chart(peaks)
