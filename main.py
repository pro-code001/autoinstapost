from instagrapi import Client
from TikTokApi import TikTokApi
import requests
import random
import os

# Instagram sessiyasini yuklab olish
cl = Client()
cl.load_settings("settings.json")
cl.login("ishowuz", "76835710.")  # faqat sessiyani faollashtiradi

# Hashtaglar ro'yxati
hashtags = [
    "#foryou", "#fyp", "#viral", "#tiktok", "#funny", "#reels", "#explore", 
    "#trend", "#xyzbca", "#relatable", "#meme", "#story", "#lol"
]

# TikTokdan video olish
with TikTokApi() as api:
    trending_videos = api.trending(count=1)
    video = trending_videos[0]
    video_url = video.video.download_addr
    title = video.desc or "Awesome video!"

    filename = "video.mp4"
    with open(filename, "wb") as f:
        f.write(requests.get(video_url).content)

# Caption tayyorlash
selected_tags = " ".join(random.sample(hashtags, 5))
caption = f"{title}\n\n{selected_tags}"

# Instagram Reels yuklash
cl.clip_upload(
    path=filename,
    caption=caption
)

# Foydalanilgach video faylni o'chirish (ixtiyoriy)
os.remove(filename)
