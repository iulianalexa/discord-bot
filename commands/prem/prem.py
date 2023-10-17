import time
import sqlite3

sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()

class Prem():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def prem(self, command, message):
        if message.author.id in self.client.dev:
            if len(command) == 3:
                serv = command[1]
                dur = 0
                try:
                    dur = int(command[2])
                except ValueError:
                    return
            elif len(command) == 2:
                serv = command[1]
                dur = 2592000
            elif len(command) == 1:
                serv = message.server.id
                dur = 2592000
            else:
                return
            timenow = time.time()
            when = timenow + dur
            when = when
            sinfocur.execute("DELETE FROM premium WHERE server = ?", [serv])
            sinfocur.execute("INSERT INTO premium (server, start, expire) VALUES (?, ?, ?)", [serv, timenow, when])
            sinfodb.commit()
            await self.client.send_message(message.channel, "**Changed.**")


def setup(bot):
    bot.add_cog(Prem(bot))
    bot.loaded_exts['commands.prem.prem'] = 'Prem'