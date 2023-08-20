import os
import json
import time

from googleapiclient.discovery import build

from dotenv import load_dotenv
from modules.general_classes import *
class ViewLikeCommentCrawler:

    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv('youtube_api_key')
        self.CHANNEL_ID = os.getenv('CHANNEL_ID')
        self.youtube = build('youtube', 'v3', developerKey=self.API_KEY)


    def get_video_comments(self, video_id):
        comments = []
        next_page_token = None
        try:
            while True:
                response = self.youtube.commentThreads().list(
                    part='snippet,replies',
                    videoId=video_id,
                    maxResults=100,
                    pageToken=next_page_token
                ).execute()
                datas = response["items"]
                next_page_token = response.get('nextPageToken')
                comments.extend(datas)
                if not next_page_token:
                    break
        except Exception as e:
            print('ViewLikeCommentCrawler-get_video_comments has an error occurred:', str(e))
            return None
        return comments

    def get_video_statics(self, video_id):
        try:
            video_statics = []

            response = self.youtube.videos().list(
                part='statistics',
                id=video_id
            ).execute()

            datas = response["items"]
            video_statics.extend(datas)
            return video_statics
        except Exception as e:
            print('ViewLikeCommentCrawler-get_video_statics has an error occurred:', str(e))
            return None

    def crawl_data(self, videos_ids: list):
        list_statics = []
        list_comment = []
        for item in videos_ids:
            video_statics = self.get_video_statics(item["video_id"])

            if video_statics:
                for video in video_statics:
                    video["playlist_program"] = item["playlist_program"]
                    list_statics.extend(video_statics)
                print(f"video_id: {item['video_id']} ----- video_statics: {video_statics}")

            video_comment = self.get_video_comments(item["video_id"])
            if video_comment:
                for comment in video_comment:
                    if comment:
                        comment["playlist_program"] = item["playlist_program"]
                list_comment.extend(video_comment)

        save_merge_json(list_statics, '../data/craw/like_share_cmt/video_statics.json')
        save_merge_json(list_comment, '../data/craw/like_share_cmt/comment_videos.json')
