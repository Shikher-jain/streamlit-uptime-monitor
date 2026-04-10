import requests
import json
import time

with open("config/apps.json") as f:
    apps = json.load(f)["apps"]

for url in apps:
    print(f"Pinging {url}")
    
    for attempt in range(3):
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                print(f"Success: {url}")
                break
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(5)
