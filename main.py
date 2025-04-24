import feedparser
import requests
import os

# === Config ===
TELEGRAM_BOT_TOKEN = '7945964210:AAFzUVq09hrsm2BppBTF0U9t70E0AGSxZNQ'
TELEGRAM_CHAT_ID = "@noti_youtube_videos" 
DATA_FOLDER = 'videos_data'  

channels = {
    "UC8GfEhFkCW0jqIq8Ci04QPg": "Kênh A",
    "UC-lHJZR3Gqxm24_Vd_AJ5Yw": "PewDiePie",
    "UCq-Fj5jknLsUf-MWSy4_brA": "Marques Brownlee"
}

def get_latest_video(channel_id):
    url = f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'
    feed = feedparser.parse(url)
    if not feed.entries:
        return None
    entry = feed.entries[0]
    return {
        'id': entry.yt_videoid,
        'title': entry.title,
        'url': entry.link
    }

def get_last_video_id(channel_id):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    path = os.path.join(DATA_FOLDER, f'{channel_id}.txt')
    if not os.path.exists(path):
        return None
    with open(path, 'r') as f:
        return f.read().strip()

def save_last_video_id(channel_id, video_id):
    path = os.path.join(DATA_FOLDER, f'{channel_id}.txt')
    with open(path, 'w') as f:
        f.write(video_id)

def send_to_telegram(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    requests.post(url, data=data)

if __name__ == '__main__':
    for channel_id, name in channels.items():
        video = get_latest_video(channel_id)
        if not video:
            continue
        last_id = get_last_video_id(channel_id)
        if video['id'] != last_id:
            message = f"📢 Video mới từ *{name}*:\n📹 {video['title']}\n🔗 {video['url']}"
            send_to_telegram(message)
            save_last_video_id(channel_id, video['id'])
        else:
            print(f"[{name}] Không có video mới.")
