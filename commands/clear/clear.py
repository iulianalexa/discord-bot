import discord

class Clear():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def clear(self, command, message):
        if message.author.permissions_in(message.channel).manage_messages:
            if len(command) == 2:
                num = command[1]
                try:
                    num = int(num)
                except ValueError:
                    await self.client.send_message(message.channel, "Usage: m!clear [number of messages]")
                    return
                if num < 1 or num > 100:
                    await self.client.send_message(message.channel, "You can only delete 1-100 messages at a time.")
                else:
                    try:
                        await self.client.purge_from(message.channel, limit=num, before=message)
                        await self.client.send_message(message.channel, "Done!")
                    except discord.Forbidden:
                        await self.client.send_message(message.channel, "I do not have permission.")
            else:
                await self.client.send_message(message.channel, "Usage: m!clear [number of messages]")


def setup(bot):
    bot.add_cog(Clear(bot))
    bot.loaded_exts['commands.clear.clear'] = 'Clear'
    bot.cmds['clear'] = ["Clear messages from a channel.", "m!clear [number of messages]", "manage_messages"]