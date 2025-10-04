import requests


response = requests.get("http://127.0.0.1:8888")
print(f"Status Code: {response.status_code}")
print(f"Content: {response.json()}")
