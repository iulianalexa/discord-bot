import discord

class ListCC():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def listcc(self, command, message):
        nc = False
        st = ""
        for i in self.client.cc[message.server].keys():
            st = st + i + ", "
        if st == "":
            nc = True
        if not nc:
            st = st[:-2]
            try:
                await self.client.send_message(message.author, st)
                await self.client.send_message(message.channel, "**I've sent you a DM!**")
            except discord.Forbidden:
                await self.client.send_message(message.channel, "**I tried to send you a DM but I couldn't.**")
        else:
            await self.client.send_message(message.channel, "**There are no custom commands on this server.**")

def setup(bot):
    bot.add_cog(ListCC(bot))
    bot.loaded_exts['commands.listcc.listcc'] = "ListCC"
    bot.cmds['listcc'] = ["List all custom commands.", "m!listcc", None]