import re
from airflow_project.modules.general_classes import *
from airflow_project.scripts.crawl.YoutubeAPI import YouTubeAPI


class VideosYoutubeCrawler(YouTubeAPI):
    def __init__(self, playlist_ids, **kwargs):
        super().__init__()
        self.playlist_ids = playlist_ids
        self.collection = kwargs.get('collection', '')

    def get_videos_from_playlist(self, next_page_token=None):
        try:
            playlist_items = self.youtube.playlistItems().list(
                part='snippet',
                playlistId=self.playlist_ids,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            _videos = self.data_mining(playlist_items['items'], kind=playlist_items['kind'])
            _next_page_token = playlist_items.get('nextPageToken')

            return _videos, _next_page_token
        except Exception as e:
            print("VideosYoutubeCrawler has an error occurs: ", str(e))
            return None, None

    def crawl_data(self):
        continue_key = read_json('../../airflow_project/data/videos_state.json')

        if continue_key is None:
            page_token = ''
        else:
            page_token = continue_key.get('page_token')
        all_videos = []

        while True:
            videos, next_page_token = self.get_videos_from_playlist(page_token)
            if videos is None:
                save_json({'page_token': page_token}, '../../airflow_project/data/videos_state.json')
                continue

            all_videos.extend(videos)
            page_token = next_page_token

            if not next_page_token:
                break
        return all_videos

    def data_mining(self, response_data, **kwargs):
        kind = kwargs.get('kind', '')
        if kind == 'youtube#playlistItemListResponse':
            _videos = []
            pattern = r"^Rap Việt Mùa 3 - Tập \d+" if self.collection == "videoids_rapvie" else r"^Người Ấy Là Ai\? 2023 [^\n]+"

            for item in response_data:
                title = item["snippet"]["title"]

                matches = re.findall(pattern, title)
                if matches:
                    title = title.split(" - ", 1)[-1].lstrip("0123456789.- ")
                    _videos.append({
                        "id": item["id"],
                        "video_id": item["snippet"]["resourceId"]["videoId"],
                        "video_title": title,
                        "playlist_program": self.collection
                    })
            return _videos
        else:
            raise ValueError("This is not correct response.")
