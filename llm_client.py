# llm_client.py
from dotenv import load_dotenv
load_dotenv()  # 🔹 Load variables from .env file automatically

import os, sys, requests

# --- Debug Information ---
print("\n---DEBUG INFO---")
print("Python executable:", sys.executable)
print("Env key:", os.getenv("OPENROUTER_API_KEY"))
print("----------------\n")

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

def ask_llm(system_prompt: str, user_prompt: str, max_tokens: int = 300, temperature: float = 0.2) -> str:
    """
    Sends a chat completion request to OpenRouter (Gemma 3 27B Free model).
    """
    # ✅ Load the key dynamically every time
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        return "[OpenRouter API key missing — set OPENROUTER_API_KEY in .env file.]"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/ritwij-ai/EV_Load_Forecaster",  # required header
        "X-Title": "EV Charging Load Forecaster",  # app title
    }

    data = {
        "model": "google/gemma-3-27b-it:free",  # ✅ Correct free-tier model
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    try:
        response = requests.post(BASE_URL, headers=headers, json=data)
        response.raise_for_status()

        # ✅ Extract and return model response
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    except Exception as e:
        # 🔍 If API returns JSON error, extract it clearly
        try:
            err_msg = response.json().get("error", {}).get("message", str(e))
        except Exception:
            err_msg = str(e)
        return f"[Error calling OpenRouter API: {err_msg}]"
