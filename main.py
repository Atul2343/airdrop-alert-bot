import feedparser
import json
import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

RSS_URL = "https://airdrops.io/feed/"

LAST_FILE = "last_airdrop.json"

def load_last():
    if os.path.exists(LAST_FILE):
        with open(LAST_FILE, "r") as f:
            return json.load(f).get("id")
    return None

def save_last(post_id):
    with open(LAST_FILE, "w") as f:
        json.dump({"id": post_id}, f)

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHANNEL_ID,
        "text": msg,
        "parse_mode": "HTML"
    })

feed = feedparser.parse(RSS_URL)
last_id = load_last()

for entry in feed.entries[:3]:  # max 3 per run
    post_id = entry.id
    if post_id == last_id:
        break

    title = entry.title
    link = entry.link
    summary = entry.summary[:300]

    message = f"""
🚀 <b>New Crypto Airdrop</b>

🪙 <b>{title}</b>

📄 {summary}...

🔗 <a href="{link}">Claim Details</a>

⚠️ DYOR | Free Airdrop
"""
    send(message)
    save_last(post_id)
    break
