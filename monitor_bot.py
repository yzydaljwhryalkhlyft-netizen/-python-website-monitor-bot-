import requests
import time
import hashlib
from bs4 import BeautifulSoup

TARGET_URL = "https://example.com"  
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

def get_page_hash(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for script in soup(["script", "style"]):
                script.extract()
            page_text = soup.get_text().encode('utf-8')
            return hashlib.md5(page_text).hexdigest()
    except Exception as e:
        print(f"Error: {e}")
    return None

def send_telegram_message(message):
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("Notification sent.")
    except Exception as e:
        print(f"Error: {e}")

def monitor():
    print("Starting monitoring...")
    last_hash = get_page_hash(TARGET_URL)
    
    if not last_hash:
        print("Initial check failed.")
        return

    while True:
        try:
            time.sleep(60)
            current_hash = get_page_hash(TARGET_URL)
            
            if current_hash and current_hash != last_hash:
                msg = f"Change detected at: {TARGET_URL}"
                send_telegram_message(msg)
                last_hash = current_hash
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    monitor()
  
