import re

import discord
import asyncio

from discord.ext import commands

user_roles = {}
admin_role_name = "Administrator"
moderator_role_name = "Moderator"
owner = "Owner"

intents = discord.Intents.default()
intents.messages = True
intents.dm_messages = True
intents.message_content = True
intents.typing = True
intents.emojis = True
intents.members = True
intents.guild_messages = True
intents.guilds = True
intents.moderation = True
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


def split_message(message, length=2000):
    return [message[i:i+length] for i in range(0, len(message), length)]

def contains_url(message):
    url_regex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    whitelist = ['tenor.com', 'giphy.com', 'tiktok.com', 'youtube.be', 'youtube.com', 'twitch.tv']  # List of allowed GIF providers

    urls = re.findall(url_regex, message)
    for url in urls:
        if not any(gif_provider in url for gif_provider in whitelist):
            return True  # Return True if there's a URL that's not in whitelist
    return False  # Return False if all URLs are from whitelist

def is_admin_or_moderator(user, guild):
    if user == guild.owner:  # Check if the user is the server owner
        return True
    return any(role.name in [admin_role_name, moderator_role_name] for role in user.roles)

def create_progress_bar(current, total):
    # Simple text-based progress bar
    bar_length = 20
    proportion = current / total
    progress = int(proportion * bar_length)
    return "🟩" * progress + "⬛" * (bar_length - progress)

async def temp_mute_user(member, duration=20):
    global user_roles

    channel = discord.utils.get(member.guild.channels, name="general")

    # Save the user's current roles
    user_roles[member.id] = [role for role in member.roles if role.name != "@everyone"]

    # Fetch the "Muted" role
    muted_role = discord.utils.get(member.guild.roles, name="Muted")

    # Remove current roles and add "Muted" role
    if muted_role:
        await member.remove_roles(*user_roles[member.id])
        await member.add_roles(muted_role)

        if channel:
            await channel.send(f"{member.mention} has been muted for {duration / 60:.0f} minutes!")

        # Wait for the duration of the mute
        await asyncio.sleep(duration)

        # Restore the original roles and remove "Muted" role
        await member.add_roles(*user_roles[member.id])
        await member.remove_roles(muted_role)

        await channel.send(f"{member.mention} has been unmuted!")

        # Remove user from the dictionary
        del user_roles[member.id]
