import json

class PlaylistProcessor:

    def __init__(self):
        self.playlists_file = '../data/craw/playlists_channel_data/all_playlist.json'
        self.videos_file = '../data/craw/videos_data/{}'


    def get_data(self, input):
        # Lưu dữ liệu JSON vào thư mục data/raw với tên tệp là filename
        with open(self.videos_file.format(input), "r", encoding="utf-8") as file:
            data = json.load(file)
            return data

    def process_videos_info(self, input):
        video_ids = []
        # Xử lý dữ liệu từ raw/video_data.json để lấy thông tin chi tiết về các video và trả về dữ liệu đã xử lý.
        with open(self.videos_file.format(input), "r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                video_ids.append(item["snippet"]["resourceId"]["videoId"])
        return video_ids

    def process_playlist_info(self):
        # Xử lý dữ liệu từ raw/video_data.json để lấy thông tin chi tiết về các video và trả về dữ liệu đã xử lý.
        id_nala = ""
        id_rapvie = ""
        with open(self.playlists_file,  "r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                if "[ LIVE STAGE ] | Rap Việt Mùa 3 (2023)" in item["snippet"]["title"]:
                    id_rapvie = item["id"]
                if "NGƯỜI ẤY LÀ AI? Mùa 5 (2023) | 20:00 Thứ 6 hàng tuần" in item["snippet"]["title"]:
                    id_nala = item["id"]
                if id_nala != "" and id_rapvie != "":
                    return id_rapvie, id_nala
        return id_rapvie, id_nala



    def process_analytics(self, analytics_data):
        # Xử lý dữ liệu từ raw/analytics_data.json để lấy thông tin thống kê và trả về dữ liệu đã xử lý.
        processed_analytics = [...]
        return processed_analytics
