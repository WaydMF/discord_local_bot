import asyncio
import itertools
import random

import discord

from ytdl_source import YTDLSource


class Song:
    __slots__ = ("source", "requester")

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def get_embed(self):
        embed = (discord.Embed(title="Сейчас играет",
                               description=f"```css\n{self.source.title}\n```",
                               color=discord.Color.blurple())
                 .add_field(name="Длительность", value=self.source.duration)
                 .add_field(name="Запросил", value=self.requester.mention)
                 .add_field(name="Автор видео", value=f"[{self.source.uploader}]({self.source.uploader_url})")
                 .add_field(name="Ссылка", value=f"[Click]({self.source.url})")
                 .set_thumbnail(url=self.source.thumbnail))

        return embed


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]
