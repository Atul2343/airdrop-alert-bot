import feedparser
import json
import os
import requests
import re

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

RSS_URL = "https://airdrops.io/feed/"
LAST_FILE = "last_airdrop.json"

def clean(text):
    return re.sub('<[^<]+?>', '', text).strip()

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
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    })

feed = feedparser.parse(RSS_URL)
last_id = load_last()

for entry in feed.entries[:5]:
    post_id = entry.id
    if post_id == last_id:
        break

    title = entry.title
    link = entry.link
    summary = clean(entry.summary)

    message = f"""
🚀 <b>New Crypto Airdrop Alert</b>

🪙 <b>Project:</b> {title}

🎁 <b>Reward:</b> Free Tokens (Depends on tasks)
👥 <b>Eligibility:</b> New & Existing Users

📋 <b>How to Participate:</b>
1️⃣ Visit official link  
2️⃣ Complete simple social tasks  
3️⃣ Submit wallet address  

⏰ <b>Status:</b> Ongoing  
🔗 <b>Official Link:</b> <a href="{link}">Click Here</a>

📝 <b>About:</b>
{summary[:500]}...

⚠️ <i>Note: Never share private keys. DYOR.</i>
"""
    send(message)
    save_last(post_id)
    break
