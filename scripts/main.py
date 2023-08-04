# Trong main.py
from scripts.playlists_youtube_crawl import PlaylistsCrawler
from scripts.playlits_processor import PlaylistProcessor
from mongodb.MongoConnector import MongoManager
from scripts.videos_youtube_crawl import VideosYoutubeCrawler

OUTPUT_RAPVIE = "playlist_rapvie.json"
OUPUT_NALA = "playlist_nala.json"
def main():

    playlists_crawler = PlaylistsCrawler()
    playlists_crawler.run()
    all_playlists = playlists_crawler.get_data()

    # Tiếp tục xử lý dữ liệu
    data_processor = PlaylistProcessor()
    playlist_ids_rapvie, playlist_ids_nala = data_processor.process_playlist_info()

    videos_crawler = VideosYoutubeCrawler()
    videos_crawler.run(playlist_ids_rapvie, OUTPUT_RAPVIE)
    videos_crawler.run(playlist_ids_nala, OUPUT_NALA)

    all_video_ids_rapvie = data_processor.get_data(OUTPUT_RAPVIE)
    all_video_ids_nala = data_processor.get_data(OUPUT_NALA)

    videos_ids_rapvie = data_processor.process_videos_info(OUTPUT_RAPVIE)
    videos_ids_nala = data_processor.process_videos_info(OUPUT_NALA)
    mongo_connection = MongoManager.getInstance()
    mongo_connection.connect()
    # mongo_connection.insert_many_to_playplists(all_playlists)
    # mongo_connection.insert_many_to_video_ids(all_video_ids)

if __name__ == "__main__":
    main()
