import urllib.request
import urllib.error
import json
import os

# Path to tokens file
TOKENS_PATH = r"d:\saif\Banking\tokens"

def get_render_token():
    if os.path.exists(TOKENS_PATH):
        with open(TOKENS_PATH, "r") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if "Render" in line and (i + 2) < len(lines):
                    return lines[i+2].split("Value")[-1].strip()
    return None

def get_service_url(service_name, token):
    url = "https://api.render.com/v1/services?limit=20"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as resp:
            services = json.loads(resp.read().decode('utf-8'))
            for s in services:
                if s['service']['name'] == service_name:
                    return s['service']['serviceDetails']['url']
    except Exception as e:
        print(f"Error fetching services: {str(e)}")
    return None

if __name__ == "__main__":
    token = get_render_token()
    if not token:
        print("Render token not found.")
        exit(1)
        
    url = get_service_url("banking-backend-api", token)
    if url:
        print(f"RENDER_URL={url}")
    else:
        print("Service not found.")
