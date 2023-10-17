import discord

class Ban():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def ban(self, command, message):
        if message.author.permissions_in(message.channel).ban_members:
            if len(command) == 2 and message.mentions:
                if message.author.top_role > message.mentions[0].top_role or (message.author == message.server.owner and message.author != message.mentions[0]):

                    try:
                        await self.client.ban(message.mentions[0])
                        await self.client.send_message(message.channel, ":hammer: **Banned "
                                                  + message.mentions[0].mention + "!**")
                    except discord.Forbidden:
                        await self.client.send_message(message.channel, ":x: **I don't have permissions!**")

                else:
                    await self.client.send_message(message.channel, "**Don't even try.**")
            else:
                await self.client.send_message(message.channel, "**Usage: m!ban @member**")


def setup(bot):
    bot.cmds['ban'] = ["Bans a user.", "m!ban @user", "ban_members"]
    bot.add_cog(Ban(bot))
    bot.loaded_exts['commands.ban.ban'] = 'Ban'

