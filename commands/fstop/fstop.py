import sys

class Fstop():
    comm = True

    def __init__(self, bot):
        self.client = bot

    async def fstop(self, command, message):
        if message.author.id in self.client.dev:
            sys.exit(1)

def setup(bot):
    bot.add_cog(Fstop(bot))
    bot.loaded_exts['commands.fstop.fstop'] = "Fstop"