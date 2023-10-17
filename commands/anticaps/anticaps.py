import sqlite3

warndb = sqlite3.connect("warnings.db")
warncur = warndb.cursor()
sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()

class Anticaps():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def anticaps(self, command, message):
        if message.author.permissions_in(message.channel).manage_server:
            if len(command) == 2:
                if command[1] == "on":
                    sinfocur.execute("UPDATE filter SET caps = 'true' WHERE server = ?", [message.server.id])
                    sinfodb.commit()
                    await self.client.send_message(message.channel, "**Anti-Caps is now on.**")
                    if message.server.id not in self.client.caps:
                        self.client.caps.append(message.server.id)
                elif command[1] == "off":
                    sinfocur.execute("UPDATE filter SET caps = 'false' WHERE server = ?", [message.server.id])
                    sinfodb.commit()
                    await self.client.send_message(message.channel, "**Anti-Caps is now off.**")
                    if message.server.id in self.client.caps:
                        self.client.caps.pop(self.client.caps.index(message.server.id))
                else:
                    await self.client.send_message(message.channel, "**Usage m!anticaps [on/off]")
            else:
                await self.client.send_message(message.channel, "**Usage m!anticaps [on/off]")


def setup(bot):
    bot.cmds['anticaps'] = ["Toggles anticaps on/off.", "m!anticaps [on/off]", "manage_server"]
    bot.add_cog(Anticaps(bot))
    bot.loaded_exts['commands.anticaps.anticaps'] = 'Anticaps'
