"""
This file can be used to initially populate the measurements database
"""


import requests
import time

url = "http://127.0.0.1:5000/api_v1/1234/upload_data"

rooms = [
    {"room": "dummy_1", "temperature": 13.4, "humidity": 63},
    {"room": "dummy_2", "temperature": 22.8, "humidity": 58},
    {"room": "dummy_3", "temperature": 31.3, "humidity": 47},
]

for i in range(4):
    time.sleep(1)
    for room in rooms:        
        room["temperature"] += 1
        room["humidity"] -= 1
        x = requests.post(url, json=room)
print(x.status_code)
