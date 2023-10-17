from discord.ext import commands
import sqlite3
import os
import sqlite3

warndb = sqlite3.connect("warnings.db")
warncur = warndb.cursor()
sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()

class Antiad():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def antiad(self, command, message):
        if message.author.permissions_in(message.channel).manage_server:
            if len(command) == 2:
                if command[1] == "on":
                    sinfocur.execute("UPDATE filter SET invite = 'true' WHERE server = ?", [message.server.id])
                    sinfodb.commit()
                    await self.client.send_message(message.channel, "**Antiad is now on.**")
                    if message.server.id not in self.client.invite:
                        self.client.slowmode.append(message.server.id)
                elif command[1] == "off":
                    sinfocur.execute("UPDATE filter SET invite = 'false' WHERE server = ?", [message.server.id])
                    sinfodb.commit()
                    await self.client.send_message(message.channel, "**Antiad is now off.**")
                    if message.server.id in self.client.invite:
                        self.client.invite.pop(self.client.invite.index(message.server.id))
                else:
                    await self.client.send_message(message.channel, "**Usage m!antiad [on/off]**")
            else:
                await self.client.send_message(message.channel, "**Usage m!antiad on/off]**")


def setup(bot):
    bot.cmds['antiad'] = ["Toggles antiadvertising on/off", "m!antiad [on/off]", "manage_server"]
    bot.add_cog(Antiad(bot))
    bot.loaded_exts['commands.antiad.antiad'] = 'Antiad'
