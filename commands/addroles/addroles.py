import sqlite3
rolesdb = sqlite3.connect("roles.db")
rolescur = rolesdb.cursor()
sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()

class AddRoles():
    comm = True
    def __init__(self, bot):
        self.client = bot

    async def addroles(self, command, message):
        if message.author.permissions_in(message.channel).manage_server:
            if len(message.role_mentions) >= 1:
                dbserv = "server" + message.server.id
                for i in message.role_mentions:
                    if i.id not in self.client.croles[message.server.id].keys():
                        rolescur.execute("SELECT MAX(rowid) FROM " + dbserv)
                        last = rolescur.fetchone()
                        if last[0]:
                            last = last[0]
                        else:
                            last = 0
                        last += 1
                        self.client.rids[message.server.id][i.id] = str(last)
                        self.client.croles[message.server.id][i.id] = []
                        rolescur.execute("INSERT INTO " + dbserv + " (roleid, rid) VALUES (?, ?)",
                                         [i.id, str(last)])
                        rolesdb.commit()
                        await self.client.send_message(message.channel, "**Done!**")
                    else:
                        await self.client.send_message(message.channel, "**Role already exists in the database.**")
            else:
                await self.client.send_message(message.channel, "**Usage: m!addroles @role "
                                                                "(can mention more roles at a time)**")


def setup(bot):
    bot.add_cog(AddRoles(bot))
    bot.loaded_exts['commands.addroles.addroles'] = "AddRoles"
    bot.cmds['addroles'] = ["Add one or more roles that can be received by users who type out the m!role command.",
                            "m!addroles @role (can mention more roles at a time)", "manage_server"]