import pandas as pd
from pymongo import MongoClient

# Tham số kết nối MongoDB
mongo_uri = "mongodb://localhost:27017/"
database_name = "youtube_db"
collection_names = ["commentvideo", "playlists", "statics", "videoids"]

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
commentvideo_data = data_dict["commentvideo"]
playlists_data = data_dict["playlists"]
statics_data = data_dict["statics"]
videoids_data = data_dict["videoids"]

# In dữ liệu từng bộ sưu tập
print("commentvideo_data:")
print(commentvideo_data)

print("\nplaylists_data:")
print(playlists_data)

print("\nstatics_data:")
print(statics_data)

print("\nvideoids_data:")
print(videoids_data)
