import discord
import sqlite3

warndb = sqlite3.connect("warnings.db")
warncur = warndb.cursor()
sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()

class CommandHandler():
    def __init__(self, bot):
        self.client = bot

    async def handler(self, message, command):
        if "commands." + command[0] + "." + command[0] in list(self.client.loaded_exts.keys()):
            modl = self.client.get_cog(self.client.loaded_exts["commands." + command[0] + "." + command[0]])
            if modl.comm is True:
                await getattr(modl, command[0])(command, message)
        elif command[0] in self.client.cc[message.server].keys():
            await self.client.send_message(message.channel, self.client.cc[message.server][command[0]])


def setup(bot):
    bot.add_cog(CommandHandler(bot))