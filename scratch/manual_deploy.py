import os
import json
import base64
import urllib.request
import urllib.error

PROJECT_NAME = "nidhibank"
FRONTEND_DIR = r"c:\Users\govtitigadag\Desktop\Banking\frontend"

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

def get_files(directory):
    files_to_deploy = []
    for root, dirs, files in os.walk(directory):
        if any(x in root for x in ["node_modules", ".next", ".git", ".vercel"]):
            continue
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, directory).replace("\\", "/")
            try:
                with open(full_path, "rb") as f:
                    content = f.read()
                    files_to_deploy.append({
                        "file": rel_path,
                        "data": base64.b64encode(content).decode('utf-8'),
                        "encoding": "base64"
                    })
            except Exception as e:
                print(f"Error reading {rel_path}: {e}")
    return files_to_deploy

def deploy():
    if not TOKEN:
        print("Error: Vercel token not found.")
        return
        
    url = "https://api.vercel.com/v13/deployments"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    print("Collecting files...")
    files_data = get_files(FRONTEND_DIR)
    
    payload = {
        "name": PROJECT_NAME,
        "files": files_data,
        "projectSettings": {
            "framework": "nextjs"
        },
        "target": "production"
    }
    
    print(f"Deploying {len(files_data)} files to Vercel...")
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("Deployment created successfully!")
            print(f"URL: https://{data.get('url')}")
    except Exception as e:
        if isinstance(e, urllib.error.HTTPError):
            print(f"HTTP Error: {e.code} {e.reason}")
            print(e.read().decode())
        else:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    deploy()
