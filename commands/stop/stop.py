import queue

class Stop():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def stop(self, command, message):
        if message.author.permissions_in(message.channel).manage_channels:
            if message.server in self.client.pl.keys():
                pl = self.client.pl[message.server]
                self.client.q[message.server] = queue.Queue()
                pl.stop()
            else:
                await self.client.send_message(message.channel, "No song is currently playing.")


def setup(bot):
    bot.add_cog(Stop(bot))
    bot.loaded_exts['commands.stop.stop'] = 'Stop'
    bot.cmds['stop'] = ["Stop the currently (if existing) playing song.", "m!stop", "manage_channels"]