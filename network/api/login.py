import requests
from network import url,auth_data
from . import login_url

def login():
    response = requests.post(login_url ,json=auth_data)
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"[+] JWT Token: {token}")
        return token
    else:
        print(f"[-] Failed to login: {response.json()}")
        exit()
