from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

#REDDIT HEADER
reddit_header_for_videos = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
}

Invite_link = 'https://discord.com/api/oauth2/authorize?client_id=1171020454283190335&permissions=2194124830838&scope=bot'
#Tokens
Token = os.getenv('Token')
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
channel = 'rweeeds'

#SPAM
SPAM_MESSAGE_LIMIT = 2
SPAM_TIMEFRAME = timedelta(seconds=3)

#database
host=os.getenv("host")
user=os.getenv("user")
password=os.getenv("passwd")
database=os.getenv("database")
