import sqlite3

warndb = sqlite3.connect("warnings.db")
warncur = warndb.cursor()
sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()

class Slowmode():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def slowmode(self, command, message):
        if message.author.permissions_in(message.channel).manage_server:
            if len(command) == 2:
                if command[1] == "on":
                    sinfocur.execute("UPDATE filter SET slowmode = 'true' WHERE server = ?", [message.server.id])
                    sinfodb.commit()
                    await self.client.send_message(message.channel, "**Slowmode is now on.**")
                    if message.server.id not in self.client.slowmode:
                        self.client.slowmode.append(message.server.id)
                elif command[1] == "off":
                    sinfocur.execute("UPDATE filter SET slowmode = 'false' WHERE server = ?", [message.server.id])
                    sinfodb.commit()
                    await self.client.send_message(message.channel, "**Slowmode is now off.**")
                    if message.server.id in self.client.slowmode:
                        self.client.slowmode.pop(self.client.slowmode.index(message.server.id))
                else:
                    await self.client.send_message(message.channel, "**Usage m!slowmode [on/off]**")
            else:
                await self.client.send_message(message.channel, "**Usage m!slowmode [on/off]**")


def setup(bot):
    bot.cmds['slowmode'] = ["Toggles slowmode on/off.", "m!slowmode [on/off]", "manage_server"]
    bot.add_cog(Slowmode(bot))
    bot.loaded_exts['commands.slowmode.slowmode'] = 'Slowmode'

