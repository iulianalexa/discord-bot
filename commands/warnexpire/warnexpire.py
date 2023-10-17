import sqlite3

warndb = sqlite3.connect("warnings.db")
warncur = warndb.cursor()
sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()

class WarnExpire():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def warnexpire(self, command, message):
        if message.author.permissions_in(message.channel).manage_server:
            if len(command) == 2:
                try:
                    days = int(command[1])
                    if days < 0:
                        raise ValueError
                except ValueError:
                    await self.client.send_message(message.channel, "**Usage m!warnexpire [days]**")
                    return
                sinfocur.execute("UPDATE warnexpire SET days = ? WHERE server = ?", [days, message.server.id])
                sinfodb.commit()
                await self.client.send_message(message.channel, "**Done!**")
            else:
                await self.client.send_message(message.channel, "**Usage m!warnexpire [days]**")


def setup(bot):
    bot.cmds['warnexpire'] = ["Changes the amount of days before the warning expires. 0 for never.",
                              "m!warnexpire [0/days]", "manage_server"]
    bot.add_cog(WarnExpire(bot))
    bot.loaded_exts['commands.warnexpire.warnexpire'] = 'WarnExpire'
