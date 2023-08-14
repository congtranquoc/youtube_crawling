import time

import pandas as pd
from googleapiclient.discovery import build
from dotenv import load_dotenv
from modules.general_classes import *

class PlaylistsCrawler:
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv('youtube_api_key')
        self.CHANNEL_ID = os.getenv('CHANNEL_ID')

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

    def run(self):
        continue_key = read_json('../data/craw/playlists_channel_data/state.json')

        if continue_key is None:
            page_token = ''
        else:
            page_token = continue_key.get('page_token')

        all_playlists = []

        while True:
            playlists, next_page_token = self.get_all_playlists(page_token)
            if playlists is None:
                save_json({'page_token':page_token}, '../data/craw/playlists_channel_data/state.json')
                continue
            all_playlists.extend(playlists)
            page_token = next_page_token

            if not next_page_token:
                break
        save_json(all_playlists, '../data/craw/playlists_channel_data/all_playlist.json')

# if __name__ == "__main__":
#     crawler = PlaylistsCrawler()
#     crawler.main()
