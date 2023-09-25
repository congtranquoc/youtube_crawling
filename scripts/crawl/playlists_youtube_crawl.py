import time
from modules.general_classes import *
from scripts.crawl.YoutubeAPI import YouTubeAPI


class PlaylistsCrawler(YouTubeAPI):
    def __init__(self):
        super().__init__()

    def get_all_playlists(self, next_page_token=None):
        try:
            response = self.youtube.playlists().list(
                part='snippet',
                channelId=self.channel_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()
            playlists = response.get('items', [])
            playlists_info = []

            for item in playlists:
                playlist_info = {
                    "playlist_id": item['id'],
                    "title": item["snippet"]["title"]
                }
                playlists_info.append(playlist_info)

            next_page_token = response.get('nextPageToken')
            return playlists_info, next_page_token
        except Exception as e:
            print('PlaylistsCrawler has an error occurred:', str(e))
            return None, None

    def crawl_data(self):
        continue_key = read_json('../../data/playlists_state.json')

        if continue_key is None:
            page_token = ''
        else:
            page_token = continue_key.get('page_token')

        all_playlists = []

        while True:
            playlists, next_page_token = self.get_all_playlists(page_token)
            if playlists is None:
                save_json({'page_token': page_token}, '../../data/playlists_state.json')
                continue
            all_playlists.extend(playlists)
            page_token = next_page_token

            if not next_page_token:
                break
        return all_playlists
