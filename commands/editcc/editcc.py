import sqlite3

ccdb = sqlite3.connect("cc.db")
cccur = ccdb.cursor()

class EditCC():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def editcc(self, command, message):
        if message.author.permissions_in(message.channel).manage_server:
            if len(command) >= 3:
                dbserv = "server" + message.server.id
                cmd = command[1]
                cccur.execute("SELECT * FROM " + dbserv + " WHERE command = ?", [cmd])
                if len(cccur.fetchall()) >= 1:
                    fornow = command[2:]
                    fornow2 = ""
                    for i in fornow:
                        fornow2 = fornow2 + i + " "
                    fornow2 = fornow2[:-1]
                    cccur.execute("UPDATE " + dbserv + " SET output = ? WHERE command = ?", [fornow2, cmd])
                    ccdb.commit()
                    self.client.cc[message.server][cmd] = fornow2
                    await self.client.send_message(message.channel, "**Done!**")
                else:
                    await self.client.send_message(message.channel, "**The command does not exist.**")

            else:
                await self.client.send_message(message.channel, "**Usage: m!editcc [command] [new output]")

def setup(bot):
    bot.add_cog(EditCC(bot))
    bot.loaded_exts['commands.editcc.editcc'] = "EditCC"
    bot.cmds['editcc'] = ["Edit a custom command.", "m!editcc [command] [new output]", "manage_server"]