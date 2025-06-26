from flask import Flask
from TikTokApi import TikTokApi
from instagrapi import Client
import os
import requests
import schedule
import time

app = Flask(__name__)

# Instagram login
cl = Client()
cl.login("ishowuz", "76835710.")  # 🔐 o'zgartiring

# Foydalanuvchini TikTok'dan olish
TIKTOK_USERNAME = "majes7ic"  # 👈 o'zgartiring

# Oxirgi yuklangan video ID sini saqlash (dublikatlarni oldini olish)
LAST_VIDEO_ID_FILE = "last_video.txt"

def get_last_video_id():
    if not os.path.exists(LAST_VIDEO_ID_FILE):
        return None
    with open(LAST_VIDEO_ID_FILE, "r") as f:
        return f.read().strip()

def save_last_video_id(video_id):
    with open(LAST_VIDEO_ID_FILE, "w") as f:
        f.write(video_id)

def download_video(url, filename="latest_video.mp4"):
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return filename

def post_latest_video():
    print("Tekshirilyapti...")

    api = TikTokApi()
    videos = api.by_username(TIKTOK_USERNAME, count=1)
    if not videos:
        print("Video topilmadi.")
        return

    latest = videos[0]
    video_id = latest['id']
    video_url = latest['video']['downloadAddr']
    caption = latest['desc']

    last_id = get_last_video_id()
    if video_id == last_id:
        print("Yangi video yo‘q.")
        return

    print("Yangi video topildi, yuklanmoqda...")

    path = download_video(video_url)
    cl.clip_upload(path, caption=caption)
    print("Instagramga yuklandi!")

    save_last_video_id(video_id)

# Har 10 daqiqada tekshir
schedule.every(10).minutes.do(post_latest_video)

@app.route("/")
def home():
    return "TikTok → Instagram repost bot ishlamoqda!"

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    import threading
    t = threading.Thread(target=run_scheduler)
    t.start()
    app.run(host="0.0.0.0", port=10000)
