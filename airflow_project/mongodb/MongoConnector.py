import os
from pymongo import MongoClient
from urllib.parse import quote_plus
from dotenv import load_dotenv

class MongoManager:
    __instance = None

    @staticmethod
    def getInstance(**kwargs):
        if MongoManager.__instance is None:
            MongoManager.__instance = object.__new__(MongoManager)
            MongoManager.__instance.__init__(**kwargs)
        return MongoManager.__instance

    def __init__(self, **kwargs):
        load_dotenv()

        # read environment variables or use default values
        self.host = os.getenv('HOST')
        self.database = os.getenv('DATABASE')

        # Initialize username and password from kwargs or default to None
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)

        self.mongo = None
        self.client = None

    def connect(self):
        # create connection string for MongoDB
        if self.username and self.password:
            connection_string = f"mongodb://{quote_plus(self.username)}:{quote_plus(self.password)}@{self.host}:27017"
        else:
            connection_string = f"mongodb://{self.host}:27017"

        # connect to MongoDB
        self.client = MongoClient(connection_string)
        self.mongo = self.client[self.database]

    def is_connected(self):
        return self.client is not None

    def insert_many(self, data, collection):
        if not self.is_connected():
            self.connect()
        database = self.mongo.get_collection(collection)
        database.insert_many(data, ordered=True)

    #Hàm lấy tất cả data của collection chỉ định
    def get_data(self, collection_name):
        if not self.is_connected():
            self.connect()
        collection = self.mongo.get_collection(collection_name)
        data = list(collection.find())
        return data

    #Hàm lấy Playlist ID của 2 chương trình RapVie mùa 3 và NALA 2023
    def get_data_from_playlist(self):
        if not self.is_connected():
            self.connect()
        target_titles = {
            "Rap Việt": "RAP VIỆT Mùa 3 (2023) | 20:00 Thứ 7 hàng tuần",
            "Người Ấy Là Ai?": "NGƯỜI ẤY LÀ AI? Mùa 5 (2023) | 20:00 Thứ 6 hàng tuần"
        }
        collection = self.mongo.get_collection(os.getenv('PLAYLISTS'))

        matched_playlist_ids = []

        # Duyệt qua các tiêu đề trong target_titles và tìm kiếm trong collection "playlist"
        for key, value in target_titles.items():
            query = {"title": value}
            playlist = collection.find_one(query)
            if playlist:
                matched_playlist_ids.append((key, playlist["playlist_id"]))

        # Tạo tuple từ danh sách các kết quả match (playlist_id)
        result_tuple = tuple([playlist_id for _, playlist_id in matched_playlist_ids])

        return result_tuple

    def close_connection(self):
        if self.client is not None:
            self.client.close()

