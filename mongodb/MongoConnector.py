import os
from urllib.parse import quote_plus

from pymongo import MongoClient
from envyaml import EnvYAML
from dotenv import load_dotenv


class MongoManager:
    __instance = None

    @staticmethod
    def getInstance(**kwargs):
        if MongoManager.__instance is None:
            MongoManager.__instance = MongoManager(**kwargs)
        return MongoManager.__instance

    def __init__(self, **kwargs):
        load_dotenv()
        if MongoManager.__instance is not None:
            raise Exception("This class is a singleton!")

        # read file env.yaml and parse config
        self.host = os.getenv('HOST')
        self.database = os.getenv('DATABASE')

        # Khởi tạo username và password từ kwargs hoặc để giá trị mặc định là None
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)

        self.mongo = None
        self.client = None
        MongoManager.__instance = self

    def connect(self):
        # create string to connection mongodb
        if self.username and self.password:
            connection_string = f"mongodb://{quote_plus(self.username)}:{quote_plus(self.password)}@{self.host}:27017"
        else:
            connection_string = f"mongodb://{self.host}:27017"

        # connection
        self.client = MongoClient(connection_string)
        self.mongo = self.client[self.database]

    def is_connected(self):
        if self.client is not None:
            return True
        return False

    def insert_many(self, datas, collection):
        if not self.is_connected():
            self.connect()
        database = self.mongo.get_collection(collection)
        database.insert_many(datas)

    def close_connection(self):
        if self.client is not None:
            self.client.close()
