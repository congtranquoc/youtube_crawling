import json
import os
from GoogleService import GoogleService
from dotenv import load_dotenv
from local.mongdb.MongoConnector import MongoManager


def main():
    load_dotenv()

    project_id = os.getenv('PROJECT_ID')
    bucket_name = os.getenv('BUCKET_NAME')

    collection_playlists = os.getenv('PLAYLISTS')
    collection_videoids = os.getenv('VIDEOIDS')
    collection_commentvideo = os.getenv('COMMENTVIDEO')
    collection_statics = os.getenv('STATICS')

    service_account_json_path = '../key-auth/bigdata-key.json'
    gcp_service = GoogleService(project_id, bucket_name, service_account_json_path)

    file_names = ['playlists_export.json', 'videoids_export.json', 'commentvideo_export.json', 'statics_export.json']
    collections = [collection_playlists, collection_videoids, collection_commentvideo, collection_statics]

    # Kết nối database
    mongo_connection = MongoManager.getInstance()
    mongo_connection.connect()

    for i, file in enumerate(file_names):
        result = gcp_service.download_file(file, f"../data/{file}")
        if result:  # Kiểm tra xem việc tải thành công hay không
            # Đọc dữ liệu từ tệp JSON
            with open(f"../data/{file}", "r", encoding="utf-8") as json_file:
                data = json.load(json_file)

            # Chọn collection tương ứng
            collection_name = collections[i]

            # Thêm dữ liệu vào cơ sở dữ liệu MongoDB
            mongo_connection.insert_many(data, collection=collection_name)

    # Đóng kết nối cơ sở dữ liệu MongoDB
    mongo_connection.close_connection()


if __name__ == "__main__":
    main()
