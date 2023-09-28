import pandas as pd
from pymongo import MongoClient

# Tham số kết nối MongoDB
mongo_uri = "mongodb://localhost:27017/"
database_name = "youtube_db"
collection_names = ["playlists", "statics", "videoids"]

# Kết nối tới MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]

# Lấy dữ liệu từ nhiều bộ sưu tập (collections) khác nhau và lưu vào dictionary
data_dict = {}
for collection_name in collection_names:
    collection = db[collection_name]
    cursor = collection.find({})
    data_dict[collection_name] = pd.DataFrame(list(cursor))

# Bạn có thể truy cập dữ liệu từng bộ sưu tập thông qua dictionary
statics_data = data_dict["statics"]
videoids_data = data_dict["videoids"]

videoids_data = videoids_data[['video_id', 'video_title', 'playlist_program']]
statics_data = statics_data[['video_id', 'view_count', 'like_count', 'comment_count']]
# Kết hợp hai bảng statics_data và videoids_data theo thuộc tính video_id
merged_data = statics_data.merge(videoids_data, on='video_id', how='inner')
# Tạo DataFrame cho merged_data
merged_data_df = pd.DataFrame(merged_data)
