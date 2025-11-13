# chatbot.py
"""
EV Load Forecasting Chatbot (Pattern-Based, Safe & Intelligent)
---------------------------------------------------------------
Features:
- Predict load for any date (pattern-based)
- Show detailed hour-by-hour forecast
- Understand natural language dates (yesterday, tomorrow, next Monday)
- Explain how forecasting works
- Tell what it can do
- Identify itself (“Who are you?”)
- Reject unrelated/gibberish queries politely
- Never outputs forecasts unless EV-related
- Remembers last date for follow-ups
"""

from datetime import datetime, timedelta
from dateutil.parser import parse as dt_parse
import calendar
import re
import pandas as pd
from data_utils import load_hourly, load_sessions, today_date

# Memory for last forecasted date
_last_date = None
_last_forecast_df = None


# ------------------------------------------------------------
# DATE PARSING UTILITIES
# ------------------------------------------------------------
WEEKDAYS = {w.lower(): i for i, w in enumerate(calendar.day_name)}


def _parse_relative(text):
    t = text.lower()
    today = today_date()

    if "day before yesterday" in t: return today - timedelta(days=2)
    if "yesterday" in t: return today - timedelta(days=1)
    if "day after tomorrow" in t: return today + timedelta(days=2)
    if "tomorrow" in t: return today + timedelta(days=1)
    if "today" in t: return today
    return None


def _parse_weekday(text):
    t = text.lower()
    today = today_date()
    wd_today = today.weekday()

    # next/last/this Monday
    m = re.search(r'\b(next|last|this)\s+(' + "|".join(WEEKDAYS) + r')\b', t)
    if m:
        qualifier, word = m.group(1), m.group(2)
        target = WEEKDAYS[word]

        if qualifier == "next":
            diff = (target - wd_today) % 7 or 7
            return today + timedelta(days=diff)
        if qualifier == "last":
            diff = (wd_today - target) % 7 or 7
            return today - timedelta(days=diff)
        if qualifier == "this":
            diff = (target - wd_today) % 7
            return today + timedelta(days=diff)

    # “on Monday”
    m2 = re.search(r'\b(on\s+)?(' + "|".join(WEEKDAYS) + r')\b', t)
    if m2:
        word = m2.group(2)
        target = WEEKDAYS[word]
        diff = (target - wd_today) % 7
        return today + timedelta(days=diff)

    return None


def _parse_explicit(text):
    try:
        return dt_parse(text, dayfirst=True, fuzzy=True).date()
    except:
        return None


def parse_date_from_text(text):
    return _parse_relative(text) or _parse_weekday(text) or _parse_explicit(text)


# ------------------------------------------------------------
# PATTERN-ONLY FORECASTING
# ------------------------------------------------------------
def _weekday_profile(wd):
    df = load_hourly()
    if df is None or df.empty:
        return None, "no_data"

    df["wd"] = df["timestamp"].dt.weekday
    df["hour"] = df["timestamp"].dt.hour

    same = df[df["wd"] == wd]

    if not same.empty:
        profile = same.groupby("hour")["energy_kwh"].mean().to_dict()
        return profile, "weekday_pattern"

    # fallback → global hourly pattern
    profile = df.groupby("hour")["energy_kwh"].mean().to_dict()
    return profile, "global_hourly_avg"


def forecast_for_date(d):
    wd = d.weekday()
    profile, src = _weekday_profile(wd)

    if profile is None:
        return None, src, None

    base = datetime.combine(d, datetime.min.time())
    hours = [base + timedelta(hours=i) for i in range(24)]

    avg = sum(profile.values()) / len(profile)
    preds = [profile.get(h.hour, avg) for h in hours]

    df = pd.DataFrame({"pred": preds}, index=pd.to_datetime(hours))
    total = df["pred"].sum()
    return df, src, total


# ------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------
def _remember(d):
    global _last_date, _last_forecast_df
    df, src, total = forecast_for_date(d)
    _last_date = d
    _last_forecast_df = df
    return df, src, total


def _friendly_total(date, total, src):
    dayname = calendar.day_name[date.weekday()]
    txt = (
        f"📅 **{date.strftime('%d %b %Y')} ({dayname})**\n"
        f"🔋 **Expected total load:** ~{total:.2f} kWh\n"
        f"📘 *Based on: {src} pattern*\n\n"
    )
    if _last_forecast_df is not None:
        peak_ts = _last_forecast_df['pred'].idxmax()
        peak_val = _last_forecast_df['pred'].max()
        txt += f"⏰ **Peak hour:** {peak_ts.strftime('%H:%M')} (~{peak_val:.2f} kWh)\n\n"

    txt += "💡 Tips: Shift flexible charging to low-demand hours and use load balancing during peaks."
    return txt


def _friendly_hours(df, src):
    lines = [f"🕒 **Hour-by-hour forecast** (source: {src}):\n"]
    for idx, r in df.iterrows():
        lines.append(f"• {idx.strftime('%H:%M')} → {r['pred']:.2f} kWh")
    return "\n".join(lines)


# ------------------------------------------------------------
# MAIN CHATBOT ROUTER
# ------------------------------------------------------------
def operator_chatbot(user_input: str):
    global _last_date, _last_forecast_df

    if not user_input or not user_input.strip():
        return "Please ask something like: 'Load tomorrow' or 'Load on 15-11-2025'."

    q = user_input.lower().strip()

    # ---------------- GREETING ----------------
    if q in ["hi", "hello", "hey", "hii", "hola"]:
        return "Hello! 👋 How can I help you with EV load forecasting today?"

    # ---------------- WHO ARE YOU ----------------
    if any(p in q for p in ["who are you", "what are you", "who is this", "who am i talking to"]):
        return (
            "I'm an **EV Load Forecasting Assistant** ⚡\n\n"
            "I help operators predict EV charging station load, identify peak hours, "
            "analyze usage patterns, and understand future demand."
        )

    # ---------------- WHAT CAN YOU DO ----------------
    if any(p in q for p in ["what can you do", "help", "capabilities", "features", "what do you do"]):
        return (
            "Here’s what I can do! ⚡\n\n"
            "• Predict load for any date (e.g., 15-11-2025)\n"
            "• Show detailed hour-by-hour forecast\n"
            "• Understand natural language dates (tomorrow, next Monday)\n"
            "• Identify peak hours\n"
            "• Provide weekly summary\n"
            "• Analyze charger-level usage\n"
            "• Explain how forecasting works\n"
            "• Smart follow-up memory\n"
        )

    # ---------------- EXPLAIN HOW YOU WORK ----------------
    if any(p in q for p in [
        "how do you work", "how are you forecasting", "how does this work",
        "explain how you work", "how do you predict", "how are you predicting",
        "how is prediction made", "how are you predicting the future load"
    ]):
        return (
            "Here’s how I predict the future EV load! ⚙️\n\n"
            "1. I read past hourly EV load data.\n"
            "2. I detect which weekday the requested date belongs to.\n"
            "3. I build an average hourly load pattern for that weekday.\n"
            "4. If weekday data is missing, I use global hourly averages.\n"
            "5. I generate total load + peak hour.\n"
            "6. If you ask 'show detailed', I provide a full 24-hour breakdown.\n\n"
            "This approach is stable and avoids issues with missing future dates."
        )

    # ---------------- DETAILED FORECAST ----------------
    if any(k in q for k in ["detailed", "hour-by-hour", "hourly", "show hours", "hourly forecast"]):
        if _last_date is None:
            return "Which date do you want the detailed forecast for?"
        return _friendly_hours(_last_forecast_df, "pattern_cached")

    # ---------------- UNRELATED / GIBBERISH DETECTION ----------------
    ev_related = ["load", "forecast", "charging", "station", "capacity", "ev", "energy", "peak"]
    maybe_date = parse_date_from_text(user_input)

    if not any(w in q for w in ev_related) and maybe_date is None:
        return (
            "Sorry! 🙏 I didn’t understand that.\n\n"
            "I'm designed only for **EV load forecasting** and **charging station insights**.\n"
            "Try asking things like:\n"
            "• 'What will be the load tomorrow?'\n"
            "• 'Load on 15-11-2025'\n"
            "• 'Peak hours this week'\n"
            "• 'Show detailed forecast'"
        )

    # ---------------- DATE PARSING + FORECAST ----------------
    d = parse_date_from_text(user_input)
    if d is None:
        d = today_date() + timedelta(days=1)

    df, src, total = _remember(d)
    return _friendly_total(d, total, src)
