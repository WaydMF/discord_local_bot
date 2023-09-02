import asyncio
import functools

import discord
import yt_dlp
from discord.ext import commands

from music.utils import *


class YTDLError(Exception):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        "format": "bestaudio/best",
        "extractaudio": True,
        "audioformat": "mp3",
        "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
        "restrictfilenames": True,
        "noplaylist": True,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "logtostderr": False,
        "quiet": True,
        "no_warnings": True,
        "default_search": "auto",
        "source_address": "0.0.0.0",
    }

    FFMPEG_OPTIONS = {
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn",
    }

    ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get("uploader")
        self.uploader_url = data.get("uploader_url")
        date = data.get("upload_date")
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get("title")
        self.thumbnail = data.get("thumbnail")
        self.description = data.get("description")
        self.duration = int(data.get("duration"))
        self.url = data.get("webpage_url")
        self.stream_url = data.get("url")

    def __str__(self):
        return f"**{self.title}** by **{self.uploader}**"

    @classmethod
    async def create_sources(cls, ctx: commands.Context, search: str, loop):

        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError(f"Couldn\'t find anything that matches `{search}`")

        if "entries" not in data:
            processed_info = cls.ytdl.extract_info(data.get('webpage_url'), download=False)
            if processed_info.get('url'):
                yield cls(ctx,
                          discord.FFmpegPCMAudio(processed_info.get('url'), **cls.FFMPEG_OPTIONS),
                          data=processed_info)
            else:
                yield cls(ctx,
                          discord.FFmpegPCMAudio(processed_info.get('entries')[0].get('url'), **cls.FFMPEG_OPTIONS),
                          data=processed_info.get('entries')[0])
        else:

            for index, entry in enumerate(data["entries"]):

                partial = functools.partial(cls.ytdl.extract_info, entry["url"], download=False)
                processed_info = await loop.run_in_executor(None, partial)
                yield cls(ctx, discord.FFmpegPCMAudio(processed_info.get('url'), **cls.FFMPEG_OPTIONS),
                          data=processed_info)
