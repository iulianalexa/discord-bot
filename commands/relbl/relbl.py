import os

class RelBl():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def relbl(self, command, message):
        if message.author.id in self.client.dev:
            if os.path.isfile("blacklist.txt"):
                f = open("blacklist.txt", "r")
                self.client.blacklisted = [x.strip() for x in f.readlines()]
                f.close()
            servers = list(self.client.servers)
            for i in servers:
                if i.id in self.client.blacklisted:
                    await self.client.leave_server(i)


def setup(bot):
    bot.add_cog(RelBl(bot))
    bot.loaded_exts['commands.relbl.relbl'] = 'RelBl'
