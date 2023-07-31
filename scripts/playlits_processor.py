import json

class PlaylistProcessor:

    def __init__(self):
        self.playlists_file = '../data/craw/playlists_channel_data/all_playlist.json'
        self.videos_file = '../data/craw/videos_data/videos.json'

    def process_videos_info(self):
        video_ids = []
        # Xử lý dữ liệu từ raw/video_data.json để lấy thông tin chi tiết về các video và trả về dữ liệu đã xử lý.
        with open(self.videos_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                video_ids.append(item["resourceId"]["videoId"])
        return video_ids

    def process_playlist_info(self):
        # Xử lý dữ liệu từ raw/video_data.json để lấy thông tin chi tiết về các video và trả về dữ liệu đã xử lý.
        with open(self.playlists_file,  "r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                if "[ LIVE STAGE ] | Rap Việt Mùa 3 (2023)" in item["snippet"]["title"]:
                    return item["id"]


    def process_analytics(self, analytics_data):
        # Xử lý dữ liệu từ raw/analytics_data.json để lấy thông tin thống kê và trả về dữ liệu đã xử lý.
        processed_analytics = [...]
        return processed_analytics
