import sqlite3

warndb = sqlite3.connect("warnings.db")
warncur = warndb.cursor()
sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()

class AntiadExempt():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def antiadexempt(self, command, message):
        if message.author.permissions_in(message.channel).manage_server:
            if len(command) == 2:
                if message.role_mentions is not None or command[1].lower() == "none":
                    if command[1].lower() == "none":
                        sinfocur.execute("UPDATE filter SET einvite = 'none' WHERE server = ?",
                                         [message.server.id])
                        sinfodb.commit()
                        self.client.einvite[message.server.id] = "none"
                    else:
                        sinfocur.execute("UPDATE filter SET einvite = ? WHERE server = ?",
                                         [message.role_mentions[0].id, message.server.id])
                        sinfodb.commit()
                        self.client.einvite[message.server.id] = message.role_mentions[0].id
                    await self.client.send_message(message.channel, "**Done!**")
                else:
                    await self.client.send_message(message.channel, "**Usage m!antiadexempt @role**")
            else:
                await self.client.send_message(message.channel, "**Usage m!antiadexempt @role**")


def setup(bot):
    bot.cmds['antiadexempt'] = ["Mention a role that will be exempt to all antiadvertising regulations.",
                                "m!antiadexempt @role", "manage_server"]
    bot.add_cog(AntiadExempt(bot))
    bot.loaded_exts['commands.antiadexempt.antiadexempt'] = 'AntiadExempt'

