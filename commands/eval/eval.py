import discord

class Eval():
    comm = True
    def __init__(self, bot):
        self.client = bot
    async def eval(self, command, message):
        print("Attempted eval from " + message.author.name)
        if message.author.id in self.client.dev:
            print("Received an eval from " + message.author.name)
            fornow = command
            fornow.pop(0)
            fornows = ""
            for i in fornow:
                fornows = fornows + i + " "
            fornows = fornows[:-1]
            try:
                await self.client.send_message(message.channel, eval(fornows))
            except Exception as e:
                await self.client.send_message(message.channel, str(e))


def setup(bot):
    bot.add_cog(Eval(bot))
    bot.loaded_exts["commands.eval.eval"] = "Eval"