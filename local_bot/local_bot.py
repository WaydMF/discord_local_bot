import argparse
import os

from discord.ext import commands

from helpers import dynamodb
from music.music import Music


default_prefix = os.getenv('default_prefix')
guild_config_table_name = os.getenv('guild_config_table_name')


def get_prefix(bot, message):
    """Gets prefix for specific guild."""
    guild_prefixes = dynamodb.get_prefixes(guild_config_table_name, message.guild.id)

    for prefix in guild_prefixes:
        if message.content.startswith(prefix):
            return message.content[:len(prefix)]


local_bot = commands.Bot(command_prefix=get_prefix, description="Local Bot")
local_bot.add_cog(Music(local_bot))


@local_bot.event
async def on_guild_join(guild):
    """Sets the prefix for new guild."""

    dynamodb.add_prefixes(guild_config_table_name, guild.id, default_prefix)


@local_bot.command(name="show_prefixes", aliases=["prefixes"])
async def show_prefixes(ctx: commands.Context):
    """Shows the prefixes for guild by admin command."""

    guild_prefixes = dynamodb.get_prefixes(guild_config_table_name, ctx.guild.id)

    await ctx.send(f"Prefixes: {guild_prefixes}")


@local_bot.command(name="remove_prefix", aliases=["remove_prefixes"])
async def remove_prefix(ctx: commands.Context):
    """Sets the prefix for guild by admin command."""

    command_part_of_message = f"{ctx.prefix}{ctx.command.name} "
    rm_prefixes = ctx.message.content[len(command_part_of_message):].split()

    dynamodb.remove_prefixes(guild_config_table_name, ctx.guild.id, rm_prefixes)


@local_bot.command(name="add_prefix", aliases=["add_prefixes"])
async def add_prefix(ctx: commands.Context):
    """Sets the prefix for guild by admin command."""

    command_part_of_message = f"{ctx.prefix}{ctx.command.name} "
    new_prefixes = ctx.message.content[len(command_part_of_message):].split()
    dynamodb.add_prefixes(guild_config_table_name, ctx.guild.id, new_prefixes)


@local_bot.event
async def on_ready():
    print(f"Logged in as:\n{local_bot.user.name}\n{local_bot.user.id}")

if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-t', "--token", help="Bot token", type=str)
    args = arg_parser.parse_args()

    local_bot.run(args.token)
