import sqlite3

warndb = sqlite3.connect("warnings.db")
warncur = warndb.cursor()
sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()

class MaxWarns():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def maxwarns(self, command, message):
        if message.author.permissions_in(message.channel).manage_server:
            if len(command) == 2:

                try:

                    maxwarn = int(command[1])
                    if maxwarn < 1:
                        raise ValueError
                except ValueError:
                    await self.client.send_message(message.channel, "**Usage: m!maxwarns [number]**")
                    return
                sinfocur.execute("UPDATE maxwarn SET maxint = ? WHERE server = ?", [maxwarn, message.server.id])
                sinfodb.commit()
                await self.client.send_message(message.channel, "**Done!**")
            else:
                await self.client.send_message(message.channel, "**Usage: m!maxwarns [number]**")


def setup(bot):
    bot.cmds['maxwarns'] = ["Changes the maximum amount of warnings before the user is being banned.",
                            "m!maxwarns [number]", "manage_server"]
    bot.add_cog(MaxWarns(bot))
    bot.loaded_exts['commands.maxwarns.maxwarns'] = 'MaxWarns'
