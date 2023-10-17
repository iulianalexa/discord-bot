import discord

class Unmute():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def unmute(self, command, message):
        if message.author.permissions_in(message.channel).kick_members:
            if len(command) == 2 and message.mentions:
                if message.author.top_role > message.mentions[0].top_role or (message.author == message.server.owner and message.author != message.mentions[0]):
                    try:
                        if self.client.mute[message.server.id] is None:
                            self.client.mute[message.server.id] = discord.utils.get(message.server.role_hierarchy,
                                                                               name="m-mute")
                            if self.client.mute[message.server.id] is None:
                                self.client.mute[message.server.id] = await self.client.create_role(message.server,
                                                                                          name="m-mute",
                                                                                          permissions=discord.Permissions.none())
                            else:
                                await self.client.edit_role(message.server, self.client.mute[message.server.id],
                                                       name="m-mute",
                                                       permissions=discord.Permissions.none())
                            overwrite = discord.PermissionOverwrite(send_messages=False)
                            channelsnow = message.server.channels
                            for j in channelsnow:
                                if j.overwrites_for(self.client.mute[message.server.id]) != overwrite:
                                    await self.client.edit_channel_permissions(j, self.client.mute[message.server.id],
                                                                          overwrite=overwrite)
                        if message.server.id in self.client.mute:
                            await self.client.remove_roles(message.mentions[0], self.client.mute[message.server.id])

                            await self.client.server_voice_state(message.mentions[0], mute=False)

                            await self.client.send_message(message.channel, ":loud_sound: **Unmuted user "
                                                      + message.mentions[0].mention + ".**")

                    except discord.Forbidden:
                        await self.client.send_message(message.channel, ":x: **I don't have permissions!**")
                else:
                    await self.client.send_message("**Don't even try.**")
            else:
                await self.client.send_message(message.channel, "**Usage: m!unmute @member**")


def setup(bot):
    bot.cmds['unmute'] = ["Unmutes a user.", "m!unmute @user", "kick_members"]

    bot.add_cog(Unmute(bot))
    bot.loaded_exts['commands.unmute.unmute'] = 'Unmute'

