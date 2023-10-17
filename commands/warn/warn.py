import sqlite3

warndb = sqlite3.connect("warnings.db")
warncur = warndb.cursor()
sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()

class Warn():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def warn(self, command, message):
        if message.author.permissions_in(message.channel).ban_members:
            if len(command) == 2 and message.mentions:
                if (message.author.top_role > message.mentions[0].top_role or (message.author == message.server.owner and message.author != message.mentions[0])) and message.mentions[0] != message.server.me:
                    if message.server.me.permissions_in(message.channel).ban_members:
                        await self.client.get_cog("WarnSys").warn_sys(message.server, message.mentions[0])
                        await self.client.send_message(message.channel, "**Warned user " + message.mentions[0].mention
                                                  + ".**")
                    else:
                        await self.client.send_message(message.channel, ":x: **I don't have permissions!**")
                else:
                    await self.client.send_message(message.channel, "**Don't even try.**")
            else:
                await self.client.send_message(message.channel, "**Usage: m!warn @member**")

def setup(bot):
    bot.cmds['warn'] = ["Warns a user.", "m!warn @user", "ban_members"]
    bot.add_cog(Warn(bot))
    bot.loaded_exts['commands.warn.warn'] = 'Warn'