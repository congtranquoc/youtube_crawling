# Trong main.py
from scripts.playlists_youtube_crawl import PlaylistsCrawler
from scripts.playlits_processor import PlaylistProcessor
from mongodb.MongoConnector import MongoManager

def main():
    api_crawler = PlaylistsCrawler()
    # api_crawler.run()
    all_playlists = api_crawler.get_data()

    # Tiếp tục xử lý dữ liệu
    data_processor = PlaylistProcessor()
    playlist_ids = data_processor.process_playlist_info()



    mongo_connection = MongoManager.getInstance()
    mongo_connection.connect()
    mongo_connection.insert_many_to_playplists(all_playlists)
    print(playlist_ids)

if __name__ == "__main__":
    main()
