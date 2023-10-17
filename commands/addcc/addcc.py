import sqlite3

ccdb = sqlite3.connect("cc.db")
cccur = ccdb.cursor()

class AddCC():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def addcc(self, command, message):
        if message.author.permissions_in(message.channel).manage_server:
            if len(command) >= 3:
                dbserv = "server" + message.server.id
                cmd = command[1]
                cccur.execute("SELECT * FROM " + dbserv + " WHERE command = ?", [cmd])
                if len(cccur.fetchall()) == 0:
                    fornow = command
                    fornow.pop(0)
                    fornow.pop(0)
                    fornow2 = ""
                    for i in fornow:
                        fornow2 = fornow2 + i + " "
                    fornow2 = fornow2[:-1]
                    cccur.execute("INSERT INTO " + dbserv + " (command, output) VALUES (?, ?)", [cmd, fornow2])
                    ccdb.commit()
                    self.client.cc[message.server][cmd] = fornow2
                    await self.client.send_message(message.channel, "**Done!**")
                else:
                    await self.client.send_message(message.channel, "**Comanda exista deja.**")
            else:
                await self.client.send_message(message.channel, "**Usage: m!addcc [command] [output]**")

def setup(bot):
    bot.add_cog(AddCC(bot))
    bot.loaded_exts['commands.addcc.addcc'] = "AddCC"
    bot.cmds['addcc'] = ["Create a custom command.", "m!addcc [command] [output]", "manage_server"]
