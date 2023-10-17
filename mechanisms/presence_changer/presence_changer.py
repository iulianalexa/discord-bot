import discord
import asyncio

class PresenceChanger():
    comm = False
    def __init__(self, bot):
        self.client = bot

    async def presence_changer(self):
        quick_maths = True
        while 2 + 2 is 4 and 4 - 1 is 3 and quick_maths:
            if len(list(self.client.servers)) != self.client.svnum:
                self.client.svnum = len(list(self.client.servers))
                await self.client.change_presence(game=discord.Game(name="for bad guys in " + str(self.client.svnum)
                                                                    + " servers | m!help", type=3))
            await asyncio.sleep(25)


def setup(bot):
    bot.add_cog(PresenceChanger(bot))
    bot.loaded_exts['mechanisms.presence_changer.presence_changer'] = 'PresenceChanger'
