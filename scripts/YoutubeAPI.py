from googleapiclient.discovery import build
from dotenv import load_dotenv
from modules.general_classes import *

class YouTubeAPI:
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv('youtube_api_key')
        self.youtube = build('youtube', 'v3', developerKey=self.API_KEY)
