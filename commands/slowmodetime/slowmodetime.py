import sqlite3

warndb = sqlite3.connect("warnings.db")
warncur = warndb.cursor()
sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()

class SlowmodeTime():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def slowmodetime(self, command, message):
        if message.author.permissions_in(message.channel).manage_server:
            if len(command) == 2:
                try:
                    fornow = float(command[1])
                    if fornow <= 0:
                        raise ValueError
                except ValueError:
                    await self.client.send_message(message.channel, "**Usage m!slowmodetime [seconds]**")
                    return
                sinfocur.execute("UPDATE filter SET oslowmode = ? WHERE server = ?",
                                 [str(fornow), message.server.id])
                sinfodb.commit()
                self.client.oslowmode[message.server.id] = str(fornow)
                await self.client.send_message(message.channel, "**Done!**")
            else:
                await self.client.send_message(message.channel, "**Usage m!slowmodetime [seconds]**")


def setup(bot):
    bot.cmds['slowmodetime'] = ["Changes the time between messages.", "m!slowmodetime [seconds]", "manage_server"]
    bot.add_cog(SlowmodeTime(bot))
    bot.loaded_exts['commands.slowmodetime.slowmodetime'] = 'SlowmodeTime'

