import requests
import time
import os

BANNER = """
=======================================
||           KenchiKane              ||
||      Rubi Auto Mining Script      ||
=======================================
"""

API_BASE = "https://rubi.click/api"

def load_accounts(filename="accounts.txt"):
    accounts = []
    try:
        with open(filename, "r") as file:
            for line in file:
                if ":" in line:
                    user, pwd = line.strip().split(":", 1)
                    accounts.append((user.strip(), pwd.strip()))
    except FileNotFoundError:
        print(f"'{filename}' file not found. Please create it with username:password per line.")
        exit(1)
    return accounts

def login(username, password):
    url = f"{API_BASE}/login"
    payload = {
        "username": username,
        "password": password
    }
    try:
        response = requests.post(url, json=payload)
        if response.ok and 'token' in response.json():
            return response.json()['token']
    except Exception as e:
        print(f"    [ERROR] Login request failed: {e}")
    return None

def exploit(token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        time_remain = requests.get(f"{API_BASE}/exploit/time-remain", headers=headers).json()

        if time_remain.get("data", {}).get("can_exploit"):
            res = requests.post(f"{API_BASE}/exploit", headers=headers)
            return res.json()
        else:
            return {"status": False, "message": "Mining not available yet"}
    except Exception as e:
        return {"status": False, "message": f"Request failed: {e}"}

def get_profile(token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        res = requests.get(f"{API_BASE}/my-profile", headers=headers)
        if res.ok:
            return res.json().get("data", {})
    except:
        pass
    return {}

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(BANNER)
    
    accounts = load_accounts("accounts.txt")
    for i, (username, password) in enumerate(accounts, start=1):
        print(f"\n[{i}] Processing account: {username}")
        token = login(username, password)
        
        if not token:
            print(f" -> Login failed for {username}")
            continue
        
        result = exploit(token)
        if result.get("status"):
            profile = get_profile(token)
            print(f" -> SUCCESS: {username}")
            print(f"    Name: {profile.get('name', 'N/A')}")
            print(f"    Balance: {profile.get('balance', 'N/A')}")
            print(f"    Message: {result.get('message')}")
        else:
            print(f" -> FAILED: {username}")
            print(f"    Reason: {result.get('message')}")

if __name__ == "__main__":
    main()
