import urllib.request
import json

TOKEN = "rnd_WQXA6hk82WxKoXPo2opvnyeRjVbG"

def find_service_by_name():
    # 1. Get all owners
    owners_req = urllib.request.Request("https://api.render.com/v1/owners", headers={"Authorization": f"Bearer {TOKEN}"})
    with urllib.request.urlopen(owners_req) as resp:
        owners = json.loads(resp.read().decode('utf-8'))
        
    for item in owners:
        owner_id = item['owner']['id']
        print(f"Checking owner: {item['owner']['name']} ({owner_id})")
        
        # 2. Get services for this owner
        svc_req = urllib.request.Request(f"https://api.render.com/v1/services?ownerId={owner_id}", headers={"Authorization": f"Bearer {TOKEN}"})
        try:
            with urllib.request.urlopen(svc_req) as resp:
                services = json.loads(resp.read().decode('utf-8'))
                for s_item in services:
                    svc = s_item['service']
                    print(f" - Found Service: {svc['name']} (ID: {svc['id']}) URL: {svc['serviceDetails'].get('url')}")
                    if "banking-backend-api" in svc['name']:
                        print("FOUND TARGET!")
        except Exception as e:
            print(f"Error checking owner {owner_id}: {e}")

if __name__ == "__main__":
    find_service_by_name()
