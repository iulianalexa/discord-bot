import discord
import queue
import asyncio
import functools
import youtube_dl as ytdl
import youtube_dl.utils as u

class YT():
    comm = True
    def __init__(self, bot):
        self.opts = dict(
            no_cache=True,
            default_search="auto"
        )
        if not discord.opus.is_loaded():
            discord.opus.load_opus('libopus.so.0')
        self.client = bot

    async def yt(self, command, message):
        if message.server not in self.client.vc.keys():
            if message.author.voice.voice_channel:
                if len(command) > 1:
                    nc = command
                    nc.pop(0)
                    url = ""
                    for i in nc:
                        url = url + i + " "
                    url = url[:-1]
                    if message.server not in self.client.q.keys():
                        self.client.q[message.server] = queue.Queue()
                        vc = await self.client.join_voice_channel(message.author.voice.voice_channel)
                        self.client.vc[message.server] = vc
                        msg = await self.client.send_message(message.channel,
                                                           "<a:updating:403035325242540032> Downloading...")
                        try:
                            pl = await vc.create_ytdl_player(url, ytdl_options=self.opts,
                                                            after=functools.partial(self.queue_2, message.server, vc, message.channel))

                            pl.start()
                            await self.client.edit_message(msg, "Now playing: `" + pl.title + "`")
                            self.client.pl[message.server] = pl
                            self.client.vs[message.server] = 0
                            self.client.voters[message.server] = []
                        except (discord.ClientException, u.DownloadError, u.UnavailableVideoError):
                            await self.client.edit_message(msg, "Error playing this song.")
                            self.client.vc.pop(message.server)
                            self.client.q.pop(message.server)

                            await vc.disconnect()

                else:
                    await self.client.send_message(message.channel, "Usage: m!yt [url or search query]")


            else:
                await self.client.send_message(message.channel, "Please connect to a channel.")
        else:
            if len(command) > 1:
                nc = command
                nc.pop(0)
                url = ""
                for i in nc:
                    url = url + i + " "
                url = url[:-1]
                self.client.q[message.server].put(url)
                await self.client.send_message(message.channel, "Added song to queue.")
            else:
                await self.client.send_message(message.channel, "Usage: m!yt [url or search query]")

    async def queue(self, server, vc, channel):
        if self.client.q[server].empty():
            self.client.vc.pop(server)
            self.client.q.pop(server)
            self.client.pl.pop(server)
            self.client.vs.pop(server)
            self.client.voters.pop(server)
            await vc.disconnect()

        else:
            msg = await self.client.send_message(channel,
                                                 "<a:updating:403035325242540032> Downloading...")
            try:
                pl = await vc.create_ytdl_player(self.client.q[server].get(), ytdl_options=self.opts, after=functools.partial(self.queue_2, server, vc, channel))

                pl.start()
            except (discord.ClientException, u.DownloadError, u.UnavailableVideoError):
                await self.client.edit_message(msg, "Error playing this song.")
                await self.queue(server, vc, channel)
                return
            await self.client.edit_message(msg, "Now playing: `" + pl.title + "`")
            self.client.pl[server] = pl
            self.client.vs[server] = 0
            self.client.voters[server] = []

    def queue_2(self, server, vc, channel):
        fut = asyncio.run_coroutine_threadsafe(self.queue(server, vc, channel), self.client.loop)
        fut.result()

def setup(bot):
    bot.add_cog(YT(bot))
    bot.loaded_exts['commands.yt.yt'] = 'YT'
    bot.cmds['yt'] = ["Play a song via YouTube.", "m!yt [url or search query]", None]