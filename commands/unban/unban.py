import discord

class Unban():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def unban(self, command, message):
        if message.author.permissions_in(message.channel).ban_members:
            bans = await self.client.get_bans(message.server)
            if len(command) >= 3:
                if command[1] == "name" or command[1] == "id":
                    if command[1] == "name":
                        fornow = ""
                        fornow2 = command
                        fornow2.pop(0)
                        fornow2.pop(0)
                        for i in fornow2:
                            fornow = fornow + i + " "
                        fornow = fornow[:-1]
                        if '#' in fornow:
                            try:
                                a, b = fornow.split('#')
                                try:
                                    await self.client.unban(message.server, discord.utils.get(bans, name=a,
                                                                                         discriminator=b))
                                    await self.client.send_message(message.channel, ":hammer: **Unbanned user.**")
                                except discord.Forbidden:
                                    await self.client.send_message(message.channel,
                                                              ":x: **I don't have permissions!**")

                            except ValueError:
                                await self.client.send_message(message.channel,
                                                          "**Usage: m!unban name [name#discriminator]**")
                            except discord.HTTPException:
                                await self.client.send_message(message.channel,
                                                          "**The user is not banned!**")
                        else:
                            await self.client.send_message(message.channel, "**Usage: m!unban name "
                                                                       "[name#discriminator]**")
                    elif command[1] == "id":
                        if len(command) == 3:
                            try:
                                await self.client.unban(message.server, discord.utils.get(bans, id=command[2]))
                                await self.client.send_message(message.channel, ":hammer: **Unbanned user.**")
                            except discord.Forbidden:
                                await self.client.send_message(message.channel,
                                                          ":x: **I don't have permissions!**")
                            except discord.HTTPException:
                                await self.client.send_message(message.channel,
                                                          "**The user is not banned!**")
                        else:
                            await self.client.send_message(message.channel, "**Usage: m!unban id [userid]**")
                else:
                    await self.client.send_message(message.channel, "**Usage: m!unban [name/id] [user]**")
            else:
                await self.client.send_message(message.channel, "**Usage: m!unban [name/id] [user]**")


def setup(bot):
    bot.cmds['unban'] = ["Unbans a user.", "m!unban [name/id] [user]", "ban_members"]
    bot.add_cog(Unban(bot))
    bot.loaded_exts['commands.unban.unban'] = 'Unban'

