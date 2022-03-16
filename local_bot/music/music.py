import math

import discord
from discord.ext import commands

from song import Song
from voice_state import VoiceState, VoiceError
from ytdl_source import YTDLSource, YTDLError


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage("Эта команда не используется в ЛС (Личные сообщения)")

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send(f"Меня это пугает. Произошла какая-то ошибка: {str(error)}")

    @commands.command(name="join", invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        """Joins a voice channel."""

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name="summon")
    @commands.has_permissions(manage_guild=True)
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        """Summons the bot to a voice channel.
        If no channel was specified, it joins your channel.
        """

        if not channel and not ctx.author.voice:
            raise VoiceError("Вы не подключены к голосовому каналу. И не указали куда подключаться.")

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name="leave", aliases=["disconnect"])
    @commands.has_permissions(manage_guild=True)
    async def _leave(self, ctx: commands.Context):
        """Clears the queue and leaves the voice channel."""

        if not ctx.voice_state.voice:
            return await ctx.send("Бот и так не подключен. Зачем его кикать?")

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

    @commands.command(name="volume")
    async def _volume(self, ctx: commands.Context, *, volume: int):
        """Sets the volume of the player."""

        if not ctx.voice_state.is_playing:
            return await ctx.send("Сейчас музыка не играет. Можете включить.")

        if not 0 <= volume <= 100:
            return await ctx.send("Громкость должна быть между 0 и 100!")

        ctx.voice_state.volume = volume / 100
        ctx.voice_state.current.source.volume = volume / 100
        await ctx.send(f"Громкость изменена на {volume}%")

    @commands.command(name="now", aliases=["current", "playing"])
    async def _now(self, ctx: commands.Context):
        """Displays the currently playing song."""

        await ctx.send(embed=ctx.voice_state.current.get_embed())

    @commands.command(name="pause")
    async def _pause(self, ctx: commands.Context):
        """Pauses the currently playing song."""

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction("⏯")

    @commands.command(name="resume")
    async def _resume(self, ctx: commands.Context):
        """Resumes a currently paused song."""

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('⏯')

    @commands.command(name="stop")
    async def _stop(self, ctx: commands.Context):
        """Stops playing song and clears the queue."""

        ctx.voice_state.songs.clear()

        if ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('⏹')

    @commands.command(name="skip", aliases=["next"])
    async def _skip(self, ctx: commands.Context):
        """Skips a song."""

        if not ctx.voice_state.is_playing:
            return await ctx.send("Сейчас музыка не играет,зачем её пропускать? Можете включить.")

        await ctx.message.add_reaction('⏭')
        ctx.voice_state.skip()

    @commands.command(name="queue", aliases=["list"])
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        """Shows the player's queue.
        You can optionally specify the page to show. Each page contains 10 elements.
        """

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send("В очереди нет треков. Можете добавить.")

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += f"`{i + 1}.` [**{song.source.title}**]({song.source.url})\n"

        embed = (discord.Embed(description=f"**{len(ctx.voice_state.songs)} tracks:**\n\n{queue}")
                 .set_footer(text=f"Viewing page {page}/{pages}"))
        await ctx.send(embed=embed)

    @commands.command(name="shuffle")
    async def _shuffle(self, ctx: commands.Context):
        """Shuffles the queue."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send("В очереди нет треков. Можете добавить.")

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

    @commands.command(name="remove")
    async def _remove(self, ctx: commands.Context, index: int):
        """Removes a song from the queue at a given index."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send("В очереди нет треков. Можете добавить.")

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

    @commands.command(name="loop")
    async def _loop(self, ctx: commands.Context):
        """Loops the currently playing song.
        Invoke this command again to unloop the song.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send("Ничего не играет в данный момент.")

        # Inverse boolean value to loop and unloop.
        ctx.voice_state.loop = not ctx.voice_state.loop
        if ctx.voice_state.loop:
            await ctx.send("Зациклено")
        else:
            await ctx.send("Разциклено")
        await ctx.message.add_reaction('✅')

    @commands.command(name="play", aliases=["p"])
    async def _play(self, ctx: commands.Context, *, search: str):
        """Plays a song.
        If there are songs in the queue, this will be queued until the
        other songs finished playing.
        This command automatically searches from various sites if no URL is provided.
        A list of these sites can be found here: https://rg3.github.io/youtube-dl/supportedsites.html
        """

        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        if ctx.voice_state.audio_player.done():
            ctx.voice_state.prepare_audio_player()

        async with ctx.typing():
            try:
                full_duration = 0
                sources_list = []
                async for source in YTDLSource.create_sources(ctx, search, loop=self.bot.loop):
                    song = Song(source)
                    full_duration += int(source.data.get("duration"))
                    await ctx.voice_state.songs.put(song)
                    sources_list.append(str(source))

                full_duration = YTDLSource.parse_duration(full_duration)
                if len(sources_list) > 1:
                    sources_list = '\n'.join(sources_list)
                    if len(sources_list) > 1000:
                        await ctx.send(f"Успешно добавлен большой плейлист общей длительностю {full_duration}")
                    else:
                        await ctx.send(f"Успешно добавлено:\n{sources_list}\nОбщая длительность: {full_duration}")
                else:
                    sources_list = '\n'.join(sources_list)
                    await ctx.send(f"Успешно добавлено:\n{sources_list}\n")
            except YTDLError as e:
                await ctx.send(f"Произошла ошибка при обработке этого запроса: {str(e)}")

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError("Сначала подключись к голосовому.")

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError("Бот уже подключен с голосовому каналу.")
