import asyncio

import discord
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from music.music import Music


class LocalBot(commands.Bot):

    def __init__(self, intents: discord.Intents) -> None:
        super().__init__(command_prefix=('-', '!'), description="Local Bot", intents=intents)

    @property
    def spotify_client(self):
        return spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    async def on_ready(self) -> None:
        await self.add_cog(Music(self))
        print(f'Logged in {self.user} | {self.user.id}')

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if member.bot and self.user.id == member.id:
            return

        vc = member.guild.voice_client
        if (
                before.channel and  # if this is None this could be a join
                after.channel and  # if this is None this could be a leave
                before.channel != after.channel and  # if these match then this could be e.g. server deafen
                isinstance(vc, discord.VoiceClient) and  # None & not external Protocol check
                vc.channel == after.channel  # our current voice client is in this channel
        ):
            # If the voice was intentionally paused don't resume it for no reason
            if vc.is_paused():
                return
            # If the voice isn't playing anything there is no sense in trying to resume
            if not vc.is_playing():
                return

            await asyncio.sleep(0.5)
            vc.pause()
            vc.resume()
