# Class thực hiện chạy từng script
# Lưu ý drop tất cả collection trong mongo và xóa tất cả json trong craw khi chạy scipt main, để cập nhật
from airflow_project.scripts.crawl.videos_youtube_crawl import VideosYoutubeCrawler
from airflow_project.mongodb.MongoConnector import *
from airflow_project.scripts.crawl.comment_like_share_cawl import ViewLikeCommentCrawler


def main():
    load_dotenv()

    collection_playlists = os.getenv('PLAYLISTS')
    collection_videoids = os.getenv('VIDEOIDS')
    collection_commentvideo = os.getenv('COMMENTVIDEO')
    collection_statics = os.getenv('STATICS')
    collection_rapvie = os.getenv('COLLECTION_RAPVIE')
    collection_nala = os.getenv('COLLECTION_NALA')

    #Kết nôí database
    mongo_connection = MongoManager.getInstance()
    mongo_connection.connect()

    all_playlists = PlaylistsCrawler().crawl_data()

    # Thực hiện thêm vào database
    if all_playlists:
        print("Insert playlists")
        mongo_connection.insert_many(all_playlists, collection_playlists)

    playlist_ids_rapvie, playlist_ids_nala = mongo_connection.get_data_from_playlist()

    if playlist_ids_rapvie:
        # Thực hiện crawl data của tất cả playlist id
        all_rapvie_videos = VideosYoutubeCrawler(playlist_ids_rapvie, collection=collection_rapvie).crawl_data()

        # Thực hiện thêm vào database
        if all_rapvie_videos:
            print("Insert all_rapvie_videos")
            mongo_connection.insert_many(all_rapvie_videos, collection_videoids)

    if playlist_ids_nala:
        # Thực hiện crawl data của tất cả playlist id
        all_nala_videos = VideosYoutubeCrawler(playlist_ids_nala, collection=collection_nala).crawl_data()
        # Thực hiện thêm vào database
        if all_nala_videos:
            print("Insert all_nala_videos")
            mongo_connection.insert_many(all_nala_videos, collection_videoids)

    # Lấy list ID videos để thực hiện bược tiếp theo crawl dữ liệu từng video
    video_ids = mongo_connection.get_data(collection_videoids)

    if video_ids:
        #Thực hiện crawl comment dựa trên list video ids
        list_statics, list_comment = ViewLikeCommentCrawler(video_ids).crawl_data()
        # Thực hiện thêm vào database
        if list_statics:
            print("Insert list_statics")
            mongo_connection.insert_many(list_statics, collection_statics)

        # Thực hiện thêm vào database
        if list_comment:
            print("Insert list_comment")
            mongo_connection.insert_many(list_comment, collection_commentvideo)

if __name__ == "__main__":
    main()
