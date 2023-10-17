import sqlite3

warndb = sqlite3.connect("warnings.db")
warncur = warndb.cursor()
sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()


class AnticapsExempt():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def anticapsexempt(self, command, message):
        if message.author.permissions_in(message.channel).manage_server:
            if len(command) == 2:
                if message.role_mentions is not None or command[1].lower() == "none":
                    if command[1].lower() == "none":
                        sinfocur.execute("UPDATE filter SET ecaps = 'none' WHERE server = ?",
                                         [message.server.id])
                        sinfodb.commit()
                        self.client.ecaps[message.server.id] = "none"
                    else:
                        sinfocur.execute("UPDATE filter SET ecaps = ? WHERE server = ?",
                                         [message.role_mentions[0].id, message.server.id])
                        sinfodb.commit()
                        self.client.ecaps[message.server.id] = message.role_mentions[0].id
                    await self.client.send_message(message.channel, "**Done!**")
                else:
                    await self.client.send_message(message.channel, "**Usage m!anticapsexempt @role")
            else:
                await self.client.send_message(message.channel, "**Usage m!anticapsexempt @role")


def setup(bot):
    bot.cmds['anticapsexempt'] = ["Mention a role that will be exempt to all anticaps regulations.",
                                  "m!anticapsexempt @role", "manage_server"]

    bot.add_cog(AnticapsExempt(bot))
    bot.loaded_exts['commands.anticapsexempt.anticapsexempt'] = 'AnticapsExempt'

