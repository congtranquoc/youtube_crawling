import json
import os

def get_id_playlists(uri_path):
    target_titles = {
        "Rap Việt": "RAP VIỆT Mùa 3 (2023) | 20:00 Thứ 7 hàng tuần",
        "Người Ấy Là Ai?": "NGƯỜI ẤY LÀ AI? Mùa 5 (2023) | 20:00 Thứ 6 hàng tuần"
    }

    id_mapping = {title: "" for title in target_titles.keys()}
    with open(os.path.join(uri_path), "r", encoding="utf-8") as file:
        data = json.load(file)
        for item in data:
            title = item["snippet"]["title"]
            if title in target_titles.values():
                for key, value in target_titles.items():
                    if value == title and not id_mapping[key]:
                        id_mapping[key] = item["id"]
                        break

            if all(id_mapping.values()):
                break

    return tuple(id_mapping.values())
