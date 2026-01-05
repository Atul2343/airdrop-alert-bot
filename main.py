import os
import requests
import feedparser
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
LAST_FILE = "last_airdrops.json"

RSS_FEEDS = [
    "https://airdrops.io/feed/",
    "https://coinmarketcap.com/alexandria/rss/airdrops"
]

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "HTML"}
    r = requests.post(url, json=payload)
    print(r.json())

def load_last_posted():
    if os.path.exists(LAST_FILE):
        with open(LAST_FILE, "r") as f:
            return json.load(f)
    return {}

def save_last_posted(data):
    with open(LAST_FILE, "w") as f:
        json.dump(data, f)

last_posted = load_last_posted()
new_last_posted = last_posted.copy()

for feed_url in RSS_FEEDS:
    feed = feedparser.parse(feed_url)
    if not feed.entries:
        continue
    latest = feed.entries[0]

    airdrop_id = latest.get("id") or latest.get("link")

    if airdrop_id in last_posted:
        print(f"Already posted: {latest.title}")
        continue

    msg = (
        f"🚨 <b>NEW AIRDROP ALERT</b> 🚨\n\n"
        f"🔥 <b>{latest.title}</b>\n"
        f"🔗 Join here: {latest.link}\n\n"
        f"#Airdrop #Crypto #FreeTokens"
    )

    send_message(msg)
    new_last_posted[airdrop_id] = True

save_last_posted(new_last_posted)
