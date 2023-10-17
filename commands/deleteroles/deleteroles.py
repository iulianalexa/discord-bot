import sqlite3

rolesdb = sqlite3.connect("roles.db")
rolescur = rolesdb.cursor()

class DeleteRoles():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def deleteroles(self, command, message):
        if message.author.permissions_in(message.channel).manage_server:
            if len(message.role_mentions) >= 1:
                dbserv = "server" + message.server.id
                for i in message.role_mentions:
                    if i.id in self.client.croles[message.server.id].keys():
                        self.client.croles[message.server.id].pop(i.id)
                    if i.id in self.client.rids[message.server.id].keys():
                        self.client.rids[message.server.id].pop(i.id)
                    rolescur.execute("DELETE FROM " + dbserv + " WHERE roleid = ?", [i.id])
                    rolesdb.commit()
                await self.client.send_message(message.channel, "**Done!**")
            else:
                await self.client.send_message(message.channel, "**Usage: m!deleteroles @role (can be more than one)**"
                                               )


def setup(bot):
    bot.add_cog(DeleteRoles(bot))
    bot.loaded_exts['commands.deleteroles.deleteroles'] = "DeleteRoles"
    bot.cmds['deleteroles'] = ["Delete roles from the database.", "m!deleteroles @role (can be more than one)",
                               "manage_server"]
