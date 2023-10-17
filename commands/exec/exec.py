import discord

class Exec():
    comm = True
    def __init__(self, bot):
        self.client = bot
    async def exec(self, command, message):
        print("Attempted exec from " + message.author.name)
        if message.author.id in self.client.dev:
            print("Received an exec from " + message.author.name)
            fornow = command
            fornow.pop(0)
            fornows = ""
            for i in fornow:
                fornows = fornows + i + " "
            fornows = fornows[:-1]
            try:
                exec(fornows)
            except Exception as e:
                await self.client.send_message(message.channel, str(e))

def setup(bot):
    bot.add_cog(Exec(bot))
    bot.loaded_exts["commands.exec.exec"] = "Exec"