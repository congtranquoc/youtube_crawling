from modules.general_classes import *
from scripts.crawl.YoutubeAPI import YouTubeAPI


class ViewLikeCommentCrawler(YouTubeAPI):
    def __init__(self, video_ids):
        super().__init__()
        self.video_ids = video_ids

    def get_video_comments(self, video_data):
        comments = []
        next_page_token = None
        # try:
        while True:
            response = self.youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_data["video_id"],
                maxResults=100,
                pageToken=next_page_token
            ).execute()
            comments_data = self.data_mining(response["items"], kind=response["kind"], collection=video_data["playlist_program"])
            if comments_data:
                comments.extend(comments_data)
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        # except Exception as e:
        #     print('ViewLikeCommentCrawler-get_video_comments has an error occurred:', str(e))
        return comments

    def get_video_statics(self, video_data):
        try:
            response = self.youtube.videos().list(
                part='statistics',
                id=video_data["video_id"]
            ).execute()

            video_statics = self.data_mining(response["items"], kind=response["kind"], collection=video_data["playlist_program"])
            return video_statics
        except Exception as e:
            print('ViewLikeCommentCrawler-get_video_statics has an error occurred:', str(e))
            return None

    def crawl_data(self):
        list_statics = []
        list_comment = []
        for item in self.video_ids:
            list_statics.extend(self.get_video_statics(item))
            list_comment.extend(self.get_video_comments(item))
        return list_statics, list_comment

    def data_mining(self, response_data, **kwargs):
        _kind = kwargs.get('kind', '')
        _collection = kwargs.get('collection', '')
        if response_data:
            if _kind == 'youtube#videoListResponse':
                _statics = []
                for item in response_data:
                    _statics.append({
                        "video_id": item["id"],
                        "view_count": item["statistics"]["viewCount"],
                        "like_count": item["statistics"]["likeCount"],
                        "comment_count": item["statistics"]["commentCount"],
                        "playlist_program": _collection
                    })
                return _statics
            elif _kind == 'youtube#commentThreadListResponse':
                comments = []
                for item in response_data:
                    data = item["snippet"]
                    comments.append({
                        "author": data["topLevelComment"]["snippet"]["authorDisplayName"],
                        "comment": data["topLevelComment"]["snippet"]["textOriginal"],
                        "video_id": data["videoId"],
                        "playlist_program": _collection
                    })
                    if "replies" in item:
                        replies = self.data_mining(item["replies"]["comments"], kind=item["replies"]["comments"][0]["kind"], collection=_collection)
                        comments.extend(replies)
                return comments
            elif _kind == "youtube#comment":
                replies = []
                for item in response_data:
                    item = item["snippet"]
                    replies.append({
                        "author": item["authorDisplayName"],
                        "comment": item["textOriginal"],
                        "video_id": item["videoId"],
                        "playlist_program": _collection
                    })
                return replies
            else:
                raise ValueError("This is not correct response.")