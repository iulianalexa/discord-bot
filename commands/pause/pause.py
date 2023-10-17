class Pause():
    comm = True

    def __init__(self, bot):
        self.client = bot

    async def pause(self, command, message):
        if message.author.permissions_in(message.channel).manage_channels:
            if len(command) == 1:
                if message.server in self.client.pl.keys():
                    self.client.pl[message.server].pause()
                    await self.client.send_message(message.channel, "Paused.")
                else:
                    await self.client.send_message(message.channel, "No song is currently playing.")
            else:
                await self.client.send_message(message.channel, "**Usage: m!pause**")

def setup(bot):
    bot.add_cog(Pause(bot))
    bot.loaded_exts['commands.pause.pause'] = 'Pause'
    bot.cmds['pause'] = ["Pause a playing (if existing) song.", "m!pause", "manage_channels"]