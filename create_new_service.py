import urllib.request
import urllib.error
import json
import os

RENDER_API_KEY = "rnd_WQXA6hk82WxKoXPo2opvnyeRjVbG"
REPO_URL = "https://github.com/Tabassumidrg/Banking"
OWNER_ID = "tea-d6t4uchj16oc73f46290"
DATABASE_URL = "postgresql://neondb_owner:npg_2fn3ecHTjFkN@ep-long-grass-amjlgvmu.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require"

def create_web_service():
    url = "https://api.render.com/v1/services"
    
    headers = {
        "Authorization": f"Bearer {RENDER_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "type": "web_service",
        "name": "banking-backend-final",
        "ownerId": OWNER_ID,
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

    print("Creating Render service...")
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("Successfully created Render service!")
            print(f"Service ID: {data.get('id')}")
            print(f"Service URL: {data.get('serviceDetails', {}).get('url')}")
            print(f"Dashboard URL: {data.get('dashboardUrl')}")
            return data
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    create_web_service()
