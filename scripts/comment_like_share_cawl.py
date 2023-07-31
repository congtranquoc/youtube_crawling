import os
import json
import time

from googleapiclient.discovery import build
from dotenv import load_dotenv
class YouTubeAPI:

    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv('youtube_api_key')
        self.CHANNEL_ID = os.getenv('CHANNEL_ID')

        self.state_file = '../data/craw/like_share_cmt/state.json'
        self.output_file = '../data/craw/like_share_cmt/like_share_cmt.json'


    def get_video_comments(self, video_id):
        youtube = build('youtube', 'v3', developerKey=self.API_KEY)
        comments = []
        next_page_token = None

        while True:
            comment_threads = youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token
            ).execute()

            # for thread in comment_threads['items']:
            #     comment = thread['snippet']['topLevelComment']['snippet']
            #     comments.append({
            #         'text': comment['textDisplay'],
            #         'likeCount': comment['likeCount'],
            #         'publishedAt': comment['publishedAt']
            #     })
            datas = comment_threads["items"]
            next_page_token = comment_threads.get('nextPageToken')
            comments.extend(datas)
            if not next_page_token:
                break
        return comments

    def get_video_statistics(self, video_id):
        youtube = build('youtube', 'v3', developerKey=self.API_KEY)
        video_response = youtube.videos().list(
            part='statistics',
            id=video_id
        ).execute()

        video = video_response['items'][0]
        return {
            'viewCount': video['statistics']['viewCount'],
            'likeCount': video['statistics']['likeCount'],
            'dislikeCount': video['statistics']['dislikeCount'],
            'commentCount': video['statistics']['commentCount']
        }

    def main(self):
        datas = self.get_video_comments("-4_ekEvTP2c")

        with open(self.output_file, 'w', encoding='utf-8') as file:
            json.dump(datas, file, ensure_ascii=False)

if __name__ == "__main__":
    crawler = YouTubeAPI()
    crawler.main()