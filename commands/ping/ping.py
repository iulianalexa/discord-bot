import datetime

class Ping():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def ping(self, command, message):

        time = datetime.datetime.now()
        await self.client.get_message(message.channel, message.id)
        time2 = datetime.datetime.now()
        time3 = time2 - time
        time3 = time3.total_seconds() * 1000
        await self.client.send_message(message.channel, "**Pong! " + str(int(time3)) + "ms.**")

def setup(bot):
    bot.add_cog(Ping(bot))
    bot.loaded_exts['commands.ping.ping'] = "Ping"
    bot.cmds['ping'] = ["Ping.", "m!ping", None]
