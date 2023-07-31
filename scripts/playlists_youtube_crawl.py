import os
import json
import time

from googleapiclient.discovery import build
from dotenv import load_dotenv

class PlaylistsCrawler:
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv('youtube_api_key')
        self.CHANNEL_ID = os.getenv('CHANNEL_ID')


        self.state_file = '../data/craw/playlists_channel_data/state.json'
        self.output_file = '../data/craw/playlists_channel_data/all_playlist.json'

    def get_all_playlists(self, next_page_token=None):
        youtube = build('youtube', 'v3', developerKey=self.API_KEY)
        try:
            response = youtube.playlists().list(
                part='snippet',
                channelId=self.CHANNEL_ID,
                maxResults=50,
                pageToken=next_page_token
            ).execute()
            _playlists = response.get('items', [])
            _next_page_token = response.get('nextPageToken')
            time.sleep(1)
            return _playlists, _next_page_token
        except Exception as e:
            print('An error occurred:', str(e))
            return None, None

    def save_state_to_json(self,page_token):
        with open(self.state_file, 'w') as f:
            json.dump({'page_token':page_token},f)

    def load_state_from_json(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                state_data = json.load(f)
            return state_data.get('page_token', [])
        return None

    def run(self):
        page_token = self.load_state_from_json()

        if page_token is None:
            page_token = ''

        all_playlists = []

        while True:
            playlists, next_page_token = self.get_all_playlists(page_token)
            if playlists is None:
                self.save_state_to_json(page_token)
                continue
            all_playlists.extend(playlists)
            page_token = next_page_token

            if not next_page_token:
                break

        with open(self.output_file, 'w', encoding='utf-8') as file:
            json.dump(all_playlists, file, ensure_ascii=False)

    def get_data(self):
        # Lưu dữ liệu JSON vào thư mục data/raw với tên tệp là filename
        with open(self.output_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data

# if __name__ == "__main__":
#     crawler = PlaylistsCrawler()
#     crawler.main()
