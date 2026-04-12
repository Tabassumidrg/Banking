import urllib.request
import json

TOKEN = "napi_h3jx72jqb3vj8ya54lutf6r2p9xdtjelhszx3oxd1u34fuji4744ndg2adunu4wj"
PROJECT_ID = "aged-paper-21106693"

def list_neon_branches():
    url = f"https://console.neon.tech/api/v2/projects/{PROJECT_ID}/branches"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json"
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("Neon Branches found:")
            for br in data.get('branches', []):
                print(f" - Name: {br['name']}, ID: {br['id']}, Primary: {br['primary']}")
    except Exception as e:
        print(f"Error listing Neon branches: {e}")

if __name__ == "__main__":
    list_neon_branches()
