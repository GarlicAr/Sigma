import asyncio

import discord
from discord.ext import commands
from flask import Flask
from src.config import config
import requests

app = Flask(__name__)
client_id = config.client_id
client_secret = config.client_secret

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

class Stream:

    def __init__(self, title, streamer, game, thumbnail_url):
        self.title = title
        self.streamer = streamer
        self.game = game
        self.thumbnail_url = thumbnail_url


def getOAuthToken():
    body = {
        'client_id': client_id,
        'client_secret': client_secret,
        "grant_type": "client_credentials"
    }
    r = requests.post('https://id.twitch.tv/oauth2/token', body)

    keys = r.json()

    return keys['access_token']

def checkIfLive(channel):
    url = "https://api.twitch.tv/helix/streams?user_login=" + channel
    token = getOAuthToken()

    HEADERS = {
        'Client-ID': client_id,
        'Authorization': 'Bearer ' + token
    }

    try:

        req = requests.get(url, headers=HEADERS)

        res = req.json()

        if len(res['data']) > 0:
            data = res['data'][0]
            title = data['title']
            streamer = data['user_name']
            game = data['game_name']
            thumbnail_url = data['thumbnail_url']
            stream = Stream(title, streamer, game, thumbnail_url)
            return stream
        else:
            return "OFFLINE"
    except Exception as e:
        return str(e)



