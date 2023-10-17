import sqlite3

rolesdb = sqlite3.connect("roles.db")
rolescur = rolesdb.cursor()

class DeleteCorrelations():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def deletecorrelations(self, command, message):
        if message.author.permissions_in(message.channel).manage_server:
            roles = message.role_mentions
            mroles = [x.mention for x in roles]

            if command[1] in mroles and len(message.role_mentions) >= 2 and roles[mroles.index(command[1])].id in \
                    self.client.croles[message.server.id].keys():
                role = roles[mroles.index(command[1])]
                dbserv = "server" + message.server.id
                roles = message.role_mentions
                roles.remove(role)
                for i in roles:
                    if i.id in self.client.croles[message.server.id][role.id]:
                        self.client.croles[message.server.id][role.id].remove(i.id)
                        rolescur.execute("DELETE FROM " + dbserv + " WHERE roleid = ? AND correlationid = ?",
                                         [role.id, i.id])
                        rolesdb.commit()
                await self.client.send_message(message.channel, "**Done!**")
            else:
                await self.client.send_message(message.channel, "**Usage: m!deletecorrelations @role (you can mention"
                                                                " more than a role)**")

def setup(bot):
    bot.add_cog(DeleteCorrelations(bot))
    bot.loaded_exts['commands.deletecorrelations.deletecorrelations'] = "DeleteCorrelations"
    bot.cmds['deletecorrelations'] = ["Delete one or more correlations from a role.", "m!deletecorrelations @role "
                                                                                      "(you can mention more than a r"
                                                                                      "ole)", "manage_server"]