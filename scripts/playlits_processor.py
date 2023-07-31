import json

class PlaylistProcessor:

    def __init__(self):
        self.input_file = '../data/craw/playlists_channel_data/all_playlist.json'

    def process_channel_info(self, channel_data):
        # Xử lý dữ liệu từ raw/channel_data.json để lấy thông tin chi tiết về các kênh và trả về dữ liệu đã xử lý.
        processed_channel_info = [...]
        return processed_channel_info

    def process_playlist_info(self):
        # Xử lý dữ liệu từ raw/video_data.json để lấy thông tin chi tiết về các video và trả về dữ liệu đã xử lý.
        with open(self.input_file,  "r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                if "[ LIVE STAGE ] | Rap Việt Mùa 3 (2023)" in item["snippet"]["title"]:
                    return item["id"]


    def process_analytics(self, analytics_data):
        # Xử lý dữ liệu từ raw/analytics_data.json để lấy thông tin thống kê và trả về dữ liệu đã xử lý.
        processed_analytics = [...]
        return processed_analytics
