from flask import Flask
import os
import time
import schedule
from TikTokApi import TikTokApi
from instagrapi import Client
from threading import Thread

app = Flask(__name__)

INSTAGRAM_USERNAME = "ishowuz"
INSTAGRAM_PASSWORD = "76835710."
TIKTOK_USERNAME = "majes7ic"

DOWNLOAD_DIR = "./videos"
USED_IDS_FILE = "used_ids.txt"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/')
def home():
    return "Bot ishlayapti 👋"

def is_new_video(video_id):
    if not os.path.exists(USED_IDS_FILE):
        return True
    with open(USED_IDS_FILE, "r") as f:
        used_ids = f.read().splitlines()
    return video_id not in used_ids

def save_video_id(video_id):
    with open(USED_IDS_FILE, "a") as f:
        f.write(video_id + "\n")

def download_latest_video():
    print("⏬ TikTok tekshirilmoqda...")
    api = TikTokApi()
    user_videos = api.by_username(TIKTOK_USERNAME, count=1)
    video = user_videos[0]
    video_id = video.id

    if not is_new_video(video_id):
        print("⏩ Yangi video yo‘q.")
        return None

    video_data = api.video(id=video_id).bytes()
    filename = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")
    with open(filename, "wb") as f:
        f.write(video_data)

    save_video_id(video_id)
    print(f"✅ Yangi video yuklandi: {filename}")
    return filename

def upload_to_instagram(video_path):
    print("⬆️ Instagram’ga yuklanyapti...")
    cl = Client()
    cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
    cl.clip_upload(video_path, caption="Avtomatik TikTok repost 😊")
    print("✅ Instagramga joylandi!")

def full_process():
    try:
        video_path = download_latest_video()
        if video_path:
            upload_to_instagram(video_path)
            os.remove(video_path)
    except Exception as e:
        print(f"❌ Xatolik: {e}")

def run_schedule():
    schedule.every(10).minutes.do(full_process)
    while True:
        schedule.run_pending()
        time.sleep(1)

# 🔁 Realtime ishga tushurish
if __name__ == "__main__":
    Thread(target=run_schedule).start()
    app.run(host="0.0.0.0", port=10000)
