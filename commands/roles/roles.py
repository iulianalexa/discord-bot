import discord

class Roles():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def roles(self, command, message):
        if len(command) == 1:
            fs = "ID | Rolename | Correlations\n"
            rids = list(self.client.rids[message.server.id].keys())
            for i in rids:
                role = discord.utils.get(message.server.role_hierarchy, id=i)
                if role is None:
                    continue
                rid = self.client.rids[message.server.id][role.id]
                corr = []
                for j in self.client.croles[message.server.id][role.id]:
                    cr = discord.utils.get(message.server.role_hierarchy, id=j)
                    if cr is not None:
                        corr.append(cr.name)
                corrs = ""
                for i in corr:
                    corrs = corrs + i + ", "
                corrs = corrs[:-2]
                fs = fs + rid + " | " + role.name + " | " + corrs + "\n"
            fc = []
            while fs:
                fc.append("```" + fs[:1993] + "```")
                fs = fs[1993:]
            for i in fc:
                await self.client.send_message(message.channel, i)

        else:
            await self.client.send_message("**Usage: m!roles**")

def setup(bot):
    bot.add_cog(Roles(bot))
    bot.loaded_exts['commands.roles.roles'] = 'Roles'
    bot.cmds['roles'] = ["Display all the roles in the database.", "m!roles", None]