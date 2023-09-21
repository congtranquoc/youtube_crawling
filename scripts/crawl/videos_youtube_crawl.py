import time
import re
from modules.general_classes import *
from scripts.crawl.YoutubeAPI import YouTubeAPI


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

            _videos = playlist_items['items']
            _next_page_token = playlist_items.get('nextPageToken')
            time.sleep(1)
            return _videos, _next_page_token
        except Exception as e:
            print("VideosYoutubeCrawler has an error occurs: ", str(e))
            return None, None

    def crawl_data(self):
        continue_key = read_json('../data/craw/videos_data/state.json')

        if continue_key is None:
            page_token = ''
        else:
            page_token = continue_key.get('page_token')
        all_videos = []

        while True:
            videos, next_page_token = self.get_videos_from_playlist(page_token)
            if videos is None:
                save_json({'page_token': page_token}, '../data/craw/videos_data/state.json')
                continue

            filtered = self.filterEpisode(videos)

            all_videos.extend(filtered)
            page_token = next_page_token

            if not next_page_token:
                break
        save_merge_json(all_videos, f'../../data/craw/videos_data/all_video.json')

    def filterEpisode(self, videos):
        filteredVideos = []

        # Xác định mẫu regex dựa trên collection
        if self.collection == "videoids_rapvie":
            pattern = r"^Rap Việt Mùa 3 - Tập \d+"
        else:
            pattern = r"^Người Ấy Là Ai\? 2023 [^\n]+"
        for item in videos:
            item['playlist_program'] = self.collection
            title = item["snippet"]["title"]

            # Kiểm tra xem title có khớp với mẫu không
            matches = re.findall(pattern, title)
            if matches:
                filteredVideos.append(item)

        return filteredVideos

