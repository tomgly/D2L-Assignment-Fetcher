import requests
from datetime import datetime, timedelta, timezone
import json
import os
import subprocess
import time

# Load config
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

D2L_USER_ID = config["user_id"]
D2L_COURSES = config["courses"]
D2L_BASE_URL = "https://46e67f64-7f24-42bc-af15-522e0a90197a.activities.api.brightspace.com"

# Calculate the date range (two week ahead)
start_date = datetime.now(timezone.utc).replace(tzinfo=None)
end_date = start_date + timedelta(days=14)
start = f"{start_date.isoformat(timespec='milliseconds')}Z".replace(":", "%3A")
end = f"{end_date.isoformat(timespec='milliseconds')}Z".replace(":", "%3A")

def check_token_validity():
    try:
        if not os.path.exists("token.json"):
            print("token.json not found! Getting a new token...")
            return refresh_token()

        with open("token.json", "r", encoding="utf-8") as f:
            token_data = json.load(f)
        
        if "expires_at" not in token_data:
            print("No expires_at in token.json! Getting a new token...")
            return refresh_token()
        
        current_time = datetime.now().timestamp()
        remaining_seconds = token_data["expires_at"] - current_time

        if remaining_seconds < 600:
            print(f"Token expiring soon! Only {remaining_seconds / 60:.1f} minutes left. Refreshing...")
            return refresh_token()
        else:
            print(f"Token is valid! {remaining_seconds / 60:.1f} minutes remaining\n")
            return True
    except Exception as e:
        print(f"Error checking token: {e}")
        print("Getting a new token to be safe...")
        return refresh_token()

def refresh_token():
    try:
        print("Getting new token...")
        result = subprocess.run(["python", "d2l_oauth2.py"], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error getting token: {result.stderr}")
            return False

        print("New token acquired!\n")
        time.sleep(1)
        return True
    except Exception as e:
        print(f"Error refreshing token: {e}")
        return False

def get_access_token():
    try:
        with open("token.json", "r", encoding="utf-8") as f:
            token_data = json.load(f)
        return token_data.get("access_token")
    except Exception as e:
        print(f"Error getting access token: {e}")
        return None

def get_assignments():
    if not check_token_validity():
        print("Failed to get valid token!")
        return
    
    access_token = get_access_token()
    if not access_token:
        print("Failed to get access token!")
        return
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    url = f"{D2L_BASE_URL}/users/{D2L_USER_ID}?start={start}&end={end}&activeCoursesOnly=true"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        assignment_data = response.json()
        assignment_links = [
            link["href"]
            for entity in assignment_data["entities"]
            for link in entity["links"]
            if link["rel"][0] in [
                "https://api.brightspace.com/rels/assignment",
                "https://api.brightspace.com/rels/quiz"
            ]
        ]
        for link in assignment_links:
            get_assignment_detail(link, headers)
    else:
        print(f"Failed to get assignments: {response.status_code}")

def get_assignment_detail(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        props = data["properties"]
        course_id = int(url.split("/")[-3])
        course_name = next((c["name"] for c in D2L_COURSES if c["id"] == course_id), "Unknown")
        print(f"\n📚 Course: {course_name}")
        print(f"📝 Assignment: {props['name']}")
        print(f"📄 Description: {props.get('instructionsText', 'No description')}")
        print(f"📅 Due Date: {props.get('dueDate')}")
        print(f"📊 Points: {props.get('outOf')}")
        print(f"🆔 Assignment ID: {url.split('/')[-1]}")
        print("-------------")
    else:
        print(f"Failed to get assignment detail: {response.status_code}")

if __name__ == "__main__":
    print("🚀 Starting to get assignment...\n=============================================")
    get_assignments()
    print("=============================================\n🎉 Process completed!")