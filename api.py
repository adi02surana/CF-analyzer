import requests
import sys

BASE_URL = "https://codeforces.com/api"

def fetch_data(endpoint: str, params: dict) -> dict:
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("status") != "OK":
            raise ValueError(data.get("comment", "API Error"))
        return data.get("result")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            try:
                print(f"❌ Error: {e.response.json().get('comment')}")
            except:
                print(f"❌ HTTP Error: {e}")
        else:
            print(f"❌ HTTP Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Request Error: {e}")
        sys.exit(1)

def get_user_info(handle: str):
    return fetch_data("user.info", {"handles": handle})

def get_user_rating(handle: str):
    return fetch_data("user.rating", {"handle": handle})

def get_user_status(handle: str):
    return fetch_data("user.status", {"handle": handle})
