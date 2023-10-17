import sqlite3

sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()

class DelPrem():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def delprem(self, command, message):
        if len(command) == 2 and message.author.id in self.client.dev:
            serv = command[1]
            sinfocur.execute("DELETE FROM premium WHERE server = ?", [serv])
            sinfodb.commit()

def setup(bot):
    bot.add_cog(DelPrem(bot))
    bot.loaded_exts['commands.delprem.delprem'] = 'DelPrem'