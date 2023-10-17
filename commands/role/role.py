import discord
import asyncio

class Role():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def role(self, command, message):
        self.client.loop.create_task(self.role_bk(command, message))

    async def role_bk(self, command, message):
        fornow = command
        fornow.pop(0)
        fornows = ""
        for i in fornow:
            fornows = i + " "
        fornows = fornows[:-1]
        role = discord.utils.get(message.server.role_hierarchy, name=fornows)
        if role is not None and role.id in self.client.croles[message.server.id].keys():
            corr = []
            for i in self.client.croles[message.server.id][role.id]:
                crol = discord.utils.get(message.server.role_hierarchy, id=i)
                if crol is not None:
                    corr.append(crol)
            corr.append(role)
            msg = await self.client.send_message(message.channel, "<a:loading:393852367751086090>")
            for i in corr:
                if i not in message.author.roles:

                    try:
                        await self.client.add_roles(message.author, i)
                        await asyncio.sleep(.2)
                    except discord.Forbidden:
                        await self.client.send_message(message.channel, ":x: **I don't have permissions!**")
                        return
            await self.client.edit_message(msg, "**Done!**")
        else:
            await self.client.send_message(message.channel, "**Usage: m!role rolename**")

def setup(bot):
    bot.add_cog(Role(bot))
    bot.loaded_exts['commands.role.role'] = 'Role'
    bot.cmds['role'] = ["Claim a role that exists in the claimable role database.", "m!role rolename", None]