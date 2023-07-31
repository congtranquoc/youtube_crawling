# Trong main.py
from scripts.playlists_youtube_crawl import PlaylistsCrawler
from scripts.playlits_processor import PlaylistProcessor
from mongodb.MongoConnector import MongoManager
from scripts.videos_youtube_crawl import VideosYoutubeCrawler
def main():
    playlists_crawler = PlaylistsCrawler()
    # playlists_crawler.run()
    # all_playlists = playlists_crawler.get_data()

    # Tiếp tục xử lý dữ liệu
    data_processor = PlaylistProcessor()
    playlist_ids = data_processor.process_playlist_info()

    videos_crawler = VideosYoutubeCrawler()
    # videos_crawler.run(playlist_ids)
    # all_video_ids = videos_crawler.get_data()

    videos_ids = data_processor.process_videos_info()
    print(videos_ids)

    mongo_connection = MongoManager.getInstance()
    mongo_connection.connect()
    # mongo_connection.insert_many_to_playplists(all_playlists)
    # mongo_connection.insert_many_to_video_ids(all_video_ids)

if __name__ == "__main__":
    main()
