import sqlite3

warndb = sqlite3.connect("warnings.db")
warncur = warndb.cursor()
sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()

class Warns():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def warns(self, command, message):
        if len(command) == 1:
            servdb = "server" + message.server.id
            warncur.execute("SELECT rowid, * FROM " + servdb + " WHERE userid = ?",
                            [message.author.id])
            fornow = warncur.fetchall()
            warnlist = ""
            if fornow:
                for i in fornow:
                    warnlist = warnlist + "ID: " + str(i[0]) + " | Warned on: " + i[1] + " | Expires on: " \
                               + i[3] + "\n"

            else:
                warnlist = "None"
            warnlist = "```" + warnlist + "```"

            await self.client.send_message(message.channel, "**Here are all the warns for this user:**\n" +
                                      warnlist)
        elif len(command) == 2 and message.mentions:
            if message.author.permissions_in(message.channel).ban_members:
                servdb = "server" + message.server.id
                warncur.execute("SELECT rowid, * FROM " + servdb + " WHERE userid = ?",
                                [message.mentions[0].id])
                fornow = warncur.fetchall()
                warnlist = ""
                if fornow:
                    for i in fornow:
                        warnlist = warnlist + "ID: " + str(i[0]) + " | Warned on: " + i[1] + " | Expires on: " \
                                   + i[3] + "\n"

                else:
                    warnlist = "None"
                warnlist = "```" + warnlist + "```"

                await self.client.send_message(message.channel, "**Here are all the warns for this user:**\n" +
                                          warnlist)


        else:
            await self.client.send_message(message.channel, "**Usage: m!warns {@member}**")

def setup(bot):

    bot.cmds['warns'] = ["Checks your (or someone else's if you have permissions) warns.", "m!warns", None]
    bot.add_cog(Warns(bot))
    bot.loaded_exts['commands.warns.warns'] = 'Warns'