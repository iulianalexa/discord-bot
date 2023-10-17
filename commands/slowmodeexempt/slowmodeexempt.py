import sqlite3

warndb = sqlite3.connect("warnings.db")
warncur = warndb.cursor()
sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()

class SlowmodeExempt():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def slowmodeexempt(self, command, message):
        if message.author.permissions_in(message.channel).manage_server:
            if len(command) == 2:
                if message.role_mentions is not None or command[1].lower() == "none":
                    if command[1].lower() == "none":
                        sinfocur.execute("UPDATE filter SET eslowmode = 'none' WHERE server = ?",
                                         [message.server.id])
                        sinfodb.commit()
                        self.client.eslowmode[message.server.id] = "none"
                    else:
                        sinfocur.execute("UPDATE filter SET eslowmode = ? WHERE server = ?",
                                         [message.role_mentions[0].id, message.server.id])
                        sinfodb.commit()
                        self.client.eslowmode[message.server.id] = message.role_mentions[0].id
                    await self.client.send_message(message.channel, "**Done!**")
                else:
                    await self.client.send_message(message.channel, "**Usage m!slowmodeexempt @role**")
            else:
                await self.client.send_message(message.channel, "**Usage m!slowmodeexempt @role**")


def setup(bot):
    bot.cmds['slowmodeexempt'] = ["Mention a role that will be exempt to all slowmode regulations.",
                                  "m!slowmodeexempt @role", "manage_server"]
    bot.add_cog(SlowmodeExempt(bot))
    bot.loaded_exts['commands.slowmodeexempt.slowmodeexempt'] = 'SlowmodeExempt'

