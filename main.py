import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    send_message("🚨 <b>FREE AIRDROP ALERT</b>\n\nNew crypto airdrop live 🔥\nJoin now & earn free tokens 💰")
