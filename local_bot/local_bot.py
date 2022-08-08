import os

from discord.ext import commands

from helpers import dynamodb, s3
from music.music import Music

import sys
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# print(sys.path)
# s3.get_ffmpeg()
# print(os.listdir(os.path.dirname(os.path.abspath(__file__))))
# print(os.getcwd())

import subprocess

print("Getting FFMPEG....")
package_name = "ffmpeg"
result = subprocess.run(["apt", "update"], capture_output=True, text=True)
print("stdout:", result.stdout)
print("stderr:", result.stderr)
print("first subprocess.run")
result = subprocess.run(["apt", "install", "-y", package_name], capture_output=True, text=True)
print("stdout:", result.stdout)
print("stderr:", result.stderr)
print("second subprocess.run")
result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
print("stdout:", result.stdout)
print("stderr:", result.stderr)
raise Exception

discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
default_command_prefix = os.getenv('DEFAULT_COMMAND_PREFIX')
guild_config_table_name = os.getenv('CONFIG_TABLE')


def get_prefix(bot, message):
    """Gets prefix for specific guild."""
    guild_prefixes = dynamodb.get_prefixes(guild_config_table_name, str(message.guild.id))

    for prefix in guild_prefixes:
        if message.content.startswith(prefix):
            return message.content[:len(prefix)]


local_bot = commands.Bot(command_prefix=get_prefix, description="Local Bot")
local_bot.add_cog(Music(local_bot))


@local_bot.event
async def on_guild_join(guild):
    """Sets the prefix for new guild."""

    for k, v in sorted(os.environ.items()):
        print(f"{k}: {v}")
    dynamodb.add_prefixes(guild_config_table_name, str(guild.id), default_command_prefix)


@local_bot.command(name="show_prefixes", aliases=["prefixes"])
async def show_prefixes(ctx: commands.Context):
    """Shows the prefixes for guild by admin command."""

    guild_prefixes = dynamodb.get_prefixes(guild_config_table_name, str(ctx.guild.id))

    await ctx.send(f"Prefixes: {guild_prefixes}")


@local_bot.command(name="remove_prefix", aliases=["remove_prefixes"])
async def remove_prefix(ctx: commands.Context):
    """Sets the prefix for guild by admin command."""

    command_part_of_message = f"{ctx.prefix}{ctx.command.name} "
    rm_prefixes = ctx.message.content[len(command_part_of_message):].split()

    dynamodb.remove_prefixes(guild_config_table_name, str(ctx.guild.id), rm_prefixes)


@local_bot.command(name="add_prefix", aliases=["add_prefixes"])
async def add_prefix(ctx: commands.Context):
    """Sets the prefix for guild by admin command."""

    command_part_of_message = f"{ctx.prefix}{ctx.command.name} "
    new_prefixes = ctx.message.content[len(command_part_of_message):].split()
    dynamodb.add_prefixes(guild_config_table_name, str(ctx.guild.id), new_prefixes)


@local_bot.event
async def on_ready():
    print(f"Logged in as:\n{local_bot.user.name}\n{local_bot.user.id}")

if __name__ == "__main__":

    local_bot.run(discord_bot_token)
