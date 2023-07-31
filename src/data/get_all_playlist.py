import time

import googleapiclient.discovery

from mongodb.MongoConnector import MongoManager



class GetAllPlaylist():

    def __init__(self):
        self.mongo_connection = MongoManager.getInstance()
        self.mongo_connection.connect()
        self.AP_KEY = 'AIzaSyAPD2awoKWWsP6h33TGJFBdiRi7PBYz7pY'
        self.youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=self.AP_KEY)
        self.channel_id = 'UCkna2OcuN1E6u5I8GVtdkOw'

    def get_all_playlists(self):
        next_page_token = None
        all_playlists = []

        while True:
            request = self.youtube.playlists().list(
                part='snippet',
                channelId=self.channel_id,
                maxResults=50,
                pageToken=next_page_token
            )

            response = request.execute()
            all_playlists.extend(response['items'])
            next_page_token = response.get('nextPageToken')
            if len(all_playlists) >= 200:
                print(f"import")
                print(f"{all_playlists}")
                self.mongo_connection.insert_many_to_playplists(all_playlists)
                all_playlists.clear()
            time.sleep(5)
            if not next_page_token:
                break



    def main(self):
        self.get_all_playlists()

if __name__ == "__main__":
    obj = GetAllPlaylist()
    obj.main()
