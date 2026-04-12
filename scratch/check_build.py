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

def check_build():
    if not TOKEN:
        print("Error: Vercel token not found.")
        return
        
    url = "https://api.vercel.com/v6/deployments?limit=1"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            last_deploy = data['deployments'][0]
            deploy_id = last_deploy['uid']
            print(f"Deployment ID: {deploy_id}")
            print(f"Status: {last_deploy['state']}")
            
            # Get build logs using the events endpoint
            events_url = f"https://api.vercel.com/v2/deployments/{deploy_id}/events?direction=backward&limit=100"
            req_events = urllib.request.Request(events_url, headers=headers)
            with urllib.request.urlopen(req_events) as resp_events:
                events = json.loads(resp_events.read().decode('utf-8'))
                for event in reversed(events):
                    if event.get('type') in ['stderr', 'stdout']:
                        print(f"[{event.get('type')}] {event.get('text')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_build()
