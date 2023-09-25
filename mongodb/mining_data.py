import json
import os
from modules.general_classes import *
def remove_property(item, property_name):
    if property_name in item:
        del item[property_name]
    return item

def mining_data(input_file, data_name):
    # Kiểm tra xem file input_file có tồn tại hay không.
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"File '{input_file}' không tồn tại.")

    # Đọc dữ liệu json từ file input_file.
    data = read_json(input_file)

    output_data = []
    if (data_name == 'all_video'):
        for item in data:
            title = item["snippet"]["title"]
            if title.startswith("Rap Việt Mùa 3 - "):
                title = title[len("Rap Việt Mùa 3 - "):]
            elif title.startswith("Người Ấy Là Ai? 2023 - "):
                title = title[len("Người Ấy Là Ai? 2023 - "):]
            elif title.startswith("Người Ấy Là Ai? 2023 "):
                title = title[len("Người Ấy Là Ai? 2023 "):]

            output_data.append({
                "id": item["id"],
                "video_id": item["snippet"]["resourceId"]["videoId"],
                "video_title": title,
                "playlist_program": item["playlist_program"]
            })
    elif(data_name == 'video_statics'):
        for item in data:
            output_data.append({
                "video_id": item["id"],
                "view_count": item["statistics"]["viewCount"],
                "like_count": item["statistics"]["likeCount"],
                "comment_count": item["statistics"]["commentCount"],
                "playlist_program": item["playlist_program"]
            })
    elif(data_name == 'all_playlist'):
        for item in data:
            output_data.append({
                "playlist_id": item['id'],
                "title": item["snippet"]["title"]
            })
    elif(data_name == 'comment_videos'):
        for item in data:
            authorDisplayName = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
            topLevelComment = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
            video_id = item["snippet"]["videoId"]
            snippet = item["snippet"]
            # replies = item["replies"]["comments"]
            # if(replies):
            #     i = 0
            #     for reply in replies:
            #         comment_reply = item["replies"]["comments"][i]["snippet"]["textOriginal"]
            #         authorDisplayName_reply = item["replies"]["comments"][i]["snippet"]["authorDisplayName"]
            #         i += 1
            # else:
            #     pass

            output_data.append({
                "authorDisplayName": authorDisplayName,
                "topLevelComment": topLevelComment,
                "video_id": video_id,
                # "comment_reply": comment_reply,
                # "authorDisplayName_reply": authorDisplayName_reply
            })
    else: print('File không tồn tại')

    # Tạo file output_file.
    output_file = os.path.join(os.path.dirname(input_file), f"new_{os.path.basename(data_name)}.json")

    # Ghi dữ liệu ra file output_file.
    save_json(output_data, output_file)