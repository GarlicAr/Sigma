import random
import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from flask import Flask
from src import responses
from collections import deque
from datetime import datetime
from src.config import config
from src.config.config import Token, SPAM_MESSAGE_LIMIT, SPAM_TIMEFRAME
from src.controllers.database_controller import setup_database, connect_to_database, update_xp
from src.functions.basic_functions import split_message, temp_mute_user, contains_url, is_admin_or_moderator
from src.text.paragraphs import discord_rules, acceptance_message, help_message, commands_list, prohibited_words
from src.controllers.twitch_controller import checkIfLive

app = Flask(__name__)
greeted_users = set()
user_roles = {}
user_messages = {}
user_warnings = {}
reacted_users = {}
giveaway_entries = {}
isLive = False

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    @bot.event
    async def on_ready():
        print(f'BOT {bot.user} is now running!')
        twitchNotification.start()
        setup_database()

    @tasks.loop(seconds=30)
    async def twitchNotification():
        channel = config.channel
        global isLive
        stream = checkIfLive(channel)

        if stream != "OFFLINE" and not isLive:
            # Find the Discord channel
            for guild in bot.guilds:
                for channel in guild.channels:
                    if channel.name == "general" and isinstance(channel, discord.TextChannel):
                        # Send a notification in the Discord channel
                        await channel.send(
                            f"Hi guys, RWEEEDS is currently LIVE on twitch!! \n https://www.twitch.tv/rweeeds \n @everyone")
                        isLive = True
                        return
        elif stream == "OFFLINE" and isLive:
            isLive = False

    @bot.event
    async def on_member_join(member):
        channel = discord.utils.get(member.guild.channels, name="welcome")
        if channel:
            await channel.send(
                f"Welcome {member.mention}! ")

            rule_parts = split_message(discord_rules)
            for part in rule_parts:
                await channel.send(part)

            await channel.send(acceptance_message)

    @bot.command()
    async def xp(ctx):
        user_id = str(ctx.author.id)
        conn = connect_to_database()
        c = conn.cursor()
        # Update the query for PostgreSQL (using placeholders)
        c.execute("SELECT xp, rank FROM users WHERE user_id = %s", (user_id,))
        result = c.fetchone()
        if result:
            xp, rank = result
            # Define XP thresholds for each rank
            thresholds = {
                "Bot": 250,
                "Alcoholic": 700,
                "MethHead": 1200,
                "Rockstar": 2000,
                "Heisenberg": 4000,
                # Assuming KURWAMACH is the highest rank with no upper XP limit
            }

            # Match rank with corresponding emoji and calculate XP to next rank
            emoji_dict = {
                "Bot": ":robot:",
                "Alcoholic": ":beer:",
                "MethHead": ":pill:",
                "Rockstar": ":guitar:",
                "Heisenberg": ":man_scientist:",
                "KURWAMACH": ":boom:",
            }

            next_rank_dict = {
                "Bot": "Alcoholic",
                "Alcoholic": "MethHead",
                "MethHead": "Rockstar",
                "Rockstar": "Heisenberg",
                "Heisenberg": "KURWAMACH",
                "KURWAMACH": "Max Rank",
            }

            emoji = emoji_dict.get(rank, "")
            next_rank = next_rank_dict.get(rank, "")

            if rank != "KURWAMACH":
                xp_to_next = thresholds[next_rank] - xp
                await ctx.send(
                    f"{ctx.author.name}, You have {xp} XP. Your rank is {emoji} {rank} {emoji}. XP to next rank ({next_rank}): {xp_to_next}")
            else:
                # Max rank reached
                await ctx.send(
                    f"{ctx.author.name}, You have {xp} XP. Your rank is {emoji} {rank} {emoji}. You have reached the maximum rank!")
        else:
            await ctx.send("You have 0 XP. Pathetic....")

        # Don't forget to close the connection
        conn.close()

    @bot.command()
    @has_permissions(administrator=True)
    async def start_giveaway(ctx, giveaway_name: str, image_url: str):
        """Starts a new giveaway."""
        try:
            await ctx.message.delete()

            embed = discord.Embed(title=f"🎉 Giveaway: {giveaway_name} 🎉", description="React with 🎁 to enter!",
                                  color=0x00ff00)
            embed.set_image(url=image_url)

            giveaway_message = await ctx.send(embed=embed)
            await giveaway_message.add_reaction("🎁")

            # Store the message ID and an empty list of entrants
            giveaway_entries[giveaway_message.id] = []

            # Inform the admin of the giveaway message ID
            await ctx.author.send(f"Giveaway '{giveaway_name}' started! Giveaway ID: {giveaway_message.id}")

        except:
            print("error")

    @bot.command()
    @has_permissions(administrator=True)
    async def end_giveaway(ctx, message_id: int):
        """Ends a giveaway and picks a winner."""
        try:
            await ctx.message.delete()

            message_id = int(message_id)
            if message_id in giveaway_entries and giveaway_entries[message_id]:
                winner_id = random.choice(giveaway_entries[message_id])
                winner_user = await ctx.guild.fetch_member(winner_id)
                await ctx.send(f"🎉 Congratulations {winner_user.mention}! You won the giveaway!")
            else:
                print("No valid giveaway!")
            # Optionally, clear the giveaway data
            del giveaway_entries[message_id]
        except:
            print("Giveaway Error")

    @bot.event
    async def on_reaction_add(reaction, user):
        """Handles reaction adds for giveaways."""
        if user == bot.user:
            return

        if user != bot.user and str(reaction.emoji) == "🎁" and reaction.message.id in giveaway_entries:
            giveaway_entries[reaction.message.id].append(user.id)

        # Initialize a set for storing users who reacted to this message
        if reaction.message.id not in reacted_users:
            reacted_users[reaction.message.id] = set()

        # Award XP only if the user hasn't reacted to this message before
        if user.id not in reacted_users[reaction.message.id]:
            await update_xp(str(user.id), 5)
            reacted_users[reaction.message.id].add(user.id)

    @bot.event
    async def on_message(message):
        global greeted_users
        user_id = message.author.id
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        # Skip processing if the message is from the bot
        if message.author == bot.user:
            return

        # Spam protection
        now = datetime.now()
        if message.author.id not in user_messages:
            user_messages[message.author.id] = deque(maxlen=SPAM_MESSAGE_LIMIT)
        msgs = user_messages[message.author.id]

        if msgs and now - msgs[0] < SPAM_TIMEFRAME:
            # Detected spamming
            await message.delete()
            warning_msg = "Please do not spam the chat."

            # Update the user's warning count
            user_warnings[message.author.id] = user_warnings.get(message.author.id, 0) + 1

            # Check if the user has reached 3 warnings
            if user_warnings[message.author.id] >= 3:
                # Mute the user and reset the warning count
                await temp_mute_user(message.author, 300)  # Mute duration in seconds
                await message.channel.send(f"{message.author.mention} has been muted for 5 minutes!")
                user_warnings[message.author.id] = 0  # Reset the warning count after muting
            else:
                # If not yet muted, send a warning message
                await message.channel.send(
                    f"{message.author.mention} {warning_msg}. Warning #{user_warnings[message.author.id]}")
        else:
            # No spam detected, process the message
            msgs.append(now)

        # Check for prohibited words
        if any(word in message.content.lower() for word in prohibited_words):
            await message.delete()
            await temp_mute_user(message.author, 600)

            # Check for URLs in the message
        if contains_url(message.content):
            # Allow SigmaBot, Admins, and Moderators to send links
            if message.author != bot.user and not is_admin_or_moderator(message.author, message.guild):
                await message.delete()
                warning_message = "Sending links is not allowed in this channel."
                await message.channel.send(f"{message.author.mention}, {warning_message}")
                return

        if message.guild is not None:
            welcome_channel = discord.utils.get(message.guild.channels, name="welcome")

            if message.channel == welcome_channel and message.content.lower() == 'i accept':
                role_name = "Junkie"
                role = discord.utils.get(message.guild.roles, name=role_name)
                if role:
                    await message.author.add_roles(role)

        if message.author == bot.user:
            return

        print(f"{username} said: {user_message}, in channel: {channel}")

        if user_message == "hello" and user_id not in greeted_users:
            greeted_users.add(user_id)
            await send_message(message, user_message, is_private=False)

        elif (user_message.startswith('!')
              and user_message != 'hello'
              and user_message != 'help'
              and user_message != '!help'
              and user_message != 'commands'
              and user_message != '!commands'):

            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)

        elif (user_message != 'hello'
              and user_message != 'help'
              and user_message != '!help'
              and user_message != 'commands'
              and user_message != '!commands'):

            await send_message(message, user_message, is_private=False)

        if user_message == 'help' or user_message == '!help':
            await message.delete()
            await message.author.send(help_message)
            return

        if user_message == 'commands' or user_message == '!commands':
            await message.delete()
            await message.author.send(commands_list)
            return

        await update_xp(str(message.author.id), 1)

        if message.guild is not None and not message.author.bot and not is_admin_or_moderator(message.author,
                                                                                              message.guild):
            # Get the user's current rank from the database
            conn = connect_to_database()
            c = conn.cursor()
            c.execute("SELECT `rank` FROM users WHERE user_id = %s", (str(user_id),))
            result = c.fetchone()
            if result:
                rank = result[0]
                # Define emojis using their Unicode characters
                emojis = {
                    "Bot": "\U0001F916",  # Robot emoji
                    "Alcoholic": "\U0001F37A",  # Beer mug emoji
                    "MethHead": "\U0001F48A",  # Pill emoji
                    "Rockstar": "\U0001F3B8",  # Guitar emoji
                    "Heisenberg": "\U0001F468\u200D\U0001F52C",  # Man scientist emoji
                    "KURWAMACH": "\U0001F4A5"  # Collision emoji
                }
                emoji = emojis.get(rank, "")  # Fallback to an empty string if rank not found
                # Rename the user locally
                new_nickname = f" {emoji} | {username.split('#')[0]}"
                member = message.guild.get_member(user_id)
                if member:
                    try:
                        await member.edit(nick=new_nickname)
                    except discord.Forbidden:
                        print("Bot does not have permission to change nicknames.")
                    except discord.HTTPException as e:
                        print(f"Failed to change nickname: {e}")

        await bot.process_commands(message)

        try:
            if message.content.lower() == ('.clearall'):
                # Check if the user has the manage messages permission
                if message.author.guild_permissions.manage_messages:
                    await message.channel.purge(limit=None, check=lambda m: True, bulk=True)
                    await message.delete()
                else:
                    await message.delete()
        except:
            print("error deleting messages")

    bot.run(Token)

