# Class thực hiện chạy từng script
# Lưu ý drop tất cả collection trong mongo và xóa tất cả json trong craw khi chạy scipt main, để cập nhật
from dotenv import load_dotenv
from scripts.playlits_processor import *
from scripts.videos_youtube_crawl import VideosYoutubeCrawler
from scripts.playlists_youtube_crawl import *
from scripts.playlits_processor import *
from scripts.videos_processed import *
from mongodb.MongoConnector import *
from scripts.comment_like_share_cawl import ViewLikeCommentCrawler

def main():
    load_dotenv()

    #lấy tất cả playlist trong kênh
    channel_id = os.getenv('CHANNEL_ID')
    collection_playlists = os.getenv('PLAYLISTS')
    collection_videoids = os.getenv('VIDEOIDS')
    collection_commentvideo = os.getenv('COMMENTVIDEO')
    collection_statics = os.getenv('STATICS')
    collection_rapvie = os.getenv('COLLECTION_RAPVIE')
    collection_nala = os.getenv('COLLECTION_NALA')

    PlaylistsCrawler(channel_id).crawl_data()

    playlist_ids_rapvie, playlist_ids_nala = get_id_playlists('../data/craw/playlists_channel_data/all_playlist.json')

    #Thực hiện crawl data của tất cả playlist id
    VideosYoutubeCrawler(playlist_ids_rapvie, collection=collection_rapvie).crawl_data()

    # Thực hiện crawl data của tất cả playlist id
    VideosYoutubeCrawler(playlist_ids_nala, collection=collection_nala).crawl_data()

    #Lấy  list ID videos để thực hiện bược tiếp theo crawl dữ liệu từng video
    video_ids = get_video_ids('../data/craw/videos_data/all_video.json')

    ViewLikeCommentCrawler(video_ids).crawl_data()

    # #Kết nôí database
    mongo_connection = MongoManager.getInstance().connect()
    print("Database has been connected")

    # đọc file json
    all_playlists = read_json('../data/craw/playlists_channel_data/all_playlist.json')
    all_video_ids = read_json('../data/craw/videos_data/all_video.json')
    all_comments = read_json('../data/craw/like_share_cmt/comment_videos.json')
    all_statics = read_json('../data/craw/like_share_cmt/video_statics.json')

    # #Thực hiện thêm vào database
    if all_playlists:
        print("Insert playlists")
        mongo_connection.insert_many(all_playlists, collection_playlists)
    if all_video_ids:
        print("Insert Video Ids")
        mongo_connection.insert_many(all_video_ids, collection_videoids)
    if all_comments:
        print("Insert Comments")
        mongo_connection.insert_many(all_comments, collection_commentvideo)
    if all_statics:
        print("Insert statics")
        mongo_connection.insert_many(all_statics, collection_statics)

if __name__ == "__main__":
    main()
