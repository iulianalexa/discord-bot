import sqlite3

sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()
rolesdb = sqlite3.connect("roles.db")
rolescur = rolesdb.cursor()

class AddCorrelations():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def addcorrelations(self, command, message):
        if message.author.permissions_in(message.channel).manage_server:
            # role = message.role_mentions[0]
            roles = message.role_mentions
            mroles = [x.mention for x in roles]

            if command[1] in mroles and len(message.role_mentions) >= 2 and roles[mroles.index(command[1])].id in\
                    self.client.croles[message.server.id].keys():
                role = roles[mroles.index(command[1])]
                dbserv = "server" + message.server.id
                roles = message.role_mentions
                roles.remove(role)
                for i in roles:
                    if i.id in self.client.croles[message.server.id][role.id]:
                        continue
                    last = self.client.rids[message.server.id][role.id]
                    self.client.croles[message.server.id][role.id].append(i.id)
                    rolescur.execute("INSERT INTO " + dbserv + " (roleid, correlationid, rid) VALUES (?, ?, ?)",
                                     [role.id, i.id, last])
                    rolesdb.commit()
                await self.client.send_message(message.channel, "**Done!**")
            else:
                await self.client.send_message(message.channel,
                                               "**Usage: m!addcorrelations @role @correlations (can be more than one)**"
                                               )

def setup(bot):
    bot.add_cog(AddCorrelations(bot))
    bot.loaded_exts['commands.addcorrelations.addcorrelations'] = "AddCorrelations"
    bot.cmds['addcorrelations'] = ["Add a correlation to a role. Whenever this role is received by a player, "
                                   "the correlation will also be received.", "m!addcorrelations @role @correlations "
                                                                             "(can be more than one)", "manage_server"]
