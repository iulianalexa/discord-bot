class VoteSkip():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def voteskip(self, command, message):
        if message.server in self.client.vs:
            if message.author.voice.voice_channel:
                if message.author not in self.client.voters[message.server]:
                    self.client.vs[message.server] += 1
                    self.client.voters[message.server].append(message.author)
                    humans = [x for x in message.author.voice.voice_channel.voice_members if not x.bot]
                    if len(humans) == 1 and self.client.vs[message.server] == 1:
                        pl = self.client.pl[message.server]
                        pl.stop()
                        await self.client.send_message(message.channel, "Skipping song...")
                        return
                    elif len(humans) > 1 and self.client.vs[message.server] == \
                        int(len(humans)/2) + 1:
                        pl = self.client.pl[message.server]
                        pl.stop()
                        await self.client.send_message(message.channel, "Skipping song...")
                        return
                    await self.client.send_message(message.channel, "You voted! " + str(self.client.vs[message.server]) + "/" +
                                                   str(int(len(humans)/2) + 1))
                else:
                    await self.client.send_message(message.channel, "You already voted.")
            else:
                await self.client.send_message(message.channel, "You are not in a voice channel.")
        else:
            await self.client.send_message(message.channel, "No song is playing.")

def setup(bot):
    bot.add_cog(VoteSkip(bot))
    bot.loaded_exts['commands.voteskip.voteskip'] = 'VoteSkip'
    bot.cmds['voteskip'] = ["Vote to skip the currently playing (if existing) song.", "m!voteskip", None]