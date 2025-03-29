import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Token acquisition using session information
url = "https://elearn.sinclair.edu/d2l/lp/auth/oauth2/token"

# Read cookies and CSRF token from .env
cookies = {
    "d2lSessionVal": os.getenv("D2L_SESSION_VAL"),
    "d2lSecureSessionVal": os.getenv("D2L_SECURE_SESSION_VAL")
}
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "x-csrf-token": os.getenv("X_CSRF_TOKEN")
}
payload = {
    "scope": "*:*:*"
}

response = requests.post(url, headers=headers, cookies=cookies, data=payload)

if response.status_code == 200:
    token_data = response.json()

    if "expires_at" in token_data:
        current_time = datetime.now().timestamp()
        remaining_minutes = (token_data["expires_at"] - current_time) / 60
        print(f"Token will expire in approximately {remaining_minutes:.1f} minutes.")
    
    with open("token.json", "w", encoding="utf-8") as f:
        json.dump(token_data, f, indent=4, ensure_ascii=False)
    print("Token acquired and saved to token.json!")
else:
    print(f"Error: {response.status_code}")
    print(response.text)