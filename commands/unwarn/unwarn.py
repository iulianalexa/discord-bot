import sqlite3

warndb = sqlite3.connect("warnings.db")
warncur = warndb.cursor()
sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()


class Unwarn():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def unwarn(self, command, message):
        if message.author.permissions_in(message.channel).ban_members:
            if len(command) == 3 and message.mentions and message.mentions[0].mention == command[1]:
                if message.author.top_role > message.mentions[0].top_role or (message.author == message.server.owner and message.author != message.mentions[0]):
                    if message.server.me.permissions_in(message.channel).ban_members:
                        try:
                            warnid = int(command[2])
                        except ValueError:
                            await self.client.send_message(message.channel, "**Usage: m!unwarn @member [warnid]**")
                            return
                        if warnid < 1:
                            await self.client.send_message(message.channel, "**Usage: m!unwarn @member [warnid]**")
                            return

                        fornow = await self.client.get_cog("UnwarnSys").unwarn_sys\
                            (message.server, message.mentions[0], warnid)

                        if fornow is True:
                            await self.client.send_message(message.channel, "**Removed one warning from " +
                                                      message.mentions[0].mention + ".**")
                        elif fornow is False:
                            await self.client.send_message(message.channel, "**This warning does not belong to the "
                                                                       "user.**")
                    else:
                        await self.client.send_message(message.channel, ":x: **I don't have permissions!**")
                else:
                    await self.client.send_message(message.channel, "**Don't even try.**")
            else:
                await self.client.send_message(message.channel, "**Usage: m!unwarn @member [warnid]**")


def setup(bot):
    bot.cmds['unwarn'] = ["Unwarns a user.", "m!unwarn @user", "ban_members"]
    bot.add_cog(Unwarn(bot))
    bot.loaded_exts['commands.unwarn.unwarn'] = 'Unwarn'
