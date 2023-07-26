import googleapiclient.discovery

# Thay thế 'YOUR_API_KEY' bằng API key của bạn
api_key = 'YOUR_API_KEY'
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

def get_channel_videos(channel_id):
    videos_info = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token
        )

        response = request.execute()
        for item in response['items']:
            video_id = item['id']['videoId']
            video_info = get_video_info(video_id)
            videos_info.append(video_info)

        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    return videos_info

def get_video_info(video_id):
    request = youtube.videos().list(
        part='snippet,statistics',
        id=video_id
    )
    response = request.execute()
    video_info = {
        'title': response['items'][0]['snippet']['title'],
        'video_id': video_id,
        'views': response['items'][0]['statistics']['viewCount'],
        'likes': response['items'][0]['statistics']['likeCount'],
        'dislikes': response['items'][0]['statistics']['dislikeCount'],
        'comments': response['items'][0]['statistics']['commentCount']
    }
    return video_info

channel_id = 'UCkna2OcuN1E6u5I8GVtdkOw'  # Thay thế 'CHANNEL_ID' bằng ID của kênh cần crawl
videos_info = get_channel_videos(channel_id)

for video_info in videos_info:
    print(f"Video Title: {video_info['title']}")
    print(f"Video ID: {video_info['video_id']}")
    print(f"Views: {video_info['views']}")
    print(f"Likes: {video_info['likes']}")
    print(f"Dislikes: {video_info['dislikes']}")
    print(f"Comments: {video_info['comments']}")
    print("---------")
