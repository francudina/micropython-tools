import json
import urequests


def get(url: str) -> {}:
    try:
        return urequests.get(url=url).json()
    except Exception as e:
        print(f'(e) failed to get response: {e}')
        return None


def post(url: str, data: {}) -> {}:
    try:
        return urequests.post(url=url, data=json.dumps(data)).json()
    except Exception as e:
        print(f'(e) failed to get response: {e}')
        return None
