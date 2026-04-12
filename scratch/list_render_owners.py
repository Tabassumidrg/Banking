import urllib.request
import json

TOKEN = "rnd_WQXA6hk82WxKoXPo2opvnyeRjVbG"

def list_owners():
    url = "https://api.render.com/v1/owners"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json"
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("Owners found:")
            for item in data:
                owner = item['owner']
                print(f" - Name: {owner['name']}, ID: {owner['id']}, Email: {owner['email']}")
    except Exception as e:
        print(f"Error listing owners: {e}")

if __name__ == "__main__":
    list_owners()
