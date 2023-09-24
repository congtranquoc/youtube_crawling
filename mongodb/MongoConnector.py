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
        database.insert_many(data)

    def get_data(self, collection_name):
        if not self.is_connected():
            self.connect()
        collection = self.mongo.get_collection(collection_name)
        data = list(collection.find())
        return data

    def close_connection(self):
        if self.client is not None:
            self.client.close()
