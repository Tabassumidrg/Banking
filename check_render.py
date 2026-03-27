import urllib.request
import json
import os

def get_render_token():
    tokens_path = r"d:\saif\Banking\tokens"
    if os.path.exists(tokens_path):
        with open(tokens_path, "r") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if "Render" in line and (i + 2) < len(lines):
                    return lines[i+2].split("Value")[-1].strip()
    return None

TOKEN = get_render_token()
SERVICE_ID = "srv-d7142kogjchc73983d80"

if not TOKEN:
    print("No Render token")
    exit(1)

url = f"https://api.render.com/v1/services/{SERVICE_ID}/deploys?limit=1"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json"
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print(json.dumps(data, indent=2))
except Exception as e:
    print(e)
