class Resume():
    comm = True

    def __init__(self, bot):
        self.client = bot

    async def resume(self, command, message):
        if message.author.permissions_in(message.channel).manage_channels:
            if len(command) == 1:
                if message.server in self.client.pl.keys():
                    self.client.pl[message.server].resume()
                    await self.client.send_message(message.channel, "Resumed.")
                else:
                    await self.client.send_message(message.channel, "No song is currently playing.")
            else:
                await self.client.send_message(message.channel, "**Usage: m!resume**")


def setup(bot):
    bot.add_cog(Resume(bot))
    bot.loaded_exts['commands.resume.resume'] = 'Resume'
    bot.cmds['pause'] = ["Resume a paused (if existing) song.", "m!resume", "manage_channels"]