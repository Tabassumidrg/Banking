import urllib.request
import json

TOKEN = "rnd_WQXA6hk82WxKoXPo2opvnyeRjVbG"

def list_services():
    url = "https://api.render.com/v1/services"
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
    except Exception as e:
        print(f"Error listing services: {e}")

if __name__ == "__main__":
    list_services()
