import asyncio
import itertools
import random

import discord


class Song:
    __slots__ = ("source", "requester")

    def __init__(self, source):
        self.source = source
        self.requester = source.requester

    def get_embed(self):
        embed = (discord.Embed(title="Is playing right now", color=discord.Color.blurple(),
                               description=f"```css\n{self.source.title}\n```")
                 .add_field(name="Duration", value=self.source.duration)
                 .add_field(name="Requester", value=self.requester.mention)
                 .add_field(name="Uploader", value=f"[{self.source.uploader}]({self.source.uploader_url})")
                 .add_field(name="URL", value=f"[Click]({self.source.url})")
                 .set_thumbnail(url=self.source.thumbnail))
        return embed


class SongQueue(asyncio.Queue):
    _queue = None

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
