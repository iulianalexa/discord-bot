import sqlite3
import time

sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()

class IsPremium():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def ispremium(self, command, message):
        if message.author.permissions_in(message.channel).manage_server:
            timenow = time.time()
            sinfocur.execute("SELECT * FROM premium WHERE server = ? AND start < ? AND expire > ?",
                             [message.server.id, timenow, timenow])
            if sinfocur.fetchone():
                await self.client.send_message(message.channel, "This server is premium.")
            else:
                await self.client.send_message(message.channel, "This server is not premium.")

def setup(bot):
    bot.add_cog(IsPremium(bot))
    bot.loaded_exts['commands.ispremium.ispremium'] = 'IsPremium'
    bot.cmds['ispremium'] = ["Check if your server is premium.", "m!ispremium", "manage_server"]