import argparse

import discord
from discord.ext import commands

from music.music import Music


intents = discord.Intents.default()
intents.message_content = True

local_bot = commands.Bot(command_prefix=('-', '!'), description="Local Bot", intents=intents)


@local_bot.event
async def on_ready():
    await local_bot.add_cog(Music(local_bot))
    print(f"Logged in as:\n{local_bot.user.name}\n{local_bot.user.id}")


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-t', "--token", help="Bot token", type=str)
args = arg_parser.parse_args()


if __name__ == "__main__":
    local_bot.run(args.token)
