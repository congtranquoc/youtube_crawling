import os
import json
import time

from googleapiclient.discovery import build
from dotenv import load_dotenv

class VideosYoutubeCrawler:
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv('youtube_api_key')
        self.CHANNEL_ID = os.getenv('CHANNEL_ID')

        self.state_file = '../data/craw/videos_data/state.json'
        self.output_file = '../data/craw/videos_data/{}'

    def get_videos_from_playlist(self, playlist_id, next_page_token=None):
        youtube = build('youtube', 'v3', developerKey=self.API_KEY)
        try:
            playlist_items = youtube.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            _videos = playlist_items['items']
            _next_page_token = playlist_items.get('nextPageToken')
            time.sleep(1)
            return _videos, _next_page_token
        except Exception as e:
            print("An Error occurs: ", str(e))
            return None, None

    def save_state_to_json(self, page_token):
        with open(self.state_file, 'w') as f:
            json.dump({'page_token': page_token}, f)

    def load_state_from_json(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                state_data = json.load(f)
            return state_data.get('page_token', [])
        return None

    def run(self, playlist_id, output_path):
        page_token = self.load_state_from_json()

        if page_token is None:
            page_token = ''

        all_videos = []

        while True:
            videos, next_page_token = self.get_videos_from_playlist(playlist_id, page_token)
            if videos is None:
                self.save_state_to_json(page_token)
                continue
            all_videos.extend(videos)
            page_token = next_page_token

            if not next_page_token:
                break

        with open(self.output_file.format(output_path), 'w', encoding='utf-8') as file:
            json.dump(all_videos, file, ensure_ascii=False)

    def get_data(self):
        # Lưu dữ liệu JSON vào thư mục data/raw với tên tệp là filename
        with open(self.output_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
