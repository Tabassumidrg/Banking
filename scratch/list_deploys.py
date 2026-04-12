import os
import json
import urllib.request
import urllib.error

def get_vercel_token():
    tokens_path = r"c:\Users\govtitigadag\Desktop\Banking\tokens"
    if os.path.exists(tokens_path):
        with open(tokens_path, "r") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if "Vercel" in line and (i + 2) < len(lines):
                    return lines[i+2].split("Value")[-1].strip()
    return None

TOKEN = get_vercel_token()

def list_deploys():
    if not TOKEN:
        print("Error: Vercel token not found.")
        return
        
    url = "https://api.vercel.com/v6/deployments?limit=5"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for d in data.get('deployments', []):
                print(f"ID: {d['uid']} | Status: {d['state']} | Source: {d.get('source', 'unknown')} | URL: https://{d['url']}")
                if d['state'] == 'ERROR':
                    # Optional: fetch error logs for this specific ID if needed
                    pass
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_deploys()
