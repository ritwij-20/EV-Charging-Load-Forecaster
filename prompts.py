# prompts.py

SYSTEM_PROMPT = (
    "You are an assistant for EV charging station operators. Be concise, factual, "
    "and cite numbers from the provided context when available. If a requested file "
    "or data is missing, clearly tell the operator which file is required."
)

TEMPLATE_FORECAST_NEXT_HOUR = (
    "Context:\n{context}\n\n"
    "Question: Based on the above, tell me the predicted energy (kWh) for {ts} and "
    "compare it briefly with the same hour yesterday. Provide a one-line recommendation for operators."
)

TEMPLATE_EXPLAIN_PREDICTION = (
    "Context:\n{context}\n\n"
    "Question: Explain why the model predicted a high load at {ts}. Use the top 3 features if available. "
    "Keep answer to two sentences and offer one operator action."
)

TEMPLATE_PEAK_HOURS = (
    "Context:\n{context}\n\n"
    "Question: What are the peak hours for the selected period (give top 3 hours) "
    "and one short operational recommendation."
)
