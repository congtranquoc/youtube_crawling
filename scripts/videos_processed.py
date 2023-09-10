import json
import os
import re

def get_video_ids(uri_path):
    processed_data = []
    # Xử lý dữ liệu từ raw/videos_data.json để lấy thông tin chi tiết về các video và trả về dữ liệu đã xử lý.
    with open(os.path.join(uri_path), "r", encoding="utf-8") as file:
        data = json.load(file)
        for item in data:
            processed_item = {
                "video_id": item["snippet"]["resourceId"]["videoId"],
                "playlist_program": item["playlist_program"]
            }
            processed_data.append(processed_item)
    return processed_data


def filterEpisode(uri_path):
    processed_data = []
    # Mẫu regex để tìm các chuỗi
    pattern = r"Rap Việt Mùa 3 - Tập \d+"


    # Xử lý dữ liệu từ raw/videos_data.json để lấy thông tin chi tiết về các video và trả về dữ liệu đã xử lý.
    with open(os.path.join(uri_path), "r", encoding="utf-8") as file:
        data = json.load(file)
        # Lấy title từ snippet

        for item in data:
            title = item["snippet"]["title"]
            # Kiểm tra xem title có khớp với mẫu không
            matches = re.findall(pattern, title)
            # Nếu có khớp, in ra
            if matches:
                processed_data.append(item)
    return processed_data

