from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

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
passwd=os.getenv("passwd")
database=os.getenv("database")
