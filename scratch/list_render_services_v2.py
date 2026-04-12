import urllib.request
import json

TOKEN = "rnd_WQXA6hk82WxKoXPo2opvnyeRjVbG"
OWNER_ID = "tea-d6t4uchj16oc73f46290"

def list_services():
    url = f"https://api.render.com/v1/services?ownerId={OWNER_ID}"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json"
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("Services found:")
            for item in data:
                svc = item['service']
                print(f" - Name: {svc['name']}, ID: {svc['id']}, URL: {svc['serviceDetails'].get('url', 'N/A')}")
                print(f"   Repo: {svc.get('repo', 'N/A')}")
    except Exception as e:
        print(f"Error listing services: {e}")

if __name__ == "__main__":
    list_services()
