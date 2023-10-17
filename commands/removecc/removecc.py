import sqlite3

ccdb = sqlite3.connect("cc.db")
cccur = ccdb.cursor()

class RemoveCC():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def removecc(self, command, message):
        if message.author.permissions_in(message.channel).manage_server:
            if len(command) == 2:
                dbserv = "server" + message.server.id
                cmd = command[1]
                cccur.execute("SELECT * FROM " + dbserv + " WHERE command = ?", [cmd])
                if len(cccur.fetchall()) >= 1:
                    cccur.execute("DELETE FROM " + dbserv + " WHERE command = ?", [cmd])
                    ccdb.commit()
                    self.client.cc[message.server].pop(cmd)
                    await self.client.send_message(message.channel, "**Done!**")
                else:
                    await self.client.send_message(message.channel, "**This command does not exist.**")
            else:
                await self.client.send_message(message.channel, "**Usage: m!removecc [command]")

def setup(bot):
    bot.add_cog(RemoveCC(bot))
    bot.loaded_exts['commands.removecc.removecc'] = "RemoveCC"
    bot.cmds['removecc'] = ["Remove a custom command.", "m!removecc [command]", "manage_server"]
