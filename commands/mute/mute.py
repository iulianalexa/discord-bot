import discord

class Mute():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def mute(self, command, message):
        if message.author.permissions_in(message.channel).kick_members:
            if len(command) == 2 and message.mentions:
                if (message.author.top_role > message.mentions[0].top_role or (message.author == message.server.owner and message.author != message.mentions[0])) and message.mentions[0] != message.server.me:
                    try:
                        if self.client.mute[message.server.id] is None or self.client.mute[message.server.id] not in \
                                message.server.role_hierarchy:
                            self.client.mute[message.server.id] = discord.utils.get(message.server.role_hierarchy,
                                                                               name="m-mute")
                            if self.client.mute[message.server.id] is None:
                                self.client.mute[message.server.id] = await self.client.create_role(message.server,
                                                                                          name="m-mute",
                                                                                          permissions=discord.Permissions.none())
                            elif self.client.mute[message.server.id].permissions != discord.Permissions.none():
                                await self.client.edit_role(message.server, self.client.mute[message.server.id],
                                                       name="m-mute",
                                                       permissions=discord.Permissions.none())
                            overwrite = discord.PermissionOverwrite(send_messages=False)
                            channelsnow = message.server.channels
                            for j in channelsnow:
                                if j.overwrites_for(self.client.mute[message.server.id]).pair() != overwrite.pair():
                                    await self.client.edit_channel_permissions(j, self.client.mute[message.server.id],
                                                                          overwrite=overwrite)
                        if message.server.id in self.client.mute:
                            await self.client.add_roles(message.mentions[0], self.client.mute[message.server.id])
                            await self.client.send_message(message.channel, ":mute: **Muted user " +
                                                      message.mentions[0].mention + ".**")
                            await self.client.server_voice_state(message.mentions[0], mute=True)
                    except discord.Forbidden:
                        await self.client.send_message(message.channel,
                                                  ":x: **I don't have permissions!**")
                else:
                    await self.client.send_message(message.channel, "**Don't even try.**")
            else:
                await self.client.send_message(message.channel, "**Usage: m!mute @member**")


def setup(bot):
    bot.cmds['mute'] = ["Mutes a user.", "m!mute @user", "kick_members"]
    bot.add_cog(Mute(bot))
    bot.loaded_exts['commands.mute.mute'] = 'Mute'
