import asyncio
import discord
import functools

class Skip():
    comm = True
    def __init__(self, bot):
        if not discord.opus.is_loaded():
            discord.opus.load_opus('libopus.so.0')
        self.client = bot

    async def skip(self, command, message):
        if message.author.permissions_in(message.channel).manage_channels:
            if message.server in self.client.pl.keys():
                pl = self.client.pl[message.server]
                pl.stop()


            else:
                await self.client.send_message(message.channel, "No song is currently playing.")

def setup(bot):
    bot.add_cog(Skip(bot))
    bot.loaded_exts['commands.skip.skip'] = "Skip"
    bot.cmds['skip'] = ["Skip a playing song (if existing)", "m!skip", "manage_channels"]