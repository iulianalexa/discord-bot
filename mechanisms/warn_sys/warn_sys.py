import datetime
import discord
import sqlite3

warndb = sqlite3.connect("warnings.db")
warncur = warndb.cursor()
sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()

class WarnSys():
    comm = False
    def __init__(self, bot):
        self.client = bot

    async def warn_sys(self, server, target):
        dbserv = "server" + server.id
        sinfocur.execute("SELECT * FROM warnexpire WHERE server = ?", [server.id])
        fornow = sinfocur.fetchall()[0][1]

        timestamp = datetime.datetime.now()
        timestamp1 = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        expiry = timestamp + datetime.timedelta(days=int(fornow))
        expiry1 = expiry.strftime('%Y-%m-%d %H:%M:%S')
        if int(fornow) == 0:
            expiry1 = "never"
            expiry = "never"

        warncur.execute("INSERT INTO " + dbserv + " (timestamp, userid, expiry) VALUES (?, ?, ?)",
                        [timestamp1, target.id, expiry1])
        warndb.commit()
        warncur.execute("SELECT rowid FROM " + dbserv + " WHERE userid = ? AND timestamp = ?", [target.id, timestamp1])
        fornow3 = warncur.fetchall()[0][0]

        warncur.execute("SELECT * FROM " + dbserv + " WHERE userid = ?", [target.id])
        sinfocur.execute("SELECT maxint FROM maxwarn WHERE server = ?", [server.id])
        if len(warncur.fetchall()) >= int(sinfocur.fetchall()[0][0]):
            try:
                await self.client.ban(target)
                warncur.execute("DELETE FROM " + dbserv + " WHERE userid=?", [target.id])
                warndb.commit()
            except discord.Forbidden:
                pass
        else:
            if expiry != "never":
                await self.client.get_cog("WarnScheduler").warn_scheduler(
                    server, target, expiry, fornow3)


def setup(bot):
    bot.add_cog(WarnSys(bot))
    bot.loaded_exts['mechanisms.warn_sys.warn_sys'] = 'WarnSys'
