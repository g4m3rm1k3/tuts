import requests
response = requests.get("http://127.0.0.1:8080/api/files")
print(f"Status Code: {response.status_code}")
print(f"Content: {response.json()}")
