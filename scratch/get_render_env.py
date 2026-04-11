import urllib.request
import json
import os

TOKEN = "rnd_WQXA6hk82WxKoXPo2opvnyeRjVbG"
SERVICE_ID = "srv-d7142kogjchc73983d80"

def get_env_vars():
    url = f"https://api.render.com/v1/services/{SERVICE_ID}/env-vars"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json"
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("Environment Variables:")
            for item in data:
                ev = item['envVar']
                # Mask password in URL for safety if needed, but I need to see it to check
                print(f" - {ev['key']}: {ev['value']}")
    except Exception as e:
        print(f"Error fetching env vars: {e}")

if __name__ == "__main__":
    get_env_vars()
