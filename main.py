import requests
from bs4 import BeautifulSoup
import os
from telegram import Bot

# -------------------- Secrets --------------------
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

if not BOT_TOKEN or not CHANNEL_ID:
    raise Exception("❌ BOT_TOKEN or CHANNEL_ID missing!")

bot = Bot(token=BOT_TOKEN)
POSTED_FILE = "posted_airdrops.txt"

# -------------------- Duplicate Prevention --------------------
def get_posted():
    if os.path.exists(POSTED_FILE):
        with open(POSTED_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_posted(airdrop_id):
    with open(POSTED_FILE, "a") as f:
        f.write(f"{airdrop_id}\n")

# -------------------- Telegram Sender --------------------
def send_telegram(title, link):
    try:
        message = f"🎁 New Airdrop Alert:\n{title}\nLink: {link}"
        bot.send_message(chat_id=CHANNEL_ID, text=message)
        print("Message sent:", title)
    except Exception as e:
        print("Error sending Telegram:", e)

# -------------------- Scrape Functions --------------------
def scrape_airdrops_io():
    airdrops = []
    try:
        res = requests.get("https://airdrops.io/", timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        cards = soup.find_all("div", class_="airdrop-card")
        for c in cards:
            title_tag = c.find("h3")
            link_tag = c.find("a", href=True)
            if title_tag and link_tag:
                airdrops.append({
                    "title": title_tag.text.strip(),
                    "link": link_tag['href'],
                    "id": title_tag.text.strip()
                })
    except Exception as e:
        print("airdrops.io error:", e)
    return airdrops

def scrape_coinmarketcap():
    airdrops = []
    try:
        res = requests.get("https://coinmarketcap.com/airdrops/", timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.find_all("div", class_="sc-16r8icm-0")
        for it in items:
            title_tag = it.find("h3")
            link_tag = it.find("a", href=True)
            if title_tag and link_tag:
                airdrops.append({
                    "title": title_tag.text.strip(),
                    "link": "https://coinmarketcap.com" + link_tag['href'],
                    "id": title_tag.text.strip()
                })
    except Exception as e:
        print("coinmarketcap error:", e)
    return airdrops

def scrape_cryptodaily():
    airdrops = []
    try:
        res = requests.get("https://cryptodaily.co.uk/airdrops", timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.find_all("div", class_="entry-title")
        for it in items:
            a_tag = it.find("a", href=True)
            if a_tag:
                title = a_tag.text.strip()
                airdrops.append({"title": title, "link": a_tag['href'], "id": title})
    except Exception as e:
        print("cryptodaily error:", e)
    return airdrops

def scrape_coinsniper():
    airdrops = []
    try:
        res = requests.get("https://www.coinsniper.net/airdrops", timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        rows = soup.find_all("div", class_="coin-name")
        for r in rows:
            a_tag = r.find("a", href=True)
            if a_tag:
                title = a_tag.text.strip()
                airdrops.append({"title": title, "link": "https://www.coinsniper.net" + a_tag['href'], "id": title})
    except Exception as e:
        print("coinsniper error:", e)
    return airdrops

def scrape_coinfunda():
    airdrops = []
    try:
        res = requests.get("https://www.coinfunda.com/airdrops/", timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.find_all("h3")
        for it in items:
            a_tag = it.find("a", href=True)
            if a_tag:
                title = a_tag.text.strip()
                airdrops.append({"title": title, "link": a_tag['href'], "id": title})
    except Exception as e:
        print("coinfunda error:", e)
    return airdrops

def scrape_airdrops_guru():
    airdrops = []
    try:
        res = requests.get("https://airdrops.guru/", timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        cards = soup.find_all("div", class_="airdrops-list-item")
        for c in cards:
            a_tag = c.find("a", href=True)
            title = a_tag.text.strip() if a_tag else "Unknown"
            if a_tag:
                airdrops.append({"title": title, "link": a_tag['href'], "id": title})
    except Exception as e:
        print("airdrops.guru error:", e)
    return airdrops

def scrape_coindoo():
    airdrops = []
    try:
        res = requests.get("https://www.coindoo.com/airdrops/", timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.find_all("h3")
        for it in items:
            a_tag = it.find("a", href=True)
            if a_tag:
                airdrops.append({"title": a_tag.text.strip(), "link": a_tag['href'], "id": a_tag.text.strip()})
    except Exception as e:
        print("coindoo error:", e)
    return airdrops

def scrape_airdropsmob():
    airdrops = []
    try:
        res = requests.get("https://airdropsmob.com/", timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.find_all("h3")
        for it in items:
            a_tag = it.find("a", href=True)
            if a_tag:
                airdrops.append({"title": a_tag.text.strip(), "link": a_tag['href'], "id": a_tag.text.strip()})
    except Exception as e:
        print("airdropsmob error:", e)
    return airdrops

def scrape_coincodex():
    airdrops = []
    try:
        res = requests.get("https://coincodex.com/airdrop/", timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.find_all("h3")
        for it in items:
            a_tag = it.find("a", href=True)
            if a_tag:
                airdrops.append({"title": a_tag.text.strip(), "link": a_tag['href'], "id": a_tag.text.strip()})
    except Exception as e:
        print("coincodex error:", e)
    return airdrops

def scrape_cryptoslate():
    airdrops = []
    try:
        res = requests.get("https://cryptoslate.com/airdrops/", timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.find_all("h3")
        for it in items:
            a_tag = it.find("a", href=True)
            if a_tag:
                airdrops.append({"title": a_tag.text.strip(), "link": a_tag['href'], "id": a_tag.text.strip()})
    except Exception as e:
        print("cryptoslate error:", e)
    return airdrops

# -------------------- Main Logic --------------------
def main():
    posted = get_posted()
    all_airdrops = []

    # Call all 10 scrape functions
    all_airdrops += scrape_airdrops_io()
    all_airdrops += scrape_coinmarketcap()
    all_airdrops += scrape_cryptodaily()
    all_airdrops += scrape_coinsniper()
    all_airdrops += scrape_coinfunda()
    all_airdrops += scrape_airdrops_guru()
    all_airdrops += scrape_coindoo()
    all_airdrops += scrape_airdropsmob()
    all_airdrops += scrape_coincodex()
    all_airdrops += scrape_cryptoslate()

    # Send Telegram alerts
    for ad in all_airdrops:
        if ad['id'] in posted:
            continue
        send_telegram(ad['title'], ad['link'])
        save_posted(ad['id'])

if __name__ == "__main__":
    main()
