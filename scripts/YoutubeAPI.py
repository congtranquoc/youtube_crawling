from googleapiclient.discovery import build
from dotenv import load_dotenv
from modules.general_classes import *

class YouTubeAPI:
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv('YOUTUBE_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.API_KEY)
        self.channel_id = os.getenv('CHANNEL_ID')

    def craw_data(self):
        pass
