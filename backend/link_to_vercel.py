import urllib.request
import urllib.error
import json
import os
import sys

# Path to tokens file
TOKENS_PATH = r"d:\saif\Banking\tokens"

def get_vercel_token():
    if os.path.exists(TOKENS_PATH):
        with open(TOKENS_PATH, "r") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if "Vercel" in line and (i + 2) < len(lines):
                    return lines[i+2].split("Value")[-1].strip()
    return None

def set_vercel_env_var(project_id, key, value, token):
    url = f"https://api.vercel.com/v9/projects/{project_id}/env"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # First check if it exists to decide whether to POST (new) or PATCH (update)
    # Actually, Vercel API allows adding, and if it exists it might error or we might need to delete first.
    # For simplicity, we'll try to add it. If it exists, we might need to handle the error.
    
    payload = {
        "key": key,
        "value": value,
        "type": "plain",
        "target": ["production", "preview", "development"]
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"Successfully set {key} in Vercel!")
            return True
    except urllib.error.HTTPError as e:
        if e.code == 400: # Often means it already exists
             print(f"Variable {key} might already exist or there was a bad request. Error: {e.read().decode()}")
        else:
            print(f"HTTP Error {e.code}: {e.read().decode()}")
    except Exception as e:
        print(f"Error: {str(e)}")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python link_to_vercel.py <RENDER_URL>")
        sys.exit(1)
        
    render_url = sys.argv[1]
    token = get_vercel_token()
    
    if not token:
        print("Vercel token not found in tokens file.")
        sys.exit(1)
        
    # Project name or ID can be used in the URL
    project_name = "nidhibank"
    db_url = os.environ.get("DATABASE_URL", "")
    
    print(f"Linking {render_url} to Vercel project {project_name}...")
    set_vercel_env_var(project_name, "NEXT_PUBLIC_API_URL", render_url, token)
    if db_url:
        set_vercel_env_var(project_name, "DATABASE_URL", db_url, token)
