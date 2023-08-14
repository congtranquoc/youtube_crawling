import time
from googleapiclient.discovery import build
from dotenv import load_dotenv
from modules.general_classes import *

class VideosYoutubeCrawler:
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv('youtube_api_key')
        self.CHANNEL_ID = os.getenv('CHANNEL_ID')

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

    def run(self, playlist_id, collection):
        continue_key = read_json('../data/craw/playlists_channel_data/state.json')

        if continue_key is None:
            page_token = ''
        else:
            page_token = continue_key.get('page_token')
        all_videos = []

        while True:
            videos, next_page_token = self.get_videos_from_playlist(playlist_id, page_token)
            if videos is None:
                save_json({'page_token': page_token}, '../data/craw/playlists_channel_data/state.json')
                continue
            for item in videos:
                item['playlist_program'] = collection

            all_videos.extend(videos)
            page_token = next_page_token

            if not next_page_token:
                break
        save_merge_json(all_videos, f'../data/craw/videos_data/all_video.json')

