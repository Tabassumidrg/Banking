import urllib.request
import json

TOKEN = "napi_h3jx72jqb3vj8ya54lutf6r2p9xdtjelhszx3oxd1u34fuji4744ndg2adunu4wj"

def list_neon_projects():
    url = "https://console.neon.tech/api/v2/projects"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json"
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("Neon Projects found:")
            for proj in data.get('projects', []):
                print(f" - Name: {proj['name']}, ID: {proj['id']}, Region: {proj['region_id']}")
                # List connection strings for each project if possible
    except Exception as e:
        print(f"Error listing Neon projects: {e}")

if __name__ == "__main__":
    list_neon_projects()
