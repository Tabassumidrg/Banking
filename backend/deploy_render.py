import urllib.request
import urllib.error
import json
import os
import sys

RENDER_API_KEY = os.environ.get("RENDER_API_KEY", "")

def get_owners():
    req = urllib.request.Request(
        "https://api.render.com/v1/owners",
        headers={"Authorization": f"Bearer {RENDER_API_KEY}", "Accept": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def create_service(owner_id):
    # This expects the code to be pushed to github. 
    # Usually you'd deploy using a github repo URL, but since we are doing this locally right now
    # We will simply instruct the user to push and create via dashboard if the repo isn't linked,
    # or create a boilerplate web service connecting to their GitHub.
    # Below is a stub to try an API-based service creation.
    # User doesn't have a linked repo known to this script. The implementation plan
    # mentions they'd need to push it anyway. 
    pass

if __name__ == "__main__":
    print("Please ensure your code is pushed to GitHub.")
    print("To automate deployment via API, the repo must be passed.")
    print("We recommend importing the project through Render Dashboard:")
    print("Build Command: pip install -r requirements.txt")
    print("Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT")
