# Class thực hiện chạy từng script
# Lưu ý drop tất cả collection trong mongo và xóa tất cả json trong craw khi chạy scipt main, để cập nhật
from scripts.playlists_youtube_crawl import PlaylistsCrawler
from scripts.playlits_processor import PlaylistProcessor
from mongodb.MongoConnector import MongoManager
from scripts.videos_youtube_crawl import VideosYoutubeCrawler

OUTPUT_RAPVIE = "playlist_rapvie.json"
OUPUT_NALA = "playlist_nala.json"
COLLECTION_RAPVIE = "videoids_rapvie"
COLLECTION_NALA = "videoids_nala"
def main():

    #lấy tất cả playlist trong kênh
    playlists_crawler = PlaylistsCrawler()
    playlists_crawler.run()
    all_playlists = playlists_crawler.get_data()

    # Tiếp tục xử lý dữ liệu trả về ID của 2 playlist
    data_processor = PlaylistProcessor()
    playlist_ids_rapvie, playlist_ids_nala = data_processor.process_playlist_info()

    #Thực hiện crawl data của tất cả playlist id trên
    videos_crawler = VideosYoutubeCrawler()
    videos_crawler.run(playlist_ids_rapvie, OUTPUT_RAPVIE)
    videos_crawler.run(playlist_ids_nala, OUPUT_NALA)

    #Lấy list data ID videos của 2 chương trình
    all_video_ids_rapvie = data_processor.get_data(OUTPUT_RAPVIE)
    all_video_ids_nala = data_processor.get_data(OUPUT_NALA)

    #Lấy  list ID videos để thực hiện bược tiếp theo crawl dữ liệu từng video
    videos_ids_rapvie = data_processor.process_videos_info(OUTPUT_RAPVIE)
    videos_ids_nala = data_processor.process_videos_info(OUPUT_NALA)



    #Kết nôí database
    mongo_connection = MongoManager.getInstance()
    mongo_connection.connect()

    #Thực hiện thêm vào database
    mongo_connection.insert_many_to_playplists(all_playlists)
    mongo_connection.insert_many_to_video_ids(all_video_ids_rapvie, COLLECTION_RAPVIE)
    mongo_connection.insert_many_to_video_ids(all_video_ids_nala, COLLECTION_NALA)

if __name__ == "__main__":
    main()
