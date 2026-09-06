import time
import json
import os
import requests
import yt_dlp

BOT_TOKEN = "8920116988:AAEgUVtaL8b9a48XsIp-oxxfDU_Kh0yv8C4" 
CHAT_ID = "7647963196"  
TARGET_USER = "nuryoruur1" 

CHECK_INTERVAL = 300  
DATA_FILE = "last_seen_ids.json"

def send_telegram_media(file_path, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    with open(file_path, "rb") as video:
        requests.post(url, data={"chat_id": CHAT_ID, "caption": caption}, files={"video": video})

def get_latest_posts():
    ydl_opts = {
        'cookiefile': 'cookies.txt',  
        'extract_flat': True,
        'playlistend': 5,             
        'quiet': True
    }
    url = f"https://www.tiktok.com/@{TARGET_USER}"
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info.get('entries', [])
        except Exception as e:
            print(f"Profil çekilirken hata: {e}")
            return []

def download_and_notify():
    seen_ids = set()
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            seen_ids = set(json.load(f))

    entries = get_latest_posts()
    
    for entry in reversed(entries):
        if not entry:
            continue
            
        post_id = entry['id']
        post_url = entry.get('url') or f"https://www.tiktok.com/@{TARGET_USER}/video/{post_id}"

        if post_id not in seen_ids:
            print(f"Yeni içerik bulundu! İndiriliyor: {post_url}")
            
            download_opts = {
                'outtmpl': f'downloads/{post_id}.%(ext)s',
                'cookiefile': 'cookies.txt',
                'quiet': True
            }
            
            try:
                with yt_dlp.YoutubeDL(download_opts) as ydl:
                    ydl.download([post_url])
                
                for filename in os.listdir('downloads'):
                    if filename.startswith(post_id):
                        file_path = os.path.join('downloads', filename)
                        print("Telegram'a gönderiliyor...")
                        send_telegram_media(file_path, f"Yeni TikTok paylaşımı!\n{post_url}")
                        os.remove(file_path) 
                        print("Başarıyla gönderildi ve dosya temizlendi.")
                        
            except Exception as e:
                print(f"İndirme sırasında hata: {e}")
            
            seen_ids.add(post_id)

    with open(DATA_FILE, "w") as f:
        json.dump(list(seen_ids), f)

os.makedirs('downloads', exist_ok=True)
print(f"@{TARGET_USER} hesabı izlenmeye başlandı...")

while True:
    download_and_notify()
    time.sleep(CHECK_INTERVAL)