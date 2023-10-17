import sqlite3

warndb = sqlite3.connect("warnings.db")
warncur = warndb.cursor()
sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()

class UnwarnSys():
    comm = False
    def __init__(self, bot):
        self.client = bot

    async def unwarn_sys(self, server, target, warnid):
        servdb = "server" + server.id
        warncur.execute("SELECT * FROM " + servdb + " WHERE userid=? AND rowid=?", [target.id, warnid])
        fornow = warncur.fetchall()
        if not fornow:
            return False
        else:
            warncur.execute("DELETE FROM " + servdb + " WHERE userid=? AND rowid=?", [target.id, warnid])
            warndb.commit()
            return True


def setup(bot):
    bot.add_cog(UnwarnSys(bot))
    bot.loaded_exts['mechanisms.unwarn_sys.unwarn_sys'] = 'UnwarnSys'
