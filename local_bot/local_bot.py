import argparse

from discord.ext import commands

from music.music import Music


local_bot = commands.Bot(command_prefix=('-', '!'), description="Local Bot")
local_bot.add_cog(Music(local_bot))


@local_bot.event
async def on_ready():
    print(f"Logged in as:\n{local_bot.user.name}\n{local_bot.user.id}")


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-t', "--token", help="Bot token", type=str)
args = arg_parser.parse_args()


if __name__ == "__main__":
    local_bot.run(args.token)
