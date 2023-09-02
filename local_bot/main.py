import argparse
import os

import discord

from local_bot import LocalBot


intents = discord.Intents.default()
intents.message_content = True

if os.getenv('DISCORD_BOT_TOKEN'):
    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
else:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-t', "--token", help="Bot token", type=str)
    args = arg_parser.parse_args()
    DISCORD_BOT_TOKEN = args.token


if __name__ == "__main__":
    local_bot = LocalBot(intents=intents)
    local_bot.run(DISCORD_BOT_TOKEN)
