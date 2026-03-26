import urllib.request
import urllib.error
import json
import os

# Path to tokens file
TOKENS_PATH = r"d:\saif\Banking\tokens"

def get_tokens():
    tokens = {}
    if os.path.exists(TOKENS_PATH):
        with open(TOKENS_PATH, "r") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if "Render" in line and (i + 2) < len(lines):
                    tokens["RENDER"] = lines[i+2].split("Value")[-1].strip()
                if "Vercel" in line and (i + 2) < len(lines):
                    tokens["VERCEL"] = lines[i+2].split("Value")[-1].strip()
    return tokens

tokens = get_tokens()
RENDER_API_KEY = tokens.get("RENDER")
REPO_URL = "https://github.com/yodakumarbasappahugar-byte/Banking"
DATABASE_URL = os.environ.get("DATABASE_URL", "")

def get_owner_id(headers):
    req = urllib.request.Request("https://api.render.com/v1/owners", headers=headers)
    with urllib.request.urlopen(req) as resp:
        owners = json.loads(resp.read().decode('utf-8'))
        if owners:
            return owners[0]['owner']['id']
    return None

def create_web_service():
    if not RENDER_API_KEY:
        print("Missing Render API key in tokens file.")
        return

    url = "https://api.render.com/v1/services"
    
    headers = {
        "Authorization": f"Bearer {RENDER_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    owner_id = get_owner_id(headers)
    if not owner_id:
        print("Could not find an owner ID for this account.")
        return

    payload = {
        "type": "web_service",
        "name": "banking-backend-api",
        "ownerId": owner_id,
        "repo": REPO_URL,
        "branch": "main",
        "autoDeploy": "yes",
        "serviceDetails": {
            "env": "python",
            "envSpecificDetails": {
                "buildCommand": "pip install -r requirements.txt",
                "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT"
            },
            "region": "oregon",
            "plan": "free"
        },
        "envVars": [
            {
                "key": "DATABASE_URL",
                "value": DATABASE_URL
            }
        ]
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req) as resp:
            response_data = json.loads(resp.read().decode('utf-8'))
            print("Successfully created Render service!")
            service_url = response_data.get('service', {}).get('serviceDetails', {}).get('url', 'URL not found')
            print(f"Service URL: {service_url}")
            print(f"Dashboard URL: {response_data.get('dashboardUrl', '')}")
            return service_url
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    create_web_service()
