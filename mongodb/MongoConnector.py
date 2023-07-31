from urllib.parse import quote_plus

from pymongo import MongoClient
from envyaml import EnvYAML


class MongoManager:
    __instance = None

    @staticmethod
    def getInstance():
        if MongoManager.__instance is None:
            MongoManager.__instance = MongoManager()
        return MongoManager.__instance

    def __init__(self):
        if MongoManager.__instance is not None:
            raise Exception("This class is a singleton!")
        # read file env.yaml and parse config
        self.env = EnvYAML("../config/config.yaml")
        self.mongodb_config = self.env['mongodb']
        self.host = self.mongodb_config['host']
        self.username = quote_plus(self.mongodb_config['username'])
        self.pwd = quote_plus(self.mongodb_config['password'])
        self.database = self.mongodb_config['database']
        self.collections = self.mongodb_config["collections"]
        self.mongo = None
        self.client = None
        MongoManager.__instance = self

    def connect(self):
        # create string to connection mongodb
        # connection_string = f"mongodb://{username}:{pwd}@{host}/{database}"
        connection_string = f"mongodb://{self.host}:27017"
        # connection
        self.client = MongoClient(connection_string)
        self.mongo = self.client[self.database]

    def is_connected(self):
        if self.client is not None:
            return True
        return False
    def insert_many_to_playplists(self, datas):
        if not self.is_connected():
            self.connect()
        playlists = self.mongo.get_collection(self.collections["playlists"])
        playlists.insert_many(datas)


    def close_connection(self):
        if self.client is not None:
            self.client.close()