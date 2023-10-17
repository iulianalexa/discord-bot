import sqlite3

warndb = sqlite3.connect("warnings.db")
warncur = warndb.cursor()
sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()

class AnticapsRatio():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def anticapsratio(self, command, message):
        if message.author.permissions_in(message.channel).manage_server:
            if len(command) == 2:
                try:
                    fornow = float(command[1])
                    if fornow <= 0 or fornow > 1:
                        raise ValueError
                except ValueError:
                    await self.client.send_message(message.channel, "**Usage m!anticapsratio [ratio]")
                    return
                sinfocur.execute("UPDATE filter SET ocaps = ? WHERE server = ?",
                                 [str(fornow), message.server.id])
                sinfodb.commit()
                self.client.ocaps[message.server.id] = str(fornow)
                await self.client.send_message(message.channel, "**Done!**")
            else:
                await self.client.send_message(message.channel, "**Usage m!anticapsratio [ratio]")


def setup(bot):
    bot.cmds['anticapsratio'] = ["Changes the tolerance for caps messages, 0 being intolerance to non-caps messages, "
                      "1 being intolerance to full-caps messages (default: 1)", "m!anticapsratio [ratio]",
                      "manage_server"]
    bot.add_cog(AnticapsRatio(bot))
    bot.loaded_exts['commands.anticapsratio.anticapsratio'] = 'AnticapsRatio'
