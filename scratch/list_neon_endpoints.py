import urllib.request
import json

TOKEN = "napi_h3jx72jqb3vj8ya54lutf6r2p9xdtjelhszx3oxd1u34fuji4744ndg2adunu4wj"
PROJECT_ID = "aged-paper-21106693"

def list_neon_endpoints():
    url = f"https://console.neon.tech/api/v2/projects/{PROJECT_ID}/endpoints"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json"
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("Neon Endpoints found:")
            for ep in data.get('endpoints', []):
                print(f" - Host: {ep['host']}, ID: {ep['id']}, Type: {ep['type']}")
    except Exception as e:
        print(f"Error listing Neon endpoints: {e}")

if __name__ == "__main__":
    list_neon_endpoints()
