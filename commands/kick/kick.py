import discord

class Kick():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def kick(self, command, message):
        if message.author.permissions_in(message.channel).kick_members:
            if len(command) == 2 and message.mentions and command[1] == message.mentions[0].mention:
                if message.author.top_role > message.mentions[0].top_role or (message.author == message.server.owner and message.author != message.mentions[0]):
                    try:
                        await self.client.kick(message.mentions[0])
                        await self.client.send_message(message.channel, ":boot: **Kicked " +
                                            message.mentions[0].mention + ".**")
                    except discord.Forbidden:
                        await self.client.send_message(message.channel,
                                            ":x: **I don't have permissions!**")
                else:
                    await self.client.send_message(message.channel, "**Don't even try.**")
            else:
                await self.client.send_message(message.channel, "**Usage: m!kick @member**")


def setup(bot):
    bot.cmds['kick'] = ["Kicks a user.", "m!kick @user", "kick_members"]
    bot.add_cog(Kick(bot))
    bot.loaded_exts['commands.kick.kick'] = 'Kick'

