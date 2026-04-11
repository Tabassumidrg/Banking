import os
import json
import base64
import urllib.request
import urllib.error
import subprocess

# Configuration
PROJECT_NAME = "nidhibank"
GIT_REMOTE = "origin"

# Tokens (Loaded from tokens file in root)
def get_tokens():
    tokens = {}
    tokens_path = os.path.join(os.path.dirname(__file__), "tokens")
    if os.path.exists(tokens_path):
        with open(tokens_path, "r") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if "Vercel" in line and (i + 2) < len(lines):
                    tokens["VERCEL"] = lines[i+2].split("Value")[-1].strip()
                if "Render" in line and (i + 2) < len(lines):
                    tokens["RENDER"] = lines[i+2].split("Value")[-1].strip()
    return tokens

TOKENS = get_tokens()
VERCEL_TOKEN = TOKENS.get("VERCEL")
RENDER_TOKEN = TOKENS.get("RENDER")
RENDER_SERVICE_ID = "srv-d7142kogjchc73983d80"
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")

def get_current_branch():
    try:
        result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception:
        return "main"

def run_git_sync():
    print("--- Git Sync ---")
    branch = get_current_branch()
    print(f"Current branch: {branch}")
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Manual redeploy via automation"], capture_output=True) # OK if no changes
        subprocess.run(["git", "push", GIT_REMOTE, branch], check=True)
        print(f"[SUCCESS] Git push successful to {branch}!")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Git error: {e}")
        return False
    return True

def get_files(directory):
    files_to_deploy = []
    max_size = 5 * 1024 * 1024
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

def deploy_vercel():
    print("--- Vercel Deployment ---")
    if not VERCEL_TOKEN:
        print("[ERROR] Missing Vercel Token")
        return
        
    url = "https://api.vercel.com/v13/deployments"
    headers = {"Authorization": f"Bearer {VERCEL_TOKEN}", "Content-Type": "application/json"}
    files_data = get_files(FRONTEND_DIR)
    
    payload = {
        "name": PROJECT_NAME,
        "files": files_data,
        "projectSettings": {"framework": "nextjs"},
        "target": "production"
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"[SUCCESS] Vercel Success: https://{data.get('url')}")
    except Exception as e:
        print(f"[ERROR] Vercel Error: {e}")

def deploy_render():
    print("--- Render Deployment ---")
    if not RENDER_TOKEN:
        print("[ERROR] Missing Render Token")
        return
        
    url = f"https://api.render.com/v1/services/{RENDER_SERVICE_ID}/deploys"
    headers = {
        "Authorization": f"Bearer {RENDER_TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(url, data=b"{}", headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"[SUCCESS] Render Success: Build {data.get('id')} started.")
    except Exception as e:
        print(f"[ERROR] Render Error: {e}")

def main():
    if run_git_sync():
        print("[SUCCESS] Vercel deployment automatically triggered via GitHub push!")
        deploy_render()
        print("\n[INFO] All deployments initiated!")

if __name__ == "__main__":
    main()
